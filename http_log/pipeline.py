import aiofiles
import asyncio
import time

from http_log import parsing
from http_log.alert import Alert
from http_log.sliding_time_window import SlidingTimeWindow
from http_log.stats import Stats


_ALERT_WINDOW_SIZE = 120
_STATS_WINDOW_SIZE = 10


def build_task(log_file_path: str, alert_threshold: int):
    alert_window = SlidingTimeWindow[int](_ALERT_WINDOW_SIZE, 0)
    stats_window = SlidingTimeWindow[Stats](_STATS_WINDOW_SIZE, Stats())
    alert = Alert(alert_window, alert_threshold)
    queue = asyncio.Queue()

    return asyncio.gather(
        _read(queue, log_file_path),
        _alerts(alert),
        _stats(stats_window),
        _process(queue, alert_window, stats_window)
    )


async def _read(queue, log_file_path: str) -> None:
    async with aiofiles.open(log_file_path, 'r') as f: # type: ignore
        await f.seek(0, 2)

        while True:
            lines = await f.readlines()

            if not lines:
                await asyncio.sleep(0.500)

                continue

            for line in lines:
                entry = parsing.parse_line(line)

                if not entry:
                    continue

                await queue.put(entry)


async def _process(queue, alert_window: SlidingTimeWindow, stats_window: SlidingTimeWindow) -> None:
    while True:
        entry = await queue.get()

        alert_window.add(entry.timestamp, 1)
        stats_window.add(
            entry.timestamp,
            Stats(
                total=1,
                codes={entry.status_code: 1},
                sections={entry.section: 1}
            )
        )

        queue.task_done()


async def _alerts(alert: Alert) -> None:
    while True:
        await asyncio.sleep(1)
        alert.run()


async def _stats(window: SlidingTimeWindow) -> None:
    while True:
        await asyncio.sleep(10)
        window.expire(int(time.time()))
        print(sorted(window.value.codes.items(), key=lambda x: -x[1]))

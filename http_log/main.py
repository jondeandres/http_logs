import asyncio
import aiofiles
import logging
import time


from http_log.alert import Alert
from http_log.sliding_time_window import SlidingTimeWindow
from http_log import parsing
from http_log.stats import Stats


log = logging.getLogger(__name__)


def bootstrap():
    asyncio.run(main())


async def main():
    logging.basicConfig(level='DEBUG')

    alert_window = SlidingTimeWindow(120, 0)
    stats_window = SlidingTimeWindow(10, Stats())
    alert = Alert(alert_window, 5)
    queue = asyncio.Queue()

    await asyncio.gather(
        read(queue),
        alerts(alert),
        stats(stats_window),
        process(queue, alert_window, stats_window)
    )


async def alerts(alert):
    while True:
        await asyncio.sleep(1)
        alert.run()


async def stats(window):
    while True:
        await asyncio.sleep(10)
        window.expire(time.time())
        print(sorted(window.value.codes.items(), key=lambda x: -x[1]))


async def read(queue):
    async with aiofiles.open('/home/jon/foo.log', 'r') as f:
        await f.seek(0, 2)

        while True:
            lines = await f.readlines()

            if not lines:
                await asyncio.sleep(0.500)

                continue

            for line in lines:
                await queue.put(parsing.parse_line(line))


async def process(queue, alert_window, stats_window):
    while True:
        entry = await queue.get()

        if not entry:
            continue

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
import argparse
import asyncio
import aiofiles
import logging
import time


from http_log.alert import Alert
from http_log.sliding_time_window import SlidingTimeWindow
from http_log import parsing
from http_log.stats import Stats


log = logging.getLogger(__name__)


_DEFAULT_THRESHOLD = 10
_DEFAULT_LOG_FILE_PATH = '/tmp/access.log'
_ALERT_WINDOW_SIZE = 120
_STATS_WINDOW_SIZE = 10


def bootstrap():
    parser = argparse.ArgumentParser()
    parser.add_argument('--threshold', default=_DEFAULT_THRESHOLD, type=int)
    parser.add_argument('--log-file-path', default=_DEFAULT_LOG_FILE_PATH)

    args = parser.parse_args()

    asyncio.run(main(args))


async def main(args: argparse.Namespace):
    logging.basicConfig(level='INFO')

    alert_window = SlidingTimeWindow(_ALERT_WINDOW_SIZE, 0)
    stats_window = SlidingTimeWindow(_STATS_WINDOW_SIZE, Stats())
    alert = Alert(alert_window, args.threshold)
    queue = asyncio.Queue()

    await asyncio.gather(
        read(queue, args.log_file_path),
        alerts(alert),
        stats(stats_window),
        process(queue, alert_window, stats_window)
    )

async def read(queue, log_file_path):
    async with aiofiles.open(log_file_path, 'r') as f:
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


async def alerts(alert):
    while True:
        await asyncio.sleep(1)
        alert.run()


async def stats(window):
    while True:
        await asyncio.sleep(10)
        window.expire(time.time())
        print(sorted(window.value.codes.items(), key=lambda x: -x[1]))

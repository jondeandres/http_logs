import asyncio
import aiofiles
import logging
import time


from http_log.alert_manager import AlertManager
from http_log.sliding_time_window import SlidingTimeWindow
from http_log import parsing
from http_log.processor import Processor
from http_log.stats import Stats


log = logging.getLogger(__name__)


def bootstrap():
    asyncio.run(main())


async def main():
    logging.basicConfig(level='DEBUG')

    alert_window = SlidingTimeWindow(120, 0)
    stats_window = SlidingTimeWindow(10, Stats())
    alert_manager = AlertManager(alert_window, 5)
    processor = Processor([alert_window, stats_window])

    await asyncio.gather(
        read(processor),
        alerts(alert_manager),
        stats(stats_window)
    )


async def alerts(alert_manager):
    while True:
        await asyncio.sleep(1)
        alert_manager.run()


async def stats(window):
    while True:
        await asyncio.sleep(10)
        window.expire(time.time())
        print(sorted(window.value.codes.items(), key=lambda x: -x[1]))


async def read(processor):
    async with aiofiles.open('/home/jon/foo.log', 'r') as f:
        while True:
            lines = await f.readlines()

            if not lines:
                await asyncio.sleep(0.500)

                continue

            processor.process(parsing.parse_line(line) for line in lines)

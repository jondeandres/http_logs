import argparse
import asyncio
import logging
import signal
import typing


from http_log import pipeline


log = logging.getLogger(__name__)


_DEFAULT_THRESHOLD = 10
_DEFAULT_LOG_FILE_PATH = '/tmp/access.log'


def bootstrap() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--threshold', default=_DEFAULT_THRESHOLD, type=int)
    parser.add_argument('--log-file-path', default=_DEFAULT_LOG_FILE_PATH)

    args = parser.parse_args()

    asyncio.run(main(args))


async def main(args: argparse.Namespace) -> None:
    logging.basicConfig(level='INFO')

    task = pipeline.build_pipeline_task(args.log_file_path, args.threshold)

    handler = signal_handler_factory(task)

    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)
    signal.signal(signal.SIGQUIT, handler)
    signal.signal(signal.SIGALRM, handler)

    try:
        await task
    except asyncio.CancelledError:
        pass


def signal_handler_factory(task):
    def signal_handler(*args, **kwargs) -> None:
        task.cancel()

    return signal_handler

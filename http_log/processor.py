import typing


from http_log.log_entry import LogEntry
from http_log.sliding_time_window import SlidingTimeWindow
from http_log.stats import Stats


class Processor:
    def __init__(self, windows: typing.List[SlidingTimeWindow]):
        self.__windows = windows

    def process(self, log_entries: typing.List[LogEntry]):
        stats = Stats()

        for entry in log_entries:
            if entry is None:
                continue

            stats = Stats(
                total=1,
                codes={entry.status_code: 1},
                sections={entry.section: 1}
            )

            for window in self.__windows:
                window.add(entry.timestamp, stats)

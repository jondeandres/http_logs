import logging
import time


from http_log.sliding_time_window import SlidingTimeWindow

log = logging.getLogger(__name__)


class Alert:
    # threshold is overridable
    def __init__(self, window: SlidingTimeWindow, threshold: int, logger: logging.Logger =log):
        self.__window = window
        self.__threshold = threshold
        self.__firing = False
        self.__logger = logger

    @property
    def firing(self) -> bool:
        return self.__firing

    @firing.setter
    def firing(self, value: bool) -> None:
        self.__firing = value

    def run(self) -> None:
        now = time.time()
        self.__window.expire(now)

        value = self.__window.value
        avg = value / self.__window.size

        if avg > self.__threshold:
            if not self.__firing:
                self.__logger.info("High traffic generated an alert - hits = %d, triggered at %d",
                                   value,
                                   now)
                self.__firing = True
        elif self.__firing:
            self.__firing = False

            self.__logger.info("High traffic alert is now inactive at %d", now)

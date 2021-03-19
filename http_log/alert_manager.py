import logging
import time


from http_log.sliding_window import SlidingWindow

log = logging.getLogger(__name__)


class AlertManager:
    # threshold is overridable
    def __init__(self, window: SlidingWindow, threshold: int, logger=log):
        self.__window = window
        self.__threshold = threshold
        self.__firing = False
        self.__logger = logger

    @property
    def firing(self):
        return self.__firing

    @firing.setter
    def firing(self, value):
        self.__firing = value

    def run(self):
        # mutex ?
        now = int(time.time())
        self.__window.expire(now)

        avg = self.__window.avg
        total = self.__window.total

        if avg > self.__threshold:
            if not self.__firing:
                self.__logger.info("High traffic generated an alert - hits = %d, triggered at %d",
                                   total,
                                   now)
                self.__firing = True
        elif self.__firing:
            self.__firing = False

            self.__logger.info("High traffic alert is now inactive at %d", now)

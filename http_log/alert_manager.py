import logging
import time


from http_log.sliding_time_window import SlidingTimeWindow

log = logging.getLogger(__name__)


class AlertManager:
    # threshold is overridable
    def __init__(self, window: SlidingTimeWindow, threshold: int, logger=log):
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
        now = int(time.time())
        self.__window.expire(now)

        agg = self.__window.agg.total
        avg = agg / self.__window.size

        if avg > self.__threshold:
            if not self.__firing:
                self.__logger.info("High traffic generated an alert - hits = %d, triggered at %d",
                                   agg,
                                   now)
                self.__firing = True
        elif self.__firing:
            self.__firing = False

            self.__logger.info("High traffic alert is now inactive at %d", now)

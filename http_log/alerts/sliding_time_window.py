class SlidingTimeWindow:
    def __init__(self, size: int) -> None:
        self.__size = size
        self.__total = 0
        self.__timestamps = []
        self.__values = []

    def add(self, timestamp: int, value: int) -> None:
        self.__timestamps.append(timestamp)
        self.__values.append(value)

        self.__total += value
        self.expire(timestamp)

    def expire(self, time_reference: int) -> None:
        if not self.__timestamps:
            return

        while self.__timestamps and self.__timestamps[0] <= time_reference - self.__size:
            self.__timestamps.pop(0)
            self.__total -= self.__values.pop(0)

    @property
    def total(self):
        return self.__total

    @property
    def avg(self) -> float:
        return self.__total / self.__size

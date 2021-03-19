import typing


class SlidingTimeWindow:
    def __init__(self, size: int, initial_agg: typing.Any = 0) -> None:
        self.__size = size
        self.__agg = initial_agg
        self.__refs = []
        self.__values = []

    def add(self, ref: int, value: int) -> None:
        self.__refs.append(ref)
        self.__values.append(value)

        self.__agg += value
        self.expire(ref)

    def expire(self, ref: int) -> None:
        if not self.__refs:
            return

        while self.__refs and self.__refs[0] <= ref - self.__size:
            self.__refs.pop(0)
            self.__agg -= self.__values.pop(0)

    @property
    def agg(self):
        return self.__agg

    @property
    def size(self):
        return self.__size

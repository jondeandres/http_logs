import typing

from http_log.stats import Stats
from http_log.lib.queue import Queue


T = typing.TypeVar('T')


class SlidingTimeWindow(typing.Generic[T]):
    def __init__(self, size: int, initial_value: typing.Any = 0) -> None:
        self.__size = size
        self.__value = initial_value
        self.__refs: Queue[int] = Queue[int]()
        self.__values: Queue[T] = Queue[T]()

    def add(self, ref: int, value: typing.Any) -> None:
        self.__refs.add(ref)
        self.__values.add(value)
        self.__value += value

        self.expire(ref)

    def expire(self, ref: float) -> None:
        while self.__refs and self.__refs.peek() <= ref - self.__size:
            self.__value -= self.__values.remove()
            self.__refs.remove()

    @property
    def value(self) -> typing.Any:
        return self.__value

    @property
    def size(self) -> int:
        return self.__size

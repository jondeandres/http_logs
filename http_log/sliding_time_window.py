import time
import typing

from http_log.stats import Stats
from http_log.lib.queue import Queue


T = typing.TypeVar('T')


class SlidingTimeWindow(typing.Generic[T]):
    """
    Implements a sliding time window algorithm keeping an accumulated
    value in its 'value' property.

    Previous timestamps and value entries are kept so we can decrease their
    values as new data is added or value is accessed.
    """

    def __init__(self, size: int, initial_value: typing.Any = 0) -> None:
        self.__size = size
        self.__value = initial_value
        self.__refs: Queue[int] = Queue[int]()
        self.__values: Queue[T] = Queue[T]()

    def add(self, ref: int, value: typing.Any) -> None:
        self.__refs.add(ref)
        self.__values.add(value)
        self.__value += value

        # We don't want to waste space so we call expire when adding data.
        self.__expire(ref)

    @property
    def value(self) -> typing.Any:
        # We call expire() before reading the accumulated value so
        # we remove old entries that might still exist in the queue.
        self.__expire(int(time.time()))

        return self.__value

    @property
    def size(self) -> int:
        return self.__size

    def __expire(self, ref: int) -> None:
        # Remove all old entries from the queues and decrement each
        # entry value from the accumulator
        while self.__refs and self.__refs.peek() <= ref - self.__size:
            self.__value -= self.__values.remove()
            self.__refs.remove()
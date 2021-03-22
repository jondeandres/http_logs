import typing

T = typing.TypeVar('T')


class EmptyQueueException(Exception):
    pass



class Node(typing.Generic[T]):
    def __init__(self, data: T):
        self.data: T = data
        self.next = None

    def __repr__(self) -> str:
        return f'<Node data={self.data}>'


class Queue(typing.Generic[T]):
    def __init__(self) -> None:
        self.head: typing.Optional[Node[T]] = None
        self.tail: typing.Optional[Node[T]] = None

    def __bool__(self):
        return self.head is not None

    def add(self, data: T) -> None:
        new_node = Node[T](data)

        if not self.head:
            self.head = new_node
            self.tail = new_node

            return

        self.tail.next = new_node
        self.tail = new_node

    def remove(self) -> T:
        if not self.head:
            raise EmptyQueueException()

        data = self.head.data
        self.head = self.head.next

        return data

    def peek(self) -> typing.Optional[T]:
        if not self.head:
            return None

        return self.head.data
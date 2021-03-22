from http_log.lib.queue import Queue


class TestQueue:
    def test_queue(self):
        ll = Queue()
        ll.add(1)
        ll.add(2)
        ll.add(3)

        assert ll.remove() == 1
        assert ll.remove() == 2
        assert ll.remove() == 3

        ll.add(4)
        ll.add(5)

        assert ll.peek() == 4
from http_log.sliding_time_window import SlidingTimeWindow


class TestSlidingTimeWindow:
    def test_total(self):
        window = SlidingTimeWindow(5)
        window.add(1, 1)
        window.add(2, 1)
        window.add(3, 1)
        window.add(4, 1)
        window.add(5, 2)

        assert window.total == 6

        window.add(6, 1)

        assert window.total == 6

        window.add(9, 1)

        assert window.total == 4

        window.add(20, 1)

        assert window.total == 1

    def test_get_average(self):
        window = SlidingTimeWindow(5)
        window.add(1, 10)
        window.add(2, 50)
        window.add(3, 20)
        window.add(4, 40)
        window.add(5, 15)

        assert window.avg == 27

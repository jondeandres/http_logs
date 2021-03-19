from http_log.alerts.sliding_time_window import SlidingTimeWindow


class TestSlidingTimeWindow:
    def test_agg(self):
        window = SlidingTimeWindow(5)
        window.add(1, 1)
        window.add(2, 1)
        window.add(3, 1)
        window.add(4, 1)
        window.add(5, 2)

        assert window.agg == 6

        window.add(6, 1)

        assert window.agg == 6

        window.add(9, 1)

        assert window.agg == 4

        window.add(20, 1)

        assert window.agg == 1

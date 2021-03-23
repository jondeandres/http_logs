import mock

from http_log.alert import Alert
from http_log.sliding_time_window import SlidingTimeWindow
from http_log.stats import Stats


class TestAlert:
    def test_run_when_no_firing_and_below_threshold(self):
        window = mock.Mock(spec=SlidingTimeWindow)
        window.value = 5
        window.size = 5
        logger = mock.Mock()
        threshold = 10

        manager = Alert(window, threshold, logger)
        manager.run()

        assert manager.firing is False

    @mock.patch('time.time')
    def test_run_when_no_firing_and_over_threshold(self, time):
        window = mock.Mock(spec=SlidingTimeWindow)
        window.value = 30
        window.size = 2
        logger = mock.Mock()
        threshold = 10
        time.return_value = 1616444723

        manager = Alert(window, threshold, logger)
        manager.run()

        assert manager.firing is True

        logger.info.assert_called_once_with("High traffic generated an alert - hits = %d, triggered at %s",
                                            30,
                                            '22/Mar/2021:21:25:23 +0100')

    @mock.patch('time.time')
    def test_run_when_firing_and_below_threshold(self, time):
        window = mock.Mock(spec=SlidingTimeWindow)
        window.value = 3
        window.size = 2
        logger = mock.Mock()
        threshold = 10
        time.return_value = 1616444723

        manager = Alert(window, threshold, logger)
        manager.firing = True
        manager.run()

        assert manager.firing is False

        logger.info.assert_called_once_with("High traffic alert is now inactive at %s", '22/Mar/2021:21:25:23 +0100')

    def test_run_when_firing_and_over_threshold(self):
        window = mock.Mock(spec=SlidingTimeWindow)
        window.value = 30
        window.size = 2
        logger = mock.Mock()
        threshold = 10

        manager = Alert(window, threshold, logger)
        manager.firing = True
        manager.run()

        assert manager.firing is True

        logger.info.assert_not_called()

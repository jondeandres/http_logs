import mock

from http_log.alert_manager import AlertManager
from http_log.sliding_time_window import SlidingTimeWindow
from http_log.stats import Stats


class TestAlertManager:
    @mock.patch('time.time')
    def test_run_expires_window(self, time):
        time.return_value = 100
        window = mock.Mock(spec=SlidingTimeWindow)
        window.agg = mock.Mock(spec=Stats, total=5)
        window.size = 5
        logger = mock.Mock()
        threshold = 10

        manager = AlertManager(window, threshold, logger)
        manager.run()

        window.expire.assert_called_once_with(100)

    def test_run_when_no_firing_and_below_threshold(self):
        window = mock.Mock(spec=SlidingTimeWindow)
        window.agg = mock.Mock(spec=Stats, total=5)
        window.size = 5
        logger = mock.Mock()
        threshold = 10

        manager = AlertManager(window, threshold, logger)
        manager.run()

        assert manager.firing is False

    @mock.patch('time.time')
    def test_run_when_no_firing_and_over_threshold(self, time):
        window = mock.Mock(spec=SlidingTimeWindow)
        window.agg = mock.Mock(spec=Stats, total=30)
        window.size = 2
        logger = mock.Mock()
        threshold = 10
        time.return_value = 123

        manager = AlertManager(window, threshold, logger)
        manager.run()

        assert manager.firing is True

        logger.info.assert_called_once_with("High traffic generated an alert - hits = %d, triggered at %d",
                                            30,
                                            123)

    @mock.patch('time.time')
    def test_run_when_firing_and_below_threshold(self, time):
        window = mock.Mock(spec=SlidingTimeWindow)
        window.agg = mock.Mock(spec=Stats, total=3)
        window.size = 2
        logger = mock.Mock()
        threshold = 10
        time.return_value = 123

        manager = AlertManager(window, threshold, logger)
        manager.firing = True
        manager.run()

        assert manager.firing is False

        logger.info.assert_called_once_with("High traffic alert is now inactive at %d", 123)

    def test_run_when_firing_and_over_threshold(self):
        window = mock.Mock(spec=SlidingTimeWindow)
        window.agg = mock.Mock(spec=Stats, total=30)
        window.size = 2
        logger = mock.Mock()
        threshold = 10

        manager = AlertManager(window, threshold, logger)
        manager.firing = True
        manager.run()

        assert manager.firing is True

        logger.info.assert_not_called()

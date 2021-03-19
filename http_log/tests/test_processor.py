import mock


from http_log.log_entry import LogEntry
from http_log.processor import Processor
from http_log.sliding_time_window import SlidingTimeWindow


class TestStats:
    def test_process(self):
        window = mock.Mock(spec=SlidingTimeWindow)
        processor = Processor([window])

        entries = [
            LogEntry(
                client='client',
                identity='identity',
                userid='userid',
                datetime='10/Oct/2020:13:55:36 -0700',
                method='GET',
                path='/apm/traces',
                protocol='HTTP/1.0',
                status_code=200,
                content_length=45
            ),
            LogEntry(
                client='client',
                identity='identity',
                userid='userid',
                datetime='10/Oct/2020:13:55:37 -0700',
                method='GET',
                path='/apm/home',
                protocol='HTTP/1.0',
                status_code=500,
                content_length=45
            ),
        ]

        processor.process(entries)

        calls = window.add.call_args_list

        assert calls[0].args[0] == 1602363336
        assert calls[0].args[1].total == 1
        assert calls[0].args[1].sections == {'/apm': 1}
        assert calls[0].args[1].codes == {200: 1}

        assert calls[1].args[0] == 1602363337
        assert calls[1].args[1].total == 1
        assert calls[1].args[1].sections == {'/apm': 1}
        assert calls[1].args[1].codes == {500: 1}

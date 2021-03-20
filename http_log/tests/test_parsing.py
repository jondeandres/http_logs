from http_log import parsing
from http_log.log_entry import LogEntry


class TestParsing:
    def test_parse_line(self):
        line = '127.0.0.1 user-identifier frank [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326'

        log_entry = parsing.parse_line(line)

        assert log_entry == LogEntry(
            client='127.0.0.1',
            identity='user-identifier',
            userid='frank',
            datetime='10/Oct/2000:13:55:36 -0700',
            method='GET',
            path='/apache_pb.gif',
            protocol='HTTP/1.0',
            status_code=200,
            content_length=2326
        )

    def test_parse_line_on_incorrect_line(self):
        assert parsing.parse_line('foo bar') is None

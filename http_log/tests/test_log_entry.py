from http_log.log_entry import LogEntry


class TestLogEntry:
    def setup_method(self):
        self.entry = LogEntry(
            client='client',
            identity='identity',
            userid='userid',
            datetime='10/Oct/2020:13:55:36 -0700',
            method='GET',
            path='/apm/traces',
            protocol='HTTP/1.0',
            status_code=200,
            content_length=45
        )

    def test_timestamp(self):
        assert self.entry.timestamp == 1602363336

    def test_section(self):
        assert self.entry.section == '/apm'

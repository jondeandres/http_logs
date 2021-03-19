from dataclasses import dataclass
from datetime import datetime
import re


_TIMESTAMP_FORMAT = '%d/%b/%Y:%H:%M:%S %z'
_SECTION_REGEX = re.compile(r'(^/[^/]+)/([^/]+)')


@dataclass
class LogEntry:
    client: str
    identity: str
    userid: str
    datetime: str
    method: str
    path: str
    protocol: str
    status_code: int
    content_length: int

    @property
    def timestamp(self) -> int:
        return int(datetime.strptime(self.datetime, _TIMESTAMP_FORMAT).timestamp())

    @property
    def section(self):
        return _SECTION_REGEX.match(self.path)[1]

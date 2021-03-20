import re
import typing

from http_log.log_entry import LogEntry

_COMMON_LOG_REGEX = re.compile(r'^(\S+) (\S+) (\S+) \[([\w:/]+\s[+\-]\d{4})\] "(\S+) (.+?) (\S+)" (\d{3}) (\S+)')


def parse_line(line: str) -> typing.Optional[LogEntry]:
    if not line:
        return None

    match = _COMMON_LOG_REGEX.match(line)

    if not match:
        return None

    groups = match.groups()

    return LogEntry(
        client=groups[0],
        identity=groups[1],
        userid=groups[2],
        datetime=groups[3],
        method=groups[4],
        path=groups[5],
        protocol=groups[6],
        status_code=int(groups[7]),
        content_length=int(groups[8])
    )
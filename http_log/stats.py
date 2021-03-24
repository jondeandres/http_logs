from copy import copy
from dataclasses import dataclass, field
import logging

import typing
import collections

log = logging.getLogger(__name__)


@dataclass
class Stats:
    codes: typing.Dict[int, int] = field(default_factory=lambda: collections.defaultdict(int))
    sections: typing.Dict[str, int] = field(default_factory=lambda: collections.defaultdict(int))
    total: int = 0

    def __copy__(self) -> 'Stats':
        return Stats(total=self.total,
                     codes=copy(self.codes),
                     sections=copy(self.sections))

    def __add__(self, other: 'Stats') -> 'Stats':
        stats = copy(self)

        stats.total += other.total

        for code, hits in other.codes.items():
            stats.codes[code] += hits

        for section, hits in other.sections.items():
            stats.sections[section] += hits

        return stats

    def __sub__(self, other: 'Stats') -> 'Stats':
        stats = copy(self)
        stats.total -= other.total

        for code, hits in other.codes.items():
            stats.codes[code] -= hits

        for section, hits in other.sections.items():
            stats.sections[section] -= hits

        return stats


def render(stats: Stats):
    top_sections = sorted(
            stats.sections.items(),
            key=lambda x: -x[1]
    )[:5]

    top_codes = sorted(
            stats.codes.items(),
            key=lambda x: -x[1]
    )[:5]

    msg = f'\nTotal requests: {stats.total}\n'
    msg += '\nTop sections:\n'

    for section in top_sections:
        msg += f'{section[0]}: {section[1]} requests\n'

    msg += '\nTop status codes:\n'

    for code in top_codes:
        msg += f'{code[0]}: {code[1]} requests\n'

    msg += '\n'

    log.info(msg)

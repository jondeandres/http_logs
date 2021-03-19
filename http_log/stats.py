from dataclasses import dataclass, field
from copy import copy

import typing
import collections


@dataclass
class Stats:
    codes: typing.Dict[int, int] = field(default_factory=lambda: collections.defaultdict(int))
    sections: typing.Dict[str, int] = field(default_factory=lambda: collections.defaultdict(int))
    total: int = 0

    def __copy__(self):
        return Stats(total=self.total,
                     codes=copy(self.codes),
                     sections=copy(self.sections))

    def __add__(self, other) -> 'Stats':
        stats = copy(self)

        stats.total += other.total

        for code, hits in other.codes.items():
            stats.codes[code] += hits

        for section, hits in other.sections.items():
            stats.sections[section] += hits

        return stats

    def __sub__(self, other) -> 'Stats':
        stats = copy(self)
        stats.total -= other.total

        for code, hits in other.codes.items():
            stats.codes[code] -= hits

        for section, hits in other.sections.items():
            stats.sections[section] -= hits

        return stats

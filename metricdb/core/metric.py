
# -*- coding: UTF-8 -*-


from dataclasses import dataclass, field
from typing import Any

from .identifier import Identifier, split_identifier
from .time import Time



class MetricId(str):

    SEPARATOR = "::"

    def __new__(cls, *keys):
        _keys = [id for k in keys for id in split_identifier(str(k))]
        return str.__new__(cls, cls.SEPARATOR.join(_keys))
    
    def keys(self):
        return self.split(self.SEPARATOR)



class MetricIdPattern(MetricId):
    def __new__(cls, *keys):
        if not keys:
            keys = ["*"]
        _keys = [id for k in keys for id in split_identifier(str(k), charset=(Identifier.CHARSET + "*"))]
        return str.__new__(cls, cls.SEPARATOR.join(_keys))



@dataclass
class MetricInfo:
    id              : MetricId
    name            : str                   = ""
    description     : str                   = ""

    def __post_init__(self):
        self.id = MetricId(self.id)
        self.name = str(self.name)
        self.description = str(self.description)


@dataclass
class MetricEntry:
    time            : Time                  = field(default_factory=Time)
    duration        : float                 = 0.0
    value           : Any                   = None

    def __post_init__(self):
        self.time = Time(self.time)
        if self.duration < 0:
            raise ValueError(f"Negative duration: {self.duration}")
        self.duration = float(self.duration)


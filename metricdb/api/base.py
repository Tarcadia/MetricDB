
# -*- coding: UTF-8 -*-


from typing import Optional, Generic, TypeVar
from typing import Set
from dataclasses import asdict

from pydantic import BaseModel

from ..core import Time
from ..core import TestId, DutId
from ..core import MetricKey, MetricInfo, MetricEntry
from ..core import MetricDB



_C = TypeVar('cls')

def _CoreMixin(cls):
    class _CoreMixin:

        def tocore(self, **kwargs) -> _C:
            return cls(**kwargs, **self.model_dump())

        @classmethod
        def fromcore(cls, obj, **kwargs):
            return cls(**kwargs, **asdict(obj))

    return _CoreMixin


class KeyRequest(BaseModel):
    key             : str


class TestRequest(BaseModel):
    test            : Optional[str]         = None


class DutRequest(BaseModel):
    dut             : Optional[Set[str]]    = None


class TimeRequest(BaseModel):
    start_time      : Optional[float]       = None
    end_time        : Optional[float]       = None


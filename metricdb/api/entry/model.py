
# -*- coding: UTF-8 -*-


from typing import Optional, Union
from typing import List, Dict, Set
from dataclasses import dataclass, asdict

from pydantic import BaseModel

from ..base import *
from ..base import _CoreMixin



class MetricEntryResp(BaseModel, _CoreMixin(MetricEntry)):
    time            : int
    duration        : int
    value           : Union[str, int, float]


class MetricEntryAdd(BaseModel, _CoreMixin(MetricEntry)):
    time            : int
    duration        : Optional[int]         = 0.0
    value           : Optional[Union[str, int, float]] = None


class KeyTestDutMetricEntryAdd(BaseModel):
    key             : str
    test            : Optional[str]         = None
    dut             : Optional[Set[str]]    = None
    entry           : MetricEntryAdd



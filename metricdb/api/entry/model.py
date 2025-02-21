
# -*- coding: UTF-8 -*-


from typing import Optional, Union
from typing import List, Dict, Set
from dataclasses import dataclass, asdict

from pydantic import BaseModel

from ..base import *
from ..base import _CoreMixin



class Entry(BaseModel, _CoreMixin(MetricEntry)):
    time            : float
    duration        : float                 = 0.0
    value           : Optional[Union[str, int, float, Dict]] = None


class MetricEntryResp(Entry, BaseModel, _CoreMixin(MetricEntry)):
    pass


class MetricEntryQuery(DutRequest, TimeRequest, BaseModel):
    pass


class TestMetricEntryQuery(TestRequest, MetricEntryQuery, BaseModel):
    pass


class TestKeyMetricEntryQuery(TestRequest, KeyRequest, MetricEntryQuery, BaseModel):
    pass


class MetricEntryAdd(DutRequest, BaseModel):
    entry: Entry


class TestMetricEntryAdd(TestRequest, MetricEntryAdd, BaseModel):
    pass


class TestKeyMetricEntryAdd(TestRequest, KeyRequest, MetricEntryAdd, BaseModel):
    pass



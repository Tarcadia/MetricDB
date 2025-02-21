
# -*- coding: UTF-8 -*-


from typing import Optional

from pydantic import BaseModel

from ..base import *
from ..base import _CoreMixin



class MetricInfoResp(BaseModel, _CoreMixin(MetricInfo)):
    key             : str
    name            : str
    description     : str


class MetricInfoUpdate(BaseModel, _CoreMixin(MetricInfo)):
    name            : str
    description     : str


class KeyMetricInfoUpdate(BaseModel, _CoreMixin(MetricInfo)):
    key             : str
    name            : str
    description     : str



# -*- coding: UTF-8 -*-


from ..core import MetricDB

from .base import *
from .base import _MdbClient


class MdbLocalClient(_MdbClient):

    def __init__(self, mdb: MetricDB):
        self.mdb = mdb


    def list_metric_info(
        self
    ) -> List[MetricInfo]:
        return self.mdb.list_metric_info()


    def query_metric_info(
        self,
        key: MetricKey
    ) -> MetricInfo:
        return self.mdb.query_metric_info(key)


    def update_metric_info(
        self,
        info: MetricInfo
    ) -> MetricInfo:
        self.mdb.update_metric_info(info)
        return info


    async def async_update_metric_info(
        self,
        info: MetricInfo
    ) -> MetricInfo:
        self.mdb.update_metric_info(info)
        return info


    def query_metric_entry(
        self,
        key: str,
        test: Optional[TestId] = None,
        dut: Union[DutId, Set[DutId], None] = None,
        start_time: Optional[Time] = None,
        end_time: Optional[Time] = None,
    ) -> List[MetricEntry]:
        return self.mdb.query_metric_entry(key, test, dut, start_time, end_time)


    def add_metric_entry(
        self,
        key: MetricKey,
        entry: MetricEntry,
        test: Optional[TestId] = None,
        dut: Union[DutId, Set[DutId], None] = None,
    ) -> MetricEntry:
        self.mdb.add_metric_entry(key, entry, test, dut)
        return entry


    async def async_add_metric_entry(
        self,
        key: MetricKey,
        entry: MetricEntry,
        test: Optional[TestId] = None,
        dut: Union[DutId, Set[DutId], None] = None,
    ) -> MetricEntry:
        self.mdb.add_metric_entry(key, entry, test, dut)
        return entry



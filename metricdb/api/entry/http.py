
# -*- coding: UTF-8 -*-


from typing import List

from fastapi import APIRouter
from fastapi import Query

from .model import *



def MetricEntryHttpRouter(mdb: MetricDB) -> APIRouter:

    router = APIRouter()


    @router.get("/metric/entry")
    @router.get("/metric/entry/{key}")
    @router.get("/metric/entry/{test}/{key}")
    def query_metric_entry(
        key: str,
        test: Optional[str] = None,
        dut: Optional[Set[str]] = Query(None),
        start_time: Optional[int] = None,
        end_time: Optional[int] = None
    ) -> List[MetricEntryResp]:
        key = key
        test = test and TestId(test)
        dut = dut and {DutId(d) for d in dut}
        start_time = start_time and Time(start_time)
        end_time = end_time and Time(end_time)
        response = [
            MetricEntryResp.fromcore(entry)
            for entry in mdb.query_metric_entry(
                key, test, dut, start_time, end_time
            )
        ]
        return response


    @router.post("/metric/entry")
    @router.post("/metric/entry/{key}")
    @router.post("/metric/entry/{test}/{key}")
    def add_metric_entry(
        key: str,
        test: Optional[str] = None,
        dut: Optional[Set[str]] = Query(None),
        request: MetricEntryAdd = None
    ) -> MetricEntryResp:
        key = MetricKey(key)
        test = test and TestId(test)
        dut = dut and {DutId(d) for d in dut}
        entry = request.tocore()
        mdb.add_metric_entry(key, entry, test, dut)
        response = MetricEntryResp.fromcore(entry)
        return response


    return router



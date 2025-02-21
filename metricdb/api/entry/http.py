
# -*- coding: UTF-8 -*-


from typing import List

from fastapi import APIRouter

from .model import *



def MetricEntryHttpRouter(mdb: MetricDB) -> APIRouter:

    router = APIRouter()


    @router.get("/metric/entry", response_model=List[MetricEntryResp])
    def query_metric_entry(request: TestKeyMetricEntryQuery):
        key = MetricKey(request.key)
        test = request.test and TestId(request.test)
        dut = request.dut and {DutId(d) for d in request.dut}
        start_time = request.start_time and Time(request.start_time)
        end_time = request.end_time and Time(request.end_time)
        response = [
            MetricEntryResp.fromcore(metric_entry)
            for metric_entry in mdb.query_metric_entry(
                key, test, dut, start_time, end_time
            )
        ]
        return response


    @router.get("/metric/entry/{key}", response_model=List[MetricEntryResp])
    def query_metric_entry(key: str, request: TestMetricEntryQuery):
        key = MetricKey(key)
        test = request.test and TestId(request.test)
        dut = request.dut and {DutId(d) for d in request.dut}
        start_time = request.start_time and Time(request.start_time)
        end_time = request.end_time and Time(request.end_time)
        response = [
            MetricEntryResp.fromcore(metric_entry)
            for metric_entry in mdb.query_metric_entry(
                key, test, dut, start_time, end_time
            )
        ]
        return response


    @router.get("/metric/entry/{test}/{key}", response_model=List[MetricEntryResp])
    def query_metric_entry(test: str, key: str, request: MetricEntryQuery):
        key = MetricKey(key)
        test = TestId(test)
        dut = request.dut and {DutId(d) for d in request.dut}
        start_time = request.start_time and Time(request.start_time)
        end_time = request.end_time and Time(request.end_time)
        response = [
            MetricEntryResp.fromcore(metric_entry)
            for metric_entry in mdb.query_metric_entry(
                key, test, dut, start_time, end_time
            )
        ]
        response = [
            MetricEntryResp.fromcore(metric_entry)
            for metric_entry in mdb.query_metric_entry(
                key, test, request.dut, request.start_time, request.end_time
            )
        ]
        return response


    @router.post("/metric/entry", response_model=MetricEntryResp)
    def add_metric_entry(request: TestKeyMetricEntryAdd):
        key = MetricKey(request.key)
        test = request.test and TestId(request.test)
        dut = request.dut and {DutId(d) for d in request.dut}
        metric_entry = request.entry.tocore()
        mdb.add_metric_entry(key, metric_entry, test, dut)
        response = MetricEntryResp.fromcore(metric_entry)
        return response


    @router.post("/metric/entry/{key}", response_model=MetricEntryResp)
    def add_metric_entry(key: str, request: TestMetricEntryAdd):
        key = MetricKey(key)
        test = request.test and TestId(request.test)
        dut = request.dut and {DutId(d) for d in request.dut}
        metric_entry = request.entry.tocore()
        mdb.add_metric_entry(key, metric_entry, test, dut)
        response = MetricEntryResp.fromcore(metric_entry)
        return response


    @router.post("/metric/entry/{test}/{key}", response_model=MetricEntryResp)
    def add_metric_entry(test: str, key: str, request: MetricEntryAdd):
        key = MetricKey(key)
        test = TestId(test)
        dut = request.dut and {DutId(d) for d in request.dut}
        metric_entry = request.entry.tocore()
        mdb.add_metric_entry(key, metric_entry, test, dut)
        response = MetricEntryResp.fromcore(metric_entry)
        return response


    return router



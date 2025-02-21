
# -*- coding: UTF-8 -*-


from fastapi import APIRouter
from fastapi import WebSocket, WebSocketDisconnect

from .model import *



def MetricEntryWsRouter(mdb: MetricDB) -> APIRouter:

    router = APIRouter()


    @router.websocket("/metric/entry")
    async def add_metric_entry(websocket: WebSocket):
        await websocket.accept()
        try:
            while True:
                request = TestKeyMetricEntryAdd(**await websocket.receive_json())
                key = MetricKey(request.key)
                test = request.test and TestId(request.test)
                dut = request.dut and {DutId(d) for d in request.dut}
                metric_entry = request.entry.tocore()
                mdb.add_metric_entry(key, metric_entry, test, dut)
        except WebSocketDisconnect:
            pass


    @router.websocket("/metric/entry/{key}")
    async def add_metric_entry(websocket: WebSocket, key: str):
        await websocket.accept()
        try:
            while True:
                request = TestMetricEntryAdd(**await websocket.receive_json())
                key = MetricKey(key)
                test = request.test and TestId(request.test)
                dut = request.dut and {DutId(d) for d in request.dut}
                metric_entry = request.entry.tocore()
                mdb.add_metric_entry(key, metric_entry, test, dut)
        except WebSocketDisconnect:
            pass


    @router.websocket("/metric/entry/{test}/{key}")
    async def add_metric_entry(websocket: WebSocket, test: str, key: str):
        await websocket.accept()
        try:
            while True:
                request = MetricEntryAdd(**await websocket.receive_json())
                key = MetricKey(key)
                test = TestId(test)
                dut = request.dut and {DutId(d) for d in request.dut}
                metric_entry = request.entry.tocore()
                mdb.add_metric_entry(key, metric_entry, test, dut)
        except WebSocketDisconnect:
            pass


    return router



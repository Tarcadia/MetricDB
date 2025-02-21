
# -*- coding: UTF-8 -*-


from fastapi import APIRouter
from fastapi import Query
from fastapi import WebSocket, WebSocketDisconnect

from .model import *



def MetricEntryWsRouter(mdb: MetricDB) -> APIRouter:

    router = APIRouter()


    @router.websocket("/metric/entry")
    async def add_metric_entry(websocket: WebSocket,) -> None:
        await websocket.accept()
        try:
            while True:
                request = KeyTestDutMetricEntryAdd(**await websocket.receive_json())
                key = MetricKey(request.key)
                test = test and TestId(request.test)
                dut = dut and {DutId(d) for d in request.dut}
                entry = request.entry.tocore()
                mdb.add_metric_entry(key, entry, test, dut)
        except WebSocketDisconnect:
            pass


    return router



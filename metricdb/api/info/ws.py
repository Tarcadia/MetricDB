
# -*- coding: UTF-8 -*-


from fastapi import APIRouter
from fastapi import WebSocket, WebSocketDisconnect

from .model import *



def MetricInfoWsRouter(mdb: MetricDB) -> APIRouter:

    router = APIRouter()


    @router.websocket("/metric/info")
    async def update_metric_info(websocket: WebSocket):
        await websocket.accept()
        try:
            while True:
                request = KeyMetricInfoUpdate(**await websocket.receive_json())
                metric_info = request.tocore()
                mdb.update_metric_info(metric_info)
        except WebSocketDisconnect:
            pass


    @router.websocket("/metric/info/{key}")
    async def update_metric_info(websocket: WebSocket, key: str):
        key = MetricKey(key)
        await websocket.accept()
        try:
            while True:
                request = MetricInfoUpdate(**await websocket.receive_json())
                metric_info = request.tocore(key=key)
                mdb.update_metric_info(metric_info)
        except WebSocketDisconnect:
            pass


    return router

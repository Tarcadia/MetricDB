
# -*- coding: UTF-8 -*-


from fastapi import APIRouter
from fastapi import WebSocket, WebSocketDisconnect

from .model import *



def MetricInfoWsRouter(mdb: MetricDB) -> APIRouter:

    router = APIRouter()


    @router.websocket("/metric/info")
    async def update_metric_info(websocket: WebSocket) -> None:
        await websocket.accept()
        try:
            while True:
                request = KeyMetricInfoUpdate(**await websocket.receive_json())
                info = request.tocore()
                mdb.update_metric_info(info)
        except WebSocketDisconnect:
            pass


    return router



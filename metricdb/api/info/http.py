
# -*- coding: UTF-8 -*-


from typing import List

from fastapi import APIRouter

from .model import *



def MetricInfoHttpRouter(mdb: MetricDB) -> APIRouter:

    router = APIRouter()


    @router.get("/metric/infos", response_model=List[MetricInfoResp])
    def list_metric_info() -> List[MetricInfoResp]:
        response = [
            MetricInfoResp.fromcore(metric_info)
            for metric_info in mdb.list_metric_info()
        ]
        return response


    @router.get("/metric/info", response_model=MetricInfoResp)
    def query_metric_info(key: str) -> MetricInfoResp:
        key = MetricKey(key)
        response = MetricInfoResp.fromcore(mdb.query_metric_info(key))
        return response


    @router.get("/metric/info/{key}", response_model=MetricInfoResp)
    def query_metric_info(key: str) -> MetricInfoResp:
        key = MetricKey(key)
        response = MetricInfoResp.fromcore(mdb.query_metric_info(key))
        return response


    @router.post("/metric/info", response_model=MetricInfoResp)
    def update_metric_info(request: KeyMetricInfoUpdate):
        metric_info = request.tocore()
        mdb.update_metric_info(metric_info)
        response = MetricInfoResp.fromcore(metric_info)
        return response


    @router.post("/metric/info/{key}", response_model=MetricInfoResp)
    def update_metric_info(key: str, request: MetricInfoUpdate):
        key = MetricKey(key)
        metric_info = request.tocore(key=key)
        mdb.update_metric_info(metric_info)
        response = MetricInfoResp.fromcore(metric_info)
        return response


    return router


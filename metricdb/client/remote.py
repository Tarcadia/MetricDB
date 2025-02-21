
# -*- coding: UTF-8 -*-


import json
import asyncio

import httpx
import websockets

from .base import *
from .base import _MdbClient



async def _aiterator(iterable: Iterator) -> AsyncIterator:
    for item in iterable:
        yield item


class MdbRemoteClient(_MdbClient):

    def __init__(
        self,
        base_url: str = "http://localhost:8000/api/v1",
        base_ws_url: str = None,
    ):
        self.base_http_url = base_url.rstrip("/")
        self.base_ws_url = base_ws_url or self.base_http_url.replace("http", "ws", 1).replace("/api", "/wsapi")
        self.http = httpx.Client(base_url=self.base_http_url)
        self.ahttp = httpx.AsyncClient(base_url=self.base_http_url)


    def list_metric_info(
        self
    ) -> List[MetricInfo]:
        response = self.http.get("/metric/infos")
        response.raise_for_status()
        return [MetricInfo(**item) for item in response.json()]


    def query_metric_info(
        self,
        key: MetricKey
    ) -> MetricInfo:
        response = self.http.get(
            "/metric/info",
            params=Query(key),
        )
        response.raise_for_status()
        return MetricInfo(**response.json())


    def update_metric_info(
        self,
        info: MetricInfo
    ) -> MetricInfo:
        response = self.http.post(
            "/metric/info",
            params=Query(info.key),
            json=MetricInfoUpdate(info),
        )
        response.raise_for_status()
        return MetricInfo(**response.json())


    async def async_update_metric_info(
        self,
        info: MetricInfo
    ) -> MetricInfo:
        response = await self.ahttp.post(
            "/metric/info",
            params=Query(info.key),
            json=MetricInfoUpdate(info),
        )
        response.raise_for_status()
        return MetricInfo(**response.json())


    def query_metric_entry(
        self,
        key: str,
        test: Optional[TestId] = None,
        dut: Optional[Union[DutId, Set[DutId]]] = None,
        start_time: Optional[Time] = None,
        end_time: Optional[Time] = None,
    ) -> List[MetricEntry]:
        response = self.http.get(
            "/metric/entry",
            params=Query(key, test, dut, start_time, end_time),
        )
        response.raise_for_status()
        return [MetricEntry(**item) for item in response.json()]


    def add_metric_entry(
        self,
        key: MetricKey,
        entry: MetricEntry,
        test: Optional[TestId] = None,
        dut: Optional[Union[DutId, Set[DutId]]] = None,
    ) -> MetricEntry:
        response = self.http.post(
            "/metric/entry",
            params=Query(key, test, dut),
            json=MetricEntryAdd(entry),
        )
        response.raise_for_status()
        return MetricEntry(**response.json())


    async def async_add_metric_entry(
        self,
        key: MetricKey,
        entry: MetricEntry,
        test: Optional[TestId] = None,
        dut: Optional[Union[DutId, Set[DutId]]] = None,
    ) -> MetricEntry:
        response = await self.async_http.post(
            "/metric/entry",
            params=Query(key, test, dut),
            json=MetricEntryAdd(entry),
        )
        response.raise_for_status()
        return MetricEntry(**response.json())


    def batch_update_metric_info(
        self,
        infos: Iterator[MetricInfo]
    ) -> List[MetricInfo]:
        return asyncio.run(
            self.abatch_update_metric_info(_aiterator(infos))
        )


    async def abatch_update_metric_info(
        self,
        infos: AsyncIterator[MetricInfo]
    ) -> List[MetricInfo]:
        response = []
        async with websockets.connect(self.base_ws_url + "/metric/info") as conn:
            async for info in infos:
                request = KeyMetricInfoUpdate(info)
                await conn.send(json.dumps(request))
                response.append(info)
        return response


    def batch_add_metric_entry(
        self,
        key: MetricKey,
        entries: Iterator[MetricEntry],
        test: Optional[TestId] = None,
        dut: Optional[Union[DutId, Set[DutId]]] = None,
    ) -> List[MetricEntry]:
        return asyncio.run(
            self.abatch_add_metric_entry(key, _aiterator(entries), test, dut)
        )


    async def abatch_add_metric_entry(
        self,
        key: MetricKey,
        entries: AsyncIterator[MetricEntry],
        test: Optional[TestId] = None,
        dut: Optional[Union[DutId, Set[DutId]]] = None,
    ) -> List[MetricEntry]:
        response = []
        async with websockets.connect(self.base_ws_url + f"/metric/entry") as conn:
            async for entry in entries:
                request = KeyTestDutMetricEntryAdd(key, entry, test, dut)
                await conn.send(json.dumps(request))
                response.append(entry)
        return response



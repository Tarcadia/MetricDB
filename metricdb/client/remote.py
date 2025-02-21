
# -*- coding: UTF-8 -*-


import json
import asyncio

import httpx
import websockets

from .base import *
from .base import _MdbClient



def _no_none(d: Dict[str, Any]) -> Dict[str, Any]:
    return {
        k: _no_none(v)
        if isinstance(v, dict)
        else v
        for k, v in d.items()
        if v is not None
    }

async def _aiterator(iterable: Iterator) -> AsyncIterator:
    for item in iterable:
        yield item


def MetricInfoQuerty(key: str) -> Dict[str, Any]:
    return _no_none({
        "key": str(key),
    })

def MetricInfoUpdate(info: MetricInfo) -> Dict[str, Any]:
    return _no_none({
        "key": str(info.key),
        "name": info.name,
        "description": info.description,
    })

def MetricEntryQuerty(
    key: str,
    test: Optional[TestId] = None,
    dut: Union[DutId, Set[DutId], None] = None,
    start_time: Optional[Time] = None,
    end_time: Optional[Time] = None,
) -> Dict[str, Any]:
    return _no_none({
        "key": str(key),
        "test": test and str(test),
        "dut": dut and {DutId(d) for d in dut},
        "start_time": start_time and float(start_time),
        "end_time": end_time and float(end_time),
    })


def MetricEntryAdd(
    key: MetricKey,
    entry: MetricEntry,
    test: Optional[TestId] = None,
    dut: Union[DutId, Set[DutId], None] = None,
) -> Dict[str, Any]:
    return _no_none({
        "key": str(key),
        "test": test and str(test),
        "dut": dut and {DutId(d) for d in dut},
        "entry": {
            "time": int(entry.time),
            "duration": int(entry.duration),
            "value": entry.value,
        },
    })



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
        key = str(key)
        response = self.http.get(
            "/metric/info",
            params=MetricInfoQuerty(key),
        )
        response.raise_for_status()
        return MetricInfo(**response.json())


    def update_metric_info(
        self,
        info: MetricInfo
    ) -> MetricInfo:
        response = self.http.post(
            "/metric/info",
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
            json=MetricInfoUpdate(info),
        )
        response.raise_for_status()
        return MetricInfo(**response.json())


    def query_metric_entry(
        self,
        key: str,
        test: Optional[TestId] = None,
        dut: Union[DutId, Set[DutId], None] = None,
        start_time: Optional[Time] = None,
        end_time: Optional[Time] = None,
    ) -> List[MetricEntry]:
        response = self.http.get(
            "/metric/entry",
            params=MetricEntryQuerty(
                key, test, dut, start_time, end_time
            ),
        )
        response.raise_for_status()
        return [MetricEntry(**item) for item in response.json()]


    def add_metric_entry(
        self,
        key: MetricKey,
        entry: MetricEntry,
        test: Optional[TestId] = None,
        dut: Union[DutId, Set[DutId], None] = None,
    ) -> MetricEntry:
        response = self.http.post(
            "/metric/entry",
            json=MetricEntryAdd(
                key, entry, test, dut
            ),
        )
        response.raise_for_status()
        return MetricEntry(**response.json())


    async def async_add_metric_entry(
        self,
        key: MetricKey,
        entry: MetricEntry,
        test: Optional[TestId] = None,
        dut: Union[DutId, Set[DutId], None] = None,
    ) -> MetricEntry:
        response = await self.async_http.post(
            "/metric/entry",
            json=MetricEntryAdd(
                key, entry, test, dut
            ),
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
                request = MetricInfoUpdate(info)
                await conn.send(json.dumps(request))
                response.append(info)
        return response


    def batch_add_metric_entry(
        self,
        key: MetricKey,
        entries: Iterator[MetricEntry],
        test: Optional[TestId] = None,
        dut: Union[DutId, Set[DutId], None] = None,
    ) -> List[MetricEntry]:
        return asyncio.run(
            self.abatch_add_metric_entry(key, _aiterator(entries), test, dut)
        )


    async def abatch_add_metric_entry(
        self,
        key: MetricKey,
        entries: AsyncIterator[MetricEntry],
        test: Optional[TestId] = None,
        dut: Union[DutId, Set[DutId], None] = None,
    ) -> List[MetricEntry]:
        response = []
        async with websockets.connect(self.base_ws_url + "/metric/entry") as conn:
            async for entry in entries:
                request = MetricEntryAdd(key, entry, test, dut)
                await conn.send(json.dumps(request))
                response.append(entry)
        return response



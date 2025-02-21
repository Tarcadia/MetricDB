
# -*- coding: UTF-8 -*-


from abc import ABC, abstractmethod
from typing import Union, Optional, Generic, TypeVar
from typing import Iterator, AsyncIterator
from typing import Tuple, List, Set, Dict, Any

from pathlib import Path
from dataclasses import dataclass, asdict

from ..core import Time
from ..core import TestId, DutId
from ..core import MetricKey, MetricInfo, MetricEntry
from ..core import MetricDB



class _MdbClient(ABC):


    @abstractmethod
    def list_metric_info(
        self
    ) -> List[MetricInfo]:
        """List all metric info."""
        pass


    @abstractmethod
    def query_metric_info(
        self,
        key: MetricKey
    ) -> MetricInfo:
        """Query metric info by key."""
        pass


    @abstractmethod
    def update_metric_info(
        self,
        info: MetricInfo
    ) -> MetricInfo:
        """Update metric info."""
        pass


    @abstractmethod
    async def async_update_metric_info(
        self,
        info: MetricInfo
    ) -> MetricInfo:
        """Async update metric info."""
        pass


    @abstractmethod
    def query_metric_entry(
        self,
        key: str,
        test: Optional[TestId] = None,
        dut: Union[DutId, Set[DutId], None] = None,
        start_time: Optional[Time] = None,
        end_time: Optional[Time] = None,
    ) -> List[MetricEntry]:
        """Query metric entry by key."""
        pass


    @abstractmethod
    def add_metric_entry(
        self,
        key: MetricKey,
        entry: MetricEntry,
        test: Optional[TestId] = None,
        dut: Union[DutId, Set[DutId], None] = None,
    ) -> MetricEntry:
        """Add metric entry."""
        pass


    @abstractmethod
    async def async_add_metric_entry(
        self,
        key: MetricKey,
        entry: MetricEntry,
        test: Optional[TestId] = None,
        dut: Union[DutId, Set[DutId], None] = None,
    ) -> MetricEntry:
        """Async add metric entry."""
        pass


    def batch_update_metric_info(
        self,
        info: Iterator[MetricInfo]
    ) -> List[MetricInfo]:
        """Batch update metric info."""
        return [self.update_metric_info(i) for i in info]


    async def abatch_update_metric_info(
        self,
        info: AsyncIterator[MetricInfo]
    ) -> List[MetricInfo]:
        """Async batch update metric info."""
        return [await self.async_update_metric_info(i) for i in info]


    def batch_add_metric_entry(
        self,
        key: MetricKey,
        entry: Iterator[MetricEntry],
        test: Optional[TestId] = None,
        dut: Union[DutId, Set[DutId], None] = None,
    ) -> List[MetricEntry]:
        """Batch add metric entry."""
        return [self.add_metric_entry(key, i, test, dut) for i in entry]


    async def abatch_add_metric_entry(
        self,
        key: MetricKey,
        entry: AsyncIterator[MetricEntry],
        test: Optional[TestId] = None,
        dut: Union[DutId, Set[DutId], None] = None,
    ) -> List[MetricEntry]:
        """Async batch add metric entry."""
        return [await self.async_add_metric_entry(key, i, test, dut) for i in entry]





#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from pathlib import Path
from datetime import datetime
from time import sleep

from metricdb.core.mdb import MetricDB
from metricdb.core.identifier import TestId, DutId
from metricdb.core.time import Time
from metricdb.core.metric import MetricKey, MetricInfo, MetricEntry



PATH_TEST_MDB_DB = Path("test_mdb.db")
if PATH_TEST_MDB_DB.exists():
    PATH_TEST_MDB_DB.unlink()

mdb = MetricDB(PATH_TEST_MDB_DB)

def test_metric_info():
    key = MetricKey("test_metric_info")
    info = MetricInfo(key, "Test Metric", "A test metric")
    mdb.update_metric_info(info)

    resp = mdb.query_metric_info(key)
    assert resp is not None
    assert resp == info

def test_metric_entry():
    key = MetricKey("test_metric")
    test = TestId("test_metric_entry")
    dut1 = DutId("dut1")
    dut2 = DutId("dut2")
    dut3 = DutId("dut3")

    t0 = Time()
    entry1 = MetricEntry(time=datetime.now(), duration=0, value="entry1"); t1 = Time()
    sleep(0.1)
    entry2 = MetricEntry(time=datetime.now(), duration=0, value="entry2"); t2 = Time()
    sleep(0.1)
    entry3 = MetricEntry(time=datetime.now(), duration=0, value="entry3"); t3 = Time()
    sleep(0.1)
    entry4 = MetricEntry(time=datetime.now(), duration=0, value="entry4"); t4 = Time()
    sleep(0.1)

    mdb.add_metric_entry(key, entry1, test=test)
    mdb.add_metric_entry(key, entry2, test=test, dut=dut1)
    mdb.add_metric_entry(key, entry3, dut=[dut1, dut2, dut3])
    mdb.add_metric_entry(key, entry4)

    entries = mdb.query_metric_entry(str(key))
    assert entries == [entry1, entry2, entry3, entry4]

    entries = mdb.query_metric_entry(str(key), test=test)
    assert entries == [entry1, entry2]

    entries = mdb.query_metric_entry(str(key), dut=dut1)
    assert entries == [entry2, entry3]

    entries = mdb.query_metric_entry(str(key), test=test, dut=[dut1])
    assert entries == [entry2]

    entries = mdb.query_metric_entry(str(key), start_time=t0, end_time=t2, dut=[dut1])
    assert entries == [entry2]

    entries = mdb.query_metric_entry(str(key), start_time=t1, end_time=t3, test=test, dut=[dut1, dut2])
    assert entries == []

test_metric_info()
test_metric_entry()

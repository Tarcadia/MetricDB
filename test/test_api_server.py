
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from pathlib import Path
from datetime import datetime
from time import sleep

from metricdb.core import Time
from metricdb.core import TestId, DutId
from metricdb.core import MetricKey, MetricInfo, MetricEntry
from metricdb.core import MetricDB

from metricdb.api import MdbAPI
from metricdb.client import MdbClient



PATH_TEST_MDB_DB = Path("test_mdb.db")
if PATH_TEST_MDB_DB.exists():
    PATH_TEST_MDB_DB.unlink()

app = MdbAPI(PATH_TEST_MDB_DB)


def test_server():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



if __name__ == "__main__":
    test_server()



# -*- coding: UTF-8 -*-

import sqlite3
from pathlib import Path
from typing import List, Tuple
from datetime import datetime
from .metric import MetricKey, MetricInfo, MetricEntry
from .time import Time



class MetricDB:

    def __init__(self, filename: Path):
        self.filename = Path(filename)
        self._init_db()


    def _init_db(self):
        with sqlite3.connect(self.filename) as conn:
            conn.execute("PRAGMA journal_mode=WAL")
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS metric_info (
                    key TEXT PRIMARY KEY,
                    name TEXT,
                    description TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS metric_entry (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT,
                    time DATETIME,
                    duration REAL,
                    value BLOB
                )
            """)
            conn.commit()


    def update_metric_info(self, info: MetricInfo) -> None:
        with sqlite3.connect(self.filename) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR REPLACE INTO metric_info VALUES (?, ?, ?)",
                (str(info.key), info.name, info.description)
            )
            conn.commit()


    def query_metric_info(self, key: MetricKey) -> MetricInfo:
        with sqlite3.connect(self.filename) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name, description FROM metric_info WHERE key = ?",
                (str(key),)
            )
            _result = cursor.fetchone()
            if _result is None:
                return MetricInfo(key)
            else:
                return MetricInfo(key, *_result)


    def add_metric_entry(self, key: MetricKey, entry: MetricEntry) -> None:
        with sqlite3.connect(self.filename) as conn:
            entry_time = entry.time.isoformat()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO metric_entry (key, time, duration, value) VALUES (?, ?, ?, ?)",
                (str(key), entry_time, entry.duration, entry.value)
            )
            conn.commit()


    def query_metric_entry(
        self,
        key: str,
        start_time: Time,
        end_time: Time
    ) -> List[MetricEntry]:
        start_time = start_time.isoformat()
        end_time = end_time.isoformat()

        with sqlite3.connect(self.filename) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT key, time, duration, value 
                FROM metric_entry 
                WHERE key GLOB ? 
                AND datetime(time, '+' || duration || ' seconds') >= ? 
                AND time <= ? 
                ORDER BY time
                """,
                (key, start_time, end_time)
            )
            return [
                MetricEntry(
                    datetime.fromisoformat(row["time"]),
                    row["duration"],
                    row["value"]
                ) for row in cursor.fetchall()
            ]


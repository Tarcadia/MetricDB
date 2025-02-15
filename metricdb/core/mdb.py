# -*- coding: UTF-8 -*-

import sqlite3
from pathlib import Path
from typing import List, Tuple
from datetime import datetime
from .metric import MetricId, MetricIdPattern, MetricInfo, MetricEntry
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
                    id TEXT PRIMARY KEY,
                    name TEXT,
                    description TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS metric_entry (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    mid TEXT,
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
                (str(info.id), info.name, info.description)
            )
            conn.commit()


    def query_metric_info(self, id: MetricId) -> MetricInfo:
        with sqlite3.connect(self.filename) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name, description FROM metric_info WHERE id = ?",
                (str(id),)
            )
            _result = cursor.fetchone()
            if _result is None:
                return MetricInfo(id)
            else:
                return MetricInfo(id, *_result)


    def add_metric_entry(self, id: MetricId, entry: MetricEntry) -> None:
        with sqlite3.connect(self.filename) as conn:
            entry_time = entry.time.isoformat()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO metric_entry (mid, time, duration, value) VALUES (?, ?, ?, ?)",
                (str(id), entry_time, entry.duration, entry.value)
            )
            conn.commit()


    def query_metric_entry(
        self,
        metric_pattern: MetricIdPattern,
        start_time: Time,
        end_time: Time
    ) -> List[Tuple[MetricId, MetricEntry]]:
        pattern = str(metric_pattern)
        start_time = start_time.isoformat()
        end_time = end_time.isoformat()

        with sqlite3.connect(self.filename) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT mid, time, duration, value 
                FROM metric_entry 
                WHERE mid GLOB ? 
                AND datetime(time, '+' || duration || ' seconds') >= ? 
                AND time <= ? 
                ORDER BY time
                """,
                (pattern, start_time, end_time)
            )
            return [
                MetricEntry(
                    datetime.fromisoformat(row["time"]),
                    row["duration"],
                    row["value"]
                ) for row in cursor.fetchall()
            ]


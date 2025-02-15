# -*- coding: UTF-8 -*-

import sqlite3
from pathlib import Path
from typing import List, Optional, Tuple
from .metric import MetricId, MetricIdPattern, MetricInfo, MetricEntry
from .time import Time



class MetricDB:

    def __init__(self, filename: Path):
        self.filename = Path(filename)
        self._init_db()


    def _init_db(self):
        with sqlite3.connect(self.filename) as conn:
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
                    time TEXT,
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
            return cursor.fetchone() or MetricInfo(id)


    def add_metric_entry(self, id: MetricId, entry: MetricEntry) -> None:
        with sqlite3.connect(self.filename) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO metric_entry (mid, time, duration, value) VALUES (?, ?, ?, ?)",
                (str(id), str(entry.time), entry.duration, entry.value)
            )
            conn.commit()


    def query_metric_entry(
        self,
        metric_pattern: MetricIdPattern,
        start_time: Time,
        end_time: Time
    ) -> List[Tuple[MetricId, MetricEntry]]:
        pattern = str(metric_pattern)
        with sqlite3.connect(self.filename) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT mid, time, duration, value 
                FROM metric_entry 
                WHERE mid GLOB ? 
                AND (
                    (time BETWEEN ? AND ?) OR
                    (datetime(time) <= datetime(?) AND 
                     datetime(time, '+' || duration || ' seconds') >= datetime(?))
                """,
                (pattern.replace('**', '*').replace('::', ':'), 
                 str(start_time), str(end_time),
                 str(start_time), str(end_time))
            )
            return [
                (MetricId(row[0]), MetricEntry(Time(row[1]), row[2], row[3]))
                for row in cursor.fetchall()
            ]

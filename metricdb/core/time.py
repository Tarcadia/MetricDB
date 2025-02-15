
# -*- coding: UTF-8 -*-

from datetime import datetime



class Time(datetime):

    FORMAT = "%Y%m%d%H%M%S%f"
    ACCURACY = 20

    def __new__(cls, time: bytes | datetime | str | int | None = None):
        if isinstance(time, Time):
            return time
        if isinstance(time, datetime):
            dt = time
        elif isinstance(time, bytes):
            dt = datetime(time)
        elif isinstance(time, int):
            dt = datetime.fromtimestamp(time)
        elif isinstance(time, str):
            lower_time = time.lower()
            if lower_time == "min":
                dt = datetime.min
            elif lower_time == "max":
                dt = datetime.max
            elif lower_time == "now":
                dt = datetime.now()
            else:
                if isinstance(time, str) and len(time) < Time.ACCURACY:
                    time += "0" * (Time.ACCURACY - len(time))
                dt = datetime.strptime(time, cls.FORMAT)
        elif time is None:
            dt = datetime.now()
        else:
            raise ValueError(f"Invalid time: {time}")

        return super().__new__(
            cls,
            dt.year, dt.month, dt.day,
            dt.hour, dt.minute, dt.second, dt.microsecond,
            dt.tzinfo
        )

    def __str__(self):
        if self == datetime.min:
            return "min"
        elif self == datetime.max:
            return "max"
        return self.strftime(self.FORMAT)

    def __repr__(self):
        return f"Time({'self'})"


Time.min = Time("min")
Time.max = Time("max")



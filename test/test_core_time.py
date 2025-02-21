
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from datetime import datetime
from datetime import timedelta
from datetime import timezone

from metricdb.core import Time

def _now():
    return datetime.now().astimezone(timezone.utc)

# Test Time class
assert Time() - _now()                                          < timedelta(seconds=1)
assert Time(None) - _now()                                      < timedelta(seconds=1)
assert Time(timedelta(days=1)) - _now() - timedelta(days=1)     < timedelta(seconds=1)

assert Time(2025, 1, 1)                     == datetime(2025, 1, 1).astimezone(timezone.utc)
assert Time(datetime(2025, 1, 1))           == datetime(2025, 1, 1).astimezone(timezone.utc)
assert Time("2025-01-01")                   == datetime(2025, 1, 1).astimezone(timezone.utc)
assert Time("2025-01-01T00:00:00.000000")   == datetime(2025, 1, 1).astimezone(timezone.utc)
assert Time("min")                          == Time(datetime.min)
assert Time("max")                          == Time(datetime.max)

assert int(Time(2000000000_000000))         == 2000000000_000000
assert int(Time(2000000000_333666))         == 2000000000_333666
assert int(Time(2000000000_333665.99))      == 2000000000_333666

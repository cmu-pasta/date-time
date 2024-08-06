"""
Description: This file contains code snippets that perform datetime arithmetic operations. It tests the behavior of the arithmetic operations when used incorrectly.

Links:
- https://dev.arie.bovenberg.net/blog/python-datetime-pitfalls/
- https://blog.ganssle.io/articles/2018/02/a-curious-case-datetimes.html
"""

import unittest
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import pendulum
from dateutil import tz
from hypothesis import example, given
from hypothesis.strategies import datetimes, timezones


class TestArithmetic(unittest.TestCase):

    # Test: Arithmetic operations on datetime objects are DST unaware.
    @unittest.expectedFailure
    @given(datetimes(), datetimes(), timezones())
    @example(
        datetime(2023, 3, 25, 22, 0, 0),
        datetime(2023, 3, 26, 7, 0, 0),
        ZoneInfo("Europe/Paris"),
    )
    def test_arithmetic_0(
        self, dt1: datetime, dt2: datetime, tz_info: timezone
    ) -> None:
        default_dt1 = dt1.astimezone(tz_info)
        default_dt2 = dt2.astimezone(tz_info)

        pendulum_dt1 = pendulum.instance(dt1, tz_info)
        pendulum_dt2 = pendulum.instance(dt2, tz_info)

        default_diff = (default_dt1 - default_dt2).total_seconds()
        pendulum_diff = (pendulum_dt1 - pendulum_dt2).total_seconds()

        assert default_diff == pendulum_diff

    # Test: Disambiguation of ambiguous datetime objects breaks equality.
    @unittest.expectedFailure
    @given(datetimes(), timezones())
    @example(datetime(2023, 10, 29, 2, 30, 0), ZoneInfo("Europe/Paris"))
    def test_arithmetic_1(self, dt: datetime, tz_info: timezone) -> None:
        d = datetime(
            dt.year,
            dt.month,
            dt.day,
            dt.hour,
            dt.minute,
            dt.second,
            tzinfo=tz_info,
            fold=1,
        )

        d_utc = d.astimezone(timezone.utc)

        assert d.timestamp() == d_utc.timestamp()
        assert d == d_utc

    # Test: Inconsistent equality within timezone.
    @unittest.expectedFailure
    @given(datetimes(), timezones())
    @example(datetime(2023, 10, 29, 2, 30, 0), ZoneInfo("Europe/Paris"))
    def test_arithmetic_2(self, dt: datetime, tz_info: timezone) -> None:
        earlier = datetime(
            dt.year,
            dt.month,
            dt.day,
            dt.hour,
            dt.minute,
            dt.second,
            tzinfo=tz_info,
            fold=0,
        )
        later = datetime(
            dt.year,
            dt.month,
            dt.day,
            dt.hour,
            dt.minute,
            dt.second,
            tzinfo=tz_info,
            fold=1,
        )

        assert earlier.timestamp() != later.timestamp()
        assert earlier != later

    # Test: Arithmetic operations on datetime objects are DST unaware.
    @unittest.expectedFailure
    @given(datetimes(), timezones())
    @example(datetime(2024, 3, 9, 2, 30, 0), ZoneInfo("America/New_York"))
    def test_arithmetic_3(self, dt: datetime, tz_info: timezone) -> None:
        default_now = datetime(
            dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, tzinfo=tz_info
        )
        default_tomorrow = default_now + timedelta(days=1)

        pendulum_now = pendulum.instance(default_now, tz_info)
        pendulum_tomorrow = pendulum_now.add(days=1)

        assert default_now.hour == default_tomorrow.hour
        assert pendulum_now.hour == pendulum_tomorrow.hour

        default_24h = default_now + timedelta(hours = 24)
        pendulum_24h = pendulum_now.add(hours = 24)

        assert default_now.hour == default_24h.hour
        assert pendulum_now.hour == pendulum_24h.hour


if __name__ == "__main__":
    unittest.main()

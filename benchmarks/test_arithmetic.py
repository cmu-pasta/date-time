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
import arrow
from dateutil import tz
from hypothesis import example, given
from hypothesis.strategies import datetimes, timezones


class TestArithmetic(unittest.TestCase):

    # Test: Arithmetic operations on datetime objects are DST unaware.
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

        arrow_dt1 = arrow.get(dt1).to(tz_info)
        arrow_dt2 = arrow.get(dt2).to(tz_info)

        default_diff = (default_dt1 - default_dt2).total_seconds()
        pendulum_diff = (pendulum_dt1 - pendulum_dt2).total_seconds()
        arrow_diff = (arrow_dt1 - arrow_dt2).total_seconds()

        assert default_diff == pendulum_diff == arrow_diff

    # Test: Disambiguation of ambiguous datetime objects breaks equality.
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

        pendulum_d = pendulum.instance(d, tz_info)
        pendulum_d_utc = pendulum_d.in_timezone('UTC')

        arrow_d = arrow.get(d)
        arrow_d_utc = arrow_d.to('UTC')

        assert d.timestamp() == d_utc.timestamp()
        assert pendulum_d.timestamp() == pendulum_d_utc.timestamp()
        assert arrow_d.timestamp() == arrow_d_utc.timestamp()
        
        assert d == d_utc
        assert pendulum_d == pendulum_d_utc
        assert arrow_d == arrow_d_utc

    # Test: Inconsistent equality within timezone.
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

        pendulum_earlier = pendulum.instance(earlier, tz_info)
        pendulum_later = pendulum.instance(later, tz_info)
        arrow_earlier = arrow.get(earlier).to(tz_info)
        arrow_later = arrow.get(later).to(tz_info)

        assert earlier.timestamp() != later.timestamp()
        assert pendulum_earlier.timestamp() != pendulum_later.timestamp()
        assert arrow_earlier.timestamp() != arrow_later.timestamp()
        assert earlier != later
        assert pendulum_earlier != pendulum_later
        assert arrow_earlier != arrow_later

    # Test: Arithmetic operations on datetime objects are DST unaware.
    @given(datetimes(), timezones())
    @example(datetime(2024, 3, 9, 1, 30, 0), ZoneInfo("America/New_York"))
    def test_arithmetic_3(self, dt: datetime, tz_info: timezone) -> None:
        default_now = datetime(
            dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, tzinfo=tz_info
        )
        default_tomorrow = default_now + timedelta(days=1)

        pendulum_now = pendulum.instance(default_now, tz_info)
        pendulum_tomorrow = pendulum_now.add(days=1)

        arrow_now = arrow.get(default_now).to(tz_info)
        arrow_tomorrow = arrow_now.shift(days=1)

        assert default_now.hour == default_tomorrow.hour
        assert pendulum_now.hour == pendulum_tomorrow.hour
        assert arrow_now.datetime.hour == arrow_tomorrow.datetime.hour

        # TODO: Add a example where the total time added is 1 day but 24hrs instead.


if __name__ == "__main__":
    unittest.main()

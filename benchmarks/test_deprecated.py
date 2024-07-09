"""
Description: This file contains code snippets that make use of deprecated date-time library API methods. 

Links:
- https://blog.ganssle.io/articles/2019/11/utcnow.html
- https://discuss.python.org/t/deprecating-utcnow-and-utcfromtimestamp/26221
- https://blog.miguelgrinberg.com/post/it-s-time-for-a-change-datetime-utcnow-is-now-deprecated#:~:text=The%20problem%20that%20the%20Python,is%20already%20known%20in%20advance.
"""

import unittest
from datetime import datetime, timezone
import arrow
import pendulum

from hypothesis import given
from hypothesis.strategies import integers, timezones


class TestDeprecatedAPIUsage(unittest.TestCase):

    def test_deprecated_api_usage_0(self) -> None:
        dt_utcnow = datetime.utcnow()
        dt_now = datetime.now(tz=timezone.utc)
        self.assertEqual(dt_utcnow, dt_now)

    @given(integers(min_value=0, max_value=4294967296), timezones())
    def test_deprecated_api_usage_1(self, timestamp: int, timezone: timezone) -> None:
        dt = datetime.utcfromtimestamp(timestamp)
        ts_new = dt.astimezone(tz=timezone).timestamp()
        self.assertEqual(ts_new, timestamp)

    def test_deprecated_api_usage_arrow(self) -> None:
        dt_local = arrow.now('local')
        dt_now = arrow.now().to('local')
        self.assertEqual(dt_local, dt_now)

    def test_deprecated_api_usage_pendulum(self) -> None:
        dt_parsed = pendulum.parse('2023-07-08T12:34:56', tz='UTC')
        dt_parsed_in_tz = pendulum.parse('2023-07-08T12:34:56').in_timezone('UTC')
        self.assertEqual(dt_parsed, dt_parsed_in_tz)


if __name__ == "__main__":
    unittest.main()

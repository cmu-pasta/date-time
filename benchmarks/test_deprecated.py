"""
Associated Category: 
    Deprecated

Description:
    Tests which make use of deprecated datetime APIs.

Notes: 
    This file only focuses on utcnow and utcfromtimestamp. Other deprecations such as datetime.datetime.timetuple() may be added later.

Further Reading:
  - https://blog.ganssle.io/articles/2019/11/utcnow.html
  - https://discuss.python.org/t/deprecating-utcnow-and-utcfromtimestamp/26221
  - https://blog.miguelgrinberg.com/post/it-s-time-for-a-change-datetime-utcnow-is-now-deprecated
"""

import unittest
from datetime import datetime, timezone

from hypothesis import given
from hypothesis.strategies import integers, timezones


class TestDeprecatedAPIUsage(unittest.TestCase):
    """
    Description:
        Test which calls datetime.utcnow()
    Failure Reason: 
        datetime.utcnow() is a deprecated function and will raise a warning when called.
    Examples:
      - https://github.com/python-poetry/tomlkit/issues/297
      - https://github.com/requests-cache/aiohttp-client-cache/issues/237
    """
    @unittest.expectedFailure
    def test_deprecated_api_usage_0(self) -> None:
        dt_utcnow = datetime.utcnow()
        dt_now = datetime.now(tz=timezone.utc)
        self.assertEqual(dt_utcnow, dt_now)

    """
    Description:
        Test which calls datetime.utcfromtimestamp()
    Failure Reason: 
        datetime.utcfromtimestamp() is a deprecated function and will raise a warning when called.
    Examples:
      - https://github.com/timvink/mkdocs-git-revision-date-localized-plugin/issues/121
    """
    @unittest.expectedFailure
    @given(integers(min_value=0, max_value=4294967296), timezones())
    def test_deprecated_api_usage_1(self, timestamp: int, timezone: timezone) -> None:
        dt = datetime.utcfromtimestamp(timestamp)
        ts_new = dt.astimezone(tz=timezone).timestamp()
        self.assertEqual(ts_new, timestamp)


if __name__ == "__main__":
    unittest.main()

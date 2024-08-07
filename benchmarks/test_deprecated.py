"""
Associated Category: 
    Deprecated

Description:
    Tests which make use of deprecated datetime APIs.

Notes:
    All of these bugs involve functions which treat naive datetimes as utc, which is being phased out in favor of using timezoned objects.
    test_deprecated_api_usage_2 is not a deprecated function but has the same root issue as the other two tests, which is why it is still included.
    Our dataset includes another bug tagged Deprecated, which may be added to this suite in the future. (https://github.com/googlemaps/google-maps-services-python/issues/185)

Further Reading:
  - https://blog.ganssle.io/articles/2019/11/utcnow.html
  - https://discuss.python.org/t/deprecating-utcnow-and-utcfromtimestamp/26221
  - https://blog.miguelgrinberg.com/post/it-s-time-for-a-change-datetime-utcnow-is-now-deprecated
"""

import unittest
import time
from datetime import datetime, timezone

from hypothesis import given
from hypothesis.strategies import integers, datetimes, timezones


class TestDeprecatedAPIUsage(unittest.TestCase):
    """
    Description:
        Test which calls datetime.utcnow()
    Failure Reason: 
        datetime.utcnow() is a deprecated function and will raise a warning when called.
    Examples:
      - https://github.com/python-poetry/tomlkit/issues/297
      - https://github.com/requests-cache/aiohttp-client-cache/issues/237
    Failing Input:
        N/A
    Notes:
        Test will only fail if you are in a non-utc timezone.
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
    Failing Input:
        All Inputs
    Notes:
        Test will only fail if you are in a non-utc timezone.
    """
    @unittest.expectedFailure
    @given(integers(min_value=0, max_value=4294967296), timezones())
    def test_deprecated_api_usage_1(self, timestamp: int, timezone: timezone) -> None:
        dt = datetime.utcfromtimestamp(timestamp)
        ts_new = dt.astimezone(tz=timezone).timestamp()
        self.assertEqual(ts_new, timestamp)
    
    """
    Description:
        Test which uses time.mktime and timetuple to construct a timestamp
    Failure Reason: 
        timetuple will drop timezone information, and so mktime assumes the timezone is local.
    Examples:
      - https://github.com/googlemaps/google-maps-services-python/issues/185
    Failing Input:
        Any input where timezone != utc
    Notes:
        Test will only fail if you are in a non-utc timezone.
    """
    @unittest.expectedFailure
    @given(datetimes(), timezones())
    def test_deprecated_api_usage_2(self, dt: datetime, timezone: timezone):
        dt = dt.astimezone(timezone)
        timestamp1 = dt.timestamp()
        timestamp2 = time.mktime(dt.timetuple())
        self.assertEqual(timestamp1, timestamp2)


if __name__ == "__main__":
    unittest.main()

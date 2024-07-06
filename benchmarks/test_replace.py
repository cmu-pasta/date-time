"""
Description: This file contains code snippets that call the replace() method on datetime objects. It tests the behavior of the method when used incorrectly.

Links:
- https://stackoverflow.com/questions/39759041/replace-tzinfo-and-print-with-localtime-amends-six-minutes
- https://stackoverflow.com/questions/1379740/pytz-localize-vs-datetime-replace
"""

import datetime
import unittest

import dateutil
import pytz
from hypothesis import given
from hypothesis.strategies import datetimes
from tzlocal import get_localzone


class TestReplace(unittest.TestCase):

    # Test that calls the replace() method on a datetime object.
    @given(datetimes())
    def test_replace_0(self, dt: datetime) -> None:
        now = datetime.datetime.now()
        local_tz = get_localzone()
        tz1 = pytz.timezone(str(local_tz))
        tz2 = dateutil.tz.gettz(str(local_tz))
        shifted1 = now.replace(tzinfo=tz1)
        shifted2 = now.replace(tzinfo=tz2)
        assert shifted1.timestamp() == shifted2.timestamp()


if __name__ == "__main__":
    unittest.main()

"""
Description: This file contains code snippets that do not follow the best coding practices when it comes to timezones.

Links:
- https://dev.arie.bovenberg.net/blog/python-datetime-pitfalls/
"""

import unittest
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
import pytz

from dateutil import tz as dutz
from hypothesis import example, given
from hypothesis.strategies import datetimes, integers, text, timezones


class TestTimeZones(unittest.TestCase):

    # Test: Creation of a non existent timezone passes silently
    @unittest.expectedFailure
    @given(datetimes(), text())
    def test_timezones_0(self, dt: datetime, tz_name: str) -> None:
        silent_failure = True
        try:
            nonexistent_tz = dutz.gettz(tz_name)
            nonexistent_dt = dt.replace(tzinfo=nonexistent_tz)
            # raise Exception("Should not reach here")
        except Exception as e:
            silent_failure = False
            pass

        assert silent_failure == False

    # Test: Creation of fixed offset timezones is bad
    @unittest.expectedFailure
    @given(integers(min_value=-12, max_value=14), timezones())
    def test_timezones_1(self, offset: int, tz_info: timezone) -> None:
        fixed_timezone = dutz.gettz("EST")
        custom_timezone = timezone(timedelta(hours=offset))
        builtin_timezone = tz_info
        now = datetime(2024,1,1)

        offset1 = now.astimezone(fixed_timezone).utcoffset().total_seconds() / 3600
        offset2 = now.astimezone(custom_timezone).utcoffset().total_seconds() / 3600
        offset3 = now.astimezone(builtin_timezone).utcoffset().total_seconds() / 3600

        # Iterate over all possible months to check if offset ever changes
        is_bad_timezone1 = True
        is_bad_timezone2 = True
        is_bad_timezone3 = True
        for month in range(1, 13):
            new_date1 = now.replace(month=month).astimezone(fixed_timezone)
            new_date2 = now.replace(month=month).astimezone(custom_timezone)
            new_date3 = now.replace(month=month).astimezone(builtin_timezone)

            new_offset1 = new_date1.utcoffset().total_seconds() / 3600
            new_offset2 = new_date2.utcoffset().total_seconds() / 3600
            new_offset3 = new_date3.utcoffset().total_seconds() / 3600

            if new_offset1 != offset1:
                is_bad_timezone1 = False
            if new_offset2 != offset2:
                is_bad_timezone2 = False
            if new_offset3 != offset3:
                is_bad_timezone3 = False

        assert not is_bad_timezone1
        assert not is_bad_timezone2
        assert not is_bad_timezone3

    # Test: Assigning specific timezones to datetime objects will succeeded even when it should not.
    @unittest.expectedFailure
    @given(datetimes())
    @example(datetime(2024, 3, 9, 12, 0, 0))  # DST transition for Eastern timezone
    def test_timezones_2(self, dt1: datetime) -> None:
        # Simulating DST transition
        temp = dt1 + timedelta(days=1)
        dt2 = datetime(
            temp.year,
            temp.month,
            temp.day,
            temp.hour,
            temp.minute,
            temp.second,
            tzinfo=temp.tzinfo,
        )
        # print(dt2.tzname()) -> EST (should be EDT)

        dt3 = dt2.astimezone()
        # print(dt3.tzname()) -> EDT

        assert dt1.tzname() != dt2.tzname()
        assert dt1.tzname() != dt3.tzname()
        assert dt2.tzname() == dt3.tzname()

    # Test: Non-existent datetimes will pass silently
    @unittest.expectedFailure
    @given(datetimes(), timezones())
    @example(
        datetime(2023, 3, 26, 2, 30, 0), ZoneInfo("Europe/Paris")
    )  # DST transition for Paris timezone
    def test_timezones_3(self, dt: datetime, tz_info: timezone) -> None:
        d = dt.replace(tzinfo=tz_info)

        # It is possible that the time does not exist in the timezone and it takes a future timestamp.
        t = d.timestamp()

        assert datetime.fromtimestamp(t, tz_info) == d

    # Test: passing pytz timezones to the tzinfo field of a datetime is bad
    @unittest.expectedFailure
    @given(datetimes(), timezones())
    def test_timezones_4(self, dt: datetime, tz_info: timezone) -> None:
        tz1 = pytz.timezone(str(tz_info))
        tz2 = dutz.gettz(str(tz_info))
        dt1 = datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond,
                       tzinfo=tz1)
        dt2 = datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond,
                       tzinfo=tz2)
        assert tz1.timestamp() == tz2.timestamp()


if __name__ == "__main__":
    unittest.main()

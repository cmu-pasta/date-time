"""
Description: This file contains code snippets that do not follow the best coding practices when it comes to timezones.

Links:
"""

import unittest
from datetime import datetime, timedelta, timezone

from dateutil import tz
from hypothesis import example, given
from hypothesis.strategies import datetimes, integers, text


class TestTimeZones(unittest.TestCase):

    # Test: Creation of a non existent timezone passes silently
    @given(datetimes(), text())
    def test_timezones_0(self, dt: datetime, tz_name: str) -> None:
        silent_failure = True
        try:
            nonexistent_tz = tz.gettz(tz_name)
            nonexistent_dt = dt.replace(tzinfo=nonexistent_tz)
            # raise Exception("Should not reach here")
        except Exception as e:
            silent_failure = False
            pass

        assert silent_failure == False

    # Test: Creation of fixed offset timezones is bad
    @given(integers(min_value=-12, max_value=14))
    def test_timezones_1(self, offset: int) -> None:
        fixed_timezone = tz.gettz("EST")
        now = datetime.now()

        fixed_offset_timezone = True
        offset = now.astimezone(fixed_timezone).utcoffset().total_seconds() / 3600

        # Iterate over all possible months to check if offset ever changes
        for month in range(1, 13):
            new_date = now.replace(month=month).astimezone(fixed_timezone)
            new_offset = new_date.utcoffset().total_seconds() / 3600
            if new_offset != offset:
                fixed_offset_timezone = False
        assert fixed_offset_timezone == False

    # Test: Assigning specific timezones to datetime objects will succeeded even when it should not
    @given(datetimes())
    @example(datetime(2024, 3, 9, 12, 0, 0))  # DST transition for New York timezone
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


if __name__ == "__main__":
    unittest.main()

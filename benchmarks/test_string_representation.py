"""
Associated Category:
    String Representation

Description:
    Tests which make use of the string form of a date. E.g., YYYY-MM-DD'T'HH:mm:ssZ

Notes:
    These bugs involve functions which attempt to store datetimes by their individual components.
    Many of these bugs involve bad regex parsing or other kinds of parsing errors.
    For example, while converting from a string to a datetime, you might lose precision or timezone information.

    In general, we suggest not using your own regex to parse datetimes ever.

Further Reading:
    -

"""

import unittest
import time
from datetime import datetime, timezone
import re

from hypothesis import given
from hypothesis.strategies import integers, datetimes, timezones

class TestStringRepresentation(unittest.TestCase):
    """
    Description:
        Test which doesn't parse the microseconds of a string datetime object
    """
    @unittest.expectedFailure
    @given(datetimes())
    def test_string_representation_0(dt: datetimes) -> None:
        datetime_str = dt.strftime('%Y-%m-%d %H:%M:%S.%f')
        datetime_pattern = r'(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})'
        match = re.match(datetime_pattern, datetime_str)

        Y, M, D, H, m, s = map(int, match.groups())
        parsed_datetime = datetime.datetime(Y, M, D, H, m, s)

        self.assertEqual(parsed_datetime, dt)


    """
    Description:
        Test which always prepends 20... to 2-digit years and never prepends 19... instead

    Examples:
        - https://github.com/sdispater/pendulum/issues/686
    """
    @unittest.expectedFailure
    @given(datetimes())
    def test_string_representation_1(dt: datetimes) -> None:
        datetime_str = dt.strftime('%y-%m-%d %H:%M:%S.%f')
        datetime_pattern = r'(\d{2})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})\.(\d{6})'
        match = re.match(datetime_pattern, datetime_str)

        Y, M, D, H, m, s, f = map(int, match.groups())
        Y += 2000
        parsed_datetime = datetime.datetime(Y, M, D, H, m, s, f)

        self.assertEqual(parsed_datetime, dt)


    """
    Description:
        Test which rounds instead of crops the milliseconds

    Examples:
        - https://github.com/art049/odmantic/issues/99
    """
    @unittest.expectedFailure
    @given(datetimes())
    def test_string_representation_2(dt: datetimes) -> None:
        datetime_str = dt.strftime('%Y-%m-%d %H:%M:%S.%f')
        datetime_pattern = r'(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})\.(\d{6})'

        match = re.match(datetime_pattern, datetime_str)

        Y, M, D, H, m, s, f = map(int, match.groups())
        incorrect_datetime = datetime.datetime(Y, M, D, H, m, s, (f + 500) // 1000 * 1000)

        dt = dt.replace(microsecond = dt.microsecond // 1000 * 1000)

        self.assertEqual(dt, incorrect_datetime)


    """
    Description:
        Test which doesn't parse the timezone
    """
    @unittest.expectedFailure
    @given(datetimes(), timezones())
    def test_string_representation_3(dt: datetimes, tz: timezone) -> None:
        dt = dt.astimezone(tz)
        datetime_str = dt.strftime('%Y-%m-%d %H:%M:%S.%fz') # has a timezone
        datetime_pattern = r'(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})\.(\d{6})'

        match = re.match(datetime_pattern, datetime_str)

        Y, M, D, H, m, s, f = map(int, match.groups())
        incorrect_datetime = datetime.datetime(Y, M, D, H, m, s, f)

        self.assertEqual(dt, incorrect_datetime)

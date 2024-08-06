"""
<<<<<<< HEAD
Associated Category: 
    Date

Description:
    Tests involving the construction, arithmetic and manipulation of dates (usually without times).

Notes: 
    List of all bugs currently tagged Date:
    https://github.com/sdispater/pendulum/issues/714        - Marked yes, I say no
    https://github.com/dateutil/dateutil/issues/1167        - Marked yes, I say no
    https://github.com/vacanza/python-holidays/issues/1774  - Marked yes, I say no
    https://github.com/vacanza/python-holidays/issues/569   - Marked no
    https://github.com/thombashi/DateTimeRange/issues/44    - Marked no
    https://github.com/scrapinghub/dateparser/issues/1053   - Maybe Benchmarkable
    https://github.com/agronholm/apscheduler/issues/911     - Marked no
    https://github.com/KoffeinFlummi/Chronyk/issues/5       - test_date_0/test_date_1
    https://github.com/sdispater/pendulum/issues/686        - Maybe Benchmarkable (but probably not this file)
    https://github.com/tobymao/sqlglot/issues/1779          - Marked no
    https://github.com/art049/odmantic/issues/99            - Dissagree with tag
    https://github.com/sktime/sktime/issues/3188            - Marked no

Further Reading:
"""

import unittest
from datetime import datetime, timezone

from hypothesis import example, given
from hypothesis.strategies import integers, datetimes, timezones


class TestDate(unittest.TestCase):
    """
    Description:
        Test which calls replace on only the year.
    Failure Reason: 
        If the original date is Feb 29, the new date may not exist
    Examples:
      - https://github.com/KoffeinFlummi/Chronyk/issues/5
    Failing Input:
        dt = datetime(2024,2,29,0,0,0)
        new_year = 2023
    """
    @unittest.expectedFailure
    @given(datetimes(), integers(min_value=1900, max_value=2100))
    @example(datetime(2024,2,29,0,0,0), 2023)
    def test_date_0(self, dt: datetime, new_year: int) -> None:
        dt_2 = dt.replace(year=new_year)
    
    """
    Description:
        Test which calls replace on only the month.
    Failure Reason: 
        If the original date is the 31st of a month, the new date may not exist
    Examples:
      - https://github.com/KoffeinFlummi/Chronyk/issues/5
      - https://github.com/scrapinghub/dateparser/issues/1053
    Failing Input:
        dt = datetime(2024,1,31,0,0,0)
        new_month = 2
    """
    @unittest.expectedFailure
    @given(datetimes(), integers(min_value=1, max_value=12))
    @example(datetime(2024,1,31,0,0,0), 2)
    def test_date_1(self, dt: datetime, new_month: int) -> None:
        dt_2 = dt.replace(month=new_month)

if __name__ == "__main__":
    unittest.main()
=======
1) https://github.com/scrapinghub/dateparser/pull/1086/files

Creating datetimes with some constant and some variable parameters.
E.g., datetime(2024, a, b, c, ...)
Also consider, potentially all being variables.
E.g., d=2024; datetime(d, a, b, c, ...)


2) https://github.com/sdispater/pendulum/issues/686

2-digit year. Not sure how to make a benchmark for this.
E.g., 85 was interpreted as 2085 instead of 1985.

3) https://github.com/KoffeinFlummi/Chronyk/issues/5

Adding X months to current date without checking if the new date exists.
E.g., Jan 31 + 1 Month = Feb 31 !!!

4) https://github.com/scrapinghub/dateparser/issues/403

Check if time is after current time but in UTC instead of local timezone.
E.g., When is the next 2pm? If you use UTC instead of local tz but the
same time, you'll get a different answer.

5) https://github.com/pyopenapi/pyswagger/issues/83

Failing to parse ms/us portion of a datetime.
Failing to parse tz.
Failing to parse tz only when usecs are present?
Etc.
E.g., parse("2016-08-05T03:14:14.809Z") => dt(2016, 8, 5, 3, 14, 14)

6) https://github.com/GoogleCloudPlatform/professional-services-data-validator/issues/1053

Parsing huge datetimes.
E.g., parse("9999-12-31T23:59:59.999999") => error

"""
>>>>>>> b1eefe5 (Merging updates from Dev (#39))

"""
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
    https://github.com/art049/odmantic/issues/99            - Disagree with tag
    https://github.com/sktime/sktime/issues/3188            - Marked no

Further Reading:
"""

import unittest
from datetime import datetime

from hypothesis import example, given
from hypothesis.strategies import datetimes, integers


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
    @example(datetime(2024, 2, 29, 0, 0, 0), 2023)
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
    @example(datetime(2024, 1, 31, 0, 0, 0), 2)
    def test_date_1(self, dt: datetime, new_month: int) -> None:
        dt_2 = dt.replace(month=new_month)


if __name__ == "__main__":
    unittest.main()

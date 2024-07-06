"""
Description: This file contains code examples that call datetime.now() multiple times within the same function. It tests the assumption that time always monotonically increases.

Links:
- https://blog.cloudflare.com/how-and-why-the-leap-second-affected-cloudflare-dns/
"""

import sys

sys.modules["_datetime"] = None

import unittest
from datetime import datetime, timedelta

from freezegun import freeze_time


# Helper function that helps call datetime.now() interprocedurally.
def get_timestamp():
    return datetime.now()


# Helper function that simulates failure when time duration is less than or equal to zero.
def cannot_pass_le_zero(duration: int) -> bool:
    # perform some computation
    return duration > 0


class TestMultipleNows(unittest.TestCase):

    # Test that calls datetime.now() multiple times within the same function.
    def test_multiple_nows_0(self) -> None:
        timestamp1 = datetime.now()
        timestamp2 = datetime.now()
        assert timestamp1 <= timestamp2

    # Test that calls datetime.now() multiple times within the same function via a helper.
    def test_multiple_nows_1(self) -> None:
        timestamp1 = get_timestamp()
        timestamp2 = get_timestamp()
        assert timestamp1 <= timestamp2

    # Test that calls datetime.now() multiple times within the same function via a helper.
    def test_multiple_nows_2(self) -> None:
        timestamp1 = datetime.now()
        timestamp2 = get_timestamp()
        assert timestamp1 <= timestamp2

    # Test that times the execution of a function but does not perform <= 0 check.
    def test_multiple_nows_3(self) -> None:
        start_time = datetime.now()
        # perform some computation
        end_time = datetime.now()
        assert cannot_pass_le_zero((end_time - start_time).total_seconds()) == True


def run_tests():
    with freeze_time("2012-01-14") as freezer:
        original_now = datetime.now

        # Decrease the time by 1 second on each call to datetime.now()
        def monkey_patched_now():
            freezer.tick(delta=timedelta(seconds=-1))
            return original_now()

        datetime.now = monkey_patched_now

        unittest.main()


if __name__ == "__main__":
    run_tests()

"""
Description: This file contains code examples that call datetime.now() multiple times within the same function. It tests the assumption that time always monotonically increases.

Links:

"""

import time
import unittest
from datetime import datetime

from hypothesis import given
from hypothesis.strategies import floats


# Helper function that calls datetime.now().
def get_timestamp():
    return datetime.now()


class TestMultipleNows(unittest.TestCase):

    # Test that calls datetime.now() multiple times within the same function.
    @given(floats(min_value=0.0, max_value=0.1))
    def test_multiple_nows_0(self, sleep_time: float) -> None:
        timestamp1 = datetime.now()
        time.sleep(sleep_time)
        timestamp2 = datetime.now()
        assert timestamp1 <= timestamp2

    # Test that calls datetime.now() multiple times within the same function via a helper.
    @given(floats(min_value=0.0, max_value=0.1))
    def test_multiple_nows_1(self, sleep_time: float) -> None:
        timestamp1 = get_timestamp()
        time.sleep(sleep_time)
        timestamp2 = get_timestamp()
        assert timestamp1 <= timestamp2

    # Test that times the execution of a function but does not perform <= 0 check.
    # @given(integers(min_value=0, max_value=10))


if __name__ == "__main__":
    unittest.main()

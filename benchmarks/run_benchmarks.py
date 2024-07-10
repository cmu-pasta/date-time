import os
import unittest
import warnings

from freezegun import freeze_time
from hypothesis import settings

length = 70


def pretty_print(string: str):
    print("\n" + "=" * length)
    print(string)
    print("-" * length)


def get_test_suites():
    loader = unittest.TestLoader()
    suites = []

    # Iterate through all files that start with test_*.py
    pretty_print("Finding test files...")
    for file in os.listdir("."):
        if file.startswith("test_") and file.endswith(".py"):
            print(f"Found test file: {file}")
            suite = loader.discover(start_dir=".", pattern=file)
            suites.append(suite)
    return suites


def run_test_suite(suite, control_time=False):
    runner = unittest.TextTestRunner(verbosity=2)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        if control_time:
            with freeze_time("2012-01-14") as freezer:
                import sys

                sys.modules["_datetime"] = None

                from datetime import datetime, timedelta

                original_now = datetime.now

                # Decrease the time by 1 second on each call to dateime.datetime.now()
                def monkey_patched_now():
                    freezer.tick(delta=timedelta(seconds=-1))
                    return original_now()

                datetime.now = monkey_patched_now
                runner.run(suite)
        else:
            runner.run(suite)


def test_runner():
    # Register and load custom testing profile with max_examples set to 1000
    settings.register_profile("testing_profile", max_examples=1000)
    settings.load_profile("testing_profile")

    suites = get_test_suites()
    for suite in suites:
        pretty_print(f"Running test suite: {suite}")
        print("Test cases found: ", suite.countTestCases())
        print("-" * length)

        runner = unittest.TextTestRunner(verbosity=2)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            if "test_multiple_nows" in str(suite):
                run_test_suite(suite, control_time=True)
            else:
                run_test_suite(suite)


if __name__ == "__main__":
    test_runner()

import os
import unittest
import warnings
import io
import sys

from datetime import datetime, timedelta

from freezegun import freeze_time
from hypothesis import settings

length = 70


def pretty_print(string: str):
    print("\n" + "=" * length)
    print(string)
    print("-" * length)

def print_result(result: unittest.TestResult):
    print("Tests run:", result.testsRun)
    if len(result.skipped) != 0:
        print("Skipped: ", len(result.skipped))
    if len(result.expectedFailures) != 0:
        print("Expected failures: ", len(result.expectedFailures))
    if len(result.unexpectedSuccesses) != 0:
        print("Unexpected successes: ")
        for us in result.unexpectedSuccesses:
            print("-", us.id())
    fails = result.errors + result.failures
    if len(fails) != 0:
        print("Failures: ")
        for fail in fails:
            print("-", fail[0].id())
    if result.wasSuccessful():
        print("All tests passed")
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


def run_test_suite(suite, control_time=False, verbose=False):
    if verbose:
        stream = sys.stdout
    else:
        stream = io.StringIO()
    runner = unittest.TextTestRunner(stream=stream, verbosity=2)

    if control_time:
        with freeze_time("2012-01-14") as freezer:
            sys.modules["_datetime"] = None

            original_now = datetime.now

            # Decrease the time by 1 second on each call to dateime.datetime.now()
            def monkey_patched_now():
                freezer.tick(delta=timedelta(seconds=-1))
                return original_now()

            datetime.now = monkey_patched_now
            result = runner.run(suite)
    else:
        result = runner.run(suite)
    
    print_result(result)


def test_runner():
    # Register and load custom testing profile with max_examples set to 1000
    settings.register_profile("testing_profile", max_examples=1000)
    settings.load_profile("testing_profile")

    suites = get_test_suites()
    for suite in suites:
        pretty_print(f"Running test suite: {suite}")
        print("Test cases found: ", suite.countTestCases())

        if "test_multiple_nows" in str(suite):
            run_test_suite(suite, control_time=True)
        else:
            run_test_suite(suite)


if __name__ == "__main__":
    test_runner()

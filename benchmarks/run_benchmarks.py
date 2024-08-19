import argparse
import io
import os
import sys
import unittest
from datetime import datetime, timedelta

from freezegun import freeze_time
from hypothesis import settings

length = 70


def pretty_print(string: str):
    print("\n" + "=" * length)
    print(string)
    print("-" * length)


def print_result(result: unittest.TestResult, print_examples: bool = False):
    print("Tests run:", result.testsRun)
    if len(result.skipped) != 0:
        print("Skipped:", len(result.skipped))
    if len(result.expectedFailures) != 0:
        print("Expected failures:", len(result.expectedFailures))
    if len(result.unexpectedSuccesses) != 0:
        print("Unexpected successes:")
        for us in result.unexpectedSuccesses:
            print("-", us.id())
    fails = result.errors + result.failures
    if len(fails) != 0:
        print("Failures:")
        for fail in fails:
            print("-", fail[0].id())

    if print_examples:
        print("-" * length)
        for ef in result.expectedFailures:
            test_name = ef[0].id()
            print(f"### {test_name} ###")
            falsifying_count = ef[1].count("Falsifying")
            if falsifying_count == 0:
                print("No falsifying example found, printing full traceback")
                print(ef[1])
            elif falsifying_count == 1:
                starti = ef[1].find("Falsifying")
                print(ef[1][starti:])
            else:
                print("Multiple falsifying examples found, printing full traceback")
                print(ef[1])

    if result.wasSuccessful():
        print("All tests executed as expected")
    print("-" * length)


def get_test_suites() -> list[tuple[str, unittest.TestSuite]]:
    loader = unittest.TestLoader()
    suites = []

    # Iterate through all files that start with test_*.py
    pretty_print("Finding test files...")
    for file in os.listdir("."):
        if file.startswith("test_") and file.endswith(".py"):
            print(f"Found test file: {file}")
            suite = loader.discover(start_dir=".", pattern=file)
            if suite.countTestCases() != 0:
                suites.append((file, suite))
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

    print_result(result, print_examples=verbose)


def test_runner(verbose=False):
    # Register and load custom testing profile with max_examples set to 1000
    settings.register_profile("testing_profile", max_examples=1000)
    settings.load_profile("testing_profile")

    suites = get_test_suites()
    for suite in suites:
        pretty_print(f"Running test suite: {suite[0]}")

        if suite[0] == "test_multiple_nows.py":
            run_test_suite(suite[1], control_time=True, verbose=verbose)
        else:
            run_test_suite(suite[1], verbose=verbose)


if __name__ == "__main__":
    # parser
    parser = argparse.ArgumentParser(
        prog="run_benchmarks.py",
        description='Run all tests "test_*.py" in this folder.',
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Output individual test results and falsifying examples",
    )
    args = parser.parse_args()

    test_runner(verbose=args.verbose)

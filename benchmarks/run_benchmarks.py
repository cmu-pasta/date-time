# freeze datetime?
# monkey patch the system time call?

import unittest
import warnings

from hypothesis import settings

"""
import unittest

class WidgetTestCase(unittest.TestCase):
    def setUp(self):
        self.widget = Widget('The widget')

    def test_default_widget_size(self):
        self.assertEqual(self.widget.size(), (50,50),
                         'incorrect default size')

    def test_widget_resize(self):
        self.widget.resize(100,150)
        self.assertEqual(self.widget.size(), (100,150),
                         'wrong size after resize')
Note The order in which the various tests will be run is determined by sorting the test method names with respect to the built-in ordering for strings.
If the setUp() method raises an exception while the test is running, the framework will consider the test to have suffered an error, and the test method will not be executed.

Similarly, we can provide a tearDown() method that tidies up after the test method has been run:

import unittest

class WidgetTestCase(unittest.TestCase):
    def setUp(self):
        self.widget = Widget('The widget')

    def tearDown(self):
        self.widget.dispose()
If setUp() succeeded, tearDown() will be run whether the test method succeeded or not.

Such a working environment for the testing code is called a test fixture. A new TestCase instance is created as a unique test fixture used to execute each individual test method. Thus setUp(), tearDown(), and __init__() will be called once per test.

It is recommended that you use TestCase implementations to group tests together according to the features they test. unittest provides a mechanism for this: the test suite, represented by unittest’s TestSuite class. In most cases, calling unittest.main() will do the right thing and collect all the module’s test cases for you and execute them.

However, should you want to customize the building of your test suite, you can do it yourself:

def suite():
    suite = unittest.TestSuite()
    suite.addTest(WidgetTestCase('test_default_widget_size'))
    suite.addTest(WidgetTestCase('test_widget_resize'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
"""


def test_runner():
    # Register and load custom testing profile with max_examples set to 1000
    settings.register_profile("testing_profile", max_examples=1000)
    settings.load_profile("testing_profile")

    print("\n" + "=" * 20)
    print(f"Running tests...")
    print("=" * 20)

    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=".", pattern="test_*.py")
    print(f"Found {suite.countTestCases()} test cases.")

    runner = unittest.TextTestRunner(verbosity=2)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        runner.run(suite)


if __name__ == "__main__":
    test_runner()

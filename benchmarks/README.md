# Benchmark Suite

This benchmark suite provides a collection of benchmark files modeling known code bugs and smells related to the usage of date-time libraries. These benchmarks serve as an important resource for testing tools and techniques designed to detect and correct issues typical within date-time manipulation code.

The benchmarks are designed to capture subtle bugs that can arise due to corner cases in date and time computations. Hence, as a design choice, none of the test cases in the benchmark suite should pass all the assosiated assertions/properties. The test cases are parametrized and integrated into the Python `unittest` framework. The the test inputs are generated using the generators provided by the `hypothesis` library for property-based testing in Python. 

The `run_benchmarks.py` script is designed to execute all the benchmark files in this directory. To run the benchmarks, use the following command:

```bash
python run_benchmarks.py
```

The script will iterate through each benchmark file in the `benchmarks` directory, executing them and providing output based on any date-time bugs or smells detected.

To execute specific types of benchmarks, you can invoke the command:
```bash
python -W ignore::DeprecationWarning <name_of_benchmark>.py
```

Note: Some of the test cases involve controlling time. This has been achieved via monkey-patching the `datetime.now()` method with the APIs from the `freezegun` library. This can cause the testing framework and other dynamic analysis tools to function improperly with impact ranging anywhere between miscalculation of test running times to complete breakdown. To work around this, just ignore controlled test cases.
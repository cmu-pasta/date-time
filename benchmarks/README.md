# Benchmark Suite

This benchmark suite provides a collection of benchmark files modeling known code bugs and smells related to the usage of date-time libraries. These benchmarks serve as an important resource for testing tools and techniques designed to detect and correct issues typical within date-time manipulation code.


The `run_benchmarks.py` script is designed to execute all the benchmark files in this directory. To run the benchmarks, use the following command:

```bash
python run_benchmarks.py
```

The script will iterate through each benchmark file in the `benchmarks` directory, executing them and providing output based on any date-time bugs or smells detected.

TODO: Explain the testing framework (any fuzzing logic, always false assertions, any generators involved, date/time freezing/manipulation techniques used via monkey patching, executing individual benchmark files, running static/dynamic analysis on the tests)

# python -W ignore::DeprecationWarning your_test_script.py
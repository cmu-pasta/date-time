import datetime
import time

def benchmark_multiple_nows_0():
    first = datetime.datetime.now()
    sleep(0.5)
    second = datetime.datetime.now()
    assert first <= second # leap seconds

def benchmark_multiple_nows_1():
    first = datetime.datetime.now()
    second = datetime.datetime.now()
    assert first == second

def benchmark_multiple_nows_2():
    first = datetime.datetime.now()
    second = datetime.datetime.now()
    total_time = 10 / (second - first).total_seconds # division by 0
    assert total_time

def run_benchmarks_multiple_nows():
    benchmarks = [
        benchmark_multiple_nows_0,
        benchmark_multiple_nows_1,
        benchmark_multiple_nows_2
    ]
    for benchmark in benchmarks:
        benchmark()

if __name__ == "__main__":
    run_benchmarks_mulitple_nows()
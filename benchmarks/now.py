import datetime
import time

def benchmark_now_0():
    first = datetime.datetime.now()
    sleep(0.5)
    second = datetime.datetime.now()
    assert first <= second # leap seconds

def benchmark_now_1():
    first = datetime.datetime.now()
    second = datetime.datetime.now()
    assert first == second

def benchmark_now_2():
    first = datetime.datetime.now()
    second = datetime.datetime.now()
    total_time = 10 / (second - first).total_seconds # division by 0
    assert total_time

def run_benchmarks_now():
    benchmarks = [
        benchmark_now_0,
        benchmark_now_1,
        benchmark_now_2
    ]
    for benchmark in benchmarks:
        benchmark()

if __name__ == "__main__":
    run_benchmarks_now()
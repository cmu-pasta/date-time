import datetime
import time

def benchmark_now_0():
    timestamps = []
    for _ in range(100):
        timestamps.append(datetime.datetime.now())
        time.sleep(0.01)
    assert all(t1 <= t2 for t1, t2 in zip(timestamps, timestamps[1:]))

def benchmark_now_1():
    timestamp1 = datetime.datetime.now()
    timestamp2 = datetime.datetime.now()
    assert timestamp1 == timestamp2

def run_benchmarks_now():
    benchmarks = [
        benchmark_now_0,
        benchmark_now_1
    ]
    for benchmark in benchmarks:
        benchmark()

if __name__ == "__main__":
    run_benchmarks_now()
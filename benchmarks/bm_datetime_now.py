import datetime
import time

def benchmark_datetime_now_monotonic():
    timestamps = []
    for _ in range(100):
        timestamps.append(datetime.datetime.now())
        time.sleep(0.01)
    assert all(t1 <= t2 for t1, t2 in zip(timestamps, timestamps[1:])), "Datetime is not monotonic."

def benchmark_datetime_now_same_instance():
    timestamp1 = datetime.datetime.now()
    time.sleep(0.01)
    timestamp2 = datetime.datetime.now()
    assert timestamp1 != timestamp2, "Datetime instances should not be the same."

def benchmark_datetime_now_dst_shift():
    timestamps = []
    for _ in range(2):
        timestamps.append(datetime.datetime.now())
        time.sleep(3600)  # Sleep for an hour
    assert timestamps[0] < timestamps[1], "Datetime did not account for DST shift."

def benchmark_datetime_now_assumed_same():
    timestamp1 = datetime.datetime.now()
    timestamp2 = datetime.datetime.now()
    assert timestamp1 == timestamp2, "Assumed same datetime instances are actually different."

def benchmark_datetime_now_microsecond_precision():
    timestamp1 = datetime.datetime.now()
    time.sleep(0.001)  # Sleep for 1 millisecond
    timestamp2 = datetime.datetime.now()
    assert timestamp1.microsecond != timestamp2.microsecond, "Microsecond precision issue detected."

def benchmark_datetime_now_hour_change():
    initial_hour = datetime.datetime.now().hour
    time.sleep(3600)  # Sleep for an hour
    new_hour = datetime.datetime.now().hour
    assert new_hour != initial_hour, "Hour did not change after 1 hour."

def run_benchmarks():
    benchmarks = [
        benchmark_datetime_now_monotonic,
        benchmark_datetime_now_same_instance,
        benchmark_datetime_now_dst_shift,
        benchmark_datetime_now_assumed_same,
        benchmark_datetime_now_microsecond_precision,
        benchmark_datetime_now_hour_change,
    ]
    for benchmark in benchmarks:
        try:
            benchmark()
            print(f"{benchmark.__name__}: Passed")
        except AssertionError as e:
            print(f"{benchmark.__name__}: Failed - {e}")

if __name__ == "__main__":
    run_benchmarks()
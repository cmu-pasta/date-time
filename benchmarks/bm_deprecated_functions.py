import datetime
import time

def benchmark_datetime_utcnow_vs_now_utc():
    utc_now = datetime.datetime.utcnow()
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    assert utc_now == now_utc.replace(tzinfo=None), "UTCNOW() and NOW() with UTC timezone do not match."
    
def benchmark_datetime_utcoffset():
    now = datetime.datetime.now(datetime.timezone.utc)
    offset = now.utcoffset()
    assert offset == datetime.timedelta(0), "UTCOFFSET did not return zero for UTC."

def benchmark_datetime_astimezone_vs_utcastimezone():
    now = datetime.datetime.now(datetime.timezone.utc)
    utc_now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
    astimezone_now = utc_now.astimezone()
    assert astimezone_now == now, "ASTIMEZONE did not return the same result as UTCNOW with timezone."

def run_deprecated_benchmarks():
    benchmarks = [
        benchmark_datetime_utcnow_vs_now_utc,
        benchmark_datetime_utcoffset,
        benchmark_datetime_astimezone_vs_utcastimezone
    ]
    for benchmark in benchmarks:
        try:
            benchmark()
            print(f"{benchmark.__name__}: Passed")
        except AssertionError as e:
            print(f"{benchmark.__name__}: Failed - {e}")

if __name__ == "__main__":
    run_deprecated_benchmarks()
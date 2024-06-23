import datetime
from dateutil import tz

def benchmark_naive_utc_local_0():
    naive = datetime.datetime(2024, 6, 7, 23, 59, 59) # naive
    utc = datetime.datetime(2024, 6, 7, 23, 59, 59).astimezone(tz.gettz("UTC")) # UTC
    assert naive == utc
    
def benchmark_naive_utc_local_1():
    utc = datetime.datetime(2024, 6, 7, 23, 59, 59).astimezone(tz.gettz("UTC")) # UTC
    local = datetime.datetime(2024, 6, 7, 23, 59, 59).astimezone() # local
    assert utc == local
    
def benchmark_naive_utc_local_2():
    local = datetime.datetime(2024, 6, 7, 23, 59, 59).astimezone() # local
    naive = datetime.datetime(2024, 6, 7, 23, 59, 59) # naive
    assert local == naive

def run_benchmarks_naive_utc_local():
    benchmarks = [
        benchmark_naive_utc_local_0,
        benchmark_naive_utc_local_1,
        benchmark_naive_utc_local_2
    ]
    for benchmark in benchmarks:
        benchmark()

if __name__ == "__main__":
    run_benchmarks_naive_utc_local()
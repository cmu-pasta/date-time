import datetime
from dateutil import tz

tzUTC = tz.gettz("UTC")

def benchmark_naive_utc_local_0():
    naive = datetime.datetime(2024, 6, 7, 23, 59, 59) # naive
    utc = datetime.datetime(2024, 6, 7, 23, 59, 59).astimezone(tzUTC) # UTC
    assert naive == utc
    
def benchmark_naive_utc_local_1():
    utc = datetime.datetime(2024, 6, 7, 23, 59, 59).astimezone(tzUTC) # UTC
    local = datetime.datetime(2024, 6, 7, 23, 59, 59).astimezone() # local
    assert utc == local
    
def benchmark_naive_utc_local_2():
    local = datetime.datetime(2024, 6, 7, 23, 59, 59).astimezone() # local
    naive = datetime.datetime(2024, 6, 7, 23, 59, 59) # naive
    assert local == naive
    
def benchmark_naive_utc_local_3():
    naive = datetime.datetime(2024, 6, 7, 23, 59, 59) # naive
    utc = datetime.datetime(2024, 6, 7, 23, 59, 59).astimezone(tzUTC) # UTC
    delta = naive - utc
    zero = datetime.timedelta(seconds=0)
    assert delta == zero
    
def benchmark_naive_utc_local_4():
    utc = datetime.datetime(2024, 6, 7, 23, 59, 59).astimezone(tz.gettz("UTC")) # UTC
    local = datetime.datetime(2024, 6, 7, 23, 59, 59).astimezone() # local
    delta = utc - local
    zero = datetime.timedelta(seconds=0)
    assert delta == zero # note that this actually passes
    
def benchmark_naive_utc_local_5():
    local = datetime.datetime(2024, 6, 7, 23, 59, 59).astimezone() # local
    naive = datetime.datetime(2024, 6, 7, 23, 59, 59) # naive
    delta = local - naive
    zero = datetime.timedelta(seconds=0)
    assert delta == zero
    
def benchmark_naive_utc_local_6():
    naive = datetime.datetime(2024, 6, 7, 23, 59, 59) # naive
    utc = datetime.datetime(2024, 6, 7, 23, 59, 59).astimezone(tzUTC) # UTC
    assert naive.hour == utc.hour
    
def benchmark_naive_utc_local_7():
    utc = datetime.datetime(2024, 6, 7, 23, 59, 59).astimezone(tzUTC) # UTC
    local = datetime.datetime(2024, 6, 7, 23, 59, 59).astimezone() # local
    assert utc.hour == local.hour
    
def benchmark_naive_utc_local_8():
    local = datetime.datetime(2024, 6, 7, 23, 59, 59).astimezone() # local
    naive = datetime.datetime(2024, 6, 7, 23, 59, 59) # naive
    assert local.hour == naive.hour

def run_benchmarks_naive_utc_local():
    benchmarks = [
        benchmark_naive_utc_local_0,
        benchmark_naive_utc_local_1,
        benchmark_naive_utc_local_2,
        benchmark_naive_utc_local_3,
        benchmark_naive_utc_local_4,
        benchmark_naive_utc_local_5,
        benchmark_naive_utc_local_6,
        benchmark_naive_utc_local_7,
        benchmark_naive_utc_local_8
    ]
    for benchmark in benchmarks:
        benchmark()

if __name__ == "__main__":
    run_benchmarks_naive_utc_local()
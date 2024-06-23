import datetime
from dateutil import tz

tzNYC = tz.gettz("America/New_York")
tzUTC = tz.gettz("UTC")
    
def benchmark_arithmetic_0():
    now = datetime.datetime.now().astimezone(tzNYC)
    tomorrow = now + datetime.timedelta(days=1)
    assert (tomorrow - now) == (tomorrow.astimezone(tzUTC) - now.astimezone(tzUTC))

def benchmark_arithmetic_1():
    now = datetime.datetime.now().astimezone(tzNYC)
    tomorrow = now + datetime.timedelta(days=1)
    assert now.hour == tomorrow.hour
    
def benchmark_arithmetic_2():
    now = datetime.datetime.now()
    a_bit_later = now + (datetime.timedelta(hours=5) * 1.5)
    assert (a_bit_later.astimezone(tzUTC) - now.astimezone(tzUTC)).total_seconds % 60 == 0 # assuming integer number of hours diff
    
def benchmark_arithmetic_3():
    now = datetime.datetime.now()
    a_bit_later = now + (datetime.timedelta(hours=5) / 2)
    assert (a_bit_later.astimezone(tzUTC) - now.astimezone(tzUTC)).total_seconds % 60 == 0 # assuming integer number of hours diff
    
def run_benchmarks_naive_utc_local():
    benchmarks = [
        benchmark_arithmetic_0,
        benchmark_arithmetic_1,
        benchmark_arithmetic_2,
    ]
    for benchmark in benchmarks:
        benchmark()

if __name__ == "__main__":
    run_benchmarks_naive_utc_local()
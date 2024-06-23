import datetime
from dateutil import tz

tzNYC = tz.gettz("America/New_York")
tzUTC = tz.gettz("UTC")
    
def benchmark_arithmetic_0():
    now = datetime.datetime.now().astimezone(tzNYC)
    tomorrow = now + timedelta(days=1)
    assert (tomorrow - now) == (tomorrow.astimezone(tzUTC) - now.astimezone(tzUTC))

def benchmark_arithmetic_0():
    now = datetime.datetime.now().astimezone(tzNYC)
    tomorrow = now + timedelta(days=1)
    assert (tomorrow - now) == (tomorrow.astimezone(tzUTC) - now.astimezone(tzUTC))

def run_benchmarks_naive_utc_local():
    benchmarks = [
        benchmark_arithmetic_0,
    ]
    for benchmark in benchmarks:
        benchmark()

if __name__ == "__main__":
    run_benchmarks_naive_utc_local()
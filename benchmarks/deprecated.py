import datetime
from dateutil import tz
import time

# TODO: add a thing for pytz

def benchmark_deprecated_0():
    utc_now_old = datetime.datetime.utcnow()
    utc_now_new = datetime.datetime.now(tz=tz.gettz("UTC"))
    assert utc_now_old == utc_now_new
    
def benchmark_deprecated_1():
    dt_utc_old = datetime.datetime.utcfromtimestamp(1000000000)
    dt_utc_new = datetime.datetime.fromtimestamp(1000000000).astimezone(tz.gettz("UTC"))
    assert dt_utc_old == dt_utc_new

def run_benchmarks_deprecated():
    benchmarks = [
        benchmark_deprecated_0,
        benchmark_deprecated_1
    ]
    for benchmark in benchmarks:
        benchmark()

if __name__ == "__main__":
    run_benchmarks_deprecated()
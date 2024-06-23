import datetime
from dateutil import tz
import pytz
import time

tzUTC = tz.gettz("UTC")
tzNYC = tz.gettz.timezone("America/New_York")
tzNYC_pytz = pytz.timezone("America/New_York")

def benchmark_deprecated_0():
    utc_now_old = datetime.datetime.utcnow()
    utc_now_new = datetime.datetime.now(tz=tzUTC)
    assert utc_now_old == utc_now_new
    
def benchmark_deprecated_1():
    dt_utc_old = datetime.datetime.utcfromtimestamp(1000000000)
    dt_utc_new = datetime.datetime.fromtimestamp(1000000000).astimezone(tzUTC)
    assert dt_utc_old == dt_utc_new

def benchmark_deprecated_2():
    now_du = datetime.datetime.now(tz=tzNYC)
    now_pytz = datetime.datetime.now(tz=tzNYC_pytz)
    tomorrow_du = now_du + timedelta(days=1)
    tomorrow_pytz = now_pytz + timedelta(days=1) # adding timedelta without normalizing
    assert tomorrow_du == tomorrow_pytz


def run_benchmarks_deprecated():
    benchmarks = [
        benchmark_deprecated_0,
        benchmark_deprecated_1,
        benchmark_deprecated_2
    ]
    for benchmark in benchmarks:
        benchmark()

if __name__ == "__main__":
    run_benchmarks_deprecated()
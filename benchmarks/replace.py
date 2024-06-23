import datetime
from dateutil import tz

tzNYC = tz.gettz("America/New_York")
tzUTC = tz.gettz("UTC")
tzNaTZ = tz.gettz("Not A Timezone")

def benchmark_replace_0():
    now = datetime.datetime.now()
    invalid_hour = now.replace(hour=25)
    assert now.hour == 25

def benchmark_replace_1():
    now = datetime.datetime.now()
    invalid_day = now.replace(day=32)
    assert now.day == 32

def benchmark_replace_2():
    now = datetime.datetime.now()
    invalid_month = now.replace(month=13)
    assert now.month == 13

def benchmark_replace_3():
    now = datetime.datetime.now(tz=tzUTC)
    nonexistent_timezone = now.replace(tz=tzNaTZ)
    assert now.tzinfo == tzNaTZ

def benchmark_replace_4():
    now = datetime.datetime.now(tz=tzNYC)
    shifted = datetime.datetime(now.year, now.month, now.day, 5, tzinfo=now.tzinfo).astimezone(tzNYC)
    assert now.tzinfo == shifted.tzinfo

def run_benchmarks_replace():
    benchmarks = [
        benchmark_replace_0,
        benchmark_replace_1,
        benchmark_replace_2,
        benchmark_replace_3,
        benchmark_replace_4
    ]
    for benchmark in benchmarks:
        benchmark()

if __name__ == "__main__":
    run_benchmarks_replace()
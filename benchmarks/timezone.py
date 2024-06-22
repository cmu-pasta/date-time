import datetime
from dateutil import tz

def benchmark_timezone_0():
    tzEST = tz.gettz('EST')
    tzNYC = tz.gettz('America/New_York')
    nowEST = datetime.datetime.now(tz=tzEST)
    nowNYC = datetime.datetime.now(tz=tzNYC)
    assert nowEST.hour == nowNYC.hour
    
def benchmark_timezone_1():
    tzEST = tz.gettz(datetime.timedelta(hours=-5))
    tzNYC = tz.gettz('America/New_York')
    nowEST = datetime.datetime.now(tz=tzEST)
    nowNYC = datetime.datetime.now(tz=tzNYC)
    assert nowEST.hour == nowNYC.hour

def run_benchmarks_timezone():
    benchmarks = [
        benchmark_timezone_EST,
        benchmark_timezone_offset,
    ]
    for benchmark in benchmarks:
        benchmark()

if __name__ == "__main__":
    run_benchmarks_timezone()
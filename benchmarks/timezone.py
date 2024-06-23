import datetime
from dateutil import tz

tzNYC = tz.gettz('America/New_York')
tzEST = tz.gettz('EST')
tzEST_offset = datetime.timezone(datetime.timedelta(hours=-5))

def benchmark_timezone_0():
    nowEST = datetime.datetime.now(tz=tzEST)
    nowNYC = datetime.datetime.now(tz=tzNYC)
    assert nowEST.hour == nowNYC.hour
    
def benchmark_timezone_1():
    nowEST_offset = datetime.datetime.now(tz=tzEST_offset)
    nowNYC = datetime.datetime.now(tz=tzNYC)
    assert nowEST_offset.hour == nowNYC.hour

def run_benchmarks_timezone():
    benchmarks = [
        benchmark_timezone_0,
        benchmark_timezone_1
    ]
    for benchmark in benchmarks:
        benchmark()

if __name__ == "__main__":
    run_benchmarks_timezone()
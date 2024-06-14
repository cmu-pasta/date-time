import datetime
from dateutil import tz

def benchmark_timezone_EST():
    tzEST = tz.gettz('EST')
    tzNYC = tz.gettz('America/New_York')
    nowEST = datetime.datetime.now(tz=tzEST)
    nowNYC = datetime.datetime.now(tz=tzNYC)
    assert nowEST.hour == nowNYC.hour, "EST and America/New York are not the same timezone"
    print(f"benchmark_timezone_EST: Passed")
    
def benchmark_timezone_offset():
    tzEST = tz.gettz(datetime.timedelta(hours=-5))
    tzNYC = tz.gettz('America/New_York')
    nowEST = datetime.datetime.now(tz=tzEST)
    nowNYC = datetime.datetime.now(tz=tzNYC)
    assert nowEST.hour == nowNYC.hour, "offset -5 and America/New York are not the same timezone"
    print(f"benchmark_timezone_offset: Passed")

def run_timezone_typing_benchmarks():
    benchmarks = [
        benchmark_timezone_EST,
        benchmark_timezone_offset,
    ]
    for benchmark in benchmarks:
        benchmark()

if __name__ == "__main__":
    run_timezone_typing_benchmarks()
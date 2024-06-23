import datetime
from dateutil import tz

tzNYC = tz.gettz("America/New_York")
tzEST = tz.gettz("EST")
tzUTC = tz.gettz("UTC")
tzEST_offset = datetime.timezone(datetime.timedelta(hours=-5))

def benchmark_timezone_0():
    nowEST = datetime.datetime.fromtimestamp(1000000000).astimezone(tzEST)
    nowNYC = datetime.datetime.fromtimestamp(1000000000).astimezone(tzNYC)
    assert nowEST.hour == nowNYC.hour
    
def benchmark_timezone_1():
    nowEST_offset = datetime.datetime.fromtimestamp(1000000000).astimezone(tzEST_offset)
    nowNYC = datetime.datetime.fromtimestamp(1000000000).astimezone(tzNYC)
    assert nowEST_offset.hour == nowNYC.hour

def benchmark_timezone_2():
    first = datetime.datetime.fromtimestamp(1000000000).astimezone(tzNYC)
    second = datetime.datetime.fromtimestamp(1000000000).astimezone(tzUTC)
    tzOFF = datetime.timezone(second - first) # create timezone from current timezone differences
    now = datetime.datetime.now()
    nowNYC = now.astimezone(tzNYC)
    nowOFF = now.astimezone(tzOFF)
    assert nowNYC.hour == nowOFF.hour

def run_benchmarks_timezone():
    benchmarks = [
        benchmark_timezone_0,
        benchmark_timezone_1,
        benchmark_timezone_2
    ]
    for benchmark in benchmarks:
        benchmark()

if __name__ == "__main__":
    run_benchmarks_timezone()
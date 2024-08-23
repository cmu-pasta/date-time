from datetime import *

# Not targetting it right now since, it is commonly used for basic operations... maybe noisy
a = datetime.now()
a1 = datetime.now(tz=None)
a2 = datetime.now(timezone.utc)
a3 = datetime.now(tz=timezone.utc)

b = datetime.fromtimestamp(1000)
b2 = datetime.fromtimestamp(1000, tz=None)
b3 = datetime.fromtimestamp(1000, None)
b4 = datetime.fromtimestamp(1000, tz=timezone.utc)
tz_info = timezone.utc
b5 = datetime.fromtimestamp(1000, tz_info)
b6 = datetime.fromtimestamp(1000, tz=tz_info)

c = datetime(2024, 6, 7)
c1 = datetime(2024, 6, 7, tzinfo=None)
c2 = datetime(2024, 6, 7, tzinfo=timezone.utc)

c = datetime.datetime(2024, 6, 7)
c1 = datetime.datetime(2024, 6, 7, tzinfo=None)
c2 = datetime.datetime(2024, 6, 7, tzinfo=timezone.utc)

d = time(12, 30, 45)
d1 = time(12, 30, 45, tzinfo=None)
d2 = time(12, 30, 45, tzinfo=timezone.utc)

d = datetime.time(12, 30, 45)
d1 = datetime.time(12, 30, 45, tzinfo=None)
d2 = datetime.time(12, 30, 45, tzinfo=timezone.utc)


# Will target this as part of a different query.
date_string = "2023-10-05 14:30:45"
naive_dt_from_string = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
aware_dt_from_string = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S").replace(
    tzinfo=timezone.utc
)

dt_string = "2023-08-22 14:30:00-0400"
dt = datetime.strptime(dt_string, "%Y-%m-%d %H:%M:%S%z")

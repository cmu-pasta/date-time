"""
1) https://github.com/scrapinghub/dateparser/pull/1086/files

Creating datetimes with some constant and some variable parameters.
E.g., datetime(2024, a, b, c, ...)
Also consider, potentially all being variables.
E.g., d=2024; datetime(d, a, b, c, ...)


2) https://github.com/sdispater/pendulum/issues/686

2-digit year. Not sure how to make a benchmark for this.
E.g., 85 was interpreted as 2085 instead of 1985.

3) https://github.com/KoffeinFlummi/Chronyk/issues/5

Adding X months to current date without checking if the new date exists.
E.g., Jan 31 + 1 Month = Feb 31 !!!

4) https://github.com/scrapinghub/dateparser/issues/403

Check if time is after current time but in UTC instead of local timezone.
E.g., When is the next 2pm? If you use UTC instead of local tz but the
same time, you'll get a different answer.

5) https://github.com/pyopenapi/pyswagger/issues/83

Failing to parse ms/us portion of a datetime.
Failing to parse tz.
Failing to parse tz only when usecs are present?
Etc.
E.g., parse("2016-08-05T03:14:14.809Z") => dt(2016, 8, 5, 3, 14, 14)

6) https://github.com/GoogleCloudPlatform/professional-services-data-validator/issues/1053

Parsing huge datetimes.
E.g., parse("9999-12-31T23:59:59.999999") => error

"""
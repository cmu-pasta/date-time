"""
1) https://github.com/kayak/pypika/issues/152

Bad regex. 100 seconds is interpreted as 1 second

2) https://github.com/jdemaeyer/brightsky/issues/101

Bad isoparse. The URL didn't percent encode + to %2b. 

3) https://github.com/python-humanize/humanize/issues/17

Subtracting tz-aware and naive datetimes.
Create a dt creation source with a 'localize' barrier and a '-' sink. 


"""
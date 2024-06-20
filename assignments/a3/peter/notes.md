Something I was worried about when testing these was that it seemed like my code would miss a lot of things that should obviously hit. For example, in `is_timestamp.ql`, there was a section where it would find the first line but no the other lines of the following code:

```
(arrow/test/test_util.py line 43)

assert util.is_timestamp(timestamp_int)
assert util.is_timestamp(timestamp_float)
assert util.is_timestamp(str(timestamp_int))
assert util.is_timestamp(str(timestamp_float))

assert not util.is_timestamp(True)
assert not util.is_timestamp(False)
```

Based on a bit of testing with other code, I think what's happening here is that CodeQL only matches on the first match per block. So while it won't catch every instance of an error at the start, it will usually find each distinct buggy section. In addition, the query matching on nothing still means no matches.

The UTC call one I was messing around with a bunch because arrow defines a function called `is_timestamp`, which I was matchin on more than the actual function. I'm pretty sure `Value::named` is the correct way to refer to a specific object like this, but as far as I can tell, CodeQL can't resolve the module path a lot of the time and so I think matching on "a function or method named utcnow" is as good as I can get it.

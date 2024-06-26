/**
 * @id py/examples/bad-utc-call
 * @name Bad UTC call
 * @description Find calls to utcnow and utcfromtimestamp
 */

import python

// find calls to finctions named "utcnow" and "utcfromtimestamp"
// from Call call, FunctionValue fun
// where call.getFunc().pointsTo(fun) and ((fun.getName() = "utcnow") or (fun.getName() = "utcfromtimestamp"))
// select call, "Functions utcnow and utcfromtimestamp use non-timestamped UTC and should not be used"

// find calls to things like ___.utcnow() or utcnow()
from Call call, Attribute attr, FunctionValue fun
where (call.getFunc() = attr and (attr.getName() = "utcnow" or attr.getName() = "utcfromtimestamp"))
    or call.getFunc().pointsTo(fun) and ((fun.getName() = "utcnow") or (fun.getName() = "utcfromtimestamp"))
select call, "Functions utcnow and utcfromtimestamp use non-timestamped UTC and should not be used"

// // find calls to specifically the functions from the date time library
// from Attribute attr
// // where call.getFunc().pointsTo(Value::named("datetime.datetime.utcnow"))
// where e.pointsTo(Value::named("calendar.timegm"))
// where attr.toString() = "calendar.timegm"
// where attr.getName() = "timegm"
// select attr, attr.pointsTo().toString()

// select Value::named("datetime.utcnow")
/**
 * @name deprecated method
 * @description Deprecated methods are dangerous and can cause silent failures.
 * @kind problem
 * @tags 
 * @problem.severity recommendation
 * @sub-severity high
 * @precision high
 * @id py/deprecated-method
 */

import python

// find calls to things like ___.utcnow() or utcnow()
from Call call, Attribute attr, FunctionValue fun
where 
    (call.getFunc() = attr and (attr.getName() = "utcnow" or attr.getName() = "utcfromtimestamp")) 
    or 
    call.getFunc().pointsTo(fun) and ((fun.getName() = "utcnow") or (fun.getName() = "utcfromtimestamp"))
select call, "Functions utcnow and utcfromtimestamp use non-timestamped UTC and should not be used"

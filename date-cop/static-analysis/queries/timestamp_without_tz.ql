/**
 * @name Block datetime.now without tz argument
 * @description Prevent usage of datetime.now without specifying a timezone.
 * @kind problem
 * @tags
 *   - naive-datetime
 * @problem.severity recommendation
 * @sub-severity high
 * @precision high
 * @id py/block-datetime-now-no-tz
 */

import python

from Call call
where
  call.getFunc() instanceof Attribute and ((Attribute)call.getFunc()).getName() = "fromtimestamp" and
  not (exists(call.getPositionalArg(0)) or exists(call.getNamedArg(0)))
select call, "datetime.now() must have a tz argument."


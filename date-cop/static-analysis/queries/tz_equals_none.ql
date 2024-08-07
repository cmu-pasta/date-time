/**
 * @name Block datetime.now without tz argument
 * @description Prevent usage of datetime.now with tz=None.
 * @kind problem
 * @tags
 *   - naive-datetime
 * @problem.severity recommendation
 * @sub-severity high
 * @precision high
 * @id py/block-datetime-now-no-tz
 */

import python

from Call c, None n
where
  (
    ((Attribute)c.getFunc()).getName() = "now" or
    ((Attribute)c.getFunc()).getName() = "fromtimestamp" or
    c.getFunc().toString() = "datetime"
  ) and
  (
    c.getANamedArg().contains(n) or
    (
      ((Attribute)c.getFunc()).getName() = "fromtimestamp" and
      not exists(c.getPositionalArg(1))
    ) or
    (
      not ((Attribute)c.getFunc()).getName() = "fromtimestamp" and
      not exists(c.getANamedArg())
    )
  )
select c, "datetime.now() must have a tz argument."


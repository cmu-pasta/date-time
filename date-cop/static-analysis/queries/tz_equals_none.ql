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

from AssignExpr_ a
where
  a.getTarget().toString() = "tz" and
  a.getValue() instanceof None
select a, "datetime.now() must have a tz argument."


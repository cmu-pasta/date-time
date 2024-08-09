/**
 * @name Block pytz in tzinfo field
 * @description Prevent passing a pytz timezone into the tzinfo field of now, datetime or fromtimestamp
 * @kind problem
 * @tags
 *   - timezone
 * @problem.severity recommendation
 * @sub-severity high
 * @precision high
 * @id py/block-pytz-in-tzinfo
 */

import python

from Call c, AssignStmt set_var, Attribute pytz_call
where
  c.getANamedArg().contains(pytz_call) and
  pytz_call.getObject().toString() = "pytz" and
  (
    ((Attribute)c.getFunc()).getName() = "now" or
    ((Attribute)c.getFunc()).getName() = "fromtimestamp" or
    ((Attribute)c.getFunc()).getName() = "datetime" or
    c.getFunc().toString() = "datetime"
  )
select c, "pytz timezones must be initialized with localize, not by passing the timezone into tzinfo"
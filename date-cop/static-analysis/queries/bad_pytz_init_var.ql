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

from Call c, AssignStmt set_var, Name var1, Name var2, Attribute pytz_call
where
  pytz_call.getObject().toString() = "pytz" and
  (
    ((Attribute)c.getFunc()).getName() = "now" or
    ((Attribute)c.getFunc()).getName() = "fromtimestamp" or
    c.getFunc().toString() = "datetime"
  ) and
  set_var.getValue().contains(pytz_call) and
  set_var.getATarget() = var1 and
  c.getANamedArg().contains(var2) and 
  var1.getId() = var2.getId()
select c, "pytz timezones must be initialized with localize, not by passing the timezone into tzinfo"


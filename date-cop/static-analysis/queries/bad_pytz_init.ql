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

from Call c, Attribute pytz_call
where
  (
    ((Attribute)c.getFunc()).getName() = "now" or
    ((Attribute)c.getFunc()).getName() = "fromtimestamp" or
    c.getFunc().toString() = "datetime"
  ) and
  pytz_call.getObject().toString() = "pytz" and
  c.getANamedArg().contains(pytz_call) 
select c, "pytz timezones must be initialized with localize, not by passing the timezone into tzinfo"
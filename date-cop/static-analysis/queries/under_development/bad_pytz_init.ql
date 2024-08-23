/**
 * @id py/block-pytz-in-tzinfo
 * @description Prevent passing a pytz timezone into the tzinfo field of now, datetime or fromtimestamp
 * @kind problem
 * @tags
 *   - correctness
 *   - timezone
 * @problem.severity warning
 * @precision high
 */

import python

from Call c, Attribute pytz_call, Name pytz
where
  pytz.toString() = "pytz" and
  c.getANamedArg().contains(pytz_call) and
  pytz = pytz_call.getObject() and
  (
    ((Attribute)c.getFunc()).getName() = "now" or
    ((Attribute)c.getFunc()).getName() = "fromtimestamp" or
    ((Attribute)c.getFunc()).getName() = "datetime" or
    c.getFunc().toString() = "datetime"
  )
select c, "pytz timezones must be initialized with localize, not by passing the timezone into tzinfo"
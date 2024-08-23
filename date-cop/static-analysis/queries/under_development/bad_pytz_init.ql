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

class BadPytzInitCall extends Call{
  Attribute pytz_call;
  Name pytz;
  BadPytzInitCall() {
    pytz.toString() = "pytz" and
    this.getANamedArg().contains(pytz_call) and
    pytz = pytz_call.getObject() and
    pytz_call.getName() != "utc" and
    (
      ((Attribute)this.getFunc()).getName() = "now" or
      ((Attribute)this.getFunc()).getName() = "fromtimestamp" or
      ((Attribute)this.getFunc()).getName() = "datetime" or
      this.getFunc().toString() = "datetime"
    )
  }
}

from BadPytzInitCall c
select c, "pytz timezones must be initialized with localize, not by passing the timezone into tzinfo"
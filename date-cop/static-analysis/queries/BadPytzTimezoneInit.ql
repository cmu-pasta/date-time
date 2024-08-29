/**
 * @id py/bad-pytz-timezone-init
 * @description Prevent passing a pytz timezone into the tzinfo field of now, datetime or fromtimestamp
 * @kind problem
 * @tags
 *   - correctness
 *   - timezone
 * @problem.severity error
 * @precision high
 */

import python
import semmle.python.ApiGraphs
import semmle.python.dataflow.new.DataFlow

 
class DatetimeCreation extends Call{
  DatetimeCreation() {
    (
      ((Attribute)this.getFunc()).getName() = "now" or
      ((Attribute)this.getFunc()).getName() = "fromtimestamp" or
      ((Attribute)this.getFunc()).getName() = "datetime" or
      this.getFunc().toString() = "datetime"
    )
  }
}

from DatetimeCreation c, DataFlow::CallCfgNode pytz_call, Expr tzarg
where
  pytz_call = API::moduleImport("pytz").getMember("timezone").getACall() and
  c.getANamedArg().contains(tzarg) and 
  DataFlow::localFlow(pytz_call, DataFlow::exprNode(tzarg))
select c, "Datetime objects using Pytz timezones must be initialized using the localize method."

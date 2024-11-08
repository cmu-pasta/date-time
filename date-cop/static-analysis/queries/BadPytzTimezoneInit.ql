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
      ((Attribute)this.getFunc()).getName() = "datetime" or
      this.getFunc().toString() = "datetime"
  }
}

class ReplaceCall extends Call{
  ReplaceCall(){
    ((Attribute)this.getFunc()).getName() = "replace"
  }
}

from DatetimeCreation c, DataFlow::CallCfgNode pytz_call, Expr tzarg, ReplaceCall rc
where
  pytz_call = API::moduleImport("pytz").getMember("timezone").getACall() and
  (
    (
      c.getANamedArg().contains(tzarg) and 
      DataFlow::localFlow(pytz_call, DataFlow::exprNode(tzarg))
    ) 
    
    // Not working for now :(
    or
    DataFlow::localFlow(pytz_call, DataFlow::exprNode(rc))
  )

select c, "Datetime objects using Pytz timezones must be initialized using the localize method."

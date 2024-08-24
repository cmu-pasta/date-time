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
import semmle.python.dataflow.new.DataFlow
import semmle.python.ApiGraphs
 
class DtConstructor extends Call{
  DtConstructor() {
    (
      ((Attribute)this.getFunc()).getName() = "now" or
      ((Attribute)this.getFunc()).getName() = "fromtimestamp" or
      ((Attribute)this.getFunc()).getName() = "datetime" or
      this.getFunc().toString() = "datetime"
    )
  }
}

from DtConstructor c, DataFlow::CallCfgNode pytz_call, Expr tzarg
where
  pytz_call = API::moduleImport("pytz").getMember("timezone").getACall() and
  c.getANamedArg().contains(tzarg) and 
  DataFlow::localFlow(pytz_call, DataFlow::exprNode(tzarg))
select c, "pytz timezones must be initialized with localize, not by passing the timezone into tzinfo"
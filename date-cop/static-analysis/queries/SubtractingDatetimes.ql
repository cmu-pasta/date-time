/**
 * @id py/subtracting-datetimes
 * @description Subtraction operators are not DST conserving.
 * @kind problem
 * @tags
 *   - code-smell
 *   - duration
 * @problem.severity warning
 * @precision high
 */

import python
import semmle.python.ApiGraphs
import semmle.python.dataflow.new.DataFlow

class DatetimeCreation extends DataFlow::CallCfgNode {
  DatetimeCreation() {
    this = API::moduleImport("datetime").getMember("datetime").getACall() or
    this = API::moduleImport("datetime").getMember("time").getACall() or
    this = API::moduleImport("datetime").getMember("datetime").getMember("now").getACall() or
    this = API::moduleImport("datetime").getMember("datetime").getMember("fromtimestamp").getACall()
  }
}

// from DataFlow::CallCfgNode dtc1, BinaryExpr sub
// where
//     dtc1 = API::moduleImport("datetime").getMember("datetime").getACall() and
//     sub.getOp() instanceof Sub and
//     DataFlow::localFlow(dtc1, DataFlow::exprNode(sub.getLeft()))
// select sub.getLeft(), "Subtraction of datetimes can result in unexpected durations."

from DatetimeCreation dtc1, DatetimeCreation dtc2, BinaryExpr sub
where
    sub.getOp() instanceof Sub and
    DataFlow::localFlow(dtc1, DataFlow::exprNode(sub.getLeft())) and
    DataFlow::localFlow(dtc2, DataFlow::exprNode(sub.getRight()))
select sub, "Datetime subtraction can result in unexpected durations."

// from BinaryExpr sub
// where
//     sub.getOp() instanceof Sub and
//     sub.getLocation().toString().matches("%codeql_queries%")
// select sub, "Subtraction of datetimes can result in unexpected durations."

// from DatetimeCreation dtc
// where
//     dtc.getLocation().toString().matches("%codeql_queries%")
// select dtc, "Datetime creation."
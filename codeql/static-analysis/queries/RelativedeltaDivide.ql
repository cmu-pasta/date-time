/**
 * @id py/relativedelta-divide
 * @description Dividing relativedeltas can result in unexpected durations.
 * @kind problem
 * @tags
 *   - code-smell
 *   - duration
 * @problem.severity recommendation
 * @precision high
 */

 import python
 import semmle.python.ApiGraphs
 import semmle.python.dataflow.new.DataFlow

from DataFlow::CallCfgNode rd, BinaryExpr div
where
	rd = API::moduleImport("dateutil").getMember("relativedelta").getMember("relativedelta").getACall() and
	div.getOp() instanceof Div and
	DataFlow::localFlow(rd, DataFlow::exprNode(div.getLeft()))
select div.getLeft(), "Division of durations constructed with dateutil.relativedelta should be done with care."

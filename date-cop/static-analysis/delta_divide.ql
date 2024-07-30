/**
 * @name delta divide
 * @description Dividing deltas can result in unintended behavior.
 * @kind problem
 * @tags
 * @problem.severity recommendation
 * @sub-severity high
 * @precision high
 * @id py/delta-divide
 */


import python

from BinaryExpr div, Call td, Attribute attr
where
	div.getOp() instanceof Div and

	td = div.getLeft() and
	td.getFunc() = attr and
	attr.getName() = "timedelta"
select div, "Division of timedelta."


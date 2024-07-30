/**
 * @name deprecated method
 * @description Multiplying deltas by floats can result in unintended behavior.
 * @kind problem
 * @tags
 * @problem.severity recommendation
 * @sub-severity high
 * @precision high
 * @id py/delta-times-float
 */


import python

from BinaryExpr div, Call td, FloatLiteral fl, Attribute attr
where
	div.getOp() instanceof Div and

	td = div.getLeft() and
	td.getFunc() = attr and
	attr.getName() = "timedelta"
select div, "Division of timedelta."


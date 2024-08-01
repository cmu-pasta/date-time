/**
 * @name delta times float
 * @description Multiplying deltas by floats can result in unintended behavior.
 * @kind problem
 * @tags
 * @problem.severity recommendation
 * @sub-severity high
 * @precision high
 * @id py/delta-times-float
 */


import python

from BinaryExpr mult, Call td, FloatLiteral fl, Attribute attr
where
	mult.getOp() instanceof Mult and

	td = mult.getLeft() and
	td.getFunc() = attr and
	attr.getName() = "timedelta" and

	fl = mult.getRight()
select mult, "Multiplication of timedelta by float."


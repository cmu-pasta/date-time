/**
 * @name multiple nows
 * @description Calling now() multiple times within a block can cause unexpected behavior.
 * @kind problem
 * @tags
 * @problem.severity recommendation
 * @sub-severity high
 * @precision high
 * @id py/multiple-nows
 */

import python

from Call now1, Call now2, AstNode scope
where

	(
		now1.getFunc().toString() = "now"
		or
		(now1.getFunc() instanceof Attribute and
		((Attribute)now1.getFunc()).getName() = "now")
	) and

	(
		now2.getFunc().toString() = "now"
		or
		(now2.getFunc() instanceof Attribute and
		((Attribute)now2.getFunc()).getName() = "now")
	) and

	now1 != now2 and

// This will fail to detect nows that aren't \
// on the _exact_ same level. E.g.:
//
// a = datetime.now()
// if True:
//   b = datetime.now()

	scope.containsInScope(now1) and
	scope.containsInScope(now2)

select now2, "Multiple datetime.nows." 

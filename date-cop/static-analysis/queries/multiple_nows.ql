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

predicate isNowOrGetTimestamp(Call call) {
	call.getFunc().toString() = "now"
	or
	(call.getFunc() instanceof Attribute and
	((Attribute)call.getFunc()).getName() = "now")
	or
	call.getFunc().toString() = "get_timestamp"
	or
	(call.getFunc() instanceof Attribute and
	((Attribute)call.getFunc()).getName() = "get_timestamp")
}

from Call now1, Call now2, AstNode scope
where
	isNowOrGetTimestamp(now1) and
	isNowOrGetTimestamp(now2) and
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

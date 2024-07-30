/**
 * @name timezone offset
 * @description Timezones with offsets don't account for DST.
 * @kind problem
 * @tags
 * @problem.severity recommendation
 * @sub-severity high
 * @precision high
 * @id py/timezone-offset
 */

import python

from Call td, Call tz
where
  // creates timedelta
	td.getFunc() instanceof Attribute and
	((Attribute)td.getFunc()).getName() = "timedelta" and

  // creates timezone
	tz.getFunc() instanceof Attribute and
	((Attribute)tz.getFunc()).getName() = "timezone" and

	tz.getArg(0) = td

select tz, "Timezone with a fixed offset." 

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

from Call td, Call tz, StringLiteral str
where
  // creates timedelta
	(
		td.getFunc().toString() = "timedelta"
		or
		(td.getFunc() instanceof Attribute and
		((Attribute)td.getFunc()).getName() = "timedelta")
	) and

  // creates timezone
	(
		tz.getFunc().toString() = "timezone"
		or
		(tz.getFunc() instanceof Attribute and (
			((Attribute)tz.getFunc()).getName() = "timezone" or	
			((Attribute)tz.getFunc()).getName() = "ZoneInfo" or
		((Attribute)tz.getFunc()).getName() = "gettz"))
	) and

	// THESE TAKE A VERY LONG TIME!!!
	// UTC is okay
	// str.getText() != "UTC" and
	// E.g., "America/New York" is okay but "EST" is not.
	// Better to actually create a list of bad tzs.
	// str.getText().length() < 4 and

	((tz.getArg(0) = td) or (tz.getArg(0) = str))

select tz, "Timezone with a fixed offset." 

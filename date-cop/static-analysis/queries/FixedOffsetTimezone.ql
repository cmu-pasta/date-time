/**
 * @id py/fixed-offset-timezone
 * @description Timezones with offsets don't account for DST.
 * @kind problem
 * @tags
 *   - code-smell
 *   - timezone
 * @problem.severity warning
 * @precision high
 */

import python
import semmle.python.ApiGraphs
import semmle.python.dataflow.new.DataFlow

// from Call td, Call tz, StringLiteral str
// where
//   // creates timedelta
// 	(
// 		td.getFunc().toString() = "timedelta"
// 		or
// 		((Attribute)td.getFunc()).getName() = "timedelta"
// 	) and

//   // creates timezone
// 	(
// 		tz.getFunc().toString() = "timezone"
// 		or
// 		(tz.getFunc() instanceof Attribute and (
// 			((Attribute)tz.getFunc()).getName() = "timezone" or	
// 			((Attribute)tz.getFunc()).getName() = "ZoneInfo" or
// 		((Attribute)tz.getFunc()).getName() = "gettz"))
// 	) and

// 	// THESE TAKE A VERY LONG TIME!!!
// 	// UTC is okay
// 	// str.getText() != "UTC" and
// 	// E.g., "America/New York" is okay but "EST" is not.
// 	// Better to actually create a list of bad tzs.
// 	// str.getText().length() < 4 and

// 	((tz.getArg(0) = td) or (tz.getArg(0) = str))

// select tz, "Timezone with a fixed offset." 

from DataFlow::CallCfgNode tdcall, DataFlow::CallCfgNode tzcall
where
	tdcall = API::moduleImport("datetime").getMember("timedelta").getACall() and
	tzcall = API::moduleImport("datetime").getMember("timezone").getACall() and
	DataFlow::localFlow(tdcall, tzcall.getArg(0))
select tzcall, "Timezone with a fixed offset."

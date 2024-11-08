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

from DataFlow::CallCfgNode tdcall, DataFlow::CallCfgNode tzcall
where
	tdcall = API::moduleImport("datetime").getMember("timedelta").getACall() and
	tzcall = API::moduleImport("datetime").getMember("timezone").getACall() and
	DataFlow::localFlow(tdcall, tzcall.getArg(0))
select tzcall, "Timezone with a fixed offset."

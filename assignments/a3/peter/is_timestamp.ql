/**
 * @id py/examples/is-timestamp
 * @name Is timestamp
 * @description Find calls to is_timestamp
 */

import python

from Call ts_c , FunctionValue ts_f
where ts_c.getFunc().pointsTo(ts_f) and ts_f.getName() = "is_timestamp"
select ts_c
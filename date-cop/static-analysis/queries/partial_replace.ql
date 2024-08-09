/**
 * @name Prevent partial date replace
 * @description Prevent calls to datetime.replace which replace a subset of {year, month, day} but not all of them
 * @kind problem
 * @tags
 *   - date
 * @problem.severity recommendation
 * @sub-severity high
 * @precision high
 * @id py/partial-replace
 */

import python

from Call c
where
  c.getFunc().(Attribute).getName() = "replace" and
  (
    c.getANamedArg().(Keyword).getArg() = "year" or
    c.getANamedArg().(Keyword).getArg() = "month" or
    c.getANamedArg().(Keyword).getArg() = "day"
  ) and not
  (
    c.getANamedArg().(Keyword).getArg() = "year" and
    c.getANamedArg().(Keyword).getArg() = "month" and
    c.getANamedArg().(Keyword).getArg() = "day"
  )
select c, "replacing individual parts of a date can be dangerous and result in invalid dates"
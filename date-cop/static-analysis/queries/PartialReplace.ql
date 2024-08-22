/**
 * @id py/partial-replace
 * @description Prevent calls to datetime.replace which replace a subset of {year, month, day} but not all of them
 * @kind problem
 * @tags
 *   - correctness
 *   - date
 * @problem.severity warning
 * @precision high
 */

import python

class PartialReplace extends Call {
  PartialReplace() {
    ((Attribute)this.getFunc()).getName() = "replace"
    and
    (
      ((Keyword)this.getANamedArg()).getArg() = "year"
      or
      ((Keyword)this.getANamedArg()).getArg() = "month"
      or
      ((Keyword)this.getANamedArg()).getArg() = "day"
    )
    and not
    (
      ((Keyword)this.getANamedArg()).getArg() = "year"
      and
      ((Keyword)this.getANamedArg()).getArg() = "month"
      and
      ((Keyword)this.getANamedArg()).getArg() = "day"
    )
  }
}

from PartialReplace c
select c, "Replacing individual parts of a date can result in invalid dates"
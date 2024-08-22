/**
 * @id py/block-datetime-now-no-tz
 * @description Prevent usage of datetime.now with tz=None.
 * @kind problem
 * @tags
 *   - code-smell
 *   - naive-datetime
 * @problem.severity recommendation
 * @precision high
 */

import python

class NaiveDatetimeCreation extends Call{
  None n;
  Attribute attr;

  NaiveDatetimeCreation() {
    attr = (Attribute)this.getFunc()
    
    and
    (
      attr.getName() = "fromtimestamp" or attr.getName() = "datetime" or this.getFunc().toString() = "datetime"
    ) 
    
    and
    (
      this.getANamedArg().contains(n) or 
      (attr.getName() = "fromtimestamp" and not exists(this.getPositionalArg(1))) or
      (not attr.getName() = "fromtimestamp" and not exists(this.getANamedArg()))
    )
  }
}

from NaiveDatetimeCreation c
select c, "Initializatio of a naive datetime object."


/**
 * @id py/naive-datetime-creation
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
    (
      attr = (Attribute)this.getFunc()
    
      and
      (
        (
          attr.getName() = "fromtimestamp" and
          (
            this.getPositionalArg(1) = n or 
            this.getKeyword(0).getValue() = n or
            (not this.getANamedArgumentName() = "tz" and (not exists(this.getPositionalArg(1))))
          )
        )

        or
        (
          (attr.getName() = "datetime" or attr.getName()= "time") and
          (not exists(string s | s = this.getANamedArgumentName() and s = "tzinfo")) or
          exists(string s | s = this.getANamedArgumentName() and s = "tzinfo" | this.getANamedArg().contains(n))
        )

        // or
        // (
        //   attr.getName() = "now" and 
        //   (
        //     this.getPositionalArgumentCount() = 0 and
        //     (this.getKeyword(0).getValue() = n or not exists(this.getAKeyword()))
        //   )
        // )
      )
    )
  }
}

from NaiveDatetimeCreation c
select c, "Initialization of a naive datetime object using $@.", c.getFunc(), ((Attribute)c.getFunc()).getName().toString()
 
/**
 * @id py/deprecated-method-call
 * @description Deprecated methods are dangerous and can cause silent failures or unexpected behaviour.
 * @kind problem
 * @tags
 *   - correctness
 * @problem.severity warning
 * @precision very-high
 */

import python

class DeprecatedMethodCall extends Call {
  DeprecatedMethodCall() {
    ((Attribute)this.getFunc()).getName() = "utcnow" or ((Attribute)this.getFunc()).getName() = "utcfromtimestamp"
  }

  string getMethod() {
    result = ((Attribute)this.getFunc()).getName()
  }
}

from DeprecatedMethodCall call
select call, "Deprecated methods such as $@ should not be used.", call, call.getMethod()

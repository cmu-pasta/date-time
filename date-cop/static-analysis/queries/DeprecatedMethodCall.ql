/**
 * @name deprecated methods being used
 * @description Deprecated methods are dangerous and can cause silent failures.
 * @kind problem
 * @tags correctness
 * @problem.severity warning
 * @precision very-high
 * @id py/deprecated-method-call
 */

import python

class DeprecatedMethodCall extends Call {
  Attribute attr;
  DeprecatedMethodCall() {
    this.getFunc() = attr and (attr.getName() = "utcnow" or attr.getName() = "utcfromtimestamp")
  }

  string getMethod() {
    result = attr.getName()
  }
}

from DeprecatedMethodCall call
select call, "Deprecated methods such as $@ should not be used.", call, call.getMethod()

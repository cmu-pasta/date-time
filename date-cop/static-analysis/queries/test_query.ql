/**
 * @name
 * @description
 * @kind problem
 * @tags
 * @problem.severity r
 * @sub-severity high
 * @precision high
 * @id py/multiple-nows
 */

import python

from Expr e
select e, e.getAQlClass()

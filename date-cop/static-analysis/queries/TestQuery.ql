/**
 * @id py/test-query
 * @description Test query to find out entity QL classes
 * @kind problem
 * @tags
 * @problem.severity recommendation
 * @precision high
 */

import python

from Expr e
select e, e.getAQlClass()

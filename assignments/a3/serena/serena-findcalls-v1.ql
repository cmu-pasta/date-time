/**
 * @name Calls to the method is_timestamp()
 * @description Finds all calls to the method is_timestamp()
 * @tags is_timestamp()
 */

 import python

 
 from Call call
 where 
    call.getFunc().pointsTo().toString().matches("%is_timestamp%")
 select call, "Call to is_timestamp() method" 

/*
from Function f
where f.getName().matches("%is_timestamp")
select f, "Call to is_timestamp() method"

from Function f
where f.getName().matches("is_timestamp") or f.getName().matches("util.is_timestamp")
select f, "Call to is_timestamp() method"
*/
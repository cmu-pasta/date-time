/**
 * @name Calls to the method utcnow() or utcfromtimestamp()
 * @description Finds all calls to the method utcnow() or utcfromtimestamp()
 * @tags utcnow(), utcfromtimestamp()
 */

 import python

 
 from Call call
 where 
    call.getFunc().pointsTo().toString().matches("%utcnow%")
    or
    call.getFunc().pointsTo().toString().matches("%utcfromtimestamp%")
 select call, "bad pattern" 

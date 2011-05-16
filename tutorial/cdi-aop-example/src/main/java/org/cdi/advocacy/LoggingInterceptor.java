package org.cdi.advocacy;

import java.util.Arrays;
import java.util.logging.Logger;

import javax.interceptor.AroundInvoke;
import javax.interceptor.Interceptor;
import javax.interceptor.InvocationContext;


@Logable @Interceptor
public class LoggingInterceptor {

    @AroundInvoke 
    public Object log(InvocationContext ctx) throws Exception {
    	System.out.println("In LoggingInterceptor");
        Logger logger = Logger.getLogger(ctx.getTarget().getClass().getName());
        logger.info("before call to " + ctx.getMethod() + " with args " + Arrays.toString(ctx.getParameters()));
        Object returnMe = ctx.proceed();
        logger.info("after call to " + ctx.getMethod() + " returned " + returnMe);
        return returnMe;
    }
}

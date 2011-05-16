package org.cdi.advocacy;

import java.io.PrintStream;
import java.lang.annotation.Annotation;
import java.util.Arrays;

//import javax.inject.Inject;
import javax.interceptor.AroundInvoke;
import javax.interceptor.Interceptor;
import javax.interceptor.InvocationContext;


@Debugable @Interceptor
public class DebugingInterceptor {

    @AroundInvoke 
    public Object log(InvocationContext invocationContext) throws Exception {
    	
    	System.out.println("In DebugingInterceptor");

        PrintStream out = System.out;
        out.println("debug ");

        out.println("target " + invocationContext.getTarget().getClass());

        out.printf("method %s: signature %s with annotations %s \n", invocationContext.getMethod().getName(), 
                invocationContext.getMethod(), Arrays.toString(invocationContext.getMethod().getAnnotations()));
        
        
        Annotation[][] parameterAnnotations = invocationContext.getMethod().getParameterAnnotations();
        Object[] parameterValues = invocationContext.getParameters();
        Class<?>[] parameterTypes = invocationContext.getMethod().getParameterTypes();
        
        for (int index = 0; index < parameterValues.length; index++) {
            out.printf("param %d value=%s type=%s annotations=%s \n", index, parameterValues[index], 
                    parameterTypes[index], Arrays.toString(parameterAnnotations[index]));
        }
        return invocationContext.proceed();
        
    }
}

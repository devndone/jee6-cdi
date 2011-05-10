package org.cdi.advocacy.security;



import javax.inject.Inject;
import javax.interceptor.AroundInvoke;
import javax.interceptor.Interceptor;
import javax.interceptor.InvocationContext;

/**
 * @author Richard Hightower
 */
@Secure @Interceptor
public class SecurityAdvice {
        
        @Inject
        private SecurityService securityManager;

        @AroundInvoke
        public void checkSecurity(InvocationContext joinPoint) throws Throwable {
                
            /* If the user is not logged in, don't let them use this method */
            if(!securityManager.isLoggedIn()){            
                throw new SecurityViolationException();
            }

            /* Get the name of the method being invoked. */
            String operationName = joinPoint.getMethod().getName();
            /* Get the name of the object being invoked. */
            String objectName = joinPoint.getTarget().getClass().getName();


           /*
            * Invoke the method or next Interceptor in the list,
            * if the current user is allowed.
            */
            if (!securityManager.isAllowed(objectName, operationName)){
                throw new SecurityViolationException();
            }
        
            joinPoint.proceed();
        }
}
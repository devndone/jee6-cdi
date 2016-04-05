<h1> CDI based AOP - An Introductory Tutorial -- NOT DONE.... IN PROGRESS </h1>




# Introduction #
<p>
This article discusses CDI based AOP in a tutorial format.<br>
<br>
<a href='http://jcp.org/aboutJava/communityprocess/final/jsr299/index.html'>CDI</a> is the<br>
Java standard for dependency injection (DI) and interception (AOP). It is evident<br>
from the popularity of DI and AOP that Java needs to address DI and AOP so that<br>
it can build other standards on top of it. DI and AOP are the foundation of many<br>
Java frameworks.<br>
<br>
</p>

<p>
CDI is a foundational aspect of Java EE 6. It is or will be shortly supported by<br>
<a href='http://www.caucho.com/resin/'>Caucho's Resin</a>, IBM's WebSphere,<br>
<a href='http://glassfish.java.net/'>Oracle's Glassfish</a>,<br>
<a href='http://www.jboss.org/jbossas/docs/6-x.html'>Red Hat's JBoss</a> and many more application servers.<br>
CDI is similar to core Spring and Guice frameworks. Like JPA did for ORM, CDI<br>
simplifies and sanitizes the API for DI and AOP. If you have worked with Spring<br>
or Guice, you will find CDI easy to use and easy to learn. If you are new to AOP,<br>
then CDI is an easy on ramp for picking up AOP quickly, as it uses a small subset of<br>
what AOP provides. CDI based AOP is simpler to use and learn.<br>
</p>

<p>
One can argue that CDI only implements a small part of AOP that is<br>
method interception. And while that is a small part of what AOP has to<br>
offer, it is also the part that most developers use.<br>
</p>

<p>
CDI can be used standalone and can be embedded into any application.<br>
</p>


<p>
<a href='http://jee6-cdi.googlecode.com/svn/tutorial/cdi-aop-example'>Source code for this tutorial</a>,<br>
and <a href='MavenAOPTutorialInstructions.md'>instructions</a> for use.<br>
It is no accident that this tutorial follows many of the same examples in the<br>
<a href='http://java.dzone.com/articles/introduction-spring-aop'>Spring 2.5 AOP tutorial</a>
written three years ago.<br>
</p>

<p>
It will be interesting to compare and contrast the examples in this tutorial<br>
with the one written three years ago for Spring based AOP.<br>
</p>

# Design goals of this tutorial #
<p>
This tutorial is meant to be a description and explanation of AOP in CDI<br>
without the clutter of EJB 3.1 or JSF.<br>
There are already plenty of tutorials that cover EJB 3.1 and JSF (and CDI).<br>
</p>

<p>
We believe that CDI has merit on its own outside of the EJB and JSF space. This<br>
tutorial only covers CDI. Repeat there is no JSF 2 or EJB 3.1 in this tutorial.<br>
There are plenty of articles and tutorials that cover using CDI as part of a larger<br>
<a href='http://download.oracle.com/javaee/6/tutorial/doc/gjbnr.html'>JEE 6 application</a>.<br>
This tutorial is not that. This tutorial series is CDI and only CDI.<br>
</p>

<p>
This tutorial only has full, complete code examples with source code you<br>
can download and try out on your own. There are no code snippets where you can't figure out<br>
where in the code you are suppose to be.<br>
</p>

<p>
So far these tutorials have been well recieved and we got a lot of<br>
feedback.  There appears to be a lot of interest in the CDI standard.<br>
Thanks for reading and thanks for your comments and participation so far.<br>
</p>






# AOP Basics #
<p>
For some, AOP seems like voodoo magic. For others, AOP seems like a cureall.<br>
For now, let's just say that AOP is a tool that you want in your developer toolbox.<br>
It can make seemingly impossible things easy. Aagin, when we talk about AOP in CDI,<br>
we are really talking about interception which is a small but very useful part of AOP.<br>
For brevity, I am going to refer to interception as AOP.<br>
</p>

<p>
The first time that I used AOP was with Spring's transaction management support.<br>
I did not realize I was using AOP. I just knew Spring could apply EJB-style<br>
declarative transaction management to POJOs. It was probably three to six months<br>
before I realized that I was using was Spring's AOP support. The Spring framework<br>
truly brought AOP out of the esoteric closet into the main stream<br>
light of day. CDI brings these concepts into the JSR standards where<br>
other Java standards can build on top of CDI.<br>
</p>

<p>
You can think of AOP as a way to apply services (called cross-cutting concerns)<br>
to objects. AOP encompasses more than this, but this is where it gets used<br>
mostly in the main stream.<br>
</p>

<p>
I've using AOP to apply caching services, transaction management,<br>
resource management, etc. to any number of objects in an application.<br>
I am currently working with a team of folks on the CDI implementation<br>
for the revived JSR-107 JCache.<br>
AOP is not a panacea, but it certainly fits a lot of otherwise difficult use cases.<br>
</p>

<p>
You can think of AOP as a dynamic decorator design pattern. The decorator<br>
pattern allows additional behavior to be added to an existing class by wrapping<br>
the original class and duplicating its interface and then delegating to the original.<br>
See this article <a href='http://en.wikipedia.org/wiki/Decorator_pattern'>decorator pattern</a>
for more detail about the decorator design pattern. (Notice in addition to supporting<br>
AOP style interception CDI also supports actual decorators, which are not covered in this article.)<br>
</p>

# Sample application revisited #

<p>
For this introduction to AOP, let's take a simple example, let's apply security<br>
services to our Automated Teller Machine example from the first<br>
[DependencyInjectionAnIntroductoryTutorial Dependency Injection example from<br>
the first tutorial] in this series.<br>
</p>

<p>
Let's say when a user logs into a system that a <b><code>SecurityToken</code></b> is created that<br>
carries the user's credentials and before methods on objects get invoked, we<br>
want to check to see if the user has credentials to invoke these<br>
methods. For review, let's look at the <b><code>AutomatedTellerMachine</code></b> interface.<br>
</p>

#### Code Listing: `AutomatedTellerMachine` interface ####

```
package org.cdi.advocacy;

import java.math.BigDecimal;

public interface AutomatedTellerMachine {

	public abstract void deposit(BigDecimal bd);

	public abstract void withdraw(BigDecimal bd);

}
```


<p>
In a web application, you could write a <b><code>ServletFilter</code></b>, that stored this<br>
<b><code>SecurityToken</code></b> in <b><code>HttpSession</code></b> and then on every request retrieved the token<br>
from Session and put it into a <b><code>ThreadLocal</code></b> variable where it could be accessed<br>
from a <b><code>SecurityService</code></b> that you could implement.<br>
</p>

Perhaps the objects that needed the **`SecurityService`** could access it as follows:

#### Code Listing: `AutomatedTellerMachineImpl` implementing security without AOP ####

```
	public void deposit(BigDecimal bd) {
	    	/* If the user is not logged in, don't let them use this method */
    		if(!securityManager.isLoggedIn()){
    			throw new SecurityViolationException();
    		}
	    	/* Only proceed if the current user is allowed. */

	    	if (!securityManager.isAllowed("AutomatedTellerMachine", operationName)){
    			throw new SecurityViolationException();
    		}
		...

		transport.communicateWithBank(...);
	}
```

<p>
In our ATM example, the above might work out well, but imagine a system with<br>
thousands of classes that needed security. Now imagine, the way we check to see<br>
if a user is "logged in" changed. If we put this code into every method that needed<br>
security, then we could possibly have to change this a thousand times if we<br>
changed the way we checked to see if a user was logged in.<br>
</p>

<p>
What we want to do instead is to use CDI to create a decorated version of the<br>
<b><code>AutomateTellerMachineImpl</code></b> bean.<br>
The decorated version would add the additional behavior to the <b><code>AutomateTellerMachineImpl</code></b> object without<br>
changing the actual implementation of<br>
the <b><code>AutomateTellerMachineImpl</code></b>.  In AOP speak, this concept is<br>
called a cross-cutting concern. A cross-cutting concern is a concern that crosses the boundry<br>
of many objects.<br>
</p>

<p>
CDI does this by creating what is called an AOP proxy. An AOP proxy is like a dynamic decorator.<br>
Underneath the covers CDI can generate a class at runtime (the AOP proxy) that<br>
has the same interface as our <b><code>AutomatedTellerMachine</code></b>. The AOP proxy wraps our<br>
existing atm object and provides additional behavior by delegating to a list of<br>
method interceptors. The method interceptors provide the additional behavior and<br>
are similar to <b><code>ServletFilter</code></b>s but for methods instead of requests.<br>
</p>

## Diagrams of CDI AOP support ##

Thus before we added CDI AOP, our atm example was like Figure 1.

#### Figure 1: Before AOP advice ####
![http://jee6-cdi.googlecode.com/svn/wiki/images/beforeAOP.png](http://jee6-cdi.googlecode.com/svn/wiki/images/beforeAOP.png)

After we added AOP support, we now get an AOP proxy that applies the **`securityAdvice`** to the **`atm`** as show in figure 2.

#### Figure 2: After AOP advice ####

![http://jee6-cdi.googlecode.com/svn/wiki/images/afterAOP.png](http://jee6-cdi.googlecode.com/svn/wiki/images/afterAOP.png)


<p>
You can see that the AOP proxy implements the <b><code>AutomatedTellerMachine</code></b> interface.<br>
When the client object looks up the atm and starts invoking methods instead of<br>
executing the methods directly, it executes the method on the proxy, which then<br>
delegates the call to a series of method interceptor called advice,<br>
which eventually invoke the actual atm instance (now called atmTarget).<br>
</p>

<p>
Let's actually look at the code for this example.<br>
</p>
<p>
For this example, we will use a simplified <b><code>SecurityToken</code></b> that gets<br>
stored into a <b><code>ThreadLocal</code></b> variable, but one could imagine one that<br>
was populated with data from a database or an LDAP server or some<br>
other source of authentication and authorization.<br>
</p>

Here is the **`SecurityToken`**, which gets stored into a **`ThreadLocal`** variable, for this example:

#### SecurityToken.java Gets stored in ThreadLocal ####
```

package org.cdi.advocacy.security;

/**
 * @author Richard Hightower
 *
 */
public class SecurityToken {
        
        private boolean allowed;
        private String userName;
        
        public SecurityToken() {
                
        }
        
        
        
        public SecurityToken(boolean allowed, String userName) {
                super();
                this.allowed = allowed;
                this.userName = userName;
        }



        public boolean isAllowed(String object, String methodName) {
                return allowed;
        }

        
        /**
         * @return Returns the allowed.
         */
        public boolean isAllowed() {
                return allowed;
        }
        /**
         * @param allowed The allowed to set.
         */
        public void setAllowed(boolean allowed) {
                this.allowed = allowed;
        }
        /**
         * @return Returns the userName.
         */
        public String getUserName() {
                return userName;
        }
        /**
         * @param userName The userName to set.
         */
        public void setUserName(String userName) {
                this.userName = userName;
        }
}
```

The **`SecurityService`** stores the **`SecurityToken`** into the **`ThreadLocal`** variable,
and then delegates to it to see if the current user has access to perform the
current operation on the current object as follows:

#### SecurityService.java Service ####
```

package org.cdi.advocacy.security;


public class SecurityService {
        
        private static ThreadLocal<SecurityToken> currentToken = new ThreadLocal<SecurityToken>();
        
        public static void placeSecurityToken(SecurityToken token){
                currentToken.set(token);
        }
        
        public static void clearSecuirtyToken(){
                currentToken.set(null);
        }
        
        public boolean isLoggedIn(){
                SecurityToken token = currentToken.get();
                return token!=null;
        }
        
        public boolean isAllowed(String object, String method){
                SecurityToken token = currentToken.get();
                return token.isAllowed();
        }
        
        public String getCurrentUserName(){
                SecurityToken token = currentToken.get();
                if (token!=null){
                        return token.getUserName();
                }else {
                        return "Unknown";
                }
        }

}


```

<p>
The <b><code>SecurityService</code></b> will throw a <b><code>SecurityViolationException</code></b> if a user<br>
is not allowed to access a resource. <b><code>SecurityViolationException</code></b> is<br>
just a simple exception for this example.<br>
</p>

#### SecurityViolationException.java Exception ####
```

package com.arcmind.springquickstart.security;

/**
 * @author Richard Hightower
 *
 */
public class SecurityViolationException extends RuntimeException {

	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;

}

```

<p>
To remove the security code out of the <b><code>AutomatedTellerMachineImpl</code></b>
class and any other class that needs security, we will write an Aspect<br>
in CDI to intercept calls and perform security checks before the<br>
method call.<br>
To do this we will create a method interceptor (known is AOP speak as an advice) and intercept method calls on the atm object.<br>
</p>

<p>
Here is the <b><code>SecurityAdvice</code></b> class which will intercept calls on the<br>
<b><code>AutomatedTellerMachineImpl</code></b> class.<br>
</p>

#### SecurityAdvice ####
```
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
        public Object checkSecurity(InvocationContext joinPoint) throws Exception {
        	
        	System.out.println("In SecurityAdvice");
                
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
        
            return joinPoint.proceed();
        }
}

```

<p>
Notice that we annotate the <b><code>SecuirtyAdvice</code></b> class with an @<b><code>Secure</code></b>
annotation. The @<b><code>Secure</code></b> annotation is an @<b><code>InterceptorBinding</code></b>. We use<br>
it to denote both the interceptor and the classes it intercepts. More<br>
on this later.<br>
</p>

<p>
Notice that we use @Inject to inject the <b><code>securityManager</code></b>. Also we mark<br>
the method that implements that around advice with and @<b><code>AroundInvoke</code></b>
annotation. This essentially says this is the method that does the<br>
dynamic decoration.<br>
</p>

<p>
Thus, the <b><code>checkSecurity</code></b> method of <b><code>SecurityAdvice</code></b> is the method that<br>
implements the advice. You can think of advice as the decoration that we want<br>
to apply to other objects. The objects getting the decoration are called advised objects.<br>
</p>

<p>
Notice that the <b><code>SecurityService</code></b> gets injected into the <b><code>SecurityAdvice</code></b>
and the <b><code>checkSecurity</code></b> method uses the <b><code>SecurityService</code></b>**to see if the<br>
user is logged in and the user has the rights to execute the method.<br>
</p>**

<p>
An instance of <b><code>InvocationContext</code></b>, namely <b><code>joinPoint</code></b>, is passed as<br>
an argument to <b><code>checkSecurity</code></b>. The <b><code>InvocationContext</code></b> has<br>
information about the method that is being called and provides control<br>
that determines if the method on the advised object's methods gets<br>
invoked (e.g., <b><code>AutomatedTellerMachineImpl.withdraw</code></b>
and <b><code>AutomatedTellerMachineImpl.deposit</code></b>). If <b><code>joinPoint.proceed()</code></b> is<br>
not called then the wrapped method of the advised object (<b><code>withdraw</code></b>
or <b><code>deposit</code></b>) is not called. (The proceed method causes the actual<br>
decorated method to be invoked or the next interceptor in the chain to<br>
get invoked.)<br>
</p>

<p>
In Spring, to apply an Advice like <b><code>SecurityAdvice</code></b> to an advised object, you need a pointcut.<br>
A pointcut is like a filter that picks the objects and methods that get decorated.<br>
In CDI, you just mark the class or methods of the class that you want<br>
decorated with an interceptor binding annotation.<br>
There is no complex pointcut language. You could implement one as a CDI extention, but<br>
it does not come with CDI by default. CDI uses the most common way<br>
developer apply interceptors, i.e., with annotations.<br>
</p>

<p>
CDI scans each class in each jar (and other classpath locations) that has a META-INF/beans.xml.<br>
<br>
The <b><code>SecurityAdvice</code></b> get installed in the CDI beans.xml.<br>
<br>
</p>

#### META-INF/beans.xml ####
```
<beans xmlns="http://java.sun.com/xml/ns/javaee" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="
http://java.sun.com/xml/ns/javaee
http://java.sun.com/xml/ns/javaee/beans_1_0.xsd">

    <interceptors>
        <class>org.cdi.advocacy.security.SecurityAdvice</class>
    </interceptors>
</beans>
```

<p>
You can install interceptors in the order you want them called.<br>
</p>

<p>In order to associate a interceptor with the classes and methods it<br>
decorates, you have to define an <b><code>InterceptorBinding</code></b> annotation. An<br>
example of such a binding is defined below in the @<b><code>Secure</code></b> annotation.</p>

#### Secure.java annotation ####
```
package org.cdi.advocacy.security;

import java.lang.annotation.Retention;
import java.lang.annotation.Target;
import static java.lang.annotation.ElementType.*;
import static java.lang.annotation.RetentionPolicy.*;
import javax.interceptor.InterceptorBinding;


@InterceptorBinding 
@Retention(RUNTIME) @Target({TYPE, METHOD})
public @interface Secure {

}

```

<p>Notice that we annotated the @Secure annotation with the<br>
@<b><code>InterceptorBinding</code></b> annotation. </p>

<p>
<b><code>InterceptorBindings</code></b> follow a lot of<br>
the same rules as <b><code>Qualifiers</code></b> as discussed in the first two<br>
articles in this series.<br>
<b><code>InterceptorBindings</code></b>  are like<br>
qaulifiers for injection in that they can have members which can<br>
further qualify the injection. You can also disable <b><code>InterceptorBinding</code></b>
annotation members from qualifying an interception by using the<br>
@<b><code>NonBinding</code></b> just like you can in <b><code>Qualifiers</code></b>.</p>

<p>To finish our example, we need to annotate our<br>
<b><code>AutomatedTellerMachine</code></b> with the same @<b><code>Secure</code></b> annotation; thus,<br>
associating the <b><code>AutomatedTellerMachine</code></b> with our <b><code>SecurityAdvice</code></b>.<br>
</p>

#### AutomatedTellerMachine class using @Secure ####
```
package org.cdi.advocacy;
...
import javax.inject.Inject;

import org.cdi.advocacy.security.Secure;

@Secure
public class AutomatedTellerMachineImpl implements AutomatedTellerMachine {

    @Inject
    @Json
    private ATMTransport transport;

    public void deposit(BigDecimal bd) {
        System.out.println("deposit called");
        transport.communicateWithBank(null);

    }

    public void withdraw(BigDecimal bd) {
        System.out.println("withdraw called");

        transport.communicateWithBank(null);

    }

}
```

<p>
You have the option of use @<b><code>Secure</code></b> on the methods or at the class<br>
level. In this example, we annotated the class itself, which then<br>
applies the interceptor to every method.<br>
</p>

<p>
Let's complete our example by reviewing the <b><code>AtmMain</code></b> main method that<br>
looks up the atm out of CDI's <b>beanContainer</b>.<br>
</p>
<p>
Let's review <b>AtmMain</b> as follows:<br>
</p>
#### AtmMain.java ####
```
package org.cdi.advocacy;

import java.math.BigDecimal;

import org.cdi.advocacy.security.SecurityToken;
import org.cdiadvocate.beancontainer.BeanContainer;
import org.cdiadvocate.beancontainer.BeanContainerManager;
import org.cdi.advocacy.security.SecurityService;

public class AtmMain {

    public static void simulateLogin() {
        SecurityService.placeSecurityToken(new SecurityToken(true,
                "Rick Hightower"));
    }

    public static void simulateNoAccess() {
        SecurityService.placeSecurityToken(new SecurityToken(false,
                "Tricky Lowtower"));
    }

    public static BeanContainer beanContainer = BeanContainerManager
            .getInstance();
    static {
        beanContainer.start();
    }

    public static void main(String[] args) throws Exception {
        simulateLogin();
        //simulateNoAccess();

        AutomatedTellerMachine atm = beanContainer
                .getBeanByType(AutomatedTellerMachine.class);
        atm.deposit(new BigDecimal("1.00"));
    }

}

```

<p>
Before we added AOP support when we looked up the atm, we looked up the object<br>
directly as shown in figure 1, now that we applied AOP when we look up the object<br>
we get what is in figure 2. When we look up the atm in the application context,<br>
we get the AOP proxy that applies the decoration (advice, method interceptor) to<br>
the atm target by wrapping the target and delegating to it after it invokes the<br>
series of method interceptors.<br>
</p>

## Victroy lap ##
<p>
The last code listing works just like you think. If you use<br>
<b><code>simulateLogin</code></b>, <b><code>atm.deposit</code></b> does not throw a <b><code>SecurityException</code></b>. If you use<br>
<b><code>simulateNoAccess</code></b>, it does throw a <b><code>SecurityException</code></b>. Now let's weave<br>
in a few more "Aspects" to the mix to drive some points home and to<br>
show how interception works with multiple interceptors.<br>
</p>

<p>
I will go quicker this time.<br>
</p>

#### LoggingInterceptor ####
```
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

```

Now we need to define the Logable interceptor binding annotation as
follows:

```
package org.cdi.advocacy;

import java.lang.annotation.Retention;
import java.lang.annotation.Target;
import static java.lang.annotation.ElementType.*;
import static java.lang.annotation.RetentionPolicy.*;
import javax.interceptor.InterceptorBinding;


@InterceptorBinding 
@Retention(RUNTIME) @Target({TYPE, METHOD})
public @interface Logable {

}

```

<p>
Now to use it we just mark the methods where we want this logging.<br>
</p>

#### AutomatedTellerMachineImpl.java using Logable ####
```
package org.cdi.advocacy;

...

@Secure
public class AutomatedTellerMachineImpl implements AutomatedTellerMachine {

...

    @Logable
    public void deposit(BigDecimal bd) {
        System.out.println("deposit called");
        transport.communicateWithBank(null);

    }

    public void withdraw(BigDecimal bd) {
        System.out.println("withdraw called");

        transport.communicateWithBank(null);

    }

}

```

<p>
Notice that we use the @<b><code>Secure</code></b> at the class level which will applies the<br>
security interceptor to every mehtod in the<br>
<b><code>AutomatedTellerMachineImpl</code></b>.<br>
But, we use @<b><code>Logable</code></b> only on the <b><code>deposit</code></b> method which applies it, you guessed it,<br>
only on the <b><code>deposit</code></b> method.<br>
</p>
<p>
Now you have to add this interceptor to the beans.xml:<br>
</p>
#### META-INF/beans.xml ####
```
<beans 
...
    <interceptors>
        <class>org.cdi.advocacy.LoggingInterceptor</class>
        <class>org.cdi.advocacy.security.SecurityAdvice</class>
    </interceptors>
</beans>
```

When we run this again, we get something like this in our console
output:

```
May 15, 2011 6:46:22 PM org.cdi.advocacy.LoggingInterceptor log
INFO: before call to public void org.cdi.advocacy.AutomatedTellerMachineImpl.deposit(java.math.BigDecimal) with args [1.00]
May 15, 2011 6:46:22 PM org.cdi.advocacy.LoggingInterceptor log
INFO: after call to public void org.cdi.advocacy.AutomatedTellerMachineImpl.deposit(java.math.BigDecimal) returned null
```

Notice that the order of interceptors in the beans.xml file determines
the order of execution in the code. (I added a println to each
interceptor just to show the ordering.) When we run this, we get the
following output.

#### Output: ####

```
In LoggingInterceptor
In SecurityAdvice
```

If we switch the order in the beans.xml file, we will get a different
order in the console output.

#### META-INF/beans.xml ####
```
<beans 
...
    <interceptors>
      <class>org.cdi.advocacy.security.SecurityAdvice</class>
      <class>org.cdi.advocacy.LoggingInterceptor</class>
    </interceptors>
</beans>
```


```
In SecurityAdvice
In LoggingInterceptor
```

This is important as many interceptors can be applied. You have one
place to set the order.

## Conclusion ##
<p>
AOP is neither a cure all or voodoo magic, but a powerful tool that<br>
needs to be in your bag of tricks. The Spring framework has brought<br>
AOP to the main stream masses and Spring 2.5/3.x has simplified using AOP.<br>
CDI brings AOP and DI into the standard's bodies where it can get further<br>
mainstreamed, refined and become part of future Java standards like<br>
JCache, Java EE 6 and Java EE 7.<br>
</p>

<p>
You can use Spring CDI to apply services (called cross-cutting<br>
concerns) to objects using AOP's interception model. AOP need not seem<br>
a foreign concept as it is merely a more flexible version of the<br>
decorator design pattern. With AOP you can add additional behavior to<br>
an existing class without writing a lot of wrapper code.<br>
This can be a real time saver when you have a use case where you need to apply<br>
a cross cutting concern to a slew of classes.<br>
</p>

<p>
<a href='http://jcp.org/aboutJava/communityprocess/final/jsr299/index.html'>CDI</a> is the<br>
Java standard for dependency injection and interception (AOP).<br>
It is evident from the popularity of DI and AOP that Java needs to address DI<br>
and AOP so that it can build other standards on top of it.<br>
DI and AOP are the foundation of many Java frameworks.<br>
I hope you share my excitement of CDI as a basis for other JSRs, Java<br>
frameworks and standards.<br>
</p>

<p>
CDI is a foundational aspect of Java EE 6. It is or will be shortly supported by<br>
Caucho's Resin, IBM's WebSphere, Oracle's Glassfish, Red Hat's JBoss and many<br>
more application servers. CDI is similar to core Spring and Guice frameworks.<br>
However CDI is a general purpose framework that can be used outside of JEE 6.<br>
</p>

<p>
CDI simplifies and sanitizes the API for DI and AOP. I find that<br>
working with CDI based AOP is easier and covers the most common use<br>
cases. CDI is a rethink on how to do dependency injection and AOP (interception really).<br>
It simplifies it. It reduces it. It gets rid of legacy, outdated ideas.<br>
</p>

<p>
CDI is to Spring and Guice what JPA is to Hibernate, and Toplink. CDI will co-exist with Spring and Guice.<br>
There are plugins to make them interoperate nicely (more on these shortly).<br>
</p>

This is just a brief taste. There is more to come.


# Resources #
  * [CDI advocacy group](http://sites.google.com/site/cdipojo/)
  * [CDI advocacy blog](http://cdi4jadvocate.blogspot.com/)
  * [CDI advocacy google code project](http://code.google.com/p/jee6-cdi/)
  * [Google group for CDI advocacy](http://groups.google.com/group/cdiadvocate4j)
  * [Manisfesto version 1](http://cdi4jadvocate.blogspot.com/2011/03/cdi-advocacy.html)
  * [Weld reference documentation](http://docs.jboss.org/weld/reference/1.1.0.Final/en-US/html/)
  * [CDI JSR299](http://jcp.org/aboutJava/communityprocess/final/jsr299/index.html)
  * [Resin fast and light CDI and Java EE 6 Web Profile implementation](http://www.caucho.com/resin/)
  * [CDI & JSF Part 1 Intro by Andy Gibson](http://www.andygibson.net/blog/tutorial/getting-started-with-jsf-2-0-and-cdi-in-jee-6-part-1/)
  * [CDI & JSF Part 2 Intro by Andy Gibson](http://www.andygibson.net/blog/tutorial/getting-started-with-cdi-part-2-injection/)
  * [CDI & JSF Part 3 Intro by Andy Gibson](http://www.andygibson.net/blog/tutorial/getting-started-with-jsf-2-0-and-cdi-part-3/)


> # About the Author #
<p> This article was written with CDI advocacy in mind by <a href='https://profiles.google.com/RichardHightower/about'>Rick Hightower</a>
<blockquote>with some collaboration from others.<br>
</p></blockquote>

<p>
<blockquote>Rick Hightower has worked as a CTO, Director of Development and a Developer for the last 20 years.<br>
He has been involved with J2EE since its inception. He worked at an EJB container company in 1999.<br>
He has been working with Java since 1996, and writing code professionally since 1990.<br>
Rick was an early <a href='http://java.sys-con.com/node/47735'>Spring enthusiast</a>.<br>
Rick enjoys bouncing back and forth between C, Python, Groovy and Java development.<br>
Although not a fan of <a href='http://java.sys-con.com/node/216307'>EJB 3</a>,<br>
Rick is a big fan of the potential of CDI and<br>
thinks that EJB 3.1 has come a lot closer to the mark.<br>
</p>
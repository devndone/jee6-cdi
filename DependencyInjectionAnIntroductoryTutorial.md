<h1> Dependency Injection - An Introductory Tutorial -- Deprecated See Split into two parts</h1>

[Goto Part 1](DependencyInjectionAnIntroductoryTutorial_Part1.md) or [Goto Part 2](DependencyInjectionAnIntroductoryTutorial_Part2.md)


# Introduction #

<p>This article discusses dependency injection in a tutorial format. It covers some<br>
of the features of CDI such as type safe annotations configuration, alternatives and more.<br>
</p>

<p>
<a href='http://jcp.org/aboutJava/communityprocess/final/jsr299/index.html'>CDI</a> is the<br>
Java standard for dependency injection (DI) and interception (AOP). It is evident<br>
from the popularity of DI and AOP that Java needs to address DI and AOP so that<br>
it can build other standards on top of it. DI and AOP are the foundation of many<br>
Java frameworks.<br>
</p>

<p>
CDI is a foundational aspect of Java EE 6. It is or will be shortly supported by<br>
<a href='http://www.caucho.com/resin/'>Caucho's Resin</a>,<br>
IBM's WebSphere,<br>
<a href='http://glassfish.java.net/'>Oracle's Glassfish</a>,<br>
<a href='http://www.jboss.org/jbossas/docs/6-x.html'>Red Hat's JBoss</a> and many more application servers.<br>
CDI is similar to core Spring and Guice frameworks. Like JPA did for ORM, CDI<br>
simplifies and sanitizes the API for DI and AOP. If you have worked with Spring<br>
or Guice, you will find CDI easy to use and easy to learn. If you are new to Dependency<br>
Injection (DI), then CDI is an easy on ramp for picking up DI quickly.<br>
CDI is simpler to use and learn.<br>
</p>

<p>
CDI can be used standalone and can be embedded into any application.<br>
</p>

<p>
<a href='https://jee6-cdi.googlecode.com/svn/tutorial/cdi-di-example'>Source code for this tutorial</a>,<br>
and <a href='MavenDITutorialInstructions.md'>instructions</a> for use.<br>
</p>

<p>
It is no accident that this tutorial follows this Spring 2.5 DI tutorial<br>
<a href='http://java.dzone.com/articles/dependency-injection-an-introd'>(using Spring "new" DI annotations)</a>
written three years ago.<br>
It will be interesting to compare and contrast the examples in this tutorial<br>
with the one written three years ago for Spring DI annotations.<br>
</p>

# Design goals of this tutorial #

<p>This tutorial is meant to be a description and explanation of DI in CDI<br>
without the clutter of EJB 3.1 or JSF. </p>

<p>
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
We start out slow, step by step and basic. Then once you understand the fundamentals,<br>
we pick up the pace quite a bit.<br>
</p>

<p>
All code examples have actually been run. We don't type in ad hoc code.<br>
If it did not run, it is not in our tutorial. We are not winging it.<br>
</p>

<p>
There are clear headings for code listings so you can use this tutorial as a cookbook when you<br>
want to use some feature of CDI DI in the future. This is a code centric tutorial.<br>
Again, the code listings are in the TOC so you can find just the code listing you are looking for quickly.<br>
</p>


<p>Decorators, Extentions, Interceptors, Scopes are out of scope for this first tutorial.<br>
</p>

<p>
If this tutorial is well recieved and we get enough feedback through our google group<br>
and comments section of the wiki then we will add a comprehensive tutorial on<br>
CDI AOP (Decorators and Interceptors) and one on Extentions.<br>
</p>

<p>
The more positive and/or constructive feedback we get the more encouraged we will be to add more.<br>
</p>





# Dependency Injection #

<p>
Dependency Injection (DI) refers to the process of supplying an external dependency<br>
to a software component. DI can help make your code architecturally pure.<br>
</p>

<p>
It aids in design by interface as well as test-driven development by providing<br>
a consistent way to inject dependencies. For example, a data access object (DAO)<br>
may depend on a database connection.<br>
</p>

<p>
Instead of looking up the database connection with JNDI, you could inject it.<br>
</p>

<p>
One way to think about a DI framework like CDI is to think of JNDI turned inside out.<br>
Instead of an object looking up other objects that it needs to get its job done<br>
(dependencies), a DI container injects those dependent objects.<br>
This is the so-called Hollywood Principle, "Don't call us�" (lookup objects),<br>
"we'll call you" (inject objects).<br>
</p>

<p>
If you have worked with <a href='http://en.wikipedia.org/wiki/Class-responsibility-collaboration_card'>CRC</a> cards<br>
you can think of a dependency as a collaborator. A collaborator<br>
is an object that another object needs to perform its role, like a DAO (data access object)<br>
needs a JDBC connection object for example.<br>
</p>

## Dependency Injection-`AutomatedTellerMachine` without CDI or Spring or Guice ##

<p>
Let's say that you have an automated teller machine (ATM, also known as an<br>
automated banking machine in other countries) and it needs the ability to talk<br>
to a bank. It uses what it calls a transport object to do this. In this example,<br>
a transport object handles the low-level communication to the bank.<br>
</p>

<p>
This example could be represented by these two interfaces as follows:<br>
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

#### Code Listing: ATMTransport interface ####
```
package org.cdi.advocacy;

public interface ATMTransport {
	public void communicateWithBank(byte[] datapacket);
}
```

<p>
Now the <b><code>AutomatedTellerMachine</code></b> needs a transport to perform its intent,<br>
namely withdraw money and deposit money. To carry out these tasks, the<br>
<b><code>AutomatedTellerMachine</code></b> may depend on many objects and collaborates with<br>
its dependencies to complete the work.<br>
</p>

<p>
An implementation of the <b><code>AutomatedTellerMachine</code></b> may look like this:<br>
</p>

#### Code Listing: **`AutomatedTellerMachineImpl`** class ####
```
package org.cdi.advocacy;
...
public class AutomatedTellerMachineImpl implements AutomatedTellerMachine {
	
	private ATMTransport transport;
	
        ...
	public void deposit(BigDecimal bd) {
		System.out.println("deposit called");
		transport.communicateWithBank(...);
	}

	public void withdraw(BigDecimal bd) {
		System.out.println("withdraw called");
		transport.communicateWithBank(...);
	}

}

```

<p>
The <b><code>AutomatedTellerMachineImpl</code></b> does not know or care how the transport<br>
withdraws and deposits money from the bank. This level of indirection allows<br>
us to replace the transport with different implementations such as in the following example:<br>
</p>

### Three example transports: `SoapAtmTransport`, `StandardAtmTransport` and `JsonAtmTransport` ###

#### Code Listing: `StandardAtmTransport` ####
```
package org.cdi.advocacy;


public class StandardAtmTransport implements ATMTransport {

	public void communicateWithBank(byte[] datapacket) {
		System.out.println("communicating with bank via Standard transport");
                ...
	}

}
```

#### Code Listing: `SoapAtmTransport` ####
```
package org.cdi.advocacy;

public class SoapAtmTransport implements ATMTransport {

	public void communicateWithBank(byte[] datapacket) {
		System.out.println("communicating with bank via Soap transport");
                ...
	}

}

```


#### Code Listing: `JsonRestAtmTransport` ####
```
package org.cdi.advocacy;

public class JsonRestAtmTransport implements ATMTransport {

	public void communicateWithBank(byte[] datapacket) {
		System.out.println("communicating with bank via JSON REST transport");
	}

}
```

<p>
Notice the possible implementations of the <b><code>ATMTransport interface</code></b>.<br>
The <code>*AutomatedTellerMachineImpl*</code> does not know or care which transport it uses.<br>
Also, for testing and developing, instead of talking to a real bank, you could<br>
easily use <a href='http://mockito.org/'>Mockito</a> or <a href='http://easymock.org/'>EasyMock</a>
or you could even write a <b><code>SimulationAtmTransport</code></b> that was a mock implementation<br>
just for testing.<br>
</p>

<p>
The concept of DI transcends CDI, Guice and Spring.<br>
Thus, you can accomplish DI without CDI, Guice or Spring as follows:<br>
</p>

#### Code Listing: `AtmMain`: DI without CDI, Spring or Guice ####

```
package org.cdi.advocacy;

public class AtmMain {
        
        public void main (String[] args) {
                AutomatedTellerMachine atm = new AutomatedTellerMachineImpl();
                ATMTransport transport = new SoapAtmTransport();
                /* Inject the transport. */           
                ((AutomatedTellerMachineImpl)atm).setTransport(transport);
                
                atm.withdraw(new BigDecimal("10.00"));
                
                atm.deposit(new BigDecimal("100.00"));
        }

}
```

<p>
Then injecting a different <b>transport</b> is a mere matter of calling a different setter method as follows:<br>
</p>

#### Code Listing: `AtmMain`: DI without CDI, Spring or Guice: `setTransport` ####
```
ATMTransport transport = new SimulationAtmTransport();
((AutomatedTellerMachineImpl)atm).setTransport(transport);
```

<p>
The above assumes we added a <b><code>setTransport</code></b> method to the <b><code>AutomateTellerMachineImpl</code></b>.<br>
Note you could just as easily use constructor arguments instead of a setter method.<br>
Thus keeping the interface of your <b><code>AutomateTellerMachineImpl</code></b> clean.<br>
</p>

## Running the examples ##

<p>
To run the examples quickly, we setup some maven pom.xml files for you.<br>
Here are the <a href='MavenDITutorialInstructions.md'>instructions</a> to get the examples up and running.<br>
</p>

## Dependency Injection-`AutomatedTellerMachine` using CDI ##

<p>
To use CDI to manage the dependencies, do the following:<br>
<ol><li>Create an empty <b>bean.xml</b> file under <b>META-INF</b> resource folder<br>
</li><li>Use the <b>@Inject</b> annotation to annotate a <b><code>setTransport</code></b> setter method in <b><code>AutomatedTellerMachineImpl</code></b>
</li><li>Use the <b>@Default</b> annotation to annotate the <b><code>StandardAtmTransport</code></b>
</li><li>Use the <b>@Alternative</b> to annotate the <b><code>SoapAtmTransport</code></b>, and <b><code>JsonRestAtmTransport</code></b>.<br>
</li><li>Use the <b>@Named</b> annotation to make the <b><code>AutomatedTellerMachineImpl</code></b> easy to look up; give it the name "atm"<br>
</li><li>Use the CDI <b><code>beanContainer</code></b> to look the <b>atm</b>, makes some deposits and withdraws.<br>
</p></li></ol>

### Step 1: Create an empty **bean.xml** file under **META-INF** resource folder ###
### META-INF/beans.xml ###

<p>
CDI needs an bean.xml file to be in META-INF of your jar file or classpath or<br>
WEB-INF of your web application. This file can be completely empty (as in 0 bytes).<br>
If there is no beans.xml file in your META-INF or WEB-INF then that war file or<br>
jar file will not be processed by CDI. Otherwise, CDI will scan the jar and war<br>
file if the beans.xml file exists even if it is 0 bytes.<br>
</p>

#### Code Listing: `META-INF/beans.xml` just as empty as can be ####

```
<beans xmlns="http://java.sun.com/xml/ns/javaee" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="
http://java.sun.com/xml/ns/javaee
http://java.sun.com/xml/ns/javaee/beans_1_0.xsd">

</beans>
```

<p>
Notice that we included a starter beans.xml file with a namespace and a <code>&lt;beans&gt;</code>
element. Although <b>beans.xml</b> could be completely empty, it is nice to have a<br>
starter file so when you need to add things (like later on in this tutorial)<br>
you can readily. Also it keeps the IDE from complaining about ill formed xml when you actually do have a 0 byte beans.xml. (I hate when the IDE complains. It is very distracting.)<br>
</p>

### Step 2: Use the **@Inject** annotation to annotate a **`setTransport`** setter method in **`AutomatedTellerMachineImpl`** ###

<p>
The <b>@Inject</b> annotation is used to mark where an injection goes. You can annotate constructor arguments, instance fields and setter methods of properties. In this example, we will annotate the <b>setTransport</b> method (which would be the setter method of the transport property).<br>
</p>

#### Code Listing: `AutomatedTellerMachineImpl` using **@Inject** to inject a transport ####

```
package org.cdi.advocacy;

...

import javax.inject.Inject;

public class AutomatedTellerMachineImpl implements AutomatedTellerMachine {
	
	private ATMTransport transport;

	@Inject
	public void setTransport(ATMTransport transport) {
		this.transport = transport;
	}

       ...

}

```

<p>
By default, CDI would look for a class that implements the <b><code>ATMTransport</code></b> interface, once it finds this it creates an instance and injects this instance of <b><code>ATMTransport</code></b> using the setter method <b><code>setTransport</code></b>. If we only had one possible instance of <b><code>ATMTransport</code></b> in our classpath, we would not need to annotate any of the <b><code>ATMTransport</code></b> implementations. Since we have three, namely, <b><code>StandardAtmTransport</code></b>, <b><code>SoapAtmTransport</code></b>,  and <b><code>JsonAtmTransport</code></b>, we need to mark two of them as <b><code>@Alternative</code></b>s and one as <b><code>@Default</code></b>.<br>
</p>

### Step 3: Use the **@Default** annotation to annotate the **`StandardAtmTransport`** ###

<p>
At this stage of the example, we would like our default transport to be <b><code>StandardAtmTransport</code></b>; thus, we mark it as <b><code>@Default</code></b> as follows:<br>
</p>

#### Code Listing: `StandardAtmTransport` using **@Default** ####
```
package org.cdi.advocacy;

import javax.enterprise.inject.Default;

@Default
public class StandardAtmTransport implements ATMTransport {
    ...

```

<p>
It should be noted that a class is <b><code>@Default</code></b> by default. Thus marking it so is redundant; and not only that its redundant.<br>
</p>

### Step 4: Use the **@Alternative** to annotate the **`SoapAtmTransport`**, and **`JsonRestAtmTransport`**. ###
<p>
If we don't mark the others as @<b><code>Alternative</code></b>, they are by default as far as CDI is concerned, marked as @<b><code>Default</code></b>.  Let's mark <b><code>JsonRestAtmTransport</code></b> and <b><code>SoapRestAtmTransport</code></b> <b>@Alternative</b> so CDI does not get confused.<br>
</p>

#### Code Listing: `JsonRestAtmTransport` using **@Alternative** ####
```
package org.cdi.advocacy;

import javax.enterprise.inject.Alternative;

@Alternative
public class JsonRestAtmTransport implements ATMTransport {

...
}

```

#### Code Listing: `SoapAtmTransport` using **@Alternative** ####
```
package org.cdi.advocacy;

import javax.enterprise.inject.Alternative;

@Alternative
public class SoapAtmTransport implements ATMTransport {
   ...
}

```


> ### Step 5: Use the **@Named** annotation to make the **`AutomatedTellerMachineImpl`** easy to look up; give it the name "atm" ###

<p>
Since we are not using <b><code>AutomatedTellerMachineImpl</code></b> from a Java EE 6 application,<br>
let's just use the <b><code>beanContainer</code></b> to look it up. Let's give it an easy logical name like "<b><code>atm</code></b>".<br>
To give it a name, use the @<b><code>Named</code></b> annotation. The @<b><code>Named</code></b> annotation is<br>
also used by JEE 6 application to make the bean accessible via the<br>
<a href='http://java.sun.com/products/jsp/reference/techart/unifiedEL.html'>Unified EL</a>
(EL stands for Expression language and it gets used by JSPs and JSF components).<br>
</p>

<p>
Here is an example of using @Named to give the <b><code>AutomatedTellerMachineImpl</code></b> the name "atm"as follows:<br>
</p>

#### Code Listing: `AutomatedTellerMachineImpl` using **@Named** ####
```
package org.cdi.advocacy;

import java.math.BigDecimal;

import javax.inject.Inject;
import javax.inject.Named;

@Named("atm")
public class AutomatedTellerMachineImpl implements AutomatedTellerMachine {
       ...

}
```

<p>
It should be noted that if you use the @<b><code>Named</code></b> annotations and don't provide a name, then the name<br>
is the name of the class with the first letter lower case so this:<br>
</p>

```
@Named
public class AutomatedTellerMachineImpl implements AutomatedTellerMachine {
       ...

}
```

<p>
makes the name automatedTellerMachineImpl.<br>
</p>



### Step 6: Use the CDI **`beanContainer`** to look up the **atm**, makes some deposits and withdraws. ###

<p>
Lastly we want to look up the <b>atm</b> using the <b><code>beanContainer</code></b> and make some deposits.<br>
</p>

#### Code Listing: `AtmMain` looking up the atm by name ####
```
package org.cdi.advocacy;

...

public class AtmMain {

        ...
        ...

	public static void main(String[] args) throws Exception {
		AutomatedTellerMachine atm = (AutomatedTellerMachine) beanContainer
				.getBeanByName("atm");

		atm.deposit(new BigDecimal("1.00"));

	}

}
```

<p>
When you run it from the command line, you should get the following:<br>
</p>

**Output**
```
deposit called
communicating with bank via Standard transport
```

<p>
You can also lookup the <b><code>AtmMain</code></b> by type and an optional list of Annotations as<br>
the name is really to support the Unified EL (JSPs, JSF, etc.).<br>
</p>


#### Code Listing: `AtmMain` looking up the atm by type ####
```
package org.cdi.advocacy;

...

public class AtmMain {

        ...
        ...

    public static void main(String[] args) throws Exception {
        AutomatedTellerMachine atm = beanContainer.getBeanByType(AutomatedTellerMachine.class);
        atm.deposit(new BigDecimal("1.00"));
    }

}
```

<p>
Since a big part of CDI is its type safe injection, looking up things by name is probably<br>
discouraged. Notice we have one less cast due to <a href='http://download.oracle.com/javase/tutorial/java/generics/index.html'>Java Generics</a>.<br>
</p>

<p>
If you remove the <b>@Default</b> from the <b><code>StandardATMTransport</code></b>, you will get the same output.<br>
If you remove the <b>@Alternative</b> from both of the other transports, namely,  <b><code>JsonATMTransport</code></b>, and  <b><code>SoapATMTransport</code></b>, CDI will croak as follows:<br>
</p>

**Output**
```
Exception in thread "main" java.lang.ExceptionInInitializerError
Caused by: javax.enterprise.inject.AmbiguousResolutionException: org.cdi.advocacy.AutomatedTellerMachineImpl.setTransport: 
Too many beans match, because they all have equal precedence.  
See the @Stereotype and <enable> tags to choose a precedence.  Beans:
    ManagedBeanImpl[JsonRestAtmTransport, {@Default(), @Any()}]
    ManagedBeanImpl[SoapAtmTransport, {@Default(), @Any()}]
    ManagedBeanImpl[StandardAtmTransport, {@javax.enterprise.inject.Default(), @Any()}]
   ...
```

<p>
CDI expects to find one and only one qualified injection. Later we will discuss how to use an alternative.<br>
</p>

## Using @Inject to inject via constructor args and fields ##

<p>
You can inject into fields,constructor arguments and setter methods (or any method really).<br>
</p>

<p>
Here is an example of field injections:<br>
</p>

### Code Listing: **`AutomatedTellerMachineImpl`**.**`transport`** using @Inject to do field injection. ###

```
...
public class AutomatedTellerMachineImpl implements AutomatedTellerMachine {
	
	@Inject
	private ATMTransport transport;

```


### Code Listing:  **`AutomatedTellerMachineImpl`**.**`transport`** using @**`Inject`** to do constructor injection. ###

```
...
public class AutomatedTellerMachineImpl implements AutomatedTellerMachine {
	
	@Inject 
	public AutomatedTellerMachineImpl(ATMTransport transport) {
		this.transport = transport;
	}

```

This flexibility allows you to create classes that are easy to unit test.

## Using simple @Produces ##

<p>
There are times when the creation of an object may be complex.<br>
Instead of relying on a constructor, you can delegage to a factory class to<br>
create the instance. To do this with CDI, you would use the @Produces from<br>
your factory class as follows:<br>
</p>

### Code Listing: **`TransportFactory`**.**`createTransport`** using @Produces to define a factory method ###

```
package org.cdi.advocacy;

import javax.enterprise.inject.Produces;

public class TransportFactory {
		
	@Produces ATMTransport createTransport() {
		System.out.println("ATMTransport created with producer");
		return new StandardAtmTransport();
	}

}
```

<p>
The factory method could use qualifiers just like a class declaration. In this example, we chose not to.<br>
The <b><code>AutomatedTellerMachineImpl</code></b> does not need to specify any special qualifiers. Here is the <b><code>AutomatedTellerMachineImpl</code></b>
that receives the simple producer.<br>
</p>

### Code Listing: **`AutomatedTellerMachineImpl`** receives the simple producer ###

```
import javax.inject.Inject;
import javax.inject.Named;

@Named("atm")
public class AutomatedTellerMachineImpl implements AutomatedTellerMachine {
	
	@Inject
	private ATMTransport transport;
        ...
```

<p>
Check your understanding by looking at the output of running this with <b><code>AtmMain</code></b>.<br>
</p>

**Output**
```
ATMTransport created with producer
deposit called
communicating with bank via Standard transport
```



## Using @Alternative to select an Alternative ##

<p>
Earlier, you may recall, we defined several alternative transports, namely, <b><code>JsonRestAtmTransport</code></b> and <b><code>SoapRestAtmTransport</code></b>.<br>
Imagine that you are an installer of ATM machines and you need to configure certain transports at certain locations.<br>
Our previous injection points essentially inject the default which is the <b><code>StandardRestAtmTransport</code></b> transport.<br>
</p>

If I need to install a different transport, all I need to do is change the /META-INF/beans.xml file to use the right transport as follows:

### Code Listing:  **`{classpath}/META-INF/beans.xml`** ###
```
<beans xmlns="http://java.sun.com/xml/ns/javaee" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="
http://java.sun.com/xml/ns/javaee
http://java.sun.com/xml/ns/javaee/beans_1_0.xsd">
	<alternatives>
		<class>org.cdi.advocacy.JsonRestAtmTransport</class>
	</alternatives>
</beans>
```
<p>
You can see from the output that the JSON REST transport is selected.<br>
</p>

**Output**
```
deposit called
communicating with bank via JSON REST transport
```

<p>
Alternatives codifies and simplifies a very normal case in DI, namely, you have different injected objects based on different builds or environments.<br>
The great thing about objects is they can be replaced (Grady Booch said this).<br>
Alternatives allow you to mark objects that are replacements for other objects and then activate them when you need them.<br>
</p>

<p>
If the DI container can have alternatives, let's mark them as alternatives.<br>
Think about it this way. I don't have to document all of the alternatives as much.<br>
It is self documenitng. If someone knows CDI and they know about Alternatives they will not be surprised.<br>
Alternatives really canoncalizes the way you select an Alternative.<br>
</p>

<p>
You can think of CDI as a canonicalization of many patterns that we have been using with more general purpose DI frameworks.<br>
The simplifcation and canonicalization is part of the evoluiton of DI.<br>
</p>

## Code Listing: Using @Qualifier to inject different types ##

<p>
All objects and producers in CDI have qualifiers. If you do not assign a qaulifier<br>
it by default has the qualifier @<b><code>Default</code></b> and @<b><code>Any</code></b>. It is like a TV crime show<br>
in the U.S., if you do not have money for a lawyer, you will be assigned one.<br>
</p>

<p>
Qualifiers can be used to discriminate exaclty what gets injected.<br>
You can write custom qualifiers.<br>
</p>

<p>
Qualifiers work like <a href='http://www.garanimals.com/about.htm'>garanimal</a> tags for kids clothes, you match the qualifier from the injection<br>
target and the injection source, then that is the type that will be injected.<br>
</p>

<p>
If the tags (Qualifiers) match, then you have a match for injection.<br>
</p>

<p>
You may decide that at times you want to inject <b><code>Soap</code></b> or <b><code>Json</code></b> or the <b><code>Standard</code></b> transport.<br>
You don't want to list them as an alternative. You actually, for example, always want the <b><code>Json</code></b> implementation in a certain case.<br>
</p>

<p>
Here is an example of defining a qualifier for <b><code>Soap</code></b>.<br>
</p>

### Code Listing: **`Soap`** runtime qualifier annotation ###
```
package org.cdi.advocacy;

import java.lang.annotation.Retention;
import java.lang.annotation.Target;
import static java.lang.annotation.ElementType.*;
import static java.lang.annotation.RetentionPolicy.*;

import javax.inject.Qualifier;


@Qualifier @Retention(RUNTIME) @Target({TYPE, METHOD, FIELD, PARAMETER})
public @interface Soap {

}

```

<p>
Notice that a qualifier is just a runtime annotation that is marked with the @<b><code>Qualifier</code></b> annotation.<br>
The @<b><code>Qualifier</code></b> is an annotation that decorates a runtime annoation to make it a qualifier.<br>
</p>

<p>
Then we would just mark the source of the injection point, namely, <b><code>SoapAtmTransport</code></b> with our new @<b><code>Soap</code></b> qualifier as follows:<br>
</p>

### Code Listing: **`SoapAtmTransport`** using new @**`Soap`** qualifier ###
```
package org.cdi.advocacy;

@Soap
public class SoapAtmTransport implements ATMTransport {

	@Override 
	public void communicateWithBank(byte[] datapacket) {
		System.out.println("communicating with bank via Soap transport");
	}

}
```

Next time you are ready to inject a **`Soap`** transport we can do that by annotating the
argument to the constructor as follows:

### Code Listing: **`AutomatedTellerMachineImpl`** injecting **`SoapAtmTransport`** using new @**`Soap`** qualifier via constructor arg ###
```
public class AutomatedTellerMachineImpl implements AutomatedTellerMachine {
	
	private ATMTransport transport;

	@Inject 
	public AutomatedTellerMachineImpl(@Soap ATMTransport transport) {
		this.transport = transport;
	}

```

You could also choose to do this via the setter method for the property as follows:

### Code Listing: **`AutomatedTellerMachineImpl`** injecting **`SoapAtmTransport`** using new @**`Soap`** qualifier via setter method arg ###

```
public class AutomatedTellerMachineImpl implements AutomatedTellerMachine {
	
	private ATMTransport transport;

	@Inject 
	public void setTransport(@Soap ATMTransport transport) {
		this.transport = transport;
	}
```

And a very common option is to use a field level injection as follows:

### Code Listing: **`AutomatedTellerMachineImpl`** injecting **`SoapAtmTransport`** using new @**`Soap`** qualifier via setter method arg ###
```
public class AutomatedTellerMachineImpl implements AutomatedTellerMachine {
	
	@Inject @Soap
	private ATMTransport transport;

```

From this point on, we are just going to use field level injection to simplify the examples.

## Using @Qualfiers to inject multiple types into the same bean using ##

<p>
Let's say that our ATM machine uses different transport based on some business rules<br>
that are configured in LDAP or config file or XML or a database (does not really matter).<br>
</p>

<p>
The point is you want it decided at runtime which transport we are going to use.<br>
</p>

<p>
In this scenario we may want to inject three different transports and then configure<br>
a transport based on the business rules.<br>
</p>

<p>
You are going to want to get notified when the injection is done and the bean is ready to go from a CDI perspective.<br>
To get this notifcation you would annotated an init method with the @PostConstruct annotation. Then you could pick<br>
which type of transport that you want to use.<br>
</p>


Note the name of the method does not matter, it is the annotation that makes it an init method.

### Code Listing: **`AutomatedTellerMachineImpl`** injecting multiple transports using new multiple qualifiers ###
```
package org.cdi.advocacy;

import java.math.BigDecimal;

import javax.annotation.PostConstruct;
import javax.inject.Inject;
import javax.inject.Named;

@Named("atm")
public class AutomatedTellerMachineImpl implements AutomatedTellerMachine {
	
	private ATMTransport transport;
	
	@Inject @Soap
	private ATMTransport soapTransport;
	
	@Inject @Json
	private ATMTransport jsonTransport;
	
	@Inject @Json
	private ATMTransport standardTransport;

	
	//These could be looked up in a DB, JNDI or a properties file.
	private boolean useJSON = true;
	private boolean behindFireWall = true;

	@PostConstruct
	protected void init() {
                //Look up values for useJSON and behindFireWall		

		if (!behindFireWall) {
			transport = standardTransport;
		} else {
			if (useJSON) {
				transport = jsonTransport;
			} else {
				transport = soapTransport;
			}
		}
				
	}
	

	public void deposit(BigDecimal bd) {
		System.out.println("deposit called");
		
		
		transport.communicateWithBank(null);
	}

       ...
}

```

Try to follow the code above. Try to guess the output.
Now compare it to this:

**Output**
```
deposit called
communicating with bank via JSON REST transport
```

How did you do?

## Using @Producer to make a decision about creation ##

This example builds on the last.

<p>Perhaps you want to seperate the construction and selection of the transports<br>
from the <b><code>AutomatedTellerMachineImpl</code></b>.<br>
</p>

<p>
You could create a <b><code>Producer</code></b> factory method that makes a decision about the<br>
creation and selection of the transport as follows:<br>
</p>

### Code Listing: **`TransportFactory`** deciding which transport to use/create ###
```
package org.cdi.advocacy;

import javax.enterprise.inject.Produces;

public class TransportFactory {
	
	private boolean useJSON = true;
	private boolean behindFireWall = true;

	
	@Produces ATMTransport createTransport() {
		//Look up config parameters in some config file or LDAP server or database

		System.out.println("ATMTransport created with producer makes decisions");
		
		if (behindFireWall) {
			if (useJSON) {
				System.out.println("Created JSON transport");
				return new JsonRestAtmTransport();
			} else {
				System.out.println("Created SOAP transport");
				return new SoapAtmTransport();
			}
		} else {
			System.out.println("Created Standard transport");
			return new StandardAtmTransport();
		}
	}

}

```

<p>
The advantage of this approach is that the logic to do the creation,<br>
is seperate from the actual <b><code>AutomatedTellerMachineImpl</code></b> code.<br>
</p>

<p>
This may not always be what you want, but if it is, then the producer can help you.<br>
</p>

<p>
The output should be the same as before.<br>
</p>

**Output**
```
ATMTransport created with producer makes decisions
Created JSON transport
deposit called
communicating with bank via JSON REST transport
```



## Using @Producer that uses qualifiers to make a decision about creation ##

This example builds on the last.

<p>You can also inject items as arguments into the producer as follows:</p>

### Code Listing: **`TransportFactory`** injecting qualifier args ###
```
package org.cdi.advocacy;

import javax.enterprise.inject.Produces;

public class TransportFactory {
	
	private boolean useJSON = true;
	private boolean behindFireWall = true;

	
	@Produces ATMTransport createTransport(	@Soap ATMTransport soapTransport, 
						@Json ATMTransport jsonTransport) {
		//Look up config parameters in some config file
		System.out.println("ATMTransport created with producer makes decisions");
		
		if (behindFireWall) {
			if (useJSON) {
				System.out.println("return passed JSON transport");
				return jsonTransport;
			} else {
				System.out.println("return passed SOAP transport");
				return soapTransport;
			}
		} else {
			System.out.println("Create Standard transport");
			return new StandardAtmTransport();
		}
	}

}

```

<p>
In the above example, <b><code>createTransport</code></b> becomes less of a factory method and more of a selection method<br>
as CDI actually creates and passes the <b><code>soapTransport</code></b> and the <b><code>jsonTransport</code></b>.<br>
</p>

<p>
<b>Advanced topic</b>: (Ignore this if it does not make sense)<br>
You may wonder why I create <b><code>StandardAtmTransport</code></b> and not inject it as a<br>
producer argument like <b><code>soapTransport</code></b> and <b><code>jsonTransport</code></b>. The problem is this<br>
<b><code>createTransport</code></b> is by default @<b><code>Default</code></b> and @<b><code>Any</code></b> but it overrides the <b><code>StandardAtmTransport</code></b>
which is also by default @<b><code>Default</code></b> and @<b><code>Any</code></b>, but since <b><code>StandardAtmTransport</code></b> is overidden<br>
then if I inject <b><code>@Default ATMTransport standardTransport</code></b> as an argument then<br>
it tries to call <b><code>createTransport</code></b> since it is the @<b><code>Default</code></b>, which will then try to inject<br>
the argument <b><code>standardTransport</code></b>, which will then call <b><code>createTransport</code></b>, ad infinitum until<br>
we get a <b><code>StackTraceOverflow</code></b>. The solution is create a qualifier for the standard, say,<br>
@<b><code>Standard</code></b> and use that to do the injection, or create one for the <b><code>createProduces</code></b> production, say,<br>
@<b><code>Transport</code></b>. The key here is that the injection arguments of a producer have to have different qualifiers than the<br>
production method or all hell breaks lose, cats sleeping with dogs, pandimodium. Ok. Okay.<br>
The key here is that the injection arguments have to have different qualifiers than the<br>
production method or you will get a <b><code>StackTraceOverflow</code></b> as CDI calls your production method<br>
to resovle the injection point of you production method ad infinitum.<br>
</p>

<p>
Here is the expected output.<br>
</p>

**Output**
```
ATMTransport created with producer makes decisions
return passed JSON transport
deposit called
communicating with bank via JSON REST transport
```


## Using multiple @Qualifiers at the same injection point to discriminate further ##

You can use more than one qaulifier to further discriminate your injection target.

<p>
To demonstrate this let's define to qualifiers <b><code>SuperFast</code></b> and <b><code>StandardFrameRelaySwitchingFlubber</code></b>.<br>
Let's say at the time we have two transports that are <b><code>StandardFrameRelaySwitchingFlubber</code></b>.<br>
Let's also say that you want to inject a <b><code>transport</code></b> that is not only a <b><code>StandardFrameRelaySwitchingFlubber</code></b>
but also <b><code>SuperFast</code></b>.<br>
</p>

First let's define the qualifier annotations as follows:

### Code Listing: **`SuperFast`** defining a new qualifier ###
```
package org.cdi.advocacy;

...

@Qualifier @Retention(RUNTIME) @Target({TYPE, METHOD, FIELD, PARAMETER})
public @interface SuperFast {

}

```

### Code Listing: **`StandardFrameRelaySwitchingFlubber`** defining another new qualifier ###
```
package org.cdi.advocacy;

...

@Qualifier @Retention(RUNTIME) @Target({TYPE, METHOD, FIELD, PARAMETER})
public @interface StandardFrameRelaySwitchingFlubber {

}

```

Ok, here is the code for the **`SuperFastAtmTransport`** which is marked with both the
@**`SuperFast`** and the @**`StandardFrameRelaySwitchingFlubber`** qualifiers.

### Code Listing: **`SuperFastAtmTransport`** uses two qualifiers ###
```
package org.cdi.advocacy;

@SuperFast @StandardFrameRelaySwitchingFlubber 
public class SuperFastAtmTransport implements ATMTransport {
	public void communicateWithBank(byte[] datapacket) {
		System.out.println("communicating with bank via the Super Fast transport " );
	}
}

```


Ok, we add the **`StandardFrameRelaySwitchingFlubber`** to the **`StandardAtmTransport`** as well.

### Code Listing: **`StandardAtmTransport`** changed to use one qualifier ###
```
package org.cdi.advocacy;


@StandardFrameRelaySwitchingFlubber @Default
public class StandardAtmTransport implements ATMTransport {
	public void communicateWithBank(byte[] datapacket) {
		System.out.println("communicating with bank via Standard transport");
	}

}

```


Next if I want my AutomatedTellerMachineImpl to have **`SuperFast`** transport with **`StandardFrameRelaySwitchingFlubber`**, I would
use both in the injection target as follows:


### Code Listing: **`AutomatedTellerMachineImpl`** changed to use two qualifier ###
```
public class AutomatedTellerMachineImpl implements AutomatedTellerMachine {
	
	@Inject @SuperFast @StandardFrameRelaySwitchingFlubber
	private ATMTransport transport;
       ...
```

Output:

```
deposit called
communicating with bank via the Super Fast transport 
```

<p>
Exercise: Create a transport that is @SuperFast, @StandardFrameRelaySwitchingFlubber and an @Alternative.<br>
Then use beans.xml to activate this SuperFast, StandardFrameRelaySwitchingFlubber,  Alternative transport.<br>
Send me your solution on the <a href='http://groups.google.com/group/cdiadvocate4j?pli=1'>CDI group mailing list</a>.<br>
The first one to send gets put on the CDI wall of fame.<br>
</p>

<p>
Exercise for the reader. Change the injection point qualifiers to make only  the<br>
<b><code>StandardAtmTransport</code></b> get injected.<br>
Send me your solution on the <a href='http://groups.google.com/group/cdiadvocate4j?pli=1'>CDI group mailing list</a>.<br>
Don't get discouraged if you get a stack trace or two that is part of the learning process.<br>
The first one to send gets put on the CDI wall of fame (everyone else gets an honorable mention).<br>
</p>

## Using @Qualfiers with members to discriminate injection and stop the explosion of annotation creation ##

<p>
There could be an explosion of qualifers annotations in your project.<br>
Imagine in our example if there were 20 types of transports. We would have 20 annotations defined.<br>
</p>

<p>
This is probably not want you want.<br>
It is okay if you have a few, but it could quickly become unmanageable.<br>
</p>

<p>
CDI allows you to descriminate on members of a qualifier to reduce the explosion of qualifiers.<br>
Instead of having three qualifier you could have one qualifier and an enum.<br>
Then if you need more types of transports, you only have to add an enum value instead of another class.<br>
</p>

<p>
Let's demonstrate how this works by creating a new qualifier annotation called <b><code>Transport</code></b>.<br>
The <b><code>Transport</code></b> qualifier annotation will have a single member, an enum called <b><code>type</code></b>. The <b><code>type</code></b> member<br>
will be an new enum that we define called <b><code>TransportType</code></b>.<br>
</p>

Here is the new **`TransportType`**:

### Code Listing: **`Transport`** qualifier that has an enum member ###
```
package org.cdi.advocacy;

import java.lang.annotation.Retention;
import java.lang.annotation.Target;
import static java.lang.annotation.ElementType.*;
import static java.lang.annotation.RetentionPolicy.*;

import javax.inject.Qualifier;


@Qualifier @Retention(RUNTIME) @Target({TYPE, METHOD, FIELD, PARAMETER})
public @interface Transport {
	TransportType type() default TransportType.STANDARD;
}

```

Here is the new enum that is part of the **`TransportType`**.
### Code Listing: **`TransportType`** enum that defines a type ###
```
package org.cdi.advocacy;

public enum TransportType {
	JSON, SOAP, STANDARD;
}
```


Next you need to qualify your transport instances like so:

### Code Listing: **`SoapAtmTransport`** using **`@Transport(type=TransportType.SOAP)`** ###
```
package org.cdi.advocacy;


@Transport(type=TransportType.SOAP)
public class SoapAtmTransport implements ATMTransport {
    ...
```


### Code Listing: **`StandardAtmTransport`** using **`@Transport(type=TransportType.STANDARD)`** ###
```
package org.cdi.advocacy;

@Transport(type=TransportType.STANDARD)
public class StandardAtmTransport implements ATMTransport {
    ...

```

### Code Listing: **`JsonRestAtmTransport`** using **`@Transport(type=TransportType.JSON)`** ###
```
package org.cdi.advocacy;

@Transport(type=TransportType.JSON)
public class JsonRestAtmTransport implements ATMTransport {
     ...
```

### Code Listing: **`AutomatedTellerMachineImpl`** using **`@Inject @Transport(type=TransportType.STANDARD)`** ###
```
@Named("atm")
public class AutomatedTellerMachineImpl implements AutomatedTellerMachine {

	@Inject @Transport(type=TransportType.STANDARD)
	private ATMTransport transport;

```

<p>
As always, you will want to run the example.<br>
</p>

Output
```
deposit called
communicating with bank via Standard transport
```

You can have more than one member of the qualifier annotation as follows:

### Code Listing: **`Transport`** qualifier annotation with more than one member ###
```
package org.cdi.advocacy;

import java.lang.annotation.Retention;
import java.lang.annotation.Target;
import static java.lang.annotation.ElementType.*;
import static java.lang.annotation.RetentionPolicy.*;

import javax.inject.Qualifier;


@Qualifier @Retention(RUNTIME) @Target({TYPE, METHOD, FIELD, PARAMETER})
public @interface Transport {
	TransportType type() default TransportType.STANDARD;
	int priorityLevel() default -1;
}

```

<p>
Now CDI is going to use both of the members to discriminate for injection.<br>
</p>

If we had a transport like so:

### Code Listing: **`SuperFastAtmTransport`** using two qualifier members to qualify ###
```
package org.cdi.advocacy;

@Transport(type=TransportType.STANDARD, priorityLevel=1)
public class SuperFastAtmTransport implements ATMTransport {
	

	public void setRetries(int retries) {
	}


	public void communicateWithBank(byte[] datapacket) {
		System.out.println("communicating with bank via the Super Fast transport ");
	}

}

```

No changes to the StandardAtmTransport.

<p>
If we run without changing the <b><code>AutomatedTellerMachineImpl</code></b>, we will get:<br>
</p>

Output
```
deposit called
communicating with bank via the Standard transport 
```

If we change the injection and set the priority level to 1 like so:

### Code Listing: **`AutomatedTellerMachineImpl`** using two qualifier members to discriminate ###
```
public class AutomatedTellerMachineImpl implements AutomatedTellerMachine {
	
	@Inject @Transport(type=TransportType.STANDARD, priorityLevel=1)
	private ATMTransport transport;


```

<p>
Then we get this:<br>
</p>

Output

```
deposit called
communicating with bank via the Super Fast transport 
```

<p>
You can match using any type supported by annotations, e.g., Strings, classes, enums, ints, etc.<br>
</p>

<p>
Exercise: Add a member String to the qualifier annotation. Change the injection point to discriminate using<br>
this new string member. Why do you think this is counter to what CDI stands for?<br>
Send me your solution on the <a href='http://groups.google.com/group/cdiadvocate4j?pli=1'>CDI group mailing list</a>.<br>
The first one to send gets put on the CDI wall of fame. (All others get honorable mentions.)<br>
</p>

# Advanced CDI tutorial #
The faint of heart stop hear. All of the folks who want to understand the inner workings of CDI continue.
So far, we have been at the shallow, warm end of the pool. Things are about to get a little deeper and colder.
If you need to master CDI, then this section if for you.

## Advanced: Using @Produces and **`InjectionPoint`** to create configuration annotations ##

Our ultimate goal is to define an annotation that we can use to configure the retry count on a transport.
Essentially, we want to pass a retry count to the transport.

We want something that looks like this:

### Code Listing: **`TransportConfig`** annotations that does configuration ###
```
	@Inject @TransportConfig(retries=2)
	private ATMTransport transport;

```

(This was my favorite section to write, because I wanted to know how to create a
annotation configuration from the start.)


Before we do that we need to learn more about @**`Produces`** and **`InjectionPoint`**s.
We are going to use a producer to read information (meta-data) about an injection point.

An [\*`InjectionPoint`\*](http://download.oracle.com/javaee/6/api/javax/enterprise/inject/spi/InjectionPoint.html)
is a class that has information about an injection point. You can learn things
like what is being decorated, what the target injection type is, what the source injection type,
what is the class of the owner of the member that is being injected and so forth.


Let's learn about passing an injection point to @**`Produces`**. Below I have rewritten our simple @Produces
example, except this time I pass an **`InjectionPoint`** argument into the mix.


### Code Listing: **`TransportFactory`** getting meta-data about the injection point ###
```
package org.cdi.advocacy;

import javax.enterprise.inject.Produces;
import javax.enterprise.inject.spi.InjectionPoint;

public class TransportFactory {
	
	
	@Produces ATMTransport createTransport(InjectionPoint injectionPoint) {
		
		System.out.println("annotated " + injectionPoint.getAnnotated());
		System.out.println("bean " + injectionPoint.getBean());
		System.out.println("member " + injectionPoint.getMember());
		System.out.println("qualifiers " + injectionPoint.getQualifiers());
		System.out.println("type " + injectionPoint.getType());
		System.out.println("isDelegate " + injectionPoint.isDelegate());
		System.out.println("isTransient " + injectionPoint.isTransient());
	
		return new StandardAtmTransport();
				
	}

}

The above produces this output.

```

Output
```
annotated AnnotatedFieldImpl[private org.cdi.advocacy.ATMTransport org.cdi.advocacy.AutomatedTellerMachineImpl.transport]
bean ManagedBeanImpl[AutomatedTellerMachineImpl, {@javax.inject.Named(value=atm), @Default(), @Any()}, name=atm]
member private org.cdi.advocacy.ATMTransport org.cdi.advocacy.AutomatedTellerMachineImpl.transport
qualifiers [@Default()]
type interface org.cdi.advocacy.ATMTransport
isDelegate false
isTransient false
deposit called
communicating with bank via Standard transport
```

It appears from the output that annotated tells us which area of the program was annotated.
It also appears that bean tells us which bean the injection is happending in.


From this output you can see that the **`annotated`** property on the **`injectionPoint`**
has information about which language feature (field, constructor argument, method argument, etc.).
In our case it is the field **`org.cdi.advocacy.AutomatedTellerMachineImpl.transport`**.
is being used as the target of the injection, it is the thing that was **`annotated`**.

From this output you can see that the **`bean`** property of the **`injectionPoint`**
is being used to describe the bean whose member is getting injected. In this case,
it is the **`AutomatedTellerMachineImpl`** whose is getting the field injected.

I won't describe each property, but as an exercise you can.

Exercise: Look up the **`InjectionPoint`** in the [API documentation](http://download.oracle.com/javaee/6/api/javax/enterprise/inject/spi/InjectionPoint.html).
Find out what the other properties mean. How might you use this meta-data?
Can you think of a use case or application where it might be useful?
Send me your answers on the [CDI group mailing list](http://groups.google.com/group/cdiadvocate4j?pli=1).
The first one to send gets put on the CDI wall of fame. (All others get honorable mentions.)



Drilling further you can see what is in the beans and annotated properties.

### Code Listing: **`TransportFactory.createTransport`** drilling further into the meta-data about the injection point ###
```
	@Produces ATMTransport createTransport(InjectionPoint injectionPoint) {
		
		System.out.println("annotated " + injectionPoint.getAnnotated());
		System.out.println("bean " + injectionPoint.getBean());
		System.out.println("member " + injectionPoint.getMember());
		System.out.println("qualifiers " + injectionPoint.getQualifiers());
		System.out.println("type " + injectionPoint.getType());
		System.out.println("isDelegate " + injectionPoint.isDelegate());
		System.out.println("isTransient " + injectionPoint.isTransient());

		Bean<?> bean = injectionPoint.getBean();
		
		System.out.println("bean.beanClass " + bean.getBeanClass());
		System.out.println("bean.injectionPoints " + bean.getInjectionPoints());
		System.out.println("bean.name " + bean.getName());
		System.out.println("bean.qualifiers " + bean.getQualifiers());
		System.out.println("bean.scope " + bean.getScope());
		System.out.println("bean.stereotypes " + bean.getStereotypes());
		System.out.println("bean.types " + bean.getTypes());
		
		Annotated annotated = injectionPoint.getAnnotated();
		System.out.println("annotated.annotations " + annotated.getAnnotations());
		System.out.println("annotated.annotations " + annotated.getBaseType());
		System.out.println("annotated.typeClosure " + annotated.getTypeClosure());
		
		return new StandardAtmTransport();
}
```

Now we are cooking with oil. Throw some gas on that flame. Look at the wealth of information
that the **`InjectionPoint`** defines.

Output
```
...
bean.beanClass class org.cdi.advocacy.AutomatedTellerMachineImpl
bean.injectionPoints [InjectionPointImpl[private org.cdi.advocacy.ATMTransport org.cdi.advocacy.AutomatedTellerMachineImpl.transport]]
bean.name atm
bean.qualifiers [@javax.inject.Named(value=atm), @Default(), @Any()]
bean.scope interface javax.enterprise.context.Dependent
bean.stereotypes []
bean.types [class org.cdi.advocacy.AutomatedTellerMachineImpl, interface org.cdi.advocacy.AutomatedTellerMachine, class java.lang.Object]
annotated.annotations AnnotationSet[@javax.inject.Inject()]
annotated.annotations interface org.cdi.advocacy.ATMTransport
annotated.typeClosure [interface org.cdi.advocacy.ATMTransport, class java.lang.Object]
...
```

We see that **`bean.beanClass`** gives up the class of the bean that is getting the
injected field. Remember that one, we will use it later.

We can see that **`bean.qualifiers*` gives up the list of qualifiers for the**`AutomatedTellerMachineImpl`**.**

We can also see that **`annotated.annotations`** gives us the list of annotations that are associated with the injected field.
We will use this later to pull the configuration annotation and configure the transport with it.

Exercise: Look up the **`Bean`** and **`Annotated`** in the [API documentation](http://download.oracle.com/javaee/6/api/index.html?javax/enterprise/inject/spi/package-summary.html).
Find out what the other properties mean. How might you use this meta-data?
Can you think of a use case or application where it might be useful?
Send me your answers on the [CDI group mailing list](http://groups.google.com/group/cdiadvocate4j?pli=1).
The first one to send gets put on the CDI wall of fame. (All others get honorable mentions.)



Ok now that we armed with an idea of what an **`Injection`** point is. Let's get configuring our transport.

First let's define an **`TransportConfig`** annotation. This is just a plain runtime annotation as follows:


### Code Listing: **`TransportConfig`** an annotation used for configuration ###
```
package org.cdi.advocacy;


import java.lang.annotation.Retention;
import java.lang.annotation.Target;
import static java.lang.annotation.ElementType.*;
import static java.lang.annotation.RetentionPolicy.*;



@Retention(RUNTIME) @Target({TYPE, METHOD, FIELD, PARAMETER})
public @interface TransportConfig {
	int retries() default 5;
}

```

Notice that this annotation has one member retries, which we will use to configure
the **`ATMTransport`** (**`transport`**).

Now go ahead and use this to decorate the injection point as follows:

### Code Listing: **`AutomatedTellerMachineImpl`** using **`TransportConfig`** to configure retries ###
```
public class AutomatedTellerMachineImpl implements AutomatedTellerMachine {
	
	@Inject @TransportConfig(retries=2)
	private ATMTransport transport;

```

Once it is configured when you run it, you will see the following output from our producer:

Output
```
annotated.annotations AnnotationSet[@javax.inject.Inject(), @org.cdi.advocacy.TransportConfig(retries=2)]
```

This means the annotation data is there. We just need to grab it and use it. Stop and ponder on this a bit.
This is pretty cool. The producer allows me to customize how annotations are consumed.
This is powerful stuff and one of the many extention points avaialable to CDI.

Please recall that the **`injectionPoint.annotated.annotations`** gives us the
list of annotations that are associated with the injected field, namely, the transport field of the
AutomatedTellerMachineImpl.Now we can use this to pull the configuration annotation
and configure the transport with it. The party is rolling now.



Now we need to change the transport implementations to handle setting retires.
Since this is an example, I will do this simply
by adding a new setter method for retires (setRetries) to the ATMTranport interface like so:

### Code Listing: **`ATMTransport`** adding a retries property ###
```
package org.cdi.advocacy;

public interface ATMTransport {
	public void communicateWithBank(byte[] datapacket);
	public void setRetries(int retries);
}

```

Then we need to change each of the transport to handle this new property as follows:

### Code Listing: **`StandardAtmTransport`** adding a retries property ###
```
package org.cdi.advocacy;

public class StandardAtmTransport implements ATMTransport {
	
	private int retries;

	public void setRetries(int retries) {
		this.retries = retries;
	}


	public void communicateWithBank(byte[] datapacket) {
		System.out.println("communicating with bank via Standard transport retries=" + retries);
	}

}
```

Now we just change the producer to grab the new annotation and configure the transport as follows:

(For clarity I took out all of the Sysout.prinltns)


### Code Listing: **`TransportFactory`** using the annotation configuration to configure a new instance of the transport ###

```
package org.cdi.advocacy;

...
import javax.enterprise.inject.spi.Annotated;
import javax.enterprise.inject.spi.Bean;
import javax.enterprise.inject.spi.InjectionPoint;

public class TransportFactory {
	@Produces ATMTransport createTransport(InjectionPoint injectionPoint) {
		
		Annotated annotated = injectionPoint.getAnnotated();
		
		TransportConfig transportConfig = annotated.getAnnotation(TransportConfig.class);
		
		
		
		StandardAtmTransport transport = new StandardAtmTransport();
		
		transport.setRetries(transportConfig.retries());
		return transport;
	}

}

```

(Side Note we are missing a null pointer check. The annotation configuration could
be null if the user did not set it, you may want to handle this. The example is kept deliberately short.)

The code just gets the annotation and shoves in the retires into the transport, and then just returns the transport.

We now have a producers that can use an annotation to configure an injection.

Here is our new output:

**Output**
```
...
deposit called
communicating with bank via Standard transport retries=2
```

You can see our retries are there as we configured them in the annotation.


Ok we are done with this example. What remains is a victory lap.
Let's say we had multiple transports in a single ATM and you wanted to configure all of the outputs at once.

Let's configure the tranport
based on an annotaion in the parent class of the injection target, namely, **`AutomatedTellerMachine`**.

### Code Listing: **`TransportFactory`** using the annotation configuration from class not field to configure a new instance of the transport ###
```
public class TransportFactory {
	@Produces ATMTransport createTransport(InjectionPoint injectionPoint) {
		
		Bean<?> bean = injectionPoint.getBean();
		TransportConfig transportConfig = bean.getBeanClass().getAnnotation(TransportConfig.class);

		StandardAtmTransport transport = new StandardAtmTransport();
		
		transport.setRetries(transportConfig.retries());
		return transport;

```

It is an exercise for the reader to make the injection level annotation
(from the last example) override the class level annotations.


Output
```
deposit called
communicating with bank via Standard transport retries=7
```

Exercise: Make the injection from the field override the injection from the class.
It is a mere matter of Java code.
Send me your solution on the [CDI group mailing list](http://groups.google.com/group/cdiadvocate4j?pli=1).
The first one to send gets put on the CDI wall of fame. (All others get honorable mentions.)

## Advanced Using @Nonbinding to combine a configuration annotation and a qaulifier annotation into one annotation ##

In the section titled **"Using @Qualfiers with members to discriminate injection and stop the explosion of annotation creation"**
we covered adding additional members to a qualifier annotation and
then in **"Advanced: Using @Produces and InjectionPoint to create configuration annotations"**
we talked about how to write an annotation to configure an injection.
Wouldn't be great if we could combine these two concepts into one annotation?

The problem is that qualifier members are used to do the discrimination.
We need some qualifier members that are not used for configuration not discrimination.

To make an qualifier member just a configuration member use @**`Nonbinding`** annotation as follows:

### Code Listing: **`Transport`** qualifier annotation using @**`Nonbinding`** to add configuration retries param ###
```
package org.cdi.advocacy;

import java.lang.annotation.Retention;
import java.lang.annotation.Target;
import static java.lang.annotation.ElementType.*;
import static java.lang.annotation.RetentionPolicy.*;

import javax.enterprise.util.Nonbinding;
import javax.inject.Qualifier;


@Qualifier @Retention(RUNTIME) @Target({TYPE, METHOD, FIELD, PARAMETER})
public @interface Transport {
	TransportType type() default TransportType.STANDARD;
	int priorityLevel() default -1;
	String name() default "standard";
	
	@Nonbinding int retries() default 5;

}
```

Now let's add the setRetries to the Fast Transport:

### Code Listing: **`Transport`** qualifier annotation using @**`Nonbinding`** to add configuration retries param ###
```
package org.cdi.advocacy;

@Transport(type=TransportType.STANDARD, priorityLevel=1, name="super")
public class SuperFastAtmTransport implements ATMTransport {
	private int retries=0;

	public void setRetries(int retries) {
		this.retries=retries;
	}


	public void communicateWithBank(byte[] datapacket) {
		System.out.println("communicating with bank via the Super Fast transport retries=" + retries);
	}

}

```

Then we use it as follows:

```
public class AutomatedTellerMachineImpl implements AutomatedTellerMachine {
	
	@Inject @Transport(type=TransportType.STANDARD, priorityLevel=1, name="super", retries=9)
	private ATMTransport transport;
        ...
```

**Ouptut**
```
deposit called
communicating with bank via Standard transport retries=9
```

The final result is we have one annotation that does both qualification and configuration.
Booyah!

Exercise:
There is an easter egg in this example. There is concept we talked about earlier in the
qualifier discrimination but never added. Please find it and describe it.
What are some potential problems of using this approach?
Send me your answers on the [CDI group mailing list](http://groups.google.com/group/cdiadvocate4j?pli=1).
The first one to send gets put on the CDI wall of fame. (All others get honorable mentions.)


## Advanced: Using Instance to inject transports ##

The use of the class Instance allows you to dynamically look up instances of a certain type.
These instances can be instances that are in a jar file.
For example the AutomatedTellerMachine could work with transports
that did not even exist when the AutomatedTellerMachine was created.
The Instance class is one of the things that makes CDI so cool and flexible.
In this section, I hope to give it some justice while still keeping the example small
and understandable.


Let's say we wanted to work with multiple transports.
But we don't know which transport is configured and on the classpath.
It could be that the build was special for a certain type of transport, and it
just does not exist on the classpath. Suspend disbelief for a moment and let's look
a the code.

### Code Listing: **`AutomatedTellerMachineImpl`** using **`Instance`** ###
```
package org.cdi.advocacy;

import java.math.BigDecimal;

import javax.annotation.PostConstruct;
import javax.enterprise.inject.Default;
import javax.enterprise.inject.Instance;
import javax.inject.Inject;
import javax.inject.Named;

@Named("atm")
public class AutomatedTellerMachineImpl implements AutomatedTellerMachine {
	
	@Inject @Soap 
	private Instance<ATMTransport> soapTransport;

	@Inject @Json 
	private Instance<ATMTransport> jsonTransport;

	@Inject @Default 
	private Instance<ATMTransport> defaultTransport;
	
	private ATMTransport transport;

	@PostConstruct
	protected void init() {
		if (!defaultTransport.isUnsatisfied()) {
			System.out.println("picked Default");
			transport = defaultTransport.iterator().next();
		} else if (!jsonTransport.isUnsatisfied()) {
			System.out.println("picked JSON");
			transport = jsonTransport.iterator().next();
		} else if (!soapTransport.isUnsatisfied()) {
			System.out.println("picked SOAP");
			transport = soapTransport.iterator().next();
		}
	}

```

Notice we are using **`Instance<ATMTransport>`** as the field type instead of **`ATMTransport`**.
Then we look up the actual transport. We can query a **`Instance`** with the **`Instance.isUnsatisfied`** to
see it this tranport actually exist. There is an **`Instance.get`** method to retrieve a single
transport, but I used **`Instance.iterator().next()`** to highlight an important aspect
of **`Instance`**, namely, it can return more the same type. There could be 20 @**`Default`** based
transports in the system.

Imagine if you were implementing a chain of responsibility pattern or a command pattern, and you
wanted an easy way to discover the actions or commands that were on the classpath.
**`Instance`** would be that way. CDI makes this type of plugin development very easy.


If it could find a single @**`Default`**, the one we have been using since the start, on the classpath.
The output from the above would be as follows:

Output
```
picked Default
deposit called
communicating with bank via Standard transport
```

Now to test how the **`Instance.isUnsatisfied`** by commenting out the **`implements ATMTransport`** in StandardAtmTransport
class definition. You are essntially taking StandardAtmTransport out of the pool of possible injection of **`ATMTransport`**.
There are no more defaults configured so it should be an unsatified.


### Code Listing: **`StandardAtmTransport`** commenting out **`implements ATMTransport`**  so **`Instance.isUnsatisfied`** returns true ###
```
package org.cdi.advocacy;

import javax.enterprise.inject.Default;

@Default
public class StandardAtmTransport { //implements ATMTransport {

	public void communicateWithBank(byte[] datapacket) {
		System.out.println("communicating with bank via Standard transport");
	}

}

```

Now the output is this:

```
picked JSON
deposit called
communicating with bank via JSON REST transport
```

Reread this section if you must and make sure you understand why you get the above output.


You can use Insstance to load more than one bean as mentioned earlier.
Let's lookup all installed installed @Default transports.
To setup this example remove all of the annotations in the ATMTransport interfaces
and make the beans.xml empty again (so no Alternative is active).



### Code Listing: **`SoapAtmTransport`** making it @**`Default`** by removing @**`Soap`** qualifier ###
```
package org.cdi.advocacy;

//import javax.enterprise.inject.Alternative;

//@Soap
public class SoapAtmTransport implements ATMTransport {

	public void communicateWithBank(byte[] datapacket) {
		System.out.println("communicating with bank via Soap transport");
	}

}
```

### Code Listing: **`JsonRestAtmTransport`** making it @**`Default`** by removing @**`Json`** qualifier ###
```
package org.cdi.advocacy;

//import javax.enterprise.inject.Alternative;

//@Alternative @Json
public class JsonRestAtmTransport implements ATMTransport {

	public void communicateWithBank(byte[] datapacket) {
		System.out.println("communicating with bank via JSON REST transport");
	}

}

```

### Code Listing: **`StandardAtmTransport`** making it @**`Default`** by removing any qualifiers from it ###
```
package org.cdi.advocacy;


//Just make sure there are no qualifiers
public class StandardAtmTransport implements ATMTransport {

	public void communicateWithBank(byte[] datapacket) {
		System.out.println("communicating with bank via Standard transport");
	}

}

```

We also need to make sure that the beans.xml file is empty.


### Code Listing: **`{classpath}/META-INF/beans.xml`** removing all alternatives ###

```
<beans xmlns="http://java.sun.com/xml/ns/javaee" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="
http://java.sun.com/xml/ns/javaee
http://java.sun.com/xml/ns/javaee/beans_1_0.xsd">
</beans>
```

Now use every transport that is installed using the annotation.

```
package org.cdi.advocacy;

import java.math.BigDecimal;
import java.util.Iterator;

import javax.annotation.PostConstruct;
import javax.enterprise.inject.Any;
import javax.enterprise.inject.Instance;
import javax.inject.Inject;
import javax.inject.Named;

@Named("atm")
public class AutomatedTellerMachineImpl implements AutomatedTellerMachine {
	
	@Inject 
	private Instance<ATMTransport> allTransports;

	@PostConstruct
	protected void init() {
		System.out.println("Is this ambigous? " + allTransports.isAmbiguous() );
		System.out.println("Is this unsatisfied? " + allTransports.isUnsatisfied() );
	}
	
	public void deposit(BigDecimal bd) {
		System.out.println("deposit called");
		
		for (ATMTransport transport : this.allTransports) {
			transport.communicateWithBank(null);
		}
		
	}

	public void withdraw(BigDecimal bd) {
		System.out.println("withdraw called");

		for (ATMTransport transport : this.allTransports) {
			transport.communicateWithBank(null);
		}

	}

}
```

In this context ambigous means more than one. Therefore, CDI found more than one possibility
for injection if ambigous returns true. It should find three defaults.

Your output should look like this (or something close to this).

Output
```
Is this ambigous? true
Is this unsatisfied? false
deposit called
communicating with bank via JSON REST transport
communicating with bank via Soap transport
communicating with bank via Standard transport
communicating with bank via the Super Fast transport
```

Note that we changed deposit to iterate through the available instances.

Now try something new comment out the **`implements ATMTransports`** in **`SuperFastAtmTransport`**, **`JsonRestAtmTransport`** and **`SoapRestAtmTransport`**.

**`JsonRestAtmTransport`** and **`SoapRestAtmTransport`** transport class defintion should have this **`//implements ATMTransport {`**.

Now rerun the example.


You get this output.

**Output**
```
Is this ambigous? false
Is this unsatisfied? false
deposit called
communicating with bank via Standard transport
```

Since the only transport left is the standard transport (**`StandardAtmTransport`**), only it is in the output.
The Instance is no longer ambigous, there is only one so it prints false.
CDI finds the one so it is not unsatisfied.

Now comment out all of //implements ATMTransport, and you get this:

```
Is this ambigous? false
Is this unsatisfied? true
deposit called
```

Notice there a no longer any  ATMTransport transport implementations in the system at all.

The @Any qualifier states that you want all instances of an implementation.
It does not matter what qualifiers they have, you want them all @**`Json`**s, @**`Soap`**s, @**`SuperFast`**s, whatever.

Add the all of the annotations we commented out back to all of the transports.



Add the @Any to the transport injection as follows:


### Code Listing: **`AutomatedTellerMachineImpl`** @**`Inject`** @**`Any`** **`Instance<ATMTransport>`** to inject all transport instances ###
```
...
import javax.enterprise.inject.Any;
...
public class AutomatedTellerMachineImpl implements AutomatedTellerMachine {
	
	@Inject @Any 
	private Instance<ATMTransport> allTransports;
	
	private ATMTransport transport;

       ...
}

```

The output of this should be:

Output
```
Is this ambigous? true
Is this unsatisfied? false
deposit called
communicating with bank via JSON REST transport
communicating with bank via Soap transport
communicating with bank via Standard transport
communicating with bank via the Super Fast transport
```

@Any finds all of the transports in the system.

Once you inject the instances into the system, you can use the **`select`** method of **`instance`** to query for a particular type.

Here is an example of that:

### Code Listing: **`AutomatedTellerMachineImpl`** using selects to find a particular transport from the list you loaded ###
```
...
import javax.enterprise.inject.Any;
...
public class AutomatedTellerMachineImpl implements AutomatedTellerMachine {
	
	@Inject @Any 
	private Instance<ATMTransport> allTransports;
	
	private ATMTransport transport;

	@PostConstruct
	protected void init() {
		transport = allTransports.select(new AnnotationLiteral<Default>(){}).get();
		
		if (transport!=null) {
			System.out.println("Found standard transport");
			return;
		}
		
		transport = allTransports.select(new AnnotationLiteral<Json>(){}).get();

		
		if (transport!=null) {
			System.out.println("Found JSON standard transport");
			return;
		}

		
		transport = allTransports.select(new AnnotationLiteral<Soap>(){}).get();
		
		
		if (transport!=null) {
			System.out.println("Found SOAP standard transport");
			return;
		}
		
	}
	

	public void deposit(BigDecimal bd) {
		System.out.println("deposit called");
		
		transport.communicateWithBank(...);
	}

       ...
}

```

Here is the expected format.

Output
```
Found standard transport
deposit called
communicating with bank via Standard transport
```


Now imagine there being a set of settings that are configured in a db or something
and the code might look like this to find a transport (this should look familiar to you by now).

### Code Listing: **`AutomatedTellerMachineImpl`** using selects and some business logic to decide which transport to use ###
```
package org.cdi.advocacy;

import java.math.BigDecimal;

import javax.annotation.PostConstruct;
import javax.enterprise.inject.Any;
import javax.enterprise.inject.Default;
import javax.enterprise.inject.Instance;
import javax.enterprise.util.AnnotationLiteral;
import javax.inject.Inject;
import javax.inject.Named;

@Named("atm")
public class AutomatedTellerMachineImpl implements AutomatedTellerMachine {
	
	@Inject @Any 
	private Instance<ATMTransport> allTransports;
	
	private ATMTransport transport;
	
	//These could be looked up in a DB, JNDI or a properties file.
	private boolean useJSON = true;
	private boolean behindFireWall = true;

	@PostConstruct
	protected void init() {
		
		ATMTransport soapTransport, jsonTransport, standardTransport;
		
		standardTransport = allTransports.select(new AnnotationLiteral<Default>(){}).get();
		jsonTransport = allTransports.select(new AnnotationLiteral<Json>(){}).get();
		soapTransport = allTransports.select(new AnnotationLiteral<Soap>(){}).get();

		if (!behindFireWall) {
			transport = standardTransport;
		} else {
			if (useJSON) {
				transport = jsonTransport;
			} else {
				transport = soapTransport;
			}
		}		
		
	}
	

	public void deposit(BigDecimal bd) {
		System.out.println("deposit called");
		
		transport.communicateWithBank(...);
	}

	public void withdraw(BigDecimal bd) {
		System.out.println("withdraw called");

		transport.communicateWithBank(...);

	}

}

```

Exercise:
Please combine the use of Instance with a producer to define the same type of lookup
but have the business logic and select lookup happen in the **`TrasportFactory`**.
Send me your answers on the [CDI group mailing list](http://groups.google.com/group/cdiadvocate4j?pli=1).
The first one to send gets put on the CDI wall of fame. (All others get honorable mentions.)


## The dirty truth about CDI and Java SE ##

The dirty truth is this. CDI is part of JEE 6. It could easily be used outside of
a JEE 6 container as these examples show. The problem is that there is no
standard interface to use CDI outside of a JEE 6 container so the three main implementations
Caucho Resin Candi, Red Hat JBoss Weld and Apache OpenWebBeans all have their own way
to run a CDI container standalone.

As part of the promotion and advocacy of CDI, we plan on comming up with a standard way to
run CDI standalone. It will be a small wrapper around CDI standalone containers.
It will work with Resin, Weld and eventually OpenWebBeans.


# Conclusion #

Dependency Injection (DI) refers to the process of supplying an external dependency
to a software component.


[CDI](http://jcp.org/aboutJava/communityprocess/final/jsr299/index.html) is the
Java standard for dependency injection and interception (AOP).
It is evident from the popularity of DI and AOP that Java needs to address DI
and AOP so that it can build other standards on top of it.
DI and AOP are the foundation of many Java frameworks.
I hope you share my vision of CDI as a basis for other JSRs, Java frameworks and standards.


This article discussed CDI dependency injection in a tutorial format.
It covers some of the features of CDI such as type safe annotations configuration,
alternatives and more. There was an introduction level and and advacned level.

CDI is a foundational aspect of Java EE 6. It is or will be shortly supported by
Caucho's Resin, IBM's WebSphere, Oracle's Glassfish, Red Hat's JBoss and many
more application servers. CDI is similar to core Spring and Guice frameworks.
However CDI is a general purpose framework that can be used outside of JEE 6.


CDI simplifies and sanitizes the API for DI and AOP. Through its use of **`Instance`**  and @Produces,
CDI provides a pluggable architecture.

With this pluggable architecture you can write code that finds new dependencies
dynamically.


CDI is a rethink on how to do dependency injection and AOP (interception really).
It simplifies it. It reduces it. It gets rid of legacy, outdated ideas.

CDI is to Spring and Guice what JPA is to Hibernate, and Toplink. CDI will co-exist with Spring and Guice.
There are plugins to make them interoperate nicely. There is more integration option
on the way.

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
> This article was written with CDI advocacy in mind by [Rick Hightower](https://profiles.google.com/RichardHightower/about)
> with some collaboration from others.

> Rick Hightower has worked as a CTO, Director of Development and a Developer for the last 20 years.
> He has been involved with J2EE since its inception. He worked at an EJB container company in 1999.
> He has been working with Java since 1996, and writing code professionally since 1990.
> Rick was an early [Spring enthusiast](http://java.sys-con.com/node/47735).
> Rick enjoys bouncing back and forth between C, Python, Groovy and Java development.
> Although not a fan of [EJB 3](http://java.sys-con.com/node/216307),
> Rick is a big fan of the potential of CDI and
> thinks that EJB 3.1 has come a lot closer to the mark.
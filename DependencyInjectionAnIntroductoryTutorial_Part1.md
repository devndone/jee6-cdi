<h1> Dependency Injection - An Introductory Tutorial - Part 1 </h1>

# Introduction #


<p>
<a href='http://jcp.org/aboutJava/communityprocess/final/jsr299/index.html'>CDI</a> is the<br>
Java standard for dependency injection (DI) and interception (AOP). It is evident<br>
from the popularity of DI and AOP that Java needs to address DI and AOP so that<br>
it can build other standards and JSRs on top of it. DI and AOP are the foundation of many<br>
Java frameworks, and CDI will be the foundation of many future<br>
specifications and JSRs.<br>
</p>


<p>This article discusses dependency injection in a tutorial format. It covers some<br>
of the features of CDI such as type safe annotations configuration,<br>
alternatives and more.<br>
This tutorial is split into two parts, the first part covers the basis<br>
of dependency injection, @Inject, @Produces and @Qualifiers.<br>
The next part in this series covers advanced topics like creating<br>
pluggable components with Instance and processing annotations for configuration.<br>
</p>

<p>
CDI is a foundational aspect of Java EE 6. It is or will be shortly supported by<br>
<a href='http://www.caucho.com/resin/'>Caucho's Resin</a>,<br>
IBM's WebSphere,<br>
<a href='http://glassfish.java.net/'>Oracle's Glassfish</a>,<br>
<a href='http://www.jboss.org/jbossas/docs/6-x.html'>Red Hat's JBoss</a> and many more application servers.<br>
CDI is similar to core Spring and Guice frameworks. <br>
<br>
<bold><br>
<br>
Like JPA did for ORM, CDI<br>
simplifies and sanitizes the API for DI and AOP<br>
<br>
</bold><br>
<br>
. If you have worked with Spring<br>
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

<p>This tutorial series is meant to be a description and explanation of DI in CDI<br>
without the clutter of EJB 3.1 or JSF. There are already plenty of<br>
tutorials that cover EJB 3.1 and JSF with CDI as a supporting actor.<br>
</p>

<p>
CDI has merit on its own outside of the EJB and JSF space. This<br>
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
Again, the code listings are in the<br>
<a href='DependencyInjectionAnIntroductoryTutorial_Part1.md'>TOC on the wiki page</a>
so you can find just the code listing you are looking for quickly like<br>
an index for a cookbook.<br>
</p>


<p>Decorators, Extentions, Interceptors, Scopes are out of scope for<br>
this first tutorial.<br>
Expect them in future tutorials.<br>
</p>

<p>
If this tutorial is well recieved and we get enough feedback through,<br>
the JavaLobby articles, our google group<br>
and comments section of the wiki then we will add a comprehensive tutorial on<br>
CDI AOP (Decorators and Interceptors) and one on Extentions.<br>
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
Notice the possible implementations of the <b><code>ATMTransport</code></b> interface.<br>
The <b><code>AutomatedTellerMachineImpl</code></b> does not know or care which transport it uses.<br>
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
</li><li>Use the CDI <b><code>beanContainer</code></b> to look up the <b>atm</b>, makes some deposits and withdraws.<br>
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
By default, CDI would look for a class that implements the <b><code>ATMTransport</code></b> interface, once it finds this it creates an instance and injects this instance of <b><code>ATMTransport</code></b> using the setter method <b><code>setTransport</code></b>. If we only had one possible instance of <b><code>ATMTransport</code></b> in our classpath, we would not need to annotate any of the <b><code>ATMTransport</code></b> implementations. Since we have three, namely, <b><code>StandardAtmTransport</code></b>, <b><code>SoapAtmTransport</code></b>,  and <b><code>JsonAtmTransport</code></b>, we need to mark two of them as <b><code>@Alternative</code></b>'s and one as <b><code>@Default</code></b>.<br>
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
If we don't mark the others as <b><code>@Alternative</code></b>, they are by default as far as CDI is concerned, marked as <b><code>@Default</code></b>.  Let's mark <b><code>JsonRestAtmTransport</code></b> and <b><code>SoapRestAtmTransport</code></b> <b>@Alternative</b> so CDI does not get confused.<br>
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
let's just use the <b><code>beanContainer</code></b> to look it up. Let's give it an easy logical name like "atm".<br>
To give it a name, use the <b><code>@Named</code></b> annotation. The <b><code>@Named</code></b> annotation is<br>
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
It should be noted that if you use the <b><code>@Named</code></b> annotations and don't provide a name, then the name<br>
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

### Code Listing: **`AutomatedTellerMachineImpl.transport`** using @Inject to do field injection. ###

```
...
public class AutomatedTellerMachineImpl implements AutomatedTellerMachine {
	
    @Inject
    private ATMTransport transport;

```


### Code Listing:  **`AutomatedTellerMachineImpl.transport`** using **`@Inject`** to do constructor injection. ###

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
Instead of relying on a constructor, you can delegate to a factory class to<br>
create the instance. To do this with CDI, you would use the @Produces from<br>
your factory class as follows:<br>
</p>

### Code Listing: **`TransportFactory.createTransport`** using @Produces to define a factory method ###

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
It is self documenting. If someone knows CDI and they know about Alternatives they will not be surprised.<br>
Alternatives really canonicalizes the way you select an Alternative.<br>
</p>

<p>
You can think of CDI as a canonicalization of many patterns that we have been using with more general purpose DI frameworks.<br>
The simplification and canonicalization is part of the evolution of DI.<br>
</p>

## Code Listing: Using @Qualifier to inject different types ##

<p>
All objects and producers in CDI have qualifiers. If you do not assign a qualifier<br>
it by default has the qualifier <b><code>@Default</code></b> and <b><code>@Any</code></b>. It is like a TV crime show<br>
in the U.S., if you do not have money for a lawyer, you will be assigned one.<br>
</p>

<p>
Qualifiers can be used to discriminate exactly what gets injected.<br>
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
Notice that a qualifier is just a runtime annotation that is marked with the <b><code>@Qualifier</code></b> annotation.<br>
The <b><code>@Qualifier</code></b> is an annotation that decorates a runtime annoation to make it a qualifier.<br>
</p>

<p>
Then we would just mark the source of the injection point, namely, <b><code>SoapAtmTransport</code></b> with our new <b><code>@Soap</code></b> qualifier as follows:<br>
</p>

### Code Listing: **`SoapAtmTransport`** using new **`@Soap`** qualifier ###
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

### Code Listing: **`AutomatedTellerMachineImpl`** injecting **`SoapAtmTransport`** using new **`@Soap`** qualifier via constructor arg ###
```
public class AutomatedTellerMachineImpl implements AutomatedTellerMachine {
	
    private ATMTransport transport;

    @Inject 
    public AutomatedTellerMachineImpl(@Soap ATMTransport transport) {
        this.transport = transport;
    }

```

You could also choose to do this via the setter method for the property as follows:

### Code Listing: **`AutomatedTellerMachineImpl`** injecting **`SoapAtmTransport`** using new **`@Soap`** qualifier via setter method arg ###

```
public class AutomatedTellerMachineImpl implements AutomatedTellerMachine {
	
    private ATMTransport transport;

    @Inject 
    public void setTransport(@Soap ATMTransport transport) {
        this.transport = transport;
    }
```

And a very common option is to use a field level injection as follows:

### Code Listing: **`AutomatedTellerMachineImpl`** injecting **`SoapAtmTransport`** using new **`@Soap`** qualifier via setter method arg ###
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
is separate from the actual <b><code>AutomatedTellerMachineImpl</code></b> code.<br>
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
<b><code>createTransport</code></b> is by default <b><code>@Default</code></b> and @<b><code>Any</code></b> but it overrides the <b><code>StandardAtmTransport</code></b>
which is also by default @<b><code>Default</code></b> and <b><code>@Any</code></b>, but since <b><code>StandardAtmTransport</code></b> is overidden<br>
then if I inject <b><code>@Default</code></b> <b><code>ATMTransport</code></b> <b><code>standardTransport</code></b> as an argument then<br>
it tries to call <b><code>createTransport</code></b> since it is the <b><code>@Default</code></b>, which will then try to inject<br>
the argument <b><code>standardTransport</code></b>, which will then call <b><code>createTransport</code></b>, ad infinitum until<br>
we get a <b><code>StackTraceOverflow</code></b>. The solution is create a qualifier for the standard, say,<br>
@<b><code>Standard</code></b> and use that to do the injection, or create one for the <b><code>createProduces</code></b> production, say,<br>
<b><code>@Transport</code></b>. The key here is that the injection arguments of a producer have to have different qualifiers than the<br>
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

### Code Listing: **`AutomatedTellerMachineImpl`** using **`@Inject`** **`@Transport(type=TransportType.STANDARD)`** ###
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



# Conclusion #

<p>
Dependency Injection (DI) refers to the process of supplying an external dependency<br>
to a software component.<br>
</p>

<p>
<a href='http://jcp.org/aboutJava/communityprocess/final/jsr299/index.html'>CDI</a> is the<br>
Java standard for dependency injection and interception (AOP).<br>
It is evident from the popularity of DI and AOP that Java needs to address DI<br>
and AOP so that it can build other standards on top of it.<br>
DI and AOP are the foundation of many Java frameworks.<br>
I hope you share my vision of CDI as a basis for other JSRs, Java frameworks and standards.<br>
</p>

<p>
This article discussed CDI dependency injection in a tutorial format.<br>
It covers some of the features of CDI such as type safe annotations configuration,<br>
alternatives and more. There was an introduction level and and advacned level.<br>
</p>

<p>
CDI is a foundational aspect of Java EE 6. It is or will be shortly supported by<br>
Caucho's Resin, IBM's WebSphere, Oracle's Glassfish, Red Hat's JBoss and many<br>
more application servers. CDI is similar to core Spring and Guice frameworks.<br>
However CDI is a general purpose framework that can be used outside of JEE 6.<br>
</p>

<p>
CDI is a rethink on how to do dependency injection and AOP (interception really).<br>
It simplifies it. It reduces it. It gets rid of legacy, outdated ideas.<br>
</p>

<p>
CDI is to Spring and Guice what JPA is to Hibernate, and Toplink. CDI will co-exist with Spring and Guice.<br>
There are plugins to make them interoperate nicely. There is more integration option<br>
on the way.<br>
</p>

This is just a brief taste. There is more to come.


# Resources #
  * [Part 2 plugins and annotation processing](http://java.dzone.com/articles/cdi-di-p2)
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

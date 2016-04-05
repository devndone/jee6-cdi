<h1> CDI Dependency Injection - Tutorial -- Part 2 -- Advanced CDI DI </h1>




# Introduction #

<p>
CDI provides a pluggable architecture allowing you to easily process your own annotations.<br>
Read this article to understand the inner workings of CDI and why this JSR is so important.<br>
</p>

<p>
CDI simplifies and sanitizes the API for DI and AOP like JPA did for ORMs.<br>
Through its use of <b><code>Instance</code></b>  and @<b><code>Produces</code></b>,<br>
CDI provides a pluggable architecture. This is a jaw dropping killer feature of CDI.<br>
Master this and you start to tap into the power of CDI. The last<br>
<a href='http://java.dzone.com/articles/cdi-di-p1'>article</a> was just<br>
to lay the ground work to the uninitiated for this article.<br>
</p>



<p>
This article continues our <a href='http://java.dzone.com/articles/cdi-di-p1'>tutorial of dependency injection with CDI</a>.<br>
</p>

<p>
This article covers:<br>
</p>

  * How to process annotations for configuration (injection level and class level)
  * How to use an annotation for both injection and configuration (@**`Nonbinding`**)
  * Using **`Instance`** to manage instances of possible injection targets
  * CDI's plugin architecture for the masses


<p>
With this pluggable architecture you can write code that finds new dependencies<br>
dynamically. CDI can be a framework to write frameworks. This is why it is so<br>
important that CDI was led through the JSR process.<br>
</p>

<p>
Just like last time, there are some instructions on how to run the examples:<br>
<a href='https://jee6-cdi.googlecode.com/svn/tutorial/cdi-di-example'>Source code for this tutorial</a>,<br>
and <a href='MavenDITutorialInstructions.md'>instructions</a> for use. A programming article<br>
without working sample code is like a sandwich with no condiments<br>
or dry toast without jelly.<br>
</p>





# Advanced CDI tutorial #
<p>
The faint of heart stop here. All of the folks who want to understand the inner<br>
workings of CDI continue. So far, we have been at the shallow, warm end of the<br>
pool. Things are about to get a little deeper and colder.<br>
If you need to master CDI, then this article if for you. If you don't know what CDI<br>
is then read the <a href='http://java.dzone.com/articles/cdi-di-p1'>first CDI DI article</a>.<br>
</p>

## Advanced: Using @Produces and **`InjectionPoint`** to create configuration annotations ##

<p>
Our ultimate goal is to define an annotation that we can use to configure the retry count on a transport.<br>
Essentially, we want to pass a retry count to the transport.<br>
</p>

We want something that looks like this:

### Code Listing: **`TransportConfig`** annotations that does configuration ###
```
	@Inject @TransportConfig(retries=2)
	private ATMTransport transport;

```

(This was my favorite section to write, because I wanted to know how to create a
annotation configuration from the start.)

<p>
Before we do that we need to learn more about @<b><code>Produces</code></b> and <b><code>InjectionPoint</code></b>s.<br>
We are going to use a producer to read information (meta-data) about an injection point.<br>
A major inflection point for learning how to deal with annotations is the<br>
<b><code>InjectionPoint</code></b>s. The <b><code>InjectionPoint</code></b>s has all the metadata we need to process<br>
configuration annotations.<br>
</p>

<p>
An <a href='http://download.oracle.com/javaee/6/api/javax/enterprise/inject/spi/InjectionPoint.html'>*`InjectionPoint`*</a>
is a class that has information about an injection point. You can learn things<br>
like what is being decorated, what the target injection type is, what the source injection type,<br>
what is the class of the owner of the member that is being injected and so forth.<br>
</p>

<p>
Let's learn about passing an injection point to @<b><code>Produces</code></b>. Below I have rewritten our simple @<b><code>Produces</code></b>
example from the previous<br>
<a href='http://java.dzone.com/articles/cdi-di-p1'>article</a>,<br>
except this time I pass an <b><code>InjectionPoint</code></b> argument into the mix.<br>
</p>


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
```


Now we just run it and see what it produces.

The above produces this output.

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

<p>
It appears from the output that <b><code>annotated</code></b> tells us about the area of<br>
the program we annotated. It also appears that <b><code>bean</code></b> tells us which bean<br>
the injection is happening on.<br>
</p>


<p>
From this output you can see that the <b><code>annotated</code></b> property on the <b><code>injectionPoint</code></b>
has information about which language feature (field, constructor argument, method argument, etc.).<br>
In our case it is the field <b><code>org.cdi.advocacy.AutomatedTellerMachineImpl.transport</code></b>.<br>
is being used as the target of the injection, it is the thing that was <b><code>annotated</code></b>.<br>
</p>

<p>
From this output you can see that the <b><code>bean</code></b> property of the <b><code>injectionPoint</code></b>
is being used to describe the bean whose member is getting injected. In this case,<br>
it is the <b><code>AutomatedTellerMachineImpl</code></b> whose is getting the field injected.<br>
</p>

<p>
I won't describe each property, but as an exercise you can.<br>
</p>

<p>
Exercise: Look up the <b><code>InjectionPoint</code></b> in the<br>
<a href='http://download.oracle.com/javaee/6/api/javax/enterprise/inject/spi/InjectionPoint.html'>API documentation</a>.<br>
Find out what the other properties mean. How might you use this meta-data?<br>
Can you think of a use case or application where it might be useful?<br>
Send me your answers on the <a href='http://groups.google.com/group/cdiadvocate4j?pli=1'>CDI group mailing list</a>.<br>
The first one to send gets put on the CDI wall of fame. (All others get honorable mentions.)<br>
</p>

<p>
Drilling further you can see what is in the beans and annotated properties.<br>
</p>

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

<p>
Now we are cooking with oil. Throw some gas on that flame. Look at the wealth of information<br>
that the <b><code>InjectionPoint</code></b> defines.<br>
</p>

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

<p>
We see that <b><code>bean.beanClass</code></b> gives up the class of the bean that is getting the<br>
injected field. Remember that one, we will use it later.<br>
</p>

<p>
We can see that <b><code>bean.qualifiers</code></b> gives up the list of qualifiers for the <b><code>AutomatedTellerMachineImpl</code></b>.<br>
</p>

<p>
We can also see that <b><code>annotated.annotations</code></b> gives us the list of annotations that are associated with the injected field.<br>
We will use this later to pull the configuration annotation and configure the transport with it.<br>
</p>

<p>
Exercise: Look up the <b><code>Bean</code></b> and <b><code>Annotated</code></b> in the<br>
<a href='http://download.oracle.com/javaee/6/api/index.html?javax/enterprise/inject/spi/package-summary.html'>API documentation</a>.<br>
Find out what the other properties mean. How might you use this meta-data?<br>
Can you think of a use case or application where it might be useful?<br>
Send me your answers on the <a href='http://groups.google.com/group/cdiadvocate4j?pli=1'>CDI group mailing list</a>.<br>
The first one to send gets put on the CDI wall of fame. (All others get honorable mentions.)<br>
</p>

<p>
Ok now that we armed with an idea of what an <b><code>Injection</code></b> point is. Let's get configuring our transport.<br>
</p>

<p>
First let's define an <b><code>TransportConfig</code></b> annotation. This is just a plain runtime annotation as follows:<br>
</p>


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

<p>
Notice that this annotation has one member retries, which we will use to configure<br>
the <b><code>ATMTransport</code></b> (<b><code>transport</code></b>).<br>
</p>

<p>
Now go ahead and use this to decorate the injection point as follows:<br>
</p>

### Code Listing: **`AutomatedTellerMachineImpl`** using **`TransportConfig`** to configure retries ###
```
public class AutomatedTellerMachineImpl implements AutomatedTellerMachine {
	
    @Inject @TransportConfig(retries=2)
    private ATMTransport transport;

```

<p>
Once it is configured when you run it, you will see the following output from our producer:<br>
</p>

Output
```
annotated.annotations AnnotationSet[@javax.inject.Inject(), @org.cdi.advocacy.TransportConfig(retries=2)]
```

<p>
This means the annotation data is there. We just need to grab it and use it. Stop and ponder on this a bit.<br>
This is pretty cool. The producer allows me to customize how annotations are consumed.<br>
This is powerful stuff and one of the many extension points available to CDI.<br>
CDI was meant to be extensible. It is the first mainstream framework that encourages you to<br>
consume your own annotation data. This not some obscure framework feature.<br>
This is in the main usage.<br>
</p>

<p>
Please recall that the <b><code>injectionPoint.annotated.annotations</code></b> gives us the<br>
list of annotations that are associated with the injected field, namely, the transport field of the<br>
<b><code>AutomatedTellerMachineImpl</code></b>. Now we can use this to pull the configuration annotation<br>
and configure the transport with it. The party is rolling now.<br>
</p>


<p>
Now we need to change the transport implementations to handle setting retires.<br>
Since this is an example, I will do this simply<br>
by adding a new setter method for retires (<b><code>setRetries</code></b>) to the <b><code>ATMTranport</code></b>
interface like so:<br>
</p>

### Code Listing: **`ATMTransport`** adding a retries property ###
```
package org.cdi.advocacy;

public interface ATMTransport {
    public void communicateWithBank(byte[] datapacket);
    public void setRetries(int retries);
}

```

<p>
Then we need to change each of the transports to handle this new <b><code>retries</code></b>
property as follows:<br>
</p>

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

<p>
Now we just change the producer to grab the new annotation and configure the transport as follows:<br>
<br>
(For clarity I took out all of the Sysout.prinltns.)<br>
</p>


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

<p>
(Side Note: we are missing a null pointer check. The annotation configuration could<br>
be null if the user did not set it, you may want to handle this.<br>
The example is kept deliberately short.)<br>
</p>

<p>
The code just gets the annotation and shoves in the retires into the transport, and then just returns the transport.<br>
</p>

<p>
We now have a producers that can use an annotation to configure an injection.<br>
</p>

<p>
Here is our new output:<br>
</p>

**Output**
```
...
deposit called
communicating with bank via Standard transport retries=2
```

<p>
You can see our retries are there as we configured them in the annotation.<br>
Wonderful! Annotation processing for the masses!<br>
</p>


<p>
Ok we are done with this example. What remains is a victory lap.<br>
Let's say we had multiple transports in a single ATM and you wanted to configure<br>
all of the outputs at once.<br>
</p>

<p>
Let's configure the transport<br>
based on an annotation in the parent class of the injection target, namely, <b><code>AutomatedTellerMachine</code></b>.<br>
</p>

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

<p>
It is an exercise for the reader to make the injection level annotation<br>
(from the last example) override the class level annotations.<br>
As always, if you are playing along in the home version of CDI hacker, send me<br>
your solution. Best solution gets my admiration.<br>
</p>


Output
```
deposit called
communicating with bank via Standard transport retries=7
```

<p>
Exercise: Make the injection from the field override the injection from the class.<br>
It is a mere matter of Java code.<br>
Send me your solution on the <a href='http://groups.google.com/group/cdiadvocate4j?pli=1'>CDI group mailing list</a>.<br>
The first one to send gets put on the CDI wall of fame. (All others get honorable mentions.)<br>
</p>

## Advanced Using @Nonbinding to combine a configuration annotation and a qualifier annotation into one annotation ##

<p>
In the section titled <b>"Using @Qualfiers with members to discriminate injection and stop the explosion of annotation creation"</b>
we covered adding additional members to a qualifier annotation and<br>
then in <b>"Advanced: Using @Produces and InjectionPoint to create configuration annotations"</b>
we talked about how to write an annotation to configure an injection.<br>
Wouldn't be great if we could combine these two concepts into one annotation?<br>
</p>

<p>
The problem is that qualifier members are used to do the discrimination.<br>
We need some qualifier members that are not used for configuration not discrimination.<br>
</p>

<p>
To make an qualifier member just a configuration member use @<b><code>Nonbinding</code></b> annotation as follows:<br>
</p>

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

Now let's add the **`setRetries`** to the Fast Transport:

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

<p>
The final result is we have one annotation that does both qualification and configuration.<br>
Booyah!<br>
</p>

<p>
Exercise:<br>
There is an easter egg in this example. There is concept we talked about earlier<br>
(in the <a href='http://java.dzone.com/articles/cdi-di-p1'>last article</a>) in the<br>
qualifier discrimination but never added. Please find it and describe it.<br>
What are some potential problems of using this approach?<br>
Send me your answers on the <a href='http://groups.google.com/group/cdiadvocate4j?pli=1'>CDI group mailing list</a>.<br>
The first one to send gets put on the CDI wall of fame. (All others get honorable mentions.)<br>
</p>


## Advanced: Using Instance to inject transports ##
<p>
The use of the class <b><code>Instance</code></b> allows you to dynamically look up instances<br>
of a certain type. This is the plugin architecture for the masses, built right into<br>
CDI. Grok this and you will not only understand CDI but have a powerful weapon in<br>
your arsenal of mass programming productivity.<br>
</p>

<p>
These instances can be instances that are in a jar files.<br>
For example the <b><code>AutomatedTellerMachine</code></b> could work with transports<br>
that did not even exist when the <b><code>AutomatedTellerMachine</code></b> was created.<br>
If you don't grok that, read the last sentence again. You are tapping into the<br>
scanning capabilities of CDI. This power is there for the taking.<br>
The <b><code>Instance</code></b> class is one of the things that makes CDI so cool and flexible.<br>
In this section, I hope to give it some justice while still keeping the example small<br>
and understandable.<br>
</p>

<p>
Let's say we wanted to work with multiple transports.<br>
But we don't know which transport is configured and on the classpath.<br>
It could be that the build was special for a certain type of transport, and it<br>
just does not exist on the classpath. Suspend disbelief for a moment and let's look<br>
at the code.<br>
</p>

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

<p>
Notice we are using <b><code>Instance&lt;ATMTransport&gt;</code></b> as the field type instead of <b><code>ATMTransport</code></b>.<br>
Then we look up the actual transport. We can query a <b><code>Instance</code></b> with the <b><code>Instance.isUnsatisfied</code></b> to<br>
see it this transport actually exist. There is an <b><code>Instance.get</code></b> method to retrieve a single<br>
transport, but I used <b><code>Instance.iterator().next()</code></b> to highlight an important aspect<br>
of <b><code>Instance</code></b>, namely, it can return more than one. For example, there could be 20 @<b><code>Default</code></b> based<br>
transports in the system.<br>
</p>

<p>
Imagine if you were implementing a chain of responsibility pattern or a command pattern, and you<br>
wanted an easy way to discover the actions or commands that were on the classpath.<br>
<b><code>Instance</code></b> would be that way. CDI makes this type of plugin development very easy.<br>
</p>

<p>
If it could find a single @<b><code>Default</code></b>, the one we have been using since the start, on the classpath.<br>
The output from the above would be as follows:<br>
</p>

Output
```
picked Default
deposit called
communicating with bank via Standard transport
```

<p>
Now to test how the <b><code>Instance.isUnsatisfied</code></b> by commenting out the <b><code>implements ATMTransport</code></b> in StandardAtmTransport<br>
class definition. You are essentially taking <b><code>StandardAtmTransport</code></b> out of the pool of possible injection of <b><code>ATMTransport</code></b>.<br>
There are no more defaults configured so it should be an unsatisfied.<br>
</p>


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

<p>
Reread this section if you must and make sure you understand why you get the above output.<br>
</p>


<p>
You can use <b><code>Instance</code></b> to load more than one bean as mentioned earlier.<br>
Let's lookup all installed installed @<b><code>Default</code></b> transports.<br>
To setup this example remove all of the annotations in the <b><code>ATMTransport</code></b> interfaces<br>
and make the beans.xml empty again (so no <b><code>Alternative</code></b> is active).<br>
</p>


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

We also need to make sure that the **`beans.xml`** file is empty.


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
        System.out.println("Is this ambiguous? " + allTransports.isAmbiguous() );
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

<p>
In this context ambiguous means more than one. Therefore, CDI found more than one possibility<br>
for injection if ambiguous returns true. It should find three defaults.<br>
</p>

<p>
Your output should look like this (or something close to this).<br>
</p>

Output
```
Is this ambiguous? true
Is this unsatisfied? false
deposit called
communicating with bank via JSON REST transport
communicating with bank via Soap transport
communicating with bank via Standard transport
communicating with bank via the Super Fast transport
```

<p>
Note that we changed deposit to iterate through the available instances.<br>
</p>

<p>
Now try something new comment out the <b><code>implements ATMTransports</code></b> in <b><code>SuperFastAtmTransport</code></b>, <b><code>JsonRestAtmTransport</code></b> and <b><code>SoapRestAtmTransport</code></b>.<br>
<b><code>JsonRestAtmTransport</code></b> and <b><code>SoapRestAtmTransport</code></b> transport class definition should have this <b><code>//implements ATMTransport {</code></b>.<br>
</p>

<p>
Now rerun the example.<br>
You get this output.<br>
</p>


**Output**
```
Is this ambiguous? false
Is this unsatisfied? false
deposit called
communicating with bank via Standard transport
```

<p>
Since the only transport left is the standard transport (<b><code>StandardAtmTransport</code></b>), only it is in the output.<br>
The <b><code>Instance</code></b> is no longer ambiguous, there is only one so it prints false.<br>
CDI finds the one so it is not unsatisfied.<br>
</p>

Now comment out all of //implements ATMTransport, and you get this:

```
Is this ambiguous? false
Is this unsatisfied? true
deposit called
```

<p>
Notice there a no longer any  ATMTransport transport implementations in the system at all.<br>
</p>

<p>
The @<b><code>Any</code></b> qualifier states that you want all instances of an implementation.<br>
It does not matter what qualifiers they have, you want them all @<b><code>Json</code></b>s, @<b><code>Soap</code></b>s, @<b><code>SuperFast</code></b>s, whatever.<br>
</p>

<p>
Add the all of the annotations we commented out back to all of the transports.<br>
<br>
Add the @<b><code>Any</code></b> to the transport injection as follows:<br>
<br>
</p>



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

<p>
@Any finds all of the transports in the system.<br>
Once you inject the instances into the system, you can use the <b><code>select</code></b> method of <b><code>instance</code></b> to query for a particular type.<br>
Here is an example of that:<br>
</p>

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

<p>
Now imagine there being a set of settings that are configured in a db or something<br>
and the code might look like this to find a transport (this should look familiar to you by now).<br>
</p>

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

    private boolean useJSON = true;
    private boolean behindFireWall = true;

    @SuppressWarnings("serial")
    @PostConstruct
    protected void init() {

        ATMTransport soapTransport, jsonTransport, standardTransport;
        standardTransport = allTransports.select(new AnnotationLiteral<Soap>() {}).get();
        jsonTransport = allTransports.select(new AnnotationLiteral<Json>() {}).get();
        soapTransport = allTransports.select(new AnnotationLiteral<Default>() {}).get();

        System.out.println(standardTransport.getClass().getName());
        System.out.println(jsonTransport.getClass().getName());
        System.out.println(soapTransport.getClass().getName());

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
        System.out.println("withdraw called");
        transport.communicateWithBank(null);

    }

    public void withdraw(BigDecimal bd) {
        System.out.println("withdraw called");

        transport.communicateWithBank(null);

    }

}
```

<p>
Exercise:<br>
Please combine the use of Instance with a producer to define the same type of lookup<br>
but have the business logic and select lookup happen in the <b><code>TrasportFactory</code></b>.<br>
Send me your answers on the <a href='http://groups.google.com/group/cdiadvocate4j?pli=1'>CDI group mailing list</a>.<br>
The first one to send gets put on the CDI wall of fame. (All others get honorable mentions.)<br>
</p>

## The dirty truth about CDI and Java SE ##

<p>
The dirty truth is this. CDI is part of JEE 6. It could easily be used outside of<br>
a JEE 6 container as these examples show. The problem is that there is no<br>
standard interface to use CDI outside of a JEE 6 container so the three main implementations<br>
<a href='http://www.caucho.com/resin/candi/'>Caucho Resin Candi</a>,<br>
<a href='http://seamframework.org/Weld'>Red Hat JBoss Weld</a> and<br>
<a href='http://openwebbeans.apache.org/owb/index.html'>Apache OpenWebBeans</a> all have their own way<br>
to run a CDI container standalone.<br>
</p>

<p>
As part of the promotion and advocacy of CDI, we (Andy Gibson, Rob Williams,<br>
and others) came up with a standard way to run CDI standalone. It is a small<br>
wrapper around CDI standalone containers.<br>
It works with <a href='http://www.caucho.com/resin/candi/'>Resin Candi</a>,<br>
<a href='http://seamframework.org/Weld'>Weld</a> and  <a href='http://openwebbeans.apache.org/owb/index.html'>OpenWebBeans</a>.<br>
If you used the examples, in the [<a href='http://java.dzone.com/articles/cdi-di-p1'>http://java.dzone.com/articles/cdi-di-p1</a> last<br>
CDI DI article] or this article<br>
then you used the first artifact that the CDISource organization put together.<br>
We plan on coming up with ways to unit test JPA outside of the container, and a few<br>
other things. As we find holes in the CDI armor we want to work with the community<br>
at large to fill the holes. CDI, although standard, is very new.<br>
We are hoping that the groundwork that CDI has laid down can get used outside of<br>
Java EE as well as inside of Java EE (we are not anti-Java EE).<br>
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
This article discussed more advanced CDI dependency injection in a tutorial format.<br>
It covered some of the features of CDI such as processing annotation data and working<br>
with multiple instances of various types using the <b><code>Instance</code></b> class to tap into the<br>
powerful CDI class scanner capabilities.<br>
</p>

<p>
CDI is a foundational aspect of Java EE 6. It is or will be shortly supported by<br>
Caucho's Resin, IBM's WebSphere, Oracle's Glassfish, Red Hat's JBoss and many<br>
more application servers. CDI is similar to core Spring and Guice frameworks.<br>
However CDI is a general purpose framework that can be used outside of JEE 6.<br>
</p>

<p>
CDI simplifies and sanitizes the API for DI and AOP. Through its use of <b><code>Instance</code></b>  and @Produces,<br>
CDI provides a pluggable architecture. With this pluggable architecture you can write code that finds new dependencies<br>
dynamically.<br>
</p>

<p>
CDI is a rethink on how to do dependency injection and AOP (interception really).<br>
It simplifies it. It reduces it. It gets rid of legacy, outdated ideas.<br>
</p>

<p>
CDI is to Spring and Guice what JPA is to Hibernate, and Toplink.<br>
CDI will co-exist with Spring and Guice.<br>
There are plugins to make them interoperate nicely. There is more integration option<br>
on the way.<br>
</p>

<p>
This is just a brief taste. There is more to come.<br>
</p>

# Resources #
  * [CDI Depenency Injection Article](http://java.dzone.com/articles/cdi-di-p1)
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
<p>
<blockquote>This article was written with CDI advocacy in mind by <a href='https://profiles.google.com/RichardHightower/about'>Rick Hightower</a>
with some collaboration from others.<br>
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
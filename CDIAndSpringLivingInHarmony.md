# Introduction #

<p>
Update: The CDI to Spring bridge works with CANDI, OpenWebBeans and Weld. The Spring to CDI extention works with CANDI and Weld.<br>
The Spring to CDI extention partially works with OpenWebBeans (just the @SpringLookup).<br>
</p>

<p>
Spring is very popular. CDI is very new. Although CDI is the standard for DI and Interception (light weight AOP), it is not as ubiquitous<br>
and Spring.<br>
</p>


<p>
Part of CDI success will be probably be indicative on how well it can play and integrate with Spring.<br>
</p>

<p>
Realizing this, we took a Roo generated application, and fooled around with it until we were able to inject CDI beans into Spring objects. This effort is called the Spring CDI Bridge.<br>
This basically allows you to inject CDI managed beans into Spring. We also had to go the other direction. We need the ability to inject Spring beans into CDI. This effort is called the CDI Spring Extension.<br>
</p>

<p>
The golden ticket, is to be able to inject Spring beans into CDI beans that are then injected into Spring beans ad infinitum. This is tricky due to the different lifecycles and typing systems involved in Spring and CDI. We have achieved this as well.<br>
</p>


## Bridging from the CDI World into Spring ##

In order to bridge from the CDI world into the Spring world, we created a [BeanFactoryPostProcessor](http://static.springsource.org/spring/docs/3.0.x/api/org/springframework/beans/factory/config/BeanFactoryPostProcessor.html).
This CdiBeanFactoryPostProcessor looks the CDI [BeanManager](http://docs.jboss.org/cdi/api/latest/javax/enterprise/inject/spi/BeanManager.html) in JNDI and uses it to find beans in CDI and map them as Spring bean definitions as follows:

**applicationContext.xml example configuring a CdiBeanFactoryPostProcessor**
```
	<bean class="org.cdisource.springintegration.CdiBeanFactoryPostProcessor" />
```

<p>
If you do not want to configure a BeanFactoryPostProcessor, you can also use CdiFactoryBean's to individually create bridges to CDI. CdiFactoryBean is similar to <a href='http://static.springsource.org/spring/docs/3.0.x/api/org/springframework/jndi/JndiObjectFactoryBean.html'>JndiObjectFactoryBean</a>. In fact the CdiBeanFactoryPostProcessor configures bean definitions that are really CdiFactoryBean configured to look up a class in CDI.<br>
</p>.

**applicationContext.xml example configuring a CdiFactoryBean to lookup a TaskRepository**
```
 <bean class="org.cdisource.springintegration.CdiFactoryBean" name="taskRespository" >
        <property name="beanClass" value="org.cdisource.springapp.TaskRepository"/>
     </bean>
```

CdiBeanFactoryPostProcessor is fairly powerful. Just install it into Spring and then all of your CDI beans are available to Spring. No fuss. This works with [Resin Candi](http://www.caucho.com/resin/candi/), [JBoss Weld](http://seamframework.org/Weld), and [OpenWebBeans http://openwebbeans.apache.org/owb/index.html](Apache.md).

You can find CdiBeanFactoryPostProcessor at  [CDI Spring Integration](https://github.com/CDISource/cdisource/tree/master/spring) which is part of the [CDI Source](https://github.com/CDISource) efforts to advocate the use of CDI. Please review [CdiBeanFactoryPostProcessor](https://github.com/CDISource/cdisource/blob/master/spring/src/main/java/org/cdisource/springintegration/CdiBeanFactoryPostProcessor.java) and the test cases for it and the [example roo based application that uses it](https://github.com/CDISource/examples/tree/master/spring-integration-example). We are seeking feedback.

## Bridging from the Spring World into CDI ##

We can also bridge from the Spring world into CDI. To do this we created two annotations: @Spring and @SpringLookup. @SpringLookup is the simpler of the two. It works in all three open source CDI implementations [Resin Candi](http://www.caucho.com/resin/candi/), [JBoss Weld](http://seamframework.org/Weld), and [OpenWebBeans http://openwebbeans.apache.org/owb/index.html](Apache.md). The @Spring annotation is more complex (has more advanced features), and only works in [Resin Candi](http://www.caucho.com/resin/candi/), and [JBoss Weld](http://seamframework.org/Weld).

(We plan on filing bug reports against OpenWebBeans and trying to work with that team to improve OpenWebBeans so that the Spring annotation can work there as well.)

**Examples of using Spring annotation**
```
package org.cdisource.springintegration;

import javax.inject.Inject;

public class CdiBeanThatHasSpringInjection {
	@Inject @Spring(name="fooBar") 
	FooSpringBean springBean;

	@Inject @Spring(name="fooBarnotActuallyThere", required=false)
	FooSpringBean notActuallyThere;
	
	
	@Inject @Spring(type=FooSpringBean2.class) 
	FooSpringBean2 injectByType;

	public void validate () {
		if (springBean==null) {
			throw new IllegalStateException("spring bean was null");
		}
		if (notActuallyThere!=null) {
			throw new IllegalStateException("notActuallyThere should be null");
		}
		if (injectByType==null) {
			throw new IllegalStateException("injectByType should be there");
		}

	}
}

```



The form
**by name**
```
	@Inject @Spring(name="fooBar") 
	FooSpringBean springBean;

```

will look up the bean in Spring at the appropriate time given the appropriate name. The extension we wrote will create a [Bean](http://docs.jboss.org/cdi/api/latest/javax/enterprise/inject/spi/Bean.html) that has a @Named qualifier when it sees this type of injection. OpenWebBeans rejects this named qualifier. This works in Weld and Resin Candi (4.0.17 and later).

The form

```
	@Inject @Spring(name="fooBarnotActuallyThere", required=false)
	FooSpringBean notActuallyThere;

```

If there is a chance the bean will not be there, i.e., the injection is optional, you can specify a required=false. This means if we can't find the bean in Spring, don't throw an exception.
This works in Weld and Resin Candi (4.0.17 and later).


The form

**by type**
```
	@Inject @Spring(type=FooSpringBean2.class) 
	FooSpringBean2 injectByType;

```

<p>
The above form will look up the type in the Spring application context by type instead of by name.<br>
FooSpringBean2 can be an interface or a concrete type.<br>
</p>

<p>
Thus you could have a concreted implementation in Spring as follows:<br>
</p>

```
	<bean name="fooBar3"  class="org.cdisource.springintegration.FooSpringBean2Impl"/>

```


The form

**by type by name**
```
	@Inject @Spring(name="foo2", type=FooSpringBean2.class) 
	FooSpringBean2 injectByType;

```

<p>
This is form will look up bean in the application context uses the name and the type. Spring throws an exemption if the types don't<br>
match.<br>
</p>

<p>
When developing this injection, using @Spring annotation was the ideal. Then we realized since the implementations did not support all of these<br>
features (OpenWebBeans at this point). This is where the @SpringLookup came into play. In our minds it is not ideal, the implementations<br>
should support the features in the @Spring annotation. @SpringLookup works in all three CDI containers. You use it as follows:<br>
</p>

```
package org.cdisource.springintegration;

import javax.inject.Inject;

public class CdiBeanThatHasSpringLookupInjection {
	@Inject @SpringLookup("fooBar2")
	FooSpringBean springBean;

	@Inject @SpringLookup("fooBar2")
	FooSpringBean springBean2;

	
	public void validate () {
		if (springBean==null) {
			throw new IllegalStateException("spring bean was null");
		}
		if (springBean2==null) {
			throw new IllegalStateException("spring bean2 was null");
		}

	}
}

```

<p>
Using @SpringLookup never uses types and it always required. @Spring and @SpringLookup work with Candi 4.0.17 and Weld.<br>
</p>


## Background ##
<p>

The SpringBridge (CDI to Spring) always worked on all containers. It worked right out of the bat. I created something similar for Presto a<br>
precursor to Crank. It would ask Hibernate for all of its managed beans and then registers a bunch of DAO, Controllers and Services on<br>
your behalf for CRUD. The SpringBridge works the same way except instead of asking Hibernate for entities, it asks CDI for managed beans.<br>
That part was easy. I had done it before (more or less) and am familiar with Spring after writing two large frameworks that sit on top of<br>
Spring (Spring is my home court).<br>
</p>

<p>
CDI is not my home court (yet). Here I needed a lot of help. The Weld reference guide to CDI was a big help. You can see the Extention uses<br>
the lessons quite extensively (you may even see a bit of copy and paste in there). Also working with Andy Gibson and Rob Williams has<br>
greatly expanded my CDI knowledge. I am more of a CDI enthusiast than a CDI expert.<br>
</p>

<p>
Early version of the Spring Extention (Spring to CDI) did not work at all. We have friends on the Resin Candi core engineering team who<br>
pointed us in the right direction. They whiteboarded a solution for us. They helped direct us what to do and then patched Resin Candi<br>
so what we did would actually work with Resin 4.0.17. This would not exist without their help.<br>
</p>

<p>
Initially, it only worked with Weld not Resin Candi 4.0.16. Then after Resin Candi 4.0.17, it worked better on Candi then Weld.<br>
Then we had to rework it so it worked the same on Weld and Candi. Eseentially, we had to remove uneeded features so it would work with<br>
Weld. Since the feature were uneeded, it was not a big deal (see Occam razor).<br>
</p>

<p>
As I write this, Mark Struberg and I are on IRC chat #openwebbeans at ircfreenode. Mark is woking on the OpenWebBeans project.<br>
He has forgotten more about CDI than I know and works from half way around the world from me in Austria.<br>
He is going to see what is what with OpenWebBeans and @Spring annotation.<br>
Perhaps @Spring Integration will work with OpenWebBeans really soon.<br>
</p>

<p>
I guess what I am trying to say is, we could not have done this without a lot of help from a lot of people. Whatever bugs you find are mine,<br>
whatever coolness you find is what we built on top of the shoulders of giants. We are seeking code reviews and feature requests.<br>
What should Spring to CDI integration look like? This is our vision. What is yours?<br>
</p>
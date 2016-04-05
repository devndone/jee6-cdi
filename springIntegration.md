## Introduction ##

<p>
Java EE 6 provides an easy-to-use, standards based, convention-over-configuration,<br>
enterprise component model.<br>
</p>

<p>
Java EE 6 also provides a new dependeny injection, annotation processing and<br>
interception system which is better than classic Spring. Some developers who<br>
currently use Spring will want to migrate to Java EE 6. This is an easy<br>
proposition for greenfield applications. Not all developers who want to migrate<br>
will be able to do it in one pass. Some developers will need to combine Spring<br>
and CDI. Other developer's may want to combine Java EE 6 and CDI with Spring<br>
based modules and libraries. The first article focuses on using CDI beans in a<br>
Spring.application context. The second article focuses using Spring managed beans<br>
in CDI.<br>
</p>


<p>
EJB 3.1 and CDI is a productive convention over configuration model.<br>
A lot of people will use EJB 3.1 and CDI because it is the standard.<br>
Even if you decide to adopt EJB 3.1 and CDI, you still may need to<br>
integrate with 3rd party libraries that use Spring or Spring modules.<br>
Thus, Spring integration might be a semi-permanent part of your architecture.<br>
Before we go into Spring / CDI integration let's cover a little bit why CDI is<br>
a good option, and why I think you should use it as your primary DI/interception<br>
framework.<br>
</p>


## Problems with Spring and Improvements to Java EE ##
<p>
Spring was born before annotations in the age of XML. Many projects end up with<br>
very large XML files that are difficult to maintain. Spring 2.5 through Spring 3<br>
added annotations but their use is not as widespread or as well understood as<br>
Spring's XML configuration. The Spring annotations are added on top of the<br>
existing Spring DI system in what some could argue a non-type safe injection.<br>
</p>

<p>
Guice created a DI system based on strongly typed annotations. Guice is a well<br>
designed strongly typed DI system.<br>
</p>

<p>
Java EE 6, based on ideas from Guice and Spring, improves further and creates an<br>
easier to use, general purpose, strongly typed DI system called Contexts and<br>
Dependency Injection (CDI). CDI clears up issues with interceptors in Java EE 5<br>
as well.<br>
</p>

<p>
One of the major advantages of Java EE 6 over Spring is there is less<br>
configuration and less moving parts. Java EE 6 usability surpasses Spring 3 and<br>
its testability comparable to Spring 3's.<br>
</p>

<p>
Spring is a collection of good ideas and trendy techniques some of which have gone out of style.<br>
A big part of Spring 3 was pruning some of these evolutionary dead ends out of the code base.<br>
However, many people who use Spring use later versions of Spring but in a style of Spring so to speak<br>
from cira 2004, i.e., XML.<br>
</p>

<p>
It is not enough for a team to say they use Spring. What do they use from Spring?<br>
Which parts do they use? Do they use custom classloaders? Do they use classpath<br>
scanning? Do they use AspectJ weaving? Do they use a combination of approaches?<br>
Do they write there own aspects? If so do they use traditional Spring AOP or<br>
AspectJ AOP? This makes integrating Spring with CDI a bit complicated as it<br>
is hard to tell exactly what a person means when they say they use Spring.<br>
</p>

<p>
The complexity and the maintainability of configuring Spring is complicated<br>
because of its build-your-own container approach to enterprise development.<br>
</p>

<p>
Roo, a utility from SpringSource to generate best-practice Spring 2.5 and Spring<br>
3.0 application, on the other hand relies heavily on AspectJ and annotations<br>
although AspectJ is not widely adopted and there is little AspectJ expertise in<br>
the industry. There is the Spring reality (XML) and the Spring vision of the<br>
future (Annotations, Roo and AspectJ). Any integration of Spring and CDI would<br>
need to take this into account.<br>
</p>

<img src='http://www.indeed.com/trendgraph/jobgraph.png?q=AspectJ%2C+Spring+Java&foo=.png' />

<p>
From the graph above, you might come to the conclusion that Spring's vision via<br>
Roo with regards to domain objects, annotations and AspectJ is different from<br>
Spring's user base, which it appears is primarily using XML. For those Spring<br>
users who are still using XML, before switching to Spring's new vision, they may<br>
want to first check out standards like Java EE 6, CDI and EJB 3.1 which provide<br>
a very productive convention over configuration environment.<br>
</p>

<p>
Spring's annotation support for injection is not strongly typed like CDI and<br>
Guice. It's annotations rely heavily on names to lookup other objects for many<br>
cases. It is an extension of the existing Spring IOC container which was written<br>
before annotations existed and before classpath scanning for annotations was the<br>
norm. Integrating CDI and Spring would need to bridge these gaps.<br>
</p>

## Integrating Spring and Java EE ##
<p>
Due to the improved useabiltty (type safe injection and convention over<br>
configuration) of CDI, a key part of Java EE 6 and the fact that it is the<br>
standard. It is very likely that many development shops will adopt Java EE 6<br>
and CDI in some form. Thus, the focus of this two part article series.<br>
</p>

<p>
Since Spring is more than just an DI container. It is a set of utility classes<br>
and modules. Java EE 6 scope is in a similar but different focus. While CDI<br>
scope is even more focused. Even if you decide to use CDI and Java EE 6, it is<br>
likely they you might need a capability that is part of the Spring ecosystem.<br>
Therefore, you will likely need to integrate CDI and Spring.<br>
Again referring to the first graph, traditional Spring is in wide use, however,<br>
Java EE use is even greater. Compare to the following graph.<br>
</p>

<img src='http://www.indeed.com/trendgraph/jobgraph.png?q=J2EE+or+%22Java+EE%22+or+JEE%2C+Spring+Java&foo.png' />

<p>
Again although Spring use is wide, it is not as wide as Java EE.<br>
</p>

<p>
For some application, you can replace Spring with Java EE 6 and CDI all the way.<br>
This will give you much simpler configuration. Then there are others who need<br>
one of the many modules at SpringSource which all not so strangely rely on Spring.<br>
Then there are third party frameworks that also use Spring. Even if you are a<br>
Java EE shop, it is very likely that you will need to integrate with Spring at<br>
some level. Then there are those who can't afford to switch over whole hog to a new<br>
framework, and must do it piecemeal.<br>
</p>

<p>
Currently, for example, there is no CDI enabled Model 2 style framework like<br>
Spring MVC. Not all developers agree with the JSF framework approach. Therefore,<br>
there may be a need and desire to integrate Spring MVC on the front end while<br>
using Java EE 6 and CDI for the backend.<br>
</p>

<p>
For other application you may want to start to use Java EE 6 and CDI for some new use cases<br>
while keeping Spring for other use cases as you start to adopt the more<br>
productive CDI and Java EE features into your development stack. This would be a<br>
gradual migration.<br>
</p>

<p>
Let's briefly cover how one might integrate Spring and CDI in the same application.<br>
We will take two applications, one a Java EE 6 application and the other a<br>
modified project that Roo generated (I stripped out the domain objects and<br>
the AspectJ mixins).<br>
</p>

## Java EE 6 and Spring 3 with annotations more similar than not ##

<p>
Spring due to project pitchfork closely aligns to the style of Java EE 5 in many respects.<br>
</p>

<p>
For an example of this let's compare some database access objects written using<br>
Spring and EJB. Look at the EJB 3.1 and CDI version of a database access object.<br>
</p>


### TaskRepository class ###

```
...
import javax.ejb.Stateless;
import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;

@Stateless                                         // <1>
public class TaskRepository {
	
    @PersistenceContext                            // <2>
    private EntityManager entityManager;

    
    public void persist(Task task) {
        this.entityManager.persist(task);
    }
...
```


&lt;1&gt;

 Identify this class as an EJB that has transaction support


&lt;2&gt;

 Inject the persistence context from JPA into the EJB

<p>
Now without blinking, look at the Spring version of the same database access object using Spring.<br>
</p>

#### TaskRepository class ####
```
...
import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;


import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;

@Repository                                      // <1>
@Transactional                                   // <2>
public class TaskRepository {
	
    @PersistenceContext
    private EntityManager entityManager;         // <3>

    
    public void persist(Task task) {
        this.entityManager.persist(task);
    }
...
```


&lt;1&gt;

 Identify this class as Spring bean (must be registered with Spring)


&lt;2&gt;

 Mark all of the methods as transactional


&lt;3&gt;

 Inject the persistence context from JPA into the Spring bean

<p>
The annotations are somewhat functionally equivalent. At first blush, there is<br>
no real difference between these. However one of the key differences is the way<br>
the EntityManager, which is stateful, is handled and the underlying design of<br>
EJBs and Spring. In the EJB world, the entityManager is injected before this<br>
EJB is used, and the container worries about the underlying thread and<br>
transaction isolation. In the Spring world, the entityManager is a proxy object<br>
to an entityManager that must be looked up on every method call to the<br>
entityManager (sometimes in map associated with a thread local varaible,<br>
sometimes as a JTA transaction resource depending on your configuration).<br>
The EJB 3 approach is more efficient and consistent in addition to being the standard.<br>
</p>

<p>
Also, in the Spring version, you would need a few extra applicationContext.xml<br>
files and a few entries in a web.xml file. Here is the applicationContext.xml<br>
file to use the Spring version of the database access object.<br>
</p>


### applicationContext.xml ###
```
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<beans xmlns="http://www.springframework.org/schema/beans"
	xmlns:aop="http://www.springframework.org/schema/aop" xmlns:context="http://www.springframework.org/schema/context"
	xmlns:jee="http://www.springframework.org/schema/jee" xmlns:tx="http://www.springframework.org/schema/tx"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://www.springframework.org/schema/aop http://www.springframework.org/schema/aop/spring-aop-3.0.xsd
	         http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans-3.0.xsd
	         http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context-3.0.xsd         
	         http://www.springframework.org/schema/jee http://www.springframework.org/schema/jee/spring-jee-3.0.xsd         
	         http://www.springframework.org/schema/tx http://www.springframework.org/schema/tx/spring-tx-3.0.xsd">
	<context:property-placeholder location="classpath*:META-INF/spring/*.properties" />
	<context:component-scan base-package="org.cdisource.springapp">                <!-- <1> -->
		<context:exclude-filter expression="org.springframework.stereotype.Controller"
			type="annotation" />
	</context:component-scan>

	<!-- <2> -->
	<bean class="org.springframework.orm.jpa.JpaTransactionManager"               
		id="transactionManager">
		<property name="entityManagerFactory" ref="entityManagerFactory" />
	</bean>

	<!-- <3> -->
	<tx:annotation-driven mode="aspectj"                                          
		transaction-manager="transactionManager" />

	<!-- <4> -->
	<jee:jndi-lookup id="dataSource" jndi-name="jdbc/basic" />                    
 
        <!-- <5> -->
	<bean                                                                           
		class="org.springframework.orm.jpa.LocalContainerEntityManagerFactoryBean"
		id="entityManagerFactory">
		<property name="dataSource" ref="dataSource" />
	</bean>


</beans>
```



&lt;1&gt;

 Look for @Repository, and @Service stereotypes and add them to the application context.


&lt;2&gt;

 Configure transaction manager for JPA


&lt;3&gt;

 Create an annotation driven transaction support using AspectJ


&lt;4&gt;

 Lookup a JNDI datasource


&lt;5&gt;

 Configure the EntityManagerFactory

<p>
In the Spring version you have to essentially configure your own container.<br>
You have many options. Do you want to use a custom Spring classloader? Do you<br>
want to use Spring AOP/AspectJ code weaving? etc. Every shop uses some subset of<br>
what is available in the Spring universe for solving even basic issues like<br>
transaction demarcation of database access object methods. There are many ways<br>
to solve the same problem. This is good but can be bad as well. It means if you<br>
are hiring someone off the street to do development with knowledge of Spring<br>
that it is unlikely that you will find two people using Spring the same way.<br>
Are they using the new annotations? Are they using the AspectJ integration?<br>
In the last three consulting engagements I was on where folks used Spring,<br>
they were all using Spring XML from 2004. There may just be too many options.<br>
</p>

<p>
To inject the <code>TaskRepository</code> bean into a Spring MVC controller we could use<br>
@AutoWire (just like before).<br>
</p>

#### Injecting a `TaskRepository` into a `TaskController` using Spring. ####
```
package org.cdisource.springapp.web;

...
import org.cdisource.springapp.TaskRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
...

@RequestMapping("/tasks")
@Controller
public class TaskController {

	@Autowired		// <1>
	private TaskRepository repo;
	...
```


&lt;1&gt;

 Injecting a `TaskRepository` into a Spring MVC controller using Spring.


This is similar to injecting a CDI bean into a JSF backing bean as shown below.


#### Injecting a `TaskRepository` into a `TaskController` using CDI. ####
```

package org.cdisource.springapp.task;

import java.io.Serializable;
import javax.inject.Inject;
import javax.inject.Named;
...

@Named("taskHome")
@ConversationScoped
public class TaskHome implements Serializable {
        ...
	
	@Inject
	private TaskRepository repo;  // <1>

        ...
```


&lt;1&gt;

 Injecting a `TaskRepository` into a JavaServer Faces (JSF) Backing bean using CDI.

<p>
For simple cases like these @Inject from CDI and  Spring's @Autowired are fairly<br>
similar. The real difference in this example is that one uses Spring MVC and<br>
one uses JavaServer Faces. The reality is that not all people use JavaServer Faces,<br>
and Java EE 6 supports non JavaServer Faces applications using JavaServer Pages<br>
(JSP) and Servlets. If you are building an application using JSP and Servlets<br>
then Spring MVC is a popular option. In addition, Spring is a popular option for<br>
integration with many other web frameworks like Tapestry, Wicket, Struts and more.<br>
</p>

<p>
The question in many developer's mind is can I use CDI with Spring<br>
MVC, Tapestry, Wicket, Struts and more? The answer is yes. You don't<br>
have to wait. If you are already using Spring, then integrating CDI is<br>
quite easy with all of these frameworks and we will show you how to do<br>
it in this article. (Note there is also a CDI plugin for Struts 2.)<br>
</p>

## Working CDI into the mix ##

<p>
One easy way to work CDI into the mix is to use a Java EE 6 container<br>
and use the EJB and CDI support with JPA. It is an understatement to<br>
say that EJB, CDI and JPA work well together. You see JPA is part of<br>
EJB. JPA defines the way modern entity beans are written. If you are<br>
like me, you may cringe at the name EJB. Well, EJB is not EJB of yore.<br>
EJB + CDI + JPA is a powerful combination of POJO productivity. The<br>
past sins of EJB have been fixed with EJB 3.1, CDI and JPA. Let's look<br>
at how easy it is to integrate a true EJB into a Spring application<br>
using CDI.<br>
</p>

<p>
In order to bridge the <code>TaskRepository</code> into Spring you could use a<br>
<code>org.springframework.beans.factory.FactoryBean</code>. A <code>FactoryBean</code> is<br>
used to bridge from Spring into other object systems. One famous<br>
<code>FactoryBean</code> that ships with the Spring framework is the<br>
<code>JndiObjectFactoryBean</code>. The <code>JndiObjectFactoryBean</code> uses JNDI to<br>
lookup a bean and map it into Spring's application context, thus<br>
bridging the gap between JNDI and Spring. Let's create a factory bean<br>
that get's a <code>TaskRepository</code> object from CDI and maps it as an<br>
injectable bean in the Spring world.<br>
</p>



#### TaskRepositoryFactoryBean ####
```
package org.cdisource.springapp;

import javax.enterprise.inject.spi.BeanManager; // <2>

import org.springframework.beans.factory.FactoryBean;
import org.springframework.beans.factory.InitializingBean;
import org.cdisource.beancontainer.BeanContainer; // <3>
import org.cdisource.beancontainer.BeanContainerImpl; // <3>

public class TaskRepositoryFactoryBean implements FactoryBean<TaskRepository>, InitializingBean  { // <1>

	private BeanContainer beanContainer; // <3>
	private BeanManager beanManager; // <2>
	
	public void setBeanManager(BeanManager beanManager) {
		this.beanManager = beanManager;
	}

	@Override
	public void afterPropertiesSet() throws Exception {
		// <3>
		beanContainer = new BeanContainerImpl(beanManager);
	}

	@Override
	public TaskRepository getObject() throws Exception {
		// <4>
		return beanContainer.getBeanByType(TaskRepository.class);
	}

	@Override
	public Class<?> getObjectType() {
		return TaskRepository.class;
	}

	@Override
	public boolean isSingleton() {
		return true;
	}


}
```


&lt;1&gt;

 `TaskRepositoryFactoryBean` is both a `FactoryBean` and an `InitializingBean` which means in Spring parlance a bean that can create a bean and a bean that will be notified after all of its members have been injected.


&lt;2&gt;

 The `BeanManager` is the main interface from CDI used to lookup beans.


&lt;3&gt;

 Since the `BeanManager` is a bit difficult to use (very low level), a bumper crop of support open source support APIs including Weld Solder and CDISource have cropped up. The `BeanContainer` is from the CDISource project (both listed in the reference section of the article).


&lt;4&gt;

 In the `getObject` method of the FactoryBean we look up the `TaskRepository` in CDI. Spring calls this method to lookup the bean for injection. The `getObject` method is from the FactoryBean interface.

Since you may or may not ever use CDISource or Weld Solder, let's briefly cover how one would look up a bean in plain CDI by showing you what the `getBeanByType` method looks like.


#### getBeanByType possible implementation, (with removed NPE checks for brevity) ####

```

	@Override
	public <T> T getBeanByType(Class<T> type, Annotation... qualifiers) {
		BeanManager beanManager = ...
		Set<Bean<?>> beans = beanManager.getBeans(type, qualifiers);
		if (beans.isEmpty()) {
			throw new RuntimeException("Could not locate a bean of type "
					+ type.getName());
		}
		Bean<?> bean = beanManager.resolve(beans);
		CreationalContext<?> context = beanManager
				.createCreationalContext(bean);
		@SuppressWarnings("unchecked")
		T result = (T) beanManager.getReference(bean, bean.getBeanClass(),
				context);
		return result;
	}
```

<p>
When you use CDI in a Java EE application, you never have to work at<br>
this level of the CDI code. However, when you are trying to get Spring<br>
to play nice with CDI, it makes sense. (You can download and use this<br>
example, see the resources section below).<br>
</p>

<p>
This technique would not just work for EJB, it would work for any CDI<br>
managed bean you wanted to inject inside of Spring application<br>
context.<br>
</p>

<p>
Now that we have integrated CDI with Spring, we can rip out all of the<br>
"configure your own container" stuff out of the application context<br>
and let the Java EE 6 container do what is was built to do as follows:<br>
</p>

#### simplified application context.xml after letting EJB CDI do its thing ####

```
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<beans xmlns="http://www.springframework.org/schema/beans" xmlns:jee="http://www.springframework.org/schema/jee" 
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans-3.0.xsd
	         http://www.springframework.org/schema/jee http://www.springframework.org/schema/jee/spring-jee-3.0.xsd">   

    <bean class="org.cdisource.springapp.TaskRepositoryFactoryBean" name="taskRespository"> <!-- <1> -->
		<property name="beanManager"><jee:jndi-lookup jndi-name="java:comp/BeanManager"/></property> <!-- <2> -->
    </bean>
</beans>
```



&lt;1&gt;

 Configure our `TaskRepositoryFactoryBean`.


&lt;2&gt;

 Use JNDI to lookup the `BeanManager`.

<p>
Ok. That is more like it. We went from forty lines of XML to 10. In<br>
most people's book that is a good. The code for the Spring controller<br>
would be the same. As you can see, Java EE 6 is much easier to<br>
configure.<br>
</p>


## Working CDI into the mix ##

<p>
Now one problem we have with this approach is that every time you want<br>
to introduce a new CDI bean into Spring, you need to create a new<br>
<code>FactoryBean</code>. It would be better to have a generic CDI <code>FactoryBean</code>.<br>
One attempt would look like this: </p>


### CdiFactoryBean, generic way to inject beans into Spring ###
```
package org.cdisource.springintegration;


import javax.enterprise.inject.spi.BeanManager;

import org.springframework.beans.factory.FactoryBean;
import org.springframework.beans.factory.InitializingBean;
import org.cdisource.beancontainer.BeanContainer;
import org.cdisource.beancontainer.BeanContainerImpl;

public class CdiFactoryBean implements FactoryBean<Object>, InitializingBean {

	private boolean singleton = true;
	private BeanManager beanManager; // <1>
	private Class<?> beanClass; // <2>
	private BeanContainer beanContainer; // <3>
	

	@Override
	public void afterPropertiesSet() throws Exception {
		beanContainer = new BeanContainerImpl(beanManager);
	}

	public void setBeanClass(Class<?> beanClass) {
		this.beanClass = beanClass;
	}

	@Override
	public Object getObject() throws Exception {
		return beanContainer.getBeanByType(beanClass);
	}

	@Override
	public Class<?> getObjectType() {
		return beanClass;
	}

	@Override
	public boolean isSingleton() {
		return singleton;
	}

	public void setSingleton(boolean singleton) {
		this.singleton = singleton;
	}

	public void setBeanManager(BeanManager beanManager) {
		this.beanManager = beanManager;
	}

}
```


&lt;1&gt;

 The `beanManager` is injected via JNDI.


&lt;2&gt;

 The `beanClass` is the type that we are creating.


&lt;3&gt;

 The `beanContainer` is the utility class we spoke of earlier to simplfy the CDI `BeanManager` access.

Now when we are configuring the application context we do the following:

#### simplified application context.xml after letting EJB CDI do its thing ####
```
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<beans xmlns="http://www.springframework.org/schema/beans" xmlns:jee="http://www.springframework.org/schema/jee" 
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans-3.0.xsd
	         http://www.springframework.org/schema/jee http://www.springframework.org/schema/jee/spring-jee-3.0.xsd">   

     <bean class="org.cdisource.springintegration.CdiFactoryBean" name="taskRespository" >
     	<property name="beanClass" value="org.cdisource.springapp.TaskRepository"/> <!-- <1> -->
	<property name="beanManager"><jee:jndi-lookup jndi-name="java:comp/BeanManager"/></property>
     </bean>

</beans>
```




&lt;1&gt;

 <p> We just have one extra property called beanClass, which tells Spring which class our FactoryBean is creating. Now we have a generic way to bridge<br>
the Spring and CDI worlds. But, now we would have to add a new entry every time we want to create the bridge to the CDI world for a new bean.<br>
If you have one CDI bean to map to Spring, no problem. If you have 40 or more, well who wants to write that much XML.<br>
If only there was some way to look up all of the beans in CDI and<br>
automatically map them into Spring. Well there is. </p>

<p>
Spring provides an extension mechanism to add beans directly into an<br>
application context. We could scan all of the CDI beans, and map them<br>
into Spring using a Spring <code>BeanFactoryPostProcessor</code>. To do this we<br>
will need to programmatically create Spring bean definition based on<br>
CDI bean objects as follows:<br>
</p>

#### Bridging the gap from CDI beans into the Spring world, every bean using a BeanFactoryPostProcessor ####
```
package org.cdisource.springintegration;

import java.util.Set;

import javax.enterprise.inject.spi.Bean;
import javax.inject.Named;
import org.springframework.beans.BeansException;
import org.springframework.beans.factory.config.BeanFactoryPostProcessor;
import org.springframework.beans.factory.config.ConfigurableListableBeanFactory;
import org.springframework.beans.factory.support.BeanDefinitionBuilder;
import org.springframework.beans.factory.support.DefaultListableBeanFactory;


public class CdiBeanFactoryPostProcessor implements BeanFactoryPostProcessor { // <1>
	
	...
	private BeanManagerLocationUtil beanManagerLocationUtil = new BeanManagerLocationUtil();


	@Override
	public void postProcessBeanFactory(
			ConfigurableListableBeanFactory beanFactory) throws BeansException {
		
		DefaultListableBeanFactory factory = (DefaultListableBeanFactory) beanFactory; 
		
		Set<Bean<?>> beans = beanManagerLocationUtil.beanManager().getBeans(Object.class); // <2>
		for (Bean<?> bean : beans) {
			
			if (bean.getName()!=null && bean.getName().equals("Spring Injection")){
				continue;
			}
			// <3>		
			BeanDefinitionBuilder definition = BeanDefinitionBuilder.rootBeanDefinition(CdiFactoryBean.class)
						.addPropertyValue("beanClass", bean.getBeanClass()) // <4>
						.addPropertyValue("beanManager", beanManagerLocationUtil.beanManager()) // <5>
						.setLazyInit(true);
			String name = generateName(bean); // <6>
			factory.registerBeanDefinition(name, definition.getBeanDefinition());
		}
	}

	private String generateName(Bean<?> bean) {
  		... // <7>
	}

}

```



&lt;1&gt;

 <p><code>CdiBeanFactoryPostProcessor</code> is a <code>BeanFactoryPostProcessor</code>
which is to say that it is a Spring extension designed to work with<br>
bean definitions from Spring after Spring initializes the application<br>
context and before it starts creating actual beans. </p>


&lt;2&gt;

 `beanManagerLocationUtil` is a helper object used to look up the CDI `beanManager` (typically in JNDI).


&lt;3&gt;

 For every CDI bean (`javax.enterprise.inject.spi.Bean`) create a Spring `BeanDefinition`. Note we are defining a bunch of CdiFactoryBean.class bean definition entries.


&lt;4&gt;

 Use the CDI bean's class (`javax.enterprise.inject.spi.Bean.beanClass`) property to populate the CdiFactoryBean beanClass.


&lt;5&gt;

 Use the beanManagerLocationUtil.beanManager() to populate the CdiFactoryBean.beanManager.


&lt;6&gt;

 We generate a nice unique bean name based on the bean definition to make things easier to debug.


&lt;7&gt;

 The nice unique bean name is based on the beanClass long or short name.

The application context is even simpler now.


#### simplified application context.xml ####
```
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<beans xmlns="http://www.springframework.org/schema/beans" xmlns:jee="http://www.springframework.org/schema/jee" 
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans-3.0.xsd
	         http://www.springframework.org/schema/jee http://www.springframework.org/schema/jee/spring-jee-3.0.xsd">   

          <bean class="org.cdisource.springintegration.CdiBeanFactoryPostProcessor"/>

</beans>
```

Now all CDI beans are in the Spring application context.



## Conclusion ##
<p>
Spring was built to solve problems with J2EE. Spring borrowed ideas<br>
from J2EE and other projects and made them easier to use and more<br>
testable. Spring was a great stop gap for many architects and<br>
developers. Java EE 5 and Java EE 6 learned from the examples of<br>
Spring, Guice and other like projects. Spring learned from the<br>
examples of Java EE 5 & 6 and Guice. Now Java EE 6 has a CDI DI<br>
mechanism that rivals Spring's except it is even easier to use and it<br>
is type safe (less error prone). That said, Spring is still a thriving<br>
community and has tons of ideas and energy and new modules and<br>
projects. </p>

<p>
In addition many other useful projects also use Spring. The task going<br>
forward for Java EE 6 is how do you combine the ease of use of CDI<br>
with the utility of Spring, and the answer is CDI/Spring integration.<br>
</p>

<p>
This article covered the first part of CDI/Spring integration which is<br>
how do you map CDI beans into Spring. The next article will cover the<br>
second part, which is how do you map Spring beans into CDI. In the<br>
next article we cover building a custom extension to map Spring beans<br>
into CDI.<br>
</p>
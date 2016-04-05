# Introduction #

There is no standard interface to doing CDI SE.
We would like this for the tutorial series so folks can download the tutorials and get them to work
with their CDI container of choice. This will also be useful for unit testing.

[Weld](http://seamframework.org/Weld) has a way.
[Caucho Resin](http://caucho.com/resin-4.0/) has a way.
And, we assume [Apache OpenWebBeans](http://openwebbeans.apache.org/) has a way.

We are most familiar with Resin and Weld so we will start with them.

# Design goals #

  * Single interface for looking up beans by annotation and name
  * Single callback for being notified when the container starts up (nice to have for now)
  * Support unit testing extension that works with all three containers

The goals may change as we progress. For now, we want this to work with both Resin and Weld. In the future, we will get it to work with OpenWebBeans.

For now, we just want a standard way to host our examples for our tutorials series.

The vision is as follows:

  * Create a github account for this project to host this common interface for CDI SE
  * Host a maven repository here at this project site which will host this artifact
  * Change tutorial to use this maven repo as a repository
  * Add items to the common lib as needed
  * To keep the maven pom.xml files simple, we will branch the tutorial into three branches,
    * one for Resin
    * one for Weld
    * one for OpenWebBeans
  * End user will use the branch based on the CDI SE container they are interested in

For now this new artifact will be called org.github.cdiadvocate:cdise.

## Design Notes for Resin ##

`com.caucho.resin.ResinBeanContainer` is the main interface for Resin's CDI container. You can use this
to run CDI from a main method.

`ResinBeanContainer` has a method called getBeanByName and getInstance(Class, Annotation...) to look up a bean by its class and a list of annotations. There is also a start method to start the container. There are methods to add jars files and classpaths locations of classes to scan. Resin uses compiling class-loaders so the locations can have Java source and Resin will compile it and add the annotations. Resin's approach is very powerful.

## Design Notes for Weld ##
Weld allows the launch of CDI applications through its `org.jboss.weld.environment.se.StartMain`. You just ensure the jar files, and classpath is setup ahead of time. You can not manipulate the classpath like you can with `ResinBeanContainer` so our common interface should probably leave that important feature out (for now). We can add this feature later if needed.

Internally `StartMain` uses `WeldContainer` (`org.jboss.weld.environment.se.WeldContainer`). `WeldContainer` does not do much.  To get a `WeldContainer` you initialize the `Weld` CDI system (`org.jboss.weld.environment.se.Weld`) like so:

```
        WeldContainer weld = new Weld().initialize();

```


```
//import InstanceManager same package internal class to Weld
//
public class WeldContainer
{

   private final InstanceManager instanceManager;
   private final BeanManager beanManager;

   @Inject
   protected WeldContainer(InstanceManager instanceManager, BeanManager beanManager)
   {
      this.instanceManager = instanceManager;
      this.beanManager = beanManager;
   }
...
   public Instance<Object> instance() {
      return instanceManager.getInstances();
   }
...
 
  public BeanManager getBeanManager()
   {
      return beanManager;
   }
}

```

## First Cut ##

**Common interface**
```
package org.cdi.advocacy;

import java.lang.annotation.Annotation;

public interface BeanContainer {
	public Object getBeanByName (String name);
	public <T> T getBeanByType(Class<T> type, Annotation ...qualifiers);
	public void start();
	public void stop();
	
}
```


**Manager**
```
package org.cdi.advocacy;

import java.util.Properties;
import java.util.ServiceLoader;

public class BeanContainerManager {
	public static String PROP_NAME = "org.cdi.advocacy.BeanContainer";

	public static BeanContainer getInstance() {
		return getInstance(System.getProperties());
	}

	public static BeanContainer getInstance(Properties properties) {
		try {
			/* The property should override the ServiceLoader if found. */
			String beanContainerClassName = properties.getProperty(PROP_NAME);

			
			/* If the property was not found, use the service loader. */
			if (beanContainerClassName == null) {
				ServiceLoader<BeanContainer> instance = ServiceLoader
						.load(BeanContainer.class);
				if (instance.iterator().hasNext()) {
					return instance.iterator().next();
				}
			}
			
			/* If class property not found in the passed properties, then Resin is the default for now, 
			 * we may switch to the RI.
			 */
			beanContainerClassName = beanContainerClassName!=null ?  beanContainerClassName : "org.cdi.advocacy.ResinBeanContainer";

			
			/* Get the classloader associated with the current webapp and not the global classloader */
			ClassLoader contextClassLoader = Thread.currentThread().getContextClassLoader();
			Class<?> clazz = Class.forName(beanContainerClassName, true, contextClassLoader);
			BeanContainer beanContainer = (BeanContainer) clazz.newInstance();
			return beanContainer;

		} catch (Exception ex) {
			throw new RuntimeException(ex);
		}
	}
}

```

**Resin Impl**
```
package org.cdi.advocacy;

import java.lang.annotation.Annotation;

public class ResinBeanContainer implements BeanContainer {
	com.caucho.resin.ResinBeanContainer delegate = new com.caucho.resin.ResinBeanContainer();
	
	public Object getBeanByName(String name) {
		return delegate.getBeanByName(name);
	}

	public <T> T getBeanByType(Class<T> type, Annotation... qualifiers) {
		return delegate.getInstance(type, qualifiers);
	}

	@Override
	public void start() {
		delegate.start();
	}
	
	@Override
	public void stop() {
		delegate.close();
	}
	

}
```

**Weld First cut**
```
package org.cdi.advocacy;

import java.lang.annotation.Annotation;
import java.util.Set;

import javax.enterprise.context.spi.CreationalContext;
import javax.enterprise.inject.spi.Bean;
import javax.enterprise.inject.spi.BeanManager;

import org.jboss.weld.environment.se.Weld;
import org.jboss.weld.environment.se.WeldContainer;

public class WeldBeanContainer implements BeanContainer {
	WeldContainer delegate;
	
	public Object getBeanByName(String name) {
		
		BeanManager beanManager = delegate.getBeanManager();
		Set<Bean<?>> beans = beanManager.getBeans(name);
		Bean<?>  bean = beanManager.resolve(beans);
		CreationalContext<?> context = beanManager.createCreationalContext(bean);
		
		return beanManager.getReference(bean, bean.getBeanClass(), context);
	}

	public <T> T getBeanByType(Class<T> type, Annotation... qualifiers) {
		return (T) delegate.instance().select(type, qualifiers).get();
	}

	@Override
	public void start() {
		delegate = new Weld().initialize();
	}
	
	@Override
	public void stop() {
		//??
	}
	

}
```



**Open WebBeans TBD**
```
package org.cdi.advocacy;

import java.lang.annotation.Annotation;

public class WeldBeanContainer implements BeanContainer {
	
	public Object getBeanByName(String name) {
              ???
	}

	public <T> T getBeanByType(Class<T> type, Annotation... qualifiers) {
             ???
	}

	@Override
	public void start() {
              ???
	}
	
	@Override
	public void stop() {
                 ???
	}
	

}

```

**Usage by name**
```
package org.cdi.advocacy;

import java.math.BigDecimal;


public class AtmMain {

	static BeanContainer beanContainer =  BeanContainerManager.getInstance();
	static { beanContainer.start(); }

	public static void main(String[] args) throws Exception {
		AutomatedTellerMachine atm = (AutomatedTellerMachine) beanContainer
				.getBeanByName("atm");

		atm.deposit(new BigDecimal("1.00"));

	}

}

```

**Usage by type**
```
...
public class AtmMain {

	static BeanContainer beanContainer =  BeanContainerManager.getInstance();
	static { beanContainer.start(); }

	public static void main(String[] args) throws Exception {
		AutomatedTellerMachine atm = beanContainer.getBeanByType(AutomatedTellerMachine.class);
		atm.deposit(new BigDecimal("1.00"));

	}

}
```
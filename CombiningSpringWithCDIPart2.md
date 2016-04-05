<p>
I added support for discovering all the beans in CDI and registering them all in Spring as bean definitions.<br>
</p>

<p>
This is a continuations of the last post <a href='CombiningSpringWithCDI.md'>part 1</a>.<br>
</p>

<p>
The last step we added a FactoryBean that was tied to the TaskRepository.<br>
The next step is to make this generic.<br>
</p>
**CdiFactoryBean**
```
package org.cdisource.springintegration;

import javax.enterprise.inject.spi.BeanManager;
import javax.naming.InitialContext;

import org.springframework.beans.factory.FactoryBean;
import org.cdisource.beancontainer.BeanContainer;
import org.cdisource.beancontainer.BeanContainerImpl;
import org.cdisource.beancontainer.BeanContainerInitializationException;

public class CdiFactoryBean implements FactoryBean<Object> {

	private BeanContainer beanContainer = null;
	private final String BEAN_MANAGER_LOCATION = "java:comp/BeanManager";
	
	private Class<?> beanClass;
	
	private boolean singleton = true;

	
	public void setBeanClass(Class<?> beanClass) {
		this.beanClass = beanClass;
	}

	@Override
	public Object getObject() throws Exception {

		if (beanContainer==null) {
			InitialContext ic = new InitialContext();
			Object bean = null;
			try {
				bean = ic.lookup(BEAN_MANAGER_LOCATION);
			} catch (Exception e) {
				throw new BeanContainerInitializationException("Unable to lookup BeanManager instance in JNDI", e);
			}
			if (bean == null) {
				throw new BeanContainerInitializationException(
						"Null value returned when looking up the BeanManager from JNDI");
			}
			if (bean instanceof BeanManager) {
				beanContainer = new BeanContainerImpl((BeanManager)bean);
			} else {
				String msg = "Looked up JNDI Bean is not a BeanManager instance, bean type is " + bean.getClass().getName();
				throw new BeanContainerInitializationException(msg);
			}
		}
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

}

```

Then you can register this in the applicationContext as follows:

**applicationContext.xml**
```

     <bean class="org.cdisource.springintegration.CdiFactoryBean" name="taskRespository" >
     	<property name="beanClass" value="org.cdisource.springapp.TaskRepository"/>
     </bean>

```

<p>
Of course, this is a bit of a pain. Do you really want to register every CDI bean in your system so it is available for Spring? Imagine a system with 25 CDI beans or 250 CDI beans. Imagine what the Spring XML file will look like. Yuck.<br>
</p>

<p>
We need a way to map CDI beans into the spring applicationContext.<br>
</p>

The next step is bulk import a bunch of beans from CDI into Spring as follows:

```

package org.cdisource.springintegration;

import java.lang.annotation.Annotation;
import java.util.Set;

import javax.enterprise.inject.spi.Bean;
import javax.enterprise.inject.spi.BeanManager;
import javax.inject.Named;
import javax.naming.InitialContext;

import org.cdisource.beancontainer.BeanContainerInitializationException;
import org.springframework.beans.BeansException;
import org.springframework.beans.factory.config.BeanFactoryPostProcessor;
import org.springframework.beans.factory.config.ConfigurableListableBeanFactory;
import org.springframework.beans.factory.support.BeanDefinitionBuilder;
import org.springframework.beans.factory.support.DefaultListableBeanFactory;

public class CdiBeanFactoryPostProcessor implements BeanFactoryPostProcessor {

	@Override
	public void postProcessBeanFactory(
			ConfigurableListableBeanFactory beanFactory) throws BeansException {
		
		DefaultListableBeanFactory factory = (DefaultListableBeanFactory) beanFactory;
		
		Set<Bean<?>> beans = beanManager().getBeans(Object.class);
		for (Bean bean : beans) {
			BeanDefinitionBuilder definition = BeanDefinitionBuilder.rootBeanDefinition(CdiFactoryBean.class).addPropertyValue("beanClass", bean.getBeanClass()).setLazyInit(true);
			Named named = (Named) bean.getBeanClass().getAnnotation(Named.class);
			String name = named != null ? named.value() : bean.getBeanClass().getSimpleName() + "FactoryBean";
			factory.registerBeanDefinition(name, definition.getBeanDefinition());
		}
	}

	
	private final String BEAN_MANAGER_LOCATION = "java:comp/BeanManager";
	private BeanManager beanManager;

	private BeanManager beanManager() {
		if (beanManager == null) {
			Object bean = null;

			try {
				InitialContext ic = new InitialContext();
				bean = ic.lookup(BEAN_MANAGER_LOCATION);
			} catch (Exception e) {
				throw new BeanContainerInitializationException(
						"Unable to lookup BeanManager instance in JNDI", e);
			}
			if (bean == null) {
				throw new BeanContainerInitializationException(
						"Null value returned when looking up the BeanManager from JNDI");
			}
			if (bean instanceof BeanManager) {
				this.beanManager = (BeanManager) bean;
			} else {
				String msg = "Looked up JNDI Bean is not a BeanManager instance, bean type is "
						+ bean.getClass().getName();
				throw new BeanContainerInitializationException(msg);
			}
		}
		return this.beanManager;

	}

}

```


The heart of the class functionality is here:

```
		DefaultListableBeanFactory factory = (DefaultListableBeanFactory) beanFactory;
		
		Set<Bean<?>> beans = beanManager().getBeans(Object.class);
		for (Bean bean : beans) {
			BeanDefinitionBuilder definition = BeanDefinitionBuilder
                                .rootBeanDefinition(CdiFactoryBean.class)
                                .addPropertyValue("beanClass", 
                                bean.getBeanClass()).setLazyInit(true);
			Named named = (Named) bean.getBeanClass().getAnnotation(Named.class);
			String name = named != null ? named.value() : bean.getBeanClass().getSimpleName() + "FactoryBean";
			factory.registerBeanDefinition(name, definition.getBeanDefinition());
		}

```

<p>
We iterate through the beans from CDI, create a Spring definition that uses CdiFactoryBean from the last step.<br>
</p>

<p>
We register the CdiFactoryBean. We use the name from the @Named attribute if possible. If not we generate a name.<br>
</p>
# Introduction #

Notes on how to combine Spring with CDI

# Using Roo to setup the sample project #

I created a simple application in Roo that generated one Task entity as follows:

```
project --topLevelPackage org.cdisource.springapp
persistence setup --provider HIBERNATE --database HYPERSONIC_IN_MEMORY --jndiDataSource jdbc/basic
entity --class ~.Task --testAutomatically 
field string --fieldName title --notNull
field boolean --fieldName done 
controller all --package ~.web
perform tests
perform eclipse
```

Then I re-factored out the AspectJ stuff from the Task and created a new class called TaskRespository as follows:

```
package org.cdisource.springapp;

import java.util.List;

import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;

@Repository
@Transactional
public class TaskRepository {
	
    @PersistenceContext
    private EntityManager entityManager;

    
    public void persist(Task task) {
        this.entityManager.persist(task);
    }
    
    public void remove(Task task) {
        if (this.entityManager.contains(task)) {
            this.entityManager.remove(task);
        } else {
            Task attached = this.findTask(task.getId());
            this.entityManager.remove(attached);
        }
    }
    
    public void flush() {
        this.entityManager.flush();
    }
    
    public void clear() {
        this.entityManager.clear();
    }
    
    public Task merge(Task task) {
        Task merged = this.entityManager.merge(task);
        this.entityManager.flush();
        return merged;
    }
        
    public  long countTasks() {
        return entityManager.createQuery("select count(o) from Task o", Long.class).getSingleResult();
    }
    
    public  List<Task> findAllTasks() {
        return entityManager.createQuery("select o from Task o", Task.class).getResultList();
    }
    
    public  Task findTask(Long id) {
        if (id == null) return null;
        return entityManager.find(Task.class, id);
    }
    
    public  List<Task> findTaskEntries(int firstResult, int maxResults) {
        return entityManager.createQuery("select o from Task o", Task.class).setFirstResult(firstResult).setMaxResults(maxResults).getResultList();
    }

}

```


I then changed the Controller (also pushing in the AspectJ stuff into the actual controller) to use the new TaskRepository as follows:

```
package org.cdisource.springapp.web;

import java.io.UnsupportedEncodingException;
import java.util.Collection;

import javax.servlet.http.HttpServletRequest;
import javax.validation.Valid;

import org.cdisource.springapp.Task;
import org.cdisource.springapp.TaskRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.util.UriUtils;
import org.springframework.web.util.WebUtils;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;

@RequestMapping("/tasks")
@Controller
public class TaskController {

	@Autowired
	TaskRepository repo;

	@RequestMapping(method = RequestMethod.POST)
	public String create(@Valid Task task, BindingResult bindingResult,
			Model uiModel, HttpServletRequest httpServletRequest) {

		if (bindingResult.hasErrors()) {
			uiModel.addAttribute("task", task);
			return "tasks/create";
		}

		System.out.println("HERE 1");
		uiModel.asMap().clear();
		System.out.println("HERE 2");
		task = repo.merge(task);
		System.out.println("HERE 3");

		return "redirect:/tasks/"
				+ encodeUrlPathSegment(task.getId().toString(),
						httpServletRequest);

	}

	@RequestMapping(params = "form", method = RequestMethod.GET)
	public String createForm(Model uiModel) {
		uiModel.addAttribute("task", new Task());
		return "tasks/create";
	}

	@RequestMapping(value = "/{id}", method = RequestMethod.GET)
	public String show(@PathVariable("id") Long id, Model uiModel) {
		uiModel.addAttribute("task", repo.findTask(id));
		uiModel.addAttribute("itemId", id);
		return "tasks/show";
	}

	@RequestMapping(method = RequestMethod.GET)
	public String list(
			@RequestParam(value = "page", required = false) Integer page,
			@RequestParam(value = "size", required = false) Integer size,
			Model uiModel) {
		if (page != null || size != null) {
			int sizeNo = size == null ? 10 : size.intValue();
			uiModel.addAttribute("tasks", repo.findTaskEntries(page == null ? 0
					: (page.intValue() - 1) * sizeNo, sizeNo));
			float nrOfPages = (float) repo.countTasks() / sizeNo;
			uiModel.addAttribute(
					"maxPages",
					(int) ((nrOfPages > (int) nrOfPages || nrOfPages == 0.0) ? nrOfPages + 1
							: nrOfPages));
		} else {
			uiModel.addAttribute("tasks", repo.findAllTasks());
		}
		return "tasks/list";
	}

	@RequestMapping(method = RequestMethod.PUT)
	public String update(@Valid Task task, BindingResult bindingResult,
			Model uiModel, HttpServletRequest httpServletRequest) {
		if (bindingResult.hasErrors()) {
			uiModel.addAttribute("task", task);
			return "tasks/update";
		}
		uiModel.asMap().clear();
		repo.merge(task);
		return "redirect:/tasks/"
				+ encodeUrlPathSegment(task.getId().toString(),
						httpServletRequest);
	}

	@RequestMapping(value = "/{id}", params = "form", method = RequestMethod.GET)
	public String updateForm(@PathVariable("id") Long id, Model uiModel) {
		uiModel.addAttribute("task", repo.findTask(id));
		return "tasks/update";
	}

	@RequestMapping(value = "/{id}", method = RequestMethod.DELETE)
	public String delete(@PathVariable("id") Long id,
			@RequestParam(value = "page", required = false) Integer page,
			@RequestParam(value = "size", required = false) Integer size,
			Model uiModel) {
		repo.remove(repo.findTask(id));
		uiModel.asMap().clear();
		uiModel.addAttribute("page", (page == null) ? "1" : page.toString());
		uiModel.addAttribute("size", (size == null) ? "10" : size.toString());
		return "redirect:/tasks";
	}

	@ModelAttribute("tasks")
	public Collection<Task> populateTasks() {
		return repo.findAllTasks();
	}

	String encodeUrlPathSegment(String pathSegment,
			HttpServletRequest httpServletRequest) {
		String enc = httpServletRequest.getCharacterEncoding();
		if (enc == null) {
			enc = WebUtils.DEFAULT_CHARACTER_ENCODING;
		}
		try {
			pathSegment = UriUtils.encodePathSegment(pathSegment, enc);
		} catch (UnsupportedEncodingException uee) {
		}
		return pathSegment;
	}
}

```

Here is the re-factored Task class with the JPA stuff pushed in:

```
package org.cdisource.springapp;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Version;
import javax.validation.constraints.NotNull;
import org.springframework.beans.factory.annotation.Configurable;

@Configurable
@Entity
public class Task {

    @NotNull
    private String title;

    private Boolean done;
    
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    @Column(name = "id")
    private Long id;
    
    @Version
    @Column(name = "version")
    private Integer version;

    
    public String getTitle() {
        return this.title;
    }
    
    public void setTitle(String title) {
        this.title = title;
    }
    
    public Boolean getDone() {
        return this.done;
    }
    
    public void setDone(Boolean done) {
        this.done = done;
    }
    
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append("Title: ").append(getTitle()).append(", ");
        sb.append("Done: ").append(getDone());
        return sb.toString();
    }

    
    public Long getId() {
        return this.id;
    }
    
    public void setId(Long id) {
        this.id = id;
    }
    
    public Integer getVersion() {
        return this.version;
    }
    
    public void setVersion(Integer version) {
        this.version = version;
    }
}

```


At this point the webapp runs. You can create tasks and list them.

I also wrote a simplified unit test for the TaskRepository:

```
package org.cdisource.springapp;


import static org.junit.Assert.assertEquals;

import java.util.List;

import org.cdisource.testing.junit.CdiTestRunner;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Configurable;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.transaction.annotation.Transactional;
import org.junit.runner.RunWith;



@Configurable
@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(locations = "classpath:/META-INF/spring/testApplicationContext.xml")
@Transactional
public class TaskRepositoryTest {

	@Autowired
	private TaskRepository taskRepository;

	@Test
    public void testCrud() {
		Task task = new Task();
		task.setDone(true);
		task.setTitle("love rockets");
		taskRepository.persist(task);
		taskRepository.flush();
		List<Task> findAllTasks = taskRepository.findAllTasks();
		assertEquals(1, findAllTasks.size());
		taskRepository.remove(task);
		taskRepository.flush();
		List<Task> findAllTasks2 = taskRepository.findAllTasks();
		assertEquals(0, findAllTasks2.size());
    }

}

```


## Using CDI for the TaskRepository instead of Spring ##

I added these to the pom.xml

#### {projecthome}/pom.xml ####
```
...
	<repositories>
        ...
        <repository>
            <id>caucho.maven.repo</id>
            <name>Caucho Repository</name>
            <url>http://caucho.com/m2</url>
        </repository>
        <repository>
            <id>caucho.maven.repo.snapshot</id>
            <name>Caucho Repository</name>
            <url>http://caucho.com/m2-snapshot</url>
        </repository>
        <repository>
			<id>java.net</id>
			<name>java.net Repository</name>
			<url>http://download.java.net/maven/2</url>
		</repository>
    </repositories>
...

	<dependencies>
	
		<dependency>
            <groupId>org.cdisource.beancontainer</groupId>
    		<artifactId>beancontainer-api</artifactId>
    		<version>1.0-SNAPSHOT</version>
		</dependency>

		<dependency>
            <groupId>org.cdisource.beancontainer</groupId>
    		<artifactId>beancontainer-resin-impl</artifactId>
    		<version>1.0-SNAPSHOT</version>
    		<scope>test</scope>
		</dependency>
        <dependency>
        	<groupId>org.cdisource.testing</groupId>
			<artifactId>cdisource-testing-junit</artifactId>
			<version>1.0-SNAPSHOT</version>
        	<scope>test</scope>
        </dependency>
...
```


The beancontainer-resin-impl is not needed at this point.
I was using it in a failed attempt to add a unit test for the new TaskRepository.

The next step is to CDIify the TaskRespository as follows:

```
package org.cdisource.springapp;

import java.util.List;
import javax.ejb.Stateless;
import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;

@Stateless
public class TaskRepository {
	
    @PersistenceContext
    private EntityManager entityManager;

    
    public void persist(Task task) {
        this.entityManager.persist(task);
    }
    
    public void remove(Task task) {
        if (this.entityManager.contains(task)) {
            this.entityManager.remove(task);
        } else {
            Task attached = this.findTask(task.getId());
            this.entityManager.remove(attached);
        }
    }
    
    public void flush() {
        this.entityManager.flush();
    }
    
    public void clear() {
        this.entityManager.clear();
    }
    
    public Task merge(Task task) {
        Task merged = this.entityManager.merge(task);
        this.entityManager.flush();
        return merged;
    }
        
    public  long countTasks() {
        return entityManager.createQuery("select count(o) from Task o", Long.class).getSingleResult();
    }
    
    public  List<Task> findAllTasks() {
        return entityManager.createQuery("select o from Task o", Task.class).getResultList();
    }
    
    public  Task findTask(Long id) {
        if (id == null) return null;
        return entityManager.find(Task.class, id);
    }
    
    public  List<Task> findTaskEntries(int firstResult, int maxResults) {
        return entityManager.createQuery("select o from Task o", Task.class).setFirstResult(firstResult).setMaxResults(maxResults).getResultList();
    }

}

```

Notice the removal of the Spring annotations and the addition of the CDI annotation.
There is only three lines of code difference.

Then to make this bean recognizable by Spring I added the following:

```

package org.cdisource.springapp;

import javax.enterprise.inject.spi.BeanManager;
import javax.naming.InitialContext;

import org.springframework.beans.factory.FactoryBean;
import org.cdisource.beancontainer.BeanContainer;
import org.cdisource.beancontainer.BeanContainerImpl;
import org.cdisource.beancontainer.BeanContainerInitializationException;

public class TaskRepositoryFactoryBean implements FactoryBean<TaskRepository> {

	private BeanContainer beanContainer = null;
	private final String BEAN_MANAGER_LOCATION = "java:comp/BeanManager";

	
	@Override
	public TaskRepository getObject() throws Exception {

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

Note that I added a new constructor to the BeanContainerImpl to make the above possible.

```
package org.cdisource.beancontainer;

import javax.enterprise.inject.spi.BeanManager;
import javax.inject.Inject;

public class BeanContainerImpl extends AbstractBeanContainer {
    @Inject protected BeanManager manager;
    
    public BeanContainerImpl() {
    	
    }
    
    public BeanContainerImpl(BeanManager manager) {
    	this.manager = manager;
    }

...
}

```

I thought I had the webapp working at this point, but then realized that I was deploying old classes. I had to go back and rework things a few times to get things going.
At this point, the webapp almost works.

I change the persistence.xml as follows:

```
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<persistence xmlns="http://java.sun.com/xml/ns/persistence" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="2.0" xsi:schemaLocation="http://java.sun.com/xml/ns/persistence http://java.sun.com/xml/ns/persistence/persistence_2_0.xsd">
<persistence-unit name="persistenceUnit" >
		<!--  transaction-type="RESOURCE_LOCAL" Took this out. We are managing this in CDI not local.-->
        <provider>org.hibernate.ejb.HibernatePersistence</provider>
        <jta-data-source>jdbc/basic</jta-data-source>
        <properties>
            <property name="hibernate.dialect" value="org.hibernate.dialect.HSQLDialect"/>
            <property name="hibernate.hbm2ddl.auto" value="create"/>
            <property name="hibernate.ejb.naming_strategy" value="org.hibernate.cfg.ImprovedNamingStrategy"/>
            <property name="hibernate.connection.charSet" value="UTF-8"/>
        </properties>
    </persistence-unit>
</persistence>

```


I then had to disable Spring transaction support/JPA support in the web.xml and in the applicationContext.xml.

First in the web.xml as follows:

**web.xml**
```
    <!-- Commented this out to get it to work with CDI
    <filter>
        <filter-name>Spring OpenEntityManagerInViewFilter</filter-name>
        <filter-class>org.springframework.orm.jpa.support.OpenEntityManagerInViewFilter</filter-class>
    </filter>
     -->
    <filter-mapping>
        <filter-name>CharacterEncodingFilter</filter-name>
        <url-pattern>/*</url-pattern>
    </filter-mapping>
    
    <filter-mapping>
        <filter-name>HttpMethodFilter</filter-name>
        <url-pattern>/*</url-pattern>
    </filter-mapping>
    
    <!-- Commented this out to get it to work with CDI
    <filter-mapping>
        <filter-name>Spring OpenEntityManagerInViewFilter</filter-name>
        <url-pattern>/*</url-pattern>
    </filter-mapping>
    -->
```

**applicationContext.xml**
```
    <context:spring-configured/>
    <context:component-scan base-package="org.cdisource.springapp">
        <context:exclude-filter expression="org.springframework.stereotype.Controller" type="annotation"/>
    </context:component-scan>


    <!-- 
    
    Spring is no longer managing the transactions.

    <bean class="org.springframework.orm.jpa.JpaTransactionManager" id="transactionManager">
        <property name="entityManagerFactory" ref="entityManagerFactory"/>
    </bean>
    
    <tx:annotation-driven mode="aspectj" transaction-manager="transactionManager"/>
     
    <jee:jndi-lookup id="dataSource" jndi-name="jdbc/basic"/>
    <bean class="org.springframework.orm.jpa.LocalContainerEntityManagerFactoryBean" id="entityManagerFactory">
        <property name="dataSource" ref="dataSource"/>
    </bean>
    
         -->
    
    
    <bean class="org.cdisource.springapp.TaskRepositoryFactoryBean" name="taskRespository"/>

```

I had some troubles getting the unit test to work. The web app does work.

The unit test is as follows:

```
package org.cdisource.springapp;


import static org.junit.Assert.assertEquals;

import java.util.List;

import javax.inject.Inject;

import org.cdisource.testing.junit.CdiTestRunner;
import org.junit.Test;
import org.junit.runner.RunWith;



@RunWith(CdiTestRunner.class)
public class TaskRepositoryTest {

	@Inject
	private TaskRepository taskRepository;

	@Test
    public void testCrud() {
		Task task = new Task();
		task.setDone(true);
		task.setTitle("love rockets");
		taskRepository.persist(task);
		taskRepository.flush();
		List<Task> findAllTasks = taskRepository.findAllTasks();
		assertEquals(1, findAllTasks.size());
		taskRepository.remove(task);
		taskRepository.flush();
		List<Task> findAllTasks2 = taskRepository.findAllTasks();
		assertEquals(0, findAllTasks2.size());
    }

}

```
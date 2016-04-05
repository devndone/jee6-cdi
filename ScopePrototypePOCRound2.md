Change... next version we are going to use
javax.enterprise.inject.spi


Interface BeforeBeanDiscovery
void	addScope(java.lang.Class<? extends java.lang.annotation.Annotation> scopeType, boolean normal, boolean passivating)

to install our scopes...

Although we still might need a mechanism for installing scopes for unit testing.


# Scope Prototype POC Round2 #

I am taking another swing at this after reading Andy's email on the subject and sensing his displeasure. :)

Look, the last one was just a POC....

(All code listings are from working POC code...)


So I want to write code that looks like this:

**AtmMain.java**
```
        startScope(threadLocalScope);

        User beanByType = beanContainer.getBeanByType(User.class);

        System.out.println("classname" + beanByType.getClass().getName());

        stopScope(threadLocalScope);

```

I have added the following concepts:
  * ScopeController stops/starts a scope
  * ScopeManager manages ScopeControllers, delegates to them for stop start. Allows us to have a fluent API.

We need ScopeManagers. I am calling them ScopeControllers since the ScopeManager is going to manage all things scope realted.

I think the interface for a Scope controller should look something like this:

**ScopeController.java**
```
package org.cdisource.beancontainer;

public interface ScopeController {
	public void stop();
	public void start();
}

```

You can do two things with a scope. You can start it. You can stop. That is it. Thoughts?

So taking a look at the example scope which I wrote (by looking at a similar concept in Resin CANDI, Open Source stuff).

Here is the implementation of a ThreadLocalScope (just an example to try out our scope mgmt):

**ThreadLocalControl.java ThreadLocalContext.java ThreadLocalScoped.java**
```
//SAME AS BEFORE
package org.cdi.advocacy.scope;

import java.lang.annotation.Annotation;
import java.util.HashMap;

import javax.enterprise.context.spi.Context;
import javax.enterprise.context.spi.Contextual;
import javax.enterprise.context.spi.CreationalContext;

public class ThreadLocalContext implements Context {
	@SuppressWarnings("unchecked")
	@Override
	public <T> T get(Contextual<T> bean) {
		HashMap<Contextual<?>, Object> map = ThreadLocalContextControl.tlvMap.get();

		if (map == null)
			throw new IllegalStateException("Thread local scope not active");
		return (T) map.get(bean);
	}

	@Override
	public <T> T get(Contextual<T> bean, CreationalContext<T> env) {
		HashMap<Contextual<?>, Object> map = ThreadLocalContextControl.tlvMap.get();

		if (map == null)
			throw new IllegalStateException("Thread local scope not active");

		@SuppressWarnings("unchecked")
		T instance = (T) map.get(bean);

		if (instance == null) {
			instance = bean.create(env);

			map.put(bean, instance);
		}

		return instance;
	}

	@Override
	public Class<? extends Annotation> getScope() {
		return ThreadLocalScoped.class;
	}

	@Override
	public boolean isActive() {
		return ThreadLocalContextControl.tlvMap.get() != null;
	}
}

//NEW NEW NEW
package org.cdi.advocacy.scope;

import java.util.HashMap;

import javax.enterprise.context.spi.Context;
import javax.enterprise.context.spi.Contextual;

import org.cdisource.beancontainer.ScopeController;

/**
NOTICE THAT THIS BAD BOY IMPLEMENTS THE SCOPE CONTROLLER
 */
public class ThreadLocalContextControl implements ScopeController{

	static final ThreadLocal<HashMap<Contextual<?>, Object>> tlvMap = new ThreadLocal<HashMap<Contextual<?>, Object>>();

	private static ThreadLocalContext _context = new ThreadLocalContext();

	public void start() {
		System.out.println("START");
		if (tlvMap.get() != null)
			throw new IllegalStateException("ThreadLocalContext begin()::already present");

		HashMap<Contextual<?>, Object> map = new HashMap<Contextual<?>, Object>(7);

		tlvMap.set(map);
	}

	public void stop() {
		System.out.println("STOP");
		if (tlvMap.get() == null)
			throw new IllegalStateException("ThreadLocalContext end()::needs start");

		tlvMap.set(null);
	}

	public static Context getContext() {
		return _context;
	}
}

//SAME AS BEFORE
package org.cdi.advocacy.scope;

import static java.lang.annotation.ElementType.METHOD;
import static java.lang.annotation.ElementType.TYPE;
import static java.lang.annotation.RetentionPolicy.RUNTIME;

import java.lang.annotation.Retention;
import java.lang.annotation.Target;

import javax.enterprise.context.NormalScope;
import javax.inject.Scope;

@Scope
@NormalScope
@Target({TYPE, METHOD})
@Retention(RUNTIME)
public @interface ThreadLocalScoped {
}

```

Ok... So how did I make this code happen...

```
        startScope(threadLocalScope);

        User beanByType = beanContainer.getBeanByType(User.class);

        System.out.println("classname" + beanByType.getClass().getName());

        stopScope(threadLocalScope);

```

Well the startScope and stopScope are static imports
```
import org.cdisource.beancontainer.ScopeManager;

import static org.cdisource.beancontainer.ScopeManager.startScope;
import static org.cdisource.beancontainer.ScopeManager.stopScope;

```

The ScopeManager is the [magic secret sauce](http://www.youtube.com/watch?v=b2F-DItXtZs&feature=player_embedded) that ties up the fluent API (startScope, stopScope), with the ScopeControllers.

**ScopeManager.java**
```
package org.cdisource.beancontainer;

import java.lang.annotation.Annotation;
import java.util.HashMap;
import java.util.Map;

import javax.enterprise.context.spi.Context;

public class ScopeManager {
	private static ScopeManager instance = new ScopeManager();
	
	private Map<Class<? extends Annotation>, ScopeController> map = new HashMap<Class<? extends Annotation>, ScopeController>(7);

	public void stop(Class<? extends Annotation> scopeType) {
		ScopeController control = map.get(scopeType);
		if (control!=null) {
			control.stop();
		}
	}
	public static void startScope(Class<? extends Annotation> scopeType) {
		instance.start(scopeType);
	}
	public static void stopScope(Class<? extends Annotation> scopeType) {
		instance.stop(scopeType);
	}

	
	public void start(Class<? extends Annotation> scopeType) {
		ScopeController control = map.get(scopeType);
		if (control!=null) {
			control.start();
		}
	}
	
	public void register(ScopeController control, Context context) {
		BeanContainerManager.getInstance().registerContext(context, true);
		map.put(context.getScope(), control);
	}

	public static ScopeManager getInstance() {
		return instance;
	}
        /* Once we add lifecycle support, this could get called when/if the container restarts. */
	public static void reset() {
		instance.map.clear();
		instance = new ScopeManager();
	}

}

```

(code needs to be hardened and add logging, etc.)

Here is the rest of the AtmMain class....

**AtmMain**
```
package org.cdi.advocacy;

import java.lang.annotation.Annotation;
import java.math.BigDecimal;


import org.cdisource.beancontainer.BeanContainer;
import org.cdisource.beancontainer.BeanContainerManager;
import org.cdisource.beancontainer.ScopeManager;
import static org.cdisource.beancontainer.ScopeManager.startScope;
import static org.cdisource.beancontainer.ScopeManager.stopScope;

//Sample custom scope
import org.cdi.advocacy.scope.ThreadLocalContext;
import org.cdi.advocacy.scope.ThreadLocalContextControl;
import org.cdi.advocacy.scope.ThreadLocalScoped;


public class AtmMain {


    public static BeanContainer beanContainer = BeanContainerManager
            .getInstance();

    public static void main(String[] args) throws Exception {
        
        //Some hidden code somewhere in the guts of our stuff.
        ScopeManager.getInstance().register(new ThreadLocalContextControl(), new ThreadLocalContext());
        Class<? extends Annotation> threadLocalScope = ThreadLocalScoped.class;

       //actually use the scope        
        startScope(threadLocalScope);
        User beanByType = beanContainer.getBeanByType(User.class);
        System.out.println("classname" + beanByType.getClass().getName());
        stopScope(threadLocalScope);

    }

}

```
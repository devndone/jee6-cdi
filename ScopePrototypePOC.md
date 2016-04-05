# Introduction DEPRECATED INTERNAL DESIGN NOTE #

Quit looking at me. There is nothing to see here. Go away. :)

[ScopePrototypePOCRound2](ScopePrototypePOCRound2.md)

The problem is that there is not one way to manage scopes.

We need a common way to handle scopes with the beancontainer.

Code taken from working example/proof of concept.

We could add a new method to the BeanContainer interface like so:

```
public interface BeanContainer {
	
	public void registerContext(Context context, boolean replace);

...
}
```

For impl that don't support it (not sure if there are any that don't), we would add code like this:

```
public class WeldBeanContainer extends AbstractBeanContainer {
        ...
	@Override
	public void registerContext(Context context, boolean replace) {
		throw new UnsupportedOperationException("TODO");
	}

```

BTW Weld probably supports this fine. We just need to figure out how to do this with OWB and Weld.
My POC works with Resin.

Here is the impl in Resin of the registerContext method.

```

public class ResinBeanContainer extends AbstractBeanContainer {
       ...
	@Override
	public void registerContext(Context context, boolean replace) {
		if (replace) {
			delegate.getCdiManager().replaceContext(context);
		} else {
			delegate.getCdiManager().addContext(context);
		}
	}

```

I tested this out and it works.
I wrote the following context classes for a TLV (after looking at similar code else where).

**ThreadLocalScoped annotation**
```
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

**ThreadLocalContext**
```
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
		HashMap<Contextual<?>, Object> map = ThreadLocalContextManager.tlvMap.get();

		if (map == null)
			throw new IllegalStateException("Thread local scope not active");
		return (T) map.get(bean);
	}

	@Override
	public <T> T get(Contextual<T> bean, CreationalContext<T> env) {
		HashMap<Contextual<?>, Object> map = ThreadLocalContextManager.tlvMap.get();

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
		return ThreadLocalContextManager.tlvMap.get() != null;
	}
}
```

**ThreadLocalContextManager**
```
package org.cdi.advocacy.scope;

import java.util.HashMap;

import javax.enterprise.context.spi.Context;
import javax.enterprise.context.spi.Contextual;

/**
 * The ThreadContext works with @ThreadScoped.
 */
public class ThreadLocalContextManager {

	static final ThreadLocal<HashMap<Contextual<?>, Object>> tlvMap = new ThreadLocal<HashMap<Contextual<?>, Object>>();

	private static ThreadLocalContext _context = new ThreadLocalContext();

	public static void start() {
		if (tlvMap.get() != null)
			throw new IllegalStateException("ThreadLocalContext begin()::already present");

		HashMap<Contextual<?>, Object> map = new HashMap<Contextual<?>, Object>(7);

		tlvMap.set(map);
	}

	public static void end() {
		if (tlvMap.get() == null)
			throw new IllegalStateException("ThreadLocalContext end()::needs start");

		tlvMap.set(null);
	}

	public static Context getContext() {
		return _context;
	}
}

```

ThreadLocalContextManager really wants to implement a common interface and be a class, but this is a POC for now.

Then to use this we would just do this:

**Usage**
```
        
        ThreadLocalContext threadContext = new ThreadLocalContext();
        beanContainer.registerContext(threadContext, true);
        
        ThreadLocalContextManager.start();
        User beanByType = beanContainer.getBeanByType(User.class);
        System.out.println("classname" + beanByType.getClass().getName());
        ThreadLocalContextManager.end();

```

**Output**
```
deposit called
communicating with bank via JSON REST transport retries=0
classnameorg.cdi.advocacy.User__ResinScopeProxy

```

Now RW just need to see if we can do this for OWB and AG for Weld and then we are off to the races.
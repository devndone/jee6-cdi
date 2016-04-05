ThreadLocal**same as before.**

**Change to Scope Manager**
```
	public void register(ScopeController control, Context context) {
		BeanContainerManager.getInstance().registerContext(context, true);
		map.put(context.getScope(), control);
	}

	public void register(AfterBeanDiscovery abd, ScopeController control, Context context) {
		abd.addContext(context);
		map.put(context.getScope(), control);
	}
```

Above.. Added a second register method.

To example project added an Extension so I could add contexts.

**Code in same project as AtmMain**
```
package org.cdi.advocacy;

import javax.enterprise.event.Observes;
import javax.enterprise.inject.spi.AfterBeanDiscovery;
import javax.enterprise.inject.spi.BeforeBeanDiscovery;
import javax.enterprise.inject.spi.Extension;
import javax.enterprise.inject.spi.ProcessAnnotatedType;

import org.cdi.advocacy.scope.ThreadLocalContext;
import org.cdi.advocacy.scope.ThreadLocalContextControl;
import org.cdi.advocacy.scope.ThreadLocalScoped;
import org.cdisource.beancontainer.ScopeManager;

public class ThreadLocalExtention implements Extension {

	void beforeBeanDiscovery(@Observes BeforeBeanDiscovery bbd) {
		bbd.addScope(ThreadLocalScoped.class, true, true);
	}
	
	
	void afterBeanDiscovery( @Observes AfterBeanDiscovery abd) {
        ScopeManager.getInstance().register(abd, new ThreadLocalContextControl(), new ThreadLocalContext());
	}
}

```

The code above is in

This is similar to the code example Rob sent out. Too bad he did not send it out earlier. It would have saved me an hour or two. :)

I think to be fully CDI compliant you should register the scope in the before and then register the context in the after. The example Rob sent did not do this, but I "think" you should. I tried it with/without it works both ways with CANDI.

That is all. It seems like the context control really needs four methods: start, stop, attach and detach.

It also seems like we should research what the spec. says about Conversation scope.

The up side, I got to write my first CDI Extension.
The down side, still not 100% sure of the direction to go with how we handle scopes.
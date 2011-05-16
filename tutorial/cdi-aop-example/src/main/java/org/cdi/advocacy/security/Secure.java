package org.cdi.advocacy.security;

import java.lang.annotation.Retention;
import java.lang.annotation.Target;
import static java.lang.annotation.ElementType.*;
import static java.lang.annotation.RetentionPolicy.*;
import javax.interceptor.InterceptorBinding;


@InterceptorBinding 
@Retention(RUNTIME) @Target({TYPE, METHOD})
public @interface Secure {

}

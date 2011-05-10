package org.cdi.advocacy;

import java.util.logging.Logger;

import javax.enterprise.inject.Produces;
import javax.enterprise.inject.spi.InjectionPoint;

public class LogFactory {

        @Produces
        public Logger createLogger(InjectionPoint injectionPoint) {
            Class<?> beanClass = injectionPoint.getBean().getBeanClass();
            System.out.println(beanClass);
            System.out.println(beanClass.getName());
            return Logger.getLogger(beanClass.getName());
        }
}

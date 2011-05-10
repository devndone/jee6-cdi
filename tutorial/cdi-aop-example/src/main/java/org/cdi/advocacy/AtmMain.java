package org.cdi.advocacy;

import java.math.BigDecimal;

import org.cdi.advocacy.security.SecurityToken;
import org.cdiadvocate.beancontainer.BeanContainer;
import org.cdiadvocate.beancontainer.BeanContainerManager;
import org.cdi.advocacy.security.SecurityService;

public class AtmMain {

    public static void simulateLogin() {
        SecurityService.placeSecurityToken(new SecurityToken(true,
                "Rick Hightower"));
    }

    public static void simulateNoAccess() {
        SecurityService.placeSecurityToken(new SecurityToken(false,
                "Tricky Lowtower"));
    }

    public static BeanContainer beanContainer = BeanContainerManager
            .getInstance();
    static {
        beanContainer.start();
    }

    public static void main(String[] args) throws Exception {
        simulateLogin();
        //simulateNoAccess();

        AutomatedTellerMachine atm = beanContainer
                .getBeanByType(AutomatedTellerMachine.class);
        atm.deposit(new BigDecimal("1.00"));
    }

}

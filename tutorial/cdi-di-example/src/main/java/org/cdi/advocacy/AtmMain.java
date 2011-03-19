package org.cdi.advocacy;

import java.math.BigDecimal;

import org.cdiadvocate.beancontainer.BeanContainer;
import org.cdiadvocate.beancontainer.BeanContainerManager;


public class AtmMain {

	static BeanContainer beanContainer =  BeanContainerManager.getInstance();
	static { beanContainer.start(); }

	public static void main(String[] args) throws Exception {
		AutomatedTellerMachine atm = (AutomatedTellerMachine) beanContainer
				.getBeanByName("atm");

		//AutomatedTellerMachine atm = beanContainer.getBeanByType(AutomatedTellerMachine.class);
		atm.deposit(new BigDecimal("1.00"));

	}

}

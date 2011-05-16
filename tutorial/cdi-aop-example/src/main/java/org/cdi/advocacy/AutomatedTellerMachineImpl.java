package org.cdi.advocacy;

import java.math.BigDecimal;

import javax.inject.Inject;

import org.cdi.advocacy.security.Secure;

@Secure
public class AutomatedTellerMachineImpl implements AutomatedTellerMachine {

    @Inject
    @Json
    private ATMTransport transport;

    @Logable @Debugable   
    public void deposit(BigDecimal bd) {
        System.out.println("deposit called");
        transport.communicateWithBank(null);

    }

    public void withdraw(BigDecimal bd) {
        System.out.println("withdraw called");

        transport.communicateWithBank(null);

    }

}

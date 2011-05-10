package org.cdi.advocacy;

public class StandardAtmTransport implements ATMTransport {
	
	private int retries;

	public void setRetries(int retries) {
		this.retries = retries;
	}


	public void communicateWithBank(byte[] datapacket) {
		System.out.println("communicating with bank via Standard transport retries=" + retries);
	}

}

package org.candi.examples.login;

import java.util.List;

import javax.ejb.TransactionAttribute;
import javax.ejb.TransactionAttributeType;
import javax.enterprise.context.RequestScoped;
import javax.enterprise.inject.Produces;
import javax.inject.Named;
import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;

public class Users {

	@PersistenceContext
	private EntityManager userDatabase;

	@SuppressWarnings("unchecked")
	@Produces
	@Named
	@RequestScoped
	@TransactionAttribute (TransactionAttributeType.REQUIRED)
	public List<User> getUsers() {

		List<User> users = userDatabase.createQuery("select u from User u")
				.getResultList();

		for (User user : users) {
			System.out.println("getUsers:" + user.getName());
		}

		if (users.size() == 0) {
			
			User user = new User();
			user.setUsername("demo");
			user.setName("demo");
			user.setPassword("demo");
			
			userDatabase.persist(user);
			
		}
		return users;
	}

}

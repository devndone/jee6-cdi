package org.candi.examples.login;

import java.io.Serializable;

import javax.persistence.Entity;
import javax.persistence.Id;

@Entity
public class User implements Serializable
{
 	private static final long serialVersionUID = 1L;
 
   @Id
   private String username;
   private String name;
   private String password;
   
   public User() {}

   public String getUsername()
   {
      return username;
   }
   
   public void setName(String name)
   {
      this.name = name;
   }
   
   public void setUsername(String username)
   {
      this.username = username;
   }

   public String getName()
   {
      return name == null ? username : name;
   }

   public void setPassword(String password)
   {
      this.password = password;
   }
   
   public String getPassword()
   {
      return password;
   }

}

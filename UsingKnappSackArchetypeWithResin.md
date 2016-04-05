I wrote my own Resin Maven plugin which is at:

```
https://github.com/CDISource/maven-resin-plugin
```

You can clone the repo and mvn clean install it.

```
$ git clone git@github.com:CDISource/maven-resin-plugin.git
$ cd cd resin-maven-plugin/cdisource-maven-resin-plugin/
$ mvn clean install
```

Right now it is more a labor of love than project I can devot too many cycles too.
It does work. It will download, install and configure Resin (4.0.17 at the moment).

<p>
Resin has long been my app server of choice although I have used WebSphere, WebLogic, Tomcat, Jetty and JBoss.<br>
Resin was the second application server that I used.<br>
It was the first application server that I used to actually launch production code.<br>
</p>

<p>
These are the steps to run the Knappsack archetype developed by the estemed Andy Gibson on Resin.<br>
</p>

<p>
His Archetype is in the maven public repo so to use it, you could do the following:<br>
</p>

**~/examples**
```
$ pwd
/home/rick/examples
$ mvn archetype:generate -DarchetypeGroupId=org.fluttercode.knappsack -DarchetypeArtifactId=jee6-sandbox-demo-archetype -DinteractiveMode=false -DarchetypeVersion=1.1 -DgroupId=org.cdisource.examples.taskcrud -DartifactId=taskcrud -Dpackage=org.cdisource.examples.taskcrud
```

After this, logically, you might want to run it as follows (using the above Resin maven plugin):

```
 [java] [11-04-19 12:20:31.550] {http://*:8080-1} 'java:/DefaultDS' is an unknown or unconfigured JDBC DataSource.
```

Add this file to src/main/webapp/WEB-INF

**resin-web.xml**
```
<web-app xmlns="http://caucho.com/ns/resin">


<database jndi-name='jdbc/basic'>
  <driver type="org.hsqldb.jdbcDriver">
    <url>jdbc:hsqldb:db/hypersonic/localDB</url>
    <user>sa</user>
    <password></password>
  </driver>
</database>
</web-app>

```

Modify the persistence.xml file remove the jta-data-source that was configure and replace it with this:

**src/main/resources/persistence.xml**
```

<jta-data-source>jdbc/basic</jta-data-source>

```

Add this to the pom.xml (or you could drop the jar into $resin\_home/webapp\_jars:

```
<dependencies>
...
		<dependency>
			<groupId>org.hsqldb</groupId>
			<artifactId>hsqldb</artifactId>
			<version>1.8.0.10</version>
		</dependency>
...
```

JBoss ships with hsqldb, Resin does not.


  * http://bugs.caucho.com/view.php?id=4513
  * http://bugs.caucho.com/view.php?id=4514
  * http://bugs.caucho.com/view.php?id=4515


To get past
http://bugs.caucho.com/view.php?id=4513
I did this

```


@Local
public interface SchoolDao {
     //public <T extends BaseEntity> T save(T entity); //was something like this
	
     //changed to something like this
    public BaseEntity save(BaseEntity entity);
    public void refresh(BaseEntity entity);


//
public class SchoolJpaDao implements SchoolDao {

        ...
	@Override
	public BaseEntity save(BaseEntity entity) {
		return entityManager.merge(entity);
	}

	@Override
	public void refresh(BaseEntity entity) {
		if (entityManager.contains(entity)) {
			entityManager.refresh(entity);
		}
	}
```


Then I ran into some EclipseLink issues:

**persistence.xml**
```
			<!-- Properties for EclipseLink (default provider for GlassFish) 
			<property name="eclipselink.ddl-generation" value="drop-and-create-tables" />
			<property name="eclipselink.logging.level" value="FINE" />
                          Got rid of this
			-->

                        <!-- Added this -->
			<property name="eclipselink.target-database" value="HSQL" />
			<property name="eclipselink.ddl-generation" value="create-tables" />
			<property name="eclipselink.ddl-generation.output-mode"
				value="database" />				
			<property name="eclipselink.weaving" value="false" />
			<property name="eclipselink.logging.level" value="FINEST" />

```


Fix for
**http://bugs.caucho.com/view.php?id=4515*
```

@Named("courseHome")
@ConversationScoped
public class CourseHome implements Serializable {

	public void init(boolean beginConversation) {
		if (id == null) {
			ViewUtil.redirect("home.jsf");
		}

		if (beginConversation && conversation.isTransient()) {
			conversation.begin();
		}
	}

	/**
           Added this
	 */
	public void init() {
		this.init(false);
	}

```**

I changed **courseView.html** as follows;

```
	<ui:define name="content">
		<f:metadata>
			<f:viewParam name="courseId" value="#{courseHome.id}" />
			<f:event type="preRenderView" listener="#{courseHome.init}" />
		</f:metadata>
		<h:form>


```
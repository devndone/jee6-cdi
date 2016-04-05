# Introduction #

This page is to support our [Dependency Injection Tutorial](DependencyInjectionAnIntroductoryTutorial.md).

# Support #
We do want to support you. If you need help running the example, please contact us on the
[CDI Avocate google group](http://groups.google.com/group/cdiadvocate4j).

# Prerequisites #

  * Subversion
    * We may later include a zip file if there is enough demand
  * Java 6 SDK
    * (you may be able to get it to work on earlier editions, but we are not going to test or support it)
  * Maven 3
    * (It has been out for a while, and there is no use of us supporting Maven 2)
    * We may include an ant script if there is enough demand. (Just add it to the list of issues or ask for it on the mailing list)
  * Eclipse (Any 3.x+ version should do)
    * (You can use other IDEs but this is the one we support. Helios Service Release 2)

# Short Video showing the steps #
[Short Video hosted on Vimeo](http://goo.gl/SLY58)

# Instructions #

Download the source code from google code, use mvn compile to pull down the dependencies, and then use mvn eclipse:eclipse to generate the .project and .classpath file for Eclipse.

```

$ svn co http://jee6-cdi.googlecode.com/svn/tutorial/cdi-di-example cdi-di-example
$ cd cdi-di-example
$ mvn compile
$ mvn eclipse:eclipse
```

Open up Eclipse and import this project File->Import... General->Existing Projects Into Workspace. Navigate to the directory where cdi-di-example. Eclipse should find the project. Hit Finish.

If this is your first time using Eclipse with Maven then you need to setup the M2\_REPO classpath variable to point to ~/.m2/repository. To do this go to Eclipse Preferences (Window->Preferences on Windows and Linux and Eclipse->Preferences on Mac OS X). Then go to Java->Build Path->Classpath variables. Hit the New... button on the right hand side. Add a variable with the name M2\_REPO pointing to the .m2/repository in your home directory.

The example should be ready to run and you should have no compile errors in Eclipse.
Open up AtmMain and then select Run->Run. It should just work.

By default the example uses the Resin CDI container, to switch to Weld, edit the pom.xml file as follows:

**Weld support pom.xml**
```
<?xml version="1.0"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <groupId>org.cdiadvocate</groupId>
    <artifactId>cdi-di-tutorial</artifactId>
    <packaging>jar</packaging>
    <name>CDI Advocacy DI tutorial</name>
    <version>1.1.0-SNAPSHOT</version>


    <description>
        Source code for CDI DI tutorial. 
	See: http://code.google.com/p/jee6-cdi/wiki/DependencyInjectionAnIntroductoryTutorial
   </description>

    <dependencies>
        <dependency>
            <groupId>org.cdiadvocate</groupId>
            <artifactId>cdiadvocate-api</artifactId>
            <version>1.0-SNAPSHOT</version>
        </dependency>
        <dependency>
            <groupId>javax.validation</groupId>
            <artifactId>validation-api</artifactId>
            <version>1.0.0.GA</version>
        </dependency>
	<dependency> 
	   <groupId>org.cdiadvocate</groupId> 
	   <artifactId>cdiadvocate-weld-impl</artifactId> 
           <version>1.0-SNAPSHOT</version> 
	</dependency>
    </dependencies>

    <repositories>
        <repository>
            <id>cdi.advocate</id>
            <name>CDI Advocacy</name>
            <url>http://jee6-cdi.googlecode.com/svn/m2/repository/</url>
        </repository>
        <repository>
            <id>jboss.maven.repo</id>
            <name>JBoss Repository</name>
            <url>http://repository.jboss.org/nexus/content/groups/public-jboss/</url>
        </repository>
    </repositories>

</project>
```

**To switch back to Resin pom.xml**
```
<?xml version="1.0"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <groupId>org.cdiadvocate</groupId>
    <artifactId>cdi-di-tutorial</artifactId>
    <packaging>jar</packaging>
    <name>CDI Advocacy DI tutorial</name>
    <version>1.1.0-SNAPSHOT</version>


    <description>
        Source code for CDI DI tutorial. 
	See: http://code.google.com/p/jee6-cdi/wiki/DependencyInjectionAnIntroductoryTutorial
   </description>

    <dependencies>
        <dependency>
            <groupId>org.cdiadvocate</groupId>
            <artifactId>cdiadvocate-api</artifactId>
            <version>1.0-SNAPSHOT</version>
        </dependency>
        <dependency>
            <groupId>org.cdiadvocate</groupId>
            <artifactId>cdiadvocate-resin-impl</artifactId>
            <version>1.0-SNAPSHOT</version>
        </dependency>
        <dependency>
            <groupId>javax.validation</groupId>
            <artifactId>validation-api</artifactId>
            <version>1.0.0.GA</version>
        </dependency>
    </dependencies>

    <repositories>
        <repository>
            <id>cdi.advocate</id>
            <name>CDI Advocacy</name>
            <url>http://jee6-cdi.googlecode.com/svn/m2/repository/</url>
        </repository>
        <repository>
            <id>caucho.maven.repo</id>
            <name>Caucho Repository</name>
            <url>http://caucho.com/m2</url>
        </repository>
    </repositories>

</project>

```
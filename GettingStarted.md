# Welcome #

You may wonder why this site and project exists.
CDI is a great technology. CDI provides a standard way to do dependency injection and AOP.
CDI is part of JEE 6.

The aim of this project is to make the CDI examples easier to use so more people learn CDI.

## Problems with existing examples ##

However, the examples that ship with the JEE 6 tutorial are too tied NetBeans and Glassfish.
Conversly the samples from the Weld project do not build easily and depend on JBoss repositories.
Also the samples from the Weld project have very complex builds, which are great if you want to run the examples on many environments, but not so good if you just want to get something working.

## Examples should work with tools that developers use ##

We find that most developers use Eclipse, Ant and Maven.

We want to create a set of examples that just work.

Literally, you should be able to download our examples, import them into Eclipse Java EE IDE, right click the project, select "Run On Server...", and it just works.

If you are spending hours configuring, hunting and pecking than there is something wrong.

## Whenever possible we want to reuse what is out there ##
Whenever possible we want to reuse existing examples and point you to the documentation that is already out there. We just want to improve the builds so that you have some examples to get started with quickly.

## CDI and beyond ##

Also, there are ways to run CDI inside and outside of a container, we are going to highlight those ways as well.

## Here are some instructions to get you started quickly ##
[Using Maven or Eclipse Java EE IDE to run the Java EE CDI samples](http://goo.gl/yS7oD)

[Using Maven or Eclipse Java EE IDE to run the Java EE CDI samples PDF](http://goo.gl/PMR9j)

[Step by Step Tutorial and cookbook for DI and CDI](DependencyInjectionAnIntroductoryTutorial.md)
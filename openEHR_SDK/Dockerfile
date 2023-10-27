# Container to build https://github.com/ehrbase/openEHR_SDK
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y openjdk-17-jdk git wget

WORKDIR /opt/

RUN wget https://dlcdn.apache.org/maven/maven-3/3.8.8/binaries/apache-maven-3.8.8-bin.tar.gz

RUN tar -xvf apache-maven-3.8.8-bin.tar.gz


ENV M2_HOME='/opt/apache-maven-3.8.8'
ENV PATH="$M2_HOME/bin:$PATH"

RUN git clone https://github.com/ehrbase/openEHR_SDK.git

WORKDIR /opt/openEHR_SDK/

RUN git checkout v2.4.0

RUN mvn install -Dmaven.test.skip=true

# docker build -t openehr_sdk .

# docker run -it openehr_sdk bash

# cd generator/target

# java -jar generator-2.4.0.jar

# Container to build https://github.com/ppazos/openEHR-OPT
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y  git wget nano curl unzip zip groovy

ENV export GROOVY_HOME=/usr/share/groovy/
ENV export PATH=$GROOVY_HOME/bin:$PATH

RUN curl -s "https://get.sdkman.io" | bash

RUN /bin/bash -c "source /root/.sdkman/bin/sdkman-init.sh; sdk version; sdk install gradle 6.4.1"

WORKDIR /opt/

RUN git clone https://github.com/ppazos/openEHR-OPT.git

WORKDIR /opt/openEHR-OPT

# The is some opt file that causes building to fail, for now we just delete
RUN cd src/main/resources/opts/com.cabolabs.openehr_opt.namespaces.default && rm Station*

WORKDIR /opt/openEHR-OPT

RUN /bin/bash -c "source /root/.sdkman/bin/sdkman-init.sh; gradle build -x test"

# docker build -t openehr-opt .

# docker run -it -e PATH=/usr/share/groovy/bin:$PATH -e GROOVY_HOME=/usr/share/groovy/ openehr-opt bash



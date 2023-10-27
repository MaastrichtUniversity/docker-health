# Dockerfile to run https://github.com/synthetichealth/synthea
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y  openjdk-17-jdk git wget nano

WORKDIR /opt/

RUN wget https://github.com/synthetichealth/synthea/releases/download/master-branch-latest/synthea-with-dependencies.jar

ADD settings.txt settings.txt

RUN mkdir /tmp/synthea_output

# Explanation about the CSV export format https://github.com/synthetichealth/synthea/wiki/CSV-File-Data-Dictionary

# docker build -t synthea .

# docker run -v $(pwd)/output:/tmp/synthea_output synthea  java -jar synthea-with-dependencies.jar -c settings.txt

# docker run -it synthea bash

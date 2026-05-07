FROM sebp/elk:9.1.5

ENV LOGSTASH_HOME=/opt/logstash

ARG VER_ELK=9.1.5
#note: elk version must correspond to the version of the docker-image of sebp/elk!

WORKDIR ${LOGSTASH_HOME}
RUN gosu logstash bin/logstash-plugin install logstash-patterns-core
RUN gosu logstash bin/logstash-plugin update logstash-patterns-core
RUN gosu logstash bin/logstash-plugin install logstash-input-beats

ADD GeoLite2-City.mmdb /etc/logstash/GeoLite2-City.mmdb

## Remove existing config files
RUN rm -r /etc/logstash/conf.d/ && mkdir /etc/logstash/conf.d/

ADD ./elasticsearch.node1.yml /opt/elasticsearch/config/elasticsearch.yml
ADD ./logstash-config /etc/logstash/conf.d

## Add customized logstash patterns
ADD ./RIT.pattern ${LOGSTASH_HOME}/patterns/RIT

EXPOSE 5000 5001 5601 80

## Create own startup script
ADD ./start.sh /usr/local/bin/start.sh
RUN chmod +x /usr/local/bin/start.sh

## Create retention script and schedule
ADD ./retention.sh /etc/cron.monthly/retention.sh
ADD ./cron_retention /etc/cron.d/cron_retention
RUN chmod +x /etc/cron.monthly/retention.sh


CMD [ "/usr/local/bin/start.sh" ]
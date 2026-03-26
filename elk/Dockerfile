FROM sebp/elk:9.1.5 AS base

ENV LOGSTASH_HOME=/opt/logstash

ARG VER_ELK=9.1.5
#note: elk version must correspond to the version of the docker-image of sebp/elk!
ARG VER_ELASTICDUMP=6.124.1
#note: commands below install always latest version of patterns-core, variable is
#      used for path lateron in the dockerfile. So the ver should correspond to latest version on

WORKDIR ${LOGSTASH_HOME}
RUN gosu logstash bin/logstash-plugin install logstash-patterns-core
RUN gosu logstash bin/logstash-plugin update logstash-patterns-core
RUN gosu logstash bin/logstash-plugin install logstash-input-beats

ADD GeoLite2-City.mmdb /etc/logstash/GeoLite2-City.mmdb

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    npm \
    apache2 \
    nano

RUN npm install -g elasticdump@${VER_ELASTICDUMP}

## Remove existing config files
RUN rm -r /etc/logstash/conf.d/ && mkdir /etc/logstash/conf.d/


ADD ./elasticsearch.node1.yml /etc/elasticsearch/elasticsearch.yml
ADD ./logstash-config /etc/logstash/conf.d
RUN rm "/etc/logstash/conf.d/99 - Output.dev.conf"

## Add customized logstash patterns
ADD ./RIT.pattern ${LOGSTASH_HOME}/patterns/RIT

### Reverse proxy for default site with password
ADD ./000-default.conf /etc/apache2/sites-available/000-default.conf

## Add custom security configuration to hide apache2 version
ADD ./security.conf /etc/apache2/conf-available/security.conf

EXPOSE 5000 5001 5601 80

## Create own startup script
ADD ./start.sh /usr/local/bin/start.sh
RUN chmod +x /usr/local/bin/start.sh

## Create retention script and schedule
ADD ./retention.sh /etc/cron.monthly/retention.sh
ADD ./cron_retention /etc/cron.d/cron_retention
RUN chmod +x /etc/cron.monthly/retention.sh

### index templates
ADD ./template.*.json /tmp/


CMD [ "/usr/local/bin/start.sh" ]

FROM base AS development

ADD ./elasticsearch.node1.dev.yml /etc/elasticsearch/elasticsearch.yml
RUN rm "/etc/logstash/conf.d/99 - Output.conf"
ADD ["logstash-config/99 - Output.dev.conf", "/etc/logstash/conf.d/99 - Output.conf"]
ADD ./start.dev.sh /usr/local/bin/start.sh

CMD [ "/usr/local/bin/start.sh" ]
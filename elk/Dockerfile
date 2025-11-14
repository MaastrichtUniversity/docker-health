FROM sebp/elk:7.17.5

ENV LOGSTASH_HOME=/opt/logstash

ARG VER_ELK=7.17.5
#note: elk version must correspond to the version of the docker-image of sebp/elk!
ARG VER_ELASTICDUMP=6.14.1
ARG VER_JRUBY=2.5.0
ARG VER_LOGTRAIL=0.1.31
ARG VER_LOGSTASH_PATTERNS=4.3.1
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

## overwrite nagios patterns with own fork of Elastic logstash-patterns because of missing Nagios patterns
#RUN cd /opt/logstash/vendor/bundle/jruby/${VER_JRUBY}/gems/logstash-patterns-core-${VER_LOGSTASH_PATTERNS}/patterns/        && \
#    curl -O https://raw.githubusercontent.com/MaastrichtUniversity/logstash-patterns-core/master/patterns/nagios && \
#    chmod 644 nagios                                                                            && \
#    chown logstash:logstash nagios

## Remove existing config files
RUN rm -r /etc/logstash/conf.d/ && mkdir /etc/logstash/conf.d/


ADD ./elasticsearch.node1.yml /etc/elasticsearch/elasticsearch.yml
ADD ./logstash-config /etc/logstash/conf.d

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

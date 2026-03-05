#!/bin/bash
#
# /usr/local/bin/start.sh
# Start Elasticsearch, Logstash and Kibana services
#
# spujadas 2015-10-09; added initial pidfile removal and graceful termination

# WARNING - This script assumes that the ELK services are not running, and is
#   only expected to be run once, when the container is started.
#   Do not attempt to run this script if the ELK services are running (or be
#   prepared to reap zombie processes).

echo "================================="
echo "BOOTSTRAP FILE FOR ELK (modified)"
echo "================================="

## handle termination gracefully

_term() {
  echo "Terminating ELK"
  service elasticsearch stop
  service logstash stop
  service kibana stop
  exit 0
}

trap _term SIGTERM SIGINT


## remove pidfiles in case previous graceful termination failed
# NOTE - This is the reason for the WARNING at the top - it's a bit hackish,
#   but if it's good enough for Fedora (https://goo.gl/88eyXJ), it's good
#   enough for me :)

rm -f /var/run/elasticsearch/elasticsearch.pid /var/run/logstash.pid \
  /var/run/kibana5.pid

####################################
### APACHE REVERSE PROXY SECTION ###
####################################
# The reverse proxy will require .htpasswd authentication on port 80/443 for client usage.
# Log-sending applications communicate with elastic on port 9200 (via logstash ports 5000 and 5044) which does not
# require authentication. This is fine, as long as ports 5000, 5044 and 9200 are not exposed outside of the Docker network
# OR if access to those ports is regulated by iptables, thereby only allowing trusted log-sending services.

#Create htpassword file
htpasswd -c -b /opt/.htpasswd elastic $ELASTIC_PASSWORD

##Make apache owner of the htpasswd file
chown www-data:www-data /opt/.htpasswd

### Add or replace servername to apache2 config to avoid warning about FQDN at startup of apache
if [ -z $VIRTUAL_HOST ]; then VIRTUAL_HOST=localhost; fi
if [ $(grep ServerName /etc/apache2/apache2.conf 2>/dev/null | wc -l) -eq 0 ]; then
  echo "Adding 'ServerName $VIRTUAL_HOST' to /etc/apache2/apache2.conf"
  echo "ServerName $VIRTUAL_HOST" >>/etc/apache2/apache2.conf
else
  echo "Replacing Servername to 'Servername $VIRTUAL_HOST' in /etc/apache2/apache2.conf"
  sed -i 's/ServerName .*/ServerName $VIRTUAL_HOST/g' /etc/apache2/apache2.conf
fi

### apache2 modules enable and server restart
a2enmod proxy
a2enmod proxy_http
a2enmod proxy_ajp
a2enmod rewrite
a2enmod deflate
a2enmod headers
a2enmod proxy_balancer
a2enmod proxy_connect
a2enmod proxy_html

service apache2 restart

####################################

## initialise list of log files to stream in console (initially empty)
OUTPUT_LOGFILES=""


## override default time zone (Etc/UTC) if TZ variable is set
if [ ! -z "$TZ" ]; then
  ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
fi


## run pre-hooks
if [ -x /usr/local/bin/elk-pre-hooks.sh ]; then
  . /usr/local/bin/elk-pre-hooks.sh
fi


## start services as needed

### crond

service cron start


### Elasticsearch

if [ -z "$ELASTICSEARCH_START" ]; then
  ELASTICSEARCH_START=1
fi
if [ "$ELASTICSEARCH_START" -ne "1" ]; then
  echo "ELASTICSEARCH_START is set to something different from 1, not starting..."
else
  # update permissions of ES data directory
  chown -R elasticsearch:elasticsearch /var/lib/elasticsearch

  # override ES_HEAP_SIZE variable if set
  if [ ! -z "$ES_HEAP_SIZE" ]; then
    awk -v LINE="-Xmx$ES_HEAP_SIZE" '{ sub(/^.Xmx.*/, LINE); print; }' ${ES_PATH_CONF}/jvm.options \
        > ${ES_PATH_CONF}/jvm.options.new && mv ${ES_PATH_CONF}/jvm.options.new ${ES_PATH_CONF}/jvm.options
    awk -v LINE="-Xms$ES_HEAP_SIZE" '{ sub(/^.Xms.*/, LINE); print; }' ${ES_PATH_CONF}/jvm.options \
        > ${ES_PATH_CONF}/jvm.options.new && mv ${ES_PATH_CONF}/jvm.options.new ${ES_PATH_CONF}/jvm.options
  fi

  if [ ! -z "$ES_HEAP_DISABLE" ]; then
    awk -v LINE="#-XX:+HeapDumpOnOutOfMemoryError" '{ sub(/^-XX:\+HeapDumpOnOutOfMemoryError.*/, LINE); print; }' ${ES_PATH_CONF}/jvm.options \
        > ${ES_PATH_CONF}/jvm.options.new && mv ${ES_PATH_CONF}/jvm.options.new ${ES_PATH_CONF}/jvm.options
  fi

  # override ES_JAVA_OPTS variable if set
  if [ ! -z "$ES_JAVA_OPTS" ]; then
    awk -v LINE="ES_JAVA_OPTS=\"$ES_JAVA_OPTS\"" '{ sub(/^#?ES_JAVA_OPTS=.*/, LINE); print; }' /etc/default/elasticsearch \
        > /etc/default/elasticsearch.new && mv /etc/default/elasticsearch.new /etc/default/elasticsearch
  fi

  # override MAX_OPEN_FILES variable if set
  if [ ! -z "$MAX_OPEN_FILES" ]; then
    awk -v LINE="MAX_OPEN_FILES=$MAX_OPEN_FILES" '{ sub(/^#?MAX_OPEN_FILES=.*/, LINE); print; }' /etc/init.d/elasticsearch \
        > /etc/init.d/elasticsearch.new && mv /etc/init.d/elasticsearch.new /etc/init.d/elasticsearch \
        && chmod +x /etc/init.d/elasticsearch
  fi

  # override MAX_MAP_COUNT variable if set
  if [ ! -z "$MAX_MAP_COUNT" ]; then
    awk -v LINE="MAX_MAP_COUNT=$MAX_MAP_COUNT" '{ sub(/^#?MAX_MAP_COUNT=.*/, LINE); print; }' /etc/init.d/elasticsearch \
        > /etc/init.d/elasticsearch.new && mv /etc/init.d/elasticsearch.new /etc/init.d/elasticsearch \
        && chmod +x /etc/init.d/elasticsearch
  fi

  service elasticsearch start

  # wait for Elasticsearch to start up before either starting Kibana (if enabled)
  # or attempting to stream its log file
  # - https://github.com/elasticsearch/kibana/issues/3077

  # set number of retries (default: 30, override using ES_CONNECT_RETRY env var)
  re_is_numeric='^[0-9]+$'
  if ! [[ $ES_CONNECT_RETRY =~ $re_is_numeric ]] ; then
     ES_CONNECT_RETRY=60
  fi

  if [ -z "$ELASTICSEARCH_URL" ]; then
    ELASTICSEARCH_URL=${ES_PROTOCOL:-http}://localhost:9200
  fi

  counter=0
  while [ ! "$(curl -k ${ELASTICSEARCH_URL} 2> /dev/null)" -a $counter -lt $ES_CONNECT_RETRY  ]; do
    sleep 1
    ((counter++))
    echo "waiting for Elasticsearch to be up ($counter/$ES_CONNECT_RETRY)"
  done
  if [ ! "$(curl -k ${ELASTICSEARCH_URL} 2> /dev/null)" ]; then
    echo "Couldn't start Elasticsearch. Exiting."
    echo "Elasticsearch log follows below."
    cat /var/log/elasticsearch/elasticsearch.log
    exit 1
  fi

  # wait for cluster to respond before getting its name
  counter=0
  while [ -z "$CLUSTER_NAME" -a $counter -lt 30 ]; do
    sleep 1
    ((counter++))
    CLUSTER_NAME=$(curl -k ${ELASTICSEARCH_URL}/_cat/health?h=cluster 2> /dev/null | tr -d '[:space:]')
    echo "Waiting for Elasticsearch cluster to respond ($counter/30)"
  done

  if [ -z "$CLUSTER_NAME" ]; then
    echo "Couldn't get name of cluster. Exiting."
    echo "Elasticsearch log follows."
    cat /var/log/elasticsearch/elasticsearch.log
    exit 1
  elif [[ "$CLUSTER_NAME" =~ "master_not_discovered_exception" ]]; then
    # If we got a JSON error back, don't treat it like the literal name of the cluster.
    # Example of what this error looks like:
    # [{"error":{"root_cause":[{"type":"master_not_discovered_exception","reason":null}]
    # We don't know the cluster name, so we'll just glob it.
    echo "Failed to contact a healthy master in cluster."
    echo "Elasticsearch logs follow."
    cat /var/log/elasticsearch/*.log
    exit 1
  fi
  OUTPUT_LOGFILES+="/var/log/elasticsearch/${CLUSTER_NAME}.log "
fi


### Logstash

if [ -z "$LOGSTASH_START" ]; then
  LOGSTASH_START=1
fi
if [ "$LOGSTASH_START" -ne "1" ]; then
  echo "LOGSTASH_START is set to something different from 1, not starting..."
else
  # override LS_HEAP_SIZE variable if set
  if [ ! -z "$LS_HEAP_SIZE" ]; then
    awk -v LINE="-Xmx$LS_HEAP_SIZE" '{ sub(/^.Xmx.*/, LINE); print; }' ${LOGSTASH_PATH_SETTINGS}/jvm.options \
        > ${LOGSTASH_PATH_SETTINGS}/jvm.options.new && mv ${LOGSTASH_PATH_SETTINGS}/jvm.options.new ${LOGSTASH_PATH_SETTINGS}/jvm.options
    awk -v LINE="-Xms$LS_HEAP_SIZE" '{ sub(/^.Xms.*/, LINE); print; }' ${LOGSTASH_PATH_SETTINGS}/jvm.options \
        > ${LOGSTASH_PATH_SETTINGS}/jvm.options.new && mv ${LOGSTASH_PATH_SETTINGS}/jvm.options.new ${LOGSTASH_PATH_SETTINGS}/jvm.options
  fi

  if [ ! -z "$LS_HEAP_DISABLE" ]; then
    awk -v LINE="#-XX:+HeapDumpOnOutOfMemoryError" '{ sub(/^-XX:\+HeapDumpOnOutOfMemoryError.*/, LINE); print; }' ${LOGSTASH_PATH_SETTINGS}/jvm.options \
        > ${LOGSTASH_PATH_SETTINGS}/jvm.options.new && mv ${LOGSTASH_PATH_SETTINGS}/jvm.options.new ${LOGSTASH_PATH_SETTINGS}/jvm.options
  fi

  # override LS_OPTS variable if set
  if [ ! -z "$LS_OPTS" ]; then
    awk -v LINE="LS_OPTS=\"$LS_OPTS\"" '{ sub(/^LS_OPTS=.*/, LINE); print; }' /etc/init.d/logstash \
        > /etc/init.d/logstash.new && mv /etc/init.d/logstash.new /etc/init.d/logstash && chmod +x /etc/init.d/logstash
  fi

  service logstash start
  OUTPUT_LOGFILES+="/var/log/logstash/logstash-plain.log "
fi


### Kibana

if [ -z "$KIBANA_START" ]; then
  KIBANA_START=1
fi
if [ "$KIBANA_START" -ne "1" ]; then
  echo "KIBANA_START is set to something different from 1, not starting..."
else
  # override NODE_OPTIONS variable if set
  if [ ! -z "$NODE_OPTIONS" ]; then
    awk -v LINE="NODE_OPTIONS=\"$NODE_OPTIONS\"" '{ sub(/^NODE_OPTIONS=.*/, LINE); print; }' /etc/init.d/kibana \
        > /etc/init.d/kibana.new && mv /etc/init.d/kibana.new /etc/init.d/kibana && chmod +x /etc/init.d/kibana
  fi

  service kibana start
  OUTPUT_LOGFILES+="/var/log/kibana/kibana5.log "
fi

# Exit if nothing has been started
if [ "$ELASTICSEARCH_START" -ne "1" ] && [ "$LOGSTASH_START" -ne "1" ] \
  && [ "$KIBANA_START" -ne "1" ]; then
  >&2 echo "No services started. Exiting."
  exit 1
fi


## run post-hooks
if [ -x /usr/local/bin/elk-post-hooks.sh ]; then
  ### if Kibana was started...
  if [ "$KIBANA_START" -eq "1" ]; then

  ### ... then wait for Kibana to be up first to ensure that .kibana index is
  ### created before the post-hooks are executed
    # set number of retries (default: 30, override using KIBANA_CONNECT_RETRY env var)
    if ! [[ $KIBANA_CONNECT_RETRY =~ $re_is_numeric ]] ; then
       KIBANA_CONNECT_RETRY=200
    fi

    if [ -z "$KIBANA_URL" ]; then
      KIBANA_URL=http://localhost:5601
    fi

    counter=0
    while [ ! "$(curl ${KIBANA_URL} 2> /dev/null)" -a $counter -lt $KIBANA_CONNECT_RETRY  ]; do
      sleep 1
      ((counter++))
      echo "waiting for Kibana to be up ($counter/$KIBANA_CONNECT_RETRY)"
    done
    if [ ! "$(curl ${KIBANA_URL} 2> /dev/null)" ]; then
      echo "Couldn't start Kibana. Exiting."
      echo "Kibana log follows below."
      cat /var/log/kibana/kibana5.log
      exit 1
    fi
    # wait for Kibana to not only be up but to return 200 OK
    counter=0
    while [[ "$(curl -s -o /dev/null -w ''%{http_code}'' ${KIBANA_URL}/api/status)" != "200" && $counter -lt 30 ]]; do
      sleep 1
      ((counter++))
      echo "waiting for Kibana to respond ($counter/30)"
    done
    if [[ "$(curl -s -o /dev/null -w ''%{http_code}'' ${KIBANA_URL}/api/status)" != "200" ]]; then
      echo "Timed out waiting for Kibana to respond. Exiting."
      echo "Kibana log follows below."
      cat /var/log/kibana/kibana5.log
      exit 1
    fi
  fi

  . /usr/local/bin/elk-post-hooks.sh
fi

### Configuration of ElasticSearch and Kibana

cd /tmp
##SKIP## elasticdump --input=kibana-exported.json --output=http://localhost:9200/.kibana --type=data

# import index templates in elastic
echo "
elasticsearch: importing index templates to"
curl -H 'Content-Type: application/json' -XPUT 'http://localhost:9200/_template/idx' -d@/tmp/template.index.json


# create dummy indexes (to avoid issues when ceating aliases)
echo "
elasticsearch: create indexes in case they don't exist (will cause ignorable error if index already exist)"
curl -XPUT "http://localhost:9200/idx-$(date +'%Y.%m')"


# wait for Kibana to be up (responding to api)

if ! [[ $KIBANA_CONNECT_RETRY =~ $re_is_numeric ]] ; then
    KIBANA_CONNECT_RETRY=200
fi

counter=0
KIBANA_STATUS=""
while [[ ! *"$KIBANA_STATUS"* =~ "OK" && $counter -le $KIBANA_CONNECT_RETRY ]]; do
    echo "waiting for Kibana to be up ($counter/$KIBANA_CONNECT_RETRY)"
    sleep 5
    ((counter+=5))
    KIBANA_STATUS="$(curl localhost:5601/status -I 2>/dev/null | grep 'HTTP' | awk '{ $1=""; $2=""; print }')"
#    echo " + kibana status: '${KIBANA_STATUS}'"
done
if [[ ! *"$KIBANA_STATUS"* =~ "OK" ]]; then
    echo "Couln't start Kibanah. Exiting."
    echo "Kibana log follows below."
    cat /var/log/elasticsearch/elasticsearch.log
    exit 1
fi

## Aliases are added when creating an index (few lines above) from the index template
# add aliases for indexes
#echo "
#elasticsearch: adding aliasses for indexes"
#curl -H 'Content-Type: application/json' -XPOST 'http://localhost:9200/_aliases' -d '{ "actions" : [ { "add" : { "index" : ".*", "alias" : "config" } } ] }'
curl -H 'Content-Type: application/json' -XPOST 'http://localhost:9200/_aliases' -d '{ "actions" : [ { "add" : { "index" : "idx-*", "alias" : "all" } } ] }'
#curl -H 'Content-Type: application/json' -XPOST 'http://localhost:9200/_aliases' -d '{ "actions" : [ { "add" : { "index" : "idx-*", "alias" : "core", "filter": { "term": { "category" : "core" } } } } ] }'
#curl -H 'Content-Type: application/json' -XPOST 'http://localhost:9200/_aliases' -d '{ "actions" : [ { "add" : { "index" : "idx-*", "alias" : "aux", "filter": { "term": { "category" : "aux" } } } } ] }'
#curl -H 'Content-Type: application/json' -XPOST 'http://localhost:9200/_aliases' -d '{ "actions" : [ { "add" : { "index" : "idx-*", "alias" : "sys", "filter": { "term": { "category" : "sys" } } } } ] }'


# import index patterns in kibana
echo ""
echo "kibana: import index patterns"
curl -H "Content-Type: application/json" -H "kbn-xsrf: reporting" -XPOST 'http://localhost:5601/api/saved_objects/index-pattern/all'  -d '{ "attributes":{ "title":"all", "timeFieldName" : "@timestamp"} }'
curl -H "Content-Type: application/json" -H "kbn-xsrf: reporting" -XPOST 'http://localhost:5601/api/saved_objects/index-pattern/core' -d '{ "attributes":{ "title":"core", "timeFieldName" : "@timestamp"} }'
curl -H "Content-Type: application/json" -H "kbn-xsrf: reporting" -XPOST 'http://localhost:5601/api/saved_objects/index-pattern/aux'  -d '{ "attributes":{ "title":"aux", "timeFieldName" : "@timestamp"} }'
curl -H "Content-Type: application/json" -H "kbn-xsrf: reporting" -XPOST 'http://localhost:5601/api/saved_objects/index-pattern/sys'  -d '{ "attributes":{ "title":"sys", "timeFieldName" : "@timestamp"} }'


# set default pattern in kibana
echo "kibana: set default index patterns in kibana"
#ToDo: not found out yet how to set the default pattern...
#curl -H 'Content-Type: application/json' -XPUT http://localhost:9200/.kibana/config/5.3.1 -d '{"defaultIndex" : "core", "discover:sampleSize:" : "10000" }'


# add logfile for retention script to OUTPUT_LOGFILES and crontab
OUTPUT_LOGFILES+="/var/log/retention.log /var/log/crontab.log"


touch $OUTPUT_LOGFILES
tail -f $OUTPUT_LOGFILES &
wait

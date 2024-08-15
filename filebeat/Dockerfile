# Using an older version so that there are no compatibility issues between an older elk version
FROM docker.elastic.co/beats/filebeat:7.13.2
COPY --chown=filebeat filebeat.yml /usr/share/filebeat/filebeat.yml
COPY certs/ca.crt /etc/pki/ca-trust/source/whitelist/ca.crt
RUN chmod go-w /usr/share/filebeat/filebeat.yml
USER root
RUN update-ca-trust
USER filebeat
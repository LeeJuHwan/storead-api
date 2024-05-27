FROM elasticsearch:7.17.9

RUN /usr/share/elasticsearch/bin/elasticsearch-plugin install analysis-nori

ENV discovery.type=single-node
ENV logger.level=WARN

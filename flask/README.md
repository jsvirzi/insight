# goto kafka installation directory
pushd /home/ubuntu/kafka_2.10-0.8.1.1
# start zookeeper
bin/zookeeper-server-start.sh config/zookeeper.properties &
# start the kafka server
bin/kafka-server-start.sh config/server.properties &
# create the topics
bin/kafka-topics.sh --create --topic citations_submit --replication-factor 1 --partitions 1 --zookeeper 127.0.0.1:2181
bin/kafka-topics.sh --create --topic citations_retrieve --replication-factor 1 --partitions 1 --zookeeper 127.0.0.1:2181

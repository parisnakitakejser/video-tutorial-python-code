# Kafka Data Stream

You can with this folder starting up a fully working Kafka cluster on your machine using docker-compose.yaml file, all the files you can test with are placed into the sample folder.

## Start Kafka Cluster

It's will start up a Kafka single node cluster, Zookeeper, Kafka UI and Kafka Connect single node Cluster there will be ready to work with locally.

```
docker-compose up -d
```

## Sample files

```
cd sample
pyenv virtualenv kafka-test
pyenv local kafka-test
pip install -r requirements.txt
```

# Redpandas_kafka_Transactions

## Redpanda,Redis and Spark Docker Compose Setup

This Docker Compose file defines services for running Redpanda and Redis containers.

### Redpanda
- **Image**: docker.redpanda.com/redpandadata/redpanda:v23.3.5
- **Container Name**: redpanda
- **Ports Exposed**: 
  - 18081: Kafka schema registry
  - 18082: Kafka REST proxy
  - 19092: Kafka broker
- **Description**: Redpanda is a Kafka-compatible event streaming platform built for modern applications and hybrid cloud environments. This service sets up a Redpanda instance with specified configuration parameters.

### Redpanda Console
- **Image**: docker.redpanda.com/redpandadata/console:v2.4.3
- **Container Name**: redpanda-console
- **Ports Exposed**: 
  - 8080: Redpanda console UI
- **Description**: Redpanda Console is a web-based UI for managing Redpanda clusters. This service provides access to the console UI and configures it to connect to the Redpanda instance.

### Redis
- **Image**: redis:latest
- **Container Name**: redis
- **Ports Exposed**: 
  - 6379: Redis port
- **Description**: Redis is an open-source, in-memory data structure store used as a database, cache, and message broker. This service sets up a Redis instance.

### Spark Master (It has been commented out because local standalone spark cluster is used in this project)
- **Image**: bitnami/spark:latest
- **Container Name**: spark-master
- **Ports Exposed**: 
  - 8088: Spark master web UI
  - 7077: Spark master RPC port
  - 3306: MySQL port
- **Description**: Spark Master is the entry point for Spark applications. It coordinates the execution of Spark jobs on Spark Workers.

### Spark Worker (It has been commented out because local standalone spark cluster is used in this project)
- **Image**: bitnami/spark:latest
- **Container Name**: spark-worker
- **Description**: Spark Worker executes tasks delegated by the Spark Master. It connects to the Spark Master to receive instructions and resources for running Spark jobs.
- **Environment Variables**:
  - `SPARK_MODE`: Specifies the mode of Spark Worker (set to `worker`).
  - `SPARK_WORKER_CORES`: Specifies the number of CPU cores allocated to the Spark Worker (set to `1`).
  - `SPARK_WORKER_MEMORY`: Specifies the amount of memory allocated to the Spark Worker (set to `2g`).
  - `SPARK_MASTER_URL`: Specifies the URL of the Spark Master (set to `spark://spark-master:7077`).


## Setup
1. Make sure you have Docker and Docker Compose installed on your machine.
2. Copy the contents of this Docker Compose file into a file named `docker-compose.yml`.
3. Navigate to the directory containing the `docker-compose.yml` file.
4. Run the following command to start the services: `sudo docker-compose up -d`.
5. To stop the services, run: `sudo docker-compose down`.
6. Configuration of the local machine is OS:Ubuntu 22.04.4 LTS | Memory: 16GB | Cores Count: 8

## Configuration
- The Redpanda service is configured with specific parameters such as the number of SMP cores, Kafka and Pandaproxy addresses, and schema registry address.
- The Redpanda Console service is configured with connection details to the Redpanda instance, including Kafka brokers and schema registry URLs.
- The Redis service uses the latest version of the Redis image and exposes port 6379.
- Optionally, you can uncomment and configure the Spark services (spark-master and spark-worker) if needed.

## Task 1
1. To create the topic run the following command:  `sudo docker exec -it redpanda rpk topic create transactions --partitions 2 --topic-config retention.ms=86400000`
2. To create the user:  `sudo docker exec -it redpanda rpk acl create --allow-principal User:abhi --operation All --cluster --topic transactions`
3. To register the schema we need to define the avro format of the schema in the `constants.py` and run the script `schema.py` this will register the schema in Schema Registry
4. Check the topic and registered schema in the redpanda console which can be accessed by the following url:  [http://localhost:8080](http://localhost:8080)



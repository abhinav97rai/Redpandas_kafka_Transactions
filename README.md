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


### Setup
1. Make sure you have Docker and Docker Compose installed on your machine.
2. Copy the contents of this Docker Compose file into a file named `docker-compose.yml`.
3. Navigate to the directory containing the `docker-compose.yml` file.
4. Run the following command to start the services: `sudo docker-compose up -d`.
5. To stop the services, run: `sudo docker-compose down`.
6. Configuration of the local machine is OS:Ubuntu 22.04.4 LTS | Memory: 16GB | Cores Count: 8

### Configuration
- The Redpanda service is configured with specific parameters such as the number of SMP cores, Kafka and Pandaproxy addresses, and schema registry address.
- The Redpanda Console service is configured with connection details to the Redpanda instance, including Kafka brokers and schema registry URLs.
- The Redis service uses the latest version of the Redis image and exposes port 6379.
- Optionally, you can uncomment and configure the Spark services (spark-master and spark-worker) if needed.

## Task 1
1. To create the topic run the following command:  `sudo docker exec -it redpanda rpk topic create transactions --partitions 2 --topic-config retention.ms=86400000`
2. To create the user:
    - `sudo docker exec -it redpanda rpk acl create --allow-principal User:transactions-backup-job-user --operation All --cluster --topic transactions`
    - `sudo docker exec -it redpanda rpk acl create --allow-principal User:transactions-ml-features-job-user --operation All --cluster --topic transactions`
4. To register the schema we need to define the avro format of the schema in the `constants.py` and run the script `schema.py` this will register the schema in Schema Registry
5. Check the topic, users and registered schema in the redpanda console which can be accessed by the following url:  [http://localhost:8080](http://localhost:8080)

![Screenshot from 2024-03-20 00-29-38](https://github.com/abhinav97rai/Redpandas_kafka_Transactions/assets/40785548/b6f69954-235a-4ece-8e0f-6e9c9351d811)
![Screenshot from 2024-03-20 00-31-12](https://github.com/abhinav97rai/Redpandas_kafka_Transactions/assets/40785548/cb468f85-c23a-4bf3-95ae-260f122746a3)
![Screenshot from 2024-03-20 00-34-42](https://github.com/abhinav97rai/Redpandas_kafka_Transactions/assets/40785548/a7f13163-6c23-4d28-ae89-1fd6acff17ff)

## Task 2
1. Ensure that Kafka and Schema Registry services are running and accessible at the specified URLs (`kafka_url` and `schema_registry_url`).
2. Modify the `kafka_url`, `schema_registry_url`, `kafka_topic`, and `schema_registry_subject` variables to match your Kafka and Schema Registry configurations(or use the variable that are provided in the script).
3. Run the script using Python: `kafka_produce.py`
4. The script will generate 10 random transaction objects and produce them to the specified Kafka topic `transactions` in Avro format.

## Task 3
1. spark_consume.py script demonstrates how to consume Avro serialized messages from a Kafka topic using Apache Spark (PySpark). The consumed messages are then processed and written to Parquet files for further analysis or storage.
2. Modify the `kafka_url`, `schema_registry_url`, `kafka_topic`, and `schema_registry_subject` variables to match your Kafka and Schema Registry configurations(or use the variable that are provided in the script).
3. Run the script using Python: `spark_consume.py`
4. The script will start consuming Avro messages from the specified Kafka topic, process them, and write the output to Parquet files.


## Task 4 & 5
This Python script demonstrates how to integrate Redis with PySpark for real-time data processing and caching. The script reads data from a Parquet file, processes it using PySpark, and then stores the aggregated results in a Redis database.

### Usage

1. Ensure that Redis server is running on `localhost:6379`.
2. Run the script using Python: `check.py`
3. The script will read data from the Parquet file, process it using PySpark, and store the aggregated results in Redis.

### Description

- The script first connects to the Redis server using the `redis` Python library.
- It creates a SparkSession for interacting with Spark.
- Parquet file containing historical data is read into a DataFrame using PySpark.
- The script reads the last processed timestamp from a CSV file and filters the Parquet data based on this timestamp.
- The DataFrame is processed to compute the total number of transactions per user using PySpark DataFrame operations.
- The results are stored in Redis using the user ID as the key and the total transaction count as the value.
- Finally, the script retrieves the aggregated data from Redis and prints it.
- To scale it even further we can use an analytical database such as clickhouse to store the data at large scale.

### Dependencies

- `pyspark`: Python API for Apache Spark.
- `pandas`: Python data analysis library.
- `redis`: Python client for Redis.

### Configuration

- Ensure that Redis server is running on `localhost:6379`.
- Adjust the `parquet_file_path` variable to point to the location of your Parquet file.
- Modify the `./transaction_timestamp.csv` file as needed to store the last processed timestamp.

### Output

- The script computes the total number of transactions per user and stores the results in Redis.
- The aggregated data can be accessed directly from Redis using the user ID as the key.

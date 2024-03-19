from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.avro.functions import from_avro
import os
import json
from confluent_kafka.schema_registry import SchemaRegistryClient



def get_schema_from_schema_registry(schema_registry_url, schema_registry_subject):
    sr = SchemaRegistryClient({'url': schema_registry_url})
    latest_version = sr.get_latest_version(schema_registry_subject)

    return sr, latest_version


# Kafka broker address
kafka_bootstrap_servers = 'localhost:19092'

# Kafka topic to consume messages from
kafka_topic = 'transactions'
schema_registry_subject = f"{kafka_topic}-value"

# Schema Registry URL
schema_registry_url = 'http://localhost:18081'

# Retrieve Avro schema from Schema Registry
sr, latest_version = get_schema_from_schema_registry(schema_registry_url, schema_registry_subject)
avro_schema = latest_version.schema.schema_str
# avro_schema = json.loads(avro_schema)
print(avro_schema)


SUBMIT_ARGS = "--packages org.apache.spark:spark-avro_2.12:3.5.0,org.apache.spark:spark-streaming-kafka-0-10_2.12:3.5.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.apache.spark:spark-token-provider-kafka-0-10_2.12:3.5.0,org.apache.kafka:kafka-clients:3.4.1,org.apache.commons:commons-pool2:2.11.1 pyspark-shell"
os.environ["PYSPARK_SUBMIT_ARGS"] = SUBMIT_ARGS

spark = SparkSession.builder \
    .appName("KafkaAvroConsumer") \
    .getOrCreate()

# Define Kafka source for consuming Avro messages
kafka_source = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("subscribe", kafka_topic) \
    .option("startingOffsets", "earliest") \
    .option("failOnDataLoss", "false") \
    .option("groupId", "transactions-job-backup") \
    .load()

# print(kafka_source.schema)
kafka_source = kafka_source.withColumn('fixedValue', expr("substring(value, 6, length(value)-5)"))

fromAvroOptions = {"mode":"PERMISSIVE"}
# fromAvroOptions = {"mode":"DROPMALFORMED"} 
decoded_output = kafka_source.select(
    from_avro(
        col("fixedValue"), avro_schema
    ).alias("transaction")
)
transaction_value_df = decoded_output.select("transaction.user_id","transaction.transaction_timestamp_millis","transaction.amount","transaction.currency","transaction.counterpart_id")
# transaction_value_df.printSchema()

# Define any further processing or output operation, e.g., writing to console
output_path = "./historical_data"



query = transaction_value_df \
    .writeStream \
    .format("parquet") \
    .outputMode("append") \
    .option("checkpointLocation", "./historical_data/checkpoint") \
    .option("path", output_path) \
    .start()

# Start the streaming query and wait for termination
query.awaitTermination()
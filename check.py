from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import pandas as pd
import redis

# Connect to Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

# Create SparkSession
spark = SparkSession.builder \
    .appName("ReadParquetFile") \
    .getOrCreate()

# Path to the Parquet file
parquet_file_path = "./historical_data"

#read the timestamp to read the record post this time
df_time = pd.read_csv('./transaction_timestamp.csv')
df_time = df_time.values.tolist()
df_time = df_time[0][0]

# Read Parquet file into DataFrame
df = spark.read.parquet(parquet_file_path)
df = df.filter(col("transaction_timestamp_millis")>=df_time).dropDuplicates()
df_processed_time = df.orderBy(col("transaction_timestamp_millis").desc()).select("transaction_timestamp_millis").limit(1).toPandas()
df_processed_time.to_csv('./transaction_timestamp.csv', index=False, header=True, mode='w')

# Show first few rows of the DataFrame
df = df.select(col("user_id"))
df = df.groupBy(col("user_id")).agg(count(col("user_id")).alias("total_transactions_count"))

print(df.show())

df = df.toPandas()
df =  df.values.tolist()
for i in df:
    pre_tansaction = redis_client.get(str(i[0]))
    if pre_tansaction:
        redis_client.set(str(i[0]),str(i[1]+int(pre_tansaction)))
    else:
        redis_client.set(str(i[0]),str(i[1]))

for i in df:
    data = redis_client.get(str(i[0]))
    print(data)

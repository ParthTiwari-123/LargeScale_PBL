import time
import pandas as pd
import pyarrow.parquet as pq
from fastavro import reader

# JSON
start = time.time()
df = pd.read_json("../data/base/orders.json", lines=True)
json_speed = len(df) / (time.time() - start)

# Parquet
start = time.time()
df = pq.read_table("../data/base/orders.parquet").to_pandas()
parquet_speed = len(df) / (time.time() - start)

# Avro
start = time.time()
with open("../data/base/orders.avro", "rb") as f:
    data = list(reader(f))
avro_speed = len(data) / (time.time() - start)

print("Records/sec:")
print("JSON:", json_speed)
print("Avro:", avro_speed)
print("Parquet:", parquet_speed)
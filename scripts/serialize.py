import pandas as pd
import json
import time
import os
from fastavro import writer, parse_schema
import pyarrow as pa
import pyarrow.parquet as pq

df = pd.read_csv("../data/base/orders.csv")

# ---------- JSON ----------
start = time.time()
df.to_json("../data/base/orders.json", orient="records", lines=True)
json_time = time.time() - start

# ---------- Avro ----------
schema = {
    "type": "record",
    "name": "Order",
    "fields": [
        {"name": "order_id", "type": "int"},
        {"name": "customer_id", "type": "int"},
        {"name": "amount", "type": "float"},
        {"name": "timestamp", "type": "long"}
    ]
}

start = time.time()
with open("../data/base/orders.avro", "wb") as out:
    writer(out, parse_schema(schema), df.to_dict(orient="records"))
avro_time = time.time() - start

# ---------- Parquet ----------
start = time.time()
table = pa.Table.from_pandas(df)
pq.write_table(table, "../data/base/orders.parquet")
parquet_time = time.time() - start

# ---------- File sizes ----------
sizes = {
    "json": os.path.getsize("../data/base/orders.json"),
    "avro": os.path.getsize("../data/base/orders.avro"),
    "parquet": os.path.getsize("../data/base/orders.parquet")
}

print("Sizes:", sizes)
print("Write times:", json_time, avro_time, parquet_time)
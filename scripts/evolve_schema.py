import pandas as pd
import os
from fastavro import writer, parse_schema
import pyarrow as pa
import pyarrow.parquet as pq

BASE_PATH = "../data/base/"
EVOLVED_PATH = "../data/evolved/"

os.makedirs(EVOLVED_PATH, exist_ok=True)

# Load base CSV
df = pd.read_csv(BASE_PATH + "orders.csv")

print("Loaded base dataset:", df.shape)


# -------------------------------
# CASE 1: ADD COLUMN
# -------------------------------

df_add = df.copy()
df_add["status"] = "completed"

schema_add = {
    "type": "record",
    "name": "Order",
    "fields": [
        {"name": "order_id", "type": "int"},
        {"name": "customer_id", "type": "int"},
        {"name": "amount", "type": "float"},
        {"name": "timestamp", "type": "long"},
        {"name": "status", "type": "string"}
    ]
}

with open(EVOLVED_PATH + "orders_add.avro", "wb") as out:
    writer(out, parse_schema(schema_add), df_add.to_dict("records"))

df_add.to_json(EVOLVED_PATH + "orders_add.json", orient="records", lines=True)

table = pa.Table.from_pandas(df_add)
pq.write_table(table, EVOLVED_PATH + "orders_add.parquet")

print("Add column schema generated")


# -------------------------------
# CASE 2: REMOVE COLUMN
# -------------------------------

df_remove = df.drop(columns=["amount"])

schema_remove = {
    "type": "record",
    "name": "Order",
    "fields": [
        {"name": "order_id", "type": "int"},
        {"name": "customer_id", "type": "int"},
        {"name": "timestamp", "type": "long"}
    ]
}

with open(EVOLVED_PATH + "orders_remove.avro", "wb") as out:
    writer(out, parse_schema(schema_remove), df_remove.to_dict("records"))

df_remove.to_json(EVOLVED_PATH + "orders_remove.json", orient="records", lines=True)

table = pa.Table.from_pandas(df_remove)
pq.write_table(table, EVOLVED_PATH + "orders_remove.parquet")

print("Remove column schema generated")


# -------------------------------
# CASE 3: RENAME COLUMN
# -------------------------------

df_rename = df.rename(columns={"customer_id": "user_id"})

schema_rename = {
    "type": "record",
    "name": "Order",
    "fields": [
        {"name": "order_id", "type": "int"},
        {"name": "user_id", "type": "int"},
        {"name": "amount", "type": "float"},
        {"name": "timestamp", "type": "long"}
    ]
}

with open(EVOLVED_PATH + "orders_rename.avro", "wb") as out:
    writer(out, parse_schema(schema_rename), df_rename.to_dict("records"))

df_rename.to_json(EVOLVED_PATH + "orders_rename.json", orient="records", lines=True)

table = pa.Table.from_pandas(df_rename)
pq.write_table(table, EVOLVED_PATH + "orders_rename.parquet")

print("Rename column schema generated")


# -------------------------------
# CASE 4: CHANGE TYPE
# -------------------------------

df_type = df.copy()
df_type["amount"] = df_type["amount"].astype(str)

schema_type = {
    "type": "record",
    "name": "Order",
    "fields": [
        {"name": "order_id", "type": "int"},
        {"name": "customer_id", "type": "int"},
        {"name": "amount", "type": "string"},
        {"name": "timestamp", "type": "long"}
    ]
}

with open(EVOLVED_PATH + "orders_type_change.avro", "wb") as out:
    writer(out, parse_schema(schema_type), df_type.to_dict("records"))

df_type.to_json(EVOLVED_PATH + "orders_type_change.json", orient="records", lines=True)

table = pa.Table.from_pandas(df_type)
pq.write_table(table, EVOLVED_PATH + "orders_type_change.parquet")

print("Type change schema generated")

print("All schema evolution cases created.")
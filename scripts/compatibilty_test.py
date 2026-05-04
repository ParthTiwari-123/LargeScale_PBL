import pandas as pd
import pyarrow.parquet as pq
from fastavro import reader
import os

BASE_PATH = "../data/base/"
EVOLVED_PATH = "../data/evolved/"
base_df = pd.read_csv(BASE_PATH + "orders.csv")

def read_json(file):
    return pd.read_json(file, lines=True)

def read_parquet(file):
    return pq.read_table(file).to_pandas()

def read_avro(file):
    with open(file, "rb") as f:
        data = list(reader(f))
    return pd.DataFrame(data)

def compare_schema(df_base, df_new):
    base_cols = set(df_base.columns)
    new_cols = set(df_new.columns)

    added = new_cols - base_cols
    removed = base_cols - new_cols

    return added, removed


def check_types(df_base, df_new):
    type_changes = []

    for col in df_base.columns:
        if col in df_new.columns:
            if df_base[col].dtype != df_new[col].dtype:
                type_changes.append(
                    (col, str(df_base[col].dtype), str(df_new[col].dtype))
                )

    return type_changes


def check_row_count(df_base, df_new):
    return len(df_base) == len(df_new)

def run_test(test_name, fmt, reader_func):
    file_path = os.path.join(EVOLVED_PATH, f"{test_name}.{fmt}")

    if not os.path.exists(file_path):
        return f"FAILED -> File not found"

    try:
        df_new = reader_func(file_path)
        added, removed = compare_schema(base_df, df_new)
        type_changes = check_types(base_df, df_new)
        row_ok = check_row_count(base_df, df_new)

        result = []
        result.append(f"Records: {len(df_new)}")

        if added:
            result.append(f"Added columns: {list(added)}")

        if removed:
            result.append(f"Removed columns: {list(removed)}")

        if type_changes:
            for col, old, new in type_changes:
                result.append(f"Type changed: {col} ({old} → {new})")

        if row_ok:
            result.append("Row count OK")
        else:
            result.append("Row count MISMATCH")

        return "SUCCESS -> " + " | ".join(result)

    except Exception as e:
        return f"FAILED -> {str(e)}"


tests = [
    "orders_add",
    "orders_remove",
    "orders_rename",
    "orders_type_change"
]

formats = {
    "json": read_json,
    "avro": read_avro,
    "parquet": read_parquet
}

print("\nSchema Compatibility Results (Improved)\n")

for test in tests:
    print(f"\n--- Testing {test} ---")

    for fmt, func in formats.items():
        result = run_test(test, fmt, func)
        print(f"{fmt.upper()} : {result}")
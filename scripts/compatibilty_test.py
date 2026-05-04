import pandas as pd
import pyarrow.parquet as pq
from fastavro import reader


BASE_PATH = "../data/base/"
EVOLVED_PATH = "../data/evolved/"


def test_json(file):
    try:
        df = pd.read_json(file, lines=True)
        return True, len(df)
    except Exception as e:
        return False, str(e)


def test_parquet(file):
    try:
        df = pq.read_table(file).to_pandas()
        return True, len(df)
    except Exception as e:
        return False, str(e)


def test_avro(file):
    try:
        with open(file, "rb") as f:
            data = list(reader(f))
        return True, len(data)
    except Exception as e:
        return False, str(e)


tests = [
    "orders_add",
    "orders_remove",
    "orders_rename",
    "orders_type_change"
]

formats = {
    "json": test_json,
    "avro": test_avro,
    "parquet": test_parquet
}


print("\nSchema Compatibility Results\n")

for test in tests:
    print(f"\n--- Testing {test} ---")

    for fmt, func in formats.items():

        path = EVOLVED_PATH + f"{test}.{fmt}"

        success, result = func(path)

        if success:
            print(f"{fmt.upper()} : SUCCESS ({result} records read)")
        else:
            print(f"{fmt.upper()} : FAILED -> {result}")
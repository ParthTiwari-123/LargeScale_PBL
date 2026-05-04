import pandas as pd
from faker import Faker
import random
import time

fake = Faker()

records = []

for _ in range(100000):
    records.append({
        "order_id": random.randint(1000, 9999),
        "customer_id": random.randint(100, 999),
        "amount": round(random.uniform(10, 1000), 2),
        "timestamp": int(time.time())
    })

df = pd.DataFrame(records)
df.to_csv("../data/base/orders.csv", index=False)

print("✅ Data generated")
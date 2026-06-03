"""
scripts/generate_sample_data.py
--------------------------------
Generates a realistic but deliberately messy orders CSV
so the cleaner has real work to do.
"""

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

SKUS = ["SKU-1001", "SKU-1002", "SKU-1003", "SKU-2001", "SKU-2002",
        "SKU-3001", "SKU-3002", "SKU-3003", "SKU-4001", "SKU-5001"]
CATEGORIES = ["Electronics", "Clothing", "Home & Garden", "Sports", "Beauty"]
STATUSES = ["Delivered", "Pending", "Dispatched", "Cancelled", "Returned"]
WAREHOUSES = ["DBN-DC1", "JHB-DC1", "CPT-DC1"]


def _random_date(start_year=2024):
    start = datetime(start_year, 1, 1)
    return start + timedelta(days=random.randint(0, 364))


def generate_sample_csv(path: str, num_rows: int = 500):
    Path(path).parent.mkdir(exist_ok=True)
    rows = []

    for i in range(1, num_rows + 1):
        order_date = _random_date()
        dispatch_offset = random.randint(1, 7)
        dispatch_date = order_date + timedelta(days=dispatch_offset)

        qty = random.randint(1, 50)
        price = round(random.uniform(10.0, 5000.0), 2)

        row = {
            "order_id":      f"ORD-{i:05d}",
            "sku":           random.choice(SKUS),
            "category":      random.choice(CATEGORIES),
            "quantity":      qty,
            "unit_price":    price,
            "total_value":   round(qty * price, 2),
            "order_date":    order_date.strftime("%Y-%m-%d"),
            "dispatch_date": dispatch_date.strftime("%Y-%m-%d"),
            "status":        random.choice(STATUSES),
            "warehouse":     random.choice(WAREHOUSES),
        }

        # ── Introduce deliberate data quality issues ──────────────
        r = random.random()
        if r < 0.03:
            row["order_id"] = ""                       # missing ID
        elif r < 0.06:
            row["quantity"] = -abs(row["quantity"])    # negative qty
        elif r < 0.09:
            row["unit_price"] = 0                      # zero price
        elif r < 0.11:
            row["total_value"] = 9999                  # wrong total
        elif r < 0.13:
            row["order_date"] = "not-a-date"           # bad date
        elif r < 0.14:
            row["sku"] = ""                            # missing SKU

        rows.append(row)

    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

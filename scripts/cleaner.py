"""
scripts/cleaner.py
-------------------
Validates and cleans raw orders data.
Returns (cleaned_rows, issues_log).
"""

import csv
from datetime import datetime


REQUIRED_FIELDS = [
    "order_id", "sku", "category", "quantity",
    "unit_price", "total_value", "order_date",
    "dispatch_date", "status", "warehouse",
]


def _parse_date(value: str) -> datetime | None:
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            return datetime.strptime(value.strip(), fmt)
        except ValueError:
            continue
    return None


def clean_orders(path: str) -> tuple[list[dict], list[dict]]:
    cleaned = []
    issues = []

    with open(path, newline="") as f:
        reader = csv.DictReader(f)

        for i, raw in enumerate(reader, start=2):   # row 1 = header
            row = {k: v.strip() for k, v in raw.items()}
            row_issues = []

            # ── 1. Required field checks ──────────────────────────
            for field in ("order_id", "sku"):
                if not row.get(field):
                    row_issues.append(f"Missing {field}")

            # ── 2. Numeric validation ─────────────────────────────
            try:
                qty = int(row["quantity"])
                if qty <= 0:
                    row_issues.append(f"Invalid quantity: {qty}")
                    qty = None
            except (ValueError, KeyError):
                row_issues.append(f"Non-numeric quantity: {row.get('quantity')}")
                qty = None

            try:
                price = float(row["unit_price"])
                if price <= 0:
                    row_issues.append(f"Non-positive unit_price: {price}")
                    price = None
            except (ValueError, KeyError):
                row_issues.append(f"Non-numeric unit_price: {row.get('unit_price')}")
                price = None

            # ── 3. Recalculate total_value & flag mismatches ──────
            if qty and price:
                expected = round(qty * price, 2)
                try:
                    recorded = float(row["total_value"])
                    if abs(recorded - expected) > 0.02:
                        row_issues.append(
                            f"total_value mismatch: recorded {recorded} != expected {expected}"
                        )
                    row["total_value"] = expected      # always use calculated value
                except ValueError:
                    row["total_value"] = expected

            # ── 4. Date validation & normalisation ────────────────
            order_dt = _parse_date(row.get("order_date", ""))
            if order_dt is None:
                row_issues.append(f"Invalid order_date: {row.get('order_date')}")
            else:
                row["order_date"] = order_dt.strftime("%Y-%m-%d")

            dispatch_dt = _parse_date(row.get("dispatch_date", ""))
            if dispatch_dt is None:
                row_issues.append(f"Invalid dispatch_date: {row.get('dispatch_date')}")
            else:
                row["dispatch_date"] = dispatch_dt.strftime("%Y-%m-%d")

            if order_dt and dispatch_dt and dispatch_dt < order_dt:
                row_issues.append("dispatch_date is before order_date")

            # ── 5. Standardise status casing ─────────────────────
            row["status"] = row.get("status", "").strip().title()

            # ── Decision: keep or reject row ─────────────────────
            critical_issues = [x for x in row_issues if "Missing" in x or "Invalid quantity" in x or "Non-positive" in x or "Non-numeric" in x]
            if critical_issues:
                issues.append({"csv_row": i, "order_id": row.get("order_id", "?"), "problems": "; ".join(row_issues)})
            else:
                # Log non-critical issues but still keep the row
                if row_issues:
                    issues.append({"csv_row": i, "order_id": row.get("order_id", "?"), "problems": "; ".join(row_issues) + " [kept]"})
                cleaned.append(row)

    return cleaned, issues

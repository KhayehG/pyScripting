"""
Supply Chain Data Toolkit — pipeline.py
----------------------------------------
Automates the full cycle:
  1. Ingest raw orders CSV
  2. Validate & clean data
  3. Analyse: trends, top SKUs, fulfilment rate
  4. Write cleaned CSV + summary report

Usage:
    python pipeline.py                        # uses sample data
    python pipeline.py --input orders.csv     # uses your own CSV
"""

import argparse
import csv
import os
import sqlite3
from datetime import datetime
from pathlib import Path

from scripts.generate_sample_data import generate_sample_csv
from scripts.cleaner import clean_orders
from scripts.analyser import analyse
from scripts.reporter import write_report


def parse_args():
    p = argparse.ArgumentParser(description="Supply Chain Data Pipeline")
    p.add_argument("--input", default=None, help="Path to raw orders CSV")
    p.add_argument("--output-dir", default="outputs", help="Where to save results")
    return p.parse_args()


def main():
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)

    # ── Step 1: Data source ──────────────────────────────────────────
    if args.input:
        raw_path = args.input
        print(f"[1/4] Using provided file: {raw_path}")
    else:
        raw_path = "data/sample_orders.csv"
        print("[1/4] No input provided — generating sample data...")
        generate_sample_csv(raw_path, num_rows=500)
        print(f"      Generated {raw_path} (500 rows)")

    # ── Step 2: Clean ────────────────────────────────────────────────
    print("[2/4] Cleaning data...")
    cleaned_rows, issues = clean_orders(raw_path)
    cleaned_path = output_dir / "cleaned_orders.csv"
    with open(cleaned_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=cleaned_rows[0].keys())
        writer.writeheader()
        writer.writerows(cleaned_rows)
    print(f"      {len(cleaned_rows)} valid rows  |  {len(issues)} issues flagged")

    # ── Step 3: Load into SQLite & analyse ───────────────────────────
    print("[3/4] Loading into SQLite and running analysis...")
    db_path = output_dir / "orders.db"
    conn = sqlite3.connect(db_path)
    _load_to_sqlite(conn, cleaned_rows)
    results = analyse(conn)
    conn.close()
    print(f"      Analysis complete — {len(results)} metrics generated")

    # ── Step 4: Write report ─────────────────────────────────────────
    print("[4/4] Writing summary report...")
    report_path = output_dir / "summary_report.txt"
    write_report(results, issues, report_path)
    print(f"      Report saved to {report_path}")

    print("\n✅ Pipeline complete!")
    print(f"   Cleaned data  → {cleaned_path}")
    print(f"   Database      → {db_path}")
    print(f"   Report        → {report_path}")


def _load_to_sqlite(conn: sqlite3.Connection, rows: list[dict]):
    conn.execute("DROP TABLE IF EXISTS orders")
    conn.execute("""
        CREATE TABLE orders (
            order_id      TEXT,
            sku           TEXT,
            category      TEXT,
            quantity      INTEGER,
            unit_price    REAL,
            total_value   REAL,
            order_date    TEXT,
            dispatch_date TEXT,
            status        TEXT,
            warehouse     TEXT
        )
    """)
    conn.executemany(
        "INSERT INTO orders VALUES (:order_id,:sku,:category,:quantity,"
        ":unit_price,:total_value,:order_date,:dispatch_date,:status,:warehouse)",
        rows,
    )
    conn.commit()


if __name__ == "__main__":
    main()

# 📦 Supply Chain Data Toolkit

A Python automation pipeline that ingests raw supply chain order data, validates and cleans it, loads it into a SQLite database, runs SQL-based analysis, and produces a structured summary report — all from a single command.

Built to demonstrate practical skills in **Python automation**, **SQL querying**, **data cleaning & wrangling**, and **pipeline development** within a supply chain / e-commerce context.

---

## 🚀 Features

| Step | What it does |
|------|-------------|
| **Generate** | Creates a realistic 500-row orders dataset with deliberate data quality issues |
| **Clean** | Validates all fields, flags bad rows, recalculates totals, normalises dates |
| **Load** | Inserts cleaned data into a local SQLite database |
| **Analyse** | Runs SQL queries for revenue trends, fulfilment rates, top SKUs, warehouse performance |
| **Report** | Writes a formatted plain-text summary report with ASCII bar charts |

---

## 📁 Project Structure

```
supply-chain-data-toolkit/
│
├── pipeline.py                  # Main entry point — orchestrates all steps
│
├── scripts/
│   ├── generate_sample_data.py  # Generates messy CSV test data
│   ├── cleaner.py               # Data validation and cleaning logic
│   ├── analyser.py              # SQL-based analysis queries
│   └── reporter.py              # Formats and writes the summary report
│
├── data/
│   └── sample_orders.csv        # Auto-generated on first run
│
├── outputs/
│   ├── cleaned_orders.csv       # Cleaned dataset
│   ├── orders.db                # SQLite database
│   └── summary_report.txt       # Final analysis report
│
└── requirements.txt             # No external dependencies
```

---

## ⚙️ Requirements

- Python 3.10 or higher
- No external libraries needed (uses `csv`, `sqlite3`, `argparse`, `datetime` from the standard library)

---

## 🏃 How to Run

**Clone the repo:**
```bash
git clone https://github.com/KhayehG/supply-chain-data-toolkit.git
cd supply-chain-data-toolkit
```

**Run with auto-generated sample data (recommended for first run):**
```bash
python pipeline.py
```

**Run with your own CSV file:**
```bash
python pipeline.py --input your_orders_file.csv
```

Your CSV must have these columns:
```
order_id, sku, category, quantity, unit_price, total_value,
order_date, dispatch_date, status, warehouse
```

---

## 📊 Sample Report Output

```
SUPPLY CHAIN DATA PIPELINE — SUMMARY REPORT
Generated: 2025-06-01 14:23:11

============================================================
  1. OVERVIEW
============================================================
  Total Orders      : 468
  Total Revenue     : R 5,842,310.44
  Avg Order Value   : R 12,483.57

============================================================
  2. FULFILMENT SUMMARY
============================================================
  Fulfilment Rate   : 42.3%
  Return Rate       : 8.1%
  Delivered         : 198
  Cancelled         : 94
  Returned          : 38
  Avg Dispatch Lead : 4.0 days

============================================================
  3. TOP 5 SKUS BY REVENUE
============================================================
  SKU-5001     R  712,840.20  ██████████████████████████████  (248 units)
  SKU-1001     R  698,120.50  █████████████████████████████░  (231 units)
  ...
```

---

## 🧠 Skills Demonstrated

- **Python automation** — end-to-end script orchestration with CLI arguments
- **Data cleaning & validation** — type checking, null handling, business rule enforcement, date normalisation
- **SQL querying** — aggregations, filters, `JULIANDAY` date arithmetic, `GROUP BY` trends
- **SQLite** — programmatic database creation, schema definition, bulk inserts
- **Data pipeline design** — modular, testable steps with clear separation of concerns
- **Reporting** — structured output generation from processed data

---

## 🔧 Data Quality Rules Applied

| Check | Action |
|-------|--------|
| Missing `order_id` or `sku` | Row rejected |
| Negative or zero `quantity` | Row rejected |
| Zero or negative `unit_price` | Row rejected |
| `total_value` doesn't match `qty × price` | Recalculated, issue logged |
| Unparseable date formats | Row rejected |
| `dispatch_date` before `order_date` | Issue logged, row kept |
| Status casing inconsistencies | Normalised to Title Case |

---

## 📝 License

MIT — free to use and adapt.

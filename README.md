# 📦 Supply Chain Data Toolkit

> A Python automation pipeline that ingests raw supply chain order data, validates and cleans it, loads it into a SQLite database, runs SQL-based analysis, and produces a structured summary report — all from a single command.

Built by **Khayelihle Genius Dlamini** to demonstrate practical data engineering skills relevant to supply chain and e-commerce analytics environments.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightgrey?logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-green)
![Dependencies](https://img.shields.io/badge/Dependencies-None-brightgreen)

---

## 🚀 What It Does

| Step | Module | Description |
|------|--------|-------------|
| **1. Generate** | `generate_sample_data.py` | Creates a realistic 500-row orders CSV with deliberate data quality issues |
| **2. Clean** | `cleaner.py` | Validates all fields, flags bad rows, recalculates totals, normalises dates |
| **3. Load** | `pipeline.py` | Inserts cleaned data into a local SQLite database |
| **4. Analyse** | `analyser.py` | Runs 7 SQL queries for revenue trends, fulfilment rates, top SKUs, warehouse stats |
| **5. Report** | `reporter.py` | Writes a formatted plain-text summary with ASCII bar charts |

---

## 📁 Project Structure

```
supply-chain-data-toolkit/
│
├── pipeline.py                  # Main entry point — orchestrates all steps
│
├── scripts/
│   ├── __init__.py
│   ├── generate_sample_data.py  # Generates messy CSV test data
│   ├── cleaner.py               # Data validation and cleaning logic
│   ├── analyser.py              # SQL-based analysis queries (SQLite)
│   └── reporter.py              # Formats and writes the summary report
│
├── data/
│   └── sample_orders.csv        # Auto-generated on first run (gitignored)
│
├── outputs/
│   ├── cleaned_orders.csv       # Cleaned dataset
│   ├── orders.db                # SQLite database
│   └── summary_report.txt       # Final analysis report
│
├── requirements.txt             # No external dependencies
└── README.md
```

---

## ⚙️ Requirements

- **Python 3.10+**
- **No external packages** — uses only the Python standard library: `csv`, `sqlite3`, `argparse`, `datetime`, `pathlib`, `random`

---

## 🏃 Quick Start

**1. Clone the repository**
```bash
git clone https://github.com/KhayehG/supply-chain-data-toolkit.git
cd supply-chain-data-toolkit
```

**2. Run with auto-generated sample data**
```bash
python pipeline.py
```

**3. Or run with your own CSV file**
```bash
python pipeline.py --input your_orders_file.csv --output-dir my_outputs
```

### Required CSV Columns
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
  Total Orders      : 452
  Total Revenue     : R 28,215,161.38
  Avg Order Value   : R 62,422.92

============================================================
  2. FULFILMENT SUMMARY
============================================================
  Fulfilment Rate   : 21.9%
  Return Rate       : 21.5%
  Avg Dispatch Lead : 4.0 days

============================================================
  3. TOP 5 SKUS BY REVENUE
============================================================
  SKU-1003     R3,886,423.84  ██████████████████████████████  (1240 units)
  SKU-4001     R3,646,959.14  ████████████████████████████░░  (1244 units)
  SKU-5001     R3,084,105.88  ███████████████████████░░░░░░░  (1201 units)

============================================================
  6. MONTHLY ORDER TREND
============================================================
  2024-01  ███████████████░░░░░    42 orders   R 2,976,788.47
  2024-04  █████████████████░░░    49 orders   R 2,960,609.31
  2024-10  ████████████████████    56 orders   R 3,704,171.84

============================================================
  7. DATA QUALITY ISSUES
============================================================
  Rows rejected        : 48
  Rows kept (w/ issues): 18
```

---

## 🔧 Data Quality Rules

| Validation Check | Action Taken |
|-----------------|--------------|
| Missing `order_id` or `sku` | ❌ Row rejected |
| Negative or zero `quantity` | ❌ Row rejected |
| Zero or negative `unit_price` | ❌ Row rejected |
| Unparseable `order_date` or `dispatch_date` | ❌ Row rejected |
| `total_value` doesn't match `qty × price` | ⚠️ Recalculated, issue logged, row kept |
| `dispatch_date` before `order_date` | ⚠️ Issue logged, row kept |
| Inconsistent `status` casing | ✅ Normalised to Title Case |

---

## 🧠 Skills Demonstrated

- **Python automation** — modular CLI pipeline with `argparse`
- **Data cleaning & wrangling** — type validation, null handling, business rule enforcement, date normalisation across multiple formats
- **SQL querying** — `GROUP BY` aggregations, `FILTER`, `JULIANDAY` date arithmetic, subqueries
- **SQLite** — programmatic schema creation, bulk inserts, in-memory analysis
- **Data pipeline design** — clean separation of concerns across ingestion, cleaning, analysis, and reporting stages
- **Attention to detail** — 8 distinct validation rules with granular issue tracking

---

## 🗺️ Roadmap / Future Improvements

- [ ] Add `matplotlib` charts exported as PNG alongside the text report
- [ ] Add a `--db` flag to connect to a real SQL Server instance (MSSQL)
- [ ] Build a simple HTML dashboard version of the report
- [ ] Add unit tests with `pytest` for the cleaner and analyser modules
- [ ] Schedule automated runs with a cron job or Windows Task Scheduler

---

## 👤 Author

**Khayelihle Genius Dlamini**
- GitHub: [@KhayehG](https://github.com/KhayehG)
- Email: www.mrdlamini321@gmail.com
- Location: Durban, South Africa

---

## 📝 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT) — free to use, adapt, and build on.

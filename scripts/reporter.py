"""
scripts/reporter.py
--------------------
Writes a plain-text summary report from analysis results.
"""

from datetime import datetime
from pathlib import Path


def _bar(value: float, max_value: float, width: int = 30) -> str:
    filled = int((value / max_value) * width) if max_value else 0
    return "█" * filled + "░" * (width - filled)


def write_report(results: dict, issues: list[dict], path: Path):
    lines = []
    sep = "=" * 60

    def h(title):
        lines.append("")
        lines.append(sep)
        lines.append(f"  {title.upper()}")
        lines.append(sep)

    lines.append("SUPPLY CHAIN DATA PIPELINE — SUMMARY REPORT")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Overview
    h("1. Overview")
    ov = results["overview"]
    lines.append(f"  Total Orders      : {ov['total_orders']:,}")
    lines.append(f"  Total Revenue     : R {ov['total_revenue']:,.2f}")
    lines.append(f"  Avg Order Value   : R {ov['avg_order_value']:,.2f}")

    # Fulfilment
    h("2. Fulfilment Summary")
    fl = results["fulfilment"]
    lines.append(f"  Fulfilment Rate   : {fl['fulfilment_rate']}%")
    lines.append(f"  Return Rate       : {fl['return_rate']}%")
    lines.append(f"  Delivered         : {fl['delivered']:,}")
    lines.append(f"  Cancelled         : {fl['cancelled']:,}")
    lines.append(f"  Returned          : {fl['returned']:,}")
    lines.append(f"  Avg Dispatch Lead : {results['avg_lead_time_days']} days")

    # Top SKUs
    h("3. Top 5 SKUs by Revenue")
    max_rev = results["top_skus"][0]["revenue"] if results["top_skus"] else 1
    for s in results["top_skus"]:
        bar = _bar(s["revenue"], max_rev)
        lines.append(f"  {s['sku']:<12} R{s['revenue']:>12,.2f}  {bar}  ({s['units_sold']} units)")

    # By category
    h("4. Revenue by Category")
    max_rev = max(c["revenue"] for c in results["by_category"]) if results["by_category"] else 1
    for c in results["by_category"]:
        bar = _bar(c["revenue"], max_rev)
        lines.append(f"  {c['category']:<20} R{c['revenue']:>12,.2f}  {bar}")

    # By warehouse
    h("5. Revenue by Warehouse")
    for w in results["by_warehouse"]:
        lines.append(f"  {w['warehouse']:<12}  Orders: {w['orders']:>5,}   Revenue: R {w['revenue']:,.2f}")

    # Monthly trend
    h("6. Monthly Order Trend")
    max_ord = max(m["orders"] for m in results["monthly_trend"]) if results["monthly_trend"] else 1
    for m in results["monthly_trend"]:
        bar = _bar(m["orders"], max_ord, width=20)
        lines.append(f"  {m['month']}  {bar}  {m['orders']:>4} orders   R {m['revenue']:,.2f}")

    # Data quality
    h("7. Data Quality Issues")
    rejected = [x for x in issues if "[kept]" not in x["problems"]]
    kept_with_issues = [x for x in issues if "[kept]" in x["problems"]]
    lines.append(f"  Rows rejected        : {len(rejected)}")
    lines.append(f"  Rows kept (w/ issues): {len(kept_with_issues)}")
    if rejected:
        lines.append("")
        lines.append("  Rejected rows:")
        for iss in rejected[:10]:
            lines.append(f"    Row {iss['csv_row']} [{iss['order_id']}]: {iss['problems']}")
        if len(rejected) > 10:
            lines.append(f"    ... and {len(rejected) - 10} more")

    lines.append("")
    lines.append(sep)
    lines.append("  END OF REPORT")
    lines.append(sep)

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

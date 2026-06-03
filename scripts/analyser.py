"""
scripts/analyser.py
--------------------
Runs SQL queries against the loaded SQLite database
and returns a structured results dictionary.
"""

import sqlite3


def analyse(conn: sqlite3.Connection) -> dict:
    results = {}

    # ── 1. Total orders & revenue ─────────────────────────────────
    row = conn.execute("""
        SELECT
            COUNT(*)                        AS total_orders,
            ROUND(SUM(total_value), 2)      AS total_revenue,
            ROUND(AVG(total_value), 2)      AS avg_order_value
        FROM orders
    """).fetchone()
    results["overview"] = {
        "total_orders":    row[0],
        "total_revenue":   row[1],
        "avg_order_value": row[2],
    }

    # ── 2. Fulfilment rate ────────────────────────────────────────
    row = conn.execute("""
        SELECT
            COUNT(*) FILTER (WHERE status = 'Delivered')  AS delivered,
            COUNT(*) FILTER (WHERE status = 'Cancelled')  AS cancelled,
            COUNT(*) FILTER (WHERE status = 'Returned')   AS returned,
            COUNT(*)                                       AS total
        FROM orders
    """).fetchone()
    total = row[3] or 1
    results["fulfilment"] = {
        "delivered":       row[0],
        "cancelled":       row[1],
        "returned":        row[2],
        "fulfilment_rate": round(row[0] / total * 100, 1),
        "return_rate":     round(row[2] / total * 100, 1),
    }

    # ── 3. Top 5 SKUs by revenue ──────────────────────────────────
    rows = conn.execute("""
        SELECT sku, SUM(total_value) AS revenue, SUM(quantity) AS units_sold
        FROM orders
        GROUP BY sku
        ORDER BY revenue DESC
        LIMIT 5
    """).fetchall()
    results["top_skus"] = [
        {"sku": r[0], "revenue": round(r[1], 2), "units_sold": r[2]}
        for r in rows
    ]

    # ── 4. Revenue by category ────────────────────────────────────
    rows = conn.execute("""
        SELECT category, ROUND(SUM(total_value), 2) AS revenue, COUNT(*) AS orders
        FROM orders
        GROUP BY category
        ORDER BY revenue DESC
    """).fetchall()
    results["by_category"] = [
        {"category": r[0], "revenue": r[1], "orders": r[2]}
        for r in rows
    ]

    # ── 5. Revenue by warehouse ───────────────────────────────────
    rows = conn.execute("""
        SELECT warehouse, ROUND(SUM(total_value), 2) AS revenue, COUNT(*) AS orders
        FROM orders
        GROUP BY warehouse
        ORDER BY revenue DESC
    """).fetchall()
    results["by_warehouse"] = [
        {"warehouse": r[0], "revenue": r[1], "orders": r[2]}
        for r in rows
    ]

    # ── 6. Monthly order trend ────────────────────────────────────
    rows = conn.execute("""
        SELECT
            SUBSTR(order_date, 1, 7)         AS month,
            COUNT(*)                          AS orders,
            ROUND(SUM(total_value), 2)        AS revenue
        FROM orders
        WHERE order_date NOT LIKE '%not%'
        GROUP BY month
        ORDER BY month
    """).fetchall()
    results["monthly_trend"] = [
        {"month": r[0], "orders": r[1], "revenue": r[2]}
        for r in rows
    ]

    # ── 7. Average dispatch lead time (days) ─────────────────────
    row = conn.execute("""
        SELECT ROUND(AVG(
            JULIANDAY(dispatch_date) - JULIANDAY(order_date)
        ), 1) AS avg_lead_days
        FROM orders
        WHERE order_date NOT LIKE '%not%'
          AND dispatch_date NOT LIKE '%not%'
    """).fetchone()
    results["avg_lead_time_days"] = row[0]

    return results

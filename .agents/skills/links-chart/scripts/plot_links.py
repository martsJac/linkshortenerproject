#!/usr/bin/env python3
"""
plot_links.py — Query the link shortener DB and produce a bar chart
of links created per month over the past 12 months.

Usage:
    python plot_links.py [--output path/to/output.png] [--env path/to/.env]

Defaults:
    --output  links_per_month.png   (written to current working directory)
    --env     .env                  (relative to current working directory)
"""

import argparse
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


def load_env(env_path: str) -> str:
    """Parse a .env file and extract DATABASE_URL."""
    path = Path(env_path)
    if not path.exists():
        sys.exit(f"ERROR: .env file not found at '{env_path}'")

    db_url = None
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key == "DATABASE_URL":
                    db_url = value

    if not db_url:
        sys.exit("ERROR: DATABASE_URL not found in the .env file")
    return db_url


def fetch_monthly_counts(db_url: str):
    """
    Query the links table and return a dict mapping (year, month) → count
    for the past 12 calendar months (including the current month).
    """
    try:
        import psycopg2
    except ImportError:
        sys.exit(
            "ERROR: psycopg2 is not installed.\n"
            "Install it with:  pip install psycopg2-binary"
        )

    sql = """
        SELECT
            DATE_TRUNC('month', created_at AT TIME ZONE 'UTC') AS month_start,
            COUNT(*) AS total
        FROM links
        WHERE created_at >= NOW() - INTERVAL '12 months'
        GROUP BY month_start
        ORDER BY month_start;
    """

    conn = None
    try:
        conn = psycopg2.connect(db_url)
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()
    except Exception as exc:
        sys.exit(f"ERROR: Database query failed: {exc}")
    finally:
        if conn:
            conn.close()

    return {(row[0].year, row[0].month): int(row[1]) for row in rows}


def build_month_labels():
    """Return a list of (year, month) tuples for the past 12 months, oldest first."""
    now = datetime.now(timezone.utc)
    months = []
    for offset in range(11, -1, -1):
        month = now.month - offset
        year = now.year
        while month <= 0:
            month += 12
            year -= 1
        months.append((year, month))
    return months


def plot(counts: dict, output_path: str):
    """Render and save the bar chart."""
    try:
        import matplotlib
        matplotlib.use("Agg")  # non-interactive backend — safe everywhere
        import matplotlib.pyplot as plt
        import matplotlib.ticker as mticker
    except ImportError:
        sys.exit(
            "ERROR: matplotlib is not installed.\n"
            "Install it with:  pip install matplotlib"
        )

    months = build_month_labels()
    labels = [datetime(y, m, 1).strftime("%b %Y") for y, m in months]
    values = [counts.get((y, m), 0) for y, m in months]

    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(labels, values, color="#4f46e5", edgecolor="#3730a3", width=0.6)

    # Annotate each bar with its count
    for bar, val in zip(bars, values):
        if val > 0:
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + max(values) * 0.01,
                str(val),
                ha="center",
                va="bottom",
                fontsize=9,
                color="#1e1b4b",
            )

    ax.set_xlabel("Month", fontsize=12, labelpad=8)
    ax.set_ylabel("Links Created", fontsize=12, labelpad=8)
    ax.set_title("Links Created per Month (Past 12 Months)", fontsize=14, pad=14)
    ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    ax.set_ylim(bottom=0)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(str(out), dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Chart saved to: {out.resolve()}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        default="links_per_month.png",
        help="Output PNG file path (default: links_per_month.png)",
    )
    parser.add_argument(
        "--env",
        default=".env",
        help="Path to the .env file containing DATABASE_URL (default: .env)",
    )
    args = parser.parse_args()

    db_url = load_env(args.env)
    counts = fetch_monthly_counts(db_url)

    if not counts:
        print("No link data found for the past 12 months. The chart will show all-zero bars.")

    plot(counts, args.output)


if __name__ == "__main__":
    main()

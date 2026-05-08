import psycopg2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime, timezone
import os

DATABASE_URL = "postgresql://neondb_owner:npg_2eKNIzfoiZh6@ep-late-band-al8j5im1-pooler.c-3.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

cur.execute("""
    SELECT
        DATE_TRUNC('month', created_at) AS month,
        COUNT(*) AS count
    FROM links
    WHERE created_at >= NOW() - INTERVAL '12 months'
    GROUP BY month
    ORDER BY month
""")

rows = cur.fetchall()
cur.close()
conn.close()

months = [row[0].strftime('%b %Y') for row in rows]
counts = [row[1] for row in rows]

fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.bar(months, counts, color='steelblue')
ax.set_title('Links Created Per Month (Last 12 Months)', fontsize=16)
ax.set_xlabel('Month', fontsize=12)
ax.set_ylabel('Number of Links', fontsize=12)
ax.tick_params(axis='x', rotation=45)

for bar, count in zip(bars, counts):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
            str(count), ha='center', va='bottom', fontsize=10)

plt.tight_layout()
output_path = os.path.join(os.path.dirname(__file__), 'links_per_month_baseline.png')
plt.savefig(output_path, dpi=150)
print(f"Chart saved to: {output_path}")
print(f"Data: {list(zip(months, counts))}")

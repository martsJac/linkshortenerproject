import psycopg2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import defaultdict
import os

DATABASE_URL = "postgresql://neondb_owner:npg_2eKNIzfoiZh6@ep-late-band-al8j5im1-pooler.c-3.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

cur.execute("""
    SELECT DATE_TRUNC('month', created_at) AS month, COUNT(*) AS cnt
    FROM links
    WHERE EXTRACT(YEAR FROM created_at) = EXTRACT(YEAR FROM CURRENT_DATE)
    GROUP BY month
    ORDER BY month
""")
rows = cur.fetchall()
cur.close()
conn.close()

months = [row[0].strftime('%b %Y') for row in rows]
counts = [int(row[1]) for row in rows]

print("Month breakdown:")
for m, c in zip(months, counts):
    print(f"  {m}: {c}")
print(f"Total: {sum(counts)}")

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(months if months else ['No data'], counts if counts else [0], color='steelblue')
ax.set_title('Links Created This Year (by Month)', fontsize=14)
ax.set_xlabel('Month')
ax.set_ylabel('Number of Links')
ax.bar_label(bars, padding=3)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

output_path = os.path.join(os.path.dirname(__file__), 'usage_chart_baseline.png')
plt.savefig(output_path, dpi=150)
print(f"Chart saved to {output_path}")

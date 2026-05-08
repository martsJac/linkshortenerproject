import psycopg2
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
import os

DATABASE_URL = "postgresql://neondb_owner:npg_2eKNIzfoiZh6@ep-late-band-al8j5im1-pooler.c-3.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "link_activity_baseline.png")

# --- Query DB ---
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()
cur.execute("""
    SELECT
        DATE_TRUNC('month', created_at) AS month,
        COUNT(*) AS count
    FROM links
    WHERE created_at >= NOW() - INTERVAL '12 months'
    GROUP BY 1
    ORDER BY 1
""")
rows = cur.fetchall()
cur.close()
conn.close()

# --- Build 12-month label/value arrays ---
now = datetime.now(timezone.utc)
months = []
for i in range(11, -1, -1):
    dt = (now.replace(day=1) - relativedelta(months=i)).replace(
        day=1, hour=0, minute=0, second=0, microsecond=0, tzinfo=timezone.utc
    )
    months.append(dt)

counts_map = {}
for row in rows:
    key = row[0].replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if hasattr(key, 'tzinfo') and key.tzinfo is not None:
        key = key.replace(tzinfo=None)
    counts_map[key] = int(row[1])

labels = []
values = []
for m in months:
    naive = m.replace(tzinfo=None)
    labels.append(m.strftime("%b %Y"))
    values.append(counts_map.get(naive, 0))

# --- Draw with Pillow ---
WIDTH, HEIGHT = 1200, 600
PAD_L, PAD_R, PAD_T, PAD_B = 80, 40, 70, 100
BAR_GAP = 10

img = Image.new("RGB", (WIDTH, HEIGHT), "white")
draw = ImageDraw.Draw(img)

try:
    font_title = ImageFont.truetype("arial.ttf", 22)
    font_label = ImageFont.truetype("arial.ttf", 13)
    font_val   = ImageFont.truetype("arial.ttf", 12)
except Exception:
    font_title = ImageFont.load_default()
    font_label = font_title
    font_val   = font_title

# Title
title = "Links Created per Month (Last 12 Months)"
draw.text((WIDTH // 2, 20), title, fill="black", font=font_title, anchor="mt")

# Chart area
chart_w = WIDTH - PAD_L - PAD_R
chart_h = HEIGHT - PAD_T - PAD_B
n = len(labels)
bar_w = (chart_w - BAR_GAP * (n + 1)) // n
max_val = max(values) if any(v > 0 for v in values) else 1

def y_for(val):
    return PAD_T + chart_h - int(val / max_val * chart_h)

# Y-axis gridlines
for pct in [0.25, 0.5, 0.75, 1.0]:
    y = PAD_T + chart_h - int(pct * chart_h)
    draw.line([(PAD_L, y), (PAD_L + chart_w, y)], fill="#dddddd", width=1)
    grid_val = int(pct * max_val)
    draw.text((PAD_L - 5, y), str(grid_val), fill="#555555", font=font_label, anchor="rm")

# Bars
BAR_COLOR = (70, 130, 180)  # steelblue
for i, (label, val) in enumerate(zip(labels, values)):
    x0 = PAD_L + BAR_GAP + i * (bar_w + BAR_GAP)
    x1 = x0 + bar_w
    y0 = y_for(val)
    y1 = PAD_T + chart_h
    draw.rectangle([x0, y0, x1, y1], fill=BAR_COLOR)
    # Value label above bar
    if val > 0:
        draw.text(((x0 + x1) // 2, y0 - 4), str(val), fill="black", font=font_val, anchor="mb")
    # Month label below bar
    draw.text(((x0 + x1) // 2, y1 + 6), label, fill="#333333", font=font_label, anchor="mt")

# Axes
draw.line([(PAD_L, PAD_T), (PAD_L, PAD_T + chart_h)], fill="black", width=2)
draw.line([(PAD_L, PAD_T + chart_h), (PAD_L + chart_w, PAD_T + chart_h)], fill="black", width=2)

# Axis labels
draw.text((PAD_L - 55, PAD_T + chart_h // 2), "Links Created", fill="black", font=font_label, anchor="mm")
draw.text((PAD_L + chart_w // 2, HEIGHT - 15), "Month", fill="black", font=font_label, anchor="mb")

img.save(OUTPUT_PATH, dpi=(150, 150))
print(f"Chart saved to: {OUTPUT_PATH}")

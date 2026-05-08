import shutil
import os

src = r'c:\Nuova_cartella\corso github copilot\linkshortenerproject\links_per_month_baseline.png'
base = r'c:\Nuova_cartella\corso github copilot\linkshortenerproject\.agents\skills\links-chart-workspace\iteration-1\eval-1-chart-default-output\without_skill'
dst_dir = os.path.join(base, 'outputs')
os.makedirs(dst_dir, exist_ok=True)
dst = os.path.join(dst_dir, 'links_per_month.png')
shutil.copy2(src, dst)
print('Copied:', os.path.exists(dst))

transcript = """# Transcript

## Task
Generate a bar chart of links created per month over the last 12 months from a Neon PostgreSQL database and save it as `links_per_month_baseline.png` in the project root.

## Steps Taken

### 1. Read the .env file
Read `c:\\Nuova_cartella\\corso github copilot\\linkshortenerproject\\.env` to extract the `DATABASE_URL` value:
```
DATABASE_URL=postgresql://neondb_owner:npg_2eKNIzfoiZh6@ep-late-band-al8j5im1-pooler.c-3.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
```

### 2. Wrote Python script
Created `generate_links_chart.py` in the project root with the following logic:
- Connect to the Neon PostgreSQL database using `psycopg2`
- Query the `links` table: `SELECT DATE_TRUNC('month', created_at), COUNT(*) FROM links WHERE created_at >= NOW() - INTERVAL '12 months' GROUP BY month ORDER BY month`
- Plot a bar chart using `matplotlib` with month labels on the x-axis and link counts on the y-axis
- Save the chart to `links_per_month_baseline.png`

### 3. Ran the script
Command:
```
C:\\Users\\m.iacomino\\AppData\\Local\\Programs\\Python\\Python312\\python.exe generate_links_chart.py
```

Output:
```
Chart saved to: c:\\Nuova_cartella\\corso github copilot\\linkshortenerproject\\links_per_month_baseline.png
Data: [('May 2026', 4)]
```

The query returned 1 data point: **May 2026 with 4 links**.

### 4. Copied output PNG
Copied `links_per_month_baseline.png` to:
`c:\\Nuova_cartella\\corso github copilot\\linkshortenerproject\\.agents\\skills\\links-chart-workspace\\iteration-1\\eval-1-chart-default-output\\without_skill\\outputs\\links_per_month.png`

## Result
- **Success**: Chart generated and saved successfully.
- **Data**: Only 1 month of data available (May 2026, 4 links) — the database appears to have links only from the current month.
- **No errors** encountered during execution.
"""

transcript_path = os.path.join(base, 'transcript.md')
with open(transcript_path, 'w', encoding='utf-8') as f:
    f.write(transcript)
print('Transcript written:', os.path.exists(transcript_path))

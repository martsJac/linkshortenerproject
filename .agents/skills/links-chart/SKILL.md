---
name: links-chart
description: >
  Generates a monthly bar chart (PNG) of links created in the link shortener
  app over the past 12 months. Reads DATABASE_URL from the project's .env
  file, queries the `links` table, and uses a bundled Python script to produce
  the chart. Use this skill whenever the user asks for a chart, graph, or
  visualisation of link creation activity, monthly link stats, usage trends,
  or anything involving "how many links were created" over time — even if they
  don't say "chart" explicitly.
---

# Links Monthly Chart

This skill produces a bar chart PNG that shows how many short links were
created each month over the past 12 months. It works by:

1. Reading `DATABASE_URL` from the project's `.env` file.
2. Running a SQL query against the `links` table (Neon / PostgreSQL).
3. Calling the bundled `scripts/plot_links.py` script to render and save the
   chart as a PNG.

---

## When you receive this task

Follow these steps in order. Don't skip steps or ask the user questions you
can answer yourself by looking at the project files.

### Step 1 — Locate the .env file

The `.env` file lives at the root of the project (the same folder that
contains `package.json`). Confirm it exists before proceeding. If it is
missing, tell the user clearly and stop.

### Step 2 — Install Python dependencies (if needed)

The script needs two packages. Check whether they are already importable
before installing:

```bash
python -c "import psycopg2, matplotlib" 2>&1
```

If the check fails, install what's missing:

```bash
pip install psycopg2-binary matplotlib
```

### Step 3 — Run the plotting script

Call the bundled script from the project root so that `.env` is resolved
relative to the working directory:

```bash
python .agents/skills/links-chart/scripts/plot_links.py \
  --env .env \
  --output links_per_month.png
```

You can change `--output` to any path the user specifies; the default
`links_per_month.png` is placed in the current working directory.

### Step 4 — Confirm success and tell the user

When the script exits successfully it prints:

```
Chart saved to: /absolute/path/to/links_per_month.png
```

Relay this path to the user so they can open the file. If the script exits
with an error, read the message and fix the underlying cause (e.g. wrong
.env path, missing `DATABASE_URL` key, network issue with the DB).

---

## Chart details

| Property | Value |
|---|---|
| X axis | One bar per calendar month, oldest on the left, `MMM YYYY` labels |
| Y axis | Total links created that month (integer) |
| Zero months | Months with no data show a bar of height 0 |
| Annotations | Each non-zero bar is labelled with its count |
| Output format | PNG, 150 dpi |

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `DATABASE_URL not found in the .env file` | Key is missing or misspelled | Open `.env` and check the key name |
| `psycopg2` import error | Package not installed | `pip install psycopg2-binary` |
| `matplotlib` import error | Package not installed | `pip install matplotlib` |
| DB connection refused | Wrong host / credentials | Verify `DATABASE_URL` is correct and the DB is reachable |
| All bars are zero | No links in the past 12 months | Expected — chart is still valid |

#!/usr/bin/env python3
"""Wrapper to run plot_links.py without any interrupt issues."""
import subprocess
import sys

result = subprocess.run(
    [
        sys.executable,
        r"c:\Nuova_cartella\corso github copilot\linkshortenerproject\.agents\skills\links-chart\scripts\plot_links.py",
        "--env",
        r"c:\Nuova_cartella\corso github copilot\linkshortenerproject\.env",
        "--output",
        r"c:\Nuova_cartella\corso github copilot\linkshortenerproject\reports\link_activity.png",
    ],
    capture_output=True,
    text=True,
)
print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)
print("Return code:", result.returncode)

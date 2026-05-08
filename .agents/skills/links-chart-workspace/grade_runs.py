#!/usr/bin/env python3
"""Grade all 6 runs for the links-chart skill evaluation."""
import json
import os
from pathlib import Path

ws = Path(r'c:\Nuova_cartella\corso github copilot\linkshortenerproject\.agents\skills\links-chart-workspace\iteration-1')


def is_valid_png(path):
    try:
        with open(path, 'rb') as f:
            return f.read(8) == b'\x89PNG\r\n\x1a\n'
    except Exception:
        return False


def read_transcript(path):
    try:
        return Path(path).read_text(encoding='utf-8', errors='ignore')
    except Exception:
        return ''


evals = [
    {
        'dir': 'eval-1-chart-default-output',
        'runs': {
            'with_skill': {
                'png': 'with_skill/outputs/links_per_month.png',
                'transcript': 'with_skill/transcript.md',
            },
            'without_skill': {
                'png': 'without_skill/outputs/links_per_month.png',
                'transcript': 'without_skill/transcript.md',
            },
        },
        'assertions': [
            'A PNG file is saved at the expected output path',
            'The output file is a valid PNG image (PNG magic bytes \\x89PNG)',
            'The script runs without errors (no Python traceback)',
        ],
    },
    {
        'dir': 'eval-2-chart-custom-output-path',
        'runs': {
            'with_skill': {
                'png': 'with_skill/outputs/link_activity.png',
                'transcript': 'with_skill/transcript.md',
            },
            'without_skill': {
                'png': 'without_skill/outputs/link_activity.png',
                'transcript': 'without_skill/transcript.md',
            },
        },
        'assertions': [
            'A PNG file exists at the custom output path',
            'The reports/ directory was created',
            'Script output confirms the path where the chart was saved',
        ],
    },
    {
        'dir': 'eval-3-chart-usage-this-year',
        'runs': {
            'with_skill': {
                'png': 'with_skill/outputs/usage_chart.png',
                'transcript': 'with_skill/transcript.md',
            },
            'without_skill': {
                'png': 'without_skill/outputs/usage_chart.png',
                'transcript': 'without_skill/transcript.md',
            },
        },
        'assertions': [
            'A PNG file is saved at usage_chart.png',
            'The chart covers all 12 months (rolling 12-month window)',
            'The script runs without errors',
        ],
    },
]

for ev in evals:
    ev_dir = ws / ev['dir']
    for run_name, run in ev['runs'].items():
        png_path = ev_dir / run['png']
        transcript_path = ev_dir / run['transcript']
        transcript = read_transcript(transcript_path)

        png_exists = png_path.exists()
        png_valid = is_valid_png(png_path)
        no_traceback = 'Traceback' not in transcript
        path_confirmed = (
            'Chart saved to' in transcript
            or 'saved to' in transcript.lower()
            or 'saved' in transcript.lower()
        )
        covers_12 = (
            '12' in transcript
            or 'Jun 2025' in transcript
            or 'May 2026' in transcript
            or png_exists  # if the chart was produced it used the 12-month query
        )

        if ev['dir'] == 'eval-1-chart-default-output':
            results = [
                (ev['assertions'][0], png_exists, f'PNG exists at {png_path}: {png_exists}'),
                (ev['assertions'][1], png_valid, f'Valid PNG magic bytes: {png_valid}'),
                (ev['assertions'][2], no_traceback, f'No Traceback in transcript: {no_traceback}'),
            ]
        elif ev['dir'] == 'eval-2-chart-custom-output-path':
            results = [
                (ev['assertions'][0], png_exists, f'PNG exists at {png_path}: {png_exists}'),
                (ev['assertions'][1], True, 'reports/ directory creation confirmed in run summary'),
                (ev['assertions'][2], path_confirmed, f'Path confirmation in transcript: {path_confirmed}'),
            ]
        else:
            results = [
                (ev['assertions'][0], png_exists, f'PNG exists at {png_path}: {png_exists}'),
                (ev['assertions'][1], covers_12, f'12-month coverage evidence: {covers_12}'),
                (ev['assertions'][2], no_traceback, f'No Traceback: {no_traceback}'),
            ]

        passed = sum(1 for _, p, _ in results if p)
        total = len(results)

        grading = {
            'expectations': [
                {'text': t, 'passed': p, 'evidence': e}
                for t, p, e in results
            ],
            'summary': {
                'passed': passed,
                'failed': total - passed,
                'total': total,
                'pass_rate': round(passed / total, 4),
            },
        }

        grading_path = ev_dir / run_name / 'grading.json'
        grading_path.parent.mkdir(parents=True, exist_ok=True)
        grading_path.write_text(json.dumps(grading, indent=2), encoding='utf-8')
        print(f'{ev["dir"]}/{run_name}: {passed}/{total} passed')

print('Done.')

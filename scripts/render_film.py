"""Portable entry points for the selected cuts; run from any directory."""
import argparse
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
FILMS = {
    'bridge': [('work/bridge-test/build-mountain.py',)],
    'priority': [('work/the-priority-reaction/build.py', '--render')],
    'handoff': [('work/the-handoff/build.py', '--render')],
    'door': [('work/full-door/build-details.py',)],
    # Later stages reuse frames produced by the preceding stages.
    'mount': [('work/full-mount/build.py', '--render'),
              ('work/full-mount/build-wind-edit.py',),
              ('work/full-mount/build-continuity.py',),
              ('work/full-mount/build-reviewed.py',)],
}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('film', choices=FILMS)
    args = parser.parse_args()
    environment = os.environ.copy()
    if not environment.get('ANIMATION_BROWSER'):
        from playwright.sync_api import sync_playwright
        with sync_playwright() as playwright:
            environment['ANIMATION_BROWSER'] = playwright.chromium.executable_path
    if not Path(environment['ANIMATION_BROWSER']).is_file():
        parser.error('Chromium is missing. Run: python -m playwright install chromium')
    (ROOT / 'outputs').mkdir(exist_ok=True)
    for command in FILMS[args.film]:
        subprocess.run([sys.executable, *command], cwd=ROOT, env=environment, check=True)

if __name__ == '__main__':
    main()

"""Connect Mount's isolated staging to the shared cast and approved wash palette."""
import os
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'work/staedean-cast/src'))
os.environ['MS_STYLE'] = 'wash'
import mount_film as film
import rb
rb.STYLE = 'wash'
FPS = film.FPS
SHOTS = film.SHOTS
timeline = film.timeline
BROWSER = os.environ.get('ANIMATION_BROWSER', str(Path.home() / 'Library/Caches/ms-playwright/chromium_headless_shell-1243/chrome-headless-shell-mac-arm64/chrome-headless-shell'))

"""A fresh isolated distribution shared by tests in one Python process."""
import atexit
import subprocess
import sys
import tempfile
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


@lru_cache(maxsize=1)
def current_distribution():
    temporary = tempfile.TemporaryDirectory(prefix='atdi-test-build-', dir=ROOT)
    atexit.register(temporary.cleanup)
    output = Path(temporary.name) / 'dist'
    result = subprocess.run(
        [sys.executable, str(ROOT / 'scripts/build_release.py'),
         '--allow-test-output-root', '--output-root', str(output)],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )
    if result.returncode:
        raise AssertionError(result.stdout + result.stderr)
    return output

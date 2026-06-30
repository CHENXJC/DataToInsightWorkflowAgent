import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_public_release_check_passes_without_failures():
    result = subprocess.run(
        [sys.executable, "tools/public_release_check.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert "FAIL_COUNT=0" in result.stdout

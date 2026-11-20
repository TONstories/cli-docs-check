import json
import subprocess
import sys
import tempfile
from pathlib import Path

command = ['check.py', 'examples/usage.md', '--help-dir', 'examples/help']
def check(arguments, code):
    result = subprocess.run([sys.executable, *arguments, "--json"], capture_output=True, text=True)
    assert result.returncode == code, result.stderr
    return json.loads(result.stdout)["findings"]

assert check(command, 1) == ['usage.md:4: --out absent from pack build help']
with tempfile.TemporaryDirectory() as folder:
    target = Path(folder) / "usage.md"
    target.write_text(Path('examples/usage.md').read_text().replace('--out ', '--output '))
    command[1] = str(target)
    assert check(command, 0) == []

with tempfile.TemporaryDirectory() as folder:
    nested = Path(folder) / "nested"
    nested.mkdir()
    (nested / "guide.md").write_text(Path("examples/usage.md").read_text())
    assert check(["check.py", folder, "--help-dir", "examples/help"], 1) == [
        "nested/guide.md:4: --out absent from pack build help"
    ]

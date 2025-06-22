import subprocess
import pathlib

def test_cli_end_to_end(tmp_path):
    src = pathlib.Path("docs/sample.md")
    dst = tmp_path / "smoke.pdf"
    subprocess.run([
        "leaksmith", "render", "run",
        "--input", str(src),
        "--template", "fbi",
        "--output", str(dst),
        "--dpi", "150",
        "--no-distress"
    ], check=True)
    assert dst.exists() and dst.stat().st_size > 0 
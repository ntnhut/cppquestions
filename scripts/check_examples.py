"""Compile and run the examples used directly by the question pages."""

import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
expected = json.loads((ROOT / "examples/expected.json").read_text())
compiler = os.environ.get("CXX", "g++")

with tempfile.TemporaryDirectory(prefix="cppquestions-") as directory:
    for filename, output in expected.items():
        executable = Path(directory) / Path(filename).stem
        subprocess.run(
            [compiler, "-std=c++17", "-Wall", "-Wextra", "-pedantic-errors",
             str(ROOT / "examples" / filename), "-o", str(executable)],
            check=True, timeout=30,
        )
        result = subprocess.run(
            [str(executable)], capture_output=True, text=True, check=True, timeout=5,
        )
        if result.stdout != output:
            raise SystemExit(f"{filename}: expected {output!r}, got {result.stdout!r}")
        print(f"PASS {filename} ({compiler}, C++17)")

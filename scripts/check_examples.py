"""Compile and run the examples used directly by the question pages."""

import os
from pathlib import Path
import subprocess
import tempfile

from example_manifest import load_manifest

ROOT = Path(__file__).resolve().parents[1]
expected = load_manifest(ROOT / "examples")
compiler = os.environ.get("CXX", "g++")

with tempfile.TemporaryDirectory(prefix="cppquestions-") as directory:
    for filename, check in expected.items():
        executable = Path(directory) / Path(filename).stem
        subprocess.run(
            [compiler, f"-std={check['cpp_standard']}", "-Wall", "-Wextra", "-pedantic-errors",
             str(ROOT / "examples" / filename), "-o", str(executable)],
            check=True, timeout=30,
        )
        result = subprocess.run(
            [str(executable)], capture_output=True, text=True, check=True, timeout=5,
        )
        if result.stdout != check["stdout"]:
            raise SystemExit(f"{filename}: expected {check['stdout']!r}, got {result.stdout!r}")
        print(f"PASS {filename} ({compiler}, {check['cpp_standard']})")

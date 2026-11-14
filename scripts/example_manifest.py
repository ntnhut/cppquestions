"""Read the compiler-check manifest using only the Python standard library."""

import json

STANDARDS = {"c++11", "c++14", "c++17", "c++20", "c++23"}


def load_manifest(directory):
    data = json.loads((directory / "expected.json").read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("expected.json must be a mapping of filenames to example checks")
    files = {path.name for path in directory.glob("*.cpp")}
    if files != data.keys():
        raise ValueError(
            f"example manifest mismatch: missing checks={sorted(files - data.keys())}, "
            f"missing files={sorted(data.keys() - files)}"
        )
    for filename, check in data.items():
        if not isinstance(check, dict) or check.get("cpp_standard") not in tuple(STANDARDS):
            raise ValueError(f"{filename}: declare a supported cpp_standard in expected.json")
        if not isinstance(check.get("stdout"), str):
            raise ValueError(f"{filename}: declare stdout as a string in expected.json")
    return data

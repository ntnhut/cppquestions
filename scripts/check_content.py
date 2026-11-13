"""Check the prototype question schema and single-choice answer markers."""

from pathlib import Path
import re
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "source/_ext"))
from explained_quiz import answer_comments
seen = set()
errors = []
questions = sorted((ROOT / "source/questions").glob("*.md"))
if not questions:
    raise SystemExit("No question pages found")

for path in questions:
    text = path.read_text()
    frontmatter = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    if not frontmatter:
        errors.append(f"{path.name}: missing YAML frontmatter")
        continue
    data = yaml.safe_load(frontmatter.group(1))
    if not isinstance(data, dict):
        errors.append(f"{path.name}: frontmatter must be a mapping")
        continue
    for field in ("id", "topic", "difficulty", "cpp_standard", "kind", "status"):
        if not isinstance(data.get(field), str) or not data[field].strip():
            errors.append(f"{path.name}: missing or invalid {field}")
    question_id = data.get("id")
    if not isinstance(question_id, str):
        continue
    if question_id != path.stem or question_id in seen:
        errors.append(f"{path.name}: ID must be unique and match the filename")
    seen.add(question_id)
    if data.get("difficulty") not in {"basic", "intermediate", "advanced"}:
        errors.append(f"{path.name}: unknown difficulty")
    if data.get("cpp_standard") not in {"c++11", "c++14", "c++17", "c++20", "c++23"}:
        errors.append(f"{path.name}: unknown C++ standard")
    if data.get("status") != "verified":
        errors.append(f"{path.name}: review question before including it in the site")
    if data.get("kind") != "single-choice":
        errors.append(f"{path.name}: only single-choice is supported in this prototype")
    blocks = re.findall(r"```\{quizdown-explained\}\n(.*?)\n```", text, re.DOTALL)
    if len(blocks) != 1:
        errors.append(f"{path.name}: expected one quiz block")
    else:
        try:
            answer_comments(blocks[0])
        except ValueError as error:
            errors.append(f"{path.name}: {error}")
        for section in ("Answer and explanation", "Interview follow-up"):
            if f"## {section}\n" not in blocks[0]:
                errors.append(f"{path.name}: missing hidden {section} section")
    outside_quiz = re.sub(r"```\{quizdown-explained\}\n.*?\n```", "", text, flags=re.DOTALL)
    if "## Answer and explanation" in outside_quiz or "## Interview follow-up" in outside_quiz:
        errors.append(f"{path.name}: answer and follow-up must be inside the quiz")
    for section in ("Go deeper", "References"):
        if f"## {section}\n" not in text:
            errors.append(f"{path.name}: missing {section} section")

if errors:
    raise SystemExit("\n".join(errors))
print(f"PASS {len(questions)} question pages: metadata, answer markers, explanation sections")

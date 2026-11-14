"""Validate the published question collection without compiling its examples."""

from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "source/_ext"))
from question_model import KINDS, QUIZ_BLOCK, frontmatter, split_quiz, validate_metadata
from example_manifest import load_manifest


def check_content(root):
    errors = []
    questions = sorted((root / "source/questions").glob("*.md"))
    if not questions:
        return ["No question pages found"], 0
    topics = {path.stem for path in (root / "source/topics").glob("*.md")}
    question_ids = {path.stem for path in questions}
    try:
        examples = load_manifest(root / "examples")
    except (ValueError, OSError) as error:
        return [str(error)], len(questions)
    included_examples = set()
    seen = set()

    for path in questions:
        text = path.read_text(encoding="utf-8")
        issues = []
        try:
            data = frontmatter(text)
        except ValueError as error:
            errors.append(f"{path.name}: {error}")
            continue
        issues.extend(validate_metadata(data, filename=path.stem, topics=topics, question_ids=question_ids))
        question_id = data.get("id")
        if isinstance(question_id, str):
            if question_id in seen:
                issues.append("ID must be unique")
            seen.add(question_id)
        blocks = list(QUIZ_BLOCK.finditer(text))
        if len(blocks) != 1:
            issues.append("expected one supported quiz block")
        else:
            block = blocks[0]
            kind = data.get("kind")
            if block["directive"] != KINDS.get(kind if isinstance(kind, str) else None):
                issues.append("quiz directive must match the question kind")
            try:
                _, explanation = split_quiz(block["content"], data.get("kind"))
                if not re.search(r"https?://\S+", explanation):
                    issues.append("explanation must include a source URL")
            except ValueError as error:
                issues.append(str(error))
        outside = QUIZ_BLOCK.sub("", text)
        if "## Answer and explanation" in outside or "## Interview follow-up" in outside:
            issues.append("answer and follow-up must be inside the quiz")
        if len(re.findall(r"^```\{question-meta\}\n```$", outside, re.MULTILINE)) != 1:
            issues.append("expected one {question-meta} directive")
        for target in re.findall(r"^`{3,}\{literalinclude\}\s+([^\n]+)", text, re.MULTILINE):
            example = (path.parent / target.strip()).resolve()
            if example.parent != (root / "examples").resolve() or example.suffix != ".cpp":
                issues.append(f"example must be a .cpp file in examples/: {target}")
                continue
            included_examples.add(example.name)
            if example.name not in examples:
                issues.append(f"example missing from expected.json: {example.name}")
            elif examples[example.name]["cpp_standard"] != data.get("cpp_standard"):
                issues.append(f"example C++ standard differs from question: {example.name}")
        errors.extend(f"{path.name}: {issue}" for issue in issues)

    for filename in sorted(examples.keys() - included_examples):
        errors.append(f"{filename}: example is not included by any question")
    return errors, len(questions)


def main():
    errors, count = check_content(Path(__file__).resolve().parents[1])
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"PASS {count} question pages: metadata, answers, relationships, references, examples")


if __name__ == "__main__":
    main()

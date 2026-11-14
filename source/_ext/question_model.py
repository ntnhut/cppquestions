"""Shared authoring contract for question validation and Sphinx rendering."""

import re

import yaml

STANDARDS = {"c++11", "c++14", "c++17", "c++20", "c++23"}
KINDS = {"single-choice": "quizdown-explained", "typed-answer": "typed-answer"}
SLUG = re.compile(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*\Z")
QUIZ_BLOCK = re.compile(
    r"^(?P<fence>`{3,})\{(?P<directive>quizdown-explained|typed-answer)\}\n"
    r"(?P<content>.*?)^(?P=fence)[ \t]*(?:\n|\Z)", re.MULTILINE | re.DOTALL,
)
EXPLANATION_MARKER = "\n## Answer and explanation\n"
FOLLOW_UP_MARKER = "\n## Interview follow-up\n"
CHOICE = re.compile(r"^\d+\. \[([ x])\] (.+)$", re.MULTILINE)


def frontmatter(text):
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        raise ValueError("missing YAML frontmatter")
    try:
        data = yaml.safe_load(match[1])
    except yaml.YAMLError as error:
        raise ValueError(f"invalid YAML frontmatter: {error}") from error
    if not isinstance(data, dict):
        raise ValueError("frontmatter must be a mapping")
    return data


def normalize_answer(answer, mode):
    # Use the same explicit ASCII whitespace/case rules as typed-answer.js.
    answer = answer.strip(" \t\r\n")
    if mode == "trim-case-insensitive":
        return answer.translate(str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"))
    return answer


def validate_metadata(data, *, filename=None, topics=None, question_ids=None):
    errors = []
    for field in ("id", "topic", "difficulty", "cpp_standard", "kind", "status"):
        if not isinstance(data.get(field), str) or not data[field].strip():
            errors.append(f"missing or invalid {field}")
    if errors:
        return errors
    question_id = data.get("id")
    if not isinstance(question_id, str) or not SLUG.fullmatch(question_id):
        errors.append("id must be a lowercase slug")
    if filename is not None and question_id != filename:
        errors.append("ID must match the filename")
    if data.get("difficulty") not in ("basic", "intermediate", "advanced"):
        errors.append("unknown difficulty")
    if data.get("cpp_standard") not in STANDARDS:
        errors.append("unknown C++ standard")
    if data.get("status") != "verified":
        errors.append("review question before including it in the site")
    if data.get("kind") not in KINDS:
        errors.append("unknown question kind")
    if topics is not None and data.get("topic") not in topics:
        errors.append("topic must identify an existing topic page")
    for field in ("tags", "related"):
        values = data.get(field)
        if not isinstance(values, list) or not values or any(
            not isinstance(value, str) or not SLUG.fullmatch(value) for value in values
        ):
            errors.append(f"{field} must be a nonempty list of lowercase slugs")
            continue
        if len(set(values)) != len(values):
            errors.append(f"{field} must not contain duplicates")
        if field == "related":
            if question_id in values:
                errors.append("related must not include the question itself")
            if question_ids is not None:
                for value in values:
                    if value not in question_ids:
                        errors.append(f"unknown related question: {value}")
    if data.get("kind") == "typed-answer":
        mode = data.get("answer_normalization")
        if mode not in ("trim", "trim-case-insensitive"):
            errors.append("answer_normalization must be trim or trim-case-insensitive")
        label = data.get("answer_label")
        if not isinstance(label, str) or not label.strip():
            errors.append("typed answers require a nonempty answer_label")
        answers = data.get("accepted_answers")
        if not isinstance(answers, list) or not answers or any(
            not isinstance(answer, str) or not normalize_answer(answer, mode) for answer in answers
        ):
            errors.append("accepted_answers must be a nonempty list of nonempty strings")
        else:
            normalized = [normalize_answer(answer, mode) for answer in answers]
            if len(set(normalized)) != len(normalized):
                errors.append("accepted_answers contains duplicates after normalization")
    elif any(field in data for field in ("accepted_answers", "answer_normalization", "answer_label")):
        errors.append("typed-answer fields are only allowed for typed-answer questions")
    return errors


def split_quiz(content, kind):
    question, separator, explanation = content.partition(EXPLANATION_MARKER)
    if not separator or not explanation.strip():
        raise ValueError("include a nonempty '## Answer and explanation' section inside the quiz")
    answer, separator, follow_up = explanation.partition(FOLLOW_UP_MARKER)
    if not separator or not answer.strip() or not follow_up.strip():
        raise ValueError("include a nonempty answer and '## Interview follow-up' inside the quiz")
    if len(re.findall(r"^#{1,6} ", question, re.MULTILINE)) != 1 or not question.startswith("## "):
        raise ValueError("expected one question heading per quiz, beginning with '## '")
    if not question.splitlines()[0][3:].strip():
        raise ValueError("question heading must not be empty")
    choices = list(CHOICE.finditer(question))
    if kind == "single-choice" and (
        len(choices) < 2 or sum(match[1] == "x" for match in choices) != 1
        or any(not match[2].strip() for match in choices)
    ):
        raise ValueError("expected at least two nonempty options and exactly one correct answer")
    if kind == "typed-answer" and choices:
        raise ValueError("typed-answer questions must not include choice markers")
    return question, "## Answer and explanation\n" + explanation


def shared_explanation(content):
    """Convert canonical editorial sections to Quizdown's explanation fence."""
    question, explanation = split_quiz(content, "single-choice")
    fence = "`" * max(3, max((len(run) for run in re.findall(r"`+", explanation)), default=0) + 1)
    return f"{question.rstrip()}\n\n{fence}explanation\n{explanation.strip()}\n{fence}\n"


def static_markdown(content):
    """Use readable labels outside the page TOC without rewriting code blocks."""
    lines = []
    fence = None
    for line in content.splitlines():
        match = re.match(r"^\s*(`{3,}|~{3,})", line)
        if match:
            marker = match[1]
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence) and not line[match.end():].strip():
                fence = None
        if fence is None and line.startswith("## "):
            lines.extend(["", f"**{line[3:]}**", ""])
        else:
            lines.append(line)
    return "\n".join(lines)

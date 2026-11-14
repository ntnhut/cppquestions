"""Reject content errors before they become published quiz behavior."""

import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from check_content import check_content
from question_model import frontmatter, shared_explanation, static_markdown, validate_metadata
from example_manifest import load_manifest


class ContentValidationTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix="cppquestions-content-")
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        shutil.copytree(ROOT / "source/questions", self.root / "source/questions")
        shutil.copytree(ROOT / "source/topics", self.root / "source/topics")
        shutil.copytree(ROOT / "examples", self.root / "examples")

    def change(self, old, new, filename="ownership-002.md"):
        path = self.root / "source/questions" / filename
        text = path.read_text()
        self.assertIn(old, text)
        path.write_text(text.replace(old, new))

    def assert_invalid(self, message):
        errors, _ = check_content(self.root)
        self.assertTrue(any(message in error for error in errors), errors)

    def test_current_collection_passes(self):
        errors, count = check_content(self.root)
        self.assertEqual(errors, [])
        self.assertGreaterEqual(count, 3)

    def test_invalid_yaml_is_reported(self):
        self.change("accepted_answers: [RAII]", "accepted_answers: [RAII")
        self.assert_invalid("invalid YAML")

    def test_bad_enum_type_is_reported_without_crashing(self):
        self.change("kind: typed-answer", "kind: [typed-answer]")
        self.assert_invalid("invalid kind")

    def test_published_draft_is_rejected(self):
        self.change("status: verified", "status: draft")
        self.assert_invalid("review question")

    def test_unknown_topic_and_related_question(self):
        self.change("topic: ownership", "topic: nonexistent")
        self.change("related: [ownership-001]", "related: [missing-001]")
        self.assert_invalid("existing topic page")
        self.assert_invalid("unknown related question")

    def test_self_reference_is_rejected(self):
        self.change("related: [ownership-001]", "related: [ownership-002]")
        self.assert_invalid("question itself")

    def test_tag_structure_is_checked(self):
        self.change("tags: [raii, lifetime, resource-management]", "tags: [RAII, lifetime]")
        self.assert_invalid("tags must be a nonempty list")

    def test_typed_answers_require_strings_and_explicit_matching(self):
        self.change("accepted_answers: [RAII]", "accepted_answers: [true]")
        self.change("answer_normalization: trim-case-insensitive", "answer_normalization: fuzzy")
        self.assert_invalid("nonempty strings")
        self.assert_invalid("answer_normalization")

    def test_normalized_answer_duplicates_are_rejected(self):
        self.change("accepted_answers: [RAII]", 'accepted_answers: ["RAII", " raii "]')
        self.assert_invalid("duplicates after normalization")

    def test_choice_requires_one_correct_option(self):
        self.change("1. [ ] `end` followed by `destroy`", "1. [x] `end` followed by `destroy`", "ownership-001.md")
        self.assert_invalid("exactly one correct answer")

    def test_kind_must_match_directive(self):
        self.change("{typed-answer}", "{quizdown-explained}")
        self.assert_invalid("directive must match")

    def test_explanation_followup_and_references_cannot_be_empty(self):
        self.change("## Interview follow-up", "## Follow-up")
        self.change("https://", "invalid://")
        self.assert_invalid("Interview follow-up")
        self.assert_invalid("References must include a source URL")

    def test_example_standard_must_match_question(self):
        self.change("cpp_standard: c++17", "cpp_standard: c++20", "ownership-001.md")
        self.assert_invalid("example C++ standard differs")

    def test_missing_and_unused_examples_are_reported(self):
        (self.root / "examples/unlisted.cpp").write_text("int main() {}")
        self.assert_invalid("missing checks=['unlisted.cpp']")

    def test_manifest_rejects_missing_file_and_invalid_standard(self):
        directory = self.root / "examples"
        data = json.loads((directory / "expected.json").read_text())
        data["ownership-001.cpp"]["cpp_standard"] = "c++99"
        (directory / "expected.json").write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, "supported cpp_standard"):
            load_manifest(directory)
        (directory / "ownership-001.cpp").unlink()
        with self.assertRaisesRegex(ValueError, "missing files"):
            load_manifest(directory)

    def test_nested_code_fence_in_explanation_is_preserved(self):
        self.change("```{typed-answer}", "````{typed-answer}")
        self.change("\n```\n\n## Go deeper", "\n````\n\n## Go deeper")
        self.change("**RAII**,", '```cpp\nint example = 0;\n```\n\n**RAII**,')
        self.assertEqual(check_content(self.root)[0], [])


class TemplateTests(unittest.TestCase):
    def test_templates_are_drafts_with_documented_schema(self):
        for path in (ROOT / "docs/templates").glob("*.md"):
            with self.subTest(path=path.name):
                data = frontmatter(path.read_text())
                self.assertEqual(data["status"], "draft")
                data["status"] = "verified"
                self.assertEqual(validate_metadata(data), [])

    def test_shared_explanation_fence_does_not_close_nested_code(self):
        source = "## Prompt\n\n1. [x] Yes\n1. [ ] No\n\n## Answer and explanation\n\n```cpp\nint x;\n```\n\n## Interview follow-up\n\nWhy? Because."
        self.assertIn("````explanation\n", shared_explanation(source))

    def test_static_labels_do_not_rewrite_code_or_join_answer_list(self):
        source = '1. Last option\n## Answer and explanation\n\n```cpp\n## an example line, not a section label\n```'
        rendered = static_markdown(source)
        self.assertIn('Last option\n\n**Answer and explanation**\n\n', rendered)
        self.assertIn('```cpp\n## an example line, not a section label\n```', rendered)


if __name__ == "__main__":
    unittest.main()

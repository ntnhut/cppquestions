"""Render question metadata and progressively enhanced quizzes."""

import html
import json
from pathlib import Path
import re

from docutils import nodes
from docutils.statemachine import StringList
from sphinx.util.docutils import SphinxDirective
from sphinxcontrib.quizdown import Quizdown

from question_model import frontmatter, shared_explanation, split_quiz, static_markdown, validate_metadata


class QuestionDirective(SphinxDirective):
    def question_data(self):
        data = frontmatter(Path(self.env.doc2path(self.env.docname)).read_text(encoding="utf-8"))
        errors = validate_metadata(data)
        if errors:
            raise self.error("; ".join(errors))
        return data

    def markdown(self, content, class_name):
        container = nodes.container(classes=[class_name])
        # Keep section labels out of the document TOC: the interactive widget
        # hides this fallback after successful initialization.
        content = static_markdown(content)
        self.state.nested_parse(StringList(content.splitlines()), self.content_offset, container)
        return container


class QuestionMeta(QuestionDirective):
    def run(self):
        data = self.question_data()
        paragraph = nodes.paragraph(classes=["question-meta"])
        paragraph += nodes.Text(" · ".join([
            data["difficulty"].capitalize(), data["cpp_standard"].upper(),
            data["topic"].replace("-", " ").capitalize(),
            {"single-choice": "Single choice", "typed-answer": "Typed answer"}[data["kind"]],
        ]))
        tags = nodes.paragraph(classes=["question-tags"])
        tags += nodes.Text("Tags: " + ", ".join(data["tags"]))
        return [paragraph, tags]


class ExplainedQuizdown(Quizdown, QuestionDirective):
    optional_arguments = 0

    def run(self):
        original = "\n".join(self.content)
        try:
            content = shared_explanation(original)
        except ValueError as error:
            raise self.error(str(error))
        self.content = StringList(content.splitlines())
        container = nodes.container(classes=["explained-question"])
        container.extend(super().run())
        fallback = re.sub(r"^(\d+)\. \[[ x]\] ", r"\1. ", original, flags=re.MULTILINE)
        container += self.markdown(fallback, "quiz-fallback")
        return [container]


class TypedAnswer(QuestionDirective):
    has_content = True

    def run(self):
        data = self.question_data()
        if data["kind"] != "typed-answer":
            raise self.error("typed-answer directive requires kind: typed-answer")
        try:
            question, explanation = split_quiz("\n".join(self.content), "typed-answer")
        except ValueError as error:
            raise self.error(str(error))
        input_id = f"{data['id']}-answer"
        help_id = f"{data['id']}-answer-help"
        feedback_id = f"{data['id']}-feedback"
        answers = html.escape(json.dumps(data["accepted_answers"]), quote=True)
        label = html.escape(data["answer_label"])
        help_text = "Leading and trailing spaces are ignored."
        if data["answer_normalization"] == "trim-case-insensitive":
            help_text += " Letter case is ignored."
        form = f'''
<form class="typed-answer-form" hidden data-answers="{answers}"
      data-normalization="{data['answer_normalization']}">
  <label for="{input_id}">{label}</label>
  <p id="{help_id}" class="answer-help">{help_text}</p>
  <input id="{input_id}" type="text" required autocomplete="off" spellcheck="false"
         aria-describedby="{help_id} {feedback_id}">
  <div class="answer-actions">
    <button type="submit">Check answer</button>
    <button type="reset">Reset</button>
  </div>
  <p id="{feedback_id}" class="answer-feedback" role="status" aria-live="polite" aria-atomic="true"></p>
</form>'''
        container = nodes.container(classes=["typed-question"])
        container += self.markdown(question, "typed-prompt")
        container += nodes.paragraph("", "Read the answer and explanation below.", classes=["typed-fallback-note"])
        container += nodes.raw("", form, format="html")
        container += self.markdown(explanation, "typed-explanation")
        return [container]


def setup(app):
    app.setup_extension("sphinxcontrib.quizdown")
    app.add_directive("quizdown-explained", ExplainedQuizdown)
    app.add_directive("typed-answer", TypedAnswer)
    app.add_directive("question-meta", QuestionMeta)
    app.add_js_file("typed-answer.js")
    return {"version": "2.1", "parallel_read_safe": True, "parallel_write_safe": True}

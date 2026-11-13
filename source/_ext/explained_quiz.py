"""Convert editorial answer sections to Quizdown's inline shared explanation."""

import re

from docutils.statemachine import StringList
from docutils import nodes
from sphinxcontrib.quizdown import Quizdown

EXPLANATION_MARKER = "\n## Answer and explanation\n"
CHOICE = re.compile(r"^\d+\. \[([ x])\] .+$", re.MULTILINE)


def shared_explanation(content):
    """Keep one explanation per question, hidden until an answer is selected."""
    question, separator, explanation = content.partition(EXPLANATION_MARKER)
    if not separator or not explanation.strip():
        raise ValueError("Include a nonempty '## Answer and explanation' section inside the quiz.")
    choices = list(CHOICE.finditer(question))
    if len(choices) < 2 or sum(match[1] == "x" for match in choices) != 1:
        raise ValueError("Expected at least two options and exactly one correct answer.")
    if len(re.findall(r"^#{1,6} ", question, re.MULTILINE)) != 1:
        raise ValueError("Expected one question per explained quiz.")
    # A longer fence keeps any code blocks inside the explanation nested safely.
    fence = "`" * max(
        3, max((len(run) for run in re.findall(r"`+", explanation)), default=0) + 1
    )
    return (
        f"{question.rstrip()}\n\n{fence}explanation\n"
        f"## Answer and explanation\n\n{explanation.strip()}\n{fence}\n"
    )


class ExplainedQuizdown(Quizdown):
    optional_arguments = 0

    def run(self):
        try:
            content = shared_explanation("\n".join(self.content))
        except ValueError as error:
            raise self.error(str(error))
        self.content = StringList(content.splitlines())
        return super().run() + [nodes.raw(
            "", "<noscript>Enable JavaScript to answer the quiz and reveal its explanation.</noscript>",
            format="html",
        )]


def setup(app):
    app.setup_extension("sphinxcontrib.quizdown")
    app.add_directive("quizdown-explained", ExplainedQuizdown)
    return {"version": "1.1", "parallel_read_safe": True, "parallel_write_safe": True}

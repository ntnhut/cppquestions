"""Sphinx configuration for cppquestions.com."""

import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / "_ext"))

project = "C++ Questions"
author = "Nhut Nguyen"
copyright = "2026, Nhut Nguyen"

extensions = ["myst_parser", "sphinxcontrib.quizdown", "question_pages"]
source_suffix = {".md": "markdown", ".rst": "restructuredtext"}
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
myst_enable_extensions = ["colon_fence"]

html_theme = "furo"
html_title = "C++ Questions"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_js_files = ["quizdown-ready.js"]
# Read the Docs sets this to the canonical URL for the current build.
html_baseurl = os.environ.get("READTHEDOCS_CANONICAL_URL", "https://cppquestions.com/")
html_theme_options = {
    "light_css_variables": {"color-brand-primary": "#245e50", "color-brand-content": "#245e50"},
    "dark_css_variables": {"color-brand-primary": "#85d1b4", "color-brand-content": "#85d1b4"},
}

quizdown_config = {
    "quizdown_js": "quizdown.js",
    "start_on_load": True,
    "shuffle_answers": True,
    "shuffle_questions": False,
    "primary_color": "#245e50",
    "secondary_color": "#e6eeeb",
    "text_color": "#172b24",
    "locale": "en",
    "immediateFeedback": True,
    "autoAdvance": False,
}

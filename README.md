# C++ Questions

Free modern C++ questions with complete explanations and clear paths to deeper
topic learning. The project domain is **cppquestions.com**.

The site uses **Sphinx + MyST Markdown + Furo + Quizdown**, following the
newindenmark quiz setup. Hosting is planned on **Read the Docs**. This initial
prototype contains two single-choice questions and two topic learning paths.

## Build locally

Requires Python 3.12, Git (for the pinned Quizdown extension), and a C++ compiler
to check examples.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/check_content.py
.venv/bin/python scripts/check_examples.py
.venv/bin/sphinx-build -n -W --keep-going -b html source _build/html
.venv/bin/python -m http.server 8000 --directory _build/html
```

Open <http://localhost:8000>. Use `CXX=clang++` when running the example checker
to check with Clang. CI checks both GCC and Clang and treats Sphinx warnings
as build failures.

## Author a question

1. Create `source/questions/<id>.md` using an existing question as a template.
2. Add YAML metadata: `id`, `topic`, `difficulty`, `cpp_standard`, `kind`, and
   `status`. IDs match filenames. For this prototype, `kind` is `single-choice`.
3. Put runnable code in `examples/<id>.cpp` and include it with MyST's
   `literalinclude` directive. Add its expected output to `examples/expected.json`.
4. Add one fenced `{quizdown-explained}` block. Use ordered task lists and mark
   exactly one option with `[x]`. Inside the same block, add an
   `## Answer and explanation` section followed by the interview follow-up.
   The Sphinx helper converts this text into one fenced `explanation` block.
   It stays hidden until an answer is selected, then appears below the choices,
   whether the answer was correct or incorrect. Reset hides it again.
5. Keep the next learning step and references outside the quiz. Check the
   language rules and code before setting `status: verified`.
6. Add the page to the relevant topic's `toctree`, then run the checks and build.

Metadata validation checks structure, not technical correctness. Code is included
from the same files checked by CI; compiler output is evidence alongside language
references. Draft questions should stay outside `source/questions/` until reviewed.

Quizdown's renderer is bundled locally, as in newindenmark, so quiz loading does
not depend on a CDN. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for its
source, hash, and license. Source downloads remain available; the answers are
intentionally public.

The bundled `quizdown.js` comes from our fork with inline explanation support.
Keep `immediateFeedback: True` in `source/conf.py` to reveal explanations on selection.
JavaScript is required for the interactive explanation reveal; downloaded page
source still contains the answer and explanation.

## Publish on Read the Docs

The build configuration is in `.readthedocs.yaml`.

1. Push this repository to GitHub and import `ntnhut/cppquestions` in Read the Docs.
2. Select the intended default branch and confirm the first HTML build succeeds.
3. Add `cppquestions.com` as the canonical custom domain in the Read the Docs
   project settings. Follow the DNS records and verification steps shown there
   by Read the Docs and your domain provider; wait for HTTPS to be ready.
4. Verify the home page, both quizzes, search, and mobile layout on the public URL.

The domain has been purchased; a live Read the Docs project and DNS configuration
are separate setup steps. Consult the current [Read the Docs custom-domain guide](https://docs.readthedocs.com/platform/stable/custom-domains.html)
when connecting it.

## Next steps

- Add deterministic typed-answer questions after validating an accessible input flow.
- Complete a keyboard-navigation accessibility review. Initial Chrome checks cover
  answer feedback, scoring, reset, mobile width, and inline explanation reveal on selection.
- Expand the initial questions and learning paths using learner feedback.
- Create the C++ Questions LinkedIn page and add its real URL to the About page.
- Publish topic-based text courses on Leanpub first, then video courses on Udemy.

Books and courses are planned; none are advertised as available in this prototype.
Project code and original editorial content have no reuse license selected yet.

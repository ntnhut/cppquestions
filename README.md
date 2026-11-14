# C++ Questions

Free modern C++ questions with complete explanations and clear paths to deeper
topic learning. The project domain is **cppquestions.com**.

The site uses **Sphinx + MyST Markdown + Furo + Quizdown**, following the
newindenmark quiz setup. Hosting is planned on **Read the Docs**. This initial
prototype contains two single-choice questions, one typed-answer question, and
two topic learning paths. The MVP pilot targets 32 questions across ownership,
move semantics, classes/polymorphism, and STL containers/iterators.

## Build locally

Requires Python 3.12, Git (for the pinned Quizdown extension), and a C++ compiler
to check examples.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/check_content.py
.venv/bin/python -m unittest discover -s tests
.venv/bin/python scripts/check_examples.py
.venv/bin/sphinx-build -n -W --keep-going -b html source _build/html
.venv/bin/python -m http.server 8000 --directory _build/html
```

Keep the server terminal running and open <http://localhost:8000> in a browser
on the same machine. The terminal staying at `Serving HTTP ...` is normal.

If VS Code is connected to a remote Linux machine and your browser runs on
your Mac or another computer, forward the server port first:

1. Open VS Code's **Ports** tab beside **Terminal**.
2. If port **8000** is not listed, select **Forward a Port** and enter `8000`.
3. Right-click the port's entry and select **Open in Browser**. Use its forwarded
   address; the local port can differ if port 8000 is already occupied.

The browser's `localhost` refers to the computer running the browser, so the
remote server needs this tunnel. See the [VS Code port-forwarding guide](https://code.visualstudio.com/docs/remote/ssh#_forwarding-a-port-creating-ssh-tunnel).

Use `CXX=clang++` when running the example checker to check with Clang. CI checks
both GCC and Clang and treats Sphinx warnings as build failures.

For browser regression checks, build HTML first, then run this optional command
with Node.js 22 and a local Chrome installation:

```sh
node scripts/check_quizzes.mjs _build/html
```

Set `CHROME_BIN` to the Chrome executable if it is not `google-chrome`. These
checks exercise both question kinds, accepted-answer rules, retry/reset,
mobile width, and readable fallbacks with scripts disabled or missing. CI runs
the Python validation/regression checks and compiler matrix; browser checks
currently run locally. A full keyboard/screen-reader review remains separate.

After changing a Sphinx extension, use `sphinx-build -E -a` with the remaining
build arguments above to refresh cached pages and static assets.

## Author a question

See the [editorial guide](docs/editorial-guide.md) for the complete schema,
templates, and technical-review checklist.

1. Start a draft outside `source/questions/`, using a
   [single-choice](docs/templates/single-choice.md) or
   [typed-answer](docs/templates/typed-answer.md) template.
2. Add YAML metadata: `id`, `topic`, `difficulty`, `cpp_standard`, `kind`, and
   `status`, plus `tags` and `related` IDs. IDs match filenames and topics identify
   existing topic pages. Typed answers also declare `answer_label`,
   `accepted_answers`, and `answer_normalization` (`trim` or `trim-case-insensitive`).
3. Add `{question-meta}` after the title to display metadata and tags. Put
   runnable code in `examples/<id>.cpp` and include it with `literalinclude`.
   Declare its `cpp_standard` and exact `stdout` in `examples/expected.json`.
4. Add one fenced `{quizdown-explained}` or `{typed-answer}` block matching `kind`.
   Single choice uses ordered task lists with exactly one `[x]`. Include complete
   `## Answer and explanation` and `## Interview follow-up` sections inside the
   same block. Either answer result reveals the explanation; reset hides it.
5. Keep `## Go deeper`, a `{related-questions}` directive, a topic-path link, and
   `## References` outside the quiz. Review the language rules and applicable code
   before setting `status: verified` and moving the question into `source/questions/`.
6. Add the page to its topic's `toctree`, then run the checks and build.

Metadata validation checks structure, not technical correctness. Code is included
from the same files checked by CI; compiler output is evidence alongside language
references. Draft questions should stay outside `source/questions/` until reviewed.

Quizdown's renderer is bundled locally, as in newindenmark, so quiz loading does
not depend on a CDN. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for its
source, hash, and license. Source downloads remain available; the answers are
intentionally public.

The bundled `quizdown.js` comes from our fork with inline explanation support.
Keep `immediateFeedback: True` in `source/conf.py` to reveal explanations on selection.
Every question also renders a complete static explanation. It remains readable
without JavaScript or if the quiz script fails. Once a widget initializes, it
hides its static explanation and reveals the interactive explanation after an
answer. Typed input uses explicit accepted strings and matching rules, without
fuzzy or AI grading. A shared topic/session score is still planned.

## Publish on Read the Docs

The build configuration is in `.readthedocs.yaml`.

1. Push this repository to GitHub and import `ntnhut/cppquestions` in Read the Docs.
2. Select the intended default branch and confirm the first HTML build succeeds.
3. Add `cppquestions.com` as the canonical custom domain in the Read the Docs
   project settings. Follow the DNS records and verification steps shown there
   by Read the Docs and your domain provider; wait for HTTPS to be ready.
4. Verify the home page, both question kinds, search, mobile layout, and
   no-JavaScript fallback on the public URL.

The domain has been purchased; a live Read the Docs project and DNS configuration
are separate setup steps. Consult the current [Read the Docs custom-domain guide](https://docs.readthedocs.com/platform/stable/custom-domains.html)
when connecting it.

## Next steps

- Add topic practice sessions with a shared score and defined retry/reset behavior.
- Complete a keyboard-navigation accessibility review. Initial Chrome checks cover
  answer feedback, scoring, reset, mobile width, and inline explanation reveal on selection.
- Review the first 15-question pilot, then expand to 30–50 verified questions and
  at least four topic paths using learner feedback.
- Create the C++ Questions LinkedIn page and add its real URL to the About page.
- Publish topic-based text courses on Leanpub first, then video courses on Udemy.

Books and courses are planned; none are advertised as available in this prototype.
Project code and original editorial content have no reuse license selected yet.

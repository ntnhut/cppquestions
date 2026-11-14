# C++ Questions

Free modern C++ questions with complete explanations and clear paths to deeper
topic learning. The project domain is **cppquestions.com**.

The site uses **Sphinx + MyST Markdown + Furo + Quizdown**, with a build
configuration for **Read the Docs**. Questions support single-choice and typed
answers, complete explanations, and topic learning paths.

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

## Quiz rendering

Quizdown's renderer is bundled locally, so quiz loading does
not depend on a CDN. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for its
source, hash, and license. Source downloads remain available; the answers are
intentionally public.

The bundled `quizdown.js` comes from our fork with inline explanation support.
Keep `immediateFeedback: True` in `source/conf.py` to reveal explanations on selection.
Every question also renders a complete static explanation. It remains readable
without JavaScript or if the quiz script fails. Once a widget initializes, it
hides its static explanation and reveals the interactive explanation after an
answer. Typed input uses explicit accepted strings and matching rules, without
fuzzy or AI grading.

## Publish on Read the Docs

The build configuration is in `.readthedocs.yaml`.

1. Push this repository to GitHub and import `ntnhut/cppquestions` in Read the Docs.
2. Select the intended default branch and confirm the first HTML build succeeds.
3. Add `cppquestions.com` as the canonical custom domain in the Read the Docs
   project settings. Follow the DNS records and verification steps shown there
   by Read the Docs and your domain provider; wait for HTTPS to be ready.
4. Verify the home page, both question kinds, search, mobile layout, and
   no-JavaScript fallback on the public URL.

Consult the [Read the Docs custom-domain guide](https://docs.readthedocs.com/platform/stable/custom-domains.html)
when connecting it.

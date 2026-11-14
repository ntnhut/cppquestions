// The static explanation remains readable if this enhancement cannot initialize.
(() => {
    function normalizeAnswer(answer, mode) {
        const trimmed = answer.replace(/^[ \t\r\n]+|[ \t\r\n]+$/g, "");
        return mode === "trim-case-insensitive"
            ? trimmed.replace(/[A-Z]/g, (letter) => letter.toLowerCase())
            : trimmed;
    }

    function initialize() {
        for (const form of document.querySelectorAll(".typed-answer-form")) {
            const question = form.closest(".typed-question");
            const input = form.querySelector("input");
            const feedback = form.querySelector(".answer-feedback");
            const explanation = question.querySelector(".typed-explanation");
            const mode = form.dataset.normalization;
            const answers = JSON.parse(form.dataset.answers).map((answer) => normalizeAnswer(answer, mode));

            form.addEventListener("submit", (event) => {
                event.preventDefault();
                const answer = normalizeAnswer(input.value, mode);
                if (!answer) {
                    feedback.textContent = "Enter an answer before checking.";
                    input.setAttribute("aria-invalid", "true");
                    input.focus();
                    return;
                }
                const correct = answers.includes(answer);
                feedback.textContent = correct
                    ? "Correct. Read the explanation below."
                    : "Not quite. Read the explanation below.";
                input.setAttribute("aria-invalid", String(!correct));
                explanation.hidden = false;
            });

            form.addEventListener("reset", () => {
                feedback.textContent = "";
                input.removeAttribute("aria-invalid");
                explanation.hidden = true;
                input.focus();
            });

            // Only hide the fallback after the controls and handlers are ready.
            form.hidden = false;
            explanation.hidden = true;
            question.querySelector(".typed-fallback-note").hidden = true;
        }
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initialize);
    } else {
        initialize();
    }
})();

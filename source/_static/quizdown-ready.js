// Keep the static question and explanation until Quizdown renders successfully.
window.addEventListener("load", () => {
    const pending = new Set(document.querySelectorAll(".explained-question .quizdown"));
    const deadline = performance.now() + 10000;
    function revealReadyQuizzes() {
        for (const quiz of pending) {
            if (quiz.shadowRoot?.querySelector(".quizdown-content input")) {
                const fallback = quiz.parentElement.querySelector(".quiz-fallback");
                quiz.classList.add("quizdown-ready");
                fallback.hidden = true;
                pending.delete(quiz);
            }
        }
        if (pending.size && performance.now() < deadline) {
            setTimeout(revealReadyQuizzes, 50);
        }
    }
    setTimeout(revealReadyQuizzes, 0);
});

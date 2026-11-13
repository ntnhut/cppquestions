// Quizdown consumes source text on load. Reveal only the rendered UI so its
// explanations cannot flash on screen while the JavaScript is loading.
window.addEventListener("load", () => {
    setTimeout(() => {
        document.querySelectorAll(".quizdown").forEach((quiz) => {
            if (quiz.shadowRoot?.querySelector(".quizdown-content")) {
                quiz.classList.add("quizdown-ready");
            }
        });
    }, 0);
});

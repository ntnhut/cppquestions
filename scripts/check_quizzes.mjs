// Optional real-browser regression checks; no npm dependencies are needed.
import { spawnSync } from "node:child_process";
import { mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const build = resolve(process.argv[2] ?? "_build/html");
const directory = mkdtempSync(join(tmpdir(), "cppquestions-browser-"));
try {
    const questionURL = pathToFileURL(join(build, "questions/")).href;
    const pages = {};
    for (const id of ["ownership-001", "move-001", "ownership-002"]) {
        pages[id] = new URL(`${id}.html`, questionURL).href;
    }
    for (const [name, id] of [["failed-choice", "ownership-001"], ["failed-typed", "ownership-002"]]) {
        const original = readFileSync(join(build, "questions", `${id}.html`), "utf8");
        const broken = original.replace("<head>", `<head><base href="${questionURL}">`)
            .replace(/src="[^"]*(?:quizdown|typed-answer)\.js[^"]*"/g, 'src="missing-quiz-script.js"');
        const path = join(directory, `${name}.html`);
        writeFileSync(path, broken);
        pages[name] = pathToFileURL(path).href;
    }
    const template = readFileSync(fileURLToPath(new URL("../tests/browser-quizzes.html", import.meta.url)), "utf8");
    const harness = template.replace("/* PAGE_URLS */ {}", JSON.stringify(pages).replaceAll("<", "\\u003c"));
    const path = join(directory, "check.html");
    writeFileSync(path, harness);
    const result = spawnSync(process.env.CHROME_BIN ?? "google-chrome", [
        "--headless", "--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage",
        "--no-first-run", "--no-default-browser-check", "--allow-file-access-from-files",
        `--user-data-dir=${join(directory, "profile")}`, "--dump-dom",
        "--virtual-time-budget=20000", pathToFileURL(path).href,
    ], { encoding: "utf8", timeout: 45000, maxBuffer: 4 * 1024 * 1024 });
    if (result.error) throw result.error;
    const report = result.stdout.match(/<pre id="report"[^>]*>([\s\S]*?)<\/pre>/);
    console.log(report ? report[1] : result.stderr);
    if (result.status !== 0 || !result.stdout.includes('data-result="passed"')) process.exitCode = 1;
} finally {
    rmSync(directory, { recursive: true, force: true });
}

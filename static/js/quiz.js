(() => {
    "use strict";

    // --- Normalization ---
    function normalize(s) {
        return s
            .toLowerCase()
            .trim()
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "") // strip diacritics
            .replace(/^(the|a|an)\s+/i, "") // strip leading articles
            .replace(/[^a-z0-9\s]/g, "") // strip punctuation
            .replace(/\s+/g, " ") // collapse whitespace
            .trim();
    }

    // --- State ---
    const basePath = window.BASE_PATH || "";
    const container = document.getElementById("quiz-container");
    const quizId = container.dataset.quizId;
    const isMapQuiz = container.dataset.hasMap === "true";
    let entries = [];
    let remaining = new Map(); // normalized answer -> entry index
    let guessed = new Set(); // entry indices that have been guessed
    let correctCount = 0;
    let totalCount = 0;
    let score = 0;
    let startTime = null;
    let timerInterval = null;
    let quizEnded = false;
    let timeLimit = 0;
    let recentGuesses = [];

    // --- DOM refs ---
    const input = document.getElementById("quiz-input");
    const correctEl = document.getElementById("correct-count");
    const totalEl = document.getElementById("total-count");
    const timerEl = document.getElementById("timer");
    const progressBar = document.getElementById("progress-bar");
    const scoreDisplay = document.getElementById("score-display");
    const recentContainer = document.getElementById("recent-guesses");
    const giveUpBtn = document.getElementById("give-up-btn");
    const resultsModal = document.getElementById("results-modal");

    // --- Init ---
    async function init() {
        const resp = await fetch(`${basePath}/api/quiz/${quizId}`);
        const data = await resp.json();
        entries = data.entries;
        timeLimit = data.time_limit;
        totalCount = entries.length;
        totalEl.textContent = totalCount;

        // Build answer lookup
        entries.forEach((entry, idx) => {
            entry.accepted_answers.forEach((answer) => {
                const norm = normalize(answer);
                if (norm) remaining.set(norm, idx);
            });
        });

        // Build tabular grid for non-map quizzes
        if (!isMapQuiz) {
            buildTable();
        }

        // Start timer on first keystroke
        input.addEventListener("input", onInput);
        input.addEventListener("compositionend", onInput);
        input.addEventListener("keydown", (e) => {
            if (e.key === "Tab") e.preventDefault(); // prevent tab-out
        });
        giveUpBtn.addEventListener("click", giveUp);
        document.getElementById("play-again-btn").addEventListener("click", () => {
            location.reload();
        });

        input.focus();
    }

    function onInput() {
        if (quizEnded) return;

        // Start timer on first input
        if (!startTime) {
            startTime = Date.now();
            timerInterval = setInterval(updateTimer, 100);
        }

        const value = normalize(input.value);
        if (!value) return;

        // Check for match
        if (remaining.has(value)) {
            const idx = remaining.get(value);
            if (!guessed.has(idx)) {
                guessed.add(idx);
                correctCount++;
                const entry = entries[idx];

                // Remove all answers for this entry from remaining
                entry.accepted_answers.forEach((a) => {
                    const norm = normalize(a);
                    if (remaining.get(norm) === idx) remaining.delete(norm);
                });

                // Calculate speed bonus
                const elapsed = (Date.now() - startTime) / 1000;
                const ratio = elapsed / timeLimit;
                let multiplier = 1;
                if (ratio <= 0.25) multiplier = 2;
                else if (ratio <= 0.5) multiplier = 1.5;
                else if (ratio <= 0.75) multiplier = 1.25;
                score += Math.round(100 * multiplier);

                // Update UI
                updateUI(entry);
                if (isMapQuiz) {
                    highlightOnMap(entry, "guessed");
                } else {
                    revealInTable(idx, "guessed");
                }
                input.value = "";

                // Check if done
                if (correctCount === totalCount) {
                    endQuiz(false);
                }
            }
        }
    }

    function updateUI(entry) {
        correctEl.textContent = correctCount;
        scoreDisplay.textContent = score;
        const pct = (correctCount / totalCount) * 100;
        progressBar.style.width = pct + "%";

        // Add to recent guesses
        recentGuesses.unshift(entry.display_name);
        if (recentGuesses.length > 5) recentGuesses.pop();
        renderRecentGuesses();
    }

    function renderRecentGuesses() {
        recentContainer.innerHTML = recentGuesses
            .map(
                (name, i) =>
                    `<div class="px-3 py-1.5 rounded-lg text-sm ${i === 0 ? "bg-green-500/20 text-green-400 font-medium" : "bg-slate-800 text-slate-400"}">${name}</div>`
            )
            .join("");
    }

    function highlightOnMap(entry, className) {
        // Try finding element by ID (most maps use this)
        let el = document.getElementById(entry.id);
        if (!el) {
            // Try uppercase (US states use uppercase class)
            el = document.getElementById(entry.id.toUpperCase());
        }

        if (el) {
            const tag = el.tagName.toLowerCase();
            if (tag === "g") {
                // Group: highlight all child paths
                el.querySelectorAll("path").forEach((p) => {
                    p.classList.add(className);
                    if (className === "guessed") {
                        p.classList.add("just-guessed");
                        setTimeout(() => p.classList.remove("just-guessed"), 600);
                    }
                });
            } else {
                el.classList.add(className);
                if (className === "guessed") {
                    el.classList.add("just-guessed");
                    setTimeout(() => el.classList.remove("just-guessed"), 600);
                }
            }

            addMapLabel(entry);
        }
    }

    function addMapLabel(entry) {
        if (!entry.label_x || !entry.label_y) return;
        const svg = document.querySelector("#map-container svg");
        if (!svg) return;

        const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
        text.setAttribute("x", entry.label_x);
        text.setAttribute("y", entry.label_y);
        text.setAttribute("class", "map-label");
        text.textContent = entry.display_name;
        svg.appendChild(text);
    }

    // --- Tabular quiz ---
    function buildTable() {
        const tc = document.getElementById("table-container");
        if (!tc) return;
        const grid = document.createElement("div");
        grid.className =
            "grid gap-1.5 h-full content-start";
        // Pick column count based on entry count
        const n = entries.length;
        if (n <= 15) grid.classList.add("grid-cols-3", "sm:grid-cols-5");
        else if (n <= 30) grid.classList.add("grid-cols-4", "sm:grid-cols-6");
        else grid.classList.add("grid-cols-5", "sm:grid-cols-7", "lg:grid-cols-9");

        entries.forEach((entry, idx) => {
            const cell = document.createElement("div");
            cell.id = "table-cell-" + idx;
            cell.className =
                "flex items-center justify-center rounded-lg bg-slate-800/60 border border-slate-700/50 text-slate-600 text-xs sm:text-sm font-medium px-1 py-2 text-center select-none transition-all duration-300 min-h-[2.5rem]";
            cell.textContent = idx + 1;
            grid.appendChild(cell);
        });
        tc.appendChild(grid);
    }

    function revealInTable(idx, className) {
        const cell = document.getElementById("table-cell-" + idx);
        if (!cell) return;
        const entry = entries[idx];
        cell.textContent = entry.display_name;
        if (className === "guessed") {
            cell.className =
                "flex items-center justify-center rounded-lg bg-green-500/20 border border-green-500/40 text-green-400 text-xs sm:text-sm font-medium px-1 py-2 text-center select-none transition-all duration-300 min-h-[2.5rem]";
        } else {
            cell.className =
                "flex items-center justify-center rounded-lg bg-red-500/15 border border-red-500/30 text-red-400 text-xs sm:text-sm font-medium px-1 py-2 text-center select-none transition-all duration-300 min-h-[2.5rem]";
        }
    }

    function updateTimer() {
        if (!startTime || quizEnded) return;
        const elapsed = Math.floor((Date.now() - startTime) / 1000);
        const mins = Math.floor(elapsed / 60);
        const secs = elapsed % 60;
        timerEl.textContent = `${mins}:${secs.toString().padStart(2, "0")}`;
    }

    function giveUp() {
        if (quizEnded) return;
        if (correctCount === 0) {
            // Confirm if nothing guessed
            if (!confirm("Are you sure you want to give up?")) return;
        }
        endQuiz(true);
    }

    function endQuiz(gaveUp) {
        quizEnded = true;
        clearInterval(timerInterval);
        input.disabled = true;
        input.placeholder = "Quiz ended";
        giveUpBtn.disabled = true;
        giveUpBtn.classList.add("opacity-50");

        // Highlight missed entries
        const missed = [];
        entries.forEach((entry, idx) => {
            if (!guessed.has(idx)) {
                missed.push(entry);
                if (isMapQuiz) {
                    highlightOnMap(entry, "missed");
                } else {
                    revealInTable(idx, "missed");
                }
            }
        });

        // Show results modal
        const elapsed = startTime ? Math.floor((Date.now() - startTime) / 1000) : 0;
        const mins = Math.floor(elapsed / 60);
        const secs = elapsed % 60;

        document.getElementById("results-correct").textContent =
            `${correctCount}/${totalCount}`;
        document.getElementById("results-score").textContent = score;
        document.getElementById("results-time").textContent =
            `${mins}:${secs.toString().padStart(2, "0")}`;

        if (gaveUp) {
            document.getElementById("results-title").textContent = "Quiz Over";
            document.getElementById("results-subtitle").textContent =
                `You got ${correctCount} out of ${totalCount}`;
        } else {
            document.getElementById("results-title").textContent = "Perfect Score!";
            document.getElementById("results-subtitle").textContent =
                `You named all ${totalCount} in ${mins}m ${secs}s`;
        }

        // Show missed answers
        if (missed.length > 0) {
            const missedSection = document.getElementById("missed-section");
            const missedList = document.getElementById("missed-list");
            missedSection.classList.remove("hidden");
            missedList.innerHTML = missed
                .map(
                    (e) =>
                        `<span class="px-2 py-1 rounded bg-red-500/20 text-red-400 text-sm">${e.display_name}</span>`
                )
                .join("");
        }

        resultsModal.classList.remove("hidden");

        // Save best score
        const bestKey = `geoquiz_best_${quizId}`;
        const existing = localStorage.getItem(bestKey);
        const bestData = { correct: correctCount, total: totalCount, score, time: elapsed };
        if (!existing || JSON.parse(existing).score < score) {
            localStorage.setItem(bestKey, JSON.stringify(bestData));
        }
    }

    // Close modal on background click
    resultsModal.addEventListener("click", (e) => {
        if (e.target === resultsModal) resultsModal.classList.add("hidden");
    });

    init();
})();

window.GeoQuizEngine = (() => {
    "use strict";

    function normalize(s) {
        return s
            .toLowerCase()
            .trim()
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "")
            .replace(/^(the|a|an)\s+/i, "")
            .replace(/[^a-z0-9\s]/g, "")
            .replace(/\s+/g, " ")
            .trim();
    }

    let entries = [];
    let remaining = new Map();
    let guessed = new Set();
    let correctCount = 0;
    let totalCount = 0;
    let score = 0;
    let startTime = null;
    let timerInterval = null;
    let quizEnded = false;
    let timeLimit = 0;
    let recentGuesses = [];
    let isMapQuiz = false;
    let quizId = "";

    // DOM refs (set during init since DOM is dynamically created)
    let input, correctEl, totalEl, timerEl, progressBar, scoreDisplay,
        recentContainer, giveUpBtn, resultsModal;

    function bindDOM() {
        input = document.getElementById("quiz-input");
        correctEl = document.getElementById("correct-count");
        totalEl = document.getElementById("total-count");
        timerEl = document.getElementById("timer");
        progressBar = document.getElementById("progress-bar");
        scoreDisplay = document.getElementById("score-display");
        recentContainer = document.getElementById("recent-guesses");
        giveUpBtn = document.getElementById("give-up-btn");
        resultsModal = document.getElementById("results-modal");
    }

    function resetState() {
        entries = [];
        remaining = new Map();
        guessed = new Set();
        correctCount = 0;
        totalCount = 0;
        score = 0;
        startTime = null;
        if (timerInterval) clearInterval(timerInterval);
        timerInterval = null;
        quizEnded = false;
        timeLimit = 0;
        recentGuesses = [];
        isMapQuiz = false;
    }

    async function init(id) {
        resetState();
        quizId = id;
        bindDOM();

        // Fetch quiz data
        const resp = await fetch("data/quizzes/" + quizId + ".json");
        const data = await resp.json();
        entries = data.entries;
        timeLimit = data.timeLimit;
        totalCount = entries.length;
        totalEl.textContent = totalCount;
        isMapQuiz = !!data.mapFile;

        // Load map or build table
        const display = document.getElementById("quiz-display");
        if (isMapQuiz) {
            try {
                const mapResp = await fetch("maps/" + data.mapFile);
                const svgText = await mapResp.text();
                display.innerHTML = '<div id="map-container" class="w-full h-full flex items-center justify-center">' + svgText + '</div>';
            } catch (e) {
                display.innerHTML = '<div class="text-slate-500 text-center">Map failed to load</div>';
                isMapQuiz = false;
            }
        }

        if (!isMapQuiz) {
            display.innerHTML = '<div id="table-container" class="w-full h-full overflow-y-auto p-2"></div>';
            buildTable();
        }

        // Build answer lookup
        entries.forEach((entry, idx) => {
            entry.accepted_answers.forEach(answer => {
                const norm = normalize(answer);
                if (norm) remaining.set(norm, idx);
            });
        });

        // Event listeners
        input.addEventListener("input", onInput);
        input.addEventListener("compositionend", onInput);
        input.addEventListener("keydown", e => {
            if (e.key === "Tab") e.preventDefault();
        });
        giveUpBtn.addEventListener("click", giveUp);
        document.getElementById("play-again-btn").addEventListener("click", () => {
            window.location.hash = "#/quiz/" + quizId;
            // Force re-init since hash didn't change
            init(quizId);
        });
        resultsModal.addEventListener("click", e => {
            if (e.target === resultsModal) resultsModal.classList.add("hidden");
        });

        input.focus();
    }

    function onInput() {
        if (quizEnded) return;
        if (!startTime) {
            startTime = Date.now();
            timerInterval = setInterval(updateTimer, 100);
        }

        const value = normalize(input.value);
        if (!value) return;

        if (remaining.has(value)) {
            const idx = remaining.get(value);
            if (!guessed.has(idx)) {
                guessed.add(idx);
                correctCount++;
                const entry = entries[idx];

                entry.accepted_answers.forEach(a => {
                    const norm = normalize(a);
                    if (remaining.get(norm) === idx) remaining.delete(norm);
                });

                const elapsed = (Date.now() - startTime) / 1000;
                const ratio = elapsed / timeLimit;
                let multiplier = 1;
                if (ratio <= 0.25) multiplier = 2;
                else if (ratio <= 0.5) multiplier = 1.5;
                else if (ratio <= 0.75) multiplier = 1.25;
                score += Math.round(100 * multiplier);

                updateUI(entry);
                if (isMapQuiz) {
                    highlightOnMap(entry, "guessed");
                } else {
                    revealInTable(idx, "guessed");
                }
                input.value = "";

                if (correctCount === totalCount) {
                    endQuiz(false);
                }
            }
        }
    }

    function updateUI(entry) {
        correctEl.textContent = correctCount;
        scoreDisplay.textContent = score;
        progressBar.style.width = ((correctCount / totalCount) * 100) + "%";
        recentGuesses.unshift(entry.display_name);
        if (recentGuesses.length > 5) recentGuesses.pop();
        recentContainer.innerHTML = recentGuesses
            .map((name, i) =>
                '<div class="px-3 py-1.5 rounded-lg text-sm ' +
                (i === 0 ? "bg-green-500/20 text-green-400 font-medium" : "bg-slate-800 text-slate-400") +
                '">' + name + '</div>'
            ).join("");
    }

    function highlightOnMap(entry, className) {
        let el = document.getElementById(entry.id);
        if (!el) el = document.getElementById(entry.id.toUpperCase());
        if (!el) return;

        const tag = el.tagName.toLowerCase();
        if (tag === "g") {
            el.querySelectorAll("path").forEach(p => {
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

    function buildTable() {
        const tc = document.getElementById("table-container");
        if (!tc) return;
        const grid = document.createElement("div");
        grid.className = "grid gap-1.5 h-full content-start";
        const n = entries.length;
        if (n <= 15) grid.classList.add("grid-cols-3", "sm:grid-cols-5");
        else if (n <= 30) grid.classList.add("grid-cols-4", "sm:grid-cols-6");
        else grid.classList.add("grid-cols-5", "sm:grid-cols-7", "lg:grid-cols-9");

        entries.forEach((entry, idx) => {
            const cell = document.createElement("div");
            cell.id = "table-cell-" + idx;
            cell.className = "flex items-center justify-center rounded-lg bg-slate-800/60 border border-slate-700/50 text-slate-600 text-xs sm:text-sm font-medium px-1 py-2 text-center select-none transition-all duration-300 min-h-[2.5rem]";
            cell.textContent = idx + 1;
            grid.appendChild(cell);
        });
        tc.appendChild(grid);
    }

    function revealInTable(idx, className) {
        const cell = document.getElementById("table-cell-" + idx);
        if (!cell) return;
        cell.textContent = entries[idx].display_name;
        if (className === "guessed") {
            cell.className = "flex items-center justify-center rounded-lg bg-green-500/20 border border-green-500/40 text-green-400 text-xs sm:text-sm font-medium px-1 py-2 text-center select-none transition-all duration-300 min-h-[2.5rem]";
        } else {
            cell.className = "flex items-center justify-center rounded-lg bg-red-500/15 border border-red-500/30 text-red-400 text-xs sm:text-sm font-medium px-1 py-2 text-center select-none transition-all duration-300 min-h-[2.5rem]";
        }
    }

    function updateTimer() {
        if (!startTime || quizEnded) return;
        const elapsed = Math.floor((Date.now() - startTime) / 1000);
        const mins = Math.floor(elapsed / 60);
        const secs = elapsed % 60;
        timerEl.textContent = mins + ":" + secs.toString().padStart(2, "0");
    }

    function giveUp() {
        if (quizEnded) return;
        if (correctCount === 0) {
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

        const elapsed = startTime ? Math.floor((Date.now() - startTime) / 1000) : 0;
        const mins = Math.floor(elapsed / 60);
        const secs = elapsed % 60;

        document.getElementById("results-correct").textContent = correctCount + "/" + totalCount;
        document.getElementById("results-score").textContent = score;
        document.getElementById("results-time").textContent = mins + ":" + secs.toString().padStart(2, "0");

        if (gaveUp) {
            document.getElementById("results-title").textContent = "Quiz Over";
            document.getElementById("results-subtitle").textContent = "You got " + correctCount + " out of " + totalCount;
        } else {
            document.getElementById("results-title").textContent = "Perfect Score!";
            document.getElementById("results-subtitle").textContent = "You named all " + totalCount + " in " + mins + "m " + secs + "s";
        }

        if (missed.length > 0) {
            const missedSection = document.getElementById("missed-section");
            const missedList = document.getElementById("missed-list");
            missedSection.classList.remove("hidden");
            missedList.innerHTML = missed
                .map(e => '<span class="px-2 py-1 rounded bg-red-500/20 text-red-400 text-sm">' + e.display_name + '</span>')
                .join("");
        }

        resultsModal.classList.remove("hidden");

        const bestKey = "geoquiz_best_" + quizId;
        const existing = localStorage.getItem(bestKey);
        const bestData = { correct: correctCount, total: totalCount, score: score, time: elapsed };
        if (!existing || JSON.parse(existing).score < score) {
            localStorage.setItem(bestKey, JSON.stringify(bestData));
        }
    }

    return { init: init };
})();

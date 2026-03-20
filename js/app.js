(() => {
    "use strict";

    const CATEGORY_ORDER = ["Continents", "Capitals", "United States", "Regional", "History", "Trivia"];

    let quizzes = null; // cached manifest

    async function loadManifest() {
        if (quizzes) return quizzes;
        const resp = await fetch("data/quizzes.json");
        quizzes = await resp.json();
        return quizzes;
    }

    function renderLanding(quizList) {
        const app = document.getElementById("app");

        // Group by category
        const categories = {};
        quizList.forEach(q => {
            if (!categories[q.category]) categories[q.category] = [];
            categories[q.category].push(q);
        });

        let html = `
            <div class="text-center mb-8">
                <h1 class="text-4xl font-bold text-white mb-2">GeoQuiz</h1>
                <p class="text-slate-400 text-lg">Test your geography knowledge. Free, no ads, no signup.</p>
            </div>
        `;

        CATEGORY_ORDER.forEach(cat => {
            const items = categories[cat];
            if (!items) return;

            html += `
                <div class="mb-6">
                    <button
                        class="category-toggle w-full flex items-center justify-between px-4 py-3 rounded-xl bg-surface-900 border border-slate-800 hover:border-slate-700 transition-colors group"
                        data-category="${cat}"
                        aria-expanded="true"
                    >
                        <div class="flex items-center gap-3">
                            <h2 class="text-lg font-semibold text-white">${cat}</h2>
                            <span class="text-xs px-2 py-0.5 rounded-full bg-slate-800 text-slate-500">${items.length}</span>
                        </div>
                        <svg class="category-chevron w-5 h-5 text-slate-500 group-hover:text-slate-300 transition-transform duration-200" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                        </svg>
                    </button>
                    <div class="category-content grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 mt-3">
            `;

            items.forEach(quiz => {
                html += `
                    <a href="#/quiz/${quiz.id}"
                       class="quiz-card group block rounded-xl border border-slate-800 bg-surface-900 hover:bg-surface-800 hover:border-slate-700 transition-all duration-200 overflow-hidden"
                       data-quiz-id="${quiz.id}">
                        <div class="p-4">
                            <h3 class="text-base font-semibold text-white group-hover:text-green-400 transition-colors mb-1">
                                ${quiz.title}
                            </h3>
                            <p class="text-slate-400 text-sm mb-3">${quiz.description}</p>
                            <div class="flex items-center justify-between">
                                <span class="text-sm text-slate-500">${quiz.entryCount} entries</span>
                                <span class="best-score text-sm text-green-500 font-medium hidden" data-quiz-id="${quiz.id}"></span>
                            </div>
                        </div>
                    </a>
                `;
            });

            html += `</div></div>`;
        });

        app.innerHTML = html;

        // Wire up category toggles
        app.querySelectorAll(".category-toggle").forEach(btn => {
            btn.addEventListener("click", () => {
                const content = btn.nextElementSibling;
                const chevron = btn.querySelector(".category-chevron");
                const expanded = btn.getAttribute("aria-expanded") === "true";
                btn.setAttribute("aria-expanded", !expanded);
                content.style.display = expanded ? "none" : "";
                chevron.style.transform = expanded ? "rotate(-90deg)" : "";
            });
        });

        // Show best scores from localStorage
        app.querySelectorAll(".best-score").forEach(el => {
            const best = localStorage.getItem("geoquiz_best_" + el.dataset.quizId);
            if (best) {
                const data = JSON.parse(best);
                el.textContent = "Best: " + data.correct + "/" + data.total;
                el.classList.remove("hidden");
            }
        });
    }

    function renderQuizPage(quizId) {
        const app = document.getElementById("app");
        const isMapQuiz = "UNKNOWN"; // will be set by quiz.js after loading data

        app.innerHTML = `
            <div id="quiz-container" data-quiz-id="${quizId}" class="flex flex-col lg:flex-row gap-4 h-[calc(100vh-5rem)]">
                <!-- Map or table area -->
                <div class="lg:w-[70%] w-full flex-shrink-0 bg-surface-900 rounded-xl border border-slate-800 overflow-hidden relative p-2">
                    <div id="quiz-display" class="w-full h-full flex items-center justify-center">
                        <div class="text-slate-600 text-sm">Loading...</div>
                    </div>
                </div>

                <!-- Sidebar -->
                <div id="quiz-sidebar" class="lg:w-[30%] w-full flex flex-col gap-3">
                    <div class="bg-surface-900 rounded-xl border border-slate-800 p-4">
                        <div class="flex items-center justify-between mb-3">
                            <div class="text-2xl font-bold text-white">
                                <span id="correct-count">0</span> / <span id="total-count">0</span>
                            </div>
                            <div class="text-lg font-mono text-slate-400" id="timer">0:00</div>
                        </div>
                        <div class="w-full bg-slate-800 rounded-full h-2">
                            <div class="bg-green-500 h-2 rounded-full transition-all duration-300" id="progress-bar" style="width: 0%"></div>
                        </div>
                        <div class="mt-2 text-sm text-slate-500">
                            Score: <span id="score-display" class="text-green-400 font-medium">0</span>
                        </div>
                    </div>

                    <div class="relative">
                        <input type="text" id="quiz-input"
                            class="w-full px-4 py-3 bg-surface-900 border border-slate-700 rounded-xl text-white text-lg placeholder-slate-500 focus:outline-none focus:border-green-500 focus:ring-1 focus:ring-green-500 transition-colors"
                            placeholder="Type an answer..."
                            autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false" autofocus>
                    </div>

                    <div class="bg-surface-900 rounded-xl border border-slate-800 p-4 flex-1 overflow-y-auto" id="recent-guesses-container">
                        <h3 class="text-sm font-medium text-slate-500 mb-2">Recent guesses</h3>
                        <div id="recent-guesses" class="flex flex-col gap-1.5"></div>
                    </div>

                    <button id="give-up-btn"
                        class="w-full py-3 px-4 rounded-xl border border-slate-700 text-slate-400 hover:text-red-400 hover:border-red-500/50 transition-colors text-sm font-medium">
                        Give Up
                    </button>
                </div>
            </div>
        `;

        // Load quiz.js if not already loaded, then initialize
        if (!window.GeoQuizEngine) {
            const s = document.createElement("script");
            s.src = "js/quiz.js";
            s.onload = () => window.GeoQuizEngine.init(quizId);
            document.body.appendChild(s);
        } else {
            window.GeoQuizEngine.init(quizId);
        }
    }

    // --- Router ---
    async function route() {
        const hash = window.location.hash || "#/";
        const quizMatch = hash.match(/^#\/quiz\/(.+)$/);

        if (quizMatch) {
            renderQuizPage(quizMatch[1]);
        } else {
            const manifest = await loadManifest();
            renderLanding(manifest);
        }
    }

    window.addEventListener("hashchange", route);
    route();
})();

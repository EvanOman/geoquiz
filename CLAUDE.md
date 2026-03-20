# GeoQuiz

Geography quiz game — a free, ad-free Sporcle alternative. Type country/state names into a text box; the SVG map fills in and tracks your score.

## Quick Start

```bash
cd /home/evan/dev/geoquiz
just dev          # Dev server with hot reload (port 9100)
just test         # Run tests
just lint         # Lint check
just fix          # Auto-fix lint issues
```

Production service runs on port 9500 via systemd user service:
```bash
systemctl --user status geoquiz
systemctl --user restart geoquiz
```

Tailscale Serve exposes it at `/geoquiz` on the tailnet.

## Architecture

### Tech Stack
- **Backend:** FastAPI + Jinja2 + uvicorn
- **Frontend:** Tailwind CSS (CDN) + vanilla JavaScript (no build step)
- **Maps:** Inline SVGs from Wikimedia Commons, included via Jinja2 `{% include %}`
- **Data:** Python dataclasses in `src/geoquiz/data/` — no database

### How a Quiz Works (Request Flow)

1. User visits `/quiz/{quiz_id}` — FastAPI renders `quiz.html` with the SVG map inlined
2. On page load, `quiz.js` fetches `/api/quiz/{quiz_id}` which returns JSON with all entries and their accepted answers
3. JS builds a `Map<normalized_answer, entry_index>` for O(1) lookup
4. On every keystroke (`input` event), the current input value is normalized and checked against the Map
5. On match: input clears, SVG path gets `.guessed` class (turns green), counter increments, score updates
6. No Enter key needed — matches happen instantly (Sporcle-style)

### Answer Matching (in quiz.js)

The `normalize()` function transforms both accepted answers (at init) and user input (on every keystroke):
```
lowercase → trim → NFD decompose → strip diacritics → strip leading articles → strip punctuation → collapse whitespace → trim
```

Key: accepted answers in the Python data files are **already lowercase**. The JS normalizer also lowercases, so matching is case-insensitive.

### Reverse Proxy Support (BASE_PATH)

When served behind Tailscale Serve at `/geoquiz`, the proxy strips the prefix before forwarding to the app. The app always handles routes at `/`, `/quiz/...`, `/api/...`, `/static/...`.

A client-side script in `base.html` detects the prefix from `window.location.pathname` and:
1. Sets `window.BASE_PATH` (used by quiz.js for API fetch URLs)
2. Rewrites all absolute `<a href>`, `<script src>`, `<link href>` attributes on DOMContentLoaded

### SVG Map IDs

Maps use ISO alpha-2 lowercase codes as element IDs (`<path id="de">` for Germany, `<g id="gb">` for UK group). US states use lowercase abbreviations (`<path id="tx">`). The `highlightOnMap()` function tries the ID as-is, then uppercase.

## File Structure

```
src/geoquiz/
  app.py              # FastAPI routes: GET /, GET /quiz/{id}, GET /api/quiz/{id}
  config.py           # BASE_DIR / TEMPLATES_DIR / STATIC_DIR paths
  data/
    registry.py       # Quiz + QuizEntry dataclasses, quiz registry
    europe_countries.py   # 47 entries
    africa_countries.py   # 54 entries
    asia_countries.py     # 49 entries
    north_america_countries.py  # 23 entries
    south_america_countries.py  # 12 entries
    oceania_countries.py  # 14 entries
    us_states.py          # 50 entries

static/js/quiz.js     # Client-side quiz engine (matching, scoring, SVG highlighting)

templates/
  base.html           # Layout: Tailwind, dark mode, SVG CSS, BASE_PATH detection
  index.html          # Landing page with quiz card grid + category filters
  quiz.html           # Quiz page: map + input + score bar + results modal
  maps/*.svg          # Cleaned SVG maps with ISO-coded path IDs

geoquiz.service       # systemd unit template (actual file at ~/.config/systemd/user/)
```

## Quiz Data Format

Each quiz data file exports a `QUIZ` constant:
```python
QUIZ = Quiz(
    id="europe-countries",        # URL slug
    title="Countries of Europe",  # Display title
    description="...",
    map_template="maps/europe.svg",  # Jinja2 include path
    time_limit=564,               # Seconds (entries * 12)
    category="Continents",        # For landing page filter
    entries=[
        QuizEntry("de", "Germany", ["germany", "deutschland"]),
        # id = SVG element ID, display_name = shown on map, accepted_answers = all valid inputs
    ],
)
```

## Scoring

- Base: 100 points per correct answer
- Speed multiplier based on elapsed time vs. time_limit:
  - First 25%: 2x (200 pts)
  - 25-50%: 1.5x (150 pts)
  - 50-75%: 1.25x (125 pts)
  - After 75%: 1x (100 pts)
- Best scores saved in localStorage (`geoquiz_best_{quiz_id}`)

## Known Issues / Debugging

### The input matching relies on the `input` event
The quiz engine listens for the DOM `input` event on the text field. If this event doesn't fire (e.g., due to mobile browser behavior, autocomplete interference, or the input not being properly focused), answers won't match. The input field has `autocomplete="off"`, `autocorrect="off"`, `autocapitalize="off"`, `spellcheck="false"` attributes to reduce interference.

### SVG maps vary in quality
- Europe, US States, Africa: clean with proper ISO-coded IDs
- Asia, North/South America: very large files (4-7MB), converted from verbose Wikimedia SVGs
- Oceania: only Australia, New Zealand, PNG, and Solomon Islands have proper IDs
- Some maps have unidentified background paths (non-quiz countries, water, etc.)

### CSS specificity for map highlighting
The base fill rule uses `#map-container svg path` (ID selector = high specificity). The guessed/missed rules use `#map-container .country.guessed` to match. If you add new CSS rules for map paths, ensure they don't override the guessed/missed states.

# gemini.md — Project Context for AI Assistants

> This file gives full project context to any AI assistant (Gemini, Claude, Copilot) working on this codebase.

---

## Project Name
**CineMatch** — Hybrid Movie Recommendation System

## Tech Stack
| Layer | Technology |
|---|---|
| Backend | Python 3.x, Flask |
| ML | scikit-learn (TF-IDF, SVD, cosine similarity), scipy |
| Data | pandas, numpy |
| Dataset | MovieLens Small (ml-latest-small) |
| Frontend | Jinja2 templates, vanilla CSS, Google Fonts |
| Dev | Antigravity IDE |

---

## Project Structure

```
movie_recommender/
├── data/
│   ├── movies.csv          # movieId, title, genres
│   └── ratings.csv         # userId, movieId, rating, timestamp
├── templates/
│   └── index.html          # Full Netflix-themed frontend
├── app.py                  # Flask routes
├── recommender.py          # All ML logic
├── requirements.txt        # Dependencies
├── README.md
├── gemini.md               # ← This file
└── guidelines.md           # Coding & design standards
```

---

## Recommendation Logic

### Content-Based Filtering
- Extracts movie genres from `movies.csv`
- Applies **TF-IDF vectorization** on cleaned genre strings
- Computes **cosine similarity** between all movie vectors
- Returns top-N most similar movies by genre overlap

### Collaborative Filtering
- Builds a **user-movie rating matrix** from `ratings.csv`
- Applies **TruncatedSVD** (20 components) to find latent factors
- Uses **cosine similarity** on user latent vectors to find similar users
- Recommends highly-rated movies from similar users that the target user hasn't seen

### Hybrid Logic
- Runs both engines independently
- Merges results: content picks come first, collaborative fills the rest
- Deduplication ensures no repeats
- Returns exactly N results (default: 10)

---

## Key Functions in `recommender.py`

| Function | Input | Output |
|---|---|---|
| `content_recommendations(title, n)` | Movie title string | List of N title strings |
| `collab_recommendations(user_id, n)` | Integer user ID | List of N title strings |
| `hybrid_recommendations(title, user_id, n)` | Title + user ID | List of N title strings |
| `get_all_titles()` | — | Sorted list of all movie titles |
| `get_movie_genres(title)` | Movie title string | Genre string (e.g. "Action · Drama") |

---

## Flask Routes

| Route | Method | Description |
|---|---|---|
| `/` | GET | Renders empty home page with search form |
| `/` | POST | Accepts `title` and `user_id`, returns recommendations |

### Form Fields
- `title` (string) — movie title, must exist in `movies.csv`
- `user_id` (int) — valid user ID from 1–610

### Template Variables Passed to `index.html`
- `recommendations` — list of dicts: `{title, genres}`
- `titles` — all movie titles for autocomplete datalist
- `error` — error message string or None
- `selected_title` — persists form value on reload
- `selected_user` — persists user ID on reload
- `genres` — genre string for the selected movie

---

## Design System

| Token | Value |
|---|---|
| `--red` | `#E50914` |
| `--red-dim` | `#8B0000` |
| `--black` | `#0A0A0A` |
| `--surface` | `#111111` |
| `--card` | `#161616` |
| `--border` | `rgba(229,9,20,0.15)` |
| `--text` | `#F0F0F0` |
| `--muted` | `#888` |
| Display font | Bebas Neue |
| Body font | DM Sans |

---

## Dataset Notes
- Source: [MovieLens Small](https://grouplens.org/datasets/movielens/latest/)
- `movies.csv` columns: `movieId`, `title`, `genres` (pipe-separated)
- `ratings.csv` columns: `userId`, `movieId`, `rating`, `timestamp`
- Valid user IDs: 1–610
- Total movies: ~9,700
- Total ratings: ~100,000

---

## Known Constraints
- Render (cloud) uses an ephemeral filesystem — if deploying, avoid file-based storage
- No database — all data loaded into memory at startup
- Cold start may be slow (~3–5s) due to SVD computation on load
- `recommeder.py` (typo duplicate) should be deleted — only `recommender.py` is used

---

## Environment
- Python 3.10+
- Install: `pip install -r requirements.txt`
- Run locally: `python app.py` → http://127.0.0.1:5000
- Debug mode: enabled in `app.py` (disable for production)
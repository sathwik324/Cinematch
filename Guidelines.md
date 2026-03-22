# guidelines.md — Coding & Design Standards

> Rules for anyone (human or AI) contributing to CineMatch. Follow these strictly.

---

## 1. Python Standards

### General
- Python 3.10+ only
- Use `f-strings` for all string formatting — no `.format()` or `%`
- All functions must have a docstring (one-liner is fine for small ones)
- Use type hints where practical

### File Responsibilities
- `recommender.py` — **ML only**. No Flask imports. No routing logic.
- `app.py` — **Flask only**. No raw pandas/numpy. Call functions from `recommender.py`.
- Never mix concerns between these two files.

### Error Handling
- All route handlers in `app.py` must wrap ML calls in `try/except`
- Catch `ValueError` separately for invalid user ID input
- Never let an uncaught exception crash the Flask server in production

### Data Loading
- CSVs are loaded **once** at module level in `recommender.py` (not inside functions)
- SVD and TF-IDF are computed **once** at startup — never recompute per request

---

## 2. Flask Standards

- Always use `render_template` — never return raw HTML strings
- Form values must be `.strip()`-ed before processing
- Pass all template variables explicitly — no `**locals()` shortcuts
- Keep routes thin: validate input → call recommender function → pass to template
- Debug mode (`debug=True`) is fine for local dev, must be `False` for production

---

## 3. HTML/CSS Standards

### Structure
- All HTML lives in `templates/index.html` — single template, no partials (for now)
- Use semantic HTML: `<nav>`, `<section>`, `<footer>`, etc.
- All interactive elements must be keyboard accessible

### CSS Rules
- All colors defined as CSS variables in `:root` — never hard-code hex values inside selectors
- Mobile-first breakpoints — `max-width: 600px` for small screens
- Animations use `animation-delay` per `.movie-card:nth-child(n)` — do not use JS for card stagger
- No external CSS frameworks (no Bootstrap, Tailwind) — pure custom CSS only
- No JavaScript except what is absolutely needed (currently: none)

### Design Tokens (Do Not Change)
```
--red:     #E50914   ← Primary accent, CTAs, borders, highlights
--black:   #0A0A0A   ← Page background
--card:    #161616   ← Card backgrounds
--text:    #F0F0F0   ← Body text
--muted:   #888      ← Labels, secondary text, genres
```

### Typography
- `Bebas Neue` — headings, logo, card numbers, button labels
- `DM Sans` — all body text, inputs, labels
- Never use Arial, Inter, Roboto, or system fonts
- Font sizes: never below `0.72rem`, never above `6rem` on hero

---

## 4. Naming Conventions

| Type | Convention | Example |
|---|---|---|
| Python functions | `snake_case` | `hybrid_recommendations` |
| Python variables | `snake_case` | `movie_indices` |
| HTML classes | `kebab-case` | `movie-card`, `form-wrapper` |
| CSS variables | `--kebab-case` | `--red-dim` |
| Template files | `snake_case.html` | `index.html` |

---

## 5. What NOT To Do

- ❌ Do NOT add a database (SQLite, PostgreSQL, etc.) unless explicitly required
- ❌ Do NOT add user authentication
- ❌ Do NOT import recommender logic directly into HTML templates
- ❌ Do NOT use localStorage or client-side state
- ❌ Do NOT add JavaScript frameworks (React, Vue, Alpine)
- ❌ Do NOT change the color palette without updating all CSS variables
- ❌ Do NOT recompute SVD on every request — it's expensive
- ❌ Do NOT leave `recommeder.py` (typo file) in the project
- ❌ Do NOT commit `data/*.csv` to version control if the repo goes public (files are large)

---

## 6. Adding New Features (Guidelines)

### Adding a new recommendation strategy
1. Write the function in `recommender.py`
2. Import and call it in `app.py`
3. Pass results to the template as a new variable
4. Render in `index.html` with the same card component pattern

### Adding a new route
1. Define it in `app.py` with full try/except
2. Create a new template in `templates/`
3. Follow the same CSS variable system for consistency

### Changing the UI theme
1. Only touch CSS variables in `:root`
2. Do not hard-code any colors elsewhere
3. Test on mobile (600px breakpoint) after any layout changes

---

## 7. Performance Notes

- SVD with 20 components on 610 users × ~9700 movies is fast enough locally
- Cold start: ~2–5 seconds (acceptable)
- If deploying on a free-tier server, consider caching the SVD matrix with `joblib.dump`
- For production scale, replace in-memory matrices with a vector database (e.g. Pinecone, Weaviate)

---

## 8. Git Commit Style

```
feat: add hybrid recommendation engine
fix: correct movie_indices iloc double-bracket bug
style: update card hover border color
refactor: separate content and collab logic into helpers
docs: update README with dataset setup instructions
```

Use conventional commits. Keep messages under 72 characters.

---

## 9. File Checklist Before Pushing

- [ ] `recommender.py` exists and has no Flask imports
- [ ] `app.py` exists and all routes have error handling
- [ ] `templates/index.html` exists with correct Jinja2 variables
- [ ] `requirements.txt` is up to date
- [ ] `data/movies.csv` and `data/ratings.csv` are present locally (not committed)
- [ ] `recommeder.py` (typo) is deleted
- [ ] `debug=True` is off if deploying
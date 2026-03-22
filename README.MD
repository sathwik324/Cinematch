# 🎬 CineMatch — Hybrid Movie Recommender

A Netflix-inspired movie recommendation system using a hybrid approach (content-based + collaborative filtering), built with Flask and scikit-learn.

## Tech Stack
- Python, Flask
- scikit-learn (TF-IDF, SVD, cosine similarity)
- pandas, numpy, scipy
- MovieLens Small Dataset

## Setup
1. Download MovieLens dataset: https://grouplens.org/datasets/movielens/latest/
2. Place `movies.csv` and `ratings.csv` inside `data/`
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `python app.py`
5. Open: http://127.0.0.1:5000

## How It Works
- **Content-Based**: TF-IDF on movie genres → cosine similarity
- **Collaborative**: SVD matrix factorization on user-movie ratings → similar user preferences
- **Hybrid**: Merges both, prioritising content matches, filled by collaborative picks
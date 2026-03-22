import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
from sklearn.decomposition import TruncatedSVD

# Load data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
movies = pd.read_csv(os.path.join(BASE_DIR, "data", "ml-latest-small", "ml-latest-small", "movies.csv"))
ratings = pd.read_csv(os.path.join(BASE_DIR, "data", "ml-latest-small", "ml-latest-small", "ratings.csv"))

# ── CONTENT-BASED FILTERING ─────────────────────────────────
movies["genres_clean"] = movies["genres"].str.replace("|", " ", regex=False)
tfidf = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf.fit_transform(movies["genres_clean"])
content_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
movie_indices = pd.Series(movies.index, index=movies["title"]).drop_duplicates()

def content_recommendations(title, n=10):
    if title not in movie_indices:
        return []
    idx = movie_indices[title]
    scores = list(enumerate(content_sim[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:n+1]
    return movies["title"].iloc[[i for i, _ in scores]].tolist()

# ── COLLABORATIVE FILTERING (SVD) ───────────────────────────
user_movie_matrix = ratings.pivot_table(
    index="userId", columns="movieId", values="rating"
).fillna(0)

svd = TruncatedSVD(n_components=20, random_state=42)
latent_matrix = svd.fit_transform(csr_matrix(user_movie_matrix))
collab_sim = cosine_similarity(latent_matrix)

def collab_recommendations(user_id, n=10):
    if user_id not in user_movie_matrix.index:
        return []
    user_idx = user_movie_matrix.index.get_loc(user_id)
    sim_scores = list(enumerate(collab_sim[user_idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:6]
    similar_users = [user_movie_matrix.index[i] for i, _ in sim_scores]
    already_watched = set(ratings[ratings["userId"] == user_id]["movieId"])
    recs = (
        ratings[
            ratings["userId"].isin(similar_users) &
            ~ratings["movieId"].isin(already_watched)
        ]
        .groupby("movieId")["rating"]
        .mean()
        .sort_values(ascending=False)
        .head(n)
        .index.tolist()
    )
    return movies[movies["movieId"].isin(recs)]["title"].tolist()

# ── HYBRID ──────────────────────────────────────────────────
def hybrid_recommendations(title, user_id, n=10):
    content = content_recommendations(title, n)
    collab  = collab_recommendations(user_id, n)
    seen, merged = set(), []
    for t in content + collab:
        if t not in seen:
            seen.add(t)
            merged.append(t)
        if len(merged) == n:
            break
    return merged

def get_all_titles():
    return sorted(movies["title"].tolist())

def get_movie_genres(title):
    row = movies[movies["title"] == title]
    if row.empty:
        return ""
    return row.iloc[0]["genres"].replace("|", " · ")
from flask import Flask, render_template, request, jsonify
from recommender import hybrid_recommendations, get_all_titles, get_movie_genres

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    recommendations = []
    error = None
    selected_title = ""
    selected_user = ""
    genres = ""
    titles = get_all_titles()

    if request.method == "POST":
        title   = request.form.get("title", "").strip()
        user_id = request.form.get("user_id", "").strip()
        selected_title = title
        selected_user  = user_id

        if not title or not user_id:
            error = "Please enter both a movie title and a user ID."
        else:
            try:
                recs = hybrid_recommendations(title, int(user_id))
                if not recs:
                    error = "No recommendations found. Try a different title or user ID."
                else:
                    recommendations = [
                        {"title": r, "genres": get_movie_genres(r)}
                        for r in recs
                    ]
                genres = get_movie_genres(title)
            except ValueError:
                error = "User ID must be a number between 1 and 610."
            except Exception as e:
                error = f"Something went wrong: {str(e)}"

    return render_template("index.html",
                           recommendations=recommendations,
                           titles=titles,
                           error=error,
                           selected_title=selected_title,
                           selected_user=selected_user,
                           genres=genres)

if __name__ == "__main__":
    app.run(debug=True)
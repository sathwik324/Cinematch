import requests
from flask import Flask, render_template, request

app = Flask(__name__)

HF_API = "https://sathwik324-cinematch-api.hf.space"

@app.route("/", methods=["GET", "POST"])
def index():
    recommendations = []
    error = None
    selected_title = ""
    selected_user = ""
    genres = ""
    titles = []

    try:
        res = requests.get(f"{HF_API}/titles", timeout=10)
        titles = res.json().get("titles", [])
    except:
        error = "Could not load movie titles. API may be starting up."

    if request.method == "POST":
        title   = request.form.get("title", "").strip()
        user_id = request.form.get("user_id", "").strip()
        selected_title = title
        selected_user  = user_id

        if not title or not user_id:
            error = "Please enter both a movie title and a user ID."
        else:
            try:
                res = requests.post(
                    f"{HF_API}/recommend",
                    json={"title": title, "user_id": int(user_id)},
                    timeout=30
                )
                data = res.json()
                recommendations = data.get("recommendations", [])
                if recommendations:
                    genres = recommendations[0].get("genres", "")
                if not recommendations:
                    error = "No recommendations found. Try a different title or user ID."
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

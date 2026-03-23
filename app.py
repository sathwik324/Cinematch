import requests
from flask import Flask, render_template, request, Response

app = Flask(__name__)

HF_API = "https://sathwik324-cinematch-api.hf.space"

@app.route("/search")
def search():
    q = request.args.get("q", "")
    if not q:
        from flask import jsonify
        return jsonify([])
    try:
        res = requests.get(f"{HF_API}/search", params={"q": q}, timeout=10)
        return Response(res.content, mimetype='application/json')
    except Exception:
        from flask import jsonify
        return jsonify([])

@app.route("/", methods=["GET", "POST"])
def index():
    recommendations = []
    error = None
    selected_title = ""
    genres = ""

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        selected_title = title

        if not title:
            error = "Please enter a movie title."
        else:
            try:
                res = requests.post(
                    f"{HF_API}/recommend",
                    json={"title": title},
                    timeout=30
                )
                data = res.json()
                recommendations = data.get("recommendations", [])
                if recommendations:
                    genres = recommendations[0].get("genres", "")
                if not recommendations:
                    error = "No recommendations found. Try a different title."
            except Exception as e:
                error = f"Something went wrong: {str(e)}"

    return render_template("index.html",
                           recommendations=recommendations,
                           error=error,
                           selected_title=selected_title,
                           genres=genres)

if __name__ == "__main__":
    app.run(debug=True)

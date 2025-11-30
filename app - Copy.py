from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Path where dataset images exist
DATASET_DIR = "static/dataset"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/recognize", methods=["POST"])
def recognize():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    filepath = "static/uploaded.jpg"
    file.save(filepath)

    # Mock recognition logic (Replace later)
    result = {
        "match": "alice.png",
        "distance": 0.79
    }

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)

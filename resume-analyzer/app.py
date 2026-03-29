from flask import Flask, render_template, request
import os
from analyzer import extract_text, analyze_resume

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Load skills
with open("skills.txt", "r") as f:
    skills_list = [line.strip().lower() for line in f.readlines()]


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["resume"]

        if file:
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

            text = extract_text(filepath)
            if text == "ERROR":
             return "⚠️ Unable to read this PDF. Please upload a valid resume PDF."
            score, found, missing, suggestions = analyze_resume(text, skills_list)

            return render_template("index.html",
                                   score=score,
                                   found=found,
                                   missing=missing,
                                   suggestions=suggestions)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

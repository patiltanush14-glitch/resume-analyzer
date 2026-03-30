from flask import Flask, render_template, request
import os
from analyzer import extract_text, analyze_resume

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Load skills
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, "skills.txt")) as f:
    skills_list = [line.strip().lower() for line in f.readlines()]


@app.route("/", methods=["GET", "POST"])
def index():
    try:
        if request.method == "POST":
            file = request.files["resume"]
            filepath = "resume.pdf"
            file.save(filepath)

            text = extract_text(filepath)

            if text == "ERROR":
                return "⚠️ Unable to read this PDF. Please upload a valid resume PDF."

            # Read skills
            import os
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            with open(os.path.join(BASE_DIR, "skills.txt")) as f:
                skills = [line.strip().lower() for line in f]

            score, found, missing, suggestions = analyze_resume(text, skills)

            return render_template(
                "index.html",
                score=score,
                found=found,
                missing=missing,
                suggestions=suggestions
            )

        return render_template("index.html")

    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
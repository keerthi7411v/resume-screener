"""Smart Resume Screener Pro - Flask application.

Run locally:   python app.py
Deploy:        works on Replit / Render / any Python host (templates + static included).
"""
import os
import uuid
from flask import Flask, render_template, request, redirect, url_for

from resume_parser import extract_text
from preprocessor import preprocess
from skills_extractor import extract_skills, skill_gap
from matcher import content_score, final_score
from ranker import rank_candidates

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
ALLOWED = {".pdf", ".docx", ".txt"}

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 32 * 1024 * 1024   # 32 MB uploads
os.makedirs(UPLOAD_DIR, exist_ok=True)


def analyze(resume_paths, jd_raw):
    jd_clean = preprocess(jd_raw)
    jd_skills = extract_skills(jd_raw)

    raws = [extract_text(p) for p in resume_paths]
    resumes = [preprocess(r) for r in raws]
    contents = content_score(resumes, jd_clean) if resumes else []

    rows = []
    for path, raw, content in zip(resume_paths, raws, contents):
        r_skills = extract_skills(raw)
        matching, missing = skill_gap(r_skills, jd_skills)
        ratio = len(matching) / len(jd_skills) if jd_skills else 0
        name = os.path.splitext(os.path.basename(path))[0]
        name = name[9:] if len(name) > 9 and name[:8].isalnum() else name  # strip uuid prefix
        rows.append({
            "name": name,
            "score": final_score(content, ratio),
            "content_score": content,
            "match_ratio": round(ratio * 100, 1),
            "resume_skills": ", ".join(sorted(r_skills)) or "-",
            "matching_skills": ", ".join(matching) or "-",
            "missing_skills": ", ".join(missing) or "-",
        })
    return rank_candidates(rows), sorted(jd_skills)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/screen", methods=["POST"])
def screen():
    jd_raw = request.form.get("job_description", "")
    files = request.files.getlist("resumes")
    if not jd_raw.strip() or not files:
        return redirect(url_for("index"))

    paths = []
    for f in files:
        ext = os.path.splitext(f.filename)[1].lower()
        if f and ext in ALLOWED:
            p = os.path.join(UPLOAD_DIR, f"{uuid.uuid4().hex[:8]}_{f.filename}")
            f.save(p)
            paths.append(p)
    if not paths:
        return redirect(url_for("index"))

    ranked, jd_skills = analyze(paths, jd_raw)
    records = ranked.to_dict("records")
    return render_template("results.html", tables=records,
                           jd_skills=", ".join(jd_skills), n=len(records))



if __name__ == "__main__":
    app.run(debug=True)

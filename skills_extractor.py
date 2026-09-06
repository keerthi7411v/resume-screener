"""Skill & keyword extraction using a curated technology taxonomy.

Each canonical skill maps to a list of surface forms / synonyms so that
"ML", "machine learning" and "scikit-learn" all count as evidence.
"""
import re

SKILL_TAXONOMY = {
    "python": ["python"],
    "machine learning": ["machine learning", "ml", "supervised learning", "unsupervised learning"],
    "deep learning": ["deep learning", "neural network", "neural networks", "cnn", "rnn", "lstm"],
    "nlp": ["nlp", "natural language processing", "text mining", "text analytics"],
    "data analysis": ["data analysis", "data analytics", "data mining", "eda"],
    "data visualization": ["data visualization", "matplotlib", "seaborn", "power bi", "tableau", "plotly"],
    "sql": ["sql", "mysql", "postgresql", "sqlite", "oracle"],
    "nosql": ["nosql", "mongodb", "cassandra", "dynamodb", "elasticsearch"],
    "statistics": ["statistics", "statistical analysis", "hypothesis testing", "a/b testing", "regression"],
    "tensorflow": ["tensorflow", "tf", "keras"],
    "pytorch": ["pytorch", "torch"],
    "scikit-learn": ["scikit-learn", "sklearn"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "spacy": ["spacy"],
    "nltk": ["nltk"],
    "flask": ["flask"],
    "fastapi": ["fastapi"],
    "django": ["django"],
    "rest api": ["rest api", "restful", "api development", "microservices"],
    "git": ["git", "github", "gitlab", "bitbucket", "version control"],
    "docker": ["docker", "containerization", "kubernetes", "k8s"],
    "aws": ["aws", "amazon web services", "ec2", "s3", "lambda"],
    "azure": ["azure", "microsoft azure"],
    "gcp": ["gcp", "google cloud"],
    "java": ["java"],
    "c++": ["c++"],
    "javascript": ["javascript", "js", "es6"],
    "react": ["react", "reactjs", "react.js"],
    "html/css": ["html", "css", "html5", "css3"],
    "excel": ["excel", "ms excel", "spreadsheet"],
    "spark": ["spark", "pyspark", "apache spark"],
    "hadoop": ["hadoop", "hive", "big data"],
    "linux": ["linux", "unix", "bash", "shell scripting"],
    "agile": ["agile", "scrum", "jira"],
    "communication": ["communication", "teamwork", "collaboration", "stakeholder"],
    "computer vision": ["computer vision", "opencv", "image processing"],
}


def extract_skills(text):
    """Return the set of canonical skills found in *text* (case-insensitive,
    word-boundary matched)."""
    text_lower = " " + text.lower() + " "
    found = set()
    for canonical, variants in SKILL_TAXONOMY.items():
        for v in variants:
            if re.search(r"(?<![a-zA-Z+#])" + re.escape(v) + r"(?![a-zA-Z])", text_lower):
                found.add(canonical)
                break
    return found


def skill_gap(resume_skills, jd_skills):
    """Split skills into (matching, missing) relative to the job description."""
    return sorted(resume_skills & jd_skills), sorted(jd_skills - resume_skills)

"""Resume <-> job-description similarity scoring with TF-IDF + cosine similarity."""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def content_score(resume_texts, jd_text):
    """Return a 0-100 content-similarity score per resume.

    resume_texts : list of preprocessed resume strings
    jd_text      : preprocessed job-description string
    """
    corpus = [jd_text] + list(resume_texts)
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
    tfidf = vectorizer.fit_transform(corpus)
    sims = cosine_similarity(tfidf[0:1], tfidf[1:]).flatten()
    return [round(float(s) * 100, 2) for s in sims]


def final_score(content, match_ratio, w_content=0.6, w_skills=0.4):
    """Blend TF-IDF similarity with the skill-coverage ratio."""
    return round(w_content * content + w_skills * 100 * match_ratio, 2)

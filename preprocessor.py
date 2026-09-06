"""Text cleaning and normalization for resume / job-description text."""
import re
import string

STOPWORDS = set("""
a an the and or of to in for on with at by from as is are was were be been being
this that these those it its i me my we our you your he she his her they them
their have has had do does did will would can could should may might must
""".split())


def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\.\S+", " ", text)          # URLs
    text = re.sub(r"[^a-zA-Z+#./\-]", " ", text)             # keep tech chars
    text = re.sub(r"[{}]+".format(re.escape(string.punctuation.replace("+#./-", ""))), " ", text)
    return re.sub(r"\s+", " ", text).strip()


def tokenize(text):
    return [t for t in clean_text(text).split() if t not in STOPWORDS and len(t) > 1]


def preprocess(text):
    return " ".join(tokenize(text))

import re
from sklearn.feature_extraction.text import TfidfVectorizer


# -------------------------------
# CLEAN TEXT
# -------------------------------
def clean_text(text):

    text = text.lower()

    # remove special chars
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# -------------------------------
# APPLY CLEANING
# -------------------------------
def preprocess_dataset(data):

    texts = []
    labels = []

    for item in data:

        text = clean_text(item["text"])
        label = item["is_requirement"]

        if not text:
            continue

        texts.append(text)
        labels.append(label)

    return texts, labels


# -------------------------------
# VECTORIZATION
# -------------------------------
def vectorize(texts):

    vectorizer = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2)   # unigram + bigram
    )

    X = vectorizer.fit_transform(texts)

    return X, vectorizer
import re


# -------------------------------
# CLEAN TEXT
# -------------------------------
def clean_text(text):

    text = text.lower()

    # remove junk
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"\d+", "", text)
    text = re.sub(r"[^a-z\s]", "", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# -------------------------------
# VALID REQUIREMENT FILTER
# -------------------------------
def is_valid_requirement(text):

    if len(text) < 25:
        return False

    if any(x in text for x in [
        "error", "crash", "http", "bug",
        "stacktrace", "exception"
    ]):
        return False

    return True


# -------------------------------
# SIMPLE RANKING
# -------------------------------
def rank_requirements(reqs):

    # prioritize "should", "must"
    def score(r):
        r = r.lower()
        if "must" in r:
            return 3
        if "should" in r:
            return 2
        return 1

    return sorted(reqs, key=score, reverse=True)
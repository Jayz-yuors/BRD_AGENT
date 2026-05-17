import json
import re
from collections import defaultdict, Counter
from ml_training.data_loader import load_all_datasets


OUTPUT_PATH = r"C:\Users\Shruti\jk\Python\Python_GUI\Project_series\6.BRD_Agent\dataPush\feature_keywords.json"

STOPWORDS = {
    "should","system","this","that","with","will","have","from","your",
    "there","also","which","would","these","their","about","please",
    "when","into","using","been","being","over","under","more"
}


def is_valid_word(word):

    if len(word) < 4:
        return False

    if re.search(r"\d", word):
        return False

    if "@" in word or "/" in word:
        return False

    if word in STOPWORDS:
        return False

    return True


def build_feature_dict():

    data = load_all_datasets()

    feature_map = defaultdict(list)

    for item in data:

        if item["is_requirement"] != 1:
            continue

        text = item["text"].lower()
        words = text.split()

        feature = item["type"]

        for word in words:

            word = word.strip(".,!?\"'()[]{}")

            if is_valid_word(word):
                feature_map[feature].append(word)

    final_map = {}

    for feature, words in feature_map.items():

        counter = Counter(words)

        # 🔥 REMOVE GENERIC WORDS AGAIN
        filtered = [
            w for w, c in counter.items()
            if c > 50 and w not in STOPWORDS
        ]

        final_map[feature] = filtered[:50]

    return final_map


def save(data):

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print(f"\n✅ Clean feature dictionary saved at: {OUTPUT_PATH}")


if __name__ == "__main__":

    data = build_feature_dict()
    save(data)
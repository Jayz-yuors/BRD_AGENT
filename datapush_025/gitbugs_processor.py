import os
import pandas as pd
import json
import re

# -------------------------------
# PATHS
# -------------------------------
BASE_PATH = r"C:\Users\Shruti\jk\Python\Python_GUI\Project_series\6.BRD_Agent\datasets\Gitbugs\gitbugs"

OUTPUT_PATH = r"C:\Users\Shruti\jk\Python\Python_GUI\Project_series\6.BRD_Agent\dataPush\ml_ready_gitbugs.json"


# -------------------------------
# LOAD CSV (SAFE ENCODING)
# -------------------------------
def load_csv_safe(path):
    try:
        return pd.read_csv(path, encoding="latin-1")
    except:
        try:
            return pd.read_csv(path, encoding="cp1252")
        except Exception as e:
            print(f"❌ Failed to load: {path}")
            return None


# -------------------------------
# TEXT CLEANING (VERY IMPORTANT)
# -------------------------------
def clean_text(text):

    text = str(text)

    # remove URLs
    text = re.sub(r"http\S+", "", text)

    # remove code blocks {code} ... {/code}
    text = re.sub(r"\{code.*?\}", "", text, flags=re.DOTALL)

    # remove HTML tags
    text = re.sub(r"<.*?>", "", text)

    # remove special characters
    text = re.sub(r"[^a-zA-Z0-9.,!?()\- ]+", " ", text)

    # remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# -------------------------------
# VALID DATA FILTER
# -------------------------------
def is_valid_bug(row):

    resolution = str(row.get("Resolution", "")).lower()

    # ❌ remove useless entries
    invalid_keywords = [
        "duplicate",
        "invalid",
        "won't fix",
        "not a bug",
        "works for me",
        "incomplete"
    ]

    for word in invalid_keywords:
        if word in resolution:
            return False

    return True


# -------------------------------
# TRANSFORM DATA
# -------------------------------
def transform_file(df, source_name):

    results = []

    for _, row in df.iterrows():

        # 🔴 filter invalid bugs
        if not is_valid_bug(row):
            continue

        summary = str(row.get("Summary", "")).strip()
        description = str(row.get("Description", "")).strip()

        # handle nulls
        if description == "nan" or description == "":
            text = summary
        else:
            text = summary + " " + description

        text = clean_text(text)

        if len(text) < 20:
            continue

        # optional features
        priority = str(row.get("Priority", "unknown"))

        results.append({
            "text": text,
            "is_requirement": 1,
            "type": "Functional",  # most bugs = functional
            "source": source_name,
            "priority": priority
        })

    return results


# -------------------------------
# SCAN ALL FILES
# -------------------------------
def process_all():

    final_data = []

    for root, dirs, files in os.walk(BASE_PATH):

        for file in files:

            # ✅ ONLY use *_bugs.csv
            if file.endswith("_bugs.csv"):

                full_path = os.path.join(root, file)

                print(f"Processing: {full_path}")

                df = load_csv_safe(full_path)

                if df is None:
                    continue

                source_name = file.replace("_bugs.csv", "")

                processed = transform_file(df, source_name)

                print(f"   → Extracted: {len(processed)} samples")

                final_data.extend(processed)

    return final_data


# -------------------------------
# SAVE OUTPUT
# -------------------------------
def save_data(data, path):

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print(f"\n✅ Saved ML dataset: {path}")
    print(f"Total samples: {len(data)}")


# -------------------------------
# MAIN
# -------------------------------
if __name__ == "__main__":

    print("🚀 Processing Gitbugs dataset...")

    data = process_all()

    save_data(data, OUTPUT_PATH)

    print("\n🔥 DONE — Gitbugs ready for ML!")
import json
from collections import defaultdict


# -------------------------------
# PATHS
# -------------------------------
INPUT_PATH = r"C:\Users\Shruti\jk\Python\Python_GUI\Project_series\6.BRD_Agent\dataPush\pattern_dataset.json"

OUTPUT_PATH = r"C:\Users\Shruti\jk\Python\Python_GUI\Project_series\6.BRD_Agent\dataPush\clustered_patterns.json"


# -------------------------------
# LOAD DATA (STREAM SAFE)
# -------------------------------
def load_data():

    print("🚀 Loading pattern dataset...")

    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"Total patterns: {len(data)}")

    return data


# -------------------------------
# CLUSTER LOGIC
# -------------------------------
def cluster_patterns(data):

    clusters = defaultdict(lambda: {
        "Functional": [],
        "Non-Functional": []
    })

    count = 0

    for item in data:

        feature = item.get("feature", "general")
        req_type = item.get("type", "Functional")

        # clean feature name
        feature = feature.lower().strip()

        clusters[feature][req_type].append(item["text"])

        count += 1

        if count % 20000 == 0:
            print(f"Processed: {count}")

    return clusters


# -------------------------------
# CLEAN OUTPUT (REMOVE DUPLICATES)
# -------------------------------
def clean_clusters(clusters):

    cleaned = {}

    for feature, types in clusters.items():

        cleaned[feature] = {}

        for t, texts in types.items():

            # remove duplicates
            unique = list(set(texts))

            # limit size (important)
            cleaned[feature][t] = unique[:200]

    return cleaned


# -------------------------------
# SAVE
# -------------------------------
def save_data(data):

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print(f"\n✅ Clustered data saved at: {OUTPUT_PATH}")


# -------------------------------
# MAIN
# -------------------------------
if __name__ == "__main__":

    data = load_data()

    print("\n🔗 Clustering patterns...")
    clusters = cluster_patterns(data)

    print("\n🧹 Cleaning clusters...")
    cleaned = clean_clusters(clusters)

    save_data(cleaned)
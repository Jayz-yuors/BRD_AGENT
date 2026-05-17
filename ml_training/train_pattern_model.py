import json
from ml_training.data_loader import load_all_datasets
from ml_training.pattern_utils import extract_pattern


OUTPUT_PATH = r"C:\Users\Shruti\jk\Python\Python_GUI\Project_series\6.BRD_Agent\dataPush\pattern_dataset.json"


def generate_patterns():

    print("🚀 Loading datasets...")
    data = load_all_datasets()

    print(f"Total samples: {len(data)}")

    patterns = []
    count = 0

    for item in data:

        if item["is_requirement"] != 1:
            continue

        try:
            pattern = extract_pattern(item["text"])

            patterns.append({
                "text": item["text"],
                "entity": pattern["entity"],
                "action": pattern["action"],
                "feature": pattern["feature"],
                "type": item["type"]
            })

            count += 1

            # 🔥 FAST LOGGING
            if count % 20000 == 0:
                print(f"Processed: {count}")

        except:
            continue

    return patterns


def save_data(data):

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f)

    print(f"\n✅ Pattern dataset saved at: {OUTPUT_PATH}")
    print(f"Total patterns: {len(data)}")


if __name__ == "__main__":

    patterns = generate_patterns()
    save_data(patterns)
import json
import random


PURE_PATH = r"C:\Users\Shruti\jk\Python\Python_GUI\Project_series\6.BRD_Agent\dataPush\ml_ready_pure.json"
GITBUGS_PATH = r"C:\Users\Shruti\jk\Python\Python_GUI\Project_series\6.BRD_Agent\dataPush\ml_ready_gitbugs.json"
ENRON_PATH = r"C:\Users\Shruti\jk\Python\Python_GUI\Project_series\6.BRD_Agent\dataPush\ml_ready_enron.json"


def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            print(f"✅ Loaded {len(data)} samples from {path}")
            return data
    except Exception as e:
        print(f"❌ Error loading {path}: {e}")
        return []


def normalize_dataset(data):
    normalized = []

    for item in data:
        text = item.get("text", "").strip()
        req_flag = item.get("is_requirement", 1)
        req_type = item.get("type", "Functional")

        if not text:
            continue

        normalized.append({
            "text": text,
            "is_requirement": int(req_flag),
            "type": req_type
        })

    return normalized


# 🔥 NEW NEGATIVE GENERATION (SMART)
def generate_negative_samples(enron_data, limit=100000):

    negatives = []

    for item in enron_data:

        text = item["text"]

        # remove "System should" to break requirement pattern
        if text.lower().startswith("system should"):
            modified = text.replace("System should", "").strip()
        else:
            modified = text

        # avoid empty
        if len(modified) < 20:
            continue

        negatives.append({
            "text": modified,
            "is_requirement": 0,
            "type": "None"
        })

        if len(negatives) >= limit:
            break

    print(f"❄️ Generated {len(negatives)} negative samples")

    return negatives


def load_all_datasets():

    pure = normalize_dataset(load_json(PURE_PATH))
    gitbugs = normalize_dataset(load_json(GITBUGS_PATH))
    enron = normalize_dataset(load_json(ENRON_PATH))

    print("\n📊 Dataset Summary:")
    print(f"PURE: {len(pure)}")
    print(f"GITBUGS: {len(gitbugs)}")
    print(f"ENRON: {len(enron)}")

    negatives = generate_negative_samples(enron)

    combined = pure + gitbugs + enron + negatives

    print(f"\n🔥 TOTAL COMBINED DATA: {len(combined)}")

    random.shuffle(combined)

    return combined


if __name__ == "__main__":
    data = load_all_datasets()

    print("\nSample:")
    for i in range(5):
        print(data[i])
import os
import joblib
import random

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

from ml_training.data_loader import load_json, normalize_dataset
from ml_training.preprocessing import vectorize


# -------------------------------
# PATHS
# -------------------------------
MODEL_DIR = r"C:\Users\Shruti\jk\Python\Python_GUI\Project_series\6.BRD_Agent\ml_models\requirement_classifier"

MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")
VECTORIZER_PATH = os.path.join(MODEL_DIR, "vectorizer.pkl")

PURE_PATH = r"C:\Users\Shruti\jk\Python\Python_GUI\Project_series\6.BRD_Agent\dataPush\ml_ready_pure.json"
GITBUGS_PATH = r"C:\Users\Shruti\jk\Python\Python_GUI\Project_series\6.BRD_Agent\dataPush\ml_ready_gitbugs.json"
ENRON_PATH = r"C:\Users\Shruti\jk\Python\Python_GUI\Project_series\6.BRD_Agent\dataPush\ml_ready_enron.json"


# -------------------------------
# LOAD + FILTER
# -------------------------------
def load_filtered():

    pure = normalize_dataset(load_json(PURE_PATH))
    gitbugs = normalize_dataset(load_json(GITBUGS_PATH))
    enron = normalize_dataset(load_json(ENRON_PATH))

    # only requirements
    pure = [d for d in pure if d["is_requirement"] == 1]
    gitbugs = [d for d in gitbugs if d["is_requirement"] == 1]
    enron = [d for d in enron if d["is_requirement"] == 1]

    print(f"\nPURE: {len(pure)}")
    print(f"GITBUGS: {len(gitbugs)}")
    print(f"ENRON: {len(enron)}")

    return pure, gitbugs, enron


# -------------------------------
# SMART SAMPLING
# -------------------------------
def sample_data(pure, gitbugs, enron):

    pure_sample = pure

    gitbugs_sample = random.sample(
        gitbugs, min(len(gitbugs), int(len(pure) * 0.5))
    )

    enron_sample = random.sample(
        enron, min(len(enron), int(len(pure) * 0.3))
    )

    combined = pure_sample + gitbugs_sample + enron_sample
    random.shuffle(combined)

    print(f"\nCombined dataset: {len(combined)}")

    return combined


# -------------------------------
# BALANCE FUNCTION
# -------------------------------
def balance_classes(data):

    func = [d for d in data if d["type"] == "Functional"]
    nfr = [d for d in data if d["type"] == "Non-Functional"]

    print(f"Functional: {len(func)}")
    print(f"Non-Functional: {len(nfr)}")

    if len(nfr) == 0:
        raise Exception("❌ No Non-Functional data. Check PURE dataset.")

    min_count = min(len(func), len(nfr))

    func = random.sample(func, min_count)
    nfr = random.sample(nfr, min_count)

    balanced = func + nfr
    random.shuffle(balanced)

    return balanced


# -------------------------------
# CLEAN TEXT (SAFE)
# -------------------------------
def clean_text(text):
    return text.lower().strip()


# -------------------------------
# TRAIN
# -------------------------------
def train():

    print("🚀 Loading datasets...")
    pure, gitbugs, enron = load_filtered()

    print("\n📦 Sampling intelligently...")
    data = sample_data(pure, gitbugs, enron)

    print("\n⚖️ Balancing...")
    data = balance_classes(data)

    print(f"Balanced size: {len(data)}")

    # -------------------------------
    # SAFE PREPROCESSING (FIXED)
    # -------------------------------
    print("\n🧹 Preprocessing (SAFE)...")

    texts = []
    labels = []

    for item in data:

        text = clean_text(item["text"])
        label = item["type"]

        if not text:
            continue

        texts.append(text)

        if label == "Non-Functional":
            labels.append(1)
        else:
            labels.append(0)

    print(f"Samples after cleaning: {len(texts)}")

    # 🔥 DEBUG CHECK
    print("\n📊 Label Distribution:")
    print(f"Functional (0): {labels.count(0)}")
    print(f"Non-Functional (1): {labels.count(1)}")

    if len(set(labels)) < 2:
        raise Exception("❌ Only one class present after preprocessing!")

    # -------------------------------
    # VECTORIZATION
    # -------------------------------
    print("\n🔢 Vectorizing...")
    X, vectorizer = vectorize(texts)

    # -------------------------------
    # SPLIT
    # -------------------------------
    print("\n📊 Splitting...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, labels, test_size=0.2, random_state=42
    )

    # -------------------------------
    # TRAIN
    # -------------------------------
    print("\n🤖 Training...")
    model = LogisticRegression(max_iter=200)
    model.fit(X_train, y_train)

    # -------------------------------
    # EVALUATE
    # -------------------------------
    print("\n📈 Evaluating...")
    y_pred = model.predict(X_test)

    print("\n" + classification_report(y_test, y_pred))

    # -------------------------------
    # SAVE
    # -------------------------------
    print("\n💾 Saving model...")

    os.makedirs(MODEL_DIR, exist_ok=True)

    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)

    print(f"✅ Model saved at: {MODEL_PATH}")
    print(f"✅ Vectorizer saved at: {VECTORIZER_PATH}")


# -------------------------------
# MAIN
# -------------------------------
if __name__ == "__main__":
    train()
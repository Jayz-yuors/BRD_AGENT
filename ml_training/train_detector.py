import os
import joblib
import random
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

from ml_training.data_loader import load_all_datasets
from ml_training.preprocessing import preprocess_dataset, vectorize


MODEL_DIR = r"C:\Users\Shruti\jk\Python\Python_GUI\Project_series\6.BRD_Agent\ml_models\requirement_detector"

MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")
VECTORIZER_PATH = os.path.join(MODEL_DIR, "vectorizer.pkl")

MAX_SAMPLES = 200000


def train():

    print("🚀 Loading data...")
    data = load_all_datasets()

    print(f"\nOriginal dataset size: {len(data)}")

    pos = [d for d in data if d["is_requirement"] == 1]
    neg = [d for d in data if d["is_requirement"] == 0]

    print(f"Positive samples: {len(pos)}")
    print(f"Negative samples: {len(neg)}")

    if len(neg) == 0:
        raise Exception("❌ STILL NO NEGATIVES → check generator")

    min_count = min(len(pos), len(neg))

    pos = random.sample(pos, min_count)
    neg = random.sample(neg, min_count)

    balanced_data = pos + neg
    random.shuffle(balanced_data)

    print(f"\nBalanced dataset size: {len(balanced_data)}")

    if len(balanced_data) > MAX_SAMPLES:
        balanced_data = random.sample(balanced_data, MAX_SAMPLES)
        print(f"Reduced dataset to: {len(balanced_data)}")

    print("\n🧹 Preprocessing...")
    texts, labels = preprocess_dataset(balanced_data)

    print("\n🔢 Vectorizing...")
    X, vectorizer = vectorize(texts)

    print("\n📊 Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, labels, test_size=0.2, random_state=42
    )

    print("\n🤖 Training model...")
    model = LogisticRegression(max_iter=200)
    model.fit(X_train, y_train)

    print("\n📈 Evaluating...")
    y_pred = model.predict(X_test)

    print("\n" + classification_report(y_test, y_pred))

    print("\n💾 Saving model...")

    os.makedirs(MODEL_DIR, exist_ok=True)

    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)

    print(f"✅ Model saved at: {MODEL_PATH}")
    print(f"✅ Vectorizer saved at: {VECTORIZER_PATH}")


if __name__ == "__main__":
    train()
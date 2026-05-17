from ml_training.data_loader import load_all_datasets

def debug():

    data = load_all_datasets()

    pos = [d for d in data if d["is_requirement"] == 1]
    neg = [d for d in data if d["is_requirement"] == 0]

    print("\n🔍 DEBUG RESULT")
    print(f"Total: {len(data)}")
    print(f"Positive: {len(pos)}")
    print(f"Negative: {len(neg)}")

    print("\nSample Negative:")
    for i in range(5):
        print(neg[i]["text"])


if __name__ == "__main__":
    debug()
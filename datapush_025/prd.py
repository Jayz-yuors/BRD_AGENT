import pandas as pd
import json

INPUT_PATH = r"C:\Users\Shruti\jk\Python\Python_GUI\Project_series\6.BRD_Agent\datasets\PURE Requirement Dataset\Pure_Annotate_Dataset.csv"

OUTPUT_PATH = r"C:\Users\Shruti\jk\Python\Python_GUI\Project_series\6.BRD_Agent\dataPush\ml_ready_pure.json"


def load_data(path):
    df = pd.read_csv(path, encoding="latin-1")
    print(f"Loaded {len(df)} rows")
    return df


def transform_data(df):

    results = []

    for _, row in df.iterrows():

        sentence = str(row["sentence"]).strip()

        if not sentence:
            continue

        # 🔹 Label from dataset
        nfr_flag = int(row["NFR_boolean"])

        if nfr_flag == 1:
            req_type = "Non-Functional"
        else:
            req_type = "Functional"

        results.append({
            "text": sentence,
            "is_requirement": 1,
            "type": req_type
        })

    return results


def save_data(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print(f"\n✅ Saved ML dataset: {path}")
    print(f"Total samples: {len(data)}")


if __name__ == "__main__":

    df = load_data(INPUT_PATH)

    processed = transform_data(df)

    save_data(processed, OUTPUT_PATH)
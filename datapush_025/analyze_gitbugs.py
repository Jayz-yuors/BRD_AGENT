import os
import pandas as pd

# -------------------------------
# BASE PATH
# -------------------------------
BASE_PATH = r"C:\Users\Shruti\jk\Python\Python_GUI\Project_series\6.BRD_Agent\datasets\Gitbugs\gitbugs"

OUTPUT_FILE = r"C:\Users\Shruti\jk\Python\Python_GUI\Project_series\6.BRD_Agent\dataPush\gitbugs_analysis.txt"


# -------------------------------
# SAFE CSV LOADER
# -------------------------------
def load_csv_safe(path):
    try:
        return pd.read_csv(path, encoding="latin-1")
    except:
        try:
            return pd.read_csv(path, encoding="cp1252")
        except Exception as e:
            return None


# -------------------------------
# ANALYZE FILE
# -------------------------------
def analyze_file(file_path):

    df = load_csv_safe(file_path)

    if df is None:
        return f"\n❌ Could not read file: {file_path}\n"

    output = []

    output.append(f"\n{'='*80}")
    output.append(f"FILE: {file_path}")
    output.append(f"{'='*80}\n")

    # Basic Info
    output.append(f"Total Rows: {len(df)}")
    output.append(f"Total Columns: {len(df.columns)}\n")

    # Column Info
    output.append("COLUMNS + DATATYPES:\n")
    for col in df.columns:
        output.append(f"  - {col} ({df[col].dtype})")

    # Null Values
    output.append("\nNULL VALUES:\n")
    for col in df.columns:
        null_count = df[col].isnull().sum()
        output.append(f"  - {col}: {null_count}")

    # Sample Data
    output.append("\nSAMPLE ROWS:\n")
    sample = df.head(3)

    for i, row in sample.iterrows():
        output.append(f"\nRow {i}:")
        for col in df.columns:
            val = str(row[col])[:200]  # limit length
            output.append(f"  {col}: {val}")

    # Text Analysis (important columns)
    output.append("\nTEXT ANALYSIS:\n")

    text_columns = []
    for col in df.columns:
        if df[col].dtype == "object":
            text_columns.append(col)

    for col in text_columns:
        output.append(f"\nColumn: {col}")

        sample_texts = df[col].dropna().astype(str).head(5)

        for text in sample_texts:
            output.append(f"  Sample: {text[:150]}")

    # Unique Values (small columns)
    output.append("\nUNIQUE VALUES (small columns only):\n")

    for col in df.columns:
        if df[col].nunique() < 20:
            output.append(f"\nColumn: {col}")
            output.append(str(df[col].unique()))

    return "\n".join(output)


# -------------------------------
# SCAN ALL FILES
# -------------------------------
def scan_all():

    final_output = []

    for root, dirs, files in os.walk(BASE_PATH):

        for file in files:

            if file.endswith(".csv"):

                full_path = os.path.join(root, file)

                print(f"Analyzing: {full_path}")

                analysis = analyze_file(full_path)

                final_output.append(analysis)

    return "\n".join(final_output)


# -------------------------------
# SAVE
# -------------------------------
def save_output(text):

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"\n✅ Analysis saved to: {OUTPUT_FILE}")


# -------------------------------
# MAIN
# -------------------------------
if __name__ == "__main__":

    print("🔍 Scanning Gitbugs dataset...")

    result = scan_all()

    save_output(result)

    print("\n✅ DONE!")
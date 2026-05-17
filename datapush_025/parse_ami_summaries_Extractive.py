import os
import json


def parse_summary_file(file_path):
    """
    Parse one ExtractiveSummary file
    """
    meeting_id = os.path.basename(file_path).split("-")[0]
    results = []

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:

            parts = line.strip().split()

            # skip invalid lines
            if len(parts) < 4:
                continue

            try:
                # last 3 elements are fixed
                start_time = float(parts[-3])
                end_time = float(parts[-2])
                spurt_id = parts[-1]

                sentence = " ".join(parts[:-3]).strip()

                # basic cleaning
                if len(sentence) < 10:
                    continue

                results.append({
                    "meeting_id": meeting_id,
                    "sentence": sentence,
                    "start_time": start_time,
                    "end_time": end_time,
                    "spurt_id": spurt_id
                })

            except:
                continue

    return results


def parse_all_files(input_folder):
    """
    Parse all files inside ExtractiveSummaries folder
    """
    all_data = []

    for file in os.listdir(input_folder):

        if not file.endswith(".txt"):
            continue

        file_path = os.path.join(input_folder, file)

        print(f"Processing: {file}")

        parsed = parse_summary_file(file_path)

        all_data.extend(parsed)

    return all_data


def save_to_json(data, output_file):
    """
    Save structured data to JSON
    """
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print(f"\n✅ JSON saved at: {output_file}")


if __name__ == "__main__":

    input_path = r"C:\Users\Shruti\jk\Python\Python_GUI\Project_series\6.BRD_Agent\datasets\AMI automatic annotations v1.5.1\PlainText-format\ExtractiveSummaries"

    output_path = r"C:\Users\Shruti\jk\Python\Python_GUI\Project_series\6.BRD_Agent\dataPush\ami_summaries_1.json"

    data = parse_all_files(input_path)

    print(f"\nTotal extracted sentences: {len(data)}")

    save_to_json(data, output_path)
import os
import json


def parse_topic_file(file_path):

    meeting_id = os.path.basename(file_path).split(".")[0]
    results = []

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:

            line = line.strip()

            # skip comments or empty lines
            if not line or line.startswith("#"):
                continue

            parts = line.split()

            if len(parts) < 3:
                continue

            try:
                topic_id = int(parts[0])

                time_range = parts[1]   # "78.8_1880.67"
                start, end = time_range.split("_")

                start_time = float(start)
                end_time = float(end)

                text = " ".join(parts[2:]).strip()

                if len(text) < 10:
                    continue

                results.append({
                    "meeting_id": meeting_id,
                    "topic_id": topic_id,
                    "start_time": start_time,
                    "end_time": end_time,
                    "topic_text": text
                })

            except:
                continue

    return results


def parse_all_files(input_folder):

    all_data = []

    for file in os.listdir(input_folder):

        if not file.endswith(".txt"):
            continue

        file_path = os.path.join(input_folder, file)

        print(f"Processing: {file}")

        parsed = parse_topic_file(file_path)

        all_data.extend(parsed)

    return all_data


def save_to_json(data, output_file):

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print(f"\n✅ JSON saved at: {output_file}")


if __name__ == "__main__":

    input_path = r"C:\Users\Shruti\jk\Python\Python_GUI\Project_series\6.BRD_Agent\datasets\AMI automatic annotations v1.5.1\PlainText-format\AutomaticTopicSegmentation"

    output_path = r"C:\Users\Shruti\jk\Python\Python_GUI\Project_series\6.BRD_Agent\dataPush\ami_summaries.json"

    data = parse_all_files(input_path)

    print(f"\nTotal extracted topics: {len(data)}")

    save_to_json(data, output_path)
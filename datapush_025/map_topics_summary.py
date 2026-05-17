import json
from collections import defaultdict


# -------------------------------
# LOAD JSON
# -------------------------------
def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# -------------------------------
# OPTIMIZED MAPPING FUNCTION
# -------------------------------
def map_summaries_to_topics(summaries, topics):

    # 🔹 Step 1: Group topics by meeting_id
    topic_map = defaultdict(list)

    for t in topics:
        topic_map[t["meeting_id"]].append(t)

    # 🔹 Step 2: Sort topics by start_time (VERY IMPORTANT for efficiency)
    for meeting_id in topic_map:
        topic_map[meeting_id].sort(key=lambda x: x["start_time"])

    final_data = defaultdict(list)

    # 🔹 Step 3: Mapping using overlap logic
    for s in summaries:

        meeting_id = s["meeting_id"]

        if meeting_id not in topic_map:
            continue

        s_start = s["start_time"]
        s_end = s["end_time"]

        topics_list = topic_map[meeting_id]

        # Efficient linear scan (sorted list)
        for t in topics_list:

            t_start = t["start_time"]
            t_end = t["end_time"]

            # 🚀 Overlap logic (BEST)
            if not (s_end < t_start or s_start > t_end):

                final_data[meeting_id].append({
                    "topic_text": t["topic_text"],
                    "summary": s["sentence"],
                    "start_time": s_start,
                    "end_time": s_end
                })

                break

            # ⚡ Optimization: stop early if topics exceed summary
            if t_start > s_end:
                break

    return final_data


# -------------------------------
# SAVE JSON
# -------------------------------
def save_json(data, output_path):

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print(f"\n✅ Final mapped data saved: {output_path}")


# -------------------------------
# MAIN
# -------------------------------
if __name__ == "__main__":

    topics_path = r"C:\Users\Shruti\jk\Python\Python_GUI\Project_series\6.BRD_Agent\dataPush\ami_summaries.json"

    summaries_path = r"C:\Users\Shruti\jk\Python\Python_GUI\Project_series\6.BRD_Agent\dataPush\ami_summaries_1.json"

    output_path = r"C:\Users\Shruti\jk\Python\Python_GUI\Project_series\6.BRD_Agent\dataPush\structured_meetings_1.json"

    print("Loading data...")

    topics = load_json(topics_path)
    summaries = load_json(summaries_path)

    print(f"Topics loaded: {len(topics)}")
    print(f"Summaries loaded: {len(summaries)}")

    print("\nMapping summaries to topics...")

    final_data = map_summaries_to_topics(summaries, topics)

    print(f"\nMeetings processed: {len(final_data)}")

    save_json(final_data, output_path)
import json
import requests
import time

# 🔹 CONFIG (Optimized for 8GB RAM)
USE_AI = True
MAX_AI_CALLS = 100        # 🔥 SAFE LIMIT
DELAY_BETWEEN_CALLS = 0.2

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "phi"   # ✅ confirmed working


# -------------------------------
# LOAD DATA
# -------------------------------
def load_data(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# -------------------------------
# FILTER (IMPROVED)
# -------------------------------
def is_requirement_candidate(sentence):

    keywords = [
        "need", "should", "must", "require",
        "allow", "enable", "provide", "support",
        "feature", "system", "user"
    ]

    sentence = sentence.lower()

    return any(word in sentence for word in keywords) and len(sentence) > 20


# -------------------------------
# CLASSIFICATION
# -------------------------------
def classify_requirement(sentence):

    sentence = sentence.lower()

    nfr_keywords = [
        "fast", "secure", "performance",
        "scalable", "efficient", "reliable",
        "latency", "response time"
    ]

    if any(word in sentence for word in nfr_keywords):
        return "Non-Functional Requirement"

    return "Functional Requirement"


# -------------------------------
# OLLAMA CALL (ROBUST)
# -------------------------------
def rewrite_with_ollama(sentence):

    prompt = f"""
Convert the following sentence into a professional software requirement.

Rules:
- Start with "System should"
- Keep it short
- Do not explain

Sentence:
{sentence}
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            },
            timeout=5   # 🔥 shorter timeout
        )

        if response.status_code == 200:
            return response.json().get("response", "").strip()

    except Exception as e:
        print(f"⚠️ Ollama error: {e}")

    return None


# -------------------------------
# FALLBACK
# -------------------------------
def basic_rewrite(sentence):
    return f"System should {sentence.strip().lower()}"


# -------------------------------
# MAIN EXTRACTION (OPTIMIZED)
# -------------------------------
def extract_requirements(data):

    results = []
    ai_calls = 0
    total_processed = 0

    for meeting_id, entries in data.items():

        for item in entries:

            total_processed += 1

            # 🔥 Progress logging (VERY IMPORTANT)
            if total_processed % 500 == 0:
                print(f"Processed {total_processed} sentences | AI used: {ai_calls}")

            sentence = item["summary"]

            # 🔹 Step 1: Filter
            if not is_requirement_candidate(sentence):
                continue

            # 🔹 Step 2: Classify
            req_type = classify_requirement(sentence)

            # 🔹 Step 3: Rewrite
            if USE_AI and ai_calls < MAX_AI_CALLS:

                rewritten = rewrite_with_ollama(sentence)

                if rewritten:
                    ai_calls += 1
                    print(f"🤖 AI rewrite #{ai_calls}")
                    time.sleep(DELAY_BETWEEN_CALLS)
                else:
                    rewritten = basic_rewrite(sentence)

            else:
                rewritten = basic_rewrite(sentence)

            results.append({
                "meeting_id": meeting_id,
                "type": req_type,
                "requirement": rewritten,
                "topic": item["topic_text"]
            })

    print(f"\n✅ AI calls used: {ai_calls}")
    print(f"✅ Total processed: {total_processed}")

    return results


# -------------------------------
# SAVE OUTPUT
# -------------------------------
def save_output(data, path):

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print(f"\n✅ Requirements saved: {path}")


# -------------------------------
# MAIN
# -------------------------------
if __name__ == "__main__":

    input_path = r"C:\Users\Shruti\jk\Python\Python_GUI\Project_series\6.BRD_Agent\dataPush\structured_meetings.json"

    output_path = r"C:\Users\Shruti\jk\Python\Python_GUI\Project_series\6.BRD_Agent\dataPush\final_requirements.json"

    print("Loading structured data...")

    data = load_data(input_path)

    print("Extracting requirements (optimized for 8GB RAM)...")

    results = extract_requirements(data)

    print(f"\nTotal requirements extracted: {len(results)}")

    save_output(results, output_path)
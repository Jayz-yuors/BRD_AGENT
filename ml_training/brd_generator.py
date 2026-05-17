import json
import requests

from ml_inference.predict import is_requirement, classify_requirement
from ml_training.utils import clean_text

# -------------------------------
# CONFIG
# -------------------------------
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "phi3"

CLUSTER_PATH = r"C:\Users\Shruti\jk\Python\Python_GUI\Project_series\6.BRD_Agent\dataPush\clustered_patterns.json"


# -------------------------------
# LOAD CLUSTERS
# -------------------------------
def load_clusters():
    with open(CLUSTER_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


# -------------------------------
# KEYWORD MAPPING (SMART)
# -------------------------------
KEYWORD_MAP = {
    "login": "authentication",
    "signup": "authentication",
    "auth": "authentication",
    "payment": "payment",
    "dashboard": "dashboard",
    "report": "dashboard",
    "user": "user_management"
}


# -------------------------------
# MATCH MODULES
# -------------------------------
def match_modules(user_input, clusters):

    user_input = user_input.lower()
    selected = {}

    for key, mapped in KEYWORD_MAP.items():
        if key in user_input and mapped in clusters:
            selected[mapped] = clusters[mapped]

    return selected


# -------------------------------
# STRICT FILTER (CRITICAL)
# -------------------------------
def is_valid_requirement(text):

    text = text.lower()

    # remove very short
    if len(text.split()) < 5:
        return False

    # remove very long (garbage dumps)
    if len(text.split()) > 25:
        return False

    # remove bug / logs / noise
    if any(x in text for x in [
        "crash", "bug", "stacktrace", "exception",
        "steps to reproduce", "published", "news",
        "http", "www", "mozilla", "firefox"
    ]):
        return False

    return True


# -------------------------------
# PROCESS REQUIREMENTS
# -------------------------------
def process_requirements(req_list):

    processed = []

    for r in req_list:

        text = clean_text(r)

        if not is_valid_requirement(text):
            continue

        if not is_requirement(text):
            continue

        # fix duplication
        if text.startswith("system should"):
            final = text
        else:
            final = "system should " + text

        processed.append(final)

    return processed


# -------------------------------
# BUILD BRD
# -------------------------------
def build_brd(modules):

    brd = "BUSINESS REQUIREMENT DOCUMENT\n\n"

    for feature, types in modules.items():

        brd += f"{feature.upper()} MODULE\n"

        func_raw = process_requirements(types["Functional"])
        nfr_raw = process_requirements(types["Non-Functional"])

        # classify again (extra safety)
        func_final = []
        nfr_final = []

        for r in func_raw:
            if classify_requirement(r) == "Functional":
                func_final.append(r)

        for r in nfr_raw:
            if classify_requirement(r) == "Non-Functional":
                nfr_final.append(r)

        # Functional
        brd += "\nFunctional Requirements:\n"
        for req in func_final[:5]:
            brd += f"- {req.capitalize()}\n"

        # Non-functional
        brd += "\nNon-Functional Requirements:\n"
        for req in nfr_final[:3]:
            brd += f"- {req.capitalize()}\n"

        brd += "\n----------------------\n\n"

    return brd


# -------------------------------
# OLLAMA FORMATTER
# -------------------------------
def refine_with_ai(brd_text):

    prompt = f"""
Convert into a professional BRD:

- Add headings
- Improve grammar
- Make concise
- Remove redundancy

Content:
{brd_text}
"""

    try:
        res = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            },
            timeout=25
        )

        if res.status_code == 200:
            return res.json()["response"]

    except:
        pass

    return brd_text


# -------------------------------
# MAIN
# -------------------------------
if __name__ == "__main__":

    clusters = load_clusters()

    print("🚀 BRD Generator (Production Ready)\n")

    while True:

        user_input = input("\nEnter system idea (or 'exit'): ")

        if user_input.lower() == "exit":
            break

        modules = match_modules(user_input, clusters)

        if not modules:
            print("❌ No modules matched")
            continue

        print("\n🧠 Generating BRD...\n")

        raw_brd = build_brd(modules)

        final_brd = refine_with_ai(raw_brd)

        print("\n📄 FINAL BRD:\n")
        print(final_brd)
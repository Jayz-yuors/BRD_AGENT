import re
import json


# -------------------------------
# LOAD FEATURE DICTIONARY
# -------------------------------
FEATURE_PATH = r"C:\Users\Shruti\jk\Python\Python_GUI\Project_series\6.BRD_Agent\dataPush\feature_keywords.json"

try:
    with open(FEATURE_PATH, "r", encoding="utf-8") as f:
        FEATURE_MAP = json.load(f)
except:
    FEATURE_MAP = {}


# -------------------------------
# ENTITY EXTRACTION (FAST RULE)
# -------------------------------
def extract_entity(sentence):

    s = sentence.lower()

    if "user" in s:
        return "user"

    if "admin" in s:
        return "admin"

    if "system" in s:
        return "system"

    return "system"


# -------------------------------
# ACTION EXTRACTION (SMART REGEX)
# -------------------------------
def extract_action(sentence):

    s = sentence.lower()

    # try "should <verb>"
    match = re.search(r"should\s+(\w+)", s)
    if match:
        return match.group(1)

    # fallback verbs
    for word in s.split():
        if word.endswith("ing") or word.endswith("ed"):
            return word

    return "unknown"


# -------------------------------
# FEATURE DETECTION (HYBRID)
# -------------------------------
def detect_feature(text):

    text = text.lower()

    # -------------------------------
    # 1. STRONG RULES (HIGH PRIORITY)
    # -------------------------------
    if any(k in text for k in ["login", "otp", "password", "signin"]):
        return "authentication"

    if any(k in text for k in ["payment", "transaction", "refund"]):
        return "payment"

    if any(k in text for k in ["dashboard", "report", "analytics"]):
        return "dashboard"

    if any(k in text for k in ["email", "sms", "notify", "alert"]):
        return "notification"

    if any(k in text for k in ["secure", "encrypt", "authorization"]):
        return "security"

    # -------------------------------
    # 2. DATA-DRIVEN MATCH (YOUR DICT)
    # -------------------------------
    for feature, keywords in FEATURE_MAP.items():

        for word in keywords:
            if word in text:
                return feature.lower()

    return "general"


# -------------------------------
# MAIN PATTERN EXTRACTOR
# -------------------------------
def extract_pattern(sentence):

    return {
        "text": sentence,
        "entity": extract_entity(sentence),
        "action": extract_action(sentence),
        "feature": detect_feature(sentence)
    }
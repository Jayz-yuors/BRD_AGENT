import re
import time
import requests
from db_config import create_connection

# -------------------------------
# CONFIG
# -------------------------------
BATCH_SIZE = 500   # 🔥 reduced for faster response
USE_AI = False
MAX_AI_CALLS = 100
DELAY = 0.2

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "phi"


# -------------------------------
# CLEAN EMAIL
# -------------------------------
def clean_email(text):

    if not text:
        return ""

    text = re.sub(r"-----Original Message-----.*", "", text, flags=re.DOTALL)
    text = re.sub(r"From:.*", "", text)
    text = re.sub(r"Sent:.*", "", text)
    text = re.sub(r"To:.*", "", text)

    text = re.sub(r"Regards,.*", "", text, flags=re.DOTALL)
    text = re.sub(r"Thanks,.*", "", text, flags=re.DOTALL)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# -------------------------------
# SPLIT
# -------------------------------
def split_sentences(text):
    return re.split(r"[.!?]", text)


# -------------------------------
# FILTER
# -------------------------------
def is_requirement(s):

    keywords = [
        "need", "should", "must", "require",
        "allow", "enable", "provide", "support"
    ]

    s = s.lower()

    return any(k in s for k in keywords) and len(s) > 15


# -------------------------------
# CLASSIFY
# -------------------------------
def classify(s):

    nfr = ["fast", "secure", "performance", "scalable"]

    s = s.lower()

    if any(x in s for x in nfr):
        return "Non-Functional"

    return "Functional"


# -------------------------------
# AI REWRITE
# -------------------------------
def rewrite_ai(sentence):

    prompt = f"Convert into requirement starting with 'System should': {sentence}"

    try:
        res = requests.post(
            OLLAMA_URL,
            json={"model": MODEL_NAME, "prompt": prompt, "stream": False},
            timeout=8
        )

        if res.status_code == 200:
            return res.json()["response"].strip()

    except Exception as e:
        print(f"⚠️ Ollama error: {e}")

    return None


# -------------------------------
# FALLBACK
# -------------------------------
def basic_rewrite(s):
    return "System should " + s.lower().strip()


# -------------------------------
# CREATE TABLES
# -------------------------------
def setup_db(conn):

    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS extracted_requirements (
        id SERIAL PRIMARY KEY,
        email_id INT,
        requirement TEXT,
        type TEXT,
        source TEXT
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS processing_tracker (
        id SERIAL PRIMARY KEY,
        last_email_id INT
    );
    """)

    cur.execute("SELECT COUNT(*) FROM processing_tracker")
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO processing_tracker (last_email_id) VALUES (0)")

    # 🔥 INDEX (VERY IMPORTANT)
    cur.execute("""
    CREATE INDEX IF NOT EXISTS idx_email_id ON enron_emails(id);
    """)

    conn.commit()
    cur.close()


# -------------------------------
# GET LAST ID
# -------------------------------
def get_last_id(conn):

    cur = conn.cursor()
    cur.execute("SELECT last_email_id FROM processing_tracker LIMIT 1")
    last_id = cur.fetchone()[0]
    cur.close()

    return last_id


# -------------------------------
# UPDATE TRACKER
# -------------------------------
def update_last_id(conn, last_id):

    cur = conn.cursor()
    cur.execute("UPDATE processing_tracker SET last_email_id = %s", (last_id,))
    conn.commit()
    cur.close()


# -------------------------------
# MAIN PIPELINE
# -------------------------------
def process_emails():

    conn = create_connection()
    setup_db(conn)

    cur = conn.cursor()

    last_id = get_last_id(conn)

    print(f"🚀 Starting from email ID: {last_id}")

    ai_calls = 0
    total = 0
    batch_num = 0

    while True:

        print(f"\n🔄 Fetching batch after ID {last_id}...")

        cur.execute("""
        SELECT id, body
        FROM enron_emails
        WHERE id > %s
        ORDER BY id
        LIMIT %s
        """, (last_id, BATCH_SIZE))

        rows = cur.fetchall()

        print(f"✅ Fetched {len(rows)} rows")

        if not rows:
            print("\n✅ ALL EMAILS PROCESSED")
            break

        insert_data = []

        for email_id, body in rows:

            if email_id % 100 == 0:
                print(f"➡ Processing email ID: {email_id}")

            cleaned = clean_email(body)
            sentences = split_sentences(cleaned)

            for s in sentences:

                s = s.strip()
                total += 1

                if not s or not is_requirement(s):
                    continue

                req_type = classify(s)

                if USE_AI and ai_calls < MAX_AI_CALLS:
                    rewritten = rewrite_ai(s)

                    if rewritten:
                        ai_calls += 1
                        time.sleep(DELAY)
                        print(f"🤖 AI rewrite #{ai_calls}")
                    else:
                        rewritten = basic_rewrite(s)
                else:
                    rewritten = basic_rewrite(s)

                insert_data.append((
                    email_id,
                    rewritten,
                    req_type,
                    "email"
                ))

            last_id = email_id

        # 🔥 BULK INSERT
        if insert_data:
            cur.executemany("""
            INSERT INTO extracted_requirements (email_id, requirement, type, source)
            VALUES (%s, %s, %s, %s)
            """, insert_data)

        conn.commit()
        update_last_id(conn, last_id)

        batch_num += 1

        print(f"\n📦 Batch {batch_num} DONE")
        print(f"➡ Last ID: {last_id}")
        print(f"➡ Total processed: {total}")
        print(f"➡ AI used: {ai_calls}")
        print(f"➡ Inserted in this batch: {len(insert_data)}")

    cur.close()
    conn.close()

    print("\n🔥 FINAL DONE")
    print(f"Total sentences processed: {total}")
    print(f"AI calls used: {ai_calls}")


# -------------------------------
# RUN
# -------------------------------
if __name__ == "__main__":
    process_emails()
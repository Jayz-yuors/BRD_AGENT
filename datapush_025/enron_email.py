import pandas as pd
import re
from dateutil import parser
from psycopg2.extras import execute_batch

from db_config import create_connection


# ---------------------------
# Extract fields from email
# ---------------------------
def extract_fields(email_text):

    msg_id = re.search(r"Message-ID:\s*(.*)", email_text)
    date = re.search(r"Date:\s*(.*)", email_text)
    sender = re.search(r"From:\s*(.*)", email_text)
    receiver = re.search(r"To:\s*(.*)", email_text)
    subject = re.search(r"Subject:\s*(.*)", email_text)

    # Extract body
    body_split = email_text.split("\n\n", 1)
    body = body_split[1] if len(body_split) > 1 else ""

    # Parse date safely
    parsed_date = None
    if date:
        try:
            parsed_date = parser.parse(date.group(1))
        except Exception:
            parsed_date = None

    return (
        msg_id.group(1) if msg_id else None,
        parsed_date,
        sender.group(1) if sender else None,
        receiver.group(1) if receiver else None,
        subject.group(1) if subject else None,
        body
    )


# ---------------------------
# Push data to PostgreSQL
# ---------------------------
def push_enron_data(csv_path):

    print("Loading dataset...")

    df = pd.read_csv(csv_path)

    conn = create_connection()
    cur = conn.cursor()

    batch = []

    print("Processing emails...")

    for _, row in df.iterrows():

        msg_id, date, sender, receiver, subject, body = extract_fields(row["message"])

        batch.append((msg_id, date, sender, receiver, subject, body))

        # Insert in batches of 1000
        if len(batch) == 1000:
            execute_batch(cur, """
                INSERT INTO enron_emails
                (message_id,email_date,sender,receiver,subject,body)
                VALUES (%s,%s,%s,%s,%s,%s)
            """, batch)

            batch.clear()

    # Insert remaining rows
    if batch:
        execute_batch(cur, """
            INSERT INTO enron_emails
            (message_id,email_date,sender,receiver,subject,body)
            VALUES (%s,%s,%s,%s,%s,%s)
        """, batch)

    conn.commit()

    cur.close()
    conn.close()

    print("Data successfully inserted into PostgreSQL.")


# ---------------------------
# Main
# ---------------------------
if __name__ == "__main__":

    push_enron_data(
        r"C:\Users\Shruti\jk\Python\Python_GUI\Project_series\6.BRD_Agent\datasets\Enron Email Dataset\emails.csv"
    )
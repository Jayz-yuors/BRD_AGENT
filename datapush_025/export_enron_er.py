import json
from db_config import create_connection

OUTPUT_PATH = r"C:\Users\Shruti\jk\Python\Python_GUI\Project_series\6.BRD_Agent\dataPush\ml_ready_enron.json"


def export_data():

    conn = create_connection()
    cur = conn.cursor()

    print("🚀 Fetching data from DB...")

    cur.execute("""
    SELECT requirement, type
    FROM extracted_requirements
    """)

    rows = cur.fetchall()

    print(f"Total rows fetched: {len(rows)}")

    data = []

    for req, typ in rows:

        data.append({
            "text": req,
            "is_requirement": 1,
            "type": typ
        })

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print(f"\n✅ Exported ML dataset: {OUTPUT_PATH}")
    print(f"Total samples: {len(data)}")

    cur.close()
    conn.close()


if __name__ == "__main__":
    export_data()
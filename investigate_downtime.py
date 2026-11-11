
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "data" / "mes.db"


def investigate_line(line_id):

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                d.event_id,
                d.line_id,
                d.start_time,
                d.end_time,
                d.duration_seconds,
                a.alarm_code,
                a.severity,
                a.description AS alarm_description,
                a.alarm_time,
                p.lot_id,
                p.status AS lot_status

            FROM downtime_events d

            LEFT JOIN equipment_alarms a
                ON d.event_id = a.event_id

            LEFT JOIN production_lots p
                ON d.event_id = p.affected_event_id

            WHERE d.line_id = ?

            ORDER BY d.event_id DESC

            LIMIT 10
        """, (line_id,))

        rows = cursor.fetchall()

        return [dict(row) for row in rows]

    finally:
        conn.close()


if __name__ == "__main__":

    line_id = input("Enter production line ID: ").strip().upper()

    results = investigate_line(line_id)

    for event in results:
        print(event)

    if not results:
        print("No downtime events found.")

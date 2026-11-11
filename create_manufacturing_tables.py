
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "data" / "mes.db"


def create_tables():

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    # Table 1: Equipment alarms
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS equipment_alarms (
            alarm_id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER NOT NULL,
            line_id TEXT NOT NULL,
            alarm_code TEXT NOT NULL,
            severity TEXT NOT NULL,
            description TEXT,
            alarm_time TEXT NOT NULL,

            FOREIGN KEY (event_id)
                REFERENCES downtime_events(event_id),

            FOREIGN KEY (line_id)
                REFERENCES production_lines(line_id)
        )
    """)

    # Table 2: Production lots
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS production_lots (
            lot_id TEXT PRIMARY KEY,
            line_id TEXT NOT NULL,
            status TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT,
            affected_event_id INTEGER,

            FOREIGN KEY (line_id)
                REFERENCES production_lines(line_id),

            FOREIGN KEY (affected_event_id)
                REFERENCES downtime_events(event_id)
        )
    """)

    # Indexes for faster incident lookups
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_alarms_event
        ON equipment_alarms(event_id)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_lots_affected_event
        ON production_lots(affected_event_id)
    """)

    conn.commit()
    conn.close()

    print("Manufacturing tables created successfully!")


if __name__ == "__main__":
    create_tables()

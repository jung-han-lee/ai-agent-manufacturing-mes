
import sqlite3
from pathlib import Path
from datetime import datetime, timezone

DB_PATH = Path(__file__).resolve().parent / "data" / "mes.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create a table for production lines
cursor.execute("""
CREATE TABLE IF NOT EXISTS production_lines (
    line_id TEXT PRIMARY KEY,
    status TEXT NOT NULL,
    last_updated TEXT NOT NULL
)
""")

# Create a table for downtime history
cursor.execute("""
CREATE TABLE IF NOT EXISTS downtime_events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    line_id TEXT NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT,
    duration_seconds REAL,
    FOREIGN KEY (line_id) REFERENCES production_lines(line_id)
)
""")

# Generate 35 production lines
timestamp = datetime.now(timezone.utc).isoformat()

lines = [
    (f"LINE-{i:02d}", "RUNNING", timestamp)
    for i in range(1, 36)
]

# Insert lines without overwriting existing records
cursor.executemany("""
INSERT OR IGNORE INTO production_lines
(line_id, status, last_updated)
VALUES (?, ?, ?)
""", lines)

conn.commit()
conn.close()

print("35 production lines initialized successfully!")

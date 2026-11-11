
import sqlite3
from pathlib import Path
from datetime import datetime, timezone

DB_PATH = Path("data/mes.db")

# Connect to MES database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create synthetic equipment data
timestamp = datetime.now(timezone.utc).isoformat()

equipment_data = [
    ("ETCH-01", "ETCH", "Plasma Etcher", "DOWN", timestamp),
    ("ETCH-02", "ETCH", "Plasma Etcher", "RUNNING", timestamp),
    ("CVD-01", "CVD", "Deposition", "RUNNING", timestamp),
    ("PHOTO-01", "PHOTO", "Lithography", "IDLE", timestamp),
    ("CMP-01", "CMP", "Polishing", "MAINTENANCE", timestamp)
]

# Insert equipment records
cursor.executemany("""
INSERT OR REPLACE INTO equipment
(equipment_id, area, equipment_type, status, last_updated)
VALUES (?, ?, ?, ?, ?)
""", equipment_data)

conn.commit()
conn.close()

print("Equipment data inserted successfully!")

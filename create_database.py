
import sqlite3
from pathlib import Path

# Define the database location
DB_PATH = Path("data/mes.db")

# Connect to SQLite database
conn = sqlite3.connect(DB_PATH)

# Create a cursor for executing SQL
cursor = conn.cursor()

# Create equipment table
cursor.execute("""
CREATE TABLE IF NOT EXISTS equipment (
    equipment_id TEXT PRIMARY KEY,
    area TEXT NOT NULL,
    equipment_type TEXT NOT NULL,
    status TEXT NOT NULL,
    last_updated TEXT NOT NULL
)
""")

# Save changes
conn.commit()

# Close database connection
conn.close()

print("MES database created successfully!")

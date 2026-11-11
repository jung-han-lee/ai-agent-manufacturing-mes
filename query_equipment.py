
import sqlite3

def get_equipment_by_status(status):
    conn = sqlite3.connect("data/mes.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT equipment_id, area, equipment_type, status
        FROM equipment
        WHERE status = ?
    """, (status,))

    rows = cursor.fetchall()
    conn.close()

    return rows


# Test our function
down_equipment = get_equipment_by_status("DOWN")

for equipment in down_equipment:
    print(equipment)



import sqlite3
import random
import time
from pathlib import Path
from datetime import datetime, timezone

DB_PATH = Path(__file__).resolve().parent / "data" / "mes.db"

DOWN_PROBABILITY = 0.02
RECOVERY_PROBABILITY = 0.10
INTERVAL_SECONDS = 5

# Synthetic equipment alarms
ALARM_TYPES = [
    ("TEMP_HIGH", "HIGH", "Equipment temperature above threshold"),
    ("SENSOR_FAULT", "MEDIUM", "Abnormal sensor signal"),
    ("PRESSURE_LOW", "HIGH", "Process pressure below threshold"),
    ("MOTOR_ERROR", "CRITICAL", "Motor malfunction detected"),
    ("COMM_ERROR", "MEDIUM", "Equipment communication failure")
]


def current_time():
    return datetime.now(timezone.utc).isoformat()


def create_lot(cursor, line_id, timestamp):
    # Generate a unique lot ID
    lot_id = (
        f"LOT-{line_id}-"
        f"{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')}"
    )

    cursor.execute("""
        INSERT INTO production_lots
        (lot_id, line_id, status, start_time)
        VALUES (?, ?, 'PROCESSING', ?)
    """, (lot_id, line_id, timestamp))

    return lot_id


def initialize_lots():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")

    try:
        with conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT line_id, status
                FROM production_lines
            """)

            for line_id, status in cursor.fetchall():
                # Only initialize lots on running lines
                if status != "RUNNING":
                    continue

                cursor.execute("""
                    SELECT lot_id
                    FROM production_lots
                    WHERE line_id = ?
                      AND status = 'PROCESSING'
                    LIMIT 1
                """, (line_id,))

                if cursor.fetchone() is None:
                    create_lot(cursor, line_id, current_time())
    finally:
        conn.close()

    print("Production lots initialized!")


def simulate_cycle():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")

    try:
        with conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT line_id, status
                FROM production_lines
            """)

            lines = cursor.fetchall()

            for line_id, status in lines:

                # RUNNING -> DOWN
                if (
                    status == "RUNNING"
                    and random.random() < DOWN_PROBABILITY
                ):
                    timestamp = current_time()

                    cursor.execute("""
                        UPDATE production_lines
                        SET status = 'DOWN',
                            last_updated = ?
                        WHERE line_id = ?
                    """, (timestamp, line_id))

                    # Create downtime event
                    cursor.execute("""
                        INSERT INTO downtime_events
                        (line_id, start_time)
                        VALUES (?, ?)
                    """, (line_id, timestamp))

                    event_id = cursor.lastrowid

                    # Generate an alarm linked to the event
                    alarm_code, severity, description = random.choice(
                        ALARM_TYPES
                    )

                    cursor.execute("""
                        INSERT INTO equipment_alarms
                        (event_id, line_id, alarm_code,
                         severity, description, alarm_time)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        event_id, line_id, alarm_code,
                        severity, description, timestamp
                    ))

                    # Mark the processing lot as affected
                    cursor.execute("""
                        UPDATE production_lots
                        SET status = 'HOLD',
                            affected_event_id = ?
                        WHERE line_id = ?
                          AND status = 'PROCESSING'
                    """, (event_id, line_id))

                    print(
                        f"[DOWN] {line_id} | "
                        f"Event: {event_id} | "
                        f"Alarm: {alarm_code}"
                    )

                # DOWN -> RUNNING
                elif (
                    status == "DOWN"
                    and random.random() < RECOVERY_PROBABILITY
                ):
                    timestamp = current_time()

                    cursor.execute("""
                        SELECT event_id, start_time
                        FROM downtime_events
                        WHERE line_id = ?
                          AND end_time IS NULL
                        ORDER BY event_id DESC
                        LIMIT 1
                    """, (line_id,))

                    event = cursor.fetchone()

                    if event:
                        event_id, start_time = event

                        duration = (
                            datetime.fromisoformat(timestamp)
                            - datetime.fromisoformat(start_time)
                        ).total_seconds()

                        cursor.execute("""
                            UPDATE downtime_events
                            SET end_time = ?,
                                duration_seconds = ?
                            WHERE event_id = ?
                        """, (timestamp, duration, event_id))

                        # Keep affected lots on HOLD for review
                        cursor.execute("""
                            UPDATE production_lots
                            SET end_time = ?
                            WHERE affected_event_id = ?
                              AND status = 'HOLD'
                              AND end_time IS NULL
                        """, (timestamp, event_id))

                    cursor.execute("""
                        UPDATE production_lines
                        SET status = 'RUNNING',
                            last_updated = ?
                        WHERE line_id = ?
                    """, (timestamp, line_id))

                    # Start a new simulated lot
                    create_lot(cursor, line_id, timestamp)

                    print(f"[RECOVERED] {line_id}")

    finally:
        conn.close()


if __name__ == "__main__":
    print("Starting enhanced manufacturing simulator...")

    initialize_lots()

    try:
        while True:
            simulate_cycle()
            time.sleep(INTERVAL_SECONDS)

    except KeyboardInterrupt:
        print("\nSimulator stopped.")

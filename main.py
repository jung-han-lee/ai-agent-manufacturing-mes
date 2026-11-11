
from investigate_downtime import investigate_line
import sqlite3
from pathlib import Path
from fastapi import FastAPI

app = FastAPI(title="MES-AI Agent API")

DB_PATH = Path(__file__).resolve().parent / "data" / "mes.db"


@app.get("/")
def home():
    return {"message": "MES API is running"}


@app.get("/equipment")
def get_equipment(status: str | None = None):

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if status:
        cursor.execute(
            "SELECT * FROM equipment WHERE status = ?",
            (status.upper(),)
        )
    else:
        cursor.execute("SELECT * FROM equipment")

    rows = cursor.fetchall()
    conn.close()

    return {
        "count": len(rows),
        "equipment": [dict(row) for row in rows]
    }


@app.get("/lines")
def get_production_lines(status: str | None = None):

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if status:
        cursor.execute("""
            SELECT *
            FROM production_lines
            WHERE status = ?
            ORDER BY line_id
        """, (status.upper(),))
    else:
        cursor.execute("""
            SELECT *
            FROM production_lines
            ORDER BY line_id
        """)

    rows = cursor.fetchall()
    conn.close()

    return {
        "count": len(rows),
        "lines": [dict(row) for row in rows]
    }


@app.get("/downtime")
def get_downtime(limit: int = 20):

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM downtime_events
        ORDER BY event_id DESC
        LIMIT ?
    """, (max(1, min(limit, 100)),))

    rows = cursor.fetchall()
    conn.close()

    return {
        "count": len(rows),
        "events": [dict(row) for row in rows]
    }

from datetime import datetime, timezone


@app.get("/downtime/active")
def get_active_downtime():

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            p.line_id,
            p.status,
            d.start_time
        FROM production_lines p
        JOIN downtime_events d
            ON p.line_id = d.line_id
        WHERE p.status = 'DOWN'
          AND d.end_time IS NULL
        ORDER BY d.start_time
    """)

    rows = cursor.fetchall()
    conn.close()

    now = datetime.now(timezone.utc)

    active_lines = []

    for row in rows:
        start = datetime.fromisoformat(row["start_time"])
        duration = (now - start).total_seconds()

        active_lines.append({
            "line_id": row["line_id"],
            "status": row["status"],
            "start_time": row["start_time"],
            "duration_seconds": round(duration, 2),
            "duration_minutes": round(duration / 60, 2)
        })

    return {
        "count": len(active_lines),
        "active_downtime": active_lines
    }

@app.get("/downtime/summary")
def get_downtime_summary():

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            line_id,
            COUNT(*) AS downtime_count,
            ROUND(
                SUM(
                    COALESCE(duration_seconds, 0)
                ) / 60.0,
                2
            ) AS total_downtime_minutes,
            ROUND(
                AVG(duration_seconds) / 60.0,
                2
            ) AS avg_downtime_minutes
        FROM downtime_events
        GROUP BY line_id
        ORDER BY total_downtime_minutes DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return {
        "count": len(rows),
        "summary": [dict(row) for row in rows]
    }

@app.get("/investigate/{line_id}")
def investigate_production_line(line_id: str):

    line_id = line_id.strip().upper()

    events = investigate_line(line_id)

    return {
        "line_id": line_id,
        "event_count": len(set(
            event["event_id"] for event in events
        )),
        "events": events
    }

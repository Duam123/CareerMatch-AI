
import sqlite3
import json
from pathlib import Path

DB_PATH = Path(__file__).parent / "careermatch.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                resume_name TEXT NOT NULL,
                jobs_json TEXT NOT NULL
            )
        """)


def save_analysis(resume_name, job_title, report):
    init_db()

    job = {
        "title": job_title,
        "match_score": float(report.get("score", 0)),
        "matched_skills": report.get("matched_skills", []),
        "missing_skills": report.get("missing_skills", []),
    }

    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO analyses
                (created_at, resume_name, jobs_json)
            VALUES (datetime('now', 'localtime'), ?, ?)
            """,
            (resume_name, json.dumps([job], ensure_ascii=False)),
        )


def get_history(limit=10):
    init_db()

    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, created_at, resume_name, jobs_json
            FROM analyses
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    history = []

    for row in rows:
        item = dict(row)

        try:
            item["jobs"] = json.loads(item["jobs_json"] or "[]")
        except (json.JSONDecodeError, TypeError):
            item["jobs"] = []

        history.append(item)

    return history


def get_analyses(limit=100):
    history = get_history(limit)

    # Format required by app.py:
    # ID, Resume, Job Title, Match Score, Date
    rows = []

    for analysis in history:
        jobs = analysis.get("jobs", [])

        if not jobs:
            rows.append((
                analysis["id"],
                analysis["resume_name"],
                "Unknown",
                0,
                analysis["created_at"],
            ))
            continue

        for job in jobs:
            rows.append((
                analysis["id"],
                analysis["resume_name"],
                job.get("title", "Unknown"),
                job.get("match_score", 0),
                analysis["created_at"],
            ))

    return rows


def get_stats():
    history = get_history(limit=100000)

    scores = []
    job_count = 0

    for analysis in history:
        for job in analysis.get("jobs", []):
            job_count += 1

            try:
                score = float(job.get(
                    "match_score",
                    job.get("score", 0)
                ))
                scores.append(max(0, min(100, score)))
            except (TypeError, ValueError):
                pass

    return {
        "total": len(history),
        "average": round(sum(scores) / len(scores), 1)
        if scores else 0,
        "jobs": job_count,
        "total_analyses": len(history),
        "total_jobs": job_count,
        "average_match_score": round(
            sum(scores) / len(scores), 1
        ) if scores else 0,
        "recent_analyses": history[:5],
    }


def delete_analysis(analysis_id):
    init_db()

    with get_connection() as conn:
        conn.execute(
            "DELETE FROM analyses WHERE id = ?",
            (analysis_id,),
        )

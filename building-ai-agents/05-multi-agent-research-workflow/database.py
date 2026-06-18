import sqlite3
from pathlib import Path
from typing import Any

from file_utils import load_sql_file


BASE_DIR = Path(__file__).resolve().parent
SQL_DIR = BASE_DIR / "sql"
DB_FILE = BASE_DIR / "research.db"


def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_db_connection() as conn:
        conn.executescript(load_sql_file(SQL_DIR / "create_research_plans_table.sql"))


def get_research_plans() -> list[dict[str, Any]]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(load_sql_file(SQL_DIR / "get_research_plans.sql"))
        return [dict(row) for row in cursor.fetchall()]


def add_research_plan(short_summary: str, details: str) -> dict[str, Any]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            load_sql_file(SQL_DIR / "insert_research_plan.sql"),
            (short_summary, details),
        )
        research_plan_id = cursor.lastrowid
        conn.commit()

    return {
        "id": research_plan_id,
        "short_summary": short_summary,
        "details": details,
    }


def delete_research_plan(research_plan_id: int) -> dict[str, Any]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            load_sql_file(SQL_DIR / "delete_research_plan.sql"),
            (research_plan_id,),
        )
        deleted_count = cursor.rowcount
        conn.commit()

    return {
        "id": research_plan_id,
        "deleted": deleted_count > 0,
    }

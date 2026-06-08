from __future__ import annotations

import json
from pathlib import Path
import sqlite3
from typing import Any


class OpportunityStore:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def upsert(self, opportunity: Any) -> bool:
        with sqlite3.connect(self.path) as connection:
            cursor = connection.execute(
                """
                INSERT OR IGNORE INTO opportunities (
                    title,
                    category,
                    audience,
                    source_name,
                    source_url,
                    opportunity_url,
                    summary
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    opportunity.title,
                    opportunity.category,
                    opportunity.audience,
                    opportunity.source_name,
                    opportunity.source_url,
                    opportunity.opportunity_url,
                    opportunity.summary,
                ),
            )
            return cursor.rowcount > 0

    def export_json(self, path: Path) -> None:
        rows = self.all()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")

    def all(self) -> list[dict[str, Any]]:
        with sqlite3.connect(self.path) as connection:
            connection.row_factory = sqlite3.Row
            rows = connection.execute(
                """
                SELECT
                    title,
                    category,
                    audience,
                    source_name,
                    source_url,
                    opportunity_url,
                    summary,
                    first_seen_at,
                    last_seen_at
                FROM opportunities
                ORDER BY first_seen_at DESC, title ASC
                """
            ).fetchall()
            return [dict(row) for row in rows]

    def _initialize(self) -> None:
        with sqlite3.connect(self.path) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS opportunities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    category TEXT NOT NULL DEFAULT 'general',
                    audience TEXT NOT NULL DEFAULT 'General Public',
                    source_name TEXT NOT NULL,
                    source_url TEXT NOT NULL,
                    opportunity_url TEXT NOT NULL UNIQUE,
                    summary TEXT NOT NULL,
                    first_seen_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    last_seen_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_opportunities_source
                ON opportunities(source_name)
                """
            )
            self._add_column_if_missing(
                connection,
                "category",
                "TEXT NOT NULL DEFAULT 'general'",
            )
            self._add_column_if_missing(
                connection,
                "audience",
                "TEXT NOT NULL DEFAULT 'General Public'",
            )
            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_opportunities_category
                ON opportunities(category)
                """
            )

    def _add_column_if_missing(
        self,
        connection: sqlite3.Connection,
        name: str,
        definition: str,
    ) -> None:
        columns = {
            row[1]
            for row in connection.execute("PRAGMA table_info(opportunities)").fetchall()
        }
        if name not in columns:
            connection.execute(f"ALTER TABLE opportunities ADD COLUMN {name} {definition}")

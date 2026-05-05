import asyncio
import json
import sqlite3
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from langgraph.store.base import (
    BaseStore,
    GetOp,
    Item,
    ListNamespacesOp,
    Op,
    PutOp,
    Result,
    SearchItem,
    SearchOp,
)

DB_PATH = Path(__file__).parent.parent / "memory.db"


class SqliteStore(BaseStore):
    def __init__(self, path: Path = DB_PATH):
        self._lock = threading.Lock()
        self._conn = sqlite3.connect(str(path), check_same_thread=False)
        self._conn.execute("""
            CREATE TABLE IF NOT EXISTS store (
                namespace TEXT NOT NULL,
                key       TEXT NOT NULL,
                value     TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                PRIMARY KEY (namespace, key)
            )
        """)
        self._conn.commit()

    def _ns(self, namespace: tuple) -> str:
        return json.dumps(namespace)

    def _handle(self, op: Op) -> Result:
        if isinstance(op, PutOp):
            ns = self._ns(op.namespace)
            if op.value is None:
                print(f"DELETE key {ns} {op.key}")
                self._conn.execute(
                    "DELETE FROM store WHERE namespace=? AND key=?", (ns, op.key)
                )
            else:
                now = datetime.now(timezone.utc).isoformat()
                existing = self._conn.execute(
                    "SELECT created_at FROM store WHERE namespace=? AND key=?",
                    (ns, op.key),
                ).fetchone()
                created_at = existing[0] if existing else now
                self._conn.execute(
                    """INSERT OR REPLACE INTO store (namespace, key, value, created_at, updated_at)
                       VALUES (?, ?, ?, ?, ?)""",
                    (ns, op.key, json.dumps(op.value), created_at, now),
                )
            self._conn.commit()
            return None

        if isinstance(op, GetOp):
            ns = self._ns(op.namespace)
            row = self._conn.execute(
                "SELECT value, created_at, updated_at FROM store WHERE namespace=? AND key=?",
                (ns, op.key),
            ).fetchone()
            if row is None:
                return None
            return Item(
                value=json.loads(row[0]),
                key=op.key,
                namespace=op.namespace,
                created_at=datetime.fromisoformat(row[1]),
                updated_at=datetime.fromisoformat(row[2]),
            )

        if isinstance(op, SearchOp):
            prefix = self._ns(op.namespace_prefix)[:-1]  # strip trailing ]
            rows = self._conn.execute(
                """SELECT namespace, key, value, created_at, updated_at
                   FROM store WHERE namespace LIKE ?
                   LIMIT ? OFFSET ?""",
                (prefix + "%", op.limit, op.offset),
            ).fetchall()
            results = []
            for ns_str, key, value_str, created_at, updated_at in rows:
                value = json.loads(value_str)
                # Simple text filter when no vector search available
                if op.query:
                    if op.query.lower() not in json.dumps(value).lower():
                        continue
                results.append(SearchItem(
                    namespace=tuple(json.loads(ns_str)),
                    key=key,
                    value=value,
                    created_at=datetime.fromisoformat(created_at),
                    updated_at=datetime.fromisoformat(updated_at),
                ))
            return results

        if isinstance(op, ListNamespacesOp):
            rows = self._conn.execute("SELECT DISTINCT namespace FROM store").fetchall()
            return [tuple(json.loads(row[0])) for row in rows]

        return None

    def batch(self, ops: Iterable[Op]) -> list[Result]:
        with self._lock:
            return [self._handle(op) for op in ops]

    async def abatch(self, ops: Iterable[Op]) -> list[Result]:
        ops = list(ops)
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.batch, ops)


store = SqliteStore()

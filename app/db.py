from typing import Any, Dict, List

import aiosqlite


_SCHEMA = """
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_messages_user_id_id
    ON messages(user_id, id);
"""


class ChatHistoryRepo:
    def __init__(self, db_path: str) -> None:
        self._db_path = db_path

    async def init(self) -> None:
        async with aiosqlite.connect(self._db_path) as db:
            await db.executescript(_SCHEMA)
            await db.commit()

    async def clear(self, user_id: int) -> None:
        async with aiosqlite.connect(self._db_path) as db:
            await db.execute("DELETE FROM messages WHERE user_id = ?", (user_id,))
            await db.commit()

    async def add(self, user_id: int, role: str, content: str) -> None:
        async with aiosqlite.connect(self._db_path) as db:
            await db.execute(
                "INSERT INTO messages(user_id, role, content) VALUES (?, ?, ?)",
                (user_id, role, content),
            )
            await db.commit()

    async def fetch(self, user_id: int, limit: int) -> List[Dict[str, Any]]:
        async with aiosqlite.connect(self._db_path) as db:
            cur = await db.execute(
                """
                SELECT role, content
                FROM messages
                WHERE user_id = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (user_id, limit),
            )
            rows = await cur.fetchall()

        rows.reverse()
        return [{"role": role, "content": content} for role, content in rows]

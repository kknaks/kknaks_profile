"""채팅 저장소 — 대화·메시지. **온톨로지 DB 와 다른 파일이다.**

브론즈~골드는 빌드가 통째로 다시 만드는 산출물이라 같은 파일에 대화를 두면 재빌드 때
기록이 함께 날아간다. 계층 경계 이전에 수명이 다르다.

표준 라이브러리 `sqlite3` 만 쓴다(레포 규약 — ORM 없음). 호출마다 커넥션을 열고 닫아
스레드 경계를 넘기지 않는다 — FastAPI 의 동기 라우터와 백그라운드 asyncio 태스크가
같은 저장소를 동시에 만진다.
"""

from __future__ import annotations

import datetime
import json
import sqlite3
import uuid
from contextlib import contextmanager
from pathlib import Path
from typing import Any

from config import settings

ROLE_USER = "user"
ROLE_ASSISTANT = "assistant"

STATUS_PENDING = "pending"
STATUS_DONE = "done"
STATUS_FAILED = "failed"

#: SPEC-003 Case Matrix — `status: failed` 일 때만 실린다
CODE_AI_FAILED = "AI_FAILED"
CODE_AI_TIMEOUT = "AI_TIMEOUT"

_DDL = [
    """CREATE TABLE IF NOT EXISTS conversations (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  ai_session_id TEXT,
  created_at TEXT NOT NULL,
  last_message_at TEXT NOT NULL
)""",
    """CREATE TABLE IF NOT EXISTS messages (
  id TEXT PRIMARY KEY,
  conversation_id TEXT NOT NULL,
  role TEXT NOT NULL,
  status TEXT NOT NULL,
  content TEXT NOT NULL DEFAULT '',
  steps TEXT NOT NULL DEFAULT '[]',
  result TEXT,
  error_code TEXT,
  task_id TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  FOREIGN KEY (conversation_id) REFERENCES conversations(id)
)""",
    "CREATE INDEX IF NOT EXISTS ix_messages_conv ON messages(conversation_id, created_at)",
    "CREATE INDEX IF NOT EXISTS ix_messages_pending ON messages(status)",
]


def _now() -> str:
    """마이크로초까지 남긴다 — 초 단위면 같은 초에 만든 대화가 동률이 돼 목록 순서가
    임의로 뒤집힌다(FE 가 최신순으로 그린다)."""
    return datetime.datetime.now(datetime.UTC).isoformat(timespec="microseconds")


def chat_db_path() -> Path:
    return settings.resolved_chat_db_path


@contextmanager
def connect(path: Path | None = None):
    target = Path(path) if path is not None else chat_db_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(target, isolation_level=None, timeout=10.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode = WAL")   # 폴링 읽기와 폴딩 쓰기가 겹친다
    try:
        for stmt in _DDL:
            conn.execute(stmt)
        yield conn
    finally:
        conn.close()


def _row_to_message(row: sqlite3.Row) -> dict:
    return {
        "id": row["id"],
        "role": row["role"],
        "status": row["status"],
        "error_code": row["error_code"],
        "content": row["content"],
        "steps": json.loads(row["steps"] or "[]"),
        "result": json.loads(row["result"]) if row["result"] else None,
        "created_at": row["created_at"],
    }


def _row_to_conversation(row: sqlite3.Row) -> dict:
    # `ai_session_id` 는 내부값이라 **응답에 싣지 않는다**(SPEC-003 Data Contract)
    return {
        "id": row["id"],
        "title": row["title"],
        "created_at": row["created_at"],
        "last_message_at": row["last_message_at"],
    }


def create_conversation(conn: sqlite3.Connection, *, question: str) -> str:
    cid = uuid.uuid4().hex
    now = _now()
    title = question.strip()[:60] or "새 대화"
    conn.execute(
        "INSERT INTO conversations (id, title, ai_session_id, created_at, last_message_at) "
        "VALUES (?, ?, NULL, ?, ?)", (cid, title, now, now))
    return cid


def add_message(
    conn: sqlite3.Connection, *, conversation_id: str, role: str, status: str,
    content: str = "",
) -> str:
    mid = uuid.uuid4().hex
    now = _now()
    conn.execute(
        "INSERT INTO messages (id, conversation_id, role, status, content, steps, "
        "created_at, updated_at) VALUES (?, ?, ?, ?, ?, '[]', ?, ?)",
        (mid, conversation_id, role, status, content, now, now))
    conn.execute("UPDATE conversations SET last_message_at = ? WHERE id = ?", (now, conversation_id))
    return mid


def get_conversation(conn: sqlite3.Connection, conversation_id: str) -> dict | None:
    row = conn.execute("SELECT * FROM conversations WHERE id = ?", (conversation_id,)).fetchone()
    return _row_to_conversation(row) if row else None


def list_conversations(conn: sqlite3.Connection, limit: int = 50) -> list[dict]:
    rows = conn.execute(
        # rowid 로 동률을 깬다 — 시각이 같아도 순서가 흔들리지 않는다
        "SELECT * FROM conversations ORDER BY last_message_at DESC, rowid DESC LIMIT ?",
        (limit,))
    return [_row_to_conversation(r) for r in rows]


def list_messages(conn: sqlite3.Connection, conversation_id: str) -> list[dict]:
    rows = conn.execute(
        "SELECT * FROM messages WHERE conversation_id = ? ORDER BY created_at, rowid",
        (conversation_id,))
    return [_row_to_message(r) for r in rows]


def get_message(conn: sqlite3.Connection, message_id: str) -> sqlite3.Row | None:
    return conn.execute("SELECT * FROM messages WHERE id = ?", (message_id,)).fetchone()


@contextmanager
def exclusive(conn: sqlite3.Connection):
    """검사와 삽입을 한 트랜잭션에 묶는다.

    `isolation_level=None`(autocommit)이라 검사 후 삽입 사이에 틈이 있다 — 동시 요청
    둘이 모두 `has_pending` 을 통과해 `pending` 이 두 건 생길 수 있다(검수 W4).
    `BEGIN IMMEDIATE` 로 쓰기 락을 먼저 잡아 그 틈을 없앤다.
    """
    conn.execute("BEGIN IMMEDIATE")
    try:
        yield conn
    except BaseException:
        conn.execute("ROLLBACK")
        raise
    conn.execute("COMMIT")


def has_pending(conn: sqlite3.Connection, conversation_id: str) -> bool:
    """한 대화에 `pending` assistant 는 **최대 1** — 동시 질문은 409 다.

    검사와 삽입을 함께 묶으려면 `exclusive()` 안에서 불러야 한다.
    """
    row = conn.execute(
        "SELECT COUNT(*) FROM messages WHERE conversation_id = ? AND role = ? AND status = ?",
        (conversation_id, ROLE_ASSISTANT, STATUS_PENDING)).fetchone()
    return row[0] > 0


#: `update_message` 가 쓸 수 있는 컬럼. 컬럼명이 f-string 으로 SQL 에 들어가므로
#: 「호출부가 전부 내부 리터럴」이라는 전제를 **코드로** 남긴다(검수 nit 5).
_UPDATABLE_COLUMNS = frozenset({
    "status", "content", "steps", "result", "error_code", "task_id",
})


def update_message(conn: sqlite3.Connection, message_id: str, fields: dict[str, Any]) -> None:
    if not fields:
        return
    unknown = set(fields) - _UPDATABLE_COLUMNS
    if unknown:
        raise ValueError(f"update_message 가 쓸 수 없는 컬럼: {sorted(unknown)}")
    payload = dict(fields)
    for key in ("steps", "result"):
        if key in payload and not isinstance(payload[key], (str, type(None))):
            payload[key] = json.dumps(payload[key], ensure_ascii=False)
    payload["updated_at"] = _now()
    assignments = ", ".join(f'"{k}" = ?' for k in payload)
    conn.execute(
        f"UPDATE messages SET {assignments} WHERE id = ?", (*payload.values(), message_id))


def set_session_id(conn: sqlite3.Connection, conversation_id: str, session_id: str) -> None:
    """대화 하나 = codex 세션 하나. 이미 있으면 덮지 않는다."""
    conn.execute(
        "UPDATE conversations SET ai_session_id = ? WHERE id = ? AND ai_session_id IS NULL",
        (session_id, conversation_id))


def get_session_id(conn: sqlite3.Connection, conversation_id: str) -> str | None:
    row = conn.execute(
        "SELECT ai_session_id FROM conversations WHERE id = ?", (conversation_id,)).fetchone()
    return row["ai_session_id"] if row else None


def list_pending(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    return conn.execute(
        "SELECT * FROM messages WHERE role = ? AND status = ?",
        (ROLE_ASSISTANT, STATUS_PENDING)).fetchall()

import json
import uuid

import aiosqlite
from fastapi import APIRouter, Depends

from database import get_db
from models import ChatRequest, ChatResponse
from services.recommendation import handle_chat

router = APIRouter()


async def _get_or_create_session(db: aiosqlite.Connection, session_id: str | None) -> str:
    if session_id:
        cursor = await db.execute("SELECT id FROM sessions WHERE id = ?", (session_id,))
        if await cursor.fetchone():
            return session_id

    new_id = session_id or str(uuid.uuid4())
    await db.execute(
        "INSERT INTO sessions (id) VALUES (?)",
        (new_id,),
    )
    await db.commit()
    return new_id


async def _load_message_history(db: aiosqlite.Connection, session_id: str) -> list[dict]:
    cursor = await db.execute(
        "SELECT role, content FROM messages WHERE session_id = ? ORDER BY created_at ASC LIMIT 20",
        (session_id,),
    )
    rows = await cursor.fetchall()
    return [{"role": row[0], "content": row[1]} for row in rows]


async def _save_message(db: aiosqlite.Connection, session_id: str, role: str, content: str, metadata: dict | None = None):
    await db.execute(
        "INSERT INTO messages (session_id, role, content, metadata) VALUES (?, ?, ?, ?)",
        (session_id, role, content, json.dumps(metadata, ensure_ascii=False) if metadata else None),
    )
    await db.commit()


@router.post("/chat")
async def chat(request: ChatRequest, db: aiosqlite.Connection = Depends(get_db)):
    session_id = await _get_or_create_session(db, request.session_id)

    # 메시지 이력 로드 + 새 메시지 추가
    messages = await _load_message_history(db, session_id)
    messages.append({"role": "user", "content": request.message})

    # 사용자 메시지 저장
    await _save_message(db, session_id, "user", request.message)

    # Claude 대화 처리
    reply, activities, sources = await handle_chat(db, messages)

    # 어시스턴트 응답 저장
    metadata = {}
    if activities:
        metadata["activities"] = [a.get("name", "") for a in activities]
    if sources:
        metadata["sources"] = [s.get("url", "") for s in sources]
    await _save_message(db, session_id, "assistant", reply, metadata or None)

    return ChatResponse(
        session_id=session_id,
        reply=reply,
        activities=activities,
        sources=sources,
    )


@router.get("/chat/history/{session_id}")
async def get_history(session_id: str, db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute(
        "SELECT role, content, created_at FROM messages WHERE session_id = ? ORDER BY created_at ASC",
        (session_id,),
    )
    rows = await cursor.fetchall()
    messages = [{"role": row[0], "content": row[1], "created_at": row[2]} for row in rows]
    return {"session_id": session_id, "messages": messages}

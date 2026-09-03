"""채팅 API — SPEC-003 §4 채팅 절.

- POST   /api/chat/conversations                              대화 생성 + 첫 질문
- GET    /api/chat/conversations                              목록(최신순)
- GET    /api/chat/conversations/{id}                         상세 — **폴링 대상**
- POST   /api/chat/conversations/{id}/messages                이어서 질문
- POST   /api/chat/conversations/{id}/messages/{mid}/retry    실패 답변 재시도

접수(201)는 **저장이 끝난 뒤** 돌려주고, 제출은 백그라운드로 나간다 — 제출 실패가
접수를 뒤집지 않는다. `pending` 동안 폴링이 자라나는 `content`·`steps` 를 읽는다.
"""

from __future__ import annotations

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel

from agent import runtime, store
from api.deps import require_session

router = APIRouter(
    prefix="/api/chat", tags=["chat"], dependencies=[Depends(require_session)]
)

#: SPEC-003 Validation — trim 후 1자 이상 1,000자 이하
MAX_QUESTION_LEN = 1_000


class QuestionRequest(BaseModel):
    question: str


def _validated_question(raw: str) -> str:
    question = (raw or "").strip()
    if not question:
        raise HTTPException(status_code=422, detail="EMPTY_QUESTION")
    if len(question) > MAX_QUESTION_LEN:
        raise HTTPException(status_code=422, detail="QUESTION_TOO_LONG")
    return question


def _conversation_payload(conn, conversation_id: str) -> dict:
    conversation = store.get_conversation(conn, conversation_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="NOT_FOUND")
    return {"conversation": conversation, "messages": store.list_messages(conn, conversation_id)}


def _enqueue(background: BackgroundTasks, *, message_id: str, conversation_id: str,
             question: str) -> None:
    background.add_task(
        runtime.start_turn, message_id=message_id, conversation_id=conversation_id,
        question=question)


@router.post("/conversations", status_code=201)
def create_conversation(
    body: QuestionRequest, background: BackgroundTasks,
) -> dict:
    question = _validated_question(body.question)
    with store.connect() as conn:
        conversation_id = store.create_conversation(conn, question=question)
        store.add_message(conn, conversation_id=conversation_id, role=store.ROLE_USER,
                          status=store.STATUS_DONE, content=question)
        message_id = store.add_message(
            conn, conversation_id=conversation_id, role=store.ROLE_ASSISTANT,
            status=store.STATUS_PENDING)
        payload = _conversation_payload(conn, conversation_id)
    _enqueue(background, message_id=message_id, conversation_id=conversation_id,
             question=question)
    return payload


@router.get("/conversations")
def list_conversations() -> dict:
    with store.connect() as conn:
        return {"conversations": store.list_conversations(conn)}


@router.get("/conversations/{conversation_id}")
def get_conversation(conversation_id: str) -> dict:
    with store.connect() as conn:
        return _conversation_payload(conn, conversation_id)


@router.post("/conversations/{conversation_id}/messages", status_code=201)
def add_message(
    conversation_id: str, body: QuestionRequest, background: BackgroundTasks,
) -> dict:
    question = _validated_question(body.question)
    with store.connect() as conn:
        if store.get_conversation(conn, conversation_id) is None:
            raise HTTPException(status_code=404, detail="NOT_FOUND")
        # 검사와 삽입을 한 트랜잭션에 묶는다 — 동시 요청 둘이 모두 통과해
        # `pending` 이 두 건 생기는 틈을 없앤다
        with store.exclusive(conn):
            if store.has_pending(conn, conversation_id):
                # 한 대화에 pending 은 최대 1 — 다른 대화끼리는 병렬이어도 된다
                raise HTTPException(status_code=409, detail="CONVERSATION_BUSY")
            store.add_message(conn, conversation_id=conversation_id, role=store.ROLE_USER,
                              status=store.STATUS_DONE, content=question)
            message_id = store.add_message(
                conn, conversation_id=conversation_id, role=store.ROLE_ASSISTANT,
                status=store.STATUS_PENDING)
        payload = _conversation_payload(conn, conversation_id)
    _enqueue(background, message_id=message_id, conversation_id=conversation_id,
             question=question)
    return payload


@router.post("/conversations/{conversation_id}/messages/{message_id}/retry", status_code=201)
def retry_message(
    conversation_id: str, message_id: str, background: BackgroundTasks,
) -> dict:
    """실패한 답변을 다시 제출한다 — 재시도는 **재제출**이다."""
    with store.connect() as conn:
        if store.get_conversation(conn, conversation_id) is None:
            raise HTTPException(status_code=404, detail="NOT_FOUND")
        row = store.get_message(conn, message_id)
        if row is None or row["conversation_id"] != conversation_id:
            raise HTTPException(status_code=404, detail="NOT_FOUND")
        if row["status"] != store.STATUS_FAILED:
            raise HTTPException(status_code=409, detail="CONVERSATION_BUSY")
        question = _last_question(conn, conversation_id, before_message_id=message_id)
        if question is None:
            raise HTTPException(status_code=404, detail="NOT_FOUND")
        # 같은 행을 되살린다 — 실패 흔적(부분 텍스트·단계)은 지우고 다시 센다
        store.update_message(conn, message_id, {
            "status": store.STATUS_PENDING, "error_code": None,
            "content": "", "steps": [], "result": None, "task_id": None})
        payload = _conversation_payload(conn, conversation_id)
    _enqueue(background, message_id=message_id, conversation_id=conversation_id,
             question=question)
    return payload


def _last_question(conn, conversation_id: str, *, before_message_id: str) -> str | None:
    """되살릴 답변 **바로 앞의** 사용자 질문. 대화 전체의 마지막 질문이 아니다."""
    messages = store.list_messages(conn, conversation_id)
    question = None
    for message in messages:
        if message["id"] == before_message_id:
            return question
        if message["role"] == store.ROLE_USER:
            question = message["content"]
    return question

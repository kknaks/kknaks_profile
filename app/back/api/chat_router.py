"""채용담당자 채팅 — 1층 (SPEC-017 §4 API Contract).

- GET  /api/chat/conversations              — 내 세션의 대화 목록. **쿠키 없으면 빈 목록**
- POST /api/chat/conversations              — 대화 생성 + 첫 질문. 세션 없으면 발급
- GET  /api/chat/conversations/{id}         — 대화 상세(폴링 대상)
- POST /api/chat/conversations/{id}/messages — 이어서 질문
- PATCH /api/admin/chat-exposure/{kind}/{id} — chat_exposed 토글 (admin)

## 쿠키를 굽는 곳은 여기 하나다

세션 서비스는 HTTP 를 모른다 — 「새 토큰을 심어야 한다」만 돌려주고, 속성(httpOnly ·
Lax · Secure · Max-Age)은 이 파일이 소유한다. `secure` · `domain` 은 어드민 쿠키와
같은 설정을 쓴다(같은 사이트라 두 벌로 두면 한쪽만 갱신된다).

## AI 제출은 **명시 커밋 뒤에** 건다

`BackgroundTasks` 로 미루되, 큐잉 **전에** 라우터가 `await db.commit()` 을 직접 부른다.

⚠ 한때 이 자리 주석은 「`get_db` 의 teardown commit 이 background task 보다 먼저
끝나므로 안전하다」였다. **틀렸다** — 이 FastAPI 버전에서는 background task 가
teardown 보다 **먼저** 돈다. 그래서 `start_turn` 이 새 세션으로 조회할 때 아직 커밋되지
않은 row 를 못 찾아 「제출 대상이 아니다」로 조용히 건너뛰었고, 대화가 **영구 pending**
으로 남았다(2026-08-28 로컬 compose 실측: `chat: message 2 는 제출 대상이 아니다`).
복구 경로도 없다 — 폴링은 재큐잉을 하지 않고 기동 스윕만이 재시작 때 failed 로 마감한다.

teardown 의 commit 은 그 뒤 no-op 이므로 이중 커밋은 무해하다. 순서를 **프레임워크
동작에 기대지 않고 코드로 고정**하는 것이 요점이다 — 레퍼런스(mediness
`landing_chat/runtime.py`)가 같은 사고 뒤 계약으로 박은 지점과 같다.
"""

from __future__ import annotations

from fastapi import APIRouter, BackgroundTasks, Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_db, require_admin
from config import get_settings
from schemas.chat import (
    ChatExposureResponse,
    ChatExposureUpdate,
    ChatMessageItem,
    ConversationDetailResponse,
    ConversationItem,
    ConversationsResponse,
    MessageResponse,
    MessagesResponse,
    QuestionRequest,
)
from service.chat.chat_service import chat_service
from service.chat.runtime import start_turn
from service.chat.session_service import chat_session_service
from service.chat.tool_service import chat_tool_service

router = APIRouter(prefix="/api/chat", tags=["chat"])
admin_router = APIRouter(
    prefix="/api/admin/chat-exposure",
    tags=["chat"],
    dependencies=[Depends(require_admin)],
)


def _cookie_token(request: Request) -> str | None:
    return request.cookies.get(get_settings().chat_cookie_name)


def _set_session_cookie(response: Response, token: str) -> None:
    """§4 세션 쿠키 계약 — httpOnly · SameSite=Lax · Secure · Max-Age 30일."""
    settings = get_settings()
    response.set_cookie(
        key=settings.chat_cookie_name,
        value=token,
        max_age=settings.chat_cookie_max_age_sec,
        httponly=True,
        samesite="lax",
        # 운영은 1(HTTPS 전용) — 어드민 쿠키와 같은 env 를 쓴다.
        secure=settings.auth_cookie_secure,
        domain=settings.auth_cookie_domain,
        path="/",
    )


async def _resolve_and_refresh(
    request: Request, response: Response, db: AsyncSession
) -> int | None:
    """세션을 찾고, 살아 있으면 **쿠키를 다시 굽는다**(sliding 의 브라우저 쪽 절반).

    서버는 `last_seen_at` 을 밀지만 그것만으로는 브라우저의 만료가 최초 발급 +30일에
    고정된다 — 매 응답에 같은 값을 Max-Age 와 함께 다시 심어야 「사용할 때마다 연장」
    (§4 · S-5 3항)이 성립한다.

    **쿠키가 없으면 아무것도 하지 않는다** — 세션을 만들지 않는 계약(DEC-026 D1)이
    여기서도 그대로다.
    """
    token = _cookie_token(request)
    session_id = await chat_session_service.resolve(db, token)
    if session_id is not None and token:
        _set_session_cookie(response, token)
    return session_id


@router.get(
    "/conversations", response_model=ConversationsResponse, response_model_by_alias=True
)
async def list_conversations(
    request: Request, response: Response, db: AsyncSession = Depends(get_db)
) -> ConversationsResponse:
    """쿠키가 없으면 **세션을 만들지 않고** 빈 목록(§3 S-2 · DEC-026 D1)."""
    session_id = await _resolve_and_refresh(request, response, db)
    dtos = await chat_service.list_conversations(db, session_id)
    return ConversationsResponse(
        conversations=[ConversationItem.from_dto(d) for d in dtos]
    )


@router.post(
    "/conversations",
    response_model=ConversationDetailResponse,
    response_model_by_alias=True,
    status_code=201,
)
async def create_conversation(
    body: QuestionRequest,
    request: Request,
    response: Response,
    background: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
) -> ConversationDetailResponse:
    """채팅 첫 사용이 세션 발급 시점이다(§3 S-1 2항).

    쿠키는 **새로 발급했든 쓰던 것이든 매번 다시 굽는다** — 만료 연장이 곧 sliding 이다.
    """
    session_id, token = await chat_session_service.resolve_or_create(
        db, _cookie_token(request)
    )
    bundle = await chat_service.create_conversation(db, session_id, body.question)
    _set_session_cookie(response, token)
    # `_append_turn` 은 `[user, assistant]` 를 준다 — 제출 대상은 뒤엣것이다.
    await _queue_turn(db, background, bundle.messages[-1])
    return ConversationDetailResponse.from_bundle(bundle)


@router.get(
    "/conversations/{conversation_id}",
    response_model=ConversationDetailResponse,
    response_model_by_alias=True,
)
async def get_conversation(
    conversation_id: int,
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
) -> ConversationDetailResponse:
    """폴링 대상 — pending 중에도 자란 content · steps 가 실린다(§4)."""
    session_id = await _resolve_and_refresh(request, response, db)
    bundle = await chat_service.get_conversation(db, session_id, conversation_id)
    return ConversationDetailResponse.from_bundle(bundle)


@router.post(
    "/conversations/{conversation_id}/messages",
    response_model=MessagesResponse,
    response_model_by_alias=True,
    status_code=201,
)
async def add_message(
    conversation_id: int,
    body: QuestionRequest,
    request: Request,
    response: Response,
    background: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
) -> MessagesResponse:
    """이어서 질문(§3 S-3). pending 이 있으면 409 `CONVERSATION_BUSY`."""
    session_id = await _resolve_and_refresh(request, response, db)
    messages = await chat_service.add_message(
        db, session_id, conversation_id, body.question
    )
    await _queue_turn(db, background, messages[-1])
    return MessagesResponse(messages=[ChatMessageItem.from_dto(m) for m in messages])


@router.post(
    "/conversations/{conversation_id}/messages/{message_id}/retry",
    response_model=MessageResponse,
    response_model_by_alias=True,
)
async def retry_message(
    conversation_id: int,
    message_id: int,
    request: Request,
    response: Response,
    background: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
) -> MessageResponse:
    """실패한 답변 재시도(§3 S-8 3항). **새 줄을 만들지 않는다** — 되살려 재제출한다.

    failed assistant 가 아니면 404, 대화에 pending 이 있으면 409.
    """
    session_id = await _resolve_and_refresh(request, response, db)
    revived = await chat_service.retry_message(
        db, session_id, conversation_id, message_id
    )
    await _queue_turn(db, background, revived)
    return MessageResponse(message=ChatMessageItem.from_dto(revived))


@admin_router.patch(
    "/{kind}/{item_id}",
    response_model=ChatExposureResponse,
    response_model_by_alias=True,
)
async def patch_chat_exposure(
    kind: str,
    item_id: int,
    body: ChatExposureUpdate,
    db: AsyncSession = Depends(get_db),
) -> ChatExposureResponse:
    """`chat_exposed` 토글(U-7). 다음 tool 호출부터 그대로 반영된다 — 캐시가 없다."""
    value = await chat_tool_service.set_exposure(db, kind, item_id, body.chat_exposed)
    return ChatExposureResponse(kind=kind, id=item_id, chat_exposed=value)


async def _queue_turn(
    db: AsyncSession, background: BackgroundTasks, assistant
) -> None:
    """pending assistant 를 제출 대기에 건다 — **명시 커밋 뒤에**.

    `start_turn` 은 요청 세션이 아니라 새 세션으로 이 row 를 다시 읽는다. 그래서
    큐잉 전에 여기서 커밋이 끝나 있어야 한다 — teardown 순서에 기대지 않는다
    (머리 주석의 실측 근거 참조).

    커밋을 서비스가 아니라 라우터에서 하는 이유: 트랜잭션 경계는 요청 하나이고
    (`core/db.py`), 그 경계를 아는 층이 여기다. 서비스는 여전히 flush 까지만 한다.
    """
    await db.commit()
    background.add_task(start_turn, assistant.id)

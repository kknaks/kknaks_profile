"""대화 · 메시지 — 2층. 공개 API 4종이 딛는 곳 (SPEC-017 §3 S-1~S-9 · §4).

## 소유권은 여기서만 판정한다

「남의 세션의 대화」와 「없는 대화」는 **같은 404** 다(§4 Case Matrix). 다르게 답하면
남의 대화 id 를 훑어 존재 여부를 알아낼 수 있다.

## 직렬화는 두 겹이고, **두 겹이 같은 답을 준다**

한 대화에 pending assistant 는 최대 하나(§5). 여기서 세어 보고 409 를 내되, 그것이
유일한 방어는 아니다 — 동시 요청이 둘 다 검사를 통과하는 창이 있으므로 DB 의 partial
unique index(`uq_chat_message_pending`)가 최종 방어선이다.

그 방어선에 걸린 요청도 **같은 409 `CONVERSATION_BUSY`** 를 받아야 한다. 안 그러면
같은 위반이 타이밍에 따라 409 도 되고 500 도 된다(W1 리뷰 W2). 그래서 `IntegrityError`
를 이 층에서 도메인 예외로 접는다 — 라우터는 여전히 DB 를 모르고, 아래층은 여전히
HTTP 를 모른다.

## AI 제출은 여기서 하지 않는다

이 층은 「pending assistant 를 만들어 두는 것」까지다. 제출은 **요청 트랜잭션이 커밋된
뒤**에 일어나야 한다(안 그러면 워커가 아직 안 보이는 row 를 찾다 실패한다) — 그 배선은
`runtime.py` 가 갖고 라우터가 background 로 부른다.
"""

from __future__ import annotations

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import ConflictError, NotFoundError, ValidationError
from dto.chat import ChatMessageDTO, ConversationBundle, ConversationDTO
from models.chat import (
    ROLE_ASSISTANT,
    ROLE_USER,
    STATUS_DONE,
    STATUS_FAILED,
    STATUS_PENDING,
)
from repository.chat_repo import ChatRepository, chat_repository
from schemas.chat import (
    CODE_CONVERSATION_BUSY,
    CODE_EMPTY_QUESTION,
    CODE_NOT_FOUND,
    CODE_QUESTION_TOO_LONG,
    QUESTION_MAX_LENGTH,
)

# 사이드바 제목 상한(§2 U-4 「최대 50자, 말줄임」). 말줄임표를 서버가 붙인다 —
# 잘렸다는 사실이 저장된 값에 남아야 어드민 열람에서도 같은 것이 보인다.
_TITLE_MAX = 50


def _validate_question(raw: str | None) -> str:
    """trim 후 1~1000자(§4 Validation). 코드는 Case Matrix 그대로 detail 에 싣는다."""
    question = (raw or "").strip()
    if not question:
        raise ValidationError(CODE_EMPTY_QUESTION)
    if len(question) > QUESTION_MAX_LENGTH:
        raise ValidationError(CODE_QUESTION_TOO_LONG)
    return question


def _title_of(question: str) -> str:
    return question if len(question) <= _TITLE_MAX else question[:_TITLE_MAX] + "…"


class ChatService:
    def __init__(self, repo: ChatRepository) -> None:
        self._repo = repo

    async def list_conversations(
        self, session: AsyncSession, session_id: int | None
    ) -> list[ConversationDTO]:
        """쿠키가 없으면 빈 목록 — 세션을 만들지 않는다(§3 S-2)."""
        if session_id is None:
            return []
        return await self._repo.list_conversations(session, session_id)

    async def _own_conversation(
        self, session: AsyncSession, session_id: int | None, conversation_id: int
    ) -> ConversationDTO:
        """내 세션의 대화만 돌려준다. 아니면 404 — 없는 것과 구분하지 않는다."""
        conversation = await self._repo.get_conversation(session, conversation_id)
        if conversation is None or conversation.session_id != session_id:
            raise NotFoundError(CODE_NOT_FOUND)
        return conversation

    async def get_conversation(
        self, session: AsyncSession, session_id: int | None, conversation_id: int
    ) -> ConversationBundle:
        """폴링이 2초마다 부르는 것 — pending 중에도 자란 content · steps 가 실린다."""
        conversation = await self._own_conversation(session, session_id, conversation_id)
        messages = await self._repo.list_messages(session, conversation_id)
        return ConversationBundle(conversation=conversation, messages=messages)

    async def create_conversation(
        self, session: AsyncSession, session_id: int, question: str
    ) -> ConversationBundle:
        """대화 생성 + 첫 질문(§3 S-1 3항). assistant 는 pending 으로 만들어만 둔다."""
        text = _validate_question(question)
        conversation = await self._repo.create_conversation(
            session, session_id=session_id, title=_title_of(text)
        )
        messages = await self._append_turn(session, conversation.id, text)
        return ConversationBundle(conversation=conversation, messages=messages)

    async def add_message(
        self, session: AsyncSession, session_id: int | None, conversation_id: int, question: str
    ) -> list[ChatMessageDTO]:
        """이어서 질문(§3 S-3). pending 이 있으면 409 — 같은 codex 세션을 동시에 resume 하지 않는다."""
        text = _validate_question(question)
        await self._own_conversation(session, session_id, conversation_id)
        if await self._repo.pending_count(session, conversation_id) > 0:
            raise ConflictError(CODE_CONVERSATION_BUSY)
        return await self._append_turn(session, conversation_id, text)

    async def retry_message(
        self,
        session: AsyncSession,
        session_id: int | None,
        conversation_id: int,
        message_id: int,
    ) -> ChatMessageDTO:
        """실패한 답변을 되살린다(§3 S-8 3항 · spec v0.0.5).

        **새 줄을 만들지 않는다** — 그 assistant 메시지를 pending 으로 되돌리고 같은
        질문으로 재제출한다. 새로 만들면 스레드에 같은 질문이 두 번 보인다(리뷰 W6).

        대상이 이 대화의 failed assistant 가 아니면 **전부 같은 404** 다: 없는 id ·
        남의 대화의 메시지 · user 줄 · 아직 pending 이거나 이미 done 인 줄. 구분하면
        남의 스레드 모양이 새어 나온다.
        """
        await self._own_conversation(session, session_id, conversation_id)
        message = await self._repo.get_message(session, message_id)
        if (
            message is None
            or message.conversation_id != conversation_id
            or message.role != ROLE_ASSISTANT
            or message.status != STATUS_FAILED
        ):
            raise NotFoundError(CODE_NOT_FOUND)
        if await self._repo.pending_count(session, conversation_id) > 0:
            raise ConflictError(CODE_CONVERSATION_BUSY)

        revived = await self._busy_guarded(
            self._repo.update_message(
                session,
                message_id,
                {
                    # 지난 시도의 흔적을 전부 지운다 — 남겨 두면 새 폴딩이 옛 단계
                    # 위에 쌓여 「이번에 무엇을 했나」를 읽을 수 없다.
                    "status": STATUS_PENDING,
                    "content": "",
                    "steps": None,
                    "sources": None,
                    "error_code": None,
                    "task_id": None,
                },
            )
        )
        if revived is None:
            raise NotFoundError(CODE_NOT_FOUND)
        return revived

    async def _append_turn(
        self, session: AsyncSession, conversation_id: int, question: str
    ) -> list[ChatMessageDTO]:
        """질문 + 빈 답변(pending) 한 쌍. 응답의 `messages` 가 이 둘이다."""
        user = await self._repo.create_message(
            session,
            {
                "conversation_id": conversation_id,
                "role": ROLE_USER,
                "status": STATUS_DONE,   # 질문은 자라지 않는다
                "content": question,
            },
        )
        assistant = await self._busy_guarded(
            self._repo.create_message(
                session,
                {
                    "conversation_id": conversation_id,
                    "role": ROLE_ASSISTANT,
                    "status": STATUS_PENDING,
                    "content": "",
                },
            )
        )
        return [user, assistant]

    @staticmethod
    async def _busy_guarded(awaitable):
        """pending 유니크 위반을 409 로 접는다 — 앱 검사와 DB 방어선이 같은 답을 준다.

        `IntegrityError` 를 통째로 접는 것이 아니라 **이 자리에서 날 수 있는 위반이
        그것 하나**라서 접는다. 이 대화에 pending 을 하나 더 만들려는 시도 외에는
        여기서 유니크 제약을 건드릴 경로가 없다(FK 위반은 소유권 검사가 먼저 잡는다).
        """
        try:
            return await awaitable
        except IntegrityError as exc:
            raise ConflictError(CODE_CONVERSATION_BUSY) from exc


chat_service = ChatService(chat_repository)

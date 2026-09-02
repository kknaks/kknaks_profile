"""채팅 — front ↔ back 계약 (SPEC-017 §4 Request/Response 그대로).

**여기서 필드를 발명하지 않는다.** FE(`lib/chat-types.ts`)가 이 모양을 그대로 물고
있으므로 이름 하나만 갈려도 화면이 조용히 빈다.

내부 필드는 여기서 걸러진다 — `conversation.ai_session_id`, 메시지의 `task_id` ·
`error_code` · turn 토큰은 응답에 없다(§4 Data Contract «내부 필드(비노출)»).
`steps` 도 저장 모양(`toolUseId`·`status` 포함)이 아니라 **spec 의 네 필드만** 나간다.
"""

from __future__ import annotations

# `date` 는 인사이트의 **필드 이름**이기도 하다 — 애너테이션이 필드에 가리지 않게 별칭으로 든다.
from datetime import date as _Date
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from dto.chat import (
    AdminConversationDTO,
    AdminConversationPageDTO,
    ChatInsightsDTO,
    ChatMessageDTO,
    ConversationBundle,
    ConversationDTO,
)

# 질문 길이 — §4 Validation. FE 의 QUESTION_MAX_LENGTH 와 같은 수다.
QUESTION_MAX_LENGTH = 1000

# Case Matrix(§4)의 에러 코드. 도메인 예외의 detail 로 그대로 실어 보낸다 —
# FE 가 `detail` 문자열에서 코드를 읽는다(lib/chat.ts `pickCode`).
CODE_EMPTY_QUESTION = "EMPTY_QUESTION"
CODE_QUESTION_TOO_LONG = "QUESTION_TOO_LONG"
CODE_NOT_FOUND = "NOT_FOUND"
CODE_CONVERSATION_BUSY = "CONVERSATION_BUSY"


class QuestionRequest(BaseModel):
    """`{question}` — 대화 생성과 이어서 질문이 같은 본문을 쓴다.

    길이 판정은 **서비스가 한다**(trim 후 1~1000). pydantic 으로 막으면 422 는 나오되
    Case Matrix 의 코드(`EMPTY_QUESTION`/`QUESTION_TOO_LONG`)를 구분해 실을 수 없다.
    """

    question: str


class ChatSourceItem(BaseModel):
    """근거 카드 — AI 가 실제로 읽은 문서(§3 S-9 2항)."""

    type: str          # career | project | problem | note
    slug: str
    title: str
    # career · problem 은 아이템 전용 상세 페이지가 없다 — 공개 표면(`/career`)을 준다.
    # 그마저 없는 유형이 생기면 null 이고, 화면은 링크를 걸지 않는다.
    url: str | None = None


class ChatStepItem(BaseModel):
    """tool 호출 한 단계 — 기록 주체는 소비자다(AI 자기 신고가 아니다)."""

    model_config = ConfigDict(populate_by_name=True)

    tool: str
    args_summary: str = Field(default="", serialization_alias="argsSummary")
    duration_ms: int | None = Field(default=None, serialization_alias="durationMs")
    called_at: str = Field(default="", serialization_alias="calledAt")


class ChatMessageItem(BaseModel):
    id: int
    role: str
    status: str
    content: str
    sources: list[ChatSourceItem] = []
    steps: list[ChatStepItem] = []
    created_at: datetime = Field(serialization_alias="createdAt")

    @classmethod
    def from_dto(cls, dto: ChatMessageDTO) -> ChatMessageItem:
        return cls(
            id=dto.id,
            role=dto.role,
            status=dto.status,
            content=dto.content,
            sources=[ChatSourceItem(**_source_fields(s)) for s in dto.sources],
            steps=[_step_item(s) for s in dto.steps],
            created_at=dto.created_at,
        )


class ConversationItem(BaseModel):
    id: int
    title: str
    created_at: datetime = Field(serialization_alias="createdAt")

    @classmethod
    def from_dto(cls, dto: ConversationDTO) -> ConversationItem:
        # ai_session_id 는 싣지 않는다 — 내부 필드다.
        return cls(id=dto.id, title=dto.title, created_at=dto.created_at)


class ConversationsResponse(BaseModel):
    """목록 봉투. 쿠키가 없으면 빈 배열이고 세션은 만들지 않는다(§3 S-2)."""

    conversations: list[ConversationItem]


class ConversationDetailResponse(BaseModel):
    conversation: ConversationItem
    messages: list[ChatMessageItem]

    @classmethod
    def from_bundle(cls, bundle: ConversationBundle) -> ConversationDetailResponse:
        return cls(
            conversation=ConversationItem.from_dto(bundle.conversation),
            messages=[ChatMessageItem.from_dto(m) for m in bundle.messages],
        )


class MessagesResponse(BaseModel):
    """이어서 질문의 응답 — `{messages: [user, assistant(pending)]}`."""

    messages: list[ChatMessageItem]


class MessageResponse(BaseModel):
    """재시도의 응답 — `{message: assistant(pending)}`.

    **한 줄만** 돌려준다. 재시도는 되살리기라 새 줄이 없다(§3 S-8 3항).
    """

    message: ChatMessageItem


class ChatExposureResponse(BaseModel):
    """어드민 토글 결과 — 무엇을 어떻게 바꿨는지 그대로 되돌려준다."""

    model_config = ConfigDict(populate_by_name=True)

    kind: str
    id: int
    chat_exposed: bool = Field(serialization_alias="chatExposed")


class ChatExposureUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    chat_exposed: bool = Field(alias="chatExposed")


# ── 어드민 열람·인사이트 (SPEC-017 §2 U-8 · §4 어드민 응답 계약) ──
#
# 필드명은 spec §4 「어드민 chat API 응답 계약」 그대로다. FE 가 이 이름으로 mock 을
# 세워 병행했으므로 하나만 갈려도 위젯이 조용히 빈다.


class AdminConversationItem(BaseModel):
    """목록 한 줄. `sessionId` 는 **정수 id 뿐**이다 — 쿠키 토큰·해시는 나가지 않는다."""

    id: int
    session_id: int = Field(serialization_alias="sessionId")
    title: str
    message_count: int = Field(serialization_alias="messageCount")
    created_at: datetime = Field(serialization_alias="createdAt")
    last_message_at: datetime = Field(serialization_alias="lastMessageAt")

    @classmethod
    def from_dto(cls, dto: AdminConversationDTO) -> AdminConversationItem:
        return cls(
            id=dto.id,
            session_id=dto.session_id,
            title=dto.title,
            message_count=dto.message_count,
            created_at=dto.created_at,
            last_message_at=dto.last_message_at,
        )


class AdminConversationsResponse(BaseModel):
    """`{items, total, page, size}` — 커밋 목록의 `pageSize` 가 아니라 spec 의 `size` 다."""

    items: list[AdminConversationItem]
    total: int
    page: int
    size: int

    @classmethod
    def from_dto(cls, dto: AdminConversationPageDTO) -> AdminConversationsResponse:
        return cls(
            items=[AdminConversationItem.from_dto(i) for i in dto.items],
            total=dto.total,
            page=dto.page,
            size=dto.size,
        )


class AdminConversationInfo(ConversationItem):
    """공개 상세의 conversation + `sessionId`(§4). `ai_session_id` 는 여전히 안 나간다."""

    session_id: int = Field(serialization_alias="sessionId")

    @classmethod
    def from_dto(cls, dto: ConversationDTO) -> AdminConversationInfo:
        return cls(
            id=dto.id,
            title=dto.title,
            created_at=dto.created_at,
            session_id=dto.session_id,
        )


class AdminConversationDetailResponse(BaseModel):
    """공개 상세와 같은 shape — 스레드 렌더를 그대로 재사용하기 위해서다(U-8 CTA)."""

    conversation: AdminConversationInfo
    messages: list[ChatMessageItem]

    @classmethod
    def from_bundle(cls, bundle: ConversationBundle) -> AdminConversationDetailResponse:
        return cls(
            conversation=AdminConversationInfo.from_dto(bundle.conversation),
            messages=[ChatMessageItem.from_dto(m) for m in bundle.messages],
        )


class ChatTotalsItem(BaseModel):
    conversations: int
    questions: int
    last7d: int


class RecentQuestionItem(BaseModel):
    question: str
    asked_at: datetime = Field(serialization_alias="askedAt")
    conversation_id: int = Field(serialization_alias="conversationId")


class DailyQuestionItem(BaseModel):
    """하루 한 칸. `date` 는 KST 날짜(`YYYY-MM-DD`) — 빈 날도 0 으로 온다."""

    date: _Date
    count: int


class TopSourceItem(BaseModel):
    type: str
    slug: str
    title: str
    count: int


class ChatInsightsResponse(BaseModel):
    totals: ChatTotalsItem
    recent_questions: list[RecentQuestionItem] = Field(
        serialization_alias="recentQuestions"
    )
    daily: list[DailyQuestionItem]
    top_sources: list[TopSourceItem] = Field(serialization_alias="topSources")

    @classmethod
    def from_dto(cls, dto: ChatInsightsDTO) -> ChatInsightsResponse:
        return cls(
            totals=ChatTotalsItem(
                conversations=dto.conversations,
                questions=dto.questions,
                last7d=dto.last7d,
            ),
            recent_questions=[
                RecentQuestionItem(
                    question=q.question,
                    asked_at=q.asked_at,
                    conversation_id=q.conversation_id,
                )
                for q in dto.recent_questions
            ],
            daily=[DailyQuestionItem(date=d.day, count=d.count) for d in dto.daily],
            top_sources=[
                TopSourceItem(type=s.type, slug=s.slug, title=s.title, count=s.count)
                for s in dto.top_sources
            ],
        )


def _source_fields(raw: dict) -> dict:
    """저장된 source dict → 계약 필드만. 모르는 키는 버린다."""
    return {
        "type": str(raw.get("type") or ""),
        "slug": str(raw.get("slug") or ""),
        "title": str(raw.get("title") or ""),
        "url": raw.get("url"),
    }


def _step_item(raw: dict) -> ChatStepItem:
    """저장된 step dict → 계약 네 필드만.

    `toolUseId`(멱등 키)·`status` 는 소비자의 내부 사정이라 나가지 않는다.
    """
    return ChatStepItem(
        tool=str(raw.get("tool") or ""),
        args_summary=str(raw.get("argsSummary") or ""),
        duration_ms=raw.get("durationMs"),
        called_at=str(raw.get("calledAt") or ""),
    )

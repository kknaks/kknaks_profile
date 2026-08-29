"""어드민 채팅 열람·인사이트 — 2층 (SPEC-017 §2 U-8 · §4 어드민 chat API 3종).

## 방문자 서비스와 갈라 두는 이유

`chat_service` 는 **소유권 판정이 존재 이유**다 — 남의 대화는 없는 대화다(§4 Case
Matrix). 어드민은 그 반대로 **전부 본다**. 같은 클래스에 두면 「session_id 를 None 으로
주면 전부 보인다」 같은 우회 인자가 생기고, 그 인자 하나가 공개 API 로 새면 남의 대화가
그대로 열린다. 층을 가르는 대신 **파일을 가른다** — 소유권을 보는 코드와 안 보는 코드가
섞이지 않게.

## 집계는 요청 시 계산한다

사전 집계 표를 두지 않는다(WORK-025 비목표 · spec §4 「데이터 규모가 작다」).
인사이트 한 번이 작은 쿼리 여섯 개다.

## 날짜는 KST

`daily` 30칸과 `last7d` 는 **같은 KST 날짜 경계**를 쓴다 — 그래서 「최근 7칸의 합 =
last7d」가 성립한다. 둘이 다른 기준(한쪽은 롤링 168시간)이면 화면에서 수치가 어긋나
보인다.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import NotFoundError
from dto.chat import (
    AdminConversationPageDTO,
    ChatInsightsDTO,
    ConversationBundle,
    DailyQuestionDTO,
)
from repository.chat_repo import ChatRepository, chat_repository
from schemas.chat import CODE_NOT_FOUND

_KST = ZoneInfo("Asia/Seoul")

# 위젯 3종의 크기 — spec §4 어드민 응답 계약에 박힌 수다.
RECENT_QUESTION_LIMIT = 20
DAILY_WINDOW_DAYS = 30
TOP_SOURCE_LIMIT = 5
LAST_N_DAYS = 7

# 목록 페이지 크기 — 기본 20, 상한은 한 화면이 감당할 만큼만.
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100


def _today_kst() -> date:
    return datetime.now(_KST).date()


class ChatAdminService:
    def __init__(self, repo: ChatRepository) -> None:
        self._repo = repo

    async def list_conversations(
        self, session: AsyncSession, *, page: int, size: int
    ) -> AdminConversationPageDTO:
        """최신순 한 페이지. 범위를 벗어난 page 는 빈 items 다 — 404 가 아니다."""
        items, total = await self._repo.list_conversations_page(
            session, limit=size, offset=(page - 1) * size
        )
        return AdminConversationPageDTO(items=items, total=total, page=page, size=size)

    async def get_conversation(
        self, session: AsyncSession, conversation_id: int
    ) -> ConversationBundle:
        """**소유 세션 무관** — admin 인증만이 문이다(§4). 없는 id 는 404."""
        conversation = await self._repo.get_conversation(session, conversation_id)
        if conversation is None:
            raise NotFoundError(CODE_NOT_FOUND)
        messages = await self._repo.list_messages(session, conversation_id)
        return ConversationBundle(conversation=conversation, messages=messages)

    async def insights(self, session: AsyncSession) -> ChatInsightsDTO:
        """위젯 3종의 원료 — totals · 최근 질문 · 일별 30일 · 근거 Top 5."""
        today = _today_kst()
        window_start = today - timedelta(days=DAILY_WINDOW_DAYS - 1)
        last_n_start = today - timedelta(days=LAST_N_DAYS - 1)

        return ChatInsightsDTO(
            conversations=await self._repo.count_conversations(session),
            questions=await self._repo.count_questions(session),
            last7d=await self._repo.count_questions(session, since_day=last_n_start),
            recent_questions=await self._repo.recent_questions(
                session, limit=RECENT_QUESTION_LIMIT
            ),
            daily=_fill_days(
                await self._repo.daily_questions(session, since_day=window_start),
                start=window_start,
                days=DAILY_WINDOW_DAYS,
            ),
            top_sources=await self._repo.top_sources(session, limit=TOP_SOURCE_LIMIT),
        )


def _fill_days(
    rows: list[DailyQuestionDTO], *, start: date, days: int
) -> list[DailyQuestionDTO]:
    """빈 날을 0 으로 채운 연속 구간(§4 「빈 날 0 포함」).

    차트는 칸의 **개수와 간격**이 곧 시간축이다 — 질문 없는 날이 빠지면 막대가 당겨져
    붙어 다른 날짜를 가리킨다.
    """
    counts = {row.day: row.count for row in rows}
    return [
        DailyQuestionDTO(day=start + timedelta(days=i), count=counts.get(start + timedelta(days=i), 0))
        for i in range(days)
    ]


chat_admin_service = ChatAdminService(chat_repository)

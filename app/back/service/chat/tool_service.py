"""chat-tool — 2층. MCP 서버가 부르는 조회와 어드민 노출 토글 (SPEC-017 §4 · DEC-027 D3·D4).

## 미노출과 없음을 구분하지 않는다

목록에서 빠지고 상세는 404 — AI 에게는 「존재하지 않는 문서」다(§3 S-9 1항). 합성 slug
파싱 실패도 같은 404 다(`core/chat_slugs.py` 머리 주석). 여기서 갈리면 id 를 훑어 원장
구조를 알아낼 수 있다.

## 상세 본문의 출처가 유형마다 다르다

`project` · `note` 는 원장 md(`detail_path`)를 읽고, `career` · `problem` 은 DB 컬럼이
곧 상세다(그 두 표는 원장 파일이 없다 — models 머리 주석). md 를 읽는 쪽은 공개 루트
밖이면 읽지 않는다(`core/chat_detail.py`).
"""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from core.chat_detail import read_public_detail
from core.chat_slugs import (
    TYPE_COMPANY_PRODUCT,
    TYPE_NOTE,
    TYPE_PROJECT,
    parse_career_slug,
    parse_problem_slug,
)
from core.exceptions import NotFoundError, ValidationError
from dto.chat_tool import ChatDocDTO, ChatProfileDTO
from repository.chat_tool_repo import (
    EXPOSED_KINDS,
    ChatToolRepository,
    chat_tool_repository,
)

# 상세를 못 찾았을 때의 단일 문구. **모든 경로가 이걸 쓴다** — 미노출·없음·파싱 실패가
# 같은 답이어야 존재 여부가 새지 않는다.
_NOT_FOUND = "NOT_FOUND"


class ChatToolService:
    def __init__(self, repo: ChatToolRepository) -> None:
        self._repo = repo

    # ── 어드민 토글 ─────────────────────────────────────
    async def set_exposure(
        self, session: AsyncSession, kind: str, item_id: int, value: bool
    ) -> bool:
        """`chat_exposed` 토글(U-7). 즉시 반영 — export · 캐시가 없다."""
        if kind not in EXPOSED_KINDS:
            raise ValidationError(
                f"chat_exposed 를 가진 유형이 아닙니다: {kind} "
                f"(가능: {', '.join(EXPOSED_KINDS)})"
            )
        result = await self._repo.set_chat_exposed(session, kind, item_id, value)
        if result is None:
            raise NotFoundError(f"{kind} not found: {item_id}")
        return result

    # ── 프로필 ──────────────────────────────────────────
    async def get_profile(self, session: AsyncSession) -> ChatProfileDTO:
        profile = await self._repo.get_profile(session)
        if profile is None:
            raise NotFoundError(_NOT_FOUND)
        return profile

    # ── 목록 ────────────────────────────────────────────
    async def list_careers(
        self, session: AsyncSession, limit: int | None = None
    ) -> list[ChatDocDTO]:
        return await self._repo.list_careers(session, limit=limit)

    async def list_projects(
        self, session: AsyncSession, limit: int | None = None
    ) -> list[ChatDocDTO]:
        return await self._repo.list_projects(session, limit=limit)

    async def list_problems(
        self, session: AsyncSession, limit: int | None = None
    ) -> list[ChatDocDTO]:
        return await self._repo.list_problems(session, limit=limit)

    async def list_company_products(
        self, session: AsyncSession, limit: int | None = None
    ) -> list[ChatDocDTO]:
        return await self._repo.list_company_products(session, limit=limit)

    async def search_notes(
        self, session: AsyncSession, query: str | None, limit: int | None = None
    ) -> list[ChatDocDTO]:
        return await self._repo.search_notes(session, query, limit=limit)

    async def list_contents(
        self, session: AsyncSession, limit: int | None = None
    ) -> list[ChatDocDTO]:
        return await self._repo.list_contents(session, limit=limit)

    async def list_algorithms(
        self, session: AsyncSession, limit: int | None = None
    ) -> list[ChatDocDTO]:
        return await self._repo.list_algorithms(session, limit=limit)

    # ── 상세 ────────────────────────────────────────────
    async def get_career(self, session: AsyncSession, slug: str) -> ChatDocDTO:
        career_id = parse_career_slug(slug)
        if career_id is None:
            raise NotFoundError(_NOT_FOUND)
        doc = await self._repo.get_career(session, career_id)
        return _require_canonical_slug(doc, slug)

    async def get_problem(self, session: AsyncSession, slug: str) -> ChatDocDTO:
        problem_id = parse_problem_slug(slug)
        if problem_id is None:
            raise NotFoundError(_NOT_FOUND)
        doc = await self._repo.get_problem(session, problem_id)
        return _require_canonical_slug(doc, slug)

    async def get_project(self, session: AsyncSession, slug: str) -> ChatDocDTO:
        found = await self._repo.get_project(session, slug)
        if found is None:
            raise NotFoundError(_NOT_FOUND)
        doc, detail_path = found
        return _with_body(doc, read_public_detail(TYPE_PROJECT, detail_path))

    async def get_company_product(self, session: AsyncSession, slug: str) -> ChatDocDTO:
        """회사 제품 상세 — showcase.md 만 읽는다.

        같은 제품 디렉토리의 `log/`(작업 회고) · README 는 공개 루트 밖이라 본문이
        비어 돌아온다(`core/chat_detail.py`) — 404 가 아니라 「요약까지만」이다.
        """
        found = await self._repo.get_company_product(session, slug)
        if found is None:
            raise NotFoundError(_NOT_FOUND)
        doc, detail_path = found
        return _with_body(doc, read_public_detail(TYPE_COMPANY_PRODUCT, detail_path))

    async def get_note(self, session: AsyncSession, slug: str) -> ChatDocDTO:
        found = await self._repo.get_note(session, slug)
        if found is None:
            raise NotFoundError(_NOT_FOUND)
        doc, detail_path = found
        return _with_body(doc, read_public_detail(TYPE_NOTE, detail_path))


def _require_canonical_slug(doc: ChatDocDTO | None, slug: str) -> ChatDocDTO:
    """복원한 행의 **정본 slug** 와 요청 slug 가 같아야 한다 — 합성 slug 공통 규약.

    합성 slug 는 꼬리의 id 만 실려 있어 앞부분이 달라도 같은 행에 닿는다
    (`problem-007` · `엉뚱한회사-3`). 그대로 200 을 주면 응답과 근거 카드의 slug 가
    요청과 다른 값으로 돌아와 **손잡이가 둘**이 된다. career 와 problem 이 같은
    규약을 쓰도록 이 함수 하나를 둘 다 거친다(리뷰 W4).

    미노출·없는 id 와 **같은 404** 다 — 존재 여부가 새지 않는다.
    """
    if doc is None or doc.slug != slug:
        raise NotFoundError(_NOT_FOUND)
    return doc


def _with_body(doc: ChatDocDTO, body: str | None) -> ChatDocDTO:
    """본문을 얹은 사본. md 가 끊겼거나 공개 루트 밖이면 body 는 None 이다 —
    404 로 만들지 않는다(행은 실재하고 요약은 줄 수 있다)."""
    return ChatDocDTO(
        type=doc.type,
        slug=doc.slug,
        title=doc.title,
        subtitle=doc.subtitle,
        summary=doc.summary,
        body=body,
        meta=doc.meta,
    )


chat_tool_service = ChatToolService(chat_tool_repository)

"""chat-tool 조회 — 3층. AI 가 보는 이력 데이터만 읽는다(read-only).

**기존 repository 를 고치지 않고 새로 둔 이유**: 기존 것들은 어드민·공개 표면의
계약을 갖고 있고, 거기에 `chat_exposed` 필터를 섞으면 두 표면의 판정이 한 쿼리에
얽힌다. 노출 경계는 이 파일 하나에서만 돈다 — 어디를 봐야 하는지가 분명해진다.

판정은 **매 호출 DB 에서** 한다(DEC-027 D4). 캐시·export 가 없어서 어드민 토글이
다음 tool 호출부터 그대로 먹는다.

## 판정식 — 「그 표면의 공개 조건 ∧ `chat_exposed`」 (spec v0.0.14 §4)

DEC-027 D3 의 「**공개 API 가 이미 보여 주는 것 = tool 이 보여 줄 수 있는 것의 상한**」이
식으로 내려온 것이다. 공개 표면에서 내린 항목이 chat 으로 새면 근거 카드가 404 페이지를
가리키게 된다 — 카드는 「실제로 읽은 것」이므로 그 링크는 살아 있어야 한다.

**유형별 공개 조건**(2026-08-28 감사 — 각 유형의 공개 API 를 직접 대조했다):

| 유형 | 공개 표면 | 공개 조건 | 여기의 판정 |
|---|---|---|---|
| career | `GET /api/career` (`career_repo.list_public`) | **없음** — 필터가 0건이다 | `chat_exposed` |
| problem | 위 번들 (`problem_repo.list_with_names`) | **없음** | `chat_exposed` |
| project | `GET /api/projects` (`project_service.get_public`) | `visible` | `visible ∧ chat_exposed` |
| product | 위 career 번들 (`career_service.get_public`) | `visible` | `visible ∧ chat_exposed` |
| note | `note_service._list_visible` | `visible` | `visible` |
| content | `content_repo.list_visible` | `visible` | `visible` |
| algorithm | `algorithm_service._list_visible` | `visible` | `visible` |

career·problem 에 공개 조건이 **없는 것은 누락이 아니다** — 그 두 표에는 visible 류 컬럼
자체가 없고 공개 API 도 전부 내려준다. 그러니 상한이 「전부」이고 `chat_exposed` 가 유일한
경계다. 나중에 그 표에 공개 플래그가 생기면 **여기 표와 아래 `_*_stmt` 를 함께** 고친다.

⚠ 이 표는 **공개 API 를 고칠 때 함께 보는 자리**다. 공개 표면에 조건이 하나 늘었는데
여기가 그대로면, 그 순간 tool 이 공개 API 보다 많이 보여 주게 된다.
"""

from __future__ import annotations

from datetime import date
from typing import Any

from sqlalchemy import Select, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.chat_slugs import (
    TYPE_ALGORITHM,
    TYPE_CAREER,
    TYPE_COMPANY_PRODUCT,
    TYPE_CONTENT,
    TYPE_NOTE,
    TYPE_PROBLEM,
    TYPE_PROJECT,
    career_slug,
    problem_slug,
)
from dto.chat_tool import ChatDocDTO, ChatProfileDTO
from models import (
    Algorithm,
    Career,
    Company,
    Content,
    Note,
    Problem,
    Product,
    Profile,
    Project,
)

# 목록 tool 의 기본·최대 반환 수. 상한을 두는 이유 = 목록 하나가 컨텍스트를 다 먹으면
# 모델이 상세를 읽을 여지가 사라진다.
DEFAULT_LIMIT = 30
MAX_LIMIT = 100


def _clamp(limit: int | None) -> int:
    if limit is None:
        return DEFAULT_LIMIT
    return max(1, min(int(limit), MAX_LIMIT))


def _period(started_on: date | None, ended_on: date | None) -> str | None:
    """`2026.02 — 현재` — 공개 career 표면과 같은 형식."""
    if started_on is None:
        return None
    until = "현재" if ended_on is None else f"{ended_on:%Y.%m}"
    return f"{started_on:%Y.%m} — {until}"


def _meta(**values: Any) -> dict[str, Any]:
    """None · 빈 값은 키 자체를 두지 않는다 — 「모른다」를 빈 문자열로 말하지 않는다."""
    return {k: v for k, v in values.items() if v not in (None, "", [], {})}


def _career_dto(career: Career, company: Company, *, body: str | None = None) -> ChatDocDTO:
    return ChatDocDTO(
        type=TYPE_CAREER,
        slug=career_slug(company.slug, career.id),
        title=career.title,
        subtitle=f"{company.name} · {_period(career.started_on, career.ended_on)}",
        summary=career.summary,
        body=body,
        meta=_meta(
            company=company.name,
            companyLocation=company.location,
            startedOn=career.started_on.isoformat() if career.started_on else None,
            endedOn=career.ended_on.isoformat() if career.ended_on else None,
            stack=list(career.stack or []),
        ),
    )


def _project_dto(row: Project, *, body: str | None = None) -> ChatDocDTO:
    return ChatDocDTO(
        type=TYPE_PROJECT,
        slug=row.slug,
        title=row.title,
        subtitle=row.category,
        summary=row.summary,
        body=body,
        meta=_meta(
            status=row.status,
            category=row.category,
            startedOn=row.started_on.isoformat() if row.started_on else None,
            stack=list(row.stack or []),
            links=row.links,
        ),
    )


def _product_dto(
    row: Product, career_title: str | None, company_name: str | None, *, body: str | None = None
) -> ChatDocDTO:
    """회사 제품 한 건. **어느 회사·어느 역할에서 만들었나**를 앞자리에 둔다 —
    채용담당자가 실제로 묻는 것이 그것이고, 모델이 개인 프로젝트와 헷갈리지 않게 한다."""
    subtitle = " · ".join(x for x in (company_name, career_title) if x) or None
    return ChatDocDTO(
        type=TYPE_COMPANY_PRODUCT,
        slug=row.slug,
        title=row.title,
        subtitle=subtitle,
        summary=row.summary,
        body=body,
        meta=_meta(
            company=company_name,
            role=career_title,
            status=row.status,
            category=row.category,
            startedOn=row.started_on.isoformat() if row.started_on else None,
            stack=list(row.stack or []),
        ),
    )


def _problem_dto(row: Problem, career_title: str | None, company_name: str | None) -> ChatDocDTO:
    subtitle = " · ".join(x for x in (company_name, career_title) if x) or None
    return ChatDocDTO(
        type=TYPE_PROBLEM,
        slug=problem_slug(row.id),
        title=row.title,
        subtitle=subtitle,
        # problem 은 상세가 md 가 아니라 DB 컬럼(body)이다 — 목록에서는 싣지 않는다.
        summary=None,
        meta=_meta(company=company_name, role=career_title),
    )


def _note_dto(row: Note, *, body: str | None = None) -> ChatDocDTO:
    return ChatDocDTO(
        type=TYPE_NOTE,
        slug=row.slug,
        title=row.title,
        subtitle=row.published_on.isoformat() if row.published_on else None,
        summary=row.summary,
        body=body,
        meta=_meta(tags=list(row.tags or [])),
    )


#: 어드민 토글이 손댈 수 있는 표 — `chat_exposed` 를 가진 넷뿐이다. 문자열을 그대로
#: 테이블 이름으로 쓰지 않고 이 표를 거치므로 `{kind}` 경로 인자로 아무 표나 못 건드린다.
#:
#: **키는 「문서 유형」이 아니라 「표 이름」이다.** 앞 셋은 두 이름이 우연히 같지만
#: 회사 제품은 갈린다 — 토글 대상은 `product` 표이고(FE `ChatExposureKind` 도 `product`),
#: 근거 카드의 유형은 `company_product` 다(spec v0.0.9). 그래서 여기만 상수가 아니라
#: 표 이름을 직접 쓴다 — `TYPE_COMPANY_PRODUCT` 를 쓰면 어드민 경로가 함께 바뀐다.
_EXPOSED_MODELS = {
    TYPE_CAREER: Career,
    TYPE_PROJECT: Project,
    TYPE_PROBLEM: Problem,
    "product": Product,
}

EXPOSED_KINDS = tuple(_EXPOSED_MODELS)


class ChatToolRepository:
    # ── 어드민 토글 (U-7) ───────────────────────────────
    async def set_chat_exposed(
        self, session: AsyncSession, kind: str, item_id: int, value: bool
    ) -> bool | None:
        """`chat_exposed` 를 세운다. 없는 행이면 None — 판단은 service 가 한다."""
        model = _EXPOSED_MODELS.get(kind)
        if model is None:
            return None
        row = await session.get(model, item_id)
        if row is None:
            return None
        row.chat_exposed = value
        await session.flush()
        return row.chat_exposed

    # ── profile ─────────────────────────────────────────
    async def get_profile(self, session: AsyncSession) -> ChatProfileDTO | None:
        row = (
            await session.execute(select(Profile).order_by(Profile.id.asc()).limit(1))
        ).scalar_one_or_none()
        if row is None:
            return None
        return ChatProfileDTO(
            name=row.name,
            role=row.role,
            years=row.years,
            location=row.location,
            focus=row.focus,
            email=row.email,
            stack=list(row.stack or []),
        )

    # ── career ──────────────────────────────────────────
    def _career_stmt(self) -> Select:
        """노출 승인된 역할만. `chat_exposed` 가 유일한 경계다(DEC-027 D4)."""
        return (
            select(Career, Company)
            .join(Company, Company.id == Career.company_id)
            .where(Career.chat_exposed.is_(True))
        )

    async def list_careers(
        self, session: AsyncSession, *, limit: int | None = None
    ) -> list[ChatDocDTO]:
        rows = (
            await session.execute(
                self._career_stmt()
                .order_by(Career.started_on.desc(), Career.id.desc())
                .limit(_clamp(limit))
            )
        ).all()
        return [_career_dto(career, company) for career, company in rows]

    async def get_career(
        self, session: AsyncSession, career_id: int
    ) -> ChatDocDTO | None:
        """미노출이면 None — 상세 tool 이 404 로 접는다. AI 에게는 없는 문서다."""
        row = (
            await session.execute(self._career_stmt().where(Career.id == career_id))
        ).one_or_none()
        if row is None:
            return None
        career, company = row
        # career 는 원장 md 가 없다 — 상세는 DB 의 description 이다(models/career.py).
        return _career_dto(career, company, body=career.description)

    # ── project ─────────────────────────────────────────
    def _project_stmt(self) -> Select:
        """`visible`(사이트 표면)과 `chat_exposed`(AI 노출)가 **둘 다** 켜져야 한다."""
        return select(Project).where(
            Project.visible.is_(True), Project.chat_exposed.is_(True)
        )

    async def list_projects(
        self, session: AsyncSession, *, limit: int | None = None
    ) -> list[ChatDocDTO]:
        rows = (
            (
                await session.execute(
                    self._project_stmt()
                    .order_by(Project.started_on.desc().nullslast(), Project.id.desc())
                    .limit(_clamp(limit))
                )
            )
            .scalars()
            .all()
        )
        return [_project_dto(row) for row in rows]

    async def get_project(
        self, session: AsyncSession, slug: str
    ) -> tuple[ChatDocDTO, str | None] | None:
        """`(dto, detail_path)` — md 를 읽는 것은 서비스다(파일은 3층의 일이 아니다).

        ORM 행을 밖으로 내보내지 않으려고 경로만 함께 준다 — 서비스가 공개 루트를
        확인하고 본문을 붙인다(`core/chat_detail.py`).
        """
        row = (
            await session.execute(self._project_stmt().where(Project.slug == slug))
        ).scalar_one_or_none()
        return (_project_dto(row), row.detail_path) if row else None

    # ── company product ─────────────────────────────────
    # **`product` 표는 전부 회사 제품이다** — 별도의 소속 구분 컬럼이 없다.
    # `career_id` 가 NOT NULL 이라 모든 행이 career → company 로 닿는다
    # (models/product.py: 「회사에서 만든 것 … career 에 속한다」). 개인 작업은
    # `project` 표로 갈린다. 그래서 여기서 거를 것은 노출 축뿐이다.
    def _product_stmt(self) -> Select:
        """`visible`(사이트 표면)과 `chat_exposed`(AI 노출)가 **둘 다** 켜져야 한다."""
        return (
            select(Product, Career.title, Company.name)
            .join(Career, Career.id == Product.career_id)
            .join(Company, Company.id == Career.company_id)
            .where(Product.visible.is_(True), Product.chat_exposed.is_(True))
        )

    async def list_company_products(
        self, session: AsyncSession, *, limit: int | None = None
    ) -> list[ChatDocDTO]:
        rows = (
            await session.execute(
                self._product_stmt()
                .order_by(Product.started_on.desc().nullslast(), Product.id.desc())
                .limit(_clamp(limit))
            )
        ).all()
        return [_product_dto(p, title, company) for p, title, company in rows]

    async def get_company_product(
        self, session: AsyncSession, slug: str
    ) -> tuple[ChatDocDTO, str | None] | None:
        """`(dto, detail_path)` — md 를 읽는 것은 서비스다(`get_project` 와 같은 규약)."""
        row = (
            await session.execute(self._product_stmt().where(Product.slug == slug))
        ).one_or_none()
        if row is None:
            return None
        product, career_title, company_name = row
        return _product_dto(product, career_title, company_name), product.detail_path

    # ── problem ─────────────────────────────────────────
    def _problem_stmt(self) -> Select:
        return (
            select(Problem, Career.title, Company.name)
            .join(Career, Career.id == Problem.career_id)
            .join(Company, Company.id == Career.company_id)
            .where(Problem.chat_exposed.is_(True))
        )

    async def list_problems(
        self, session: AsyncSession, *, limit: int | None = None
    ) -> list[ChatDocDTO]:
        rows = (
            await session.execute(
                self._problem_stmt()
                .order_by(Problem.display_order.asc(), Problem.id.asc())
                .limit(_clamp(limit))
            )
        ).all()
        return [_problem_dto(p, title, company) for p, title, company in rows]

    async def get_problem(
        self, session: AsyncSession, problem_id: int
    ) -> ChatDocDTO | None:
        row = (
            await session.execute(self._problem_stmt().where(Problem.id == problem_id))
        ).one_or_none()
        if row is None:
            return None
        problem, career_title, company_name = row
        dto = _problem_dto(problem, career_title, company_name)
        # problem 의 상세는 DB 컬럼(body)이다 — 원장 md 가 없다(models/problem.py).
        return ChatDocDTO(
            type=dto.type,
            slug=dto.slug,
            title=dto.title,
            subtitle=dto.subtitle,
            summary=dto.summary,
            body=problem.body,
            meta=dto.meta,
        )

    # ── note · content · algorithm ──────────────────────
    # 이 셋은 `chat_exposed` 축이 없다 — **이미 공개 페이지가 있는 표면**이라
    # `visible` 이 곧 공개 여부다(DEC-027 D3 「공개 학습노트」·「공개 목록」).
    async def search_notes(
        self, session: AsyncSession, query: str | None, *, limit: int | None = None
    ) -> list[ChatDocDTO]:
        stmt = select(Note).where(Note.visible.is_(True))
        text = (query or "").strip()
        if text:
            pattern = f"%{text}%"
            stmt = stmt.where(
                or_(
                    Note.title.ilike(pattern),
                    Note.summary.ilike(pattern),
                    # 태그는 배열이다 — 원소 하나라도 걸리면 잡는다.
                    Note.tags.any(text),
                )
            )
        rows = (
            (
                await session.execute(
                    stmt.order_by(
                        Note.published_on.desc().nullslast(), Note.id.desc()
                    ).limit(_clamp(limit))
                )
            )
            .scalars()
            .all()
        )
        return [_note_dto(row) for row in rows]

    async def get_note(
        self, session: AsyncSession, slug: str
    ) -> tuple[ChatDocDTO, str | None] | None:
        """`(dto, detail_path)` — `get_project` 와 같은 규약."""
        row = (
            await session.execute(
                select(Note).where(Note.visible.is_(True), Note.slug == slug)
            )
        ).scalar_one_or_none()
        return (_note_dto(row), row.detail_path) if row else None

    async def list_contents(
        self, session: AsyncSession, *, limit: int | None = None
    ) -> list[ChatDocDTO]:
        rows = (
            (
                await session.execute(
                    select(Content)
                    .where(Content.visible.is_(True))
                    .order_by(
                        Content.published_on.desc().nullslast(), Content.id.desc()
                    )
                    .limit(_clamp(limit))
                )
            )
            .scalars()
            .all()
        )
        return [
            ChatDocDTO(
                type=TYPE_CONTENT,
                slug=row.slug,
                title=row.title,
                subtitle=row.speaker,
                summary=row.summary,
                meta=_meta(duration=row.duration, tags=list(row.tags or [])),
            )
            for row in rows
        ]

    async def list_algorithms(
        self, session: AsyncSession, *, limit: int | None = None
    ) -> list[ChatDocDTO]:
        rows = (
            (
                await session.execute(
                    select(Algorithm)
                    .where(Algorithm.visible.is_(True))
                    .order_by(
                        Algorithm.published_on.desc().nullslast(), Algorithm.id.desc()
                    )
                    .limit(_clamp(limit))
                )
            )
            .scalars()
            .all()
        )
        return [
            ChatDocDTO(
                type=TYPE_ALGORITHM,
                slug=row.slug,
                title=row.title,
                subtitle=row.difficulty,
                summary=row.summary,
                meta=_meta(
                    difficulty=row.difficulty,
                    platform=row.source_platform,
                    tags=list(row.tags or []),
                ),
            )
            for row in rows
        ]


chat_tool_repository = ChatToolRepository()

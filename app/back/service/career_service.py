"""역할(career) — 2층."""

from __future__ import annotations

from datetime import date
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from core.detail import read_detail
from core.exceptions import ConflictError, NotFoundError, ValidationError
from dto.career import CareerDTO, PublicCareerBundle
from repository.career_repo import CareerRepository
from repository.company_repo import CompanyRepository
from repository.education_repo import EducationRepository
from repository.problem_repo import ProblemRepository
from repository.product_repo import ProductRepository
from repository.profile_repo import ProfileRepository

# DB 에서 NOT NULL — null 로 지우려는 요청은 여기서 막는다.
_NOT_NULLABLE = frozenset({"title", "started_on", "company_id"})


def _check_dates(started_on: date, ended_on: date | None) -> None:
    if ended_on is not None and ended_on < started_on:
        raise ValidationError("endedOn cannot be before startedOn")


class CareerService:
    def __init__(
        self,
        career_repo: CareerRepository,
        company_repo: CompanyRepository,
        profile_repo: ProfileRepository,
        product_repo: ProductRepository,
        problem_repo: ProblemRepository,
        education_repo: EducationRepository,
    ) -> None:
        self._career_repo = career_repo
        self._company_repo = company_repo
        self._profile_repo = profile_repo
        self._product_repo = product_repo
        self._problem_repo = problem_repo
        self._education_repo = education_repo

    async def _require_company(self, session: AsyncSession, company_id: int) -> None:
        if await self._company_repo.get_by_id(session, company_id) is None:
            raise NotFoundError(f"company not found: {company_id}")

    async def list_careers(self, session: AsyncSession) -> list[CareerDTO]:
        return await self._career_repo.list_with_company(session)

    async def get_public(self, session: AsyncSession) -> PublicCareerBundle:
        """공개 /career 한 벌 — 역할별 펼침(product 카드 · problem)까지 조립한다.

        visible=false 인 제품은 여기서 걸러진다 — 응답에 visible 필드는 없다
        (erd §미결 3 의 확정: 공개 API 가 걸러서 내려준다).
        """
        careers = await self._career_repo.list_public(session)

        products_by_career: dict[int, list] = {}
        for p in await self._product_repo.list_with_career(session):
            if p.visible:
                products_by_career.setdefault(p.career_id, []).append(p)

        problems_by_career: dict[int, list] = {}
        for pr in await self._problem_repo.list_with_names(session):
            problems_by_career.setdefault(pr.career_id, []).append(pr)

        education = await self._education_repo.list_all(session)
        # 상세는 md — detail_path 를 읽어 본문으로 내려준다(core/detail.py).
        education_bodies: dict[int, str] = {}
        for e in education:
            body = read_detail(e.detail_path)
            if body is not None:
                education_bodies[e.id] = body

        profile = await self._profile_repo.get_first(session)
        return PublicCareerBundle(
            careers=careers,
            products_by_career=products_by_career,
            problems_by_career=problems_by_career,
            education=education,
            education_bodies=education_bodies,
            total_years=profile.years if profile else None,
            focus=profile.focus if profile else None,
        )

    async def create(self, session: AsyncSession, fields: dict[str, Any]) -> CareerDTO:
        _check_dates(fields["started_on"], fields.get("ended_on"))
        await self._require_company(session, fields["company_id"])
        # profile_id 는 클라이언트가 정하지 않는다 — 1인 사이트라 첫 행이 곧 프로필이다.
        profile = await self._profile_repo.get_first(session)
        if profile is None:
            raise NotFoundError("profile not found")
        return await self._career_repo.create(
            session, {**fields, "profile_id": profile.id}
        )

    async def update(
        self, session: AsyncSession, career_id: int, fields: dict[str, Any]
    ) -> CareerDTO:
        for name in _NOT_NULLABLE & fields.keys():
            if fields[name] is None:
                raise ValidationError(f"{name} cannot be null")
        if "company_id" in fields:
            await self._require_company(session, fields["company_id"])
        # 날짜 일관성 — 한쪽만 바뀌어도 합쳐서 본다. 기존 행이 없으면 404.
        if "started_on" in fields or "ended_on" in fields:
            current = await self._career_repo.get(session, career_id)
            if current is None:
                raise NotFoundError(f"career not found: {career_id}")
            _check_dates(
                fields.get("started_on", current.started_on),
                fields.get("ended_on", current.ended_on),
            )
        dto = await self._career_repo.update(session, career_id, fields)
        if dto is None:
            raise NotFoundError(f"career not found: {career_id}")
        return dto

    async def delete(self, session: AsyncSession, career_id: int) -> None:
        """제품이 붙어 있으면 지우지 않는다 — FK CASCADE 가 제품까지 쓸어간다.

        company_service 의 career 가드와 같은 패턴.
        """
        count = await self._career_repo.product_count(session, career_id)
        if count > 0:
            raise ConflictError(
                f"제품 {count}개가 이 역할에 있습니다 — 제품을 먼저 옮기거나 지우세요"
            )
        problem_count = await self._career_repo.problem_count(session, career_id)
        if problem_count > 0:
            raise ConflictError(
                f"문제 {problem_count}개가 이 역할에 있습니다 — 문제를 먼저 지우세요"
            )
        if not await self._career_repo.delete(session, career_id):
            raise NotFoundError(f"career not found: {career_id}")


career_service = CareerService(
    CareerRepository(),
    CompanyRepository(),
    ProfileRepository(),
    ProductRepository(),
    ProblemRepository(),
    EducationRepository(),
)

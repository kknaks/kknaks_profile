"""GitHub 조회 — 2층. 레포 연결 모달의 owner 후보와 레포 목록.

스코프가 핵심이다(이직 대비 — 새 회사 제품 폼에 옛 회사 레포가 안 뜬다):
- product 폼: product → career → company 사슬로 회사를 판정하고, **그 회사 것만** —
  company.github_org(있으면) + 그 회사에 연결된(git_token.company_id) company 토큰의 account.
- project 폼: personal 토큰의 account 만.

owner 가 토큰을 데리고 온다 — 후보마다 token_id 가 딸려 오고, 레포 조회·저장이
그 토큰을 쓴다. GitHub 실패는 도메인 예외(422) — 화면이 메시지를 그대로 띄운다.
"""

from __future__ import annotations

import re

import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from core.crypto import decrypt_token
from core.exceptions import NotFoundError, ValidationError
from dto.github import GithubOwnerDTO, GithubRepoDTO
from repository.career_repo import CareerRepository
from repository.company_repo import CompanyRepository
from repository.git_token_repo import GitTokenRepository
from repository.product_repo import ProductRepository
from repository.project_repo import ProjectRepository

_API = "https://api.github.com"
_PER_PAGE = 100
_MAX_PAGES = 3            # 모달 목록용 — 최근 갱신순 300개면 충분하다

# GitHub owner — 슬래시 없는 한 조각.
_OWNER_RE = re.compile(r"^[A-Za-z0-9_.-]+$")


class GithubService:
    def __init__(
        self,
        product_repo: ProductRepository,
        project_repo: ProjectRepository,
        career_repo: CareerRepository,
        company_repo: CompanyRepository,
        git_token_repo: GitTokenRepository,
    ) -> None:
        self._product_repo = product_repo
        self._project_repo = project_repo
        self._career_repo = career_repo
        self._company_repo = company_repo
        self._git_token_repo = git_token_repo

    # ── owner 후보 ──────────────────────────────────────────────────────
    async def list_owners(
        self,
        session: AsyncSession,
        product_id: int | None,
        project_id: int | None,
    ) -> list[GithubOwnerDTO]:
        """폼의 소속(product/project 둘 중 정확히 하나)에 맞는 owner 후보."""
        if (product_id is None) == (project_id is None):
            raise ValidationError(
                "product_id / project_id 둘 중 정확히 하나를 보내야 합니다"
            )
        if product_id is not None:
            return await self._company_owners(session, product_id)
        assert project_id is not None
        return await self._personal_owners(session, project_id)

    async def _company_owners(
        self, session: AsyncSession, product_id: int
    ) -> list[GithubOwnerDTO]:
        """product → career → company 사슬 — **그 회사 것만** 내려간다."""
        product = await self._product_repo.get(session, product_id)
        if product is None:
            raise NotFoundError(f"product not found: {product_id}")
        career = await self._career_repo.get(session, product.career_id)
        assert career is not None  # FK — product 가 있으면 career 도 있다
        company = await self._company_repo.get_by_id(session, career.company_id)
        assert company is not None  # FK

        # 그 회사에 연결된 enabled company 토큰만 — 다른 회사·개인 토큰은 후보가 아니다.
        tokens = [
            t
            for t in await self._git_token_repo.list_all(session)
            if t.kind == "company" and t.company_id == company.id and t.enabled
        ]
        items: list[GithubOwnerDTO] = []
        if company.github_org:
            # org 의 조회 토큰 — 그 회사 토큰 중 첫 번째. 없으면 무토큰(공개만).
            items.append(
                GithubOwnerDTO(
                    owner=company.github_org,
                    label=f"{company.github_org} — 회사 조직",
                    source="org",
                    token_id=tokens[0].id if tokens else None,
                )
            )
        for t in tokens:
            items.append(
                GithubOwnerDTO(
                    owner=t.account,
                    label=f"{t.account} — 회사 계정",
                    source="account",
                    token_id=t.id,
                )
            )
        return _dedupe(items)

    async def _personal_owners(
        self, session: AsyncSession, project_id: int
    ) -> list[GithubOwnerDTO]:
        """개인 프로젝트 폼 — personal 토큰의 account 만. 회사 것은 절대 안 뜬다."""
        if await self._project_repo.get(session, project_id) is None:
            raise NotFoundError(f"project not found: {project_id}")
        items = [
            GithubOwnerDTO(
                owner=t.account,
                label=f"{t.account} — 개인 계정",
                source="account",
                token_id=t.id,
            )
            for t in await self._git_token_repo.list_all(session)
            if t.kind == "personal" and t.enabled
        ]
        return _dedupe(items)

    # ── 레포 목록 ───────────────────────────────────────────────────────
    async def list_repos(
        self, session: AsyncSession, owner: str, token_id: int | None
    ) -> list[GithubRepoDTO]:
        """GitHub 에서 owner 의 레포 — /orgs 먼저, 404 면 /users 폴백. 최근 갱신순."""
        owner = owner.strip()
        if not _OWNER_RE.match(owner):
            raise ValidationError(f"owner 형식이 아닙니다: {owner!r}")
        token = None
        if token_id is not None:
            cipher = await self._git_token_repo.get_cipher(session, token_id)
            if cipher is None:
                raise NotFoundError(f"git_token not found: {token_id}")
            token = decrypt_token(cipher)

        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if token:
            headers["Authorization"] = f"Bearer {token}"
        async with httpx.AsyncClient(headers=headers, timeout=30.0) as client:
            rows = await self._fetch_pages(client, f"/orgs/{owner}/repos")
            if rows is None:  # org 가 아니다 — 사용자 계정으로 폴백
                rows = await self._fetch_pages(client, f"/users/{owner}/repos")
            if rows is None:
                raise ValidationError(f"GitHub 에 없는 owner 입니다: {owner}")
        return [
            GithubRepoDTO(
                slug=r["full_name"],
                name=r["name"],
                private=bool(r.get("private")),
                updated_at=r.get("updated_at"),
            )
            for r in rows
        ]

    async def _fetch_pages(
        self, client: httpx.AsyncClient, path: str
    ) -> list[dict] | None:
        """pagination — 최대 3페이지. 404 는 None(폴백 신호), 그 외 실패는 422."""
        params = {"per_page": _PER_PAGE, "sort": "updated", "direction": "desc"}
        rows: list[dict] = []
        for page in range(1, _MAX_PAGES + 1):
            res = await client.get(f"{_API}{path}", params={**params, "page": page})
            if res.status_code == 404:
                return None if page == 1 else rows
            if res.status_code != 200:
                detail = ""
                try:
                    detail = res.json().get("message", "")
                except Exception:
                    pass
                raise ValidationError(
                    f"GitHub {res.status_code} — {detail or res.text[:200]}"
                )
            batch = res.json()
            rows.extend(batch)
            if len(batch) < _PER_PAGE:
                break
        return rows


def _dedupe(items: list[GithubOwnerDTO]) -> list[GithubOwnerDTO]:
    """같은 owner 가 org·account 양쪽에서 오면 앞(org)을 남긴다."""
    seen: set[str] = set()
    out: list[GithubOwnerDTO] = []
    for item in items:
        if item.owner in seen:
            continue
        seen.add(item.owner)
        out.append(item)
    return out


github_service = GithubService(
    ProductRepository(),
    ProjectRepository(),
    CareerRepository(),
    CompanyRepository(),
    GitTokenRepository(),
)

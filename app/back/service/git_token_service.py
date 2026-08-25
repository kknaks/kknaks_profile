"""git_token — 2층. 토큰 등록·교체·삭제. 원문은 등록 순간에만 만지고 즉시 암호화한다."""

from __future__ import annotations

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from core.crypto import encrypt_token
from core.exceptions import NotFoundError, ValidationError
from dto.git_token import GitTokenDTO
from repository.company_repo import CompanyRepository
from repository.git_token_repo import GitTokenRepository

_KINDS = {"personal", "company"}


class GitTokenService:
    def __init__(
        self, repo: GitTokenRepository, company_repo: CompanyRepository
    ) -> None:
        self._repo = repo
        self._company_repo = company_repo

    async def list_tokens(self, session: AsyncSession) -> list[GitTokenDTO]:
        return await self._repo.list_all(session)

    async def _check_company(self, session: AsyncSession, company_id: int) -> None:
        if await self._company_repo.get_by_id(session, company_id) is None:
            raise ValidationError(f"없는 회사입니다: {company_id}")

    async def create(
        self,
        session: AsyncSession,
        kind: str,
        account: str,
        email: str,
        token: str,
        company_id: int | None = None,
    ) -> GitTokenDTO:
        if kind not in _KINDS:
            raise ValidationError(f"구분은 personal/company 중 하나여야 합니다: {kind!r}")
        account = account.strip()
        if not account:
            raise ValidationError("계정 id 를 입력하세요")
        email = email.strip()
        if not email:
            raise ValidationError("email 을 입력하세요")
        token = token.strip()
        if not token:
            raise ValidationError("토큰을 입력하세요")
        # 소속 — company 토큰은 회사 필수, personal 은 보내와도 None 으로 접는다.
        if kind == "company":
            if company_id is None:
                raise ValidationError("회사를 선택하세요")
            await self._check_company(session, company_id)
        else:
            company_id = None
        return await self._repo.create(
            session, kind, account, email, encrypt_token(token), company_id
        )

    async def replace(self, session: AsyncSession, token_id: int, token: str) -> None:
        """토큰 교체 — 이직·만료 갱신. 행(연결)은 유지되고 값만 바뀐다."""
        token = token.strip()
        if not token:
            raise ValidationError("토큰을 입력하세요")
        if not await self._repo.replace_cipher(session, token_id, encrypt_token(token)):
            raise NotFoundError(f"git_token not found: {token_id}")

    async def update(
        self, session: AsyncSession, token_id: int, fields: dict[str, Any]
    ) -> GitTokenDTO:
        """부분 수정 — enabled · company_id. 검증은 **이번 요청에 온 필드**만 —
        기존 company 행이 미연결(NULL)이어도 enabled 토글은 막히지 않는다."""
        current = await self._repo.get(session, token_id)
        if current is None:
            raise NotFoundError(f"git_token not found: {token_id}")
        if "enabled" in fields and fields["enabled"] is None:
            raise ValidationError("enabled cannot be null")
        if "company_id" in fields:
            if current.kind != "company":
                fields["company_id"] = None  # personal 은 소속이 없다 — None 으로 접는다
            elif fields["company_id"] is not None:
                await self._check_company(session, fields["company_id"])
            # company 인데 null — 해제. 기존 행이 NULL 인 것과 같은 상태라 허용.
        dto = await self._repo.update(session, token_id, fields)
        assert dto is not None  # 방금 존재를 확인했다
        return dto

    async def delete(self, session: AsyncSession, token_id: int) -> None:
        """삭제 — 붙어 있던 repo 는 FK SET NULL 로 무토큰이 된다."""
        if not await self._repo.delete(session, token_id):
            raise NotFoundError(f"git_token not found: {token_id}")


git_token_service = GitTokenService(GitTokenRepository(), CompanyRepository())

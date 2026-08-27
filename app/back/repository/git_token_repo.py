"""git_token — 3층. 암호문은 여기서만 읽는다(수집기용 cipher_map)."""

from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dto.git_token import GitTokenDTO
from models.company import Company
from models.git_token import GitToken


def _to_dto(row: GitToken, company_name: str | None) -> GitTokenDTO:
    return GitTokenDTO(
        id=row.id,
        kind=row.kind,
        account=row.account,
        email=row.email,
        company_id=row.company_id,
        company_name=company_name,
        enabled=row.enabled,
        created_at=row.created_at,
    )


# company 는 kind=company 에만 붙어 outer join — 없는 쪽은 NULL 로 온다.
_JOINED = select(GitToken, Company.name).outerjoin(
    Company, Company.id == GitToken.company_id
)


class GitTokenRepository:
    async def list_all(self, session: AsyncSession) -> list[GitTokenDTO]:
        rows = (await session.execute(_JOINED.order_by(GitToken.id))).all()
        return [_to_dto(token, name) for token, name in rows]

    async def get(self, session: AsyncSession, token_id: int) -> GitTokenDTO | None:
        row = (
            await session.execute(_JOINED.where(GitToken.id == token_id))
        ).one_or_none()
        return _to_dto(row[0], row[1]) if row else None

    async def create(
        self,
        session: AsyncSession,
        kind: str,
        account: str,
        email: str,
        token_cipher: str,
        company_id: int | None,
    ) -> GitTokenDTO:
        row = GitToken(
            kind=kind,
            account=account,
            email=email,
            token_cipher=token_cipher,
            company_id=company_id,
        )
        session.add(row)
        await session.flush()
        dto = await self.get(session, row.id)
        assert dto is not None  # 방금 넣었다
        return dto

    async def replace_cipher(
        self, session: AsyncSession, token_id: int, token_cipher: str
    ) -> bool:
        row = await session.get(GitToken, token_id)
        if row is None:
            return False
        row.token_cipher = token_cipher
        await session.flush()
        return True

    async def update(
        self, session: AsyncSession, token_id: int, fields: dict[str, Any]
    ) -> GitTokenDTO | None:
        """보낸 필드만 얹는다 — PATCH 시맨틱. 없는 id 면 None, 판단은 service."""
        row = await session.get(GitToken, token_id)
        if row is None:
            return None
        for name, value in fields.items():
            setattr(row, name, value)
        await session.flush()
        return await self.get(session, token_id)

    async def delete(self, session: AsyncSession, token_id: int) -> bool:
        row = await session.get(GitToken, token_id)
        if row is None:
            return False
        await session.delete(row)
        await session.flush()
        return True

    async def get_cipher(self, session: AsyncSession, token_id: int) -> str | None:
        """행 하나의 암호문 — GitHub 조회(레포 연결 모달)용. 복호는 호출부가 한다.

        enabled 를 안 본다 — 수집(cipher_map)과 달리 사람이 그 자리에서 고른
        토큰이라, 꺼진 토큰이어도 조회에는 그대로 쓴다.
        """
        row = await session.get(GitToken, token_id)
        return row.token_cipher if row else None

    async def get_personal_with_cipher(
        self, session: AsyncSession
    ) -> tuple[GitTokenDTO, str] | None:
        """personal 행 하나 — 착지 커밋 신원(account·email) + push 자격(암호문).

        enabled 를 안 본다 — 수집 제외 토글이지 착지 신원을 끄는 스위치가 아니다.
        복호는 호출부(core/crypto)가 한다. 없으면 None — service 가 422 로 바꾼다.
        """
        row = (
            await session.scalars(
                select(GitToken)
                .where(GitToken.kind == "personal")
                .order_by(GitToken.id)
                .limit(1)
            )
        ).first()
        if row is None:
            return None
        return _to_dto(row, None), row.token_cipher  # personal 은 소속이 없다

    async def cipher_map(self, session: AsyncSession) -> dict[int, str]:
        """수집기용 — {id: 암호문}. 복호는 호출부(core/crypto)가 한다.

        **비활성(enabled=false) 행은 제외한다** — 수집기는 map 에 없는 id 를
        무토큰으로 취급하므로, 끈 토큰이 붙은 레포는 공개 범위만 읽힌다.
        """
        rows = (await session.scalars(select(GitToken).where(GitToken.enabled))).all()
        return {r.id: r.token_cipher for r in rows}

"""노트(note) — 2층.

케이스 4 (case_flow.md): **공개는 선택이다.** 글을 쓴다고 사이트에 뜨지 않는다 —
원장은 para/resources/note/ 의 md 이고, 어드민이 파일을 골라 등록해야 뜬다.
그래서 시드가 없고, detail_path 는 그 디렉토리 하위의 **실존 파일**이어야 한다.
md 파일은 읽기만 한다 — 등록/해제가 파일을 만들거나 지우지 않는다.
"""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from config import get_settings
from core.detail import read_detail
from core.exceptions import ConflictError, NotFoundError, ValidationError
from dto.note import (
    NoteDTO,
    NoteFileDTO,
    NoteNeighbor,
    PublicNoteDetail,
    PublicNoteList,
)
from repository.note_repo import NoteRepository
from repository.profile_repo import ProfileRepository

# DB 에서 NOT NULL — null 로 지우려는 요청은 여기서 막는다.
# profile_id 는 입력받지 않는다 — 서버가 첫 profile 로 채운다.
_NOT_NULLABLE = frozenset({"slug", "title", "detail_path", "visible"})

# 리포 루트 기준 — 노트 md 원장이 사는 곳.
_NOTE_DIR = ("para", "resources", "note")
_NOTE_PREFIX = "/".join(_NOTE_DIR) + "/"


def _require_note_file(detail_path: str) -> None:
    """detail_path 검사 — para/resources/note/ 하위의 실존 md 파일이어야 한다.

    경로 조립이라 탈출 문자를 먼저 막는다 (`..` · 절대경로 · 역슬래시 → 422).
    """
    if ".." in detail_path or "\\" in detail_path or detail_path.startswith("/"):
        raise ValidationError(f"detail_path 에 경로 탈출 문자를 쓸 수 없습니다: {detail_path}")
    if not detail_path.startswith(_NOTE_PREFIX):
        raise ValidationError(
            f"detail_path 는 {_NOTE_PREFIX} 하위여야 합니다: {detail_path}"
        )
    target = Path(get_settings().repo_root) / detail_path
    if target.suffix != ".md" or not target.is_file():
        raise ValidationError(
            f"파일이 없습니다 — 원장이 먼저, 등록이 나중입니다 (케이스 4): {detail_path}"
        )


# ── frontmatter — 첫 `---` 블록만 읽는 간단 파서 ─────────────────────────────
# 원장 144건이 전부 같은 모양이라 yaml 라이브러리 없이 세 가지만 다룬다:
# `key: value` 스칼라 · `key: [a, b]` 인라인 리스트 · `key:` + `  - a` 블록 리스트.

_KEY_RE = re.compile(r"^([A-Za-z_][\w-]*):\s*(.*)$")
_ITEM_RE = re.compile(r"^\s+-\s*(.+)$")


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
        return value[1:-1]
    return value


def _parse_frontmatter(text: str) -> dict[str, Any]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    data: dict[str, Any] = {}
    list_key: str | None = None
    for line in lines[1:]:
        if line.strip() == "---":
            break
        match = _KEY_RE.match(line)
        if match:
            key, raw = match.group(1), match.group(2).strip()
            if raw == "":
                data[key] = []
                list_key = key
                continue
            list_key = None
            if raw.startswith("[") and raw.endswith("]"):
                inner = raw[1:-1].strip()
                data[key] = (
                    [_unquote(v) for v in inner.split(",") if v.strip()] if inner else []
                )
            else:
                data[key] = _unquote(raw)
            continue
        item = _ITEM_RE.match(line)
        if item and list_key is not None:
            data[list_key].append(_unquote(item.group(1)))
    return data


def _parse_fm_date(raw: Any) -> date | None:
    """frontmatter date — `2024.10.17` 과 `2024-10-17` 둘 다 받는다."""
    if not isinstance(raw, str):
        return None
    parts = re.split(r"[.\-/]", raw.strip())
    if len(parts) != 3:
        return None
    try:
        return date(int(parts[0]), int(parts[1]), int(parts[2]))
    except ValueError:
        return None


class NoteService:
    def __init__(
        self, note_repo: NoteRepository, profile_repo: ProfileRepository
    ) -> None:
        self._note_repo = note_repo
        self._profile_repo = profile_repo

    async def _require_free_slug(
        self, session: AsyncSession, slug: str, exclude_id: int | None = None
    ) -> None:
        existing = await self._note_repo.get_by_slug(session, slug)
        if existing and existing.id != exclude_id:
            raise ConflictError(f"slug already exists: {slug}")

    async def list_notes(self, session: AsyncSession) -> list[NoteDTO]:
        return await self._note_repo.list_all(session)

    async def _list_visible(self, session: AsyncSession) -> list[NoteDTO]:
        """공개 목록의 원천 — published_on DESC NULLS LAST(repo 정렬) 에서 visible 만.

        visible=false 는 여기서 걸러진다 — 응답에 visible 필드는 없다
        (erd §미결 3 의 확정: 공개 API 가 걸러서 내려준다).
        """
        return [n for n in await self._note_repo.list_all(session) if n.visible]

    async def get_public(self, session: AsyncSession, limit: int) -> PublicNoteList:
        """공개 /notes 목록 — 앞에서 limit 개. total_count 는 자르기 전 전체 수."""
        visible = await self._list_visible(session)
        return PublicNoteList(items=visible[:limit], total_count=len(visible))

    async def get_public_detail(
        self, session: AsyncSession, slug: str
    ) -> PublicNoteDetail:
        """공개 상세 한 벌 — md 전문 + 이웃.

        이웃(newer/older)은 컬럼이 아니라 published_on 정렬의 이웃이다(erd.md).
        없는 slug 도, visible=false 도 같은 404 다 — 숨긴 글의 존재를 드러내지 않는다.
        detail_path 가 끊기면 상세 없음 — 빈 본문으로 그린다(_RESUME.md §4).
        """
        visible = await self._list_visible(session)
        idx = next((i for i, n in enumerate(visible) if n.slug == slug), None)
        if idx is None:
            raise NotFoundError(f"note not found: {slug}")
        dto = visible[idx]
        newer = visible[idx - 1] if idx > 0 else None
        older = visible[idx + 1] if idx + 1 < len(visible) else None
        return PublicNoteDetail(
            dto=dto,
            body=read_detail(dto.detail_path) or "",
            newer=NoteNeighbor(slug=newer.slug, title=newer.title) if newer else None,
            older=NoteNeighbor(slug=older.slug, title=older.title) if older else None,
        )

    async def list_file_candidates(self, session: AsyncSession) -> list[NoteFileDTO]:
        """등록 후보 — para/resources/note/ 재귀의 *.md 중 아직 등록 안 된 것.

        frontmatter 의 title·summary·date·tags 를 담아 내려준다 — 폼 프리필용.
        읽기만 한다. date DESC NULLS LAST 로 최근 글이 위로 온다.
        """
        registered = await self._note_repo.list_detail_paths(session)
        root = Path(get_settings().repo_root)
        note_dir = root.joinpath(*_NOTE_DIR)
        items: list[NoteFileDTO] = []
        for md in note_dir.rglob("*.md"):
            rel = md.relative_to(root).as_posix()
            if rel in registered:
                continue
            try:
                fm = _parse_frontmatter(md.read_text(encoding="utf-8"))
            except (OSError, UnicodeDecodeError):
                fm = {}
            tags = fm.get("tags")
            items.append(
                NoteFileDTO(
                    path=rel,
                    stem=md.stem,
                    title=fm.get("title") if isinstance(fm.get("title"), str) else None,
                    summary=fm.get("summary")
                    if isinstance(fm.get("summary"), str)
                    else None,
                    date=_parse_fm_date(fm.get("date")),
                    tags=tags if isinstance(tags, list) and tags else None,
                )
            )
        # 안정 정렬 2단 — path ASC 를 깔고 date DESC 를 얹는다. None 은 min 이라 맨 뒤.
        items.sort(key=lambda i: i.path)
        items.sort(key=lambda i: i.date or date.min, reverse=True)
        return items

    async def create(self, session: AsyncSession, fields: dict[str, Any]) -> NoteDTO:
        _require_note_file(fields["detail_path"])
        await self._require_free_slug(session, fields["slug"])

        profile = await self._profile_repo.get_first(session)
        if profile is None:
            raise NotFoundError("profile not found — seed_profile 을 먼저 돌린다")
        fields["profile_id"] = profile.id
        return await self._note_repo.create(session, fields)

    async def update(
        self, session: AsyncSession, note_id: int, fields: dict[str, Any]
    ) -> NoteDTO:
        for name in _NOT_NULLABLE & fields.keys():
            if fields[name] is None:
                raise ValidationError(f"{name} cannot be null")
        if "detail_path" in fields:
            # 다른 파일을 가리키는 것도 같은 검사를 거친다 — 실존 md 만 등록된다.
            _require_note_file(fields["detail_path"])
        if "slug" in fields:
            await self._require_free_slug(session, fields["slug"], exclude_id=note_id)
        dto = await self._note_repo.update(session, note_id, fields)
        if dto is None:
            raise NotFoundError(f"note not found: {note_id}")
        return dto

    async def delete(self, session: AsyncSession, note_id: int) -> None:
        """등록 해제일 뿐이다 — md 파일은 건드리지 않으므로 가드가 없다."""
        if not await self._note_repo.delete(session, note_id):
            raise NotFoundError(f"note not found: {note_id}")


note_service = NoteService(NoteRepository(), ProfileRepository())

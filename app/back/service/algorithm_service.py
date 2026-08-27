"""알고리즘(algorithm) — 2층.

원장은 para/resources/algorithms/ 의 md 파일이다 — detail_path 가 실존
파일을 가리키지 않으면 등록·수정이 422 로 막힌다(md 가 먼저, DB 가 나중).

「오늘의 문제」는 하나뿐이다. today=true 로 올리는 요청은 **한 트랜잭션에서**
기존 today 행을 먼저 내리고 이 행을 올린다 — DB 의 partial unique index
(uq_algorithm_today) 가 최종 방어다.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml
from sqlalchemy.ext.asyncio import AsyncSession

from config import get_settings
from core.detail import read_detail
from core.exceptions import ConflictError, NotFoundError, ValidationError
from dto.algorithm import (
    AlgorithmDTO,
    AlgorithmNeighbor,
    PublicAlgorithmDetail,
    PublicAlgorithmList,
)
from repository.algorithm_repo import AlgorithmRepository
from repository.profile_repo import ProfileRepository

# DB 에서 NOT NULL — null 로 지우려는 요청은 여기서 막는다.
# profile_id 는 입력받지 않는다 — 서버가 첫 profile 로 채운다.
_NOT_NULLABLE = frozenset(
    {"slug", "title", "difficulty", "source_platform", "today", "detail_path", "visible"}
)

_DIFFICULTIES = frozenset({"easy", "medium", "hard"})

# 리포 루트 기준 — 알고리즘 md 원장이 사는 곳.
_ALGORITHMS_DIR = ("para", "resources", "algorithms")


def _require_difficulty(value: str) -> None:
    if value not in _DIFFICULTIES:
        raise ValidationError(
            f"difficulty 는 easy·medium·hard 중 하나여야 합니다: {value}"
        )


def _require_detail_file(detail_path: str) -> None:
    """detail_path 검사 — para/resources/algorithms/ 하위 실존 파일이어야 한다.

    경로 조립이라 탈출을 먼저 막는다 — `..`·역슬래시·절대경로는 422.
    """
    prefix = "/".join(_ALGORITHMS_DIR) + "/"
    if "\\" in detail_path or ".." in detail_path or detail_path.startswith("/"):
        raise ValidationError(f"detail_path 에 경로 탈출 문자를 쓸 수 없습니다: {detail_path}")
    if not detail_path.startswith(prefix):
        raise ValidationError(
            f"detail_path 는 {prefix} 하위여야 합니다: {detail_path}"
        )
    full = Path(get_settings().repo_root) / detail_path
    if not full.is_file():
        raise ValidationError(
            f"detail_path 가 가리키는 md 가 없습니다 — 원장이 먼저입니다: {detail_path}"
        )


# ── 공개 상세 — md 의 `## Data` fenced yaml 을 계약 모양으로 정규화 ──────────
#
# 단계 구조(Problem → Clarifying → Approach → Logic → Trace → Solution)는
# **컬럼이 아니다** — md 본문의 `## Data` fenced yaml 이 갖는다(erd.md §algorithm).
# 원장 yaml 은 표면 문자열을 {ko, en} 이중 축으로 갖는데 표면은 한국어 하나다
# (database.md 서두) — 여기서 ko 로 접는다(없으면 en). 프론트는 접힌 값을 그대로
# 그린다(lib/types.ts AlgorithmDetail).
#
# yaml 이 없거나 깨져도 500 을 내지 않는다 — 단계별 빈 구조로 내려서 컴포넌트의
# 빈 상태 문구(「LLM 이 아직 …」)가 그리게 둔다.

_DATA_YAML = re.compile(r"^##\s*Data\s*\n+```yaml\n(.*?)\n```", re.MULTILINE | re.DOTALL)


def _ko(value: Any) -> str:
    """{ko, en} 이중 축을 한국어 하나로 접는다. 이미 문자열이면 그대로."""
    if isinstance(value, dict):
        for key in ("ko", "en"):
            v = value.get(key)
            if isinstance(v, str) and v.strip():
                return v
        return ""
    return value if isinstance(value, str) else ""


def _str_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [v for v in value if isinstance(v, str)]


def _ko_list(value: Any) -> list[str]:
    """{ko, en} 항목이 섞인 리스트 — 각 항목을 ko 로 접는다."""
    if not isinstance(value, list):
        return []
    return [_ko(v) for v in value]


def _quiz_type(value: Any) -> str:
    """good/distractor 두 값만 — 오값은 distractor 로. 퀴즈 채점이 type 을 본다."""
    return value if value in ("good", "distractor") else "distractor"


def _load_stage_data(detail_path: str) -> dict:
    """detail_path md 에서 `## Data` fenced yaml 을 파싱. 없거나 깨지면 빈 dict."""
    body = read_detail(detail_path)
    if not body:
        return {}
    match = _DATA_YAML.search(body)
    if not match:
        return {}
    try:
        data = yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return {}
    return data if isinstance(data, dict) else {}


def _problem(raw: Any) -> dict:
    src = raw if isinstance(raw, dict) else {}
    io = [
        {"input": _ko(ex.get("input")), "output": _ko(ex.get("output"))}
        for ex in (src.get("io") or [])
        if isinstance(ex, dict)
    ]
    return {
        "title": _ko(src.get("title")) or None,
        "statement": _ko(src.get("statement")),
        "constraints": _str_list(src.get("constraints")),
        "io": io,
    }


def _quiz_group(raw: Any) -> dict:
    """clarifying·approach 공용 — clarifying 항목은 q, approach 항목은 name 을 갖는다."""
    src = raw if isinstance(raw, dict) else {}
    items = []
    for it in src.get("items") or []:
        if not isinstance(it, dict):
            continue
        entry: dict[str, Any] = {"type": _quiz_type(it.get("type")), "why": _ko(it.get("why"))}
        if "q" in it:
            entry["q"] = _ko(it["q"])
        if "name" in it:
            entry["name"] = _ko(it["name"])
        if isinstance(it.get("complexity"), str):
            entry["complexity"] = it["complexity"]
        items.append(entry)
    return {"items": items}


def _logic(raw: Any) -> dict:
    """슬롯 퀴즈 — format 은 원장 값을 지나가게 두되 기본은 slot(화면이 slot 만 지원)."""
    src = raw if isinstance(raw, dict) else {}
    fmt = src.get("format") if isinstance(src.get("format"), str) else "slot"
    slots = []
    for slot in src.get("slots") or []:
        if not isinstance(slot, dict):
            continue
        options = [
            {"code": _ko(opt.get("code")), "type": _quiz_type(opt.get("type")), "why": _ko(opt.get("why"))}
            for opt in (slot.get("options") or [])
            if isinstance(opt, dict)
        ]
        slots.append(
            {
                "label": _ko(slot.get("label")),
                "indent": slot["indent"] if isinstance(slot.get("indent"), int) else 0,
                "options": options,
            }
        )
    return {"format": fmt, "slots": slots}


def _trace(raw: Any) -> dict:
    src = raw if isinstance(raw, dict) else {}
    cases = [
        {"input": _ko(c.get("input")), "expected": _ko(c.get("expected"))}
        for c in (src.get("cases") or [])
        if isinstance(c, dict)
    ]
    we = src.get("worked_example")
    worked = (
        {"input": _ko(we.get("input")), "steps": _ko_list(we.get("steps")), "answer": _ko(we.get("answer"))}
        if isinstance(we, dict)
        else None  # 없으면 null — 화면이 펼침 버튼 자체를 그리지 않는다
    )
    return {"code": _str_list(src.get("code")), "cases": cases, "worked_example": worked}


def _solution(raw: Any) -> dict:
    src = raw if isinstance(raw, dict) else {}
    comp = src.get("complexity") if isinstance(src.get("complexity"), dict) else {}
    return {
        "code": _ko(src.get("code")),
        "complexity": {"time": _ko(comp.get("time")), "space": _ko(comp.get("space"))},
        "followup": _ko_list(src.get("followup")),
    }


class AlgorithmService:
    def __init__(
        self, algorithm_repo: AlgorithmRepository, profile_repo: ProfileRepository
    ) -> None:
        self._algorithm_repo = algorithm_repo
        self._profile_repo = profile_repo

    async def _require_free_slug(
        self, session: AsyncSession, slug: str, exclude_id: int | None = None
    ) -> None:
        existing = await self._algorithm_repo.get_by_slug(session, slug)
        if existing and existing.id != exclude_id:
            raise ConflictError(f"slug already exists: {slug}")

    async def list_algorithms(self, session: AsyncSession) -> list[AlgorithmDTO]:
        return await self._algorithm_repo.list_all(session)

    async def _list_visible(self, session: AsyncSession) -> list[AlgorithmDTO]:
        """공개 목록의 원천 — published_on DESC NULLS LAST, id DESC 에서 visible 만.

        visible=false 는 여기서 걸러진다 — 응답에 visible 필드는 없다
        (erd §미결 3 의 확정: 공개 API 가 걸러서 내려준다).
        """
        return [a for a in await self._algorithm_repo.list_published(session) if a.visible]

    async def get_public(self, session: AsyncSession) -> PublicAlgorithmList:
        """공개 /algorithms 목록 — 전체 + today 한 건(meta 로 따로 내려간다).

        today 는 DB 가 하나뿐임을 강제한다(uq_algorithm_today). 그 한 건이
        visible=false 면 오늘의 문제 없음 — 숨긴 문제를 meta 로 드러내지 않는다.
        """
        visible = await self._list_visible(session)
        today = next((a for a in visible if a.today), None)
        return PublicAlgorithmList(items=visible, total_count=len(visible), today=today)

    async def get_public_detail(
        self, session: AsyncSession, slug: str
    ) -> PublicAlgorithmDetail:
        """공개 상세 한 벌 — 메타 + `## Data` yaml 의 단계 구조 + 이웃.

        이웃(newer/older)은 컬럼이 아니라 published_on 정렬의 이웃이다(erd.md).
        없는 slug 도, visible=false 도 같은 404 다 — 숨긴 문제의 존재를 드러내지 않는다.
        detail_path 가 끊기거나 yaml 이 깨지면 단계별 빈 구조로 내린다 — 500 이 아니다.
        """
        visible = await self._list_visible(session)
        idx = next((i for i, a in enumerate(visible) if a.slug == slug), None)
        if idx is None:
            raise NotFoundError(f"algorithm not found: {slug}")
        dto = visible[idx]
        newer = visible[idx - 1] if idx > 0 else None
        older = visible[idx + 1] if idx + 1 < len(visible) else None
        data = _load_stage_data(dto.detail_path)
        return PublicAlgorithmDetail(
            dto=dto,
            problem=_problem(data.get("problem")),
            clarifying=_quiz_group(data.get("clarifying")),
            approach=_quiz_group(data.get("approach")),
            logic=_logic(data.get("logic")),
            trace=_trace(data.get("trace")),
            solution=_solution(data.get("solution")),
            newer=AlgorithmNeighbor(slug=newer.slug, title=newer.title) if newer else None,
            older=AlgorithmNeighbor(slug=older.slug, title=older.title) if older else None,
        )

    async def create(
        self, session: AsyncSession, fields: dict[str, Any]
    ) -> AlgorithmDTO:
        _require_difficulty(fields["difficulty"])
        _require_detail_file(fields["detail_path"])
        await self._require_free_slug(session, fields["slug"])

        profile = await self._profile_repo.get_first(session)
        if profile is None:
            raise NotFoundError("profile not found — seed_profile 을 먼저 돌린다")
        fields["profile_id"] = profile.id

        if fields.get("today"):
            # 새 행을 today 로 올리려면 기존 today 를 같은 트랜잭션에서 먼저 내린다.
            await self._algorithm_repo.clear_today(session)
        return await self._algorithm_repo.create(session, fields)

    async def update(
        self, session: AsyncSession, algorithm_id: int, fields: dict[str, Any]
    ) -> AlgorithmDTO:
        for name in _NOT_NULLABLE & fields.keys():
            if fields[name] is None:
                raise ValidationError(f"{name} cannot be null")
        if "difficulty" in fields:
            _require_difficulty(fields["difficulty"])
        if "detail_path" in fields:
            _require_detail_file(fields["detail_path"])
        if "slug" in fields:
            await self._require_free_slug(
                session, fields["slug"], exclude_id=algorithm_id
            )
        if fields.get("today"):
            current = await self._algorithm_repo.get_today(session)
            if current is not None and current.id != algorithm_id:
                # 이전 「오늘의 문제」를 먼저 내린다 — 같은 트랜잭션이라 중간
                # 실패면 통째로 롤백. DB partial unique 가 최종 방어다.
                await self._algorithm_repo.clear_today(session)
        dto = await self._algorithm_repo.update(session, algorithm_id, fields)
        if dto is None:
            raise NotFoundError(f"algorithm not found: {algorithm_id}")
        return dto

    async def delete(self, session: AsyncSession, algorithm_id: int) -> None:
        if not await self._algorithm_repo.delete(session, algorithm_id):
            raise NotFoundError(f"algorithm not found: {algorithm_id}")


algorithm_service = AlgorithmService(AlgorithmRepository(), ProfileRepository())

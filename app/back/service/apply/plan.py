"""발행 계획 조립과 검증 (KDEV-WORK-015 P4 / KDEV-SPEC-010).

**하나라도 위반이면 발행 전체를 거부한다.** 부분 적용을 허용하면 reference 만 나가고
concept 는 빠진 상태가 되어, 링크가 깨진 채로 origin 에 올라간다. 그건 사람이 나중에
손으로 고쳐야 하는 상태다.

검증은 **파일을 쓰기 전에** 전부 끝난다. 커밋 후 부팅 검증으로 잡으면 이미 origin 에
나간 뒤라 늦다.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import frontmatter

logger = logging.getLogger("kknaks-back.apply.plan")

#: 발행이 쓸 수 있는 디렉토리. **이 밖은 전부 거부한다** —
#: 경로 조립에 버그가 있어도 `app/` 이나 `.github/` 를 건드리지 못하게 한다.
ALLOWED_PREFIXES = (
    "reference/",
    "permanent/",
    "inbox/",
    "persona/contents/",
)

#: 층과 경로의 정합. 개념이 `reference/` 에 들어가면 로더가 다른 타입으로 읽는다.
LAYER_PREFIX = {
    "reference": "reference/",
    "concept": "permanent/concept/",
    "permanent": "permanent/",
    "idea": "inbox/",
    "content": "persona/contents/",
}

_TRAVERSAL = re.compile(r"(^/)|(\.\.)")


@dataclass
class FileAction:
    action: str  # create | replace
    path: str
    content: str
    note_type: str
    stem: str
    source_gate: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "action": self.action,
            "path": self.path,
            "content": self.content,
            "note_type": self.note_type,
            "stem": self.stem,
            "source_gate": self.source_gate,
        }


@dataclass
class Violation:
    rule: str
    path: str
    detail: str

    def as_dict(self) -> dict[str, str]:
        return {"rule": self.rule, "path": self.path, "detail": self.detail}


@dataclass
class Plan:
    actions: list[FileAction] = field(default_factory=list)
    violations: list[Violation] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.violations

    def as_json(self) -> list[dict[str, Any]]:
        return [a.as_dict() for a in self.actions]


def _note_type(content: str) -> str:
    try:
        return str(frontmatter.loads(content).metadata.get("type") or "")
    except Exception:  # noqa: BLE001
        return ""


def build_actions(approved: dict[str, dict[str, Any]]) -> list[FileAction]:
    """승인된 게이트 산출물 → 파일 액션 목록.

    `approved` 는 `{stage_name: payload}`. **경로는 payload 의 `target_path` 를 쓰되**,
    그것도 시스템이 조립한 값이지 AI 가 낸 값이 아니다(스테이지에서 stem 만 받는다).
    """
    actions: list[FileAction] = []

    for stage in ("source_note", "derived"):
        payload = approved.get(stage)
        if not payload:
            continue
        content = str(payload.get("content") or "")
        actions.append(
            FileAction(
                action="create",
                path=str(payload.get("target_path") or ""),
                content=content,
                note_type=_note_type(content),
                stem=str(payload.get("filename_stem") or ""),
                source_gate=stage,
            )
        )

    for concept in (approved.get("concept") or {}).get("concepts") or []:
        if concept.get("excluded"):
            # 제외한 개념은 계획에 들어가지 않는다 — 승인 화면에서 뺀 것이 그대로 반영된다.
            continue
        content = str(concept.get("content") or "")
        actions.append(
            FileAction(
                action="replace" if concept.get("mode") == "supplement" else "create",
                path=str(concept.get("target_path") or ""),
                content=content,
                note_type=_note_type(content),
                stem=str(concept.get("stem") or ""),
                source_gate="concept",
            )
        )
    return actions


def validate_plan(
    actions: list[FileAction],
    *,
    repo_root: Path,
    known_stems: set[str] | None = None,
) -> list[Violation]:
    """검증 6종 중 파일 단위 5종. 그래프 검증(L1~L6)은 `validate_virtual_graph` 가 맡는다.

    1. 경로 allowlist  2. 층-경로 정합  3. `up:` 필수  4. 신규 중복  5. stale 대상
    """
    violations: list[Violation] = []
    seen: set[str] = set()

    for action in actions:
        path = action.path

        # 1. 경로 allowlist
        if not path or _TRAVERSAL.search(path) or not path.endswith(".md"):
            violations.append(Violation("PATH_SHAPE", path, "경로 형태가 올바르지 않다"))
            continue
        if not any(path.startswith(prefix) for prefix in ALLOWED_PREFIXES):
            violations.append(
                Violation("PATH_NOT_ALLOWED", path, "발행이 쓸 수 없는 디렉토리다")
            )
            continue
        if path in seen:
            violations.append(Violation("DUPLICATE_PATH", path, "한 발행에 같은 경로가 두 번"))
            continue
        seen.add(path)

        # 2. 층-경로 정합
        expected = LAYER_PREFIX.get(action.note_type)
        if expected is None:
            violations.append(
                Violation("UNKNOWN_TYPE", path, f"알 수 없는 type: {action.note_type or '(없음)'}")
            )
        elif not path.startswith(expected):
            violations.append(
                Violation(
                    "LAYER_PATH_MISMATCH",
                    path,
                    f"type={action.note_type} 는 {expected} 아래여야 한다",
                )
            )
        elif action.note_type == "permanent" and path.startswith("permanent/concept/"):
            violations.append(
                Violation("LAYER_PATH_MISMATCH", path, "종합 노트가 concept 디렉토리에 있다")
            )

        # 3. `up:` 필수 (concept·permanent)
        if action.note_type in ("concept", "permanent"):
            try:
                meta = frontmatter.loads(action.content).metadata
            except Exception:  # noqa: BLE001
                meta = {}
            if not meta.get("up"):
                violations.append(Violation("MISSING_UP", path, "up: 이 비어 있다"))

        target = repo_root / path
        exists = target.exists()

        # 4. 신규 중복 — 새로 만든다면서 이미 있으면 덮어쓰는 것이다
        if action.action == "create":
            if exists:
                violations.append(
                    Violation("ALREADY_EXISTS", path, "신규인데 파일이 이미 있다")
                )
            if known_stems and action.stem in known_stems:
                violations.append(
                    Violation("STEM_TAKEN", path, f"stem '{action.stem}' 이 이미 그래프에 있다")
                )
        # 5. stale 대상 — 고친다면서 대상이 없으면 초안 이후 사라진 것이다
        elif action.action == "replace" and not exists:
            violations.append(
                Violation("TARGET_MISSING", path, "수정 대상 파일이 사라졌다")
            )

    if not actions:
        violations.append(Violation("EMPTY_PLAN", "", "발행할 것이 없다"))
    return violations

"""노트를 만드는 게이트 스테이지의 공통부 (KDEV-WORK-015 / KDEV-SPEC-010).

**AI 가 md 전문을 낸다.** 종전 캡처 경로는 `AI → JSON → render.py → md` 였는데,
그러면 `render.py` 의 하드코딩된 섹션 구성이 `templates/knowledge/` 와 나란히
**형식의 SoT 두 번째**가 된다. 규칙을 고쳐도 렌더러가 안 따라오면 조용히 어긋난다.

그래서 여기서는 에이전트가 레포의 템플릿을 읽고 **완성된 markdown 을 직접** 낸다.
`render.py` 는 롤백 경로(`KnowledgeCaptureRunner`)에만 남는다.

AI 가 내는 것은 `filename_stem` 과 본문뿐이다. **디렉토리는 시스템이 층·목적지에서
조립한다**(SPEC-010) — 경로 결정을 AI 에 맡기면 allowlist 밖으로 쓰는 계획이 나온다.
"""

from __future__ import annotations

import json
import re
from typing import Any

import frontmatter

from ..gates import GateError, GenerationInput

#: `rules/knowledge-note-pipeline.md` 의 파일명 규약.
REFERENCE_STEM_RE = re.compile(r"\d{4}-\d{2}-\d{2}-[a-z0-9]+(?:-[a-z0-9]+)*")
#: concept 는 **날짜를 붙이지 않는다** — 개념은 특정 시점에 묶이지 않는다.
#: 숫자 자체는 허용한다(`gpt-4`, `http2`). 앞머리의 날짜 형태만 막는다.
CONCEPT_STEM_RE = re.compile(r"(?!\d{4}-\d{2}-\d{2})[a-z0-9]+(?:-[a-z0-9]+)*")

READ_THE_RULES = """작성 전에 레포의 규칙과 양식을 **반드시 읽어라.** 이 프롬프트에 복사돼 있지 않다.

1. `rules/knowledge-note-pipeline.md` — 4층 모델, SoT 위임, 개념 성장, `up:` 방향, 층별 필수 필드
2. `templates/knowledge/{template}` — 만들 노트의 양식 (섹션 구성과 각 섹션에 넣을 것)

읽지 않고 쓰면 형식이 어긋나 발행 전 검증에서 거부된다."""

OUTPUT_CONTRACT_LIST = """아래 JSON 하나만 출력한다. 코드펜스나 설명 문장을 붙이지 않는다.

{shape}

`content` 는 완성된 노트 그대로다. 요약이나 발췌가 아니다.
경로는 시스템이 조립하므로 디렉토리를 지어내지 않는다."""

OUTPUT_CONTRACT = """아래 JSON 하나만 출력한다. 코드펜스나 설명 문장을 붙이지 않는다.

{
  "filename_stem": "<파일명 stem. 확장자·디렉토리 없이>",
  "content": "<frontmatter 를 포함한 markdown 전문>"
}

`content` 는 완성된 노트 그대로다. 요약이나 발췌가 아니다.
경로는 시스템이 조립하므로 디렉토리를 지어내지 않는다."""


def parse_json_output(raw: str) -> dict[str, Any]:
    """모델 출력에서 JSON 객체를 꺼낸다. 코드펜스를 붙이는 경우가 있어 한 겹 벗긴다."""
    cleaned = (raw or "").strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[-1]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()
        if cleaned.startswith("json"):
            cleaned = cleaned[4:].strip()
    try:
        data = json.loads(cleaned)
    except ValueError as exc:
        raise GateError("INVALID_NOTE_OUTPUT", f"JSON 파싱 실패: {exc}") from exc
    if not isinstance(data, dict):
        raise GateError("INVALID_NOTE_OUTPUT", "출력이 객체가 아니다")
    return data


def parse_note_output(raw: str) -> tuple[str, str]:
    """`{filename_stem, content}` 를 꺼낸다. 어긋나면 `GateError`."""
    data = parse_json_output(raw)
    stem = str(data.get("filename_stem") or "").strip()
    content = data.get("content")
    if not stem:
        raise GateError("INVALID_NOTE_OUTPUT", "filename_stem 이 없다")
    if not isinstance(content, str) or not content.strip():
        raise GateError("INVALID_NOTE_OUTPUT", "content 가 비었다")
    if "/" in stem or stem.endswith(".md"):
        # 경로를 지어내면 allowlist 밖으로 쓰는 계획이 만들어진다.
        raise GateError("INVALID_NOTE_OUTPUT", f"stem 에 경로나 확장자가 들어갔다: {stem}")
    return stem, content


def check_note(
    stem: str,
    content: str,
    *,
    expected_type: str,
    stem_pattern: re.Pattern[str],
    required: tuple[str, ...],
) -> dict[str, Any]:
    """게이트 시점의 가벼운 검사 — 사람이 보기 전에 명백히 틀린 것을 거른다.

    전체 그래프 검증(L1~L6)은 발행 직전에 가상 그래프로 돈다(SPEC-010 S-3).
    여기서 그걸 다 하지 않는 이유는, 이 시점에는 형제 노트들이 아직 안 만들어져
    링크가 깨져 보이기 때문이다.
    """
    if not stem_pattern.fullmatch(stem):
        raise GateError("INVALID_NOTE_STEM", f"'{stem}' 은 파일명 규약에 맞지 않는다")
    try:
        post = frontmatter.loads(content)
    except Exception as exc:  # noqa: BLE001
        raise GateError("INVALID_NOTE_OUTPUT", f"frontmatter 파싱 실패: {exc}") from exc

    meta = post.metadata
    declared = meta.get("type")
    if declared is not None and declared != expected_type:
        raise GateError(
            "INVALID_NOTE_OUTPUT", f"type 이 {declared} 다 — {expected_type} 이어야 한다"
        )
    missing = [f for f in required if not meta.get(f)]
    if missing:
        raise GateError("MISSING_NOTE_FIELD", f"필수 필드 누락: {', '.join(missing)}")

    declared_id = str(meta.get("id") or "").strip()
    if declared_id and declared_id != stem:
        # stem 과 id 가 다르면 로더가 실패한다(지식 노트는 id = 파일명 stem).
        raise GateError("INVALID_NOTE_OUTPUT", f"id({declared_id}) 와 stem({stem}) 이 다르다")
    return meta


def up_targets(meta: dict[str, Any]) -> list[str]:
    raw = meta.get("up") or []
    if isinstance(raw, str):
        return [raw]
    return [str(v) for v in raw if str(v).strip()]


def body_links(content: str) -> set[str]:
    """본문 `[[...]]` 대상. `|` 별칭 표기를 걷어낸다."""
    return {
        match.split("|")[0].strip()
        for match in re.findall(r"\[\[([^\]]+)\]\]", content)
    }


def require_up_in_body(meta: dict[str, Any], content: str) -> None:
    """`up:` 은 본문 링크의 부분집합이어야 한다 (L3 · KDEV-DEC-004).

    본문이 엣지의 단일 소스이고 `up:` 은 그중 계보인 것을 마킹하는 오버레이다.
    여기서 잡지 않으면 발행 직전 검증에서 통째로 거부돼 다시 만들어야 한다.
    """
    links = body_links(content)
    missing = [stem for stem in up_targets(meta) if stem not in links]
    if missing:
        raise GateError(
            "UP_NOT_IN_BODY",
            f"up: 에 있는 {', '.join(missing)} 이 본문 [[]] 에 없다",
        )


def context_payload(request: GenerationInput) -> dict[str, Any]:
    """모든 노트 스테이지가 공통으로 넘기는 입력."""
    preparation = (request.preparation.payload or {}) if request.preparation else {}
    payload: dict[str, Any] = {
        "source_url": request.item.source_url,
        "source_kind": request.item.source_kind,
        "note": request.item.note,
        "summary": preparation.get("summary"),
        "material_source": preparation.get("material_source"),
        "collected_at": preparation.get("source", {}).get("accessed_at")
        if isinstance(preparation.get("source"), dict)
        else None,
    }
    source = preparation.get("source")
    if isinstance(source, dict):
        payload["source_title"] = source.get("title")
        payload["source_excerpt"] = (source.get("content") or "")[:40_000] or None
    if request.previous_payload is not None:
        payload["previous_draft"] = request.previous_payload
    if request.feedback:
        payload["feedback"] = request.feedback
    return payload

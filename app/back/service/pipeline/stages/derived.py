"""`derived` 스테이지 — 교안 (KDEV-WORK-015 P3 / SPEC-008 stage 6).

`persona/contents/` 의 교안을 만든다. 형식 명세는 **`templates/persona/content.md` 한 곳**에서
불러온다(`service/content_format.py`) — `content_enrich` 잡도 같은 파일을 읽는다.

처음에는 8개 섹션 명세를 이 파일 프롬프트에 적었는데, 그건 `reference`·`concept` 에서
없앤 이중 SoT 를 교안에서 다시 만드는 것이었다. 한쪽만 고치는 날 두 경로의 산출물이
조용히 갈라진다.

**`status: pending` 을 쓰지 않는다.** 그것이 `content_enrich` 의 스캔 조건이라,
쓰면 게이트가 만든 교안을 그 잡이 한 번 더 덮어쓴다. 게이트 산출물은 처음부터
`published` 로 완성돼 나온다 — owner 결정(교안 경로 공존, WORK-015 P1).

**식별자와 순번은 AI 가 정하지 않는다.** `C-NNN` 과 `Day NN` 은 기존 파일을 세어
시스템이 매긴다 — AI 에 맡기면 중복 번호가 나온다.
"""

from __future__ import annotations

import json
import re
from datetime import date, datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import frontmatter

from ..executor import AgentStage
from ..gates import GateError, GenerationInput
from ...content_format import content_format, content_stem
from .common import OUTPUT_CONTRACT_LIST, context_payload, parse_json_output

KST = ZoneInfo("Asia/Seoul")
CONTENTS_DIR = "persona/contents"
_ID_RE = re.compile(r"C-(\d+)")

RESULT_SHAPE = """{
  "title":   {"ko": "...", "en": "..."},
  "summary": {"ko": "...", "en": "..."},
  "tags":    ["#tag1", "#tag2"],
  "concept": ["문장1", "문장2", "문장3", "문장4"],
  "kind":    "tutorial | study | talk | review",
  "body":    "<## 개요 부터 시작하는 markdown 전문>"
}"""

INSTRUCTION = """이 영상의 **강의 교안**을 작성하라.

아래 양식을 그대로 따른다 — 이것이 교안 형식의 SoT(`templates/persona/content.md`)다.

────────────────────────────────────────
{format}
────────────────────────────────────────

{output}"""

KINDS = ("tutorial", "study", "talk", "review")


def next_content_id(repo_root: Path) -> tuple[str, int]:
    """다음 `C-NNN` 과 Day 순번. 기존 파일을 세어 시스템이 매긴다."""
    directory = repo_root / CONTENTS_DIR
    highest = 0
    count = 0
    if directory.is_dir():
        for path in directory.glob("C-*.md"):
            match = _ID_RE.match(path.name)
            if match:
                highest = max(highest, int(match.group(1)))
                count += 1
    return f"C-{highest + 1:03d}", count + 1


def video_header(preparation_payload: dict[str, Any]) -> dict[str, Any]:
    """수집 결과 앞머리의 영상 메타(JSON) — 채널·길이가 frontmatter 에 들어간다."""
    source = preparation_payload.get("source")
    if not isinstance(source, dict):
        return {}
    content = source.get("content") or ""
    head = content.split("\n\n", 1)[0]
    try:
        parsed = json.loads(head)
        return parsed if isinstance(parsed, dict) else {}
    except ValueError:
        return {}


def format_duration(seconds: Any) -> str:
    try:
        total = int(seconds)
    except (TypeError, ValueError):
        return ""
    return f"{total // 60}:{total % 60:02d}"


def _require(data: dict[str, Any], key: str, kind: type) -> Any:
    value = data.get(key)
    if not isinstance(value, kind) or (kind in (str, list, dict) and not value):
        raise GateError("INVALID_DERIVED_OUTPUT", f"{key} 가 없거나 형식이 맞지 않는다")
    return value


def build_content_note(
    data: dict[str, Any],
    *,
    repo_root: Path,
    preparation_payload: dict[str, Any],
    source_url: str | None,
    today: date | None = None,
) -> dict[str, Any]:
    """AI 출력 + 시스템 값 → 완성된 교안 파일. 어긋나면 `GateError`."""
    title = _require(data, "title", dict)
    summary = _require(data, "summary", dict)
    for field, value in (("title", title), ("summary", summary)):
        if not value.get("ko") or not value.get("en"):
            raise GateError("INVALID_DERIVED_OUTPUT", f"{field} 에 ko/en 이 모두 필요하다")

    tags = _require(data, "tags", list)
    concept = _require(data, "concept", list)
    body = _require(data, "body", str)
    kind = str(data.get("kind") or "").strip()
    if kind not in KINDS:
        raise GateError("INVALID_DERIVED_OUTPUT", f"알 수 없는 kind: {kind}")
    if "## 개요" not in body:
        raise GateError("INVALID_DERIVED_OUTPUT", "본문에 「개요」 섹션이 없다")

    content_id, day_index = next_content_id(repo_root)
    stem = content_stem(content_id, title)
    header = video_header(preparation_payload)
    stamp = datetime.now(KST)
    meta: dict[str, Any] = {
        "type": "content",
        "id": content_id,
        "date": (today or stamp.date()).strftime("%Y.%m.%d"),
        "day": f"Day {day_index:02d}",
        "title": title,
        "summary": summary,
        "duration": format_duration(header.get("duration_s")),
        "speaker": header.get("channel") or "",
        "tags": [str(t) for t in tags],
        "concept": [str(c) for c in concept],
        "kind": kind,
        "transcript": bool(preparation_payload.get("material_source") == "fetched"),
        "enriched_at": stamp.isoformat(timespec="seconds"),
        # `pending` 이면 content_enrich 가 한 번 더 덮어쓴다.
        "status": "published",
    }
    if header.get("video_id"):
        meta["youtubeId"] = header["video_id"]
    elif source_url:
        meta["source"] = source_url

    rendered = frontmatter.dumps(frontmatter.Post(content=body, **meta))
    return {
        "filename_stem": stem,
        "content": rendered,
        "target_path": f"{CONTENTS_DIR}/{stem}.md",
        "content_id": content_id,
    }


class DerivedStage(AgentStage):
    """open-kknaks 로 교안 초안을 만든다."""

    source = "pipeline-derived"

    def prompt(self, request: GenerationInput) -> str:
        return INSTRUCTION.format(
            format=content_format(self.repo_root),
            output=OUTPUT_CONTRACT_LIST.format(shape=RESULT_SHAPE),
        )

    def payload(self, request: GenerationInput) -> dict[str, Any]:
        return {
            **context_payload(request),
            "video": video_header(_preparation(request)),
        }

    def parse(self, raw: str, request: GenerationInput) -> dict[str, Any]:
        # `C-NNN` 과 Day 순번은 **수확 시점에** 매긴다 — 제출 시점에 매기면 그 사이
        # 발행된 다른 교안과 번호가 겹친다.
        return build_content_note(
            parse_json_output(raw),
            repo_root=self.repo_root,
            preparation_payload=_preparation(request),
            source_url=request.item.source_url,
        )


def _preparation(request: GenerationInput) -> dict[str, Any]:
    return (request.preparation.payload or {}) if request.preparation else {}

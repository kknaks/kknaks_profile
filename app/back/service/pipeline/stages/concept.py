"""`concept` 스테이지 — 개념 추출과 신규/보충 판정 (KDEV-WORK-015 P2 / SPEC-008 stage 5).

이 파이프라인의 실질 품질은 **추출보다 매칭**이 결정한다. 같은 개념의 두 번째 출처가
새 파일을 만들면 SoT 가 둘로 갈라지고, 반대로 다른 개념을 같은 것으로 보면 남의
노트를 덮어쓴다.

둘 다 나쁘지만 **오매칭이 더 나쁘다** — 갈라진 건 나중에 합칠 수 있지만 덮어쓴 건
git 이력을 뒤져야 한다. 그래서 의심스러우면 **실패시킨다.** 사람이 피드백으로 고치는
편이, 조용히 잘못된 판정으로 발행되는 것보다 낫다.

판정 구조:

    인덱스 조회 (결정적)  →  AI 가 mode·전문 작성  →  서버가 재검증
                                                      └ 어긋나면 거부

AI 에게 인덱스를 미리 주고도 서버가 다시 보는 이유는, 프롬프트를 무시하는 경우가
실제로 있기 때문이다. 재검증이 없으면 그 순간이 조용한 덮어쓰기가 된다.
"""

from __future__ import annotations

import difflib
from pathlib import Path
from typing import Any

from ..concept_index import ConceptIndex, build_index, read_concept
from ..executor import AgentStage
from ..gates import GateError, GenerationInput
from .common import (
    CONCEPT_STEM_RE,
    OUTPUT_CONTRACT_LIST,
    READ_THE_RULES,
    check_note,
    context_payload,
    parse_json_output,
    require_up_in_body,
    up_targets,
)
import frontmatter

INSTRUCTION = """이 자료에서 **원자 개념**을 뽑아 concept 노트를 작성하라.

{rules}

**개념을 억지로 만들지 않는다.** 뽑을 것이 없으면 빈 목록을 낸다 — 자료에만 붙어 있는
설명은 개념이 아니다. 판단 기준(독립 재사용 가능성)은 위 규칙 문서에 있다.

**이미 있는 개념인지 먼저 확인하라.** 아래 `existing_concepts` 에 stem·title·aliases 가
있다. 이름이 달라도 같은 개념이면 **새로 만들지 말고 보충한다.**

- `mode: "supplement"` — 기존 개념이다. 그 파일(`path`)을 **직접 읽고**, 이번 자료가
  더하는 내용을 **녹여서 전문을 다시 쓴다.** 덧붙이는 게 아니라 다시 쓰는 것이다.
  기존 `aliases` 와 `up:` 은 **하나도 빠뜨리지 않고** 유지한 뒤 새 것을 더한다.
- `mode: "create"` — 정말 새 개념이다. `existing_concepts` 어디에도 없어야 한다.

공통으로 지켜야 할 것:
- `filename_stem` 에 **날짜를 붙이지 않는다.** 개념은 특정 시점에 묶이지 않는다.
- `aliases` 는 **필수**다. 같은 개념의 다른 이름(약어·영문·한글)을 넣는다.
  여기가 비면 다음 자료에서 같은 개념이 두 파일로 갈라진다.
- `up:` 은 **필수**이고 이번 자료의 reference stem `{reference_stem}` 을 포함해야 한다.
  본문 「출처」에도 `[[{reference_stem}]]` 를 둔다 — `up:` 은 본문 링크의 부분집합이다.

{output}"""

RESULT_SHAPE = """{
  "concepts": [
    {
      "filename_stem": "<날짜 없는 소문자-하이픈 slug>",
      "mode": "create" 또는 "supplement",
      "names": ["<이 개념을 부르는 이름들 — 매칭 확인용>"],
      "content": "<frontmatter 를 포함한 markdown 전문>"
    }
  ]
}"""


def _diff(before: str, after: str, stem: str) -> str:
    """보충 diff — **사라지는 줄**이 보여야 한다.

    보충은 덧붙이기가 아니라 다시 쓰기라서, 무엇이 빠지는지가 승인 판단의 핵심이다.
    """
    return "".join(
        difflib.unified_diff(
            before.splitlines(keepends=True),
            after.splitlines(keepends=True),
            fromfile=f"a/{stem}.md",
            tofile=f"b/{stem}.md",
            n=3,
        )
    )


def _aliases_of(content: str) -> set[str]:
    try:
        meta = frontmatter.loads(content).metadata
    except Exception:  # noqa: BLE001
        return set()
    raw = meta.get("aliases") or []
    if isinstance(raw, str):
        raw = [raw]
    return {str(v).strip() for v in raw if str(v).strip()}


def verify_concepts(
    raw_concepts: list[dict[str, Any]],
    *,
    index: ConceptIndex,
    repo_root: Path,
    reference_stem: str | None,
) -> list[dict[str, Any]]:
    """AI 판정을 서버가 다시 본다. 어긋나면 `GateError`.

    통과하면 `concept_result[]` 계약 형태로 정규화해 돌려준다.
    """
    results: list[dict[str, Any]] = []
    seen: set[str] = set()

    for raw in raw_concepts:
        if not isinstance(raw, dict):
            raise GateError("INVALID_CONCEPT_OUTPUT", "concepts 항목이 객체가 아니다")
        stem = str(raw.get("filename_stem") or "").strip()
        mode = str(raw.get("mode") or "").strip()
        content = raw.get("content")
        names = [str(n) for n in (raw.get("names") or []) if str(n).strip()]

        if "/" in stem or stem.endswith(".md"):
            raise GateError("INVALID_CONCEPT_OUTPUT", f"stem 에 경로가 들어갔다: {stem}")
        if mode not in ("create", "supplement"):
            raise GateError("INVALID_CONCEPT_OUTPUT", f"알 수 없는 mode: {mode}")
        if not isinstance(content, str) or not content.strip():
            raise GateError("INVALID_CONCEPT_OUTPUT", f"{stem} 의 content 가 비었다")
        if stem in seen:
            raise GateError("DUPLICATE_CONCEPT", f"같은 stem 이 두 번 나왔다: {stem}")
        seen.add(stem)

        check_note(
            stem,
            content,
            expected_type="concept",
            stem_pattern=CONCEPT_STEM_RE,
            required=("title", "aliases", "up"),
        )
        meta = frontmatter.loads(content).metadata
        require_up_in_body(meta, content)

        # 이번 자료가 상류로 걸려야 계보가 생긴다(DEC-010 D4).
        ups = up_targets(meta)
        if reference_stem and reference_stem not in ups:
            raise GateError(
                "MISSING_LINEAGE",
                f"{stem} 의 up: 에 이번 자료({reference_stem})가 없다",
            )

        # --- 매칭 재검증 -------------------------------------------------
        entry, matched_by = index.match_any([stem, *names])

        if mode == "create":
            if entry is not None:
                # 이게 이 스테이지에서 가장 비싼 실수다 — 조용히 통과시키지 않는다.
                raise GateError(
                    "CONCEPT_ALREADY_EXISTS",
                    f"'{matched_by or stem}' 는 이미 {entry.stem} 로 존재한다 — "
                    "신규가 아니라 보충이어야 한다",
                )
            results.append(
                {
                    "mode": "create",
                    "stem": stem,
                    "matched_by": None,
                    "content": content,
                    "excluded": False,
                    "target_path": f"resources/concept/{stem}.md",
                }
            )
            continue

        # supplement
        target = index.get(stem) or entry
        if target is None:
            raise GateError(
                "CONCEPT_NOT_FOUND", f"보충 대상 {stem} 이 기존 개념에 없다"
            )
        before = read_concept(repo_root, target.stem)
        if before is None:
            raise GateError("CONCEPT_NOT_FOUND", f"{target.stem} 파일을 읽지 못했다")

        # 보충은 다시 쓰기라 **기존 alias 를 잃기 쉽다.** 잃으면 다음 자료에서
        # 같은 개념이 또 갈라진다.
        lost = {a for a in target.aliases if a} - _aliases_of(content)
        if lost:
            raise GateError(
                "ALIASES_LOST",
                f"{target.stem} 의 기존 aliases 가 빠졌다: {', '.join(sorted(lost))}",
            )
        # 기존 출처도 유지돼야 한다 — 지우면 그 자료가 이 개념에 기여한 사실이 사라진다.
        before_ups = set(up_targets(frontmatter.loads(before).metadata))
        lost_ups = before_ups - set(ups)
        if lost_ups:
            raise GateError(
                "SOURCES_LOST",
                f"{target.stem} 의 기존 up: 이 빠졌다: {', '.join(sorted(lost_ups))}",
            )

        results.append(
            {
                "mode": "supplement",
                "stem": target.stem,
                "matched_by": matched_by,
                "content": content,
                "excluded": False,
                "target_path": target.path,
                "diff": _diff(before, content, target.stem),
            }
        )

    return results


def apply_exclusions(
    approved: dict[str, Any], proposed: dict[str, Any]
) -> dict[str, Any]:
    """승인 시 사람이 바꿀 수 있는 것은 **제외 토글뿐**이다.

    화면에서 본문을 바꿔 보낼 수 있게 두면, 검증을 통과한 내용과 발행되는 내용이
    달라진다 — 게이트가 무의미해진다. 그래서 stem·mode·content 는 제안된 그대로여야
    하고 `excluded` 만 반영한다.
    """
    proposed_list = proposed.get("concepts") or []
    incoming = approved.get("concepts")
    if not isinstance(incoming, list):
        raise GateError("INVALID_CONCEPT_APPROVAL", "concepts 가 목록이 아니다")
    if len(incoming) != len(proposed_list):
        raise GateError("INVALID_CONCEPT_APPROVAL", "개념 개수가 제안과 다르다")

    by_stem = {c["stem"]: c for c in proposed_list}
    merged: list[dict[str, Any]] = []
    for entry in incoming:
        if not isinstance(entry, dict):
            raise GateError("INVALID_CONCEPT_APPROVAL", "concepts 항목이 객체가 아니다")
        stem = str(entry.get("stem") or "")
        original = by_stem.get(stem)
        if original is None:
            raise GateError("INVALID_CONCEPT_APPROVAL", f"제안에 없는 개념이다: {stem}")
        if entry.get("content") != original["content"] or entry.get("mode") != original["mode"]:
            raise GateError(
                "INVALID_CONCEPT_APPROVAL",
                f"{stem} 의 내용을 승인 시점에 바꿀 수 없다 — 고치려면 피드백으로 재생성한다",
            )
        merged.append({**original, "excluded": bool(entry.get("excluded"))})

    if merged and all(c["excluded"] for c in merged):
        # 전부 제외면 이 게이트는 아무것도 만들지 않는다. 그건 route 에서 개념을
        # 끄는 것과 같은 결정이라 여기서 조용히 통과시키지 않는다.
        raise GateError(
            "ALL_CONCEPTS_EXCLUDED",
            "개념을 전부 제외했다 — 목적지 재검토로 개념을 끄는 편이 맞다",
        )
    return {"concepts": merged}


class ConceptStage(AgentStage):
    """open-kknaks 로 개념 초안을 만들고 서버가 판정을 재검증한다.

    **인덱스는 수확 시점에 다시 읽는다.** 제출과 수확 사이에 다른 항목이 개념을 발행할
    수 있어, 제출 때의 인덱스로 재검증하면 방금 생긴 개념을 못 보고 `create` 를 통과시킨다.
    """

    source = "pipeline-concept"

    def prompt(self, request: GenerationInput) -> str:
        return INSTRUCTION.format(
            rules=READ_THE_RULES.format(template="concept.md"),
            reference_stem=_reference_stem(request) or "(이번 자료의 reference 없음)",
            output=OUTPUT_CONTRACT_LIST.format(shape=RESULT_SHAPE),
        )

    def payload(self, request: GenerationInput) -> dict[str, Any]:
        return {
            **context_payload(request),
            "reference_stem": _reference_stem(request),
            "existing_concepts": build_index(self.repo_root).as_prompt_payload(),
        }

    def parse(self, raw: str, request: GenerationInput) -> dict[str, Any]:
        data = parse_json_output(raw)
        raw_concepts = data.get("concepts")
        if not isinstance(raw_concepts, list):
            raise GateError("INVALID_CONCEPT_OUTPUT", "concepts 가 목록이 아니다")

        return {
            "concepts": verify_concepts(
                raw_concepts,
                index=build_index(self.repo_root),
                repo_root=self.repo_root,
                reference_stem=_reference_stem(request),
            )
        }


def _reference_stem(request: GenerationInput) -> str | None:
    """같은 항목의 승인된 `source_note` stem — concept 가 `up:` 으로 가리킬 대상.

    reference 를 끈 경우에는 `None` 이고, 그때는 계보 요구를 걸지 않는다.
    """
    return (request.upstream or {}).get("source_note_stem")

"""`source_note` 스테이지 — reference 초안 (KDEV-WORK-015 P1 / SPEC-008 stage 4).

출처 기록층 노트 하나를 만든다. 개념 상세는 여기 쓰지 않고 concept 노트에 위임한다
— 그 규칙은 프롬프트가 아니라 `rules/knowledge-note-pipeline.md` 에 있다.
"""

from __future__ import annotations

from typing import Any

from ..executor import AgentStage
from ..gates import GenerationInput
from .common import (
    OUTPUT_CONTRACT,
    READ_THE_RULES,
    REFERENCE_STEM_RE,
    check_note,
    context_payload,
    parse_note_output,
)

INSTRUCTION = """이 자료의 **출처 기록 노트**(reference) 를 작성하라.

{rules}

지켜야 할 것:
- `filename_stem` 은 `{{YYYY-MM-DD}}-{{slug}}` 형태다. 날짜는 수집일, slug 는 소문자-하이픈.
- frontmatter 에 `up:` 을 두지 않는다. reference 는 출처 기록층이라 상류가 없다.
- 자료가 말한 것과 내 해석을 섞지 않는다. 「적용 가능성」부터가 해석이다.
- 개념을 길게 설명하지 않는다. 「주요 개념」에는 이름 + 한 줄만 쓰고 상세는 concept 노트에 위임한다.
  아직 concept 노트가 없으므로 이 섹션은 비워 두거나 개념 후보만 적는다.
- 수치를 옮길 때는 조건과 한계를 함께 적는다.

{output}"""


class SourceNoteStage(AgentStage):
    """open-kknaks 로 reference 초안을 만든다."""

    source = "pipeline-source-note"

    def prompt(self, request: GenerationInput) -> str:
        return INSTRUCTION.format(
            rules=READ_THE_RULES.format(template="reference.md"), output=OUTPUT_CONTRACT
        )

    def payload(self, request: GenerationInput) -> dict[str, Any]:
        return context_payload(request)

    def parse(self, raw: str, request: GenerationInput) -> dict[str, Any]:
        stem, content = parse_note_output(raw)
        check_note(
            stem,
            content,
            expected_type="reference",
            stem_pattern=REFERENCE_STEM_RE,
            required=("title", "date"),
        )
        return {
            "filename_stem": stem,
            "content": content,
            # 경로는 시스템이 조립한다 — 화면이 "어디에 저장될지"를 보여줄 수 있게 함께 담는다.
            # `reference/` 는 flat — 하위 폴더가 없다.
            "target_path": f"reference/{stem}.md",
        }

"""`source_note` 스테이지 — reference 초안 (KDEV-WORK-015 P1 / SPEC-008 stage 4).

출처 기록층 노트 하나를 만든다. 개념 상세는 여기 쓰지 않고 concept 노트에 위임한다
— 그 규칙은 프롬프트가 아니라 `rules/knowledge-note-pipeline.md` 에 있다.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ..gates import GenerationInput, GenerationResult
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


class SourceNoteStage:
    """open-kknaks 로 reference 초안을 만든다."""

    def __init__(
        self,
        client,
        *,
        repo_root: Path,
        provider: str,
        model: str | None,
        work_dir: str | None,
        timeout_seconds: float = 900,
    ) -> None:
        self.client = client
        self.repo_root = repo_root
        self.provider = provider
        self.model = model
        self.work_dir = work_dir
        self.timeout_seconds = timeout_seconds

    async def __call__(self, request: GenerationInput) -> GenerationResult:
        group = _group_of(request.route)

        payload: dict[str, Any] = {
            **context_payload(request),
            "group": group,
        }
        prompt = INSTRUCTION.format(
            rules=READ_THE_RULES.format(template="reference.md"), output=OUTPUT_CONTRACT
        )

        options: dict[str, Any] = {"cwd": self.work_dir} if self.work_dir else {}
        if request.session_ref:
            options["resume"] = {"mode": "session", "session_id": request.session_ref}

        task_id = await self.client.submit(
            prompt + "\n\n" + json.dumps(payload, ensure_ascii=False),
            provider=self.provider,
            model=self.model,
            options=options or None,
            max_retries=2,
            metadata={"source": "pipeline-source-note", "item_id": request.item.id},
        )
        task = await self.client.result(task_id, timeout=self.timeout_seconds)
        if task is None or not task.result:
            raise RuntimeError(getattr(task, "error", None) or "open_kknaks returned no result")

        stem, content = parse_note_output(str(task.result))
        check_note(
            stem,
            content,
            expected_type="reference",
            stem_pattern=REFERENCE_STEM_RE,
            required=("title", "date"),
        )
        return GenerationResult(
            payload={
                "filename_stem": stem,
                "content": content,
                "group": group,
                # 경로는 시스템이 조립한다 — 화면이 "어디에 저장될지"를 보여줄 수 있게 함께 담는다.
                "target_path": f"reference/{group}/{stem}.md",
            },
            session_ref=getattr(task, "result_session_id", None),
            external_task_ref=str(task_id),
        )


def _group_of(route_payload: dict[str, Any] | None) -> str:
    destinations = (route_payload or {}).get("destinations") or {}
    return str((destinations.get("reference") or {}).get("group") or "study")

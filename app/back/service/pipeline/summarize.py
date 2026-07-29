"""요약 스테이지 — route 판단의 근거를 만든다 (KDEV-WORK-014 P2 / KDEV-SPEC-008 stage 2).

여기서 만드는 것은 **노트가 아니다.** 자료를 어디로 보낼지(reference·concept·파생)
사람이 정하기 위해 읽는 판단 재료다. 그래서 형식 규칙(`rules/knowledge-note-pipeline.md`,
`templates/knowledge/`)을 참조하지 않는다 — 노트를 쓰는 단계는 route 승인 뒤다.

AI 호출은 open-kknaks 를 거친다. Anthropic SDK 를 직접 import 하지 않는다(OKK ADR-04).
"""

from __future__ import annotations

import json
from typing import Any

from .executor import Execution, poll_execution

PROMPT = """다음 자료를 읽고, 이 자료를 어떻게 정리할지 사람이 판단할 수 있도록 요약하라.

노트를 작성하는 것이 아니다. 아래 네 가지만 한국어로 간결하게 쓴다.

1. 이 자료가 무엇에 대한 것인가 (2~3문장)
2. 핵심 주장 3~5개 (자료의 주장으로서 정리한다. 네 판단을 섞지 않는다)
3. 뽑을 만한 개념 후보 (이름 + 한 줄). 없으면 "없음"
4. 자료의 성격 — 1차 자료 / 의견글 / 홍보물 중 무엇에 가까운가와 그 근거

마크다운 산문으로 답한다. JSON 이나 코드펜스로 감싸지 않는다."""


def _trim(material: Any, limit: int) -> Any:
    """긴 자막·본문을 자른다 — 프롬프트 상한을 넘겨 통째로 실패하는 편보다 낫다."""
    if not isinstance(material, dict):
        return material
    content = material.get("content")
    if isinstance(content, str) and len(content) > limit:
        return {**material, "content": content[:limit], "content_truncated": True}
    return material


class AgentSummarizer:
    """open-kknaks 로 요약을 만든다 — **제출과 수확이 나뉜다** (KDEV-WORK-016 P2).

    게이트 스테이지(`AgentStage`)와 같은 계약이지만 입력이 다르다. 요약은 게이트가
    아니라서 `GenerationInput` 이 없고 수집 결과와 메모만 받는다. 그 하나 때문에
    억지로 같은 기반 클래스에 넣지 않는다 — 폴링만 함께 쓴다.
    """

    def __init__(
        self,
        client,
        *,
        provider: str,
        model: str | None,
        work_dir: str | None,
        timeout_seconds: float = 600,
        content_limit: int = 120_000,
    ) -> None:
        self.client = client
        self.provider = provider
        self.model = model
        self.work_dir = work_dir
        self.timeout_seconds = timeout_seconds
        self.content_limit = content_limit

    async def submit(self, *, material: Any, note: str | None) -> str:
        payload = {
            "source_material": _trim(material, self.content_limit),
            "note": note,
            # 원문을 못 받아 메모로 대체했는지 알려준다 — 근거의 성격이 다르다.
            "material_source": "fetched" if material is not None else "note",
        }
        options = {"cwd": self.work_dir} if self.work_dir else None
        return await self.client.submit(
            PROMPT + "\n\n" + json.dumps(payload, ensure_ascii=False),
            provider=self.provider,
            model=self.model,
            options=options,
            max_retries=2,
            metadata={"source": "pipeline-summarize"},
        )

    async def poll(self, task_id: str) -> Execution:
        return await poll_execution(
            self.client, task_id, timeout_seconds=self.timeout_seconds
        )

    def parse(self, raw: str) -> str:
        summary = (raw or "").strip()
        if not summary:
            # 빈 요약을 성공으로 넘기면 route 게이트가 근거 없이 판단한다.
            raise RuntimeError("open_kknaks returned no summary")
        return summary

"""잔디 LLM 종합 — Claude Haiku 4.5 via open-kknaks (spec-03 §3, ADR-04)."""

from __future__ import annotations

import json
import logging
from datetime import date

from open_kknaks import ClaudeClient

logger = logging.getLogger("kknaks-back.llm")

LLM_MODEL = "claude-haiku-4-5-20251001"
LLM_TIMEOUT_S = 120
ALLOWED_KINDS = {"commit", "note", "study"}


def _build_prompt(
    today: date,
    narrative: str | None,
    notes: list[dict],
    contents: list[dict],
    commits: list[dict],
) -> str:
    """spec-03 §3.2 프롬프트 빌드."""
    bullets_notes = (
        "\n".join(f"- {n.get('subject', '')}" for n in notes) or "(없음)"
    )
    bullets_contents = (
        "\n".join(f"- {c.get('subject', '')}" for c in contents) or "(없음)"
    )
    bullets_commits = (
        "\n".join(
            f"- [{c.get('repo', '')}] {(c.get('msg', '') or '').splitlines()[0] if c.get('msg') else ''}"
            for c in commits
        )
        or "(없음)"
    )
    narrative_block = (
        f"[본인 narrative — 1순위 입력]\n{narrative}\n"
        if narrative
        else "[본인 narrative]\n(오늘 daily/*.md 미작성 — 사실 데이터로만 요약)\n"
    )
    return f"""오늘({today.isoformat()}) 한 사람의 활동 데이터다.
narrative는 본인 시각의 컨텍스트(1순위 입력), 나머지 3개는 kind 후보다.

{narrative_block}
[kind 후보 1 — note] notes 변경
{bullets_notes}

[kind 후보 2 — study] contents 변경
{bullets_contents}

[kind 후보 3 — commit] GitHub 외부 커밋
{bullets_commits}

다음을 결정해라:
1. kind: "commit" | "note" | "study" 중 가장 의미 있는 활동의 kind. 세 후보 모두 비어있으면 null
2. count: notes + contents + commits 항목 수의 합 (narrative는 셈에서 제외)
3. summary: 무슨 작업을 했는지 한국어/영어 한 줄 (각각 60자 이내, 자연스러운 어투)

응답은 다음 JSON 한 객체만 (다른 텍스트 X, 코드블록 ```json``` 도 박지 않음):
{{"kind": "...", "count": 0, "summary": {{"ko": "...", "en": "..."}}}}
"""


def _extract_json(text: str) -> str:
    """LLM 응답에서 JSON 객체만 추출 (Claude 가 종종 ```json ... ``` 코드블록 박음)."""
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end > start:
        return text[start : end + 1]
    return text


def validate_llm_response(resp: dict, expected_count: int) -> dict:
    """spec-03 §3.3 — 응답 검증.

    kind 가 ALLOWED 밖이면 None fallback (Claude 가 종종 빠뜨림).
    count 는 LLM 응답 무시하고 expected_count (실 입력 합계) 박아 idempotent 보장.
    """
    kind = resp.get("kind")
    summary = resp.get("summary")

    if kind not in ALLOWED_KINDS:
        logger.warning("kind=%r not in %s — fallback to None", kind, ALLOWED_KINDS)
        kind = None

    if summary is not None:
        if not (
            isinstance(summary, dict)
            and "ko" in summary
            and "en" in summary
        ):
            raise ValueError("invalid_summary")

    return {"kind": kind, "count": expected_count, "summary": summary}


async def summarize_activity(
    today: date,
    narrative: str | None,
    notes: list[dict],
    contents: list[dict],
    commits: list[dict],
    client: ClaudeClient,
) -> dict:
    """입력 4개 → kind/count/summary 결정 — open-kknaks 실 호출 (spec-03 §3.2)."""
    total = len(notes) + len(contents) + len(commits)
    if total == 0:
        # 활동 없음 — LLM 호출 skip
        return {"kind": None, "count": 0, "summary": None}

    prompt = _build_prompt(today, narrative, notes, contents, commits)
    task_id = await client.submit(
        prompt=prompt,
        model=LLM_MODEL,
        timeout=LLM_TIMEOUT_S,
        max_retries=2,
    )
    task = await client.result(task_id, timeout=LLM_TIMEOUT_S)
    resp = json.loads(_extract_json(task.result or ""))
    return validate_llm_response(resp, expected_count=total)

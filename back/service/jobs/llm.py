"""LLM 종합 — Claude Haiku 4.5 via open-kknaks (spec-03 §3, ADR-04).

STUB — 내일 open-kknaks ClaudeClient 호출로 교체.
현재는 mock 응답 (휴리스틱 kind 결정).
"""

from __future__ import annotations

from datetime import date


def summarize_activity(
    today: date,
    narrative: str | None,
    notes: list[dict],
    contents: list[dict],
    commits: list[dict],
) -> dict:
    """입력 4개 → kind/count/summary 결정.

    Stub 휴리스틱:
    - count = notes + contents + commits 합 (narrative 제외 — spec-03 §3.2)
    - kind 우선순위: study > note > commit > null
    - summary = 활동 수 한 줄 요약 (mock)
    """
    # TODO: ADR-04 — `await client.submit(prompt, model="claude-haiku-4-5-20251001", ...)` — spec-03 §3.2
    total = len(notes) + len(contents) + len(commits)
    if total == 0:
        return {"kind": None, "count": 0, "summary": None}

    if contents:
        kind = "study"
    elif notes:
        kind = "note"
    else:
        kind = "commit"

    return {
        "kind": kind,
        "count": total,
        "summary": {
            "ko": f"[mock] 오늘 {total}개 활동 ({kind})",
            "en": f"[mock] {total} activities today ({kind})",
        },
    }

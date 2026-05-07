"""잔디 LLM 종합 — Claude Haiku 4.5 via open-kknaks (spec-03 §3, ADR-04, ADR-06).

새 flow (ADR-06):
- counts 는 코드가 deterministic 으로 계산 (LLM 안 받음)
- LLM 은 body (≤500자 markdown narrative) + summary (ko/en 한 줄) 만 생성
- 결과는 daily/{date}.md 에 frontmatter (auto/counts/summary) + body 로 박힘
"""

from __future__ import annotations

import json
import logging
from datetime import date

from open_kknaks import ClaudeClient

logger = logging.getLogger("kknaks-back.llm")

LLM_MODEL = "claude-haiku-4-5-20251001"
LLM_TIMEOUT_S = 120
BODY_HARD_LIMIT = 600  # 500자 룰 + 100자 grace


def _format_notes_block(notes_changes: list[dict]) -> str:
    """notes 변경 파일들 → bullet block (id + 본문 발췌)."""
    if not notes_changes:
        return "(없음)"
    parts = []
    for n in notes_changes:
        fm = n.get("frontmatter", {}) or {}
        nid = fm.get("id") or n.get("path", "")
        title = fm.get("title", "")
        body_excerpt = (n.get("body") or "").strip()
        parts.append(f"### [{nid}] {title}\n{body_excerpt}")
    return "\n\n".join(parts)


def _format_contents_block(contents_changes: list[dict]) -> str:
    """contents 변경 파일들 → bullet block (id + 본문 발췌)."""
    if not contents_changes:
        return "(없음)"
    parts = []
    for c in contents_changes:
        fm = c.get("frontmatter", {}) or {}
        cid = fm.get("id") or c.get("path", "")
        title_ko = ""
        title = fm.get("title")
        if isinstance(title, dict):
            title_ko = title.get("ko", "") or title.get("en", "")
        elif isinstance(title, str):
            title_ko = title
        body_excerpt = (c.get("body") or "").strip()
        parts.append(f"### [{cid}] {title_ko}\n{body_excerpt}")
    return "\n\n".join(parts)


def _format_commits_block(commits: list[dict]) -> str:
    """GitHub commits → bullet block ([repo] msg 전체)."""
    if not commits:
        return "(없음)"
    parts = []
    for c in commits:
        repo = c.get("repo", "")
        msg = (c.get("msg") or "").strip()
        parts.append(f"- [{repo}]\n  {msg}")
    return "\n".join(parts)


def _build_prompt(
    target: date,
    notes_changes: list[dict],
    contents_changes: list[dict],
    commits: list[dict],
    counts: dict,
) -> str:
    """spec-03 §3.2 프롬프트 — counts 박고 (LLM 가 셈 안 함), body+summary 만 받음."""
    return f"""오늘({target.isoformat()}) 한 사람의 활동 데이터다.

활동 분포 (자동 집계):
- commits: {counts.get("commit", 0)}
- notes:   {counts.get("note", 0)}
- study:   {counts.get("study", 0)}

[notes 변경 — frontmatter id + 본문]
{_format_notes_block(notes_changes)}

[contents 변경 — frontmatter id + 본문]
{_format_contents_block(contents_changes)}

[GitHub commits — msg 전체]
{_format_commits_block(commits)}

다음 두 가지를 JSON 으로 출력해라:
1. summary: 활동 단위별 한 줄 요약 — list[str] (ko/en 각각).
   라벨 규칙 (한 활동 단위 = 한 줄, 활동 0 인 카테고리는 라인 생성 X):
     - GitHub commits: `[<repo>] 작업요약` — 같은 repo 의 여러 commit 은 1줄로 합침
     - notes 변경: `[notes] 항목 요약` — 전체 1줄로 합침
     - contents 변경: `[study] 항목 요약` — 전체 1줄로 합침
   각 줄 80자 이내, 자연스러운 어투.
2. body: ≤500자 markdown narrative. 다음 섹션 구조 그대로:

# 한 일

## commits
- [repo] msg 한 줄 + 의미 (1줄)

## notes
- [note-id] 한 줄 정리

## study
- [content-id] 키 takeaway

# 회고 / 다음
1~2줄. 추론 어렵면 비움.

각 섹션 항목 없으면 `- (없음)` 한 줄. body 전체는 frontmatter 제외 500자 이내로 압축.

응답은 다음 JSON 한 객체만 (다른 텍스트 X, 코드블록 ```json``` 도 박지 않음):
{{"summary": {{"ko": ["[repo] ...", "[notes] ..."], "en": ["[repo] ...", "[notes] ..."]}}, "body": "..."}}
"""


def _extract_json(text: str) -> str:
    """LLM 응답에서 JSON 객체만 추출 (Claude 가 종종 ```json ... ``` 코드블록 박음)."""
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end > start:
        return text[start : end + 1]
    return text


def validate_llm_response(resp: dict) -> dict:
    """spec-03 §3.3 — body+summary 검증.

    - summary: {"ko": list[str], "en": list[str]} 필수. 각 항목은 활동 단위 1줄 (`[repo] ...`).
    - body: str. BODY_HARD_LIMIT (=600자) 초과 시 truncate (soft enforcement, spec-03 §9)
    """
    summary = resp.get("summary")
    body = resp.get("body", "")

    if not (isinstance(summary, dict) and "ko" in summary and "en" in summary):
        raise ValueError("invalid_summary")
    for k in ("ko", "en"):
        v = summary[k]
        if not isinstance(v, list) or not all(isinstance(x, str) for x in v):
            raise ValueError(f"invalid_summary_{k}_not_list_str")
    if not isinstance(body, str):
        raise ValueError("invalid_body")
    if len(body) > BODY_HARD_LIMIT:
        logger.warning("body length=%d exceeds %d — truncate", len(body), BODY_HARD_LIMIT)
        body = body[:BODY_HARD_LIMIT] + "\n...(truncated)"
    return {"summary": summary, "body": body}


async def summarize_daily(
    target: date,
    notes_changes: list[dict],
    contents_changes: list[dict],
    commits: list[dict],
    counts: dict,
    client: ClaudeClient,
) -> dict:
    """입력 → body+summary (counts 는 deterministic 이라 LLM 안 거침). spec-03 §3.2.

    JSON 파싱 / 응답 검증 실패 시 LLM 1회 retry (spec-03 §9).
    """
    if sum(counts.values()) == 0:
        # 활동 0 — LLM 호출 skip
        return {"summary": None, "body": "(활동 없음)"}

    prompt = _build_prompt(target, notes_changes, contents_changes, commits, counts)

    last_error: Exception | None = None
    for attempt in range(2):  # spec-03 §9 — 1회 retry
        task_id = await client.submit(
            prompt=prompt,
            model=LLM_MODEL,
            timeout=LLM_TIMEOUT_S,
            max_retries=2,
        )
        task = await client.result(task_id, timeout=LLM_TIMEOUT_S)
        raw = task.result or ""
        try:
            resp = json.loads(_extract_json(raw))
            return validate_llm_response(resp)
        except (json.JSONDecodeError, ValueError) as e:
            last_error = e
            logger.warning(
                "LLM 응답 파싱/검증 실패 (attempt=%d/2): %s — raw[:200]=%r",
                attempt + 1,
                e,
                raw[:200],
            )
    raise RuntimeError(f"LLM 응답 파싱 2회 실패: {last_error}")

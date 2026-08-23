"""LLM gap-filler — spec-07 §7.1 (d). open-kknaks 1회 호출 (adr-04).

normalize 결과 (raw HTML + 솔루션 코드 + cases_input + core_lines + tags)
→ spec-07 yaml 6 키의 LLM 가공 영역 dict.

source-first 정신 — 정답 코드는 LLM 이 짓지 않음:
- logic.slots[].good = `good_line_index` (core_lines 의 정수 index) 로만 받음 — LLM 이 코드 string 출력 X
- trace.worked_example.input = `input_case_index` (cases_input 의 정수 index)
- distractor 코드는 LLM 생성 (정답 변형)
- HTML 파싱 (statement·constraints·io.output) 은 LLM 위임 (정형 파서 robust 안 함)

write.py 가 본 dict + normalize 결과 를 합쳐 최종 spec-07 yaml 트리 조립.
"""

from __future__ import annotations

import json
import logging
from typing import Any

from open_kknaks import AgentClient

logger = logging.getLogger("kknaks-back.algorithms.llm")

LLM_MODEL = "claude-haiku-4-5-20251001"
LLM_TIMEOUT_S = 180
RETRIES = 2  # 총 시도 = RETRIES (1차 + retries-1 재시도)


class LLMFillError(Exception):
    """LLM 응답이 schema 위반 또는 RETRIES 회 모두 실패."""


async def fill_gaps(
    normalized: dict, *, client: AgentClient, retries: int = RETRIES
) -> dict:
    """normalize 결과 → LLM 1회 호출 → 검증된 gap dict.

    Args:
        normalized: normalize_question() 결과.
        client: open-kknaks AgentClient (lifespan 에서 inject).
        retries: 파싱·검증 실패 시 재시도 횟수 (default 2).

    Raises:
        LLMFillError: retries 회 모두 실패.
    """
    prompt = _build_prompt(normalized)

    last_error: Exception | None = None
    last_raw = ""
    for attempt in range(retries):
        task_id = await client.submit(
            prompt=prompt,
            model=LLM_MODEL,
            options={"timeout_sec": LLM_TIMEOUT_S},
            max_retries=2,
        )
        task = await client.result(task_id, timeout=LLM_TIMEOUT_S)
        raw = task.result or ""
        last_raw = raw
        try:
            parsed = json.loads(_extract_json(raw))
            _validate_schema(parsed, normalized)
            return parsed
        except (json.JSONDecodeError, ValueError) as e:
            last_error = e
            logger.warning(
                "LLM 응답 파싱·검증 실패 (attempt=%d/%d): %s — raw[:200]=%r",
                attempt + 1,
                retries,
                e,
                raw[:200],
            )

    raise LLMFillError(
        f"fill_gaps {retries}회 실패: {last_error} | last_raw[:300]={last_raw[:300]!r}"
    )


def _extract_json(text: str) -> str:
    """LLM 응답에서 JSON 객체만 — 코드 펜스 / 둘러싼 prose 안전 처리."""
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end > start:
        return text[start : end + 1]
    return text


def _build_prompt(n: dict) -> str:
    """spec-07 §7.1 (d) prompt 조립.

    inputs (n 의 키): slug · title · difficulty · tags · hints · raw_html · params
                     · cases_input · code · core_lines · method_name · return_type
    """
    core_lines_block = (
        "\n".join(f"  [{i}] {line}" for i, line in enumerate(n["core_lines"]))
        if n["core_lines"]
        else "(missing — solution code unavailable, omit logic_slots)"
    )
    cases_block = (
        "\n".join(f"  [{i}] {case}" for i, case in enumerate(n["cases_input"]))
        if n["cases_input"]
        else "(missing)"
    )
    tags_str = ", ".join(n["tags"]) if n["tags"] else "(none)"
    code_block = n["code"] if n["code"] else "(missing — generate fallback)"

    is_design = bool(n.get("is_design"))
    if is_design:
        methods = n.get("methods") or []
        method_signatures = ", ".join(
            f"{m.get('name')}({', '.join(p.get('name', '?') for p in (m.get('params') or []))})"
            for m in methods
        ) or "(unknown)"
        case_format_line = (
            f"Test cases (LeetCode systemdesign format — each case = 2 lines: "
            f"operations array + per-op args array; class={n.get('classname')!r}, "
            f"methods={method_signatures}):"
        )
        design_note = f"""
[DESIGN PROBLEM — class-based]

This is a LeetCode `systemdesign` problem (class with multiple methods, state across calls).
- Class: {n.get("classname")}
- Methods: {method_signatures}
- core_lines above is the CONCAT of every method body in declaration order (e.g. __init__, then push, then pop, ...). One line index points to one line inside one method — logic_slots should reflect the data-structure invariant + each method's key step.
- Each test case is TWO lines: line 1 = operation name array (first op is the constructor, e.g. "MinStack"), line 2 = per-op argument arrays (matching length, [] for no-arg ops).
- For `io_outputs`: produce ONE string per case — a Python-list-shaped string of return values per operation (use "null" for void ops, including the constructor). Example for Min Stack 1 case of 8 ops: "[null, null, null, null, -3, null, 0, -2]".
- trace.worked_example.steps should narrate the operation sequence (op-by-op or grouped logically). The `answer` field should be the same shape as io_outputs[input_case_index].
"""
    else:
        case_format_line = (
            f"Test case inputs (parsed from LeetCode exampleTestcases — "
            f"index → text, params={n['params_count']}):"
        )
        design_note = ""

    return f"""You are filling content gaps for a coding interview practice problem (Korean & English bilingual).

Site: kknaks.dev — daily NeetCode 150 dojo for foreign coding interviews. The user is studying on a phone, no keyboard.
{design_note}
[INPUT — source-direct, do not modify]

slug: {n["slug"]}
title: {n["title"]}
difficulty: {n["difficulty"]}
tags: {tags_str}
LeetCode hints: {n["hints"]}

LeetCode raw HTML content:
'''
{n["raw_html"]}
'''

Solution code (neetcode-gh):
```python
{code_block}
```

Method core_lines (the algorithm body — index → text):
{core_lines_block}

{case_format_line}
{cases_block}


[YOUR JOB — produce a single JSON object]

1. **problem**:
   - title: {{"ko": str, "en": str}}  short topic ("Two Sum" style; KO can be same English or translated)
   - statement: {{"ko": str, "en": str}}  full problem statement converted from HTML to clean plain text. EXCLUDE the Examples and Constraints sections (handled separately as `io_outputs` and `constraints`). Preserve paragraph breaks. `en` = LeetCode source body with HTML tags removed (paragraph structure preserved). `ko` = natural Korean translation of `en` (faithful, paragraph structure preserved). Educational/personal use authorized — full text is OK.
   - constraints: list[str]  2-5 entries from the HTML <strong>Constraints:</strong> section. Concise (e.g. "2 ≤ nums.length ≤ 1e4").
   - io_outputs: list[str]  expected outputs corresponding 1:1 to the cases_input above (same length, same order).

2. **clarifying_items**: 5-8 items. Each:
   - q: {{"ko": str, "en": str}}  one-line question
   - type: "good" | "distractor"  (3+ good, 2-3 distractor)
   - why: {{"ko": str, "en": str}}  one-two sentences

3. **approach_items**: 3-5 items. Each:
   - name: {{"ko": str, "en": str}}  approach name (e.g. "Brute force", "Hash map (one-pass)")
   - complexity: str  (e.g. "O(n) time / O(n) space")
   - type: "good" | "distractor"  (1-2 good, 2-3 distractor)
   - why: {{"ko": str, "en": str}}

4. **logic_slots**: 4-7 slots. Each represents one step in the algorithm body. Each:
   - label: {{"ko": str, "en": str}}  (e.g. "초기화", "반복문", "분기 조건")
   - indent: 0|1|2  nesting depth visualization
   - good_line_index: int  INDEX into the core_lines array above. The good answer = source line at that index. DO NOT invent code.
   - good_why: {{"ko": str, "en": str}}
   - distractors: 2-3 items. Each {{"code": str, "why": {{"ko": str, "en": str}}}}. Distractor code MUST be a plausible *variation* of the good line (off-by-one, wrong data structure, swapped key/value, etc).

5. **trace_worked_example**:
   - input_case_index: int  index into cases_input above (usually 0)
   - steps: list of 2-4 items, each {{"ko": str, "en": str}}  free-form one-liner mental dry-run
   - answer: str  final return value for that input

6. **solution**:
   - complexity: {{"time": str, "space": str}}  (e.g. "O(n)", "O(n)")
   - followup: 1-3 items, each {{"ko": str, "en": str}}  variation / interviewer follow-up

[OUTPUT FORMAT]

Return EXACTLY ONE JSON object. No prose, no code fence, no markdown. Schema:

{{
  "problem": {{"title": {{"ko": "...", "en": "..."}}, "statement": {{"ko": "...", "en": "..."}}, "constraints": ["..."], "io_outputs": ["..."]}},
  "clarifying_items": [{{"q": {{"ko": "...", "en": "..."}}, "type": "good", "why": {{"ko": "...", "en": "..."}}}}],
  "approach_items": [{{"name": {{"ko": "...", "en": "..."}}, "complexity": "...", "type": "good", "why": {{"ko": "...", "en": "..."}}}}],
  "logic_slots": [{{"label": {{"ko": "...", "en": "..."}}, "indent": 0, "good_line_index": 0, "good_why": {{"ko": "...", "en": "..."}}, "distractors": [{{"code": "...", "why": {{"ko": "...", "en": "..."}}}}]}}],
  "trace_worked_example": {{"input_case_index": 0, "steps": [{{"ko": "...", "en": "..."}}], "answer": "..."}},
  "solution": {{"complexity": {{"time": "...", "space": "..."}}, "followup": [{{"ko": "...", "en": "..."}}]}}
}}
"""


# ---------- schema validation ----------


_TOP_KEYS = {
    "problem",
    "clarifying_items",
    "approach_items",
    "logic_slots",
    "trace_worked_example",
    "solution",
}


def _check_i18n(d: Any, label: str) -> None:
    if not (isinstance(d, dict) and "ko" in d and "en" in d):
        raise ValueError(f"{label}: must be {{ko, en}} dict")
    if not (isinstance(d["ko"], str) and isinstance(d["en"], str)):
        raise ValueError(f"{label}: ko/en must be string")


def _validate_schema(d: dict, normalized: dict) -> None:
    """Top-level keys + 각 섹션 핵심 필드 검증. spec-07 yaml 어셈블에 충분한지."""
    if not isinstance(d, dict):
        raise ValueError("response: not a dict")

    missing = _TOP_KEYS - set(d.keys())
    if missing:
        raise ValueError(f"missing top-level keys: {sorted(missing)}")

    # problem
    p = d["problem"]
    if not isinstance(p, dict):
        raise ValueError("problem: not a dict")
    _check_i18n(p.get("title"), "problem.title")
    _check_i18n(p.get("statement"), "problem.statement")
    cons = p.get("constraints")
    if not (isinstance(cons, list) and all(isinstance(x, str) for x in cons)):
        raise ValueError("problem.constraints: list[str] required")
    ios = p.get("io_outputs")
    if not (isinstance(ios, list) and all(isinstance(x, str) for x in ios)):
        raise ValueError("problem.io_outputs: list[str] required")
    if normalized.get("cases_input") and len(ios) != len(normalized["cases_input"]):
        raise ValueError(
            f"problem.io_outputs length {len(ios)} != cases_input length {len(normalized['cases_input'])}"
        )

    # clarifying / approach items
    for key, name in [("clarifying_items", "q"), ("approach_items", "name")]:
        items = d[key]
        if not (isinstance(items, list) and 3 <= len(items) <= 10):
            raise ValueError(f"{key}: list of 3–10 items required, got {len(items) if isinstance(items, list) else type(items).__name__}")
        for i, it in enumerate(items):
            if not isinstance(it, dict):
                raise ValueError(f"{key}[{i}]: not a dict")
            _check_i18n(it.get(name), f"{key}[{i}].{name}")
            if it.get("type") not in ("good", "distractor"):
                raise ValueError(f"{key}[{i}].type: must be 'good' or 'distractor'")
            _check_i18n(it.get("why"), f"{key}[{i}].why")

    # logic_slots — only if core_lines available
    slots = d["logic_slots"]
    if not isinstance(slots, list):
        raise ValueError("logic_slots: list required")
    core_count = len(normalized.get("core_lines") or [])
    if core_count > 0:
        if not (3 <= len(slots) <= 8):
            raise ValueError(f"logic_slots: 3–8 slots required, got {len(slots)}")
        for i, s in enumerate(slots):
            if not isinstance(s, dict):
                raise ValueError(f"logic_slots[{i}]: not a dict")
            _check_i18n(s.get("label"), f"logic_slots[{i}].label")
            if s.get("indent") not in (0, 1, 2, 3):
                raise ValueError(f"logic_slots[{i}].indent: must be 0|1|2|3")
            gli = s.get("good_line_index")
            if not (isinstance(gli, int) and 0 <= gli < core_count):
                raise ValueError(
                    f"logic_slots[{i}].good_line_index: must be 0..{core_count - 1}, got {gli}"
                )
            _check_i18n(s.get("good_why"), f"logic_slots[{i}].good_why")
            distractors = s.get("distractors")
            if not (isinstance(distractors, list) and 1 <= len(distractors) <= 4):
                raise ValueError(f"logic_slots[{i}].distractors: 1–4 items required")
            for j, dist in enumerate(distractors):
                if not isinstance(dist, dict):
                    raise ValueError(f"logic_slots[{i}].distractors[{j}]: not a dict")
                if not isinstance(dist.get("code"), str):
                    raise ValueError(f"logic_slots[{i}].distractors[{j}].code: str required")
                _check_i18n(dist.get("why"), f"logic_slots[{i}].distractors[{j}].why")

    # trace_worked_example
    twe = d["trace_worked_example"]
    if not isinstance(twe, dict):
        raise ValueError("trace_worked_example: not a dict")
    ici = twe.get("input_case_index")
    cases_count = len(normalized.get("cases_input") or [])
    if not (isinstance(ici, int) and 0 <= ici < cases_count):
        raise ValueError(
            f"trace_worked_example.input_case_index: must be 0..{cases_count - 1}, got {ici}"
        )
    steps = twe.get("steps")
    if not (isinstance(steps, list) and 1 <= len(steps) <= 6):
        raise ValueError("trace_worked_example.steps: list of 1–6 items required")
    for i, st in enumerate(steps):
        _check_i18n(st, f"trace_worked_example.steps[{i}]")
    if not isinstance(twe.get("answer"), str):
        raise ValueError("trace_worked_example.answer: str required")

    # solution
    sol = d["solution"]
    if not isinstance(sol, dict):
        raise ValueError("solution: not a dict")
    cx = sol.get("complexity")
    if not (
        isinstance(cx, dict)
        and isinstance(cx.get("time"), str)
        and isinstance(cx.get("space"), str)
    ):
        raise ValueError("solution.complexity: {time, space} strings required")
    fu = sol.get("followup")
    if not (isinstance(fu, list) and 1 <= len(fu) <= 5):
        raise ValueError("solution.followup: 1–5 items required")
    for i, f in enumerate(fu):
        _check_i18n(f, f"solution.followup[{i}]")

"""LLM gap-filler 결과 + normalize + sequence → 완성 md 파일 (spec-07 §7.1 e).

spec-07 §3 frontmatter + §4 본문 (`## Data` 단일 yaml 트리). 작업:
1. assemble_md — 인-메모리 dict 조립 (LLM gap → spec-07 yaml 형식 변환)
2. write_algorithm_md — 새 파일 + today=true 박음
3. clear_today_flag — 이전 today=true 항목들 false 로 갱신 (spec-03 §11.5)

main.py orchestrator 가 위 3 함수 호출 후 git commit/push (spec-03 §5).
"""

from __future__ import annotations

import datetime
import logging
from pathlib import Path
from typing import Any

import frontmatter
import yaml

from .sequence import SequenceItem

logger = logging.getLogger(__name__)


def assemble_md(
    *,
    a_id: str,
    sequence_item: SequenceItem,
    normalized: dict,
    llm_result: dict,
    target_date: datetime.date,
    today: bool = True,
) -> str:
    """input 들 → 완성된 md 파일 string (frontmatter + body).

    spec-07 §3 frontmatter (id·type·title·date·day·source·difficulty·tags·today·status·visible) +
    §4 본문 `## Data` 단일 yaml 블록 (problem·clarifying·approach·logic·trace·solution).

    Args:
        a_id: "A-002" 같은 항목 id.
        sequence_item: NeetCode 150 시퀀스 항목 (slug·number·pattern 등).
        normalized: normalize_question() 결과 (code·core_lines·cases_input 포함).
        llm_result: fill_gaps() 결과 (LLM 가공 dict).
        target_date: 박는 날짜 (frontmatter date·created·updated).
        today: 새 항목의 today 필드 (default True — spec-07 §3).
    """
    day_num = _parse_day_num(a_id)
    title = llm_result["problem"]["title"]

    # ---------- frontmatter ----------
    fm = {
        "id": a_id,
        "type": "algorithm",
        "title": title,
        "date": target_date.isoformat(),
        "day": f"Day {day_num:02d}",
        "source": {
            "platform": "leetcode",
            "number": sequence_item.number,
            "slug": sequence_item.slug,
            "url": f"https://leetcode.com/problems/{sequence_item.slug}/",
            "curated_in": ["neetcode150"],
        },
        "difficulty": normalized.get("difficulty", "easy"),
        "tags": normalized.get("tags", []),
        "today": today,
        "status": "draft",
        "visible": True,
        "created": target_date.isoformat(),
        "updated": target_date.isoformat(),
    }

    # ---------- body data tree (spec-07 §5) ----------
    cases_input: list[str] = normalized.get("cases_input", []) or []
    io_outputs: list[str] = llm_result["problem"]["io_outputs"]
    core_lines: list[str] = normalized.get("core_lines", []) or []
    code_str: str = normalized.get("code") or ""

    # problem.io — cases_input + io_outputs 짝 맞춤
    io_pairs = [
        {"input": cases_input[i], "output": io_outputs[i]}
        for i in range(min(len(cases_input), len(io_outputs)))
    ]

    # logic.slots — good_line_index → core_lines[idx] (lstripped)
    logic_slots = []
    for slot in llm_result.get("logic_slots", []):
        gli = slot["good_line_index"]
        good_code = core_lines[gli].lstrip() if 0 <= gli < len(core_lines) else ""
        options: list[dict[str, Any]] = [
            {"code": good_code, "type": "good", "why": slot["good_why"]}
        ]
        for d in slot.get("distractors", []):
            options.append(
                {"code": d["code"], "type": "distractor", "why": d["why"]}
            )
        logic_slots.append(
            {
                "label": slot["label"],
                "indent": slot["indent"],
                "options": options,
            }
        )

    # trace
    code_lines = code_str.splitlines() if code_str else []
    trace_cases = [
        {"input": cases_input[i], "expected": io_outputs[i]}
        for i in range(min(len(cases_input), len(io_outputs)))
    ]
    twe = llm_result["trace_worked_example"]
    ici = twe["input_case_index"]
    trace_worked = {
        "input": cases_input[ici] if 0 <= ici < len(cases_input) else "",
        "steps": twe["steps"],
        "answer": twe["answer"],
    }

    # solution
    solution_block = {
        "code": code_str,
        "complexity": llm_result["solution"]["complexity"],
        "followup": llm_result["solution"]["followup"],
    }

    data_tree = {
        "problem": {
            "title": title,
            "statement": llm_result["problem"]["statement"],
            "constraints": llm_result["problem"]["constraints"],
            "io": io_pairs,
        },
        "clarifying": {
            "items": [
                {"q": it["q"], "type": it["type"], "why": it["why"]}
                for it in llm_result["clarifying_items"]
            ]
        },
        "approach": {
            "items": [
                {
                    "name": it["name"],
                    "complexity": it["complexity"],
                    "type": it["type"],
                    "why": it["why"],
                }
                for it in llm_result["approach_items"]
            ]
        },
        "logic": {"format": "slot", "slots": logic_slots},
        "trace": {
            "code": code_lines,
            "cases": trace_cases,
            "worked_example": trace_worked,
        },
        "solution": solution_block,
    }

    # ---------- compose md ----------
    yaml_block = yaml.safe_dump(
        data_tree,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
        width=1000,  # 긴 문자열 줄바꿈 회피
    )
    h1 = title.get("ko") or title.get("en") or sequence_item.title
    body = f"# {h1}\n\n## Data\n\n```yaml\n{yaml_block}```\n"
    post = frontmatter.Post(content=body, **fm)
    return frontmatter.dumps(post)


def write_algorithm_md(
    *,
    a_id: str,
    sequence_item: SequenceItem,
    normalized: dict,
    llm_result: dict,
    target_date: datetime.date,
    persona_dir: Path,
) -> Path:
    """assemble_md → file write. 새 파일 today=true (spec-07 §3).

    Returns:
        새로 박은 md 파일 path.
    """
    algos = persona_dir / "algorithms"
    algos.mkdir(parents=True, exist_ok=True)

    content = assemble_md(
        a_id=a_id,
        sequence_item=sequence_item,
        normalized=normalized,
        llm_result=llm_result,
        target_date=target_date,
        today=True,
    )
    new_path = algos / f"{a_id}-{sequence_item.slug}.md"
    new_path.write_text(content, encoding="utf-8")
    logger.info("wrote algorithm md: %s", new_path)
    return new_path


def clear_today_flag(persona_dir: Path, *, except_path: Path | None = None) -> list[Path]:
    """이전 today=true 항목들 → false. spec-03 §11.5.

    Args:
        except_path: 이 path 는 건너뜀 (방금 박은 새 파일).

    Returns:
        갱신된 path 리스트 (commit 시 paths 에 합류).
    """
    algos = persona_dir / "algorithms"
    if not algos.is_dir():
        return []

    changed: list[Path] = []
    for p in sorted(algos.glob("A-*.md")):
        if except_path is not None and p.resolve() == except_path.resolve():
            continue
        try:
            post = frontmatter.load(p)
        except Exception as e:  # noqa: BLE001 — frontmatter 파싱 실패 graceful skip
            logger.warning("clear_today_flag: skip %s (parse error: %s)", p.name, e)
            continue
        if post.metadata.get("today") is True:
            post.metadata["today"] = False
            p.write_text(frontmatter.dumps(post), encoding="utf-8")
            changed.append(p)
            logger.info("today=false set on %s", p.name)
    return changed


def _parse_day_num(a_id: str) -> int:
    """'A-002' → 2."""
    parts = a_id.split("-")
    if len(parts) >= 2:
        try:
            return int(parts[1])
        except ValueError:
            return 0
    return 0

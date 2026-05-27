"""raw fetch 결과 → LLM prompt 입력용 정규화 (spec-07 §7.1 c).

deterministic 작업만 (HTML 파싱·constraints·output 추출 X — LLM 책임).
- metaData JSON.loads → params count (or design 분기 — `systemdesign: true` / `classname`)
- exampleTestcases newline split → 일반 = params count 줄씩 / design = 2 줄씩 ([ops]\n[args])
- difficulty .lower()
- topicTags slug 그대로
- 솔루션 코드의 본체 inner 라인 set 식별 (adr-08 §2.4)
  - 일반: `class Solution: def methodName` 첫 메서드 본체
  - design: `class <classname>` 의 모든 메서드 (__init__ 포함) 본체 concat

본 모듈 의 출력 dict 가 §7.1 (d) LLM 호출의 입력이 됨.
"""

from __future__ import annotations

import ast
import json
import logging
from typing import Any

logger = logging.getLogger(__name__)


def normalize_question(question: dict, code: str | None) -> dict[str, Any]:
    """fetch 결과 → LLM 입력용 정규화 dict.

    Args:
        question: fetch_leetcode 의 raw 응답.
        code: fetch_neetcode_gh 의 솔루션 코드. None 이면 LLM fallback (logic·solution).

    Returns dict — 모든 키 LLM prompt 에 그대로 박힘.
    """
    metadata_raw = question.get("metaData") or "{}"
    try:
        metadata = json.loads(metadata_raw)
    except json.JSONDecodeError as e:
        logger.warning("metaData JSON decode failed: %s — falling back to empty", e)
        metadata = {}

    classname = metadata.get("classname")
    is_design = bool(metadata.get("systemdesign") or classname)

    if is_design:
        params: list = []
        params_count = 2  # design = [operations]\n[args] 2 줄/case
        method_name = classname
        return_type = "design"
        core_lines = _extract_core_lines_design(code, classname) if code else []
    else:
        params = metadata.get("params") or []
        params_count = len(params)
        method_name = metadata.get("name")
        return_type = (metadata.get("return") or {}).get("type")
        core_lines = _extract_core_lines(code) if code else []

    return {
        "slug": question.get("titleSlug"),
        "number": _to_int(question.get("questionFrontendId")),
        "title": question.get("title"),
        "difficulty": (question.get("difficulty") or "").lower(),
        "tags": [t["slug"] for t in (question.get("topicTags") or []) if "slug" in t],
        "hints": question.get("hints") or [],
        "raw_html": question.get("content") or "",
        "params": params,
        "params_count": params_count,
        "method_name": method_name,
        "return_type": return_type,
        "is_design": is_design,
        "classname": classname,
        "methods": metadata.get("methods") if is_design else None,
        "cases_input": _split_testcases(question.get("exampleTestcases") or "", params_count),
        "code": code,
        "core_lines": core_lines,
    }


def _to_int(v: Any) -> int | None:
    if v is None:
        return None
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


def _split_testcases(raw: str, params_count: int) -> list[str]:
    """exampleTestcases newline string → 1 case 당 1 string (params_count 줄 join).

    예: params_count=2, raw='[2,7,11,15]\\n9\\n[3,2,4]\\n6\\n[3,3]\\n6'
        → ['[2,7,11,15]\\n9', '[3,2,4]\\n6', '[3,3]\\n6']
    """
    if not raw or params_count <= 0:
        return []
    lines = raw.split("\n")
    cases: list[str] = []
    for i in range(0, len(lines), params_count):
        chunk = lines[i : i + params_count]
        if len(chunk) == params_count:
            cases.append("\n".join(chunk))
    return cases


def _extract_core_lines(code: str) -> list[str]:
    """class Solution: def methodName(...) 의 body 라인 추출.

    adr-08 §2.4 — core region = 함수 본체 inner. signature·class line 제외.
    공백 라인 / 주석-only 라인 제외 — slot 후보가 되지 못하므로.

    Returns:
        list of code line strings (non-blank, non-comment-only).
        AST 파싱 실패 또는 class Solution 미발견 시 [].
    """
    if not code or not code.strip():
        return []

    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        logger.warning("solution code AST parse failed: %s", e)
        return []

    code_lines = code.splitlines()

    # class Solution 의 첫 method body 추출
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == "Solution":
            for member in node.body:
                if isinstance(member, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if not member.body:
                        return []
                    start = member.body[0].lineno  # 1-indexed
                    end = member.end_lineno or len(code_lines)
                    body = code_lines[start - 1 : end]
                    return [
                        line
                        for line in body
                        if line.strip() and not line.lstrip().startswith("#")
                    ]
    # class Solution 미발견 → fallback: top-level def
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if not node.body:
                return []
            start = node.body[0].lineno
            end = node.end_lineno or len(code_lines)
            body = code_lines[start - 1 : end]
            return [
                line for line in body if line.strip() and not line.lstrip().startswith("#")
            ]
    return []


def _extract_core_lines_design(code: str, classname: str | None) -> list[str]:
    """class <classname> 의 모든 메서드 (__init__ 포함) 본체 라인 concat.

    design 문제 (Min Stack·LRU Cache 등) — 단일 메서드가 없고 클래스 전체가 알고리즘.
    각 메서드 본체를 순서대로 이어붙여 LLM 이 step slot 으로 분해할 수 있게 한다.
    공백 라인 / 주석-only 라인 제외 (slot 후보 X).

    Args:
        code: neetcode-gh 솔루션 코드.
        classname: metaData.classname (e.g. "MinStack"). None 이면 fallback — 첫 class.

    Returns:
        list of code line strings (non-blank, non-comment-only).
        AST 실패 또는 class 미발견 시 [].
    """
    if not code or not code.strip():
        return []

    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        logger.warning("design solution code AST parse failed: %s", e)
        return []

    code_lines = code.splitlines()
    target_class: ast.ClassDef | None = None
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            if classname is None or node.name == classname:
                target_class = node
                break
    if target_class is None:
        return []

    result: list[str] = []
    for member in target_class.body:
        if not isinstance(member, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if not member.body:
            continue
        start = member.body[0].lineno
        end = member.end_lineno or len(code_lines)
        body = code_lines[start - 1 : end]
        result.extend(
            line
            for line in body
            if line.strip() and not line.lstrip().startswith("#")
        )
    return result

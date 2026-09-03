"""답변 객체 파싱·검증 — SPEC-005 §4 가 SoT.

**게이트 5 가 사는 자리다.** LLM 이 낸 텍스트에서 객체를 꺼내고, 그 객체가 계약을
지키는지 서버가 판정한다. 판정은 세 축이다:

1. **스키마** — 필수 필드 존재·타입·개수 상한.
2. **`used_edges` ⊆ 확정 엣지** — `ontology_edges` 에 실존하고 판정이
   `채택`·`자동 확정`·`선언` 인 것만. 보류·기각은 `excluded_edges` 로만 간다.
3. **`citations` 역추적** — `source.table`·`source.column` 으로 **DB 를 다시 읽어**
   값이 같은지 본다. 곱셈으로 만든 추정치는 여기서 성립하지 않는다.

LLM 을 믿고 통과시키는 자리가 아니다 — 위반은 예외이고, 소비자가 `ai_schema_retry` 만큼
재제출한 뒤 그래도 안 되면 `failed` 로 마감한다(SPEC-005 OQ-5).
"""

from __future__ import annotations

import json
import re
import sqlite3
from dataclasses import dataclass, field
from typing import Any

from service import allowlist as al

#: 인과 서술에 쓸 수 있는 판정. SPEC-001 §4 의 값을 그대로 쓴다.
CAUSAL_VERDICTS = frozenset({"채택", "자동 확정", "선언"})

#: `followups` 상한 (SPEC-005 §4 Validation — 0~3개)
MAX_FOLLOWUPS = 3

#: PII 표기 — 마스킹된 값에는 이 문자들이 반드시 있다. 원값 검출의 보조 신호다.
_MASK_MARKS = ("○", "*")

_JSON_FENCE = re.compile(r"```(?:json)?\s*(\{.*?\})\s*```", re.DOTALL)


class AnswerSchemaError(ValueError):
    """스키마 위반. 소비자가 `settings.ai_schema_retry` 만큼 **재제출**하고,
    그래도 통과 못 하면 `failed` + `AI_FAILED` 다(SPEC-005 OQ-5).

    같은 텍스트를 다시 파싱하는 것은 결정적이라 의미가 없다 — 재시도는 재제출이다.
    """

    code = "SCHEMA_VIOLATION"

    def __init__(self, message: str, detail: list[str] | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.detail = detail or []

    def render(self) -> str:
        return "\n".join([f"{self.code}: {self.message}", *(f"  {d}" for d in self.detail)])


class EvidenceError(AnswerSchemaError):
    """게이트 5 위반 — 근거 무결성. 재시도 대상이지만 원인이 다르다."""

    code = "EVIDENCE_VIOLATION"


@dataclass
class ValidationReport:
    """검증 결과 — 통과해도 **무엇을 어떻게 확인했는지** 남긴다.

    게이트 5 의 증거가 「예외가 안 났다」로 끝나면 나중에 재현할 수 없다.
    """

    citations_checked: int = 0
    citation_matches: list[dict] = field(default_factory=list)
    used_edges_checked: int = 0
    drilldown_rows: int = 0
    pii_scanned_fields: int = 0
    #: PII 대조를 건너뛴 사유. None 이면 실제로 대조했다는 뜻이다 —
    #: 「검사했다」와 「검사 못 했다」가 리포트에서 구분돼야 한다(검수 W3).
    pii_skipped: str | None = None


def extract_answer_object(text: str) -> dict:
    """LLM 출력에서 답변 객체를 꺼낸다.

    ```json 펜스를 우선하고(프롬프트가 그렇게 지시한다), 없으면 마지막 균형 잡힌
    `{...}` 를 찾는다 — 모델이 펜스를 빠뜨리는 것은 흔하고, 그것 하나로 답변을
    버리는 것은 과하다. 둘 다 실패하면 스키마 위반이다.
    """
    if not text or not text.strip():
        raise AnswerSchemaError("빈 응답 — 답변 객체가 없다")

    candidates = [m.group(1) for m in _JSON_FENCE.finditer(text)]
    for raw in reversed(candidates):
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            return parsed

    fallback = _last_balanced_object(text)
    if fallback is not None:
        return fallback
    raise AnswerSchemaError(
        "응답에서 JSON 답변 객체를 찾지 못했다",
        [f"응답 길이 {len(text)}자 · ```json 펜스 {len(candidates)}개"],
    )


def _last_balanced_object(text: str) -> dict | None:
    """뒤에서부터 균형 잡힌 중괄호 덩어리를 찾는다. 문자열 안의 괄호는 세지 않는다."""
    for start in range(len(text) - 1, -1, -1):
        if text[start] != "{":
            continue
        depth, in_str, escaped = 0, False, False
        for i in range(start, len(text)):
            ch = text[i]
            if in_str:
                if escaped:
                    escaped = False
                elif ch == "\\":
                    escaped = True
                elif ch == '"':
                    in_str = False
                continue
            if ch == '"':
                in_str = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    try:
                        parsed = json.loads(text[start : i + 1])
                    except json.JSONDecodeError:
                        break
                    if isinstance(parsed, dict) and "answer" in parsed:
                        return parsed
                    break
    return None


# --- 스키마 -----------------------------------------------------------------


def validate_schema(obj: dict) -> None:
    """필수 필드·타입·상한. DB 를 보지 않는 순수 검사다."""
    problems: list[str] = []

    if not isinstance(obj.get("answer"), str) or not obj["answer"].strip():
        problems.append("answer 는 비어 있지 않은 문자열이어야 한다")

    pc = obj.get("premise_correction")
    if not isinstance(pc, dict):
        # 「교정 없음」도 `{"corrected": false}` 로 **항상 존재**해야 한다 —
        # 필드가 없는 것과 교정이 없는 것은 다른 사실이다.
        problems.append("premise_correction 은 항상 존재해야 한다(교정 없으면 corrected:false)")
    elif not isinstance(pc.get("corrected"), bool):
        problems.append("premise_correction.corrected 는 bool 이어야 한다")
    elif pc["corrected"]:
        for key in ("claimed", "actual", "restated_question"):
            if not isinstance(pc.get(key), str) or not pc[key].strip():
                problems.append(f"corrected:true 면 premise_correction.{key} 가 필수다")

    for key in ("used_edges", "citations"):
        if not isinstance(obj.get(key), list):
            problems.append(f"{key} 는 배열이어야 한다(해당 없으면 빈 배열)")

    for key in ("excluded_edges", "followups", "unknowns"):
        if key in obj and obj[key] is not None and not isinstance(obj[key], list):
            problems.append(f"{key} 는 배열이어야 한다")

    followups = obj.get("followups") or []
    if isinstance(followups, list) and len(followups) > MAX_FOLLOWUPS:
        problems.append(f"followups 는 {MAX_FOLLOWUPS}개 이하다(요청 {len(followups)})")

    for i, edge in enumerate(obj.get("used_edges") or []):
        if not isinstance(edge, dict):
            problems.append(f"used_edges[{i}] 는 객체여야 한다")
            continue
        for key in ("edge_id", "from", "to", "verdict"):
            if not edge.get(key):
                problems.append(f"used_edges[{i}].{key} 가 비었다")

    for i, cite in enumerate(obj.get("citations") or []):
        if not isinstance(cite, dict):
            problems.append(f"citations[{i}] 는 객체여야 한다")
            continue
        if "value" not in cite:
            problems.append(f"citations[{i}].value 가 없다")
        source = cite.get("source")
        if not isinstance(source, dict):
            problems.append(f"citations[{i}].source 가 없다")
        else:
            for key in ("tool", "table", "column"):
                if not source.get(key):
                    problems.append(f"citations[{i}].source.{key} 가 비었다")

    drill = obj.get("drilldown")
    if drill is not None:
        if not isinstance(drill, dict):
            problems.append("drilldown 은 객체여야 한다")
        else:
            for key in ("layer", "table", "view", "rows", "total"):
                if key not in drill:
                    problems.append(f"drilldown.{key} 가 없다")

    if problems:
        raise AnswerSchemaError(f"답변 객체 스키마 위반 {len(problems)}건", problems)


# --- 게이트 5 ---------------------------------------------------------------


def validate_evidence(
    conn: sqlite3.Connection, obj: dict, report: ValidationReport | None = None
) -> ValidationReport:
    """근거 무결성 — `used_edges` ⊆ 확정 · `citations` 재조회 · PII 0건."""
    report = report or ValidationReport()
    problems: list[str] = []

    _check_used_edges(conn, obj, problems, report)
    _check_citations(conn, obj, problems, report)
    _check_drilldown(conn, obj, problems, report)
    _check_pii(conn, obj, problems, report)

    if problems:
        raise EvidenceError(f"근거 무결성 위반 {len(problems)}건", problems)
    return report


def _check_used_edges(
    conn: sqlite3.Connection, obj: dict, problems: list[str], report: ValidationReport
) -> None:
    rows = {
        f"{r['cause']}__{r['effect']}": r["verdict"]
        for r in conn.execute("SELECT cause, effect, verdict FROM ontology_edges")
    }
    for edge in obj.get("used_edges") or []:
        report.used_edges_checked += 1
        edge_id = edge.get("edge_id")
        pair_id = f"{edge.get('from')}__{edge.get('to')}"
        if edge_id != pair_id:
            problems.append(f"used_edges: edge_id({edge_id})가 (from, to)와 어긋난다 → {pair_id}")
        actual = rows.get(edge_id)
        if actual is None:
            # 지어낸 엣지 — 관계를 프롬프트가 아니라 데이터에서 가져왔다면 있을 수 없다
            problems.append(f"used_edges: 존재하지 않는 엣지 {edge_id!r}")
            continue
        if actual not in CAUSAL_VERDICTS:
            problems.append(
                f"used_edges: 확정 엣지가 아니다 — {edge_id} 판정 {actual!r} "
                f"(보류·기각은 excluded_edges 로만 간다)")
        if edge.get("verdict") != actual:
            problems.append(
                f"used_edges: {edge_id} 판정 표기가 정본과 다르다 — "
                f"응답 {edge.get('verdict')!r} vs DB {actual!r}")


def _check_citations(
    conn: sqlite3.Connection, obj: dict, problems: list[str], report: ValidationReport
) -> None:
    """`source.table`·`column` 으로 다시 읽어 값이 실제로 존재하는지 본다.

    허용하는 대응은 셋이다 — ① 그 기간 단일 행의 값 ② 기간 값들의 합 ③ 기간 값 중 하나.
    셋 중 어느 것도 아니면 **도구가 주지 않은 수치**이고, 곱셈으로 만든 추정치가 여기서
    걸린다(정량 추정 금지 · 게이트 5-①).

    **`period` 는 기간이 있는 테이블에서 필수다.** 없으면 재조회 창이 컬럼 전체로 넓어져
    ②·③ 이 헐거워지고, 그러면 **지시를 어긴 응답이 더 느슨한 검사를 받는 역전**이 생긴다
    (검수 W2). 면제는 모델의 선택이 아니라 **테이블의 성질**로만 정한다 — 그레인 키가 없는
    관계(프로모션 캘린더·온톨로지·계층 뷰)는 좁힐 창 자체가 없으므로 면제다.
    """
    for i, cite in enumerate(obj.get("citations") or []):
        report.citations_checked += 1
        source = cite.get("source") or {}
        table, column = source.get("table"), source.get("column")
        value = cite.get("value")

        if not _is_allowed_relation(table):
            problems.append(f"citations[{i}]: 허용 목록 밖 출처 {table!r}")
            continue
        if not _column_exists(conn, table, column):
            problems.append(f"citations[{i}]: {table} 에 컬럼 {column!r} 이 없다")
            continue
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            # 문자열 수치("3.69억")는 재조회 대조가 성립하지 않는다 — claim 에 써야 한다
            problems.append(
                f"citations[{i}].value 는 숫자여야 한다(받은 값 {value!r}). "
                "반올림·단위 표기는 claim 에만 쓴다")
            continue

        period = cite.get("period")
        key = _period_key(table)
        if key is not None and not _has_period(period):
            # 기간이 있는 테이블인데 창을 안 줬다 — 넓은 창으로 봐주지 않고 거부한다
            problems.append(
                f"citations[{i}]: {table} 은 기간이 있는 테이블이라 "
                "period.start·period.end 가 필수다(창이 없으면 재조회가 컬럼 전체로 넓어진다)")
            continue

        values = _requery(conn, table, column, period)
        if not values:
            problems.append(f"citations[{i}]: 재조회 결과가 비었다 — {table}.{column}")
            continue
        windowed = key is not None
        matched = _match_rule(value, values, cite.get("row_count"), windowed=windowed)
        if matched is None:
            problems.append(
                f"citations[{i}]: 재조회 불일치 — {table}.{column} = {value!r} 는 "
                f"해당 구간 {len(values)}행에서 나오지 않는다(단일값·합계·행값 어느 것도 아님)")
            continue
        report.citation_matches.append(
            {"claim": cite.get("claim"), "value": value,
             "table": table, "column": column, "rule": matched, "rows": len(values),
             # 창을 좁혀서 맞춘 것인지 테이블 전체에서 맞춘 것인지 리포트에 남긴다 —
             # 「검사했다」와 「좁혀서 검사했다」는 다른 사실이다
             "window": "period" if windowed else "table"})


def _has_period(period: Any) -> bool:
    return isinstance(period, dict) and bool(period.get("start")) and bool(period.get("end"))


def _match_rule(
    value: float, values: list[float], row_count: Any = None, *, windowed: bool = True
) -> str | None:
    """가장 좁은 규칙부터 맞춰 본다.

    `row_value`(구간 안 어느 행과 같으면 통과)가 가장 헐거우므로,
    인용이 `row_count` 를 스스로 1이라고 적었을 때만 인정한다 — 「30행에서 나왔다」고
    적어 놓고 값이 그중 한 행과 우연히 같은 경우를 통과시키지 않는다(검수 nit 3).
    """
    if len(values) == 1 and _eq(value, values[0]):
        return "single_row"
    if _eq(value, sum(values)):
        return "sum"
    declared_single = isinstance(row_count, int) and not isinstance(row_count, bool) \
        and row_count == 1
    if declared_single and any(_eq(value, v) for v in values):
        return "row_value"
    return None


def _eq(a: float, b: float) -> bool:
    """오차 0 — 부동소수 표현 차이만 흡수한다(SPEC-005 Validation)."""
    if isinstance(a, int) and isinstance(b, int):
        return a == b
    return abs(float(a) - float(b)) < 1e-9


def _requery(
    conn: sqlite3.Connection, table: str, column: str, period: Any
) -> list[float]:
    key = _period_key(table)
    sql = f'SELECT "{column}" AS v FROM {table}'
    params: tuple = ()
    if key and isinstance(period, dict) and period.get("start") and period.get("end"):
        start, end = str(period["start"]), str(period["end"])
        if key in ("month", "cohort_month"):
            start, end = start[:7], end[:7]
        sql += f' WHERE "{key}" >= ? AND "{key}" <= ?'
        params = (start, end)
    return [r["v"] for r in conn.execute(sql, params)
            if r["v"] is not None and isinstance(r["v"], (int, float))]


def _period_key(table: str) -> str | None:
    for grain, relation in al.GRAIN_RELATION.items():
        if relation == table:
            return al.GRAIN_KEY[grain]
    return None


def _is_allowed_relation(table: str | None) -> bool:
    """허용 목록의 `relation` 만 출처가 될 수 있다 — 원 테이블 이름은 여기 없다."""
    if not table:
        return False
    return any(spec.relation == table for spec in al.TABLES.values())


def _column_exists(conn: sqlite3.Connection, table: str, column: str | None) -> bool:
    if not column:
        return False
    cols = {r[1] for r in conn.execute(f"PRAGMA table_info({table})")}
    return column in cols


def _check_drilldown(
    conn: sqlite3.Connection, obj: dict, problems: list[str], report: ValidationReport
) -> None:
    drill = obj.get("drilldown")
    if not isinstance(drill, dict):
        return
    view = drill.get("view")
    layer, table = drill.get("layer"), drill.get("table")
    spec = al.resolve(str(layer), str(table)) if layer and table else None
    if spec is None:
        problems.append(f"drilldown: 허용 목록 밖 대상 {layer!r}/{table!r}")
        return
    if view != spec.relation:
        # 원 테이블 산출을 실을 수 없다 — 마스킹 뷰 경유가 유일한 경로다
        problems.append(f"drilldown.view 가 마스킹 뷰가 아니다 — {view!r} (기대 {spec.relation})")
    rows = drill.get("rows") or []
    report.drilldown_rows = len(rows)
    if spec.masked_fields:
        missing = set(spec.masked_fields) - set(drill.get("masked_fields") or [])
        if missing:
            problems.append(f"drilldown.masked_fields 누락 {sorted(missing)}")


def _has_bronze(conn: sqlite3.Connection) -> bool:
    row = conn.execute(
        "SELECT COUNT(*) FROM sqlite_master WHERE type IN ('table','view') "
        "AND name = 'bronze_vegas_reservations'").fetchone()
    return bool(row and row[0])


def _check_pii(
    conn: sqlite3.Connection, obj: dict, problems: list[str], report: ValidationReport
) -> None:
    """답변 본문·인용·드릴다운 행에 원값이 있는가 (게이트 3 · SPEC-005 Validation).

    브론즈 원값 집합을 훑어 **실제로 존재하는 값**이 텍스트에 있는지 본다 —
    「마스킹 문자가 없다」가 아니라 「원값이 있다」로 판정해야 오탐이 안 난다.
    """
    haystacks: list[tuple[str, str]] = [("answer", str(obj.get("answer") or ""))]
    for i, cite in enumerate(obj.get("citations") or []):
        haystacks.append((f"citations[{i}].claim", str(cite.get("claim") or "")))
    drill = obj.get("drilldown")
    if isinstance(drill, dict):
        haystacks.append(("drilldown.rows", json.dumps(drill.get("rows") or [], ensure_ascii=False)))

    # 브론즈 존재를 **먼저 본다.** 예외를 삼키면 리포트에 스캔한 것처럼 남아
    # 「검사했다」와 「검사 못 했다」가 구분되지 않는다(검수 W3).
    if not _has_bronze(conn):
        report.pii_scanned_fields = 0
        report.pii_skipped = "브론즈 원값 테이블이 없어 대조를 건너뛰었다"
        return
    report.pii_scanned_fields = len(haystacks)

    names = {
        r[0] for r in conn.execute(
            "SELECT DISTINCT patientName FROM bronze_vegas_reservations "
            "WHERE patientName <> '' AND length(patientName) >= 2")
    }
    phones = {
        r[0] for r in conn.execute(
            "SELECT DISTINCT phone FROM bronze_vegas_reservations "
            "WHERE phone <> '' AND length(phone) >= 8")
    }

    for label, text in haystacks:
        if not text:
            continue
        for raw in names:
            if raw in text:
                problems.append(f"{label}: 환자 실명 원값 노출")
                break
        for raw in phones:
            if raw in text:
                problems.append(f"{label}: 전화 원값 노출")
                break


def validate(conn: sqlite3.Connection, obj: dict) -> ValidationReport:
    """스키마 → 근거 순으로 전부 검증한다. 통과하면 리포트를 돌려준다."""
    validate_schema(obj)
    return validate_evidence(conn, obj)

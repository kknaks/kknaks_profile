"""마스킹 뷰 `v_*` — 소비자가 브론즈·실버에 닿는 **유일한 경로**(DEC-002).

표기 형식은 SPEC-001 §4 가 SoT 다. 화면·API·에이전트 응답에 이 문자열이 그대로 나간다.

| 대상 | 표기 |
|---|---|
| `patientName` | `김○○` — 성 1자만 노출 |
| `phone` | `010-****-1234` — 가운데 마스킹, 앞 3자리·뒤 4자리 유지 |
| `birthday` | `1990-**-**` — 연도만 |
| 리뷰 본문 직원 실명 | `[직원]` — 기록 03·04 의 실명 사전 그대로 |
| 리뷰 작성자명 | 원천 표기 유지(이미 마스킹 닉네임) — 대상으로 **명시**만 |

뷰 정의에 실명 사전이 박힌다. DB 자체가 브론즈 원값을 갖는 PII 저장소이므로 경계는
「DB 밖으로 나가는 것」이고, 뷰가 그 경계다 — 사전이 DB 안에 남는 것은 그 경계 안쪽이다.
"""

from __future__ import annotations

import re
import sqlite3

from db.schema import REVIEW_HEADER_MAP, VEGAS_COLUMNS

MASK_TOKEN = "[직원]"

# 기록 04 리뷰 전처리 1단계와 같은 규칙 — vegas `staff` 고유값 중 실명형만.
NON_NAME = {"미지정"}
TITLE_SUFFIXES = ("부총괄실장", "총괄실장", "실장", "대표님", "원장님", "원장", "팀장", "부장")

VIEWS = [
    "v_bronze_vegas_reservations",
    "v_bronze_reviews",
    "v_silver_reservations",
    "v_silver_reviews",
]


def staff_names(conn: sqlite3.Connection) -> list[str]:
    """브론즈 vegas `staff` 에서 실명형 토큰을 뽑는다 — 기록 04 `reviews_prepare` 이식.

    긴 이름부터 치환해야 부분 일치로 짧은 토큰이 먼저 먹는 일이 없다.
    """
    values = {r[0] for r in conn.execute("SELECT DISTINCT staff FROM bronze_vegas_reservations")}
    names = set()
    for v in values:
        if v is None or v in NON_NAME or v.startswith("데스크"):
            continue
        token = v.split()[0] if v.split() else ""
        for suf in TITLE_SUFFIXES:
            if token.endswith(suf) and len(token) > len(suf):
                token = token[: -len(suf)]
                break
        if re.fullmatch(r"[가-힣]{2,4}", token):
            names.add(token)
    return sorted(names, key=len, reverse=True)


def _sql_literal(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def mask_name_sql(col: str) -> str:
    """`김○○` — 성 1자 + 나머지 글자수만큼 `○`.

    1자 이름은 성만 남기면 원값 그대로가 되므로 통째로 `○` 로 덮는다. 그렇게 두면
    게이트 3 의 값 집합 대조가 이를 `PII_LEAK` 으로 잡아 **마스킹이 아니라 빌드 실패**로
    끝난다 — 현재 데이터에 1자 이름이 없어 드러나지 않을 뿐이다.
    """
    return (
        f"CASE WHEN {col} IS NULL OR {col} = '' THEN {col} "
        f"WHEN length({col}) = 1 THEN '○' "
        f"ELSE substr({col}, 1, 1) || "
        f"replace(hex(zeroblob(length({col}) - 1)), '00', '○') END"
    )


def mask_phone_sql(col: str) -> str:
    """`010-****-1234`. 8자리 미만은 가운데가 없어 전체를 `*` 로 덮는다."""
    return (
        f"CASE WHEN {col} IS NULL OR {col} = '' THEN {col} "
        f"WHEN length({col}) >= 8 THEN substr({col}, 1, 3) || '-****-' || substr({col}, -4) "
        f"ELSE replace(hex(zeroblob(length({col}))), '00', '*') END"
    )


def mask_birthday_sql(col: str) -> str:
    """`1990-**-**` — 연도만."""
    return (
        f"CASE WHEN {col} IS NULL OR {col} = '' THEN {col} "
        f"WHEN length({col}) >= 4 THEN substr({col}, 1, 4) || '-**-**' "
        f"ELSE '' END"
    )


def mask_body_sql(col: str, names: list[str]) -> str:
    """실명 사전을 중첩 replace 로 감는다 — 긴 토큰이 바깥쪽(먼저 적용)."""
    expr = col
    for name in names:  # staff_names 가 길이 내림차순으로 준다
        expr = f"replace({expr}, {_sql_literal(name)}, {_sql_literal(MASK_TOKEN)})"
    return expr


def view_ddl(conn: sqlite3.Connection) -> list[str]:
    names = staff_names(conn)

    maskers = {
        "patientName": mask_name_sql,
        "phone": mask_phone_sql,
        "birthday": mask_birthday_sql,
    }
    vegas_select = []
    for col, _ in VEGAS_COLUMNS:
        quoted = '"' + col + '"'
        masker = maskers.get(col)
        vegas_select.append(masker(quoted) + " AS " + quoted if masker else quoted)

    review_select = []
    for _, col in REVIEW_HEADER_MAP:
        quoted = '"' + col + '"'
        if col == "body":
            review_select.append(mask_body_sql(quoted, names) + " AS " + quoted)
        else:
            # authorName 은 원천 표기 유지 — 대상 목록에 남기되 값은 그대로(SPEC-001 §4)
            review_select.append(quoted)

    return [
        "DROP VIEW IF EXISTS v_bronze_vegas_reservations",
        "CREATE VIEW v_bronze_vegas_reservations AS SELECT "
        + ", ".join(vegas_select)
        + " FROM bronze_vegas_reservations",
        "DROP VIEW IF EXISTS v_bronze_reviews",
        "CREATE VIEW v_bronze_reviews AS SELECT "
        + ", ".join(review_select)
        + " FROM bronze_reviews",
        # 실버는 가릴 원값이 없다(patientName·phone 미반입, birthday → age_band).
        # 그래도 뷰를 둔다 — 소비자가 계층에 상관없이 같은 진입점을 쓰게 하려는 것(OQ-4).
        "DROP VIEW IF EXISTS v_silver_reservations",
        "CREATE VIEW v_silver_reservations AS SELECT * FROM silver_reservations",
        "DROP VIEW IF EXISTS v_silver_reviews",
        "CREATE VIEW v_silver_reviews AS SELECT * FROM silver_reviews",
    ]


def build(conn: sqlite3.Connection) -> list[str]:
    from db.connection import atomic

    with atomic(conn, "views"):
        for stmt in view_ddl(conn):
            conn.execute(stmt)
    return VIEWS

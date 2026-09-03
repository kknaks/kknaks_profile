"""마스킹 뷰 `v_*` — 소비자가 브론즈·실버에 닿는 **유일한 경로**(DEC-002).

표기 형식은 SPEC-001 §4 가 SoT 다. 화면·API·에이전트 응답에 이 문자열이 그대로 나간다.

| 대상 | 표기 |
|---|---|
| `patientName` | `김○○` — 성 1자만 노출 |
| `phone` | `010-****-1234` — 가운데 마스킹, 앞 3자리·뒤 4자리 유지 |
| `birthday` | `1990-**-**` — 연도만 |
| `chartNo`·`chart_no` | 숫자면 그대로, **숫자가 아니면 `[비정형]`**(WORK-005) |
| 리뷰 본문 직원 실명 | `[직원]` — 기록 03·04 의 실명 사전 그대로 |
| 리뷰 작성자명 | 원천 표기 유지(이미 마스킹 닉네임) — 대상으로 **명시**만 |

뷰 정의에 실명 사전이 박힌다. DB 자체가 브론즈 원값을 갖는 PII 저장소이므로 경계는
「DB 밖으로 나가는 것」이고, 뷰가 그 경계다 — 사전이 DB 안에 남는 것은 그 경계 안쪽이다.
"""

from __future__ import annotations

import re
import sqlite3

from db.connection import atomic
from db.schema import REVIEW_HEADER_MAP, VEGAS_COLUMNS

MASK_TOKEN = "[직원]"

#: 차트번호 자리에 **숫자가 아닌 것**이 들어와 있을 때 덮는 표기(WORK-005).
#:
#: 차트번호는 숫자다. 숫자가 아닌 값이 앉아 있다면 그건 차트번호가 아니라 다른 무언가가
#: 흘러든 것이고(실측 1건 — 이름 문자열), **무엇인지 모르는 값을 그대로 내보낼 수 없다.**
#: 기록 03 의 「chart_no 는 마스킹하지 않는다」는 조인·검증 추적성을 위한 결정인데,
#: 그 추적성은 **숫자일 때만** 성립한다 — 비정형 값은 조인 키로 쓰이지도 않는다.
#:
#: 이름 마스킹(`성 1자 + ○`)을 쓰지 않는 이유: 그 값이 이름인지 모른다. 이름으로
#: 가정하고 성을 남기면, 이름이 아닐 때는 앞 1자를 그냥 노출하는 것이 된다.
#: 길이도 남기지 않는다 — 길이가 곧 힌트다.
CHART_NO_TOKEN = "[비정형]"

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


def mask_chart_no_sql(col: str) -> str:
    """숫자면 그대로, 숫자가 아니면 `[비정형]`. 빈 값은 빈 값 그대로다.

    `GLOB '*[^0-9]*'` — 숫자 아닌 문자가 하나라도 있으면 참이다. `LIKE` 와 달리
    문자 클래스를 쓸 수 있고 대소문자 규칙에 안 걸린다.
    """
    return (
        f"CASE WHEN {col} IS NULL OR {col} = '' THEN {col} "
        f"WHEN {col} GLOB '*[^0-9]*' THEN {_sql_literal(CHART_NO_TOKEN)} "
        f"ELSE {col} END"
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
        "chartNo": mask_chart_no_sql,
    }
    vegas_select = []
    for col, _ in VEGAS_COLUMNS:
        quoted = '"' + col + '"'
        masker = maskers.get(col)
        vegas_select.append(masker(quoted) + " AS " + quoted if masker else quoted)

    # 실버는 컬럼 목록이 DDL 문자열 하나에만 있다 — 규약을 두 번 적지 않으려고
    # 테이블에서 읽는다. 뷰 단계는 실버 뒤에 오므로(`build all` · conftest 순서)
    # 이 시점에 테이블이 있어야 정상이다.
    silver_columns = [r[1] for r in conn.execute("PRAGMA table_info(silver_reservations)")]
    if not silver_columns:
        raise RuntimeError(
            "silver_reservations 가 없다 — 뷰를 실버보다 먼저 만들 수 없다. "
            "`build all` 로 순서대로 돌려라")
    silver_select = [
        (mask_chart_no_sql(f'"{col}"') + f' AS "{col}"') if col == "chart_no" else f'"{col}"'
        for col in silver_columns
    ]

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
        # 실버는 브론즈에서 온 **원값 컬럼이 없다**(patientName·phone 미반입,
        # birthday → age_band). 남은 것은 `chart_no` 하나인데, 브론즈에서 비정형 값이
        # 그대로 따라 올라오므로 여기서도 같은 규칙으로 덮는다 — 뷰 하나만 고치면
        # 다른 뷰로 같은 값이 새는 길이 생긴다(WORK-005).
        "DROP VIEW IF EXISTS v_silver_reservations",
        "CREATE VIEW v_silver_reservations AS SELECT "
        + ", ".join(silver_select)
        + " FROM silver_reservations",
        "DROP VIEW IF EXISTS v_silver_reviews",
        "CREATE VIEW v_silver_reviews AS SELECT * FROM silver_reviews",
    ]


def build(conn: sqlite3.Connection) -> list[str]:
    with atomic(conn, "views"):
        for stmt in view_ddl(conn):
            conn.execute(stmt)
    return VIEWS

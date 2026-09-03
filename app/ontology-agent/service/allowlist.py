"""허용 목록 — 조회 가능한 것의 **단일 정의**. 도구(MCP)와 API 가 이것만 공유한다.

**allowlist 다. blocklist 가 아니다.** 새 컬럼이 생기면 자동으로 새는 쪽이 아니라
자동으로 막히는 쪽이어야 한다(SPEC-002 §5).

이 모듈이 AC-8(뷰 경유 강제)의 뿌리다 — 소비자 표면이 물리적으로 부를 수 있는 대상이
여기 적힌 것뿐이고, 브론즈·실버 **원 테이블 이름은 이 파일 어디에도 없다.**
정적 검사 테스트가 `tools/`·`api/`·`service/` 전체에서 원 테이블 문자열을 찾아 FAIL 시킨다.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# --- 계층별 조회 대상 -------------------------------------------------------
# 브론즈·실버는 **마스킹 뷰만**(DEC-002). 골드·온톨로지는 PII 가 없어 원 테이블을 읽는다.


@dataclass(frozen=True)
class TableSpec:
    """조회 대상 하나. `relation` 이 실제로 SQL 에 들어가는 유일한 식별자다."""

    layer: str
    table: str                       # 소비자가 부르는 이름(계층 접두어 없음)
    relation: str                    # 실제 조회 대상 — 뷰 또는 PII 없는 테이블
    masked_fields: tuple[str, ...] = ()
    note_ref: str = ""
    flows_to: tuple[dict, ...] = ()
    fields: tuple[str, ...] = ()     # 빈 튜플이면 런타임에 PRAGMA 로 채운다
    #: 원천 축 — **브론즈 전용**이다(SPEC-003 v0.0.8 §4). 허용값 `vegas`·`review`·`nexus`,
    #: **실버·골드는 null.** 화면이 이 값으로 칩을 묶으므로(SPEC-004 U-13 의 2단 구조는 브론즈에만
    #: 규정됐다) 실버에 실으면 칩 6개가 3개로 접혀 계층 탭 카운트와 어긋난다.
    source_group: str = ""
    #: 컬럼 목록을 **계약이 갖지 않는** 테이블의 사유. 그 외는 None.
    #: 화면이 「컬럼 설명이 왜 없나」를 추측하지 않게 이유를 문자열로 준다.
    columns_note: str | None = None

    @property
    def masked(self) -> bool:
        return bool(self.masked_fields)


#: nexus 브론즈 14종 — **관계명을 문자열 그대로 적는다.**
#: 예전에는 `f"bronze_{t}"` 로 조립했는데, 그러면 AC-8 정적 게이트가 그 줄을 볼 수 없다
#: (접두어 뒤가 `{` 라 이름이 안 붙는다 — 검수 W2 실측). 지금은 전부 홑이름이라
#: 게이트가 `bronze_nexus_` 접두어를 확인하고 PII 없는 테이블로 통과시킨다.
#: 소비자가 부르는 `table` 이름은 접두어를 떼어 파생한다 — 관계명 쪽이 정본이다.
_BRONZE_NEXUS_RELATIONS = (
    "bronze_nexus_branches", "bronze_nexus_categories",
    "bronze_nexus_category_translations_ko", "bronze_nexus_procedure_groups",
    "bronze_nexus_procedure_products_ko",
    "bronze_nexus_procedure_group_product_mappings",
    "bronze_nexus_event_procedure_groups", "bronze_nexus_event_procedure_products_ko",
    "bronze_nexus_event_procedure_group_product_mappings",
    "bronze_nexus_procedure_packages_ko", "bronze_nexus_promotions_v1",
    "bronze_nexus_promotion_v2s", "bronze_nexus_promotion_v2_event_group_mappings",
    "bronze_nexus_promotion_v2_group_mappings",
)

# 마스킹 표기 — SPEC-001 §4 가 SoT. 화면·API·에이전트 응답에 그대로 나가는 문자열이다.
MASK_NOTATION = {
    "patientName": "김○○",
    "phone": "010-****-1234",
    "birthday": "1990-**-**",
}

#: 컬럼 계약이 없는 테이블의 사유. 글로서리(기록 03)가 용어를 판정한 컬럼만 계산식·근거를
#: 갖는데, 아래 둘은 그 대상이 아니다 — 「없다」와 「아직 안 적었다」를 구분해 준다.
_NEXUS_COLUMNS_NOTE = (
    "nexus 원천 스키마를 원형 그대로 반입한 테이블이라 컬럼별 변환 규칙이 없다 — "
    "글로서리(기록 03)가 판정한 용어가 아니라 외부 시스템의 컬럼이다"
)
_PROMO_COLUMNS_NOTE = (
    "프로모션 이벤트 속성은 실버 스키마를 그대로 옮긴 것이라 KPI 계산식이 없다 — "
    "구성 특성 4컬럼만 매핑 사슬에서 파생된다(기록 05 4장 개정 1)"
)

_TABLES: tuple[TableSpec, ...] = (
    TableSpec(
        layer="bronze", table="vegas_reservations",
        relation="v_bronze_vegas_reservations",
        masked_fields=("patientName", "phone", "birthday"),
        note_ref="기록 02 브론즈 실사", source_group="vegas",
        flows_to=({"layer": "silver", "table": "reservations",
                   "note": "중복 제거 + 파생 컬럼(기록 04 2장)"},),
    ),
    TableSpec(
        layer="bronze", table="reviews", relation="v_bronze_reviews",
        masked_fields=("body", "authorName"),
        note_ref="기록 02 브론즈 실사", source_group="review",
        flows_to=({"layer": "silver", "table": "reviews",
                   "note": "실명 마스킹 + LLM 채점 병합(기록 04 3장)"},),
    ),
    *(TableSpec(layer="bronze", table=rel.removeprefix("bronze_"), relation=rel,
                note_ref="기록 02 브론즈 실사", source_group="nexus",
                columns_note=_NEXUS_COLUMNS_NOTE)
      for rel in _BRONZE_NEXUS_RELATIONS),
    TableSpec(
        layer="silver", table="reservations", relation="v_silver_reservations",
        note_ref="기록 04 실버 빌드",
        flows_to=({"layer": "gold", "table": "gold_kpi_daily",
                   "note": "일별 KPI 의 주 원천"},
                  {"layer": "gold", "table": "gold_retention_monthly",
                   "note": "신환 코호트 재방문 전환율"}),
    ),
    TableSpec(
        layer="silver", table="reviews", relation="v_silver_reviews",
        note_ref="기록 04 실버 빌드",
        flows_to=({"layer": "gold", "table": "gold_kpi_daily",
                   "note": "네이버 개입 신호(naver_reviews)"},
                  {"layer": "gold", "table": "gold_kpi_weekly",
                   "note": "강남언니 유기 신호(gu_reviews)"}),
    ),
    TableSpec(layer="silver", table="catalog", relation="silver_catalog",
              note_ref="기록 04 실버 빌드",
              flows_to=({"layer": "gold", "table": "gold_promo_calendar",
                         "note": "이벤트 상품 정가·할인가"},)),
    TableSpec(layer="silver", table="promotions", relation="silver_promotions",
              note_ref="기록 04 실버 빌드",
              flows_to=({"layer": "gold", "table": "gold_promo_calendar",
                         "note": "프로모션 이벤트 1행"},)),
    TableSpec(layer="silver", table="mappings", relation="silver_mappings",
              note_ref="기록 04 실버 빌드",
              flows_to=({"layer": "gold", "table": "gold_promo_calendar",
                         "note": "프로모→이벤트 그룹→상품 구성 사슬"},)),
    TableSpec(layer="silver", table="branch_alias", relation="silver_branch_alias",
              note_ref="기록 04 실버 빌드"),
    TableSpec(layer="gold", table="gold_kpi_daily", relation="gold_kpi_daily",
              note_ref="기록 05 골드 KPI",
              flows_to=({"layer": "gold", "table": "gold_kpi_weekly", "note": "ISO 주 합계"},
                        {"layer": "gold", "table": "gold_kpi_monthly", "note": "달력 월 합계"})),
    TableSpec(layer="gold", table="gold_kpi_weekly", relation="gold_kpi_weekly",
              note_ref="기록 05 골드 KPI"),
    TableSpec(layer="gold", table="gold_kpi_monthly", relation="gold_kpi_monthly",
              note_ref="기록 05 골드 KPI"),
    TableSpec(layer="gold", table="gold_promo_calendar", relation="gold_promo_calendar",
              note_ref="기록 05 프로모션 캘린더",
              columns_note=_PROMO_COLUMNS_NOTE),
    TableSpec(layer="gold", table="gold_retention_monthly",
              relation="gold_retention_monthly", note_ref="기록 05 4b 재방문 전환율"),
    TableSpec(layer="ontology", table="ontology_nodes", relation="ontology_nodes",
              note_ref="기록 07 온톨로지"),
    TableSpec(layer="ontology", table="ontology_edges", relation="ontology_edges",
              note_ref="기록 07 온톨로지"),
)

TABLES: dict[tuple[str, str], TableSpec] = {(t.layer, t.table): t for t in _TABLES}
LAYERS = ("bronze", "silver", "gold", "ontology")


def tables_of(layer: str) -> list[TableSpec]:
    return [t for t in _TABLES if t.layer == layer]


def resolve(layer: str, table: str) -> TableSpec | None:
    return TABLES.get((layer, table))


# --- KPI 지표 ---------------------------------------------------------------
# 기록 05 2.2 의 지표 목록. grain 별로 실제 골드 View 하나에 대응한다 —
# **도구·API 가 집계하지 않는다**(S-002).

GRAIN_RELATION = {
    "daily": "gold_kpi_daily",
    "weekly": "gold_kpi_weekly",
    "monthly": "gold_kpi_monthly",
    "retention_monthly": "gold_retention_monthly",
}
GRAIN_KEY = {
    "daily": "date",
    "weekly": "week_start",
    "monthly": "month",
    "retention_monthly": "cohort_month",
}
GRAIN_PARTIAL_FLAG = {
    "daily": None,
    "weekly": "is_partial_week",
    "monthly": "is_partial_month",
    "retention_monthly": "is_partial_cohort",
}

_BASE_METRICS = (
    "sales_total", "payment_visits", "avg_ticket", "visits", "new_patients",
    "revisits", "reservations", "cancels", "cancel_rate", "noshows", "noshow_rate",
    "new_churns", "naver_reviews", "new_patients_domestic", "foreign_sales_share",
    "sales_foreign_est", "visits_foreign_est", "new_patients_foreign_est",
)
_WEEKLY_EXTRA = ("gu_reviews", "gu_positive", "gu_negative")
_RETENTION_METRICS = (
    "cohort_size", "retained_60d", "retention_rate",
    "domestic_retention_rate", "foreign_est_share",
)

METRICS_BY_GRAIN: dict[str, tuple[str, ...]] = {
    "daily": _BASE_METRICS,
    "weekly": _BASE_METRICS + _WEEKLY_EXTRA,
    "monthly": _BASE_METRICS,
    "retention_monthly": _RETENTION_METRICS,
}

#: 방향 없는 개입 변수 — 상태(양호/주의/경고)를 부여하지 않는다(SPEC-001 §4).
NO_STATUS_METRICS = frozenset({"naver_reviews"})

MAX_METRICS = 8
MAX_FILTERS = 5
MAX_LIMIT = 200
DEFAULT_TOOL_LIMIT = 20
DEFAULT_API_LIMIT = 50
MAX_DEPTH = 3

FILTER_OPS = ("eq", "ne", "gte", "lte", "in", "between", "contains")

VERDICTS = ("채택", "자동 확정", "선언", "보류", "기각")
#: 기본 조회 — 인과 서술에 쓸 수 있는 판정만. 보류·기각은 명시해야 온다(SPEC-002 AC-6).
DEFAULT_VERDICTS = ("채택", "자동 확정", "선언")
CAUSAL_VERDICTS = frozenset(DEFAULT_VERDICTS)


def metrics_of(grain: str) -> tuple[str, ...]:
    return METRICS_BY_GRAIN.get(grain, ())


# --- 필드 화이트리스트 -------------------------------------------------------
# 뷰의 실제 컬럼을 런타임에 읽어 채운다. 뷰가 이미 마스킹된 표면이므로 「뷰에 있는 컬럼」이
# 곧 허용 필드다 — PII 원 컬럼은 뷰에 마스킹된 형태로만 존재하고, 원값 컬럼은 없다.


@dataclass
class _FieldCache:
    #: (DB 경로, 관계명) → 컬럼. 경로를 키에 넣어야 DB 를 갈아 끼울 때 스키마가 안 섞인다.
    by_relation: dict[tuple[str, str], tuple[str, ...]] = field(default_factory=dict)


_cache = _FieldCache()


def fields_of(conn, spec: TableSpec) -> tuple[str, ...]:
    """조회 대상의 허용 필드. 뷰 스키마가 곧 허용 목록이다.

    뷰가 마스킹 컬럼의 **별칭을 원본과 같게** 주므로(`build/masking.py` 의
    `... AS "patientName"`) `masked_fields` 3종도 이 목록에 들어온다 — 필터·정렬이 통과한다.
    값이 마스킹본이라 원값 조회는 0건이고 `contains` 는 따로 차단하므로 누출 경로는 아니다.
    별칭을 바꾸고 싶다면 SPEC-002 AC-3 문언과의 관계를 먼저 정해야 한다(검수 W1).
    """
    # 키에 DB 경로를 넣는다 — 관계명만으로 캐시하면 서로 다른 DB 를 오갈 때 오염된다
    row = conn.execute("PRAGMA database_list").fetchone()
    key = (row[2] if row else "", spec.relation)
    cached = _cache.by_relation.get(key)
    if cached is not None:
        return cached
    cols = tuple(r[1] for r in conn.execute(f"PRAGMA table_info({spec.relation})"))
    _cache.by_relation[key] = cols
    return cols


def reset_field_cache() -> None:
    _cache.by_relation.clear()

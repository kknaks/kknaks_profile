"""스키마 정의 — 브론즈 16 + 실버 6 + 골드 5 + 온톨로지 2.

이름은 SPEC-001 §4 표 그대로다. 임의로 바꾸지 않는다 — 후속 WORK-002 가 이 이름으로 소비한다.

**타입 방침 (WORK-001 Open Issue 1 판정)**
- nexus 브론즈는 **전 컬럼 TEXT**. 원천이 CSV 라 타입 정보가 없고, 숫자로 보이는 컬럼도
  빈 문자열·선행 0 이 섞여 있어 INTEGER 로 받으면 원형이 변형된다(`""` → `NULL`,
  `007` → `7`). 원형 보존이 상위 규칙이므로 문자열 그대로 받고, 형변환은 실버가 한다.
- vegas 는 원천이 **JSON** 이라 타입이 원형에 포함된다 — `sales`·`receipt`·`visitCount`
  는 JSON number 이므로 INTEGER 로 받는 것이 원형 보존이다. 나머지는 TEXT.
- 어느 쪽도 행수 대사에 영향을 주지 않는다(게이트 1 은 행 단위 대사).
"""

from __future__ import annotations

import sqlite3

# --- 브론즈 ---------------------------------------------------------------

VEGAS_COLUMNS: list[tuple[str, str]] = [
    ("branch", "TEXT"),
    ("resvDate", "TEXT"),
    ("chartNo", "TEXT"),
    ("patientName", "TEXT"),
    ("birthday", "TEXT"),
    ("phone", "TEXT"),
    ("staff", "TEXT"),
    ("sales", "INTEGER"),
    ("receipt", "INTEGER"),
    ("visitCount", "INTEGER"),
    ("visitStatus", "TEXT"),
]

# 리뷰 CSV 한글 헤더 → 브론즈 컬럼. **값은 손대지 않고 식별자만 바꾼다.**
# `authorName` 은 SPEC-001 마스킹 뷰 표가 그 이름으로 부르는 필드다.
REVIEW_HEADER_MAP: list[tuple[str, str]] = [
    ("플랫폼", "platform"),
    ("리뷰일", "reviewDate"),
    ("작성자", "authorName"),
    ("평점", "rating"),
    ("리뷰내용", "body"),
    ("원문URL", "sourceUrl"),
    ("플랫폼리뷰ID", "reviewPk"),
    ("답변상태", "replyStatus"),
    ("답변일시_KST", "repliedAt"),
    ("수집일시_KST", "collectedAt"),
]
REVIEW_COLUMNS: list[tuple[str, str]] = [(c, "TEXT") for _, c in REVIEW_HEADER_MAP]

# nexus 14종 — 파일 stem → 원천 CSV 헤더(기록 02 실사 스키마). 전 컬럼 TEXT.
NEXUS_COLUMNS: dict[str, list[str]] = {
    "branches": [
        "created_at", "updated_at", "deleted_at", "id", "branch_id", "slug",
        "subdomain", "domain", "name", "representative_name",
        "representative_image_url", "status", "group_id",
    ],
    "categories": [
        "created_at", "updated_at", "deleted_at", "branch_id", "id", "ca_id",
        "display_order", "is_displayed", "parent_id",
    ],
    "category_translations_ko": [
        "deleted_at", "language", "id", "name", "sub_name", "category_id",
    ],
    "procedure_groups": [
        "created_at", "updated_at", "deleted_at", "branch_id", "language", "id",
        "group_code", "name", "highlight", "search_hashtags", "display_order",
        "is_displayed",
    ],
    "procedure_products_ko": [
        "created_at", "updated_at", "deleted_at", "branch_id", "language", "id",
        "name", "short_description", "description", "search_codes",
        "regular_price", "discounted_price", "discount_rate", "inquiry_type",
        "duration_minutes", "badges", "display_order", "is_displayed",
        "product_code",
    ],
    "procedure_group_product_mappings": [
        "created_at", "updated_at", "id", "procedure_group_id",
        "procedure_product_id", "display_order",
    ],
    "event_procedure_groups": [
        "created_at", "updated_at", "deleted_at", "branch_id", "language", "id",
        "group_code", "name", "highlight", "search_hashtags", "display_order",
        "is_displayed",
    ],
    "event_procedure_products_ko": [
        "created_at", "updated_at", "deleted_at", "branch_id", "language", "id",
        "name", "short_description", "description", "search_codes",
        "regular_price", "discounted_price", "discount_rate", "duration_minutes",
        "badges", "display_order", "is_displayed", "product_code",
    ],
    "event_procedure_group_product_mappings": [
        "created_at", "updated_at", "id", "display_order",
        "event_procedure_group_id", "event_procedure_product_id",
    ],
    "procedure_packages_ko": [
        "created_at", "updated_at", "deleted_at", "branch_id", "language", "id",
        "package_code", "name", "summary", "keywords", "thumbnail_type",
        "thumbnail_url", "youtube_url", "recommended_cycle", "duration",
        "display_order", "is_displayed", "main_category_id", "sub_category_id",
    ],
    "promotions_v1": [
        "created_at", "updated_at", "deleted_at", "branch_id", "id",
        "promotion_code", "promotion_started_at", "promotion_ended_at",
        "display_started_at", "display_ended_at", "is_displayed",
        "is_main_displayed", "display_order", "total_selection_limit",
        "group_selection_limit", "page_url", "thumbnail_url", "banner_url",
    ],
    "promotion_v2s": [
        "created_at", "updated_at", "deleted_at", "branch_id", "language", "id",
        "promotion_code", "prefix", "title", "subtitle", "promotion_started_at",
        "promotion_ended_at", "display_started_at", "display_ended_at",
        "is_displayed", "is_main_displayed", "display_order",
        "total_selection_limit", "group_selection_limit", "page_url",
        "thumbnail_url", "banner_url", "notices",
    ],
    "promotion_v2_event_group_mappings": [
        "id", "display_order", "event_procedure_group_id", "promotion_v2_id",
    ],
    "promotion_v2_group_mappings": [
        "id", "display_order", "procedure_group_id", "promotion_v2_id",
    ],
}

BRONZE_TABLES: list[str] = (
    ["bronze_vegas_reservations", "bronze_reviews"]
    + [f"bronze_nexus_{name}" for name in NEXUS_COLUMNS]
)


def _ddl(table: str, columns: list[tuple[str, str]]) -> str:
    cols = ",\n  ".join(f'"{name}" {type_}' for name, type_ in columns)
    return f"CREATE TABLE IF NOT EXISTS {table} (\n  {cols}\n)"


def bronze_ddl() -> list[str]:
    stmts = [
        _ddl("bronze_vegas_reservations", VEGAS_COLUMNS),
        _ddl("bronze_reviews", REVIEW_COLUMNS),
    ]
    for name, cols in NEXUS_COLUMNS.items():
        stmts.append(_ddl(f"bronze_nexus_{name}", [(c, "TEXT") for c in cols]))
    return stmts


# --- 실버 -----------------------------------------------------------------

SILVER_DDL = [
    """CREATE TABLE IF NOT EXISTS silver_reservations (
  branch_code TEXT NOT NULL,
  resv_date TEXT NOT NULL,
  chart_no TEXT,
  unidentified_flag INTEGER NOT NULL,
  age_band TEXT,
  staff TEXT,
  sales INTEGER NOT NULL,
  receipt INTEGER NOT NULL,
  visit_count INTEGER NOT NULL,
  visit_status TEXT NOT NULL,
  is_new INTEGER NOT NULL,
  is_revisit INTEGER NOT NULL,
  is_new_churn INTEGER NOT NULL,
  sales_exception_flag INTEGER NOT NULL,
  outstanding_flag INTEGER NOT NULL,
  outstanding_direction TEXT,
  is_payment_visit INTEGER NOT NULL,
  is_foreign_est INTEGER NOT NULL
)""",
    """CREATE TABLE IF NOT EXISTS silver_reviews (
  review_pk TEXT PRIMARY KEY,
  platform TEXT NOT NULL,
  review_date TEXT,
  collected_at TEXT,
  rating TEXT,
  body_masked TEXT,
  procedure_concept TEXT,
  body_part TEXT,
  predicted_score REAL,
  score_evidence TEXT,
  sentiment TEXT NOT NULL,
  signal_type TEXT NOT NULL
)""",
    """CREATE TABLE IF NOT EXISTS silver_catalog (
  entity_type TEXT NOT NULL,
  line_type TEXT,
  id TEXT NOT NULL,
  code TEXT,
  name TEXT,
  branch_pk TEXT,
  regular_price TEXT,
  discounted_price TEXT,
  is_deleted INTEGER NOT NULL
)""",
    # `source_id` — 원천(nexus) 내부 id 보존. 골드가 프로모션 구성 사슬을 실버만 읽고
    # 이을 수 있게 하는 유일한 연결 고리다(계층 경계 — 골드는 브론즈를 읽지 않는다).
    # 기존 CSV 산출물에는 없는 컬럼이라 `csv_parity` 는 공유 컬럼만 대조한다.
    """CREATE TABLE IF NOT EXISTS silver_promotions (
  promo_version TEXT NOT NULL,
  code TEXT,
  title TEXT,
  branch_pk TEXT,
  benefit_start TEXT,
  benefit_end TEXT,
  display_start TEXT,
  display_end TEXT,
  is_deleted INTEGER NOT NULL,
  source_id TEXT
)""",
    """CREATE TABLE IF NOT EXISTS silver_branch_alias (
  alias TEXT NOT NULL,
  branch_code TEXT NOT NULL,
  branch_pk TEXT
)""",
    """CREATE TABLE IF NOT EXISTS silver_mappings (
  map_type TEXT NOT NULL,
  parent_id TEXT,
  child_id TEXT
)""",
]

SILVER_TABLES = [
    "silver_reservations", "silver_reviews", "silver_catalog",
    "silver_promotions", "silver_branch_alias", "silver_mappings",
]

SILVER_INDEX_DDL = [
    "CREATE INDEX IF NOT EXISTS ix_silver_resv_date ON silver_reservations(resv_date)",
    "CREATE INDEX IF NOT EXISTS ix_silver_resv_chart ON silver_reservations(chart_no)",
    "CREATE INDEX IF NOT EXISTS ix_silver_reviews_date ON silver_reviews(review_date)",
    "CREATE INDEX IF NOT EXISTS ix_bronze_vegas_date ON bronze_vegas_reservations(resvDate)",
]

# --- 골드 -----------------------------------------------------------------
# 골드는 컬럼이 지표 × 파생(_dod/_dod_pct/_ma7/_status)으로 불어나므로 빌드가 산출
# 컬럼에서 DDL 을 만든다(`build/gold.py`). 이름·행수 계약만 여기 남긴다.

GOLD_TABLES = [
    "gold_kpi_daily", "gold_kpi_weekly", "gold_kpi_monthly",
    "gold_promo_calendar", "gold_retention_monthly",
]

# --- 온톨로지 -------------------------------------------------------------

ONTOLOGY_DDL = [
    """CREATE TABLE IF NOT EXISTS ontology_nodes (
  node_id TEXT PRIMARY KEY,
  name_ko TEXT NOT NULL,
  node_type TEXT NOT NULL,
  controllable TEXT,
  grain TEXT,
  source TEXT
)""",
    """CREATE TABLE IF NOT EXISTS ontology_edges (
  cause TEXT NOT NULL,
  effect TEXT NOT NULL,
  sign TEXT,
  lag TEXT,
  lag_days INTEGER,
  edge_kind TEXT NOT NULL,
  confidence TEXT,
  evidence TEXT,
  verdict TEXT NOT NULL,
  rationale TEXT,
  FOREIGN KEY (cause) REFERENCES ontology_nodes(node_id),
  FOREIGN KEY (effect) REFERENCES ontology_nodes(node_id)
)""",
]

ONTOLOGY_TABLES = ["ontology_nodes", "ontology_edges"]


def bootstrap(conn: sqlite3.Connection) -> None:
    """빈 DB 에 계층 스키마를 세운다. 이미 있으면 그대로 둔다(파괴적 마이그레이션 없음).

    **커밋하지 않는다** — 호출자의 트랜잭션에 참여한다. 여기서 커밋하면 바깥
    savepoint 가 통째로 풀려 「게이트 실패 시 이전 DB 유지」가 깨진다.
    """
    for stmt in bronze_ddl() + SILVER_DDL + ONTOLOGY_DDL + SILVER_INDEX_DDL:
        conn.execute(stmt)


def table_names(conn: sqlite3.Connection, prefix: str = "") -> list[str]:
    rows = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE ? ORDER BY name",
        (f"{prefix}%",),
    ).fetchall()
    return [r[0] for r in rows]

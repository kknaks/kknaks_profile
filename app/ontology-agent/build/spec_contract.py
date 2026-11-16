"""SPEC-001 §4 가 계약으로 고정한 값 — 코드에 박아 두고 적재본과 1:1 대조한다.

이 표는 **정본(`ontology/nodes.csv`)이 SoT** 이고 SPEC-001 이 그 표기를 받아 적은 것이다
(2026-09-02 코디네이터 판단 — spec 표 8건·type/판정 라벨·lag 규칙을 정본 기준으로 정정).
여기 값을 정본에 맞춰 고치는 것은 금지다 — 어긋나면 `NODE_ID_MISMATCH` 로 적재를 실패시키고
어긋난 id·라벨을 보고한다(AC-6). 정본이 바뀌면 spec 을 먼저 고치고 이 표를 갱신한다.
"""

from __future__ import annotations

# (node_id, 라벨, node_type) — SPEC-001 v0.0.6 §4 표 순서 그대로 25종
SPEC_NODES: list[tuple[str, str, str]] = [
    ("weekday", "요일", "exogenous"),
    ("season", "계절(월)", "exogenous"),
    ("holiday", "연휴·공휴일", "exogenous"),
    ("promo_event", "프로모션 이벤트", "intervention"),
    ("naver_reviews", "네이버 리뷰 수", "intervention"),
    ("discount_rate", "프로모션 평균 할인율", "attribute"),
    ("gu_reviews", "강남언니 리뷰 수", "organic"),
    ("reservations", "예약 수", "kpi"),
    ("cancels", "취소 수", "kpi"),
    ("noshows", "부도 수", "kpi"),
    ("visits", "총 내원 수", "kpi"),
    ("cancel_rate", "취소율", "kpi"),
    ("noshow_rate", "노쇼율", "kpi"),
    ("new_patients", "신환 수", "kpi"),
    ("new_patients_domestic", "한국인 신환 수", "kpi"),
    ("new_patients_foreign_est", "외국인 추정 신환 수", "kpi"),
    ("revisits", "재진 수", "kpi"),
    ("payment_visits", "결제 내원 수", "kpi"),
    ("new_churns", "신규 이탈 수", "kpi"),
    ("avg_ticket", "객단가", "kpi"),
    ("sales_total", "매출", "kpi"),
    ("sales_foreign_est", "외국인 추정 매출", "kpi"),
    ("foreign_sales_share", "외국인 매출 비중", "kpi"),
    ("retention_rate_60d", "재방문 전환율(60일)", "kpi"),
    ("foreign_inflow_channel", "외국인 유입 채널", "unobserved"),
]

# node_type 별 기대 개수 — 영문 enum 이 정본이다(SPEC-001 v0.0.6).
# 한글 표기는 화면 카피 매핑이며 SPEC-004 가 갖는다 — 계약 값이 아니다.
NODE_TYPE_COUNTS: dict[str, int] = {
    "kpi": 17, "intervention": 2, "organic": 1,
    "exogenous": 3, "unobserved": 1, "attribute": 1,
}

# 외생 노드 — 들어오는 엣지가 0 이어야 한다
EXOGENOUS_NODES = {"weekday", "season", "holiday"}

# 엣지 판정별 기대 개수 — 총 27
VERDICT_COUNTS: dict[str, int] = {
    "채택": 4, "자동 확정": 14, "선언": 3, "보류": 3, "기각": 3,
}

# 사유 필드가 필수인 판정 (「왜 그리지 않았나」가 조회 가능해야 한다)
VERDICTS_REQUIRING_RATIONALE = {"기각", "보류"}

EXPECTED_NODE_COUNT = 25
EXPECTED_EDGE_COUNT = 27

# --- 게이트 2 대조값 (SPEC-001 §6 AC-2 · 기록 05 5장) ---------------------

REBUILD_TOTALS: dict[str, int] = {
    "매출 합(예외 1건 제외)": 2_615_555_218,
    "결제 내원": 5_428,
    "신환": 3_447,
    "총 내원(실버 기준)": 47_537,
}
REBUILD_ROWCOUNTS: dict[str, int] = {
    "silver_reservations": 75_479,
    "silver_reviews": 1_962,
    "silver_catalog": 6_198,
    "silver_promotions": 73,
    "silver_branch_alias": 11,
    "silver_mappings": 9_689,
    "gold_kpi_daily": 235,
    "gold_kpi_weekly": 34,
    "gold_promo_calendar": 57,
    # OQ-3 닫힘 (2026-09-02) — 기록 05 에 행수가 없어 WORK-001 P4 빌드 실측으로 확정하고
    # SPEC-001 v0.0.6 §4·§6 에 등재했다.
    "gold_kpi_monthly": 8,
    "gold_retention_monthly": 8,
}
# 브론즈 내원 47,602 와의 대사 — 중복 제거로 빠진 완전 동일 내원 행
VISIT_DEDUP_DELTA = 65
BRONZE_VISITS = 47_602
MISSING_DAY = "2026-02-17"

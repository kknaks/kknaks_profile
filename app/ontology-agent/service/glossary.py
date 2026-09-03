"""글로서리 — 기록 03 용어 판정 표 + KPI 계산식(기록 05) + enum(SPEC-001 §4).

`get_definition` 도구와 `lineage` API 가 같은 사전을 읽는다. **정의가 두 곳에 있으면
언젠가 한쪽만 고쳐진다** — 도구가 말하는 노쇼율과 화면이 말하는 노쇼율이 갈리는 자리다.

여기 있는 것은 「사실의 서술」이지 관계 지식이 아니다. 어떤 KPI 가 어떤 KPI 의 원인인지는
이 파일에 없고 `ontology_edges` 조회로만 나온다(S-001).
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Term:
    term: str
    definition: str
    status: str                       # 확정 · 승계 · 대기 (기록 03 1장)
    source_note: str
    aliases: tuple[str, ...] = ()
    related_columns: tuple[str, ...] = ()
    formula: str | None = None
    note: str | None = None
    direction: str | None = None      # 낮을수록 나쁨 · 높을수록 나쁨
    unit: str | None = None
    fmt: str | None = None            # number · percent · currency
    label: str | None = None
    gate: str | None = None
    source_columns: tuple[str, ...] = field(default_factory=tuple)


_TERMS: tuple[Term, ...] = (
    Term(term="매출", aliases=("sales_total", "sales"),
         definition="`sales` 합계. 청구·발생액 기준이 정본이다. 취소인데 금액이 있는 예외 행 1건은 집계에서 제외한다.",
         formula="Σ sales (매출 예외 행 제외)",
         note="수납(receipt)이 아니라 청구(sales)가 KPI 정본이다",
         status="확정", source_note="기록 03 1장 매출 · 매출 예외 행",
         related_columns=("gold_kpi_daily.sales_total", "silver_reservations.sales"),
         source_columns=("silver_reservations.sales", "silver_reservations.sales_exception_flag"),
         gate="기록 05 게이트 1(실버 재집계 일치) 통과 — 대조값 2,615,555,218원",
         direction="낮을수록 나쁨", unit="원", fmt="currency", label="매출"),
    Term(term="결제 내원 수", aliases=("payment_visits",),
         definition="`sales` 가 0이 아니고 `visit_status` 가 내원인 행 수. 객단가의 분모다.",
         formula="COUNT(sales ≠ 0 AND visit_status = 내원)",
         status="승계", source_note="기록 03 1장 객단가",
         related_columns=("gold_kpi_daily.payment_visits",),
         source_columns=("silver_reservations.is_payment_visit",),
         gate="기록 05 게이트 1 통과 — 대조값 5,428",
         direction="낮을수록 나쁨", unit="건", fmt="number", label="결제 내원"),
    Term(term="객단가", aliases=("avg_ticket",),
         definition="매출 합 ÷ 결제 발생 내원 수. **전체 내원으로 나누지 않는다** — 내원 47,602건 중 결제 발생은 5,428건뿐이라 전체 분모는 값을 뭉갠다.",
         formula="매출 ÷ 결제 내원 수",
         note="결제 내원이 0인 날은 0이 아니라 null 이다",
         status="승계", source_note="기록 03 1장 객단가",
         related_columns=("gold_kpi_daily.avg_ticket",),
         source_columns=("gold_kpi_daily.sales_total", "gold_kpi_daily.payment_visits"),
         gate="분모 0인 날은 null(0 채움 없음)",
         direction="낮을수록 나쁨", unit="원", fmt="currency", label="객단가"),
    Term(term="총 내원 수", aliases=("visits", "내원"),
         definition="`visit_status` 가 내원인 행 수. 신환 + 재진과 같아야 한다.",
         formula="COUNT(visit_status = 내원) = 신환 + 재진",
         status="확정", source_note="기록 03 1장 신환·재진",
         related_columns=("gold_kpi_daily.visits",),
         source_columns=("silver_reservations.visit_status",),
         gate="기록 05 게이트 3(내원 대사) — 235일 전일에서 신환 + 재진 = 총 내원",
         direction="낮을수록 나쁨", unit="건", fmt="number", label="총 내원"),
    Term(term="신환", aliases=("new_patients", "신환 수"),
         definition="`visit_count` = 1 이고 `visit_status` = 내원.",
         formula="COUNT(visit_count = 1 AND visit_status = 내원)",
         status="확정", source_note="기록 03 1장 신환",
         related_columns=("gold_kpi_daily.new_patients",),
         source_columns=("silver_reservations.is_new",),
         gate="기록 05 게이트 1 통과 — 대조값 3,447",
         direction="낮을수록 나쁨", unit="명", fmt="number", label="신환"),
    Term(term="재진", aliases=("revisits", "재진 수"),
         definition="`visit_count` ≥ 2 이고 `visit_status` = 내원.",
         formula="COUNT(visit_count ≥ 2 AND visit_status = 내원)",
         status="확정", source_note="기록 03 1장 재진",
         related_columns=("gold_kpi_daily.revisits",),
         source_columns=("silver_reservations.is_revisit",),
         direction="낮을수록 나쁨", unit="건", fmt="number", label="재진"),
    Term(term="예약 수", aliases=("reservations",),
         definition="전체 예약 행 수(내원 + 취소 + 부도).",
         formula="COUNT(*) = 내원 + 취소 + 부도",
         status="확정", source_note="기록 03 1장 취소율",
         related_columns=("gold_kpi_daily.reservations",),
         direction="낮을수록 나쁨", unit="건", fmt="number", label="예약"),
    Term(term="취소 수", aliases=("cancels",),
         definition="`visit_status` 가 취소인 행 수.",
         formula="COUNT(visit_status = 취소)",
         status="확정", source_note="기록 03 1장 취소율",
         related_columns=("gold_kpi_daily.cancels",),
         direction="높을수록 나쁨", unit="건", fmt="number", label="취소"),
    Term(term="취소율", aliases=("cancel_rate",),
         definition="취소 ÷ 전체 예약 행(내원 + 취소 + 부도). 노쇼와 별개 사건으로 집계한다.",
         formula="취소 ÷ 예약",
         note="노쇼율과 분모가 다르다 — 취소는 「예약을 무른 것」이다",
         status="확정", source_note="기록 03 1장 취소율",
         related_columns=("gold_kpi_daily.cancel_rate",),
         source_columns=("gold_kpi_daily.cancels", "gold_kpi_daily.reservations"),
         gate="비율형은 주별·월별에서 합계 재계산(일별 평균 아님)",
         direction="높을수록 나쁨", unit="%", fmt="percent", label="취소율"),
    Term(term="부도 수", aliases=("noshows", "노쇼 수"),
         definition="`visit_status` 가 부도인 행 수. enum 정본 표기는 「부도」다.",
         formula="COUNT(visit_status = 부도)",
         status="확정", source_note="기록 03 1장 노쇼율",
         related_columns=("gold_kpi_daily.noshows",),
         direction="높을수록 나쁨", unit="건", fmt="number", label="부도"),
    Term(term="노쇼율", aliases=("noshow_rate",),
         definition="부도 ÷ (내원 + 부도). 취소는 분모에서 제외한다 — 취소는 「안 온 것」이 아니라 「예약을 무른 것」이다.",
         formula="부도 ÷ (내원 + 부도)",
         note="취소는 분모에서 제외",
         status="승계", source_note="기록 03 1장 노쇼율",
         related_columns=("gold_kpi_daily.noshow_rate", "silver_reservations.visit_status"),
         source_columns=("gold_kpi_daily.noshows", "gold_kpi_daily.visits"),
         gate="분모 0인 날은 null",
         direction="높을수록 나쁨", unit="%", fmt="percent", label="노쇼율"),
    Term(term="신규 이탈", aliases=("new_churns", "신규 이탈 수"),
         definition="`visit_count` = 0 인 예약 행. 첫 방문 전 이탈로 해석하며 버리지 않고 별도 KPI 로 집계한다.",
         formula="COUNT(visit_count = 0)",
         status="승계", source_note="기록 03 1장 신규 이탈",
         related_columns=("gold_kpi_daily.new_churns",),
         source_columns=("silver_reservations.is_new_churn",),
         direction="높을수록 나쁨", unit="건", fmt="number", label="신규 이탈"),
    Term(term="개입 신호", aliases=("naver_reviews", "네이버 리뷰 수"),
         definition="네이버 플레이스 리뷰 수. 마케팅 리뷰 확보 전략의 산출물이라 **개입 변수**로 취급하고 유기 신호와 합산하지 않는다.",
         formula="COUNT(platform = 네이버 플레이스)",
         note="관측 개시(2026-03-21) 이전은 0이 아니라 null 이다. 방향이 없어 상태를 부여하지 않는다",
         status="승계", source_note="기록 03 1장 개입 신호",
         related_columns=("gold_kpi_daily.naver_reviews",),
         source_columns=("silver_reviews.platform",),
         gate="관측 개시 이전 구간은 빈 값(기록 05 승인 4)",
         direction=None, unit="건", fmt="number", label="네이버 리뷰"),
    Term(term="유기 신호", aliases=("gu_reviews", "강남언니 리뷰 수"),
         definition="강남언니 리뷰만 유기 신호다. **주 단위** 집계이고 표본이 얇아 **보조 신호 지위**다 — 단독 근거로 엣지를 확정하지 않는다.",
         formula="COUNT(platform = 강남언니) — 주 단위",
         note="리뷰 없는 주의 0 은 결측이 아니라 실제 0 이다",
         status="확정", source_note="기록 03 1장 유기 신호 · 4장 대기 항목 1 종결",
         related_columns=("gold_kpi_weekly.gu_reviews",),
         direction="낮을수록 나쁨", unit="건", fmt="number", label="강남언니 리뷰"),
    Term(term="한국인 신환 수", aliases=("new_patients_domestic",),
         definition="신환 − 외국인 추정 신환.",
         formula="신환 − 외국인 추정 신환",
         status="확정", source_note="기록 05 개정 4",
         related_columns=("gold_kpi_daily.new_patients_domestic",),
         direction="낮을수록 나쁨", unit="명", fmt="number", label="한국인 신환"),
    Term(term="외국인 추정", aliases=("is_foreign_est", "new_patients_foreign_est",
                                  "sales_foreign_est", "visits_foreign_est"),
         definition="`patientName` 에 로마자가 1자 이상 포함된 예약 행을 외국인 추정으로 표지한다. **추정이다** — 영문 표기 내국인·교포가 섞일 수 있고 국적 원천 컬럼은 없다. 판정은 브론즈에서 하고 실버에는 플래그만 내려간다.",
         formula="patientName 에 [A-Za-z] 포함 여부",
         note="추정치다 — 단정하지 않는다",
         status="확정", source_note="기록 03 1장 외국인 추정(개정 3)",
         related_columns=("gold_kpi_daily.new_patients_foreign_est",
                          "gold_kpi_daily.sales_foreign_est"),
         direction="낮을수록 나쁨", unit="명", fmt="number", label="외국인 추정 신환"),
    Term(term="외국인 매출 비중", aliases=("foreign_sales_share",),
         definition="외국인 추정 매출 ÷ 매출. **높을수록 의존 리스크**다.",
         formula="외국인 추정 매출 ÷ 매출",
         status="확정", source_note="기록 05 개정 4",
         related_columns=("gold_kpi_daily.foreign_sales_share",),
         direction="높을수록 나쁨", unit="%", fmt="percent", label="외국인 매출 비중"),
    Term(term="재방문 전환율", aliases=("retention_rate", "retention_rate_60d", "재방문 전환율(60일)"),
         definition="월 신환 코호트 중 첫 내원 후 **60일 안에 재진이 1회 이상** 발생한 비율. 코호트는 `chart_no` 가 있는 신환만(미식별 그룹 제외).",
         formula="60일 내 재진 발생 수 ÷ 코호트 크기",
         note="관찰 60일이 확보되지 않은 코호트는 `is_partial_cohort` 로 표지하고 집계에서 제외한다",
         status="확정", source_note="기록 03 1장 재방문 전환율(개정 2·3)",
         related_columns=("gold_retention_monthly.retention_rate",),
         gate="코호트 합 = 실버 신환 chart_no 수와 일치",
         direction="낮을수록 나쁨", unit="%", fmt="percent", label="재방문 전환율"),
    Term(term="환자 식별", aliases=("chart_no", "chartNo"),
         definition="`chartNo` 를 해시하지 않고 그대로 쓴다. 빈 `chartNo` 는 「환자 미식별」 그룹으로 묶고, 같은 `chartNo` 에 다른 이름이 붙은 건은 장부 오기로 보아 `chartNo` 를 신뢰한다.",
         status="확정", source_note="기록 03 1장 환자 식별 · 3장 PII 반입 규칙",
         related_columns=("silver_reservations.chart_no",)),
    Term(term="지점", aliases=("branch_code", "CERAMIQUE-GN-001"),
         definition="정본은 `branches.branch_id` 코드(강남 = `CERAMIQUE-GN-001`). 나머지 표기는 alias 매핑 테이블로 흡수한다.",
         status="확정", source_note="기록 03 1장 지점",
         related_columns=("silver_branch_alias.branch_code",)),
    Term(term="결측일 처리", aliases=("missing_day",),
         definition="결측일은 0으로 채우지 않고 **행 자체를 만들지 않는다**. 창 236일 중 2026-02-17 하루가 결측이라 일별은 235행이다.",
         status="승계", source_note="기록 03 1장 결측일 처리",
         related_columns=("gold_kpi_daily.date",)),
    Term(term="리뷰 예상 평점", aliases=("predicted_score",),
         definition="LLM 이 본문 텍스트만 보고 매기는 0.5~5점(0.5 단위) 예상 평점. 플랫폼 불문 동일 척도다 — 평점 없는 네이버에 강남언니와 같은 자를 대는 장치. 채점이 성립하지 않는 건은 점수 없이 판정불가다.",
         status="확정", source_note="기록 03 1장 리뷰 예상 평점",
         related_columns=("silver_reviews.predicted_score",)),
    Term(term="리뷰 감성", aliases=("sentiment",),
         definition="예상 평점의 임계값 분류 — ≥4 긍정 / 3~3.5 중립 / ≤2.5 부정 / 채점 불가는 판정불가. **중립과 판정불가를 합치지 않는다.**",
         status="확정", source_note="기록 03 1장 리뷰 감성",
         related_columns=("silver_reviews.sentiment",)),
    Term(term="평점의 지위", aliases=("rating",),
         definition="강남언니 실제 평점은 감성의 정답이 아니라 **검증 게이트**다. 예상 평점과의 정합률(±0.5 이내 80% 이상)을 재고 큰 불일치만 사람이 본다.",
         status="확정", source_note="기록 03 1장 평점의 지위",
         related_columns=("silver_reviews.rating",)),
    Term(term="수납", aliases=("receipt",),
         definition="`receipt` 합계. **KPI 정본이 아니며** 실버에 보존만 한다. `sales` ≠ `receipt` 인 행에는 미수 방향 플래그를 단다.",
         status="확정", source_note="기록 03 1장 수납",
         related_columns=("silver_reservations.receipt",
                          "silver_reservations.outstanding_direction")),
    Term(term="담당자", aliases=("staff",),
         definition="v1 분석 축에서 **제외**한다. 실버 컬럼은 보존하고 중복 제거 키에는 포함한다. 「미지정」 35.4% + 데스크 단말 계정 혼재로 분석 단위가 성립하지 않는다.",
         status="확정", source_note="기록 03 1장 담당자(staff) 축",
         related_columns=("silver_reservations.staff",)),
    Term(term="시술 개념", aliases=("procedure_concept", "ProcedureConcept"),
         definition="nexus 강남 생존(미삭제) 루트 카테고리 **13종의 폐쇄 목록**. 목록 밖 개념 태그는 금지하고, 추가는 제안만 하고 사람이 승인한 뒤 목록을 갱신한다.",
         status="확정", source_note="기록 03 2장 시술 개념 폐쇄 목록",
         related_columns=("silver_reviews.procedure_concept",)),
    Term(term="프로모션", aliases=("promo_event", "promotions"),
         definition="v1 + v2 모두 포함한다(v1 은 과거 실사용). 기간 정본은 **혜택 기간**이고 노출 기간은 참고 속성이다. 프로모션 1건 = 이벤트 1행이며 「일별 활성 개수」류 변수를 만들지 않는다.",
         status="확정", source_note="기록 03 1장 프로모션 · 기록 05 4장",
         related_columns=("gold_promo_calendar.code",)),
    Term(term="매출 예외 행", aliases=("sales_exception_flag",),
         definition="취소인데 `sales` 가 0이 아닌 행. 예외 플래그를 달아 KPI 집계에서 제외한다. 해당 행은 정확히 1건(2026-08-20, 12,100원)이다.",
         status="확정", source_note="기록 03 1장 매출 예외 행",
         related_columns=("silver_reservations.sales_exception_flag",)),
)

#: 폐쇄 목록·enum — SPEC-001 §4 가 SoT
ENUMS: dict[str, list[str]] = {
    "visit_status": ["내원", "취소", "부도"],
    "sentiment": ["긍정", "중립", "부정", "판정불가"],
    "signal_type": ["유기(강남언니)", "개입(네이버)"],
    "line_type": ["Standing(일반)", "Event(이벤트)"],
    "promo_version": ["v1", "v2"],
    "outstanding_direction": ["미수", "수납 선행"],
    "node_type": ["kpi", "intervention", "organic", "exogenous", "unobserved", "attribute"],
    "verdict": ["채택", "자동 확정", "선언", "보류", "기각"],
    "edge_kind": ["causal", "derivation", "exogenous", "candidate", "rejected"],
    "confidence": ["높음", "중간", "낮음"],
    "kpi_status": ["양호", "주의", "경고"],
    "node_state": ["정상", "관찰", "알림"],
    "procedure_concept": [
        "시그니처", "보톡스", "통증 케어", "필러", "제모", "세라셀 / 수액 테라피",
        "리프팅", "메디컬 스킨케어", "스킨부스터", "레이저", "모공 • 흉터",
        "지방분해", "수액",
    ],
}

_INDEX: dict[str, Term] = {}
for _t in _TERMS:
    _INDEX[_t.term] = _t
    for _a in _t.aliases:
        _INDEX.setdefault(_a, _t)


def lookup(term: str) -> Term | None:
    if term in _INDEX:
        return _INDEX[term]
    lowered = term.strip().lower()
    for key, value in _INDEX.items():
        if key.lower() == lowered:
            return value
    return None


def suggestions(term: str, limit: int = 5) -> list[str]:
    """유사 후보 — `UNKNOWN_TERM` 응답에 동봉해 재시도가 헤매지 않게 한다."""
    needle = term.strip().lower()
    pool = list(_INDEX) + list(ENUMS)      # enum 키도 조회 대상이라 후보에 든다
    hits = [k for k in pool if needle and needle in k.lower()]
    return sorted(dict.fromkeys(hits))[:limit] or sorted(t.term for t in _TERMS)[:limit]


def all_terms() -> list[str]:
    return sorted(t.term for t in _TERMS)


def formula_of(metric: str) -> dict | None:
    t = lookup(metric)
    if t is None or t.formula is None:
        return None
    return {"metric": metric, "formula": t.formula,
            "note": t.note, "glossary_ref": t.source_note}


def direction_of(metric: str) -> str | None:
    t = lookup(metric)
    return t.direction if t else None


def label_of(metric: str) -> str:
    t = lookup(metric)
    return (t.label or metric) if t else metric


def unit_of(metric: str) -> tuple[str | None, str | None]:
    t = lookup(metric)
    return (t.unit, t.fmt) if t else (None, None)


#: enum 키 자체를 물었을 때 쓸 설명. Term 이 없는 enum(대부분)도 `get_definition` 으로
#: 닿아야 한다 — SPEC-002 OQ-5 「글로서리 판정 표 + KPI 컬럼 + **enum**」.
_ENUM_NOTES: dict[str, tuple[str, str]] = {
    "visit_status": ("예약 행의 내원 상태. 이 셋 밖의 값이 1건이라도 있으면 실버 빌드가 중단된다",
                     "기록 03 1장 · SPEC-001 §4 enum"),
    "sentiment": ("리뷰 감성 — 예상 평점의 임계값 분류. 중립과 판정불가를 합치지 않는다",
                  "기록 03 1장 리뷰 감성"),
    "signal_type": ("리뷰 신호의 성격. 유기(강남언니)와 개입(네이버)을 한 컬럼으로 합산하지 않는다",
                    "기록 03 1장 개입 신호 · 유기 신호"),
    "line_type": ("시술 라인 구분. 일반과 이벤트는 구조적 쌍둥이라 한 테이블로 통합하고 이 컬럼으로 가른다",
                  "기록 04 4장"),
    "promo_version": ("프로모션 세대. v1 은 기간·존재만, 상세 정본은 v2 다",
                      "기록 03 1장 프로모션"),
    "outstanding_direction": ("미수 방향. `sales` > `receipt` 는 미수, 반대는 수납 선행이다",
                              "기록 03 1장 수납"),
    "node_type": ("온톨로지 노드 유형. **영문 enum 이 정본**이고 한글 표기는 화면 카피다",
                  "SPEC-001 §4 · 기록 07"),
    "verdict": ("엣지 판정. 인과 서술에 쓸 수 있는 것은 채택·자동 확정·선언 셋뿐이고 "
                "보류·기각은 조회는 되지만 사용은 막힌다",
                "SPEC-001 §4 · 기록 07"),
    "edge_kind": ("엣지 종류. 인스펙터 배지가 이 값을 쓴다", "SPEC-001 §4 · 기록 07"),
    "confidence": ("엣지 신뢰도. 자동 확정·선언은 해당 없음(null)이다", "SPEC-001 §4 · 기록 07"),
    "kpi_status": ("KPI 상태 — **그 시점의 값**이 어느 구간인지. 전 기간 백분위 25%/10% 로 가른다",
                   "기록 05 승인 1"),
    "node_state": ("노드 상태 — **최근 7일의 빈도**. 주의·경고인 날이 알림 ≥3 · 관찰 ≥1 · 정상 0. "
                   "KPI 상태와 다른 축이다",
                   "SPEC-003 OQ-5"),
    "procedure_concept": ("시술 개념 폐쇄 목록 13종. 목록 밖 값은 금지이고 추가는 사람이 승인한다",
                          "기록 03 2장"),
}


def _enum_payload(key: str) -> dict:
    definition, source = _ENUM_NOTES.get(key, ("", "SPEC-001 §4 enum"))
    return {
        "term": key,
        "aliases": [],
        "definition": definition,
        "status": "확정",
        "source_note": source,
        "related_columns": [],
        "enum_values": ENUMS[key],
    }


def _enum_key(name: str) -> str | None:
    if name in ENUMS:
        return name
    lowered = name.strip().lower()
    for key in ENUMS:
        if key.lower() == lowered:
            return key
    return None


def definition_payload(term: str) -> dict:
    t = lookup(term)
    if t is None:
        # Term 이 없는 enum 키(visit_status·verdict·node_type …)도 조회 대상이다.
        # 예전에는 「Term 의 **첫** 별칭이 ENUMS 키와 같을 때」만 닿아 13종 중 2종만 나왔다.
        key = _enum_key(term)
        if key is not None:
            return _enum_payload(key)
        raise KeyError(term)
    # 별칭 전체를 훑는다 — 첫 별칭만 보면 순서에 따라 조용히 빠진다
    enum_values = None
    for candidate in (t.term, *t.aliases):
        key = _enum_key(candidate)
        if key is not None:
            enum_values = ENUMS[key]
            break
    payload = {
        "term": t.term,
        "aliases": list(t.aliases),
        "definition": t.definition,
        "status": t.status,
        "source_note": t.source_note,
        "related_columns": list(t.related_columns),
    }
    if t.formula:
        payload["formula"] = t.formula
    if t.note:
        payload["note"] = t.note
    if enum_values:
        payload["enum_values"] = enum_values
    return payload

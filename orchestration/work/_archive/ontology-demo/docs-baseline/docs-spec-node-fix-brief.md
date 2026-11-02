
# [docs] 소수정 — SPEC-001 노드 표·판정/타입 라벨·lag 규칙을 정본 기준으로 정정

너는 **ontology-demo `docs` 워커**다. 같은 워크트리(`docs-baseline`), 같은 규칙.

## 배경

WORK-001 backend 워커가 SPEC-001 §4 node_id 25종 표와 정본의 불일치를 실측 보고했다
(SPEC-001 OQ-6 이 예고한 그 건). **정본이 SoT 다** — spec 을 정본에 맞춘다.
정본 확인은 backend 보고값을 그대로 쓴다 (원천 CSV 를 직접 열 필요 없다 — 아래 §대상이 전부다):

## 대상 — 정정 내용 (backend 실측, 코디 확정)

1. **SPEC-001 node_id 표 8건 정정**:
   - 표기 정정 5건 (spec → 정본): `dow`→`weekday` · `sales`→`sales_total` ·
     `retention_rate`→`retention_rate_60d` · `foreign_channel`→`foreign_inflow_channel` ·
     `promo_avg_discount`→`discount_rate`
   - 노드 교체 3건 (spec 의 `review_campaign`·`organic_new`·`review_positive_rate` 는 정본에 없다 → 삭제하고
     정본의 `visits`(총 내원)·`new_patients_domestic`(한국인 신환)·`sales_foreign_est`(외국인 추정 매출) 등재)
   - OQ-6·※ 표시 해소 (전건 정본 대조 완료로).
2. **node_type enum = 정본 영문값 그대로** (`kpi`/`intervention`/`organic`/`exogenous`/`unobserved`/`attribute`) —
   적재·API·도구가 이 값을 그대로 노출. 한글 표기(개입·유기·외생·미관측·속성)는 화면 카피 매핑으로
   SPEC-004 몫이라고 명시.
3. **엣지 판정 라벨 = 정본 한글값 그대로** (`채택`/`자동 확정`/`선언`/`보류`/`기각`) — spec 이 만든
   `산출0`·`외생` 라벨을 전부 정본 라벨로 치환. **SPEC-002·003·005 와 20-spec/README Terms 표에도
   같은 라벨이 나온다 — 전수 grep 으로 동기하라** (인과 서술 허용 = 채택·자동 확정·선언 3종, 건수 4·14·3·3·3).
4. **lag 규칙 명확화**: 적재(`ontology_edges.lag`)는 정본 문자열 원형 보존(`2w`·빈 값 포함).
   API·도구 노출은 `lag`(원형) + `lag_days`(일 단위 정수, `2w`=14, 빈 값=null) 병기 —
   SPEC-002·003 의 「전건 `<정수>d`」 AC 를 이 규칙으로 교체.
5. 개정 spec 의 `updated_at`·version(patch 올림)·log.md 엔트리 1줄.

## 하지 말 것

- 위 5건 외 수정 금지. 30-work·decision 무변경. 커밋·push 금지.

## 완료 보고 — 동일 2채널 (preamble 값, 코디 `term_45e793be-0adb-44c7-9d9a-eb35c4f48320`)

body 에: 파일별 정정 건수 / 라벨 치환 grep 수치 / 남은 불일치 0 확인.

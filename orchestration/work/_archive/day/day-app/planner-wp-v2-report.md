# planner-wp-v2 결과 보고 — Delivery #235 v2 갱신 입력

## 상태: done (입력 JSON 작성까지 · CLI plan/apply · 승인 receipt · GitHub · 커밋 없음)

## 산출물 (allowed_paths 2개)

- `delivery-request-v2.json` — `start-delivery` CLI 입력(기존 #235 갱신용). 별도 WP 원장 아님.
- `planner-wp-v2-report.md` — 이 보고서.
- 스펙 트리(HEAD `1551fa22` · clean) · 30-work · 코드 · 옆 세션 수정 없음. 생성 스크립트는 scratchpad 에만.

## 계약 요지

| 칸 | 값 |
|---|---|
| idempotency_key · product · root | `day/day-app` · `day` · `products/day` (v1 과 같음) |
| contract_version · risk | **2** (v1 +1) · **L3** 유지 |
| target_specs | `DAY-SPEC-003` · `DAY-SPEC-001` (유지) |
| spec_baseline_revision | `3f57c1af09afa7ce185cd754244c714bf1ec11e5` = latest origin/main(로컬 `git rev-parse origin/main` 일치). main 에 SPEC-003 없음 · SPEC-001 `status: draft` → **pending 그대로**. 1551fa22 는 원천 표기만, ready 위장 없음 |
| scope_delta | 문자열 1개(973자) — v1 plan_digest `sha256:c4f70ae3…` · contract `sha256:f3d03f99…` → v2 사유(사용자 2026-11-10 UI 교정 13항목 · 바뀐 계약 · 보존 계약 · app/ 만 · L3 유지 · baseline pending) |
| target_delta 14 | v1 8개를 「[v1 · 완료된 기반 · 회귀 대상 — PR #237 head 0b776e90]」로 보존 + v2 UI 6개 |
| acceptance 26 | 완료 정의(v2) + v1 A1 ~ A13(A2 · A8 · A12 · A13 개정, 나머지 원문) + **A14 ~ A25 신규** |
| non_goals 11 | v1 8개 중 3개를 v2 와 충돌 없게 고침 + D-5 · 옆 세션 기능 · SPEC 수정/머지/receipt 대행 3개 추가 |
| execution | code_surface = app/ 만 · dependencies 7 · phases 0~7 · verification 5 · rollback(v2 revert + v1 보존) · open_questions 3 |

## 13항목 → Acceptance 매핑

| # | 사용자 확정 | v2 Acceptance | SPEC-003 @1551fa22 |
|---|---|---|---|
| 1 | 하단 4메뉴 · 예약 「곧 출시 예정」 · 5번째 탭 없음 | A14 · A8(탭바/레일) | A-25 · A-13 |
| 2 | 머리 DAY · 종 · 배지(D-5 전 없음) · 설정 계정 | A15 | A-26 · A-27 |
| 3 | 필터 4개 · inbox.section | A14 | U-2 · OQ-A2 |
| 4 | 4행 카드 | A16 | A-28 · OQ-A27 |
| 5 | 마취 한 줄 · long 빨강 · 마취 완료 N분 | A17 | A-29 |
| 6 | 목록 카드 호출 상태 · 카드에서 수락 · 상세 강조 상자 | A18 · A19 | A-30 · A-31 |
| 7 | 원장 즉시 본인 · 간호사 드로어 대리 · 3곳 공통 | **A2 개정** | A-2 · OQ-A28 |
| 8 | 상세 머리 · 메모 여백 · 시술 카드 · 완료 회색 · 세로 ⋮ | A19 | A-31 |
| 9 | 상시 체크박스 없음 · 호출 시트(시술+원장) | A20 | A-32 |
| 10 | 모두 완료 상자 · 귀가 대기 | A21 | A-33 |
| 11 | 원형 통역 드로어 · 칩 | A22 | A-36 |
| 12 | TW → zh-Hant · 같은 언어 · 덮지 않음 | A23 | A-35 |
| 13 | 성공 토스트 2.6초 · 되돌리기 없음 · 본인 조작만 | A24 | A-34 |
| — | 스크린샷 시각 검수(원본 프로토 read-only) | A25 | — |

## 기존 계약 보존 · 완료 기반

- v1 A1 · A3 ~ A7 · A9 ~ A11 원문 그대로(환경 연결 · 세션 보안 · SSE · 푸시/통역 클라이언트). D-1 은 재발주 없이 「완료된 기반 · 회귀 대상」.
- 옛 수치(앱 155 · native 47 · 서버 663 · analyze 0 · unsigned 17.6MB)는 **옛 head 0b776e90 실행 기록**으로만 적고 v2 완료 근거로 쓰지 않는다(완료 정의 · A12).
- A13: v2 후속 커밋 경로 = `git diff --name-only 0b776e90…..HEAD` 가 app/ 만. PR #237 의 v1 backend 변경은 누적 diff 로 남되 새 backend 수정 승인 아님(non_goals).
- 코드 PR #237 → dev 하나 · 이슈 #235 하나 유지 · 머지는 사용자 마지막 지시 · 문서 선머지 게이트 없음(dependencies 에 명시).

## v1 대비 충돌 정리 (Non-Goals ↔ Acceptance 0건)

| v1 Non-Goal | v2 처리 |
|---|---|
| 「국적 → 언어 자동 선택(OQ-A9)」 | SPEC 확정분(TW + 프로토 대응)은 범위, HK · VN 등 미확정분만 non-goal |
| 「예약 · 내원 · 설정 탭 · 알림 목록」 | 4메뉴 자리 · 예약 문구 · 설정 계정은 범위, 예약/채팅 기능 · 내원현황 · 설정 상세 · 알림 목록은 non-goal |
| 「D-1 · AGENTS.md 외 backend 변경」 | 「v2 후속은 app/ 밖 변경 없음」으로 강화 |
| v1 A2 「원장 기본 선택 = 본인」 | v2 A2 「원장 창 없이 즉시 본인」으로 대체 |
| v1 U-13 「성공 토스트 없음」(SPEC) | A24 성공 토스트 · 되돌리기 없음 |

## 옆 세션 호환 — 판단 · 적용 안 함, 차이만 표시

원천: 옆 SPEC-002 브랜치 `e421b77b4bb836c7c557419dd3fad22db1900862`(미머지 · 개정 ⑬ ⑭) · 옆 코드 `a1c90b9dc63271dc06023ec0a530c53a216a296c`(미머지 · 확인용).

| # | 옆 SPEC-002 / 코드 | SPEC-003 @1551fa22 | 앱 영향 |
|---|---|---|---|
| ① | [재호출] 호출 줄에 늘(:169) · `tasks[].canRecall`(board_rules.py:180 · :546) | A-22 need.why = call 조건 | A2 재호출 노출 |
| ② | 시작/완료 취소 확인 창(:208 · :319-320 · :735) | U-7 · A-31 확인 없이 | A19 ⋮ |
| ③ | 확인 필요 5상황 · `need` → `needs[]`(:235-251 · :710-711 · 코드 :621) | need.why = anes · call | A7 · A2(need.why) — **스냅샷 칸 깨짐** |
| ④ | 마취 회차 · `lastMinutes` → `lastSeconds` 「mm:ss」(:219 · :503 · 코드 :607) | A-29 「마취 완료 {N}분」 | A17 — **스냅샷 칸 깨짐** |
| ⑤ | pickable = 준비중만(:167 · 코드 :173-178) | pickable 서버 값 그대로 | A20 시트 체크 범위(앱 로직 영향 적음) |
| ⑥ | 담당 원장 바꾸기 API · 알림(:443 · :725 · OQ-29 :796 · router :201) | 없음 | 범위 밖(non_goal) |

- Review Surface 1행 + dependencies 2행(SPEC 대조 · backend 머지 시 스냅샷 회귀) + **phase 1 「구현 직전 최신 병합 SPEC-002 ↔ SPEC-003 대조 · 다르면 SPEC-003 먼저 정합 후 재버전업」**으로 둠. 순수 UI 항목은 그 대조를 기다리지 않음.
- Acceptance 는 SPEC-003 @1551fa22 기준 하나만 약속(A-22 조건 · 확인 없음 · lastMinutes) — always/확인 창을 동시에 약속하지 않음. 옆 세션 진행 · 머지 상태는 추측하지 않음.

## 검증

- JSON 파싱 OK · `jsonschema` Draft 2020-12 로 `delivery-request.schema.json`(+ `delivery-issue.schema.json` execution ref) 검증 → **0 errors**
- harness 실제 모델 `mediness_harness.workflow.DeliveryRequest.model_validate` → **OK**(contract_version 2 · L3 · scope_delta 973자)
- scope_delta 형식: schema `string | null` · harness 는 contract digest 가 다르면 scope_delta 필수 + `contract_version == 이전 + 1` 검사(workflow.py:1060-1065) → v1=1 → v2=2 충족. v1 contract 는 #235 스냅샷 `delivery235-current.json` meta `contract_version=1` · digest `f3d03f99…` 와 대조함
- baseline 검사: harness 는 계약이 바뀌면 `spec_baseline_revision == fetch 한 origin/main` 요구(workflow.py:1042) → `3f57c1af…` 가 현재 origin/main 과 같음(코디 plan 때 다시 fetch 해 확인 필요)
- 40자 full SHA 6개(0b776e90 · 1551fa22 · 3f57c1af · 91728737 · a1c90b9d · e421b77b) 모두 실제 rev-parse 값. 8자 약칭은 같은 full SHA 를 이미 적은 뒤 보조 표기로만
- 코드 · 문구 · 번역 · API 발명 없음(문구는 SPEC-003 · 프로토 원문 참조만)

## 남은 단계 · 주의

1. 코디: 독립 리뷰 → `start-delivery` plan(fetch 로 origin/main 재확인) → L3 이라 새 plan_digest 에 사람 승인 receipt → apply 로 #235 를 v2 로. v1 승인 · evidence 는 stale 이 된다(receipt 복제 금지).
2. 승인 뒤 app/ 후속 구현은 사용자 지시가 있을 때(이번 범위 아님). phase 1 옆 SPEC-002 대조가 업무 동작 항목 앞에 있다.
3. SPEC-003 OQ-A8 · A18 ~ A28 · A9 남은 것은 기본값 · 후속 확인점 그대로(새 질문 없음). 다른 원장 지정 호출 본인 수락 = 현 서버 성공 사실 보존 · 새 차단 없음.
4. 옆 backend 가 dev 에 먼저 머지되면 지금 앱(need · lastMinutes)이 회귀할 수 있다 — 머지 순서는 사용자 결정.

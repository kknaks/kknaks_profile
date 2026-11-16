
# [frontend] WORK-004 후속 픽스 — 검수 경고 3건 + 픽스처 정합 2건

너는 **ontology-demo `frontend` 워커**다. WORK-004 이어서(커밋됨 — 그 위에 변경만 남겨라, git 조작 금지).
검수 리포트 참조(read-only): `/Users/kknaks/orca/workspaces/kknaks_profile/ontology-demo/orchestration/work/work-001-data-foundation/review-work-004-report.md`

## 할 일 (전부 app/front/ 안, 소규모)

1. **W2** 토큰 hex 이중 전사 해소 — encoding.ts·causal-graph.tsx 의 hex 를 한 곳(토큰 정의)으로 단일화.
2. **W3** '최근 7일' 카피를 응답 window_days 파생으로.
3. **◀ 비활성** — SPEC-003 v0.0.5 에 has_prev_period 가 생겼다(has_next_period 대칭). 스테퍼 이전 화살표 비활성에 사용, mock 픽스처에도 반영(2026-01 에서 false). 기간이 조용히 최신으로 튀는 경로 제거.
4. **sign 문자 정합** — 엣지 sign 은 정본 원형 U+2212('−')다. 픽스처·비교 로직을 U+2212 기준으로 통일(ASCII '-' 비교 잔존 0).
5. **error_code 대비** — 채팅 실패 응답에 error_code(AI_TIMEOUT/AI_FAILED 구분)가 계약으로 들어온다(SPEC-003 개정 예정). 픽스처와 분기에 반영해 AC-12 5종이 성립하게.

## 검증 — `cd app/front && npx tsc --noEmit && npm run build` 1회.

## 완료 보고 — 2채널 (preamble 값, 코디 term_45e793be-0adb-44c7-9d9a-eb35c4f48320), subject "frontend 완료: WORK-004 fix", body 항목별 처리+검증 수치.

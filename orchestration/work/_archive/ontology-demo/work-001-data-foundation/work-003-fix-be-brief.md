
# [backend] WORK-003 WARN 수정 — W1·W2 필수, 나머지 판정

너는 **ontology-demo `backend` 워커**다. WORK-003 이어서. 리포트 (read-only):
`/Users/kknaks/orca/workspaces/kknaks_profile/ontology-demo/orchestration/work/work-001-data-foundation/review-work-003-report.md`

## 필수 2건

- **W1**: SPEC-005 OQ-5 확정은 '스키마 위반 시 1회 재시도 후 실패'다 — `ai_schema_retry` 를 실제로 읽어
  1회 재시도를 구현하라(재시도도 실패하면 failed·error_code). 독스트링 3곳을 실동작과 일치시키고 회귀 1건
  (1차 위반→재시도 성공 / 2연속 위반→failed).
- **W2**: citations 에 period 가 없으면 느슨한 재조회로 빠지는 역전 제거 — single_row/aggregate 등 기간이
  의미 있는 인용은 period 필수(없으면 검증 실패 방향), 기간 무관 인용만 명시적 면제. '지시를 어긴 응답이
  더 느슨한 검사를 받는' 경로가 없음을 회귀로 고정(period 누락 픽스처 추가).

## 나머지 경고 3건·nit 5건 — 리포트 읽고 「수정함/안 함+사유」. W5(compose 의 ontology-mcp·agent 서비스 부재)는 WORK-005 이월 — 손대지 마라.

## 완료 — 테스트 전건 통과. 보고 2채널(코디 term_45e793be-0adb-44c7-9d9a-eb35c4f48320), subject "backend 완료: WORK-003 fix".

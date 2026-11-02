
# [backend] 긴급 소수정 — /api/graph verdicts 전송 형식 (사용자 E2E 실측 버그)

너는 **ontology-demo `backend` 워커**다. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/work-001-data-foundation`, `app/ontology-agent/` 만, git 조작 금지.

버그: FE 가 `verdicts=채택,자동 확정,선언,보류,기각`(콤마 결합 단일 파라미터)로 보내는데
API(`api/monitoring_router.py:61`)가 `list[str]` 반복 파라미터로만 받아 전체 문자열을 판정값
1개로 읽고 400 INVALID_RANGE. 계약이 전송 형식 미정이었다 — 코디 확정: **콤마 구분 단일
파라미터가 정본, 반복 파라미터도 허용**(SPEC-003 v0.0.12 로 docs 동기 중).

할 일: 받은 verdicts 각 항목을 콤마 split·trim 해 평탄화. 알 수 없는 판정값 에러는 기존 유지.
회귀 2건(콤마 단일 200+필터 동작 · 반복 파라미터 200). 관련 테스트만 실행.
보고 2채널(코디 term_9b07d036-3622-4fc7-9d9e-a5fda263b871), subject "backend 완료: verdicts hotfix".

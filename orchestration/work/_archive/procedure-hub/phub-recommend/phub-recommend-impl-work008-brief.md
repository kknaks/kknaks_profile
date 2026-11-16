# 발주서 — WORK-008 구현(허브 · SPEC-005 v3.3 0.3.4)
정본 `SPEC-005.md`(0.3.4 · §5-16 T11 짧은 fact 꼴 · peek bytes = 실제 expand 본문 바이트 · §5-0-1 크기 표 측정값 기준 · §5-13 C′ · §6-7 끝 조건 · 걸음 재생 규칙) · `WORK-008.md`(WP-0~5) · 검수 `review-v33-v22-report.md`(005 PASS · WARN 8 은 planner 가 패치 중 — 의미 변경 없음 · Scope 에 `tests/test_gold_tools.py` 추가) · 배경 `phub-recommend-walk-fix-context.md` · 측정 `spec005-v33-measure.py/.json`.
코디 결정: V-15 cut 줄 원문은 받되 걸음 예산에 포함 · V-17 바이트 셈 = compact 직렬화(앱도 같게) · V-18 걸음에서는 1쪽.
순서: WP-0 walk3 측정 기준선 → WP-1 expand 짧은 꼴 → WP-2 peek bytes · n_facts → **WP-2 끝나면 heartbeat 「꼴 확정」**(앱 WORK-009 착수 신호 · 코디에게 ask 아님) → WP-3 상한 · 기존 시험 · recheck2 쪽 넘김 → WP-4 발행 · 측정 → 「재시작 요청」 ask → 코디 재시작 → base-url 재측정 → worker_done.
끝 조건 = SPEC §6-7(섹션당 중앙 ≤2KB · 걸음 재생 평균 ≥3 · 이웃 도달 ≥85% · peek bytes 차 0 · 기존 품질 6/6 · 106/106 · 결정론 · 시험 · ruff). 미달이면 멈추고 ask(숫자 · 손잡이).
제약: 로컬 커밋 · push 금지 · 실버 · 시맨틱 · 앱 수정 금지 · 18005 는 코디가 재시작 · 사용자 포트 · procedure-* 손대지 않음 · 추측 금지.

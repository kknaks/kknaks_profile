# 발주서 — WORK-010 구현(허브 · SPEC-005 v3.4 0.3.5 · 실버 9단계 골드 반영)
정본 `SPEC-005.md`(0.3.5 · §2-1 입력 13 · 가드 · §3-1 G19~G22 · §4-3 section 18 · §5-14 I-04 · §5-16 · §6-8 끝 조건) · `WORK-010.md`(WP-0~5 · 코드 표면 grep) · 검수 `review-spec005-v34-report.md`(FAIL 1 = 006 짝 의존 · planner 가 패치 중 — 허브 구현엔 영향 없음 · WARN 5 패치 중) · 입력 `step9-decisions.json` · `step9-explanations.json` · `semantic.json`.
할 일: WP-0 셈 스크립트 → WP-1 입력 · section → WP-2 G19~G22(② resolved 하나 · alternatives id 메타만 · D-13b) → WP-3 도구(safety.management · globals) → WP-4 **발행까지**(DB 포인터) · 측정(in-process) → 「재시작 요청」 ask 는 보내되 **코디가 rerun-v6b 끝난 뒤(약 01시) 재시작** — 그 전엔 18005 를 띄우지도 끄지도 말 것 → base-url 재측정 → worker_done.
끝 조건 = §6-8(빌드 결정론 · 가드 · step9 fact 5,273 export · section 셈 · A 닫힘 51/54 · 25/30 · 품질 6/6 · 106/106 · walk3 회귀 없음 · 크기 표 영향 보고). 미달이면 ask.
제약: 로컬 커밋 · push 금지 · 실버 · 시맨틱 수정 금지 · 앱 수정 금지 · 사용자 포트 · procedure-* 손대지 않음 · 추측 금지.


# [docs] 초소수정 — SPEC-001 부분 월 판정식 등재

너는 **ontology-demo `docs` 워커**다. 같은 워크트리, 같은 규칙. 한 가지만:

WORK-001 검수(리뷰어 의견, 코디 승인)에 따라 SPEC-001 §4 `gold_kpi_monthly` 에
**부분 월(is_partial_month) 판정식**을 계약으로 등재한다 — 주별 규칙 준용:
「해당 월의 관측일 수(days_observed)가 달력 일수보다 적으면 부분 월. 결측일(예: 2026-02-17)이
있는 달도 부분 월로 잡힌다. 응답에 `is_partial_month`·`days_observed` 노출.」
version patch(v0.0.5→0.0.6)·updated_at·log.md 1줄. 다른 수정 금지. 커밋·push 금지.

완료 보고: 동일 2채널 (preamble 값, 코디 term_45e793be-0adb-44c7-9d9a-eb35c4f48320), subject "docs 완료: 부분 월 등재".

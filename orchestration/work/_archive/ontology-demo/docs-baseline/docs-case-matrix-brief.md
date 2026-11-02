
# [docs] 초소수정 — SPEC-001 Case Matrix 에러 코드 6종 등재

너는 **ontology-demo `docs` 워커**다. 같은 워크트리, 같은 규칙. 한 가지만:

WORK-001 fix 에서 구현이 실제로 던지는 에러 코드 6종이 SPEC-001 Case Matrix 에 없다 — 등재하라
(backend 실구현 기준, 코디 승인): `AGREEMENT_BELOW_THRESHOLD`(강남언니 정합률 미달 — 빌드 중단) ·
`REVIEW_SCORE_VIOLATION` · `MASKING_RESIDUE`(기존 코드에서 분리) · `SILVER_ROWCOUNT_MISMATCH`(실버 산출 행수 대사 불일치 — 중단) ·
`UNKNOWN_BRANCH` · (기존 REBUILD_MISMATCH 의 트리거 조건에 「전 게이트 통과 시에만 스왑 채택」 서술 보강).
정확한 이름·조건은 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/work-001-data-foundation/app/ontology-agent/build/errors.py` (read-only)를 대조해 옮겨라 — 발명 금지.
version v0.0.6→0.0.7 · updated_at · README Spec List 버전 동기 · log.md 1줄. 다른 수정 금지. 커밋·push 금지.

완료 보고: 동일 2채널 (preamble 값, 코디 term_45e793be-0adb-44c7-9d9a-eb35c4f48320), subject "docs 완료: Case Matrix 6종".

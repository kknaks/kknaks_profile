# [backend] CENTURION_DAY#234 구현 — 데모/운영 연결 구분 없앰

너는 이 작업의 day backend 워커다(앞서 seed_demo_board.py 를 만든 세션). 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/roles/day/backend/role.md`(+ 같은 폴더). 레포 `AGENTS.md` 먼저.

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-procedure-board-2`(base origin/dev 91728737). 미추적 `scripts/seed_demo_board.py` · `backend/tests/scripts/` 는 그대로 둔다(같은 PR 에 들어감).

## SSOT
- **Delivery Issue #234**(결과 계약 · 사용자 승인 2026-11-09): `gh issue view 234 --repo MediSolveAIDev/CENTURION_DAY` — 바뀌는 것 · 하지 않는 것 · 완료 조건 A1~A5 · 실행 정보(수정 후보 · verification 목록 · rollback). **여기 없는 건 발명하지 마라.**
- 스펙(PR #920 · 미머지): `/Users/kknaks/orca/workspaces/mediness-mediness/day-procedure-board-2-spec/products/day/20-spec/` spec-000 · 001 · 002(개정 ⑫ · §3 KOS 쓰기 표)
- 자리 전수: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-procedure-board-2/research-demo-vs-live-report.md` §1 · §3 · 리뷰 W3 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-procedure-board-2/review-doc-demo-vs-live-report.md`

## 배경
사용자 결정: KOS 데모와 실제 병원은 같은 API · 테넌트만 다르다. dev/prod 분리는 스키마의 연결 데이터로 된다. 코드에서 `is_demo` 로 동작을 가르는 모든 분기와 칸을 없앤다.

## 단계 (Issue 실행 정보 순서)
1. (가) trial 구분 제거 — factory · config · writes · adapter · board · deploy config · docs/development/deployment.md
2. (나) APP_ENV 연결 거르기 제거 — crm_connections · tasks/emr · emr_sync · board._connection · auth(처음 · 다시 고를 때)
3. (다) is_demo 칸 삭제 — 새 migration(forward-only) · 모델 · ConnectionConfig · fingerprint · 시드 · public.py · scripts/seed_demo_connection.py
4. 테스트 정리 · 새 테스트(데모 · 실제 병원 연결 픽스처 둘에서 같은 op) · Issue verification 목록 전부(W3 `test_board_api.py:370-` 포함)

**전수조사**: 끝나면 `git grep -n -E 'is_demo|trial_writes|TRIAL_STEPS|TRIAL_WRITES|kos_trial_writes_on_live|demo connections only'` 로 남은 것을 전부 보고(남겨도 되는 것은 사유 — 예: seed_demo_board 의 함수 이름). 목록 밖에서 걸린 자리도 고친다.

## 하지 말 것
- 화면 · API 계약 · 화면 문구 변경 금지
- 다른 not-supported 경로(시스템 계정 없음 등)는 남긴다(Issue 「바뀌는 것」 5번째)
- /dev/kit* · /docs · APP_ENV 필수 · prod↔day_prod 짝 검사는 그대로(Non-Goals)
- 커밋 · push · PR 금지 · 사용자 포트 · 프로세스 · day-local 건드리지 않음 · 공유 dev/prod DB 금지(테스트 DB 는 로컬 compose)
- A6(데모 실물)는 dev 배포 뒤 코디 · 사용자 몫 — 하지 마라

## 검증
- 단계마다 관련 테스트만 1회. 끝에 한 번: `uv run pytest -q -m 'not infra'` · compose postgres/redis 위 `scripts/test.sh -q`(migration upgrade 포함) · `uv run ruff check backend scripts` · format
- A1~A5 를 하나씩 근거(테스트 이름 · grep 결과)와 함께 보고

## 완료 보고
원 브리프(`/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-procedure-board-2/day-procedure-board-2-be-brief.md` §9)와 같은 두 명령, 코디 핸들 `term_b915fb18-742f-4779-962c-79848020b8d5`. 변경 파일 · 단계별 요약 · A1~A5 판정 · 테스트 수 · grep 결과 · migration revision.

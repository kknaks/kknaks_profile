# [backend] CENTURION_DAY#236 구현 — backend 단계 (기획안 맞추기)

너는 day **backend** 워커다. 역할 문서 먼저: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/roles/day/backend/role.md`(+ 같은 폴더) · 레포 `AGENTS.md`.

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-procedure-board-2`(브랜치 `kknaksss/day-procedure-board-2` — 이미 커밋 481fe102 시드 스크립트 · 96fff917 #234). 그 위에서.

## SSOT
- **Delivery #236 v2**(사용자 승인 2026-11-10 · delivery-plan:approved): `gh issue view 236 --repo MediSolveAIDev/CENTURION_DAY` — Target Delta 16 · Acceptance A1~A10 · Execution(backend phase 1~3 · frontend phase) · Non-Goals. **여기 없는 건 발명하지 마라.**
- 스펙: `/Users/kknaks/orca/workspaces/mediness-mediness/day-procedure-board-2-spec/products/day/20-spec/spec-002-procedure-board.md` 개정 ⑬ · ⑭(U-1 · U-3 ~ U-8 · U-10 · U-12 · U-13 · 규칙 · 케이스 매트릭스 · 스냅샷 모양 · API · KOS 쓰기 표 · 「이번에 안 하는 것」 표)
- 결정 정본: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-procedure-board-2/_RESUME.md` §2(11-09 ~ 11-10 기획 · 디자인 행)

## 범위 — backend phase 전부(Issue Execution 대로)
서비스 · 규칙 · 쿼리 · API(JSON) · 스냅샷 · KOS 쓰기 · 테스트. 예: 체크 가능 규칙(준비중만) · 「시술 완료」 탭 검색(이름 · 담당 원장 · 관리실 — 서버에서 거름) · 확인 필요 5상황 계산(since · 풀리는 때 · 기준 분 env) · 마취 회차 · [귀가 대기]가 열린 마취 닫기 · 담당 원장 바꾸기(라우트 · change-tasks-doctors 1명 덮어쓰기 · 새 원장 표시 · 수락 뒤 미시작 다시 셈 · event_log) · 동시 수락 거절 · 스냅샷 필드(스펙 모양 그대로).

**frontend 몫(템플릿 · 화면 라우터(api 제외) · static · styles)은 손대지 마라** — 다음에 frontend 워커가 한다. 화면이 쓸 값(스냅샷 · HX 조각에 넘길 값)은 스펙 모양대로 준비만.

## 하지 말 것
- 화면 문구 지어내기 금지(스펙 · 결정 「」만) · Non-Goals 금지
- 커밋 · push · PR 금지 · 사용자 포트 · 프로세스 · day-local api/worker 건드리지 않음(로컬 compose postgres · redis 는 떠 있음 — 테스트에 써도 됨) · 공유 dev/prod DB 금지 · KOS 호출 금지(실물은 코디 · 사용자)

## 검증
phase 마다 관련 테스트만 1회. 끝에 `DAY_ENV_FILE=/Users/kknaks/git/CENTURION_DAY/deploy/local.env scripts/test.sh -q`(infra 포함) 1회 · `uv run ruff check backend scripts` · format. Acceptance 별 판정(테스트 이름) 보고.

## 완료 보고 (두 명령 모두)
```bash
orca orchestration send --to term_28f2b422-a0ae-490a-bbed-aeb19fbd7fdd --from <네 워커handle> --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "backend 완료: <한 줄>" --body "변경 파일 / phase 별 요약 / Acceptance 판정 / 테스트 수 / 미결"
orca terminal send --terminal term_28f2b422-a0ae-490a-bbed-aeb19fbd7fdd --text "[worker_done] backend 완료 — <한 줄>. 상세는 인박스." --enter
```
막히면 `orca terminal send --terminal term_28f2b422-a0ae-490a-bbed-aeb19fbd7fdd --text "[질문] backend: <질문>" --enter`. 핸들은 dispatch preamble 값이 맞다.

# [backend + frontend] CENTURION_DAY#239 구현 — 차트 작성 · 방 이동

너는 day 워커다. 역할 문서 먼저: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/roles/day/backend/role.md` · `.../frontend/role.md`(+ 같은 폴더) · 레포 `AGENTS.md`. 이번엔 backend 와 frontend 둘 다 네 몫이다(Execution phase 순서대로).

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-procedure-board-2` — 브랜치 `kknaksss/day-procedure-board-2`. **먼저 `git pull --ff-only` 로 최신(origin head f1e67a2c — #234 · #236 · 앱 · 채팅 · 알림 합친 상태)을 받는다.** 그 위에서.

## SSOT
- **Delivery #239**(사용자 승인 2026-11-10): `gh issue view 239 --repo MediSolveAIDev/CENTURION_DAY` — Target Delta ① ~ ⑦ · Acceptance A1 ~ A10 · Non-Goals · Execution(수정 후보 · phase · 응답 모양 = #236 ⑲ · rollback). **여기 없는 건 발명하지 마라.**
- 스펙: `/Users/kknaks/orca/workspaces/mediness-mediness/day-procedure-board-2-spec/products/day/20-spec/spec-002-procedure-board.md` 개정 ⑯ · `spec-000-data-model.md`(커밋 4490876e) — U-12 · U-14 · U-15 · 규칙 3 · 23 · 28 ~ 33 · KOS 쓰기 표 · 동기화 표 · 스냅샷 · 매트릭스 · OQ-38 ~ 50
- 결정 · HAR: 같은 폴더 `_RESUME.md` §2(11-10 차트 · 방 이동 행) · `research-har-room-chart-report.md` · `e2e-feedback.md` F10

## 핵심
- ① 「방 배정」 판정 = `crm_connection.config.room_assign_etc_task_id` ↔ KOS `etceteraConfiguration.etceteraTaskId` → `visit_task.is_room_assign` · 그 밖 기타 작업은 판 시술 줄에 보임 · 기타 작업도 [종료]해야 [귀가 대기] · 데모 설정 값 `683ba150dccf503ddc5487e9`(로컬 · dev 데이터 넣는 방법은 Execution 대로 — 시드/스크립트)
- ② migration(새 revision · 지금 head 다음): `is_room_assign` · `started_room_id` · `visit_task_chart_log` — downgrade() 는 테스트용으로 두되 운영에선 안 돌림
- ③④ 차트: 탭 · 표 · 직무별 첫 탭 · 담당자(DAY 만 · 필수 · 처음 값) · 집도의(KOS) · 메모 KOS(assignee/doctor memo) · 자동 저장(blur + 약 2초) · 「최근 저장 : HH:MM」 · 이력 · 동시성 · 시술 전 의사차트 = DAY 만 → [수락] 때 검증 뒤 KOS · KOS 웹 수정 → DAY 반영 + 이력(source kos)
- ⑤ 방 이동: 방 이름 → 방 목록 팝오버 + 푸터 「점유 이동」 「이동」 · 점유 이동 = 기존 방에 「방 배정」 남기고(없으면 add-flow-tasks + change-tasks-room) 나머지 전부(완료 포함) 새 방 · 이동 = 전부 · 점유 중엔 [복귀하기]만(room_held) · 복귀 = 「방 배정」 cancel + 전부 원래 방 · 파란 띠 · 기존 방 카드 없음 · 제한 없음
- ⑥ started_room_id · 「시술 완료」 탭 원래 방 묶음(오늘만)
- 웹 조작 응답 = 누른 카드 + OOB + version(#236 ⑲)

## 하지 말 것
화면 문구 지어내기(스펙 「」만 · 없으면 OQ 대로 비움) · Non-Goals · 손 CSS · 인라인 스크립트 · 커밋 · push · PR · 사용자 포트/프로세스(로컬 11040 재기동은 코디) · 공유 DB · **KOS 호출 금지**(데모 실물 A9 는 코디 · 사용자). 앱(`app/`) 은 손대지 마라 — 앱 세션 몫.

## 검증
phase 마다 관련 테스트 · 끝에 `DAY_ENV_FILE=/Users/kknaks/git/CENTURION_DAY/deploy/local.env scripts/test.sh -q`(전부) 1회 · ruff check · format · build-css · alembic heads 하나 · 손 CSS · 인라인 grep 0. Acceptance 별 판정(테스트 이름). 앱이 쓸 새 JSON API(차트 · 방 이동) 경로 · 본문 목록을 보고에 따로.

## 완료 보고
`orca orchestration send --to term_28f2b422-a0ae-490a-bbed-aeb19fbd7fdd --from <네 워커handle> --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "#239 완료: <한 줄>" --body "<변경 파일 · phase 별 · Acceptance · 테스트 수 · migration revision · 앱용 API 목록 · 미결>"` + `orca terminal send --terminal term_28f2b422-a0ae-490a-bbed-aeb19fbd7fdd --text "[worker_done] #239 완료 — <한 줄>" --enter`. 막히면 `[질문] …` 을 같은 터미널에 send.

# [reviewer] 코드 리뷰 — CENTURION_DAY#239 (차트 · 방 이동 · 방 배정 판정)

너는 day reviewer 다. 역할 문서 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/roles/day/reviewer/role.md`(+ 같은 폴더). **읽기만** — 레포 수정 · 커밋 · KOS 호출 · 공유 DB 금지. pytest · ruff 는 돌려도 됨(`DAY_ENV_FILE=/Users/kknaks/git/CENTURION_DAY/deploy/local.env scripts/test.sh -q`).

대상: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-procedure-board-2` — `git diff`(HEAD f1e67a2c 위 미커밋 50파일 · migration 0008_chart_room). 워커 보고: 같은 폴더 `code-239-report.md`.

## SSOT
Delivery #239(승인 · `gh issue view 239 --repo MediSolveAIDev/CENTURION_DAY`) · 스펙 PR #921 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-procedure-board-2-spec/products/day/20-spec/` SPEC-002 개정 ⑯ · SPEC-000 · 결정 `_RESUME.md` §2(차트 · 방 이동 · 방 배정 id 행).

## 볼 것
1. Acceptance A1 ~ A8 · A10 이 스펙대로이고 테스트가 실제로 막나 — 「방 배정」 판정(설정 id · 비었을 때) · 기타 작업 보임 · [종료]해야 귀가 대기 · 차트(담당자 DAY 만 · 집도의 KOS · 메모 KOS · 자동 저장 · 이력 · baseLogId 충돌 · 시술 전 의사차트 DAY 만 → 수락/호출 없는 시작 때 검증 · KOS 수정 반영 · guard) · 방 이동(점유 이동 완료 포함 전부 · 방 배정 남김/만들기 → 다음 조회 뒤 이동 · 점유 한 번 room_held · 복귀 · 띠 · 원래 방 묶음 · started_room_id)
2. outbox 순서 · 중복 쓰기 · 반쯤 실패(집도의 → 메모 · add-flow-tasks → change-tasks-room) · 「조용히 통과하는 자리」
3. migration 0008(head 하나 · downgrade 있음 · 기존 데이터에서 upgrade) · 차트 이력 지우지 않음
4. 웹 응답 = #236 ⑲ 모양(누른 카드 + OOB + version) · 화면 글자 새로 지은 것(워커가 밝힌 새 코드 room_assign_unset — 스펙에 없음) · 손 CSS · 인라인 0
5. 앱 JSON API 계약이 스펙과 맞나(앱은 다음 작업 — 계약만)
6. 기존 #234 · #236 · 앱 · 채팅 · 알림 회귀 없음 · test.sh 941 passed 직접 1회

산출물 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-procedure-board-2/review-239-report.md` · FAIL / WARN / PASS · 파일:줄 + 근거. 완료 보고 두 명령(코디 핸들 `term_28f2b422-a0ae-490a-bbed-aeb19fbd7fdd` · worker_done + terminal send).

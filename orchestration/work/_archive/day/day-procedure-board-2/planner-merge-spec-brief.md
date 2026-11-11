# [planner] 스펙 PR 하나로 — #920 + #921 합치기 (#921 로 감)

사용자 결정(2026-11-10): 스펙도 코드처럼 하나로 — **#921(kknaksss/day-app-spec · 앱 세션) 에 합치고 그 PR 로 간다**. #920 은 코디가 닫는다.

작업 = 너의 스펙 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-procedure-board-2-spec`(브랜치 `kknaksss/day-procedure-board-2-spec` · 깨끗해야 함). 앱 세션 워크트리는 건드리지 마라.

## 할 것
1. `git fetch origin` · `git merge --no-commit --no-ff origin/kknaksss/day-app-spec` — **커밋하지 마라**(코디가 확인 뒤 커밋 · push 는 코디가 day-app-spec 로)
2. 충돌 3개 풀기: `products/day/20-spec.md`(목록 — 양쪽 행 다) · `20-spec/spec-001-login-session.md`(우리 = is_demo 거르기 없앰 개정 ⑥ / 앱 = 데모 계정 로그인 환경 — 둘 다 살림) · `40-architecture/mobile-deployment.md`. 자동 병합된 `spec-000-data-model.md` 도 열어 양쪽 칸(is_room_assign · started_room_id · visit_task_chart_log / 채팅 · 기기 · 알림)이 다 맞는지 · `30-work.md`
3. **내용 맞추기**(같은 merge 안에서 고쳐도 됨 — 바꾼 곳을 보고에): 앱 스펙 SPEC-003 · 004 · 005 가 우리 SPEC-002 ⑬ ~ ⑯ 결정과 어긋나는 곳 — 특히 **[재호출] = 창 없이 · 본문 {} · 처음 대상**(앱 코드는 이미 f1e67a2c 로 맞춤) · 체크박스(준비중 · 호출 중) · 「원장 변경」 · 확인 필요 · 마취 · 카드 순서. 결정 정본 = `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-procedure-board-2/_RESUME.md` §2. 판단이 필요한 차이는 고치지 말고 「정할 것」으로
4. 차트 · 방 이동(⑯)을 앱에서 쓸지는 앱 스펙에 없음 — 고치지 말고 「정할 것」에 한 줄
5. log.md 행 · `python3 scripts/lint-pipeline.py --strict` products/day ERROR 0

## 하지 말 것
커밋 · push · PR 조작 · Delivery 조작 · 앱 세션 워크트리.

## 완료 보고
충돌 3개 각각 · spec-000 확인 · 맞춘 곳 · 정할 것 · lint. 코디 핸들 `term_28f2b422-a0ae-490a-bbed-aeb19fbd7fdd`(worker_done + terminal send 두 명령).

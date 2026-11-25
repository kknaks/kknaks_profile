# [planner] SPEC-002 ㉚ · 005 · 006 ⑭ · 007 → WP 나누기 · Delivery Issue 발행

SPEC 은 검수 r3 PASS · 커밋됨: 브랜치 `kknaksss/day-kos-call-notify-spec` `a498d34b` · PR MediSolveAIDev/mediness#965(머지 전 — 최초 Delivery = pending baseline · **머지하지 마라**).
같은 터미널이라 앞 맥락 그대로다. Delivery 절차: `start-delivery` 스킬 · `rules/delivery-workflow.md` · `tools/harness/references/requests.md`(이 워크트리).

작업 워크트리(문서): `/Users/kknaks/orca/workspaces/mediness-mediness/day-kos-call-notify-spec`
코드 워크트리(읽기만): `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-kos-call-notify`(origin/dev `55e60aa4` · 미커밋 변경 없음)

## 할 것
1. WP 나누기 — **두 판**, backend · frontend 병렬:
   - **WP-1 BE · KOS 호출 → DAY 원장 호출** (SPEC-002 규칙 40 ① ~ ⑨ · SPEC-005 「KOS 에서 건 호출」): `_apply_tasks` 판정 · 잠금 뒤 이전 값 · 묶음 · 메아리 · 늦은 관측 · 재호출 사슬 · KOS 수락 전이 · 커밋 뒤 `after_call`(두 경로) · `_recipients` called_doctor(kind one 규칙 40 만) · 시험.
   - **WP-2 웹 · 예약 / 고객 화면 열림 설정** (SPEC-006 ⑭ · 007): `DAY_WEB_RESERVATION_CUSTOMER_ENABLED`(common/config · deploy/config/dev.env 켬 · prod.env 안 씀 · local.env.example) · 메뉴 숨김 · 주소 직접 = 303 /board · HTMX = HX-Redirect · SSE · 권한보다 먼저. 서버 라우터 쪽 가드 + 템플릿/메뉴.
   - 각 WP: 범위 · 계약(SPEC 인용) · 완료 조건(WP-1 = 로컬 KOS DEMO 지점 실물 1회 — KOS 웹에서 지정 호출 · 전체 호출 · 여러 작업 동시 호출 → DAY 알림 행 · 웹 OS 알림 · iPad 시뮬레이터 앱 표시. OQ-99 · OQ-106 을 이 실물로 닫는다 / WP-2 = 설정 켬 · 끔 두 번 화면 확인) · migration 없음 · 되돌리기.
2. Delivery Issue 발행 — `mediness start-delivery --mediness-repo /Users/kknaks/orca/workspaces/mediness-mediness/day-kos-call-notify-spec --code-repo /Users/kknaks/orca/workspaces/CENTURION_DAY/day-kos-call-notify --github-repo MediSolveAIDev/CENTURION_DAY` `--plan` → `--apply`. baseline = `a498d34b`(머지 전 · spec-baseline:pending). 막히면 우회하지 말고 출력 그대로 보고. **승인 receipt 는 적용하지 마라**(사용자 몫). json 은 `/Users/kknaks/orca/workspaces/kknaks_profile/day-시술/orchestration/work/day-kos-call-notify/delivery/`
3. `30-work.md` Spec Coverage 행 · `log.md` 한 줄 → **커밋 · push 해서 PR #965 에 얹어라**(lint 0 error).

## 금지
코드 수정 · SPEC 본문 계약 변경(필요하면 멈추고 보고) · PR 머지.

## 보고
`/Users/kknaks/orca/workspaces/kknaks_profile/day-시술/orchestration/work/day-kos-call-notify/delivery-1-report.md` — Issue 번호 · WP 표 · BE ↔ FE 계약 · baseline · 막힌 것. 완료 보고 두 명령(subject 「planner 완료: Delivery 1」 · 이번 dispatch 의 taskId · dispatchId · 코디 handle term_ff2b168e-072a-4b6d-ac4a-8dd2eacda5ce):

```bash
orca orchestration send --to term_ff2b168e-072a-4b6d-ac4a-8dd2eacda5ce --from <네 워커handle> --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "planner 완료: Delivery 1" --body "<요약>"
orca terminal send --terminal term_ff2b168e-072a-4b6d-ac4a-8dd2eacda5ce --text "[worker_done] planner 완료 — Delivery 1 <한 줄>. 상세는 인박스." --enter
```

# [frontend] 예약 현황 구현 — SPEC-005 0.2.0 · WORK-007

너는 **cc-prototype `frontend` 워커**다. **앞 판의 맥락이 없다.** 먼저 역할 문서를 읽어라:

- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/roles/cc-prototype/frontend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리(코드): `/Users/kknaks/orca/workspaces/cc-prototype/overall-board` (branch `kknaksss/overall-board`) — backend · frontend 두 워커가 **같은 워크트리**를 쓴다(back / front 나눠서). 레포 `AGENTS.md` · `procedure/README.md` 를 먼저 읽어라.

## 1. SSOT

- **계약 = `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/para/projects/summer-star/cc-prototype/20-spec/spec-005-reservation-board.md`(0.2.0)** — 이 문서가 기준. 결정 원문 `10-decision/decision-006-reservation-board.md` · 작업 쪼개기 **`30-work/work-007-reservation-board.md`**(네 WP 행의 대상 파일 · 완료 조건 · 검증 명령이 곧 너의 할 일)
- KOS 실호출 근거 = `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/reservation-kos-probe-report.md`(K1~K10 · 본문 모양) + 같은 폴더 `reservation-*-report.md`
- 시안(정본) = `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/reference/2026-10-23-cc-overall-board/design/Ceramique 전체현황판.dc.html` 「예약 현황」 `M:93-715` · 분석 `orchestration/work/overall-board/design-analysis-report.md`
- 같은 앱의 지금 계약(회귀 금지): `20-spec/spec-003-procedure-board.md` 0.5.1 · `spec-004-procedure-app.md`

## 2. 할 일

**WP-FE1 → WP-FE2 → WP-FE3** 를 차례로. 각 WP 의 완료 조건을 채우고 다음으로.

backend 의 WP-BE0(가짜 응답)이 아직 없으면 SPEC-005 §7 모델로 front 타입 · 화면부터 짜고, BE0 가 생기면 붙여라(같은 코드 워크트리 — back 파일은 읽기만). 시안 실명은 화면에 옮기지 마라(SPEC 의 치환 규칙)

## 3. allowed_paths

- procedure/front/** (WORK-007 WP-FE* 대상 파일) — procedure/back/** 수정 금지(가짜 값이 모자라면 backend 에 요청 — 코디 경유 질문)

## 4. 하지 말 것

- 사용자 포트(3600 · 8600 · 3700 · 8700) · 사용자 프로세스 · 사용자 compose 를 건드리지 마라
- **KOS 쓰기 금지**(시험은 가짜 KOS · 단위 시험으로). 운영 명동점 키 금지. env 값 출력 금지
- 커밋 · push · PR 금지(코디가 한다) · SPEC 에 없는 동작 발명 금지 — 막히면 질문
- public 레포: 실명 · KOS id · 키 · 토큰 금지

## 5. 검증

```
cd procedure/front && npx tsc --noEmit && npm run lint && npm run build — WP 마다 tsc · 마지막에 build 1회. 화면 확인은 네 임시 포트(예: 3790 · 백은 가짜 모드)에서만, 끝나면 그 프로세스를 끈다
```
실행 못 한 검증은 사유와 함께 pending 으로 보고.

## 6. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 같은 워크트리의 다른 코디 세션으로 보내지 마라.

```bash
orca orchestration send \
  --to term_fa2737b7-e69a-40e1-9fac-019199b9dad3 --from <네 handle> \
  --type worker_done \
  --task-id <preamble 의 taskId> --dispatch-id <preamble 의 dispatchId> \
  --subject "frontend 완료: 예약 현황 <한 줄>" \
  --body "변경 파일 목록 / WP 별 완료 조건 / 검증 결과(수치) / SPEC 과 다르게 한 곳 / 미결"

orca terminal send --terminal term_fa2737b7-e69a-40e1-9fac-019199b9dad3 \
  --text "[worker_done] frontend 예약 현황 — <한 줄>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_fa2737b7-e69a-40e1-9fac-019199b9dad3 --text "[질문] frontend: <질문>" --enter`

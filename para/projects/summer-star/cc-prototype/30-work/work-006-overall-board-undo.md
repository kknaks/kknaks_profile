---
type: work
id: WORK-006
title: "전체현황판 — [시작] · [종료] 되돌리기(토스트 · 시술 줄 아이콘 · KOS 반영)"
status: in-progress
product: cc-prototype
feature: procedure
work_type: new-feature
owner: kknaks
progress: 15
created_at: 2026-10-26
updated_at: 2026-10-26
tags:
  - product/cc-prototype
  - feature/procedure
  - doc/work
  - status/in-progress
links:
  baselines:
    - "[[baseline-008-procedure-board|BASE-008]]"
  decisions:
    - "[[decision-005-procedure-board|DEC-005]]"
  specs:
    - "[[spec-003-procedure-board|SPEC-003]]"
    - "[[spec-004-procedure-app|SPEC-004]]"
  works:
    - "[[work-005-overall-board-procedure|WORK-005]]"
  releases: []
  related: []
sources:
  - "orchestration/work/overall-board/_RESUME.md §2 (2026-10-26 결정 줄 3개)"
  - "orchestration/work/overall-board/spec-r5-addendum.md"
  - "cc-prototype overall-board procedure/ (PR #6 상태 9a317a2 — 읽기만)"
  - "procedure/front/node_modules/@medisolve-ai/medikit 1.4.0 dist/index.d.ts"
  - "orchestration/work/overall-board/review-doc-r4.md"
  - "orchestration/work/overall-board/kos-undo-probe-report.md (WP-KOS K1 ~ K4)"
---

# 전체현황판 — [시작] · [종료] 되돌리기

시술 줄의 [시작] · [종료]를 잘못 눌렀을 때 되돌린다 — [시작] 되돌리기 → 시술 대기 · [종료] 되돌리기 → 시술 중. 들어가는 곳은 ① [시작] · [종료] 직후 토스트 [되돌리기](모달 없음) ② 시술 줄 되돌리기 아이콘(호버 툴팁 → medikit 확인 모달). 계약은 **SPEC-003 0.5.0 §5.13**(부록 I 가 `_RESUME 10-26` 결정 줄 → 절 대응표) — 이 문서는 빌드 계획만 적고 계약을 다시 쓰지 않는다.

> 1 파일 = 1 work = **빌드 계획**. 결정 원천 = `orchestration/work/overall-board/_RESUME.md` §2 2026-10-26 줄. 시안에는 되돌리기 그림이 없다 — 모양은 SPEC-003 §6.3 기본값(§6.7 #23).

## Meta

- Covers spec: SPEC-003 0.5.1(r6 — review-doc r4 · WP-KOS 반영 · 부록 J) · 0.5.0(r5 · §3.2 · §4.3 · §4.4 · §5.9 ~ §5.11 · **§5.13** · §6.3 · §6.7 #3 · #23 · §7.2 ~ §7.5 · §8 · §9 #21 ~ #26 · §10 OQ-528 ~ OQ-532 · §10.1) · SPEC-004 0.3.2(§3.4 한 줄)
- 코드 레포: `kknaksss/cc-prototype` — 범위 `procedure/back/**` · `procedure/front/**`. **`procedure/app/`(시술실 앱) · infra 는 건드리지 않는다**(웹이 정본 · 앱은 SPEC-003 §10.1 후속)
- base: WORK-005 코드(PR #6 · `9a317a2`) 위 — PR #6 머지 뒤 `origin/main` 에서 새 워크트리 · slug 는 코디가 정한다(작업 단위 = 워크트리 1개)
- 워커: backend(WP-KOS · WP-BE) · frontend(WP-FE) · reviewer · 코디(E2E)
- (r6) **게이트 통과(2026-10-26)** — WP-KOS K2 `complete:false` 받음(`DONE → READY`) · K4 flow-step 뒤로 가기 받음 → OQ-529 · OQ-530 닫힘 · 고정점 그대로 BE ∥ FE. OQ-528(K5)은 게이트와 따로 — WP-E2E 전까지
- 순서 원칙: **WP-KOS(실 KOS 확인)를 맨 앞에** — `complete:false` · flow-step 뒤로 가기는 실 KOS 에서 본 적이 없다(SPEC-003 §5.13 · OQ-529 · OQ-530). 결과가 「안 받음」이면 사용자 결정 → planner 가 SPEC 을 고친 뒤 WP-BE · WP-FE. 「받음」이면 아래 계약 고정점 그대로 BE ∥ FE
- 검증은 WP 마다 그 범위만. 전체 검증(compose · 데모 지점)은 WP-E2E 에서 한 번
- 배포: 이번 문서 범위 밖 — 사용자 E2E 통과 뒤 코디가 따로 정한다

## 계약 고정점 — BE ↔ FE 병렬의 기준

| 고정점 | 값 | SPEC-003 |
|---|---|---|
| 되돌리기 API | `POST /api/procedures/{id}/undo-start` → `{ok:true, flowStepChanged}` · `POST /api/procedures/{id}/undo-finish` → `{ok:true}` · 본문 없음 | §7.3 |
| 오류 | 409 `visit_home` · `procedure_not_doing`(undo-start) · `procedure_not_done` · `procedure_not_started`(undo-finish) · 404 `not_found`(「방 배정」 · 없는 id · 카드 아님) · 403 `fake_board` · 401 — 모양 `{error:{code,message}}` | §7.3 · §5.13 |
| 역할 | admin · doctor · nurse 모두 | SPEC-004 §3.4 |
| 스냅샷 | `procedures[]` 에 **`canUndoStart` · `canUndoFinish: bool`** 두 필드만 더함(그 밖 모양 그대로) | §7.2 · §5.13 |
| 이벤트 | `event_log.type` `proc_undo_start` `{procedureId, startedAt, startedEventId, flowStepChanged}` · `proc_undo_finish` `{procedureId, completedAt}` | §3.2 |
| KOS op | undo-finish = `change-tasks-complete {complete:false}` · 확인 `statusNot:"DONE"` / undo-start = 고객이 시술 대기로 돌아갈 때만 `change-flow-step {step:"PROCEDURE_WAITING"}` · 그 밖 op 0 | §8 |
| SSE | 되돌리기 직후 `board` 1개 | §7.5 ① |
| 화면 | 토스트 [되돌리기] 5초 · 모달 없음 / 아이콘 = 진행 줄 [종료] 왼쪽 · 완료 줄 「완료」 왼쪽 · medikit `ResetIcon` · `Tooltip` 「되돌리기」 · `ConfirmModal`(`caution` · 「취소」 · 「되돌리기」) | §5.13 · §6.3 |

front 는 back 을 기다리지 않고 가짜 보드(`PROC_FAKE_BOARD`)로 그린다 — **가짜 보드의 예시 스냅샷에 `canUndoStart` · `canUndoFinish` 가 true 인 줄이 있어야 한다** — ~~WP-BE 가 `service/fake_board.py` 에 싣는다~~ (r6 바뀜 — review-doc r4 W2) → **WP-FE 가 `procedure/back/app/service/fake_board.py` 의 예시 줄에 두 값을 싣는다**(back 파일은 이 하나만 · 지어낸 값). 그래야 FE 가 BE 를 기다리지 않고 스크린샷을 찍는다. `schemas/board.py` 의 두 필드는 WP-BE 몫 — FE 가 먼저 가면 가짜 보드 dict 에 두 키를 더하고, 스키마 필드가 아직 없으면 응답 모델이 버리므로 **WP-BE 의 `schemas/board.py` 두 필드 커밋을 먼저**(아래 병렬 절). 가짜 보드에서 되돌리기 API 는 403 `fake_board` → 일반 오류 토스트(예외 없음 · WORK-005 와 같다). 그래서 FE 는 가짜 보드에서 **아이콘 · 툴팁 · 모달 · [시작] · [종료] 실패 토스트 모양**까지 확인하고, 성공 토스트 [되돌리기] · 실제 되돌림은 WP-E2E(데모 지점)에서 본다.

## Work Packages

| WP | 내용 | 계약 | 워커 | 대상 파일(범위) | 완료 조건 | 검증 명령(부분) | 상태 |
|---|---|---|---|---|---|---|---|
| **WP-KOS** | **데모 지점 실호출 확인 — 구현 전, 맨 앞**. backend 가 데모 지점(데모 테넌트 · 4층 · 오늘 일정 하나 — 작업 PROCEDURE ≥ 1 · 방 없는 ETCETERA(시트팩 등) ≥ 1 · 방 있음)에 **아래를 1회씩** 보내고, 보낼 때마다 1 ~ 2초 뒤 `get-schedules-grouped-by-zone` 로 다시 읽어 전후 값을 적는다. K1 `change-tasks-complete {complete:true}`(PROCEDURE · 기준선 — `DONE` 확인) → **K2 같은 작업 `{complete:false}`**(HTTP · 본문 모양 · 작업 `status` · `completedDateTimeUtc` · `doctors` · `assignees` 가 어떻게 되나 · KOS 웹 화면 작업 칸 표시) → K3 `change-flow-step` `PROCEDURE_WAITING` → `PROCEDURE`(기준선) → **K4 `PROCEDURE` → `PROCEDURE_WAITING`(뒤로 가기)**(HTTP · 거절 코드 · `flowStep`) → **K5 (OQ-528) ETCETERA 작업에** `change-tasks-room` → `change-tasks-assignees` → `call-tasks-doctors`(→ `WAITING`?) → `change-tasks-doctors`(→ `READY`?) → `change-tasks-complete {complete:true}`(→ `DONE`?) → `{complete:false}` → K6 정리(일정을 시작 상태로 돌리거나 데모 도구로 다시 채움 · 결과 적기). 호출은 **일회성 스크립트**(back `KosClient` 를 import 해도 됨) — 코드 레포에 남기지 않고, 떠 있는 사용자 스택(3700 · 8700)은 건드리지 않는다. env 값은 사용자 `procedure/.env` 원천 그대로 · 출력에 찍지 않는다 | §5.13 「KOS 실호출 확인」 · §8 · OQ-528 · OQ-529 · OQ-530 | backend | 코드 변경 없음 · 리포트 `orchestration/work/<slug>/kos-undo-probe-report.md`(코디가 정한 slug 폴더) | 리포트에 K1 ~ K6 표(요청 경로 · 본문 모양 · HTTP 상태 · 거절 코드 · 전후 KOS 값 · KOS 화면 관찰) · **OQ-528 · OQ-529 · OQ-530 판정 각각 「받음 / 안 받음」 한 줄**(r6 결과: OQ-529 받음 · OQ-530 받음 · OQ-528 K5 대기) · K2 뒤 작업 상태 실제 값(SPEC §5.13 즉시 값 `READY` 와 같은지). **public — KOS id · 키 · 토큰 · 실명 · 고객 이름 0**(id 는 「일정 A · 작업 1」 식으로) | ~~리포트 grep: 이메일 · `Bearer` · UUID 모양 문자열 0~~ (r6 — W5) `grep -nE '[0-9a-f]{8}-[0-9a-f]{4}-\|@[A-Za-z0-9.-]+\.[a-z]{2,}\|Bearer \|eyJ\|\b[0-9]{5,}\b' orchestration/work/overall-board/kos-undo-probe-report.md \| wc -l` = **0**(표 안이라 `\|` — 실행 때는 역슬래시 없이) | **K1 ~ K4 완료 · K5 대기**(2026-10-26 · 방 없는 ETCETERA 붙은 일정 대기 — 사용자가 데모 KOS 에 시트팩을 붙이면 진행) (r6) |
| (게이트) | 코디가 WP-KOS 판정을 읽는다 — ~~셋 다 「받음」~~ (r6 바뀜 — review-doc r4 W3) → **OQ-529 · OQ-530 둘만** 본다 — 둘 다 「받음」 → WP-BE ∥ WP-FE 시작. 하나라도 「안 받음」 → SPEC-003 OQ-529 · OQ-530(옵션 + 권장)으로 사용자 결정 → planner 가 SPEC-003 · 이 문서를 고친 뒤 시작. **OQ-528(K5)은 게이트에 넣지 않는다** — 되돌리기 계약(§5.13)과 무관하고 「안 받음」이어도 바뀌는 곳은 §5.1(WORK-005 · PR #6)이다 → WP-E2E 전까지 따로 확인 · 「안 받음」이면 WORK-005 쪽 사용자 결정. K2 의 실제 작업 상태가 `READY` 가 아니면 §5.13 즉시 값을 그 값으로 고친다(planner) | §10 | 코디 | — | 판정 기록 · (필요하면) SPEC 개정 | — | **통과(2026-10-26)** — OQ-529 · OQ-530 받음 · K2 = `READY`(§5.13 즉시 값과 같음 → SPEC 0.5.1 확정) (r6) |
| **WP-BE** | **되돌리기 back** — ① `domain/kos_ops.py` `uncomplete_op`(경로 = `PATH_COMPLETE` · `complete:false` · expect `{tasks:[seq], statusNot:"DONE"}`) ② `domain/rules.py` 되돌리기 판정 한 곳(`undo_start_block` · `undo_finish_block` → 409 코드 또는 None — §5.13 표 · 귀가 대기 → `visit_home` 먼저) · 「고객을 시술 대기로 돌리나」 판정(되돌린 뒤 `procedures(v)` 중 `doing` · `done` 0 · 고객 `doing`) ③ `service/actions.py` `undo_start` · `undo_finish`(트랜잭션 하나 · `_procedure` 404 그대로 · `event_log` 1줄 · undo-start = `started_at` · `started_event_id` 비움 · 필요하면 `update_visit(flow_step=PROCEDURE_WAITING, flow_step_at=now)` + flow-step op(ccc 고객이 `doing` → `waiting` 이 될 때 **항상** — 보내기 전에 KOS 값을 따로 읽지 않는다 · SPEC §8 (r6)) / undo-finish = `completed_at` 비움 · `kos_status="READY"`(WP-KOS K2 로 확정 (r6)) + `uncomplete_op` · `MESSAGES` 두 코드) ④ `api/actions.py` 경로 둘(`require_real_board` 그대로) · `schemas/actions.py` 응답 ⑤ `schemas/board.py` `Procedure.canUndoStart` · `canUndoFinish` · `service/board_service.py` `_proc` ⑥ `kos/ops.py` `expect_met` 에 `statusNot` · `superseded` 가 `status` 와 `statusNot` 을 같은 필드로 봄(SPEC §8 대체 규칙) ~~⑦ `service/fake_board.py` 진행 · 완료 예시 줄에 두 값 true(지어낸 값)~~ (r6 — WP-FE 로 옮김 · W2). **⑤ 의 `schemas/board.py` 두 필드는 먼저 커밋한다**(FE 의 가짜 보드가 이 필드를 지나야 보인다) | §3.2 · §4.3 · §5.10 · §5.13 · §7.2 · §7.3 · §7.4 · §7.5 · §8 · SPEC-004 §3.4 | backend | `procedure/back/app/domain/{kos_ops,rules}.py` · `service/{actions,board_service}.py` · `api/actions.py` · `schemas/{actions,board}.py` · `kos/ops.py` · `tests/test_undo.py`(새) · `tests/test_kos_ops.py` · `tests/test_auth_roles.py` · `tests/test_order.py`(경로 수 17 → 19 · 244행) · `tests/test_contract.py` | SPEC-003 §9 끝 「0.5.0 더함」 시험 **전부** pytest — undo-start(`doing` 만 · 호출 · 수락 · 집도의 남음 · [시작] 다시 켜짐 · 진행 · 완료 0 이면 고객 `waiting` + flow-step op **항상 1줄** · 남으면 op 0 · ~~KOS 가 이미 그 단계면 op `confirmed`~~ (r6) → 그 op 이 400 을 받은 뒤 다음 조회에서 KOS 가 `PROCEDURE_WAITING` 이면 `confirmed`(재전송 없음) · 첫 [시작] 직후 되돌리면 앞 `PROCEDURE` op 은 `superseded`) · undo-finish(`done` + ccc [시작] 있음만 · `completed_at` 비움 · op 1줄 · 고객 그대로 · `canHome` 풀림) · 409 네 코드 · 404 「방 배정」 · 403 `fake_board` · 세 역할 · `event_log` 1줄 · SSE 1개 · 스냅샷 두 필드(귀가 대기 · 「방 배정」 false) · `statusNot` 확인 · **[종료] → 되돌리기 → [종료] 에서 앞 op 재전송 0**(`superseded`) · 경로 19. 기존 시험 전부 통과(지금 162) | `cd procedure/back && uv run ruff check . && uv run pytest -q tests/test_undo.py tests/test_kos_ops.py tests/test_auth_roles.py tests/test_order.py tests/test_contract.py` | 대기(게이트 뒤) |
| **WP-FE** | **되돌리기 front** — ① `lib/api.ts` `undoStart` · `undoFinish` · `lib/types.ts` `Procedure.canUndoStart` · `canUndoFinish` · (r6 — W2) `procedure/back/app/service/fake_board.py` 진행 · 완료 예시 줄에 `canUndoStart` · `canUndoFinish` true(지어낸 값 · back 파일은 이것 하나) ② `live/page.tsx` 토스트: [시작] · [종료] 성공 토스트 문구(§6.3) + [되돌리기] 버튼 · **5초**(되돌리기 토스트만 · 다른 토스트 2.6초 그대로) · 새 토스트가 앞 토스트를 바꿈 · [되돌리기] = 토스트 닫고 바로 API(모달 없음) → 「… 시술 대기로 되돌림」 / 「… 시술 중으로 되돌림」 · 실패 = back `message` 토스트 · 주석 「되돌리기 없음(D-28)」 고침 ③ `OrderCard.tsx` 진행 줄 [종료] 왼쪽 · 완료 줄 「완료」 왼쪽에 아이콘 버튼(26 × 26 · medikit `ResetIcon` sm · `gray-500` → 호버 primary · `aria-label`) — `canUndoStart` · `canUndoFinish` 값으로만 · medikit `Tooltip` 「되돌리기」(`TooltipProvider` 페이지에 하나) ④ 확인 모달 = medikit `ConfirmModal`(`isOpen` · `title` 「시술 대기로 되돌리겠습니까?」 / 「시술 중으로 되돌리겠습니까?」 · `description` 「<방> · <시술 이름>」 · `variant="caution"` · `leftButton` 「취소」 · `rightButton` 「되돌리기」 · 바깥 누르면 닫힘) — 새 컴포넌트 하나(예: `components/procedures/UndoConfirm.tsx`) · 열린 동안 SSE 로 그 시술 아이콘 조건이 꺼져도 모달은 그대로(누르면 back 이 409 로 답한다) | §5.9 · §5.11 · §5.13 · §6.3 · §6.7 #3 · #23 · §7.2 · §7.3 | frontend | `procedure/front/lib/{api,types}.ts` · `app/(main)/procedures/live/page.tsx` · `components/procedures/OrderCard.tsx` · `components/procedures/UndoConfirm.tsx`(새 · 이름은 frontend 가) · `procedure/back/app/service/fake_board.py`(예시 값만 · r6) | frontend 가 가짜 보드 스크린샷을 보고서에 붙인다 — 진행 줄 아이콘 · 완료 줄 아이콘 · 대기 줄 아이콘 없음 · 툴팁 「되돌리기」 · 모달 두 문구 · 모달 [되돌리기] 뒤 403 오류 토스트. `ResetIcon` 이 되돌리기 화살표 모양인지 · 토스트 버튼 색 토큰을 보고서에 적는다(SPEC §6.3 기본값). reviewer 가 SPEC §5.13 · §6.3 과 대조 · 아이콘 조건을 front 가 다시 계산하지 않음(`canUndo*` 만) · `cc/` import 0 | `cd procedure/front && npx tsc --noEmit && npm run lint && npm run build` · `grep -rn "canUndoStart\|canUndoFinish" procedure/front/components procedure/front/app` ≥ 2 | 대기(게이트 뒤) |
| **WP-E2E** | **리뷰 + 코디 E2E(데모 지점)** — reviewer: SPEC-003 0.5.0 부록 I 의 절 전부 ↔ 코드 · 기본값(§I.3)이 코드에 그대로인지 · KOS op 순서 · 대체 규칙. FAIL 은 모아서 한 번에 수정 발주. 코디: 백엔드 커밋 뒤 **compose 다시 올리고** 데모 지점 연결 → SPEC-003 §9 **#21 ~ #26**(브라우저 2개 · #24 는 두 화면 필수) + 회귀 #6 · #8 · #9 · #14 → 사용자 E2E(사용자 표면 · 피드백은 모아서 한 batch) | §9 | reviewer · 코디 · backend · frontend(수정) | `procedure/back/**` · `procedure/front/**` | 리뷰 PASS · 코디 §9 #21 ~ #26 통과(KOS 쪽 확인 칸 포함 — #22 30초 뒤 `DONE` 으로 안 돌아감 · #26 재전송 없음) · 사용자 E2E 통과 | `cd procedure/back && uv run ruff check . && uv run pytest -q` · `cd procedure/front && npx tsc --noEmit && npm run lint && npm run build` · `cd procedure && docker compose up --build` | 대기 |

## 병렬

```text
WP-KOS(데모 지점 실호출 · 리포트) ── (게이트: 코디 판정 · 필요하면 사용자 결정 → SPEC 개정)
                                        ├─ WP-BE ─┐
                                        └─ WP-FE ─┴─ WP-E2E
```

- **WP-KOS 가 끝나기 전에 WP-BE · WP-FE 를 발주하지 않는다** — KOS 가 안 받으면 [종료] 되돌리기 자체가 빠질 수 있다(OQ-529 권장 (a)). (r6) 게이트 통과 — OQ-529 · OQ-530 받음(2026-10-26). K5(OQ-528)는 게이트 밖
- (r6 — W2) 숨은 의존 하나: FE 의 가짜 보드 스크린샷은 `schemas/board.py` 의 `canUndoStart` · `canUndoFinish` 필드가 있어야 보인다 → **WP-BE 가 그 두 필드를 첫 커밋으로** 낸다. 가짜 보드 예시 값(`fake_board.py`)은 WP-FE 가 넣는다. 두 워커가 같은 back 파일을 만지지 않는다
- WP-BE ↔ WP-FE 병렬 가능 — 위 고정점(경로 · 두 필드 · 오류 코드)이 박혀 있다. 모양을 바꿔야 하면 SPEC-003 §7 을 먼저 고친다(코디 → planner)

## 하지 않는 것

- 시술실 앱(`procedure/app/`) — 되돌리기 UI · `canUndo*` 사용 · 공유 순서 · `isRoomTask` 맞추기는 **SPEC-003 §10.1 앱 후속**(웹 기준). 스냅샷에 두 필드가 늘었지만 앱은 모르는 필드를 무시한다(SPEC-004 §7.2) → 앱 빌드 필요 없다
- 호출 · 수락 · [다른 원장에게] · [귀가 대기] · 마취 되돌리기 — 결정 범위 밖(SPEC-003 §1.2 · §5.5)
- 귀가 대기 카드 되돌리기(OQ-531) · 토스트 되돌리기 이벤트 id 검사(OQ-532) · KOS 반영 실패 복구(OQ-509)
- 시안 파일 수정 — 되돌리기 그림은 시안에 없다(SPEC-003 §6.7 #23 · 모양은 §6.3 기본값)

## 주의

- public 레포(코드 · 문서 모두) — KOS 키 · 토큰 · 비밀번호 · 계정 이메일 · 실명 · KOS id 값을 코드 · 시험 데이터 · 리포트 · 커밋에 넣지 않는다. WP-KOS 리포트도 같다
- 실 데모 지점에서만 쓴다 — 운영 명동점 키 금지(D-06). WP-KOS 는 데모 일정 하나만 건드리고 끝나면 정리한다
- 워커는 사용자 포트(3600 · 8600 · 3700 · 8700)에 떠 있는 사용자 프로세스를 죽이지 않는다
- 백엔드 커밋 뒤 compose 를 다시 올리고 E2E(옛 코드가 떠 있는 채로 확인 금지)
- 외부 서비스 경로(KOS)는 **실물 호출이 완료 조건** — 가짜 KOS 시험만으로 done 하지 않는다(WP-KOS · WP-E2E #22 · #26)

## 열린 것 (2026-10-26)

| 무엇 | 지금(기본값) | 근거 |
|---|---|---|
| ~~KOS 가 `complete:false` 를 받나~~ | **닫힘 — 받음**(K2 · `DONE → READY`) (r6) | SPEC-003 ~~OQ-529~~ |
| ~~KOS 가 flow-step 뒤로 가기를 받나~~ | **닫힘 — 받음**(K4) (r6) | SPEC-003 ~~OQ-530~~ |
| ETCETERA 에 호출 · 완료가 되나 | WP-KOS K5 로 확인 — 게이트 밖 · WP-E2E 전까지 · 사용자가 시트팩을 붙이면 진행 (r6) | SPEC-003 OQ-528 |
| 귀가 대기 카드 되돌리기 | 막음 | SPEC-003 OQ-531 |
| 토스트 되돌리기 「내 조작만」 | 상태 검사만 | SPEC-003 OQ-532 |

## r4 처분 (r6 · 2026-10-26)

review-doc r4 FAIL 1 · WARN 6 + WP-KOS K1 ~ K4 반영 — 정본 SPEC-003 0.5.1 부록 J. 이 문서에서 바뀐 곳: frontmatter(진행 중 · 15 · sources) · Meta(0.5.1 · 게이트 통과) · 고정점 아래 문단(가짜 보드 예시 = WP-FE — W2) · WP-KOS(검증 명령 grep — W5 · 상태 K1 ~ K4 완료 · K5 대기) · 게이트(OQ-529 · OQ-530 만 — W3 · 통과) · WP-BE(flow-step op 항상 · 시험 줄 — W1 · `READY` 확정 · ⑦ 뺌 · `schemas/board.py` 먼저 커밋) · WP-FE(`fake_board.py` 예시 값) · 병렬(숨은 의존) · 열린 것(OQ-529 · OQ-530 닫힘).

# 리뷰 리포트 — overall-board / code r2 (2026-10-26)

## 판정: FAIL — FAIL 1(FE 몫) · WARN 3 · BE 몫 FAIL 0

- 대상: 코드 워크트리 `cc-prototype/overall-board`
  - 커밋 `9a317a2` 이후 미커밋 변경 전부: back 15 파일(M) + `tests/test_undo.py`(새) · front 4 파일(M) + `components/procedures/UndoConfirm.tsx`(새)
  - `9a317a2` 안의 r1 이후 변경(r1 이 못 본 곳): 카드 방 type 무관 · 규칙 하나 · `isRoomTask`. `back/app/domain/rules.py` · `back/app/kos/sync.py` · `back/app/service/actions.py` · `front/components/procedures/view.ts` 등을 SPEC §5.1 · §5.7 과 직접 대조했다
- SSOT: SPEC-003 **0.5.1**(§5.1 · §5.7 · §5.9 ~ §5.11 · §5.13 · §6.3 · §7.2 · §7.3 · §8 · §9 #21 ~ #26 · 「0.5.0 더함」 · 「0.4.3 더함」) · WORK-006(계약 고정점 · WP-BE · WP-FE) · `_RESUME.md` §2 10-25(35 ~ 41행) · 10-26(42 ~ 45행)
- FE 수정 발주 1건(F1, 한 줄짜리 수정). BE 수정은 필요 없다

### 검증 방식

`tools.md` 에 「수정 · 테스트 실행 금지」라고 되어 있어 시험은 돌리지 않았다. 수치는 워커 보고서에서 가져왔다.

| 명령 | 결과(출처) |
|---|---|
| `uv run ruff check . && uv run pytest -q`(back 전체) | ruff 통과 · **178 passed**(162 + 16) — `backend-r1-report.md` 「되돌리기」 절 |
| WP-BE 부분 명령(5 파일) | 69 passed — 같은 곳 |
| `npx tsc --noEmit && npm run lint && npm run build` | 통과 — `frontend-r1-report.md` 「되돌리기」 절 |
| `procedure/app/` 변경 | **0**(`git diff --stat HEAD -- procedure/app` 결과 없음) — WORK-006 「하지 않는 것」 |
| `procedure/` 밖 변경 · 밖 import | 0 |
| public — 새 파일 · 시험 데이터 | `sch-1` · `room-1` · `doc-a` · 「방 배정」 · 「시트팩」 같은 지어낸 값뿐. KOS id · 키 · 실명 0 |

---

## FAIL

### F1 (FE 몫) — 확인 모달의 [되돌리기] 버튼이 모달 상자 밖으로 삐져나온다(`fe-shots/undo-modal-finish.png` · `undo-modal-start.png` 둘 다)

- **원인 = 우리 레포의 medikit 전역 보정 한 줄과 `ConfirmModal` 버튼 줄의 조합.** `data-fill-buttons` 는 원인이 아니다. 모달은 페이지 맨 바깥 div 에 그려지고(`live/page.tsx:361`), 그 위에 `data-fill-buttons` 조상이 없다. medikit `Modal` 은 portal 을 쓰지 않는다
  1. `procedure/front/app/styles/medikit-patches.css:13` — `[Button-1]` 보정 `button.inline-flex.items-center.justify-center { white-space: nowrap; flex-shrink: 0; }`. medikit `Button` **전부**에 `flex-shrink: 0` 이 걸린다(선택자 명시도 0,3,1)
  2. `node_modules/@medisolve-ai/medikit/dist/index.js:1799` — `ConfirmModal` 본문은 `min-w-[444px]` 이다(모달 패딩 26 안쪽 폭 = 444). `:1808` 버튼 줄은 `flex gap-[16px]` 이고, `:1817` · `:1833` 에서 좌 · 우 버튼이 둘 다 `w-full` 이다(medikit 1.4.0)
  3. 그래서 각 버튼이 100% = 444px 를 차지하고, 1번 보정 때문에 줄어들지 못한다 → 444 + 16 + 444 = 904px 가 된다. 스크린샷에서도 [취소]는 x 578 ~ 1022(= 444), [되돌리기]는 x 1038 ~ 1482 로 모달 오른쪽 끝(1048) 밖에 있다. 숫자가 그대로 맞는다
- 쓰는 쪽: `procedure/front/components/procedures/UndoConfirm.tsx:30-31` 이 `leftButton` · `rightButton` 에 `label` · `onClick` 만 넘긴다. 이 레포에서 `ConfirmModal` 을 쓰는 곳은 여기 하나뿐이라(grep), 전역 보정과 부딪힌 일이 이번에 처음 드러났다
- 근거: SPEC-003 §6.3 「누르면 확인 모달 = medikit `ConfirmModal` … 좌 · 우 버튼」 · §9 #22(모달에서 [취소] · [되돌리기]). 버튼이 상자 밖으로 나가 깨진 모달은 계약한 모양이 아니고, 사용자가 실물에서 바로 보게 된다
- 놓친 곳: `frontend-r1-report.md:163` 은 두 모달 스크린샷을 「같음」으로 적었다(조용히 통과한 자리)
- 고치는 방향(FE 판단 — 둘 중 하나):
  - (권장 · 국소) `UndoConfirm.tsx` 의 두 버튼 props 에 `style: { flexShrink: 1, minWidth: 0 }` 를 더한다. `ConfirmModal` 이 `...leftButtonProps` · `...rightButtonProps` 를 `Button` 에 넘기고(`index.js:1777~` 구조분해 → spread), `Button` 은 `...props` 를 요소에 그대로 붙인다. 인라인 style 이므로 1번 보정을 이긴다. `className: 'shrink'` 은 명시도에서 져서 효과가 없다
  - (전역) `medikit-patches.css:13` 아래에 `[role="dialog"] .flex.gap-\[16px\] > button { flex-shrink: 1; min-width: 0; }` 처럼 범위를 좁힌 예외를 둔다. 다른 화면 버튼에 영향이 없는지 함께 봐야 한다
  - 고친 뒤 `undo-modal-start.png` · `undo-modal-finish.png` 를 다시 찍는다. 두 버튼이 각 214px(= (444 − 16) / 2)씩 모달 안에 나란히 있으면 통과다
- 참고: 오른쪽 버튼이 연한 파랑 채움인 것은 결함이 아니다. medikit 은 `variant` 가 `warning` 일 때만 red 이고, 그 밖은 `filled` + `blue` = `bg-primary-100`(`index.js:1776`)이다. FE 보고서 187행과 같은 내용이다

---

## WARN

### W1 — 「방 배정」 판정이 「ccc 가 호출한 적 있나」에 기대고 있다. 그래서 ccc 밖에서 생긴 방 붙은 ETCETERA 는 조용히 숨고, [귀가 대기] 때 KOS 에서 취소된다
- 위치: `back/app/domain/rules.py:68`(`p.kind == "etc" and bool(p.room_kos_id) and p.id not in self._called`) · `back/app/service/actions.py:294`(취소 = `is_room_task` 이고 끝나지 않은 작업)
- 근거: SPEC §5.1 「예외는 「방 배정」 하나 = 방 붙은 ETCETERA 이면서 ccc 가 한 번도 호출하지 않은 작업」 · `_RESUME` 10-25(41행). 코드는 계약과 같다 → FAIL 이 아니다
- 어긋날 수 있는 경우: ① KOS 화면에서 직원이 시트팩 같은 ETCETERA 에 방을 붙이거나 거기서 호출한 경우 ② ccc DB(볼륨)를 새로 만들어 `doctor_call` 이력이 사라진 경우. 이때 그 작업은 화면에서 사라지고, 「전부 완료」에서도 빠지며, [귀가 대기]를 누르면 `CANCELED` 가 된다. r1 「조용히 통과」 4번과 같은 뿌리인데, 이제는 **취소까지 한다**는 점이 다르다
- 판정: WARN. E2E #0 준비 때 「방 없는 ETCETERA」를 KOS 화면에서 붙이는 방식에 따라 이 경우가 바로 생길 수 있다 → 아래 E1

### W2 — ETCETERA(시트팩 등)의 호출 · 완료 · **완료 풀기**는 실 KOS 에서 한 번도 확인하지 않았다(OQ-528 · WP-KOS K5 대기)
- 위치: 규칙 하나 때문에 ETCETERA 도 [시작] · [종료] · 되돌리기 대상이다(`actions.py:208-211` `_procedure` 는 「방 배정」만 404). `uncomplete_op` 은 type 을 가리지 않는다(`back/app/domain/kos_ops.py` `uncomplete_op`)
- 근거: WORK-006 「열린 것」 OQ-528 · `_RESUME` 10-26(45행). K2(`complete:false` → `READY`)는 PROCEDURE 작업에서만 봤다. `tests/fake_kos.py` 의 `complete:false → READY` 도 그 값을 따라 만든 것이다
- 판정: WARN. 시트팩 [종료] → 되돌리기에서 KOS 가 거절하거나 다른 상태로 보내면 op 이 재전송되다가 3회 뒤 `failed` 가 된다. 웹에는 아무것도 보이지 않는다(OQ-522). E2E 전에 K5 를 확인해야 한다

### W3 — 되돌리기 성공 경로(토스트 [되돌리기] → 실제 되돌림 · SSE 반영)는 FE 화면에서 실 back 으로 한 번도 돌려 보지 않았다
- 위치: `front/app/(main)/procedures/live/page.tsx:113-124`(`undo` · `undoFromToast` · `undoFromModal`) · `:140-141`(성공 토스트 + `undoOf`)
- 근거: 가짜 보드에서는 조작이 늘 403 이다(WORK-006 고정점 아래 문단). FE 는 성공 토스트를 Playwright 가로챔(`undo-toast-mocked-success.png`)으로만 봤다. 코드를 읽어 보면 §5.13 · §6.3 과 같다(아래 PASS 표)
- 판정: WARN. 계약 위반은 아니고 E2E #21 ~ #24 에서 볼 일이다

---

## PASS — 항목별 대조

### 1. 규칙 하나 · 「방 배정」 (SPEC §5.1 · §5.7 · §7.2 · `_RESUME` 10-25)

| 확인 | 코드 | 판정 |
|---|---|---|
| 스냅샷 `procedures[]` = 작업 전부(CANCELED 만 뺌 · 「방 배정」 포함 · type 무관) | `rules.py:87-93` `items` · sync 는 PROCEDURE · ETCETERA 둘 다 저장(`sync.py:125`) | PASS |
| 판정은 type 무관 · 「방 배정」만 뺌 — `procedures` · `all_done` · `payment_required` · `pickable` · `start_block` · `canFinish` · `busy_room` | `rules.py:95-112` · `:138-150` · `:51-57` · `board_service.py:104`. `kind ==` 로 가르는 규칙 코드 0(grep) | PASS |
| 「방 배정」 = 방 붙은 ETCETERA + 호출 이력 없음 | `rules.py:60-68` · 시험 `test_rules.py:225` `test_called_sheet_pack_with_room_is_not_room_task` | PASS (실물 위험 → W1) |
| 「방 배정」 [시작] · [종료] · 되돌리기 = 404 | `actions.py:208-211` `_procedure` · `test_undo.py:145` | PASS |
| `isRoomTask` 필드 · front 숨김 — 카드 줄 · 선택 · N건 · 호출 팝오버 · 고객 탭 번호 원 · 현황 탭 | `schemas/board.py:98` · `view.ts:81` `procsOf` 를 `OrderCard.tsx:56,187` · `CallPopover.tsx:76` · `Aside.tsx:197-198,492` · `live/page.tsx:145` 가 씀. `c.procedures` 를 바로 읽는 곳 0. 호출 탭 `Aside.tsx:334` `k.procedures` 는 호출 항목이라 「방 배정」이 들어갈 수 없다(호출되면 「방 배정」이 아님) | PASS |
| 기타 작업 읽기 전용 줄 · `etcStatus` · `kind === 'etc'` 분기 제거 | front grep 0 | PASS |
| [귀가 대기] = 「방 배정」 뺀 작업이 전부 완료일 때만 · 아니면 409 `procedures_not_done` | `actions.py:290-291` · `test_e2e3_home.py:84` | PASS |
| [귀가 대기] 취소 = 안 끝난 「방 배정」만 · 없으면 ① 생략 · 그다음 `PROCEDURE_DONE` | `actions.py:294-298` · `test_e2e3_home.py:53,73,84` | PASS |
| 카드 방 = type 무관 · 가장 늦은 `roomAssignedDateTimeUtc` · 같으면 ETCETERA → 큰 sequence · 방 없으면 카드 없음 | `sync.py:38-49` · `test_kos_sync.py:145-216` | PASS (SPEC 「0.4.3 더함」과 같음) |
| 가짜 보드: 시트팩(etc) = 일반 줄 · 「방 배정」 = `isRoomTask: true` | `fake_board.py:82,84` | PASS |
| 앱 무변경 | `procedure/app/` diff 0 | PASS (§10.1 후속) |

### 2. 되돌리기 — back (SPEC §5.13 · §7.3 · §8 · WORK-006 고정점)

| §5.13 · §7.3 · §8 | 코드 | 판정 |
|---|---|---|
| 경로 둘 · 본문 없음 · `undo-start` → `{ok, flowStepChanged}` · `undo-finish` → `{ok}` | `api/actions.py:69-79` | PASS |
| 검사 순서 401 → 403 `fake_board` → 404 → 409(`visit_home` 먼저) | `require_real_board` 그대로 · `_procedure` → `undo_*_block`(`rules.py:153-167` — `is_home` 이 맨 위) · `test_undo.py:118,159` | PASS |
| 409 네 코드: `visit_home` · `procedure_not_doing` · `procedure_not_done` · `procedure_not_started` · 메시지 | `rules.py:153-167` · `actions.py:38-39` · `schemas/actions.py` `CONFLICT_CODES` · `test_conflicts` · `test_messages` | PASS |
| `canUndoStart` = `doing` · 「방 배정」 아님 · 귀가 대기 아님 / `canUndoFinish` = `done` · ccc `started_at` 있음 · 「방 배정」 아님 · 귀가 대기 아님 — 판정 한 곳(block 과 같은 함수) | `board_service.py:105` · `test_snapshot_flags` · `test_conflicts` | PASS |
| **[시작] 되돌리기 = `started_at` · `started_event_id` 비움**, 호출 · 수락 · 집도의는 그대로 · [시작] 다시 켜짐 | `actions.py:261` · `test_undo.py:45` (`p.startedAt is None`) · `:68` | PASS (사용자 확인 10-26) |
| **[종료] 되돌리기 = `started_at` 유지**(「<원장> · HH:MM 시작」이 원래 시각) · `completed_at` 비움 · `kos_status = READY` | `actions.py:278`(`started_at` 은 손대지 않음) · `test_undo.py:92` (`startedAt == "…11:00…"`) · front `view.ts:104` 가 `startedAt` 으로 그림 | PASS (사용자 확인 10-26) |
| 고객 → 시술 대기 = 「방 배정」 뺀 시술 중 진행 · 완료 0 이고 고객 `doing` · 그때 flow-step op **항상 1줄**(KOS 값을 읽지 않음) · 아니면 op 0 | `rules.py:169-172` · `actions.py:257-264` · `test_undo.py:45,78` | PASS |
| undo-finish op = `change-tasks-complete {complete:false}` · expect `{tasks, statusNot:"DONE"}` · 고객 상태 그대로 · `canHome` 풀림 | `kos_ops.py` `uncomplete_op` · `test_undo.py:92` | PASS |
| `statusNot` 확인 · `status` 와 `statusNot` 을 같은 필드로 보는 대체 규칙 · [종료] → 되돌리기 → [종료] 재전송 0 | `kos/ops.py:46,70,82-85` · `test_kos_ops.py` 두 시험 · `test_undo.py:234` (보낸 값 = [true, false, true]) | PASS |
| 첫 [시작] 직후 되돌리기 → 앞 `PROCEDURE` op `superseded` · 같은 단계 400 → 다음 조회에서 `confirmed` | `test_undo.py:254,268` | PASS |
| 반영 대기 중 sync 가 덮지 않음 — undo-finish op 의 `sequences` · undo-start 의 flow-step | `sync.py:110,121-132` (`touched_sequences` · `touches_flow_step`) | PASS |
| `event_log` 1줄(payload 모양 그대로) · SSE 1개 · 거절이면 0 | `actions.py:258-260,277` · `test_one_event_one_publish` | PASS |
| 세 역할 · 경로 수 19 | `test_auth_roles.py` 행렬 3 × 10 · `test_order.py:237` (HTTP 18 + WS 1 = 19. SPEC 「router 18 + health」는 WS 를 router 쪽에 센 것이고 합계가 같다) | PASS |

### 3. 되돌리기 — front (SPEC §5.11 · §5.13 · §6.3)

| 확인 | 코드 | 판정 |
|---|---|---|
| 아이콘 위치: 진행 줄 [종료] **왼쪽** · 완료 줄 「완료」 **왼쪽** · 대기 줄 없음 | `OrderCard.tsx:252-253`이 [시작](`:245`) 뒤, [종료](`:254`) · 「완료」(`:259`) 앞에 있다. 대기 줄에는 그리는 분기가 없다 | PASS |
| 조건은 스냅샷 `canUndo*` 만 쓴다(front 가 다시 계산하지 않음) | `:252-253` 의 `p.state` 는 어느 자리에 그릴지만 정한다. 켜짐 판단은 `canUndo*` | PASS |
| 26 × 26 · 테두리 없음 · `ResetIcon sm` · gray-500 → hover primary · `aria-label` · `Tooltip` 「되돌리기」 · `TooltipProvider` 하나 | `OrderCard.tsx:365-398` · `live/page.tsx:280` | PASS. `ResetIcon` 을 `scaleX(-1)` 로 뒤집은 것(`:376`)은 SPEC §6.3 이 FE 몫으로 둔 판단이고 보고서에 적혀 있다 |
| 확인 모달: `ConfirmModal` · 제목 두 문구 · 설명 「<방> · <시술>」 · `caution` · 「취소」/「되돌리기」 · 바깥 누르면 닫힘 · API 전에 닫음 · 실패면 오류 토스트 | `UndoConfirm.tsx:16-33` · `live/page.tsx:121-124,361` | 내용은 PASS · **모양 FAIL → F1** |
| 열린 동안 SSE 로 조건이 꺼져도 모달 그대로(누르면 409) | 대상(`UndoTarget`)을 state 로 들고 있음 · `live/page.tsx:66` | PASS |
| 토스트: [시작] · [종료] 성공 문구 「<방> · <시술> 시작/종료」 + [되돌리기] · **5초** · 다른 토스트는 2.6초 · 새 토스트가 앞 것을 바꿈(마지막 조작만) · 누르면 모달 없이 바로 API · 성공 「… 시술 대기로/시술 중으로 되돌림」(2.6초 · 버튼 없음) · 실패 = back `message` | `live/page.tsx:20-25,56-63,113-124,140-141,343-354` | PASS |
| 호출 · 수락 · 마취 · 귀가 대기 토스트에는 [되돌리기] 없음 | `run` 의 세 번째 인자를 넘기는 곳은 `onStart` · `onFinish` 둘뿐 | PASS |
| 토스트 버튼 간격 16 · `text-typo-body-600` · 밝은 primary(`text-primary-300` = `#d3f4fe`) | `live/page.tsx:336,347` | PASS (FE 가 고른 값 · 보고서 186행) |
| `api.ts` 두 함수 · `types.ts` 두 필드 | `lib/api.ts:70-72` · `lib/types.ts:85-86` | PASS(아래 참고 1) |

### 4. 범위 · public

- back 은 브리프 목록 밖에서 `repository/repo.py`(`started_event_id` 읽기) · `tests/fake_kos.py` 를 고쳤다. 둘 다 `procedure/back/**` 안이라 WORK-006 범위 안이고 보고서에도 적혀 있다 → PASS
- FE 의 back 파일은 `service/fake_board.py` 하나다(r6 W2 예외) → PASS

---

## 조용히 통과하는 자리

1. **모달 스크린샷을 「같음」으로 넘겼다** — F1. FE 보고서의 스크린샷 대조표가 버튼이 넘친 모달을 통과시켰다. 이번 판 FE 확인은 사람 눈 하나뿐이었다
2. **`canUndoStart` · `canUndoFinish` 기본값** — back 스키마는 `= False`(`schemas/board.py:100-101`), front 타입은 `?:`(`types.ts:85-86`)다. 앞으로 `_proc` 가 이 값을 빼먹어도 계약 시험(`test_contract.py`)은 bool 인지만 보니 통과한다. 지금은 `test_snapshot_flags` 가 True/False 를 직접 확인하므로 실해는 없다
3. **가짜 KOS 의 `complete:false → READY` 는 K2(PROCEDURE)를 흉내 낸 값이다** — ETCETERA 에서는 확인하지 않았다(W2)
4. **「방 배정」 시험 데이터는 `room_kos_id` 를 직접 넣는다** — KOS 화면에서 붙인 방 · ccc 밖 호출 경로는 시험에 없다(W1)
5. **가짜 보드는 늘 403** 이라 되돌리기 성공 · SSE 반영 · 두 화면 경합(#24)은 FE 쪽에서 실행된 적이 없다(W3). back 은 `TestClient` 안에서 SSE 1개까지만 본다

## 사용자가 실물에서 만날 자리 (코디 E2E 체크리스트 — SPEC §9 #21 ~ #26 + 회귀)

| # | 보는 것 | SPEC |
|---|---|---|
| E0 | **F1 수정 뒤에** 시작한다. 모달 두 버튼이 상자 안에 반씩 들어가 있는지 | §6.3 · F1 |
| E1 | §9 #0 준비: 「방 없는 ETCETERA」(시트팩)를 KOS 화면에서 붙일 때 **방이 붙지 않았는지** 먼저 본다. 방이 붙어 있으면 그 줄이 「방 배정」으로 숨고 [귀가 대기] 때 취소된다(W1). ccc 에서 [의사 호출]을 한 번 하면 일반 줄로 돌아온다 | §5.1 · W1 |
| E2 | (#21) 고객의 **첫** [시작] → 토스트 「<방> · <시술> 시작 · 되돌리기」가 5초 → 누른다(모달 없음) → 줄이 「<원장> 수락 · 시작 가능」/「<원장>」로 돌아오고 [시작] 켜짐 · 고객 「시술 대기」 · KOS 웹 화면 flowStep 도 시술 대기. 6초 뒤에는 토스트가 없다 | §5.13 · §8 |
| E3 | (#22) [종료] → 「완료」 **왼쪽** 아이콘 · 호버 「되돌리기」 → 모달 [취소] = 변화 없음 → 다시 열어 [되돌리기] → 줄 「<원장> · **원래 시작 시각** 시작」(경과도 원래 시작부터) · [종료] 켜짐 · 카드 아래 [귀가 대기] 사라짐 · KOS 작업 `READY` · KOS 웹 화면에서도 완료가 풀림 · **30초 뒤에도 `DONE` 으로 돌아가지 않음** | §5.13 · 사용자 확인 10-26 |
| E4 | (#23) 다른 시술이 진행 · 완료인 고객에서 진행 줄 [종료] **왼쪽** 아이콘 → 「시술 대기로 되돌리겠습니까?」 → 그 시술만 대기 · 고객 「시술 진행」 그대로 · KOS flowStep 변화 없음. 되돌린 시술은 「HH:MM 시작」이 사라지고 다시 [시작]하면 **새 시각**으로 시작 | §5.13 · 사용자 확인 10-26 |
| E5 | (#24) 브라우저 A [종료] → B 가 아이콘으로 되돌림 → A 토스트 [되돌리기] → 오류 토스트 「완료된 시술이 아니에요」 · 두 화면 모두 진행 | §5.13 동시성 |
| E6 | (#25) 아이콘이 없어야 하는 곳: 귀가 대기 카드의 완료 줄 · KOS 화면에서만 완료한 시술 · 대기 줄 · 「방 배정」(줄 자체가 없음) | §5.13 |
| E7 | (#26) #22 뒤 같은 시술 [종료] → 1분 뒤에도 완료 그대로 · `GET /api/board` 그 카드 `kos.status = ok` · KOS `DONE` | §8 대체 규칙 |
| E8 | **시트팩(ETCETERA)** 으로 [의사 호출] → 수락 → [시작] → [종료] → 되돌리기 한 바퀴. KOS 가 받는지(K5 · OQ-528). 거절되면 웹에는 아무것도 보이지 않으므로 `GET /api/board` 의 `kos` 나 back 로그로 본다 | W2 |
| E9 | 시트팩이 안 끝났으면 [귀가 대기]가 없다. 끝내고 [귀가 대기]를 누르면 KOS 에서 「방 배정」만 `CANCELED` 가 되고 시트팩은 `DONE` 그대로 | §5.7 |
| E10 | 아이콘(26px)은 끌 수 있는 카드 안에 있다 → 누르다 마우스가 조금 밀리면 카드 드래그가 시작될 수 있다(r1 E10 과 같은 결). 간호 스테이션에서 불편한지 본다 | §6.3 |
| E11 | 회귀 #6 · #8 · #9 · #14(호출 · 수락 · 귀가 대기 · 드래그 순서)가 그대로인지 | WORK-006 WP-E2E |

## 참고 (판정 밖)

1. `types.ts:85-86` 의 `?:` 는 「back 반영 전 스냅샷 호환」 때문이라고 주석에 있다. back 이 이제 늘 싣으므로 `boolean` 으로 좁혀도 된다(SPEC §7.2 「새 필드 · bool」)
2. r1 참고의 옛 주석 두 곳(`schemas/board.py:85` · `front/lib/types.ts:66`)은 모두 「규칙은 type 무관」으로 고쳐졌다
3. `visit.open_task_seqs` 는 이제 [귀가 대기]에서 쓰지 않는다(`actions.py:294` 가 `items` 를 본다). 열 · 동기화는 남아 있다(`db.py:28` 주석 「[귀가 대기] 취소 대상」은 옛말). 해는 없다
4. `SUPERSEDABLE` 의 `status` 묶음에는 호출(WAITING) · 수락(READY) op 도 원래부터 함께 들어 있다. 같은 작업의 뒤 되돌리기 op 이 앞 호출 · 수락 op 을 `confirmed` 로 닫을 수 있는데, 그 op 들은 그 시점에 이미 반영된 뒤라 실해는 없다

---

## F1 처리 — frontend (2026-10-26)
- 권장안(국소)대로 `UndoConfirm.tsx` 두 버튼 props 에 `style: { flexShrink: 1, minWidth: 0 }` · 전역 css 변경 0
- `undo-modal-start.png` · `undo-modal-finish.png` 다시 찍음 — 모달 x 552 ~ 1048 안에 [취소] 215px · [되돌리기] 213px 나란히
- tsc · lint · build 통과 · 상세 `frontend-r1-report.md` 「되돌리기 — 수정 r2」

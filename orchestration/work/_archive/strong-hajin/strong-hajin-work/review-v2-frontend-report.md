# 리뷰 리포트 — strong-hajin-work / v2 frontend 구현 (2026-09-17)

## 판정: **FAIL — 막는 것 하나(F-1, FE 두 줄).** 그 밖에는 WARN 7 · BE 연결과제 3.

**F-1 만이 재발주 사유**이고, **BE 작업도 통합도 막지 않는다.** 나머지는 전부 비차단이다.
**이 검수는 FE 구현분만 본다** — BE 는 지금 수정 중이고, 이 리포트는 **v2 전체 완료를 주장하지 않는다.**

## 검수 범위와 실행한 검사

- 대상: `v2-frontend-implementation-report.md`(253줄) + **baseline↔현재 frontend diff**.
- **기준선**: HEAD 차이가 아니라 `v2-code-baseline/{manifest.json, working-files.zip}` 이다.
  zip 에 없는 파일은 baseline = `git show HEAD:<path>` 로 복원해 대조했다(zip 은 W1 당시 **미커밋 파일만** 담는다).
  변경 규모: 제품 코드 8 · 신규 4 · 테스트 11. `MeetingDetailPage.tsx`·`labels.test.ts`·`InboxRail.tsx`
  셋은 **HEAD 와는 다르지만 baseline 과 바이트 동일** — v2 변경이 아니다(W1 미커밋분).
- 대조한 BE: `entrypoints/http.py` · `modules/work/application.py`(**수정 중인 실물**).
- **실행 0건** — 테스트·빌드·DB·브라우저 돌리지 않았다. 기존 로그만 열어 읽었다.
- **코디의 v2 `make verify` 는 아직 돌지 않았다.** 아래 수치는 FE 워커 세션 로그와 Phase 0 기준선뿐이다.

---

## 막는 것 (FAIL)

### F-1. 「취소 제안」·「조건 변경 제안」 단추가 **담당자에게도 선다 — 누르면 항상 403**

- **자리**: `frontend/src/features/work/WorkModals.tsx:1138`
  ```
  {!closed && requestTaskAccepted && !pendingProposal && ( 취소 제안 / 조건 변경 제안 )}
  ```
  이 구획 전체의 바깥 게이트는 `canManage`(`:1126`)이고, 그 값은 `MyWorkPage.tsx:844` 에서
  **`canManage={canManageOwnTasks}`** — **세션 역량**이지 「이 업무에서 내 자리」가 아니다.
  `requestTaskAccepted`(`:721`)도 `isRequestTask && assignee 있음 && !awaiting_acceptance` 뿐이라
  **요청자 판정이 없다.**
- **계약 근거**: BE 가 요청자만 허용한다 —
  `modules/work/application.py:1134-1135` `TaskAccessDenied("이 업무의 제안은 요청자만 낼 수 있습니다")`.
  SPEC-003 §5 도 제안은 요청자, 응답은 담당자로 갈랐다.
- **재현 조건**: 수락된 요청 업무를 **담당자 계정**으로 「내 업무」에서 열면 두 단추가 보인다 →
  누르면 403 이 오류 배너로 뜬다. 담당자는 그 드로어의 **가장 흔한 사용자**다.
- **같은 파일이 바로 아래에서는 제대로 갈랐다**: 응답 단추는 `:1285`
  `personaId && task.assignee?.member_id === personaId`, 제안 철회는 `:1294`
  `pendingProposal.proposed_by === personaId`. **한 파일 안에서 기준이 둘이다.**
- **최소 수정 (FE, 두 줄)** — `:721` 옆에 한 줄 두고 `:1138` 조건에 붙인다:
  ```ts
  /* 제안은 요청자의 자리다 (SPEC-003 §5 · application.py:1134). origin.actor 가 요청자이고,
     :726 이 이미 그 값을 이름으로 읽고 있다. 최종 판정은 서버가 다시 한다. */
  const viewerIsRequester = Boolean(personaId) && task.origin?.actor?.member_id === personaId;
  ```
  → `{!closed && requestTaskAccepted && viewerIsRequester && !pendingProposal && (…)}`
- **같은 원인의 짝 (따로 세지 않는다)**: `:1133` 「업무 취소」가 **수락 전 요청 Task** 를 보는
  수신자에게도 선다(`!requestTaskAccepted` 이므로). 위 한 줄과 같은 축이라 함께 닫힌다.
- **담당**: FE. **차단 범위**: 이 두 단추뿐. BE·통합·다른 Phase 를 막지 않는다.

---

## 비차단 (WARN)

### W-1. `isChildSettled` 의 보수 분기가 `TaskChild` 에서 **죽어 있다**
`features/work/workRows.ts:56` — `return !("origin" in child && isRequestTask(...) && !child.derived);`
`TaskChild`(`lib/viewModels.ts:160-170`)에는 **`origin` 도 `lineage` 도 없다.** 그래서
`state=done` + `approval` 이 `null`/부재인 하위는 **언제나 완결**로 센다. 주석(`:45-47`)은
「승인 축을 모르는 요청 업무만 보수적으로 미완결」이라 약속하는데 **코드가 그렇게 동작하지 않는다.**
**영향은 표시뿐이다** — 완료 단추를 이 값으로 막지 않고(확인함, 아래 PASS), 원장은 서버
`derived.blocking_children` 이며 `blockingChildrenOf`(`:65-66`)가 서버 값을 먼저 쓴다.
**최소 수정 (택일)**: (a) FE — 분기를 지우고 주석을 「승인 축을 모르면 완결로 센다. 원장은 서버다」로
정직하게 바꾼다. (b) BE — `children[]` 에 `origin_kind` 또는 `derived.approval` 을 언제나 싣는다(→ B-2).

### W-2. 코디가 지적한 「`derived` 존재를 요청 판정으로 오용」은 **실제로 제거됐다**
`workRows.ts:52-54` 가 승인 **값**(`awaiting_review`/`awaiting_revision`/`approved`)을 읽고,
요청 축은 `isRequestTask`(`:31-33`)가 **서버의 `origin.kind`/`lineage`** 로만 읽는다.
**새로 잘못 추측하는 자리도 없다.** 이 지적은 닫혔다 — W-1 은 그 분기의 잔여이지 재발이 아니다.

### W-3. `include_removed` 실패가 **말 없이** 일반 목록으로 내려간다
`MyWorkPage.tsx:193` `getWorkRequests(true).catch(() => getWorkRequests().catch(() => []))`.
서버가 `include_removed` 를 거절하면 사용자는 **영속이 깨진 것을 모른 채** 「숨긴 항목 보기」가
세션 로컬 값만 세는 화면을 본다. (바깥 `.catch(() => [])` 자체는 **기존 부채** — baseline `:145` 에 이미 있다.)
**최소 수정 (FE, 한 줄)**: 두 번째 catch 에서
`onError("숨긴 항목까지 읽지 못했습니다 — 「숨긴 항목 보기」가 이 세션에만 적용됩니다.")`.

### W-4. Phase 7-A 를 `[x]` 로 적었으나 **명시된 네 요소 중 둘이 다르게 처분**됐다
| 요소 | 시안 | WORK 7-A | FE | 판단 |
|---|---|---|---|---|
| 첨부 **DropZone** | `work-modal.jsx:242` `<Field label="첨부파일">` + `.scax-dropzone`(`:151-168`) | 이름으로 적혀 있다 | 만들지 않음 | **기존 기능 소실은 아니다** — baseline `CreateWorkModal` 에도 없었고 업로드는 상세의 `upload()`(baseline `:683`)뿐이다. 이유(생성 전 업로드 계약 없음)도 타당하다. **다만 그 처분이 WORK 가 아니라 보고서 부록 표에만 있다** |
| Composer **200자** | `maxLength`(하드 캡, `:76`) + 「200자 까지 입력 가능합니다」 힌트(`:227`) | 「내용 Composer 200자」 | 세고 스타일만 바꾸고 **막지 않는다**(`WorkModals.tsx:3626-3640`) | 판단은 합리적(붙여넣기가 조용히 잘린다)이나 같은 성격의 처분이다 |
**최소 수정**: WORK Phase 7-A 에 한 줄 처분(예 — 「첨부는 상세에서 붙는다. 생성 모달의 DropZone 은
**두 단계 업로드 계약**이 생길 때 세운다 · Composer 는 세되 막지 않는다」) 또는 FE 가 두 단계로 구현.
**7-A 는 `[x]` 가 아니라 「부분 완료」로 읽어야 한다.** 담당: 코디/planner 판정.

### W-5. 보고의 테스트 **회차 표 1행이 로그와 맞지 않는다** · 「마지막 두 회차」 표현

> **보존 위치 (코디, 17:46)**: `orchestration/work/strong-hajin-work/v2-frontend-verification/`
> 에 `frontend-test-5/6/7.log` · `tsc.log` · `frontend-build.log` 가 복사됐다. 보존본으로 재확인:
> **5 = `683 passed (683)` · 6 = `3 failed | 680 passed (683)` · 7 = `683 passed (683)` ·
> `tsc.log` 0바이트 · build `✓ built in 1.96s`.** 세션 scratchpad 원본과 바이트 크기까지 같다.

두 가지다.

1. **1회차 행.** 세션 scratchpad 의 가장 이른 로그 `frontend-test.log`(17:36:00)는
   **`Tests 7 failed | 676 passed (683)`** 인데 보고는 「1회차 · 부하 낮음 · exit 0 · **681/681**」로 적었다.
   **681 이 적힌 로그가 없다.** ⚠ **이 파일(과 2·3·4회차)은 보존본에 포함되지 않았다** —
   보존된 것은 5·6·7 뿐이므로, 나중에 이 행을 감사하려면 그 수치를 **본문에 적어 두어야** 한다.
2. **「마지막 두 회차」.** 코디 확인대로 그 둘은 **연속 두 회가 아니라 통과한 5·7** 이다(6이 그 사이에 있다).
   표현만의 문제이고 판정에 영향이 없다.

**결론 자체는 검증된다** — 보존본 `frontend-test-5.log`·`-7.log` 가 각각
**`Test Files 52 passed (52)` · `Tests 683 passed (683)`** 이고, Phase 0 기준선
`v2-phase0-frontend-test.log` 가 **`50 passed (50)` · `645 passed (645)`** 이므로 **+2 파일 · +38 테스트**가 맞다.
6회차 3건(`App`·`OrgPage`·`MeetingList`)도 보존본 `frontend-test-6.log` 와 일치하고, 보고가
「전량 green 을 단정하지 않는다」고 적은 것도 옳다.

**최소 수정 (둘 다 비차단)**: ① 1회차 행을 「`7 failed | 676 passed (683)` · 로그는 세션
scratchpad 에만 있음」으로 고친다(또는 그 로그도 보존본에 넣는다). ② 「마지막 두 회차」를
**「통과한 5·7 회차」**로 바꾼다.

### W-6. `baseline 82/82 불일치 0건` 은 **착수 시점** 값이다
지금 다시 재면 **동일 60 / 달라짐 22(FE 10 · BE 12)** 다(manifest 82 파일을 직접 재해시했다).
BE 12 는 `http.py`·`work/application.py`·`work_tasks.py`·`persistence.py`·`mcp.py`·`tool_catalog.py`·
`bootstrap/application.py`·`requests.py`·`assignments.py`·`creation_commands.py`·`errors.py`·
`unified-operations-inventory.json` — **지금 수정 중인 파일들**이다. 보고 §0 제목이 「착수 점검」이라
오독 여지는 작지만, **현재 대조가 아니라는 것**을 코디가 물었으므로 수치로 남긴다.

### W-7. `… | string` 타입 확장은 **기존 집 규칙**이다
새로 든 것은 `viewModels.ts:136,169,227,264,265`(`why`·`cancel_reason`×2·`kind`·`state`)이고,
baseline 에도 `:339,720,722,857,932` 가 같은 모양이다. 미지 값이 타입을 통과하지만 런타임은
`proposalKindLabel[...] ?? "제안"` 류 폴백으로 내려간다 — **새로 생긴 위험이 아니다.**
통합에서 BE 의 실제 값 집합과 한 번 맞춰 보면 족하다.

---

## BE 연결과제 (FE 결함 아님 — 코디가 BE 검수로 넘길 것)

| # | 무엇 | 근거 |
|---|---|---|
| **B-1** | **`GET /api/tasks/{id}/children` 이 `http.py` 에 없다** (grep 0건) | **SPEC-003 §4 API Contract `spec-003:544` 에 있는 계약**이다. FE `api.ts:326` 이 그 계약대로 함수를 두었고 **제품 호출부는 아직 없다**(테스트 mock 뿐) — 두 단계 표시는 상세 응답의 `children` 으로 서므로 지금 화면은 깨지지 않는다. BE 가 열면 그대로 쓰인다 |
| **B-2** | `children[]` 에 `derived`(최소한 `approval`)가 실리는지 | W-1 의 정확도와 UX-U5/U-7 이 여기 달렸다 |
| **B-3** | `started_at`/`accepted_at` 을 **각각** 내는지(UX-U3) · 완료 거부 409 의 **비공개 하위 일반 문구** | FE 는 서버 메시지를 **그대로** 배너에 낸다(`MyWorkPage.tsx:299`) — 문구 자체는 BE 몫이다 |

---

## 확인하고 문제 없던 것 (PASS 근거)

**코디가 이름으로 짚은 여섯 — 실물 수정 확인**

1. **`isChildSettled` 의 `derived` 오용** — 제거됐다(W-2). 잔여는 W-1.
2. **proposal mutation 봉투 타입** — FE `TaskProposalMutation`/`TaskProposalsView` 가
   `{task_id, proposal, task_version}` · `{task_id, pending[], history[]}` 이고,
   BE `application.py:1145`·`:1187`·`:1192-1196` 과 **같다.**
3. **`terms_change` payload 실제 입력** — `TermsChangePrompt`(`WorkModals.tsx:2038-2050`)가
   `title`·`due_date`·`description` 중 **고친 칸만** 싣고, 기한을 비우면 `due_date: null`,
   **하나도 안 고치면 전송이 비활성**이라 빈 payload 가 서버에 닿지 않는다.
   BE `application.py:1137`(빈 payload 거부)·`_apply_proposal(:1215-1225)`(정확히 그 세 칸 적용)과 일치.
   `cancellation` 은 payload 키 없이 `reason` 필수 — BE `:1139-1140` 과 일치.
4. **`include_removed`/`list_entry_hidden` 새로고침 토글** — 서버 먼저(`MyWorkPage.tsx:365`) →
   `reload()` → 실패하면 세션 로컬로 접고 **「이 화면에서만 숨겼습니다 — 새로고침하면 다시 나타납니다」**를
   말한다(`:374`). 목록은 서버 행의 `list_entry_hidden` 과 로컬의 **합집합**(`:459`).
   BE `http.py:1881-1893`(`include_removed` Query)·`:1925-1929`(DELETE, 본문 없음)과 일치.
5. **외부 `done` 으로 명령 추론 금지** — `reopenBlockedByApproval()`(`WorkModals.tsx:119-123`)를
   `allowedTaskTransitions`(`:131`)·행 액션(`:2181`)·상세 재개(`:1196`) **세 자리가 같이** 쓴다.
   `derived` 가 통째로 없으면 게이트를 걸지 않아 **옛 응답에서 있던 길을 닫지 않는다.**
   내가 재검수 1차에 낸 R-1 이 그대로 구현됐다(코드 주석이 「검수 R-1」로 출처를 적었다).
6. **비공개 하위 409 일반 문구** — 완료를 `blocking` 으로 **막지 않는다.** `complete()`(`:751-757`)가
   확인 모달을 띄우는 조건은 **체크리스트 남은 단계**(`openSteps`)뿐이고 하위가 아니다.
   막는 하위 구획(`:1310`)은 본문에 「**안내이지 관문이 아니다 · 내가 읽을 수 없는 하위도 서버는 센다**」로
   적혀 있다. 서버 오류는 `transitionTask` 의 catch(`MyWorkPage.tsx:299`)가 **메시지 그대로** 낸다.

**서버 권한 봉투 소비**

- 제안 **응답**·**철회**는 `assignee.member_id`·`proposed_by` 로 갈랐다(`:1285`·`:1294`) — 서버 값이다.
- 세션 역량(`canManageOwnTasks`·`canAssignTasks`·`canReadOrganizationWork`)은 **세션 봉투**에서 오고
  화면이 만들지 않는다. **유일한 구멍이 F-1** 이다(역량을 «이 업무에서의 자리» 로 쓴 자리).
- `api.ts` 밖 `fetch` **0건**.

**계약·금지 항목**

- **멱등 키**: 새 상태 명령에 싣지 않고(SPEC §4 Validation) 발송·생성에만 `Idempotency-Key` **헤더**로
  간다(`api.ts:230`·`:504`·`:587`). 새 명령은 전부 `expected_version`. DELETE list-entry 는 본문 없음 —
  BE 도 본문 없음. **일치.**
- **가짜 데이터·TODO·placeholder**: 새 제품 파일(`workRows.ts`·`WorkTables.tsx`)과 `MyWorkPage.tsx` 에 **0건.**
- **기존 생성 경로 소실 없음**: 회의 승격의 좁은 골격(`WorkModals.tsx:3286` `narrow`)이 살아 있고,
  담당자 비움 → 본인 업무 갈래도 남아 있다. baseline 에 있던 상세 업로드 경로도 그대로다.
- **`open → done`**: 상세 상단 「완료 처리」가 `open`·`in_progress` 둘 다에서 선다(`:1174`).
  행 액션은 `transitionFor.open = {in_progress:"start"}`(`:103`)라 **[시작]만** — WORK 7-C 그대로.
- **7-D·7-E 의 「만들지 않는다」**: `InboxRail.tsx`·`SideNav.tsx` 가 **baseline 과 바이트 동일**이다.
  아바타·수신 시각·출처를 안 그린다는 주석도 baseline 의 것이다 — **지켜졌으나 「구현」이 아니라 「유지」**이므로
  보고의 `[x]` 는 그렇게 읽어야 한다.
- **시안 대조(자동 범위)**: 탭 셋 · 칩 세트(「막힘」 없음 — M-6) · `TaskTable` `--nostar` 5열(M-21) ·
  글리프 10종 추가. 「내 업무」 칩에 시안에 없는 「시작 전·진행 중」 둘이 더 있는데 **기존 필터의 계승**이고
  계약 위반이 아니다. **배치·여백·읽힘은 사용자 E2E 몫이다.**

## 자동 검증 ↔ 사용자 E2E 의 경계

- **자동으로 닫힌 것**: 타입(`tsc --noEmit` exit 0 — 보존본 `v2-frontend-verification/tsc.log` 0바이트) · API 매핑(위 대조) ·
  `workRows`/`TaskLifecycleV2` 회귀 · `frontend-test` **683/683**(5·7회차) · `frontend-build` exit 0.
- **닫히지 않은 것**: UX-U1~U-15 의 **표시·자리** 칸 전부, E-1~E-12, 시안 배치.
  **브라우저 E2E 는 실행되지 않았고, 이 리포트는 그것을 통과로 세지 않는다.**
- **코디의 v2 `make verify` 는 아직 돌지 않았다.** `make frontend-test` 단독 결과만 있다.

## 기존 부채 (v2 직접 위반과 분리)

- `reload()` 의 `.catch(() => [])` 묶음(baseline `MyWorkPage.tsx:143-146`) — 목록 읽기 실패가
  **빈 목록으로 조용히** 보인다. v2 가 그 위에 `include_removed` 폴백만 얹었다(W-3).
- `… | string` 타입 확장 관행(W-7).
- 부하에서 5초 한도에 걸리는 시간 민감 테스트(`App`·`OrgPage`·`RelationGraph`·`MeetingList`) —
  이번 범위 밖이고 FE 워커도 손대지 않았다. 통합 검증에서 다시 뜨면 같은 성격이다.

## 결론

FE 구현은 **계약을 추정으로 메우지 않았고**, 코디가 이름으로 짚은 여섯 지적이 **전부 실물로 반영**됐다.
막는 것은 **F-1 하나**이고 **FE 두 줄**이다. W-4 는 FE 가 아니라 **WORK 문서의 한 줄 처분**이 필요한 자리다.
**이 검수로 BE 나 v2 전체의 완료를 주장하지 않는다** — B-1~B-3 과 사용자 E2E 가 그대로 열려 있다.

---

# 재검수 1차 (2026-09-17) — FE 정정 1차 한정

## 판정: **FAIL 해소.** F-1 · W-1 · W-3 · W-5 **넷 다 닫혔다.** 새로 남는 것은 **비차단 둘**(N-1 · N-2).

최초 검수 전체를 반복하지 않았다. **정정된 자리와 새 첨부 구현만** 봤다.
**실행 0건** — 보존 로그(`v2-frontend-verification/fix1-*`)만 읽었다. 제품 무수정.

## 해소표

| # | 어떻게 닫혔나 (실물 확인) | 판정 |
|---|---|---|
| **F-1** | 게이트 셋이 **서버 판정과 같은 값**을 읽는다. 아래 별도 절 | **해소** |
| **W-1** | `workRows.ts:52-57` — 죽은 분기를 지우고 규칙이 **승인 값 한 줄**이 됐다. 주석(`:35-51`)이 **실제 동작과 일치**하고 「이 함수는 원장이 아니다 · 서버 값을 먼저 쓴다」를 근거까지 적었다. `blockingChildrenOf`·`childProgressOf` 가 서버 값 우선인 것도 그대로다 | **해소** |
| **W-3** | `MyWorkPage.tsx:198-207` — `getWorkRequests(true)` 성공 시 플래그 해제, 실패 시 **일반 목록은 살리고** 플래그를 세운다. `settleError()`(`:242-243`)가 **아직 참인 경고만 남기고** 호출부 6곳(`:253·323·339·357·375·396`)에 걸려 **성공 한 번에 지워지지 않는다** | **해소** |
| **W-5** | `v2-frontend-implementation-report.md` §5 — 「exit 0 · 681/681」 행을 **지우고** 「로그 없음(덮어씀) · **근거로 쓰지 않는다**」로 바꿨다. 회차마다 **로그 파일명**을 달았고 「마지막 두 회차」도 **「통과한 5·7 회차」**로 고쳤다. `frontend-test.log` 도 보존본에 들어왔다 | **해소** |
| W-6 | §0 에 「이 수치는 착수 시점 값이다 · 현재 상태로 읽지 않는다」를 박았다 | 해소(확인만) |

## F-1 — 해소. 그리고 **내가 제안한 한 줄이 틀렸다**

내 최소 수정은 `task.origin?.actor?.member_id === personaId` 였다. **FE 가 BE 를 열어 보고 그것을
쓰지 않은 판단이 옳다.**

- 서버 판정은 `_is_request_owner`(`modules/work/application.py:1281-1294`)이고 내용은
  **`principal.id ∈ {request.requester_id, request.promoted_by_member_id}`** 다.
- `origin.actor` 자리에 실리는 값은 `_origin_projection` 의 **`request_requester_id`** 뿐이다
  (`application.py:1378`). **회의 승격 요청은 `requester_id` 가 `system:meeting`** 이라
  내 제안대로 했으면 **승격을 누른 본인이 자기 요청에서 빠졌다.**
- FE `isRequestOwner`(`workRows.ts:143-146`)는 **서버와 같은 두 항**을 읽는다. 대조해 일치 확인.
- 새 조회를 열지 않고 **이미 읽어 둔 요청 목록**에서 행을 찾아 넘긴다(`MyWorkPage.tsx:908·926`).
  못 찾으면 `false` — **모르면 없는 권한을 그리지 않는다.**

**함께 고친 두 축도 서버와 맞는다** (BE 실물 대조):

| 명령 | 서버가 여는 사람 | 근거 | 화면 | 일치 |
|---|---|---|---|---|
| 취소·조건 변경 제안 | 요청자 **또는 승격을 누른 사람** | `_is_request_owner` (`:1281-1294`) | `viewerIsRequester`(`WorkModals.tsx:1166`) | ✓ |
| 직접 취소·시작·완료·막힘 | **활성 담당** | `transition()` → `repository.task(id, principal)` 의 `_held_by` | `viewerDrives`(`:746`, `:1159`) | ✓ |
| 재개 | 요청 업무는 **요청자**, 그 밖은 담당자 | `_require_may_reopen`(`:1123-1136`) | `reviewed ? viewerIsRequester : viewerDrives`(`:1226`) | **거의** — N-1 |

- 「수락 전 요청 Task 에 수신자에게도 「업무 취소」가 선다」(내 F-1 의 짝)도 `heldByNobody`(`:744`)로 닫혔다.
  FE 의 정정 — 그 자리는 403 이 아니라 **404** 라는 것 — 이 맞다. `_held_by` 는 조회부터 막는다.
- **정상 경로 보존 확인**: `personaId` 를 넘기지 않는 화면(오늘·캘린더)에서는 `heldByOther` 가
  `false` 로 남아 **본인 업무 취소가 그대로 선다**(`:744-746`). 모른다고 있던 길을 닫지 않았다.
- 요청자 본인의 제안 둘·재개·제안 철회, 담당자의 완료 보고·시작·막힘·동의/동의하지 않음은 전부 그대로다.

## 새로 남는 것 — 비차단 둘

### N-1. 재개 게이트가 **승격 경로에서만** 서버보다 한 사람 넓다 (지금은 닿지 않는다)
서버의 두 축이 서로 다르다 — 제안은 `_is_request_owner`(promoted_by **포함**)인데,
재개는 `_require_may_reopen` → **`_requester_of`(`application.py:995-999`)** 이고 그것은
**`request.requester_id` 하나만** 돌려준다(대행 없음 · BASE-002 O-29·O-31).
FE 는 두 자리에 **같은 `viewerIsRequester`** 를 쓰므로(`WorkModals.tsx:1226`), 회의 승격 요청
업무에서는 **누른 사람에게 「재개」가 서지만 서버는 `TaskReopenForbidden`** 을 낸다.
- **재현 조건**: 요청자가 `system:meeting` 인 요청 Task 가 **승인까지 끝나** `state=done` ·
  `derived.approval=approved` 가 된 뒤, **승격을 누른 사람**이 상세를 연다.
- **지금은 도달하지 않는다** — **OQ-206 이 미답**이라 그 Task 의 완료 승인을 부를 수 있는 사람이
  0명이고(SPEC-003 §7 안 A 의 결과), 그래서 `approved` 에 이르지 못한다. **OQ-206 이 답되는 순간
  살아나는 자리**다.
- **최소 수정 (택일)**: (a) FE 한 줄 — 재개에만 요청자 단일 판정을 쓴다
  `const viewerReopens = reviewed ? request?.requester_id === personaId : viewerDrives;`
  (b) OQ-206 답과 함께 BE `_requester_of`/`_require_may_reopen` 을 제안 축과 맞추고 FE 는 그대로 둔다.
  **(b) 가 두 축을 하나로 모으므로 낫다** — 다만 그것은 OQ-206 의 답이 정하는 자리다.
- **담당**: FE 한 줄이면 즉시, 아니면 BE 통합 때. **착수를 막지 않는다.**

### N-2. fix1 의 **빌드 증거가 없다**
`make frontend-build` 는 이번 판에서 **돌지 않았다**(FE 가 「코디 몫」이라 적었고 실제로 로그가 없다).
보존본의 `frontend-build.log`(17:42)는 **fix1 이전 코드**의 것이다. `npx tsc --noEmit` 은 exit 0 이라
타입은 닫혔지만 **fix1 코드의 빌드 통과를 주장할 수 없다.**
→ 코디 통합 검증에서 `make frontend-build` 한 번이면 닫힌다. **비차단.**

## 새 첨부 (Phase 7-A) — 브리프의 검사 항목별

| 검사 | 결과 | 근거 |
|---|---|---|
| 본인 생성에 **한정**한 DropZone | ✓ | `attachSupported = kind === "task" && ownerRoute === "self"`(`WorkModals.tsx:3182`) |
| 다른 갈래는 **담당자 상세 첨부 안내**, 발송자 권한 확대 없음 | ✓ | `attachBoundary`(`:3183-3186`)가 **「누가」를 문장에 넣었다** — 「담당자가 … 요청은 상대가 수락해 담당자가 된 뒤」. 새 API·새 권한 0건 |
| **evidence 에 파일을 대신 넣지 않음** | ✓ | `uploadRequestEvidence` 호출은 `:2399` **하나뿐**이고 그것은 baseline 의 요청 상세 근거자료 경로다. 생성 모달은 부르지 않는다 |
| 갈래 변경 때 **조용한 유실 없음** | ✓ | 파일은 `attachments` 에 **그대로 남고**, 못 붙는 갈래에서 `FieldMessage` + 「함께 붙지 않는 파일」 목록으로 **명시**된다(`:3824-3840`). 담당을 되돌리면 다시 선다. 그 갈래에서 업로드를 **성공한 척 부르지 않는다** |
| 생성 성공 + 업로드 실패 → **중복 생성 없음** | ✓ | `submitAttempt.current = null` 뒤 `setCreated(...)`(`:3318-3321`), 그리고 `submit()` 첫 줄이 `if (created) { await retryAttach(); return; }`(`:3222-3226`) — **생성 경로로 돌아가지 않는다** |
| 일부만 성공 후 재시도 → **중복 첨부 없음** | ✓ | `attachTo()`(`:3189-3198`)가 **실패한 것만** 돌려주고 `retryAttach()` 가 `created.failed` 만 다시 올린다(`:3207`) |
| **거짓 실패로 숨기지 않음** | ✓ | 업로드 실패 분기에서도 `onCreated(...)` 를 **먼저** 부른다(`:3313-3316`) — 목록이 그 업무를 들고, 그 다음에 「업무는 만들어졌지만 첨부 N건을 …」로 말한다 |
| 취소/닫기 | ✓ | `created` 상태의 세 출구(「나중에 붙이기」·「업무 열기」·「첨부 다시 시도」, `:3421-3444`)가 전부 안전하다. 모달이 **조건부 마운트**(`MyWorkPage.tsx:993`)라 닫으면 `created`·`attachments`·`submitAttempt` 가 초기화되어 **다음 생성이 옛 업무에 재첨부되지 않는다** |
| 생성 성공 후 `onCreated` 자체가 실패할 때 | ✓ | 그 경로는 `submitAttempt.current` 를 지우지 않으므로 재시도가 **같은 멱등 키**로 가고 서버가 영수증을 돌려준다 — 업무가 둘 서지 않는다 |
| Composer 200자 | ✓ | 하드 캡 없이 카운터만(현행 유지). **이 해석을 첨부 누락의 면제로 쓰지 않았다** — 본인 갈래는 실제로 구현했다 |

**다만 Phase 7-A 는 여전히 「전부 완료」가 아니다** (내 W-4 의 잔여). 관리자 배정·요청 발송·회의 승격
세 갈래는 **기존 자료 쓰기 권한 계약**(`materials.attach` → `work_tasks.task()` 의 `_held_by`) 때문에
열리지 않았고, FE 도 **완료라고 적지 않았다.** WORK 에 그 경계를 한 줄 적는 것은 **코디/planner 몫**이다.

## 검증 증거 — 보존 로그를 직접 열어 확인

| 파일 | exit | 수치 |
|---|---|---|
| `fix1-frontend-test-1.log/.exit` | **2** | `Tests 7 failed \| 697 passed (704)` |
| `fix1-frontend-test-2.log/.exit` | **0** | `Test Files 53 passed (53)` · `Tests 704 passed (704)` |
| `fix1-tsc.log/.exit` | **0** | 로그 0바이트 |

- **1회차 실패 7건은 전부 «이번에 새로 더한» 테스트**다 — `CreateWorkAttach.test.tsx` 5 ·
  `MyWorkPage.test.tsx` 의 W-3 회귀 2. **부하 flake 가 아니라 빨강→초록 사이클**이고,
  FE 가 원인을 자기 탓(요청 갈래 JSX 안에 첨부 칸을 둠 · `renderPage` 뒤 모킹)으로 적은 것과 맞는다.
- 기준선 **645(50파일)** → 직전 판 **683(52)** → 지금 **704(53)**. **+21 테스트 · +1 파일.**
  삭제·skip·단언 약화는 보이지 않는다.
- 사소: `.exit` 파일 내용이 `exit=2`·`exit=0`·`tsc exit=0` 문자열이라 **순수 종료코드가 아니다.**
  사람이 읽는 데는 문제없지만 기계 파싱은 안 된다.
- **`make frontend-build` 와 `make verify` 는 이번 판에서 돌지 않았다** → N-2.

## 경계 — 이 재검수가 주장하지 않는 것

- **BE 는 수정 중이다.** 이번 검수로 **v2 전체·통합 완료를 주장하지 않는다.**
- **B-1~B-3 은 그대로 열려 있다** — `GET /api/tasks/{id}/children` 부재(SPEC-003 §4 계약) ·
  `children[]` 의 `derived` 동반 · `started_at`/`accepted_at` 분리. **후속 BE 통합 검수 몫**이다.
- **브라우저 E2E 미실행.** UX-U1~U-15 의 표시·자리 칸과 E-1~E-12 는 사용자 몫이다.
- **코디의 `make verify` 는 아직 없다.**

## 결론

**막는 것이 없다.** F-1 이 닫혔고, 정정이 **내 제안보다 정확한 자리가 하나**(`origin.actor` 대신
`requester_id`/`promoted_by_member_id`) 있다. 새 첨부는 두 단계·중복 없음·유실 없음·거짓 실패 없음이
전부 회귀로 서 있고, **못 여는 세 갈래를 완료라고 적지 않은 것**이 옳다.
남은 N-1 은 **OQ-206 이 답될 때** 함께 닫으면 되고, N-2 는 코디 빌드 한 번이면 끝난다.

---

# 재검수 2차 (2026-09-17) — N-1 정정 한정

## 판정: **N-1 해소.** 새 결함 없음. 새 지적은 **테스트 구멍 하나**(N-3, 비차단).

N-1 만 봤다. 앞선 검수의 닫힌 항목은 다시 열지 않았다. **실행 0건** — 보존 로그만 읽었다. 제품 무수정.

## N-1 — 해소

**고친 자리가 정확히 둘이고, 그 둘뿐이다.**

| 확인 | 결과 |
|---|---|
| `isRequestRecordRequester` 가 **raw `requester_id` 하나만** 읽나 | ✓ `workRows.ts:163-166` — `request.requester_id === personaId` 뿐 |
| BE `_requester_of` 와 일치하나 | ✓ `modules/work/application.py:1044-1048` — `str(request.requester_id)` 하나만 돌려준다(대행 없음). **BE 가 수정 중이라 줄 번호가 밀렸으므로 다시 찾아 대조했다** |
| 제안의 **두 항**은 그대로인가 | ✓ `isRequestOwner`(`workRows.ts:143-146`)가 `requester_id \|\| promoted_by_member_id` 로 **손대지 않았고**, 제안 게이트(`WorkModals.tsx:1175`)가 여전히 `viewerIsRequester` 를 쓴다. BE `_is_request_owner` 와 일치 |
| 재개만 좁아졌나 | ✓ `WorkModals.tsx:1236` — `reviewed ? viewerIsRecordRequester : viewerDrives`. 바뀐 항은 **요청 갈래 하나**뿐이다 |
| 배선이 반대로 꽂히지 않았나 | ✓ `MyWorkPage.tsx:908`(넓은 판정 → `viewerIsRequester`) · `:909`(좁은 판정 → `viewerIsRecordRequester`). 관련 업무 드로어도 같다(`:927-928`) |

**보존 확인**

- **일반 요청의 요청자**: `requester_id` 가 사람 id 이므로 두 판정이 같은 답을 낸다 → **재개 그대로 선다.**
- **본인 업무·배정 업무**: `reviewed` 가 거짓이라 `viewerDrives` 로 가고 **그 축은 건드리지 않았다.**
- **오늘·캘린더**(`personaId` 를 넘기지 않는 화면): 두 prop 모두 기본 `false`(`WorkModals.tsx:387-388`)인데,
  **fix2 이전에도 `viewerIsRequester` 가 같은 기본값이었다** — 그 화면들의 동작은 **변하지 않았다.**
- **승격자**: 제안 둘은 **그대로 서고**, 서버가 거부하는 **재개만** 숨는다.
- **서버 입력·역량 불변.** 화면 노출만 좁혔다.

**OQ-206 을 확정하지 않았다** — 코드 주석(`workRows.ts:159-161`)과 회귀 주석(`TaskLifecycleV2.test.tsx:207`)
둘 다 「지금 서버가 여는 만큼으로 노출을 맞출 뿐 · 미결을 기본값으로 확정하지 않는다 · 서버가 열면 함께
넓힌다」를 명시한다. **승격 재개 정책을 새로 정한 것이 아니다.** 이 판정에 동의한다.

## 검증 증거 — 보존 로그 직접 대조

| 파일 | exit | 수치 |
|---|---|---|
| `v2-frontend-verification/fix2-frontend-test.log/.exit` | **0** | `Test Files 53 passed (53)` · `Tests 706 passed (706)` · `FAIL` 0줄 |
| `v2-frontend-verification/fix2-tsc.log/.exit` | **0** | 로그 **0바이트** |

- 직전 판 **704** → **706**: **+2** 가 이번 회귀이고 둘 다 실물로 확인했다 —
  「승격 요청의 누른 사람에게 제안은 서지만 재개는 서지 않는다」(`TaskLifecycleV2.test.tsx:209`) ·
  「일반 요청의 요청자는 재개를 그대로 부른다」(`:235`). 삭제·skip·단언 약화 없음.
- **한 번에 통과했다** — fix1 과 달리 재실행 로그가 없다.

## 새 지적 — N-3 (비차단, 테스트 구멍)

**`isRequestRecordRequester` 에 단위 테스트가 없다.** `workRows.test.ts` 에 그 이름이 **0건**이고,
드로어 회귀 둘은 `viewerIsRequester`/`viewerIsRecordRequester` 를 **props 로 직접 주입**한다
(`TaskLifecycleV2.test.tsx:222·229·239`). 그래서 **두 조각이 각각만 검증되고 «어느 판정이 어느 prop 에
꽂히는가»는 아무 테스트도 보지 않는다.**

- **실제 조건**: `MyWorkPage.tsx:908-909`(또는 `:927-928`)의 두 줄을 **서로 바꿔도** 현재 스위트가
  **전부 통과한다.** 그러면 승격자에게 재개가 다시 서고(N-1 재발) 제안이 사라진다.
- **지금 코드는 옳다** — 위 표에서 배선을 눈으로 확인했다. 구멍은 **회귀가 그것을 지키지 못한다**는 것뿐이다.
- 형제 판정인 `isRequestOwner` 는 fix1 에서 단위 회귀 4건을 받았으므로 **비대칭**이기도 하다.
- **최소 수정 (택일, 한 건)**:
  (a) `workRows.test.ts` 에 한 줄 — `isRequestRecordRequester({requester_id:"system:meeting",
  promoted_by_member_id:"mina"}, "mina")` 가 **false**, `{requester_id:"mina"}` 가 **true**.
  (b) 더 나은 쪽 — `MyWorkPage.test.tsx` 에서 **승격 요청 업무의 상세를 열어** 「재개」가 없고
  「취소 제안」이 있는 것을 단언한다. 배선까지 함께 묶인다.
- **담당**: FE. **차단 없음** — 코드가 이미 맞으므로 통합·발주를 막지 않는다.

## 경계 — 그대로 남는 것

- **`make frontend-build` 와 전체 `make verify` 는 여전히 미실행이다**(N-2 그대로). fix2 도 돌리지 않았다.
- **브라우저 E2E 미실행** · **B-1~B-3(BE 연결과제)** 열려 있음 · **BE 통합 검수는 별도.**
- Phase 7-A 의 세 갈래 첨부(W-4 잔여)도 그대로다.
- **이번 재검수로 v2 전체·통합 완료를 주장하지 않는다.**

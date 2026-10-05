# WORK-010 Phase 2b 결과 보고 (frontend)

## 상태: done

- 워크트리 `Strong_hajin/strong-hajin-polish3`. HEAD 는 `cc64d18`(2a 커밋)이고 Phase 3 는 `9c15934` 로 이미 커밋돼 있다. 커밋·push 는 하지 않았다.
- 손대지 않은 곳: `lib/shell.ts` · `src-tauri/` · `App.tsx` 다운로드 수신부(`onShellDownload`).

## 수행 내용

### 변경 파일

| 파일 | 무엇 |
|---|---|
| `features/work/WorkModals.tsx` | `TaskDetailDrawer` (아래 항목) · `ReasonPrompt` · `TermsChangePrompt` · `BlockReasonPrompt` 서명 · `stateTriggerTone` export |
| `ds/Modal.tsx` | `OverlayShellProps.headerActions` 를 더했다 — 머리 오른쪽, × 바로 앞. 안 넘기면 예전과 같다. |
| `ds/Select.tsx` · `styles/meetings.css` | `SelectOption.tone?: "danger"` → `.popover-item.danger`(글자색만) |
| `features/work/MyWorkPage.tsx` | `TaskStateCell` 이 공용 `stateTriggerTone` 을 쓴다(사본 삭제) · W5 `settleError()` |
| `features/today/TodayPage.tsx` · `features/calendar/CalendarPage.tsx` | W5 `onError(null)` |
| `App.tsx` · `features/chat/ChatDrawer.tsx` | W2 죽은 AX 참고 자료 경로를 지웠다 |
| `lib/labels.ts` | `taskDetail` 키를 정확히 그 자리만 고쳤다. **더함**: `blockers` · `metaStateSelect` · `stateCancel` · `metaAssigneeSelect` · `handoverDescription()` · `proposalMenu` · `proposeCancel` · `proposeTerms` · `assigneeProposedNobody` · `inlineSaving`. **바꿈**: `assigneeProposed` → `(name) => 「{name}에게 변경 제안 중」`. **지움**: `blockProgress`. |
| `styles/task-detail.css` | `.task-blockers` · `.desc--editable` 상자(W3) · `textarea.desc` 활자 · 제목의 「저장 중」 |
| `styles/components.css` · `styles/screens-a.css` | 쓰는 곳이 0 이 된 `.scax-block-reason*` 3규칙 · `.handover` 1규칙을 지웠다 |

**테스트**
- 신규: `TaskDetailStateSelect.test.tsx` 31건 · `taskDetailHarness.test-utils.ts`(셀렉트·`⋯` 손잡이)
- 고침: `TaskLifecycleV2` · `TaskCompletionFlow` · `TaskDelivery` · `Checklist` · `Predecessors` · `TaskDetailRelations` · `TaskDetailDates` · `ChatDrawer`

### 구현 요점

- **한 줄(W1)**: `enqueue(job)` 하나에 다음이 모두 선다.
  - 인라인 저장(`saveInline`)
  - 진행 상태 전이(`transition`)
  - 재개(`reopenTask`)
  - 담당 변경 제안(`reassignTask`)
  - 체크리스트 명령 5종(추가·체크·이름·순서·삭제)

  다음 명령은 그때의 `versionRef`(마지막 응답 회차)를 싣는다. 전이가 성공하면 `readDetail()` 로 회차를 새로 받는다.
  `queued > 0` 이면 진행 상태·담당 셀렉트·`⋯` 가 잠긴다.
- **진행 상태 셀렉트**: `stateMoves` 가 SPEC §2.10.5 표를 그대로 옮긴 것이다(아래 대조).
  - 고르면(`pickState`) 다음 중 하나가 일어난다.
    - 막힘 → `BlockReasonPrompt`(필수)
    - 업무 취소 → 기존 사유 `ReasonPrompt`(필수 · danger)
    - 완료에서 재개 → 기존 재개 `ReasonPrompt`(선택)
    - 요청 업무 완료 → `CompletionReportModal`
    - 미완 체크리스트 완료 → 기존 `ConfirmModal`
    - 그 밖 → 바로 `onTransition`
  - 셀렉트 값은 늘 `task.state` 다(낙관적 갱신 없음). 그래서 모달을 닫거나 서버가 거부하면 원래 값이다. 거부는 호출부의 공통 오류 토스트다.
  - 트리거 톤은 목록 `TaskStateCell` 과 같은 `stateTriggerTone` 이다(공용으로 뺐다).
  - 「업무 취소」는 목록 맨 아래에 `tone:"danger"` 로 둔다.
- **선행(R5)**: 상세의 `startBlocked`·`blockedText`·푸터 `scax-blocked-note` 경로를 지웠다. 셀렉트는 `진행 중`·`완료` 를 미리 막지 않는다.
- **`⋯`**: `headerActions` 자리에 `Select` + 아이콘 단추 트리거(「⋯」, 접근 이름 「요청자 제안」)를 둔다.
  - 조건 = `editable && requestTaskAccepted && viewerIsRequester && !pendingProposal` — 예전 푸터 조건 + 읽기 전용 입구 제외.
  - 항목 「취소 제안」·「조건 변경 제안」은 기존 `ReasonPrompt`·`TermsChangePrompt` 를 연다.
- **담당 셀렉트**
  - 조건 = `canAssign && editable && !assignments.pending`.
  - 후보는 셀렉트가 설 때 한 번 읽는다(`GET /api/task-assignment-candidates`). 지금 담당이 후보에 없으면 그 이름을 첫 줄에 넣어 값이 읽히게 한다.
  - 고르면(지금 담당이면 무동작) 사유(선택) `ReasonPrompt` 가 열린다. 「변경」 → `reassignTask` 를 줄에 세워 보낸다.
  - 실패 문장은 모달 안(`ReasonPrompt` 의 새 `error`)에 낸다.
  - 성공하면 토스트 · `readDetail` · `getTaskAssignments` 다시 읽기 → 「{대상}에게 변경 제안 중」 배지 + 「담당 변경 대기」 상자.
  - 「담당자 변경」 단추와 그 겹 `Modal sm`(대상 Select · 대상 칸 오류)은 지웠다.
- **걸린 일 상자**: 「진행과 판단」 `section.block`·`h3` 를 지웠다.
  - `div.task-blockers[role=group][aria-label="걸린 일"]` 를 메타 정보 바로 다음 형제로 둔다.
  - 상자 순서는 SPEC 표 그대로다: 막힘 사유(이제 `notice` 상자) · 완료 확인 대기 · 보완 필요 · 담당 변경 대기 · 응답 대기 제안 · 미완 하위.
  - 상자 안의 조건·단추·명령은 그대로다. 하나도 없으면 아무것도 서지 않는다.
- **푸터**: `footer` prop 을 넘기지 않는다 → `.scax-modal__foot` 가 없다.
- **W3**
  - 읽는 칸 `p.desc.desc--editable` 이 입력과 같은 상자(투명 1px 선 + 안여백 8·10 · 모서리 8)를 미리 쥔다. 글자는 둘 다 `.desc`(13px · 1.65)이고, `textarea.desc` 는 전역 `min-height`·글자 크기를 덮는다.
  - 캐럿은 `autoFocus` 대신 effect 에서 `focus()` + `setSelectionRange` 로 놓는다. 누른 자리의 선택 오프셋을 쓰고, 못 잡으면 글 끝이다.
- **W4**: 칸마다 `saving` 표시를 둔다. 날짜·내용은 `FieldMessage` help 자리(실패 문장이 서는 자리)에, 제목은 머리 안 `span.scax-field__hint` 에 「저장 중…」을 낸다. 성공 토스트는 없다.
- **W5**: 인라인 저장이 성공하면 호출부 3곳이 전역 오류를 걷는다.
- **W2**: 아래 「지운 자리」 표.
- **발견해 함께 고친 것**
  - `ReasonPrompt`·`TermsChangePrompt` 는 겹 스택(`useEscape`)에 오르지 않았다. 그래서 그 모달의 Esc 가 **아래 업무 상세까지 닫았다**(window 리스너가 같은 Esc 를 받는다).
  - 두 모달에 `useEscape(onClose)` 를 더하고 입력칸의 개별 Esc 처리를 걷었다. 사용처 9+1 전부에서 Esc 가 그 모달만 닫는다.
  - `ReasonPrompt` 의 Enter 는 한글 조합 중이면 보내지 않는다.

## 계약 체크 (WP 2b)

### 2b-1 진행 상태 셀렉트
- [x] 메타 정보 진행 상태 = 셀렉트. 확인 대기 완료는 글자만(업무 취소도 없음). 옵션은 §2.10.5 표 그대로다.
  - 완료 업무에 업무 취소가 없다. 요청자에게 시작·막힘·완료가 없다.
  - 톤은 목록과 같다. 부품은 **`stateTriggerTone` 을 나눠 쓴다.** 셀렉트 몸통은 목록 선례와 갈 곳 규칙이 달라(취소·재개·역할) 공용으로 합치지 않았다 — 「판단」이다.
- [x] 막힘(필수) · 업무 취소(필수, 맨 아래 빨강) · 완료에서 재개(선택)는 작은 모달이다. 본문 막힘 입력 `isBlocking` 을 지웠다.
- [x] 요청 업무 완료 = `CompletionReportModal` · 미완 체크리스트 = 「남은 단계가 있습니다」
- [x] 서버 거절은 공통 오류 토스트 + 셀렉트 원래 값이다. 상세의 `startBlocked` disabled 경로를 지웠다.
- [x] 성공 토스트·다시 읽기는 호출부 `transitionTask` 등을 재사용하고, 상세는 `readDetail` 로 다시 읽는다.
- [x] `⋯` 는 요청자에게만 선다. 항목 둘 → 지금 모달.

### 2b-2 담당 셀렉트
- [x] `canAssign && !readOnly`(+ 취소 아님 + 대기 제안 없음)일 때 셀렉트, 그 밖은 이름 글자다. 고르면 사유(선택) 모달 → `/reassign`.
- [x] 성공 뒤 「{대상}에게 변경 제안 중」. 토스트 문장은 그대로다. 대기 제안이 있으면 셀렉트를 열지 않는다.
- [x] 「담당자 변경」 단추와 겹 `Modal` 을 지웠다(남는 코드·CSS 정리 포함).

### 2b-3 걸린 일 · 진행과 판단 · 푸터
- [x] 「진행과 판단」 구역 제목·덩어리를 지웠다. 구획 1~5·7 은 조건이 참일 때만 메타 정보 바로 아래 상자로 선다.
- [x] 푸터 전부를 지웠다(빈 footer 줄 없음).
- [x] 목록 행 `TaskQuickActions` 의 `scax-blocked-note`·`startBlocked` disabled 와 공용 CSS `.scax-blocked-note` 는 그대로다(W8).
- [x] §2.10.9 대조표 — 아래.

### 2-1 (2a 검수 넘어온 것)
- [x] W1 한 줄 · W2 삭제 · W3 글자 안 뜀 + 캐럿 · W4 저장 중 · W5 오류 걷기. W6 은 그대로다.

## §2.10.5 표 ↔ 코드(`stateMoves`) ↔ 테스트

| 지금 상태 | 활성 담당자 · 일반 | 활성 담당자 · 요청 | 요청자 · 요청 |
|---|---|---|---|
| 시작 전 | 진행 중 · 완료 · 업무 취소 ✓ | 진행 중 ✓ | — ✓ |
| 진행 중 | 막힘 · 완료 · 업무 취소 ✓ | 막힘 · 완료(→보고) ✓ | — ✓ |
| 막힘 | 진행 중 · 업무 취소 ✓ | 진행 중 · 완료(→보고) ✓ | — |
| 완료(최종) | 진행 중(재개) ✓ | — ✓ | 진행 중(재개) ✓ |
| 완료(확인 대기) | 글자 ✓ | 글자 ✓ | 글자 ✓ |
| 취소 | 없음 ✓ | 없음 | 없음 |

(✓ = `TaskDetailStateSelect.test.tsx` 의 행. 그 밖에 읽기 전용 입구·남의 업무는 셀렉트 없음.)

## SPEC §2.10.9 「지우는 것 — 전수」 1:1

| 지우는 것 | 판 | 지금 |
|---|---|---|
| 「업무 상세」 머리글 | 2a | 없음 |
| 상태 칩 | 2a/2b | 메타 정보 진행 상태 **셀렉트**(2b) |
| 버전 배지 | 2a | 메타 정보 버전 |
| 「편집」/「편집 끝내기」 | 2a | 인라인 즉시 저장 |
| 「AX」 | 2a | 없음 + 참고 자료 경로까지 삭제(2b W2) |
| 「마감일 초과」 | 2a | 마감일 값 옆 |
| `업무 메타` 한 줄 | 2a | 메타 정보 격자 |
| 「진행과 판단」 구역 제목 | **2b** | 없음 — 걸린 일 상자(있을 때만) |
| 「담당자 변경」 단추 | **2b** | 담당 셀렉트 |
| 막힘 사유 입력(본문 펼침) | **2b** | 작은 모달(`BlockReasonPrompt`) |
| 시작 막힘 배너 | 2a | 서버 문장 토스트(셀렉트 → 호출부 `onError`) |
| 푸터 — 업무 취소 | **2b** | 진행 상태 셀렉트 맨 아래 빨강 |
| 푸터 — 취소 제안 · 조건 변경 제안 | **2b** | `⋯` |
| 푸터 — 변경 저장 | 2a | 인라인 저장 |
| 푸터 — 막힘 · 시작 · 완료 처리 · 완료 보고 · 재개(둘) | **2b** | 진행 상태 셀렉트 |
| 푸터 — 선행 안내 문구(`scax-blocked-note`) | **2b** | 없음(상세만 · 목록 행 그대로) |
| 푸터 — 닫기 | **2b** | 머리 × |
| *지우지 않는 것* — 자료·이력·체크리스트·연관 업무·걸린 일 조건·명령·권한·서버 게이트 | — | 그대로 |

## grep 으로 센 자리 (`frontend/src`, 변경 후 — 테스트·test-utils 제외)

| 심볼 | 지금 | 바꾼 자리 / 유지한 자리(이유) |
|---|---|---|
| 푸터 단추 11종 | 상세 0 | 전부 지웠고 핸들러는 셀렉트·`⋯`·×로 옮겼다(위 표). `footer={` 8은 다른 모달이라 유지 |
| `isBlocking` | 3 | 상세 지움. 남은 3은 **목록 행 `TaskQuickActions`** 로 유지(W8) |
| `startBlocked` | 7 | 상세 지움. 남은 7은 `workRows.ts` 정의 + `TaskQuickActions` 로 유지(W8) |
| `scax-blocked-note` | 2 | 상세 지움. 목록 행 JSX 1 + 공용 CSS 1 로 유지(W8) |
| `hasProgressBlock` → `hasBlockers` | 0 → 2 | 이름·조건 바꿈(담당자 변경·막힘 입력 조건 빠짐) |
| `openHandover`·`handoverTargetError`·`handoverPending` | 0 | 지움 → `pickAssignee`·`submitHandover` |
| `<ReasonPrompt` | 9 | 상세 7(취소·제안·응답·재개·보완·**담당 변경 신규**) · `MyWorkPage` 1 · `AxDraftCard` 1. 부품에 `useEscape`·`error` 를 더했다 — 9곳 모두 Esc 가 그 모달만 닫는다 |
| `<BlockReasonPrompt` | 5 | 상세 1(**신규** — 본문 입력 대체) · `TaskQuickActions` · `TaskStateCell` · `ProjectTaskPanel` · `WorkViews` 는 그대로 |
| `<TermsChangePrompt` | 1 | 상세 `⋯` 에서. `useEscape` 를 더했다 |
| `<CompletionReportModal` | 4 | 상세(셀렉트 「완료」·요청) · `TaskQuickActions` · `TaskStateCell` · `ProjectTaskPanel`. 상세 쪽만 `version` 을 `versionRef` 와 맞춘다 |
| `<ConfirmModal` | 4 | 상세 「남은 단계」 그대로 |
| `stateTriggerTone` | 6 | `WorkModals` export(정의) · 상세 셀렉트 · `MyWorkPage TaskStateCell`(사본을 지우고 import) |
| `allowedTaskTransitions` | 12 | 손대지 않았다 — 목록 `TaskStateCell`·`TaskQuickActions`·칸반·`ProjectTaskPanel` 이 쓴다(회귀 통과) |
| `TaskStateCell` / `TaskStateValue` | 5 / 2 | 톤 표 import 만 바뀌었다 / 그대로 |
| `enqueue(` | 13 | 정의 1 + 인라인·전이·재개·담당·체크리스트 5 |
| `headerActions` | 6 | `Modal`·`Drawer` 렌더 · 타입 · 상세 1. 다른 표면은 안 넘긴다 |
| W2 지운 자리 | — | 아래 표 |

### W2 — 지운 자리 (`App.tsx` · `ChatDrawer.tsx`)

| 자리 | 처리 |
|---|---|
| `App.tsx` import `getMyWork`·`getWorkRequests` | 지움(App 안 다른 사용 0) |
| import `contextKey`·`LabeledContextReference`·`ConversationContextReference` | 지움 |
| state `contextOptions`·`selectedContextKey` · ref `contextGeneration` | 지움 |
| 페르소나 전환 초기화 2줄 | 지움 |
| `loadContextOptions` + AX 열 때 effect(실패 토스트 「현재 화면의 AX 참고 자료를 불러오지 못했습니다.」) + 선택 정리 effect | 지움 → 설명 주석 1개 |
| `sendMessage` 의 context | `chat.sendCurrent(body, [])` |
| `refreshProjections` 의 `loadContextOptions()` 항목 + 주석 | 지움 — 판단 뒤 stale 띠의 원인 하나가 사라졌다 |
| 렌더용 `selectedContext` · `onClearContext` · `selectedContext` prop · `stripLabel` | 지움 |
| `ChatDrawer.tsx` `LabeledContextReference`·`contextKey` export · props 2 · 「업무 · 제목」 칩 · `ConversationContextReference` import | 지움 |
| `ChatDrawer.test.tsx` props 2줄 | 지움 |
| `App.test.tsx` 「참고 자료 없이 간다(`context: []`)」 | **유지**(계약) |
| `onShellDownload` 수신부 | **손대지 않음** |
| 서버의 대화 context 계약 · `useConversations.sendCurrent(body, context)` 서명 | 유지 |

## 테스트 결과

- 기준선: 5 failed
- `npx vitest run --no-file-parallelism`(1회): **Test Files 2 failed | 83 passed (85) · Tests 5 failed | 1301 passed (1306)**
  - 실패 5 = 기준선 5(`CreateWork` 4 · `CreateWorkLayout` 1)이다. **새 실패 0.**
- `npx tsc --noEmit`: 0
- `make frontend-build`: 성공(기존 500kB 청크 경고만)
- WP 2b 검증 목록 ↔ 테스트

  | 계약 | 테스트 |
  |---|---|
  | 상태×역할 옵션 | `TaskDetailStateSelect` 15행 |
  | 사유 필수 모달(빈 사유 막음) | 막힘 `TaskCompletionFlow` · 취소 `TaskLifecycleV2` |
  | 완료 보고 모달 | `TaskCompletionFlow` · `TaskDelivery` |
  | 남은 단계 확인창(+돌아가기 무동작) | `Checklist` · `TaskDetailStateSelect` |
  | 409/거부 → 원래 값 | `Predecessors` — `onTransition` 거부 시 셀렉트가 「시작 전」이다. 토스트는 호출부 `onError` 경로로 기존 그대로다. |
  | `⋯` 요청자만(담당자·읽기 전용·대기 제안 없음) | `TaskDetailStateSelect` · `TaskLifecycleV2` |
  | 담당 셀렉트 권한·제안 중·Esc·바깥·실패 | `Checklist` 9건 |
  | 걸린 일 상자 각 조건·순서·없을 때 | `TaskDetailRelations` 2건 |
  | 푸터 없음 | 상태 5종 |
  | 「진행과 판단」 없음 | 여러 곳 |
  | 한 줄(저장 중 전이 대기 · version 이어받기 · 잠금 · 저장 중 표시) | `TaskDetailStateSelect` |
  | 캐럿 끝 · 같은 활자 클래스 | `TaskDetailStateSelect` |

- 회귀
  - 내 업무 목록 상태 칸(`TaskStateCell`)·`TaskQuickActions`·프로젝트 우 패널(`ProjectTaskPanel`)은 `src/features/work`·`src/features/project` 전부 통과다.
  - W5 의 호출부 한 줄은 별도 테스트를 두지 않았다. 기존 `MyWorkPage`·`TodayPage`·`Calendar` 테스트는 통과한다.

## DS-gaps
- **`⋯` 메뉴 시안·글리프가 없다.** 아이콘 세트에 「더보기」가 없어 `scax-icon-button` 안에 글자 「⋯」를 넣었다. 목록은 DS `Select` 팝오버다.
- **위험 항목 톤**: `SelectOption.tone:"danger"` 를 더했다(글자색만, `.popover-item.danger`). DS 에 그 갈래가 없었다.
- **걸린 일 상자 배치 시안이 없다.** 기존 `drawer-section.notice` 상자를 메타 정보 아래 grid(gap 10 · 위 16)로 쌓았다.
- **담당 셀렉트 트리거**: 목록 상태 칸과 같은 `scax-select__trigger--neutral` 을 썼다(사람 고르기 전용 시안이 없다).
- **「저장 중…」**: `scax-field__hint` 자리를 썼다(SPEC 에 모양이 없다).
- **업무 내용 여러 줄 인라인**: 여전히 `p` → `textarea` 갈아끼우기다. 상자를 미리 쥐어 글자가 뛰지 않게 맞췄지만 노드는 바뀐다.

## 미결
1. **`⋯` 와 읽기 전용**: SPEC 대로 `editable`(= `canManage && !closed && access!=="read_only"`)일 때만 선다. 서버가 요청자에게 `access:"read_only"` 를 주는 업무라면 요청자는 어느 입구에서도 `⋯` 를 못 본다. 지금 푸터도 같았다(SPEC §2.10.7 ⚠). 데모 DB 확인이 필요하다.
2. **담당 후보 조회 시점**: SPEC 은 「처음 열 때 한 번」인데 DS `Select` 에 「열림」 콜백이 없다. 그래서 **셀렉트가 설 때 한 번** 읽는다(`canAssign` 인 상세에서만).
3. **W6**(내 업무·홈 날짜 저장의 해제 문장)은 지시대로 그대로다.
4. 실제 브라우저 렌더 확인은 하지 않았다(서버·프론트 미기동 지시). 다음은 E2E·코디 데모 DB 확인 몫이다.
   - 셀렉트 폭 · `⋯` 위치 · 상자 간격 · 업무 내용 전환 시 상자 일치

---

## fix1 — 검수 WARN 처리 (`review-fe-p2b-report.md`)

| # | 처리 | 자리 |
|---|---|---|
| W1 | 업무 회차를 올리는 **나머지 명령을 같은 줄**(`enqueue`)에 세웠다. 아래 「W1 줄에 세운 명령」 참고. | `WorkModals.tsx` |
| W2 | 후보는 **상세를 연 동안 한 번만** 읽는다 · 「변경 제안 중」 이름은 `proposedNameOf` 로 찾는다. 아래 「W2 상세」 참고. | `WorkModals.tsx` |
| W3 | `styles/ax.css` 의 `.scax-chat__context*` 5규칙을 지웠다. 사용처는 0(남은 1건은 삭제를 적은 주석)이다. | `styles/ax.css` |
| W4 | **기록만 한다.** `⋯` 는 글자 글리프다(아이콘 세트에 「더보기」 없음). `SelectOption.tone:"danger"` 는 DS 밖 확장이다. 위 DS-gaps 그대로이고 고치지 않았다. | — |

### W1 줄에 세운 명령

| 명령 | 회차 |
|---|---|
| 제안 생성 `createTaskProposal` | `versionRef.current` |
| 제안 응답 `respondTaskProposal` | `versionRef.current` |
| 제안 철회 `withdrawTaskProposal` | `versionRef.current` |
| 자료 `uploadTaskMaterial` · `attachTaskMaterialLink` · `detachTaskMaterial` | — |
| 연결 편집 저장 | 칸 저장 전부 + 다시 읽기를 한 줄 항목으로 묶었다. 이 업무의 상위 패치는 `versionRef.current` 다. |
| 완료 보고 제출 | `CompletionReportModal` 에 선택 prop `inLine` 을 더했다. 상세가 `inLine={(job) => enqueue(() => job(versionRef.current))}` 를 넘기면, 보고는 **보낼 때** 줄이 준 회차로 나간다. 목록 행·프로젝트 패널은 안 넘기므로 예전 그대로다. |

- 결과: `current.version` 으로 명령을 보내는 자리가 상세에 **0**이다. 남은 `current.version` 은 버전 행 표시 1 · 모달 초기값 1 · `inLine` 이 없을 때의 대체 1 이다. `enqueue(` 는 21이다(정의 포함).
- 테스트
  - 「완료 보고 모달을 연 채 제목을 저장해도 — 보고는 저장이 끝난 뒤 그 응답의 version(4)으로 나간다」(저장 중에는 보고가 안 나감을 단언한다)
  - 「제안에 동의하는 명령도 마지막 응답의 version 을 싣는다」

### W2 상세
- **한 번만**: ref(`candidatesAsked`)가 «물었다» 를 든다. 셀렉트가 사라졌다 다시 서도, 첫 조회가 도중에 끊겨도 다시 묻지 않는다.
- **조회 조건**: `canAssign && editable` 이다 — 대기 제안이 있어 셀렉트가 없을 때도 읽는다(이름 찾기용).
- **이름 찾기**: 후보 목록 → `personas` 순서다. 담당 관계 응답은 id 만 싣는다(서버 `assignments.py:455-467`).
  - 못 찾으면 **날 id 대신** 기존 대체 문구 「새 담당 후보」다. 예전 `displayNameOf` 는 못 찾으면 id 를 그대로 냈다.
  - 사유 모달 설명의 이름도 같은 함수를 쓴다.
- 테스트
  - 「후보는 한 번만 읽고, 이름은 후보 목록에서 — personas 없는 화면에서도 『유나에게 변경 제안 중』」
  - 「못 찾으면 『새 담당 후보에게 변경 제안 중』이고 `task.assign` 없는 화면은 후보를 묻지 않는다」

### 검증
- 전체 `npx vitest run --no-file-parallelism`: **Test Files 2 failed | 83 passed (85) · Tests 5 failed | 1305 passed (1310)**
  - 실패 5 = 기준선 5 이다. 새 실패 0. 신규 4건(`TaskDetailStateSelect` 35).
- `npx tsc --noEmit`: 0

### fix1 변경 파일
`features/work/WorkModals.tsx` · `features/work/TaskDetailStateSelect.test.tsx` · `styles/ax.css`

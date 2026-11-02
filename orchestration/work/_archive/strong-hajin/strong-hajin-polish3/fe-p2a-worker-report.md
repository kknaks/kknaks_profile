# WORK-010 Phase 2a 결과 보고 (frontend)

## 상태: done

- 워크트리 `Strong_hajin/strong-hajin-polish3`. HEAD 는 `7f01c5b`(Phase 1 커밋)다.
- 커밋·push 하지 않았다.
- `lib/shell.ts`·`src-tauri/` 는 손대지 않았다.
- `App.tsx` 는 AX 정리 두 군데(`askAboutTask` 함수 · `onAskAboutTask` 전달)와 그 결과 안 쓰게 된 `DirectTask` import 만 고쳤다. 같은 파일의 다운로드 수신부(Phase 3)는 그대로다.

## 수행 내용

### 변경 파일

**제품 코드 8**

| 파일 | 무엇 |
|---|---|
| `features/work/WorkModals.tsx` | `TaskDetailDrawer` 를 개편했다 — 헤더 · 메타 정보 · 인라인 저장 · 배너 삭제 · 「변경 저장」 삭제 · `onAskAx` 삭제 |
| `ds/Modal.tsx` | `OverlayShellProps.title` 타입을 `string` → `ReactNode` 로 넓혔다. 업무 상세만 `InlineText` 를 넘기고, 글자를 넘기는 다른 표면은 렌더가 같다. |
| `ds/InlineText.tsx` | 편집 중 Esc 에 `stopPropagation` 을 더했다. 고치기 취소가 모달까지 닫지 않게 하려는 것이다. |
| `features/work/MyWorkPage.tsx` · `features/today/TodayPage.tsx` · `features/calendar/CalendarPage.tsx` | `onUpdate` 가 저장된 업무를 **돌려주고**, 실패는 **던진다**. 저장마다 성공 토스트를 띄우지 않는다(캘린더는 K3 해제 문장만 낸다). `onAskAboutTask` prop 은 지웠다. |
| `App.tsx` | `askAboutTask` 와 그 전달을 지웠다. |
| `lib/labels.ts` | `taskDetail` 키를 정확히 그 자리만 고쳤다. 더한 것: `blockMeta`·`metaState`·`metaVersion`·`metaOrigin`·`assigneeProposed`·`originAx`·`originOpenDecision`·`titleEdit`·`descriptionEdit`·`descriptionPlaceholder`·`inlineStale`·`inlineFailed`. 지운 것(쓰는 곳 0): `edit`·`editDone`·`ax`·`blockedHeading`·`blockedTitles`·`blockedTitlesSuffix`·`blockedHiddenSuffix`. |
| `styles/task-detail.css` | 옛 `.meta`/`.meta__*` 규칙을 지웠다(쓰는 곳 0). 머리 아래 간격, 메타 정보 격자, 제목 오류 자리, `desc--editable` 규칙을 더했다. |

**테스트 12**
- `TaskDetailDates.test.tsx`: 다시 썼다. 25건(헤더 3 · 격자 6 · 출처 3 · 인라인 저장 10 · 읽기 전용 3).
- `Checklist.test.tsx`: 6건 고침, +1건.
- `TaskDetailRelations.test.tsx`: 4건 고침.
- `MyWorkPage.test.tsx`: 1건 고침.
- `App.test.tsx`: 1건 고침.
- `CalendarInteractions.test.tsx`: +1건.
- 나머지 6파일(`CalendarPage`·`TodayPage`·`WorkTabsAndTables`·`WorkRowCompletion`·`WorkRequestModalFlow`·`InboxRead`)은 지운 prop `onAskAboutTask` 한 줄씩만 뺐다.

### 구현 요점

- **헤더**
  - `Shell` 은 모달일 때 모듈 자리의 `TaskDetailModalShell` 을 쓴다. 이것은 `Modal` + `className="scax-modal--task-detail"` 이다.
  - 그래서 렌더마다 새 부품이 되지 않고, 공용 `Modal` 의 시그니처도 그대로다(`className` 은 원래 받던 prop 이다).
  - `kicker`·`headerExtra` 를 넘기지 않는다.
  - `title`: 고칠 수 있으면 `<InlineText label="업무 제목">` 과 실패 시 `span.scax-field__error`, 아니면 글자다.
- **메타 정보**: 기존 공용 `dl.meta-grid`(dt/dd 2열, `components.css:527-531`)에 `.meta-info` 를 얹어 이 화면에서만 촘촘하게 했다(36px 행 · 13px).
  - 행 순서는 진행 상태 · 버전 · 담당(+「변경 제안 중」) · 시작 예정일 · 실제 시작일 · 실제 종료일 · 마감일(+「마감일 초과」) · 결재 · 참조 · 출처다.
  - 날짜 둘은 고칠 수 있으면 늘 서고 `DateField` 다. 읽기 전용이면 값이 있을 때만 선다.
- **인라인 저장**
  - `saveInline(field, patch)` 는 `saveQueue` 프라미스 체인으로 직렬화한다. `versionRef` 는 마지막으로 받은 회차를 든다 — 인라인 응답·체크리스트·자료(`moved`)·상세 다시 읽기를 모두 반영한다.
  - 성공하면 `moved(saved.version)` 하고, `detailTask` 에 title·description·start_date·due_date·version 을 합친다.
  - **422 stale**(`status===422` 또는 상태 없음 + 문장에 `stale`)이면 다시 보내지 않는다. `readDetail()` 로 서버 값을 세우고 칸 옆에 「다른 곳에서 바뀌어 최신 값으로 다시 불렀습니다.」를 낸다.
  - 그 밖의 실패는 칸 옆에 서버 문장을 낸다. 어느 실패든 던진다 → `InlineText` 가 원복하고, 날짜·내용은 `pending` 을 비워서 원복한다.
- **업무 내용**: 누르면 `textarea.desc` 다. 이 화면이 이미 가진 `.scax-td textarea.desc` 규칙이라 새 모양이 아니다. blur 저장 · Enter 줄바꿈 · Esc 취소(전파를 끊어 모달은 그대로). 칸 머리 `h5` 하나이고, 입력의 이름은 aria-label 이다.
- **R6**: `.scax-modal--task-detail .scax-modal__head{padding-bottom:var(--scax-space-300)}` · `.scax-modal--task-detail .scax-modal__body{padding-top:var(--scax-space-300)}` 다.
  - **41px → 25px**(12 + 선 1 + 12). 업무 상세 스코프만이다.
  - 첫 구역 `.block:first-child{margin-top:0}` 는 그대로 걸린다.

## 계약 체크 (WP 2a · SPEC §2.10)

### 2a-1 헤더
- [x] 머리 = (겹일 때) 뒤로 · 제목 · ×. kicker·ChipRow 를 지웠다. 상태·버전·마감일 초과는 메타 정보로 옮겼다.
- [x] 「AX」 단추를 지웠다. `onAskAx`(TaskDetailDrawer)·`onAskAboutTask`(호출부 3)·`askAboutTask`(App)까지 쓰는 곳이 0 이다. 대체 입구는 없다.
- [x] 제목은 클릭 인라인이고, 읽기 전용이면 글자다. 모달 `aria-label` 은 「업무 상세」 그대로다. 제목은 한 번만 보인다(테스트로 확인).
- [x] 공용 `Modal` 의 머리 규칙은 그대로다. 업무 상세 전용 className 을 쓴다. `title` 타입만 넓혔고, 13 표면 중 나머지 12는 string 을 넘겨 렌더가 같다.

### 2a-2 메타 정보
- [x] 「업무 정보」와 같은 계층의 구역 「메타 정보」(`.block`·`.block__row h3`)다. 2열 격자이고, 행 순서는 §2.10.2 그대로다.
- [x] 진행 상태는 `StatusText` 글자, 담당은 이름 글자다(셀렉트는 2b).
- [x] 시작 예정일·마감일은 `DateField` 이고 **고르는 즉시 저장**한다. 비어 있어도 선다. 예정 > 마감이면 보내지 않고 칸 옆에 「시작 예정일은 마감일보다 늦을 수 없습니다.」를 낸다.
- [x] 실제 시작일·실제 종료일·버전·결재·참조는 읽기 전용이다. 값이 없으면 서지 않는다(버전은 늘 선다).
- [x] 「마감일 초과」는 마감일 값 옆 danger 배지다. 머리에는 없다.
- [x] 출처 행
  - AX 제안은 「AX 제안 · **판단 보기**」, `onOpenSource` 가 없으면 「AX 제안」 글자만이다.
  - 요청·직접 배정은 지금 문구·링크 그대로다.
  - origin 이 없으면 행이 없다.
- [x] 업무 내용은 클릭 인라인 여러 줄이고 blur 저장한다. 칸 머리 「업무 내용」은 하나다.

### 2a-3 인라인 즉시 저장
- [x] `metaEditing`·「편집」/「편집 끝내기」·「변경 저장」·`dirty`·`save()`·`editingRef` 를 지웠다. 읽는 자리 6을 포함해 **0**이다.
- [x] 필드 하나 = PATCH 하나. 안 바뀌면 요청이 없다. **직렬 대기열**이고, 앞 응답의 `version` 을 다음 `expected_version` 으로 싣는다.
- [x] 성공하면 그 필드 값·버전을 갱신하고, 호출부 `reload` 를 재사용한다. **성공 토스트는 없다**(캘린더는 K3 해제가 있을 때만 그 문장).
- [x] 실패하면 원래 값 + 필드 옆 문장이다. 422 stale 은 다시 읽고 서버 값 + 필드 옆 「다른 곳에서 바뀌어…」이며 자동 재전송은 없다.
- [x] IME 조합 중 Enter 무시(제목, Phase 1 가드) · Esc 취소(제목·내용 모두 모달은 그대로).
  - 저장 중에는 보낸 값을 보여 준다(`InlineText` 의 `sent`, 날짜·내용의 `pending`).
  - 별도의 「저장 중」 표시는 두지 않았다 — 아래 미결.
- [x] 호출부 3곳의 `onUpdate` 는 `Promise<DirectTask>` 를 돌려주고, 실패는 던진다.
  - 형태: `onUpdate: (task, patch) => Promise<DirectTask | void>`. `void` 는 내 업무의 읽기 전용 no-op 이다.

### 2a-4 읽기 전용 · 배너 · 여백
- [x] `canManage=false`·`access=read_only`·`cancelled` 이면 제목·내용·날짜가 글자다. 빈 날짜 행은 서지 않는다(테스트 3 갈래).
- [x] 「시작할 수 없습니다」 배너를 지웠고 `blockedBanner` 도 지웠다. 쓰는 곳이 0 이 된 라벨 4개도 지웠다.
  - 「연관 업무」 선행 칸의 미완 배지는 그대로다.
  - 푸터 `scax-blocked-note`·목록 행 `TaskQuickActions` 는 **그대로**다(2b · W8).
- [x] 여백 41 → 25px, `.scax-modal--task-detail` 스코프만이다. 공용 `components.css:257,263` 은 그대로다.
- [x] 푸터는 그대로이고 「변경 저장」만 지웠다. 「진행과 판단」도 그대로다(2b).

### SPEC §2.10.9 — 이 페이지 몫 1:1

| 지우는 것 | 이 판 | 대신 |
|---|---|---|
| 「업무 상세」 머리글 | 지움 | 없음 |
| 상태 칩 | 지움 | 메타 정보 진행 상태(읽기 — 셀렉트는 2b) |
| 버전 배지 | 지움 | 메타 정보 버전 |
| 「편집」/「편집 끝내기」 | 지움 | 인라인 즉시 저장 |
| 「AX」 | 지움 | 없음 |
| 「마감일 초과」 배지 | 옮김 | 마감일 행 값 옆 |
| `업무 메타` 한 줄 | 지움 | 메타 정보 격자 |
| 시작 막힘 배너 | 지움 | (서버 문장 토스트는 2b 의 셀렉트 몫 — 지금 경로는 푸터 단추) |
| 푸터 중 「변경 저장」 | 지움 | 인라인 저장 |
| 「진행과 판단」·「담당자 변경」·막힘 사유 입력·나머지 푸터 | **2b** | — |

## grep 으로 센 자리 (`frontend/src`, 변경 후)

| 심볼 | 제품 코드 | 테스트 | 바꾼 자리 / 유지한 자리(이유) |
|---|---|---|---|
| `metaEditing` | 0 | 0 | 선언 1·읽는 자리 6 전부 지움 |
| `onAskAx`(업무) | 0 | 0 | `TaskDetailDrawer` prop·사용 지움. 남은 `onAskAx` 4는 **홈의 「AX에게 오늘 업무 묻기」**(`TodayPage.tsx:50,71,288` · `App.tsx:506`)로 다른 기능이라 유지 |
| `onAskAboutTask` | 0 | 0 | 호출부 3 prop·전달 지움, 테스트 9자리 prop 한 줄씩 뺌 |
| `askAboutTask` | 0 | 0 | `App.tsx` 함수 지움 |
| `AX에게 이 업무 묻기` | 0 | 5 | 테스트는 전부 「없다」 단언 |
| `blockedBanner`·`blockedHeading`·`blockedTitles` | 0 | 0 | 지움 |
| `scax-blocked-note` | 3 (JSX 2 + CSS 1) | 0 | **유지**(2b) |
| `meta__facts`·`meta__title-input`·`meta__edit`·`meta__left`·`.meta` | 0 | 0 | JSX·CSS 함께 지움 |
| `origin-chip` | 4 | 0 | 출처 `dd` 1(JSX) · 전역 CSS 1 · 새 스코프 CSS 2 |
| `scax-modal--task-detail` | 4 | 1 | 껍데기 1 · CSS 3 |
| `onUpdate=` 호출부 | 3 | — | 내 업무·홈·캘린더 전부 새 형태 |
| `updateTask(` 호출 | 화면 9 | — | 바꾼 것: 호출부 `onUpdate` 3. 유지: 캘린더 드롭·손잡이 `saveDates`(:272) 1 · 연결 편집 `saveRelations` 5 |
| 공용 `<Modal` 사용 | 8 | — | 머리·본문 규칙은 그대로다. 업무 상세만 modifier 를 얹는다. `title: ReactNode` 는 타입만 넓힌 것이다. |
| 바꾼 CSS 선택자 | — | — | **지움**: `.scax-td .meta` · `.meta h2` · `.meta__facts`(+`b`) · `.meta__facts + .origin-chip`(2) · `.meta__left` · `.meta__title-input` · `.meta__facts .date-field` · `.meta__edit`. **더함**: `.scax-modal--task-detail .scax-modal__head/__body/__title .scax-field__error` · `.scax-td .meta-info`(+`> div`·`dt`·`dd`·`dd:has(> .scax-badge)`·`.date-field`·`.select-trigger`·`.origin-chip`) · `.meta-info__value` · `.desc--editable`. 공용 `.meta-grid` 는 그대로다. |

## 테스트 결과

- 기준선: 5 failed (1232 중)
- `npx vitest run --no-file-parallelism`(1회): **Test Files 2 failed | 82 passed (84) · Tests 5 failed | 1269 passed (1274)**
  - 실패 5 = 기준선 5(`CreateWork` 4 · `CreateWorkLayout` 1)이다. **새 실패 0.**
  - 이 수에는 같은 워크트리에서 진행 중인 Phase 3 테스트도 함께 들었다.
- `npx tsc --noEmit`: 0
- `make frontend-build`: 성공(기존 500kB 청크 경고만)
- WP 2a 검증 목록 ↔ 테스트

  | 계약 | 테스트 |
  |---|---|
  | 헤더에 kicker·상태·버전·편집·AX 없음 · 제목 한 번 | `TaskDetailDates` 헤더 · `TaskDetailRelations` · `App.test` |
  | 안 바뀜 = 요청 없음 | 날짜 · 제목 · 내용 |
  | 직렬 · version 이어받기 | 「두 칸을 연달아」 · `Checklist` 「saves with the version the server just answered」(체크리스트 직후 제목) |
  | 422 → 다시 읽기 + 서버 값 + 칸 옆 문장 | `TaskDetailDates` |
  | 날짜 즉시 저장 · 뒤집힘 막음 | `TaskDetailDates` |
  | 읽기 전용 입구 3 갈래 | `TaskDetailDates` |
  | 배너 없음 | `TaskDetailRelations` 2건 |
  | 출처 「판단 보기」/글자만 | `TaskDetailDates` · `Checklist` |
  | 마감일 초과 배지 자리 | `TaskDetailDates` |
  | K3 해제 문장 회귀(캘린더 상세) | `CalendarInteractions` |

- 회귀: `ProjectTaskPanel`(공용 `StatusText`·`Badge`·`allowedTaskTransitions`)는 손대지 않았다. `src/features/project` 전체 통과.

## 다른 팀 영향
- BE: 없다. 기존 `PATCH /api/tasks/{id}` 에 한 칸 + `expected_version` 만 보낸다.

## DS-gaps
- **메타 정보 2열 격자 시안이 없다.** 기존 `.meta-grid`(dt/dd) + 화면 스코프 촘촘함으로 짰다.
- **업무 내용 「그 자리 여러 줄」 부품이 DS 에 없다.** `InlineText` 는 한 줄 계약(Enter = 저장, 줄바꿈 걷음)이다. 그래서 이 화면이 이미 가진 `textarea.desc` 규칙으로 갈아끼운다 — 누르면 textarea 가 선다(노드가 바뀌어 글자가 약간 움직일 수 있다).
- **제목 오류 자리 시안이 없다.** 머리 `h3` 안에 `scax-field__error` span 을 넣었다.
- `InlineText` 시안(previews)은 여전히 없다(Phase 1 과 같다).

## 미결
1. **AX 참고 자료 경로가 죽었다**(`App.tsx`).
   - `askAboutTask` 가 `setSelectedContextKey(키)` 의 유일한 호출부였다. 그래서 채팅 입력 위 「업무 · 제목」 칩(`ChatDrawer.tsx` `selectedContext`)은 이제 설 길이 없다.
   - 그런데 `contextOptions`·`loadContextOptions`(AX 를 열면 `getMyWork()`·`getWorkRequests()` 를 부른다)·`LabeledContextReference.pinned` 는 남아 있다. 보내기도 `selectedContext` 가 늘 없으니 빈 context 로 간다(App.test 로 고정).
   - 이번 지시가 `App.tsx` 를 「AX 단추 삭제에 따른 정리만」으로 묶어 **지우지 않았다.** 쓸모없는 조회를 걷을지는 코디가 판단한다.
2. **저장 중 표시**: 보낸 값을 바로 보여 주는 것 말고 「저장 중」 글자·스피너는 두지 않았다(SPEC §2.10.4 에 모양이 없다). 필요하면 2b 와 함께 정한다.
3. **2b 몫으로 남은 것**: 푸터 전부(시작·막힘·완료 처리·업무 취소·제안·재개·닫기·`scax-blocked-note`) · 「진행과 판단」 · 진행 상태/담당 셀렉트 · `⋯` · 목록 행 `TaskQuickActions` 문구.
4. 실제 브라우저 렌더(격자 폭·날짜 칸 180px·25px 간격·textarea 전환 시 글자 움직임)는 확인하지 않았다(서버·프론트 미기동 지시). E2E 몫이다.

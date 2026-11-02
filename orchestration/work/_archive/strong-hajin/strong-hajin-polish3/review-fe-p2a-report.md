# 리뷰 리포트 — strong-hajin-polish3 / frontend · WORK-010 Phase 2a (2026-10-04)

## 판정: WARN

FAIL 0 · WARN 6. WP Phase 2a 체크박스 **19개 중 18 PASS · 1 부분(저장 중 표시)** 이다.

**인라인 저장은 맞게 직렬이다.**
- 대기열이 `run` 이 **실행되는 순간** `versionRef` 를 읽는다. 그래서 두 칸을 빠르게 연달아 고쳐도 뒤 요청이 앞 응답의 회차를 싣는다(지연 프라미스로 검증하는 테스트 있음).
- 422 stale → 다시 읽고 서버 값 · 실패 원복 · 안 바뀜 = 요청 없음 · 호출부 3곳이 저장된 업무를 돌려줌, 모두 확인했다.
- 헤더의 머리글·상태·버전·편집·AX 와 AX 심볼(`askAboutTask`·`onAskAboutTask`)은 0건이다.
- 공용 `Modal`(title 타입만 넓힘)·`InlineText`(Esc 전파 끊기) 변경은 다른 사용처를 깨지 않는다.
- 2b 몫(푸터 상태 단추·「진행과 판단」·`scax-blocked-note`·목록 행)은 그대로다. 「변경 저장」만 사라졌다.
- 전체 스위트(직렬)는 실패 5 = 기준선 5, 새 실패 0이다.

WARN 은 다음 세 종류다.
- 대기열 밖 명령과의 회차 경합(2b 에서 닫을 것)
- 죽은 AX 참고 자료 경로가 **아직 네트워크를 부르고 오류를 낼 수 있다**
- 눈에 보이는 거친 자리 몇 곳

## 검수 범위

- 대상: 워크트리 `Strong_hajin/strong-hajin-polish3`, HEAD `7f01c5b`(Phase 1) 이후의 미커밋 diff 중 Phase 2a 파일
  - 제품 코드: `features/work/WorkModals.tsx`(diff 740줄) · `MyWorkPage.tsx` · `today/TodayPage.tsx` · `calendar/CalendarPage.tsx` · `ds/Modal.tsx` · `ds/InlineText.tsx` · `App.tsx`(AX 정리만) · `lib/labels.ts`(`taskDetail` 만) · `styles/task-detail.css`
  - 테스트 12 파일
  - 제외: Phase 3 의 `src-tauri/`·`lib/shell.ts`·App 다운로드 수신부·`shellDownload`
- 기준: SPEC-007 v0.5.1 §2.10.1 · §2.10.2 · §2.10.4 · §2.10.7 · §2.10.8 · §2.10.9 · §6 「고도화 3차」 · WP Phase 2a · `fe-p2a-worker-report.md` · fe-survey §4~§6 · be-survey §4
- 실행한 검사
  - `npx vitest run --no-file-parallelism`(전체) → **Test Files 2 failed | 82 passed · Tests 5 failed | 1269 passed (1274)**. 실패 5 = 기준선(`CreateWork` 4 · `CreateWorkLayout` 1, 날짜 의존)
  - 테스트 변경: 파일마다 지운 `it` 과 더한 `it` 을 대조했다(아래 「조용히 통과하는 자리」)
  - grep 직접 재계수
    - `<TaskDetailDrawer` 3
    - `onUpdate=` 3
    - `<Modal` 8 · `<Drawer` 2
    - `<InlineText` 4(업무 1 · 회의 제목 1 · 안건 2)
    - 화면의 `updateTask(` 9
    - `askAboutTask|onAskAboutTask|metaEditing|blockedBanner|blockedHeading` 0
    - `scax-blocked-note` JSX 2 + CSS 1
    - `onAskAx` 는 홈 「AX에게 오늘 업무 묻기」 4자리만 남는다(다른 기능)

    **워커 표와 모두 같다.**
  - `useEscape` 가 window 의 **버블** 단계 리스너인지 확인했다(`ds/Modal.tsx:24-39`). 그래서 React 의 `stopPropagation` 이 겹 닫기를 실제로 막는다.

## 위반 (FAIL 사유)

없음.

## 경미 (WARN)

- **W1 · 대기열 밖 명령과의 회차 경합** `WorkModals.tsx` `saveInline`(diff `+1085~1130`) · 호출부 3곳 `setBusy` 제거
  - 인라인 저장끼리는 직렬이다. 하지만 **푸터 전이·체크리스트·자료·연결 편집**은 그 줄 밖에서 `current.version`(=`settledVersion`)으로 나간다.
  - 호출부가 인라인 저장 중 `setBusy(true)` 를 더 이상 걸지 않아, 저장이 도는 동안에도 푸터 단추가 눌린다.
  - 결과: 제목을 저장하는 사이 「시작」을 누르면 둘 중 하나가 422 가 된다. 전이 쪽 422 는 전역 오류 띠로 뜬다.
  - SPEC §2.10.4 「회차의 원천」(인라인·전이·담당 제안이 같은 줄, **(제안)**)과 §5 동시성 줄이 이 자리다. 푸터가 셀렉트로 바뀌는 **2b 에서 같은 대기열로 묶어야 한다** — 코디가 2b 브리프에 명시하기를 권한다.
- **W2 · 죽은 AX 참고 자료 경로가 살아서 일한다** `App.tsx` — 브리프 §3-8 판정
  - **정말 죽었다.** `setSelectedContextKey(키)` 를 비어 있지 않은 값으로 부르는 곳이 **0**이다(남은 호출은 초기화 `:242` · 정리 effect `:313` · 칩 떼기 `:671`). `contextOptions` 를 고르는 UI 도 없다 — ChatDrawer 에 넘기는 것은 `selectedContext` 하나다. 그래서 `selectedContext` 는 늘 `undefined` 다.
  - **그런데 일은 계속한다.**
    - AX 를 열 때마다 `loadContextOptions` 가 `getMyWork()`·`getWorkRequests()` 를 부른다(`:280-309`).
    - 판단을 내릴 때마다 `refreshProjections`(`:337-346`)도 그것을 부른다.
    - 실패하면 **「현재 화면의 AX 참고 자료를 불러오지 못했습니다.」 오류 토스트**(`:304`)가 뜬다.
    - 판단 뒤 갱신에서는 **「판단은 저장되었지만 화면을 갱신하지 못했습니다.」 stale 띠**(`:344`)까지 뜬다.

    없는 기능 때문에 사용자가 오류를 볼 수 있다.
  - **지울 범위**(2b 에서 정리할지는 코디가 정한다)
    - `App.tsx:17` — `contextKey`·`LabeledContextReference` import
    - `App.tsx:165-166` — `contextOptions`·`selectedContextKey` state
    - `App.tsx:184` — `contextGeneration`
    - `App.tsx:241-242` — 페르소나 전환 초기화
    - `App.tsx:278-315` — `loadContextOptions` + 두 effect
    - `App.tsx:326-328` — `sendMessage` 를 `chat.sendCurrent(body, [])` 로
    - `App.tsx:340` — `refreshProjections` 의 `loadContextOptions()` 항목. 주석의 「AX context candidates」도 함께
    - `App.tsx:381` — `selectedContext`
    - `App.tsx:671` — `onClearContext`
    - `App.tsx:755` — `selectedContext` prop
    - `App.tsx:764-767` — `stripLabel`
    - `getMyWork`·`getWorkRequests` import(App 안의 다른 사용이 없으면)
    - `features/chat/ChatDrawer.tsx:13,16` — `LabeledContextReference`·`contextKey`(다른 사용 0)
    - `ChatDrawer.tsx:103,105,135,137` — props
    - `ChatDrawer.tsx:341-352` — 「업무 · 제목」 칩
    - `ChatDrawer.test.tsx` 의 칩 시험
    - `App.test.tsx` 의 `context: []` 단언은 남긴다(계약 「참고 자료 없이 간다」)
    - 서버의 대화 context 계약은 건드리지 않는다
- **W3 · 업무 내용 편집이 노드를 갈아끼운다** `WorkModals.tsx`(diff `+2160~2200`)
  - 누르면 `p.desc` 가 `textarea.desc` 로 바뀐다. textarea 는 테두리 1px + 안여백 8·10px 이라 **글자가 그만큼 오른쪽·아래로 뛴다.**
  - `autoFocus` 로 열리므로 캐럿이 누른 자리가 아니라 **글 맨 앞**(WebKit 기본)에 선다.
  - SPEC §2.10.4 는 「인라인 여러 줄」만 정했고, InlineText 의 「글자가 안 움직인다」 계약은 한 줄 부품의 것이다. 워커가 DS-gaps 로 보고했다. **위반은 아니고 실물 자리다.**
- **W4 · 저장 중 표시가 없다** — WP 2a-3 「저장 중 표시·포커스 이동·IME」 체크박스 중 「저장 중 표시」만 비었다(워커 미결 2).
  - 보낸 값을 바로 보여 주므로 화면은 「이미 저장됨」처럼 보인다.
  - 실패하면 값이 되돌아가고 칸 옆 문장이 뜬다. 422 로 다시 읽을 때는 1~2초 동안 보낸 값 → 서버 값으로 바뀐다.
  - SPEC 이 모양을 정하지 않았다. 코디 결정 사항이다(지금 상태로 받을지, 2b 에서 정할지).
- **W5 · 성공 시 전역 오류를 걷지 않는다** `MyWorkPage.tsx:524-532` · `TodayPage.tsx:229-238` · `CalendarPage.tsx:593-605`
  - 예전 `updateTaskFields` 는 성공하면 `settleError()`/`onError(null)` 로 남아 있던 전역 오류를 걷었다. 새 함수는 걷지 않는다.
  - 앞선 다른 조작의 오류 띠가 인라인 저장이 성공한 뒤에도 남는다. 공통 토스트는 4초 자동 닫힘이라 대개 사라지지만, `persist` 오류는 남는다.
  - 권장: 성공 갈래에 한 줄을 다시 넣는다.
- **W6 · 내 업무·홈에서 날짜 저장의 K3 문장이 없다** `MyWorkPage.tsx:524` · `TodayPage.tsx:229`
  - 날짜가 시간 배정을 닫아도 「N건의 시간 배정이 기간 밖이라 해제되었습니다.」는 **캘린더 상세에서만** 뜬다.
  - 예전에도 이 두 호출부는 이 문장을 내지 않았다(`git show HEAD` 확인). 그래서 회귀는 아니다.
  - SPEC §2.10.4 「지금처럼」 · AC 「그대로 뜬다(회귀)」와는 맞다. 다만 인라인 날짜 저장이 쉬워져 내 업무에서 날짜를 고칠 일이 늘었으니, 같은 문장을 내는 것이 자연스럽다. 코디 판단으로 남긴다.

## WP 체크박스 · SPEC 절 판정

**2a-1 헤더 (§2.10.1)**

| 계약 | 판정 | 근거 |
|---|---|---|
| 머리 = (겹일 때) 뒤로 · 제목 · × — kicker·ChipRow 삭제 | PASS | `kicker`·`headerExtra` 를 넘기지 않는다. 「뒤로」는 공용 `Modal` 의 `onBack` 그대로다(OQ-711). 테스트 `TaskDetailDates` 「제목 · × 만 선다」 |
| AX 단추 삭제 · `onAskAx`/`onAskAboutTask`/`askAboutTask` 0 | PASS | grep 0. `App.test.tsx` 의 AX 시험을 지우지 않고 「단추 없음 + `context: []`」로 **뒤집었다** |
| 제목 클릭 인라인 · 읽기 전용이면 글자 · `aria-label` 「업무 상세」 유지 | PASS | `title={editable ? <InlineText/> + 오류 span : shown.title}`, `label="업무 상세"` 그대로. 테스트 「고칠 수 없는 입구에서는 제목이 글자뿐」 |
| 공용 `Modal` 의 다른 12 표면 불변 | PASS | `TaskDetailModalShell` 은 모듈 자리에 있다(렌더마다 재마운트 없음). 기존 `className` prop 으로 `scax-modal--task-detail` 만 얹는다. `title: ReactNode` 는 타입만 넓혔다 — 7개 다른 `<Modal>`·2개 `<Drawer>` 는 string 을 넘겨 같은 `<h3>{title}</h3>` 이고, `ActionCenter` 의 `Shell` 타입도 호환된다 |

**2a-2 메타 정보 (§2.10.2 · §2.10.8)**

| 계약 | 판정 | 근거 |
|---|---|---|
| 「업무 정보」와 같은 계층 · 2열 격자 · 행 순서 | PASS | `section.block` + `h3` 「메타 정보」 · `dl.meta-grid.meta-info`. 순서: 진행 상태 → 버전 → 담당 → 시작 예정일 → 실제 시작일 → 실제 종료일 → 마감일 → 결재 → 참조 → 출처. 테스트 「행 순서」·「결재·참조·출처 순서」 |
| 진행 상태·담당 = 읽기 글자(셀렉트는 2b) | PASS | `StatusText` · `ownerName`. 「변경 제안 중」 배지는 `assignments?.pending` |
| 날짜 = `DateField` 즉시 저장 · 비어도 선다 · 예정 > 마감 막음 | PASS | `saveDate`. 비교는 상대 칸의 `pending` 값까지 본다. 테스트 3건 |
| 실제 두 값·버전·결재·참조 읽기 전용 · 빈 행 규칙 | PASS | 고칠 수 없는 화면은 `(editable || 값)` 조건, 버전은 늘 선다 |
| 「마감일 초과」 = 마감일 값 옆 danger | PASS | `.meta-info__value` 안 · 테스트 「머리에는 없다」 |
| 출처 「AX 제안 · 판단 보기」 / `onOpenSource` 없으면 「AX 제안」 글자 / 요청·배정 그대로 / 없으면 행 없음 | PASS | `source.type==="action_item"` 갈래. 링크에 `canLeave()` 를 유지한다. 테스트 3 + `Checklist` 2 |
| 업무 내용 클릭 인라인 여러 줄 · blur 저장 · 칸 머리 하나 | PASS(W3) | `textarea` aria-label 「업무 내용 고치기」, `h5` 하나. 테스트 「Enter 는 줄바꿈 · Esc 취소」 |

**2a-3 인라인 즉시 저장 (§2.10.4)**

| 계약 | 판정 | 근거 |
|---|---|---|
| 편집 모드 폐지 — `metaEditing`·편집 단추·「변경 저장」·`dirty` 0 | PASS | grep 0 · diff 에서 푸터 「변경 저장」 블록만 삭제 |
| 한 칸 = 저장 하나 · 안 바뀜 요청 없음 · 직렬 · 앞 응답 version | PASS | `saveQueue.current.then(run, run)`. `run` 안에서 `versionRef.current` 를 읽는다. 성공 시 `moved(saved.version)` 이 ref 를 동기로 올린다. 실패해도 줄은 이어진다(`next.catch`). 테스트 「두 칸을 연달아」는 첫 응답을 붙잡아 둔 동안 둘째가 안 나가고, 이어서 v1 → v2 를 확인한다 |
| 성공: 값·버전 갱신 · 호출부 reload 재사용 · 저장마다 토스트 없음 | PASS(W5·W6) | `setDetailTask` 에 네 칸 + version 을 합친다. 호출부는 `reload()` 후 `saved` 를 돌려준다. 다시 읽기 실패는 삼킨다 |
| 실패 원복 + 칸 옆 · 422 → 다시 읽기 + 서버 값 + 「다른 곳에서 바뀌어…」 · 자동 재전송 없음 | PASS | `isStaleVersion`(422 또는 상태 없음 + `stale`) → `readDetail()`(이 안에서 `moved`) → `fieldErrors`. 테스트가 v5·2026/10/25 서버 값과 `onUpdate` 1회를 확인한다 |
| 저장 중 표시 · 포커스 · IME | **부분** | IME(제목은 Phase 1 가드) · Esc 취소(모달 유지)는 PASS. 저장 중 표시 없음(W4) |
| 호출부 3곳이 새 version 을 돌려준다 | PASS | `onUpdate: (task, patch) => Promise<DirectTask \| void>`. 내 업무 `:525` · 홈 `:231` · 캘린더 `:594` 가 `updateTask` 응답을 그대로 돌려준다. 내 업무 읽기 전용 입구는 no-op |

**2a-4 읽기 전용 · 배너 · 여백 (§2.10.7 · R5 · R6)**

| 계약 | 판정 | 근거 |
|---|---|---|
| `canManage=false`·`read_only`·`cancelled` → 글자만 | PASS | `editable = canManage && !closed && !readOnly` 한 값이 제목·내용·날짜를 모두 가른다. 입구 16곳 중 10곳은 `canManage=false` 로 연다(호출부 변경 없음 — `MyWorkPage.tsx:1316` `detail.manage`). 테스트는 세 갈래를 `it.each` 로 다룬다 |
| 「시작할 수 없습니다」 배너 삭제 · 심볼 정리 · 선행 배지 유지 · 푸터 문구·목록 행은 2b | PASS | `blockedBanner`·라벨 4 삭제 · `scax-blocked-note` 2곳(`:1924` 푸터 · `:3623` 목록 행) 유지 · 테스트를 「배너 없음」으로 뒤집음 |
| 여백 41 → 25px · 업무 상세 스코프만 | PASS | `.scax-modal--task-detail .scax-modal__head/__body` 만 바뀌었다. `components.css:257,263` 은 diff 0 |
| (2b 경계) 푸터·「진행과 판단」 그대로, 「변경 저장」만 삭제 | PASS | 시작·막힘·완료 처리·완료 보고·재개·업무 취소·제안 단추와 `blockProgress` 구획이 그대로다 |

**검증**

| 계약 | 판정 | 근거 |
|---|---|---|
| frontend-test(직렬)·tsc·build | PASS(test 직접 · tsc/build 는 워커 수치 인용) | 위 |
| 계약별 테스트 | PASS | 헤더 3 · 격자 6 · 출처 3(+Checklist 2) · 인라인 10 · 읽기 전용 3 · K3 회귀(캘린더) 1 |
| 공용 부품·라벨 회귀(`ProjectTaskPanel` 등) | PASS | `StatusText`·`Badge`·`allowedTaskTransitions` 는 diff 0. 전체 스위트 통과 |

## 공용 부품 변경 (브리프 §3-9)

- **`ds/Modal.tsx` `title: string → ReactNode`**: 렌더는 `<h3>{title}</h3>` 그대로다(Modal `:171` · Drawer `:115`). string 을 넘기는 다른 표면은 바이트 단위로 같고 타입도 호환된다. **안전.**
- **`ds/InlineText.tsx` Esc `stopPropagation`**: 편집 중 Esc 에서만 끊는다. 닫힌 칸의 Esc 는 그대로 겹으로 간다.
  - 다른 사용처 셋(회의 제목 1 · 안건 제목 · 메모 줄)에서는 Esc 가 바깥 겹(드로어 등)을 닫지 않게 될 뿐이다. 개선이고 회귀가 아니다.
  - `MeetingLive`·`MeetingTitle` 시험이 전체 스위트에서 통과했다.

## 조용히 통과하는 자리 점검

- 지운 `it` 은 모두 **같은 계약을 뒤집은 `it` 으로 바뀌었다.** 「없다」가 된 계약을 그냥 지운 곳은 없다.

  | 파일 | 바뀐 것 |
  |---|---|
  | `App.test` | AX 첨부 → 「단추 없음 + context []」 |
  | `TaskDetailRelations` | 「AX 그대로」 → 「없다」 · 「배너가 갈려 선다」 → 「배너 없음, 완료 막힘 그대로」 |
  | `Checklist` | 「편집 전 글자」 → 「눌러서 여러 줄」 · 출처 칩 → 「AX 제안 · 판단 보기」 |
  | `TaskDetailDates` | 「사실 줄 날짜 넷」 → 격자 순서 · 「편집」 → 「없다」 |

- 직렬 시험은 지연 프라미스로 첫 응답을 붙잡아 둔 동안의 호출 수를 확인한다. 빈 단언이 아니다.
- 422 시험은 화면 값(2026/10/25)과 버전 행(v5)으로 서버 값이 섰음을 확인한다.
- `isStaleVersion` 의 「상태 없음 + 문장」 폴백은 테스트 목 때문이다(주석에 적혀 있다). 실제 `ApiError` 는 `status` 를 실으므로 영향이 없다.

## 사용자가 실물에서 만날 자리

1. **업무 내용을 누르면 글자가 뛴다**(W3). 테두리 상자가 나타나고 글자가 몇 px 옮겨 가며, 캐럿은 글 맨 앞에 선다.
2. **저장 중 표시가 없다**(W4). 저장이 실패하면 값이 되돌아가며 칸 아래 빨간 문장이 뜬다. 다른 곳에서 바뀐 업무는 보낸 값이 잠깐 섰다가 서버 값으로 바뀐다.
3. **성공 토스트가 사라졌다** — 예전 「업무 내용을 저장했습니다.」가 없다. 제대로 됐는지는 버전 행이 +1 된 것으로만 보인다.
4. **메타 정보가 테두리 있는 카드다** — `.meta-grid` 의 1px 테두리·둥근 모서리 12. 아래 「업무 정보」·「연관 업무」 블록과 모양이 다르다.
5. **날짜 칸 폭 180px · 높이 30px** — 행 높이 36px 안에서 DateField 트리거가 꽉 찰 수 있다.
6. **제목이 길면 머리에서 여러 줄로 접힌다.** 모달 제목에 말줄임 규칙이 없고, InlineText 는 `pre-wrap` 이다.
7. **제목 저장 실패 문장이 머리 안 제목 바로 아래**에 선다(작은 빨간 글자). 시안이 없는 자리다.
8. **저장하는 동안에도 푸터 「시작」 등이 눌린다**(W1). 연달아 누르면 전역 오류 띠가 뜰 수 있다.
9. **AX 를 열거나 판단을 내릴 때** 쓰지도 않는 참고 자료 목록을 부른다. 망이 흔들리면 「현재 화면의 AX 참고 자료를 불러오지 못했습니다.」 토스트가 뜬다(W2).
10. **「AX에게 이 업무 묻기」가 사라졌다** — 업무 상세에서 AX 로 가는 길이 없다(결정 d). 홈의 「AX에게 오늘 업무 묻기」는 그대로다.
11. **머리 아래가 좁아졌다**(41 → 25px). 업무 상세만이고 다른 모달은 그대로다.

## 기존 부채 (이번 판정 제외)

- 내 업무·홈의 날짜 저장에 K3 문장이 원래 없었다(W6 에 같이 적음).
- 목록 다시 읽기(`reload`)가 열린 상세의 `task` prop 을 목록 투영으로 바꾸는 구조는 그대로다. 화면은 `detailTask` 를 우선해서 값은 맞다.

## 확인한 것 (PASS 근거)

- allowed_paths: 리포트 한 장만 썼다. 코드 수정 0.
- `WorkModals.tsx` diff 전체 · 호출부 3 · 공용 부품 2 · App AX 정리 · CSS · labels 를 정독했다.
- 전체 vitest 를 직렬로 1회 돌렸다(새 실패 0).
- grep 재계수가 워커 표와 일치한다.
- 죽은 경로를 판정하고 지울 범위를 파일:줄로 적었다.

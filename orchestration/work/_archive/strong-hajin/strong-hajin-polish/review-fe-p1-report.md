# 리뷰 리포트 — strong-hajin-polish / frontend Phase 1 (2026-10-01)

## 판정: WARN

- 계약과 다르게 도는 곳(FAIL)은 **없다**. B-02 · F-01 · F-02 · F-03 · D-01의 WP 체크박스가 모두 코드로 맞는다.
- 바뀐 동작마다 경계를 실제로 무는 테스트가 있다.
- WARN은 넷이다. 남은 옛 주석·죽은 분기 둘, 실패 문구 자리 하나, F-02 테스트의 성격 하나다. 모두 동작이 아니라 읽는 사람이 헷갈릴 자리다.

## 검수 범위

- diff: 코드 워크트리 `strong-hajin-polish`의 미커밋 변경 14파일과 신규 2개(`frontend/src/lib/weekWindow.ts` · `.test.ts`). `backend/` · `src-tauri/` 변경은 0이다. allowed_paths(`frontend/src/`)를 벗어난 변경은 없다.
- 기준: WORK-008 Phase 1(1-1~1-5) · P-2 · P-3 / SPEC-001 U-6-a · U-16 / SPEC-005 §2.4 / SPEC-007 §2.9 / `strong-hajin-polish-fe-p1-brief.md`
- 실행한 검사
  - `git diff` 정독
  - P-3 재계수 grep: `<CreateWorkModal` · `assigneeId` · `type="search"` · `.search-input-box` 계열 · 범위 계산 · `fetch(` · 하드코딩 색·px
  - 바뀐 테스트 7파일을 **직렬** 실행: `npx vitest run --no-file-parallelism <7파일>` → 231 중 227 통과, **4 실패**
    - 실패 넷은 모두 `CreateWork.test.tsx`의 「업무/요청 갈래의 시작일…」이다
    - `flaky-baseline-evidence.md`가 기록한 **기준선 날짜 의존 실패**(오늘이 10월이라 09-xx 달력 칸이 없다)와 같다
    - 이번 diff는 그 4개 테스트를 건드리지 않았다
    - 기준선 다섯째(CreateWorkLayout)는 이번에 돌린 파일이 아니다
  - tsc · build는 다시 돌리지 않았다. 워커 보고(tsc 0 · build 성공)를 그대로 옮긴다.

## 1. 계약 충실도 — 체크박스별

### 1-1 B-02 참조자 후보 (SPEC-001 U-6-a)

| 계약 | 결과 | 근거 |
|---|---|---|
| 내 업무 갈래의 담당 = 본인, 숨은 담당 후보 값 없음 | **PASS** | `WorkModals.tsx:4430` `useState(initial?.assigneeId ?? "")` 로 첫 후보 자동 선택을 없앴다. `:5014` `requestAssigneeId = kind === "request" ? assigneeId : ""` 이라 `업무` 갈래는 담당 값을 읽지 않는다. 업무 갈래 제출은 `assignee_id`를 싣지 않는다(테스트 `CreateWork.test.tsx` 「숨은 담당 값이 실려 나가지 않는다」 `body.assignee_id` undefined) |
| 요청 갈래 담당은 빈칸 시작, 필수 검사는 기존 그대로 | **PASS** | `:4430` · 필수 검사 `:4691` 그대로. 테스트 「담당자를 고르지 않으면 기존 필수 검사가 막는다」 |
| 처음 열면 두 갈래 모두 참조자 전원(본인 제외) | **PASS** | `:5281` 필터가 `requestAssigneeId` 기준. 테스트 두 갈래 각각 `["지호","소라","유나"]` |
| 요청에서 고른 사람만 빠지고, 바꾸면 이전 사람이 돌아옴 | **PASS** | `:5281`. 테스트 「고른 담당자만 … 바꾸면 이전 사람이 돌아온다」 |
| 참조자로 체크한 사람을 담당으로 고르면 체크 해제 | **PASS** | `:5233-5237` `setCcIds(current.filter(id !== next))`. 테스트가 제출 payload `cc_member_ids: ["yuna"]`까지 단언한다 |
| `initial` 자리 불변 | **PASS** | 옛 식 `initial ? initial.assigneeId ?? "" : 첫 후보`와 새 식 `initial?.assigneeId ?? ""`는 `initial`이 있을 때 **같은 값**이다. 그러니 바뀌는 것은 `initial` 없는 자리뿐이다. 다섯 자리 중 `initial` 있는 셋(하위 업무 `WorkModals.tsx:2997`, 다시 요청 `MyWorkPage.tsx:1327`, 회의 승격 `MeetingDetailPage.tsx:1289`)은 불변이다. 없는 둘(`CalendarPage.tsx:645` · `TodayPage.tsx:442`)은 의도대로 B-02 동작을 받는다. 테스트: 다시 요청 · 하위 업무 |
| 범위 밖(결재자 필터) 미변경 | **PASS** | `approverCandidates`(`:5015-5018`) 변경 없음 |

### 1-2 F-01 담당자 변경 작은 모달 (SPEC-007 §2.9)

| 계약 | 결과 | 근거 |
|---|---|---|
| 기존 `Modal size="sm"`을 상세 **위**에 | **PASS** | `WorkModals.tsx:2794-2842`. 상세 `Shell`의 **형제**로 렌더한다. 두 오버레이 모두 `z-index:50`이고 DOM 뒤쪽이 위에 온다(`components.css:247` · `workspace.css:102`). 기존 선례와 같은 방식이다 |
| 내용 그대로: 대상(빈칸) · 사유(선택) · 변경/취소 | **PASS** | `openHandover` `{assigneeId:"", reason:""}` · 사유 `reason.trim() \|\| undefined`. 테스트가 `reassignTask(…,"jiho", undefined)`를 단언한다 |
| ESC · 바깥 클릭은 작은 모달만 닫음 | **PASS** | `ds/Modal.tsx:18-41` `useEscape` 스택은 맨 위 한 겹만 닫는다. 바깥 클릭은 오버레이 자신의 `onMouseDown`(`target === currentTarget`)이라 형제인 상세 오버레이로 번지지 않는다. 테스트 둘 다 있다 |
| 성공 → 작은 모달 닫고 상세 재조회, 낙관적 갱신 없음 | **PASS** | `:1271-1283`: `closeHandover` → `settleVersion()`(= `onChanged` 목록 갱신, `:962-968`) → `readDetail()`(`getTask`) → `getTaskAssignments`. 테스트가 `getTask` 호출 증가를 단언한다 |
| 실패 문구는 모달 안, 입력은 남음 | **PASS** | `handoverError` → `FieldMessage`(`:2839`). 테스트가 alert 문구와 남은 입력을 단언한다. 단, 문구 자리는 아래 WARN-3 |
| 두 번 누름 방지 | (더함) | `handoverPending`. 계약 밖이지만 무해하다 |
| P-2 · 범위 밖(「자료 링크 추가」) 미변경 | **PASS** | 새 모양 없음, 부품 `Modal` · `Select` · `Button` · `FieldMessage` 재사용. 자료 링크 폼은 손대지 않았다 |

### 1-3 F-02 「대화 검색」

| 계약 | 결과 | 근거 |
|---|---|---|
| 다른 입력칸과 같은 DS 스타일 | **PASS** | `components.css:737` 전역 입력 셀렉터에 `input[type="search"]`를 더했다. `ax.css:118` `.scax-chat__search`의 `height:42px` · 패딩 · 글자 덮어쓰기를 지웠다. 셀렉터 강도(0,1,1)가 `.search-input-box`(0,1,0)를 이겨 높이 38px · 반경 · 테두리 · 글자가 다른 입력칸과 같아진다 |
| WebKit 꾸밈 제거 | **PASS** | `:743` `appearance:none` · `:744` `::-webkit-search-{decoration,cancel-button,results-button,results-decoration}` 넷 |
| `type="search"`·검색칸 클래스를 전부 셈 | **PASS** | 아래 재계수 |

### 1-4 F-03 간트 · 1-5 D-01 타임라인 (SPEC-005 §2.4 · SPEC-001 U-16)

| 계약 | 결과 | 근거 |
|---|---|---|
| 범위 함수 **하나**를 둘이 공유 | **PASS** | `lib/weekWindow.ts:32` `weekWindow(baseWeek, spans)`를 `projectModel.ts:245`와 `WorkViews.tsx:406`이 함께 부른다. 다른 날짜 창 계산은 0이다(grep) |
| 월요일 시작 W-1~W+3 5주 | **PASS** | `mondayOf` `(weekday+6)%7` · `from = 월-7` · `to = 월+27`. 테스트: 월·일요일 경계 · 해 넘김 |
| 주 경계 넓힘(OQ-608) | **PASS** | `:37-38` 앞은 `mondayOf(start)`, 뒤는 `mondayOf(end)+6`. 테스트: 앞·뒤 두 방향, 경계 닿음 불변 |
| 넓힘은 첫 화면만, ‹ ›는 1주 밀기(OQ-P) | **PASS** | `WorkViews.tsx:405` `weekShift === 0`일 때만 `spans`를 넘긴다. 라벨은 「이전 주」·「다음 주」. 테스트: 민 창에서는 넓히지 않고 자른다 |
| 「오늘」 = 첫 화면(넓힘 포함) + 오늘 보이게 | **PASS** | `backToToday`(`:424-427`) · DS `Button size="sm"`. 캘린더 보기의 「오늘」(`:323`)과 같은 부품이다. 테스트가 범위와 `scrollLeft 204`를 단언한다 |
| 처음 열 때 오늘이 보이게 · 사람이 민 자리를 되감지 않음 | **PASS** | 간트는 기존 D-36 로직(`ProjectGantt.tsx:132-142`), 타임라인은 `scrollRequest` effect. 테스트 있음 |
| 34px · 0건 숨김 | **PASS** | `ganttAxis`가 `placed.length === 0`이면 `null`(L-56). 테스트는 빈 배열 · 기간 없는 업무 둘 다 |
| 타임라인 시작 높이를 목록과 맞춤 | **코드로는 PASS, 화면 확인 필요** | `screens-a.css:469` 위쪽 패딩 0. 목록 보기와 같은 높이인지는 jsdom이 못 잰다 |
| 막대·범례·이름 열 DS 그대로 | **PASS** | 해당 CSS · JSX 변경 없음 |

## 2. 전수조사 재계수 (P-3)

| 대상 | 직접 센 수 | 처리 |
|---|---|---|
| `<CreateWorkModal` 여는 곳 | **5**: `CalendarPage.tsx:645` · `TodayPage.tsx:442` · `WorkModals.tsx:2997` · `MyWorkPage.tsx:1327` · `MeetingDetailPage.tsx:1289` | `initial` 있음 3(불변), 없음 2(B-02 적용). 위 1-1 표 |
| `CreateWorkModal` 안의 `assigneeId` | 선언 `:4430` · 필수 `:4691` · 지문 `:4741` · 승격 `:4841` · 요청 생성 `:4850` · `:4856`(cc 제외) · 표시 `:4875` · `:5014` · 선택값 `:5241` | 모두 요청 갈래나 승격 경로에서 쓴다. 업무 갈래 제출(`:4787`)은 `ccIds`를 거르지 않는다 → 요청에서 남긴 값이 업무 갈래 참조자를 빼는 길이 없다 |
| `type="search"` | **1**: `ChatDrawer.tsx:258` | 처리 |
| `.search-input-box` | **3**: `ChatDrawer.tsx:254`(search) · `ds/Select.tsx:272`(text) · `PeoplePicker.tsx:41`(text) | text 두 자리는 이번 변경 영향이 0이다(전역 규칙에 이미 잡혀 있었고 새 규칙은 search만 본다) |
| `.scax-textfield--search` | 1(`ProjectManageModal.tsx:252`). CSS 정의 0 | DS 텍스트필드 골격이고 search 입력이 아니다. 같은 문제가 아니라 손대지 않은 것이 맞다 |
| 범위 계산 | `weekWindow` 호출 2 · `mondayOf` 2 · 옛 `ganttAxis` 자체 계산 · 옛 `TaskTimeline` 14일 창 계산 둘 다 0 | 하나로 모였다 |

빠진 자리는 찾지 못했다.

## 3. 조용히 통과하는 자리 · 테스트 품질

- 날짜 경계는 **오늘을 주입해서** 잰다.
  - `weekWindow` · `ganttAxis`는 인자로 받는다.
  - 타임라인과 간트 화면 테스트는 `seoulToday`를 목으로 고정한다.
  - 월요일 · 일요일 · 해 넘김 · 앞뒤 넓힘 · 경계 닿음 · 민 창을 모두 단언한다. 빈 단언이나 이름만 바꾼 테스트는 없었다.
- 간트 화면 테스트(`ProjectPage.test.tsx`)는 「오늘이 축 밖」 두 케이스를 **새 계약으로 뒤집었다**(축이 늘 오늘을 품는다).
  - 그래서 `ProjectGantt.tsx:138` 「오늘이 축 밖이면 가장 가까운 끝으로 접는다」는 이제 **도달할 수 없는 분기**다(WARN-2).
- `TaskTimeline`은 안에서 `seoulToday()`를 부른다. 주입은 되지 않지만 모듈 목으로 고정할 수 있고, 기존 패턴(간트 페이지와 같음)을 따른 것이라 지적하지 않는다.
- F-02 테스트는 CSS 문자열 포함 여부만 잰다(WARN-4).

## 4. P-2 · CSS 부작용

- 새 색 · 새 모양 0. 하드코딩 px는 기존 34px 짝뿐이다.
  - `WorkViews.tsx:389` `TIMELINE_DAY = 34`는 `screens-a.css:476-486`의 `minmax(34px,1fr)`와 짝이라고 주석으로 묶었다.
  - 간트 `GANTT.day`와 같은 값이다. 상수를 공유하지 않는 것은 경미하다.
- `components.css:737` 전역 규칙 확장은 `type="search"` 한 자리에만 닿는다(grep 1건). 다른 입력칸 영향은 0이다.
- `ax.css:118` 변경으로 대화 검색은 42px → 38px, 글자는 label2 → body1이 된다. 다른 입력칸과 같아지는 것이 계약이다.
- `screens-a.css:469` `.work-timeline`은 타임라인 한 곳에서만 쓴다.
- 프론트 규율: `api.ts` 밖 fetch 0. 권한 판단 변경 0. `Modal` · `Select` · `Button` · `FieldMessage` · `Icon`을 재사용했다.

## 위반 (FAIL)

없음.

## 경미 (WARN)

- **WARN-1** `frontend/src/features/project/ProjectPage.test.tsx:427-434`
  - 테스트 이름과 단언은 새 계약(「오늘」이 보이는 자리, 340px)으로 바뀌었다.
  - 그런데 위 주석은 옛 근거를 그대로 말한다: 「오늘이 축 왼쪽 밖이면 … 가장 가까운 끝 = 기간의 첫날」, 「68 에서 열린 화면」, 「0 을 덮어써야 통과한다」.
  - 다음 사람이 이 주석을 계약으로 읽는다. 권장: 주석을 「전환해도 340 으로 다시 맞춰야 통과한다」로 고친다.
- **WARN-2** `frontend/src/features/project/ProjectGantt.tsx:138` 부근
  - 「오늘이 축 밖이면 가장 가까운 끝으로 접는다」 분기와 주석이 남았다.
  - 업무가 있으면 축이 늘 W0(오늘)를 품으므로 이제 도달하지 않는다. 동작에는 해가 없지만 읽는 사람이 헷갈린다.
  - 권장: 주석에 「F-03 이후 방어용」 한 줄을 달거나 분기를 정리한다.
- **WARN-3** `frontend/src/features/work/WorkModals.tsx:2839`
  - 작은 모달의 실패 문구(`FieldMessage`)가 **사유 칸 아래** 하나뿐이다.
  - 그래서 「옮길 담당자를 골라 주세요」(대상을 안 고른 경우, `:1258`)도 사유 칸 밑에 뜬다.
  - SPEC-007 §2.9 「모달 안에 낸다」는 지켰다. 다만 대상 칸 오류가 다른 칸 밑에 서는 것은 어색하다. 화면 확인 목록 3번과 같은 자리다.
- **WARN-4** `frontend/src/features/chat/ChatDrawer.test.tsx` F-02 describe
  - CSS 파일 문자열 포함 여부를 잰다. 규칙 순서나 강도가 바뀌어도 통과한다. 주석이 「규칙이 서 있는지만 잰다, 모양은 화면으로」라고 밝혔고 기존 선례(`HoverContrast.test.tsx`)도 있어 FAIL은 아니다.
  - 실제 계약(웹 = Tauri)은 **코디의 화면 두 장**만이 증명한다.

## 5. 화면 확인 목록 (코디용 — 「막히진 않는데 눈에 이상할」 자리)

1. **F-02 Tauri**: `make tauri-local`에서 대화 검색칸의 높이 · 반경 · 테두리가 같은 서랍의 다른 입력과 같은지 본다. ×(지우기) 단추가 사라졌는지도 본다. 우리가 지운 것이니 **입력을 지울 단추가 없다**는 점을 사용자가 알고 있는지 확인한다.
2. **F-01 겹침 농도**: 상세 위에 작은 모달이 뜨면 32% 딤이 **두 겹**이 된다(같은 색 오버레이 둘). 기존 7종 선례와 같지만 상세가 꽤 어두워진다.
3. **F-01 오류 자리**: 대상을 안 고르고 [변경]을 누르면 오류가 **사유 칸 아래**에 뜬다(WARN-3).
4. **F-01 Select 팝오버**: 420px 작은 모달 안에서 「담당자 변경 대상」 목록이 잘리지 않고 모달 밖으로 펼쳐지는지 본다.
5. **F-01 성공 뒤**: 모달이 닫히고 상세에 「담당 변경 대기」가 선다. 상단 알림 「담당 변경을 제안했습니다…」가 같이 뜨는지 본다.
6. **D-01 시작 높이**: 같은 탭에서 목록 ↔ 타임라인을 바꿔 칩 바 아래 첫 줄 높이가 같은지 본다(코드는 위 패딩만 0으로 했다. `.calendar-toolbar` 아래 여백은 남는다).
7. **D-01 민 뒤의 스크롤 자리**: 범위 밖 업무로 넓어진 첫 화면(예: 63일)을 오른쪽으로 스크롤한 뒤 ›를 누르면 창이 35일로 줄어든다. 그때 스크롤 위치는 되감지 않으므로 **어정쩡한 자리**에 설 수 있다(의도: 사람이 민 자리를 뺏지 않는다).
8. **D-01 넓은 화면**: 35일 × 34px + 200px ≈ 1390px보다 넓은 창에서는 칸이 늘어나 스크롤이 없다. 「오늘」을 눌러도 움직임이 보이지 않는다(정상).
9. **F-03 간트**: 이미 끝난 프로젝트나 아직 시작 안 한 프로젝트도 이제 오늘 주변 5주 + 업무 쪽으로 넓어진 축이다. **업무 막대가 축 한쪽 끝에 몰리고 큰 빈 구간**이 보이는 것은 계약대로다. 사용자가 처음 보면 놀랄 수 있다.
10. **B-02**: 「새 업무 추가」를 캘린더 · 오늘 화면에서 열었을 때도 요청 담당이 빈칸으로 시작하는지 본다(`initial` 없는 두 자리).

## 기존 부채 (이번 판정 제외)

- `CreateWork.test.tsx`의 날짜 의존 4건과 CreateWorkLayout 1건: 오늘 날짜에 따라 달력 칸이 없어 실패한다(`flaky-baseline-evidence.md`).
- 업무 갈래의 「업무 주인」(`taskOwnerId` · `assignTarget`, `WorkModals.tsx:4518`)으로 남을 고르면, 그 사람은 참조자 후보에서 빠지지 않는다. 이번 diff 전부터 그랬고 B-02 계약(요청 갈래 담당자)의 범위 밖이다. 같은 사람이 주인 겸 참조자로 실릴 수 있는지는 따로 볼 일이다.

## 확인한 것 (체크리스트)

- envelope · 권한: 변경 없음 ✔
- `api.ts` 밖 fetch 0 ✔
- 재사용: `Modal` · `Select` · `Button` · `FieldMessage` · 기존 `useEscape` 스택 ✔
- 카피: 새 한국어 문자열(「담당자 변경」 · 「이전 주」 · 「다음 주」 · 「오늘」)이 `labels.ts` 밖 JSX에 있다. 바꾼 자리 주변의 기존 문자열도 같은 방식이라 기존 패턴을 따른 것으로 본다
- 하드코딩 hex 0 ✔
- 옆자리 테스트: `weekWindow.test.ts` 신설 · 바뀐 동작마다 테스트 ✔
- 직렬 테스트 실행: 7파일 227/231. 실패 4는 기준선과 같다 ✔
- tsc · build: **재실행 안 함**(워커 보고를 그대로 옮긴다)

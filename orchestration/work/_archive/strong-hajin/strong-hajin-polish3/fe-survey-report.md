# 고도화 3차 조사 (frontend)

- 대상: `Strong_hajin/strong-hajin-polish3` @ `d1b5137` (origin/main, 운영 반영 코드)
- 방식: 읽기 전용. 코드·테스트·빌드·서버·Tauri 실행 없음. 브라우저·운영 서버 접속 없음.
- 경로: 따로 적지 않으면 `frontend/src/` 기준이다. `backend/…`·`frontend/src-tauri/…`·`frontend/index.html` 은 저장소 루트 기준이다.
- 숫자: `grep -rn` 결과에서 `*.test.*` 를 뺀 값이다(§7).
- ⚠ 직전 조사(polish2)와 달리 화면 파일이 `features/<영역>/` 아래로 옮겨져 있다. 업무 상세는 `features/work/WorkModals.tsx` 의 `TaskDetailDrawer`(`:606-3039`)다. 이름은 Drawer 지만 **기본 골격은 가운데 모달**이다(`presentation = "modal"` 기본값 `:625`, 골격 선택 `:1782`).

---

## 0. 한 줄 요약

| 요청 | 한 줄 |
|---|---|
| R1 | h1·설명 `p` 는 `features/auth/LoginPage.tsx:68-69` 한 자리뿐이다. 같은 문구는 저장소 어디에도 없다(각 1건). 문서 title 은 `MEDISOLVE`(`frontend/index.html:11`)이고, Tauri 창 제목은 판의 `productName`(`medi-ax` / `Strong Hajin`)이다. |
| R2 | **크기 원인**: 「내보내기」 `<a>` 에는 `scax-button--sm` 이 없다. 그래서 기본 md 크기(높이 39px·14px 글자·좌우 16px)로 선다. 옆 두 단추는 `<Button size="sm">` 이라 `scax-button--sm`(32px·13px·12px)이 붙는다(`MeetingDetailPage.tsx:1005` · `ds/Button.tsx:77` · `styles/components.css:8,11` · `styles/scax.css:122-123`). **Tauri**: 앱은 원격 origin 웹뷰다. 다운로드 핸들러·새 창 핸들러·파일/다이얼로그 플러그인이 하나도 없다(`src-tauri/src/lib.rs:372-413` · `Cargo.toml:35`). 같은 origin `<a href>` 는 이동이 허용되고 쿠키 인증도 실린다. 그 뒤 첨부 응답을 웹뷰가 어떻게 처리하는지는 코드로 확정되지 않는다(§8). |
| R3 | 제목 `h2` 는 `meeting.title ?? "제목 없는 회의"`(`MeetingDetailPage.tsx:962` · `labels.ts:761`)를 그린다. 제목이 없고 `title_candidate` 가 있으면 옆에 `span.t-meta`「제목 후보 …」(`:964-967` · `labels.ts:931`)가 선다. 제목을 바꾸는 화면 입구는 **회의 목록 카드 [수정] → `MeetingEditModal` 하나**이고, 그 단추는 `scheduled` 일 때만 선다(`MeetingListPage.tsx:409`). 서버는 `done` 회의의 제목 변경도 받는다(`backend …/meetings/domain.py:104`). 인라인 편집 부품 `ds/InlineText.tsx`(contenteditable · Enter/blur 저장 · Esc 취소)가 있고, 회의 안건·메모 2곳에서 쓴다. |
| R4 | 업무 상세는 **머리**(kicker「업무 상세」·제목·상태 글자·마감 초과·버전·편집·AX·×)와 본문으로 나뉜다. 본문은 **메타 한 줄 + 출처 줄 + 시작 막힘 배너 + 덩어리 다섯**(업무 정보 · 진행과 판단 · 연관 업무 · 자료 · 이력)이고, 푸터에는 **단추가 최대 11종** 선다. 「편집」은 제목·업무 내용·시작 예정일·마감일 넷을 입력칸으로 바꿀 뿐이다. 저장은 푸터의 「변경 저장」(PATCH `/api/tasks/{id}`)이 따로 한다. 「업무 내용」 라벨이 두 번 나오는 원인은 칸 머리 `h5`(`:2068`)와 필드 `label`(`:2071`)이 함께 서기 때문이다. 상세를 그리는 자리는 **3곳**(내 업무·홈·캘린더)이다. 다른 화면(채팅·프로젝트·관계 그래프)은 모두 내 업무 화면으로 넘겨 **`manage:false`(읽기 전용)** 로 연다. |
| R5 | 빨간 배너(`WorkModals.tsx:2054-2059`)와 푸터 문구(`:1853`)는 **같은 조건 `startBlocked`** 로 선다. 조건은 `state==="open"` + 볼 수 있는 미완 선행 ≥1(`workRows.ts:147-149`)이다. 그때 「시작」·「완료 처리」는 **disabled** 다(`:1834,1849`). 같은 문구는 목록 행 `TaskQuickActions`(`:3515`)에도 있다. 상태 드롭다운 두 곳(`MyWorkPage.tsx:1483` `TaskStateCell` · `ProjectTaskPanel.tsx` `TaskStateValue`)은 미리 막지 않는다. 이 두 곳에서는 서버가 409 로 거절하고, 그 문장이 **이미 공통 토스트(오류)** 로 뜬다(`App.tsx:118,637-650`). |
| R6 | 칩 줄 아래부터 「담당」 줄 위까지 = 머리 padding-bottom **20** + 머리 border **1** + 본문 padding-top **20** + `.scax-td`·`.meta` 위 여백 **0** = **41px**(`components.css:257, 263` · `task-detail.css:96-99`). 칩 줄 높이가 32px(편집·AX 단추)이면 22px 배지가 가운데 정렬되어, 배지 기준으로는 약 46px 이다. 두 공용 규칙을 쓰는 표면은 **13개**(Modal 직접 7 · Shell 경유 2 · ConfirmModal 4)다. |

---

## 1. R1 로그인 브랜드

### 1-1. 위치와 같은 문구
- 컴포넌트: `features/auth/LoginPage.tsx`
  - `main.login-shell` `:62` › `section.login-brand[aria-hidden]` `:63`
  - `.wordmark`(「M」 + 「MEDISOLVE」) `:64-67`
  - **h1** `:68` — `기록 → 판단 → 수행 → 보고를 한 흐름으로`
  - **p** `:69` — `조직의 업무를 하나의 원장에서 다루고, AX가 허용된 범위 안에서 조회하고 제안합니다.`
- CSS(`styles/screens-a.css`)
  - `.login-shell` `:65` (2열 grid)
  - `.login-brand` `:68` (flex column · gap `--scax-space-400` · padding `--scax-space-1200` · 그라디언트 배경)
  - `.login-brand .wordmark` `:69`
  - `.login-brand h1` `:70` (max-width 520 · 28px · lh 1.5)
  - `.login-brand p` `:71` (max-width 480 · body1)
  - `@media (max-width:900px) .login-brand{display:none}` `:116`. 같은 규칙이 `styles/components.css:713` 에 한 번 더 있다.
  - DS 번들 사본 `.design-sync/screens/_ds_bundle.css:1731, 2141-2144, 2189` 에는 규칙만 있고 문구는 없다.
- grep(저장소 전체 — src·index.html·src-tauri·tests·docs·scripts·.design-sync)

  | 문구 | 건수 |
  |---|---|
  | `보고를 한 흐름으로` | **1** (`LoginPage.tsx:68`) |
  | `조직의 업무를 하나의 원장에서` | **1** (`LoginPage.tsx:69`) |

  테스트·스냅샷에도 없다.
- 이웃 문자열(같은 문구가 아님 — 참고)
  - 문서 title `frontend/index.html:11` `<title>MEDISOLVE</title>`
  - meta description `frontend/index.html:6` `MEDISOLVE 업무 운영 시스템`
  - `document.title` 을 쓰는 코드: 0건
  - Tauri 창 제목: `tauri.conf.json:9` `"windows": []`. 창은 Rust 가 `.title(app.package_info().name)` 로 만든다(`src-tauri/src/lib.rs:374-376`). 값은 판의 productName 이다.
    - `flavors/medi-ax/tauri.conf.json:3` → `medi-ax`
    - `flavors/strong-hajin/tauri.conf.json:3` → `Strong Hajin`
    - 기본값 `src-tauri/tauri.conf.json:3` → `Strong Hajin`

---

## 2. R2 회의 상세 「내보내기」

### 2-1. 머리 단추 묶음과 크기 차이의 원인
- 묶음 `div.scax-detail__head-actions`: `features/meetings/MeetingDetailPage.tsx:972`. CSS 는 `styles/workspace.css:122`(flex · center · gap 200 · `margin-left:auto`)다.
  - 「공유」 `:997-999`: `<Button size="sm" type="button">` — 조건 `attendee && (settled || failedState)`
  - 「내보내기」 `:1003-1007`: `<a className="scax-button scax-button--outlined-neutral" href={meetingExportUrl(id)}>` — 조건 `settled`. 바로 위 주석 `:1003` 은 「받는 것은 브라우저가 한다 — 서버가 Content-Disposition 을 실어 보낸다」이다.
  - 「다음 회의 예약」 `:1009-1012`: `<Button size="sm" type="button">` — 조건 `settled && attendee`
  - 문구 `lib/labels.ts:766-769` · URL `lib/api.ts:1372-1374` `/api/meetings/${id}/export?format=html`
- **원인 = 크기 modifier 하나**
  - `Button` 은 `size !== "md"` 일 때 `scax-button--${size}` 를 붙인다(`ds/Button.tsx:77`). `<a>` 에는 그 클래스가 없어 기본(md)이 된다.

  | 항목 | `<a>` — `.scax-button`(`components.css:8`) | `<button>` 둘 — `.scax-button--sm`(`components.css:11`) |
  |---|---|---|
  | 높이 | `--scax-control-height-md` **39px** (`scax.css:123`) | `--scax-control-height-sm` **32px** (`scax.css:122`) |
  | 좌우 안여백 | `--scax-space-400` 16px | `--scax-space-300` 12px |
  | 모서리 | `--scax-radius-md` 10px | `--scax-radius-sm` 8px |
  | 글자 | label1 14px | label2 13px |

  - 요소 차이는 원인이 아니다. 전역 `button{…}`(`styles/shell.css:41-42`)·`a{color;text-decoration:none}`(`shell.css:46`)은 명시도 0,0,1 이라 `.scax-button`(0,1,0)이 모두 덮는다.
  - 차이로 남는 것은 `.scax-button:disabled`(`components.css:10`) 하나다. `<a>` 에는 걸리지 않는다.
- `ds/Button.tsx` 는 늘 `<button>` 을 그린다(`:81`). `href`/`as` prop 은 없다(props 는 `ButtonHTMLAttributes` `:70`).

### 2-2. `<a>` 에 `scax-button` 을 쓰는 자리 — **3곳**

| # | 자리 | 클래스 | 크기 |
|---|---|---|---|
| 1 | `features/meetings/MeetingDetailPage.tsx:1005` 회의 내보내기 | `scax-button scax-button--outlined-neutral` | **md(39px) — 옆 단추와 어긋남** |
| 2 | `features/meetings/MaterialDrawer.tsx:66` 회의 자료 내려받기 | `… --outlined-neutral scax-button--lg` | lg(47px), 의도적으로 지정 |
| 3 | `features/chat/MessageList.tsx:782` 근거 「원본 열기」 | `… --text-neutral scax-button--sm` | sm |

(참고: `ds/Empty.tsx:75` 는 `scax-button` 을 쓰지만 `<button>` 이다.)

### 2-3. Tauri 에서 다운로드
- **앱은 원격 origin 웹뷰다**
  - `frontendDist: "shell-noop"` (`src-tauri/tauri.conf.json:6`)
  - 창 = `WebviewUrl::External(start_url)` (`src-tauri/src/lib.rs:374`)
  - medi-ax 판: `operationalOrigin: "https://ax.medisolveai.xyz"` (`flavors/medi-ax/shell.config.json:10`)
  - strong-hajin 판: `null` (`flavors/strong-hajin/shell.config.json:10`) → 「설정되지 않음」 화면
- **권한**: `flavors/medi-ax/capabilities/product-shell.json`
  - remote url `https://ax.medisolveai.xyz/*` (`:8`)
  - 권한 4개뿐이다: `allow-shell-info` · `allow-wake-guard-acquire/release` · `allow-open-external` (`:10-15`)
  - description 에 「파일·프로세스·범용 셸·open_path 권한은 하나도 없다」고 적혀 있다(`:4`).
- **플러그인**: `tauri-plugin-opener` 하나다(`src-tauri/Cargo.toml:35`). Rust 에서만 쓴다(`lib.rs:235, 340, 395`). dialog·fs·download 플러그인은 없다.
- **이동 처리**: `on_navigation` (`lib.rs:384-406`)
  - 셸 자기 스킴은 허용한다.
  - `nav_allow` 의 origin(= 운영 origin)이면 `true`(허용)다.
  - 그 밖의 http(s) 는 **취소**하고 `tauri_plugin_opener::open_url` 로 OS 기본 브라우저에 넘긴다(`:392-402`).
  - `on_page_load` Started 는 문서가 실제로 바뀌면 `clear_window`(웨이크 가드 해제)를 부른다(`:410-413`).
  - `.incognito(false)` 로 쿠키를 유지한다(`:381-383`).
- **다운로드·새 창 처리**: `src-tauri` 전체에서 `on_download|on_new_window|new_window|download` 는 **0건**이다.
- **같은 origin `<a href="/api/meetings/{id}/export?format=html">` 를 누르면**
  - 코드로 확인되는 것
    1. 같은 origin 이므로 `on_navigation` 이 통과시킨다.
    2. 요청은 웹뷰의 쿠키(`scax_session`)를 싣는다.
    3. 서버는 `text/html; charset=utf-8` + `Content-Disposition: attachment; filename*=UTF-8''…` 로 답한다(`backend/src/ax_workspace/entrypoints/http.py:896-912`, 헤더 `:911`).
  - 코드로 확인되지 않는 것: 그 첨부 응답을 WKWebView/wry 가 **저장하는지, 무시하는지, 창 안에 HTML 로 여는지**. 앱 코드에는 이를 다루는 자리가 없다 → §8 조사 한계.
- **인증**
  - FE 요청은 전부 상대경로 `/api/…` + `credentials: "same-origin"` 이다(`lib/api.ts:138` 공용 `request`, 업로드 `:112,127`).
  - `Authorization` 헤더·토큰·API base env 는 없다. dev 는 vite proxy 다(`frontend/vite.config.ts:14`).
  - 서버는 쿠키 `scax_session` 을 읽는다(`backend/src/ax_workspace/entrypoints/http_auth.py:21, 41-42`; dev 용 `X-Demo-Persona` 헤더 `:75`). 쿠키 속성은 httponly·samesite=lax·secure 다(`backend/.../http.py:653-659`).
  - → **웹뷰 안의 같은 origin `<a href>` 에는 인증이 실린다.** OS 브라우저로 넘어가는 URL(`open_external` 또는 막힌 이동)에는 **웹뷰 쿠키가 없다.**
  - `target="_blank"` 링크: 새 창 핸들러가 없다. `lib/shell.ts:183-197` 은 셸 안에서 `window.open` 을 일부러 쓰지 않는다(「앱 창 안에 두 번째 웹뷰가 앉는」 사고를 막는다는 주석). `_blank` 가 셸에서 무엇을 하는지는 코드로 확정되지 않는다(§8).

### 2-4. 파일을 내려받거나 여는 자리 전부 — 10자리

| # | 자리 | 방식 | URL |
|---|---|---|---|
| 1 | 회의 내보내기 `features/meetings/MeetingDetailPage.tsx:1005` | 같은 탭 `<a href>` (`download` 속성 없음) | `meetingExportUrl` `api.ts:1372` → 서버 attachment |
| 2 | 회의 자료 내려받기 `features/meetings/MaterialDrawer.tsx:66` | 같은 탭 `<a href>` | `meetingMaterialContentUrl` `api.ts:1409` → `http.py:1105-1122`(형식별 inline/attachment `:1117`) |
| 3 | 회의 자료 PDF 미리보기 `MaterialDrawer.tsx:88` | `<object data>` | 위와 같음 |
| 4 | 회의 자료 Markdown 본문 `api.ts:1414-1417` | `fetch` + `.text()` | 위와 같음 |
| 5 | 업무 자료(참고·결과) `features/work/WorkModals.tsx:1756` | `<a target="_blank">` | `item.url ?? taskMaterialContentUrl` `api.ts:328` |
| 6·7 | 요청 첨부 `WorkModals.tsx:4115`, `:4143` | `<a target="_blank">` | `requestAttachmentUrl` `api.ts:1096` |
| 8 | 채팅 근거 「원본 열기」 `features/chat/MessageList.tsx:782` | `<a target="_blank">` | `item.origin`(서버 값) |
| 9 | AX 답변 안 링크 `features/chat/AssistantMarkdown.tsx:199` | `<a target="_blank">` | 본문 href. `/api/…/content` 도 통과한다(`:34, :56`). |
| 10 | 자료 리소스 열기 `App.tsx:719-728` | 셸이면 Tauri `openExternal`(OS 브라우저), 아니면 `window.open` | `resource.origin` |

- 그 밖: dev 전용 `dev/ProbePage.tsx:424` `<a target="_blank">`. `workRequestMaterialContentUrl`(`api.ts:635`)은 호출 0건이다.
- **fetch + Blob 다운로드 0건 · `URL.createObjectURL` 0건 · `download` 속성 0건 · Tauri 파일 API 0건**이다. `Blob` 6건은 전부 녹음이다(`liveTranscription.ts` · `BrowserRecordingPage.tsx` · `api.ts:108`).

---

## 3. R3 회의 제목

### 3-1. 제목과 「제목 후보」
- 마크업(`features/meetings/MeetingDetailPage.tsx`)
  - `header.scax-detail__head` `:960` › `div.scax-detail__title-row` `:961`
  - `h2.scax-detail__title` `:962` — `{meeting.title ?? meetingScreen.noTitle}`
  - 주석 `:963`: 「합성이 낸 제목 후보 — 아직 제목이 아니다. 목록의 [수정]으로 열어 저장해야 제목이 된다」
  - `:964-967` — `!meeting.title && meeting.title_candidate` 일 때 `span.t-meta`(인라인 `style={{fontSize:12}}`) `{meetingScreen.titleCandidate(candidate)}`
- 데이터 필드
  - `meeting.title: string | null` (`lib/viewModels.ts:1240`, `MeetingInfo` `:1238~`)
  - `meeting.title_candidate: string | null` (`viewModels.ts:1272`, 주석 `:1271` 「사람이 저장해야 제목이 된다」)
  - 편집 가능 여부 `can_edit_info` (`viewModels.ts:1251`)
  - 목록 행 `MeetingRow.title`(`:1133`)에는 `title_candidate` 가 없다.
- 대체 문구
  - `meetingScreen.noTitle: "제목 없는 회의"` (`lib/labels.ts:761`)
  - `titleCandidate: (c) => \`제목 후보 ${c}\`` (`labels.ts:931`)
  - `noTitle` 사용 5곳: `MeetingDetailPage.tsx:299`(상위로 제목 전달 `onTitleChange`) · `:962` · `MeetingListPage.tsx:401` · `shell/CalendarRail.tsx:134` · `features/calendar/calendarModel.ts:92`
- CSS: `styles/workspace.css:15`(`.scax-detail__title-row` flex · gap 8) · `:16`(`.scax-detail__title` 제목 크기 · nowrap · 말줄임)
- 서버 쪽 대체(참고): `TITLELESS_MEETING`/`UNTITLED_MEETING`(`material_sources.py:117` · `native_materials.py:29` · `work_tasks.py:99` · `export.py:89`). 문자열 「제목 없는 회의」도 `platform/actions.py:1338` · `modules/meetings/application.py` `update_info` 에 있다.

### 3-2. 회의 제목을 바꾸는 화면 입구 — 1곳
- **회의 목록 카드 [수정] → `MeetingEditModal`**
  - 단추: `features/meetings/MeetingListPage.tsx:409-420`. 조건은 **`row.status === "scheduled"` 만**이다.
  - 모달: `MeetingListPage.tsx:312`, `MeetingEditModal` 은 이 한 곳에서만 쓴다.
  - 모달 안(`features/meetings/MeetingEditModal.tsx`)
    - 초기값 `meeting.title ?? meeting.title_candidate ?? ""` (`:81`)
    - `can_edit_info` 게이트 (`:98`)
    - 회의명 `<input>` (`:159-168`)
    - 저장 `updateMeetingInfo(id, {title: trim()||null, starts_at, ends_at, location, attendee_ids})` (`:119-125`)
    - DS `Modal` 이 아니라 옛 `.modal-backdrop/.modal/.modal-head/.modal-body` 손마크업이다(`:138-147`).
- API: 회의 갱신 함수는 `updateMeetingInfo` 하나다 → **`PATCH /api/meetings/{id}`** (`lib/api.ts:1225-1237`, `title?: string|null`).
- 서버
  - `backend/src/ax_workspace/entrypoints/http.py:778`(`exclude_unset` `:783`)
  - 입력 모델 `modules/meetings/commands.py:163-171` `MeetingInfoPatch.title(max 300, extra=forbid)`
  - `modules/meetings/application.py:474` `update_info`: 참석자만, `can_edit_info` 일 때. 빈 제목은 null 로 정규화한다(`:516`).
  - **편집 가능한 상태 `{SCHEDULED, DONE}`** (`modules/meetings/domain.py:104`, 적용 `policy.py:233`)
  - → 끝난(`done`) 회의는 서버가 받지만, 화면에는 그 입구가 없다(목록 [수정]이 `scheduled` 에만 선다).
- 입구가 아닌 것
  - 회의 상세 머리에는 연필 단추가 없다(`MeetingDetailPage.tsx:947-958` 주석).
  - `MeetingDetailPage.tsx:23` 은 `updateMeetingInfo` 를 **import 만 하고 쓰지 않는다**(파일 안 다른 사용 0건).
  - `BookingModal.tsx:242`(생성 시 title) · `features/action/ActionMeetingCard.tsx:397-405`(AX 회의 초안 생성)는 생성용이다.

### 3-3. 인라인 편집 부품

| 부품 | 위치 | 동작 | 쓰는 자리 |
|---|---|---|---|
| **`InlineText`** (CMP-118) | `ds/InlineText.tsx:46-213` · CSS `styles/components.css:767-776` | 같은 `<span>` 이 `contentEditable` 로 바뀐다. 입력칸이 나타나지 않는다(`:179`). 열기: 클릭 / Enter·Space (`:181-189`). **blur 저장**(`:180`) · **Enter 저장**(`:192-196`) · **Esc 취소**(blur 저장 건너뜀, `:198-202`). 빈 값·안 바뀐 값은 저장하지 않는다(`:162`). 줄바꿈을 걷는다(`:158`). 거절되면 `value` 로 돌아온다(`:163-166`). 부모 행이 여는 손잡이 `InlineTextHandle.open(point)`(`:41-44, 100`). | **2** — `features/meetings/AgendaBlock.tsx:138`(안건 제목) · `:189`(메모 줄) |
| 체크리스트 단계 수정 | `features/work/WorkModals.tsx:2139-2160`(`input.step-edit`, autoFocus) · 저장 `renameStep` `:1012-1025` · CSS `screens-a.css:445` | [수정] 단추를 눌러야 input 으로 바뀐다. **blur 저장** · **Enter 저장**(IME 조합 중 건너뜀) · **Esc 취소**. 빈 값·안 바뀐 값은 저장하지 않는다. | 1 |
| 업무 상세 제목 입력 | `WorkModals.tsx:1964-1974` | 클릭 인라인이 아니다 — 머리 「편집」 토글 + 푸터 「변경 저장」(§4-2) | 1 |

- 프로젝트 이름을 바꾸는 자리는 없다(`api.ts` 에 `updateProject` 없음). `contentEditable` 은 `ds/InlineText.tsx:179` 한 곳뿐이다.
- `InlineText` 의 DS 시안(`.design-sync/previews`)은 없다.

---

## 4. R4 업무 상세 모달 — 개편 근거

### 4-1. 구조 — 코드 그대로 (`features/work/WorkModals.tsx` `TaskDetailDrawer`)

**골격**: `Shell = presentation === "modal" ? Modal : Drawer` (`:1782`). 기본값이 `"modal"`(`:625`)이고 세 호출부 모두 넘기지 않는다 → `ds/Modal.tsx` `Modal`(`:135-187`) 기본 폭 880(`components.css:256`). `className`·`size` 는 넘기지 않는다.

```
div.scax-modal-overlay                                   ds/Modal.tsx:159
└ section.scax-modal[role=dialog][aria-modal][aria-label="업무 상세"]   :165-170 · label WorkModals:1932
  ├ header.scax-modal__head                              ds/Modal.tsx:171
  │ ├ (onBack 있을 때) IconButton chevron-left            :174  ← 내 업무에서 겹이 2개 이상일 때만 (MyWorkPage.tsx:1298-1299)
  │ ├ div[style flex:1 1 auto; min-width:0]              :175
  │ │ ├ small.modal-kicker  「업무 상세」                    :176 · kicker WorkModals:1931
  │ │ ├ h3.scax-modal__title  {task.title}                 :177 · title WorkModals:1934
  │ │ └ headerExtra = ChipRow(div.scax-chip-row)           WorkModals:1896-1929 · ds/Chip.tsx:62
  │ │    ├ StatusText → span.status.{state}  상태 글자        :1897 · 정의 :321-323
  │ │    ├ (마감 초과일 때) Badge tone=danger 「마감일 초과」     :1898
  │ │    ├ Badge tone=outline 「v{version}」                 :1899
  │ │    ├ (editable && relDraft===null) Button text sm 「편집」/「편집 끝내기」  :1905-1909
  │ │    └ (onAskAx) Button variant=ai sm  ✦「AX」 aria-label「AX에게 이 업무 묻기」  :1911-1928
  │ └ IconButton close  aria-label「상세 닫기」            ds/Modal.tsx:180 · closeLabel WorkModals:1787
  ├ div.scax-modal__body                                  ds/Modal.tsx:182
  │ └ div.scax-td                                         WorkModals:1952  (styles/task-detail.css 스코프)
  │   ├ div.meta[aria-label="업무 메타"]                    :1962
  │   │ └ div.meta__left                                   :1963
  │   │   ├ (metaEditing) label.sr-only「제목」 + input.meta__title-input   :1964-1974
  │   │   ├ div.meta__facts                                :1975-1995
  │   │   │  · 담당 <b>{ownerName}</b>                       :1976  (늘)
  │   │   │  · 시작 예정일 {start_date}     조건 !metaEditing && start_date     :1982
  │   │   │  · 실제 시작일 {started_at}     조건 started_at                     :1983
  │   │   │  · 실제 종료일 {completed_at}   조건 completed_at                   :1984
  │   │   │  · 마감일 {due_date}           조건 !metaEditing && due_date       :1985
  │   │   │  · 결재 {approver 이름}         조건 approver_id                    :1986-1988
  │   │   │  · 참조 {cc 이름들 · 로 이음}    조건 cc_member_ids 1+               :1989-1994
  │   │   ├ (task.origin) p.origin-chip[aria-label="업무 출처"]   :1996-2009
  │   │   │  · Badge outline {originSentence}               :2000
  │   │   │  · source 있고 onOpenSource 있으면 Button inline {source.title ?? "출처 보기"}  :2002-2005
  │   │   │    없으면 small.t-meta {source.title}             :2007
  │   │   └ (metaEditing) div.meta__edit > DateField 「시작 예정일」 · DateField 「마감일」  :2015-2040
  │   ├ (startBlocked) section.drawer-section.notice.danger[aria-label="시작할 수 없습니다"]  :2054-2059  → §5
  │   ├ section.block 「업무 정보」                          :2064-2227
  │   │  ├ div.block__row > h3                             :2065
  │   │  └ div.stack
  │   │     ├ div.cell — cell__head h5「업무 내용」          :2067-2068
  │   │     │   · metaEditing: div.scax-field > label.scax-field__label「업무 내용」 + textarea.task-description(rows 4)  :2069-2081
  │   │     │   · 값 있으면 p.desc / 없으면 p.desc.desc--empty「적어 둔 내용이 없습니다.」  :2082-2086
  │   │     └ (!readOnly) div.cell[aria-label="체크리스트"]       :2093-2225
  │   │         · cell__head h5「체크리스트」 + 진행 n/m        :2104-2113
  │   │         · ProgressBar (1건 이상)                       :2125-2127
  │   │         · 빈 상태「단계가 없습니다.」 / CollapsingList(5줄 접힘)  :2128-2197
  │   │           행: Checkbox · (canManage) 위로·아래로·수정·삭제  :2163-2190
  │   │           「수정」 → input.step-edit (blur·Enter 저장, Esc 취소)  :2139-2159
  │   │         · (canManage) 새 단계 input + 「추가」           :2199-2223
  │   ├ (hasProgressBlock) section.block 「진행과 판단」     :2242-2427   → 4-3
  │   ├ section.block 「연관 업무」 / 편집 중 「연관 업무 편집」   :2438-2787
  │   │  · 머리 단추: 편집 중 「취소」「저장」 / (editable) 「연결 편집」  :2441-2457
  │   │  · div.cols 2열 여섯 칸: 상위|프로젝트 · 하위|선행 · 참고(!readOnly)|후행  :2459-2786
  │   │    하위 칸 머리 「하위 업무 생성」(!relDraft && editable) → CreateWorkModal  :2553-2566, 3017-3036
  │   ├ (!readOnly) section.block 「자료」 > div.cols  참고 자료 | 결과 자료   :2794-2802 · renderMaterials :1666-1779
  │   │    칸 머리 (editable) 「파일 추가」「링크 추가」 · 행 「떼기」
  │   └ section.block 「이력」 > TaskHistorySection         :2805-2808 · 정의 :190-313
  │        (안쪽 section.drawer-section > h4「활동·이력」 + 「이력 보기/접기」 + 필터 칩 + 목록 + 「변경 내용」)
  └ footer.scax-modal__foot                              ds/Modal.tsx:183 · 내용 WorkModals:1790-1888  → 4-4
겹 위 겹(Shell 의 형제로 그린다)
  · 담당자 변경 Modal size=sm                              :2811-2865
  · CompletionReportModal                                  :2872-2890
  · ConfirmModal「남은 단계가 있습니다」                      :2891-2905
  · ReasonPrompt 업무 취소 / 취소 제안 / 응답 / 재개 / 보완 요청   :2906-3016
  · TermsChangePrompt                                      :2950-2960
  · CreateWorkModal(하위 업무 생성)                          :3017-3036
```

- 값의 출처: 메타 줄은 `shown = detailTask ?? task`(`:1314`)를 읽는다. 상세 조회 `getTask` 가 오면 그 값이고, 아직이면 prop 이다(`:837-857`). 출처 줄만 `task.origin`(prop)을 읽는다(`:1996`).
- 권한 판정 변수(전부 이 함수 안)
  - `closed = state==="cancelled"` (`:796`)
  - `readOnly = access==="read_only"` (`:797`)
  - `editable = canManage && !closed && !readOnly` (`:798`)
  - `viewerDrives = !heldByNobody && !heldByOther && access!=="read_only"` (`:1105-1107`)
  - `requestTaskAccepted` (`:1094`)
  - `reviewed = Boolean(delivery) || origin.kind==="work_request"` (`:1092`)
  - `startBlocked` (`:1335`)
- DS 부품: `Modal`·`ConfirmModal`(`ds/Modal.tsx`) · `ChipRow`(`ds/Chip.tsx:61`) · `Badge` · `Button`·`IconButton` · `Icon` · `DateField` · `Select` · `Checkbox`·`FieldMessage` · `ProgressBar` · `Skeleton` · `SegmentedControl`(import `:6`). 화면 CSS 는 `styles/task-detail.css`(190줄, 전부 `.scax-td` 아래).

### 4-2. 「편집」 흐름
- **상태**: `const [metaEditing, setMetaEditing] = useState(false)` (`:749`). 단추는 머리 ChipRow 에 있다. `editable && relDraft === null` 일 때만 서고, 누를 때마다 켜고 끈다. 문구는 「편집」 ↔ 「편집 끝내기」(`:1905-1909` · `labels.ts` `taskDetail.edit/editDone`).
- **켜면 바뀌는 것 — 넷**

  | 필드 | 읽기 | 편집 | 줄 |
  |---|---|---|---|
  | 제목 | 머리 `h3`(그대로 남음) | 메타 맨 위 `input.meta__title-input` 추가 | `:1964-1974` |
  | 시작 예정일 | 사실 줄 글자 | 글자는 감추고 `.meta__edit` 안 `DateField` | `:1982`, `:2017-2027` |
  | 마감일 | 사실 줄 글자 | 위와 같음 | `:1985`, `:2028-2038` |
  | 업무 내용 | `p.desc` | `textarea.task-description` | `:2069-2081` |

  - 실제 시작일·실제 종료일·담당·결재·참조는 편집 중에도 글자로 남는다.
- **「업무 내용」 라벨이 두 번 나오는 원인**: 칸 머리 `div.cell__head > h5{taskDetail.description}`(=「업무 내용」, `:2068`)는 늘 선다. 편집 중에는 그 아래 `label.scax-field__label`「업무 내용」(`:2071`)이 하나 더 선다.
- **제목 입력**
  - `input` 에 `type` 이 없다(`:1967-1972`). 그래서 전역 `input:not([type]){width:100%;height:38px;padding:0 var(--scax-space-300);border…;font-size:body1}`(`components.css:737`)가 먼저 걸린다.
  - `.scax-td .meta__title-input`(`task-detail.css:119-123`, 명시도 0,2,0)이 그 위에 `padding:0; border:0; border-bottom:1px; font:inherit; font-size:19px; font-weight:700` 을 덮는다. **높이는 덮지 않아 38px 그대로**다.
  - 한편 머리 `h3.scax-modal__title` 에도 같은 제목이 그대로 남아 **제목이 두 번 보인다**(머리 + 입력칸).
  - 「잘려 보인다」의 실제 픽셀 원인(높이 38px 안의 19px·line-height 상속 등)은 렌더 없이 확정하지 못했다 → §8.
  - 참고: `.scax-td .meta__facts .date-field{display:inline-grid}`(`task-detail.css:125`)는 맞는 요소가 없다. DateField 는 `.meta__facts` 가 아니라 `.meta__edit` 안에 선다(`:2016`).
- **저장/취소 단추 위치**
  - 저장은 **푸터 「변경 저장」** 하나다(`:1819-1823`). 조건은 `editable && dirty` 이고 **`metaEditing` 과 무관**하다. `dirty` 는 네 값 중 하나라도 prop 과 다르면 참이다(`:806-810`).
  - **편집 「취소」(되돌리기) 단추는 없다.** 「편집 끝내기」는 입력칸만 접는다. 고친 값은 state 에 남고, 「변경 저장」도 계속 선다.
- **저장 경로**
  1. `save()`(`:1073-1088`): 빈 제목이면 「업무 제목을 입력해 주세요.」, 시작>마감이면 「시작 예정일은 마감일보다 늦을 수 없습니다.」 → `onError`
  2. 바뀐 필드만 담은 `TaskPatch`
  3. `onUpdate(current, patch)`
  4. 호출부 함수
     - 내 업무 `updateTaskFields` `MyWorkPage.tsx:519-531`
     - 홈 `TodayPage.tsx:225`
     - 캘린더 `update` `CalendarPage.tsx:594-608`
  5. 셋 다 `updateTask(task_id, version, patch)` → **`PATCH /api/tasks/{id}`** body `{expected_version, title?, description?, start_date? | clear_start_date:true, due_date? | clear_due_date:true}` (`api.ts:255-285`)
- **저장 뒤 갱신**
  - 내 업무: `reload()` → 토스트 「업무 내용을 저장했습니다.」(`MyWorkPage.tsx:519-531`). `reload` 가 열린 겹의 `task` 를 새 목록 값으로 바꾼다(`:356-372`).
  - 캘린더: `reload()` + `setTask(await getTask(id))` + 「업무 내용을 저장했습니다.」(+해제 건수, `CalendarPage.tsx:594-608`)
  - 상세 쪽: prop 이 바뀌면 입력 state 를 다시 맞춘다(`:821-829`, 쓰는 중이면 건너뜀). **`metaEditing` 은 저장 뒤에도 켜진 채 남는다** — `save` 가 끄지 않는다.

### 4-3. 「담당자 변경」과 「진행과 판단」
- **단추**: 「진행과 판단」 안 `div.handover > Button text sm「담당자 변경」`(`:2362-2369`). 조건은 `canAssign && !readOnly` 다.
  - `canAssign` 은 **내 업무에서만** 넘긴다: `detail.manage && canAssignTasks`(`MyWorkPage.tsx:1306`). `canAssignTasks` = 세션 역량 `task.assign`(`App.tsx:404`).
  - 홈·캘린더는 넘기지 않는다 → 기본 `false`(`:608`).
- **누르면**(`openHandover` `:1244-1256`)
  - 상세 위에 `Modal size="sm"` 「담당자 변경」이 겹친다(`:2811-2865`). 안에는 대상 `Select`(후보 = `GET /api/task-assignment-candidates`, `api.ts:1015-1017`, 처음 열 때 한 번 읽음)와 사유 `input`(선택)이 있고, 푸터는 「취소」「변경」이다.
  - 「변경」 → `reassignTask` → **`POST /api/tasks/{id}/reassign`** `{expected_version, assignee_id, reason?}`(`api.ts:357-367`)
  - 성공하면 토스트 「담당 변경을 제안했습니다. 상대가 수락할 때까지 기존 담당이 그대로입니다.」 → `settleVersion` → `readDetail` → `getTaskAssignments` 를 다시 읽는다(`:1264-1294`).
  - 실패는 모달 안 `FieldMessage` 에 낸다(`:2861`).
- **「진행과 판단」 덩어리가 서는 조건**(`hasProgressBlock` `:1569-1577`) — 여덟 중 하나라도 참이면 선다. 담당자 변경 말고도 아래가 이 덩어리 안에 선다.

  | # | 구획 | 조건 | 안의 것 | 줄 |
  |---|---|---|---|---|
  | 1 | 「완료 확인 대기」 notice | `awaitingReview`(파생 approval==="awaiting_review" 또는 delivery.status==="awaiting_review") | 문장 + 보고한 결과. 요청 행의 요청자(`viewerIsRecordRequester`)이고 열린 `task.delivery` 판단 항목이 있으면 「완료 인정」·「보완 요청」 | `:2250-2270` (항목 찾기 `:1116-1142`, 명령 `runActionCommand(accept/request_changes)` `:1145-1173`) |
  | 2 | 「보완 필요」 notice.danger | `delivery.status==="awaiting_revision" && last_reason` | 사유·회차 | `:2271-2277` |
  | 3 | 「담당 변경 대기」 notice | `assignments.pending` | 지금 담당·제안 대상·거절 사유 | `:2283-2295` |
  | 4 | 「응답 대기 제안」 notice | `proposals.pending[0]` | 취소 합의/조건 변경 내용. 담당자면 「동의」「동의하지 않음」, 제안자면 「제안 철회」 | `:2300-2339` |
  | 5 | 「아직 끝나지 않은 하위가 있습니다」 notice | `blockingChildren.length>0` | 하위 이름 단추(열기) + 사유 | `:2346-2361` |
  | 6 | 「담당자 변경」 단추 | `canAssign && !readOnly` | 위 | `:2362-2369` |
  | 7 | 「막힘 사유」 | `shown.block_reason` | 적힌 사유(검정 글자) | `:2370-2382` |
  | 8 | 「막힘 사유 입력」 | `isBlocking`(푸터 「막힘」을 누름) | 입력 + 「입력 취소」「막힘 처리」 → `onTransition(block, reason)` | `:2391-2425` · 제출 `:1186-1196` |

  - 상태별로 보면: `blocked` 면 7, `in_progress` 에서 「막힘」을 누르면 8, 요청 업무의 완료 보고 뒤면 1·2 다. 권한별로 보면: 1의 단추는 요청자, 4의 동의는 담당자, 4의 철회는 제안자, 6은 `task.assign` 다.

### 4-4. 푸터 단추 매트릭스 (`:1790-1888`)
- **`canManage === false` 이면 「닫기」 하나뿐이다**(`:1883-1887`). `canManage` 는 호출부가 정한다(4-7 표).
- `canManage === true` 일 때 각 단추의 조건(왼쪽부터 그 순서로 선다)

  | 단추 | 조건 | 핸들러 → API | 확인창 |
  |---|---|---|---|
  | 업무 취소 (text) | `!closed && !requestTaskAccepted && viewerDrives` `:1799` | `ReasonPrompt`(사유 **필수**, danger) `:2916-2933` → `onTransition(cancel, reason)` → `POST /api/tasks/{id}/cancel` `{expected_version, reason}` (`api.ts:443-453`) | 사유 입력 모달 |
  | 취소 제안 (text) | `!closed && requestTaskAccepted && viewerIsRequester && !pendingProposal` `:1806` | `ReasonPrompt` `:2935-2949` → `createTaskProposal(kind:"cancellation")` → `POST /api/tasks/{id}/proposals` (`api.ts:407-416`) | 사유 입력 모달 |
  | 조건 변경 제안 (text) | 위와 같음 `:1813` | `TermsChangePrompt` `:2950-2960` → `createTaskProposal(kind:"terms_change", payload)` | 입력 모달 |
  | (spacer) | — | `:1818` | — |
  | 변경 저장 | `editable && dirty` `:1819` | `save` → `PATCH /api/tasks/{id}` | 없음 |
  | 막힘 | `state==="in_progress"` `:1824` | `setIsBlocking(true)` → 「진행과 판단」 안 입력 → `POST /api/tasks/{id}/block` `{reason}` | 본문 안 입력 구획 |
  | 시작 (solid primary) | `state==="open"` · **disabled `busy‖startBlocked`** `:1833-1837` | `onTransition(start)` → `POST /api/tasks/{id}/start` | 없음 |
  | 완료 처리 (solid primary) | `(state==="in_progress"‖"open") && !reviewed` · **disabled `busy‖startBlocked`** `:1846-1852` | `complete()` `:1176-1182` → `POST /api/tasks/{id}/complete` | 미완 체크리스트가 있으면 `ConfirmModal`「남은 단계가 있습니다」(「그래도 완료」/「돌아가기」) `:2891-2905` |
  | (안내) `small.scax-blocked-note` | `startBlocked` `:1853` | — | — |
  | 완료 보고 (solid primary) | `(state==="in_progress"‖"blocked") && reviewed` `:1854` | `CompletionReportModal` → `POST /api/tasks/{id}/completion-report` (`api.ts:172-180`) | 입력 모달 |
  | 재개 (outlined sm) | `state==="blocked"` `:1859` | `onTransition(resume)` → `POST /api/tasks/{id}/resume` | 없음 |
  | 재개 (outlined sm) | `state==="done" && !reopenBlockedByApproval && (reviewed ? viewerIsRecordRequester : viewerDrives)` `:1872` | `ReasonPrompt`(사유 선택) `:2983-2998` → `reopenTask` → `POST /api/tasks/{id}/reopen` (`api.ts:390-395`) | 사유 입력 모달 |
  | 닫기 | `closed` `:1877` | `close` | — |

- **상태 × 자리로 펼친 결과** (`canManage=true` 기준. 「담당자」= `viewerDrives`, 「요청자」= `viewerIsRequester`/`viewerIsRecordRequester`. 「그 외」는 사실상 `canManage=false` 라 「닫기」만 선다)

  | state | 일반 업무(본인·배정) 담당자 | 요청 업무 담당자(`reviewed`) | 요청 업무 요청자(수락 후) |
  |---|---|---|---|
  | open | 업무 취소 · 시작 · 완료 처리 (+선행 막힘이면 둘 disabled + 안내) | 시작 | 취소 제안 · 조건 변경 제안 · 시작 |
  | in_progress | 업무 취소 · 막힘 · 완료 처리 | 막힘 · 완료 보고 | 취소 제안 · 조건 변경 제안 · 막힘 |
  | blocked | 업무 취소 · 재개 | 완료 보고 · 재개 | 취소 제안 · 조건 변경 제안 · 재개 |
  | done | 업무 취소 · 재개(최종 완료일 때) | — (승인 대기면 재개 없음) | 취소 제안 · 조건 변경 제안 · 재개(최종 완료 · 요청 행 요청자) |
  | cancelled | 닫기 | 닫기 | 닫기 |

  - ⚠ 시작·막힘·완료 처리·완료 보고·재개(blocked)는 **`viewerDrives`·요청자 여부를 보지 않고 `state` 만** 본다(`:1824,1833,1846,1854,1859`). 그래서 `canManage=true` 인 화면에서 요청자 자리에도 선다(최종 판정은 서버).
  - ⚠ 「업무 취소」는 `done` 에서도 선다 — 조건에 state 가 없다(`:1799`). 「변경 저장」은 위 표와 별개로 `dirty` 일 때 선다.
- **전이 결과 알림**: 내 업무 `transitionTask` 는 성공하면 토스트 「업무를 시작했습니다./완료 처리했습니다./막힘으로 표시했습니다./업무를 재개했습니다./업무를 취소했습니다.」를, 실패하면 서버 문장을 `onError`(오류 토스트)로 낸다(`MyWorkPage.tsx:501-517`). 홈 `TodayPage.tsx:207-223` 은 같고, 캘린더 `CalendarPage.tsx:573-592` 는 「상태를 바꿨습니다.」다.

### 4-5. 헤더 「AX」 단추
- 핸들러(`:1914-1922`): `canLeave()`(업로드 중이면 막고 오류 토스트 「파일 업로드가 끝난 뒤 이동할 수 있습니다.」) → `onAskAx(task)` → `onClose()`(상세를 닫는다).
- `onAskAx` = `App.tsx:313-327` `askAboutTask`
  1. `{resource_type:"task", resource_id, resource_version, label: title, pinned:true}` 를 AX 참고 자료 후보 맨 앞에 넣고 선택한다.
  2. 대화 초안이 비어 있으면 `'<제목>' 업무에 대해 알려줘.` 를 채운다.
  3. AX 패널을 연다(`setIsAxOpen(true)`). **보내지는 않는다.**
- 선택된 참고 자료는 채팅 입력 위 칩 「업무 · 제목」으로 보이고 떼기 단추가 있다(`features/chat/ChatDrawer.tsx:341-352`). 보낼 때 함께 실린다(`App.tsx:329-335`).
- **같은 기능의 다른 입구 — 없다.**
  - `askAboutTask` 를 쓰는 자리는 상세 세 호출부(`MyWorkPage.tsx:1302` · `TodayPage.tsx:421` · `CalendarPage.tsx:704`)가 넘기는 `onAskAx` 하나뿐이다(`App.tsx:407`, `sharedWorkProps.onAskAboutTask`).
  - `setSelectedContextKey(키)` 를 부르는 곳도 `App.tsx:323` 한 곳이다. 나머지는 초기화 `:232, :303` 와 떼기 `:678` 다.
  - 이웃 기능(같은 기능은 아님): 홈 「AX에게 오늘 업무 묻기」(`TodayPage.tsx:286-294`, `askAx(text)` 로 바로 보낸다) · 런처 오브(`App.tsx:612-624`).

### 4-6. 출처 배지와 링크
- 데이터: `task.origin: {kind, actor_role, actor, source:{type,id,title}|null}` (`lib/viewModels.ts:440-445`). 서버 `_origin_projection`(`backend/src/ax_workspace/modules/work/application.py:2458-2500`)이 만든다. 목록·상세 모두 싣는다(`:1093, :1165`).
- 배지 문구 `originSentence`(`WorkModals.tsx:384-390`) — **문구 4종**

  | 서버 갈래 | origin | 배지 | 링크 |
  |---|---|---|---|
  | 요청으로 생김 (`source_work_request_id`) | kind `work_request`, actor=요청자 | 「{요청자}가 보낸 업무」 | source `{type:"work_request", title: 요청 제목}` — **요청을 읽을 수 있을 때만** (`application.py:2474-2479`) |
  | AX 제안으로 생김 (`source_action_item_id`) | kind `self_created`, actor `null` | 「**AX 제안에서 생성됨**」 | source `{type:"action_item", id, title: subject_label(action)}` — `action.read` 역량이 있고 내 action 일 때만 (`:2480-2484, 2511-2519`) |
  | 직접 배정 | kind `direct_assignment`, actor=배정자 | 「{배정자}가 담당자를 지정함」 | 없음 |
  | (그 밖의 actor 있음) | — | 「{actor}가 만든 업무」 | — (현재 서버 갈래로는 나오지 않음) |
  | 본인 생성 | origin 자체가 없음 (`:2489-2492` continue) | 배지·줄 없음 | — |

  - actor 가 없고 source 도 못 읽으면(예: AX 제안인데 `action.read` 가 없음) origin 이 빠져 **출처 줄이 통째로 서지 않는다**(`application.py:2489-2492`).
- **링크 글자** = `source.title ?? "출처 보기"`(`:2004`)
  - AX 제안이면 서버 `subject_label(action)` 이고, 주석상 「만든 업무의 이름」이다(`application.py:2518`). 그래서 업무 제목과 같아 보인다(polish2 E2E-4 과 같은 사실).
- **링크가 가는 곳**: `onOpenSource` 를 넘기는 곳은 **내 업무 하나**다(`MyWorkPage.tsx:1314`).
  - `openSource` (`MyWorkPage.tsx:696-709`)
    - `action_item` → 같은 겹에 `ActionItemDrawer`(판단 상세)를 얹는다(`pushDetail({kind:"action"})`, `:1361-1374`).
    - `work_request` → `getWorkRequest` 로 읽은 뒤 `WorkRequestDetailDrawer` 를 얹는다.
    - 그 밖(`project` 등)은 조용히 돌아간다.
  - 홈·캘린더는 `onOpenSource` 를 안 넘긴다 → 링크 대신 `small.t-meta` 글자다(`:2007`).
- 출처 배지는 이 한 자리뿐이다. CSS 는 `.origin-chip`(`styles/screens-a.css:437`)과 `.scax-td .meta__facts + .origin-chip`(`task-detail.css:109-112`)이다.

### 4-7. 업무 상세를 여는 자리 전부
**`<TaskDetailDrawer` 를 그리는 화면은 3곳**이다. 다른 화면은 모두 내 업무로 넘겨서 연다.

| # | 입구 | 경로 | 그리는 화면 | `canManage` | `onOpenSource` / `canAssign` / `onBack` |
|---|---|---|---|---|---|
| 1 | 내 업무 「내 업무」 탭 표 행 | `MyWorkPage.tsx:1179-1182` → `openMyTask` `:628-643` | 내 업무 `:1297` | `canManageOwnTasks` | ○ / `task.assign` 이면 ○ / 겹≥2 |
| 2 | 내 업무 타임라인 보기 | `:1173` `openMyTask` | 〃 | 〃 | 〃 |
| 3 | 내 업무 우 레일(캘린더 레일) | `:1037-1039` `openMyTask` | 〃 | 〃 | 〃 |
| 4 | 내 업무 「보낸 업무」 행(업무만 있는 행) | `:1241` `openDerivedTask` | 〃 | **false** | ○ / × |
| 5 | 내 업무 「조직 업무」 표 | `:1258` `openDetail(manage:false)` | 〃 | **false** | 〃 |
| 6 | 내 업무 「완료」 탭 | `:1283` `openDerivedTask` | 〃 | **false** | 〃 |
| 7 | 업무 생성 뒤 「업무 열기」(다시 요청 모달 `onOpenTask`) | `:1459` `openDerivedTask` | 〃 | **false** | 〃 |
| 8 | 요청 상세 → 파생 업무 | `WorkModals.tsx:3868-3869, 3920` → `MyWorkPage.tsx:1382` `pushDerivedTask` | 〃 (겹 위에 얹음) | **false** | 〃 + 뒤로 |
| 9 | 판단 상세(ActionItemDrawer) → 파생 업무 | `features/action/ActionCenter.tsx:571-574` → `MyWorkPage.tsx:1373` | 〃 | **false** | 〃 + 뒤로 |
| 10 | 상세 안 관계 칸·하위·참고·자료 resource_ref | `WorkModals.tsx` `openTask` → `MyWorkPage.tsx:1308` `pushDerivedTask` | 〃 | **false** | 〃 + 뒤로 |
| 11 | 채팅 카드 「업무 열기」(ActionTaskCard `:583-584` · AxDraftCard `:330-331`) | `MessageList.tsx:313,321` → `ChatDrawer.tsx:311` → `App.tsx:740-745` `setFocusTaskId` → `MyWorkPage.tsx:680-684` `openDerivedTask` | 내 업무 | **false** | ○ / × |
| 12 | 프로젝트 우 패널 「업무 열기」 | `features/project/ProjectTaskPanel.tsx:264` → `ProjectPage.tsx:248-256, 413` → `App.tsx:578` `openTaskInWork` (`:142-148`) | 내 업무(화면 이동) | **false** | 〃 |
| 13 | 관계 그래프 노드·「업무 열기」 | `features/graph/RelationGraphPage.tsx:141, 410` → `App.tsx:604-607` | 내 업무(화면 이동) | **false** | 〃 |
| 14 | 홈 업무 행(세 목록) | `TodayPage.tsx:356, 365, 375` `setSelectedTask` | 홈 `:418` | `canManageOwnTasks` | × / × / × |
| 15 | 캘린더 카드 | `CalendarPage.tsx:505` `openTask` `:481-490`(`getTask`) | 캘린더 `:701` | `canManageOwnTasks` | × / × / × |
| 16 | 캘린더 업무 생성 뒤 「업무 열기」 | `CalendarPage.tsx:696` | 캘린더 | 〃 | 〃 |

- **회의 할 일**: 회의 상세에는 업무 상세를 여는 입구가 없다. 승격은 `CreateWorkModal`(요청)로 가고, 성공 문구만 낸다(`MeetingDetailPage.tsx:1289-1330`, 업무를 여는 호출 0건).
- **홈·내 업무의 AX 제안 모달**(`AxDraftModal` `TodayPage.tsx:434` · `MyWorkPage.tsx:1343`)은 `onOpenTask` 를 넘기지 않는다 → 「업무 열기」가 서지 않는다(`AxDraftCard.tsx:330`).
- **개편이 닿는 표면**: 그리는 컴포넌트는 1벌이고 호출부는 3곳(내 업무·홈·캘린더)이다. 열리는 입구는 16자리이고, 그중 `canManage=true` 로 열리는 곳은 1·2·3·14·15·16뿐이다.

### 4-8. 개편에 쓸 기존 부품

| 부품 | 파일:줄 | 쓰는 자리(호출, `ds/` 제외) | DS 시안(`.design-sync/previews`) |
|---|---|---|---|
| `Select`(단일 고르기 팝오버, `trigger` 갈아끼우기 가능) | `ds/Select.tsx:338` | **15** — `org/AccessDrawer` · `project/ProjectTaskPanel` · `project/ProjectRail` · `work/WorkModals` · `work/MyWorkPage` · `meetings/BookingModal` · `meetings/MemoComposer` | `Select.tsx` ○ |
| `MultiSelect` | `ds/Select.tsx:437` | 1 (`action/ActionMeetingCard.tsx:441`) | `MultiSelect.tsx` ○ |
| **상태 드롭다운 선례** — `Select` + 톤별 트리거 `scax-select__trigger--{neutral,positive,danger}` | `MyWorkPage.tsx:1483-1567` `TaskStateCell`(톤 표 `:1475-1481`) · `ProjectTaskPanel.tsx` `TaskStateValue`(`:296-383`) · CSS `components.css:48-55` | 2 | — |
| `DateField`(앱 달력 팝오버 · `onChange(iso)`) | `ds/DateField.tsx:17` (내부 `DatePicker` `ds/DatePicker.tsx:165`) | **16** — project/ProjectCreateModal · action/ActionTaskCard · action/CommandConfirmationForm · action/ActionMeetingCard · action/ActionCenter · work/WorkModals · report/DailyReportPage · meetings/MeetingEditModal · meetings/BookingModal | `DateField.tsx`·`DatePicker.tsx` ○ |
| 사람 고르기 | **전용 부품 없음** — `Select` 에 사람 목록을 options 로 넣는다: 담당자 변경 `WorkModals.tsx:2846` · 생성 담당 `:5424` · 결재 `:5497` | 3 | — |
| **토스트** | `ds/Modal.tsx:265` `Toast`(4초 · `persist` · `tone` success/error · `action`) | 3 — **공통 통 `App.tsx:637-650`** · `features/org/OrgPage.tsx:457` · `features/meetings/AttachModal.tsx:171` | `Toast.tsx` ○ |
| 토스트 띄우는 법 | `App.tsx:108-121` — `putNotice(kind, message)`. 갈래(error·success·stale)마다 한 줄만 남는다. 화면에는 `onNotice=setToast`(성공)·`onError=setError`(실패)로 내려간다(`App.tsx:397, 408`). 업무 상세도 `onNotice`·`onError` prop 으로 받는다(`WorkModals.tsx:679-680`) | `onNotice=` 류 전달 38건 | — |
| `ConfirmModal` | `ds/Modal.tsx:200` | 4 — org/OrgPage · work/WorkModals · work/MyWorkPage · meetings/MeetingListPage | `ConfirmModal.tsx` ○ |
| `ReasonPrompt`(사유 받는 작은 모달) | `WorkModals.tsx:3241` | 8 — action/AxDraftCard · work/WorkModals · work/MyWorkPage | — |
| `BlockReasonPrompt` | `WorkModals.tsx:3416` | 4 — ProjectTaskPanel · WorkModals · MyWorkPage · WorkViews | — |
| `Modal` / `Drawer` 골격 | `ds/Modal.tsx:135` / `:78` | Modal 7 · Drawer 2 | `Modal.tsx`·`Drawer.tsx` ○ |
| `Popover` | `ds/Popover.tsx:51` | 1 (`features/org/AxisHistoryPopover.tsx`) — 나머지는 ds 안 | `Popover.tsx` ○ |
| 인라인 편집 `InlineText` | `ds/InlineText.tsx:46` | §3-3 참조 | **없음** |
| 체크리스트 단계 제자리 수정(input · blur/Enter 저장 · Esc 취소) | `WorkModals.tsx:2139-2159` | 1 | — |

- `.design-sync/previews` 에 있는 것: Select · MultiSelect · DateField · DatePicker · Toast · Modal · ConfirmModal · Drawer · Popover · StatusNote · Badge · Chip 등(전체 37종). **InlineText·사람 선택기·상태 드롭다운 시안은 없다.**

### 4-9. 상태 표시 문구·색

| state | 문구 `taskStateLabel`(`lib/labels.ts:3-9`) | 상세 머리 `StatusText` 색(`styles/components.css:468-476`) | 배지 톤 `taskStateTone`(`labels.ts:19-25`) | 드롭다운 트리거 톤(`MyWorkPage.tsx:1475-1481`) |
|---|---|---|---|---|
| open | 시작 전 | 기본 `ink-assistive` + 점(currentColor) `:468-469` | neutral | `--neutral` |
| in_progress | 진행 중 | `progress-ink`/점 `progress` `:470-471` | accent | (기본) |
| blocked | 막힘 | `danger` `:474-475` | danger | `--danger` |
| done | 완료 | `accent` `:472-473` | positive | `--positive` |
| cancelled | 취소 | 점만 `ink-disabled` `:476` | neutral | `--neutral` |

- 상세 머리의 「상태 칩」은 **Badge 가 아니라 `span.status.{state}`**(`WorkModals.tsx:321-323`)다. 점과 글자로 그린다.
- `taskStateTone[…]` 을 쓰는 곳(6): `features/calendar/ScheduleCard.tsx:72` · `features/project/ProjectTaskPanel.tsx:240, 324, 332, 437` · `features/project/ProjectRail.tsx:149`.
- 파생 표시는 상태가 아니다: `derivedAssignmentLabel`(수락 대기·담당 변경 대기)·`derivedApprovalLabel`(확인 대기…)(`labels.ts:33-40`).

---

## 5. R5 선행업무 안내

### 5-1. 두 안내의 자리·조건·데이터
- **본문 배너**: `WorkModals.tsx:2054-2059`
  - `section.drawer-section.notice.danger[aria-label="시작할 수 없습니다"] > h4「시작할 수 없습니다」 + p{blockedBanner}`
  - 자리는 `.meta` 바로 다음, 「업무 정보」 앞이다. `.scax-td` 의 직계 자식이다.
  - 본문 `blockedBanner`(`:1351-1358`)는 `<b>{막는 제목 최대 3개, 「, 」로 이음}</b>` + 「이 끝나지 않았습니다.」(+ 못 읽는 미완이 있으면 ` 끝나지 않은 선행 N건`)이다. 문구는 `labels.ts:446, 452-456`.
  - 스타일: `.drawer-section.notice`(`screens-a.css:281-283`) + `.notice.danger`(`:284` 빨간 테두리·danger-soft 바탕) + `.scax-td .drawer-section.notice{margin-top:14px}`(`task-detail.css:188`)
- **푸터 문구**: `WorkModals.tsx:1853`
  - `small.t-meta.scax-blocked-note{blockedText}`, CSS `components.css:869`(`display:block; color:danger`)
  - `blockedText = predecessorsUnfinishedText(제목들)` = 「끝나지 않은 선행업무가 있습니다: A, B」(`labels.ts:338-340`, 제목 개수 제한 없음)
- **조건 — 둘 다 `startBlocked`**(`:1335`) = `startBlockedByPredecessors(related)` = `state==="open" && blockingPredecessorsOf(...).length>0`(`features/work/workRows.ts:147-149`)
  - `blockingPredecessorsOf` = `predecessors` 중 `title!==null && state∉{done,cancelled}`(`workRows.ts:113-117`)
  - **볼 수 없는 선행(title null)은 막는 판정에서 빠진다**(OQ-709). 배너에는 건수만 덧붙는다.
- **데이터**: `related.predecessors` ← 상세 조회 `getTask` 의 `predecessors`(`:845`). 조회 전에는 prop 값이다(`:735`). 목록 투영에는 `predecessors` 가 없다(`MyWorkPage.tsx:618-622` 주석).

### 5-2. 막힌 상태에서 누르면
- **상세 푸터**: 「시작」(`:1834`)·「완료 처리」(`:1849`) 모두 `disabled={busy || startBlocked}` 다 → **눌리지 않는다.** 서버 호출이 없고 에러 표시도 없다. 왜 막혔는지는 바로 옆 `scax-blocked-note` 와 본문 배너가 말한다.
- **목록 행 `TaskQuickActions`**: `WorkModals.tsx:3471-3472, 3487-3504` 도 같은 disabled 다. 다만 목록 투영에 `predecessors` 가 없어서(위) 행에서는 `startBlocked` 가 사실상 거짓이다(코드상 추론). 그러면 서버 거절 경로를 탄다.
- **상태 드롭다운 두 곳은 미리 막지 않는다**
  - 내 업무 표 상태 칸 `TaskStateCell`(`MyWorkPage.tsx:1483-1567`)
  - 프로젝트 우 패널 `TaskStateValue`(`ProjectTaskPanel.tsx:296-383`)
  - 둘 다 `allowedTaskTransitions` 만 보고 바로 `onTransition` 을 보낸다.
- **서버 거절**
  - `backend/src/ax_workspace/modules/work/lifecycle.py:130-140`: `open` 에서 `in_progress`/`done` 으로 갈 때 미완 선행이 있으면 `TaskPredecessorsUnfinished`(409, `errors.py:175-187`)를 던진다. 문장은 「끝나지 않은 선행업무가 있습니다: {제목 최대 3}」이다.
  - FE `request` 가 `ApiError(status, detail)` 로 던진다(`api.ts:147-148`).
  - 호출부 `transitionTask` 의 catch 가 `onError(message)`(`MyWorkPage.tsx:511-513` · `TodayPage.tsx` · `CalendarPage.tsx:584-586`)로 넘긴다.
  - → **`App.tsx` 공통 통의 오류 토스트**(`role="alert"`, 4초, `Toast tone="error"`)가 선다(`App.tsx:118, 637-650` · `ds/Modal.tsx:294-305`).
  - 즉 「상태를 바꾸려 할 때 토스트로 알리는」 경로가 드롭다운에는 **지금도 서 있다.**

### 5-3. 같은 막힘 안내가 나오는 다른 화면 전부

| 자리 | 형태 | 줄 |
|---|---|---|
| 업무 상세 본문 배너 | `section.notice.danger` 「시작할 수 없습니다」 | `WorkModals.tsx:2054-2059` |
| 업무 상세 푸터 | `small.scax-blocked-note` 「끝나지 않은 선행업무가 있습니다: …」 | `WorkModals.tsx:1853` |
| 내 업무 표 행 액션 `TaskQuickActions` | 같은 `small.scax-blocked-note` | `WorkModals.tsx:3515` (호출 `MyWorkPage.tsx:1096`) |
| 업무 상세 「연관 업무」 선행 칸 | 미완 선행만 `Badge tone=danger {상태}` · 못 읽는 것 「🔒 비공개 선행 업무 N건」 · 셈 「N · 미완 M」 | `WorkModals.tsx:2628-2683` · `labels.ts` `precedingCount`·`hiddenPreceding` |
| 상태 드롭다운 두 곳 · 캘린더/홈 상세의 전이 실패 | 서버 문장 → 공통 오류 토스트 | 위 5-2 |
| 연결 편집의 프로젝트 칸 | 「선행업무를 먼저 비워야 프로젝트를 바꿀 수 있습니다.」(선행 → 프로젝트 잠금. 시작 막힘과 다른 안내) | `WorkModals.tsx:2510` · `labels.ts:343` |

- grep 근거: `predecessorsUnfinishedText` 호출 2(`:1336`, `:3472`) · `scax-blocked-note` 2 + CSS 1 · `blockedHeading` 사용 2. AX 카드·채팅·프로젝트·캘린더 화면에는 이 안내가 없다(`선행|predecessor` grep 결과 파일 12개 중 안내 문구를 그리는 파일은 `WorkModals.tsx` 하나).

---

## 6. R6 업무 상세 헤더 아래 여백

### 6-1. 칩 줄 아래 ~ 「담당」 줄 위의 CSS 전부
- DOM 순서
  - 머리 `header.scax-modal__head`(`ds/Modal.tsx:171`) › `div[style="flex:1 1 auto;min-width:0"]`(`:175`) › `small.modal-kicker` · `h3.scax-modal__title` · `div.scax-chip-row`(headerExtra, `ds/Chip.tsx:62`)
  - 본문 `div.scax-modal__body`(`:182`) › `div.scax-td`(`WorkModals.tsx:1952`) › `div.meta`(`:1962`) › `div.meta__left` › `div.meta__facts` › 첫 `span` 「담당」(`:1976`)
- 토큰: `--scax-space-100` 4 · `-200` 8 · `-400` 16 · `-500` 20 · `-600` 24 (px 리터럴, `styles/scax.css:52-61`)

| 선택자 | 파일:줄 | 값 |
|---|---|---|
| `.scax-modal__head` | `styles/components.css:257` | **padding 20px 24px**(`--scax-space-500` `--scax-space-600`) · gap 8 · `align-items:center` · **border-bottom 1px** line-weak |
| `.scax-modal__head .modal-kicker` | `components.css:260` | block · margin-bottom 4 · 12px |
| `.scax-modal__title` | `components.css:261` | 17px / lh 1.412 · margin 0(전역 리셋 `shell.css:43`) |
| `.scax-chip-row` | `components.css:428` | gap 8 · **margin-top 8** · margin-bottom 없음 |
| 머리 안 div | `ds/Modal.tsx:175` 인라인 style | padding·margin 없음 |
| `.scax-modal__body` | `components.css:263` | **padding 20px 24px** · gap 16 · overflow-y auto |
| `.scax-modal__body>*` | `components.css:264` | flex-shrink 0 |
| `.scax-td` | (규칙 없음) | 스코프 클래스일 뿐 |
| `.scax-td .meta` | `styles/task-detail.css:96-99` | flex · gap 12 · **padding 0 0 14px**(위 0) · border-bottom 1px |
| `.scax-td .meta__left` | `task-detail.css:118` | 여백 없음 |
| `.scax-td .meta__facts` | `task-detail.css:101-104` | flex-wrap · gap 6px 14px · 12px · margin 없음 |
| (편집 중만) `.scax-td .meta__title-input` | `task-detail.css:119-123` | margin-bottom 6 — 「담당」 위에 입력칸이 끼어든다 |
| 이후 참고: `.scax-td .meta__facts + .origin-chip` | `task-detail.css:109` | margin 8px 0 4px |
| 이후 참고: `.scax-td .block` | `task-detail.css:17` | margin-top 22 |

- `:has()` 나 `.scax-modal … .scax-td` 를 묶은 규칙은 **없다**.
- **px 합(읽기 상태)**

  ```
  ChipRow margin-bottom          0   components.css:428 (margin-top 만)
  head padding-bottom           20   components.css:257
  head border-bottom             1   components.css:257
  body padding-top              20   components.css:263
  .scax-td / .meta 위 여백        0   (규칙 없음) · task-detail.css:97 「0 0 14px」
  .meta__left / .meta__facts     0   task-detail.css:118, 101-104
                               ----
                                41px
  ```

  - 칩 줄 안에 「편집」·「AX」(`scax-button--sm` 높이 32, `components.css:11`)가 있으면 줄 높이는 32px 이다. 22px 배지·상태 글자는 가운데 정렬되어(`components.css:428` `align-items:center`), **배지 아래 끝 기준으로는 약 46px** 이 된다.
  - 단추가 없는 읽기 전용(`canManage=false`·AX 없음)이면 줄 높이가 22px 이고 41px 그대로다.
  - 「담당」 12px 글자의 line-height 가 위로 1~2px 를 더한다(렌더 미확인).
- 머리 전체 높이 구성(참고): padding 20 + kicker(12px·lh)+4 + 제목 약 24 + 칩 줄 margin-top 8 + 칩 줄 22~32 + padding 20.

### 6-2. 같은 공용 규칙을 쓰는 다른 모달 — 13 표면
- **`<Modal` 직접 호출 7**

  | # | 파일:줄 | 이름 |
  |---|---|---|
  | 1 | `features/project/ProjectManageModal.tsx:53` | 프로젝트 관리 (md) |
  | 2 | `features/project/ProjectCreateModal.tsx:74` | 프로젝트 만들기 (md) |
  | 3 | `features/action/AxDraftCard.tsx:526` | AX 초안 모달 `axDraftCard.modalTitle` (sm) |
  | 4 | `features/work/WorkModals.tsx:2817` | 담당자 변경 (sm) |
  | 5 | `WorkModals.tsx:3173` | 완료 보고 (md, kicker 「완료 보고」) |
  | 6 | `WorkModals.tsx:3772` | 업무 요청 상세 (기본 880, headerExtra ChipRow `:3841`) |
  | 7 | `WorkModals.tsx:5232` | 새 업무 추가/요청 (`className="scax-modal--create"`, body padding 0 으로 덮음 `components.css:808`) |

- **Shell 경유 2**
  - 업무 상세 `WorkModals.tsx:1786`(늘 Modal)
  - 판단 상세 `features/action/ActionCenter.tsx:423`(기본 `drawer` `:329`): 내 업무 `MyWorkPage.tsx:1337, 1363` 에서는 Modal, 홈 `TodayPage.tsx:444` 에서는 Drawer
- **`<ConfirmModal` 4** (`.scax-modal--sm`, `ds/Modal.tsx:200-247`)
  - `features/org/OrgPage.tsx:444`
  - `WorkModals.tsx:2892`「남은 단계가 있습니다」
  - `MyWorkPage.tsx:1411`「요청을 철회할까요?」
  - `features/meetings/MeetingListPage.tsx:295`(회의 삭제)
- `ds/Modal.tsx` 밖에서 `scax-modal` 을 손으로 쓴 JSX: **0**
- 비교: `<Drawer` 직접 2(`features/org/AccessDrawer.tsx:48` · `features/meetings/MaterialDrawer.tsx:57`)는 `scax-drawer__*` 라 무관하다. 옛 `.modal-backdrop/.modal-head` 손마크업 15자리(`ReasonPrompt` `WorkModals.tsx:3287` · `TermsChangePrompt :3360` · `MeetingEditModal` · `BookingModal` · `ShareModal` · `AttachModal` · `MeetingDetailPage.tsx:1373/1398/1428` · `AssistantCharacterPicker` 등)도 이 규칙과 무관하다.
- **머리에 ChipRow 를 얹는 모달**은 업무 상세 · 업무 요청 상세 2개다. 완료 보고는 ChipRow 가 본문에 있다(`:3221`).

---

## 7. grep 개수표 (`frontend/src`, `*.test.*` 제외)

| 요청 | 심볼 / 문자열 | 개수 | 비고 |
|---|---|---|---|
| R1 | `보고를 한 흐름으로` | 1 | 저장소 전체 |
| R1 | `조직의 업무를 하나의 원장에서` | 1 | 저장소 전체 |
| R1 | `login-brand` 규칙 | `screens-a.css` 4 + `components.css:713` 1 | |
| R1 | `document.title` | 0 | |
| R2 | `<a` + `scax-button` | 3 | 크기 modifier 없는 것 1 |
| R2 | `meetingExportUrl` / `export?format` | 2 / 1 | 정의 1 + 사용 1 |
| R2 | `target="_blank"` | 6 | 운영 5 + dev 1 |
| R2 | `window.open` | 1 | + 주석 1 |
| R2 | `createObjectURL` · `download` 속성 | 0 · 0 | |
| R2 | `ContentUrl` / `AttachmentUrl` | 7 / 4 | |
| R2 | `src-tauri` 의 `on_download\|on_new_window\|download` | 0 | |
| R3 | 「제목 없는 회의」 문자열 | 1 (+주석 2) | 테스트 4줄 |
| R3 | 「제목 후보」 문자열 | 1 (+주석 1) | 테스트 2줄 |
| R3 | `meetingScreen.noTitle` | 5 | |
| R3 | `updateMeetingInfo` | 정의 1 · 사용 1(`MeetingEditModal`) · import-only 1(`MeetingDetailPage`) | |
| R3 | `<InlineText` | 2 | `AgendaBlock.tsx` |
| R3 | `contentEditable` | 1 | `ds/InlineText.tsx` |
| R4 | `<TaskDetailDrawer` | 3 | 내 업무·홈·캘린더 |
| R4 | 업무 상세를 여는 입구 | 16 | §4-7 |
| R4 | `onAskAboutTask` 를 넘기는 자리 / `askAboutTask` 정의 | 3 / 1 | |
| R4 | `aria-label="AX에게 이 업무 묻기"` | 1 | |
| R4 | `setSelectedContextKey(키)` | 1 | `App.tsx:323` |
| R4 | `originSentence` | 정의 1 · 사용 2 | `WorkModals.tsx:2000` |
| R4 | `onOpenSource` 를 넘기는 호출부 | 1 | 내 업무 |
| R4 | `<Select` / `<MultiSelect` | 15 / 1 | `ds/` 제외 |
| R4 | `<DateField` | 16 | |
| R4 | `<ConfirmModal` / `<ReasonPrompt` / `<BlockReasonPrompt` | 4 / 8 / 4 | |
| R4 | `<Toast` | 3 | 공통 통 1 |
| R4 | `<Modal` / `<Drawer` | 7 / 2 | |
| R4 | `taskStateTone[` 사용 | 6 | 3파일 |
| R4 | `metaEditing` | 선언 1 · 읽는 자리 6 | `:749` · `:1907, 1964, 1982, 1985, 2015, 2069` |
| R5 | `predecessorsUnfinishedText` | 정의 1 · 호출 2 | |
| R5 | `startBlockedByPredecessors` | 정의 1 · 호출 2 | |
| R5 | `scax-blocked-note` | JSX 2 · CSS 1 | |
| R5 | `taskDetail.blockedHeading` | 사용 2 (같은 구획) | |
| R5 | `notice danger` | 4 | 선행 1 · 보완 필요 1 · 보고 막는 하위 1 · 일일보고 1(무관) |
| R6 | `.scax-modal__head`·`__body` 를 쓰는 표면 | 13 | Modal 7 · Shell 2 · ConfirmModal 4 |
| R6 | `.scax-td` 규칙 | `task-detail.css` 전부 | `.scax-td` 자체 규칙 0 |

---

## 8. 조사 한계

- **R2 — Tauri 웹뷰가 첨부 응답을 어떻게 처리하는지 코드로 확정하지 못했다.**
  - 확인된 사실
    - 같은 origin 이동은 허용된다(`lib.rs:384-406`).
    - 쿠키가 실린다.
    - 서버가 `Content-Disposition: attachment` 를 준다.
    - 앱에 `on_download`·새 창 핸들러·dialog/fs 플러그인이 없다.
  - 확정하지 못한 것: 그 뒤 WKWebView(wry 기본값)가 파일을 저장하는지, 응답을 버리는지, 창 안에 HTML 을 여는지(이 경우 `on_page_load` Started → `clear_window` 가 돈다).
  - `target="_blank"` 링크 5종(업무 자료·요청 첨부·근거 원본·AX 답변 링크)이 셸에서 무엇을 하는지도 같은 이유로 미확정이다. 앱을 띄워 보지 않았다(금지 사항).
- **R4-2 — 제목 입력이 「잘려 보이는」 픽셀 원인은 렌더 없이 확정하지 못했다.**
  - 코드로 확인된 것
    - 입력칸에 `type` 이 없어 전역 `height:38px` 가 남는다(`components.css:737`). 그 위에 19px·bold 를 얹는다(`task-detail.css:119-123`).
    - 같은 제목이 머리 `h3` 에도 남는다.
    - 머리 `.scax-modal__title` 의 말줄임 여부는 `components.css:261` 에 `nowrap`/`ellipsis` 가 없다(회의 상세 `.scax-detail__title` 과 다름).
  - 실제 화면에서 무엇이 잘리는지는 브라우저 확인이 필요하다.
- **R4-4 — 표의 「요청 업무 요청자」 열은 `canManage=true` 로 상세가 열린다는 전제다.**
  - 실제로 요청자는 보통 「보낸 업무」에서 `openDerivedTask`(`manage:false`)로 연다 → 푸터는 「닫기」뿐이다.
  - 요청자가 `canManage=true` 로 같은 업무를 여는 길(내 업무 목록에 그 업무가 들어오는 경우)이 실제 데이터에서 생기는지는 서버 목록 규칙(BE 몫)을 따른다.
- **R5-2 — 목록 행의 `startBlocked` 가 늘 거짓이라는 판단은 코드 주석에 근거한 추론이다.** 근거는 `MyWorkPage.tsx:618-622` 의 「목록 투영에는 `predecessors` 도 … 없어서」다. 목록 응답 스키마에 `predecessors` 가 정말 없는지는 BE 조사로 확인해야 한다.
- **R6 — px 는 CSS 값의 산술**이다. 실제 렌더된 줄 높이(폰트 메트릭·line-height)는 재지 않았다.
- **R1 — 운영 화면의 실제 문구**는 이 커밋(`d1b5137`) 기준이다. 운영 배포본과 같은지는 확인하지 않았다.
- **서버 측 권한 판정**(누가 실제로 시작·취소·재개할 수 있나)은 FE 조건만 적었다. 서버 판정은 BE 리포트가 정본이다.

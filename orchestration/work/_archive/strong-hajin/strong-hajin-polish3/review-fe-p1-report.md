# 리뷰 리포트 — strong-hajin-polish3 / frontend · WORK-010 Phase 1 (2026-10-04)

## 판정: WARN

FAIL 0 · WARN 4. WP Phase 1 체크박스 **13개 전부 PASS** 다.
InlineText IME 가드는 다른 사용처를 깨지 않는다. 같은 규칙이 저장소에 이미 여섯 자리 있어, 계약 밖 변경으로 받아도 된다.
WARN 넷은 다음과 같다.
- 테스트가 확인한다고 말하는 것을 실제로는 확인하지 못하는 자리 둘
- 남은 CSS 한 줄
- 긴 제목의 줄바꿈 동작이 읽기 전용과 편집 가능 화면에서 달라지는 점

## 검수 범위

- 대상: 코드 워크트리 `Strong_hajin/strong-hajin-polish3`, base `d1b5137` 의 미커밋 diff 중 Phase 1 파일만
  - `frontend/src/features/auth/LoginPage.tsx` · `LoginPage.test.tsx`
  - `frontend/src/features/meetings/MeetingDetailPage.tsx` · `MeetingTitle.test.tsx`(신규, untracked) · `MeetingAfter.test.tsx`
  - `frontend/src/lib/labels.ts`(회의 제목 키 `:930-935` 만)
  - `frontend/src/ds/InlineText.tsx`
  - 제외: `src-tauri/Cargo.*` 등 Phase 3 파일
- 기준: WP `work-010-polish3.md` Phase 1(1-1·1-2·1-3·검증) · `fe-p1-worker-report.md` · fe-survey §1~§3 · be-survey §3
- 실행한 검사
  - diff 정독
  - 서버 응답 모양 대조: `PATCH /api/meetings/{id}` → `update_meeting` → `update_info` → `_detail`. `GET` 과 같은 모양이다(`backend/.../bootstrap/application.py:1700-1709`, `modules/meetings/application.py:291-293`, `:533`)
  - `can_edit_info` 의 출처: `policy.py:233` → `application.py:1792` → `viewModels.ts:1251`
  - grep: `InlineText` 사용처 · `isComposing` · `제목 후보`/`title_candidate` · 옛 로그인 문구 · `.login-brand`
  - 테스트(직렬): `npx vitest run --no-file-parallelism MeetingTitle MeetingAfter LoginPage MeetingLive MeetingDetail MeetingWorkspace` → **6 files · 154 passed · 0 failed**
  - 전체 스위트·tsc·build 는 워커 보고 수치를 인용만 했다(전체 실패 5 = 기준선 5, tsc 0, build 성공). 다시 돌리지 않았다

## 위반 (FAIL 사유)

없음.

## 경미 (WARN)

- **W1 · 조용히 통과하는 단언** `MeetingTitle.test.tsx:175` — 「응답을 세운다」를 `findByText("DB AX 전환 범위")` 로 확인한다.
  - `InlineText` 는 보낸 값을 응답이 오기 전부터 그린다(`sent`, `InlineText.tsx:84,163`). 그래서 이 단언은 `setRecord` 가 없어도 **보내는 순간** 통과한다.
  - 목 응답이 입력과 같은 제목이라, 응답 값이 화면에 섰는지도 구별되지 않는다.
  - 다만 후보 [적용] 테스트(`:269` 「후보 줄이 사라진다」)는 `setRecord` 가 있어야만 통과한다. 경로 자체는 간접적으로 잠겨 있다.

  권장: 목 응답 제목을 입력과 다르게 하거나(예: 서버가 다듬은 값), 정착 뒤에도 그 글자가 남는지 단언한다.
- **W2 · 연타 방지 무테스트** `MeetingDetailPage.tsx:565`(`claim("title")`) · `:1012`(`disabled={isBusy("title")}`) — 연타를 막는 장치는 있는데 테스트가 0건이다. WP 1-3 체크박스는 아니고 리뷰 브리프 §3-3 항목이다.
  - 코드 흐름은 맞다. 같은 키가 돌면 `claim` 이 거짓을 내고 `throw new Error("busy")` 한다. InlineText 는 그것을 삼키고 원래 값으로 돌아간다. [적용]은 `.catch(() => undefined)` 로 조용히 끝난다. 둘 다 토스트가 없다.
  - 권장: [적용] 두 번 클릭 → `updateMeetingInfo` 1회를 확인하는 테스트 한 건.
- **W3 · 남은 CSS** `styles/screens-a.css:71` `.login-brand p {…}` — 설명 `p` 를 지워 맞는 요소가 없는 규칙이다. 동작 영향은 0.
  - 참고: 새 h1 문구는 `LoginPage.tsx:68` 에 직접 박혀 있다. 옛 문구도 그랬으므로(기존 패턴) 위반으로 세지 않는다.
- **W4 · 긴 제목이 화면에 따라 다르게 보인다** `workspace.css:16`(`.scax-detail__title{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}`) vs `components.css:769`(`.scax-inline-text{display:inline;white-space:pre-wrap}`)
  - 편집 가능한 회의(`can_edit_info`)에서는 제목이 InlineText span 안에 들어간다. span 의 `pre-wrap` 이 부모의 `nowrap` 을 이기므로, 긴 제목이 **말줄임 없이 두 줄 이상으로 접힐 수 있다**. h2 에 높이 제한이 없어 머리 줄이 높아진다.
  - 읽기 전용 회의(진행 중·참석자 아님 등)는 지금처럼 한 줄 말줄임이다.
  - 같은 제목이 회의 상태에 따라 한 줄로 서거나 두 줄로 선다. 렌더로 확인하지 않은 CSS 추론이다. 아래 「실물 자리」 1번.

## InlineText IME 가드 — 다른 사용처 영향 · 계약 밖 수용 여부

- 바뀐 것은 `InlineText.tsx:198` 한 줄이다. 편집 중 Enter 이면서 `nativeEvent.isComposing` 이 참일 때 **저장만 건너뛴다**.
  - `preventDefault` 는 그대로 앞에서 돈다. 조합 Enter 는 줄바꿈도 저장도 하지 않는다.
  - 닫힌 상태의 Enter(열기)·Esc·blur 분기는 손대지 않았다.
- 사용처 셋
  - `AgendaBlock.tsx:138` 안건 제목
  - `AgendaBlock.tsx:189` 메모 줄
  - `MeetingDetailPage.tsx:993` 새 회의 제목

  조합이 아닌 Enter·blur·Esc 는 예전과 같다. 회귀 테스트 `MeetingLive.test.tsx`(85건, InlineText 사용 테스트 포함)가 통과했다.
- 같은 규칙이 이미 여섯 자리에 있다(`ChatDrawer.tsx:366` · `RelationGraphPage.tsx:200` · `WorkModals.tsx:2153` · `:2212` · `:4167` · `:5541`). 부품 하나가 그 관례를 따라가는 변경이고 계약 세 줄(입력칸 없음·글자 안 움직임·캐럿만)도 건드리지 않는다. **받아도 된다.**
- ⚠ 남는 확인: 데스크톱 앱의 macOS 웹뷰(WebKit)는 조합을 끝내는 Enter 에서 `isComposing` 을 거짓으로 줄 수 있다(조합 종료가 keydown 보다 먼저 온다).
  - 그 경우 이 가드는 **아무것도 하지 않는다.** 결과는 예전 동작(그 Enter 로 저장)과 같다. 새 문제가 생기지는 않지만 개선도 없다.
  - 실물 자리 3번에서 Chrome·데스크톱 앱을 각각 한 번씩 확인하기를 권한다.

## `saveTitle` 점검 (브리프 §3-3)

| 무엇 | 결과 | 근거 |
|---|---|---|
| 응답으로 바로 세운다 | PASS | `MeetingDetailPage.tsx:567` `setRecord(await updateMeetingInfo(...))`. PATCH 응답은 `GET` 과 같은 `_detail` 이다(제목만 보내면 회의실 동기화 분기를 건너뛴다, `application.py:1705-1706`) |
| 연타 방지 | PASS(테스트 없음 — W2) | `:565` `claim("title")` 은 ref 잠금이라 같은 tick 연타도 막는다(`:545-549`). [적용]은 `disabled={isBusy("title")}`(`:1012`) |
| 실패 원복 | PASS | `:570-573` `onError(서버 문장)` 뒤 다시 던진다 → InlineText 가 `sent` 를 비워 `value` 로 돌아간다(`InlineText.tsx:164-166`). 테스트 `MeetingTitle.test.tsx:230-241` |
| 목록 갱신 | PASS | `:569` `onMeetingChanged?.()` → `MeetingWorkspace.tsx:128` `reloadList` → `listReloadToken` → `MeetingListPage.tsx:88` 다시 읽기. 상단 제목은 `record` 가 바뀌면 `:300` effect 가 다시 돈다 |
| 권한 없으면 입력·[적용]이 안 선다 | PASS | 입력은 `:992` `meeting.can_edit_info ? <InlineText/> : 글자`, [적용]은 `:1009` `meeting.can_edit_info &&` 안에만 있다. 테스트 `:243-250`(클릭해도 contenteditable 0) · `:274-278`(버튼 0). `can_edit_info` 는 서버 값이다(참석자 + 예정·완료, `policy.py:233`) |
| 실패 시 토스트 | PASS | `onError` → `MeetingWorkspace` → App 공통 오류 토스트(기존 경로) |

## WP 체크박스 판정

**1-1 R1 로그인**

| 계약 | 판정 | 근거 |
|---|---|---|
| h1 = 「메디솔브 AX 프로젝트」 | PASS | `LoginPage.tsx:68` · 테스트 `LoginPage.test.tsx:17-26` |
| 설명 `p` 삭제(빈 요소 없음) · 워드마크·레이아웃·900px 숨김 유지 | PASS | diff 는 `p` 한 줄 삭제뿐이다. `.login-brand{display:none}` 두 자리(`screens-a.css:116` · `components.css:713`)는 손대지 않았다. 테스트가 `p` 없음과 워드마크를 단언한다. 남은 CSS 는 W3 |
| 문서 title·Tauri 창 제목 불변 | PASS | `index.html`·`src-tauri` 의 Phase 1 변경 0 |

**1-2 R2a 내보내기**

| 계약 | 판정 | 근거 |
|---|---|---|
| 옆 단추와 같은 sm·같은 변형, 동작 불변 | PASS | `MeetingDetailPage.tsx:1060` 에 `scax-button--sm` 만 더했다. href 는 같고 target 은 없다. 테스트 `:298-308` 이 「공유」 단추와 같은 클래스임을 대조한다 |
| 다른 두 `<a>`(`MaterialDrawer` lg · `MessageList` sm) 불변 | PASS | diff 0 |

**1-3 R3 회의 제목**

| 계약 | 판정 | 근거 |
|---|---|---|
| `can_edit_info` 면 클릭 → 그 자리 인라인(InlineText) · Enter·blur 저장 · Esc 취소 · 빈 값/안 바뀐 값 미전송 · 실패면 원래 값 + 오류 토스트 | PASS | `:992-998` · InlineText 계약(`:155-167`). 테스트 `:154-241` 이 일곱 갈래를 다룬다(W1 참고) |
| 아니면 글자만 | PASS | `:999-1001` · 테스트 `:243-250` |
| 제목이 비면 「제목 없는 회의」, 열면 빈 칸 | PASS | `value={meeting.title ?? ""}` + `placeholder` · 테스트 `:252-258`. 색이 흐린 회색(`--empty`)으로 바뀐다 — 실물 자리 2번 |
| 제목 후보 「제목 후보: {후보} [적용]」 · [적용] = `PATCH {title: 후보}` · 권한 없으면 글자만 · 제목이 생기면 줄 사라짐 | PASS | `:1005-1023` · `labels.ts:931-933` · 테스트 `:262-295`(서버가 후보를 남긴 응답으로도 줄이 사라짐을 확인) |
| 저장 뒤 상세·상위 제목·목록·캘린더 레일이 새 제목을 보인다 | PASS | 위 「목록 갱신」. 캘린더·내 업무 레일은 회의 화면과 동시에 서지 않는다. 진입 때 다시 읽는다는 워커 보고를 코드로 대조했다(`MeetingWorkspace.tsx:136` `onTitleChange` 는 원래 no-op) |
| `updateMeetingInfo` import 실사용 · 목록 [수정] 모달 불변 | PASS | `:567` 이 쓴다. `MeetingEditModal.tsx` diff 0 |

**Phase 1 검증**

| 계약 | 판정 | 근거 |
|---|---|---|
| frontend-test(직렬, 기존 실패 5 분리) · tsc · build | PASS(워커 수치 인용 + 대상 6파일 직접 실행 154/154) | 워커 보고 「테스트 결과」 |
| 바뀐 계약마다 테스트 | PASS | 로그인 1 · 내보내기 1 · 제목 9 · 후보 4. 단언의 강도는 W1·W2 |

## 「제목 후보:」 문구 변경의 파급 (브리프 §3-4)

- `meetingScreen.titleCandidate` 를 쓰는 곳은 상세 `MeetingDetailPage.tsx:1007` **한 곳**이다(grep). 목록 카드(`MeetingListPage.tsx:401`)·캘린더·레일은 후보를 그리지 않는다. 다른 표면과 어긋날 자리가 없다.
- `MeetingEditModal.tsx:81` 은 후보를 입력 초깃값으로만 쓰고 문구를 그리지 않는다. 영향 없다.
- 테스트: 후보 문구를 단언하는 곳은 `MeetingAfter.test.tsx:566`(정확 일치 → 정규식으로 바꿈)과 신규 파일뿐이다. 정규식으로 바꾼 이유는 같은 span 안에 「적용」 글자가 붙기 때문이다. 단언이 약해진 것이 아니라 부분 일치다. e2e 스크립트(`frontend/scripts`)에는 그 문구가 0건이다.

## 실물에서 만날 자리 (사용자 E2E 목록 후보)

1. **긴 제목의 줄바꿈**(W4) — 편집 가능한 끝난 회의에 칸 폭보다 긴 제목을 넣으면 머리 줄이 두 줄로 접힐 수 있다. 진행 중이거나 참석자가 아닌 회의는 같은 제목이 한 줄 말줄임이다. 편집 중 캐럿이 끝에 있을 때 넘친 글자가 잘리는지도 같이 본다.
2. **「제목 없는 회의」가 흐린 회색** — 편집 가능한 회의는 placeholder 색(`--scax-color-ink-assistive`)이고, 읽기 전용 회의는 지금처럼 검정이다. 의도된 DS 동작이지만 「제목이 사라졌다」로 보일 수 있다.
3. **한글 Enter** — Chrome 과 데스크톱 앱(macOS 웹뷰)에서 각각 한 번씩 확인한다. 조합 중 Enter 한 번으로 저장되는지, 두 번 쳐야 하는지, 닫힌 칸이 다시 열리지 않는지.
4. **눌리는 범위** — 제목은 `fill` 없는 인라인이라 **글자 위만** 눌린다. 제목 오른쪽 빈 자리를 눌러도 열리지 않는다. 「제목 없는 회의」도 글자 폭만큼이다.
5. **편집 표시가 캐럿뿐** — 포커스 링도 입력칸도 없는 것이 DS 계약이다. 제목을 눌렀는데 아무 일도 없는 것처럼 보일 수 있다. 커서는 `text` 모양이다.
6. **후보 줄 모양** — 「제목 후보: …」(12px 회색) 뒤에 파란 「적용」 글자 단추(label2 크기)가 붙어 활자 크기가 살짝 다르다. 시안이 없는 자리다(워커 DS-gaps).
7. **보내는 사이의 표시** — 저장을 누르면 응답 전부터 새 제목이 보인다. 서버가 거절하면 원래 제목으로 돌아가고 오류 토스트가 뜬다. 깜박임처럼 보일 수 있다.
8. **동시 수정** — 버전 잠금이 없어 나중에 저장한 쪽이 이긴다(be §3-2). 두 참석자가 같은 회의 제목을 고치면 앞 사람 것이 경고 없이 덮인다.
9. **내보내기 단추 높이** — 32px 로 「공유」·「다음 회의 예약」과 같은 높이가 됐는지 확인한다(끝난 회의).
10. **로그인 왼쪽** — 큰 h1 한 줄만 남아 아래가 비어 보일 수 있다. 900px 이하에서는 칸 자체가 숨는다.

## 기존 부채 (이번 판정 제외)

- `MeetingWorkspace.tsx:136` `onTitleChange={() => undefined}` — 상위 제목 전달이 원래 no-op 이다.
- 목록 [수정] 버튼이 `scheduled` 에만 서는 것은 WP 가 「그대로」로 정했다.

## 확인한 것 (PASS 근거)

- **계층·호출 자리**: 새 fetch 0건. `updateMeetingInfo`(`lib/api.ts:1225`) 를 그대로 쓴다.
- **권한 판단**: 서버 값 `can_edit_info` 하나다. status·viewer_relation 으로 다시 추론하지 않는다.
- **재사용**: 기존 `InlineText` · `Button variant="inline"` · `claim/release`. 새 부품은 없다.
- **카피**: 새 문자열 셋이 `labels.ts:931-935` 에 있다. 로그인 h1 은 기존 패턴(직접 박음)을 따랐다.
- **스타일**: 임의 hex 0. 인라인 `style={{fontSize:12}}` 는 기존 줄 그대로다.
- **테스트**: 신규 `MeetingTitle.test.tsx` 14건 · `LoginPage.test.tsx` +1건. 대상 6파일 154/154 통과.
- **allowed_paths**: 리포트 한 장만 썼다. 코드 수정 0.

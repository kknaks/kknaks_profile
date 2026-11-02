# WORK-010 Phase 1 결과 보고 (frontend)

## 상태: done

- 워크트리 `Strong_hajin/strong-hajin-polish3` · base `d1b5137`
- 커밋·push 없음
- `src-tauri/`·`lib/shell.ts`·`App.tsx` 손대지 않음 — Phase 3 워커 영역

## 수행 내용

### 변경 파일 (7)

| 파일 | 무엇 |
|---|---|
| `frontend/src/features/auth/LoginPage.tsx` | h1 → 「메디솔브 AX 프로젝트」, 설명 `p` 삭제(빈 요소 없음) |
| `frontend/src/features/meetings/MeetingDetailPage.tsx` | 「내보내기」 `<a>` 에 `scax-button--sm` 추가 · 제목 `InlineText` · 후보 [적용] · `saveTitle` 신설 · `updateMeetingInfo` 실제 사용 |
| `frontend/src/lib/labels.ts` | `meetingScreen.titleCandidate` 를 「제목 후보: {후보}」로 바꿈 · `titleCandidateApply: "적용"` · `titleEdit: "회의 제목"` 추가 |
| `frontend/src/ds/InlineText.tsx` | 편집 중 Enter 에 IME 조합 가드 한 줄(`event.nativeEvent.isComposing` 이면 저장 안 함) — 아래 「계약 밖 변경」 |
| `frontend/src/features/meetings/MeetingTitle.test.tsx` (신규) | 14건 |
| `frontend/src/features/auth/LoginPage.test.tsx` | +1건 |
| `frontend/src/features/meetings/MeetingAfter.test.tsx` | 후보 문구 기대값을 새 문구(콜론)로 1줄 바꿈 |

### 1-1 R1 로그인
- [x] h1 = 「메디솔브 AX 프로젝트」 (`LoginPage.tsx:68`)
- [x] 설명 `p` 삭제. 워드마크·레이아웃·900px 숨김 CSS 는 손대지 않음
- [x] 문서 title(`index.html`)·Tauri 창 제목은 손대지 않음

### 1-2 R2a 내보내기
- [x] `<a className="scax-button scax-button--outlined-neutral scax-button--sm">`
  - 옆 `<Button size="sm">` 의 기본 변형은 `outlined`/`neutral` 이다(`ds/Button.tsx:42-44`).
  - 따라서 같은 변형·같은 크기(32px)다.
  - href·같은 탭 이동은 그대로다.
- [x] `MaterialDrawer.tsx:66`(lg)·`MessageList.tsx:782`(sm)는 그대로

### 1-3 R3 회의 제목
- [x] `can_edit_info` 일 때 `h2.scax-detail__title` 안에 `InlineText`
  - Enter·blur 저장 · Esc 취소 · 빈 값/안 바뀐 값은 보내지 않음(InlineText 계약)
  - 실패하면 InlineText 가 원래 값으로 되돌리고, `onError(서버 문장)` 이 공통 오류 토스트로 뜬다.
- [x] `can_edit_info=false` 면 지금처럼 `h2` 안의 글자만 — 칸이 없다
- [x] 제목이 비면 placeholder 「제목 없는 회의」를 보이고, 열면 빈 칸에서 시작한다(value `""`)
  - 색은 InlineText 의 `--empty`(assistive)라 예전 검정보다 흐리다. DS 부품의 기존 동작이다.
- [x] 후보 줄: 제목이 없고 후보가 있을 때만 「제목 후보: {후보}」를 보인다.
  - `can_edit_info` 면 그 뒤에 `Button variant="inline" size="sm"` [적용]을 둔다.
  - [적용]은 `PATCH {title: 후보}` 다.
  - 제목이 생기면 줄이 사라진다. 서버가 후보를 남겨도 `title` 이 있으면 그리지 않는다.
- [x] 저장 경로 `saveTitle`(`MeetingDetailPage.tsx`, `run` 바로 위)
  - `claim("title")` 로 연타를 막는다.
  - `updateMeetingInfo(meetingId, {title})` → 응답(상세와 같은 `_detail` 모양, `backend …/meetings/application.py` `update_info` 끝 `return self._detail(...)`)을 `setRecord` 로 바로 세운다. 다시 읽지 않는다.
  - 이어서 `onError(null)` → `onMeetingChanged()` 를 부른다(목록 칸 다시 읽기 신호).
  - 실패하면 `onError(문장)` 후 다시 던진다 → InlineText 가 원복한다.
- [x] `updateMeetingInfo` import 를 실제로 쓴다. 목록 [수정] 모달은 그대로다.

### 계약 밖 변경 (보고)
- **`ds/InlineText.tsx` IME 가드**
  - 편집 중 Enter 가 `isComposing` 이면 저장하지 않는다.
  - 이유: 한글 조합 중 Enter 에서 저장해 칸이 닫히면, 조합을 끝내는 뒤따른 Enter 가 **닫힌 칸을 다시 연다**(닫힌 상태의 Enter = 열기, `InlineText.tsx` keyDown 분기).
  - 체크리스트 단계 수정(`WorkModals.tsx` `step-edit`)과 같은 규칙이다.
  - 영향: InlineText 쓰는 곳 전부(회의 안건 제목·메모 줄 `AgendaBlock.tsx` 2곳 + 새 회의 제목 1곳). 기존 테스트는 통과한다.

## grep 으로 센 자리 (변경 후, `frontend/src`, 테스트 제외)

**「제목 없는 회의」 대체 (`meetingScreen.noTitle` 사용 6 + 정의 1)**

| 자리 | 바뀜? | 새 제목이 보이는 길 |
|---|---|---|
| `lib/labels.ts:761` 정의 | 유지 | — |
| `MeetingDetailPage.tsx:300` `onTitleChange` | 유지 | `record` 가 바뀌면 effect 가 다시 분다. 호출부 `MeetingWorkspace.tsx:136` 은 no-op 이다(기존) |
| `MeetingDetailPage.tsx:996` InlineText placeholder | **신규** | 응답 `setRecord` |
| `MeetingDetailPage.tsx:1000` 읽기 전용 글자 | 바뀜(분기 안으로) | 응답 `setRecord` |
| `MeetingListPage.tsx:401` 목록 카드 | 유지 | `onMeetingChanged` → `MeetingWorkspace` `reloadList` → `reloadToken` → 목록 `reload`(`MeetingListPage.tsx:88`) |
| `shell/CalendarRail.tsx:134` 내 업무 우 레일 | 유지 | 회의 화면과 동시에 서지 않는다. 화면 전환 때 `MyWorkPage` 가 새로 마운트되어 `getCalendar` 를 다시 부른다(`App.tsx` 조건부 렌더 · `MyWorkPage.tsx` `railRange` ref 초기화) |
| `features/calendar/calendarModel.ts:92` 캘린더 | 유지 | 같은 이유로 진입 때 `getCalendar` 를 다시 부른다(`CalendarPage.tsx:167`) |

**`updateMeetingInfo`**: 정의 `api.ts:1225` · 사용 2 — `MeetingEditModal.tsx:119`(목록 [수정], 그대로) · `MeetingDetailPage.tsx:567`(**신규**, 예전 import-only)

**`<a>` + `scax-button` 3곳**

| 자리 | 크기 | 바뀜? |
|---|---|---|
| `MeetingDetailPage.tsx:1060` 내보내기 | md → **sm** | 바뀜 |
| `MaterialDrawer.tsx:66` 자료 내려받기 | lg | 유지(의도) |
| `MessageList.tsx:782` 근거 원본 열기 | sm | 유지 |

**옛 로그인 문구**: 0건(새 테스트의 부정 단언 1건만)

## 테스트 결과
- 기준선: Test Files 2 failed | 81 passed (83) · Tests 5 failed | 1227 passed (1232)
- `npx vitest run --no-file-parallelism`(1회): **Test Files 2 failed | 82 passed (84) · Tests 5 failed | 1242 passed (1247)**
  - 실패 5건 = 기준선 5건과 같다(`CreateWork.test.tsx` 4 · `CreateWorkLayout.test.tsx` 1, 날짜 의존). **새 실패 0.**
  - +15 = 신규 `MeetingTitle.test.tsx` 14 + `LoginPage.test.tsx` 1
- `npx tsc --noEmit`: 0 에러
- `make frontend-build`: 성공(기존 500kB 청크 경고만)
- 새 테스트 목록
  - 로그인: h1 문구 · `p` 없음 · 워드마크 유지 · 옛 문구 없음
  - 내보내기: `scax-button--sm`·`--outlined-neutral` · href 그대로 · target 없음 · 옆 「공유」와 같은 클래스
  - 제목 인라인
    - 열림(같은 노드 · input 없음)
    - Enter 저장(`{title}` 하나 · 응답 반영 · `onMeetingChanged` 1회)
    - blur 저장
    - IME 조합 중 Enter 무시
    - Esc 취소
    - 빈 값·안 바뀐 값 무시
    - 실패 원복 + 오류 문장
    - 권한 없음 = 글자만
    - 제목 없음 = 「제목 없는 회의」 + 빈 칸에서 시작
  - 후보 [적용]: 권한 있음(저장 · 후보 줄 사라짐 · 서버가 후보를 남겨도) · 권한 없음([적용] 없음) · 제목 있으면 줄 없음 · 실패하면 줄 유지 + 오류

## 다른 팀 영향
- BE: 없음. 기존 `PATCH /api/meetings/{id}` `{title}` 만 쓴다. 버전 잠금 없음(be-survey §3-2) — 나중에 저장한 쪽이 이긴다.

## DS-gaps
- **InlineText 시안이 `.design-sync/previews` 에 없다**(fe-survey §4-8). 이번 자리도 시안 없이 기존 부품만 재사용했다.
- 제목 후보 줄은 기존 `span.t-meta` + 인라인 `style={{fontSize:12}}`(기존 코드)에 DS `Button variant="inline" size="sm"` 을 붙인 것이다. 「후보 + 적용」 모양의 시안은 없다.
- `h2.scax-detail__title` 은 `white-space:nowrap; overflow:hidden; text-overflow:ellipsis`(`workspace.css:16`)다. 그래서 칸 폭보다 긴 제목을 고칠 때 넘친 부분이 잘려 보일 수 있다(렌더 미확인). 공용 CSS 는 손대지 않았다.

## 이슈/미결
- 목록 [수정] 버튼은 여전히 `scheduled` 에만 선다(계약이 「그대로」).
  - 끝난 회의 제목은 이제 상세 인라인으로 고칠 수 있다.
- 실제 브라우저·Tauri 렌더 확인은 하지 않았다(서버·프론트를 띄우지 않음 지시). 다음 둘은 E2E 에서 볼 자리다.
  - InlineText 제목의 시각 확인
  - 한글 IME 실제 동작

---

## fix1 — 검수 WARN 처리 (`review-fe-p1-report.md`)

| # | 처리 | 파일 |
|---|---|---|
| W1 | 「응답을 세운다」 테스트를 **응답 값으로만 통과하게** 고쳤다. 목 응답 제목 = 「DB AX 전환 범위 (서버)」(입력과 다름) → 그 값이 보이고, 보낸 값 「DB AX 전환 범위」는 없다. `readMeeting` 은 첫 읽기 1회뿐이다(저장 뒤 다시 읽지 않음). | `frontend/src/features/meetings/MeetingTitle.test.tsx` |
| W2 | 연타 방지 테스트 1건을 추가했다. 첫 저장(인라인 Enter)이 끝나지 않은 동안 다음을 확인한다. ① [적용]이 `disabled` 이고, 눌러도 요청이 없다. ② 칸을 다시 열어 다른 값으로 Enter 해도 요청이 없다(`claim("title")` 이 거절 → `InlineText` 원복). 첫 응답 뒤에도 요청은 1회다. | 같은 파일 |
| W3 | `.login-brand p` 죽은 규칙을 삭제했다(`styles/screens-a.css` 옛 `:71`). `frontend/src` 안 `login-brand` 사용처는 `LoginPage.tsx:63`(section)과 테스트 1뿐이고, `p` 를 겨누는 것은 0이다. | `frontend/src/styles/screens-a.css` |
| W4 | **고치지 않음**(코디 답). 긴 제목 편집 시 `h2.scax-detail__title` 의 nowrap/ellipsis 차이는 사용자 E2E 2루프에서 본다. | — |

- **참고**: `.design-sync/screens/_ds_bundle.css:2144` 에도 같은 `.login-brand p` 사본 규칙이 있다. allowed_paths(`frontend/src/`) 밖이라 손대지 않았다. 번들 재생성 때 함께 빠질 자리다.
- **검증**
  - `npx vitest run --no-file-parallelism src/features/meetings/MeetingTitle.test.tsx src/features/auth/LoginPage.test.tsx` → **19 passed**(MeetingTitle 15 · Login 4)
  - `npx tsc --noEmit` → 0 에러
- **fix1 변경 파일**: `MeetingTitle.test.tsx` · `styles/screens-a.css`. 제품 코드 동작 변경 없음.

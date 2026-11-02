# WP1-FE 결과 보고 (frontend)

## 상태: done

- 워크트리 `strong-hajin-enhance` · base `f0ad522` · 커밋·push 없음(변경은 워크트리에만)
- 범위: WORK-012 「Phase WP1-FE」 계약 5건 + 추가 지시 SH-IMP-020(§6)
- 기준선: `fe-baseline.md` (손대기 전 9건 실패 · 빌드 통과)

## 1. 계약 체크박스별 구현 위치 — 5/5 (+ 추가 1/1)

| # | 계약 | 구현 위치(파일:줄) |
|---|---|---|
| 1 | **002/004** 수정 모달 날짜 칸 폭을 줄여 세 칸이 왼쪽 열 안에 — 생성 모달도 넘치지 않음 · 종료 칸이 검색 입력 밑에 깔리지 않음 | `frontend/src/styles/meetings.css:148-157` — 날짜 `flex: none; width: 200px`(고정) → `flex: 0 1 200px; min-width: 0`(남는 폭까지만, 최대 200) · `.meeting-when` 에 `min-width: 0` · **수정 모달(`.meeting-meta-edit`) 안에서만** 시각 한 쌍을 줄인다(`gap: 5px` · 트리거 `padding: 0 7px; min-width: 0` · 시계 아이콘 숨김). 줄이는 방식은 AX 회의 카드의 기존 규칙(`styles/ax.css:438-441`)과 같다 |
| 2 | **002 중복** — 수정 모달 `onPick` 이 이미 있는 사람을 다시 넣지 않음 · 생성·공유 모달 확인 | 공용 함수 `addPersonOnce` `features/meetings/PeoplePicker.tsx:12` → 수정 모달 `MeetingEditModal.tsx:231` · 공유 모달 `ShareModal.tsx:109`(검색) · `:123`(조직도). 생성 모달은 이미 `togglePerson` 이 id 로 가른다(`BookingModal.tsx:191`) — 바꾸지 않음 |
| 3 | **005** — `applySuggestion` 이 날짜·시작·종료를 건드리지 않음 · 제출이 안건마다 `source` · [다음 회의 예약] 입구도 · `manual` 문구 = 「새로 추가된 안건」 | `BookingModal.tsx:199-201`(주석) — `setDate`·`setFrom`·`setTo` 세 줄 삭제 · 제출 `BookingModal.tsx:250` `agendas.map((a) => ({ title, source }))` · API 타입 `lib/api.ts:1229` `Array<{ title; source?: "manual" \| "carried" }>` · [다음 회의 예약] 입구는 이미 `source: "carried"` 초안 + `carriedFrom` 을 넘긴다(`MeetingDetailPage.tsx:1392-1399`) → 같은 제출 줄을 타서 **코드 변경 없이** 안건별 출처가 나간다(시험으로 잠금) · 문구 `lib/labels.ts:750` 「직접 입력」 → 「새로 추가된 안건」(`manual` 을 정하는 자리 넷 모두에 붙음 — 화면 문구는 이 상수 하나) · 안 쓰게 된 import 정리 `BookingModal.tsx:13`(`meetingClock`·`meetingDateInput`) |
| 4 | **014** — 받기 셋에서 `download`·`_blank` 빼고 `download=1` · 받기 주소와 원본 보기·미리보기 주소를 가른다 · `Thumb` 은 `hasShell()` 참이면 받기 주소·같은 탭, 거짓이면 새 탭 · 모양·미리보기 그대로 | 받기 주소 함수 `lib/api.ts:1687`(`inboxMailAttachmentDownloadUrl`) · `:1692`(`inboxRoomAttachmentDownloadUrl`) — 원본 주소 + `?download=1` · `InboxAttachments.tsx:45-50` `DownloadLink`(download·target 삭제) · `:87-97` `downloadAll`(`anchor.download` 삭제, 받기 주소) · `:105` `type Linked` 에 `downloadHref` · 조립 `:292`(`AttachmentList` 가 `downloadOf` 로 채움) · 받기 자리 `:131`(FileGroup) · `:159`(PdfBlock) · `:305`(파일 하나) · `Thumb` `:164-205`(`download` prop · `saveInApp = Boolean(download) && hasShell()` `:189` · `target` `:197`) · 원본 보기 자리 `:213`(ImageBlock) · `:230`(AlbumBlock) · 방: `RoomView.tsx:547` `downloadOf` 정의 + prop 길 `:298, :311, :345, :441, :455, :496, :503, :715, :751` · 메일: `MailView.tsx:391-397`(미리보기 `src` 와 받기 `download` 를 가름 · `Thumb` 에 `download`) · `:404`(이미지 받기 단추) · `:416`(파일 카드) |
| 5 | **010** — 설정 화면은 이미 `integration.changed` 에 다시 읽는다(확인만) | **코드 변경 없음.** 구독 `features/settings/SettingsPage.tsx:181-187`(`integration.changed` → `load(true)`). 화면 쪽 절반을 시험으로 잠갔다(§3) — 숫자가 실제로 느는지는 WP1-BE 사건 + 앱 E2E 몫 |
| + | **SH-IMP-020** 목록 머리 「회의 시작」 → 「빠른 회의」 | §6 |

## 2. Code Surface 대비 닿은 자리 (WP1 표 · 시작 때 다시 셈)

| 무엇 | 표의 수 | 다시 센 수(시작 때) | 바꾼 자리 / 건드리지 않은 자리 |
|---|---|---|---|
| 002/004 `meeting-when\|date-field` | prod 17/7 · test 3/2 | prod 17 · test 3 (같음) | 바꿈: `meetings.css:148-150` → `:148-157`. 쓰는 곳 `MeetingEditModal.tsx:175` · `BookingModal.tsx:362` 은 마크업 그대로(생성 모달은 날짜 최대 200 그대로 · 두 열 규칙이 안 걸림 — 시험). 건드리지 않음: `ds/DateField.tsx:55` · `components.css:584` · `task-detail.css:142-189` · `ax.css:413-422` · `meetings.css:99` |
| 002 `PersonSearch\|PickedTags` | 12/5 | 12/5 (같음) | 담는 자리 넷 중 수정·공유 둘에 `addPersonOnce` · 생성은 기존 toggle · `MeetingDetailPage.tsx:55` 는 import 만(쓰는 곳 없음 — 원래부터, 그대로 둠) |
| 005 ① `setFrom(\|setTo(\|setDate(` in BookingModal | 8 | 8 → **5** | `applySuggestion` 셋만 삭제 · `:377-378`(고르개) · `:387-389`([지금]) 그대로 |
| 005 ② `"carried"…` 화면 | `BookingModal.tsx:42,225` · `MeetingDetailPage.tsx:1399` · `viewModels.ts:1235` | 같음 | 화면용 출처를 **보낸다**(`:250`) · `:42`·`:225`·`:1399` 는 그대로(이미 맞는 값) · `viewModels.ts` 그대로 |
| 005 ② `manual` 을 정하는 화면 자리 | `BookingModal.tsx:443` | 같음(현재 `:442`) | 값 그대로 `manual` — 문구만 `labels.ts:750` |
| 005 ② 안건 입력 모델 화면 | `BookingModal.tsx:251` · `api.ts:1228` | 같음 | 둘 다 바꿈(`:250` · `api.ts:1229`) |
| 005 ② 문구 `meetingAgendaSourceText\|직접 입력\|지난 회의에서 넘어옴` | prod 7/3 · test 1/1 | 같음 | `labels.ts:750` 바꿈 · 쓰는 곳 `MeetingDetailPage.tsx:1210` · `BookingModal.tsx:425` 그대로 · 시험 `MeetingAfter.test.tsx:236` 새 문구로 |
| 014 `download[={ ]\|target="_blank"\|\.download ?=` | prod 14/8 · test 2/1 | prod 14 · test 2 (같음) | 바꾼 넷: `InboxAttachments.tsx:40`(DownloadLink) · `:80-91`(downloadAll) · `MailView.tsx:401` · `InboxAttachments.tsx:162`(Thumb — 웹은 `_blank` 유지·앱은 없음). **지금 prod 의 `download=`·`.download =` 코드 0건**, `_blank` 는 표의 「바꾸지 않음」 목록(`:286` unfurl · `RoomView.tsx:165,673` · `KakaoSection.tsx:215` · `WorkModals.tsx:1936,4306,4334` · `MessageList.tsx:782` · `AssistantMarkdown.tsx:199`)과 `Thumb` 의 웹 갈래뿐 |
| 014 받기 주소 `inboxMailAttachmentUrl\|inboxRoomAttachmentUrl` | `api.ts:1668-1679` + 쓰임 4 | 같음 | 받기 함수 둘을 더함 · 쓰임: 메일 `MailView.tsx:393`(미리보기 `src`) 그대로 · `:416` 파일 카드는 받기 함수로 · 방 `RoomView.tsx:546-547` 원본·썸네일 그대로 + 받기 함수 |
| 014 F-3 `Linked\|hrefOf\|href={file.href}` | — | 방 prop 길 10(정의 포함) | `Linked` 에 `downloadHref` · 조립 `:292` · prop 길 10곳 전부에 `downloadOf` 를 같이 내림 · 받기 자리 5(`:60` FileCard 안 · `:131` · `:159` · `:305` · `downloadAll`) → `downloadHref` · 원본 보기 `:213`·`:230` → `href` + `download` · 메일 `Thumb` 에 받기 주소 넘김(`MailView.tsx:397`) |
| 014 앱/웹 판별 `hasShell` | `lib/shell.ts:70` | 같음 | 새 쓰는 곳 1(`InboxAttachments.tsx:189`) · `dev/probeShell.ts` 안 씀 |
| 010 화면 | `SettingsPage.tsx:181-187` · `InboxPage.tsx:143` · `viewModels.ts:1650` | 같음 | 바꾸지 않음 |

**표 밖에서 더 찾은 것**
- `ShareModal.tsx:123` — 조직도(`OrgDirectory mode="add"`)로 담는 자리도 append 만 하고 있었다 → `addPersonOnce`(표는 검색 자리만 셌다)
- `MailView.tsx:416` — 메일 **파일** 카드(`FileCard`)도 받기 단추라 받기 주소로 바꿨다(표는 이미지 받기 `:401` 만 셌다. SPEC 「파일 카드의 받기 단추」 에 든다)
- `InboxPage.test.tsx` 두 곳(메일 `범위.pdf 받기` · 방 `범위.pdf 받기`)이 옛 주소를 단언하고 있어 새 계약(`?download=1`)으로 바꿨다
- 020 의 문구 상수는 공유였다 — §6

## 3. 새 시험 (22개 · 시험 수 1371 → 1393)

| 파일 | 시험 | 계약 |
|---|---|---|
| `features/meetings/MeetingEditModal.test.tsx` | 날짜·시작·종료가 왼쪽 열 `.meeting-when` 한 줄에 선다 — 오른쪽 열에는 검색 입력뿐 | 002/004 |
| 〃 | 날짜 칸은 고정 200px 이 아니라 줄어들고, 수정 모달의 시각 한 쌍은 좁게 선다(CSS 규칙을 `node:fs` 로 읽어 단언) | 002/004 |
| 〃 | 생성 모달도 같은 줄 모양 — 두 열 규칙(`.meeting-meta-edit`)은 안 걸린다 | 002/004 |
| 〃 | 검색으로 고른 사람은 한 번만 담기고 결과에서 빠진다 · 저장 `attendee_ids` 에 한 번 | 002 중복 |
| 〃 | `addPersonOnce` 는 같은 사람을 두 번 넣지 않는다 | 002 중복 |
| `features/meetings/MeetingList.test.tsx` | [불러오기]는 날짜·시작·종료를 바꾸지 않는다 · 결론 안 난 안건만 · 「지난 회의에서 넘어옴」 | 005 (AC-09) |
| 〃 | 제출은 안건마다 출처 — 불러온 = `carried` · 손으로 = `manual` · `carried_from_meeting_id` · 「새로 추가된 안건」 | 005 (AC-10) |
| 〃 | 불러오지 않은 회의의 안건은 전부 `manual` · 이어온 회의 없음 | 005 |
| 〃 | 목록 머리 주 단추는 「빠른 회의」 — 재생 아이콘·solid-primary·옆 「회의 생성」 그대로 · 「회의 시작」 없음 | 020 |
| `features/meetings/MeetingAfter.test.tsx` | [다음 회의 예약]도 안건마다 출처를 보낸다 | 005 (AC-10 두 입구) |
| `features/inbox/InboxAttachments.test.tsx`(새 파일) | 파일 카드 하나 · PDF 카드 · 파일 묶음 받기 단추 = `?download=1`, `download`·`target` 없음 | 014 |
| 〃 | 「모두 다운로드」가 받기 주소를 `download` 속성 없이 차례로 누른다 | 014 |
| 〃 | 받을 수 없는 첨부(만료·대기)에는 받기 링크 없음 | 014(회귀) |
| 〃 | 웹 — 썸네일은 미리보기 주소, 누르면 원본 새 탭(내려받기 아님) | 014 / OQ-812 |
| 〃 | 앱(셸 전역 대역) — 썸네일 그대로, 누르면 받기 주소·같은 탭 | 014 / OQ-812 |
| 〃 | 앨범 칸도 앱/웹이 갈린다 | 014 |
| 〃 | 받기 주소 없는 `Thumb` 은 앱에서도 지금처럼 새 탭 | 014(회귀) |
| 〃 | 메일(웹) — 이미지 썸네일·원본 보기 = 미리보기 주소 새 탭 · 받기 둘 = `?download=1` | 014 |
| 〃 | 메일(앱) — 이미지 원본 보기도 받기 주소·같은 탭 · 썸네일은 미리보기 주소 | 014 |
| `features/settings/SettingsPage.test.tsx` | `integration.changed` 가 오면 숫자가 새로고침 없이 바뀐다 · 메시지 도착 사건으로는 다시 읽지 않는다 | 010 |

고친 기존 시험: `MeetingAfter.test.tsx`(출처 문구) · `InboxPage.test.tsx`(받기 주소 둘) · `MeetingList.test.tsx`·`MeetingWorkspace.test.tsx`(머리 단추 문구 — §6)

## 4. 검증 수치

| | 기준선(손대기 전) | 이번 |
|---|---|---|
| 시험 명령 | `cd frontend && npx vitest run --no-file-parallelism` | 같음 |
| 시험 파일 | 92 — 통과 88 · 실패 4 | 93 — 통과 90 · 실패 3 |
| 시험 | 1371 — 통과 1362 · 실패 9 | **1393 — 통과 1385 · 실패 8** |
| 이번 판이 만든 실패 | — | **0** — 실패 8건 모두 기준선 목록 안(`CreateWork.test.tsx` 4 · `CreateWorkLayout.test.tsx` 1 · `TaskDetailDates.test.tsx` 3). 기준선의 `ActionCenter.test.tsx` 1건은 이번 실행에서 통과(이번 판과 무관한 파일 — 흔들리는 시험으로 보인다) |
| 빌드 `npm run build`(= `make frontend-build`) | 통과 | **통과**(청크 500kB 경고만) |

- `make frontend-test` 를 그대로 부르지 않고 **직렬**로 돌렸다 — `make frontend-test` = `vitest run`(파일 병렬)이고, 병렬 vitest 가 사용자 로컬 스택을 죽인 전례가 있다(WORK-012 P-9 · 사용자 메모). 시험 집합은 같다
- 중간에 빌드가 한 번 깨졌다 — 새 시험의 `node:fs` 동적 import 에 타입이 없어서(`@types/node` 없음). 기존 선례(`ChatDrawer.test.tsx`)와 같은 `@ts-expect-error` 를 달아 해결했다
- 워크트리에 `frontend/node_modules` 가 없어 `npm ci`(lock 그대로 · `package-lock.json` 변경 없음)를 먼저 돌렸다

## 5. 미결 · 주의점

1. **WP1-BE 와 같이 나가야 한다(005).** 생성 요청이 안건마다 `source` 를 싣는다. 지금 운영 서버의 생성 입력은 안건 `{title}` 만 받고 `extra=forbid` 라(WORK-012 Code Surface 005 ②), **새 프론트 + 옛 서버면 안건이 있는 회의 생성이 422** 가 된다. WP1-BE(생성 전용 안건 모델)가 같은 판에 들어가야 한다
2. **WP1-BE 와 같이 나가야 한다(014).** 옛 서버는 `?download=1` 을 모르고 지금 규칙대로 이미지·PDF 를 `inline` 으로 낸다 — 그러면 앱에서 이미지·PDF 받기와 이미지 원본 보기가 여전히 「아무 일 없음」(셸이 가로챈 뒤 `inline` 이면 알림 없이 끝남 — FE 조사 §1-1). 앱 확인은 BE 반영 뒤에
3. **웹의 「모두 다운로드」 — 확인 필요.** 계약대로 `download` 속성을 뺀 같은 탭 링크를 300ms 간격으로 누른다. 브라우저에서 같은 탭 이동이 연달아 나가면, 앞 응답(첨부 중계 — 상류에서 받아 오느라 느릴 수 있음)의 머리가 오기 전에 다음 이동이 앞 이동을 **취소할 수 있다**(브라우저 동작 — 실측 못 함). 앱은 셸이 이동마다 가로채므로 해당 없다. 운영 웹 E2E 에서 파일 여럿 「모두 다운로드」 를 한 번 봐야 한다(코디 몫). 계약을 바꾸지 않았다
4. **010 은 화면 코드 변경 없음** — 숫자가 실제로 늘려면 WP1-BE 의 「저장마다 `integration.changed`」 가 필요하다
5. **002/004 는 실측이 아니다** — jsdom 은 배치를 계산하지 않는다. 폭은 CSS 계산(왼쪽 열 ≈277px 에 날짜 ≈140 + 줄인 시각 한 쌍 ≈129)이고, 앱 창 기본 크기에서 한 줄에 드는지는 앱 E2E 에서 확인해야 한다. 수정 모달의 시각 칸은 시계 아이콘이 빠진다(AX 회의 카드와 같은 모양)
6. 수정 모달은 지금도 저장마다 시각을 함께 보낸다 — 「바뀐 값만 보낸다」(SPEC-010 §4.3 · OQ-1010)는 회의실과 함께 WP3 몫이라 이번에 손대지 않았다
7. `MeetingDetailPage.tsx:55` 의 `PersonSearch`·`PickedTags` import 는 쓰는 곳이 없다(원래부터) — 범위 밖이라 그대로 뒀다

## 6. SH-IMP-020 — 목록 머리 「회의 시작」 → 「빠른 회의」 (추가 지시)

**바꾼 것**: 문구 상수 `meetingScreen.start`(「회의 시작」)는 **공유**였다 — 목록 머리 단추와 회의 상세의 「예정 회의를 지금 시작」 단추가 같이 쓴다. 그래서 상수를 가르고 목록 머리만 새 상수를 쓴다.
- `lib/labels.ts:776-779` — `start: "회의 시작"`(상세용 · 그대로) 옆에 `quickStart: "빠른 회의"` 를 더함
- `features/meetings/MeetingListPage.tsx:190` — `{meetingScreen.start}` → `{meetingScreen.quickStart}`. 아이콘(`play`)·모양(`solid`·`primary`·`sm`)·동작(`quickStartMeeting`)은 그대로

**「회의 시작」 문구를 쓰는 곳 전부**(`rg -n "회의 시작" frontend/src` + 상수 `meetingScreen.start` 쓰임)

| 파일:줄 | 무엇 | 처리 |
|---|---|---|
| `lib/labels.ts:776` | 상수 `meetingScreen.start` | 그대로(상세 단추용) · 옆에 `quickStart` 신설 |
| `features/meetings/MeetingListPage.tsx:190` | **목록 머리 주 단추**(재생 + 문구, 옆 「회의 생성」) | **바꿈 → 「빠른 회의」** |
| `features/meetings/MeetingDetailPage.tsx:1040` | 회의 상세 제목 줄의 [▷ 회의 시작] — **예정 회의를 시작**(`startMeeting`) — 빠른 회의와 **다른 동작** | 그대로 |
| `features/meetings/MeetingList.test.tsx:279,282,690,714,716` | 머리 단추 시험(바로 연다 · 한 번 = 회의 하나) | 「빠른 회의」 로 갱신 |
| `features/meetings/MeetingWorkspace.test.tsx:172,225,227` | 목록 머리 단추로 빠른 시작 → 목록에 선다 | 「빠른 회의」 로 갱신(`:172` 는 주석) |
| `features/meetings/MeetingWorkspace.test.tsx:187-188` | 상세 단추(`meetingScreen.start`) | 그대로 |
| `features/meetings/MeetingDetail.test.tsx:201,206,207,365` | 상세 단추 | 그대로 |
| `lib/labels.ts:1070-1071` · `labels.test.ts:57` · `LiveScript.tsx:59` · `MeetingDetailPage.tsx:136,304,437,670,972,978,981` · `MeetingEditModal.tsx:37` · `viewModels.ts:1182` | 주석·경과 시간 설명(「회의 시작에서 몇 분」 등) — 단추 문구 아님 | 그대로 |

**같은 동작 다른 입구**: 프론트 코드에서 `quickStartMeeting`(빠른 시작)을 부르는 곳은 **목록 머리 단추 하나뿐**이다(`MeetingListPage.tsx:160-165` — `rg quickStartMeeting` 결과 api 정의 + 이 한 곳). 빈 상태 화면·AX 안내 문구에서 같은 동작을 부르는 입구는 찾지 못했다. 주석에 「빠른 시작」 이라는 옛 이름이 남아 있다(`MeetingListPage.tsx:43,140,157,180` · `MeetingDetailPage.tsx:175,979,1211` · `labels.ts:808`) — 문구가 아니라 바꾸지 않았다. 서버가 내는 문구(AX 안내 등)는 프론트 범위 밖이라 보지 않았다.

**시험**: `MeetingList.test.tsx` 「목록 머리의 주 단추는 「빠른 회의」다」(새) + 기존 머리 단추 시험 문구 갱신(§3).

## 다른 팀 영향

- BE: 위 §5-1·2 — WP1-BE 의 생성 안건 `source` 모델과 `?download=1` → `attachment` 가 같은 판에 들어가야 한다
- SPEC·디자인 시스템과 어긋난 지점: 없음(수정 모달 시각 칸 축소는 AX 카드의 기존 규칙을 그대로 따름)

# WP4-FE 결과 보고 (frontend)

## 상태: done

- 워크트리 `strong-hajin-enhance` · WP1 `e51fe3b` · WP2 `e58fb25` · WP3 `cfc2e1c` 위 · 커밋 없음(변경은 워크트리에만)
- 계약: WORK-012 「Phase WP4-FE」 · SPEC-008 v0.6.0 §2.8 · §2.9 · §4.4 · §4.8 · **WP4 계약 고정**(`wp4-contract-fixed.md` 1 — FE 가 물은 「참고 자료 한 줄」 = `context_references[]` 의 `turn_id` · `label`)
- 표기(OQ-908): 「AX 업무 생성 · AX 요약」 · 「스레드에 답글」 · 아이콘만 + 아이콘 호버 툴팁
- 검증 = 바꾼 부분 관련 시험 파일만(코디 지시)

## 1. 계약 체크박스별 구현 위치 — 6/6 (`frontend/src/` 기준)

| # | 계약 | 구현 위치 |
|---|---|---|
| 1 | **호버 막대** — `Message` 한 곳 · 슬랙 셋 / 카톡 둘 · 아이콘만 + 툴팁 · 키보드 포커스 · 패널 안 답글(스레드 아이콘 없음 — OQ-813) · 로컬 줄 없음 | `features/inbox/RoomView.tsx` — 행동 타입 `MessageActions` `:71` · 막대 `MessageBar` `:147`(DS `IconButton` 아이콘만 · 툴팁 = 감싸개 `data-tip` → CSS `::after` · `role="toolbar"`) · `Message` 한 곳에서 그림(로컬 줄이면 안 그림 · 막대가 있으면 행 `tabIndex=0`) · 대화 열 `rowActions` `:703`(슬랙 = 스레드·AX 둘 / 카톡 = AX 둘) · 패널 안 `panelActions` `:533`(AX 둘만 — 부모·답글 모두). CSS `styles/inbox.css` 끝(막대는 행 위에 겹쳐 뜸 — `position:absolute` · `:hover`·`:focus-within` 으로 1차, 아이콘 `:hover`·`:focus-within` 으로 2차 툴팁). DS 에 툴팁 부품이 없어 CSS 로 했다(§5-3) |
| 2 | **「스레드에 답글」** — 답글 0개도 패널 열기(입구만 더함) | `RoomView.tsx:703` `rowActions` 의 `onThread = () => setThreadKey(line.key)` — 답글 수 조건 없음. 패널·조회(`thread_ts`)·답장 경로는 손대지 않음(원래 조건이 없었다 — FE 조사 §6-1) |
| 3 | **메일 머리** [AX 업무 생성][AX 요약][답장][전체 답장] | `features/inbox/MailView.tsx:366-375` — AX 둘이 답장 앞(글자 단추 · 툴팁 없음 — SPEC §2.9 ②) |
| 4 | **서랍 열며 참고 자료 보내기** — `askAx` 를 메시지함이 받도록 넓히고 `context` 를 싣는다 · 말풍선 본문 넷 · 말풍선 아래 참고 자료 한 줄 | `App.tsx:313` `askAx(text, context = [])`(서랍 열기 → `chat.start()` = 새 대화 → `sendCurrent(text, context)`) · 메시지함에 넘김 `App.tsx:574` · `features/inbox/InboxPage.tsx:221` `askFrom` — 본문 넷(메시지/메일 × 업무/요약 · `labels.ts:1506~`) + 참고 자료 `[{resource_type:"inbox_message", resource_id, resource_version:1, included:true}]`(§4.8 ①) · 방(`RoomView` `onAsk`)·메일(`MailView` `onAsk`)에 내림. 타입 `lib/viewModels.ts:1041`(`inbox_message`) · 말풍선 아래 한 줄은 #6 |
| 5 | **출처 링크** — 업무 상세 출처 행 「원래 메시지 · …」(「판단 보기」 와 함께) · 누르면 메시지함의 그 메시지로(스크롤·강조 — OQ-817) · **「업무 만듦」** — `inbox.message_updated` 를 받아 그 방·메일을 다시 읽어 새로고침 없이 | 출처 행 `features/work/WorkModals.tsx:2176~`(「판단 보기」 뒤에 「원래 메시지 · 슬랙 #…」/「원래 메일 · …」 · 통로가 없는 화면은 글자만) · 타입 `TaskOriginMessage` `viewModels.ts:444` · 문구 `labels.ts:404` · 통로: `App.tsx:320` `openInboxMessage`(메시지함으로 + `inboxFocus`) → `sharedWorkProps.onOpenInboxMessage` `:405` → `MyWorkPage` · `TodayPage` · `CalendarPage` 의 `TaskDetailDrawer`. 메시지함 쪽 `InboxPage.tsx:235~`(그 방·메일 카드를 고름 — 레일에 없으면 출처 값으로 카드를 세움) → `RoomView` `focusMessageId` `:570` · 짚기 `:716~`(최상위면 그 줄로 스크롤 + `scax-imsg--focus` 2.5초 · 스레드 답글이면 그 스레드 패널을 열고 부모를 짚음 · 첫 페이지에 없으면 위로 최대 3쪽 더 읽음 · 못 찾으면 「메시지를 찾을 수 없습니다」 — `App.tsx` `onFocusHandled`). **「업무 만듦」**: 방 행 머리 `RoomView.tsx:374`(묶인 줄은 본문 위 `:378`) · 메일 제목 옆 `MailView.tsx:366` · 사건 구독 — 방 `:648` · 스레드 패널 `:528` · 메일 `MailView.tsx:297`(`room_id` 없음 + 그 `message_id`). 사건 타입 `viewModels.ts:1692` · 응답 칸 `made_task_count` `:1648`(메일) · `:1675`(방 메시지) |
| 6 | 말풍선 아래 참고 자료 한 줄 = **실제 실은 범위**(OQ-816) · 단추마다 새 대화(OQ-815) | `features/chat/MessageList.tsx:253` — `context_references` 중 `resource_type="inbox_message"` · 같은 `turn_id` · `label` 이 있는 것만 그 턴의 사용자 말풍선 바로 아래 `ul.scax-msg__references`(서버 글자 그대로 · `label` 없으면 줄 없음 — 계약 고정 1). 대화 합치기 키에 `turn_id` 를 더함 `useConversations.ts:84`(같은 메시지를 두 턴에서 가리켜도 줄이 둘). 새 대화 = `askAx` 의 `chat.start()`(누를 때마다) · CSS `styles/ax.css` 끝 |

## 2. Code Surface WP4 표 대비 닿은 자리

| 무엇(표 — 화면 쪽) | 닿은 자리 |
|---|---|
| 참고 자료 종류 나열 지점 — `viewModels.ts:1030-1031` · 함께 보는 곳 `useConversations.ts:13,28,83,305,319,384` · `api.ts:44,744-756` | `viewModels.ts`(`inbox_message` + `turn_id`·`label`) · `useConversations.ts:84`(합치기 키). 나머지(`api.ts` 전송 · `useConversations` 전송 길)는 타입을 따라가 그대로 — 바꿀 것 없음. 프론트에 `"task" \| "work_request"` 를 손으로 나열한 곳은 다시 세어 **이 타입 하나뿐**이다 |
| 서랍 열며 보내기 `askAx\|isAxOpen\|sendCurrent(\|onAskAx` — `App.tsx:186,210,307-317,481,609-650` · `TodayPage.tsx:50,71,290` | `askAx` 에 `context` 인자 · 메시지함에 `onAskAx` · 오늘 화면 입구(`App.tsx:498`)는 그대로(참고 자료 없음) |
| 메시지 행·스레드 `scax-imsg\|ThreadLine\|onOpenThread\|scax-mail__actions` — `RoomView.tsx` 행·스레드 줄·`toLine`·패널 · `inbox.css` · `MailView.tsx:358-364` | 행 `Message`(막대·표지·강조·`data-message-id`) · `toLine`/`localLine`(`madeTaskCount`) · 패널(막대·사건) · 대화 열(막대·0개 스레드·짚기·사건) · `inbox.css`(`.scax-imsg { position: relative }` 외) · 메일 머리. `ThreadLine` 은 그대로(답글 N개 줄은 지금처럼) |
| 업무 출처 화면 — `WorkModals.tsx:390,2142-2170,2270` · `MyWorkPage.tsx:704-729` · `workRows.ts:208` | 출처 행에 원래 메시지 링크(`WorkModals.tsx:2176~`) · 서랍 prop. `originSentence`(`:391`) · `MyWorkPage` 의 `openSource` · `workRows.ts` 는 `origin.source` 만 보므로 그대로 |
| 사건 `viewModels.ts:1650` · `InboxPage.tsx` 구독 | 사건 타입에 `inbox.message_updated` · `InboxPage` 는 이미 모든 사건을 허브로 흘린다 — 방·메일·스레드 패널이 허브에서 받는다(코드 변경 없음) |

**표 밖에서 더 닿은 자리**
- `TaskDetailDrawer` 를 그리는 화면 셋(내 업무 · 오늘 · 캘린더)에 `onOpenInboxMessage` 를 내렸다 — 표는 출처 행만 셌다. 그래야 어느 화면에서 업무 상세를 열어도 링크가 선다
- `App.tsx` 에 메시지함으로 가는 통로(`inboxFocus` · `openInboxMessage`) — 업무 화면의 `focusTaskId` 와 같은 결
- `useConversations.ts` 합치기 키(위)

## 3. 새 시험 (21개)

| 파일 | 시험 |
|---|---|
| `features/inbox/InboxPage.test.tsx` (+12) | 슬랙 행 막대 = 아이콘 셋 · 툴팁 문구 셋 · 단추 글자 없음 · 행 `tabindex=0` / 카톡 = AX 둘 / **답글 0개 메시지 → 「스레드에 답글」 로 패널**(`thread_ts` 조회 · 입력창) · 패널 안 줄 막대는 AX 둘(스레드 아이콘 없음) / 로컬 줄에는 막대 없음 / 메시지 AX 업무 생성·AX 요약 → 말풍선 본문 + `inbox_message` 참고 자료 / 메일 머리 순서 넷 + 메일 문구 둘 / `inbox.message_updated` → 방 다시 읽어 「업무 만듦」(새로고침 없이 · 막지 않음) / 메일도 / 출처 링크로 들어오면 그 방을 열고 그 메시지 강조 + 짚기 완료 알림 / 없는 메시지 → 「찾지 못함」 / `onAskAx` 를 안 받은 메시지함은 스레드 입구만 |
| `App.test.tsx` (+1) | 메시지함 → 막대의 AX 업무 생성 → **새 대화 POST** + 대화 메시지 전송 본문에 `body` = 「이 메시지 읽고 업무를 생성해 줘」 · `context` = `[{inbox_message, msg-7, 1, true}]` |
| `features/chat/MessageListReferences.test.tsx` (새 · 3) | 그 턴 말풍선 바로 아래에 서버 글자 그대로 · 다른 턴엔 없음 / 스레드·메일·카톡 모양도 그대로 / `label` 없음·업무 참고 자료는 줄 없음 |
| `features/work/TaskDetailDates.test.tsx` (+3) | 「판단 보기」 와 「원래 메시지 · 슬랙 #pilot-launch」 가 함께 · 누르면 그 메시지로 / 메일은 「원래 메일 · …」 / 통로 없는 화면은 글자만 |

## 4. 검증 — 돌린 시험 파일과 수치(직렬 · 관련 파일만)

| 시험 파일 | 결과 |
|---|---|
| `features/inbox/InboxPage.test.tsx` | 25/25 |
| `features/inbox/InboxAttachments.test.tsx` | 11/11 |
| `features/inbox/MailFrame.test.tsx` | 4/4 |
| `features/inbox/inboxModel.test.ts` | 15/15 |
| `features/chat/ChatDrawer.test.tsx` | 65/65 |
| `features/chat/MessageListReferences.test.tsx` | 3/3 |
| `features/chat/MessageListMeetingCards.test.tsx` | 2/2 |
| `features/chat/ChatButtonStates.test.tsx` | 8/8 |
| `features/chat/AssistantMarkdown.test.tsx` | 8/8 |
| `features/chat/useConversations.test.tsx` | 4/4 |
| `App.test.tsx` | 34/34 |
| `features/work/TaskDetailDates.test.tsx` | 31/34 — **실패 3 = 기준선(`fe-baseline.md`)의 「메타 정보 격자」 기존 실패 그대로**(이 판 새 시험 3 은 통과) |
| `features/work/TaskDetailRelations.test.tsx` | 35/35 |
| `features/work/TaskDetailStateSelect.test.tsx` | 35/35 |
| `features/work/MyWorkPage.test.tsx` | 43/43 |
| `features/today/TodayPage.test.tsx` | 3/3 |
| `features/calendar/CalendarPage.test.tsx` | 20/20 |
| `features/calendar/CalendarInteractions.test.tsx` | 31/31 |
| `features/calendar/calendarModel.test.ts` | 34/34 |
| `features/calendar/calendarWrites.test.ts` | 40/40 |
| `lib/labels.test.ts` | 10/10 |
| **합계** | **21 파일 · 464 중 461 통과 · 실패 3(전부 기준선)** — 이번 판 실패 0 |

- 빌드 `make frontend-build` 통과 · `tsc -b` 0 오류 · 전체 시험은 돌리지 않았다(코디 지시)

## 5. 미결 · 주의점

1. **WP4-BE 와 같이 나가야 한다** — 화면이 쓰는 서버 계약: 대화 메시지 `context[].resource_type="inbox_message"`(남의 메시지 404) · 대화 응답 `context_references[].turn_id`·`label`(계약 고정 1 — 없으면 한 줄이 안 선다) · 방 메시지·메일 응답 `made_task_count` · 사건 `inbox.message_updated {message_id, room_id|null}` · 업무 상세 `origin.message {message_id, source_kind, room_id, label}`. 옛 서버면 `inbox_message` 참고 자료가 422/404 로 거절돼 서랍의 말풍선이 실패 줄로 선다
2. **「업무 만듦」 다시 읽기 범위** — 방은 사건을 받으면 **최신 페이지**를 다시 읽어 합친다(지금 새 메시지 사건과 같은 길). 위로 많이 올려 읽어 둔 오래된 메시지의 표지는 그 방을 다시 열 때 선다
3. **툴팁은 CSS** — DS 에 툴팁 부품이 없어 `data-tip` + `::after` 로 그렸다(새 부품을 만들지 않음 — P-8). 접근성 이름은 `aria-label`(같은 글자)
4. **짚기(OQ-817)** — 첫 페이지에 없으면 위로 최대 3쪽까지 읽어 찾는다. 더 오래된 메시지는 「메시지를 찾을 수 없습니다」. 스레드 답글이면 그 스레드 패널을 열고 부모 줄을 강조한다(패널 안 답글 강조는 하지 않음)
5. **출처 링크로 연 카드가 레일에 없을 때**(다른 출처 탭·페이지 밖) 출처 값(`label`)으로 카드를 세워 연다 — 방 머리 이름은 방을 읽으면 서버 이름으로 바뀐다. 메일은 열면 짚기 끝(그 메일이 곧 그 메시지)
6. **업무 요청(요청 상세)의 원래 메시지 링크**는 이번에 그리지 않았다 — SPEC §4.8 ③ 은 「업무 상세 응답의 `origin`」 만 정했다(요청 상세에 출처 칸이 생기면 같은 부품으로 붙인다)
7. 완료 조건(실물 · 앱 — S-11 ~ S-14 · 출처 링크 왕복)은 코디 E2E 몫

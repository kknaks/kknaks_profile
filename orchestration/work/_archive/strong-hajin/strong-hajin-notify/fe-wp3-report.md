# WP3-FE 결과 보고 — 알림 화면 · 사이드바 점 · 설정 알림 탭

## 상태: done (커밋 없음 · 워크트리에 변경만)

- SSOT: WORK-013 「Phase WP3-FE」 · SPEC-011 v0.2.2 §2.1~§2.3 · §4.4 · §4.5 · 확정 시안 `handoff/alerts/*` · `handoff/settings/*` · design-change-1~4
- **시작 조건 예외(코디)**: WP2-BE 는 쓰는 중이다. 알림 API 모양은 **SPEC §4.5 대로** 지었고, 서버와 다른 자리는 §6 에 모았다. `backend/` 는 손대지 않았다
- 경로는 `frontend/` 기준. `src-tauri/` · 회의 WS 는 손대지 않았다

## 1. 계약 체크박스 — 6/6

| # | 계약 | 구현 위치 |
|---|---|---|
| 1 | **알림 목록 화면** `surface="notifications"` — 시안 A 그대로 · 스크롤 끝 자동 이어 불러오기(실패면 끝에 한 줄) · [모두 읽음] = 전부 · 비활성은 전체 기준 | **화면 종류**: `src/lib/viewModels.ts:1` `ProductSurface` 에 `"notifications"` · `src/App.tsx:732-741` 렌더 · `:637` 「한 화면에 갇히는」 스크롤 · `surfaceLabel` 「알림」<br>**화면**: 새 `src/features/notifications/NotificationsPage.tsx`<br>• 머리(`:269-293`): 「안 읽음 N」(Badge count — `titleEnd` 자리) · [모두 읽음](`disabled` = 전체 안 읽음 0 — 필터와 무관)<br>• 필터 넷 · 테마 탭 수(`:295-298`)<br>• 날짜 구분 넷(`:313-326`, 서울 기준 `labels.ts:1951` `notificationDay`)<br>• 한 줄 `AlertRow`(`:51-83`): 표식(실패 = `--fail` · `circle-exclamation`) · 문장 · 보조 줄 · 테마 → 꼬리표 → 시각 → 가는 곳 · 안 읽음 점<br>• **상태 넷**(`:300-311`): 로딩(제목 막대 1 + 줄 6) · 오류(+다시 시도) · 빈(전체 · 테마별 `EMPTY_BY_FILTER`) · 기본. 빈(전체)·로딩·오류는 머리 수·[모두 읽음]·필터 수를 숨긴다<br>**이어 불러오기**(`:170-207`): 끝 표지를 `IntersectionObserver` 로 본다(없는 환경은 스크롤 거리). 실패면 「더 불러오지 못했습니다 · 다시 시도」, 마지막 쪽이면 표지가 없다(단추 없음)<br>**[모두 읽음]**(`:256-267`): 본문 없는 `POST /api/notifications/read-all` → 모든 줄 읽음 · 요약 0 · 점 다시 읽기 |
| 2 | **문장 함수 하나**(`labels.ts`) — `kind` · `data` → 문장 · 보조 줄 · 가는 곳 · OS 알림도 이 함수 | `src/lib/labels.ts:2039` `describeNotification(n)` → `{parts, sub, destination, title, text}`<br>• 종류 19 전부(§4.2-1)<br>• `parts` = 시안 `Sentence` 조각(`{b}` 누가 · `{q}` 무엇을)<br>• `title` = 「테마 · 꼬리표」, `text` = 맨 글자 — **WP4 OS 알림의 제목·본문**<br>• 가는 곳 `destinationOf`(`:2023`) — `target` 이 있으면 그것으로, `null` 이어도 종류로 짐작한다<br>• 시각 `notificationTime`(`:1969` — 오늘 상대 · 「어제 HH:MM」 · 「M월 D일(요일) HH:MM」 · 「M월 D일(요일)」)<br>• 꼬리표 `notificationRelationLabel`(`:1798` · 16) · 화면 문구 `notificationScreen`(`:1819`) |
| 3 | **실시간** — `notification.upserted` 끼우기/고치기 · `notification.read` 반영 · 요약 다시 읽기 | `NotificationsPage.tsx:209-237` `useEventStream`<br>• upserted: 지금 필터에 맞으면 새 줄은 맨 위, 있는 줄은 그 자리에서 고친다(목록 전체는 다시 읽지 않는다) → 요약 다시 읽기<br>• read: `notification_ids` · `{all, theme}` 반영 → 요약 다시 읽기<br>• `resync`: 목록 · 요약 다시 읽기<br>(id·순번 중복은 WP1 채널이 이미 거른다) |
| 4 | **누르면** — 읽음 + `target` → 포커스 상태(`onOpenResource` 와 같은 함수) · 메시지 줄 강조 · `target: null` 이면 「열 수 없는 항목입니다」 | `src/App.tsx:354-402` **`openFocus(target)`** — 업무(task · 요청) · 회의 · 프로젝트 · 보고 · 메시지함 · 설정 탭 · 알림 목록. **AX 서랍 `onOpenResource` 의 업무·요청·회의·프로젝트·보고 갈래도 이 함수로 바꿨다**(`:857-893`)<br>`:438-457` **`openNotification(id, target, label)`** — 읽음 API(`POST …/{id}/read` → 점 다시 읽기, 실패면 토스트) → `target` 이 `null` 이면 공통 토스트 「열 수 없는 항목입니다」, 아니면 `openFocus`. **WP4 OS 알림 클릭도 이 자리를 부르면 된다**(묶음 = `id: null`)<br>메시지함: `inboxFocus`(출처 링크 SPEC-008 §2.9 ④ 와 같은 길) — 방 + `message_id` 면 그 줄로 스크롤 · 강조(`RoomView` `focusMessageId`). **`message_id` 가 없는 방 대상은 방만 연다** — `InboxPage.tsx:258-261`(전에는 짚을 메시지가 없으면 `onFocusHandled` 가 영영 안 불렸다)<br>설정: `settingsFocus`(`App.tsx:349`) → `SettingsPage initialTab` + `key` 로 그 탭(`:746-747`). 사이드바로 들어오면 비운다 |
| 5 | **사이드바 점 둘** — `disabled` 걷기 · `dot` 넘기기 · `GET /api/me/badges` 를 §2.2 의 때마다 | `App.tsx:601` 알림 줄 `disabled` 를 걷고 `dot: badges.notifications`(옛 주석 「셀 값이 없으므로」는 지웠다) · `:593` 주 메뉴 매핑이 `dot` 을 넘긴다(메시지함 = `badges.inbox`)<br>`:403-430` `refreshBadges` — 겹쳐 불리면 하나만 날리고 끝난 뒤 한 번 더 읽는다. 회원이 바뀌면 끄고 다시 읽는다. 응답 모양이 아니면 꺼짐으로 둔다<br>**때**: 앱 시작(로그인 · `personaId` 바뀜) · `NavBadgeWatcher`(`:93-99`, SSE `ready` · `resync` · `notification.upserted` · `notification.read` · `inbox.message_arrived` · `inbox.message_updated`) · 알림 읽음 뒤(`openNotification` · [모두 읽음]) · **메시지함 읽음 뒤**(`InboxPage` 새 prop `onReadChanged` — 메일 · 방 · 모두 읽음 성공 시, `InboxPage.tsx:49,93-95`)<br>그리기는 `SideNav` 의 `dot` 그대로(부품 무변경) |
| 6 | **설정 알림 탭** — 시안 B 그대로 · `Switch`(`settingsParts.tsx`) · 바꿀 때마다 저장 · 실패 되돌림 · 409 다시 읽기 · `tab=notify` 콜백 쿼리 | **메뉴**: `SettingsPage.tsx:37` `SettingsTab` 에 `notify` · `:52` `disabled` 를 걷었다(눌림 거름 · 툴팁 · 꼬리 숫자 예외 삭제) · `:261` 탭 본문<br>**콜백 쿼리**: `App.tsx:79` `tab=notify`<br>**화면**: 새 `src/features/settings/NotifySection.tsx` — intro · 「알림 받기」(꺼짐 문구) · 테마 카드 셋(머리 스위치 · 「N개 중 M개」/「꺼짐」) · 항목 체크(DS `CheckboxBox`) · 메시지 note · 받는 경로 카드 없음. 전체 끔이면 `--off`(머리까지 흐림 · 테마 스위치 잠금), 테마 끔이면 그 목록 흐림·잠금<br>**저장**(`:71-100`): 바꿀 때마다 `PUT /api/me/notification-settings`(전체 + 읽은 `version`). 저장은 **한 줄로 세운다** — 앞 저장의 새 version 으로 뒤 저장을 보낸다. 저장 중 **그 칸만** 잠근다. 실패면 그 칸만 되돌리고 토스트 「알림 설정을 저장하지 못했습니다」. `409` 면 토스트 + 서버 값 다시 읽기(`:88`)<br>**Switch**: `settingsParts.tsx:31` — `<button role="switch" aria-checked>` + `__knob` · `disabled` 지원<br>**CSS**: `styles/settings.css` 끝에 시안 「알림 설정」 블록 그대로 + `.scax-switch:disabled{cursor:default}` 한 줄 |

**API · 타입**(`src/lib/api.ts:731-770` · `src/lib/viewModels.ts:1024-1082`): `getNotifications({theme,cursor,limit})` · `getNotificationSummary` · `markNotificationRead` · `markAllNotificationsRead` · `getNavBadges` · `getNotificationSettings` · `saveNotificationSettings` / `Notification`(§4.5-2 모양) · `NotificationTarget`(§4.5-2 3 · 7갈래) · `NotificationPage` · `NotificationSummary` · `NavBadges` · `NotificationSettings`. 사건 채널의 `StreamNotification` 은 `Notification` 과 같은 모양이 됐다.

**셸 머리 `titleEnd`**(`src/shell/AppShell.tsx:28-31,51,67-75` · App seam `registerSurfaceTitleEnd`) — 시안 `AppHeader` 의 슬롯을 들였다. 주지 않으면 옛 마크업 그대로다(다른 화면 무변경 · AppShell 시험 통과). ⚠ 프로젝트 화면(WORK-005 D-25)은 같은 슬롯을 「셸 신설 안 함」으로 버렸던 선례가 있다. 이번엔 SPEC §2.1 이 머리에 「안 읽음 N」 을 정해 들였다 — 코디가 확인할 자리다.

**함께 고친 주석**(WORK-013 WP2 표 「알림을 내지 않는다 문구」 의 화면 쪽 셋): `labels.ts` 회의 공유 문구 주석 · `api.ts` `shareMeetingWith` docstring · `ShareModal.tsx:22` — 「알림은 가지 않는다」를 「공유받은 사람의 알림 설정이 정한다(M12)」로 바꿨다. 화면 문구(「공유했습니다.」)는 그대로다.

## 2. Code Surface WP3 표 대비

| 패턴 | 표 | 지금 prod / test | 처분 |
|---|---|---|---|
| `getNotifications\|markNotificationRead` | 2/1(정의만) | 7/3 · 0 | 정의를 고치고(쿼리 · 쪽) 화면 · App 이 부른다 |
| `type Notification\b\|Notification[]\|<Notification>` | 5/2 | 6/3 · 5/2 | §4.5-2 모양으로 바꿨다 |
| `type ProductSurface` | 1 | `"notifications"` 를 더했다 | App 조건부 렌더 1줄 더함 |
| `utilityItems\|visibleNavigation.map` | 8/2 | 8/2 | 알림 줄 `disabled` 걷기 · `dot` · 주 메뉴 `dot` |
| 점 `dot?:\|scax-nav-item__dot\|\bdot:` | 4/3 | 5/3 · 1/1 | 부품·CSS 무변경, App 이 값을 넘긴다 |
| 설정 탭 `notifyOutOfScope\|id: "notify"\|"notify"` | 6/2 | 4/2 · 0 | `notifyOutOfScope` 삭제 · `notify` 탭 |
| 스위치 `scax-switch\|role="switch"` | 8/1(CSS 만) | tsx 6/2 · test 3/1 · CSS 11줄 | `Switch` 부품 + 알림 탭 |
| 포커스 이동 | 42/5 · 6/2 | 42/5 · 6/2 | `openFocus` 한 함수로 모았다(`onOpenResource` 다섯 갈래 포함) |
| 토스트 `putNotice(` | 5/1 | 5/1 | 「열 수 없는 항목입니다」 · 설정 저장 실패 · 읽음 실패는 `setError`(같은 통) |
| 메시지함 안 읽음 | 11/3 · 5/2 | 11/3 · 7/2 | 셈은 그대로. 메시지함 점은 badges, 읽음 뒤 점 다시 읽기 |
| 시안 옮기기 | — | — | `RELATIONS` 16 · `THEMES` · `EMPTY_BY_FILTER` · 날짜 구분 · `alerts.css`(새 `styles/alerts.css` · `index.css` 에 한 줄) |

**표 밖에서 고친 것**
1. `InboxPage.tsx` — 방 대상에 `message_id` 가 없으면 짚기가 안 끝나던 자리. 새 prop `onReadChanged`
2. `AppShell.tsx` `titleEnd`
3. 회의 공유 주석 셋

## 3. 시안 대조

| 축 | 시안 | 코드 | 결과 |
|---|---|---|---|
| 설정 항목 16 | `settings/js/data.js` `NOTIFY_GROUPS`(업무 8 · 메시지 3 · 회의 5 · design-change-3·4 문구) | `labels.ts:1859` `notifySettingsCopy.groups` — id · label · desc 글자 그대로. 기본값은 서버가 준다(시안 `on` = 업무 `comment` 만 끔 — 시험 대역이 같은 값) | **16/16** · 시험이 문구 둘(⑥ change · ⑦ answer)과 「8개 중 7개」를 단언 |
| 꼬리표 16 | `alerts.v1.jsx` `RELATIONS` | `labels.ts:1798` | **16/16** · 시험이 표 전체를 대조 |
| 상태 넷 | 기본 · 빈 · 로딩 · 오류(DevSwitch) | `NotificationsPage.tsx:300-326` | **4/4** · 머리 숨김 규칙 포함 |
| 필터 · 테마 | `FILTERS` · `THEMES`(표식 아이콘 셋) | `notificationScreen.filters` · `THEME_ICON` | 같음 |
| 날짜 구분 | 오늘 · 어제 · 이번 주 · 이전 | `notificationDay` — 서울 · 이번 주 = 월요일부터 | 같음 |
| 줄 모양 | 표식 · 문장 · 보조 · meta(테마 · 꼬리표 · 시각 · 가는 곳) · 점 | `AlertRow` | 같음. 줄 요소만 `<a>` → `<button>`(아래 DS-gaps ②) |
| 문장 | 목데이터 22줄의 짜임 | `describeNotification` | 시안 줄을 본뜬 26건을 시험이 단언(a01·a02·a04·a05·a06·a07·a08·a09·a12·a14·a15·a16·a18·a19·a20·a21·a22 꼴) |
| 시안에서 다르게 둔 것 | — | — | ① 「요청 협의」 문장은 SPEC 그대로면 「…업무를 조건을 제시했습니다」라 「업무**에** 조건을 제시했습니다」로 ② 회의록 실패 보조 줄은 사유가 서버에 없어 「회의에서 다시 정리할 수 있다」 ③ 외부 발신자 이름에는 「님」을 붙이지 않는다(받은 이름 그대로 — §6-4) |

## 4. DS-gaps 후보 (기록만 · DS 로 올리지 않음)

1. **Switch** — DS 에 Toggle 부품이 없다(`ds/FormControls.tsx:9`). 설정 부품 `settingsParts.tsx` 에 두었다. 크기는 시안 40×22, DS 문서 Toggle 규격은 36×20(`docs/design/design-system-v2.dc.html:914`)이다. 쓰는 곳은 설정 하나다
2. **줄 전체가 누르는 자리** — 시안은 `<a href>` 이지만 우리 이동은 앱 상태라 `<button>` 으로 세웠다. `alerts.css` 에 단추 기본 모양을 지우는 규칙 한 줄을 더했다
3. **StatusNote(title · desc · action)** · **Skeleton(variant · width)** — 우리 DS 부품 API 가 시안과 다르다. 메시지함 선례처럼 `Empty variant="error"` 와 `scax-skeleton--*` 클래스로 그렸다
4. **AppHeader `titleEnd`** — 셸 슬롯을 신설했다(§1 끝 ⚠)

## 5. 시험 (관련만 — 브리프 · P-8)

| 명령 | 결과 |
|---|---|
| `cd frontend && npx vitest run src/shell/AppShell.test.tsx src/features/settings/SettingsPage.test.tsx src/SettingsLanding.test.tsx src/App.test.tsx src/features/notifications/NotificationsPage.test.tsx src/features/settings/NotifySection.test.tsx src/lib/notificationLabels.test.ts src/features/inbox/InboxPage.test.tsx src/lib/eventStream.test.ts --no-file-parallelism` | **9 files · 151 passed · 0 failed** · 17.2s |
| `cd frontend && npx tsc --noEmit` | **0 오류** |

- WP1 끝(95 = 5파일)에서 늘어난 수: 새 파일 셋 51(NotificationsPage 12 · NotifySection 8 · notificationLabels 31) + AppShell 1 + App 3 + Landing 1. 바뀐 것은 SettingsPage 1(같은 수)이다
- **바뀐 disabled 단언 둘**: `AppShell.test.tsx`(알림 줄 → 화면 · fixed 스크롤 · 활성) · `SettingsPage.test.tsx`(「범위 밖 · 눌리지 않음」 → 「열려 있음 · 그 탭 · 제목」)
- **새 시험이 잡은 제품 결함 하나**: App 이 넘긴 인라인 `onReadChanged` 때문에 알림 화면의 머리 등록 effect 가 매 렌더 다시 돌아 **무한 렌더**가 났다(App 주석의 그 함정). 콜백을 ref 로 들어 고쳤다(`NotificationsPage.tsx:252-267`)
- 시험 이름별 덮는 것: 꼬리표 · 날짜 구분(서울 자정 경계) · 빈/로딩/오류 · 자동 이어 불러오기(+실패 한 줄) · [모두 읽음] 전부(테마 탭에서도 · 필터 무관 비활성) · 이동(task · 방+메시지 · 회의 · 설정 탭 · null 토스트, 누를 때마다 읽음 API) · 점(켜짐 · 사건 뒤 꺼짐 · 메시지함 점) · 설정 저장 · 줄 세운 version · 되돌림 · 그 칸만 잠금 · 409 다시 읽기 · 전체/테마 끔 · Switch
- `make frontend-build` 는 돌리지 않았다(브리프가 `tsc --noEmit` 으로 정함 · 코디 몫)

## 6. 서버와 맞춰 볼 자리 (WP2-BE 완료 뒤 코디)

워크트리의 지금 서버(`backend/` WP2 진행 중)를 읽은 결과다:

1. **항목 모양** — 서버 `NotificationView`(`modules/notifications.py:31`)는 아직 옛 모양(`summary` · `actor_id` · `resource{…}`)이다. 화면은 §4.5-2(`seq · kind · theme · item · relation · failure · actor · subject · data · target · created_at · updated_at · read_at`)를 읽는다. 생성기(`modules/notification_events.py`)의 `KINDS` 19 · 테마/항목 · `RELATION_PRIORITY` 16 은 화면과 같은 이름이다
2. **경로** — 지금 서버에는 `GET /api/notifications`(옛 배열 응답 — 화면은 `{items, next_cursor}`) · `POST …/{id}/read` 만 있다. `summary` · `read-all` · `/api/me/badges` · `/api/me/notification-settings`(GET/PUT)는 아직 없다. 화면은 없어도 깨지지 않는다(요약은 목록으로 세고, 점은 꺼짐, 설정은 오류 + 다시 시도)
3. **`data` 칸 이름 — 화면이 가정한 것**(SPEC 표에 이름이 없는 것 위주):
   - `work.assigned`(`displaced`) → `data.new_assignee_name`(새 담당 이름)
   - `message.slack`(채널 합침) → `data.senders` = 이름 문자열 배열 · `data.count`
   - `work.changed` → `before`/`after` = 날짜(`YYYY-MM-DD`) 또는 ISO
   - `meeting.changed` → ISO 시각
   - `meeting.invited` → `starts_at` · `ends_at` · `place`
   - `message.mail` → `subject` · `attachment_count` · `account`
   - `message.integration_lost` → `channel` · `reason` · `account?` · `room_name?`
   - `meeting.minutes_ready` → `agenda_count` · `action_count`
4. **외부 발신자 이름** — `actor.external_name` 을 받은 그대로 쓴다(회원만 「이름님」). 시안은 메일·슬랙·카톡 사람에게 「님」을 붙이고 단체(「노을웍스 인사팀」)에는 붙이지 않았다. 서버가 사람/단체를 가르지 않으면 어느 쪽인지 화면이 알 수 없다 → 사용자·코디 판단
5. **`read-all`** — 화면은 본문 없이 `POST` 한다(`Content-Type: application/json` 머리는 붙는다). 서버가 빈 본문을 받아야 한다
6. **설정 `PUT`** — 화면은 `{enabled, themes, version}` 전체를 보낸다(테마의 `items` 는 그 테마 항목 전부). `409` 는 상태 코드로만 가른다(본문 코드 `SETTINGS_VERSION_CONFLICT` 는 읽지 않음)
7. **`target` 메시지함 방** — `message_id` 가 없으면 방만 연다. `thread_ts` 는 지금 쓰지 않는다(스레드 패널 열기는 2루프 후보)
8. **`notification.read`** — `{notification_ids}` 또는 `{all: true, theme}` · `theme` 이 `null` 이면 전부로 본다

## 7. 미결

1. 앱 실물(완료 조건)은 코디 몫이다 — WP2-BE 반영 · 스택 재기동(P-4) 뒤: 목록 · 눌러서 고른 상태로 · 점 둘 켜짐/꺼짐 · 설정을 꺼서 그 알림이 안 생김
2. `AppHeader titleEnd` 신설은 프로젝트 선례(D-25 「셸 신설 안 함」)와 다르다 — 코디 확인
3. 외부 발신자 「님」(§6-4) · 문장 다듬은 두 곳(§3 끝)은 사용자 E2E 에서 보고 2루프
4. WP4 가 받는 것: `describeNotification(n).title/text`(OS 글자) · `openNotification(id | null, target)`(클릭)

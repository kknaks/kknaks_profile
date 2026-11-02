# 코드 검수 — WORK-011 FE-a·FE-b (커밋 `496fc1e`) (2026-10-06)

## 판정: FAIL

FAIL 은 **1건**이다. 슬랙 메시지 링크와 URL 미리보기 링크가 `openLink` 를 거친다. 그런데 `openLink` 가 **스킴을 보지 않고** 브라우저에서 `window.open` 한다. 그래서 `javascript:` 링크가 우리 origin 에서 실행될 수 있다. 한 줄로 고칠 수 있는 크기다.

나머지는 탄탄하다.
- 메일 iframe 샌드박스와 링크·원격 이미지 처리
- 기기 토큰을 남기지 않는 흐름
- OAuth JSON 시작
- api.ts 와 be3 모양의 정합
- 캐릭터 진입점 둘 제거
- 시안의 화면·상태 문구 전수

> 검수 방법: `git show 496fc1e` 로만 읽었다(34 파일 +6726/−159). 시험·빌드는 돌리지 않았다(fe-report: tsc 0 · vitest 1352 통과/5 실패는 날짜 의존 기존 부채).
> 기준: SPEC-008 v0.5.1 §2·§4 · 시안 `P2/` Inbox·Settings + DC-1~6 · `be3-report.md` · `fe-report.md`.
> 약칭: `F/` = `frontend/src/`.

## FAIL

| # | 근거 파일:줄(커밋 496fc1e) | 무엇 | 고칠 것 |
|---|---|---|---|
| **F-1** XSS | `F/features/inbox/inboxStream.ts` `openLink`(`openExternal(url)` 이 `absent` 면 `window.open(url, "_blank", "noopener,noreferrer")` — **스킴 검사 없음**) ← `F/features/inbox/RoomView.tsx:153-163`(슬랙 링크 조각 `onClick` 이 `openLink(seg.href)`) · `RoomView.tsx:650-652`(퍼머링크) · URL 미리보기 `href` / 출처 `F/features/inbox/inboxModel.ts:102-114` `parseInline`(`<target\|label>` 의 target 을 그대로 href) · `:202`(rich_text `element.url` 그대로) · `:343`(첨부 `title_link`·`original_url`·`from_url` 그대로) | 슬랙 원문은 사람만 쓰는 게 아니다. **봇·앱·웹훅 메시지도 그대로 쌓인다**(D-13). 원문의 `<javascript:…\|보기>` · `blocks` 의 link `url` · `attachments[].title_link` 는 보낸 쪽이 정한다. React 19 는 `href` 속성의 `javascript:` 는 막지만, 여기는 `onClick` 이 기본 동작을 막고 **원문 문자열을 `window.open` 에 넘긴다.** 브라우저에서는 `about:blank` 새 창이 만든 쪽 origin 을 물려받는다 → 그 스크립트가 **세션 쿠키로 `/api` 를 부를 수 있다**(답장 보내기·기기 토큰 발급 포함). 데스크톱은 `open_external` 이 http(s) 만 받아 막힌다(`guard.rs`) — **브라우저만** 열린 구멍이다 | `openLink` 첫 줄: `new URL(url)` 로 풀어 `http:`·`https:`·`mailto:` 만 통과, 나머지는 무시. 같은 검사로 `parseInline`·`richBlock`·언퍼일이 만드는 `href` 도 걸러 링크 대신 글자로 그린다. 시험 한 줄: `javascript:` 링크를 눌러도 `window.open` 이 불리지 않는다 |

## 항목별 판정

### 보안

| 항목 | 판정 | 근거 |
|---|---|---|
| 메일 iframe 샌드박스 | PASS | `F/features/inbox/MailFrame.tsx` `MAIL_SANDBOX = "allow-same-origin allow-popups allow-popups-to-escape-sandbox"` — **`allow-scripts` 없음.** `allow-same-origin` 은 스크립트가 없을 때만 안전한 조합이다. 담는 것은 서버 안전본(`srcDoc={html}` — CSP meta 가 맨 앞)뿐이다. 부모가 `contentDocument` 로 높이를 잼(W3-6) · `<style>` 은 부모가 넣음(CSP `style-src 'unsafe-inline'` 범위). 시험 `InboxPage.test.tsx:217` |
| 메일 링크 열기 | PASS | `MailFrame.tsx` `prepare` — iframe 문서의 `click` 을 가로채 `openLink`. 서버 소독이 href 를 `http(s)`·`mailto`·`tel`·`#` 로 이미 줄였으므로 F-1 과 달리 안전하다(F-1 수정 뒤에도 그대로). 가운데 클릭(`auxclick`)은 가로채지 않는다 → 소독본의 `target=_blank` + `allow-popups-to-escape-sandbox` 로 새 탭이 열린다(웹은 허용 · 데스크톱 macOS 는 셸이 새 창을 막음 — 경미 W-6) |
| 원격 이미지 | PASS | `MailFrame.tsx` `showImages` — 「이미지 보기」를 눌러야 `data-ax-remote-src` → `inboxRemoteImageUrl`(서버 프록시)로만 `src` 를 단다. 차단 개수 안내 |
| 기기 토큰이 남지 않나 | PASS(경미 W-3) | `F/features/settings/KakaoSection.tsx:130` — `kakaoStoreDeviceToken((await issueDeviceToken(…)).token)` 한 식 안에서만 산다(상태·스토리지·로그 없음). `F/lib/shell.ts` `kakaoStoreDeviceToken` 의 경고 로그에 토큰 없음. 커밋 diff 에 `localStorage`·`sessionStorage`·`console.log` 추가 0. 「이 Mac 연결」 단추는 앱 웹뷰에서만. 시험 `SettingsPage.test.tsx:218` · `shellKakao.test.ts:44` |
| OAuth — 동의 URL 이외로 안 가나 | PASS(경미 W-4) | `F/features/settings/consent.ts` `beginConsent` — 서버 JSON 의 `authorize_url` 만 쓴다. 데스크톱 `open_external` · 브라우저 `location.assign`. 302 를 따라가지 않음(F-2) · `focus`/`visibilitychange` 재조회. 시험 `SettingsPage.test.tsx:129` |
| api.ts 밖 fetch · 셸 invoke 자리 | PASS | 새 fetch 는 `F/lib/api.ts` `sendForm`(multipart) 뿐 · 셸 호출은 `F/lib/shell.ts` 만(fe-report 주장 확인) |

### 계약 (api.ts ↔ be3-report)

| 항목 | 판정 | 근거 |
|---|---|---|
| 경로·메서드·필드 | PASS | `F/lib/api.ts`(diff 끝 블록): 목록 `sender`·`snippet`·`unread_counts` · 메일 본문 `safe_html`·`to/cc/reply_to`·`sent_replies` · 방 `room`·`messages[{id,key,at,author,thread_key,raw,attachments}]` · 읽음 `{up_to_ts}` · 답장 multipart(`text`·`thread_ts`·`files` / `body`·`reply_all`·`to`·`cc`·`files`) + `Idempotency-Key` · 프로필 `PUT` multipart `file` · 비밀번호 `{current, new}`(백엔드 `PasswordChangeCommand` 와 일치) · reset-account = 세션 · 카톡 수집기 라우트는 웹에 없음 |
| 콜백 결과 | **WARN(W-1)** | `F/App.tsx` `readLanding` 은 `connect=ok\|denied` 만 읽는다. 백엔드 `settings_return_url` 은 교환 실패 때 **`connect=error`** 도 보낸다(BE-1 `application.py` `complete_callback`) → 실패가 조용히 사라진다 |
| 첨부 `state` 이름 | 경미(W-2) | `F/lib/viewModels.ts` `InboxAttachment.state` 에 `"remote"` 가 있다. 백엔드 저장값은 `"reference"`(BE-1 `ck_external_attachments_state`)다. 동작은 부정 목록(`expired`·`too_large`·`not_stored`·`pending`)으로 판정해 맞게 돌지만, 타입·시험 픽스처(`InboxPage.test.tsx:38-39`)가 실제와 다르다 |
| available-rooms | 의존 | `listSlackAvailableRooms` 는 SPEC 모양으로 부른다. **백엔드에 아직 없다**(BE-2·3 검수 F-2) — 백엔드가 고쳐지면 그대로 붙는다 |

### UX (시안·SPEC §2)

| 항목 | 판정 | 근거 |
|---|---|---|
| 메시지함 2/3열 · 폭 전체 · 스레드 420 | PASS | `F/styles/inbox.css:257` `.scax-thread-panel{flex:0 0 420px}` · 대화·메일 폭 제한 없음(카드형 부품만 폭) · `RoomView.tsx` 「답글 N개」 → 오른쪽 패널 · 시험 `InboxPage.test.tsx:278` |
| 네 상태 · 빈/출처 빈/오류 | PASS | `labels.ts`: 「쌓인 메시지가 없습니다」·「이 출처에는…」·「…불러오지 못했습니다」·「고른 메시지가 없습니다」 · 시험 `:172` |
| 답장 상태 | PASS | 작성·보내는 중·보냄·실패·다시 보내기(같은 멱등 키) · 메일 「한 번에 25MB까지」·합계 초과 차단 · 「보낸 답장」 · 시험 `:234`·`:298` |
| 카톡 본문 | PASS | 조회 전용(입력창·스레드·외부 열기 없음) · 만료 · 동영상 칩 · 「카카오톡에서 보기」·「(이모티콘)」·「너무 큼」 · 시험 `:318` |
| 설정 세 연동 | PASS | 메일(계정 여럿·실시간/채우는 중/끊김·해제 확인) · 슬랙(방 고르기 창·실명·`앱`·추가됨·끊김 = 모든 방 멈춤) · 카톡(앱 없음 → Releases · 브라우저/앱 웹뷰 갈림 · 상태 카드 · 읽기 불가 사유별 · 계정 바뀜 → reset-account · 카톡 꺼짐 문구) · 시험 `SettingsPage.test.tsx:137-260` |
| 프로필 | PASS | 명부 값 읽기 전용 · 이미지 즉시 저장·1MB · 캐릭터 고르면 저장 · 비밀번호 불일치/현재 틀림 · 알림 메뉴 비활성(D-37) · 시험 `:272-311` |
| 실패 배너(D-50) | PASS | 「{이름} 연결이 끊겼습니다」 · 시험 `InboxPage.test.tsx:196` |
| 시안과 다른 점의 근거 | PASS | fe-report 「SPEC·시안 어긋남」 — 앱 이름 중립(N-12) · 원격 이미지 안내·배너·「이 Mac 연결」·계정 바뀜 줄(SPEC 이 더한 자리) · PDF 미리보기 없음(서버 미제공) · `.scax-imsg*` 이름 변경(ax.css 충돌) — 각각 근거가 있다 |
| 캐릭터 진입점 둘 제거 | PASS | `F/App.tsx` diff — `onUserClick` 삭제 · `utilityItems` 설정이 surface 로 · `AssistantCharacterPicker`(+test) 삭제 · 프로필 설정 안으로 · 시험 `AppShell.test.tsx`·`AssistantPreferenceApp.test.tsx` 갱신 |

## 경미 (WARN)

| # | 근거 | 무엇 | 고칠 것 |
|---|---|---|---|
| W-1 | `F/App.tsx` `readLanding` | 콜백 `connect=error`(토큰 교환 실패)를 읽지 않아 사용자가 실패를 모른다 | `error` 도 받아 「연결하지 못했습니다 — 다시 시도」를 알린다 |
| W-2 | `F/lib/viewModels.ts` `InboxAttachment.state` · `InboxPage.test.tsx:38-39` | `"remote"` ↔ 실제 `"reference"` | 타입·픽스처를 `"reference"` 로 |
| W-3 | `KakaoSection.tsx:125-139` | 새 발급은 서버에서 **옛 토큰을 먼저 철회**한다. 그 뒤 키체인 저장(`kakao_store_device_token`)이 실패하면 그 Mac 의 수집기가 토큰을 잃는다 — 화면은 「넣지 못했습니다」만 보인다 | 실패 문구에 「다시 『이 Mac 연결』을 누르세요 — 지금 이 Mac 의 수집이 멈췄습니다」를 넣는다 |
| W-4 | `consent.ts` `beginConsent` | 서버가 준 URL 을 검사 없이 연다(서버는 신뢰하지만 이동 대상이 고정돼 있다) | `accounts.google.com`·`slack.com` 만 허용하는 한 줄(심층 방어) |
| W-5 | `F/lib/shell.ts` `openExternal` 의 `console.warn(… url=${url})` | 기존 코드다. 메시지함 링크가 이 길을 타면서 **메일·슬랙 링크 주소(추적 토큰이 실릴 수 있음)** 가 콘솔에 남는다 | url 대신 host 만 남긴다 |
| W-6 | `MailFrame.tsx` `prepare` | `auxclick`(가운데 클릭)은 가로채지 않는다. 웹은 새 탭이 정상으로 열리지만, 데스크톱에서는 아무 일도 안 한다 | `auxclick` 도 같은 처리 |
| W-7 | 시험 빈칸 | ① F-1(javascript: 링크) ② `connect=error` 착지 ③ 메일 iframe 링크 가로채기 | 각 한 줄 |

## 참고 — 다른 팀 요청(fe-report gap) 확인

- 슬랙 사용자 이름표(`users`)·퍼머링크·워크스페이스 domain·직책/직무가 응답에 없어 프론트가 「—」·id·단추 숨김으로 대처했다 — **그 대처는 지어내지 않는 쪽**이라 맞다. 백엔드 할 일로 넘길 목록(fe-report §다른 팀 영향 1~6)은 코디가 BE 수정 판에 붙일 것
- 이미지 첨부 썸네일은 화면에 서는 순간 중계를 부른다(메일·슬랙은 매번 상류에서 받음). 큰 사진이 많은 방은 느리다 — 동작 문제는 아니다. 실물 확인 때 볼 것

## 총평

**FAIL(1건)** — F-1 의 `openLink` 스킴 검사 한 줄(+ 그 시험)만 들어가면 PASS 로 볼 수 있다. W-1·W-2 도 한 줄짜리라 같이 고치기를 권한다. available-rooms 는 백엔드 F-2 가 닫혀야 실물로 붙는다. 재검수는 F-1·W-1·W-2·W-7① 만 본다.

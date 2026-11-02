# FE 재검수 — 커밋 `17ea307` (review-fe.md 의 F-1·W-1·W-2·W-7①) (2026-10-06)

## 판정: PASS

지시된 네 항목이 모두 본문과 시험에서 닫혔다. 지시 밖의 W-3·W-4·W-5·W-6 도 함께 고쳐졌다. 새 위반은 없다.

> 검수 방법: `git show 17ea307` 로만 읽었다(15 파일 +220/−26). 시험은 돌리지 않았다.

| # | 앞 판 지적 | 판정 | 근거(커밋 17ea307) |
|---|---|---|---|
| **F-1** | `openLink` 스킴 검사 없음 → `javascript:` 가 브라우저에서 우리 origin 으로 실행 | **해소** | `frontend/src/features/inbox/inboxModel.ts` `safeHref`(`new URL` 로 풀어 `http:`·`https:`·`mailto:` 만 · 상대 주소·`data:`·대소문자 섞인 `JavaScript:` 는 `null`) · `linkSeg` — 안전하지 않으면 **링크가 아니라 글자 조각**으로 떨어진다. 걸리는 자리: `parseInline`(mrkdwn `<target\|label>`) · `richSegs`(rich_text link url) · `slackUnfurls`(`title_link`·`original_url`·`from_url`) · `RoomView.tsx` 퍼머링크. **여는 자리 `inboxStream.ts` `openLink` 도 `safeHref` 를 한 번 더 거친다**(이중) · 메일 iframe 가로채기(`MailFrame.tsx` `intercept`)도 `openLink` 를 거친다 |
| **W-1** | 콜백 `connect=error` 미처리 | **해소** | `frontend/src/App.tsx` `readLanding` 이 `error` 를 받는다 · `features/settings/SettingsPage.tsx` 가 `role="alert"` 배너(「연결하지 못했습니다 — …」 · 닫기)를 세운다 · 쿼리는 지운다 |
| **W-2** | 첨부 `state` `"remote"` ↔ 실제 `"reference"` | **해소** | `frontend/src/lib/viewModels.ts` 타입이 `"reference"` · 시험 픽스처(`InboxPage.test.tsx:38-39`)도 `"reference"` · 커밋 트리에 `"remote"` 문자열 0(`git grep '"remote"' 17ea307 -- frontend/src`) |
| **W-7①** | `javascript:` 링크 시험 없음 | **해소** | `inboxModel.test.ts` 「링크 스킴 — http · https · mailto 만」(safeHref 7 경우 + `parseInline` + rich_text + 언퍼일) · `InboxPage.test.tsx` 「javascript: 링크는 링크로 서지 않고 눌러도 새 창이 열리지 않는다」(미끼 원문 → `closest("a")` 가 없음 · `window.open` 0회 · 안전한 퍼머링크는 `noopener,noreferrer` 로 열림) · `MailFrame.test.tsx`(iframe 안 `javascript:` 는 막기만) |

### 지시 밖에서 함께 닫힌 것(참고)

- **W-3** — 키체인 실패 문구가 「지금 이 Mac 의 수집이 멈췄습니다 — 다시 『이 Mac 연결』」(`labels.ts`)
- **W-4** — `consent.ts` 동의 URL 허용 목록(https 의 `accounts.google.com` · `slack.com`/하위). 밖이면 이동하지 않고 `failed`. 시험 `consent.test.ts`(`evil-slack.com`·`accounts.google.com.evil.example`·http 거절 포함)
- **W-5** — `shell.ts` `openExternal` 경고 로그가 주소 전체 대신 host 만
- **W-6** — `MailFrame.tsx` 가 `auxclick`(가운데 클릭)도 가로챔 · 같은 문서에 듣는 손 한 벌(`WeakSet`) · 시험 `MailFrame.test.tsx`
- W-7②(connect=error 착지)·③(iframe 링크 가로채기) 시험도 들어왔다(`SettingsLanding.test.tsx` · `MailFrame.test.tsx`)

### 경미 — 참고만(판정 무관)

- `safeHref` 가 `tel:` 을 받지 않는다. 그래서 서버 소독이 남긴 메일 본문의 `tel:` 링크는 이제 눌러도 아무 일도 안 한다. 의도라면 그대로 두고, 아니면 `SAFE_SCHEMES` 에 `tel:` 을 더한다(안전한 스킴)
- 안전하지 않은 링크에 라벨이 없으면 원래 주소 문자열이 **글자로** 보인다(`linkSeg` 의 `label || href`). 실행되지 않으니 무해하다

## 총평

**PASS** — FE-a·b 는 검수 기준을 통과했다. 실물로 붙는 데 남은 의존은 백엔드 `available-rooms`(BE-2·3 검수 F-2)다.

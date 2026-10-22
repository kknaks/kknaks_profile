# WP1-FE 기준선 — 고치기 전 (2026-10-08)

- 워크트리 `strong-hajin-notify`. frontend 는 `d2a06fa` 그대로이고, backend WP1-BE 변경만 워크트리에 있다
- `node_modules` 가 없어 `npm ci` 를 했다(341 packages · `.gitignore` 대상)

| 명령 | 결과 |
|---|---|
| `cd frontend && npx vitest run src/features/inbox/InboxPage.test.tsx src/features/settings/SettingsPage.test.tsx src/SettingsLanding.test.tsx src/App.test.tsx --no-file-parallelism` | **4 files · 74 passed · 0 failed**(App 34 · InboxPage 25 · SettingsPage 13 · SettingsLanding 2) · 12.3s |
| `cd frontend && npx tsc --noEmit` | **0 오류**(exit 0) |

**기존 실패: 0**

## Code Surface WP1 화면 줄 — 다시 셈(`rg` · `frontend/src`)

| 패턴 | 표 | 다시 셈(prod / test) |
|---|---|---|
| `useInboxStream\(` | 3 / 3 | 3/3 · 0 |
| `new WebSocket` | 2 / 2 | 2/2 · 0 |
| `inboxStreamUrl` | 3 / 2 | 3/2 · 0 |
| `createInboxEventHub\|hub\.subscribe\|hub\.emit` | 8 / 4 · test 2 / 1 | 8/4 · 2/1 |
| `InboxStreamEvent` | 9 / 3 | 9/3 · 0 |
| 메시지함 사건 이름 넷 | 14 / 6 · test 13 / 2 | 14/6 · 13/2 |
| `stubGlobal\("WebSocket"` | test 9 | 0 · 9/5 |
| `onReconnect` | — | 20/5 — 사건 채널과 관계있는 것은 `inboxStream.ts:12,16,19,20` · `InboxPage.tsx:157` · `SettingsPage.tsx:186` 여섯 줄이다. 나머지는 「연동 다시 연결」 단추 prop(`settingsParts.tsx` · `IntegrationSections.tsx` · `SettingsPage.tsx:302,324` · `InboxPage.tsx:54,75,293`)으로 이름만 같다 |
| `onSessionLost` | — | 8/3 · 10/6 — 회의 스트림 경로(건드리지 않음) |

표와 수가 모두 같다.

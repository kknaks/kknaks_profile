# WP3 검수 손질 결과 — FAIL 2 · WARN 2 · 코디 결정 둘

## 상태: done (커밋 없음)

- 정본: `review-wp2-wp3-report.md` §FAIL · §6 WARN · 코디 결정
- 손댄 파일: `frontend/src/lib/labels.ts` · `frontend/src/lib/notificationLabels.test.ts` · `frontend/src/App.tsx` · `frontend/src/App.test.tsx`. 셸(`src-tauri/`)과 `backend/` 는 손대지 않았다 — 그래서 cargo 는 돌리지 않았다

## 처분

| # | 지적 | 한 일 | 자리 |
|---|---|---|---|
| **F-2** | `meeting.changed` 의 `before`/`after` 가 서버는 객체인데 화면은 ISO 글자를 기대 | 새 `scheduleOf` 로 서버 모양 `{starts_at, ends_at, place}`(`_schedule_data`)를 읽는다<br>• **시간이 바뀌면** 「…회의 시간을 바꿨습니다」 + 「10월 8일(목) 11:00 → 15:00」(다른 날이면 날짜 둘)<br>• **시작은 같고 끝만** 바뀌면 「11:00–12:00 → 11:00–13:00」(시작만 보이면 「11:00 → 11:00」 이 돼서)<br>• **장소만** 바뀌면 「…회의 장소를 바꿨습니다」 + 「3층 회의실 → 5층 라운지」<br>• **둘 다** 바뀌면 시간 문장 + 보조 줄 끝에 「· 5층 라운지」<br>• 모양을 모르면 「…회의 정보를 바꿨습니다」<br>**OS 알림 문장도 같은 함수**(`describeNotification`)라 함께 바뀐다 | `labels.ts:1997`(`scheduleOf`) · `:2179-2205`(갈래) |
| **F-3** | `App.test.tsx` 「대상마다 고른 상태로 연다」 가 처리 안 된 예외를 남겨 vitest exit 1 | 회의 상세 `GET /api/meetings/g1…` 에 목록 모양 대신 **404** 를 돌려준다. 상세 화면이 `record.meeting` 을 읽다 던지던 자리가 사라졌고, 화면은 오류 상태로 선다. 시험이 보는 것(「그 회의를 읽으러 갔다」 · 읽음 API)은 그대로 단언한다 | `App.test.tsx:2628-2630` |
| **W-1**(화면) | 합친 슬랙 줄 「외 N명」 이 `senders.length` 로 센다 | 서버 `sender_count` 가 있으면 그것을 쓴다 — `max(sender_count, senders.length)` − 보이는 둘. 없으면(옛 서버) 목록 길이 | `labels.ts:2141-2143` |
| **W-5** | `openFocus` 의 의존이 `[setSurface]` 인데 안에서 `changeSurface` 를 부른다 | 의존을 `[changeSurface, setSurface]` 로 고쳤다(useState setter 라 바뀌지 않지만 적는다) | `App.tsx:432` |
| **W-6**(코디 결정) | 머리 `titleEnd` 슬롯 | **받아들임 — 그대로 둔다** | `shell/AppShell.tsx` |
| 코디 결정 | 외부 발신자 이름에 「님」 을 붙이지 않는다 · 회원만 「이름님」 | **지금 구현 그대로다**(`labels.ts` `actorName` — 회원 `display_name` → 「이름님」, `external_name` → 받은 그대로). 시험으로 못박았다(메일 「서지안이 …」 · 카톡 「박지윤이 …」 · 영문 이름 「Ji Hoon이 …」) | `labels.ts:2020-2024` |

## 시험

| 명령 | 결과 |
|---|---|
| `cd frontend && npx vitest run src/App.test.tsx` | **exit 0** · 40 passed · Errors 0(F-3 의 관문) |
| `npx vitest run src/lib/notificationLabels.test.ts src/App.test.tsx src/features/notifications/NotificationsPage.test.tsx src/lib/osNotifier.test.ts src/shell/AppShell.test.tsx src/features/settings/SettingsPage.test.tsx src/features/settings/NotifySection.test.tsx src/SettingsLanding.test.tsx src/features/inbox/InboxPage.test.tsx src/lib/eventStream.test.ts src/lib/shell.test.ts --no-file-parallelism` | **exit 0** · 11 files · **189 passed** · 0 failed · Unhandled 0 |
| `npx tsc --noEmit` | **0 오류** |

- `notificationLabels.test.ts` 는 31 → **38**:
  - `meeting.changed` 대역을 서버 객체 모양으로 바꿨다(시간 · 다른 날 · 장소만 · 둘 다 · 끝만 · 모양 모름 — 1 → 6)
  - 슬랙 `sender_count` 우선 +1
  - 「님」 규칙 +1

## 미결

- SPEC-011 §4.2-1 `meeting.changed` `data` 에 「`before`/`after` = `{starts_at, ends_at, place}`」 한 줄을 넣는 것은 writer 몫이다(검수 F-2 비고)
- W-1 의 서버 쪽(정확한 `sender_count` 세기)은 backend 가 올리는 중이다. 화면은 그 값이 오면 그대로 쓴다

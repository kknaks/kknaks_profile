# 재검수 r2(좁게) — WP2-BE · WP3-FE

> reviewer(read-only) · 2026-10-08 · 앞 판 `review-wp2-wp3-report.md`(FAIL 3 · WARN 6) · 손질 보고 `be-wp2fix-report.md` · `fe-wp3fix-report.md` · SPEC-011 v0.2.4 · 코디 결정 셋(W-6 titleEnd 받아들임 · 외부 발신자 「님」 없음 · E2E W17/W24/W30 문구)
> 약어: `B/` = `backend/src/ax_workspace/` · `F/` = `frontend/src/`

## 0. 판정 — **PASS** (FAIL 0 · WARN 0 · 참고 2)

F-1 · F-2 · F-3 · W-1 ~ W-5 가 **코드로** 닫혔다. 서버↔화면 이음매 셋(`new_assignee_name` · `meeting.changed` 객체 · `sender_count`)을 양쪽 코드와 SPEC v0.2.4 로 대조했고, 세 곳이 같은 이름 · 같은 모양이다. `App.test.tsx` 는 exit 0 이다. 코드 레포 문서 둘도 코드와 맞는다.

### 실행한 것(관련만)
- `make test-contract-serial FILES="tests/unit/test_notification_rules.py tests/contract/test_notification_rows.py tests/contract/test_notifications.py tests/contract/test_external_inbox.py tests/architecture/test_architecture.py tests/architecture/test_operation_inventory.py"` → **115 passed**(`test_architecture` 를 넣어 문서 문장을 읽는 시험 `:59-61` 도 확인)
- `npx vitest run src/App.test.tsx` → **exit 0 · 40 passed · Errors 0**
- `npx vitest run src/lib/notificationLabels.test.ts src/features/notifications/NotificationsPage.test.tsx src/lib/osNotifier.test.ts src/features/inbox/InboxPage.test.tsx --no-file-parallelism` → **exit 0 · 84 passed**
- `npx tsc --noEmit` → 0

## 1. 서버 ↔ 화면 이음매

| 이음매 | 서버 | 화면 | SPEC v0.2.4 | 결과 |
|---|---|---|---|---|
| **F-1** W14 새 담당 이름 | 사건 자리는 `new_assignee_id` 를 넘기고, 저장소 `_named`(`B/platform/notifications.py:164-170`)가 **만들 때의 `display_name`** 을 `new_assignee_name` 으로 붙여 저장한다(`write` `:126`). 시험 `test_w13_w14_w15_…` 이 이름 단언 | `d.new_assignee_name`(`labels.ts` `work.assigned` displaced) | §4.2-1 `work.assigned` `new_assignee_name?` | **닫힘** |
| **F-2** `meeting.changed` | `before`/`after` = `_schedule_data` 객체 `{starts_at, ends_at, place}`(그대로) | 새 `scheduleOf`(`labels.ts:1997-2006`)로 객체를 읽는다(`:2179-2205`)<br>• 시간 → 「회의 시간을 바꿨습니다」 + 「HH:MM → HH:MM」(끝만이면 범위 · 다른 날이면 날짜 둘)<br>• 장소만 → 「회의 장소를 바꿨습니다」<br>• 둘 다 → 시간 문장 + 「· 새 장소」<br>• 모양 모름 → 「정보를 바꿨습니다」<br>시험 대역이 서버 모양으로 바뀌어 6경우 | §4.2-1 `before`/`after` = 객체(ISO 글자 아님) | **닫힘** — 양쪽 시험이 같은 모양을 쓴다 |
| **W-1** `sender_count` | 첫 줄 `sender_count`(이름 있으면 1 · `notification_events.py:342`) · 합칠 때 자른 목록(5)에 없는 이름이면 +1(`platform/notifications.py:143-151`) — 근사(잘려 나간 이름이 다시 오면 한 번 더 셈 · 앞 검수가 허용) · 시험 7명 · 8건 → `senders` 5 · `sender_count` 7 · `count` 8 | `max(sender_count, senders.length)` − 보이는 둘(`labels.ts:2141-2143`) · 옛 서버면 목록 길이 | §4.2-1 `sender_count?` | **닫힘** |

## 2. 나머지 손질 — 코드로

| # | 확인 | 판정 |
|---|---|---|
| **F-3** | `App.test.tsx:2628-2630` 이 회의 상세에 404 를 돌려준다. 상세는 오류 상태로 서고 처리 안 된 예외가 사라졌다. 단언(그 회의를 읽으러 감 · 읽음 API)은 그대로 · exit 0 | 닫힘 |
| **W-2** | 재개(`B/modules/work/application.py:2240-2247`) — 행위자가 담당이면 W30 → `_requester_people`(요청자 · 승격자), 아니면 W29 → **담당 하나**. 새 시험 `test_w29_reopening_by_the_requester_does_not_reach_the_meeting_promoter` | 닫힘 |
| **W-3** | `my_badges` 가 `SqlAlchemyInboxStore.has_unread`(`external_channels_inbox_store.py:164-188`) 하나만 부른다 — `EXISTS` 둘(활성 연동의 안 읽은 메일 · 지우지 않은 방의 본문 줄 중 읽음 지점 뒤) · 둘 다 `_not_mine()`. 레일 셈(`list_messages` — `active_integrations` = `removed_at IS NULL` · `room_cards` = 지우지 않은 방 · 읽음 지점 뒤 · `_top_level` · `_not_mine`)과 **같은 규칙**이다. 새 시험이 내 줄만 → False · 받은 메일 → True · 읽음 → False · 채널 줄 → True · 방 읽음 → False | 닫힘 |
| **W-4** | `test_w11_reference_read_evidence_and_list_cleanup_make_nothing` — 참고 읽음 · 자료 채택 · 목록 정리 각각 `_none` | 닫힘 |
| **W-5** | `openFocus` 의존 `[changeSurface, setSurface]`(`App.tsx:432`) | 닫힘 |
| 코디 결정 「님」 | 회원 `display_name` → 「이름님」 · `external_name` → 받은 그대로(`labels.ts:2020-2024`) · 시험이 메일 · 카톡 · 영문 이름 셋을 고정 | 결정대로 |
| 코디 결정 W-6 | `AppShell` `titleEnd` 그대로 | 결정대로 |

## 3. 코드 레포 문서 — 코드와 맞나

| 문서 | 바뀐 문장 | 코드 대조 |
|---|---|---|
| `docs/domain-model.md` 대조표 `notifications` | 사건 자리 → 생성기 · 같은 트랜잭션 · 원천 멱등 · 칸 목록(`kind` 19 · `theme` · `item` · `relation` · `failure` · `actor` · `resource_*` · `data` · `target` · `coalesce_key` · `seq` · `updated_at` · `read_at`) · `actor_member_id` 옛 칸 = 받는 사람 · 지우는 규칙 없음 | `persistence.py` 모델 · `platform/notifications.py` `write` 와 같다 |
| 같은 문서 `notification_settings` | 회원마다 한 벌 · `version` → 409 · 없으면 기본(업무 댓글만 끔) · 캐시 없음 | `NotificationSettingsRecord` · `save_settings` · `DEFAULT_OFF` 와 같다 |
| 같은 문서 `external_messages.from_me` | 저장 때 판정 셋 · `null` = 아님 · 안 읽음 · 원칙 ① · 백필 파일 | `mail_from_me` · `slack_from_me` · 카톡 업로드 · `_not_mine` 과 같다 |
| 같은 문서 「알림 — 아직 구현하지 않음」 머리 주석 | 구현됐고 모양이 다르다(파생 projection 이 아니라 사건 자리 → 생성기 저장 투영 · 대상자는 SPEC-011 §4.2) | 맞다 |
| `docs/unified-operations.md:57` | `list_notifications` — 저장한 값 · `target` 만 인가 · 19 종류 | `notification_item(target_open=…)` 와 같다 |
| `:85` · `:113` | 화면 조작 경로는 알림을 따로 만들지 않음(사람 알림은 SPEC-011) · 진행 상태엔 알림 없음, 회의록 완료 · 실패만 M09~M11 | `commit_finalized` · `fail_finalize` 만 생성기를 부른다 — 맞다 |

## 4. 참고 (판정 밖)

- **R-1** `sender_count` 는 근사다 — 잘려 나간(6번째 이후) 사람이 다시 쓰면 한 번 더 센다. 정확히 하려면 이름 집합(또는 해시)을 따로 두면 된다. 앞 검수가 허용한 범위라 그대로 둔다
- **R-2** `scheduleOf` 는 서버 객체만 읽는다 — 옛 ISO 글자 모양(이번 판 전에 운영에 선 M04 줄)은 없다(알림이 이번 판에 처음 서므로 옛 행이 없다). 해당 없음

## 5. 목록
- FAIL: 없음
- WARN: 없음
- 사용자에게 물을 것: 없음

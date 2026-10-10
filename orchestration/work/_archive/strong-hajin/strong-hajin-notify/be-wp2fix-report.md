# WP2 검수 손질 — 결과 (FAIL 1 · WARN 4 · 코드 레포 문서)

- 출처: `review-wp2-wp3-report.md` §FAIL · §6
- 경로 약어: `B/` = `backend/src/ax_workspace/` · `BT/` = `backend/tests/`
- 커밋 없음

| # | 무엇 | 한 것 (파일:줄) | 시험 |
|---|---|---|---|
| **F-1** | W14 새 담당 **이름** | 사건 자리(`B/modules/work/assignments.py:253`)는 `new_assignee_id` 를 넘긴다. 저장소가 행을 쓸 때 **만들 때의 이름** `new_assignee_name`(`display_name`)을 붙인다 — `B/platform/notifications.py` `_named`(`write` 의 `data=`). 화면 키 이름 그대로 | `test_w13_w14_w15_…` 단언에 `"new_assignee_name": "지호 (팀장)"` |
| **W-1** | 합친 슬랙 줄 보낸 사람 수 | 첫 줄이 `sender_count` 를 싣는다(`B/modules/notification_events.py` `message_notification` — 이름이 있으면 1)<br>합칠 때 자른 목록(5명)에 없는 새 이름이면 +1(`platform/notifications.py` `_merge`)<br>근사다 — 잘려 나간 이름이 다시 오면 한 번 더 셀 수 있다(검수가 허용한 범위) | `test_x06_…` — 7명 · 8건 → `senders` 5 · `sender_count` 7 · `count` 8 |
| **W-2** | W29 은 담당만 · W30 일 때만 요청자 · 승격자 | `B/modules/work/application.py`(reopen 의 W29/W30 자리) — 행위자가 담당이면 W30 → `_requester_people`, 아니면 W29 → 담당 하나 | 새 `test_w29_reopening_by_the_requester_does_not_reach_the_meeting_promoter`(승격자 칸을 세운 요청에서 승격자 0 줄) |
| **W-3** | `/api/me/badges` 메시지함 점 = `EXISTS` 하나 | `B/platform/external_channels_inbox_store.py` `has_unread(member_id)` — 내 활성 연동의 메일 중 읽음 표지 없는 것 **또는** 내 방의 본문 줄 중 방 읽음 지점 뒤의 것. 둘 다 `_not_mine()`<br>`B/bootstrap/application.py` `my_badges` 가 이것만 부른다(`list_messages` 전체 셈을 걷었다) | 새 `test_the_inbox_badge_is_one_exists_with_the_rail_rules` — 내 줄만 → False · 받은 메일 → True · 읽음 → False · 채널 줄 → True(레일 > 0) · 방 읽음 → False(레일 0) |
| **W-4** | W11 자료 채택 · 목록 정리 | `test_w11_reference_read_evidence_and_list_cleanup_make_nothing` — 참고 읽음 · `POST …/evidence`(채택) · 거절 뒤 `DELETE …/list-entry`(정리) 각각 `_none` | 같은 시험 |
| **문서** | `docs/domain-model.md` · `docs/unified-operations.md:57,85,113` | **domain-model** 대조표에 `notifications`(칸 · 생성기 · 멱등 · `actor_member_id` 옛 칸 처리) · `notification_settings` 두 줄을 넣었다. 외부 채널 절에 `external_messages.from_me` 한 줄. 「완료·검수·알림 — 아직 구현하지 않음」 머리에 **구현됐고 모양이 다르다**(사건 자리 → 생성기 저장 투영 · 대상자는 사건 × 관계 표)는 주석<br>**unified-operations** — :57 `list_notifications`(저장한 값 · target 인가 · 19 종류) · :85 「이 화면 조작 경로는 따로 만들지 않는다 — 사람 알림은 SPEC-011」 · :113 「이 진행 상태에는 알림을 더하지 않는다 — 회의록 완료 · 실패만 M09~M11」 | `BT/architecture/test_architecture.py:59-61` 이 읽는 문장은 건드리지 않았다(그 시험은 시험 줄 밖이라 돌리지 않음) |

## 검증 — 관련만 (Makefile 타겟)

| 명령 | 결과 |
|---|---|
| `make test-contract-serial FILES="tests/unit/test_notification_rules.py tests/contract/test_notification_rows.py tests/contract/test_notifications.py tests/contract/test_external_inbox.py tests/contract/test_events_stream.py tests/contract/test_task_successors.py"` | **136 passed** · 0 failed |

- 첫 실행에서 새 badges 시험이 한 번 실패했다. 원인은 **시험이 메일을 `from_me=None` 으로 고른 것**이다(받은 메일은 저장 때 `False` 로 판정된다). 시험을 고쳐 통과했고, 제품 코드는 그대로다
- PG 시험은 이번 손질과 무관해 돌리지 않았다(SQL · NOTIFY 경로 무변경)

## 미결
- 없음(W-1 의 「외 N명」 화면 쪽은 frontend 몫 — 서버는 `sender_count` 를 싣는다)

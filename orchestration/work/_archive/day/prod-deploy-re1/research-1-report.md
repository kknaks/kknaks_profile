# research-1 — 웹 피드백 W3 · W4 · W5 원인 · 판정 조사 (read-only)

- 조사일: 2026-11-11 · researcher 워커 (task_26594b683aa5)
- 코드 기준: `CENTURION_DAY/prod-deploy-re1` HEAD `5f7806d3` (아래 파일은 frontend 워커의 작업트리 수정 대상 밖이다 — `board_parts.html` · `board_rules.py` · `board.py` · `writes.py` · `outbox.py` · `sync.py` 는 수정 안 됨)
- 스펙 기준: `mediness-mediness/prod-deploy-re1-spec` HEAD `84561044` · `products/day/20-spec/spec-002-procedure-board.md`
- dev 실물: `ssh day-vm` docker logs(api · worker) · dev DB(`day` DB · 스키마 `day_dev`) — **읽기 전용 세션**(`default_transaction_read_only=on`)으로만 조회 · 조회 뒤 터널 닫음
- 값(고객 · 키 · 토큰 · id 값)은 옮기지 않았다. 시각 · 단계 · 상태 · 건수만.
- **결정하지 않았다** — 각 절 끝 「고칠 방향 후보」 · 「정할 것」.

---

## W3. 방 옮기기 목록 — 「비어 있음」 / 「이미 다른 사람이 배정됨」

### Q1. 지금 팝오버 목록은 어디서 · 무엇으로 만드나

| 단계 | 근거 | 내용 |
|---|---|---|
| 방 원천 | `backend/day/queries/board.py:321-328` | `room` 테이블 — 세션 병원 · `deleted_at IS NULL` 전부. 정렬 `Room.sort_order, Room.title, Room.id` |
| 스냅샷 | `backend/day/services/board_rules.py:1013-1014` | `"rooms": [{"id", "title"}]` — 방 id · 이름만. **상태 칸 없음** |
| 화면 | `backend/day/templates/partials/board_parts.html:301-325` (`room_pop`) | `snapshot.rooms` 를 돌며 카드 지금 방(`card.room.id`)만 빼고 `<label class="day-opt">` + 이름(`day-opt__name`)만 그림. 상태 글자 칸(`day-opt__status`) 없음 |
| 스펙 | SPEC-002 :162 · U-15 :332 | 「**방 이름만** · 그 병원 방 전부 · 카드 지금 방 뺌 · `room.order` 순 · 침대 수 · 「(n/m)」 없음 · 점유 중인 방도 고를 수 있다」 — 지금 구현은 스펙 그대로다. W3 는 **스펙 변경**이다 |

dev 데모 지점 방 수: 41개(`room` · `deleted_at IS NULL`) — 그림의 긴 목록과 맞다.

### Q2. 「다른 사람이 배정된 방」 후보 — 지금 데이터로 얻어지나 · 판 기준과 어긋나는 곳

판 화면 기준(U-1): 카드 = 오늘 방문 중 `flow_step ∈ {procedure_waiting, procedure}` 이고 `visit.room_id` 가 있는 것(`board_rules.py:22` `BOARD_STEPS` · `:70-71` `is_card`).

| # | 후보 | 지금 얻어지나 | 근거 | 판 기준과 어긋나는 경우 |
|---|---|---|---|---|
| A | **판 카드의 방**(`visit.room_id` of `cards()`) | 예 — 이미 메모리에 있음(`BoardRules.cards()` · 스냅샷 `cards[].room`) | `board_rules.py:67-71` | 판과 **정확히 같다**. 다만 아래 B · D · E 를 못 본다 |
| B | **살아 있는 「방 배정」 작업의 방**(점유 띠의 「이전 방」 = `hold_room`) | 예 — `room_assigns(v)` · `hold_room(v)` | `board_rules.py:554-575` | 점유 이동한 카드는 새 방(F)에 카드가 있고 이전 방(A)은 「방 배정」만 남는다. A 방만 보면 카드가 없어 「비어 있음」이 된다. 판에선 A 가 점유 띠 글자로 보인다 |
| C | 진행중(`started_at` 있음) 시술 작업의 방(`visit_task.room_id`) | 예 — `w.tasks` | `board_rules.py:109-117` `task_state` | 작업은 방 이동 때 카드와 같이 움직이므로(규칙 28) A 와 거의 같다. 다를 수 있는 경우 = KOS 웹에서 작업만 다른 방으로 옮겼을 때(카드 방 = 「방 배정」 뺀 가장 늦게 배정된 작업 방 · `emr/sync.py:1330-1356` `card_room_of`). 별도 신호로서 얻는 것 적음 |
| D | **판에 없는 단계의 오늘 방문 방**(상담 · 접수 단계인데 방이 있음) | 예 — `load_world` 가 오늘 방문 전부를 읽는다(`queries/board.py:98-110` — 단계로 거르지 않음). `is_card` 로만 판에서 뺀다 | dev DB 오늘(KST): `reception` 1건이 방 있음 · `procedure_waiting` 1건 · `reserved` 1건(방 없음) | 판에 카드는 없지만 그 방에 사람이 있다. A 만 쓰면 「비어 있음」 |
| E | **귀가 대기(`procedure_done`) 방문의 방** | 예 — DAY 는 귀가 대기 때 `room_id` 를 비우지 않는다(규칙 17 · SPEC :821) | `board_rules.py:80-81` `is_home` · `ordered_cards` `:536` 이 귀가 대기를 따로 다룸 | 판에서 빠졌지만 고객이 아직 방에 있을 수 있다(「귀가 대기」 = 실제 귀가 전 · OQ-22). 귀가(`completed`)는 오늘 방문이라도 방에 없다고 볼지 확인 안 됨 |
| F | 같은 고객의 다른 카드(같은 날 방문 2건) | 예 — 방문 단위라 A 에 그대로 들어감 | U-1 「카드 1장 = 방문 1건」 | 방 옮기는 카드 **자기 자신**의 방은 이미 목록에서 빠진다(`board_parts.html` `r.id != here`). 같은 고객의 다른 방문 카드가 있는 방을 「다른 사람」으로 볼지 — 판정 기준 필요. 데모에 그런 데이터가 있는지 확인 안 됨 |
| G | 반영 대기(옮기는 중) 값 | 예 — DAY 는 방 이동 때 `visit.room_id` 를 바로 바꾼다(반영 중 값 · `services/board.py:1360-1368`) · 조회가 덮지 않음(`emr/sync.py:914-917` `hold_room`) | — | 화면 기준과 같다(판도 DAY 값을 그림) |
| H | KOS `occupiedResources`(`visit_occupied_resource`) | **아니오** — 방이 아니라 예약 그룹 · 구역 · 시간 | `models/room.py:81-92` | 방 판정에 못 씀 |

정리: 판 화면과 같은 기준 = **A**. 「사람이 있는 방」에 가까운 기준 = A ∪ B ∪ D ∪ E(어디까지 넣을지 = 정할 것). 침대 수(capacity)로 「가득 참」을 셈하는 것은 스펙이 뺐다(U-15 「침대 수 · 「(n/m)」 없음」).

### Q3. 원장 목록 「비어 있음」(규칙 19 · :823) 구현 — 재사용할 수 있나

| 층 | 근거 | 재사용 |
|---|---|---|
| 상태 계산 | `board_rules.py:154-168` `doctor_status` — 판 카드(`self.cards()`)의 시술을 돌며 doing / waiting_start / free | **방식(카드를 돌며 상태 정하기)만** 재사용 가능 — 방 판정은 새 함수(예: 방마다 카드 방 · 점유 방 집계) 필요 |
| 정렬 | `board_rules.py:32` `DOCTOR_RANK` · `:170-177` `doctors()` — `(rank, name)` 로 정렬 · free 먼저 | 같은 모양으로 「비어 있음 먼저 → 배정됨」 가능. 단 지금 방 목록은 `room.order` 순(스펙) — 두 정렬의 우선순위가 정할 것 |
| 스냅샷 | `board_rules.py:1010` `"doctors"` 에 `status` · `room` 칸 | `rooms[]` 에 `status` 칸을 더하는 같은 방식 |
| 글자 | `board_parts.html:33-36` `doctor_label` 매크로(free → 「비어 있음」) | 같은 매크로 방식 가능. 「점유 중」 · 「이미 다른 사람이 배정됨」 글자는 사용자 말 두 개가 다르다(아래 정할 것) |
| 마크업 | `ui.html:432` `<span class="day-opt__status{{ ' is-free' if d.free }}">` | 방 목록도 같은 `day-opt` 행이라(`board_parts.html:311`) 같은 `day-opt__status` · `is-free` 를 붙일 수 있다 |

**스크롤 · 묶음**: 사용자 보충 「비어 있는 방이 먼저 나오고 스크롤 내리면 이미 다른 사람이 배정됨」 — 원장 목록은 묶음 머리 없이 한 줄씩 정렬만 한다(`ui.html:425-433` — 「전체」 라벨 하나). 방 목록에 묶음 머리를 둘지는 정할 것.

### W3 — 고칠 방향 후보

1. 서버 `rooms[]` 에 상태(`free` / `taken`) 칸 추가 — 판정은 Q2 의 A(판 카드 방) 기본 + B(점유 방) 포함 여부 선택. 정렬 = 상태 → `room.order`.
2. 템플릿 `room_pop` 에 `day-opt__status` 칸 — 원장 목록과 같은 마크업 · 클래스.
3. 판정을 카드 방(A)으로만 하면 서버 계산 없이 템플릿에서도 가능(`snapshot.cards[].room.id` 집합) — 다만 B · D · E 는 스냅샷에 없어 못 본다.

### W3 — 정할 것

- W3-a 글자: 「점유 중」(사용자 첫 말) vs 「이미 다른 사람이 배정됨」(보충) — 하나로? 「점유 중」은 이미 U-15 에서 **점유 이동의 이전 방**(B)이라는 다른 뜻으로 쓰인다(겹침 주의).
- W3-b 「배정됨」 판정 범위: A(판 카드)만 / +B(점유 이동으로 남은 방) / +D(접수 · 상담 단계인데 방 있음) / +E(귀가 대기).
- W3-c 같은 고객의 다른 방문 카드가 있는 방도 「다른 사람이 배정됨」인가(F).
- W3-d 정렬: 상태 먼저 → 그 안 `room.order`(사용자 보충대로라면) — 스펙 「`room.order` 순」 바꿈. 묶음 머리 줄 둘지.
- W3-e 「배정됨」 방도 고를 수 있는 것은 그대로인지(U-15 「점유 중인 방도 고를 수 있다」 · 「막지 않는다」 — 스펙 :339).

---

## W4. 「방 배정」 없는 카드에서 [점유 이동]이 오래 걸림

### Q4. 그 경로의 KOS 쓰기 순서 · 각 단계가 기다리는 것

| 단계 | 무엇 | 기다리는 것 | 근거 |
|---|---|---|---|
| 0 | 클릭 → `room_move(mode=hold)` · 남길 「방 배정」 없음 → `add_room_assign` intent 하나만 쌓음 · DAY 작업 방 · 카드 방은 바로 새 방 | — | `services/board.py:1328-1398` · `:1401-1437` |
| 1 | 조작 commit 뒤 발송 태스크 바로 발행(kick) → `add-flow-tasks` 전송 | Redis kick · worker | `services/outbox_kick.py:31-58` · `services/board.py` `_finish` (:328 `send_now`) |
| 2 | **다음 일정 조회(10초 주기)** 가 새 「방 배정」 sequence 를 찾아 add op `confirmed` | **조회 주기 최대 10초** — KOS 응답 `{}` 라 sequence 를 조회로만 안다(SPEC :766) | `tasks/emr.py:3` · `common/config.py:114` `sync_schedule_interval_seconds=10` · `emr/outbox.py:618-634` `added_room_assign` · `:713-720` |
| 3 | 같은 조회 transaction 안에서 `follow_room_assign` 이 `change-tasks-room` 2건(① 새 「방 배정」 → 원래 방 ② 나머지 → 새 방)을 **쌓기만 함** | **kick 없음** → 다음 발송 주기(10초)까지 대기 | `services/emr_sync.py:195-198` · `services/board.py:1509-1562`(enqueue 만 · `send_now` 호출 없음) · `tasks/emr.py:7` `OUTBOX_SEND_INTERVAL_SECONDS` 10 |
| 4 | 발송 주기에 2건 연달아 전송(앞이 2xx 면 확인 안 기다리고 다음) | — | `emr/outbox.py:496-504` |
| 5 | 확인 = 다음 일정 조회 | 발송 주기와 조회 주기가 **같은 초에 함께 돈다** → 같은 회차 조회는 전송 전 값을 읽어 못 맞춤 → **한 회차(10초) 더** | 아래 로그 08:59:47 |

재시도 · 지연 상수: `MISS_LIMIT`(조회 2번 안 맞으면 재전송) · `MAX_ATTEMPTS` 3 · `OUTBOX_SENT_STALE_SECONDS` — 이번 실측 건들은 모두 `attempts 0 · checks 0` 으로 확인돼 재시도는 원인이 아니다.

### Q5. dev 실물 — 단계별 시간

dev DB `event_log`(`visit.room_move` · `visit.room_return`) ↔ `external_outbox`(같은 `event_id`) · 시각 = `created_at` / `updated_at`(확인 시각). 오늘 방 이동 15건 · 전부 같은 데모 방문 1건.

**「방 배정」 없음(add 경로) 4건 — 클릭 → 마지막 확인**

| 클릭(UTC) | add 확인 | 뒤 2건 쌓임 | 뒤 2건 확인 | 총 |
|---|---|---|---|---|
| 01:17:03.265 | +9.8초 | +9.8초 | +19.8초 | **19.8초** |
| 01:17:21.479 | +1.6초 | +1.6초 | +21.6초 | **21.6초** |
| 01:21:36.728 | +6.4초 | +6.4초 | +26.4초 | **26.4초** |
| 08:59:30.034 | +7.2초 | +7.2초 | +27.1초 | **27.1초** |

**비교 — 「방 배정」 있음(점유 이동 · 이동) · 복귀**: 확인까지 1.1 ~ 9.9초(`change-tasks-room` 1건 또는 `cancel` + `room` 2건 · 한 조회 주기 안).

**최근 1건(08:59:30) worker 로그 타임라인**

| 시각(UTC) | 일 |
|---|---|
| 08:59:30.034 | 클릭 · add op 쌓임(api 응답 08:59:30.172 · 200) |
| 08:59:30.117 → 30.829 | kick 받은 발송 태스크 · `sent: 1`(KOS `add-flow-tasks` 약 0.7초) |
| 08:59:37.0 → 37.4 | 일정 조회 — add 확인(37.260) · `change-tasks-room` 2건 쌓임(37.265) · **발송은 이 회차 37.040 에 이미 끝남(빈 큐)** |
| 08:59:47.0 → 47.205 | 일정 조회(전송 전 값 — 못 맞춤) |
| 08:59:47.0 → 47.330 | 발송 주기 · `sent: 2` |
| 08:59:57.0 → 57.216 | 일정 조회 — 2건 확인(57.095) |

**원인(사실)**: add 경로는 「조회로 sequence 확인」 1회 + 「쌓은 뒤 kick 없음」 1회 + 「발송 · 조회 같은 초 경쟁」 1회 = **조회 · 발송 주기 2 ~ 3번**을 직렬로 탄다. KOS 호출 자체는 짧다(add 약 0.7초). 「방 배정」 있음 경로는 kick 으로 바로 보내 한 주기 안에 끝난다.

화면에서 보이는 것(코드 기준 · 화면 실측은 안 함): 클릭 즉시 카드는 새 방(DAY 값). add 확인 전까지 `room_assign_creating` 으로 방 이동이 막히고(`board_rules.py:596` · `queries/board.py:253-275`) 점유 띠는 아직 없다(살아 있는 「방 배정」의 방이 정해지기 전). 띠는 add 확인 회차(위 +1.6 ~ +9.8초)에 DAY 가 새 「방 배정」 방을 원래 방으로 두면서 나타난다(`services/board.py:1540-1549`). KOS 웹에서 작업이 새 방으로 보이는 것은 마지막 확인 무렵(+20 ~ 27초). 사용자가 「오래 걸린다」고 본 곳이 DAY 띠인지 KOS 웹인지는 **확인 안 됨**.

### W4 — 고칠 방향 후보

1. `follow_room_assign` 으로 쌓은 뒤 발송 kick(`outbox_kick.send_now`) — 「쌓임 → 전송」 최대 10초 줄임(worker 안에서 kick 가능한지 · 아키텍처 규칙 `tests/architecture` 확인 필요).
2. 또는 확인 회차 안에서 바로 전송(같은 worker 태스크).
3. add 전송 직후 그 병원 일정 조회를 한 번 당겨 발행 — 「add → 확인」 대기 줄임.
4. 발송 · 조회 주기를 같은 초에 돌지 않게(오프셋) — 「같은 회차 경쟁」 10초 줄임.
5. 화면: 「만드는 중」 동안 띠 · 상태를 먼저 보이기(체감만 — 스펙 변경).

### W4 — 정할 것

- W4-a 목표 시간(예: 「방 배정」 있음 경로와 같은 한 주기 안)인지, 화면 체감만 맞추면 되는지.
- W4-b 사용자가 기다린 곳 = DAY 점유 띠가 뜨는 때인가 / KOS 웹 반영인가(재현 한 번으로 확인 필요).

---

## W5. [복귀하기] — 「방 배정」을 취소가 아니라 삭제

### Q6. HAR 의 삭제 요청 두 개 vs DAY 지금 복귀

`reference/2026-11-06-repo-structure/har/시술삭제.har`(데모 테넌트 · 2026-11-11 11:19 UTC).

| HAR # | 시각(UTC) | 요청 | 본문 키 · 값 | 응답 |
|---|---|---|---|---|
| #3 | 11:19:13.567 | `POST schedule/flow/v1/commands/change-tasks-complete` | `scheduleId` · `sequences`(1개) · **`complete: false`** | 200 · `{}` |
| #14 | 11:19:20.315 | `POST schedule/v1/commands/cancel-flow-tasks` | `scheduleId` · `sequences`(1개) · **`reason: "DELETE"`** | 200 · `{}` |

- 두 요청은 같은 일정 · 같은 sequence(스크립트로 비교 · 값 미출력).
- 사이 7초에는 `get-reservation-group` · `get-purchase-summaries` 조회뿐(사람이 확인 창을 누른 시간으로 보임 — 추정 아님 · 요청이 없다는 사실만).
- 지운 작업은 **시술 작업**(`kind = procedure` · `is_room_assign = false`)이고 지우기 전 **완료(DONE)** 상태였다(dev DB 사본 — `completed_at` 있음 · 마지막 status `ready` = `complete:false` 뒤 값). **「방 배정」(기타 작업 · 완료 아님)을 지울 때 KOS 웹이 `complete:false` 를 먼저 보내는지는 HAR 에 없다 — 확인 안 됨.**
- 이 HAR 의 일정 = DAY dev 에서 오늘 방 이동 · 복귀를 한 **같은 방문**(dev DB 대조).

**DAY 지금 복귀**(`services/board.py:1440-1506`): ① `cancel-flow-tasks {scheduleId, sequences(원래 방 「방 배정」), reason: "CANCEL"}` ② `change-tasks-room {나머지 전부 → 원래 방}`. `complete` 요청 없음.

| 차이 | HAR(삭제) | DAY(복귀) | 근거 |
|---|---|---|---|
| `reason` | `DELETE` | `CANCEL` | `emr/kos/writes.py:63` `CANCEL_REASON` · `:182-188` |
| 앞 요청 | `change-tasks-complete false` | 없음 | `services/board.py:1488-1505` |
| 보내기 문(gate) | — | `write_open` 이 `reason == "CANCEL"` 만 연다 → `DELETE` 는 지금 **막힘**(failed · not supported) | `emr/kos/writes.py:82-83` |
| 확인 조건 | — | `status = canceled` | `emr/kos/writes.py:187` · `emr/outbox.py:575` |

### Q7. 삭제한 행을 KOS 조회(DAY 가 쓰는 일정 조회)가 돌려주나

**돌려주지 않는다 — dev 실물 1건 확인.**

- HAR #14(11:19:20.315) 다음 DAY 일정 조회(`schedule/v2/queries/get-schedules-grouped-by-zone` · `emr/kos/__init__.py:49`) 로그: 11:19:17 회차 `visit_task 12 upserted · absent {}` → **11:19:27 회차 `visit_task 11 upserted · absent {visit_task: 1}`**(dev worker 로그).
- dev DB 사본: 그 sequence 의 `visit_task.deleted_at = 11:19:27.089` · status 는 마지막 값(`ready`) 그대로 · `canceled` 로 바뀐 적 없음.
- DAY 는 「응답에 없던 작업」만 `deleted_at` 을 채운다(응답엔 있었는데 필수 칸이 없어 뺀 작업은 제외) — `emr/sync.py:1546-1561` · `:238-261`. 그러므로 KOS 응답에서 **그 작업이 빠졌다**.
- 비교: 같은 방문의 「방 배정」 6행은 복귀 · 귀가 대기로 `CANCEL` 취소된 것 — DAY 사본에 `status = canceled` · `deleted_at` 없음 = **조회가 계속 돌려준다**(dev DB · 11:28:57 회차 갱신).
- 한계: 표본 1건이고 지운 것이 **시술 작업**이다. 「방 배정」(기타 작업)을 `DELETE` 했을 때도 빠지는지는 **확인 안 됨**(같을 가능성이 높지만 데모 실물 1회 필요 — 쓰기라 이 조사에서 안 함). HAR 안에는 일정 조회 응답이 없다(작업 목록이 든 응답 없음 · `get-reservation-group` 은 작업 없음).

### Q8. 규칙 33(취소된 「방 배정」 행으로 원래 방 판정)이 삭제로 바뀌면

규칙 33 구현: `board_rules.py:577-583` `home_room` — 「방 배정」 전부(취소 포함 · `live=False`) 중 `sort_order` 첫 행의 방 · 없으면 `visit.room_id`. 판 world 는 `deleted_at IS NULL` 작업만 읽는다(`queries/board.py:150`).

| 상황 | CANCEL(지금) | DELETE 로 바꾸면 | 깨지나 |
|---|---|---|---|
| 점유 이동 → **복귀** → 귀가 대기 | 취소된 「방 배정」 = 원래 방 | 「방 배정」 행이 사본에서 `deleted_at` → `home_room` 은 `visit.room_id` 로 떨어짐. 복귀 뒤엔 작업 전부가 원래 방이라 `visit.room_id` = 원래 방일 것 | **대개 안 깨짐**. 단 카드 방 = 「방 배정」 뺀 가장 늦게 배정된 작업 방(`sync.py:1330-1356`)이고, 복귀 `change-tasks-room` 뒤 `roomAssignedDateTimeUtc` 가 새로 찍히는지 미확인(SPEC OQ-38) — 안 찍히면 카드 방이 원래 방이 아닐 수 있다(확인 안 됨) |
| 점유 이동 → (복귀 없이) **귀가 대기** | 귀가 대기가 「방 배정」을 `CANCEL` → 원래 방(A) | 귀가 대기 경로를 같이 DELETE 로 바꾸면 → `visit.room_id` = 새 방(F)로 떨어짐 → 「시술 완료」 탭 묶음이 **A → F 로 바뀜** | **귀가 대기까지 바꾸면 깨짐**. 복귀만 바꾸면 이 경로는 그대로 |
| 「방 배정」이 여럿 쌓인 방문(dev 같은 방문에 취소된 「방 배정」 6행) | `sort_order` 첫 행(가장 처음) | 복귀로 지운 행이 빠짐 → 남은 행 중 첫 행 | 「원래 방」이 바뀔 수 있다(어느 행이 처음인지에 따라) |
| 점유 판정(`hold_room`) | 살아 있는 것만 봄 · 취소 행 무시 | 지운 행은 아예 없음 | 안 깨짐 |
| 복귀 확인 | `status = canceled` 로 확인 | 다음 조회에 그 sequence 가 없음 → `_task_met(task=None)` = False(`emr/outbox.py:569-571`) → 끝내 안 맞음 → 재전송 · `failed`(+ 뒤 op 막힘) | **깨짐** — 확인 조건을 「사라짐」으로 바꿔야 함 |
| 반영 중 DAY 값 | 「방 배정」 status 를 바로 `canceled`(`services/board.py:1456-1460`) | 확인 전까지 `canceled` 로 두고, 조회가 빼면 `deleted_at`(sync 가 처리) | 별 문제 없음(확인 조건만 위) |

**대신할 「원래 방」 기준 후보**
1. `event_log` `visit.room_move` payload `fromRoomId`(첫 점유 이동 · `services/board.py:1370-1381`) — DAY 에서 옮긴 것만 안다(KOS 웹에서 옮긴 것 못 봄).
2. `visit_task.started_room_id`(규칙 30 · 첫 [시작] 때 카드 방) — 시작 전 이동이면 비어 있음.
3. 지운 행도 사본에 남김(`deleted_at` 있는 「방 배정」 행까지 `home_room` 이 읽게) — 사본에 행은 남아 있다(dev 확인 · `deleted_at` 만 채움).
4. 처음 방(접수 때 방) = 첫 `visit.room_id` 이력 — 지금 따로 남기는 칸 확인 안 됨.
5. 「방 배정」 지움은 복귀만 · 귀가 대기는 `CANCEL` 유지 → 규칙 33 그대로 대부분 성립.

### Q9. 같은 코드 경로를 쓰는 다른 동작에 번질 위험

`cancel-flow-tasks` 를 만드는 곳은 `WriteIntent("cancel_room_tasks")` 하나뿐이고 쓰는 동작은 둘이다(`git grep cancel_room_tasks`):

| 동작 | 근거 | `CANCEL_REASON` 을 전역으로 바꾸면 |
|---|---|---|
| [복귀하기] | `services/board.py:1488-1492` | 의도한 변경 |
| [귀가 대기] — 안 끝난 「방 배정」 취소 | `services/board.py:967-984` | **같이 바뀐다** → 규칙 33(「시술 완료」 탭 원래 방) · 귀가 대기 확인(`status = canceled`) 이 함께 영향 |

번지지 않는 것(경로가 다름):
- 「시작 취소」 = `change-flow-step(PROCEDURE_WAITING)`(`writes.py:162-168`) — `cancel-flow-tasks` 안 씀.
- 「완료 취소」 = `change-tasks-complete false`(`writes.py:169-177`) — HAR 삭제의 앞 요청과 **같은 경로 · 같은 값**. 복귀에 `complete:false` 를 붙이면 `intent.kind = "complete"` 를 재사용하게 되는데, 그 확인 조건은 `status_not = done`(`writes.py:175`) — 지울 행은 사라지므로 이것도 확인 조건을 바꿔야 함.
- 점유 이동 「방 배정」 만들기(`add-flow-tasks`) — 무관. 다만 복귀 뒤 다시 점유 이동하면 지금은 취소된 「방 배정」 행이 쌓이고(dev 같은 방문 6행), 삭제로 바꾸면 쌓이지 않는다(사실: `add_room_assign` 의 `known` sequence 계산 `services/board.py:1430-1432` 은 사본 작업 기준 — 지운 행이 사본에서 빠져도 새 sequence 판정은 「만들기 전에 없던 sequence」라 영향 확인 안 됨: KOS 가 지운 sequence 번호를 다시 쓰는지 확인 안 됨).
- 스펙 문서 동기: SPEC-002 :738(cancel 표) · :766 · :832(규칙 29) · :836(규칙 33) · U-15 :336 · :338 · :340 · `writes.py:22-24` 표 · `write_open` gate.

### W5 — 고칠 방향 후보

1. 복귀 intent 만 새 종류(예: `delete_room_tasks`)로 나눠 `reason: "DELETE"` — 귀가 대기는 `CANCEL` 유지. `write_open` 에 `DELETE` 를 그 경로 · 값 단위로 열기.
2. 확인 조건 = 「그 sequence 가 조회 응답에 없음」(새 expect 키) — 지금 `status = canceled` 로는 영영 안 맞음.
3. HAR 순서를 따라 `complete:false` 를 앞에 둘지 — 「방 배정」이 DONE 이 아니면 필요한지 확인 안 됨(데모 실물 1회).
4. 규칙 33 기준 바꿈 — Q8 후보 1 ~ 5 중.

### W5 — 정할 것

- W5-a 삭제 범위: 복귀만 / 귀가 대기의 「방 배정」 취소까지.
- W5-b `complete:false` 를 앞에 보내나(KOS 웹 순서 그대로) — 「방 배정」 삭제 데모 실물 확인 필요(쓰기 — 사용자 또는 코드 워커 e2e).
- W5-c 「방 배정」(기타 작업)을 `DELETE` 해도 조회에서 빠지는지 데모 실물 1회(시술 작업은 빠짐 확인).
- W5-d 규칙 33 「원래 방」 새 기준(Q8 후보).
- W5-e 이미 `CANCEL` 로 쌓인 「방 배정」 행(dev 같은 방문 6행)은 그대로 두나.

---

## 확인 안 됨 (모음)

- W3: 같은 고객 · 같은 날 방문 2건이 데모에 있는지 · 귀가(`completed`) 방문을 「방에 없음」으로 볼지.
- W4: 사용자가 기다린 표면(DAY 띠 vs KOS 웹) · 화면 실측(브라우저 조작 안 함).
- W5: 「방 배정」 삭제 때 KOS 웹이 `complete:false` 를 먼저 보내는지 · 「방 배정」 DELETE 도 조회에서 빠지는지 · KOS 가 지운 sequence 번호를 재사용하는지 · 복귀 `change-tasks-room` 뒤 `roomAssignedDateTimeUtc` 갱신(SPEC OQ-38).

## 무관 · 참고

- dev api 컨테이너는 4시간 전 재시작(로그 범위 그만큼) — 01:07 ~ 02:52 건은 DB 시각으로만 봤다.
- 오늘 dev 의 방 이동 · 복귀 15건 모두 `attempts 0 · checks 0 · last_error 없음` — 실패 · 재시도 없음.

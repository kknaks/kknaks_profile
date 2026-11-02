# 리뷰 리포트 — strong-hajin-calendar / backend Phase BE-4 (2026-09-21)

## 판정: PASS (WARN 4)

**위반 0건.** allowed_paths 이탈 없음 · 계층 경계 위반 없음 · 계약과 다른 것이 도는 자리 없음 ·
증명 없는 주장 없음. **※1 회귀 수정은 정당하다** — 근거는 아래 §※1 에 전부 적었다.

WARN 넷 중 **하나(W-1)는 PR 전에 고치는 것을 권한다** — 코드와 정반대를 말하는 문장이
영구 기록에 남아, 다음 사람이 ※1 수정을 「버그」로 읽고 지울 수 있다. 고치면 한 줄이다.

---

## 검수 범위

- diff: **uncommitted**(base `bc3b5d8`) — 수정 11 · 신규 2. `git status --porcelain` 실물과 일치.
- allowed_paths 대조(`be4-instructions.md` §allowed_paths = `backend/` · `docker-compose.yml` ·
  `Makefile` · `docs/unified-operations-inventory.json` · `docs/domain-model.md`):
  변경 파일은 `backend/` 10 + `docs/domain-model.md` 1 + 신규 `backend/tests/` 2.
  **이탈 0건.**
- 실행한 검사: `git diff` 전문 · `grep` 호출자 추적 · `python3` 로 `docs/unified-operations-inventory.json`
  파싱 · 스펙/결정문 대조(`spec-004` §2.9·§4·§6 · `decision-003` K22·K25~K30).
  **테스트·빌드는 돌리지 않았다** (reviewer `tools.md` 금지 사항 · 브리프 지시).
- 코디 실측을 그대로 쓴 것: `test-unit` 369p/0f · `test-contract` 1158p/2f(기준선 flaky) ·
  `test-postgres` 102p/0f · 운영 대장 0줄.

---

## 위반 (FAIL 사유)

**없음.**

---

## ※1 — 방예약 재전송 회귀 수정의 정당성 (제일 중요한 자리)

### 회귀는 실재한다 — 그리고 **기존 테스트 둘이 그것을 증명한다**

`create_meeting` 의 회의실 갈래는 **`Idempotency-Key` 가 필수**다
(`bootstrap/application.py:1109-1113` `_room_creation_request_key` — 없으면 `RoomCreationIdempotencyRequired`).
그래서 이 경로의 **모든 재전송**이 `MeetingRoomCreationAttemptRecord` 원장을 지난다.
그 원장의 영수증은 `:1563-1568`(`attempt.meeting_id is not None` → `meetings.get(...)`)에 있고,
**겹침 관문(`:1538` `validate_creation`)보다 뒤**다.

겹침 검증을 관문에 넣으면서 자기 자신을 빼지 않으면, 재전송이 **1차 시도가 세운 자기 회의와 겹쳐
409** 를 맞는다. 이것은 가설이 아니다 — **아래 두 기존 계약 테스트가 지금 그대로 실패한다**:

| 테스트 | 무엇이 깨지나 |
|---|---|
| `tests/contract/test_meeting_rooms.py:340` `test_unknown_room_creation_outcome_is_persisted_and_same_key_never_posts_again` | 같은 키·같은 본문 재전송이 `201` + `replay.json() == first.json()` 이어야 하는데 **겹침 409** |
| `tests/contract/test_meeting_rooms.py:407` `test_one_room_creation_key_cannot_be_reused_for_different_content` | 같은 키·다른 본문이 `detail["code"] == "reservation_idempotency_conflict"` 여야 하는데 **겹침 409 의 `detail` 은 문자열**이라 `["code"]` 첨자에서 터진다 |

즉 워커는 **검수 census 밖에서 실제 회귀를 찾은 것이 맞고**, 고치지 않았다면 `test-contract` 가
붉어진다. 코디 실측 1158p/2f(둘 다 기존 material flaky)가 그 사실을 뒤에서 받쳐 준다.

### 「K12 를 회의로 들여온 것 아닌가」 — **아니다. 다만 브리프의 전제가 틀렸었다**

- **도메인에 멱등 개념이 들어가지 않았다.** `modules/meetings/application.py:335` 가 받은 것은
  `ignore_meeting_id: UUID | None` 하나이고, 이것은 **`update_info` 가 이미 쓰던 것과 똑같은 원시값**
  (`:513 ignoring=meeting.id`)이다. 「그 회의 하나를 검사에서 뺀다」 이상의 의미가 없다.
  원장을 아는 코드는 **조립 층(`bootstrap`)에만** 있다 — `:1534-1540` 의 `select(...)` 한 줄이고,
  그 파일은 이미 `MeetingRoomCreationAttemptRecord` 를 열두 자리에서 읽는 합성 루트다.
- **HTTP·MCP 표면에 새 파라미터가 없다.** `validate_creation` 의 기본값은 `None` 이고,
  비기본 인자를 넘기는 호출자는 `bootstrap/application.py:1538` **하나뿐**이다(grep 전수).
  `MeetingApplication.create` 는 이 인자를 노출조차 하지 않는다.
- **스펙 쪽 근거도 같은 방향이다.** SPEC-004 §4 Case Matrix `TASK_SCHEDULE_OVERLAP` 행(:1052)과
  §6 체크리스트가 **「같은 멱등 키의 재전송은 자기 것과 겹쳐도 영수증이다 — K12 가 K22 보다 먼저다」**
  를 이미 못 박았다. 회의 쪽에 같은 줄이 없는 이유는 **스펙이 회의실 갈래의 생성 원장을 몰랐기 때문**
  이지, 회의를 예외로 정했기 때문이 아니다.

→ **워커 주장(「있는 원장을 안 깨는 것」)이 맞다.** 브리프 §틀리기 쉬운 자리 5 의
「K12 사정권 밖이다 — 멱등 영수증 규칙을 끌어들이지 마라」는 **회의실 갈래를 세지 않은 전제**였고,
그대로 따랐으면 기존 계약 둘이 깨졌다. 조용히 정하지 않고 보고한 것도 맞다.

### 「관문을 앞에 둔 채 자기만 뺀 이유」 — **선다. 거두는 호출이 정말 없다**

- `_release_orphan_reservation`(`bootstrap/application.py:1575`)의 **호출자는 0개다.**
  `grep -rn "_release_orphan_reservation" src/ tests/ frontend/` → **정의 한 줄뿐.**
- **이번 판이 만든 죽은 코드가 아니다** — `git show HEAD:...` 에도 같은 자리(`:1567`)에 있고
  호출자가 없다. 즉 **기존 부채**이고, 관문을 provider 호출 뒤로 옮기면 잡힌 방을 거둘 경로가
  실제로 없다. 워커의 근거가 사실에 부합한다.
- 대안(K12 문자 그대로의 「영수증 먼저」)은 **지문 검사를 관문 앞으로 끌어올리는 재구성**을 요구한다
  (`test_meeting_rooms.py:407` 이 같은 키·다른 본문에 `409` 를 요구하므로, 영수증을 먼저 돌려주면
  그 계약이 깨진다). 잘 덮인 외부 provider 멱등 흐름을 흔드는 것보다 **최소 변경이 옳은 선택**이다.

### 덧: 이 수정이 구멍을 내지는 않는가 — **안 낸다**

같은 키 + **다른 본문**으로 겹침을 우회하려 해도, 관문을 지난 뒤
`_resolve_room_creation_attempt`(`:1197-1200`)의 지문 검사가 `RoomCreationIdempotencyConflict` 로
막는다. **회의는 서지 않고 응답은 여전히 409 다.** (위 `:407` 테스트가 이 자리를 고정한다.)

---

## 경미 (WARN)

### W-1. `domain.py:44` 가 바로 옆 코드와 **정반대**를 말한다 — PR 전 수정 권장

`backend/src/ax_workspace/modules/meetings/domain.py:44-45`:

> **`TASK_SCHEDULE_OVERLAP` 과 달리 멱등 영수증 규칙(증보 K12)의 사정권 밖이다** —
> 회의 명령이라 생성 멱등 원장을 지나지 않는다.

**사실이 아니다.** 회의실을 고른 생성은 `Idempotency-Key` 가 **필수**이고
(`bootstrap/application.py:1109-1113`) 생성 멱등 원장(`MeetingRoomCreationAttemptRecord`)을 **지난다**.
같은 diff 의 `bootstrap/application.py:1534-1540` 과 `meetings/application.py:335-350` 이
정확히 K12 의 취지대로 그 원장을 읽어 자기 회의를 빼고 있다.

- **근거**: reviewer `rules.md` 공통 3(근거 없는 단정)·backend 체크리스트 「판단 계약 — 재전송이
  영수증인가」. 그리고 `validate_creation` docstring(「K12 를 회의로 들여오는 것이 아니다」)과
  `domain.py`(「사정권 밖이다」)가 **서로 다른 말을 한다.**
- **왜 남기면 위험한가**: `domain.py` 가 이 예외의 정본 설명 자리다. 다음 사람이 그 문장을 읽고
  `bootstrap:1534` 의 제외를 「K12 를 잘못 들여온 것」으로 보고 지우면 `test_meeting_rooms.py:340`·`:407`
  둘이 다시 깨진다. **이번 판이 발견으로 뒤집은 전제가, 뒤집히지 않은 채로 기록에 남는다.**
- **권장 수정**: 그 두 줄을 사실로 바꾼다 — 「회의실을 고른 생성은 생성 멱등 원장을 지나고,
  그 영수증이 이 검사보다 뒤에 있으므로 조립 층이 그 키가 세운 회의를 검사에서 뺀다
  (`bootstrap` `ignore_meeting_id`). 방을 안 고른 생성·시각 변경에는 멱등 원장이 없다.」
- **FE-3 브리프: 싣지 않는다** (백엔드 내부 기록).

### W-2. 재전송 보호가 **자기 충돌에만** 걸린다 — 잔여 틈

`ignore_meeting_id` 는 **그 키가 세운 회의 하나**만 뺀다. 1차 시도와 재전송 **사이에 새 블록이
생기면** 재전송은 영수증 대신 겹침 409 를 받는다. 구체적 시나리오(전부 현재 코드로 도달 가능):

1. 민아가 방을 골라 회의 M(내일 10:00–11:00, 참석 지호)을 예약 → provider 응답 유실, `attempt` 에
   `meeting_id` 는 이미 박혔다.
2. 지호가 **`DONE` 이던 업무를 되열면**(그 업무에 10:30–11:30 살아 있는 배정이 있다) —
   `platform/time_blocks.py:114` 가 `DONE` 을 걸렀기 때문에 1번 때는 블록이 아니었는데 **이제 블록이다.**
   (`quick_start` 로 지금 시각을 덮는 회의를 세우는 길도 같은 모양이다 — 그쪽은 관문을 안 지난다.)
3. 클라이언트가 같은 키로 재전송 → 관문이 그 배정을 보고 **409**. 계약이 요구한 답은 **영수증**이다.

- **근거**: SPEC-004 §6 「같은 멱등 키의 재전송은 자기 배정과 겹쳐도 `200` 영수증이다 —
  **증보 K12 가 K22 보다 먼저다**」(:1478-1480). 배정 쪽은
  `modules/work/creation_commands.py:241` 이 **원장 조회 → 영수증 → 그 다음 검사** 순서로 그것을
  문자 그대로 지킨다. 회의 쪽은 순서가 반대라 **부분적으로만** 지킨다.
- **이번 판정에 넣지 않는 이유**: 도달 경로가 좁고(`quick_start` 또는 되열기), 이번 diff 가 만든
  회귀가 아니라 **이번 diff 가 90% 막은 것의 나머지**다. 최소 변경 판단이 옳았다는 §※1 의 결론과
  모순되지 않는다.
- **권장(후속)**: 회의실 갈래 맨 앞에서 `_room_creation_lock` 을 잡고 지문 검사 → `meeting_id` 가
  있으면 곧장 영수증, 없으면 관문. 배정 쪽과 순서가 같아지고 잔여 틈이 닫힌다.
- **FE-3 브리프: 싣지 않는다** (백엔드 후속).

### W-3. `test_editing_a_meeting_without_moving_it_never_asks_about_overlap` 이 **공회전한다**

`tests/contract/test_meeting_time_overlap.py:266-283`. 회의 하나만 세우고 **같은 시각**을 다시 실어
제목을 바꾼 뒤 `200` 을 단언한다. 그런데 그 픽스처에는 **다른 블록이 하나도 없고**, 시각 검사는
`ignoring=meeting.id` 로 자기 자신을 빼므로 — **`:508` 의 시각 동일성 가드가 있든 없든 결과가
똑같이 `200` 이다.** 즉 docstring 이 말하는 「이미 겹쳐 있는 회의의 제목조차 고칠 수 있다」를
이 테스트는 **재지 않는다.**

- **가드 자체가 무방비인 것은 아니다** — 같은 파일 `:285` `test_adding_an_attendee_alone_does_not_pass_the_overlap_gate`
  는 실제로 겹치는 배정을 깔아 두므로, 「항상 검사」로 바뀌면 그 테스트가 잡는다. **커버리지 0 은 아니다.**
- **근거**: reviewer `rules.md` backend 「테스트 — 새 경로에 테스트가 있나」. 있긴 한데 **그 문장을
  재는 테스트가 아니다.**
- **권장 수정(한 함수)**: `:285` 의 수법을 그대로 쓴다 — ① 회의 A(지호+민아, 10:00–11:00) ②
  회의 B(소라만, 10:00–11:00) ③ **참석자만** 바꿔 B 에 민아를 넣는다(관문을 안 지난다) →
  **진짜로 겹쳐 있는 한 쌍**이 선다 ④ B 의 제목만 바꿔 `200` 을 단언. 그러면 「기존 데이터를 소급해
  막지 않는다」가 실제로 측정된다.
- **FE-3 브리프: 싣지 않는다** (백엔드 테스트 품질).

### W-4. 겹침 409 의 `detail` 은 **문자열**이고 **마침표가 없다** — FE-3 이 알아야 한다

`entrypoints/http.py:531` 이 `detail=str(error)` 로 낸다. 방예약 409 들(`room_unavailable` 등)이
`{"code", "message", "available_rooms"}` **객체**를 내는 것과 모양이 다르다.

- 서버가 내는 문자열: `"민아 님의 일정과 겹칩니다"` — **마침표 없음.**
  SPEC §4 Case Matrix(:1053)의 예시 문구는 「민아 님의 일정과 겹칩니다.」 로 마침표가 있지만
  **(제안 — 문구)** 표기이고, 형제인 `TaskScheduleOverlap`(`modules/work/application.py:663`)도
  같은 방식으로 마침표를 뺐다. **BE-3 과 일관되므로 위반이 아니다.**
- 프론트는 이미 문자열 `detail` 을 처리한다(`frontend/src/lib/api.ts:106·121·138`) — 깨지지 않는다.
- **FE-3 브리프: 싣는다** — 셋을 적어 주는 것이 좋다.
  ① 겹침 거절 문구는 **서버가 만든다**(`ApiError.message` 그대로 띄우고 FE 가 문장을 짓지 않는다).
     `detail.code` 를 읽으면 `undefined` 다.
  ② **마침표를 붙이지 마라** — 서버 문자열이 정본이다.
  ③ **참석자만 추가하는 것은 겹침 검사를 지나지 않는다**(K30, 사용자 확인). 사람을 나중에 부르는
     화면이 「충돌 없음」을 약속하면 안 된다.

---

## 기존 부채 (이번 판정 제외)

- `bootstrap/application.py:1575` `_release_orphan_reservation` — **호출자 0개의 죽은 코드.**
  `HEAD`(`bc3b5d8`) 에도 같은 상태다. 이번 diff 가 만든 것이 아니지만, ※1 의 설계 근거가
  「거두는 호출이 없다」이므로 **그 사실이 기록되어 있지 않다는 점**은 남는다.
- `tests/contract/test_material_search.py` · `test_material_worker_recovery.py` 의 **병렬 격리** —
  `flaky-baseline-evidence.md` 가 이미 무관으로 닫았다. 범위 밖.
- K29 `meetings_visible_to` 의 SQLite tz 바인딩 — 코디가 「남긴다」로 정했고 **실제로 손대지 않았다**
  (`platform/meetings.py` 가 diff 에 없다). 확인만 한다.

---

## 확인한 것 (PASS 근거) — 볼 것 아홉 + 체크리스트

### 1. 문이 하나인가 — ✅

- 회의 쪽이 규칙을 **다시 쓰지 않았다.** `meetings/application.py:379-381` 이
  `overlapping_blocks(member_ids, (starts_at, ends_at), ignore_meeting_id=...)` **한 줄**만 부르고,
  그 뒤 하는 일은 `blocks[0].member_id` 로 이름을 고르는 것뿐이다.
- **반열림 판정도 자정 분할도 회의 쪽에 복사돼 있지 않다** — `platform/time_blocks.py:158-159`
  (`starts_at < window_to AND ends_at > window_from`)와 `:170` `split_across_office_dates` 가
  문 안에 그대로 있다. `modules/meetings/` 어디에도 `<`/`>` 시각 비교가 없다(grep 전수).
- 포트 이동이 옳다: `TimeBlockRepository` 가 `modules/work/application.py` 에서
  `modules/time_blocks.py:73` 로 **옮겨졌다**(복제가 아니라 이동 — 원본이 삭제됐다).
  배정·회의 두 도메인이 서로를 import 하지 않게 하는 유일한 자리다.
- 정렬은 문 안(`platform/time_blocks.py:91`, `(starts_at, source, source_id, member_id)`)에 있어
  **「가장 먼저 시작하는 블록의 주인」이 결정적**이다.

### 2. `member_ids` 가 주최자 + 활성 참석자 전원인가 — ✅

- **생성**: `_validated_creation:411` `attendees = self._resolved_attendees(principal, attendee_ids or [])`
  → `policy.py:124-126` `meeting_attendees(...)` 가 **owner 를 항상 더하고 중복을 제거**한다.
  그 집합 그대로 `:418` 에 들어간다.
- **시각 변경**: `:510` 이 `self._repository.attendee_ids(meeting)` 를 쓰고, 그 구현
  (`platform/meetings.py:193-201`)은 **`removed_at IS NULL`** 로 제한한다.
  **제거된 참석자는 안 섞인다.** owner 는 생성·`replace_attendees` 양쪽에서 언제나 참석 행을 갖는다.
- **블록 쪽도 같다**: `platform/time_blocks.py:153`·`:200` 두 질의 모두 `removed_at.is_(None)`.
- **사외 참석자는 구조적으로 빠진다** — `MeetingRecord.external_attendees` 는
  `JSON` 이름 배열(`persistence.py:318`)이라 member id 가 존재하지 않는다.
  `frozenset(attendees)` 는 `list[str]` member id 로만 만들어진다. **제외 분기가 없다.**
- `member_ids` 가 빌 수 없다(언제나 owner 포함) → `overlapping_blocks:85` 의 조기 `return []` 로
  검사가 통째로 무력화되는 경로가 없다.

### 3. `quick_start` 가 정말 안 걸리나 — ✅ (코드로 확인)

- `quick_start`(`meetings/application.py:437-461`)는 `self._repository.create(...)` 를 **직접** 부른다.
  `_validated_creation` 도 `_require_free_time` 도 **지나지 않는다.** 분기가 없는 것이 맞다.
- 회의 생성 자리 **둘**(`create:297` · `quick_start:437`)과 시각 변경 **하나**(`update_info:474`),
  `meeting.starts_at` 쓰기 자리 **하나**(`:521`) — 브리프 census 와 실물이 일치한다(grep 전수).
- **워커가 남긴 「리팩터가 오면 잡는 테스트」는 실제로 그 일을 한다.**
  `test_quick_start_is_never_refused_for_overlapping`(`test_meeting_time_overlap.py:165`)이
  **지금 시각을 통째로 덮는 회의**(now−1h ~ now+3h)를 같은 사람(JIHO)으로 먼저 세운다.
  `quick_start` 창(now ~ now+`QUICK_START_LENGTH`)이 그 안에 완전히 들어가므로,
  `quick_start` 를 `_validated_creation` 으로 합치는 리팩터가 오면 **반드시 409 가 되어 잡힌다.**

### 4. 시각이 안 바뀌면 검사를 안 지나는 것이 옳은가 — ✅ (판단 타당)

- 가드는 `:508` `if (starts_at, ends_at) != (_aware(meeting.starts_at), _aware(meeting.ends_at))`.
  **순간 비교**라 tz 표기에 흔들리지 않는다(aware datetime 비교는 instant 비교).
- 근거가 계약에 있다: SPEC §2.9 「**검증은 새 쓰기에만** 건다」 + §6 「이미 겹쳐 있는 기존 데이터를
  건드리지 않는다」. 안 걸면 quick-start 로 겹쳐 버린 회의의 **제목조차** 못 고친다.
- **시각과 참석자가 같이 오면 바뀐 뒤의 명부로 묻는다** — `:499-504` 가 쓰기(`:523`)보다 **먼저**
  `attendees` 를 풀고 `:510` 이 그 값을 쓴다. 두 번 풀지 않는다.
  `test_moving_a_meeting_asks_about_the_attendees_it_will_have`(`:300`)가 이 자리를 재고,
  **거절 뒤 명부·시각이 그대로인 것까지** 단언한다.
- K30(참석자만 추가는 관문을 안 지난다)은 사용자 확인 사항 — 지적하지 않는다.
  `test_adding_an_attendee_alone_does_not_pass_the_overlap_gate`(`:285`)가 그 사실을 고정하고,
  docstring 이 「구멍으로 볼 수도 있는 자리」라고 **숨기지 않고** 적었다.
- 검사 순서가 옳다: 403(`_require`) → 404(`_readable`) → 회차 409 → 참석자 403 → 미지 필드 422 →
  상태 409 → 스케줄 422 → 참석자 해석 422 → **겹침 409 가 마지막**.

### 5. ※1 — 위 전용 절 참조. **정당하다.**

### 6. `approval` — ✅

- **같은 함수·같은 어휘**: `modules/work/application.py:791` 이 목록·상세가 쓰는
  `self._approval_from_rounds(task, rounds.get(task.id))`(`:1052`)를 **그대로** 부른다.
  값 어휘는 `None`·`awaiting_review`·`awaiting_revision`·`approved` — SPEC §4 그대로.
- **`derived` 묶음 전체를 싣지 않는다**: `CalendarTaskRow`(`task_results.py:362-370`)에
  `approval` 한 키만 더했다. `test_a_calendar_task_row_carries_the_approval_and_nothing_else_of_derived`
  (`:414`)가 **행의 필드 집합 11개를 통째로 못 박고** `derived`·`overdue_days`·`blocking_children`
  부재를 명시 단언한다.
- **열을 안 만들었다**: `tasks` 에 `approval` 칼럼 없음. 값은 `DecisionItem`/`Submission`/`ReviewDecision`
  회차 사실에서 파생된다. `docs/domain-model.md` 가 「열이 아니라 투영이다」로 그 사실을 적었다.
- **한 질의인가(N+1 아닌가)**: `:780` 이 `approval_rounds_for([모든 task.id])` 를 **루프 밖에서 한 번**
  부른다. 그 구현(`platform/work_tasks.py:484-529`)은 업무 수와 무관하게 **`in_()` 3회**로 끝난다.
  **부모 것만 묻는 것**도 옳다 — 캘린더 행은 `blocking_children` 을 내지 않으므로 하위 id 가 불필요하다.
- **운영 대장 0줄이 맞다 — 독립 확인.** `docs/unified-operations-inventory.json` 의
  `GET /api/calendar` 행 `http_signature` 는
  `(from_: date, to: date, principal: Principal) -> list[dict[str, object]]` 이다.
  반환 원소가 `dict[str, object]` 라 **키를 더해도 시그니처가 안 바뀐다.** `http_count` 159 불변.

### 7. WARN-2 수정 — ✅

- `_members_held_by`(회의 1건당 1질의)가 삭제되고 `_attendees_of`(`platform/time_blocks.py:184-207`)로
  바뀌었다. `MeetingAttendeeRecord.meeting_id.in_([...])` **한 질의** + 파이썬 그루핑.
  → 회의 쪽 질의는 `meetings 1 + attendees 1 + schedules 1` 로 **회의 수와 무관**해졌다.
- **계약이 안 갈렸다**: 필터 셋(`removed_at IS NULL` · `member_id.in_(member_ids)` · owner 합집합)이
  **문자 그대로 같다**. 정렬(`sorted(...)`)도 유지.
- **조용히 비는 함정을 확인했다**: `grouped` 의 키는 `MeetingAttendeeRecord.meeting_id` 이고
  조회는 `meeting.id` 로 한다. 둘 다 `Uuid(as_uuid=True)`(`persistence.py:296`·`:475`)라
  **파이썬 `UUID` 로 타입이 일치**한다 — str/UUID 불일치로 참석자 블록이 통째로 사라지는 사고가 없다.
  PostgreSQL 실측(`test-postgres` 102p/0f, +6건)이 이 자리를 뒤에서 받친다.

### 8. 기존 회의 계약 회귀 — ✅ 실제로 잰다

| 브리프가 요구한 것 | 재는 테스트 | 무엇을 단언하나 |
|---|---|---|
| 목록 **두 모양** | `:351 test_the_meeting_list_keeps_both_of_its_shapes` | 기간 갈래 = `list` · 무기간 갈래 = `{upcoming, past}` + `past = {items, next_cursor}` |
| 기간 갈래 **행 필드** | 같은 테스트 | `set(row)` 9개 정확 일치, `created_by_display_name` **부재**(K4) |
| **열람 권한** | `:372 test_someone_who_may_not_open_a_meeting_still_cannot` | 남의 회의 상세 **404** |
| **생성 응답 모양** | `:380 test_a_meeting_with_no_conflict_is_created_exactly_as_before` | `status`·`location`·참석자 집합 |

`my_meetings`·`readable_rows` 는 `meetings_visible_to` 를 건드리지 않았으므로(그 파일이 diff에 없다)
1루프에서 걸렸던 소비처 셋이 그대로다.

### 9. 조용히 통과하는 자리 — **워커의 「전수 확인, 없다」는 대체로 맞다. 하나 찾았다**

- **※2 는 약화가 아니다.** `test_meeting_core.py:339` 의 `days=5.0` 은 두 번째 회의를 다른 날로
  옮긴 것뿐이고, 그 테스트가 재는 것은 「**취소**와 **회의록만 삭제**가 다른 것을 지운다」다.
  날짜는 그 단언과 무관하다 — 취소 204 · `status == "cancelled"` · `agendas == []` 단언이 전부 그대로다.
  같은 시각이었던 것은 우연이지 계약이 아니었다.
- **가려질 수 있던 409 를 전수 확인했다.** 회의를 세우는 테스트 파일 넷
  (`test_meeting_core` 24 · `test_meeting_rooms` 23 · `test_task_schedules` 26 · `test_meeting_creation_input` 1)의
  `409` 단언을 전부 읽었다.
  - `test_meeting_rooms` 의 409 들은 **모두 `detail["code"]` 를 함께 단언**한다
    (`room_unavailable`·`reservation_unavailable`·`reservation_auth_failed`·`reservation_idempotency_conflict`).
    겹침 409 의 `detail` 은 문자열이므로 **가려지면 첨자에서 터진다** — 조용히 통과할 수 없다.
  - `test_meeting_core` 의 409 들은 안건·삭제·시작 등 **다른 엔드포인트**이거나 상태 충돌이다.
  - `test_task_schedules` 의 409 들은 배정 쪽(BE-3)이고, `:106` 은 10–11 vs 14–15 로
    **겹치지 않는 두 시각**이라 「하루 한 칸」을 겹침이 대신 답할 수 없다.
  - 회의 생성 헬퍼(`_schedule`·`_book`·`_booked`)가 전부 `assert status == 201` 이라
    새 관문에 걸리면 **곧바로 시끄럽게 실패**한다.
- **찾은 하나 → W-3.** `test_editing_a_meeting_without_moving_it_never_asks_about_overlap` 이
  가드 유무와 무관하게 통과한다. 다만 가드 자체는 `:285` 가 잡으므로 무방비는 아니다.
- **정직하게 적을 것 하나**: `test_an_external_attendee_never_blocks_the_meeting`(`:191`)은
  **구조적으로 공회전할 수밖에 없다** — 사외 이름에는 member id 가 없어 충돌 픽스처를 만들 방법이
  애초에 없다. 이 사실은 테스트가 아니라 **스키마**(`persistence.py:318` JSON 이름 배열)가 증명하고,
  워커의 docstring 도 그렇게 적었다. **약점이 아니라 증명 수단이 다른 것**이므로 WARN 에 넣지 않는다.

### 그 밖 backend 체크리스트

- **경계** — `modules/meetings/application.py` 새 import 는 `modules.time_blocks` 하나(순수 파이썬).
  `modules/time_blocks.py` 는 `typing.Protocol` · `uuid.UUID` 만 더했다.
  `fastapi`·`mcp`·`sqlalchemy` 유입 **0**. 원장 조회는 조립 층에만 있다.
  `tests/architecture` 포함 `test-unit` 369p/0f 가 이것을 기계로 확인했다.
- **스키마** — `create_all`·DDL 신규 호출 0. **새 표 0** — 그래서 `docs/domain-model.md` 도
  대조표에 행을 더하지 않고 `task_schedules` 행에 「겹침 금지는 이 표의 제약이 아니다」와
  「`approval` 은 열이 아니라 투영」 두 사실만 덧댔다. **표와 본문이 안 어긋난다.**
- **판단 계약** — envelope 를 만지지 않았다. command 위임 구조 그대로.
- **재사용** — `overlapping_blocks` · `approval_rounds_for` · `_approval_from_rounds` ·
  `_resolved_attendees` 전부 **있는 것을 썼다.** 재구현 0.
  `_person_name`(`meetings/application.py:2002-2009`)만 새로 썼는데,
  `platform/work_tasks.py:81-89` `_person` 과 **같은 규칙**(`" ("` 앞을 자르고 없으면 id)이고
  docstring 이 그 출처를 밝힌다. 층이 달라(모듈 vs 플랫폼) 그 함수를 직접 못 쓴다 — 중복이 아니다.
- **예외** — 아래층이 `HTTPException` 을 던지지 않는다. 새 `except Exception` **0건**
  (`git diff | grep '^+.*except Exception'` → 없음).
  조립 누락 방어(`:353-355`)가 `MeetingError`(→422)인 것은 배정 쪽
  `_schedule_repository`/`_time_block_repository`(`work/application.py:628-636`, `TaskError`→422)와
  **같은 기존 패턴**이고 `# pragma: no cover` 표기도 같다.
- **테스트** — 새 계약 19건(`test_meeting_time_overlap.py`) + PostgreSQL 6건.
  `integration` 마커는 `tests/integration/postgres/` 의 **기존 관례**이고
  BE-3 이 같은 자리에 `test_task_schedule_overlap_postgres.py` 를 두었다. 브리프 §검증이
  `make test-postgres` 를 명시 요구하므로 **허가 안에 있다.**
- **K28** — 코디 지시대로 고쳤고, 형제 모델
  `MeetingReservationInput.validate_schedule`(`commands.py:145-153`)과 **한 글자도 다르지 않은 방식**이다.
  `model_config` 에 `validate_assignment` 가 없어 after-validator 안의 대입이 재귀하지 않는다.
  `test_a_meeting_never_collides_with_itself_when_it_slides`(`:233`)가 `01:30:00+00:00` 로
  **밀린 값을 정면으로 단언**한다 — 코디가 말한 「단언하는 테스트 없음」이 이 판에서 닫혔다.
- **K29** — `platform/meetings.py` 가 diff 에 없다. **손 안 댔다.** 결정대로다.

---

## 한 줄

**PASS.** ※1 은 정당하다 — K12 를 도메인에 들인 것이 아니라 `update_info` 가 이미 쓰던
`ignore_meeting_id` 를 조립 층에서 한 번 더 쓴 것이고, 고치지 않으면 `test_meeting_rooms.py` 의
기존 계약 둘이 깨진다. 브리프의 「K12 사정권 밖」이 틀린 전제였음을 워커가 실물로 뒤집었다.
**다만 그 뒤집힌 전제가 `domain.py:44` 에 그대로 남아 있다(W-1) — 한 줄, PR 전에 닫는 것이 좋다.**

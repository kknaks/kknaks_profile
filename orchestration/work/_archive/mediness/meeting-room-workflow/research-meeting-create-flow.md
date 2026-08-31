# 조사 — 회의 생성 요청이 FE→BE→DB 로 어떻게 흐르나 (현행)

- 대상 워크트리: `/Users/kknaks/orca/workspaces/mediness-app/meeting-room-workflow` (브랜치 `meeting-room-workflow`)
- 방식: **코드 리딩만** (DB 접속·docker·테스트 실행 없음). 모든 주장에 `파일:줄` 근거.
- 결론 한 줄 먼저: **회의실·예약은 우리 DB 에 테이블이 없다.** 방·예약은 전부 외부 시스템 **THE CONNECT(TDL)** 가 원장이고, 우리 쪽에는 `actions`(승인 카드) 원장의 payload 안에 방 정보가 박혀 있을 뿐이다. 스케줄(시간대별 점유) 뷰와 자동 배정은 이 사실이 설계의 1차 제약이다.

---

## §3-1. 요청 경로 — 모달 제출 → front API route → back router → service → repository → DB

### 1-a. 단계 나열

| # | 계층 | 위치 | 함수/엔드포인트 |
|---|---|---|---|
| 1 | FE 컴포넌트 | `front/components/meeting-v2/MtgV2CreateModal.tsx:252-320` | `submit()` — `fetch("/api/meetings-v2", {method:"POST"})` (`:260`) |
| 2 | BFF route | `front/app/api/meetings-v2/route.ts:25-32` | `POST` → `createMeetingV2Envelope(() => req.text())` |
| 3 | BFF server 계층 | `front/lib/server/meetings-v2.ts:73-77` (+ `:34` `MEETINGS_V2_PATH = "/meetings-v2"`) | `requestBack("/meetings-v2", {method:"POST", body})` |
| 4 | back router | `back/app/routers/meetings_v2.py:81-89` | `create_meeting_v2()` — `POST /api/v1/meetings-v2` (prefix 는 `back/app/main.py:378`), 201, `require_capability("meeting.meeting.basic")` (`:71`) |
| 5 | service | `back/app/services/meeting_v2_service.py:206-257` | `MeetingV2Service.create_meeting()` |
| 5-a | 참석자 검증 | 같은 파일 `:259-272` | `_assert_invitable()` → `invitable_member_ids()` (`back/app/services/meeting_v2_participants.py:61-71`) |
| 5-b | 태그 검증 | `back/app/services/product_catalog.py:345-360` | `validate_product_tags()` |
| 5-c | (조건부) 회의실 예약 | `meeting_v2_service.py:312-396` | `_reserve_room_now()` — §3-2 참조 |
| 6 | repository | `back/app/repositories/meeting_v2_repo.py:79-113` | `MeetingV2Repository.create()` |
| 6-a | 예약 run 연결 | 같은 파일 `:115-118` | `link_reservation()` — `meeting_v2.reservation_run_id = run_id` |
| 7 | DB | — | `INSERT meeting_v2` 1행 + `INSERT meeting_v2_attendee` N행 (`meeting_v2_repo.py:96-112`). commit 은 service `:253` |
| 8 | 응답 조립 | `meeting_v2_service.py:916-950` | `_to_detail()` — 예약 상태는 저장값이 아니라 `actions` 카드에서 되읽는다 (`:500-532`) |

### 1-b. 요청 payload shape

FE 가 만드는 body (`MtgV2CreateModal.tsx:263-277`):

```jsonc
{
  "title": "string",                    // trim 됨
  "scheduled_date": "YYYY-MM-DD",
  "scheduled_start": "HH:MM",           // 30분 슬롯
  "scheduled_end":   "HH:MM",
  "attendee_member_ids": ["<organization_member.id>", ...],  // host 는 FE 가 제외해 보냄(:269-271)
  "visibility": "public" | "private",
  "product_tags": ["medi"] | ["company"] | ["leader"] | [],  // productTagsForChip(:273)
  "room_reservation": { "room_id": 3 }   // 선택 시에만 키가 존재(:274-276). 없으면 "예약 안 함"
}
```

- 서버 계약: `back/app/schemas/meeting_v2.py:34-74` (`MeetingV2CreateRequest`), `:29-32` (`RoomReservationRequest`, `room_id: int >= 1`).
- 시간 3필드 전부 필수, `_SLOT = ^([01][0-9]|2[0-3]):(00|30)$` (`schemas/meeting_v2.py:25`), `종료 > 시작` (`:69-74`).
- `product_tags` 는 서버가 소문자화 (`:61-67`).
- **host 는 body 로 받지 않는다** — 요청자가 곧 host (`meeting_v2_service.py:225`, `self.policy.member_id`).
- 참석자 축은 `organization_member.id` 다 (`users.id` 아님 — `schemas/meeting_v2.py:38-42`).
- `productTagsForChip` 매핑: `all` 칩 → `company`, `leader` 칩 → `leader`, 제품 칩 → 그 slug, 부서 칩 → `[]` (`front/lib/meeting-participants.ts:213-223`).

### 1-c. 응답 shape

`DataResponse[MeetingV2Detail]`, 201 (`routers/meetings_v2.py:81`). 주요 필드는 `schemas/meeting_v2.py` 의 `MeetingV2Detail` + `_to_detail`(`meeting_v2_service.py:931-950`):

```jsonc
{ "data": {
  "id", "host_user_id",        // ⚠ 값은 organization_member.id (schemas/meeting_v2.py:157-170 규율)
  "host_name", "title",
  "scheduled_date", "scheduled_start", "scheduled_end",
  "state": "waiting", "visibility",
  "audio_path": null,
  "attendees": [{"user_id": "<member_id>", "name": "..."}],
  "product_tags": [...],
  "room_reservation": { "status": "done", "room_name": "회의실 3", "action_id": "..." },  // 예약 요청한 회의만. 부재 ≠ null
  "created_at", "updated_at", "viewerRelation", "permissions": {...}
}}
```

### 1-d. v1 과의 관계

v1(`back/app/routers/meetings.py` · `services/meeting_service.py`)은 **GET 전용 보관 read surface** 이고 생성 POST 는 제거됐다 — BFF 도 GET 만 프록시한다 (`front/app/api/meetings/route.ts:1-8` 주석: "POST(회의 생성)는 v1 라이브 은퇴(WP-045)로 제거됨"). **모달이 쏘는 쪽은 전부 v2 다.**

---

## §3-2. 회의실 조회·예약

### 2-a. 후보 목록이 어디서 오나 (조회 경로)

| # | 계층 | 위치 |
|---|---|---|
| 1 | 모달 | `MtgV2CreateModal.tsx:183-204` `runRoomLookup()` → `fetchRoomCandidates({date,start,end,headcount})` |
| 2 | FE lib | `front/lib/meeting-room.ts:54-72` → `GET /api/meetings-v2/rooms/availability?date&start&end&headcount` |
| 3 | BFF route | `front/app/api/meetings-v2/rooms/availability/route.ts:14-28` — 화이트리스트 4개 질의만 전달 |
| 4 | BFF server | `front/lib/server/meetings-v2.ts:56-60` |
| 5 | back router | `back/app/routers/meetings_v2.py:132-153` `get_meeting_v2_room_availability()` — leaf `meeting.meeting.basic`, `bind_tenant`(`:148`) |
| 6 | service | `meeting_v2_service.py:534-565` `room_availability()` |
| 7 | 예약 도메인 | `back/app/services/action_runtime/workflow/meeting/surface.py:104-151` `room_candidates()` |
| 8 | 외부 gateway | `back/app/clients/the_connect.py:252-274` `HttpTdlGateway.availability()` → `rooms()`(`:223-232`) + `list_reservations()`(`:276-302`) |

**후보 필터 3겹** (`surface.py:114-151`):
1. 그 시각 겹치는 THE CONNECT 예약 제외 → `available_rooms` (`the_connect.py:256-272`, `_overlaps` `:144-145`)
2. `room.capacity >= headcount` (정원 미달 제외)
3. `held_room_ids` — **로컬 hold**: 우리 `actions` 원장에서 같은 날짜·`APPROVED|EXECUTING|FAILED_RETRYABLE` 상태의 reserve 카드가 물고 있는 방 (`workflow/meeting/workflow.py:660-687`, `HOLD_STATUSES` `:66-70`)

방 카탈로그 자체도 THE CONNECT 다 — `GET /api/rooms` 를 받아 `type` 없음 + `id <= 7` + 이름에 "스튜디오" 없음 으로 거른다 (`the_connect.py:223-232`). `has_monitor` 는 **`id != 1` 이라는 하드코딩 규칙**이다 (`:229`).

응답: `{"data": {"rooms": [{id, name, capacity, has_monitor}]}}` (`schemas/meeting_v2.py:139-149`). FE 는 `roomMetaText` 로 "정원 6 · 모니터" 를 만들고(`front/lib/meeting-room.ts:75-79`), 꼬리표 `N명 가능` 은 후보의 정원이 아니라 **입력한 headcount 를 그대로 찍는 것**이다 (`MtgV2CreateModal.tsx:593`).

`headcount` = FE 는 `memberIds.length`(host 포함, `MtgV2CreateModal.tsx:124-128`), BE 는 `len(attendee_ids) + 1` (`meeting_v2_service.py:302-310`).

조회 트리거 조건: `시간 3필드 유효 && 태그 칩 선택됨 && headcount > 0` 일 때만 (`MtgV2CreateModal.tsx:178-181`), 350ms 디바운스(`:75`, `:215-218`), 조건 변경 시 **선택 초기화**(`:209`).

실패 계약: 자격 미설정·THE CONNECT 장애는 빈 배열이 아니라 `503 ROOM_LOOKUP_FAILED` (`meeting_v2_service.py:549-557`, `back/app/core/errors.py:838-848`). FE 는 `idle / loading / ready(0건) / error` 4상태를 구분한다 (`MtgV2CreateModal.tsx:533-599`).

### 2-b. 예약은 회의 생성과 한 트랜잭션인가

**한 요청·동기·all-or-nothing 이지만, DB 트랜잭션은 하나가 아니다.** 별도 요청도 아니다 — `POST /meetings-v2` 한 방에 끝난다.

순서 (`meeting_v2_service.py:206-257` + `:312-396`):

```
① ② 실행 직전 재검증  _classify_room()  (:274-300 → surface.classify_room_choice :177-207)
      ├ stale     → 422 ROOM_CANDIDATE_STALE   (회의 미생성)
      └ preempted → 422 ROOM_PREEMPTED          (회의 미생성)
① run 생성   meeting_surface.start_reservation(source="meeting_modal", preferred_room=verdict.room)
      (:352-381 · surface.py:215-292)   → 실패 시 db.rollback() + 422 RESERVATION_EXEC_FAILED
   ★ await self.db.commit()   (:383) ← 여기서 run 원장이 먼저 커밋된다
③ 자동승인 + THE CONNECT 동기 실행  _auto_approve()  (:391 → :398-438)
      kernel.approve() → the_connect.create()  (the_connect.py:314-324)
      ├ DONE            → 통과
      ├ NEEDS_APPROVAL / FAILED_TERMINAL → run 실패 종결 + 422 ROOM_PREEMPTED
      └ FAILED_RETRYABLE 등             → run 실패 종결 + 422 RESERVATION_EXEC_FAILED
   ★ await self.db.commit()   (:392)
④ 회의 저장  meetings.create() + link_reservation()  (:241-252)
   ★ await self.db.commit()   (:253)
```

- **커밋 3회**다 (`:383`, `:392`, `:253`). "예약이 성공해야 회의가 존재한다" 는 성립하지만 그 역은 아니다 — ④ 직전에 프로세스가 죽으면 **THE CONNECT 예약은 잡혔는데 회의는 없는** 고아 예약이 남는다. 보상 경로는 코드에 없다.
- 모달 발 예약은 **승인 카드를 사람에게 안 보인다** — 만들자마자 자동승인해 종결시킨다 (`:315-326` docstring, `source` 로 예외 경계 판정 `:373`, `MEETING_MODAL_SOURCE = "meeting_modal"` `:79`).
- FE 는 `ROOM_PREEMPTED` / `ROOM_CANDIDATE_STALE` / `RESERVATION_EXEC_FAILED` 3코드를 잡아 **모달을 닫지 않고** 선택 초기화 + 후보 재조회한다 (`MtgV2CreateModal.tsx:284-299`).
- 오류 정의: `back/app/core/errors.py:838-884` (`ROOM_LOOKUP_FAILED` 503, 나머지 3종 422).

### 2-c. 충돌(동시간 중복 예약) 방지는 어디서 하나

**DB 제약은 하나도 없다.** 3겹 방어 전부 애플리케이션·외부다:

1. **조회 시점 필터** — `surface.room_candidates` 가 THE CONNECT 예약 겹침 + 로컬 hold 제외 (`surface.py:142-151`)
2. **실행 직전 재검증** — `classify_room_choice` 가 같은 산식을 한 번 더 돌린다 (`surface.py:177-207`; service `:345-349`)
3. **외부 최종 재검증** — `the_connect.create()` 가 자기 후보를 다시 계산해 요청 방이 빠졌으면 `ReservationPreempted` 를 돌려준다 (`the_connect.py:314-324`)

즉 **최종 권한은 THE CONNECT** 이고, 우리 쪽 방어는 낙관적 재검증이다. 2 와 3 사이 race 는 3 이 잡지만, THE CONNECT 자체가 원자적으로 막아 주는지는 이 리포에서 확인 불가(외부 API). 로컬 hold 는 조직 스코프로만 센다 (`workflow.py:673-675`).

---

## §3-3. DB 모델

### 3-a. 회의 v2 스택 (`back/app/models/meeting_v2.py`)

**`meeting_v2`** (`:50-101`)

| 컬럼 | 타입 | 비고 |
|---|---|---|
| `id` | uuid PK | |
| `host_user_id` | uuid FK `users.id` RESTRICT, **nullable** | legacy — 읽지 않음 (`:54-58`) |
| `host_member_id` | uuid FK `organization_member.id` RESTRICT, NOT NULL | host **정본** (`:60-64`) |
| `title` | text NOT NULL | |
| `scheduled_time` | text NOT NULL | legacy 자유 문자열, 읽지 않음 (`:66-67`, 저장값은 repo `:99`) |
| `scheduled_date` | date NOT NULL | 정본 (`:70`) |
| `scheduled_start` / `scheduled_end` | varchar(5) NOT NULL | `HH:MM` (`:71-72`) |
| `reservation_run_id` | uuid FK `workflow_runs.id` RESTRICT, nullable | **회의 ↔ 예약 유일한 연결 축**, 회의당 최대 1 (`:73-76`, alembic `0118_meeting_v2_reservation_link.py:38-47`) |
| `state` | enum `meeting_v2_state` (waiting/live/paused/ended) | `:77-81` |
| `visibility` | enum `meeting_v2_visibility` (public/private) | `:82-91` |
| `audio_path`, `llm_session_id` | text nullable | |
| `product_tags` | `varchar(32)[]` NOT NULL default `{}` | `:94-98` |
| `deleted_at`, `created_at`, `updated_at` | timestamptz | soft delete |

CHECK 제약 2개 (`back/alembic/versions/0115_meeting_v2_schedule_split.py:167-176`):
- `ck_meeting_v2_scheduled_time_format` — `HH:MM` 형식
- `ck_meeting_v2_scheduled_end_after_start` — `end > start`

**인덱스는 `scheduled_date` 에 없다** — 0115 는 컬럼 3개 + CHECK 2개만 추가한다(`:83-176`, `create_index` 없음).

**`meeting_v2_attendee`** (`:104-121`)

| 컬럼 | 비고 |
|---|---|
| `meeting_id` | uuid FK `meeting_v2.id` RESTRICT, **PK 구성** |
| `organization_member_id` | uuid FK `organization_member.id` RESTRICT, **PK 구성** — 참석자 정본 |
| `user_id` | uuid FK `users.id` nullable — legacy, 읽지 않음 |
| `created_at` | timestamptz |

복합 PK 가 곧 유니크 제약 — 같은 회의에 같은 구성원 2행 불가. 그래서 서비스가 host 를 attendee 에서 뺀다 (`meeting_v2_service.py:226-229`).

그 외 회의 v2 하위: `meeting_v2_transcript`(`:133`), `meeting_v2_summary`(`:167`), 구조화 회의록 7테이블(`:393-659`, `MINUTES_ITEM_MODELS`), 구 4분류(`:662-693`). **회의실과 무관하다.**

### 3-b. 회의실·예약 — **우리 DB 에 테이블이 없다**

`grep -rn "회의실" back/app/models/` → `meeting_v2.py:7` 주석 1건뿐. room/reservation 모델 0개.

방·예약의 실제 저장소:

| 개념 | 원장 | 근거 |
|---|---|---|
| 회의실 카탈로그 (id·name·capacity) | THE CONNECT `GET /api/rooms` | `the_connect.py:223-232` |
| 예약 (누가·언제·어느 방) | THE CONNECT `GET/POST/PUT/DELETE /api/reservations` | `the_connect.py:276-302`, `:314-324`, `:326-363`, `:365-368` |
| 우리 쪽 흔적 ① | `actions` 테이블 (승인 카드) — `type='meeting_room.reserve'`, `payload` JSONB 안에 `{date,start,end,headcount,room:{id,name,capacity,has_monitor},title,attendees,participants}`, `result.external_id` = THE CONNECT 예약 id | `back/app/models/action_runtime.py:331-379`; payload 조립 `surface.py:249-258`; external_id `surface.py:507` |
| 우리 쪽 흔적 ② | `workflow_runs` — run 축. `meeting_v2.reservation_run_id` 가 여기를 가리킨다 | `meeting_v2.py:73-76` |
| 우리 쪽 흔적 ③ | `tdl_sessions` — THE CONNECT 세션 쿠키 캐시 | `the_connect.py:212-220`, `TdlSessionRepository` |

즉 **"어느 방에 예약이 있다" 는 사실은 우리 DB 에 정규화돼 있지 않다.** `actions.payload->'room'->>'name'` 을 긁는 것이 유일한 로컬 경로이고, 실제로 목록 뱃지가 그렇게 한다 (`meeting_v2_service.py:587-623` — `Action.status == DONE` 인 카드의 `payload.room.name`).

### 3-c. "시간대별 누가 어디" 를 지금 스키마로 조회하면

**되는 것**

- 회의 단위: `meeting_v2` 에 `scheduled_date` + `scheduled_start` + `scheduled_end` 가 정규화돼 있으므로 **회의의 시간대 슬라이스는 순수 SQL 로 가능**하다 (`meeting_v2.py:70-72`).
- 참석자: `meeting_v2_attendee` join 으로 "그 회의에 누가" 가 나온다 (`:104-121`).
- 확정 방 이름: `meeting_v2.reservation_run_id` → `subjects.workflow_run_id` → `actions`(type=`meeting_room.reserve`, status=`DONE`) → `payload.room.name`. 일괄 1쿼리 패턴이 이미 있다 (`meeting_v2_service.py:603-618`).

**안 되는 것 / 위험한 것**

1. **`room_id` 로 인덱싱된 로컬 축이 없다.** 방 축 질의(`이 방의 오늘 일정`)는 `actions.payload` JSONB 스캔이거나 THE CONNECT 왕복이다. `held_room_ids` 가 실제로 그렇게 한다 — `Action.payload['date'].astext == payload.date` 로 날짜를 문자열 비교하고 시간 겹침은 파이썬에서 돈다 (`workflow.py:669-687`).
2. **우리 회의가 아닌 예약이 안 보인다.** THE CONNECT 는 우리 앱 밖(사람이 TDL 에서 직접 잡은 예약)도 담고 있고, 그건 우리 DB 어디에도 없다. 완전한 점유 뷰는 **반드시 THE CONNECT 왕복**이 필요하다 (`the_connect.py:276-302`).
3. **예약 없는 회의는 방이 없다.** 기본값이 "예약 안 함" 이라 `reservation_run_id IS NULL` 인 회의가 대부분이고, 그 회의는 스케줄 테이블의 방 칸에 넣을 값이 없다 (`meeting_v2_service.py:597-599` 가 "연결 축이 하나도 없으면 쿼리 자체를 안 돈다" 고 적은 이유).
4. **`scheduled_date` 인덱스가 없다** (0115 확인) — 날짜 범위 조회를 새로 열면 seq scan 이다.
5. **목록 API 는 시간축 조회를 지원하지 않는다** — `updated_at DESC` + limit 100 이 전부고 날짜 파라미터가 없다 (`meeting_v2_repo.py:149-166`, `:168-` `list_all`). 원장 조회 `GET /meetings-v2/ledger/meetings` 는 `since`/`until` 이 있지만 그건 **`created_at`/검색 축**이지 `scheduled_date` 축인지 별도 확인 필요 (`routers/meetings_v2.py:181-200`).
6. **`actions.payload.room.id` 는 THE CONNECT 의 int 이고 우리 FK 가 아니다** — 방이 개명·삭제되면 과거 카드의 이름이 그대로 남는다(스냅샷). 스케줄 뷰가 이 값을 방 식별자로 쓰면 카탈로그와 어긋날 수 있다.

---

## §3-4. 태그와 제품–멤버 연결 ★ 자동 배정의 핵심

### 4-a. 모달 태그는 어디서 오나

칩 목록은 `GET /api/v1/meetings-v2/participants` 가 준다 (`routers/meetings_v2.py:116-129`, leaf 는 회의가 아니라 `directory.basic.read` — `:67`, `:72-74`). 조립부는 `back/app/services/meeting_v2_participants.py:84-170`:

| 칩 kind | id | 출처 |
|---|---|---|
| `all` | `"all"` | 초대 가능한 전 구성원. 저장 태그는 `company` (`:43-47`, `:116-123`) |
| `all` | `"leader"` | C레벨 + `leader` org_role (`:74-81`, `:139-150`) |
| `product` | 제품 slug | **`product_assignment` 원장** (`:124-129`) |
| `org_unit` | `org_unit.id` (str) | 부서 트리 + 하위 전개 (`:151`, `:173-199`) |

저장되는 값(`meeting_v2.product_tags`)은 칩 kind 별로 다르다 — `all`→`company`, `leader`→`leader`, `product`→slug, **부서 칩은 빈 배열** (`front/lib/meeting-participants.ts:213-223`). 검증은 `validate_product_tags` 가 제품 카탈로그 active slug 대조로 한다 (`product_catalog.py:345-360`). 즉 `meeting_v2.product_tags` 는 varchar(32)[] 이고 **FK 가 없다** (`meeting_v2.py:94-98`).

### 4-b. 제품–멤버 매핑 테이블 — **있다**

**`product_assignment`** — 모델 `back/app/models/product_version.py:170-208`, DDL `back/alembic/versions/0054_product_assignment.py:36-53`.

| 컬럼 | 타입 | 비고 |
|---|---|---|
| `id` | uuid PK | |
| `product_slug` | varchar(32) NOT NULL | FK `product.slug` CASCADE (`0054:44-47`). `product` 는 ORM 모델 없음 — alembic 소유 (`product_version.py:176`) |
| `department` | text NOT NULL | SPEC-002 8값 (`:189`) |
| `department_org_unit_id` | uuid FK `org_unit.id` RESTRICT, nullable | 부서 **정본** (`:190-193`) |
| `user_id` | uuid FK `users.id` CASCADE, nullable | legacy — 읽지 않음 (`:180`, `:194-196`) |
| `organization_member_id` | uuid FK `organization_member.id` RESTRICT, **NOT NULL** | **person ref 정본** (`:197-199`) |
| `is_lead` | bool NOT NULL default false | 제품당 1명 대표, 유일성은 alembic 0078 EXCLUDE 제약 (`:181`, `:200`) |
| `valid_from` / `valid_to` | timestamptz / nullable | **기간 축** (`:205-208`) |

유니크: `uq_product_assignment_slug_dept_user (product_slug, department, user_id)` (`0054:51-52`) — ※ legacy `user_id` 축 기준이며, 0090 에서 `organization_member_id` 축으로 재정의된 흔적이 있다 (`0090_assignment_org_cutover.py:38,44`). 스펙 작성 전 정확한 현행 유니크 키는 0090 원문 재확인 권장.

읽는 정본 술어: `OrganizationDirectory.product_assignments_now()` — `back/app/services/organization_directory_provider.py:448-479`. 조건은 `p.organization_id = :org AND p.is_active AND p.kind='product'` + `valid_from <= now < valid_to`. 배치 1쿼리.

### 4-c. 자동 배정이 이 연결을 쓸 수 있나 — **쓸 수 있다. 단, 방을 고르는 데는 직접 못 쓴다.**

- **가능**: `제품 slug → 담당 구성원 목록` 은 이미 양방향으로 나온다 (`meeting_v2_participants.py:98-108` 가 `products_by_member` / `members_by_product` 두 맵을 같은 원장에서 만든다). 회의가 `product_tags=['medi']` 이면 그 제품 담당 인원수를 서버가 알 수 있고, 그게 곧 **정원 판정에 넣을 headcount** 다.
- **불가**: **제품 ↔ 회의실을 잇는 축이 코드·DB 어디에도 없다.** `product_assignment` 는 (제품, 부서, 사람) 3축뿐이고 방 컬럼이 없다. THE CONNECT 방에도 제품/팀 속성이 없다 — 방은 `{id, name, capacity, has_monitor}` 가 전부다 (`the_connect.py:229`, `schemas/meeting_v2.py:139-145`).
- 따라서 자동 배정이 지금 쓸 수 있는 재료는 사실상 **① 시간 ② 인원(정원) ③ 모니터 여부** 셋이고, 제품–멤버 연결은 **② 인원을 자동으로 채우는 데** 기여한다. "제품 X 회의는 항상 3번 방" 같은 선호 규칙을 원하면 **새 매핑 축이 필요하다**(우리 DB 신설 or 방 이름 규약).
- 배정 산식 자체는 이미 있다 — `the_connect._candidates()` 가 정원≥인원 + 모니터 조건으로 거른 뒤 `(capacity, not has_monitor)` 오름차순 정렬해 **가장 작은 적합 방**을 1순위로 준다 (`the_connect.py:384-407`), `plan()` 이 `{room, alternatives[0:3]}` 를 돌려준다 (`:234-250`). 즉 **"자동으로 잡기" 는 `payload.room` 을 비운 채 `plan()` 을 태우는 것**이고, 현행 모달 경로는 사람이 고른 방을 `preferred_room` 으로 심어 그 정렬을 덮는다 (`surface.py:242-245`, `the_connect.py:246-249`).
- 다만 `_candidates` 에는 **정원 무시 fallback** 이 있다 — 정원 만족 빈 방이 없으면 모니터 조건만 맞는 빈 방을 정원 큰 순으로 준다 (`the_connect.py:402-407`). 모달 조회 경로(`room_candidates`)는 이 fallback 을 **일부러 안 탄다** (`surface.py:119-121`). 자동 배정이 `plan()` 을 그대로 쓰면 이 fallback 이 살아나 **정원 초과 방이 조용히 배정된다.**

---

## §3-5. 참석자 저장 · 정원 검증

### 5-a. 저장

- FE: `buildRoster(roster, organizationMemberId)` 가 host 포함 명단을 만들고(`MtgV2CreateModal.tsx:124-127`), 제출 시 **host 를 빼서** 보낸다 (`:269-271`).
- BE: 중복 제거 + host 제외를 **한 번 더** 한다 (`meeting_v2_service.py:226-229`) — PK 충돌 방지.
- 검증: `_assert_invitable()` 이 `invitable_member_ids` 집합과 대조해 하나라도 밖이면 `422 NOT_INVITABLE` + `error.members` 배열 (`meeting_v2_service.py:259-272`, `errors.py:812-833`). 초대 가능 = 조직 활성 구성원 **AND `user_id IS NOT NULL`(계정 연결)** (`meeting_v2_participants.py:52-58`, `:61-71`).
- INSERT: `meeting_v2_attendee` N행 (`meeting_v2_repo.py:108-112`). **HOST 는 별도 행이 아니다** — `meeting_v2.host_member_id` 컬럼 하나로 표현된다 (`meeting_v2.py:60-64`). 응답 `attendees` 배열에도 host 는 없고 `host_user_id`/`host_name` 이 따로 나간다 (`meeting_v2_service.py:931-943`).

### 5-b. 참석자 수 ↔ 회의실 정원 검증

**있다. 3중이다.** 다만 전부 "정원 미달 방을 후보에서 뺀다" 이지 "참석자를 더 넣으면 막는다" 가 아니다.

1. 후보 조회 — `room.capacity >= headcount` (`surface.py:149`)
2. 실행 직전 재검증 — 후보 밖이면 `stale`, 카탈로그엔 있으나 정원 미달이면 역시 `stale` (`surface.py:198-207`)
3. 접수 시 바닥 올림 — `payload.headcount = max(headcount, len(participants))` (`workflow.py:250-262`)

**빈 구멍**: 회의 생성 후 참석자를 늘리는 경로에서 방 정원 재검증이 도는지는 확인 못 했다(이번 조사 범위 밖 — 참석자 수정 API 자체를 v2 에서 못 찾음). 그리고 **`headcount` 는 `meeting_v2` 에 저장되지 않는다** — `actions.payload.headcount` 에만 있다.

### 5-c. ⚠ 참석자 축이 두 벌이다

회의 참석자는 `organization_member.id` 인데, THE CONNECT 예약 참석자는 **이메일**이다. 이어 붙이는 방식이 이렇다:

1. `_attendee_names()` — 참석자 `organization_member.display_name` **문자열 배열**을 만든다 (`meeting_v2_service.py:482-498`)
2. `resolve_attendees()` — 그 이름 문자열을 THE CONNECT `members()` 디렉터리 + 사내 `org_members` 와 **이름 매칭**해 이메일로 해소한다 (`workflow.py:566-599`, gateway 디렉터리는 `surface.py:262`)
3. 미매칭은 조용히 버리지 않고 `payload.unmatched` 로 남아 카드에 "초대 제외" 로 표기된다 (`workflow.py:575`)

즉 **id 축이 아니라 이름 문자열 축으로 외부에 넘어간다.** 동명이인·THE CONNECT 미가입자는 여기서 새고, 그 사실이 모달에는 안 보인다(카드가 인박스에 안 뜨므로 — `meeting_v2_service.py:322-324`).

---

## §3-6. 기존 스케줄/점유 뷰

### 6-a. BE — 있다 (3종, 단 소비자가 다르다)

`back/app/routers/action_runtime_v2.py:1261-1330`, leaf 는 `action.runtime.basic`:

| 엔드포인트 | 하는 일 | 근거 |
|---|---|---|
| `GET /api/v1/action-runtime/rooms` | 정적 카탈로그 `[{id,name,capacity,has_monitor}]` | `:1269-1273` → `read_surface.room_catalog` (`read_surface.py:70-73`) |
| `GET /api/v1/action-runtime/rooms/status` | **점유/가용 뷰 또는 일정 상세 뷰** | `:1276-1311` → `read_surface.room_status` (`:75-82`) → `tools/room.py:224-235` |
| `POST /api/v1/action-runtime/rooms/plan` | 예약안 → `{room, alternatives}` (조회 전용) | `:1314-1327` |

`/rooms/status` 가 §2 의 "스케줄 테이블" 에 **가장 가깝다**:

- `include_reservation_details=false` → **가용성 뷰** `{kind:"availability", rooms, available_rooms, occupied_rooms:[{room, reservation:{start,end}}]}` — 제목·참석자 없음 (`tools/room.py:136-159`)
- `include_reservation_details=true` → **일정 상세 뷰** `{kind:"schedule", reservations:[ReservationSummary], attendees_by_reservation, attendee_records_by_reservation}` — 제목·참석자 이름/이메일 포함 (`tools/room.py:161-221`)
- `attendee` 파라미터로 그 사람 건만 좁힐 수 있고, 못 찾으면 빈 목록이 아니라 `attendee_unresolved` 표시 (`tools/room.py:198-204`)
- 입력 축: `date` **하루치** + `start`/`end` 구간 (또는 `start==end` 점시각) + 선택적 `room_id`(1~7) (`tools/room.py:59-71`, 겹침 판정 `:128-134`)

**한계**

1. **날짜 1일 단위**다 — 주간 그리드를 그리려면 7회 호출이고, 매 호출이 THE CONNECT 왕복 2~3회(`rooms()` + `list_reservations()`)다 (`the_connect.py:252-274`).
2. **leaf 가 `action.runtime.basic`** — 회의 leaf 로 열려면 새 표면이 필요하다(모달 후보 조회를 신설한 것과 같은 사유 — `surface.py:127-138` 이 §6.2a 재사용을 검토하고 기각한 기록).
3. **로컬 hold 를 반영하지 않는다** — `room_candidates` 만 hold 를 뺀다 (`surface.py:122-124`, `:146`). 그래서 status 뷰가 "비었다" 고 한 방을 모달은 후보에서 뺄 수 있다(두 뷰가 다른 답을 낸다).
4. **우리 회의(`meeting_v2`)와 조인되지 않는다** — THE CONNECT 예약 제목/참석자만 보인다. "이 시간에 어느 회의(우리 회의 id)가 어느 방에" 를 잇는 것은 `meeting_v2.reservation_run_id → actions.result.external_id` 를 THE CONNECT 예약 id 와 대조해야 성립한다. **그 조인을 하는 코드는 없다.**

### 6-b. FE — 없다

- `front/components` · `front/app` 에 calendar / schedule 디렉터리·컴포넌트 0건 (`ls`/`find` 결과 무).
- `/rooms/status` 를 부르는 FE 코드 0건 (`grep -rn "rooms/status" front/` 무결과). **BE 3종은 MCP/에이전트 툴 전용이다.**
- 지금 화면에 보이는 회의실 정보는 두 군데뿐:
  - 목록 행 뱃지 — `room_name` 하나 (`front/components/meeting-v2/MtgV2List.tsx:111-115`, 서버 `meeting_v2_service.py:587-623`)
  - 상세 메타바 — `확정 (방이름)` (`front/components/meeting-v2/MtgV2MetaBar.tsx:290`)
- 즉 **시간대 × 회의실 그리드 화면은 존재하지 않는다.** 신설이다.

### 6-c. 회의 목록 조회는 시간축이 아니다

`GET /meetings-v2` 는 `updated_at DESC` + limit 100 이 전부다 (`meeting_v2_repo.py:149-166`). 날짜/기간 파라미터가 없다. 원장 조회 `GET /meetings-v2/ledger/meetings` 에 `since`/`until` 이 있지만 검색·필터 축이라 `scheduled_date` 슬라이스인지 확인 필요 (`routers/meetings_v2.py:181-200`).

---

## 스펙 작성 전에 정해야 할 것 (열린 질문 · 리스크)

**A. 스케줄 뷰의 데이터 원천 — 이게 1번 결정이다**

1. **점유 뷰의 정본을 THE CONNECT 로 할 것인가, 우리 DB 로 할 것인가.** THE CONNECT 를 읽으면 앱 밖 예약까지 다 보이지만 날짜당 왕복 2~3회이고 장애가 곧 화면 장애다. 우리 DB(`meeting_v2` + `actions.payload`)만 읽으면 빠르지만 **앱 밖 예약이 안 보이고 예약 안 한 회의는 방 칸이 빈다.**
2. **회의 ↔ 예약 조인이 지금 없다.** `meeting_v2.reservation_run_id → actions.result.external_id ↔ THE CONNECT 예약 id` 를 잇는 코드가 없다. 스케줄 테이블이 "이 시간 이 방 = 이 회의" 를 말하려면 이 조인을 누가 어디서 하는지 정해야 한다.
3. **방 축 로컬 캐시/투영 테이블을 만들 것인가.** 지금은 `actions.payload` JSONB 스캔이 유일한 방 축 질의다(`workflow.py:669-687` 이 실제로 그렇게 한다). 주간 그리드를 이걸로 그리면 성능이 안 나온다.
4. `meeting_v2.scheduled_date` 에 **인덱스가 없다** — 날짜 범위 조회를 열면 추가 필요.
5. 두 점유 산식이 답이 다르다 — `/rooms/status` 는 hold 를 안 빼고 `room_candidates` 는 뺀다. 스케줄 뷰가 어느 쪽을 보여줄지 정해야 한다("예약 확정" vs "잡혀 있음" 을 구분해 둘 다 보이는 것이 아마 맞다).

**B. 자동 배정**

6. **제품 ↔ 회의실 매핑 축이 없다.** `product_assignment` 는 (제품, 부서, 사람)뿐이고 방에는 제품 속성이 없다. "제품–멤버 연결을 활용해 방을 자동으로" 를 문자 그대로 하면 실제로 쓰이는 것은 **인원수(정원)** 뿐이다. 그 이상(제품별 선호 방)을 원하면 새 축 신설이 필요하고, 그건 이번 발주 범위인지 확인이 필요하다.
7. **정원 무시 fallback 을 자동 배정이 탈 것인가.** `the_connect._candidates` 는 적합 방이 없으면 정원 초과 방을 준다(`:402-407`). 모달 조회는 일부러 안 탄다. 자동 배정이 `plan()` 을 그대로 쓰면 **정원 초과 방이 조용히 잡힌다.**
8. **"예약 안 함" 기본값을 없앨 것인가.** 지금은 기본이 미예약이라 대부분의 회의에 방이 없다(`MtgV2CreateModal.tsx:576-580`). 자동 배정이 기본이 되면 THE CONNECT 장애 시 **회의 생성 자체가 막힌다** — 현행 계약은 all-or-nothing 이라 예약 실패 = 회의 미생성이다(`meeting_v2_service.py:206-257`). 이때 폴백(방 없이 만들기)을 허용할지 정해야 한다.
9. `has_monitor` 가 **`room.id != 1` 하드코딩**이다 (`the_connect.py:229`). 자동 배정 규칙이 장비를 보면 이 값을 신뢰할 수 있는지 확인 필요.
10. `monitor=False` 가 모달 경로에 **하드코딩**돼 있다 (`meeting_v2_service.py:357`) — 자동 배정이 모니터를 요구하려면 입력 축이 없다.

**C. 현행 코드에서 발견한 리스크 (개선안 아님, 사실 기록)**

11. **고아 예약 창**: 생성 경로에 커밋이 3회 있다(`:383`, `:392`, `:253`). ③ 성공 후 ④ 실패/크래시면 THE CONNECT 예약은 남고 회의는 없다. 보상 경로 없음.
12. **참석자가 이름 문자열로 외부에 넘어간다** (`meeting_v2_service.py:482-498` → `workflow.py:566-599`). 동명이인·THE CONNECT 미가입자는 조용히 `unmatched` 로 빠지고, 모달 발 예약은 카드를 인박스에 안 띄우므로 **사용자가 초대 누락을 알 방법이 없다.**
13. **로컬 hold 는 우리 조직 원장만 센다** (`workflow.py:673-675`). 멀티테넌트에서 다른 조직이 같은 THE CONNECT 방을 쓰면 hold 가 서로 안 보인다 — 마지막 방어는 외부 재검증 하나다.
14. `uq_product_assignment_slug_dept_user` 의 현행 축(legacy `user_id` vs `organization_member_id`)이 0054 와 0090 에서 갈린다. 자동 배정이 이 테이블을 키로 쓰면 정확한 현행 제약을 0090 원문에서 확인해야 한다.
15. `actions.payload.room.id` 는 THE CONNECT 의 int 이고 FK 가 아니다 — 방 개명·폐지 시 과거 카드 이름이 스냅샷으로 남는다. 스케줄 뷰가 이걸 방 식별자로 쓰면 카탈로그와 어긋난다.

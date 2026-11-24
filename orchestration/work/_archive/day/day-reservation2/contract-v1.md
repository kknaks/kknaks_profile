# day-reservation2 1판 — BE ↔ FE 계약 v1 (화면 라우트 ↔ 서비스 · SSE · 화면 값)

> frontend 워커가 먼저 적음(2026-11-24). 원천 = delivery-1-report 계약 W · S · V · SPEC-007 §3. 이름은 제안 — backend 가
> 다르게 만들었으면 **이 파일을 고치고** frontend 에 알린다(한쪽만 바꾸지 않는다).
> 소유: 화면 라우트 `backend/day/routers/reservation_detail.py`(새) · 템플릿 · day.js = frontend /
> 아래 `services/*` · `policies/permissions.py` 상수 · 스트림 라우트 = backend.

## 0. 권한 상수 (backend · `day/policies/permissions.py`)

- `DETAIL_KEY = "reservation.detail"` — 화면 라우트가 쓰기마다 `sessions.require_permission(..., DETAIL_KEY, EDIT)`.
  보기(모달 · 창 · 고객 찾기) = `RESERVATION_KEY` view. 동행 저장 = `COMPANION_KEY` edit.

## 1. 서비스 함수 (backend 가 만든다 · 라우트가 부른다)

모두 `async` · 인자 `(session: AsyncSession, current: CurrentSessionData, ..., now: datetime)` · 돌려주는 값은
**템플릿 값 dict**(아래 §3 이름 그대로 · dict/list/str/int/bool/None 만) · 오류 = 기존 도메인 예외(ServiceError 계열 —
`web_errors` 가 HX 응답 `X-Day-Error` 공용 토스트로 그림). 문구는 서비스가 만들지 않는다(화면 몫).

### `day.services.reservation_detail` (읽기 — DB 사본만 · KOS 안 부름)

| 함수 | 인자(문자열은 화면이 받은 그대로) | 돌려줌 | 오류 |
|---|---|---|---|
| `detail_view` | `visit_id: str` | `{"detail": D}` | 404 없는 방문 · 다른 병원 |
| `book_view` | `date: str, group_id: str, start: str` (빈 값 허용) | `{"book": B}` (mode `"new"`) | 400 형식 · 409 `reservation_past_date` |
| `edit_view` | `visit_id: str` | `{"book": B}` (mode `"edit"`) | 404 · 409 `visit_stage_changed` · `reservation_past_date` |
| `customer_search` | `q: str` | `{"search": S}` | — |

### `day.services.reservation_writes` (쓰기 — 쓰기 큐에 넣음까지 · 결과는 SSE)

| 함수 | 인자 | 돌려줌 |
|---|---|---|
| `book` | `form: Mapping[str, str]` (POST /reservations 칸 그대로 — §2) | `Q`(kind `"queued"`) 또는 `{"kind": "duplicate", "duplicate_token": str, "customer": C}` |
| `change_schedule` | `visit_id: str, form: Mapping[str, str]` (`date` · `start` · `group_id` · `doctor_id` — 옮기기는 `start` · `group_id` 만) | `Q` |
| `cancel` | `visit_id: str` | `Q` |
| `set_doctor` | `visit_id: str, doctor_id: str` (빈 값 = 지정 안 함) | `Q` |
| `save_companions` | `visit_id: str, mate_visit_ids: list[str]` (빈 목록 = 풀기) | `{"date": date, "count": int}` (count = 저장 뒤 묶음 인원 · 0 = 풀림) |
| `retry` | `visit_id: str \| None, write_id: str \| None` | `Q` |

`Q`(쓰기 큐에 넣음) = `{"kind": "queued", "write_id": str, "visit_id": str | None, "action": str, "customer_name": str,
"group_title": str | None, "start": "HH:MM" | None, "doctor_name": str | None, "new_customer": bool}`
- `write_id` = 이 버튼의 순서 묶음 id(쓰기 큐 행 · 다시 시도도 같은 값) — SSE `write_confirmed` · `kos_failed` 가 같은 값을 싣는다.
- `action` ∈ `reserve` · `schedule` · `move` · `cancel` · `doctor` (1판).
- 새 예약은 `visit_id = None`(KOS id 전 DAY 행 없음 — Rule 2).

## 2. 화면 라우트 (frontend · `routers/reservation_detail.py`)

| 경로 | 응답 |
|---|---|
| `GET /reservations/visits/{visit_id}` | `partials/reservations_detail.html` (`<dialog>` → `#modal-root`) |
| `GET /reservations/book?date&group_id&start` | `partials/reservations_book.html` (→ `#reservation-float`) |
| `GET /reservations/visits/{visit_id}/edit` | 같은 창 · mode edit |
| `GET /reservations/customers?q` | `partials/reservations_book_who.html` (목록 조각) |
| `POST /reservations` | queued → 창 다시(잠김 · `data-day-res-wait=write_id`) / duplicate → RB-11 창 조각 |
| `PUT /reservations/visits/{id}/schedule` | 창(edit) 또는 옮기기 — 잠김 조각 / 옮기기는 `HX-Reswap: none` + 대기 표시 |
| `POST /reservations/visits/{id}/cancel` | 모달 잠김 조각(또는 우클릭 = 빈 응답 + 대기) |
| `PUT /reservations/visits/{id}/doctor` | 모달 잠김 조각 |
| `PUT /reservations/companions/group` | 모달 조각 + `#reservation-main` oob 없음(→ SSE `reservation`) + `HX-Trigger` 알림 |
| `POST /reservations/visits/{id}/retry` · `POST /reservations/retry`(form `write_id` — 새 예약 실패) | 빈 응답 · 결과는 SSE |

POST /reservations 칸(SPEC-007 §3 그대로): `customer_id` · `name` · `phonetic_name` · `dial`(국가번호 숫자 · 예 `82`) ·
`phone` · `sns_type`(SnsType 값) · `sns_id` · `birth_date`(`YYYY.MM.DD` 화면 입력 그대로 — 서버가 바꿈) · `nationality`(ISO 2자 ·
빈 값 = 선택 안 함) · `gender`(`FEMALE` · `MALE` · 빈 값) · `date`(YYYY-MM-DD) · `start`(HH:MM) · `group_id` · `funnel_id` ·
`doctor_id` · `memo` · `duplicate_token`.

## 3. 화면 값 (계약 V — 1판)

### 표 값 보탬 (`reservations.board_view` 최상위 · backend)
- `detail_editable: bool` — 보는 날짜가 오늘 · 앞날 ∧ `reservation.detail` edit. 화면: 빈 칸 누르기 = 등록 창(`data-day-res-bookable`) ·
  우클릭 「예약 변경」 · 「예약 취소」 켜짐(그 카드 state = reserved 일 때). 「동행 추가」 = 기존 `companion_editable` ∧ 취소 · 노쇼 아님.
- 화면 라우트는 쓰기 응답에 본문을 싣지 않는다(`HX-Reswap: none` + `HX-Trigger: day:res-queued`) — 서비스 `Q` 값만 쓴다.
- 새 오류 코드(`reservation_past_date` · `visit_stage_changed` · `visit_not_today` · `duplicate_expired` · `kos_unavailable`)는
  `web_errors.handlers()` 에 `board_error_handler` 로 등록하고 글자는 `UNSET_MESSAGES`(빈 문구 · OQ-D17) — backend.

### D (예약 상세 · `detail`)
```
visit_id: str
stage: reserved|reception|consultation_waiting|consultation|procedure_waiting|procedure|procedure_done|completed|canceled|no_show
date_kind: today|future|past
is_new: bool|None                       # None = 배지 · 이전 방문 없음
pending: {"write_id": str, "action": str}|None   # 결과 전 쓰기 — 버튼 잠금
editable: {                              # 서버 판정(경계 표 · 권한 reservation.detail · 동행 = reservation.companion)
  change: bool,    # [예약 변경] · 우클릭 예약 변경
  cancel: bool,    # [예약 취소] · 우클릭 예약 취소
  doctor: bool,    # 의사 지정 고르기(오늘 ∧ 예약 · 접수 ∧ 권한)
  companion: bool, # 동행 [수정] · + 동행 추가
  identity: bool,  # 1판 = 늘 false(신분증 체크 2판) — 자리만
  qr: bool,        # [문진 QR] 보임(비활성) — D55 시안 조건
  scan: bool,      # [여권 스캔] 보임(비활성)
}
customer: {name: str, passport_name: str|None, contact: str|None, birth: "YYYY.MM.DD"|None, age: int|None,
           gender: "FEMALE"|"MALE"|None, nationality: str|None (보이는 글자 — 카드 국가 글자 규칙과 같은 값),
           is_domestic: bool|None (None = 국적 빔), notes: str|None}
reservation: {assignee: str|None, date: "YYYY.MM.DD", start: "HH:MM", end: "HH:MM", funnel: str|None, memo: str|None,
              doctor: {"id": str, "name": str}|None,
              companions: [{"visit_id": str, "name": str}],
              candidates: [{"visit_id": str, "name": str, "nationality": str|None, "group_id": str|None (동행 그룹), "checked": bool}]}
doctors: [{"id": str, "name": str}]        # 직무 doctor (의사 지정 목록)
previous_visits: [{"date": "YYYY.MM.DD", "assignee": str|None, "counselor": str|None, "consult_doctor": str|None,
                   "procedure_doctor": str|None, "treatments": [str]}]
```
1판 빈 값: 신분확인 · 초진 문진 · 건강정보 줄 = 값 비움 · 상담 정보 칸 = 1판에 그리지 않음(2판) · 오른쪽(시술 목록 · 수납) = 칸 자리만(3판).

### B (예약 등록 / 변경 창 · `book`)
```
mode: new|edit, visit_id: str|None
assignee: str                     # 로그인 직원 이름(보기만)
today: "YYYY-MM-DD", date: "YYYY-MM-DD"|None, start: "HH:MM"|None, group_id: str|None
groups: [{"id": str, "title": str, "slots": [{"start": "HH:MM", "label": "HH:MM - HH:MM"}]}]   # 그룹 간격 칸
funnels: [{"id": str, "name": str}], funnel_id: str|None, funnel_name: str|None (edit 보기만)
doctors: [{"id": str, "name": str}], doctor_id: str|None
memo: str
customer: C|None                  # edit 이면 그 고객(고객 변경 없음)
nationalities: [{"code": str, "name": str}]   # 국적 목록(「선택」 · 「대한민국」은 화면이 앞에 붙이지 않음 — 목록 첫 줄 KR 포함)
dials: [{"code": "82", "label": "+82 대한민국"}]
```
C(고객 카드) = `{"customer_id": str, "chart_no": str|None, "name": str, "local": str|None, "nationality": str|None,
"contact": str|None, "birth": str|None, "gender": "FEMALE"|"MALE"|None, "notes": str|None}` — duplicate 의 C 는
`customer_id` 대신 비움(KOS id 를 브라우저로 안 보냄 · 토큰만).

### S (고객 찾기 · `search`)
`{"q": str, "recent": bool, "items": [C], "can_new": bool}` — `can_new` = 글자에 숫자 · 기호 아닌 글자가 있음(시안 정규식 `[^\d\s+.\-]`).

## 4. SSE (계약 S · backend 스트림 라우트 `GET /reservations/stream`)

- `reservation` — data = version 숫자(없으면 빈 값 = 늘 다시 받기). 화면: 보는 날짜 `#reservation-main` 다시 받기(`poll=1`).
- `write_confirmed` — data = JSON `{"visitId": str|null, "writeId": str, "action": str}`(새 예약은 확인 뒤 생긴 visitId).
  화면: 그 writeId 를 기다리는 창 · 모달 잠금 풂 · 다시 받기 · 성공 알림(문구 = 화면이 응답 때 받아 둔 것).
- `kos_failed` — data = HTML 조각 = **`partials/reservations_toast_kos_failed.html`**(frontend 템플릿) 을 backend 가
  값 `customer_name` · `message`(공용 문구 `KOS_FAILED_MESSAGE`) · `visit_id`(str|None) · `write_id`(str) 로 렌더.
  조각에 `data-day-res-failed="{write_id}"` · 「다시 시도」(retry 경로) 가 들어 있다 — 화면이 그 writeId 잠금을 푼다.
- `session_expired` · `retry: 3000` · 15초 `: ping` — 시술 현황과 같음.
- 10초 폴링(`[data-day-res-poll]` 시계)은 없앤다 — 같은 요소는 SSE `reservation` 의 다시 받기 source 로만 남긴다.

## 5. backend 확인 (2026-11-24 · backend 워커)

- §0 · §1 · §3 · §4 이름 그대로 구현함 — `services/reservation_detail.py`(detail_view · book_view(`date` 키워드) · edit_view ·
  customer_search) · `services/reservation_writes.py`(book · change_schedule · cancel · set_doctor · save_companions · retry) ·
  `policies/permissions.DETAIL_KEY` · `reservations.board_view` 최상위 `detail_editable`.
- `write_id` = 그 버튼의 `event_log.id`(쓰기 큐 행들의 `event_id`). 새 예약 Q 의 `visit_id` = None — 확인 뒤
  SSE `write_confirmed.visitId` = 미리 정한 DAY 방문 id(그 id 로 사본이 생김).
- change_schedule: form 에 `date` 키가 **없으면 옮기기**(같은 날 · 길이 그대로 · action `move`) · 있으면 창(action
  `schedule` · 끝 = 시작 + 그룹 간격). `doctor_id` 키가 없으면 의사 그대로 · 빈 값 = 지정 안 함. 옮기면 동행에서 빠짐(U-11).
- save_companions: 판 신호(SSE `reservation`)는 서비스가 보냄 · 응답 `{"date": date, "count": int}`.
- 오류: `reservation_past_date` · `visit_stage_changed` · `duplicate_expired` · `no_failed_write`(다시 시도할 실패 없음 · 409)
  → `web_errors.handlers()` 에 board_error_handler · `UNSET_MESSAGES` 등록함. `visit_not_today` 는 UNSET 에만(1판에 던지는 곳 없음).
  `kos_unavailable`(503 · W1 실패)은 전역 등록 안 함(로그인 화면 처리와 겹침) — 라우트에서 공지처럼 `notice_error_handler` 로
  받거나 그대로 두면 공용 처리.
- 같은 방문에 결과 전 화면 쓰기가 있으면 쓰기 409 `visit_stage_changed`(서버도 잠금).
- SSE `kos_failed` 조각 값 = `customer_name` · `message` · `visit_id`(쓰기 큐 방문 id — 새 예약은 아직 사본 없음 · retry 에 그대로 써도 됨) · `write_id`.
- 끌어 묶기 서버 입구 정리: `reservation_companions.join` 삭제 · `leave` 는 옮기기가 씀(남김).
- **이름 바뀜(구조 검사 `identifiers.py` — `*_id: str` 인자 금지)**: 서비스 인자 이름만 바뀌었다 · 위치 인자는 그대로.
  `book_view(session, current, date=…, group_text=…, start=…, now=…)` — **`group_id=` 키워드 → `group_text=`** 로 고쳐 주세요
  (routers/reservation_detail.py:177). 나머지(detail_view · edit_view · change_schedule · cancel · set_doctor ·
  save_companions · retry)는 위치 인자로 부르면 바뀐 것 없음(`visit_text` · `mate_texts`).
- `book` 은 `services/reservation_book.py` 에 있고 `reservation_writes.book` 으로도 그대로 부를 수 있다.

## 6. 마무리 — B1 ~ B10 + 2 · 3 · 4판 (frontend 가 먼저 적음 · 2026-11-24 18:00)

> backend 가 다르게 만들면 이 절을 고치고 알린다. 템플릿은 아래 키가 **없어도** 깨지지 않게(빈 값 · 「미확인」 등) 그린다.

### 6-1. D 보탬 · 바뀜 (`detail_view` — **backend 이름 그대로 맞춤** · `services/reservation_detail_care.py` · `policies/reservation_detail.Editable` · `policies/reservation_treatments`)
- `is_new` — **KOS 값 그대로**(코디 정정 · D7 유지): 상세 = `visit.is_new` · 고객 카드 C(등록 창 · 미리보기) = `customer.is_new`(C 에 `is_new` 키 **새로 실음** — B9 원인 = C 에 키가 없어 화면이 「초진」으로 떨어짐). null = 배지 없음. 재진(false)이면 이전 방문 기록.
- `customer.nationality` = **이름**(B3) · `customer.contact` = **대시 꼴**(B4). 화면: 외국인 「{국적} / 통역필요」 · 내국인 국적 이름(시안 L2172 · B8 ⑨).
  고객 카드 C(등록 창 목록 · 같은 고객 창)에도 같은 꼴 + 선택 `is_new`(있으면 미리보기 카드 초진 배지 판정 — B7 · B9).
- `identity: {"confirmed": bool}` · `procedure_info: bool`(접수 뒤 제목 「시술 정보」 — OQ-D04) · `discharge_reason: str|None`
- `consult: {"counselor": {"id","name"}|None, "room": {"id","name"}|None, "counselors": [{"id","name"}], "rooms": [{"id","name"}], "order_memo": str|None}`
- `treatments: [{"id", "title", "indent": bool, "header": bool, "today": bool, "state": "doing"|"before"|"after"|"idle"|None, "rounds": "n/m"|None, "pickable": bool}]`(평평한 줄 · 머리 줄이 묶음을 엶)
- `payment: {"product_total": int|None, "discount": int|None, "total", "received", "unpaid": int, "warn": bool, "settled": bool, "button": "paying"|"pay"|None}`
- `links: {"purchase": str|None, "prescription": str|None}`(딥링크 · 없으면 버튼 꺼짐)
- `editable` 보탬: `reception` · `procedure_only` · `consult_pick` · `consult_live` · `today_check` · `send_waiting` · `order_memo` · `discharge` · `prescription` · `payment_button`.
- 화면 글자: state doing 「시술 중」 · before 「시술 전」 · after 「시술 후」 · idle 「미진행」 · rounds → 「n/m회」.

### 6-2. 쓰기 서비스 (`reservation_writes` · 모두 Q 반환 — 신분증만 dict)

> frontend 라우트는 **`reservation_writes.<위 표 이름>`** 으로 부른다(backend 가 `reservation_care_writes` 에 만들고 `reservation_writes` 로 다시 내보냄 — 이름은 표 그대로 `set_counselor` · `set_room` · `set_order_memo` · `procedure_waiting`).
| 함수 | 인자 | action · 알림(화면) |
|---|---|---|
| `reception` | `visit_text` | `reception` · 「접수했어요」 |
| `set_identity` | `visit_text, checked: bool` | DAY 만 · 돌려주는 값 무시 → 라우트가 `detail_view` 로 모달 다시 그림 |
| `consultation_waiting` | `visit_text, form{counselor_id, room_id}` | `consultation_waiting` · 「접수했어요 · 상담 대기」 |
| `set_counselor` | `visit_text, counselor_id: str` | `counselor` · 「{counselor_name} 상담실장으로 바꿨어요」(Q 에 `counselor_name`) |
| `set_room` | `visit_text, room_id: str` | `room` · 「관리실을 {room_name}로 바꿨어요」(Q 에 `room_name`) |
| `procedure_waiting` | `visit_text, form{room_id, order_memo}, line_ids: list[str]` | `procedure_waiting` · 「접수했어요 · 시술 대기」 |
| `set_order_memo` | `visit_text, memo: str` | `order_memo` · 「오더 메모를 저장했어요」 |
| `discharge` | `visit_text, reason: str` | `discharge` · 「귀가 처리했어요」 |

- 경로 = POST …/reception · PUT …/identity(`checked`) · POST …/consultation-waiting · PUT …/counselor · PUT …/room · POST …/procedure-waiting(`room_id` · `order_memo` · `line_ids` 여러 개) · PUT …/order-memo(`order_memo`) · POST …/discharge(`reason`) — **화면 라우트는 위 함수 이름 · 위치 인자로 부른다**(frontend 가 `routers/reservation_detail.py` 에 이미 씀 · 모두 `(session, current, visit_text, …, now)`).


### 6-3. backend 확인 (2026-11-24 · backend 워커)
- 6-1 키 이름 그대로 구현 · 더한 것: `customer.nationality_code`(ISO 원값 · C 에도) · `payment.payment_required`(R42 원천). `payment.warn` = **시안 그대로 귀가 대기 · 귀가에서만**(사용자 「시안 그대로」).
- 「통역필요」: DAY · KOS 사본에 통역 원천 칸이 없다 — 서버 값 없음(화면이 시안대로 외국인에 붙이면 그것이 정함).
- 6-2 함수 이름 그대로 `reservation_writes` 에 있다(실제 몸 = `services/reservation_care_writes.py`). `change_counselor` · `change_room` · `save_order_memo` 도 같은 함수(별칭).
- `set_counselor` Q 에 `counselor_name` · `set_room` Q 에 `room_name` · `discharge` Q 에 `counselor_name`.
- 새 오류: `visit_not_today`(409 · `VisitNotToday`) · `reception_missing`(400 · `ReceptionMissing` · field = identity · counselor_id · room_id · line_ids) — `web_errors` 등록 · UNSET 문구.
- **`procedure_waiting` = 검사(오늘 · 접수 · 신분확인 · line_ids · 관리실)까지만 · 그 뒤 400 `invalid_request`(W13 미개방)** — pending.

### 6-4. 고침 화면 확인 1 (frontend 가 먼저 적음 · B15 · B18)
- B15 `consult.rooms[]` = `{"id", "name", "empty": bool}` — 빈 방 먼저(서버 정렬) · `empty` = 지금 그 방에 있는 오늘 방문 0. 화면: 목록 줄 오른쪽에 「비어 있음」(시안 목록 배지 모양).
- B18 시술권 없는 오늘 작업(수납 필요) = `treatments[]` 같은 줄 모양(`header` 옵션 줄 → `indent` 시술 줄 · `today` · `state`) — 화면은 그대로 그린다(새 키 없음).
- B20 관리실 쓰기 실패 = 기존 공용 오류 토스트(HX 오류 응답) — 화면은 고른 값을 되돌리고 토스트.


### 6-4. 고침 화면 확인 1 (backend · 2026-11-24)
- B15 `consult.rooms[]` = `{"id", "name", "empty": bool}` — `empty` = 그 방에 지금 있는 오늘 방문 0(빈 방 먼저 정렬은 그대로) · 화면이 「비어 있음」.
- B18 `treatments[]` 끝에 **구매 · 시술권 없는 오늘 시술**(수납 필요 등) 줄: 옵션 머리 `id = "option:<옵션>"`(header) + 시술 줄 `id = "task:<visit_task id>"`(indent · today true · state) · 옵션에 작업 하나 · 같은 이름이면 한 줄(`task:`). `pickable` = false.
- B19 `payment.product_total` = 할인 전 합 + 수납 필요 옵션가(+VAT · R50 ⓑ) — `product_total − discount = total`.
- B14 `previous_visits` = 이번 방문 시작보다 앞선 방문 전부(오늘 앞서 귀가한 방문 포함 · 취소 · 노쇼 뺌 · 최신 순).
- B20 `set_room`(PUT …/room): 「방 배정」 작업이 없으면 만들고(W8 → W9 연쇄) 방 지정 · 실패 = 400 `invalid_request`(공용 토스트 · 설정 없음 등) / 409.

### 6-5. 고침 화면 확인 2 (frontend 가 먼저 적음 · B23 ~ B33)
- B29 `editable.today_check` = 쓰기 ∧ 오늘 ∧ 단계 **예약 · 접수**(지금 접수만 → 예약도) — 화면: 「시술만 진행」 켬일 때만 「오늘」 체크가 켜짐(day.js).
- B24 · B26 · B27 `consult.rooms[]` = `{"id", "name", "empty": bool}` 그대로 · **목록 = 그 방문 접수 구역 방만(「미사용」 뺌)** · 순서 = 빈 방 먼저 → 사용 중 · 각 묶음 안 = 시술 현황 방 순서(`room.order`). 화면 = 시술 현황 방 고르기 부품(`day-opt` · 오른쪽 끝 파란 「비어 있음」 / 「배정됨」).
- B30 오더 메모 = 오른쪽 시술 목록 아래 · 예약 · 접수 ∧ 시술만 ∧ 「오늘」 ✓ 있을 때만 글 칸 · 시술 대기부터 안 그림(`consult.order_memo` 는 그대로 둬도 됨 · 화면이 안 씀).
- B33 `treatments[]` 줄 모양 그대로(header 머리 = 옵션 이름 · indent 구성 시술 · rounds `n/m` · today · state · pickable) — 화면은 받은 순서대로 그린다.


### 6-5. 고침 화면 확인 2 (backend · 2026-11-24)
- **B33 `treatments[]` 모양(B18 · B31 · B32 를 대신함)** — 평평한 줄 목록 · 묶음마다 `header: true` 머리 줄 1개 + 아래 `indent: true` 줄들.
  - 시술권 묶음: 머리 `id = 묶음 id` · `title = 시술권 묶음 이름(KOS 카드 머리 · 옵션 이름)` · 아래 = 구성 시술(세트)마다 `id = 세트 id` · `title = 세트 이름` · `rounds = "n/m"`(n = 전체 − 남음 · 취소 뺌) · `today` · `state` · `pickable`(남은 회차 있음 — [시술 대기] `line_ids` 에 이 세트 id).
  - 구매 전 수납 필요 오늘 시술: 머리 `id = "option:<옵션>"` · `title = 옵션 이름` · 아래 `id = "task:<visit_task id>"` · `title = 작업 이름` · `rounds = null` · `today = true` · `pickable = false`.
  - 오늘 작업은 시술권 id 로 자기 세트 줄에 붙음(사본에 시술권 id 가 아직 없으면 같은 옵션 묶음 첫 세트) — 새 줄 없음. 순서 = 오늘 받는 묶음 먼저 → 남은 시술권(구매 순). 이번 방문 구매 항목 줄(구성 줄)은 없앰 — 시술권으로만.
- B29 `editable.today_check` = 오늘 ∧ 예약 · 접수(시술만 진행 켬일 때 화면이 체크를 보임).
- B24 · B26 `consult.rooms[]` = 그 방문 구역(접수 → 지금 → 예약 구역)의 방만 · 빈 방 먼저 → 사용 중 · 각 안 순서 = 시술 현황 방 고르기(`sort_order` · 이름) · `empty` = 사용 중 아님(그 방 오늘 방문 또는 살아 있는 「방 배정」 방).
- B28 `change-flow-step` 도 보낸 즉시 다시 읽어 확인(D53).

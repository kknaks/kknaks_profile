# research-companion-1 — 예약 표 「동행 그룹」(카드 겹쳐 놓기) · 원천 · 저장 · 화면 (조사 · 읽기 전용)

- 조사일: 2026-11-23 · task_4ebb4de38327
- 원천:
  - KOS openapi `ax-clinic-project/para/archive/inbox_archive/2026-09-18-kos-openapi.yaml`(25,055줄)
  - DAY 워크트리 `CENTURION_DAY/day-reservation`
  - cc-prototype `origin/main`
  - centurion
  - mediness `products/day/`
  - 시안 `20261113_예약현황_시연 (1).html`
  - `e2e-1-feedback.md` E7
- 고친 것 0, 커밋 0, KOS 호출 0. `.env` 는 읽지 않았고 고객 정보도 없다.

## 물음 1 ~ 7 요약

| # | 물음 | 답 | 그대로 / 가공 / 없음 |
|---|---|---|---|
| 1 | KOS 에 동행 개념이 있나 | **없다.**<br>openapi 에 companion · accompan · party · together · 동행 · 일행이 0건이다. 「group」은 모두 예약 그룹(`reservationGroup` · `get-reservation-slots-by-group(s)`) · 시술권 묶음 · 상품의 `linkedReservationGroupId` 뿐이다. 사람 사이 연결은 통계 응답의 소개자 · 추천인(`referrerAccount` · `referrerVisitor` · `referrerUnregisteredName` L12556 ~ 12566)뿐이다.<br>DAY 어댑터 · 매퍼 · DB 에도 칸이 없다(grep 0 — 데모 가짜 글 「보호자 동행 퇴실」 한 줄만, `emr/kos/demo/board_data.py:105`).<br>지금은 예약 메모 글(「동행2명」 같은 자유 글)로만 오간다 | **없음** — DAY 에만 두는 기능이다(KOS 읽기 · 쓰기 없음) |
| 2 | cc · centurion · 기획 | cc: 화면 · 칸 없다. 옛 cc 가 예약 메모에서 「동행 칸」을 뽑던 것은 **없앴다**(`_archive/cc/back/README.md:171`) · 메모 글 예시뿐이다(`:157`).<br>centurion: grep 0.<br>기획: 동행자는 **예약 메모**로 본다(`예약-현황-·-예약.md:198` · `:367`). 「트윈룸은 일행 최대 2명」(`설정.md:579`)은 방 정책이라 그룹 기능이 아니다 | **없음** — 메모 글뿐이고 기능 근거는 사용자 요청(E7)뿐이다 |
| 3 | 시안 | drag · draggable · dnd · dataTransfer · pointerdown · 동행 · 일행이 **0건**이다 | **없음** — 띠 모양 · 문구는 새로 정해야 한다 |
| 4 | DAY 배치 · 끌어 놓기 자리 | 표 카드 가로 자리는 `policies/reservations.py:200-222` `stack` 이 정한다. 기존 끌어 놓기는 **시술 현황 카드 순서 G9** 하나다(`static/day.js:738-855` pointer 이벤트 · FLIP · 놓으면 `day:sorted` → 폼 `hx-trigger` → `PUT /board/order` · 끄는 동안 폴링 미룸 `busy`). 프론트 규약: JS 는 `day.js` 하나 · 이벤트 위임 + `data-*` · 인라인 스크립트 금지(`AGENTS.md:119`) | **가공** — G9 의 끌기 · 히트 테스트 · 폴링 미룸을 다시 쓴다. 놓는 결과만 「순서」에서 「겹친 카드와 묶기」로 다르다 |
| 5 | DB 설계 | ⓐ `companion_group` + `companion_member`(연결 테이블) / ⓑ `visit.companion_group_id`(+ `companion_group`) — 표 5 | 새 테이블이다. SPEC-000 §2 규칙(`hospital_id` · soft delete · 부분 유일 · JSON 목록 금지 · 외부 id 없음)에 맞춘다 |
| 6 | 「같은 시간대」 | 후보 셋 — 같은 시작 분 / **그 열 간격의 같은 시작 칸**(`start // interval_minutes`) / 시간 겹침 | 추천: **같은 시작 칸(그 열 간격)**(표 6) |
| 7 | 코디가 정할 것 | §7 표(Q1 ~ Q10) | — |

---

## 1. KOS (근거)

| 찾은 것 | 위치 | 뜻 |
|---|---|---|
| companion · accompan · party · together · 동행 · 일행 | openapi 전체 0건 | 개념 없음 |
| `group` 이 들어간 경로 · 스키마 | `/schedule/open/v1/queries/get-reservation-slots-by-group`(L2591) · `…/v2/…by-groups`(L3572) · `ZoneNotInGroup` 오류들(L3104 · L3303 · L3461) | 모두 **예약 그룹(열)** |
| `linkedReservationGroupId` | L12329 (`OpenLinkableProductContract`) | 상품 ↔ 예약 그룹 연결 — 사람 묶음 아님 |
| `referrerAccount` · `referrerUnregisteredName` · `referrerVisitor` | L12556 ~ 12566 (선불카드 충전 통계 항목) | 소개자 · 추천인 — 동행과 다름 |
| DAY `backend/day/emr/kos/*` · `models` · `migrations` | grep 0 | DAY 도 받지 않는다 |

- 결론: **동행 그룹은 DAY 에만 있는 기능**이다. KOS 로 보내지 않고 KOS 에서 받지도 않는다. 쓰기 큐와 `external_ref` 가 필요 없다.
- 한계: openapi 는 공개(open) API 문서다. 내부 API 는 문서가 없어 **확인 안 됨**이다. 다만 KOS 웹 예약 화면 HAR 이나 시안에도 근거가 없다.

## 2. cc · centurion · 기획

- **cc-prototype** `origin/main`:
  - `_archive/cc/back/README.md:157` · `tests/fixtures/scenario/seed.json:21` — 예약 메모 글에 「동행2명」이 들어 있다(예시).
  - `_archive/cc/back/README.md:171` — 「메모 속 … 동행 칸은 **없앴다**」. 메모는 원문 그대로 둔다.
  - `procedure/**` 지금 코드에는 동행 기능이 없다.
- **centurion** (`/Users/kknaks/git/centurion`): 0건.
- **기획** (`00-baseline/planning/`):
  - `예약-현황-·-예약.md:198`: 「예산 · 동행자 · 귀가 희망 시각은 예약 메모에서 본다」.
  - `:367`: 예약 메모(1,000자)에 「예산 · 동행자 · 귀가 희망 시각처럼 위 값에 없는 요청을 적고」.
  - `설정.md:579`: 「트윈룸은 일행 최대 2명이 같이 쓴다」 — 방 정책이다.
- 결론: 동행은 지금 **메모 글로만** 다룬다. 묶는 기능의 근거는 사용자 E7 하나다. 기획안과 다른 곳(새 기능)으로 SPEC 에 적어야 한다.

## 3. 시안

- drag · draggable · dnd · dragstart · ondrop · dataTransfer · pointerdown · 동행 · 일행 · companion 모두 0건이다(긴 data URI 줄은 빼고 셌다).
- 띠 모양, 띠 위 글자(있다면), 끌기 중 미리보기, 빠지는 동작은 모두 **새로 정해야 한다**(§7 Q4).

## 4. DAY 지금 배치 · 끌어 놓기 코드

| 무엇 | 위치 | 지금 |
|---|---|---|
| 카드 높이 · 자리 | `policies/reservations.py:188-196` `_card_span` | 시작 = `reserved_start_at` 분 · 끝 = `reserved_end_at`(없으면 열 간격 한 칸) · 최소 30분 · 24:00 에서 자름 |
| 가로 자리(lane) | `policies/reservations.py:200-222` `stack` | 정렬 키 = (시작 // **30분(SLOT_MINUTES)** · 닫힘 · 시작 · 생성 시각). 시간 겹치는 카드끼리 비어 있는 가장 왼쪽 자리를 쓴다 |
| 열 단위 | `policies/reservations.py:240-285` `_cards` | 열(`visit.group_id`)마다 따로 `stack` · `ReservationCardData.stack_index` |
| 템플릿 | `templates/partials/reservations_parts.html:67-69` `card` | `data-day-res-card` · `data-day-res-start` · `-end` · `-stack` 으로 자리를 놓는다(위치는 JS · CSS 토큰) |
| 폴링 | `static/day.js:1654-1660` | 10초 조각 폴링(`poll=1`) · 날짜 요청 중이거나 팝오버가 열려 있으면 그 회차를 건너뛴다 · 공지 편집 칸은 지킨다(`:1681-`) |
| **기존 끌어 놓기 G9** | `static/day.js:738-855` · `templates/ui.html:229` · `templates/partials/board_main.html:40-47` · `routers/board.py:592` | 시술 현황 카드 순서다. `[data-day-sort]` · `[data-day-sort-item]` · `[data-day-sort-handle]` · pointerdown · move · up · cancel · 손을 따라오는 translate · FLIP · 화살표 키 · 놓으면 `day:sorted`(detail.order) → 폼 `hx-trigger` → `PUT /board/order`(`visitIds` 순서) · 끄는 동안 다시 받기를 미룸(`busy` `:936`) |
| 저장 선례 | `models/task.py:266-275` `BoardCardOrder` · SPEC-000 `board_card_order`(L857-865) | DAY 에만 있는 화면 상태 테이블(`hospital_id` · `board_date` · `visit_id` · `position` · `updated_by_staff_id` · soft delete) |
| 동기화가 DAY 칸을 덮나 | `emr/sync_persistence.py:15-35` `SyncTable.write` | upsert 가 **그 동기화가 가진 칸만** `set_` 한다. `visit` 에 DAY 칸을 더해도 일정 동기화가 덮지 않는다(ⓑ 안의 전제) |

**넣을 자리(추천)**

1. G9 의 끌기 엔진(따라오기 · 히트 테스트 · 놓기 · 폴링 미룸)을 예약 표 카드에도 건다. 손잡이는 카드 전체이거나 별도 손잡이다(카드에 다른 누르기 동작이 없음 — R2).
2. 놓았을 때 아래 카드가 있으면 `day:grouped`(끈 카드, 대상 카드) → `hx` 로 **`PUT /reservations/companions`**(이름 제안)를 보낸다. 띠 밖에 놓으면 「빠지기」 요청이다.
3. 응답은 `#reservation-main` 조각이다. 다른 화면은 10초 폴링에 반영된다(사용자 기본값).
4. `stack` 은 **같은 그룹 카드를 이웃 lane 으로** 모아야 띠가 하나로 감싸진다. 지금 정렬 키는 (시작 칸 · 닫힘 · 시작 · 생성 순)이라 다른 카드가 사이에 끼일 수 있다. 정렬 키에 「그룹 묶음」을 넣는 정책 변경이 필요하다(§7 Q5).
5. 인라인 스크립트는 금지다. 위임 + `data-*` 로 하고 CSS 는 `styles/app.css` → `static/day.css`.

## 5. DB 설계 후보

SPEC-000 §2 규칙:
- 업무 테이블은 `hospital_id` 를 둔다.
- **소프트 딜리트**: `deleted_at` 을 두고, 유일 제약은 살아 있는 행만(부분 유일).
- **목록을 JSON 에 담지 않는다** — 연결 테이블을 쓴다.
- 외부 id 는 `external_ref` 에만 둔다. 동행은 DAY 전용이라 해당이 없다.
- `created_at` · `updated_at` · `deleted_at` 을 둔다.

### 표 5 — 두 안

| | ⓐ `companion_group` + `companion_member` (추천) | ⓑ `companion_group` + `visit.companion_group_id` |
|---|---|---|
| 꼴 | `companion_group(id uuid PK, hospital_id FK, created_by_staff_id FK?, created_at · updated_at · deleted_at)`<br>`companion_member(id uuid PK, group_id FK, visit_id FK, added_by_staff_id FK?, created_at · updated_at · deleted_at)` · 부분 유일 `(visit_id) WHERE deleted_at IS NULL`(방문은 한 그룹에만) | `companion_group(…위와 같음)` + `visit.companion_group_id uuid FK NULL` |
| 빠지기 | 멤버 행 `deleted_at` · 남은 멤버가 1명이면 그 멤버와 그룹도 `deleted_at`(사용자 기본값) | `visit.companion_group_id = null` · 남은 1명도 null · 그룹 `deleted_at` |
| 이력 | 누가 언제 넣고 뺐는지 행으로 남는다(soft delete) | 마지막 상태만 있다 — 이력은 `event_log` 로 |
| KOS 와 경계 | 핵심 테이블(`visit` = KOS 데스크 몫)을 건드리지 않는다. KOS 를 떼도 그대로다 | `visit` 에 DAY 전용 칸이 생긴다(일정 동기화는 덮지 않음 — `sync_persistence.py`). 다만 「`visit` 은 KOS 스케줄 1건」(`models/visit.py:64`)인 표에 DAY 상태가 섞인다 |
| 읽기 | 그날 방문 목록 + 멤버 join 한 번 | `visit` 칸 그대로(join 없음) |
| 「방문은 한 그룹」 | 부분 유일 인덱스로 막는다 | 칸 하나라 자연히 하나 |
| 날짜 | 그룹에 날짜 칸이 없다 — 멤버 방문의 `reserved_start_at` 으로 안다. `board_date` 칸을 둘지는 선택(그날 목록 쿼리용 · `board_card_order` 선례) | 같음 |
| migration | 새 테이블 2 | 새 테이블 1 + `visit` 칸 1 |

**추천: ⓐ**

- SPEC-000 의 「핵심 테이블에 외부 · 화면 상태 칸을 늘리지 않음」「연결 테이블」 방향과 맞는다.
- `board_card_order` 처럼 화면 상태를 따로 두는 선례가 있다.
- 넣고 뺀 이력도 남는다.

**공통 — 그룹이 깨지는 조건(사용자 기본값)**

- KOS 에서 시간이나 예약 그룹이 바뀌어 조건이 깨지면 「자동으로 빠짐」이다.
- 갈래 ① 동기화 회차 뒤 정리 작업이 `deleted_at` 을 채운다. 저장이 맞아진다.
- 갈래 ② 읽을 때 조건이 맞는 멤버만 묶어 보인다. 저장은 그대로라, 다시 맞아지면 되살아난다.
- 추천은 ① 이다(「빠짐」은 실제로 없어지는 것). 다만 ① 은 일정 동기화에 단계가 하나 더 붙는다. 시술 현황과 같은 회차이므로, 실패해도 회차를 오류로 만들지 않게 하는 것이 R62 와 같은 원칙이다.
- 취소 · 노쇼 · 지운 방문도 같은 정리 대상이다(§7 Q6).

## 6. 「같은 시간대」 판정

### 표 6

| 후보 | 판정 | 맞는 점 | 문제 |
|---|---|---|---|
| ① 같은 시작 분 | `start_min` 같음 | 가장 엄격 · 오해 없음 | 10:00 과 10:10 처럼 한 칸 안의 다른 분은 못 묶는다 |
| ② **같은 시작 칸(그 열 간격)** | `start_min // interval_minutes` 같음(열 `reservation_group.interval_minutes` — 열 머리 「{간격}분」 · `models/room.py:81`) | 표에 보이는 「칸」과 같다. 정원(「n명 / m분」)도 칸 단위다 | 간격이 30분이 아닌 열이면 `stack` 의 30분 칸(`SLOT_MINUTES`)과 기준이 다르다 → `stack` 도 같은 기준으로 맞춰야 한다 |
| ③ 시간 겹침 | `[start, end)` 가 겹침 | 길이가 달라도 묶인다 | 사슬 문제가 생긴다(A–B 겹침, B–C 겹침, A–C 안 겹침). 조건이 깨지는 때가 애매하다 |

**추천: ②**

- 카드를 겹쳐 놓는 화면 동작이 「같은 칸에 겹쳐 놓기」와 같다.
- 「조건이 깨짐」 판정도 「시작 칸이 바뀜 또는 열이 바뀜」 하나로 끝난다.
- 30분 열에서는 지금 `stack` 의 칸과 같다.

## 7. 코디가 정할 것 (추천 포함)

| Q | 정할 것 | 갈래 | 추천 |
|---|---|---|---|
| Q1 | 저장 꼴 | ⓐ 연결 테이블 / ⓑ `visit` 칸 | **ⓐ** (§5) |
| Q2 | 「같은 시간대」 | ① 같은 분 / ② 같은 시작 칸(열 간격) / ③ 겹침 | **②** (§6) |
| Q3 | 끌기 손잡이 · 놓기 판정 | 카드 전체 / 손잡이 · 놓은 점 아래 카드 / 겹친 면적 | 카드 전체를 끌고 **놓은 점(포인터) 아래 카드**에 묶는다(G9 히트 테스트 재사용). 조건(같은 열 · 같은 칸)이 안 맞는 카드 위에 놓으면 아무 일 없이 제자리다 |
| Q4 | 띠 모양 · 글자 | 시안에 없다 — 띠 색 · 두께 · 둥글기 · 그룹 이름이나 수 표시 여부 | 사용자 그림 `---|[카드][카드]|---` 대로 카드 묶음을 감싸는 얇은 테두리만 두고 **글자는 없게**(문구를 짓지 않음) — 디자인 확인을 받는다 |
| Q5 | 표 배치 | 같은 그룹을 이웃 lane 으로 / 지금 자리 그대로 띠만 | **이웃 lane** — `stack` 정렬 키에 그룹을 넣는다(그룹 먼저 생긴 순 → 그 안 넣은 순) |
| Q6 | 닫힌 카드 | 취소 · 노쇼 · 지운 방문 | **자동으로 빠짐**(조건이 깨지는 것과 같게) · 1명 남으면 그룹 없음 |
| Q7 | 이미 다른 그룹인 카드를 끌어 다른 그룹 위에 놓기 | 옮김 / 막음 | **옮김**(앞 그룹에서 빠지고 새 그룹에 들어감 · 앞 그룹이 1명 남으면 없어짐) |
| Q8 | 그룹 크기 상한 | 없음 / n명 | 상한 없음 — 결정이 필요하면 사용자 확인 |
| Q9 | 권한 키 · 기록 | 키 이름 · `event_log` | 새 키 `reservation.companion` edit · 기본 모든 직무(데이터 migration · `reservation.notice` 와 같은 방식) · `event_log` `companion_join` / `companion_leave`(자동 빠짐 포함) |
| Q10 | 날짜 · 화면 범위 | 오늘만 / 모든 날짜 | 모든 날짜(표가 보이는 날) — 지난 날짜를 막을지는 확인한다(공지는 지난 날을 막음 — R61) |

### 덧붙임

- **동시 편집**: 두 데스크가 같은 카드를 거의 같이 끌면 나중 저장이 이긴다. 「방문은 한 그룹」 부분 유일 인덱스가 이중 소속을 막는다.
- **원내 현황 · 시술 현황**: 동행 표시를 넣을지는 이번 범위 밖이다(E7 은 예약 표만).
- **SPEC**: SPEC-006 새 개정으로 넣는다. 「기획안과 다른 곳」(기획은 메모로 봄), 「시안과 다른 곳」(시안 없음), DAY-SPEC-000 새 테이블(00 데이터 모델 — 다른 스펙과 다른 곳 · 또는 SPEC-000 개정)이 들어간다.

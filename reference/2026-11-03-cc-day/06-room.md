# 06 방 · 구역 · 예약 그룹

2026-11-03 사용자와 정함. 공통 규칙은 [README.md](README.md). 검토표: https://claude.ai/artifact/PkubnqZG3Hn5piJJnqTFp2

## 정한 것

- cc 의 `zone` · `room` · `reservation_group` 을 옮긴다. cc 가 JSON 으로 두던 구역별 정원 · 요일 시간표는 행으로 푼다.
- **예약 그룹(3번에서 미룬 것)** — KOS 가 예약 안 `reservationGroupId` 를 폐기 예정으로 두고 점유 자원(`occupiedResources`)으로
  옮기는 중이다. 그래서 `visit.reservation_group_id` 를 두지 않고 **`visit_occupied_resource`**(방문이 잡은 예약 그룹 · 구역 · 시간)로 둔다.
- cc `reservation_slot`(칸별 정원 · 예약 수 캐시)은 테이블로 두지 않는다 — 정원과 방문 점유에서 계산한다.
- 요일 운영 시간은 `time`(병원 현지 시계 시간) — 순간이 아니므로 UTC 규칙의 예외.
- 1차는 KOS 원장 — 기준 정보라 1시간마다 받는다. KOS id 는 `external_ref`.

```text
hospital ─< zone ─< room
hospital ─< reservation_group ─< reservation_group_capacity >─ zone
                              └─< reservation_group_timetable (요일 7행)
visit ─< visit_occupied_resource >─ reservation_group · zone   (+ 지정 의사 N:M)
```

## zone · 구역 (층)

| 필드 | 타입 | 필수 | 설명 | 외부(KOS) · (cc) |
|---|---|---|---|---|
| `id` | uuid PK | ✓ | 병원 안을 나눈 단위 — 보통 층(명동점 4층 · 데모엔 미사용 구역도) | id (cc zone.kos_id) |
| `hospital_id` | uuid FK → hospital | ✓ |  |  |
| `title` | varchar | ✓ | 예: 4층 | title (cc zone.title) |
| `sort_order` | int | ✓ |  | order (cc zone.order) |
| `is_default` | bool | ✓ | 기본 구역 | isDefault (cc zone.is_default) |
| `created_at · updated_at · deleted_at` | timestamptz | ✓ | 외부에서 사라지면 deleted_at (cc zone.present) |  |

## room · 방

| 필드 | 타입 | 필수 | 설명 | 외부(KOS) · (cc) |
|---|---|---|---|---|
| `id` | uuid PK | ✓ | 시술 현황판의 칸 — 작업 · 방문이 들어가는 방 | id (cc room.kos_id) |
| `hospital_id` | uuid FK → hospital | ✓ |  |  |
| `zone_id` | uuid FK → zone | ✓ | 어느 층의 방 | zoneId (cc room.zone_kos_id) |
| `title` | varchar | ✓ | 예: 레이저 1번 | title (cc room.title) |
| `sort_order` | int | ✓ | 현황판 칸 순서 | order (cc room.order) |
| `created_at · updated_at · deleted_at` | timestamptz | ✓ |  |  |

## reservation_group · 예약 그룹

| 필드 | 타입 | 필수 | 설명 | 외부(KOS) · (cc) |
|---|---|---|---|---|
| `id` | uuid PK | ✓ | 예약을 받는 칸 — 예약 현황판의 세로 열(예: 시술 · 상담 · 기타). 시간표 · 간격 · 구역별 정원을 갖는다 | id (cc reservation_group.kos_id) |
| `hospital_id` | uuid FK → hospital | ✓ |  |  |
| `title` | varchar | ✓ |  | title |
| `sort_order` | int | ✓ | 예약 현황판 열 순서 | order |
| `interval_minutes` | int | ✓ | 예약 간격 — 기본 30분 | intervalMinutes (cc interval_minutes) |
| `same_day_close_buffer_minutes` | int |  | 당일 예약 마감 — 시작 몇 분 전까지 받나 | sameDayCloseBufferMinutes (cc close_buffer_min) |
| `created_at · updated_at · deleted_at` | timestamptz | ✓ |  | deleted |

## reservation_group_capacity · 구역별 정원 (그룹 1 : N)

| 필드 | 타입 | 필수 | 설명 | 외부(KOS) · (cc) |
|---|---|---|---|---|
| `group_id · zone_id` | uuid FK · PK | ✓ | 그룹이 켜진 구역 — cc 의 JSON [{zoneKosId, capacity}] 대신 행 | intervalCapacities[] (cc capacities) |
| `capacity` | int | ✓ | 한 칸(간격)에 받는 예약 수 | capacity |
| `created_at · updated_at · deleted_at` | timestamptz | ✓ |  |  |

## reservation_group_timetable · 요일별 운영 시간 (그룹 1 : 7)

| 필드 | 타입 | 필수 | 설명 | 외부(KOS) · (cc) |
|---|---|---|---|---|
| `group_id · weekday` | uuid FK · enum mon~sun · PK | ✓ | cc 의 JSON {요일 → …} 대신 요일마다 행 | timetable (cc timetable) |
| `is_enabled` | bool | ✓ | 그 요일 운영 | enabled |
| `start_time · end_time` | time |  | 운영 시작 · 끝 — 병원 현지 시각(시계 시간). 순간이 아니라 UTC 규칙의 예외 | start · end |
| `break_start · break_end` | time |  | 휴게 시간 | breakStart · breakEnd |
| `created_at · updated_at · deleted_at` | timestamptz | ✓ |  |  |

## visit_occupied_resource · 방문이 잡은 예약 칸 (방문 1 : N)

| 필드 | 타입 | 필수 | 설명 | 외부(KOS) · (cc) |
|---|---|---|---|---|
| `id` | uuid PK | ✓ | 방문(예약)이 어느 예약 그룹 · 구역의 몇 시 칸을 잡았나 — KOS 가 visit 의 reservationGroupId(폐기 예정) 대신 쓰는 구조. 3번의 visit.reservation_group_id 를 이걸로 바꾼다 | occupiedResources[].id (cc reservation.resources) |
| `visit_id` | uuid FK → visit | ✓ |  |  |
| `type` | enum reservation_group | ✓ | 점유 종류 — KOS 값은 지금 RESERVATION_GROUP 하나 | type |
| `reservation_group_id · zone_id` | uuid FK | ✓ |  | reservationGroup.reservationGroupId · zoneId |
| `start_at · end_at` | timestamptz | ✓ | 잡은 시간 | reservationTime |
| `doctor_ids` | — |  | 지정 의사 — 있으면 visit_occupied_resource_doctor(N:M) | reservationGroup.doctors[] |
| `created_at · updated_at · deleted_at` | timestamptz | ✓ |  |  |

## 다른 곳으로

| 필드 | 타입 | 필수 | 설명 | 외부(KOS) · (cc) |
|---|---|---|---|---|
| `reservation_slot (cc)` | — |  | 칸별 정원 · 예약 수 캐시 — 정원(reservation_group_capacity)과 방문(visit_occupied_resource)에서 계산한다. 테이블로 두지 않는다 → 계산 | get-reservation-slots-by-groups (cc reservation_slot) |
| `visit.reservation_group_id (3번)` | — |  | 폐기 예정 칸 — visit_occupied_resource 로 바꾼다 → visit_occupied_resource | reservation.reservationGroupId |
| `room_title (cc reservation)` | — |  | 방 이름 사본 — room_id 로 읽는다 → room |  |
| `외부 id` | — |  | 구역 · 방 · 예약 그룹 · 점유의 KOS id → external_ref | id |

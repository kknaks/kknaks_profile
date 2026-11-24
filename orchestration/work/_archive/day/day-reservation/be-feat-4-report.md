# day-reservation backend 기능 4 — 동행 그룹 + 카드 배치(E6 · E7) + 검수 3 W3-1 · W3-2

## 상태: done

- 커밋 · 스택 손대기 없음.
- 템플릿 · JS · CSS는 frontend 몫이라 건드리지 않았다.
- 정본: 결정 R63 ~ R69 · 계약 v4 · 조사 research-companion-1 §4 ~ §6.

## 1. 테이블 + migration

- `models/companion.py`(DAY 전용 · KOS 읽기 / 쓰기 없음)
  - `companion_group(id, hospital_id, created_by_staff_id, created_at · updated_at · deleted_at)`
  - `companion_member(id, hospital_id, companion_group_id, visit_id, added_by_staff_id, 시각 셋)`
  - 부분 유일 `uq_companion_member_visit_id`(`deleted_at IS NULL` — 방문 하나는 한 그룹에만)와 `ix_companion_member_companion_group_id`(살아 있는 행)를 둔다.
- 칸 이름은 `group_id`가 아니라 `companion_group_id`다. 저장소 이름 규칙상 `group_id`는 `ReservationGroupId` 전용이다(architecture 시험).
- `visit` 칸은 바꾸지 않았다(조사 ⓐ).
- migration:
  - `0021_companion_tables`: 테이블 둘 + 인덱스 둘
  - `0022_companion_permission`: 살아 있는 모든 직무에 (`reservation.companion`, edit) · `ON CONFLICT DO NOTHING`
  - `alembic heads`는 `0022_companion_permission` 하나다. 이름은 모두 32자 안(앞 판 재발 방지 시험 통과).
- 권한: `policies/permissions.COMPANION_KEY`를 두고 기본 표 full · view 둘 다에 edit를 넣었다(R69).

## 2. 배치 policy (`policies/reservation_layout.py` · 순수)

**시간 행**: 전 열 공통 **30분**(`ROW_MINUTES` = 축 눈금 단위). 축 시작부터 24:00까지 끊김 없이 이어진다. 카드는 **시작 시각이 든 행**에 놓인다.

**자리**: 같은 열 · 같은 행에서 자리 i의 `lane = i % 5` · `line = i // 5`(R64 — 6번째부터 아래 줄).

**자리 순서**:
1. 동행 그룹 카드 먼저. 그룹이 먼저 생긴 순, 그 안은 넣은 순이다(R68 · 조사 Q5 — 같은 그룹은 늘 이웃 자리).
2. 그다음 그룹 없는 카드. 닫힘(취소 · 노쇼)을 뒤로 하고 시작 → 생성 순이다(앞 판 `stack` 순서 그대로).

**행 줄 수**: `rows[].lines` = 그 행에서 가장 많은 줄 수(전 열 공통 · 최소 1).

**띠**: `bands[]` = 그룹 · 줄마다 하나. `lane_from` ~ `lane_to`는 이어진 자리다. 그룹이 줄을 넘으면 줄마다 하나씩 생긴다.

**묶기 조건**(R66 `can_join`): 같은 열 ∧ 같은 시작 칸(`start // 그 열 interval_minutes`) ∧ 둘 다 열린 카드 ∧ 다른 방문.

**읽을 때 자동 빠짐**(R67 `valid_members`):
- 빠지는 멤버:
  - 그 날짜 사본에 없는(지운 · 다른 날로 옮긴) 방문
  - 닫힌 카드
  - 그룹 첫 멤버(넣은 순)와 열이나 시작 칸이 달라진 멤버
- 남은 멤버가 2명 미만이면 그룹을 보이지 않는다.
- 저장은 쓰기 · 동기화 때 맞춘다(§4).

R63(담당의 = 시작 순으로 보아 담당의가 정해진 첫 줄)은 기능 2의 `doctor_names`가 이미 그렇게 한다. 미정 줄은 건너뛴다.

## 3. 보기 모델 (계약 v4)

`cards[]`:
- 더함: `lane: int`(0 ~ 4) · `line: int`(0 ~) · `companion_group_id: str|null`(읽을 때 맞는 그룹만)
- **`stack_index`는 없앴다.**

새로 더한 칸:
- `rows: [{start_min, end_min, lines}]` — **단위 = 30분** · 전 열 공통 · 축 시작 ~ 1440
- `bands: [{group_id, column_id, start_min(그 행 시작), line, lane_from, lane_to}]`
- `companion_editable: bool` = 날짜 ≥ 오늘(KST) ∧ `reservation.companion` edit

예시 — 10:00 행 A 열에 동행 6명(G1) + 혼자 1명이면:

```
rows: [..., {"start_min": 600, "end_min": 630, "lines": 2}, {"start_min": 630, "end_min": 660, "lines": 1}, ...]
cards: G1 6명 = (lane, line) (0,0)(1,0)(2,0)(3,0)(4,0)(0,1) · 혼자 = (1,1)
bands: [{"group_id": "<G1>", "column_id": "<A>", "start_min": 600, "line": 0, "lane_from": 0, "lane_to": 4},
        {"group_id": "<G1>", "column_id": "<A>", "start_min": 600, "line": 1, "lane_from": 0, "lane_to": 0}]
```

화면은 행마다 높이 = `lines` × 카드 줄 높이로 쌓는다. 카드 top = 그 행 top + `line` × 줄 높이, left = `lane` × (카드 폭 140 + 간격)이다.

## 4. 쓰기 두 경로 (`routers/reservations.py` · `services/reservation_companions.py`)

**경로**:
- `PUT /reservations/companions` — form `visit_id`(끈 카드) · `target_visit_id`(놓은 카드)
  - 놓은 카드가 그룹이 없으면 새 그룹을 만든다(놓은 카드 → 끈 카드 순).
  - 있으면 그 그룹에 넣는다.
  - 끈 카드가 다른 그룹이면 **옮긴다**. 앞 그룹이 1명 남으면 없어진다.
  - 이미 같은 그룹이면 바뀌는 것이 없다.
- `PUT /reservations/companions/leave` — form `visit_id`
  - 그룹에서 뺀다. 1명 남으면 그룹이 없어진다.
  - 그룹이 없으면 바뀌는 것이 없다.

**검사 순서**:
1. 401
2. 403(CSRF · `reservation.companion` edit)
3. 400(폼 꼴 · 모르는 칸 · uuid 아님)
4. 404(없는 · 다른 병원 방문)
5. 409 `companion_past_date`(그 방문 날짜 < 오늘 KST · 묶기 / 풀기 둘 다)
6. 409 `companion_condition`(다른 열 · 다른 칸 · 취소 · 노쇼 · 같은 카드)

**응답**:
- 200 = `partials/reservations_main.html` 조각(`#reservation-main` — 폴링과 같은 값 · 그 방문의 날짜)
- 409는 본문 없이 `X-Day-Error: <code>` + `HX-Reswap: none`이다(공지와 같은 꼴 · 화면은 카드를 제자리로).
- 400은 기존 토스트 규약 + `X-Day-Error`다.

**동시 편집**: 두 방문 행을 `FOR UPDATE`로 잡고 나중 저장이 이긴다. 이중 소속은 부분 유일 인덱스가 막는다.

**event_log** (`visit_id` = 끈 카드):
- `companion_join {groupId, visitId, targetVisitId, fromGroupId}`
- `companion_leave {groupId, visitId, reason: manual | moved | alone | auto}`

**정리**(R67 「정리는 쓰기 / 동기화 때」):
- `prune(groups)`: 쓰기 전 대상 그룹 · 옮긴 앞 그룹 · 푼 그룹을 맞춘다.
- `prune_window(start, end)`: 10초 일정 회차와 날짜 회차가 일정 반영 뒤 같은 transaction의 **savepoint**에서 부른다. 실패해도 회차는 `done`이고 경고 로그를 남긴다. 결과는 `counts.absent.companion_member`로 센다.

## 5. 검수 3

- **W3-1**: 공지 **반영**도 일정 transaction에서 떼었다. `emr/sync_notices.apply_notices_isolated`는 `session.begin_nested()` savepoint 안에서 돈다.
  - 반영 중 DB 오류(잠금 시간 초과 · 교착 등)가 나면 그 savepoint만 되돌린다. 일정 반영은 commit된다.
  - 10초 회차는 공지 수를 세지 않는다. 날짜 회차는 `skipped.notice.unavailable`로 센다.
  - 두 회차 모두 이 도우미를 쓴다.
- **W3-2**: `tests/day/emr/test_date_sync_notices.py` 셋을 더했다.
  - 날짜 회차가 그 날짜 공지를 맞춘다.
  - 공지 읽기가 실패해도 C1이 `done`이다(`notice.unavailable`).
  - 공지 반영 DB 오류(`SELECT 1/0`)가 나도 savepoint만 되돌린다. 일정은 남고, 10초 회차도 `done`이다.

## 6. 시험

새 시험:
- `tests/day/test_reservation_layout.py`(값 · 6개): 조건 · 자동 빠짐 + 1명 남음 · 그룹 이웃 자리(먼저 생긴 순 → 넣은 순) · **6명 = 2줄 + 띠 줄마다** · 그룹 없는 순서 · rows lines(전 열 최대)
- `tests/day/board/test_reservation_companions.py`(실 PG · 앱 · 4개):
  - 묶기 → 더하기 → 다른 그룹 옮김(앞 그룹 1명 → 없어짐) → 풀기 → 1명 남음 → 그룹 없음
  - event_log 이유
  - 조건 409 다섯(다른 열 · 다른 칸 · 취소 · 노쇼 · 같은 카드)
  - 지난 날짜 409(묶기 · 풀기) · 400 · 404 · 403
  - 읽을 때 자동 빠짐(취소 + 시간 바뀜 → 그룹 안 보임 · 저장은 그대로) → `prune_window`가 3행 정리
- `tests/day/emr/test_date_sync_notices.py`(3개 · W3-1 · W3-2)
- `tests/migrations/test_companion_migration.py`(3개): 사슬 · 0021 up / down / up + 부분 유일(살아 있는 행 중복 거절 · 지운 뒤 다시 넣기) · 0022 권한 up / down / up

바꾼 시험:
- `test_reservation_rules`: `stack_index` → `lane` · `line`(순서 그대로 `[2,0,3,1,0,0]`)
- `test_reservation_queries`: lane · 쿼리 수 13 → **15**
- `test_reservation_inhouse_queries`: 오늘 16 → **18** · 다른 날 13 → **14**
  - 늘어난 것 = 동행 권한 확인 1 + 동행 멤버 1(그 날 방문이 있을 때만)
- `test_default_permissions` · `board/test_board_default_view`: 기본 표에 새 키
- `tests/migrations/test_alembic.py`: HEAD 0022

결과:
- 관련 묶음(`./scripts/test.sh -q`): reservation 시험 전부 · `tests/day/board` · `tests/day/web` · `tests/day/emr` · `tests/migrations` · default_permissions → **916 passed**
- architecture **317 passed**
- **`./scripts/check.sh --static` All requested checks passed**
- 전체 `check.sh`는 돌리지 않았다.

## 7. frontend · 코디가 확인할 것

1. **frontend**:
   - 카드 자리 = `lane` · `line` + `rows[].lines`(30분 단위)
   - 띠 = `bands`
   - 끌기 = `companion_editable`일 때만
   - 놓기는 `PUT /reservations/companions`(`visit_id`, `target_visit_id`), 띠 밖은 `PUT /reservations/companions/leave`(`visit_id`)
   - 응답 = `#reservation-main` 조각
   - 409는 본문 없이 `X-Day-Error`
   - `stack_index`가 없어졌으니 템플릿 `data-day-res-stack`은 바꿔야 한다.
2. **카드 높이**: 이제 카드는 시작 행 한 줄 높이다. `end_min`은 그대로 실어 두었다(쓸지는 화면 몫). 길게 이어지는 예약(끝 시각)을 표에서 높이로 보이던 방식은 R64 배치로 바뀐다 — 디자인 확인이 필요하다.
3. **열 간격 ≠ 30분일 때**: 묶기 조건은 그 열 간격의 칸이다(R66). 배치 행은 30분이다. 60분 열의 10:00 · 10:30 카드는 묶이지만 서로 다른 행에 놓인다. 띠도 행마다 따로 생긴다.
4. **배포**: migration 0021 · 0022 적용 + api · worker 재기동(코디 몫).
5. **SPEC**: SPEC-006 · SPEC-000 개정(새 테이블 둘 · R63 ~ R69)은 코디 · planner 몫이다.

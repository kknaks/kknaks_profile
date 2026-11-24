# day-reservation backend 결과 보고: Delivery #267(조회 · 권한) → #268(다른 날짜 최신화)

## 상태: done (실물 e2e만 pending. 순서 조건과 사유는 아래)

커밋 · push · PR 없음. 변경은 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-reservation`(base `origin/dev` 5ece25ea)에만 있다.

## 수행: 파일

### #267 조회 · 권한
| 파일 | 내용 |
|---|---|
| `backend/day/routers/reservations.py` (새) | `GET /reservations?date=&poll=`. 검사 순서는 401(`required_web_view`) → 403(`reservation` view) → 400(`date`). `HX-Request`면 `partials/reservations_main.html`, 아니면 `reservations.html`. 오늘이 아니고 `poll≠1`일 때만 계약 T 요청을 넣는다 |
| `backend/day/services/reservations.py` (새) | `parse_day`(빈 값이면 오늘, 10자 `YYYY-MM-DD`가 아니거나 없는 날짜면 400) · `board_view`(조회 → 판정 → 표현) · `needs_refresh`(오늘 · poll은 제외) · `request_refresh`(이름으로 `AsyncKicker.kiq(hospital_id, date)` 1회. 결과를 기다리지 않음. 시간 상한 = `OUTBOX_KICK_TIMEOUT_SECONDS`. 실패는 로그만) |
| `backend/day/queries/reservations.py` (새) | 묶음 조회. 쿼리 6개(그룹 · 정원 · 그 요일 시간표 · 휴무 · 방문+고객+열린 구매 EXISTS · 공지)로 고정. DB 사본만 읽음 |
| `backend/day/policies/reservations.py` (새) | 순수 판정: 카드 상태(취소 · 노쇼 먼저) · 겹침 순서(같은 30분 칸에서는 취소 · 노쇼가 뒤, 겹치면 빈 가장 왼쪽 자리) · 높이(끝 없음 = 간격 · 최소 30분 · 24:00 자름) · 정원 null(구역 0 또는 2+) · 열 회색 · 시간 칸 회색 · `open_min` · 축 · 필터 수 · 수납 필요 · 공지 순서 |
| `backend/day/presentation/reservations.py` (새) | 계약 V1 ~ V4 + V1 보충을 dict로(템플릿 최상위 이름) |
| `backend/day/dtos/reservation.py` (새) | 사본 행 · 판정 결과 DTO |
| `backend/day/policies/permissions.py` · `services/default_permissions.py` | `RESERVATION_KEY = "reservation"`. full · view 두 묶음 모두에 `reservation` VIEW 행 추가(board 방식 · `ON CONFLICT DO NOTHING` · 지운 행은 되살리지 않음). migration 없음. 다음 기준 정보 회차의 시드가 넣는다 |
| `backend/day/menu.py` | `HREFS`에 `reservation` · `reservation_board` → `/reservations` 추가 |
| `backend/day/main.py` | 라우터 등록 |

### #268 다른 날짜 최신화
| 파일 | 내용 |
|---|---|
| `backend/day/services/emr_date_sync.py` (새) | `run_reservation_date(hospital, day)`. 자세한 설계는 아래 「C1 ~ C3 설계」 |
| `backend/day/tasks/emr.py` | 새 task `day.sync_reservation_date_hospital(hospital_id: str, date: str)`. 주기 없음. 메시지가 깨졌거나 DB 예외(교착 등)가 나면 오류 이름만 로그로 남기고 `"error"` |
| `backend/day/services/emr_sync.py` | 더하기만 했다: `Job`에 `reservation_date` · `Status`에 `skipped_today` · `lock_ttl("reservation_date")` = 기준 정보 TTL(300초) · `_run` / `run_job`에 선택 인자 `key`(기본값은 지금처럼 병원 단위 키). 오늘 회차 코드 경로는 바뀌지 않음 |

### 테스트(새로 만들거나 고친 것)
- 새 파일: `tests/day/test_reservation_rules.py` · `tests/day/web/test_reservation_page.py` · `tests/day/test_reservation_queries.py`(infra) · `tests/day/board/test_reservation_permissions.py`(infra) · `tests/day/emr/test_date_sync.py`(infra) · `tests/day/emr/test_date_sync_rules.py`
- 고친 파일(새 기본 권한 행을 반영): `tests/day/test_default_permissions.py` · `tests/day/board/test_board_default_view.py` · `tests/day/emr/test_emr_sync_service.py`(「full 직무 = 행 2개」 전제를 `board.accept` 기준으로 바꿈)

## C1 ~ C3 설계 (#268)
- **창**: 병원 현지 d 00:00 ~ d+1 00:00을 UTC로 바꾼다(`today_window`와 같은 계산). 오늘이면 `skipped_today`로 끝나고 KOS · DB에 닿지 않는다.
- **C1**: KOS 읽기(일정 → 구매 → 고객마다 시술권 · 카드 → 바뀐 카드 이력)를 전부 transaction 밖에서 끝낸다. 그 뒤 `apply_schedules` → 처방 → 구매 → 시술권 → 카드 → 카드 이력 → 결제 카드 연결 → 작업 참조 → `apply_kos_keys`(일정 · 구매 · 시술권 · 카드 응답의 더할 칸을 합침)를 **한 transaction에서 commit 한 번**으로 한다. commit이 하나뿐인지는 AST 테스트로 막았다.
- **C2**: 잠금은 `day:lock:emr:reservation_date:{병원}:{날짜}` 하나뿐이다. 오늘 회차의 병원 잠금(`schedules` · `sales` · `kos_keys`)은 잡지 않는다. `apply_isolated`의 「잠금을 못 얻으면 None」 길도 쓰지 않는다. 실패나 시간 초과(상한 295초)면 전체가 되돌아가 `error` / `timeout`이 된다.
- **C3**: `sales_published_at` · 병원 `sales` 잠금 · 바뀐 고객 대기 집합 · 풀리지 않은 티켓 집합을 읽지도 쓰지도 않는다(AST 테스트 + Redis 확인). 시술권 · 카드를 받는 고객은 그 날 구매나 시술권 참조가 있는 고객 **전부**다. 상한이 없는 이유는 넘치는 고객을 조용히 건너뛰지 않기 위해서다(백필 ③과 같은 기준).
- **동시 요청**: 기다리지 않는 `try_lock`이다. 이미 도는 중이면 `skipped_locked`. 주기적 재최신화는 없다.
- **하지 않는 것**: 쓰기 큐 확인 · 「방 배정」 잇기 · 판 신호 · `record_sync` · 공지 · 기준 정보.

## 검증: 명령과 수치
- `./scripts/test.sh -q`(격리 PostgreSQL · Redis)로 #267 + #268 새 테스트, 고친 테스트, `tests/day/emr` 전체(오늘 회차 회귀), `tests/runtime`을 돌렸다: **373 passed**
  - #267 새 테스트: rules 13 · page 7 · queries(infra) 2 · permissions(infra) 2 = 24 passed
  - #268 새 테스트: date_sync(infra) 9 · date_sync_rules 8 = 17 passed
- `./scripts/test.sh --pure -q backend/tests/architecture`: **317 passed**. 중간에 3건이 실패했었는데 모두 frontend 작업 중인 템플릿 · day.js 때문이었고, 마지막 실행에서는 0건
- `ruff check` · `ruff format --check`: 만진 파일 22개 통과
- `mypy`(전체): **Success, 474 files**
- `taut check`(작업 트리): **diagnostics 0**. assurance 미완은 작업 트리에서 직접 돌려 migrations · stubs가 잡힌 것이고 내 변경과 무관하다. `scripts/check.sh`는 mirror 스냅샷으로 돈다
- `scripts/check.sh` 전체(frontend npm 검사 포함)는 돌리지 않았다. frontend 변경이 진행 중이라서다. 코디네이터가 PR 전에 1회 돌려야 한다

## 계약 대조
| 계약 | 같음/다름 |
|---|---|
| S `poll=1` → 요청 0 · 날짜 바꾸기 = poll 없음 | 같음 (test_reservation_page: 오늘 0 · 다른 날짜 열기 1 · 폴링 0 · 바꾸기 1) |
| T 이름 `day.sync_reservation_date_hospital` · 인자 `hospital_id: str` · `date: str` · kiq 한 번 · 안 기다림 · 오늘 · poll 제외 | 같음 (인자 이름까지 테스트) |
| V0 조각 `#reservation-main` = `partials/reservations_main.html` | 템플릿 이름은 frontend에 알렸다. 조각 범위는 frontend 몫 |
| V1 + 보충 `date · weekday · is_today · today · now_min · open_min · axis{start_min,end_min,time_gray_spans[]}` | 같음 |
| V2 `columns[]{group_id,title,capacity,interval_minutes,gray_spans[]}` | 같음 |
| V3 `cards[]{visit_id,group_id,start_min,end_min,stack_index,name,nationality,is_new,state,payment_due}` | 같음. state 10개 |
| V4 `filter{total,counts{reserved,reception,consultation,procedure,procedure_done,completed,canceled}}` · `notice{items[]{content}}` | 같음 |
| 셸 값 | `session · active_menu="reservation" · active_tab="reservation_board" · hospital_name · permissions · is_admin` |

## 이슈 · 코디가 확인할 것
1. **해석한 곳(SPEC 문장이 비어 있던 곳):**
   - 시간 칸 회색에서 「지난 날 끝까지」의 끝을 **켜진 시간표 중 가장 늦은 운영 끝**으로 잡았다. U-3 ③ 「운영 끝까지」에 맞춘 것이고, 그런 끝이 없으면 24:00이다.
   - `open_min`은 켜진 시간표 중 가장 이른 시작이다. 켜진 시간표가 없으면 null이다.
   - 휴무 행에 시작이나 끝 한쪽이 null이면 무시한다(OQ-4A-2 · 짓지 않음).
   - 그룹이 없거나 지운 그룹을 가리키는 방문은 카드 · 필터 수에서 빠진다(R20 전제).
   - 열 회색에 시간표의 시작이나 끝이 null이면 각각 0과 24:00으로 본다.
2. **KOS 호출량(#268)**: 그 날 구매나 시술권 참조가 있는 고객마다 2회(시술권 · 카드) + 바뀐 카드 이력 + 일정 1 + 구매 1. 붐비는 날은 수십 ~ 백여 회가 된다. 상한 295초를 넘으면 실패하고 이전 사본이 남는다.
3. **동시성**: 오늘 회차와 같은 행(같은 고객 · 시술권)을 동시에 쓰면 PostgreSQL 행 잠금이 기다린다(건너뜀 없음). 교착이 나면 한쪽 transaction이 되돌아가고, 날짜 최신화는 task가 `error`로 끝난다. 오늘 회차 쪽이 되돌아가는 경우는 다음 10초 회차가 다시 받는다. 실물에서 관찰한 적은 없다.
4. **기본 권한 행**: migration 없이, 다음 기준 정보 회차(1시간)의 `default_permissions.seed`가 기존 직무에 `reservation` view를 넣는다. 배포 직후 최대 1시간은 403일 수 있다.
5. **실물 e2e(#267 A5 · #268 A6): pending.** 순서 조건이 「①②③이 모두 들어간 뒤 마지막 머지 Issue에서 1회」이고, 브리프 §7이 사용자 포트 · 프로세스와 공유 DB를 금지한다. 로컬 앱 · worker · KOS 데모를 띄우는 일은 코디네이터 승인 뒤에 해야 한다. 확인 수단은 이미 있다: 요청 로그 `reservation refresh requested hospital=… date=…`와 task 결과 `skipped_locked`로 「같은 날짜 두 창 = 일정 조회 1회」를 본다.
6. 시드 파일 등 `scripts/`는 건드리지 않았다. 워크트리 루트에 `.venv`가 생겼다(uv가 만들었고 git ignore 대상).

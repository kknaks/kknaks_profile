# 리뷰 리포트 — day-reservation / code (2026-11-23)

대상: 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-reservation`(base `origin/dev` 5ece25ea)의 미커밋 변경. 수정 15개 · 새 파일 17개. Delivery #267 · #268 · #269.
근거: Issue 본문(contract_version 2) · `contract-v1-addendum.md` · `delivery-3-report.md`(계약 S · T · V0 ~ V4) · SPEC-006 · 시안 · AGENTS.md.
방법: 코드와 테스트를 직접 읽었다. 테스트는 다시 돌리지 않았다(코디가 350 + 12 passed를 확인함 · 역할 규칙상 실행 안 함).

## 판정: WARN

계약 S · T · V0 ~ V4와 C1 ~ C3 · R39 · R40은 코드에서 지켜진다. 오늘 10초 회차 경로도 바뀌지 않았다. FAIL은 1건이고 작은 것이다(addendum §3 문구 규칙 위반). 「조용히 통과하는 자리」는 테스트 3곳에서 나왔고, 브라우저에서만 드러날 폴링 경쟁 1건이 있다.

---

## FAIL

### F-1 시안에 없는 aria-label 「예약 표」를 넣고 문구 표에 「보이지 않음」으로 올렸다 (작음)
- `backend/day/templates/partials/reservations_parts.html:85` `<main class="day-res-board" aria-label="예약 표">`
- `backend/tests/architecture/test_screen_copy.py` HIDDEN `"예약 표": "보이지 않음 — 예약 표 main aria-label"`
- 근거: `contract-v1-addendum.md` §3 「더하는 문구는 **시안에 있는 글자만**, 각 행 근거 = 시안 html 줄 번호. 시안에 없는 글자는 더하지 않는다(그 자리는 비움)」. 시안에서 「예약 표」를 찾으면 0건이다(`.sched-wrap`에는 aria-label이 없다). 이번에 더한 다른 HIDDEN 행(상태 필터 L1475 · 날짜 고르기/이전 달/다음 달 L2419 · 왼쪽/오른쪽 열 보기 L1707-1708)에는 시안 근거가 있다. 이 행만 없다.
- 고칠 것: aria-label을 빼고 문구 표의 그 행도 지운다. 한 줄씩이다.

---

## WARN

### W-1 폴링 응답과 날짜 바꾸기 응답이 경쟁하면 화면이 옛 날짜에 묶일 수 있다 (#269 · 계약 S) — 브라우저 확인 필요
- `reservations_main.html:35` 폴링 요소(`hx-get=/reservations?date={{date}}&poll=1` · target `#reservation-main`)와 `day.js` `resGo` → `htmx.ajax(... source: #reservation-nav, target: #reservation-main)`는 **서로 다른 요소에서 보내는 요청**이다. `hx-sync`도 없고 요청 취소도 없다.
- 일어나는 경우: 날짜 A의 폴링 요청이 떠 있을 때 [다음 날]을 누른다. B 응답이 먼저 들어오고 A 응답이 뒤에 들어오면 A 조각이 덮는다. 주소 줄은 B인데 화면은 A다. 덮은 조각 안의 폴링 요소도 `date=A`라서 10초마다 A만 다시 읽는다. **사용자가 다시 날짜를 바꿀 때까지 그대로 남는다.** htmx 2.0.4는 요청을 보낸 요소가 DOM에서 빠져도 응답 swap을 버리지 않는 것으로 안다. 확인은 못 했다.
- 근거: 계약 S(날짜 바꾸기와 폴링의 구분) · SPEC U-6 · R41. 테스트(`test_reservations_screen.py:204`)는 속성 문자열만 본다. 순서는 시험하지 않는다.
- 제안: 두 요청을 `hx-sync`로 같은 대상에 묶어 마지막 요청만 살린다(예: `#reservation-main`에 `hx-sync="this:replace"`). 아니면 `htmx:beforeSwap`에서 응답 날짜가 지금 날짜와 다르면 버린다. A4 e2e 때 같이 확인한다.

### W-2 `request_refresh`의 실제 `kiq`를 시험하는 테스트가 없다 — 조용히 통과하는 자리 (#267 A2 · 계약 T)
- `services/reservations.py:69-99`. 라우트 테스트 3개(`test_reservation_page.py:90` · `test_reservation_permissions.py:41` · `test_reservations_screen.py:151`)는 모두 `request_refresh`를 가짜로 바꾼다. `test_date_sync_rules.py:32`는 등록된 task의 이름과 인자 이름만 본다.
- 그래서 producer broker 구성이 틀리거나, 이름이나 인자 순서가 어긋나거나, kiq가 예외를 내도 테스트는 초록이다. 코드는 예외를 **삼키고 경고 로그만** 남긴다(`:87-97`). 화면은 200이고, 그 날짜는 영영 최신화되지 않으며, 표시도 없다(R19는 2루프).
- 제안: 메모리 broker(`InMemoryBroker`)로 `request_refresh`를 한 번 불러 「task 이름 = `day.sync_reservation_date_hospital` · args = `[str(hospital), 'YYYY-MM-DD']`」 메시지가 들어갔는지 단언한다. 실패 로그도 하나 확인한다.

### W-3 #268 테스트 가운데 하나는 아무것도 증명하지 않고, 하나는 범위를 덜 본다
- `test_date_sync.py:251-265` `test_A3_C2_실패면_중간_상태_없이_실패[fetch]`. 구매 **읽기**에서 실패하면 transaction을 열기 전에 끝난다. 그래서 `visits == []`는 늘 참이다. rollback을 증명하는 것은 `[apply]` 쪽(apply_kos_keys 예외)뿐이다. 시간 초과(`timeout`)로 되돌아가는 경우는 테스트가 없다.
- `test_date_sync.py:199-215` A1. 선불카드는 「`cards:vis-1`을 **불렀다**」만 단언한다. 카드와 작업(`apply_task_refs`)이 저장됐는지는 보지 않는다. #268 A1 범위(방문 · 고객 · 작업 · 그룹 칸 · 구매 · 시술권 · 선불카드)의 저장 증명이 비어 있다.
- 같은 파일 `:63-72` 고정본은 모든 일정에 `reservationGroupId="group-1"`을 넣는다. KOS가 그룹을 비워 보내면 카드는 `_cards`에서 조용히 빠진다(`policies/reservations.py:245`). R20 전제를 따른 것이라 허용하지만, 실물에서 그런 방문이 나오면 화면에는 아무 표시도 없다(아래 「실물」 참고).

### W-4 날짜 최신화는 오늘 회차와 같은 행을 잠금 없이 같이 쓴다 — 오늘 회차의 실패 · 건너뜀이 늘 수 있다 (오늘 회차 회귀 · 간접)
- 코드 경로는 그대로다. `emr_sync._run` / `run_job`에 `key=None` 기본값만 더해졌다. `Job` · `Status` 리터럴과 `lock_ttl`에 항목이 하나씩 늘었다. 오늘 회차 코드는 한 줄도 바뀌지 않았다.
- 하지만 `emr_date_sync.py:155-210`은 transaction 하나 안에서 고객 · 시술권 · 카드 · 카드 이력 · KOS 키 행을 쓴다. 이것은 오늘 회차(`run_schedules` → `_kos_keys` · `sync_sales_hospital`)가 같은 고객이면 함께 쓰는 행이다. 오늘 회차는 원래 「같은 잠금 안에서만 쓴다」로 행 경합을 피했다(`emr_kos_keys.py:88-93` W1 주석). 날짜 최신화는 그 잠금을 일부러 잡지 않는다(C2).
- 영향: 날짜 transaction이 길면 오늘 쪽 KOS 키 보충(상한 8초 · `SCHEDULES_APPLY_TIMEOUT_SECONDS`)이 행 잠금을 기다리다 시간 초과로 로그만 남기고 건너뛴다. 교착이 나면 오늘 일정 회차가 `error`가 되고 `record_sync(error)` → 시술 현황에 「동기화 멈춤」 근거가 한 회차 남는다. be 리포트 「이슈 3」과 같은 내용이다. 테스트는 Redis 잠금 경합만 본다(`test_date_sync.py:238`). DB 행 경합은 시험하지 않는다.
- C2 위반은 아니다. 날짜 쪽은 실패로 끝나고 건너뛰지 않는다. 다만 「오늘 10초 회차 동작은 바뀌지 않는다」(#268 A5)를 **부하 아래에서** 보장하지는 않는다. A6 e2e 때 동시에 돌려 로그(`emr kos keys schedules … failed` · `deadlock`)를 본다.

### W-5 범위 밖 날짜는 400이 아니라 500이다
- `services/reservations.py:38-48` `parse_day`는 형식만 본다. `date=9999-12-31`이면 `policies/reservations.py:82` `day + timedelta(days=1)`에서 `OverflowError`가 나서 500이다. `0001-01-01`은 UTC로 바꿀 때 해가 넘쳐 같은 결과가 날 수 있다.
- 근거: SPEC-006 케이스 매트릭스 「`date` 형식 오류 … 400 `invalid_request`」. 형식은 맞지만 다룰 수 없는 날짜에 대한 줄은 없다. 화면 버튼으로는 생기지 않고 주소를 손으로 칠 때만 생긴다.
- 제안: `parse_day`에서 `date.min < d < date.max` 밖이면 같은 400으로 거절한다.

### W-6 정원이 null인 열 머리는 「/」까지 지운다 — 사용자 확인 (V2)
- `reservations_parts.html:91` capacity가 null이면 `{{ interval }}분`만 남는다(「n명 / 」 전체를 뺀다).
- 계약 V2 「capacity null 이면 「n명」 부분 비움」은 「/ m분」을 남긴다고도 읽힌다. fe 리포트 「이슈 1」이 이미 올렸다. 계약 문장으로는 어느 쪽인지 닫히지 않는다.

---

## PASS (항목별 대조)

### #267
| Acceptance / 계약 | 판정 | 근거 |
|---|---|---|
| A1 HX → `partials/reservations_main.html`, 아니면 `reservations.html` · V1 ~ V4 이름 · 모양 | PASS | `routers/reservations.py:51-61` · `presentation/reservations.py:16-55`(최상위 11개 이름 = addendum §2) · `test_reservation_page.py:113` |
| V1 + 보충(`today` · `open_min` · `axis.time_gray_spans`) · 판정 = backend | PASS | `policies/reservations.py:159-179` · `:305-316`. 화면은 `time_gray_spans`를 그대로 쓴다(`reservations_parts.html:95`) · 열 gray_spans로 되살리지 않는다 |
| V2 정원 null(구역 0 · 2+) · 회색(운영 전 · 지난 · 쉬는 · 꺼짐 · 휴무 · 행 없음 = 없음 · 운영 끝 뒤 없음) | PASS | `:115-146` · `:182-184` = SPEC U-2 · U-3 ①~⑤ |
| V3 state 10개 · 취소/노쇼 먼저 · stack(같은 칸 닫힌 것 뒤 → 시작 → 생성) · payment_due = 귀가 대기 ∧ initialized | PASS | `:86-92` · `:199-221` · `:266` · `queries/reservations.py:111-115` = SPEC U-5 |
| V4 total(취소 · 노쇼 제외) · counts 7(reception = 접수 + 상담 대기 · procedure = 시술 대기 + 시술 · canceled = 취소 + 노쇼) · notice(`released_at` 순 · null 제외 · 그 날짜) | PASS | `:64-72` · `:230-236` · `queries:158-174` = SPEC U-6 · U-7 |
| A2 KOS 0(R39) · 오늘 0 · 다른 날짜 1 · `poll=1` 0 | PASS | `services/reservations.py:60-62` · `test_reservation_page.py:125-142` · import 경계 `:168-187`. 단 실제 kiq는 W-2 |
| A3 `reservation` view = full · view 두 묶음 모두 · 지운 행 안 되살림 · 행 없음 403 | PASS | `policies/permissions.py:27-34` · `test_reservation_permissions.py:51`(실 PostgreSQL) · `test_board_default_view.py` 고침 |
| A4 케이스 매트릭스(401 · 403 · 400 · 그룹 0 · 예약 0 · 취소 · 노쇼 · 수납 · 정원 0/2+) · 검사 순서 401 → 403 → 400 | PASS | 라우터 `:45-47` 순서 · `test_reservation_rules.py` 13개(DB 없음) · `test_reservation_queries.py`(infra 2개 · 쿼리 수 고정 6) |
| 계층: router가 DB를 만지지 않음 · repository 없음 · 묶음 조회 = `queries/` · 정책은 I/O 모름 · 같은 파일 이름 | PASS | AGENTS.md 「계층 규칙」 · 「기능 하나를 고치면 같은 파일 이름」 |
| 메뉴 링크 한 곳(`menu.py` HREFS) | PASS | `menu.py:34-39` |

### #268
| Acceptance / 조건 | 판정 | 근거 |
|---|---|---|
| 계약 T 이름 · 인자 · 주기 없음 | PASS | `tasks/emr.py:150-173` · `test_date_sync_rules.py:32-40`(`schedule` 라벨 없음) |
| A1 범위 = 오늘과 같음(일정 · 처방 · 구매 · 시술권 · 카드 · 이력 · 결제 카드 · 작업 참조 · 키 보충) · 쓰기 큐 확인 · 방 배정 · record_sync 안 함 | PASS(코드) / 테스트 W-3 | `emr_date_sync.py:155-210` · 금지 이름 AST `test_date_sync_rules.py:125-144` |
| A2 C1 — KOS 읽기는 모두 transaction 밖 · 반영 + 키 보충 = transaction 하나 · commit 한 번 | PASS | `:144-152` 읽기 → `:155-210` 반영. 아래 apply_* 모듈(`emr/sync_schedules · sync_purchases · sync_tickets · sync_schedule_sales · sync_kos_keys`)에도 `commit` 0을 grep으로 확인했다. 테스트 `test_A2_C1`은 다른 연결에서 읽어 중간 상태가 안 보임을 실제로 확인한다(가짜 아님) |
| A3 C2 — 오늘 회차 병원 잠금(`schedules · sales · kos_keys · master · menu`)을 쥐어도 done · `apply_isolated` 길 안 씀 | PASS | `test_date_sync.py:238-248`(실 Redis 잠금 세팅) · AST 금지 |
| A4 C3 — `sales_published_at` · pending · unresolved를 읽지도 쓰지도 않음 · 미래 published 키가 있어도 구매 저장 | PASS | `test_date_sync.py:268-281` — 진짜로 잡는다(오늘 구매 회차 함수를 아예 부르지 않는 설계) |
| A5 R40 같은 (병원, 날짜) 한 번 · 기다리지 않음 · 끝나면 다시 요청마다 | PASS | `date_lock_key` `:68-70` · `run_job(key=…)` · `test_A5`(gate로 겹침 · 일정 조회 1회 → 2회) |
| 오늘이면 KOS · DB에 닿지 않음 | PASS | `:135-137` · `test_date_sync_rules.py:66` |
| 오늘 회차 회귀(코드 경로) | PASS / 부하 아래는 W-4 | `emr_sync.py` diff = 리터럴 2 · TTL 1 · 선택 인자 `key` |

### #269
| Acceptance / 계약 | 판정 | 근거 |
|---|---|---|
| V0 조각 = 머리 날짜 줄 + 표 + 패널 · 셸은 전체 페이지만 | PASS | `reservations.html:8-10` · `reservations_main.html` · `test_reservations_screen.py:182-202` |
| 계약 S — 폴링 `poll=1` · push 없음(nav 밖이라 물려받지 않음) · 날짜 바꾸기는 poll 없이 · nav `hx-push-url` · 히스토리 복원은 전체 페이지(`web.is_htmx`가 `HX-History-Restore-Request` 제외) | PASS / 경쟁은 W-1 | `reservations_main.html:16` · `:35` · `day.js resGo` |
| A2 인라인 스크립트 · style 속성 0 · 자리는 CSSOM · 값은 `--day-res-*` 토큰 · 빌드 CSS | PASS | 새 템플릿 grep 0 · app.css 원시값은 토큰 정의(시안 줄 근거)에만 |
| A3 필터 = V4 수 그대로(다시 세지 않음) · 흐리게만 · 날짜를 옮겨도 유지 · 툴팁 state → 시안 글자(노쇼 = 「노쇼」) · 넘김 (폭 − 52) × 0.8 · 스크롤 유지(시안 L1698과 같음) | PASS | `reservations_parts.html:7-28` · `day.js` |
| 문구 — 시안 근거 표 | PASS · F-1 1건 제외 | `test_screen_copy.py` diff |
| 뺌 요소(RV-04 · 05 · 28 ~ 31 · 36 · 37 · 39 ~ 41) | PASS | `test_뺀_요소는_그리지_않는다` |

---

## 직원이 실물에서 만날 자리 (2루프 재료)

1. **배포 뒤 최대 1시간은 모든 직원이 403이다.** `reservation` view 행은 migration 없이 기준 정보 회차(1시간 · `run_master` → `default_permissions.seed`)가 넣는다(be 「이슈 4」). 메뉴 링크는 바로 열리니 「예약」을 누르면 거절 화면이 나온다. 연결이 꺼진 병원(`not_syncable`)은 시드가 돌지 않아 계속 403이다.
2. **꺾쇠를 빠르게 누르면 지나간 날짜마다 KOS 최신화가 한 번씩 돈다.** 잠금은 (병원, 날짜)마다라 서로 다른 날짜는 **동시에** 돈다. 날짜 하나가 「일정 1 + 구매 1 + 고객 × 2(시술권 · 카드) + 바뀐 카드 이력」이고 속도 제한(KosPacer)도 없다(be 「이슈 2」). 붐비는 날 앞뒤로 다섯 번 누르면 수백 회가 된다. 업체 쪽 속도 제한이나 오늘 회차 지연으로 나타날 수 있다. 화면 쪽에서 늦게 보내기(debounce)나 병원당 동시 1개 상한을 2루프에서 볼 만하다.
3. **다른 날짜 첫 화면은 빈 표일 수 있고, 최신화가 실패해도 아무 표시가 없다**(R30 · R19 2루프). kiq 실패(W-2)도 로그뿐이다. 데스크는 「그날 예약 없음」으로 읽을 수 있다.
4. **화면이 옛 날짜에 붙는 경우**(W-1). 주소 줄과 화면 날짜가 다르게 보이고, 다시 누를 때까지 그대로 남는다.
5. **오늘 회차 흔들림**(W-4). 다른 날짜를 열 때 같은 고객이 오늘도 오면 오늘 KOS 키 보충이 한 회차 건너뛸 수 있다. 시술 현황에서 새 방문이 10초 더 늦게 열에 들어가는 정도다. 교착이 나면 시술 현황 「동기화 멈춤」 근거가 한 회차 남는다.
6. **그룹이 빈 방문은 카드에서 조용히 빠진다**(`policies/reservations.py:245` · R20 전제). 키 보충이 실패한 오늘 방문이나 KOS에 그룹이 없는 일정이 그렇다. 필터 수에서도 빠진다.
7. **be 「해석 5곳」**: (a) 지난 날 시간 칸 회색의 끝 = 켜진 시간표 중 가장 늦은 운영 끝(없으면 24:00) (b) `open_min` = 켜진 시간표 중 가장 이른 시작 · 없으면 null(처음 세로 위치 맨 위) (c) 휴무 행 한쪽 끝이 null이면 무시 (d) 그룹 없음 · 지운 그룹 방문 = 카드와 수에서 뺌 (e) 시간표 시작이나 끝이 null이면 0 · 24:00. 모두 SPEC 문장과 부딪히지 않는다. 실물 KOS 데이터에서 (c) · (e)가 나오는지 본다.
8. **정원 글자**: 구역이 2개 이상인 그룹은 「30분」만 보인다(W-6). 데스크가 정원을 못 봐서 물어볼 수 있다.
9. **JS가 늦거나 실패하면 카드가 열 맨 위에 겹친다**(자리는 day.js가 놓음 — fe 「이슈 2」).

## 참고 (기존 부채 · 무관)

- `day/policies/interpret/chinese.py:14` opencc stub 없음(mypy) — 무관, 기존(fe 리포트).
- 병원 시간대가 병원마다가 아니라 전역 설정 `hospital_zone` 하나다 — 기존 `today_window`와 같아서 이번 변경 탓은 아니다.
- worker가 프로세스 1개(`deploy/compose.yaml:73 --workers 1`)라 날짜 최신화(상한 295초)가 오늘 10초 회차와 같은 event loop를 나눠 쓴다. 지금은 모두 async라 문제는 없다. W-4와 같이 본다.

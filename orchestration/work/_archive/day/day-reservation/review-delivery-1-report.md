# 리뷰 리포트 — day-reservation / delivery #267 · #268 · #269 (2026-11-23)

- 대상: CENTURION_DAY Delivery Issue #267(① 조회 · 권한) · #268(② 다른 날짜 최신화) · #269(③ 화면) — `gh issue view` 본문 · 숨은 metadata
- 기준: DAY-SPEC-006(stable · 커밋 `1870f68c` · PR #958) · 결정 R1 ~ R41 · planner 보고 `delivery-1-report.md` · `delivery-2-report.md` · CENTURION_DAY `origin/dev` `5ece25ea` `AGENTS.md`
- 판정 기준: FAIL = 구현 워커가 짐작해야 하는 빈칸 · 모순만. Issue · 레포는 고치지 않았다.

## 판정: FAIL

범위 합은 SPEC-006 과 맞다. 새어 들어온 것(쓰기 · 모달 · 근무표 · 앱 보내기 · 예약 요청 내용)도 없다. #268 의 C1 ~ C3 · R40 시험도 「조용히 건너뜀」 · 「중간 상태 보임」을 잡도록 적혀 있다.
그러나 **Issue 끼리 맞물리는 계약 세 개가 Issue 안에 없다.** planner 보고서(`delivery-1-report.md` §BE↔FE 계약)에만 있다. 구현 워커는 Issue 를 받으므로 짐작해야 한다(FD-1 ~ FD-3).
그리고 #267 의 수정 후보가 레포 계층 규칙과 부딪친다(FD-4).

---

## FAIL

### FD-1. 「폴링은 최신화 요청을 넣지 않는다」 — 폴링과 날짜 바꾸기를 서버가 구분할 방법이 어느 Issue 에도 없다
- #267 바뀌는 것 셋째 줄 · A2: 「다른 날짜는 열거나 바꿀 때 1회만 넣는다 · 다시 읽기(폴링)는 넣지 않는다」. #269 바뀌는 것 둘째 줄: 「날짜 바꾸기 = HTMX GET 조각 · 10초 조각 폴링」. 두 요청이 **같은 경로**(`GET /reservations?date=` + `HX-Request`)라는 것은 SPEC-006 API 표와 planner 보고서 경로 표가 같다.
- 그러니 ①은 폴링 요청과 날짜 바꾸기 요청을 가를 신호를 받아야 하고, ③은 그 신호를 실어야 한다. planner 보고서도 「구분이 필요 — 제안: `HX-Trigger` 값 또는 `poll=1` · ① · ③ 가 같이 정한다」고 적었다(`delivery-1-report.md:59` · `:94`). 그런데 그 내용이 #267 · #269 본문에 없다. 두 워커가 각자 다른 신호를 고르면 A2 를 통과해도 실물에서 폴링마다 KOS 최신화가 들어간다(R40 · R41 위반).
- 고칠 것: #267 · #269 에 같은 한 줄을 넣는다. 예: 「폴링 요청은 `HX-Trigger: reservation-poll`(또는 쿼리 `poll=1`)을 싣고, ①은 그 요청이면 최신화 요청을 넣지 않는다」. #267 A2 에 그 신호로 시험한다고 붙인다.

### FD-2. ① → ② 최신화 요청 입구(task 이름 · 인자)가 두 Issue 모두에 「계약 먼저」로만 적혀 있다
- #267 의존성: 「Delivery ② 의 최신화 요청 입구(task name · 인자) — 계약만 먼저 맞추고 병렬」. #268 의존성: 「Delivery ① 이 요청을 넣는 입구(task name · 인자 — 계약 먼저)」. 정작 이름 · 인자는 어느 쪽에도 없다.
- planner 보고서에만 있다: `sync_reservation_date_hospital(hospital_id: str, date: "YYYY-MM-DD")` · ①은 `kiq` 만 하고 기다리지 않음 · 중복 제거는 ② 안에서(`delivery-1-report.md` 「최신화 요청 입구」).
- CENTURION_DAY `AGENTS.md:131` 은 「task name 은 외부 계약으로 취급한다」고 한다. 병렬로 가면 두 워커가 서로 다른 이름을 고를 수 있다.
- 고칠 것: 두 Issue 에 같은 입구 계약을 넣는다 — task 이름(제안) · 인자(`hospital_id` · `date` 형식) · 「① 은 넣고 기다리지 않음 · 잠금 · 중복 제거는 ②」 · 「오늘 날짜는 넣지 않음」.

### FD-3. ① → ③ 화면 값(view model) 계약이 Issue 에 없다 — #267 A1 이 없는 절을 가리킨다
- #267 A1: 「SPEC-006 『화면이 읽는 칸』의 값을 **계약(아래 execution · BE↔FE 값)대로** 싣는다」. 그런데 #267 본문에는 「BE↔FE 값」 절이 없다(숨은 metadata 의 execution 에도 없다).
- #269 의존성: 「Delivery ① 의 view model 값 · 조각 id(계약 먼저 — **가짜 값으로 병렬**)」. 값 이름 · 모양이 없으면 가짜 값을 만들 수 없다.
- planner 보고서 view model 표(`date` · `is_today` · `axis` · `columns[]{capacity_text, gray_spans}` · `cards[]{start_min, end_min, stack_index, state, payment_due, tooltip}` · `filter` · `notice` · `reservation_request_title`)가 그 계약이다.
- 판정 위치도 계약에 따라 갈린다. 예: 「정원 글자 비움」은 ①의 `capacity_text` 가 빈 값인가, ③이 판단하는가. 「취소 · 노쇼 판정 순서」는 ①의 `state` 인가 ③인가. 「툴팁 글자」는 ①의 `tooltip` 인가 ③의 시안 문구인가. 이것이 정해지지 않았다.
- 고칠 것: view model 표를 #267(제공) · #269(소비) 본문에 같은 표로 넣는다. 조각 id `#reservation-main` 이 담는 범위(페이지 머리 날짜 · 표 · 오른쪽 패널)도 같이 넣는다.

### FD-4. #267 수정 후보 `backend/day/repositories/` — 레포 계층 규칙과 모순
- CENTURION_DAY `AGENTS.md:44` 「services — 세션 직접 사용, **repository 층 없음**」 · `:88` 「repository 층을 만들지 않는다」 · `:89` 「여러 행을 한 화면에 그리는 묶음 조회는 `queries/` 에 둔다」. 지금 `backend/day/repositories/` 디렉토리는 없다.
- 고칠 것: 수정 후보를 `backend/day/queries/`(새 예약 현황 묶음 조회) · `backend/day/services/reservations.py` 로 바꾼다. 이름은 `AGENTS.md:80-83` 「같은 파일 이름」 규칙(`routers/reservations.py` · `services/reservations.py`)을 따른다.

---

## WARN

### WD-1. 실물 e2e — 세 Issue 가 같은 문장 · 기대 결과가 없음 · 실제로는 셋 다 머지 뒤에만 가능
- 세 Issue 모두 「오늘 열기 · 다른 날짜 열기 · 같은 날짜를 두 창에서 동시에 열기」만 적었다. 무엇을 보면 통과인지가 없다.
  - 예: 다른 날짜 = 첫 화면은 이전 사본(빈 표 가능) → 다음 폴링에 채워짐.
  - 예: 동시 = KOS 일정 조회가 그 (병원, 날짜)에 1회 — 로그 · 횟수로 확인.
  - 예: 오늘 = 최신화 요청 0.
- 의존은 「계약 먼저 · 병렬」로 적혀 있는데, ①의 「다른 날짜 열기」 e2e 는 ②가 없으면 표가 계속 비고, ③의 e2e 는 ①이 없으면 돌 수 없다. 그러니 각 Issue 의 완료 조건이 사실상 셋 다 머지된 뒤에야 닫힌다. planner 보고서는 「③ 은 마지막 e2e 만 ① 뒤」라고 했지만 Issue 에는 없다.
- 고칠 것: e2e 에 기대 결과를 한 줄씩 넣는다. 각 Issue 에 「e2e 는 ① · ② · ③ 이 다 들어간 뒤(마지막 머지 Issue 에서 1회)」 같은 순서 조건을 적는다.

### WD-2. #268 A1 이 R26 범위보다 좁다
- 바뀌는 것 첫 줄 = 「일정 → KOS 키 보충 → 구매 · **시술권 · 선불카드**」(R26). A1 = 「방문 · 고객 · 작업 · 그룹 칸 · 구매」 — 시술권 · 선불카드가 빠졌다. 이 화면은 시술권 · 카드를 읽지 않지만, R26 은 「오늘 동기화와 같은 범위」다. → A1 에 넣거나 「화면이 읽는 구매만 확인」으로 범위를 밝힌다.

### WD-3. 필터 수를 누가 세는지
- #267 view model 에 「필터 수」가 있다(planner 표 `filter{total, counts}`). 반면 #269 는 「필터는 화면 안에서만(서버 조회 없음)」이고, SPEC-006 U-6 은 「이미 받은 카드로 세고 흐리게 한다」고 한다. 서버가 세어 넘기는 것도 「서버 조회 없음」과 모순은 아니다. 다만 ③이 다시 세면 두 수가 어긋날 수 있다. → 「수 = ① 이 넘긴 값 · ③ 은 다시 세지 않음」 또는 그 반대를 FD-3 의 표에 적는다.

### WD-4. 메뉴 링크를 두 Issue 가 다 가진다
- #267 수정 후보 `menu.py(HREFS reservation · reservation_board)`와 #269 target_delta 「아이콘 줄 「예약」 · 헤더 탭 「예약 현황」 링크」. → 한쪽(①의 `menu.py`)으로 정하고 ③은 「링크가 켜졌는지 e2e 확인」으로만 둔다.

### WD-5. 템플릿 조각 파일 이름
- #269 `templates/partials/reservation_*.html` ↔ `AGENTS.md:83` 「`templates/partials/reservations_*.html`」(복수). → 복수로 맞춘다.

### WD-6. spec-baseline:pending — 구현 시작 조건
- 세 Issue 모두 `spec-baseline:pending` · next = `prepare-spec-baseline` 이다. SPEC-006 이 Mediness main 에 들어가 재결속(contract_version 2)되기 전에는 구현 단계가 아니다(`delivery-2-report.md` 「재결속 조건」). Issue 본문 「검토할 부분」 첫 줄에 이미 적혀 있으니 결함은 아니다. 다만 FD-1 ~ FD-4 를 고치면 Target Delta · Acceptance 가 바뀐다. 그러면 재결속 때 「결과 계약이 같으면 재승인 없음」에 해당하지 않을 수 있다 — `scope_delta` · 새 승인이 필요한지 코디가 판단해야 한다.

---

## 볼 것별 확인

| 볼 것 | 판정 | 근거 |
|---|---|---|
| 1. 범위 합 = SPEC-006 · 빠진 것 · 넘친 것 | PASS | ① 조회 · view model · 권한 R31 · 메뉴 / ② R26 범위 · R40 잠금 · C1 ~ C3 · 오늘 제외 / ③ RV-01 ~ RV-41 · U-1 ~ U-7 · 공지 · 예약 요청 제목만(R32). 셋의 「이번에 하지 않는 것」에 쓰기 · 모달 · 예약 요청 내용 · 근무표 · 원내 현황 · 고객 검색 · 고객 등록(R1 ~ R5 · R15 · R33) · 낡음 표시(OQ-R21) · 오늘 화면 C1(R41 ⓐ) · 쓰기 큐 확인(R33) · 새 테이블. 새어 들어온 것 없음 |
| 2. R26 · R27 · R39 · R40 · R41 · C1 ~ C3 시험 | PASS(WD-2) | R39: #267 A2 「KOS 호출 0(테스트)」 · R40: #267 A2 「다른 날짜 1회 · 오늘 0」 · #268 A5 「동시 = 한 번」 · R41: #267 A2 「폴링은 안 넣음」(구분 방법은 FD-1) · C1: #268 A2 「최신화 중 다른 읽기가 그룹 빈 방문을 안 봄」 = 「중간 상태 보임」 시험 · C2: #268 A3 「오늘 10초 회차가 같은 병원 잠금을 잡고 있어도 안 건너뜀 · 실패면 중간 상태 없음」 = 「조용히 건너뜀」 시험 · C3: #268 A4 · R27: #268 A5(같은 (병원, 날짜) 한 번) · 오늘 회귀: #268 A5 「기존 테스트 그대로」 · 테스트는 실 PostgreSQL · Redis(#268 P4) |
| 3. ① ↔ ③ · ① ↔ ② 계약 | **FAIL** | 경로 · 조각 id 는 맞다(`GET /reservations` · `#reservation-main`). 폴링 구분(FD-1) · task 입구(FD-2) · view model(FD-3)이 Issue 에 없다 |
| 4. 실물 e2e · 의존 | WARN | e2e 세 경우는 셋 다 있다. 기대 결과 · 순서 조건이 없다(WD-1). 의존은 계약 순서만이다 — 맞다. 다만 계약이 Issue 에 없으니 FD-2 · FD-3 이 먼저다 |
| 5. #269 문구 짓기 금지 · 인라인 스크립트 0 · 손 CSS 0 | PASS | #269 A1 「문구를 짓지 않음」 · A2 「인라인 스크립트 0 · 손 CSS 0 — day.js 이벤트 위임 + data-* · medikit 토큰 · ui.html 매크로」 · `AGENTS.md:107-116` 「웹 화면」과 같다 |

## 직원이 실물에서 만날 자리

- (FD-1) 구분 신호가 어긋나면 다른 날짜 화면을 열어 둔 PC 마다 10초에 한 번 KOS 하루 일정 조회가 생긴다. R40 이 막으려던 부하다.
- (FD-2) task 이름이 어긋나면 ①이 넣은 요청을 ②가 받지 못한다. 다른 날짜가 계속 빈 표로 남고, 화면에는 아무 알림이 없다(낡음 표시는 2루프).

## 참고

- planner 보고서의 계약(경로 · view model · task 입구)은 내용 자체가 SPEC-006 과 맞다. 문제는 그것이 Issue 에 실리지 않은 것뿐이다.

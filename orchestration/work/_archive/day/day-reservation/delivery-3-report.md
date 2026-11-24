# delivery-3 결과 보고 — Delivery #267 · #268 · #269 고침(검수 review-delivery-1 FAIL 4 · WARN 6)

## 상태: done — 세 Issue contract_version 2 · 재승인 적용 · `delivery-plan:approved` · `spec-baseline:pending` 그대로

## Issue 마다 바뀐 절

| Issue | 바뀐 절 | 새 plan_digest(승인 대상) | 새 contract_digest | 승인 |
|---|---|---|---|---|
| [#267](https://github.com/MediSolveAIDev/CENTURION_DAY/issues/267) ① | 바뀌는 것 1 ~ 3 줄(경로 `routers/reservations.py` · V0 · 화면 값 = V1 ~ V4 · 계약 T · S) + 새 줄 계약 S · T · V0 ~ V4 · A1(V0 ~ V4) · A2(오늘 0 · 다른 날짜 T 1회 · `poll=1` 0 — 계약 S 로 시험) · A5(e2e 기대 결과 · 순서 조건) · 수정 후보(`queries/reservations.py` · `services/reservations.py` · `presentation/reservations.py` · `menu.py` 한 곳 — FD-4 · WD-4) · 의존 | `sha256:424ce42e73c8f299ef848c92fc6cf50abf0525ec2378e7946b023af54ac9de80` | `sha256:9d5f994493c5beac2e4b0f9c06a4cf4621ab66666cc8044635e32290f049fc21` | 재승인 적용 |
| [#268](https://github.com/MediSolveAIDev/CENTURION_DAY/issues/268) ② | 새 줄 계약 T · A1(방문 · 고객 · 작업 · 그룹 칸 · 구매 · **시술권 · 선불카드** — WD-2) · A6(e2e 기대 결과 · 순서 조건) · 수정 후보 task 이름 · 의존 | `sha256:6c4a7ba257e736038dbfc868f4b5e609c00eb6ff4d683ed87b2ce368904ad3f6` | `sha256:4ece6ae3b352f076dec0a9613109d0704fd51dd8da3e7a3aefdbb7b93982299a` | 재승인 적용 |
| [#269](https://github.com/MediSolveAIDev/CENTURION_DAY/issues/269) ③ | 바뀌는 것 2 줄(계약 S `poll=1` · push 안 함 · 필터 = V4 수 그대로 · now_min) · 3 줄(메뉴 링크는 ① — ③ 은 e2e 확인만 · WD-4) + 새 줄 계약 S · V0 ~ V4 · A3(V 가짜 값 렌더 테스트) · A4(e2e 기대 결과 · 순서 · 메뉴 링크) · 수정 후보 `templates/partials/reservations_*.html`(복수 — WD-5) · 의존 | `sha256:40b43608cba7077988d1ab6033de148f3857456dc4f5883cfcaf8436374b4f4e` | `sha256:1d70907bdaecba1d275dae4260a2cdf497f70c5fd30d8aa47ac48acedbc47207` | 재승인 적용 |

- 세 request 모두 같은 idempotency key · `contract_version` 1 → 2 · `scope_delta` = 「2026-11-23 Delivery 검수(review-delivery-1) FAIL 4 · WARN 6 반영 — 계약 명시(폴링 신호 S · task 입구 T · 화면 값 V0 ~ V4) · 수정 후보 이름(AGENTS.md 규칙) · e2e 기대 결과 · 순서 조건. 범위(무엇을 만드는지)는 그대로」.
- baseline 은 그대로 — `origin/main` `8aef9206036d076798242ca66abd30d644762180` + `spec-baseline:pending`(#958 머지 안 함).
- harness 흐름: `--plan`(planned · review-delivery-plan) → `--apply`(status `scope-delta-recorded` · 결과 계약이 바뀌어 새 plan_digest → **재승인 요구**) → 승인 receipt `{"decision":"approved","reviewer_type":"human","reviewer":"kknaksss","plan_digest":<새 digest>}` 적용(**재승인 적용** — 사용자가 이 Delivery 를 승인했고 이번 변경은 검수 반영 · 범위 같음 · 코디 지시) → status `plan-approved` · next = `prepare-spec-baseline`(human_gate false).
- 첫 `--plan` 은 `scope_delta` 를 배열로 넣어 schema 오류(exit 2 · 「Input should be a valid string」)로 끝났다 — 아무것도 바뀌지 않았고 문자열로 고쳐 다시 실행했다.
- gh 확인: 세 Issue 라벨 = `delivery-plan:approved` · `execution-plan:ready` · `spec-baseline:pending` · #267 · #268 본문에 task 이름 · #267 · #269 본문에 `poll=1` · 계약 V · `repositories` 없음 · #269 에 `reservations_*`.

## 계약 세 개 — 최종 문장(Issue 본문 그대로)

**신호 S(#267 · #269)**

> 계약 S(폴링 구분 — #267 · #269 같은 문장): 10초 폴링 요청은 쿼리 `poll=1` 을 싣는다(`GET /reservations?date=YYYY-MM-DD&poll=1` + `HX-Request` · 폴링 요소는 hx-push-url 을 쓰지 않음) · ① 은 `poll=1` 이면 최신화 요청을 넣지 않고 DB 사본만 돌려준다 · 날짜 바꾸기(꺾쇠 · [오늘] · 달력)는 `poll` 없이 보낸다. 고른 이유: HX-Trigger 헤더는 HTMX 가 누른 요소 id 를 싣는 칸이라 요소 id 에 묶이지만, 쿼리는 요소와 무관하고 로그 · 테스트에서 바로 보인다

**task 입구 T(#267 · #268)**

> 계약 T(최신화 요청 입구 — #267 · #268 같은 문장): taskiq task 이름 `day.sync_reservation_date_hospital`(기존 `tasks/emr.py` task 이름 꼴 · 이름 제안 — 외부 계약 AGENTS.md:131) · 인자 `hospital_id: str`(DAY hospital uuid 문자열) · `date: str`(병원 현지 날짜 `YYYY-MM-DD`). ① 은 오늘이 아닌 날짜를 열거나 바꿀 때(`poll` 없음) `kiq` 로 한 번 넣고 기다리지 않는다 · 오늘 날짜 · `poll=1` 요청은 넣지 않는다 · 같은 (병원, 날짜) 잠금 · 중복 제거 · 실패 처리는 ② 안에서 한다(① 은 모른다)

**화면 값 V(#267 제공 · #269 소비)**

> 계약 V0(조각 범위 — #267 제공 · #269 소비 같은 문장): HX 조각 `#reservation-main` = 페이지 머리 날짜 줄(날짜 · 꺾쇠 · [오늘] · [필터] 버튼과 팝오버) + 예약 표 + 오른쪽 패널(공지 / 예약 요청 제목). 셸(아이콘 줄 · 헤더)은 전체 페이지에만
>
> 계약 V1(화면 값 · 페이지): `date`(YYYY-MM-DD) · `weekday`(요일 한 글자) · `is_today`(bool) · `now_min`(오늘만 · 자정부터 분 · 아니면 null) · `axis`{`start_min`, `end_min`}(30분 단위 · 기본 08:00 ~ 24:00 · 축 밖 예약이면 ① 이 늘림) — 판정 위치 = ①
>
> 계약 V2(화면 값 · 열 `columns[]`): {`group_id`, `title`, `capacity` (int 또는 null — 살아 있는 구역이 1개면 그 정원 · 0개 · 2개 이상이면 null), `interval_minutes`, `gray_spans[]`{`start_min`, `end_min`}(운영 전 · 지난 시간 · 쉬는 시간 · 꺼진 요일 · 그룹 휴무를 합친 회색 구간)} — 정원 null 판정 · 회색 구간 계산 = ① / 「n명 / m분」 글자 조립 · capacity null 이면 「n명」 부분 비움 = ③(시안 문구)
>
> 계약 V3(화면 값 · 카드 `cards[]`): {`visit_id`, `group_id`, `start_min`, `end_min`, `stack_index`(같은 열 겹침 순서 · 취소 · 노쇼 뒤), `name`(한글 발음 없으면 이름), `nationality`(값 그대로 · 없으면 빈 문자열), `is_new`(bool), `state`(`reserved` · `reception` · `consultation_waiting` · `consultation` · `procedure_waiting` · `procedure` · `procedure_done` · `completed` · `canceled` · `no_show` — 예약 상태(취소 · 노쇼)를 먼저 보는 판정 = ①), `payment_due`(bool — 귀가 대기 ∧ 열린 구매 판정 = ①)} — 띠 색 · 툴팁 글자(예약 · 예약 취소 · 노쇼 …) · 취소 / 귀가 모양은 ③ 이 `state` 키로 시안대로 그린다(① 은 문구 · 색을 넘기지 않음)
>
> 계약 V4(화면 값 · 필터 · 패널): `filter`{`total`(취소 · 노쇼 제외), `counts`{`reserved`, `reception`(접수 + 상담 대기), `consultation`, `procedure`(시술 대기 + 시술 중), `procedure_done`, `completed`, `canceled`(취소 + 노쇼)}} — 수를 세는 곳 = ① · ③ 은 다시 세지 않고 이 값을 그대로 보이며 흐리게 하기만 화면 안에서 · `notice`{`items[]`{`content`}}(`released_at` 순 · null 제외 = ①) · 예약 요청 칸 제목 「예약 요청」은 ③ 템플릿 글자(① 은 넘기지 않음)
>

**e2e(세 Issue 같은 문장)**

> 실물 e2e 1회(로컬 · KOS 데모 지점 · 기대 결과): 오늘 열기 = 최신화 요청 0(로그 · task 큐로 확인) · 10초 폴링이 DB 사본만 다시 읽음 / 다른 날짜 열기 = 첫 화면은 이전 사본(빈 표 가능) · 최신화 요청 1회 → 다음 폴링에 그 날짜 카드가 채워짐 · 폴링 동안 최신화 요청 0 / 같은 날짜를 두 창에서 동시에 열기 = 그 (병원, 날짜) KOS 일정 조회 1회(로그 · 호출 수로 확인) · 두 창 모두 다음 폴링에 같은 사본. 순서 조건: e2e 는 ① #267 · ② #268 · ③ #269 가 모두 들어간 뒤 마지막으로 머지되는 Issue 에서 1회 돌리고 그 결과를 세 Issue 에 남긴다

## 검수 항목별

| 지적 | 반영 |
|---|---|
| FD-1 폴링 구분 | 계약 S — 쿼리 `poll=1`(이유: HX-Trigger 는 요소 id 칸 · 쿼리는 요소와 무관하고 로그 · 테스트에서 보임) · #267 A2 를 그 신호로 시험 |
| FD-2 task 입구 | 계약 T — `day.sync_reservation_date_hospital(hospital_id, date)` · ① 은 넣고 안 기다림 · 오늘 · poll 은 안 넣음 · 잠금 · 중복 제거 · 실패는 ② |
| FD-3 view model · 조각 범위 · 판정 위치 | 계약 V0 ~ V4 — 판정(정원 null · 회색 구간 · state 순서 · payment_due · 필터 수 · 공지 순서)은 ① · 문구 · 색(「n명 / m분」 조립 · 툴팁 글자 · 띠 색 · 「예약 요청」 제목)은 ③ 이 시안대로 |
| FD-4 repositories | `queries/reservations.py` · `services/reservations.py` · `presentation/reservations.py` · `routers/reservations.py`(AGENTS.md:80-89) |
| WD-1 e2e 기대 결과 · 순서 | 오늘 0 · 다른 날짜 이전 사본 → 다음 폴링에 채움 · 동시 = KOS 조회 1회 · 마지막 머지 Issue 에서 1회 · 결과를 세 Issue 에 |
| WD-2 #268 A1 | 시술권 · 선불카드 넣음(화면이 읽는 건 구매뿐이라고 밝힘) |
| WD-3 필터 수 | V4 — ① 이 세고 ③ 은 다시 세지 않음 |
| WD-4 메뉴 링크 | ① `menu.py` 한 곳 · ③ 은 e2e 확인만 |
| WD-5 partials 이름 | `reservations_*.html` 복수 |
| WD-6 재결속 재승인 | 이번에 결과 계약을 바꿔 재승인까지 적용했다 — 나중 SPEC 재결속(version 3 · 새 main SHA)은 결과 계약이 같으면 재승인 없음(requests.md) |

## 남긴 파일 (`delivery/`)

`request-*.json`(v2) · `plan-v2-*.json` · `apply-v2-*.json`(scope-delta-recorded) · `approval-v2-*.json` · `apply-v2-approved-*.json`(plan-approved). v1 파일은 그대로 둠.

## 문서

- `30-work.md` · `log.md` 변경 없음(Delivery 번호 그대로).

## 남은 것

- 세 Issue 모두 `prepare-spec-baseline` — SPEC-006 이 Mediness main 에 들어가면 같은 key · version 3 · 새 main SHA 로 재결속(결과 계약 같으면 재승인 없음) 뒤 구현.

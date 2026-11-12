# reviewer_doc add1 — DEC-011 · SPEC-008 0.3.0 · WORK-013 검수

- 대상: `10-decision/decision-011-ext-api-add1.md` · `20-spec/spec-008-product-ext-api.md` 0.3.0(§0 · §1.1 I6 · §2.1 add1 행 · §6.2 · §6.6 ~ §6.9 · §7.3 · §8 0.3.0 줄 · §9 T29 · T32 ~ T44 · 실물 확인 0.3.0 · 부록 D · E · 변경 이력) · `30-work/work-013-ext-api-add1.md` · README 네 행 · `work-index.md` 행
- 원천: `add1-spec-instructions.md` · `_RESUME.md` §2 2026-11-12 행 · planner Q1 ~ Q4 답(부록 E)
- 코드 기준: `kknaksss/cc-prototype` main `e0e4a16`(`git show e0e4a16:…` 로만 읽음 · 워크트리 파일은 열지 않음 — 병렬 구현 중)
- 제약 지킴: 파일 수정 0(이 리포트 1개만) · KOS 호출 0 · 커밋 0

## 종합 판정: **WARN** — FAIL 0 · WARN 6 · INFO 3

결정(D-01 ~ D-14)은 SPEC 에 빠짐 · 뒤틀림 없이 들어갔고, 브리프가 「특히 볼 것」으로 짚은 핵심 둘(정원 규칙 일치 · 404 바이트 일치)은 코드와 맞는다. WARN 은 모두 **SPEC 문구 · 시험 기준이 코드 사실과 어긋나 구현자가 그대로 따르면 틀리게 되거나 기존 시험이 깨지는 자리**다. 각 줄에 「구현자가 무엇을 다르게 해야 하나」를 붙였다.

---

## 1. 특히 볼 것 — 항목별 결과

| 항목 | 결과 | 근거 |
|---|---|---|
| 「목록에 있는 시각이면 정원으로 거절되지 않는다」= 예약 생성 정원 검사와 같은 규칙인가 | **맞다** | `create()` 는 `tx.slots(day)` 중 `start_at == start` 행을 (그룹 · 구역)으로 모아 `_pick_zone()` 이 `enabled_zones(g)` 를 order 순으로 돌며 `has_room` = 「행 없음 또는 `not is_full`」인 구역을 고른다(`service/reservations.py:779-787` · `:857-873`). 그 구역 행만 `is_full(capacity, count)` = `capacity·count 둘 다 있고 count ≥ capacity` 일 때 `409 slot_full`(`:818-819` · `domain/reservation_rules.py:154-155`). SPEC §6.6 5단계 합 ≥ 1 ⇒ 켜진 구역 중 `capacity − count ≥ 1` 인 행이 있음 ⇒ `has_room` 구역이 적어도 하나 ⇒ 고른 구역은 늘 `has_room` ⇒ `slot_full` 없음. `capacity` 있고 `count` null 인 행은 양쪽 다 「자리 있음」, `capacity` null 은 목록만 빼고(보수적) 예약은 허용 — 방향이 안전하다. 예약 경로는 `ensure_day` 를 부르지 않고 사본을 그대로 본다(`service/ext.py:235-258`) — D-12 의 「같은 사본」 전제가 코드와 맞다 |
| 고객 찾기 = DEC-010 규칙 · 404 바이트 같음 | **맞다**(구현이 `ExtService.find` 를 쓰면) | `find()` 가 D-15 ~ D-22 를 한 함수에 담고(`service/ext.py:163-190`), 조회 404 = `NotFound(NOT_FOUND, "customer_not_found")` · 문구 상수 `NOT_FOUND`(`:32` · `:200-201`). SPEC §6.7 1 · WORK-013 고정점이 「`find` 하나 · 같은 `NotFound`」로 묶어 둠. T39 가 바이트 비교로 고정 |
| 내보내는 칸에 메모 · 의사 · 담당자 | **섞이지 않음** | `previous_visits()` 는 `reservationMemo` · `consultationMemo` · `procedures[].doctors` · `resultRaw` · `zoneTitle` · `groupTitle` 을 싣는다(`service/reservations.py:206-215`). SPEC §6.7 은 그 함수를 **재사용하지 않고** 칸 4개(`date` · `start` · `result` · `procedures: string[]`)만 정했고, 「넣지 않는 칸」 목록 + T38 키 부재 단언이 있다. §6.8 도 `{reservationId, date, start, end, state}` 5칸 · 담당자 · 상담사 · 메모 · `sub` 제외 · T40 키 집합 단언 |
| KOS 호출 수 | **맞다** | 가능 시간대 = `_slots` 1번(`kos/reservation_sync.py:322-341` · 그룹이 비면 0번 — 2단계 503 이 먼저 막으므로 도달 안 함) · 과거 시술 · 예약 내역 = `get-visitors` 1 + `get-schedules-by-visitor` 1, 404 · 409 · 이름 검색 502 = 1. §6.9 표 · T43 |
| 시험 T 가 모든 오류 갈래를 덮는가 | **대체로 · 빈 곳 있음** → W6 |
| 기존 0.2.3 계약을 깨지 않는가 | **응답 계약은 안 깸 · 기존 시험 하나와 Swagger 문구 둘이 깨짐** → W3 · W4 |

## 2. 지적 표

| # | 판정 | 파일:줄 | 무엇이 틀렸나 | 근거 | 고칠 방향 · **구현자가 다르게 할 것** |
|---|---|---|---|---|---|
| W1 | **WARN(우선)** | spec-008 §6.7 2단계(493행) · §6.8 2단계(521행) · T39(671행) · work-013 WP-BE2(71행) | 「`data` 가 배열이 아님 → 502」로 적어, **응답이 `{}`(`data` 키 없음)인 경우도 502** 가 된다. KOS 공개 API 는 결과가 없을 때 `{}` 를 주는 사례가 확인돼 있고(같은 계열 `getTicketBundlesQuery` — KDA 182 · 258행), SPEC 자신도 시술권에서는 `{}` = 「없음」으로 정했다(§4.3 「결과 없음」). 직원 「이전 방문」도 `prev.get("data") or []` 로 키 없음을 빈 목록으로 본다(`service/reservations.py:614-615`). 이대로면 **일정이 하나도 없는 고객**(예약 없이 등록된 고객)이 `visits: []` · `reservations: []` 대신 `502` 를 받는다 — D-14 계열 「없음 ≠ 실패」가 거꾸로 깨진다 | KDA 182 · §4.3 · `service/reservations.py:614-615` | SPEC: §4.3 과 같은 규칙으로 — 「`data` 키 없음(`{}`) · `data: []` = 일정 없음 → `[]` / `data` 가 있으면서 배열 아님 = 502」. T39 에 `{}` → `200 visits: [] · reservations: []` 한 줄 더함. **구현자**: `resp.get("data", [])` 로 읽고 `isinstance(list)` 아니면 502(지금 `lookup` 시술권 `service/ext.py:210-212` 와 같은 꼴). `_data_list` 를 그대로 쓰지 말 것 |
| W2 | WARN · DEC 질문 | spec-008 §6.7 3단계 · §6.8 3단계 · DEC-011 D-03 · D-04 · D-13 | KOS 일정 원소의 **`deleted`** 를 어떻게 다룰지 없다. 일정 모양에 `deleted` 칸이 있고(KDA 219행), 사본 쓰기는 `deleted` 일정을 건너뛴다(`kos/reservation_sync.py:156` `apply_schedule`). 반면 직원 「이전 방문」은 거르지 않는다(`previous_visits`). 예약 내역에서 지워진 일정이 `state: reserved` 로 나가면 연동처는 「살아 있는 예약」으로 읽는다. `get-schedules-by-visitor` 가 지워진 일정을 돌려주는지는 확인된 사실이 없다 | KDA 215-223 · `kos/reservation_sync.py:156` · `service/reservations.py:192-217` | **DEC 질문**(코디 · 정책): 「`deleted: true` 일정은 두 목록에서 뺀다(사본 쓰기와 같은 규칙)」인가, 「직원 이전 방문과 같이 그대로」인가. **구현자**: 답이 오기 전에는 거르는 코드를 넣지 말고 한 곳(고르기 함수)에서만 판단하게 둘 것 — 답이 「뺀다」면 3단계 조건 한 줄로 끝나게 |
| W3 | **WARN(기존 시험 깨짐)** | spec-008 §8 「시험 고침」(622행) · T29(661행) · work-013 WP-BE3(72행) | 0.2.3 의 `tests/test_ext_docs.py` 마지막 단언 = 「`/api/ext` 모든 operation 의 parameters 이름 집합 == `{"X-Api-Key"}` 이고 전부 header」. 새 `GET /api/ext/availability` 의 질의 `date` 가 들어오면 **이 단언이 깨진다**. SPEC 은 `OPS` 여섯 · `n_ops - 5 - 6` 만 고치라 하고 이 단언은 말하지 않는다. 이 단언의 뜻(이름 · 이메일이 경로 · 질의에 없음 — D-24 · DEC-011 D-06)은 지켜야 한다 | `tests/test_ext_docs.py`(e0e4a16) 끝 4줄 | SPEC §8 「시험 고침」에 한 줄: 「parameters 단언을 `X-Api-Key`(header) + `GET /api/ext/availability` 의 `date`(query) 하나로 넓힌다 — 그 밖 query · path 칸 0」. **구현자**: 단언을 지우지 말고 `date` 를 그 operation 에만 허용하도록 고칠 것(`name` · `email` 이 query 에 생기면 실패해야 한다) |
| W4 | WARN | spec-008 §8 앱 설명(618행) · 엔드포인트(0.3.0)(623행) · work-013 WP-BE3 | 「경로 셋 → 여섯」만 적었는데, 코드에는 「셋」이 두 군데 더 있다: `openapi_docs.py:85` 「키당 최근 60초 60번(**세 경로 합산**)」 · `api/ext.py:100` `EXT_RATE` 「(**세 엔드포인트 합산**)」. `EXT_RATE` 는 `COMMON` 으로 새 셋의 429 표에도 그대로 붙는다 → 새 경로 Swagger 가 「세 엔드포인트 합산」이라고 틀리게 말한다(§7.3 · DEC-011 D-01 은 여섯 합산) | `openapi_docs.py:77` · `:85` · `api/ext.py:99-101` | SPEC §8 에 「`세 경로 합산` · `세 엔드포인트 합산` 문구도 여섯으로(또는 숫자 없이 「외부 경로 전부 합산」)」. **구현자**: `git grep -n "셋\|세 경로\|세 엔드포인트" app/` 로 전부 세고 고칠 것 · T29 에 429 줄 「여섯」(또는 「전부」) 단언 하나 |
| W5 | WARN | spec-008 §6.6 1단계(454행) · 오류 표(479행) · T34(666행) · work-013 WP-BE1 | 「`date` 없음 = FastAPI 칸 검증 400」과 「message = `date: <이유>`」가 **같이 성립하지 않는다**. 검증 처리기는 message 를 `".".join(loc)` 로 만든다(`main.py:120-124`) → 질의 칸이 빠지면 `query.date: Field required` 다(본문 칸이 `body.name: …` 인 것과 같은 규칙). T34 가 「`date` 없음 → message `date: …`」를 단언하면 실패한다. 또 `date` 를 pydantic `date` 타입으로 받으면 `20261105` 같은 숫자 문자열을 lax 파싱이 받아들일 수 있어 SPEC 의 「`parse_day` 와 같은 검사」와 어긋난다 | `main.py:120-124` · `domain/reservation_rules.py:51-60` | SPEC: 둘 중 하나로 정한다 — (가) 없음은 `query.date: …`(지금 규칙 그대로)로 적고 T34 단언을 「`date` 없음 = message 가 `query.date:` 로 시작」으로, 나머지(꼴 · 범위)는 `date: …` / (나) 칸을 `str` 필수로 받고 꼴 · 범위만 `date: …`. 어느 쪽이든 **구현자**: `date: str = Query(...)`(pydantic `date` 타입 금지)로 받고 꼴 검사는 `parse_day` 와 같은 10글자 + `fromisoformat` — 단 `parse_day` 의 「빈 값 = 오늘」 갈래는 타지 않게 빈 문자열을 먼저 400 으로. (가)가 지금 규칙과 맞아 권함 |
| W6 | WARN | spec-008 §9 T34 ~ T44 | 오류 갈래 중 시험 줄이 없는 것: ① 가능 시간대 `502` 의 「KOS 설정 없음(`sync`/runtime 없음)」 · KOS `4xx` · `401` 갈래(T36 은 5xx · 배열 아님만) ② 새 두 경로의 **이름 검색 실패 → 502**(T39 는 일정 읽기 실패만) ③ 새 셋의 `405`(예 `POST /api/ext/availability`) · `500` 공통 줄이 Swagger 표에 붙는지(T29 는 `OPS` 루프로 덮일 수 있으나 T44 행에 명시 없음) ④ W1 의 `{}` · W2 의 `deleted`(답이 나면) | §6.6 오류 표 · §6.7 오류 · `api/ext.py:111` `COMMON` | SPEC: T36 에 「runtime 없음 → 502 · KOS 호출 0」, T39 에 「이름 검색 5xx → 502 · 일정 읽기 0번」, T44 에 「`POST /api/ext/availability` → 405 `http_error`」. **구현자**: 새 세 operation 에 `responses=errors(*COMMON, …)` 를 빠짐없이 붙이고, 위 갈래를 시험에 넣을 것(코드가 갈래를 공유하더라도 경로마다 1줄) |

## 3. INFO (고치지 않아도 계약은 선다)

| # | 자리 | 내용 |
|---|---|---|
| I1 | `30-work/README.md` WORK-012 행 | 「draft (2026-11-11 · 문서만 · 코드 미착수)」 — 실제는 main `e0e4a16` 으로 머지 · 배포됐다(WORK-013 39행도 「이미 배포됐다」). WORK-012 본문 frontmatter 도 `status: draft` 라 행 자체는 본문과 맞지만, 마감 때 같이 고칠 자리로 적어 둔다 |
| I2 | §6.6 3단계 · WORK-013 주의 87행 | `refresh_slots` 는 날짜 잠금(`ensure` 의 `_locks`) 밖에서 `replace_slots` 를 한다. 직원 화면의 `fetch_day` 가 먼저 KOS 를 읽고 늦게 쓰면 더 오래된 슬롯으로 덮일 수 있다. DEC-011 이 받아들인 「동시 요청 경합」 범위 안이라 WARN 아님. 구현자가 원하면 `refresh_slots` 도 같은 날짜 잠금 안에서 돌리면 줄어든다(비용 변화 없음) |
| I3 | §6.7 · WORK-013 주의 90행 | 과거 시술 · 예약 내역은 `_keep` 을 부르지 않는다(조회 §6.4 는 부름). 그래서 외부 예약 없이 이 두 경로만 쓴 고객은 ccc `customer` 사본이 안 생긴다 — 응답에 `customerId` 가 없으므로 계약 문제는 없다. T39 끝의 「고객 · 예약 사본 행 수 그대로」가 성공 갈래까지 뜻하는지 404/409/502 갈래만인지 읽기에 따라 갈린다 — WORK-013 WP-BE2 완료 조건(「요청 앞뒤 같음」)이 성공 갈래까지라 그쪽을 따르면 된다 |

## 4. DEC 대조 (부록 D 를 믿지 않고 본문으로)

| DEC-011 | SPEC 본문 | 결과 |
|---|---|---|
| D-01 공유(인증 · 제한 · 기록 · no-store · tag · 오류) | §6.2 머리 「여섯 경로」 · §7.3 「여섯을 합쳐」 · §8 tag · T44 | 맞음(문구 「셋」 잔여 → W4) |
| D-02 기본 그룹 하나 · 간격 칸 · 0 뺌 · 지난 시각 뺌 · 같은 규칙 | §6.6 2 · 4 · 5 · 「같은 규칙인 까닭」 · T32 · T33 · T37 | 맞음 — 코드로 확인(§1 첫 행) |
| D-03 과거 · 최신 순 · 날짜 · 시작 · 결과 · 시술 이름 · 메모 · 의사 없음 | §6.7 3 · 4 · 응답 표 · 「넣지 않는 칸」 · T38 | 맞음(`{}` → W1 · `deleted` → W2) |
| D-04 오늘(KST) 이후 · 오름차순 · 상태(취소 포함) | §6.8 3 · 4 · T40 | 맞음 |
| D-05 고객 찾기 = DEC-010 · 404 바이트 · 2+ 409 | §6.7 1 · §6.8 1 · T39 | 맞음 |
| D-06 이름 · 이메일 본문 POST | §6.6 요청(날짜만 GET) · §6.7 요청 · T42 | 맞음(Swagger 단언 → W3) |
| D-07 경로 셋 | §6.6 ~ §6.8 머리 · 지시 파일 코디 기본값과 같음 | 맞음 |
| D-08 오늘 ~ 90일 · 그 밖 400 | §6.6 1 · T34 | 맞음(message 꼴 → W5) |
| D-09 설정 빔 · 그룹 없음 · 구역 0 = 503 · KOS 전 | §6.6 2(예약과 같은 검사 · `service/ext.py:235-242`) · T35 | 맞음 — 검사 순서 400 → 503 → KOS 도 일관 |
| D-10 50건 | §6.7 4 · T38(55건 → 50) | 맞음 |
| D-11 후보 · 남은 자리 · 행 없는 구역 뺌(Q1) | §6.6 4 · 5 · T32 | 맞음 — `open_spans`(`reservation_rules.py:108-117`) · `lines` 경계(`:133-138`) 확인. T32 기대값(10:00 ~ 12:30 · 14:00 ~ 19:30) 계산 맞음 |
| D-12 요청마다 슬롯 1번 · 공유 사본 · 502(Q2) | §6.6 3 · T36 · §6.9 | 맞음 — 본문이 `fetch_day` 와 같은 `_slots(groups=present 전부, day_range)` 라 다른 그룹 행을 지우지 않음 확인(`replace_slots` 는 그날 전 그룹 DELETE — 그래서 「전부」가 필수인데 SPEC 이 그렇게 적었다) |
| D-13 예약 내역 칸 · id = 사본 있으면 · 상태 = 2계층(Q3) | §6.8 5 · 응답 표 · T40 | 맞음 — `state_of(reservation.status, sch.flowStep)` 가 사본 쓰기(`reservation_fields` `:128`)와 같은 원천 · `reservation_id_of`(`repo.py:538-540`) · `resources_of` 정렬 첫 묶음(`:80-98`) 확인 |
| D-14 오늘 겹침 그대로 · 적음(Q4) | §6.7 · §6.8 「오늘 겹침」 · §8 · T41 | 맞음 |
| 원천: 지시 「코디 기본값」 4개 · `_RESUME` §2 2026-11-12 행 | DEC-011 D-07 ~ D-10 「코디 기본값」 표기 · D-11 ~ D-14 「planner 질문 Qn」 표기 | 맞음. DEC 에 없는 정책을 SPEC 이 새로 만든 곳 없음 |

**코드 규약 줄 확인**(e0e4a16): `service/ext.py:235-242` · `:163-190` · `:198-203` / `kos/reservation_sync.py:283-284` · `:322-341` · `:80-99` / `repository/repo.py:547-554` · `:538-540` / `service/reservations.py:82` · `:206` · `:207` · `:212-215` · `:593-594` · `:818-819` · `:827` · `:843-847` · `:847-851` · `:857-871` · `:905` · `:925` / `domain/reservation_rules.py:13-22` · `:41-47` · `:51-60` · `:103-117` · `:133-138` · `:154-155` · `:333` · `:336-340` / `api/ext.py:119-169` — 모두 그 줄에 적힌 것이 있다. (`main.py:117-121` 은 e0e4a16 에서 `:120-124` 로 밀렸으나 앞 판 절의 `c9f30ac` 기준 줄이라 지적하지 않음.)

## 5. 조용히 통과하는 자리

- **W1** — 일정 없는 고객의 `{}` 가 502 로 나가면, 연동처는 「KOS 장애」로 읽고 재시도한다. 시험 가짜 KOS 는 늘 `{"data": [...]}` 를 주므로(`tests/fake_kos.py:313-316`) **시험은 전부 통과하고 실물에서만 터진다.** WORK-013 실물 확인 ③ 은 「email 이 채워진 데모 고객」이라 일정이 있는 고객일 가능성이 높아 거기서도 안 걸린다
- **W2** — 지워진 일정이 예약 내역에 `reserved` 로 나가는 것은 오류 응답이 아니라 200 이라 누구도 알아채지 못한다
- **W3** — 단언을 「고쳐서 통과」시킬 때 지워 버리면 D-06(이름 · 이메일 질의 금지)을 지키는 유일한 Swagger 시험이 사라진다
- **W4** — Swagger 429 줄의 「세 엔드포인트 합산」은 틀린 문서인데 시험이 문구를 보지 않아 통과한다
- 이름 · 이메일 · 키 원문이 새는 틈: 새 세 경로는 기존 미들웨어(`ext_call` 은 경로 틀 · code 만) · `DropQueryString`(접근 로그 질의 제거 · `main.py:55-64`)를 그대로 탄다 — 새 틈 없음. 가능 시간대에 연동처가 `?name=` 을 붙여도(T42) 접근 로그에서 질의가 지워진다
- 「없음」과 「특정할 수 없음」으로 어느 쪽이 틀렸는지 새는 틈: 새 두 경로는 `find` 를 그대로 쓰고 404 · 409 이후 KOS 를 더 부르지 않으므로(응답 시간 차도 조회와 같음) 새 틈 없음

## 6. WORK-013

- WP 순서(BE1 → BE2 → BE3 → REVIEW → E2E-LOCAL → DEPLOY → E2E-PROD) · 한 워커 한 브랜치 · 부분 검증 명령 · 전체 `pytest` 는 BE3 끝 1번 — 규칙(`feedback_verify_scope_per_phase`)과 맞다. 명령에 쓴 시험 파일(`test_ext_reserve.py` · `test_resv_board.py` · `test_ext_lookup.py` · `test_resv_detail.py` · `test_ext_auth.py` · `test_ext_docs.py` · `test_openapi_docs.py`)은 e0e4a16 에 모두 있다
- 끝 조건에 데모 KOS 실물 호출(WP-E2E-LOCAL ① ~ ④ · 재기동 먼저) · 운영 호스트 확인(WP-E2E-PROD)이 있다
- 고칠 것: WP-BE1 완료 조건 · 검증에 W5 · W6 ①, WP-BE2 에 W1 · W6 ②, WP-BE3 에 W3 · W4 를 더한다. WP-E2E-LOCAL ③ 에 「일정이 없는 데모 고객이 있으면 그 고객으로 1번(`{}` 확인)」을 권한다(W1 실물 확인 — 없으면 건너뜀으로 적기)

## 7. public grep

DEC-011 · SPEC-008 · WORK-013 에서 이메일 꼴 = `a@example.com` 자리표시뿐 · 24자 이상 hex · UUID · 토큰 · 비밀번호 꼴 0 · 실명 0 · KOS id 값 0. `msg_ad6deebe3459` 는 orca 메시지 id(비밀 아님).

## 8. DEC 질문 (결정하지 않음 — 코디에게)

- **Q-add1-A**(W2): `get-schedules-by-visitor` 가 `deleted: true` 일정을 주면 과거 시술 · 예약 내역에서 뺄 것인가(사본 쓰기 `apply_schedule` 과 같은 규칙), 직원 「이전 방문」처럼 그대로 둘 것인가.

---
type: work
id: WORK-014
title: "외부 연동 API 3차(charty 1차 상담) — KOS0 이력 · 모양 확인 → BE1 lookup 고침 · 열람 헤더 → BE2 예약 상세 → BE3 접수 목록 → BE4 쓰기 셋 → BE5 병원 · 직원 → BE6 Swagger · 회귀 → REVIEW → 로컬 데모 실물 → 배포 → 운영 실물"
status: done
product: cc-prototype
feature: procedure
work_type: enhancement
owner: kknaks
progress: 0
created_at: 2026-11-16
updated_at: 2026-11-16
tags:
  - product/cc-prototype
  - feature/procedure
  - doc/work
  - status/draft
links:
  baselines: []
  decisions:
    - "[[decision-012-ext-api-charty1|DEC-012]]"
    - "[[decision-011-ext-api-add1|DEC-011]]"
    - "[[decision-010-product-ext-api|DEC-010]]"
  specs:
    - "[[spec-008-product-ext-api|SPEC-008]]"
    - "[[spec-005-reservation-board|SPEC-005]]"
  works:
    - "[[work-013-ext-api-add1|WORK-013]]"
    - "[[work-012-product-ext-api|WORK-012]]"
  releases: []
  related: []
sources:
  - "para/projects/summer-star/cc-prototype/20-spec/spec-008-product-ext-api.md (0.4.6 · §3.5 · §3.6 · §4.3 · §4.4 · §6.4 · §6.9 ~ §6.18 · §8 · §9 T48 ~ T73 · 부록 F · G)"
  - "para/projects/summer-star/cc-prototype/10-decision/decision-012-ext-api-charty1.md (D-01 ~ D-47)"
  - "orchestration/work/ext-api-charty1/review-doc-r1.md (문서 검수 r1 — 0.4.1 에서 반영)"
  - "orchestration/work/ext-api-charty1/review-doc-r2.md (문서 검수 r2 — 0.4.2 에서 반영)"
  - "orchestration/work/ext-api-charty1/research-charty1-sources.md · research-clinic-staff.md · research-har-history-hospital.md"
  - "cc-prototype procedure/back origin/main 0a58aba (읽기만 — 대상 파일 · 줄 · tests/ 파일 이름)"
---

# 외부 연동 API 3차(charty 1차 상담) — 빌드 계획

계약은 **SPEC-008 0.4.6** 에 있다(§3.5 · §3.6 · §4.3 · §4.4 · §6.4 · §6.9 ~ §6.18 · §8 · §9 T48 ~ T73). 이 문서는 빌드 순서만 적고 계약을 다시 쓰지 않는다. 결정은 DEC-012(D-01 ~ D-47)다. 공유 규칙(인증 · 제한 · 기록 · 오류)은 DEC-010 · WORK-012 · WORK-013 으로 이미 운영 중이다(origin/main `0a58aba`). 화면은 없다.

## Meta

- **진행**: 문서만 있다. 코드는 아직 손대지 않았다. progress 0
- **착수 전 게이트**: ~~SPEC-008 부록 G Q1 ~ Q14 답~~ (2026-11-16 답함 → DEC-012 D-24 ~ D-38 · SPEC 0.4.1). 부록 G Q15 · Q16 도 같은 날 답함(→ DEC-012 D-39 · D-40). Q17 도 같은 날 답함(→ DEC-012 D-41). **남은 질문 없음** — ~~남은 게이트는 KOS0 판정(BE3 · BE5 앞)뿐이다~~ (2026-11-16 KOS0 완료 · 판정 D-16 그대로 · 휴무 칸 D-43) — **남은 게이트 없음.** BE3 · BE5 도 착수할 수 있다
- Covers spec: SPEC-008 0.4.6. 0.3.3 까지의 계약(여섯 경로)은 lookup 의 칸 **추가**만 하고 바꾸지 않는다(DEC-012 D-03). lookup 의 행동 변화는 SPEC 변경 이력 0.4.0 · 0.4.1 · 0.4.2 에 적힌 것뿐이다(사용 중 묶음 · 선불카드 실패 = 200 + `partialErrors` · 요청 스키마 required · 갈래 오류 message). 헤더를 읽지 않는 다섯 기존 경로는 무엇도 바뀌지 않는다
- 코드 레포: `kknaksss/cc-prototype` — 범위는 **`procedure/back/**`** 하나다. front · app 은 건드리지 않는다
- **infra 없음**: 새 env 가 없다(열람 헤더 · `clinicId` 는 코드 상수 · 새 표 하나는 앱이 시작할 때 만든다). ingress 변경도 없다(`/api/ext/…` 안)
- base: 지금 main(`0a58aba` 이후 운영본). 워크트리 · 브랜치는 코디가 정한다
- 워커: backend(KOS0 · BE1 ~ BE6 · 한 브랜치에서 차례로) · reviewer · 코디(실물 확인 · 배포)
- **검증 규칙**: WP 마다 **그 WP 의 시험만** 돌린다. 전체 `uv run pytest -q` 는 **BE6 끝에 한 번** 돌린다
- **실물 e2e 없이 done 금지**: 데모 KOS 로 SPEC-008 §9 「실물 확인(0.4.0)」(0.4.3 판) ⓪ ~ ⑥ 을 실제로 부른다(WP-E2E-LOCAL). 쓰기 셋은 **시험 고객의 시험 예약에만** 하고 **끝나면 원래 값으로 되돌린다**. 운영 호스트에서 연동처 키로 읽기 경로를 1번씩(WP-E2E-PROD)
- public 레포다 — 리포트 · 커밋 · 시험 데이터에 키 · 실명 · 이메일 · 연락처 · KOS id · 테넌트 id · 병원 이름 값을 쓰지 않는다. 시험 값은 `<이름>` · `a@example.com` 꼴로만 쓴다

## 계약 고정점 (WP 사이에서 바뀌면 멈추고 코디에게)

| 고정점 | SPEC-008 | 쓰는 WP |
|---|---|---|
| 경로 일곱 · 메서드 · 경로 칸 이름(`reservationId` · `customerId` · `clinicId`) · board 를 상세보다 먼저 등록 | §6.11 ~ §6.17 머리 | BE2 ~ BE5 |
| lookup — 두 갈래 중 하나(갈래 오류 message `body: …`) · 기존 칸 그대로 · `inUseCount` · `prepaidCards` · `partialErrors` 더함 · 사용 중 묶음 나옴 · 선불카드 실패 = `200` + `prepaidCards: null` | §4.3 · §4.4 · §6.4 | BE1 |
| **과거 시술 · 예약 내역 본문 모델 `ExtCustomerRequest` 는 지금 칸 · 검증 그대로**(`name` · `email` 필수 · `customerId` = 모르는 키 400 · message 꼴 그대로 · Swagger `required` 그대로) — lookup 새 모델과 **상속을 끊는다** | §6.4 「요청 모델을 따로 둔다」 · T71 ⓐ ⓑ ⓒ | BE1 |
| 열람 헤더 `X-Ext-Staff-Id` — **다섯 경로에만**(lookup = 틀리면 없는 것 · 상세 · 쓰기 셋 = 틀리면 400) · 꼴 `[A-Za-z0-9._-]` 1 ~ 64 · `event_log` `ext_view`(`actor` = `ext:<연동처>[:<직원 id>]`) · `ext_call` 무변경 | §3.5 · §6.10 | BE1 · BE2 · BE4 |
| 쓰기 행위자 `ext:<연동처>:<직원 id>` · KOS 먼저 · 새 type `order_memo` · `consultation_memo` | §3.5 · §6.13 ~ §6.15 | BE4 |
| 처음 상담 대기 표 `consult_wait_first`(`first_at` null = 시도 행 · `checked_at` · `last_failed` · `retries` · `wait_called` · `final_tried`) · 대상 = 접수 뒤 일정 전부 · 찾은 값만 굳힘 · **다시 부르기는 사건 때만**(처음 봄 · 대기 새로 봄 · 귀가 뒤 · 실패 재시도 5분 뒤 ≤ 3) · 시도 예약(고르는 순간 먼저 적음) · 요청당 상한 10 · 칸 모양(null 허용) | §3.6 · §6.11 4 | KOS0 · BE3 |
| 상담 거침 판정 = 함수 하나(직원 `_flow` 와 외부 board 가 같이 부름 · board 도 `after` 문을 먼저 거침) | §6.11 3 | BE3 |
| 부분 실패 = `partialErrors` · board 는 502 없음 | §6.11 · §6.12 | BE2 · BE3 |
| 새 오류 code = `reservation_not_found` · `clinic_not_found`(그 밖은 지금 code — `reservation_gone` · `customer_not_found` · `kos_rejected` · `kos_unavailable` · `invalid_request`) | §6.12 · §6.17 | BE2 · BE4 · BE5 |
| 경로별 KOS 호출 수 | §6.9 | 전부 |

## Work Packages

| WP | 내용 | 계약 | 워커 | 대상 파일(범위) | 완료 조건 | 검증 명령(부분) | 상태 |
|---|---|---|---|---|---|---|---|
| **WP-KOS0** | **데모 KOS 확인(조회만 · 쓰기 0)** — ① 내부 `schedule/v1/queries/get-schedule-event-logs {scheduleId}` 를 **상담 대기를 거친 데모 일정 1건**(가능하면 상담 대기를 두 번 거친 일정도 1건)에 불러 응답 키 트리 · `eventType` 값 · `payload`(JSON 문자열)의 `flowStep` 꼴(숫자 · 문자열)과 `CONSULTATION_WAITING` 대응 · 같은 단계 반복이 원소 둘로 남는지 · `raisedDateTimeUtc` 꼴을 본다 ② 내부 `get-default-days-off {startDateTime, endDateTime}`(90일) 원소 모양 → 낼 칸 후보(날짜 · 이름 정도 · KOS id 빼고) ③ 공개 선불카드 요약 조회 — **카드가 있는 고객** 1명(데모 고객 중 카드가 있는 사람 · 없는 고객이면 빈 배열만 보므로 다시 고른다) — `remainingBalance` · `remainingPoint` 의 `balance` · `total` 이 금액 객체 `{value, currency}` 인지 ④ 내부 `ticket/v1/queries/get-ticket-bundles` 1명 — 다 쓴 · 다 취소된 묶음(`AVAILABLE` · `IN_USE` 0장)을 주는지(건수만). 내부 토큰은 지금 `KosClient` 가 받는 방식 그대로(시스템 계정). 원 응답은 레포 밖(스크래치)에만 두고 리포트에는 **키 · 꼴 · 건수만** | SPEC-008 §6.11 4 · §6.16 · §4.4 · §4.3 · DEC-012 D-16 · D-17 · D-27 | backend | 코드 변경 0(조회 스크립트는 레포 밖) | 리포트에 ① ~ ④ 의 모양 + **판정 한 줄**: 「D-16 그대로」 또는 「D-17 대안」 + 휴무 낼 칸 후보. 코디가 그 판정으로 DEC-012 · SPEC-008(§6.11 4 · §3.6 · §6.16 `daysOff` · §4.4 · T50 가짜 응답) 고침 줄을 넣은 뒤 BE3 · BE5 를 발주한다 | — | **완료**(2026-11-16 · `kos0-report.md` · 판정 = D-16 그대로 · DEC-012 D-42 ~ D-44 · SPEC 0.4.3) |
| **WP-BE1** | **lookup 고침 · 열람 헤더** — 요청 갈래(`customerId` 만 · `name` + `email` 만 · 섞이면 400) · `customerId` 갈래(사본 `kos_id` → 내부 `get-visitor` 1 → `upsert_customer` · 없으면 이름 갈래와 같은 404 본문) · 시술권 내부 `ticket/v1/queries/get-ticket-bundles {visitorId, sort}` · 거르기(`AVAILABLE` 또는 `IN_USE` 1장 이상) · `inUseCount` · 선불카드 공개 1번(시술권과 `asyncio.gather`) · `prepaidCards[]` · 선불카드 실패 → `200` + `prepaidCards: null` + `partialErrors` · lookup 새 요청 모델(세 칸 선택 + 갈래 검사) — **`ExtCustomerRequest` 와 상속을 끊고 그 모델은 지금 칸 · 검증 그대로** · 갈래 오류 message `body: …` · 열람 헤더 의존성 **둘**(꼴 검사 함수 하나 — lookup 용 = 틀리면 없는 것 · 새 경로 용 = 틀리면 400 · **lookup 에만 단다** · 기존 다섯 경로에 달지 않는다) · `ext_view` 쓰기(200 일 때만 · `payload` · `actor` §3.5) | SPEC-008 §3.5 · §4.3 · §4.4 · §6.4 · §6.10 | backend | `procedure/back/app/{api/ext.py,service/ext.py,schemas/ext.py}` · `tests/test_ext_lookup.py`(공개 → 내부 시술권 · 비용 2 → 3 · 키 집합만 고침) · `tests/test_ext_lookup2.py`(새) · `tests/test_ext_history.py`(T71 ⓐ ⓑ ⓒ 더함 · 기존 단언 그대로) · `tests/fake_kos.py`(내부 시술권 · 선불카드 · `get-visitor` 응답을 시험이 지정) | §9 T48 ~ T52 · T53 중 lookup 몫(T52) · T69(lookup 부분) · T71 의 헤더 갈래(기존 다섯 경로에 이상한 헤더 → 같은 응답) 통과 · 기존 lookup 시험은 위 세 단언 말고 그대로 통과 | `uv run pytest -q tests/test_ext_lookup.py tests/test_ext_lookup2.py tests/test_ext_auth.py tests/test_ext_menu.py tests/test_ext_reserve.py tests/test_ext_availability.py tests/test_ext_history.py` | 완료 (2026-11-16) |
| **WP-BE2** | **예약 상세** — `GET /api/ext/reservations/{reservationId}`(사본 없음 404 `reservation_not_found` · runtime 없음 502 · `refresh_schedule(…, gone=True, sink=raw)` · 404 → `reservation_gone` · 그 밖 실패 = `partialErrors: schedule`) · `_detail_reads` 재사용(키워드 인자 `amount: bool = True` 를 더하고 외부는 `amount=False` — `main` 에 가짜 값을 넘기지 않는다 · **이전 방문 실패를 따로 알리는 값 하나 더함 — 직원 응답 무변경**) · 지금 `orderMemo` · `consultationMemo`(3단계 원본) · 열람 헤더 엄격 의존성(꼴 400) · 칸 조립(`personal_of` 의 `language` · `age_on` · `visitor_funnel_of` · `funnel_of` · `_staff_ref` · `_health` · `previous_visits` + `counselors[]` · `requestedProcedures` · `requestedDoctor`) · `ext_view` · 직원 날짜 캐시 부르지 않음 | SPEC-008 §6.12 | backend | `procedure/back/app/{api/ext.py,service/ext.py,schemas/ext.py,service/reservations.py(_detail_reads 한 곳)}` · `tests/test_ext_detail.py`(새) | §9 T53(상세 몫) · T59 ~ T61 통과 · `tests/test_resv_detail.py` 그대로 통과(직원 상세 무변경 · 귀가 예약 수납 금액 그대로) | `uv run pytest -q tests/test_ext_detail.py tests/test_resv_detail.py` | 완료 (2026-11-16) |
| **WP-BE3** | **접수 목록** — **KOS0 판정 뒤에만 착수**(완료 · D-16 그대로 · 대안 안 씀 · `eventType` 끝 조각 · `flowStep` 문자열 · 시각 파싱은 소수 2 ~ 3자리 둘 다 시험). `GET /api/ext/reservations/board`(BE2 의 상세 경로보다 먼저 등록) · `ensure_day(오늘)` · 예약 단위 줄 · 상담 거침 판정을 `domain/reservation_rules.py` 함수 하나로 옮기고 `_flow()` 도 그것을 부름(직원 무변경) · 표 `consult_wait_first`(`EXT_SCHEMA` 에 더함 · repo 읽기 · 쓰기) · 이력 조회(대상 = `after` 인 줄 중 `first_at` 없는 줄 · **사건 넷**(처음 봄 · 대기 새로 봄 · 귀가 뒤 · 실패 재시도 5분 뒤 ≤ 3) · 시도 예약(고르기 + 적기 = `BEGIN IMMEDIATE` 짧은 트랜잭션 · KOS 호출 전 커밋 · 요청 트랜잭션과 따로 · 프로세스 잠금 없음) · 요청당 상한 10 = 동시 한 바퀴 · 고르는 차례 · 결과 적기 · `partialErrors`(D-39 — 이번 요청에서 사건이 있었는데 상한으로 못 부른 줄 포함) · 귀가 뒤 1번 실패도 실패 재시도(D-41) — §6.11 4) · `partialErrors` · `sync`. **D-17 대안이면** 이력 조회 대신 날짜 조회(`reservation_sync.fetch_day` 의 사본 쓰기 자리 — 요청이 와야 돈다)에서 처음 본 `CONSULTATION_WAITING` 을 행으로 쓴다(`source` 가 다른 행은 덮는다 · 그 경우 대상 파일에 `kos/reservation_sync.py` 가 더해지고 T73 을 시험한다) | SPEC-008 §3.6 · §6.11 | backend | `procedure/back/app/{api/ext.py,service/ext.py,schemas/ext.py,repository/db.py,repository/repo.py,domain/reservation_rules.py,service/reservations.py(_flow 한 곳)}` · `tests/test_ext_board.py`(새) · `tests/fake_kos.py`(이력 응답 — KOS0 에서 본 모양) · 시험 시계(실패 재시도 5분) | §9 T54 ~ T58(대안이면 + T73) 통과 · `tests/test_resv_detail.py` · `tests/test_resv_board.py` 그대로 통과 | `uv run pytest -q tests/test_ext_board.py tests/test_resv_board.py tests/test_resv_detail.py` | 완료 (2026-11-16) |
| **WP-BE4** | **쓰기 셋** — 언어(`ReservationService.personal()` 을 그대로 부름 · `actor` 타입을 `Account \| str` 로 넓힘 · 직원 `NotFound` → `customer_not_found`) · 오더 메모(내부 `schedule/v1/commands/change-order-memo` · `kos_write` · `order_memo` · `visit.order_memo` 갱신 = **행이 있을 때만 UPDATE · upsert 금지** · `after_write`) · 상담 메모(공개 `schedule/open/v1/commands/update-schedule-consultation-info` · `consultation_memo` · `after_write`) · 행위자 문자열(§6.10) · 열람 헤더 엄격 의존성(꼴 400) | SPEC-008 §3.5 · §6.13 ~ §6.15 | backend | `procedure/back/app/{api/ext.py,service/ext.py,schemas/ext.py,service/reservations.py(personal 타입 한 줄),repository/repo.py(visit 오더 메모 UPDATE 함수 하나)}` · `tests/test_ext_write.py`(새) · `tests/fake_kos.py`(세 쓰기 경로) | §9 T53(쓰기 몫) · T62 ~ T65 통과(T63 visit 행 수 그대로) · `tests/test_resv_write.py` 그대로 통과(직원 `event_log.actor` = `login_id`) | `uv run pytest -q tests/test_ext_write.py tests/test_resv_write.py` | 완료 (2026-11-16) |
| **WP-BE5** | **병원 · 직원** — **KOS0 판정 뒤에만 착수**(`daysOff` 고른 칸 = `{startDate, endDate}` · DEC-012 D-43 · KOS0 완료). `GET /api/ext/clinic`(내부 3번 동시 · `timetable_of({"operationTimetable": data})` · 빈 문자열 → null · 칸 = 이름 · 주소 · 전화 · 운영 시간 · 휴무 · `clinicId`만(DEC-012 D-25) · 휴무 원소 = `{startDate, endDate}`(이름 없음) · 선불카드 만료 시각 초 없는 꼴 파싱은 BE1 시험 · 하나라도 실패 502) · `GET /api/ext/clinics/{clinicId}/staff`(`clinicId` 상수 비교 → 404 `clinic_not_found` · 내부 `account/v2/queries/get-accounts {}` · 시스템 계정 · 제외 목록 뺌 · 직원 사본과 KOS id 로 결합) | SPEC-008 §6.16 · §6.17 | backend | `procedure/back/app/{api/ext.py,service/ext.py,schemas/ext.py}` · `tests/test_ext_clinic.py`(새) · `tests/fake_kos.py`(get-hospital · 운영 시간 · 휴무 · 내부 계정) | §9 T66 · T67 통과 | `uv run pytest -q tests/test_ext_clinic.py` | 완료 (2026-11-16) |
| **WP-BE6** | **Swagger · 공유 규칙 · 회귀** — 새 일곱 + lookup 의 `summary` · `description`(§8 「엔드포인트(0.4.0)」 줄 전부 — 희망 상담사 · 행동 변화 · 신고값 · 덮어쓰기 위험 · 예약 메모와 다른 칸 · 차트 메모 = 상담 메모 · 외주 = 역할 이름 · KOS 호출 수) · 모든 응답 칸 `description` · 응답 표 `errors(*COMMON, …)` · `openapi_docs.py` `DESCRIPTION` 외부 절(경로 열셋 · 열람 헤더 줄) · `tests/test_openapi_docs.py` `n_ops - 5 - 13` · `tests/test_ext_docs.py` `OPS` 열셋 · parameters 허용 목록(§8 「시험 고침(0.4.0)」 · 지우지 않고 넓힘) · 공유 규칙 시험 · **전체 시험 한 번** | SPEC-008 §8 · §9 T68 · T70 ~ T72 | backend | `procedure/back/app/{api/ext.py,openapi_docs.py,schemas/ext.py}` · `tests/{test_openapi_docs.py,test_ext_docs.py,test_ext_auth.py}` | T68 · T70 ~ T72 통과 · `/api/docs` 에 외부 열셋이 `외부 연동` tag 로 보임 · **전체 `uv run pytest -q` 통과(수치 리포트)** · `ruff`(레포 설정이 있으면) | `uv run pytest -q`(이 WP 끝에 한 번) | 완료 (2026-11-16) |
| **WP-REVIEW** | reviewer: SPEC-008 0.4.0 절 전부 ↔ 코드 · 부록 F(DEC-012 D-01 ~ D-47) · 부록 G 답 반영 · **기존 여섯 계약 무변경**(lookup 은 칸 추가만 · 과거 시술 메모 · 의사 0) · **직원 API 무변경**(`_flow` · `_detail_reads` · `personal` 손댄 곳이 응답 · `event_log` 를 바꾸지 않음) · 쓰기 = KOS 먼저(실패 때 성공 줄 · 사본 변경 0) · 경로별 KOS 호출 수(§6.9) · `ext_call` 에 직원 id · 고객 · 예약 id 0 · 이력 조회 = 찾은 값만 굳힘 · 사건 때만 다시 · 실패 재시도 ≤ 3 · 시도 예약(겹친 요청 1번) · 요청당 상한 10(board 를 자주 불러도 · 실패가 이어져도 호출이 늘지 않음) · 과거 시술 · 예약 내역 본문 모델 무변경 · 헤더를 읽지 않는 다섯 기존 경로 무변경 · 실명 · 키 grep. FAIL 은 모아서 한 번에 수정 발주 | 전체 | reviewer | 코드 변경 전체 | PASS | — | 완료 (2026-11-16) |
| **WP-E2E-LOCAL** | 코디: 백엔드 커밋 뒤 로컬 compose 를 **재기동**한다(옛 코드로 확인 금지) → **데모 KOS 실물**로 SPEC-008 §9 「실물 확인(0.4.0)」 ⓪ ~ ⑥. 쓰기 ④ 는 **시험 고객(example.com)의 시험 예약 1건에만** 하고, 쓰기 전 값을 리포트 밖(스크래치)에 적어 두었다가 **끝나면 원래 값으로 되돌린다**(오더 메모 · 상담 메모 · 언어 — 되돌린 뒤 KOS 웹에서 다시 확인). 상담 메모 쓰기 뒤 **같은 일정의 상담사 · 의사 · 결과 칸이 그대로인지**, **상담 전 일정에 쓰면 무엇이 오는지**를 본다(SPEC §6.15 · 실물 확인 ④). 시험 예약을 새로 만들었으면 직원 화면으로 취소한다. 그 밖에 키 없음 401 · 응답 시간(ms) · 경로별 KOS 호출 수(로그)를 리포트에 적는다. 값은 기록하지 않는다 | SPEC-008 §9 「실물 확인(0.4.0)」 | 코디 · 사용자 | — | ⓪ ~ ⑥ 확인 · 되돌림 확인 · **기존 여섯 경로 회귀 ⑥** | — | 완료 (2026-11-16) |
| **WP-DEPLOY** | 코디: 코드 PR 머지 → back 이미지 → infra `back.imageTag` PR → sync · `/api/health` · `/api/docs` 에 외부 열셋 확인 | — | 코디 | — | 운영 back = 이 판 | — | 완료 (2026-11-16) |
| **WP-E2E-PROD** | 코디: **운영 호스트**(운영 조건 · Cloudflare 경유)에서 연동처 키로 읽기 경로 — board · 상세 1건 · lookup(`customerId`) · 병원 · 직원 — 각 1번 · 키 없음 401 · `ext_call` · `ext_view` 행 확인. **쓰기는 하지 않는다**(사용자가 원하면 시험 예약에 1번 하고 되돌림). 협업자에게 새 경로를 알리는 것은 사용자 몫 | SPEC-008 §6.11 ~ §6.17 | 코디 · 사용자 | — | 운영 확인 끝 · 사용자에게 보고 | — | 완료 (2026-11-16) |

## 병렬

- KOS0 은 질문 답을 기다리지 않고 먼저 한다. BE1 · BE2 · BE4 는 KOS0 과 상관없다
- BE1 ~ BE6 은 **한 워커가 한 브랜치에서 차례로** 한다. 모두 `api/ext.py` · `service/ext.py` · `schemas/ext.py` 를 고친다. 차례 = BE1 → BE2 → (KOS0 판정 반영) → BE3 → BE4 → BE5 → BE6
- infra 작업이 없으므로 코드와 병렬로 할 일은 없다
- WP-REVIEW 는 BE6 끝 · 전체 시험 통과 뒤에 한다

## 주의

- **KOS 쓰기는 WP-E2E-LOCAL ④ 에서만** 한다(데모 테넌트 · 운영 지점 키 금지 · 시험 고객 · 끝나면 되돌림). KOS0 은 조회만 한다
- **쓰기 순서는 KOS 먼저**다(DEC-012 D-04). CC 사본 · `event_log` 를 먼저 쓰고 KOS 를 나중에 부르는 코드를 만들지 않는다. 실패 기록은 `kos_write` 의 `kos_rejected` 하나다
- 고객 언어 쓰기는 **직원 `personal()` 을 그대로** 부른다. 묶음 만드는 코드를 외부 쪽에 따로 짜지 않는다(두 벌 금지)
- 상담 거침 판정은 **함수 하나**다. 외부 board 에 같은 조건을 다시 쓰지 않는다. 옮긴 뒤 직원 상세 시험이 그대로 통과해야 한다
- 직원 서비스에서 손대는 곳은 셋뿐이다 — `_flow`(판정 함수 부르기) · `_detail_reads`(이전 방문 실패 알림 값) · `personal`(`actor` 타입). 응답 · `event_log` 값이 바뀌면 FAIL 이다
- `consult_wait_first` 는 **`first_at` 이 있는 행만** 굳는다(다시 쓰지 않고 다시 부르지 않는다). **못 찾음만으로는 다시 부르지 않는다** — 사건(대기를 새로 봄 · 귀가 뒤)이 있을 때만 부르고, 실패는 5분 뒤 · 일정마다 하루 3번까지만 다시 부른다. 고르는 순간 행에 먼저 적는다(시도 예약 — `BEGIN IMMEDIATE` 로 고르기 · 적기를 묶고 KOS 를 부르기 전에 커밋 · 그 트랜잭션 안에 `await` 를 두지 않는다). 요청 1번당 이력 호출은 10을 넘지 않는다(SPEC §6.9 · DEC-012 D-38)
- 이력 대상은 **CC 상담 판정이 아니라 `after` 문**이다(DEC-012 D-16 ③). `consultation` 과 시각 칸을 같은 조건으로 묶지 않는다
- 열람 헤더 의존성을 **기존 다섯 경로**(메뉴 · 예약 · 가능 시간대 · 과거 시술 · 예약 내역)에 달지 않는다. lookup 은 틀린 헤더에 400 을 내지 않는다(DEC-012 D-37)
- 오더 메모 사본은 visit 행이 있을 때만 UPDATE 한다. `tx.upsert("visit", …)` 를 쓰지 않는다(유령 행)
- `ext_call` 표는 바꾸지 않는다. 열람 헤더 값 · 고객 · 예약 id 를 싣지 않는다. 앱 로그에도 헤더 값을 쓰지 않는다
- 병원 정보 응답은 이름 · 주소 · 전화 · 운영 시간 · 휴무 · `clinicId` 뿐이다. 국적 · 언어 · 웹사이트 · `translsMap` · 사업자 번호 · 요양기관 번호 · 대표자 같은 칸을 넣지 않는다(DEC-012 D-25). 휴무는 KOS 원소를 그대로 내지 않는다(D-27)
- 이름 · 이메일 · 키 · 메모 글 · 직원 id 값을 응답 외 · `ext_call` · 로그 · 리포트 어디에도 남기지 않는다(DEC-010 D-24 · public)

---
type: spec
id: SPEC-008
title: "시술 · 상품 메뉴 저장 + 외부 연동 API(`/api/ext` — 메뉴 · 고객 조회(이름+이메일 · customerId) · 남은 시술권 · 선불카드 · 예약 · 예약 가능 시간대 · 과거 시술 · 예약 내역 · 접수 목록 · 예약 상세 · 고객 언어 · 오더 메모 · 상담 메모 · 병원 정보 · 직원 목록) · 연동처별 키 계약"
version: 0.4.7
status: draft
product: cc-prototype
feature: procedure
created_at: 2026-11-11
updated_at: 2026-11-17
tags:
  - product/cc-prototype
  - feature/procedure
  - doc/spec
  - status/draft
links:
  baselines: []
  decisions:
    - "[[decision-010-product-ext-api|DEC-010]]"
    - "[[decision-011-ext-api-add1|DEC-011]]"
    - "[[decision-012-ext-api-charty1|DEC-012]]"
    - "[[decision-006-reservation-board|DEC-006]]"
    - "[[decision-005-procedure-board|DEC-005]]"
  specs:
    - "[[spec-005-reservation-board|SPEC-005]]"
    - "[[spec-003-procedure-board|SPEC-003]]"
    - "[[spec-006-customer-questionnaire-web|SPEC-006]]"
  works:
    - "[[work-012-product-ext-api|WORK-012]]"
    - "[[work-013-ext-api-add1|WORK-013]]"
    - "[[work-014-ext-api-charty1|WORK-014]]"
    - "[[work-015-ext-api-staff-fields|WORK-015]]"
  releases: []
  related: []
sources:
  - "para/projects/summer-star/cc-prototype/10-decision/decision-010-product-ext-api.md (DEC-010 · accepted · D-01 ~ D-36 · 2026-11-11 D-16 · D-19 · D-31 고침 · D-35 · D-36 추가)"
  - "orchestration/work/api-swagger-docs/review-doc-r1.md (doc 검수 r1 · WARN 13 · DEC 질문 Q-A ~ Q-C)"
  - "orchestration/work/api-swagger-docs/_RESUME.md §2 (2026-11-11 줄)"
  - "orchestration/work/api-swagger-docs/research-procedure-menu.md (조사 1 · 메뉴 키 트리 · §1 ~ §7)"
  - "orchestration/work/api-swagger-docs/research-purchase-snapshot.md (조사 2 · 고객 → 수납 → 시술권 · §1 ~ §4)"
  - "orchestration/work/api-swagger-docs/research-har-product-edit.md (조사 3 · 가격 수정 뒤 산 값 유지 · 옵션 id 유지)"
  - "orchestration/work/api-swagger-docs/research-name-email-lookup.md (조사 4 · 내부 get-visitors 이름 검색 · email 칸 · 페이징)"
  - "reference/2026-10-12-cc-prototype/kos-demo-api.md (공개 API 경로 · getTicketBundlesQuery 모양)"
  - "reference/2026-11-11-cc-product/har/ (내부 get-ticket-bundles 응답 키 모양만 · 값 안 옮김)"
  - "cc-prototype procedure/back origin/main c9f30ac (읽기만 — db.py · kos/ · service/reservations.py · schemas/reservations.py · domain/ · api/ · config.py · main.py · openapi_docs.py · tests/test_openapi_docs.py)"
  - "planner 질문 Q1 ~ Q5 코디 답(2026-11-11 · 부록 B)"
  - "para/projects/summer-star/cc-prototype/10-decision/decision-011-ext-api-add1.md (DEC-011 · accepted · D-01 ~ D-16(D-15 = 문서 검수 add1 Q-add1-A · D-16 = 코드 검수 add1 r1 N1 · 2026-11-12) · 2026-11-12 · add1 세 경로)"
  - "orchestration/work/api-swagger-docs/add1-spec-instructions.md (add1 지시 · 협업자 요청 요지)"
  - "cc-prototype procedure/back main e0e4a16 (읽기만 — §6.6 ~ §6.9 의 코드 규약 줄)"
  - "planner 질문 add1 Q1 ~ Q4 코디 답(2026-11-12 · 부록 E)"
  - "orchestration/work/api-swagger-docs/review-doc-add1.md (문서 검수 add1 · WARN 6 · Q-add1-A → 0.3.1)"
  - "para/projects/summer-star/cc-prototype/10-decision/decision-012-ext-api-charty1.md (DEC-012 · accepted · D-01 ~ D-48 · 2026-11-16 · charty 1차 상담 — 0.4.0 · D-24 ~ D-40 은 0.4.1 · D-41 은 0.4.2 · D-42 ~ D-44 는 0.4.3 · D-45 는 0.4.4 · D-46 은 0.4.5 · D-47 은 0.4.6 · D-48 은 0.4.7(2026-11-17 · 직원 목록 칸 셋 더함))"
  - "orchestration/work/ext-api-charty1/research-charty1-sources.md (조사 1차 · C1 §)"
  - "orchestration/work/ext-api-charty1/research-clinic-staff.md (조사 2차 · C2 §)"
  - "orchestration/work/ext-api-charty1/research-har-history-hospital.md (조사 3차 · C3 §)"
  - "reference/2026-11-16-cc-charty1/har/ (상담대기.har · 상담대기2.har · 병원정보.har — 키 모양만 · 값 안 옮김)"
  - "cc-prototype procedure/back origin/main 0a58aba (읽기만 — 0.4.0 절의 코드 규약 줄)"
  - "orchestration/work/ext-api-charty1/review-doc-r1.md (문서 검수 r1 · FAIL F1 ~ F3 · WARN W1 ~ W17 · DEC 질문 DQ1 ~ DQ6 — 0.4.1)"
  - "orchestration/work/ext-api-charty1/spec-fix-r2-instructions.md (r1 사용자 답 · 코디 방향 — 0.4.1)"
  - "orchestration/work/ext-api-charty1/review-doc-r2.md (문서 검수 r2 · FAIL N1 · WARN N2 ~ N6 · DEC 질문 DQ7 — 0.4.2)"
  - "orchestration/work/ext-api-charty1/spec-fix-r3-instructions.md (DQ7 코디 기본값 · N1 ~ N6 방향 — 0.4.2)"
  - "orchestration/work/ext-api-charty1/kos0-report.md (WORK-014 KOS0 · 데모 실호출 · 키 · 꼴 · 건수만 — 0.4.3)"
  - "orchestration/work/ext-api-charty1/spec-fix-kos0-instructions.md (KOS0 코디 기본값 — 0.4.3)"
  - "orchestration/work/ext-api-charty1/review-code-r1.md (코드 검수 r1 · Q1 ~ Q3 · W5 — 0.4.4)"
  - "orchestration/work/ext-api-charty1/spec-fix-code-r1-instructions.md (코디 기본값 — 0.4.4)"
  - "orchestration/work/ext-api-charty1/be-fix-e2e1-instructions.md (로컬 e2e lookup 502 · 코디 실물 확인 · 코디 기본값 — 0.4.5)"
  - "orchestration/work/ext-api-charty1/fix-e2e2-instructions.md (로컬 e2e 2번째 · 상담 메모 비움 불가 · 예약 직후 404 · 코디 기본값 — 0.4.6)"
  - "reference/2026-11-16-cc-charty1/har/상담대기3.har (내부 get-visitor-prepaid-card-balance 금액 객체 키 · 일정 상세 orderMemo · consultation.consultationMemo 키 — 키 · 꼴만)"
  - "orchestration/work/ext-api-staff-fields/ext-api-staff-fields-spec-brief.md (0.4.7 지시 · DEC-012 D-48 계약 표)"
  - "orchestration/work/ext-api-staff-fields/review-doc-r1.md (문서 검수 r1 · WARN W1 ~ W5 — 0.4.7 같은 판 고침)"
  - "cc-prototype procedure/back main 969f44f (읽기만 — 0.4.7 §6.17 의 코드 규약 줄 · app/service/ext.py staff() · app/schemas/ext.py ExtStaff · app/api/ext.py STAFF_DOC · tests/test_ext_clinic.py)"
---

# 시술 · 상품 메뉴 저장 + 외부 연동 API 계약

> `procedure/back`(FastAPI) 이 지킬 계약이다. 정책의 원천은 **DEC-010(D-01 ~ D-36)** 이고, 결정 원천은 `orchestration/work/api-swagger-docs/_RESUME.md` §2 다. DEC-010 과 `_RESUME` 가 다르면 `_RESUME` 가 맞다.
> 화면(front · app)은 이번 범위가 아니다(D-01). 직원 API(SPEC-003 · SPEC-004 · SPEC-005 · SPEC-006 · SPEC-007)의 계약은 **바꾸지 않는다**. 이 문서가 더하는 것은 새 표 · 새 동기화 작업 · `/api/ext` 경로 열셋(0.3.0 에 셋 — DEC-011 · 0.4.0 에 일곱 — DEC-012) · 외부 키 인증뿐이다. 예외로 Swagger 문서 설정(`openapi_docs.py`)과 그 시험의 개수 단언 한 줄을 고친다(§8). (0.4.0) 직원 서비스 안의 함수 셋을 **응답 · 동작을 바꾸지 않고** 손본다(§2.1 — 판정 함수 옮김 · 이전 방문 실패 알림 · `personal()` 행위자 타입).
>
> 근거 표기: `D-nn` = DEC-010 · `R1 §` · `R2 §` · `R3 §` · `R4 §` = 조사 1 ~ 4 리포트의 절 · `KDA` = `kos-demo-api.md` · **`코드 규약: 파일:줄`** = DEC 에 없는 세부(이름 · 경로 · 표 · 코드 문자열)를 지금 코드에서 끌어온 곳(`procedure/back/` 아래 경로 · origin/main `c9f30ac` 줄) · **`코디 Q1 ~ Q5`** = DEC 와 코드 규약으로 정해지지 않아 planner 가 묻고 코디가 답한 것(부록 B · 2026-11-11).
> **0.3.0(add1)**: §6.6 ~ §6.9 · §9 T32 ~ T47 · 부록 D · E 는 **DEC-011(D-01 ~ D-16)** 을 근거로 한다 — 그 자리의 `DEC-011 D-nn` 은 DEC-011 번호이고, 꾸밈 없는 `D-nn` 은 지금처럼 DEC-010 이다. 그 절의 「코드 규약」 줄은 main `e0e4a16` 기준이다(앞 판 절은 `c9f30ac` 그대로).
> **0.4.0(charty 1차)**: §4.3 고침 · §4.4 · §6.4 고침 · §6.10 ~ §6.18 · §9 T48 ~ T73 · 부록 F · G 는 **DEC-012(D-01 ~ D-48 · D-24 ~ D-40 은 0.4.1 · D-41 은 0.4.2 · D-42 ~ D-44 는 0.4.3 · D-45 는 0.4.4 · D-46 은 0.4.5 · D-47 은 0.4.6 · D-48 은 0.4.7)** 를 근거로 한다 — 그 자리의 `DEC-012 D-nn` 은 DEC-012 번호다. `C1 §` · `C2 §` · `C3 §` = 조사 1 · 2 · 3차 리포트(`orchestration/work/ext-api-charty1/research-*.md`)의 절. 그 절의 「코드 규약」 줄은 origin/main `0a58aba` 기준이다. **「제안(Qn)」** 이 붙은 칸은 DEC-012 와 코드 규약만으로 정해지지 않아 planner 가 제안값을 적고 물은 것이다(부록 G). **0.4.1**: Q1 ~ Q14 는 답이 와서 DEC-012 D-24 ~ D-38 이 되었고 본문 표기를 그 D 번호로 바꿨다. 0.4.1 에서 새로 생긴 Q15 · Q16 도 답이 와서 DEC-012 D-39 · D-40 이 되었다. **0.4.2**: 0.4.2 에서 새로 생긴 Q17 도 답이 와서 DEC-012 D-41 이 되었다. 남은 「제안(Qn)」 은 없다.
> **0.4.7(직원 목록 칸 더함)**: §6.17 의 세 칸(`email` · `realName` · `kosAccountId`) · §4.4 괄호 · §6.1 「id」 예외 줄 · §8 직원 설명 · §9 T67 · T70 은 **DEC-012 D-48** 을 근거로 한다. 그 자리의 「코드 규약」 줄은 main `969f44f` 기준이다. 필드 추가만이다 — 그 밖의 절은 0.4.6 그대로다.
> **이 레포는 public 이다** — 키 · 토큰 · 비밀번호 · 실명 · 이메일 · 연락처 · KOS id 값 · 실제 금액을 쓰지 않는다. env 는 이름만 적는다. 예시 값은 자리표시(`<이름>` · `a@example.com` · `<KOS id>`)다.

**변경 이력**

| 판 | 날짜 | 무엇 |
|---|---|---|
| 0.1.0 | 2026-11-11 | 첫 판(D-01 ~ D-34 · 코디 Q1 ~ Q5) |
| 0.2.0 | 2026-11-11 | doc 검수 r1 반영 — 이름 검색 한 페이지(1000) · 상한 · 중복 제거 · 이름 정확 일치(D-16 · D-19) · 시술권 가격 칸 `bundlePrice`(D-31) · 예약 이메일 드러남 수용 · Swagger 적기(D-35) · `syncedAt`(D-36) · 키 없는 거절 IP 제한 · 기록 미들웨어 · 검사 순서 · 켜진 구역 0 = 503 · 행위자 문자열 겹 · Swagger 503 · 근거 줄 고침 |
| 0.2.1 | 2026-11-11 | doc 검수 r2 N1 ~ N3 반영 — 「키 없는 거절」= `client` null 인 오류 응답 전부(깨진 본문 400 · 405 포함) · §6.2 `405 http_error` · 이름 띄어쓰기는 KOS 그대로(Swagger · 안내 줄 · T12 한정 · 404 시험 추가) · 메뉴 동기화가 실패해도 이전 `last_ok_at` 유지(`syncedAt` · T6) |
| 0.2.2 | 2026-11-11 | 코드 검수 r1 W1 · W3 · W7 반영 — 이름 검색 2xx 인데 `data` 가 배열 아님 = 502(예약은 새 고객 안 만듦) · 예약 502 · 409 `kos_rejected` 줄을 실제 단계대로 · 메뉴 구성 · 옵션 칸과 단위 `value` 에 「KOS 가 주지 않으면 null」 |
| 0.2.3 | 2026-11-11 | 코드 검수 r2 N1 반영 — 처리하지 못한 예외 = `500 internal_error` · `ext_call` 1줄 · IP 카운트 안 함(§6.2 · §7.4 · §3.4 정의에 예외 한 줄) |
| 0.3.0 | 2026-11-12 | add1(DEC-011) — 경로 셋 더함: `GET /api/ext/availability`(기본 그룹 예약 가능 시간대 · 남은 자리 · 슬롯 1번 새로 읽기) · `POST /api/ext/customers/visits`(과거 시술 · 최근 50) · `POST /api/ext/customers/reservations`(오늘 이후 예약 · 상태) · 경로별 KOS 호출 비용 표(§6.9) · 시험 T32 ~ T44 · Swagger 개수 단언 · 부록 D · E |
| 0.3.1 | 2026-11-12 | 문서 검수 add1 W1 ~ W6 반영 — 일정 응답 `{}` · `[]` = 빈 목록 · `data` 가 있으면서 배열 아님만 502(§6.7 · §6.8 2단계) · `deleted: true` 일정은 두 목록에서 뺌(DEC-011 D-15 · Q-add1-A 코디 기본값) · `date` 없음 message = `query.date: …` · 빈 문자열 400 · `str` 로 받음 · Swagger 시험 parameters 단언 넓힘 · 「세 경로 · 세 엔드포인트 합산」 → 「외부 경로 전부 합산」 · T29 · T34 · T36 · T39 · T44 줄 더함 |
| 0.3.2 | 2026-11-12 | 코드 검수 add1 r1 N1 ~ N3 반영 — 일정 원소 모양 오류 = `502 kos_unavailable`(원문 0 · DEC-011 D-16 · 코디 기본값) · 날짜는 `YYYY-MM-DD` 숫자 꼴만(ISO 주 날짜 등 400) · 경계 시험(시작 = 지금 정각 · 오늘 00:00) · 일정 읽기 4xx · 401 → 502 시험 · T45 ~ T47 |
| 0.3.3 | 2026-11-12 | 코드 검수 add1 r2 M1 반영 — T47: 작업 `title` 숫자 갈래는 과거 시술만 502(예약 내역은 작업을 보지 않음 · 200) · 로그 원문 0 은 리뷰 재현으로 확인(시험 단언 없음) |
| 0.4.0 | 2026-11-16 | charty 1차(DEC-012) — **lookup 고침**: `customerId` 갈래 더함(이름+이메일 갈래 그대로) · 시술권 원천 공개 → 내부 `get-ticket-bundles` · `tickets[].inUseCount` · `prepaidCards[]` 칸 더함(이름 · 뜻이 바뀐 칸 0). **행동 변화**: 사용 중(`IN_USE`) 장만 남은 묶음이 이제 나온다(지금까지는 통째로 빠짐) · `totalCount` 는 뜻 그대로(상태 무관 장수)이고 사용 중 장이 세어지는 만큼 커질 수 있다. **경로 일곱 더함**: `GET /api/ext/reservations/board` · `GET /api/ext/reservations/{reservationId}` · `PUT /api/ext/customers/{customerId}/language` · `PUT /api/ext/reservations/{reservationId}/order-memo` · `PUT /api/ext/reservations/{reservationId}/consultation-memo` · `GET /api/ext/clinic` · `GET /api/ext/clinics/{clinicId}/staff`. 열람 헤더 · `event_log` 새 type · 처음 상담 대기 시각 표 · 경로별 KOS 호출 수 · 내부 의존 표(§6.18) · 시험 T48 ~ T73 · 부록 F · G(planner 질문 Q1 ~ Q14) |
| 0.4.1 | 2026-11-16 | 문서 검수 r1(F1 ~ F3 · W1 ~ W17) · 사용자 답(DQ1 ~ DQ6 · Q2) · planner 질문 답(Q1 ~ Q14 → DEC-012 D-24 ~ D-38) 반영 — **처음 상담 대기**: 이력 조회 대상 = 접수 뒤 일정 전부(CC 판정 아님 · D-16 ③) · 찾은 값만 굳힘 · 못 찾음 · 실패는 일정마다 5분 간격 · 요청당 상한 10 · 날짜가 지나면 멈춤 · §3.6 표 칸 바꿈(`first_at` null = 시도 기록 · `checked_at` = 마지막 시도 · `last_failed`) · §6.9 · §6.11 비용 문장 고침(D-38) · D-17 대안 = 요청이 와야 도는 날짜 조회(늦음 상한 없음). **열람 헤더**: 헤더를 쓰는 다섯 경로(lookup · 상세 · 쓰기 셋)만 읽음 · lookup 은 틀린 헤더를 없는 것으로(400 없음) · 새 경로만 꼴 400 · 꼴에서 `@` 뺌 · `ext_view` 행위자 = `ext:<연동처>[:<직원 id>]`(D-37). **lookup 행동 변화 더함**(D-03 · W4 · W12): 선불카드 조회 실패 = `200` + `prepaidCards: null` + 새 칸 `partialErrors`(D-36 · 새 502 없음) · 요청 스키마의 `name` · `email` 이 required 에서 빠짐(갈래 검사로 옮김) · 틀린 요청의 400 message 가 `body.name: Field required` 꼴에서 `body: …` 한 꼴로 바뀜(code 는 그대로 `invalid_request`). **그 밖**: 선불카드 `remaining` · `total` = 금액 꼴 `{value, currency}`(W3) · 예약 상세에 지금 `orderMemo` · `consultationMemo`(D-34) · 병원 칸 = 이름 · 주소 · 전화 · 운영 시간 · 휴무만(D-25) · 휴무 원소 = KOS0 뒤 고른 칸만(D-27) · board 상담 판정도 `after` 문을 거침(W6) · `_detail_reads` 키워드 인자 `amount`(W7) · 오더 메모 사본 = visit 행이 있을 때만 UPDATE(W9) · 실물 확인 ⓪ ③ ④ 더함(W10 · W15) · 코드 줄 `main.py:120-124`(W17) · 부록 G Q15 · Q16(새 질문) → 같은 날 답(코디 기본값 · DEC-012 D-39 `partialErrors` 넣는 때 · D-40 귀가 등 끝난 단계 뒤 1번 더 부르고 멈춤 · §3.6 칸 `final_tried`) |
| 0.4.2 | 2026-11-16 | 문서 검수 r2(N1 ~ N6) · DQ7 코디 답 반영 — **처음 상담 대기 다시 부르기 = 사건이 있을 때만**(DEC-012 D-38 고침 · D-16 고침 줄): 처음 봄 · 대기를 새로 봄(대기 구간마다 1 · 재진입) · 귀가 뒤 1(D-40) · 실패 재시도(5분 뒤 · 일정마다 하루 ≤ 3) — 「못 찾음 → 5분마다 다시」 버림 · 하루 합 ≤ 접수 뒤 일정 수 × 3 + 실패 재시도 · board 요청 수에 비례 안 함 · §3.6 칸 `retries` · `wait_called` 더함 · **시도 예약**(고르는 순간 행에 먼저 적음 · 겹친 요청도 같은 사건 1번 · N2) · §6.9 · §6.11 비용 문장 · T57. **N1**: lookup 요청 모델은 새로 따로 만들고 `ExtCustomerRequest`(과거 시술 · 예약 내역)는 지금 칸 · 검증 그대로(상속 끊음) · T71 ⓐ ⓑ ⓒ. **N4**: Swagger 옛 문장 「`AVAILABLE` 이 0장인 묶음은 KOS 가 주지 않는다」 지움 · `tickets` 칸 설명 고침 · T70. **N5**: T73 「요청이 와서 도는 날짜 조회」 · 대안 덮어쓰기 단언. **N6**: T71 바꿔도 되는 키에 `partialErrors`. 부록 G Q17(새 질문) → 같은 날 답(코디 기본값 · DEC-012 D-41 — 귀가 뒤 1번 실패도 실패 재시도 ≤ 3 이 받음). **문서 검수 r3(PASS · WARN M1 ~ M5) 정리**: §6.9 board 칸 · T58 을 사건 규칙으로(M1) · D-38 원 번호 근거 고침(M3) · §6.7 · §6.8 요청 줄 「`ExtLookupRequest` 와 같은 칸」 지움(M4) · 시도 예약 = `BEGIN IMMEDIATE` 짧은 트랜잭션 · KOS 호출 전 커밋(M5) · D-39 ⓑ 넓힘 = 이번 요청에서 사건이 있었는데 상한으로 못 부른 줄(참고 P2 · 코디 기본값) |
| 0.4.3 | 2026-11-16 | WORK-014 KOS0 결과(`kos0-report.md` · 데모 실호출 · 키 · 꼴 · 건수만) 반영 — **판정 = D-16 그대로 · D-17 대안 쓰지 않음**(대안 절 · T73 은 취소선 · 「쓰지 않음」) · 이력 단계 변경 = `eventType` 의 마지막 `.` 뒤 조각이 `FlowStepChanged`(실물 전체 이름 `protos.schedule.event.FlowStepChanged`) · `flowStep` = 문자열 enum 이름(숫자 대응표 없음) · 시각 = 원소 `raisedDateTimeUtc` 최솟값(차례가 섞여 옴 · 소수 자릿수 가변은 파싱 몫) · **휴무 `daysOff[]` 원소 = `{startDate, endDate}`**(KST 날짜 둘 · `name` 뺌 — KOS 에 칸 없음) · 선불카드 금액 객체 · 내부 시술권이 다 쓴 · 취소 묶음을 줌 = 확인(고침 없음 · 근거 칸만) · T57 가짜 응답 모양 · T66 · §6.18 · §10 1 · 2 닫음(DEC-012 D-42 ~ D-44) |
| 0.4.4 | 2026-11-16 | 코드 검수 r1(`review-code-r1.md`) Q1 ~ Q3 · W5 의 SPEC 한 줄들(DEC-012 D-45) — ⓐ 처음 봄 때 이미 귀가면 ⓒ 몫도 겸함(`final_tried = 1` · T57) · lookup `customerId` 갈래의 KOS 「고객 없음」 = HTTP 404 또는 400 + `errorProperties` `id NotFound` → 같은 `404 customer_not_found`(T48) · 예약 상세 `customer.customerId` = 고객 사본이 없으면 null(직원 상세의 0 과 다름) · board 는 `event_log` 를 그날 예약 id 로 걸러 읽음(§6.11 3 · §6.9) · T49 명시 `null` = 없음(섞임은 값이 있는 칸 기준) |
| 0.4.5 | 2026-11-16 | 로컬 e2e 결과(`be-fix-e2e1-instructions.md` · 2026-11-16 로컬 e2e · 데모 고객 1명의 묶음 12 중 4 가 `price` 에 `value` 없이 옴 → lookup 전체 `502`) 반영(DEC-012 D-46) — §4.3 **거르기를 먼저**(장 상태로 산 묶음만 고른 뒤 그 묶음만 칸을 만든다 · 걸러진 묶음의 모양 오류는 502 사유가 아님) · `bundlePrice` 는 내부 원천이 0 값을 뺀다 → `price` 객체에 `value` 없음 = `0`(`price` 없음 · 객체 아님 · 숫자 아닌 `value` 는 그대로 `502`) · T50 두 갈래 더함. 칸 이름 · 뜻 바뀐 것 0 |
| 0.4.6 | 2026-11-16 | 로컬 e2e 2번째(`fix-e2e2-instructions.md`) 반영(DEC-012 D-47 · D-35 를 상담 메모만 고침) — **상담 메모 빈 값 = `400 invalid_request`**(앞뒤 공백 지운 뒤 빈 문자열 · message `body.consultationMemo: KOS 는 상담 메모를 비울 수 없어요` 꼴 · KOS 호출 0 · `event_log` 0 · 실물: KOS 가 `""` · `null` 에 200 을 주고 값을 그대로 둠) · 오더 메모 빈 값 = 비움 그대로 · §6.15 요청 · 오류 · 모르던 두 가지(다른 상담 칸 · 상담 전 일정) 결과 · §6.12 · §8 상세 설명 「예약을 만든 직후에는 `reservation_gone` 이 잠깐 날 수 있다 · 다시 부르면 된다」 한 줄(코드로 막지 않음 · 재시도 없음) · T64 · 실물 확인 ④ 결과. 응답 칸 이름 · 뜻 바뀐 것 0 |
| 0.4.7 | 2026-11-17 | 직원 목록 칸 셋 더함(DEC-012 D-48 · D-15 의 「이메일은 내지 않는다」 를 뒤집음 · slug `ext-api-staff-fields`) — §6.17 `staff[]` 원소에 **`email`**(string \| null · 내부 `email`) · **`realName`**(string \| null · 내부 `realName` · 기존 `name` 과 다른 칸) · **`kosAccountId`**(string · 내부 원소 `id`) · 「넣지 않는 칸」 에서 셋을 뺌(`userId` · `licenseNumber` · `mfaMethods` · `roleId` 는 그대로 안 냄) · Swagger 설명의 「이메일 · 실명 · KOS id 는 내지 않는다」 를 고침(§6.17 · §8) · §6.1 「id」 에 직원 KOS 계정 id 예외 한 줄 · T67 고침(「키 0」 → 세 키 있음) · 부록 F D-15 줄 고침 · D-48 줄. **필드 추가만** — 기존 다섯 칸 · 행 고르기 · 차례 · 오류 · KOS 호출 수(1) · 직원 사본 · `ext_call` 바뀐 것 0. **문서 검수 r1(`review-doc-r1.md` · WARN W1 ~ W5) 반영**(같은 판 고침 · 미배포): §4.4 「KOS id 는 … 에만」 괄호에 직원 목록 `kosAccountId` 더함(W1) · T70 에 직원 목록 설명 단언(`kosAccountId` 있음 · 옛 문장 없음 · W2) · `email` · `realName` null 규칙 = `null` · 빈 문자열 · 칸 없음(W3 · 코디 기본값) · §6.17 2단계에 원소가 객체 아님 · `id` 없음 → 502(지금 코드 그대로 · W4) · T67 `id` 없는 원소 갈래 · §0 3차 줄 근거 칸 D-46 · D-47 메움 |

## 0. 이 판에서 정한 것 한눈에

| 무엇 | 계약 | 근거 |
|---|---|---|
| 메뉴 저장 | KOS 메뉴 9종을 새 표 9개에 전부 넣는다. 각 행에는 조회 칸과 **KOS 원본 JSON(`raw`)** 이 함께 있다 | D-03 · D-04 |
| 메뉴 동기화 | 마스터 루프(1시간) + 서버 시작 1회. 작업 8개 | D-05 · D-06 · 코디 Q4 |
| 외부 API | `GET /api/ext/menu` · `POST /api/ext/customers/lookup` · `POST /api/ext/reservations` | D-10 · D-11 |
| 인증 | 헤더 `X-Api-Key`. 연동처 `linky` · `charty` 키는 각각 env 로 둔다. 직원 Bearer 와 섞이지 않는다 | D-10 · D-23 |
| 기록 · 제한 | 호출마다 미들웨어가 `ext_call` 1줄(이름 · 이메일 원문 없음 · 키 없는 거절은 같은 IP · 같은 결과 1분에 1줄). 키당 최근 60초 60회를 넘으면 `429`. 키 없는 거절(`client` null 인 오류 응답 전부)이 IP 당 최근 60초 10번이면 그 IP 를 `429` | D-24 · D-25 · D-34 · 코드 규약: 문진 웹 선례 |
| 고객 조회 | 내부 `get-visitors` 이름 검색 **한 페이지(1000)** → `count` > 1000 이면 「없음」 → KOS id 중복 제거 → 이름(또는 발음명) 정확 일치 → 이메일 정확 일치 → 0명 / 1명 / 2명 이상 | D-15 ~ D-22 |
| 시술권 가격 | `bundlePrice` = KOS 묶음 `price` 그대로 — 고객이 낸 돈이 아니고 부가세 포함 여부를 표기하지 않는다 | D-31 |
| 예약 | 1명이면 그 고객, 0명이면 새 고객(이름 + 이메일)으로 예약한다. 2명 이상이거나 KOS 중복 검사에 걸리면 `409 customer_ambiguous`. 이 409 가 이메일 존재를 드러내는 것은 받아들이고 Swagger 에 적는다 | D-32 · D-35 · 코디 Q1 |
| 2차(add1) | `GET /api/ext/availability?date=` · `POST /api/ext/customers/visits` · `POST /api/ext/customers/reservations`. 가능 시간대 = 기본 그룹 하나 · 예약 정원 검사와 같은 규칙 · 요청마다 KOS 슬롯 1번. 과거 시술 · 예약 내역 = 조회 규칙으로 고객을 정하고 KOS 고객 일정 1번 | DEC-011 D-01 ~ D-16 |
| 3차(charty 1차 · 0.4.0) | lookup 고침(`customerId` 갈래 · 내부 시술권 · `inUseCount` · `prepaidCards`) + 일곱 경로(접수 목록 · 예약 상세 · 고객 언어 · 오더 메모 · 상담 메모 · 병원 정보 · 직원 목록). 연동처 공통 · 권한 분기 없음 · 새 경로에는 DEC-011 D-03(메모 · 의사 미노출)과 이름+이메일 규칙을 걸지 않는다(기존 여섯은 그대로) · 쓰기 = KOS 먼저 · 열람 = 선택 헤더 직원 id → `event_log`(신고값 · 검증 안 함) · (0.4.7) 직원 목록 원소에 `email` · `realName` · `kosAccountId` 더함(§6.17 · DEC-012 D-48) | DEC-012 D-01 ~ D-48 |

---

## 1. 범위

### 1.1 In (D-01 · D-02)

| # | 무엇 | 근거 |
|---|---|---|
| I1 | KOS 메뉴(카테고리 · 상품 · 옵션 · 구성 · 시술 · 진료항목 · 기기 · 약물 · 타겟 국가)를 ccc DB 에 **모든 칸** 그대로 저장한다(§3) | D-03 · D-04 |
| I2 | 메뉴 동기화를 마스터 루프에 얹는다(§4.1) | D-05 · D-06 · D-07 |
| I3 | 외부 연동 API 셋: 메뉴 조회 · 고객 조회(이름 + 이메일 → 고객 + 남은 시술권) · 예약(이름 + 이메일)(§6) | D-11 |
| I4 | 연동처별 API 키 인증 · 호출 기록 · 호출 제한(§7) | D-23 · D-24 · D-25 · D-34 |
| I5 | Swagger 에 외부 API 를 따로 tag 와 securityScheme 으로 싣는다(§8) | 코드 규약: `app/openapi_docs.py:98-159` |
| I6 | (0.3.0) 외부 연동 API 셋 더함: 예약 가능 시간대 · 고객 과거 시술 · 고객 예약 내역(§6.6 ~ §6.9) | DEC-011 D-01 · D-07 |
| I7 | (0.4.0) lookup 고침(§4.3 · §4.4 · §6.4) · 외부 연동 API 일곱 더함(§6.11 ~ §6.17) · 열람 헤더 · 열람 기록(§6.10) · 처음 상담 대기 시각 저장(§3.6) | DEC-012 D-08 ~ D-45 |

### 1.2 Out — 하지 않는 것

| # | 무엇 | 근거 |
|---|---|---|
| O1 | 화면(front · app) — 메뉴 · 외부 연동 화면 없음 | D-01 |
| O2 | 고객이 산 것(수납 · 시술권)의 ccc DB 저장. 남은 시술권은 조회 때마다 KOS 에서 읽는다 | D-12 |
| O3 | 다 쓴 시술권 · 취소된 시술권 · 시술권 그룹 통계 응답 | D-12 |
| O4 | 외부 메뉴 응답의 진료항목 · 기기 · 약물 객체, 공급가 · 부가세 · 면세 · 과세 유형 · 특별가 · 프로모션(이것들은 DB 에만 있다) | D-27 · D-30 |
| O5 | 고객 조회 응답의 전화 · 생년월일 · 국적 · 여권 · 차트번호 · 이메일 | D-13 · D-31 |
| O6 | email 이 빈 기존 고객을 보조 키(전화 · 생년월일)로 찾는 것 | D-22 |
| O7 | 이름 띄어쓰기 · 순서를 바꿔 다시 검색하는 것 | D-17 |
| O8 | 외부에서 예약 그룹 · 구역 · 담당자를 받는 것 | D-33 |
| O9 | KOS Webhook(`PRODUCT_*`) 받기 · 빈 검색어 `searchProductOptionSummaries` 호출 | D-05 · D-06 |
| O10 | 협업자 admin 계정 회수 — 언제 할지는 사용자가 정한다. 이 문서는 회수를 권한다고만 적는다(§7.6) | D-26 |
| O11 | 직원 API 의 동작 · 응답 변경(직원 고객 검색 `search()` 의 `countInPage:20` 도 그대로 둔다 — D-16 은 외부 조회에만 걸린다) | D-10 · D-16 |
| O12 | (0.4.0) 시술권 차감 · 예산 · 동행자 · 통역 필요 · 피부 진단 · **시술권 만료일 칸**(KOS 에 없음 — 발행일 `purchasedDate` 만) | DEC-012 D-07 |
| O13 | (0.4.0) 연동처별 권한 분기 · 「KOS = 저장소 / CC = 원본」 전환(고도화 작업 몫) · 작업 단위 메모(간호 · 의사) · 고객 특이사항 쓰기 | DEC-012 D-01 · D-04 · D-05 |
| O14 | (0.4.0) 기존 여섯 경로의 계약 변경 — lookup 은 칸 **추가**만, 나머지 다섯은 그대로. 과거 시술(§6.7)은 계속 메모 · 의사를 내지 않는다 | DEC-012 D-02 · D-03 |

---

## 2. 폴더 · env

### 2.1 폴더 — `procedure/back/` 안에 더한다(코드 레포 `kknaksss/cc-prototype`)

| 자리 | 무엇 | 근거 |
|---|---|---|
| `app/repository/db.py` | `MENU_SCHEMA`(§3.2 메뉴 표 9) · `EXT_SCHEMA`(§3.4 `ext_call`)를 지금 `SCHEMA` · `RESV_SCHEMA` 와 같은 방식(`CREATE TABLE IF NOT EXISTS` + `Database.__init__` 의 `executescript`)으로 더한다 | 코드 규약: `app/repository/db.py:96-149` · `:256-261` |
| `app/repository/repo.py` | 메뉴 upsert · 「없음」 표시 · 메뉴 트리 읽기 · `ext_call` 쓰기 함수 | 코드 규약: `app/repository/repo.py:272` · `:476-480` |
| `app/kos/menu_sync.py`(새) | 메뉴 동기화(§4.1) | 코드 규약: `app/kos/reservation_sync.py:177-190` |
| `app/kos/runtime.py` | `master_once()` 에서 메뉴 동기화 1번 호출 | 코드 규약: `app/kos/runtime.py:53-62` |
| `app/service/ext.py`(새) | 외부 API 서비스 — 메뉴 응답 조립 · 고객 조회(§5) · 예약(지금 `ReservationService.create()` 재사용) | D-11 · 코드 규약: `app/service/reservations.py:773` |
| `app/service/reservations.py` | 행위자 문자열 겹(§3.5) — `create()` · `_new_visitor()` · `kos_write()` · `_event()` 의 `actor` 가 `Account` 또는 행위자 문자열을 받고, `_event` 가 문자열은 그대로 · `Account` 는 `login_id` 로 적는다. 부르는 곳은 고치지 않는다. 그 밖 동작은 바꾸지 않는다 | D-11 · D-24 · 코드 규약: `app/service/reservations.py:478-479` · `:709-720` · `:773` · `:890` |
| `app/api/ext.py`(새) | 라우터 `prefix="/api/ext"` · 의존성 `require_ext_key` | D-10 · 코드 규약: `app/api/public_questionnaire.py:17-18` |
| `app/schemas/ext.py`(새) | 요청 · 응답 모델(모든 칸 `description` · 요청은 모르는 키 400) | 코드 규약: `app/schemas/reservations.py:696-722` · `tests/test_openapi_docs.py:63-68` |
| `app/domain/errors.py` | `ServiceUnavailable`(status 503) 1개 더함(§6.5 `ext_not_configured`) | 코디 Q3 · 코드 규약: `app/domain/errors.py:4-47` |
| `app/config.py` | env 3개(§2.2) | 코드 규약: `app/config.py:13-31` |
| `app/main.py` | 라우터 등록 · `/api/ext` 미들웨어(IP 차단 §7.3 · `ext_call` 쓰기 §7.4 · `Cache-Control: no-store`) | 코드 규약: `app/main.py:104-111` · `:128-129` |
| `app/openapi_docs.py` · `app/api/docs.py` | tag `외부 연동` · securityScheme `ExtApiKey` · 앱 설명 절 · `STATUS_TEXT` 503(§8) | 코드 규약: `app/openapi_docs.py:98-159` · `app/api/docs.py:42-47` |
| `tests/test_ext_*.py`(새) · `tests/test_openapi_docs.py`(개수 단언 고침) | §9 | 코드 규약: `tests/` 구성 |
| (0.3.0 · add1) `app/api/ext.py` · `app/service/ext.py` · `app/schemas/ext.py` · `app/kos/reservation_sync.py` · `app/openapi_docs.py` · `tests/test_ext_*.py` · `tests/test_openapi_docs.py` | 경로 셋 · 서비스(가능 시간대 · 과거 시술 · 예약 내역) · 응답 모델 · `ResvSync.refresh_slots(day)`(지금 `_slots` 를 부르는 공개 함수 하나 · 동작 무변경) · 앱 설명 · 시험. 직원 서비스(`reservations.py`) · `reservation_rules.py` 는 **고치지 않고** 함수만 가져다 쓴다(`open_spans` · `is_full` · `schedule_start` · `PREV_RESULT` · `state_of` · `resources_of` · `reservation_id_of`) | DEC-011 · §6.6 ~ §6.8 |
| (0.4.0 · charty 1차) `app/api/ext.py` · `app/service/ext.py` · `app/schemas/ext.py` · `app/repository/db.py`(§3.6 표 1개) · `app/repository/repo.py`(그 표 읽기 · 쓰기 · (0.4.1) visit 오더 메모만 고치는 UPDATE 함수 하나 — §6.14) · `app/domain/reservation_rules.py`(상담 거침 판정 함수 하나로 옮김 — §6.11) · `app/service/reservations.py`(① `_flow` 가 옮긴 판정 함수를 부름 · ② `_detail_reads` 에 키워드 인자 `amount: bool = True` 를 더하고(직원 기본값 그대로 · 외부는 `False`) 이전 방문 실패를 따로 알림 · ③ `personal()` 의 `actor` 타입을 `Account \| str` 로 넓힘 — 셋 다 **직원 응답 · 동작 무변경**) · `app/openapi_docs.py` · `tests/test_ext_*.py` · `tests/test_openapi_docs.py` · `tests/fake_kos.py` | 경로 일곱 · lookup 고침 · 열람 기록 · 응답 모델 · 시험. 그 밖 직원 코드는 고치지 않고 함수를 가져다 쓴다(`refresh_schedule` · `_detail_reads` · `personal_of` · `previous_visits` · `_health` · `visitor_funnel_of` · `funnel_of` · `_staff_ref` · `kos_write` · `after_write` · `timetable_of` · `state_of`) | DEC-012 · §6.10 ~ §6.17 |

### 2.2 env 더함 — **이름만**(값은 레포 밖 `.env` · 클러스터 Secret)

| env | 뜻 | 비면 | 근거 |
|---|---|---|---|
| `PROC_EXT_KEY_LINKY` | 링키 연동처 API 키 | 그 연동처는 꺼진다. 어떤 키도 링키로 인정되지 않는다 | D-23 · 코드 규약: `app/config.py:59`(`PROC_SESSION_SECRET` 같은 서버 비밀 = `PROC_` 접두) · `:30-31`(비면 끈다) |
| `PROC_EXT_KEY_CHARTY` | 차티 연동처 API 키 | 위와 같음 | D-23 · 위와 같음 |
| `KOS_EXT_RESERVATION_GROUP_ID` | 외부 예약이 들어갈 KOS 예약 그룹 id(하나) | 외부 예약만 `503 ext_not_configured`. 조회 · 메뉴는 그대로 | D-33 · 코디 Q3 · 코드 규약: `app/config.py:24` · `:31`(KOS id 설정 = `KOS_` 접두) |

- 키를 바꾸거나 끄는 것은 이 env 를 바꿔 배포하는 것으로 한다(D-23). 키 값은 로그 · 응답 · `ext_call` 에 싣지 않는다(§7.1).
- **값을 두는 곳**: 세 env 모두 지금 `KOS_ZONE_ID` 와 같은 길을 탄다 — infra 레포(private) `provisioning/secrets/cc-prototype-prod.env.example` 에 **이름만 빈 값으로** 한 줄씩 더하고, 값은 클러스터 Secret `cc-prototype-secret` 에만 넣는다(로컬은 gitignore `.env`). infra · profile · 코드 레포 어디에도 키 · KOS id **값은 0** 이다(근거: infra `origin/main` 의 그 파일 25행 `KOS_ZONE_ID=` · `deploy.md` ② 「새 env 는 sync 전에 Secret — 값은 레포 밖」)

---

## 3. 데이터 모델 (D-03 · D-04 · D-07 · D-24)

### 3.1 원칙

- 메뉴 표는 모두 **조회 칸 + `raw`(KOS 원본 객체 JSON 문자열)** 로 이뤄진다. 표에 칸으로 뽑지 않은 값(다국어 · 가격 세부 · 상태 · deprecated 칸)도 `raw` 에 남는다(D-03 · D-04). `raw` 는 KOS 가 준 객체를 **고치지 않고** `json.dumps` 한 것이다(키 순서 · 빈 값 · deprecated 칸을 보존한다)
- 시각 = UTC ISO 문자열 · json 열 = 문자열(D-04 · 코드 규약: `app/repository/db.py:1`)
- KOS 에서 오는 행은 `kos_id`(UNIQUE)로 맞춰 **덮어쓴다**. KOS 에 id 가 없는 것(구성 · 타겟 국가)은 §3.2 에 적은 키로 맞춘다(코드 규약: `app/repository/db.py:100` · `:120-124` 복합 키 `reservation_slot`)
- **「없음」 표시(D-07)**: 이번 동기화 결과에 없는 행은 지우지 않고 `present = 0` 으로 둔다. 다시 나오면 `present = 1` 로 되살린다(코드 규약: `app/repository/repo.py:476-480` `mark_absent_kos` · 되살림 = upsert 칸에 `present: True` 를 넣는 `app/kos/reservation_sync.py:200-201` 선례). `mark_absent_kos` 는 `kos_id` 로 견주므로 `kos_id` 가 없는 `menu_composition`(복합 키 `option_kos_id` · `seq`) · `menu_target_country`(`raw` 키)에는 그대로 쓸 수 없다 — 그 두 표는 「이번 결과에 없는 행 = `present = 0`」을 자기 키로 하는 함수를 따로 둔다. KOS 가 행을 주면서 삭제 · 숨김 · 닫힘 표시를 단 경우(`deleted` · `opened:false` · `closed:true`)에는 행은 `present = 1` 로 두고 그 표시 칸만 저장한다. 외부 응답에서는 두 경우 모두 빠진다(§6.3)
- 동기화가 실패한 작업은 그 표를 건드리지 않는다. 이전 값과 `present` 가 그대로 남는다(§4.1)
- 고객이 산 것(수납 · 시술권)은 저장하지 않는다(D-12). 고객 조회가 찾은 고객은 지금 `customer` 사본에 덮어쓴다(이름 · 발음 · 국적 · 신규 여부 · 차트번호 · 성별). email 은 저장하지 않는다(코드 규약: `app/kos/reservation_sync.py:143-151` `upsert_customer` · SPEC-005 §3.1 「저장하는 개인정보」)

### 3.2 메뉴 표 (`MENU_SCHEMA`)

모든 표에 `id INTEGER PRIMARY KEY` · `raw TEXT NOT NULL` · `present INTEGER NOT NULL DEFAULT 1` · `synced_at TEXT` 가 있다. 아래 표에는 그 밖의 칸만 적는다.

| 표 | 맞추는 키 | 조회 칸 | 원천(§4.1) | 근거 |
|---|---|---|---|---|
| `menu_category` | `kos_id` UNIQUE | `name` · `"order"` · `opened`(0/1) · `deleted`(0/1) | `getCategories` `data[]` | R1 §1.6 |
| `menu_product` | `kos_id` UNIQUE | `title` · `is_event`(0/1) · `closed`(0/1) · `deleted`(0/1) · `seq`(`getProducts` 배열 순서 0..) · `category_kos_ids`(json `[..]` — `categories[].id`) | `getProducts` `data[]`(`raw` 에서 `options[]` 는 **빼고** 둔다 — 옵션은 `menu_option.raw` 에 있다) | R1 §1.2 · R1 §4 「정렬」 |
| `menu_option` | `kos_id` UNIQUE | `product_kos_id` · `seq`(그 상품 `options[]` 순서) · `type`(`SINGLE` · `GROUP` · `CONSULTATION` 그대로) · `title` · `deleted`(0/1) · `list_price`(`price.amount.value` 정수 · 없으면 null) · `currency`(`price.amount.currency` · 없으면 null) · `count`(SINGLE 만 · 그 밖 null) · `procedure_kos_id`(SINGLE `procedure.id` · 그 밖 null) · `medical_service_kos_id`(SINGLE 만 — §4.1 ③ `getProductOptions` 로 채움 · 그 밖 null) | `getProducts` `data[].options[]`(`raw` 에서 `compositions[]` 는 빼고 둔다) | R1 §1.1 `Option` · D-28 · D-09 · 코디 Q4 |
| `menu_composition` | (`option_kos_id`, `seq`) UNIQUE — KOS 구성에는 id 가 없다(R1 §2.1) | `title` · `count` · `unit_type` · `unit_value` · `list_price` · `currency` · `procedure_kos_id` · `medical_service_kos_id` | `getProducts` GROUP `options[].compositions[]` | R1 §1.1 `Composition` · R1 §2.1 「2 → 3」 |
| `menu_procedure` | `kos_id` UNIQUE | `name` | `getProcedures` `data[]` | R1 §1.7 |
| `menu_medical_service` | `kos_id` UNIQUE | `title` · `status` · `code`(`configuration.code`) · `procedure_kos_id`(`configuration.procedure.id`) · `unit_type` · `unit_value`(`configuration.unit` · 없으면 null) | `getMedicalServices` `data[]` | R1 §1.1 `MedicalService` · R1 §1.8 |
| `menu_machine` | `kos_id` UNIQUE | `name` | `getMachines` `data[]` | R1 §1.7 |
| `menu_medicine` | `kos_id` UNIQUE | `name` | `getMedicines` `data[]` | R1 §1.7 |
| `menu_target_country` | `raw` UNIQUE — id 가 없고 같은 `code` 가 두 번 온다(R1 §1.9 · §7-9). 객체 전체가 곧 행이다 | `code` · `"order"` | `getTargetCountries` `data[]` | R1 §1.9 |

- `getProducts` 의 상품 · 옵션 · 구성은 한 응답에서 함께 오므로 **한 트랜잭션**으로 반영한다. 상품이 빠지면 그 아래 옵션 · 구성도 이번 결과에 없으므로 같이 `present = 0` 이 된다
- 구성은 옵션마다 `seq` 0.. 로 맞춘다. 옵션의 구성이 줄면 남는 `seq` 행이 `present = 0` 이 된다
- 기기 · 약물 연결(`medicineAndMachines[]`)은 표 칸으로 뽑지 않고 옵션 · 구성의 `raw` 에 둔다. 이 배열은 기기와 약물을 섞어서 담고, 원소에 종류 칸이 없다(R1 §2.1). 외부 응답에도 나가지 않는다(D-27)
- 인덱스: `menu_option(product_kos_id)` · `menu_composition(option_kos_id)`(트리 읽기용 · 코드 규약: `app/repository/db.py:82` · `:119`)

### 3.3 KOS 필드 대응 (메뉴 응답에 쓰는 것)

| 외부 응답 칸(§6.3) | ccc | KOS | 근거 |
|---|---|---|---|
| 카테고리 `id` · `name` · `order` · `translsMap` | `menu_category.kos_id` · `name` · `order` · `raw.translsMap` | `getCategories` `data[].id` · `name` · `order` · `translsMap` | R1 §1.6 · D-29 · 코디 Q2 |
| 상품 `id` · `title` · `description` · `isEvent` · `translsMap` | `menu_product.kos_id` · `title` · `raw.description` · `is_event` · `raw.translsMap` | `getProducts` `data[]` 같은 이름 | R1 §1.2 · D-29 · 코디 Q5 |
| 옵션 `id` · `type` · `title` · `description` · `translsMap` | `menu_option.kos_id` · `type` · `title` · `raw.description` · `raw.translsMap` | `options[]` 같은 이름 | R1 §1.1 · D-28 · D-29 |
| 옵션 · 구성 `listPriceExVat` | `list_price` · `currency` | `price.amount{value, currency}`(정가 · 부가세 별도) | D-09 · D-30 · R1 §3 · R2 §1.2 |
| 옵션 · 구성 `count` | `menu_option.count` · `menu_composition.count` | SINGLE `count` · 구성 `count` | R1 §1.1 · 코디 Q5 |
| 옵션 `unit`(SINGLE) | `menu_medical_service.unit_type` · `unit_value`(`menu_option.medical_service_kos_id` 로 이음) | 진료항목 `configuration.unit{type, value}` | R1 §2.2(옵션 `unit` 은 0/307 · 단위는 진료항목에 있다) · 코디 Q4 · Q5 |
| 구성 `unit` | `menu_composition.unit_type` · `unit_value` | 구성 `unit{type, value}` | R1 §1.1 · 코디 Q5 |
| `procedure{id, name}` | 옵션 · 구성 `raw.procedure.id` · `.name` | SINGLE `procedure` · 구성 `procedure` | D-27 · R1 §1.1 |

### 3.4 외부 호출 기록 표 (`EXT_SCHEMA` · D-24)

| 표 | 칸 | 근거 |
|---|---|---|
| `ext_call`(쌓기만) | `id INTEGER PRIMARY KEY` · `at TEXT NOT NULL`(UTC ISO) · `client TEXT`(`linky` \| `charty` \| null) · `endpoint TEXT NOT NULL`(`<METHOD> <경로 틀>` — 예 `POST /api/ext/customers/lookup`) · `status INTEGER NOT NULL`(HTTP 상태) · `outcome TEXT NOT NULL`(성공 = `ok`, 오류 = §6 의 오류 `code` 그대로) | D-24 · 코드 규약: `app/repository/db.py:71-74`(`event_log` · 쌓기만) · `:152-163`(`push_log` 내역 표) |

- **누가 쓰나**: `/api/ext` 미들웨어가 응답을 낸 뒤 쓴다(401 · 없는 경로 404 · JSON 이 아닌 본문 400 은 라우터 의존성이 돌기 전에 끝나므로 의존성에서는 쓸 수 없다 — 코드 규약: `app/main.py:104-111` 미들웨어 선례 · `:117-125`)
- **`client`** = `require_ext_key` 가 키를 맞힌 뒤 `request.state` 에 남긴 연동처 이름. 남긴 값이 없으면(키 없음 · 틀림 · 의존성 전에 끝난 요청) **null**. 미들웨어는 키를 다시 견주지 않는다
- **`endpoint`** = 매칭된 라우트의 경로 틀(`path_format`). 매칭된 라우트가 없으면(없는 경로) **고정값 `"<METHOD> (unknown)"`**(예 `GET (unknown)`) — 실제 경로를 적지 않는다. 경로에 실린 이름 · 이메일 원문이 표에 남지 않게 하기 위해서다(D-24)
- **키 없는 거절**(정의 — §7.3 · §7.4 도 이 뜻): `client` 가 null 인 모든 `/api/ext` 오류 응답 — 401 · 없는 경로 404 · 깨진 본문 400 · 405 · IP 차단 429. 처리하지 못한 예외의 `500 internal_error` 는 서버 쪽 잘못이라 들어가지 않는다(§7.4). 라우터 밖 처리기에서 끝나는 400 · 405 도 들어간다(코드 규약: `app/main.py:117-125` — `RequestValidationError` · `StarletteHTTPException` 처리기). 401 · 404 만 고르지 않는다
- **줄이기**: 키 없는 거절은 **같은 IP · 같은 `outcome` 이면 1분에 1줄**만 쓴다. IP 는 이 판단의 메모리 키로만 쓰고 표 · 로그에 남기지 않는다(코드 규약: `app/service/questionnaire.py:108` · `:271-282` `_deny` — 「같은 IP 같은 이유는 1분에 1행 · IP 는 남기지 않음」)

- **싣지 않는 것**: 요청 이름 · 이메일 원문, 키 값, 고객 · 예약 id, KOS 응답 본문(D-24). 고객 · 예약 결과는 기존 `customer` · `reservation` · `event_log` 가 이미 갖는다
- 인덱스 `ext_call(at)`. 보존 기간은 정하지 않는다 — 지금 `event_log` · `push_log` 처럼 쌓기만 한다(코드 규약: `app/repository/db.py:153`)

### 3.5 `event_log` (지금 표 그대로 · 0.4.0 에 새 `type` 셋)

- 외부 예약이 지금 `create()` 를 다시 쓰므로 지금 `resv_create` · `kos_rejected` 줄이 그대로 남는다(SPEC-005 §3.2). 그때 `event_log.actor` 는 직원 `login_id` 대신 **`ext:<연동처>`**(`ext:linky` · `ext:charty`)다(코드 규약: `app/service/reservations.py:709-720` · `app/repository/db.py:72` `actor TEXT`). 새 `type` 은 없다
- **넘기는 법 — 행위자 문자열 겹(하나로 정함)**: `create()` · `_new_visitor()` · `kos_write()` · `_event()` 는 지금 `Account` 를 받지만, 그 안에서 쓰는 것은 `actor.login_id` 하나뿐이다(`_event` → `tx.add_event(…, actor.login_id, …)` · 코드 규약: `app/service/reservations.py:478-479`. `create` · `_new_visitor` · `kos_write` 는 `actor` 를 아래로 넘기기만 한다 — `:709-720` · `:773-851` · `:890-924`). 그래서 이 네 함수의 `actor` 타입을 **`Account | str`** 로 넓히고, `_event` 한 곳에서만 「문자열이면 그대로 · `Account` 면 `login_id`」로 적는다. 외부 서비스는 `"ext:<연동처>"` 문자열을 넘긴다. 가짜 `Account` 를 만들지 않는다
- **이 방식을 고른 근거(더 작은 쪽)**: 네 함수를 「문자열만 받기」로 바꾸면 `kos_write` · `_event` 를 부르는 직원 쪽 30여 곳(`app/service/reservations.py` 안 · `app/service/reception.py:67` · `:183` · `:205` · `:222-225` · `:239-242` · `:260-263` · `app/api/reservations.py:224`)을 모두 `actor.login_id` 로 고쳐야 한다. 타입을 넓히면 부르는 곳은 한 줄도 바뀌지 않고, 직원 `event_log.actor` 값은 지금과 **같다**(`Account` → `login_id` 그대로). 문자열 actor 를 바로 적는 선례 = `app/service/questionnaire.py:38` · `:282`(`ACTOR = "customer"`). 시험 T17(외부 = `ext:linky`) · T30(직원 값 그대로)이 고정한다
- **(0.4.0) 행위자 문자열에 직원 id**: 0.4.0 쓰기(§6.13 ~ §6.15)의 `actor` = **`ext:<연동처>:<직원 id>`**, 열람 헤더(§6.10)가 없으면 `ext:<연동처>`(DEC-012 D-19). (0.4.1) 열람 줄 `ext_view` 의 `actor` 도 같은 값이다 — `ext:<연동처>[:<직원 id>]`(DEC-012 D-37 ⑤ · 검수 r1 W8). 직원 id 는 연동처가 신고한 값이고 CC 가 검증하지 않는다(DEC-012 D-18). 같은 겹을 `personal()` 에도 넓힌다(§2.1 · 그 안에서 `actor` 는 `kos_write` · `_event` 로 넘기기만 한다 — 코드 규약: `app/service/reservations.py:1056-1084`)
- **(0.4.0) 새 `type`**(열 추가 없음 · `payload` JSON · `visit_id` null):

| type | 언제 | payload | 근거 |
|---|---|---|---|
| `ext_view` | 고객 데이터를 연 응답이 **200** 일 때 1줄 — lookup(§6.4) · 예약 상세(§6.12). 오류 응답에는 남기지 않는다. `actor` = `ext:<연동처>[:<직원 id>]`(위 · DEC-012 D-37) | `{client, staffId(헤더 값 · 없으면 null), path(경로 틀 · 예 `GET /api/ext/reservations/{reservationId}`), customerId, reservationId(상세만 · lookup 은 null)}` | DEC-012 D-18 · C1 §3-8 ② |
| `order_memo` | 오더 메모 KOS 쓰기 성공 뒤(§6.14) | `{reservationId, length}`(글 원문은 싣지 않는다 — `notice_save` 의 `length` 선례) | DEC-012 D-04 · D-12 · 코드 규약: `app/service/reservations.py:1049-1050` |
| `consultation_memo` | 상담 메모 KOS 쓰기 성공 뒤(§6.15) | `{reservationId, length}` | DEC-012 D-04 · D-13 · 같음 |

- 고객 언어(§6.13)는 직원 `personal()` 을 그대로 타므로 지금 `visitor_personal`(`{customerId, fields: ["language"]}`) 줄이 남는다(새 type 아님). KOS 실패는 셋 다 `kos_write` 의 `kos_rejected` 줄이다(DEC-012 D-04)
- `ext_call`(§3.4)은 **바꾸지 않는다** — 직원 id · 고객 · 예약 id 를 싣지 않는다(DEC-012 D-18 · DEC-010 D-24)

### 3.6 (0.4.0) 처음 상담 대기 시각 표 (`consult_wait_first` · DEC-012 D-16 · D-17 · D-38 · D-40)

| 칸 | 뜻 | 근거 |
|---|---|---|
| `reservation_kos_id TEXT PRIMARY KEY` | KOS 일정 id(= 사본 `reservation.kos_id`) | DEC-012 D-16 |
| `first_at TEXT` | 처음 `CONSULTATION_WAITING` 이 된 시각(UTC ISO). **찾았을 때만 값이 있다.** null = 아직 못 찾음(시도 기록만 있는 행) | DEC-012 D-16 · D-38 ① |
| `source TEXT` | `first_at` 을 정한 곳 — `kos_event_log`(D-16) · ~~`cc_poll`(D-17 대안)~~(0.4.3 · KOS0 — 대안 쓰지 않음 · 값은 늘 `kos_event_log`). `first_at` 이 null 이면 null | DEC-012 D-17 · D-42 |
| `checked_at TEXT NOT NULL` | 마지막으로 이력 부르기를 **예약한** 시각(§6.11 4 「시도 예약」 — 부르기 전에 적는다) — 실패 재시도의 5분 판단에 쓴다 | DEC-012 D-38 ② · 검수 r2 N2 |
| `last_failed INTEGER NOT NULL DEFAULT 0` | 마지막 시도가 실패(네트워크 · 5xx · 4xx · 401 · 403 · 모양 오류)였거나 결과를 아직 못 받았으면 1(시도 예약 때 1 로 적고 결과가 오면 고친다), 못 찾음이면 0 — 실패 재시도 · `partialErrors` 에 쓴다 | DEC-012 D-23 · D-38 ② ④ |
| `retries INTEGER NOT NULL DEFAULT 0` | (0.4.2) 실패 재시도로 부른 횟수(그날 누적). 3 이면 더 재시도하지 않는다 | DEC-012 D-38 ② ⓓ |
| `wait_called INTEGER NOT NULL DEFAULT 0` | (0.4.2) 지금 대기 구간에서 「대기를 새로 봄」 몫을 이미 불렀으면 1. 사본에서 그 일정이 `CONSULTATION_WAITING` 이 아닌 것을 보면 0 으로 되돌린다(다음 대기 구간을 새 사건으로 보려고) | DEC-012 D-38 ② ⓑ |
| `final_tried INTEGER NOT NULL DEFAULT 0` | 끝난 단계(귀가)를 본 뒤 마지막 1번을 불렀으면 1 — 그 뒤 그 일정은 사건으로 다시 부르지 않는다(§6.11 4) | DEC-012 D-40 |

- **`first_at` 이 있는 행만 굳는다** — 그 행은 다시 쓰지 않고, 그 일정은 다시 부르지 않는다(「한 번 정해지면 안 바뀐다」는 찾은 값의 성질이다 · DEC-012 D-16 ② · D-38 ①). `first_at` 이 null 인 행은 시도 기록이다 — 시도마다 칸을 고치고, 찾으면 `first_at` · `source` 를 채운다(0.4.1 · 검수 r1 F1 · F3). ~~한 번 쓴 행은 고치지 않는다 · 조회 실패는 행을 쓰지 않는다~~
- ~~**D-17 대안으로 바꿀 때**~~ (0.4.3 · KOS0 — **쓰지 않음** · DEC-012 D-42. 아래는 기록으로 둔다)(DEC-012 D-38 ⑥): 대안이 상담 대기를 처음 본 일정은 `source` 가 `cc_poll` 이 아닌 행(`kos_event_log` 로 굳은 행 · `first_at` null 시도 행)을 **덮는다**(`first_at` = 본 시각 · `source = cc_poll`). 대안에서는 이력을 부르지 않으므로 `first_at` null 시도 행은 더 쓰지 않는다. 지우는 이주는 두지 않는다(덮어쓰기로 충분하다)
- 행은 지우지 않고 쌓는다(지난 날 행은 읽히지 않을 뿐이다 · `event_log` 처럼). 보존 기간은 정하지 않는다
- 지금 `SCHEMA` · `EXT_SCHEMA` 와 같은 방식(`CREATE TABLE IF NOT EXISTS`)으로 `EXT_SCHEMA` 에 더한다. 사본 `reservation` 표에 열을 더하지 않는다 — 날짜 조회 upsert(`reservation_fields`)가 덮어쓰지 않게 따로 둔다(코드 규약: `app/repository/db.py:288-296` · `app/kos/reservation_sync.py:117-160`)

---

## 4. KOS 연동

### 4.1 메뉴 동기화 (D-05 · D-06 · D-07 · 코디 Q4)

**언제**: `KosRuntime.master_once()` 안, 지금 예약 목록(`resv.master()`) 다음에 1번 부른다. 서버 시작 때 1회(`startup()` → `master_once(force=True)`), 그 뒤 `KOS_POLL_MASTER_SEC`(기본 3600초)마다 돈다. 예약 목록처럼 **조회 시간(09:00 ~ 21:00)과 상관없이** 돈다(D-06 · 코드 규약: `app/kos/runtime.py:45-62` · `:107-109`). Webhook 은 받지 않는다(D-06).

**작업 순서**(내부 = 없음 · 모두 **공개** API, `KosClient.open` · 코드 규약: `app/kos/client.py:179-180`):

| # | 작업 | 공개 경로 | 본문 | 반영 표 | 근거 |
|---|---|---|---|---|---|
| ① | `getCategories` | `product/open/v1/queries/get-categories` | `{}` | `menu_category` | D-05 · R1 §1.6 |
| ② | `getProducts` | `product/open/v1/queries/get-products` | `{}`(필터 없음 · 페이징 없음) | `menu_product` · `menu_option` · `menu_composition`(한 트랜잭션) | D-05 · R1 §1.2 · §4 「페이징」 |
| ③ | `getProductOptions` | `product/open/v1/queries/get-product-options` | `{optionIds:[②의 SINGLE 옵션 kos_id], includePromotions:false}` — **N개씩 나눠 부른다**(N = 구현 때 데모에서 실측해 정하고 코드 상수 + WORK 리포트에 적는다. KOS 문서에 개수 상한이 있으면 그 값을 따른다 · R1 §1.4 「옵션 4개 = 8KB」) | `menu_option.medical_service_kos_id` 만(응답 `data[].medicalService.id`). 진료항목 본문은 ⑤ 행에 있다 | D-05 · 코디 Q4 · R1 §1.4 · §7-1 |
| ④ | `getProcedures` | `product/open/v1/queries/get-procedures` | `{}` | `menu_procedure` | D-05 · R1 §1.7 |
| ⑤ | `getMedicalServices` | `product/open/v1/queries/get-medical-services` | `{}` | `menu_medical_service` | D-05 · R1 §1.8 |
| ⑥ | `getMachines` | `product/open/v1/queries/get-machines` | `{}` | `menu_machine` | D-05 · R1 §1.7 |
| ⑦ | `getMedicines` | `product/open/v1/queries/get-medicines` | `{}` | `menu_medicine` | D-05 · R1 §1.7 |
| ⑧ | `getTargetCountries` | `target-country/open/v1/queries/get-target-countries` | `{}` | `menu_target_country` | D-05 · R1 §1.9 |

- **경로 문자열은 구현 때 KOS `openapi.yaml`(1.0.1)의 operationId 에서 옮긴다.** 위 경로 칸은 지금 공개 경로 모양(`<영역>/open/v1/queries/<동작>` — KDA 표 · 코드 규약: `app/kos/reservation_sync.py:24` · `:29-31`)으로 적은 것이다. 스펙의 경로와 다르면 **스펙이 맞다**. WP-BE1 리포트에 실제 경로를 적는다
- **부르지 않는 것**: 빈 검색어 `searchProductOptionSummaries`(D-05 · R1 §1.5 가이드 권고) · `getProduct` 단건(②가 같은 값 · R1 §1.3)
- ③ 은 ② 가 성공했을 때만 부른다. ③ 응답에서 빠진 옵션(KOS 가 「삭제 · 사용 중지 · 없는 id」를 뺀다 — R1 §1.4)은 `medical_service_kos_id` 를 **바꾸지 않는다**(이전 값 그대로). 나머지 작업은 서로 독립이다
- **실패**(네트워크 · 5xx · 401 재시도 뒤 · 2xx 인데 `data` 가 배열 아님): 그 작업이 반영하는 표는 **건드리지 않는다**(이전 값 · `present` 그대로). 다른 작업은 계속한다. 하나라도 실패하면 `sync_state("menu")` 의 `last_error` 에 `"<작업 이름>: <오류>"` 를 `; ` 로 이어 적고, 다 성공하면 `last_ok_at` 을 찍는다. **하나라도 실패한 바퀴는 `last_ok_at` 을 지우지 않는다 — 이전 값을 그대로 두고 `last_error` 만 바꾼다**(`set_sync("menu", None, <오류>)` 는 `ok_at or prev_ok` 로 이전 값을 남긴다 · 코드 규약: `app/repository/repo.py:452-455`. `syncedAt` 이 「언제 받은 메뉴인가」를 계속 알려 주게 하기 위해서다 — D-36). 로그에는 예외 종류 · HTTP 상태만 남긴다(본문 · 키 없음)(코드 규약: `app/kos/reservation_sync.py:35-43` `_err` · `_data_list` · `:177-190` `master()` · `app/kos/sync.py:158-169`)
- 작업마다 `present` 맞추기: 그 작업이 성공했을 때만, 이번 결과에 없는 행을 `present = 0` 으로 둔다(코드 규약: `app/kos/reservation_sync.py:192-202` `_zones` · `mark_absent_kos`)
- 동시에 두 번 돌지 않게 잠금 하나를 둔다(코드 규약: `app/kos/reservation_sync.py:173` `_master_lock`)
- 크기 · 시간: 한 바퀴에 약 0.9MB 와 ③ 정도이고, 각 작업은 0.03 ~ 0.8초다(R1 §6). 1시간 주기면 부담이 없다

### 4.2 고객 이름 검색 (D-15 · D-16 · D-17)

| 항목 | 계약 | 근거 |
|---|---|---|
| 작업 | **내부** `visitor/v2/queries/get-visitors`(지금 `PATH_VISITORS`) · `KosClient.internal`(시스템 계정 토큰 · 브라우저 UA) | D-15 · 코드 규약: `app/service/reservations.py:78` · `app/kos/client.py:10-11` · `:182-185` |
| 본문 | `{indexOfPage: 0, countInPage: 1000, visitorName: <다듬은 이름>, phoneNumber: "", chartNumber: "", sort: {by: "lastVisitedDateTimeUtc", order: "DESC"}}` | D-16 · 코드 규약: `app/service/reservations.py:448-450`(같은 본문 · 페이지 크기만 다름) · R4 §2.1(`countInPage` 100 · 500 · 1000 · 5000 모두 200) |
| 한 페이지만 | 조회 1건당 `get-visitors` **1번**. 다음 페이지를 부르지 않는다 | D-16 |
| 상한 | 응답 `count` 가 1000 을 넘으면 받은 결과를 **거르지 않고** §5 갈래 「없음」(`404 customer_not_found` — D-21 과 같은 바이트)으로 끝낸다. 시술권 조회도 하지 않는다 | D-16 · D-21 |
| 중복 제거 | 받은 `data[]` 를 KOS `id` 로 중복 제거한 뒤(처음 나온 것을 남김) §5 로 거른다 | D-16 |
| 이름 | 보낼 때는 앞뒤 공백만 지운다(`strip()`). 가운데 공백 · 순서는 그대로다. 다시 검색하지 않는다. 받은 뒤의 이름 정확 일치는 §5 3단계다 | D-17 · R4 §2.1 「이름 검색 시험」 |
| 응답에서 쓰는 칸 | `count`(상한) · `data[].id`(중복 제거) · `name` · `phoneticName`(이름 대조 · 사본) · `nationality` · `isNew` · `chartNumber` · `gender`(사본 덮어쓰기) · `email`(거르기에만 · 저장 안 함) · `lastVisitedDateTimeUtc`(최근 방문일) | D-16 · D-19 · R4 §0 #1 · 코드 규약: `app/kos/reservation_sync.py:143-151` |
| 실패 | KOS 호출 실패 = `502 kos_unavailable`. **2xx 인데 `data` 가 배열이 아님(키가 없는 경우 포함) = `502 kos_unavailable`** — 「0명」으로 보지 않는다. 그래서 조회는 404 가 아니라 502 이고, 예약은 새 고객을 만들지 않는다(`create-visitor` 0번) | D-14 · D-15 · 코드 규약: `app/service/reservations.py:454-458`(지금 검색 실패 = `502 kos_unavailable`) · `app/kos/reservation_sync.py:39-43` `_data_list`(같은 규칙) · 코드 검수 r1 W1 |

- `lastVisitedDateTimeUtc` 는 지금 코드가 정렬 키로 보내는 이름이다. 목록 원소에 이 칸이 실제로 오는지는 조사 4 가 키 목록을 적지 않아 **확인하지 않았다**. WP-BE4 의 데모 확인 1회로 확인한다(WORK-012). 키가 없거나 빈 값이면 응답 `lastVisitDate = null` 이다(지어 채우지 않는다)

### 4.3 남은 시술권 (D-12 · D-08 · D-31)

> (0.4.1) DEC-010 D-12 의 원천(공개 → 내부)과 범위(사용 가능만 → 사용 가능 또는 사용 중)는 **DEC-012 D-08 이 고쳤다**(DEC-010 D-12 고침 줄 · 검수 r1 W5 · DQ3). 아래 「작업」 · 「거르기」 칸이 그 고침이다.

| 항목 | 계약 | 근거 |
|---|---|---|
| 작업 | ~~공개 `getTicketBundlesQuery` — `ticket/open/v1/queries/get-ticket-bundles` · 본문 `{visitorId}`~~ (0.4.0 고침) → **내부** `ticket/v1/queries/get-ticket-bundles` · `KosClient.internal` · 본문 `{visitorId: <KOS 고객 id>, sort: {by: "ticket.createdDateTimeUtc", order: 2}}`(`상담대기.har` 의 요청 모양 그대로) · 고객 1명당 1번. 응답 묶음 모양은 공개와 같다(`optionConfiguration` · `price` · `ticketSets[].tickets[]{id, status, price, createdDateTimeUtc}`) | DEC-012 D-08 ② · C1 §3-3 · `상담대기.har` 키만 |
| 언제 | 고객 조회(§6.4)에서 1명이 맞았을 때만, 매 조회마다 부른다. 캐시 · 저장은 없다 | D-12 |
| 결과 없음 | 응답이 `{}`(`data` 키 없음)이거나 `data: []` 이면 → 「남은 시술권 없음」(`tickets: []`) | KDA 182행 · R2 §3.2 · D-14 |
| (0.4.0) 거르기 | (0.4.5 · DEC-012 D-46) **거르기가 먼저다** — 장 상태만 보고 산 묶음을 고른 뒤, 고른 묶음만 아래 표의 칸을 만든다(모양 검사 포함). 걸러진 묶음의 모양(`price` 등)은 보지 않는다 — 내지 않을 묶음의 모양 오류는 `502` 사유가 아니다(2026-11-16 로컬 e2e · 데모 고객 1명의 묶음 12 중 4 가 다 쓴 · 다 취소된 묶음이고 `price.value` 가 없었다 · 이 순서가 거꾸로면 lookup 전체가 `502`). 묶음 안 장 중 `AVAILABLE` 또는 `IN_USE` 가 **1장 이상**인 묶음만 낸다. 둘 다 0 인 묶음(다 쓴 · 다 취소된 묶음)은 뺀다 — ~~내부 조회가 그런 묶음을 주는지는 확인하지 않았으므로~~ (0.4.3 · KOS0 ④ **확인함**: 내부 조회는 다 쓴 · 다 취소된 묶음을 준다 — 데모 86묶음 중 11) 우리가 거른다(D-12 「다 쓴 · 취소된 시술권은 내주지 않는다」). 그래서 **사용 중 장만 남은 묶음이 새로 나온다**(공개 조회에서는 통째로 빠졌다 — C1 §3-3) | DEC-012 D-03 · D-08 ② · D-12 |
| 모양 오류 | 2xx 인데 `data` 가 있으면서 배열이 아니면 → `502 kos_unavailable`. (0.4.5) 고른 묶음(거르기 뒤)의 칸 모양 오류도 `502` — `bundlePrice` 의 규칙은 아래 표 | 코드 규약: `app/kos/reservation_sync.py:39-43` · DEC-012 D-46 |
| 실패 | 네트워크 · 5xx · 4xx · 401 재시도 뒤 = `502 kos_unavailable`(고객 칸만 주고 시술권을 빈 배열로 주지 않는다 — 「시술권 없음」과 섞이면 D-14 가 깨진다). (0.4.1) 시술권 실패는 지금처럼 lookup 전체 502 다 — 선불카드(§4.4)만 부분 실패로 둔다(DEC-012 D-36) | D-14 · 코드 규약: `app/service/kos_errors.py:6` |

묶음(`data[]` 원소) → 응답 한 줄(§6.4 `tickets[]`): 모양은 KDA 258행 · HAR(`reference/2026-11-11-cc-product/har/` 내부 `get-ticket-bundles`, 키만)을 따른다.

| 응답 칸 | KOS | 규칙 | 근거 |
|---|---|---|---|
| `optionId` | `optionConfiguration.optionId` | 그대로(KOS id 문자열). 메뉴에 없는 옵션이어도 그대로 준다 | D-08 · D-31 · 코디 Q2 |
| `optionTitle` | `optionConfiguration.optionTitle` | 그대로(산 시점 값). 메뉴 이름으로 덮지 않는다 | D-08 · R2 §1.3 · R3 §0 |
| `remainingCount` | `ticketSets[].tickets[].status` | 묶음 안 모든 세트의 `AVAILABLE` 장수 합. `IN_USE`(쓰는 중) · `USED` · `CANCELED` 는 넣지 않는다 | D-31 · R2 §3.2 |
| `inUseCount` | `ticketSets[].tickets[].status` | (0.4.0) 묶음 안 모든 세트의 `IN_USE`(사용 중 — 시술 작업에 붙어 아직 안 끝남) 장수 합 | DEC-012 D-08 ② · C1 §3-3 |
| `totalCount` | `ticketSets[].tickets[]` | 묶음 안 모든 세트의 시술권 장수 합(상태 무관). (0.4.0) 뜻은 그대로다. 내부 조회는 `IN_USE` 장을 주므로 그만큼 값이 커질 수 있다 | D-31 · R2 §3.3 · DEC-012 D-03 |
| `purchasedDate` | `ticketSets[].tickets[].createdDateTimeUtc` | 그중 가장 이른 값의 KST 날짜 `YYYY-MM-DD`. 시술권은 수납이 끝날 때 만들어진다. 값이 없으면 null | D-31 · R2 §2(「발행 일시(수납 완료로 티켓그룹 생성)」) |
| `bundlePrice` | `price{value, currency}` | **KOS 묶음 가격 그대로**. `value` 는 정수로 바꿔 준다(원 단위). 칸 이름에 `purchase` · `VatIncluded` 를 넣지 않는다. (0.4.5) 내부 원천은 0 값을 빼고 보낸다 — `price` 가 객체인데 `value` 키가 없으면 `0` 으로 준다(2026-11-16 로컬 e2e · 데모 고객 1명의 묶음 12 중 4 가 `price = {currency}` 만 · 같은 묶음을 공개 원천은 `value` 와 함께 줌). `price` 가 없거나 객체가 아니거나 `value` 가 숫자가 아닌 꼴(문자열 등)이면 그대로 `502 kos_unavailable` | D-08 · D-31 · R2 §0(연결 그림) · §3.3 · DEC-012 D-46 |

- KOS 그대로의 성질을 Swagger 설명에도 적는다(지어 바꾸지 않는다 · D-08 · D-31). ① `bundlePrice` 는 **고객이 낸 돈이 아니다**. 산 시점 값에서 출발하지만, GROUP 묶음에서 한 세트를 다 쓰면 그 세트가 응답에서 빠지므로 `totalCount` 와 함께 줄 수 있다(R2 §3.3 확인 1건). **부가세 포함 여부는 표기하지 않는다**. ② ~~`AVAILABLE` 이 0장인 묶음은 KOS 가 주지 않는다(R2 §2)~~ (0.4.0 고침) `AVAILABLE` 과 `IN_USE` 가 둘 다 0장인 묶음은 나오지 않는다 — 사용 중 장만 남은 묶음은 나온다(위 「거르기」). ③ `remainingCount` 는 `AVAILABLE` 만 센다 — `IN_USE`(쓰는 중)는 남은 장수에 넣지 않고 `inUseCount` 로 따로 준다. ④ (0.4.0) 시술권 **만료일 칸은 없다**(KOS 에 없음 · 발행일 `purchasedDate` 만 · DEC-012 D-07)
- 순서 = KOS 배열 순서

### 4.4 (0.4.0) 선불카드 (DEC-012 D-08 ③)

| 항목 | 계약 | 근거 |
|---|---|---|
| 작업 | **공개** `getPrepaidCardSummaries` — `purchase/open/prepaid-card/v1/queries/get-prepaid-card-summaries` · 본문 `{visitorId: <KOS 고객 id>, available: true}` · 고객 1명당 1번. `available: true` = 「만료되지 않았고 잔액이 남은 카드만」(KOS 스펙 · KOS 웹도 같은 조회를 `available: true` 로 부른다 — `상담대기.har` 요청 키) | DEC-012 D-08 ③ · D-31 · C1 §3-5 |
| 언제 | lookup(§6.4)에서 고객이 1명으로 정해졌을 때만, 시술권 조회와 **동시에**(`asyncio.gather`) 매번 부른다. 저장 · 캐시 없음 | DEC-012 D-08 · D-12 와 같은 방식 |
| 결과 없음 | `{}` · `data: []` → `prepaidCards: []` | §4.3 과 같은 규칙 |
| 모양 오류 · 실패 | `data` 가 있으면서 배열 아님 · 원소 모양 깨짐 · 네트워크 · 5xx · 4xx · 401 재시도 뒤 → (0.4.1 고침) **lookup 은 `200`** 이다. `prepaidCards: null` · `partialErrors: ["prepaidCards"]`(§6.4). 빈 배열로 주지 않는다(「카드 없음」과 섞지 않는다 · D-14 와 같은 이유). lookup 에 새 502 를 만들지 않는다. ~~lookup 전체 `502 kos_unavailable`~~ | DEC-012 D-36 · D-23 · 검수 r1 W4 |

카드(`data[]` 원소) → 응답 한 줄(§6.4 `prepaidCards[]`):

| 응답 칸 | KOS | 규칙 | 근거 |
|---|---|---|---|
| `title` | `title` | 그대로 | C1 §3-5 |
| `issuedDate` | `createdDateTimeUtc` | KST 날짜 `YYYY-MM-DD` · 없으면 null | C1 §3-5 · §4.3 `purchasedDate` 와 같은 꼴 |
| `expiresAt` | `expirationDateTimeUtc`(스펙 필수 · 만료 일시) | ISO `+09:00` · 없으면 null | C1 §3-5 |
| `balance` | `remainingBalance{balance, total}` | `{remaining, total}` — 둘 다 **§6.1 금액 꼴 `{value: int, currency}`**(KOS 금액 객체 · `value` 는 정수로 바꿔 준다). 값이 없으면 그 칸 null | C1 §3-5 · `상담대기3.har` 내부 `get-visitor-prepaid-card-balance` 의 `remainingBalance.balance` · `.total` = 금액 객체(키 · 꼴만) · 검수 r1 W3 · KOS0 ③(공개 요약 · 금액 객체 확인) |
| `point` | `remainingPoint{balance, total}` | `{remaining, total}` — 위와 같은 금액 꼴 | C1 §3-5 · 같은 HAR `remainingPoint.balance` · `.total` = 금액 객체 |

- 내지 않는 칸: 카드 KOS id · `description` · `ownerId` · `updatedDateTimeUtc`(KOS id 는 메뉴 · 시술권 id 와 직원 목록 `kosAccountId`(§6.17 · 0.4.7)에만 낸다 — 코디 Q2 · 부록 B · DEC-012 D-48)
- (0.4.1 고침) 금액 꼴의 근거는 KOS 웹이 부르는 **내부** 합산 조회(`get-visitor-prepaid-card-balance`)다. 우리가 부르는 **공개** 요약 조회의 원소도 같은 금액 객체다 — (0.4.3) WORK-014 KOS0 ③ 확인함(카드가 있는 데모 고객 1명 · 4/4 장 · `value` int). 표 · T51 고침 없음. 만료 시각 꼴은 초 없는 `YYYY-MM-DDTHH:MMZ` 로 온다(파싱 몫 · BE1 시험). ~~「원 단위 숫자」~~
- 순서 = KOS 배열 순서

---

## 5. 조회 규칙 — 이름 + 이메일 (D-15 ~ D-22)

고객 조회(§6.4)와 예약(§6.5)이 **같은 함수**로 고객을 정한다(D-32).

| 단계 | 규칙 | 근거 |
|---|---|---|
| 0. 입력 | 요청 `name` · `email` 은 둘 다 필수다. 앞뒤 공백을 지운 뒤 비면 `400 invalid_request` 이다 | D-11 · D-32 · 코드 규약: `app/main.py:117-121` |
| 1. 검색 | `name.strip()` 으로 §4.2 를 **한 번** 부른다. `count` > 1000 이면 여기서 「없음」 | D-16 · D-17 |
| 2. 중복 제거 | KOS `id` 로 중복 제거 | D-16 |
| 3. 이름 정확 일치 | 입력 이름과 KOS `name` · `phoneticName` 을 각각 **공백을 전부 지우고**(가운데 공백 포함) 대소문자를 무시해(`lower()` — 4단계 이메일과 같은 방식) 견준다. 둘 중 하나라도 **정확히 같은** 고객만 남긴다. 부분 일치로만 걸려 온 고객은 빠진다. KOS 쪽 값이 없거나 비면 그 칸은 맞지 않은 것으로 본다 | D-19 · R4 §2.1 |
| 4. 이메일 정규화 | 입력과 KOS `email` 양쪽 모두 `strip().lower()`. KOS 쪽에 키가 없거나 빈 문자열이면 그 고객은 후보에서 뺀다. 형식 검사(`@` 유무 등)는 하지 않는다 — 같으냐만 본다 | D-18 · R4 §2.2 |
| 5. 이메일 대조 | 정규화한 값이 **정확히 같은** 고객만 남긴다 | D-18 |
| 6. 갈래 | **0명** → 「없음」 · **1명** → 그 고객 · **2명 이상** → 「특정할 수 없음」(아무도 돌려주지 않음) | D-20 · D-21 |

- 「없음」은 이름이 틀린 경우(부분 일치만 맞는 경우 포함) · 이메일이 틀린 경우 · 고객이 없는 경우 · KOS 에 그 고객의 email 이 비어 있는 경우 · 이름 검색 `count` 가 1000 을 넘는 경우가 **모두 같은 응답**이다(코드 · 문구 · 칸이 같다). 어느 쪽이 틀렸는지 응답에서 알 수 없다(D-16 · D-21 · D-22)
- 보내는 이름(1단계)은 앞뒤 공백만 지우고, 견주는 이름(3단계)은 공백을 전부 지운다. 서로 다른 단계다 — KOS 에 다시 검색하지 않는다(D-17)
- 「특정할 수 없음」 응답에도 후보 수 · 이름 · id 를 싣지 않는다(D-20 · D-21)
- 1명이 맞으면 그 고객을 `customer` 사본에 덮어쓰고(§3.1) ccc `customerId` 를 얻는다(코드 규약: `app/service/reservations.py:461-466`)

---

## 6. 외부 API (D-10 · D-11 · D-27 ~ D-36 · DEC-011)

### 6.1 공통

| 항목 | 계약 | 근거 |
|---|---|---|
| 경로 | `/api/ext/…` — 직원 API 와 나눈다 | D-10 |
| 인증 | 헤더 `X-Api-Key: <연동처 키>`(§7.1). `Authorization` 은 보지 않는다 | D-10 · D-23 · 코드 규약: `app/api/public_questionnaire.py:1-8` · `app/openapi_docs.py:64-66`(`X-Questionnaire-Token` 선례) |
| 형식 | JSON · 칸 이름 camelCase · 요청에 모르는 키가 있으면 `400 invalid_request` | 코드 규약: `app/openapi_docs.py:54-62` · `app/schemas/reservations.py:696`(`_Req`) |
| 시각 | 요청 `start` = ISO-8601(오프셋이 없으면 KST). 응답 날짜 = KST `YYYY-MM-DD` · 응답 시각 = ISO `+09:00` 초 단위 | 코드 규약: `app/domain/reservation_rules.py:63-69` · `app/openapi_docs.py:60-62` |
| 금액 | `{value: int(원), currency: "KRW"}`. 메뉴 정가는 칸 이름으로 부가세 별도(`…ExVat`)를 밝힌다. 시술권 `bundlePrice` 는 KOS 묶음 가격 그대로이고 부가세 포함 여부를 표기하지 않는다(§4.3) | D-09 · D-30 · D-31 · R1 §1.1 `Money` |
| id | 메뉴 · 시술권의 카테고리 · 상품 · 옵션 · 시술 id = **KOS id 문자열**. 고객 id · 예약 id = **ccc 정수**(직원 API 와 같다). 고객의 KOS id 는 내지 않는다. (0.4.7) **예외 하나** — 직원 목록(§6.17)의 `kosAccountId` 는 직원의 KOS 계정 id 문자열이다(DEC-012 D-48 · 다른 응답의 `staffId` 는 그대로 ccc 정수) | 코디 Q2 · D-08 · D-12 · DEC-012 D-48 |
| 오류 | `{"error": {"code", "message"}}`. 분기는 `code` 로 한다. 외부 API 오류에는 `step` · `candidate` 를 싣지 않는다 | 코드 규약: `app/main.py:66-67` · `:113-125` · `app/api/docs.py:23-37` |
| 캐시 | 모든 `/api/ext` 응답(오류 포함)에 `Cache-Control: no-store` | 코드 규약: `app/main.py:104-111`(공개 경로 선례) |
| 검사 순서 | **키(`401 ext_unauthorized`) → 제한(`429 too_many_requests`) → 칸 검증(`400 invalid_request` — 필수 · 타입 · 모르는 키 · 빈 값) → 엔드포인트 규칙.** 단 ① IP 차단(§7.3 — `429`)은 미들웨어라서 무엇보다 먼저다. ② JSON 이 아닌 본문(형식이 깨진 JSON)은 FastAPI 가 본문을 읽는 단계에서 끝나므로 **키보다 먼저 `400`** 이다. ③ 없는 경로는 라우터 밖이라 **키 없이 `404 not_found`** 다 | 코드 규약: `app/openapi_docs.py:40`(검사 순서를 문서에 적는 선례) · `app/main.py:117-125` · FastAPI 요청 처리 순서(본문 JSON 읽기 → 의존성 → 칸 검증 오류) · review-doc r1 W6 |

### 6.2 공통 오류 표 (외부 경로 전부 — 0.3.0 셋 · 0.4.0 일곱 포함 · DEC-011 D-01 · DEC-012 D-01)

| HTTP | code | 언제 | 근거 |
|---|---|---|---|
| 401 | `ext_unauthorized` | `X-Api-Key` 가 없거나 · 비었거나 · 어느 연동처 키와도 같지 않거나 · 그 연동처 env 가 비어 꺼졌을 때. 직원 Bearer 토큰만 실린 경우도 같다 | D-10 · D-23 · 코드 규약: `tests/test_openapi_docs.py:119-141`(`unauthorized` ↔ `require_login` 단언 — 외부 키는 다른 code 여야 그 시험이 그대로 맞다) |
| 429 | `too_many_requests` | 그 키로 최근 60초 안에 60번을 이미 불렀을 때 · 그 IP 의 키 없는 거절이 최근 60초 안에 10번 이상일 때(§7.3) | D-25 · D-34 · 코드 규약: `app/service/questionnaire.py:243`(같은 code) · `:254` |
| 400 | `invalid_request` | 본문이 JSON 이 아님 · 필수 칸 · 타입 · 모르는 키 · 앞뒤 공백을 지우면 빈 `name` · `email` · ISO 가 아닌 `start` · (가능 시간대) `date` 없음 · 꼴 틀림 · 범위 밖(§6.6) · (0.4.0) 경로 id(`reservationId` · `customerId` · `clinicId`)가 정수 아님 · 열람 헤더 꼴 틀림(§6.10 — **새 경로 넷(예약 상세 · 쓰기 셋)만**. lookup 과 그 밖 기존 경로는 이 사유로 400 을 내지 않는다 · DEC-012 D-37) | 코드 규약: `app/main.py:117-121`(0.4.0 절은 `0a58aba` `:120-124`) · `app/domain/reservation_rules.py:63-69` |
| 404 | `not_found` | 없는 `/api/ext/…` 경로 | 코드 규약: `app/main.py:123-125` |
| 405 | `http_error` | 있는 `/api/ext/…` 경로에 틀린 메서드(예 `GET /api/ext/customers/lookup`). 키 검사 전에 끝난다(키 없는 거절 · §3.4) | 코드 규약: `app/main.py:123-125`(404 가 아닌 HTTP 오류 = `http_error`) |
| 500 | `internal_error` | 처리하지 못한 예외(서버 쪽 잘못). `ext_call` 1줄을 쓰고, `client` 가 null 이어도 IP 카운트(§7.3)에는 넣지 않는다 | 코드 검수 r2 N1(미들웨어 `except` 갈래) |

### 6.3 `GET /api/ext/menu` — 메뉴 조회 (D-11 ①)

우리 DB(§3.2)에서만 읽는다. KOS 를 부르지 않는다. 질의 칸은 없다.

**응답 200** `ExtMenu`:

| 칸 | 타입 | 뜻 · null | 근거 |
|---|---|---|---|
| `syncedAt` | string \| null | 메뉴 동기화가 마지막으로 다 성공한 시각(`sync_state("menu").last_ok_at` · ISO `+09:00`). 그 뒤 바퀴에서 작업이 실패해도 **이전 시각이 그대로 남는다**(§4.1). 한 번도 다 성공한 적 없으면 null. 메타 칸 — 언제 받은 메뉴인지 연동처가 알게 한다 | D-36 · 코드 규약: `app/repository/db.py:86-88` · SPEC-005 §4.2(`sync.lastError` 선례) |
| `categories[]` | array | 지금 있는 카테고리. `order` 오름차순 → `id` | D-07 · D-27 |
| `.id` · `.name` · `.order` | string · string · int | KOS 값 | D-29 · 코디 Q2 · Q5 |
| `.translsMap` | object | KOS `translsMap` 그대로. 없으면 `{}` | D-29 |
| `.products[]` | array | 그 카테고리에 속한(`category_kos_ids` 에 그 id 가 있는) 지금 있는 상품. `seq` 순서(KOS 배열 순서). 한 상품이 카테고리 여럿에 걸리면 각 카테고리 아래에 다 나온다 | D-07 · D-27 · R1 §1.2 · §4 |
| `..id` · `..title` · `..description` · `..isEvent` · `..translsMap` | string · string · string · bool · object | KOS 값. `description` 이 없으면 빈 문자열 | D-29 · 코디 Q5 |
| `..options[]` | array | 그 상품의 지금 있는 옵션. `seq` 순서 | D-07 · D-27 |
| `...id` · `...type` | string · `SINGLE` \| `GROUP` \| `CONSULTATION` | KOS 판별자 그대로 | D-28 |
| `...title` · `...description` · `...translsMap` | string · string · object | KOS 값 | D-29 · 코디 Q5 |
| `...listPriceExVat` | `{value, currency}` \| null | **정가 · 부가세 별도**(KOS `price.amount`). CONSULTATION 은 null | D-09 · D-28 · D-30 |
| `...count` | int \| null | SINGLE 의 시술 횟수(KOS `count`). GROUP · CONSULTATION 은 null(GROUP 은 구성마다 있다) | 코디 Q5 · R1 §1.1 |
| `...unit` | `{type, value}` \| null | SINGLE 의 단위 = 이어진 진료항목의 `configuration.unit`(§3.3). 진료항목이 이어지지 않았거나 단위가 없으면 null. GROUP · CONSULTATION 은 null | 코디 Q4 · Q5 · R1 §2.2 |
| `...procedure` | `{id, name}` \| null | SINGLE 의 시술. GROUP · CONSULTATION 은 null. SINGLE 이어도 KOS 가 주지 않으면 null | D-27 · R1 §2.2 |
| `...compositions[]` | array | GROUP 의 구성(지금 있는 것 · `seq` 순서). SINGLE · CONSULTATION 은 `[]` | D-27 · D-28 |
| `....title` · `....count` | string · int \| null | KOS 값. `count` 는 KOS 가 주지 않으면 null | 코디 Q5 |
| `....unit` | `{type, value}` \| null | KOS 구성 `unit` 그대로(`UnitType_UNKNOWN` 도 그대로 준다). KOS 가 주지 않으면 null | 코디 Q5 · R1 §1.1 |
| `....listPriceExVat` | `{value, currency}` \| null | 구성 정가 · 부가세 별도. KOS 가 주지 않으면 null. 구성 정가를 다 더하면 옵션 정가가 된다(R1 §3) | D-30 · 코디 Q5 |
| `....procedure` | `{id, name}` \| null | 구성의 시술. KOS 가 주지 않으면 null | D-27 |

- **단위 `{type, value}` 의 `value`**(옵션 `unit` · 구성 `unit`): KOS 가 주지 않으면 null 이다. 위 표의 「KOS 가 주지 않으면 null」 칸은 모두 지어 채우지 않는다(D-08 · D-29 「KOS 그대로」 · 데모에서는 모두 값이 있었다 · 코드 검수 r1 W7)
- **「지금 있는 것」**(D-07): `present = 1` 이면서 KOS 표시가 살아 있는 것이다. 카테고리는 `opened` 이고 `deleted` 가 아니어야 한다. 상품은 `closed` 도 `deleted` 도 아니어야 한다. 옵션은 `deleted` 가 아니어야 한다. 위 층이 빠지면 아래 층도 나오지 않는다. 지금 있는 카테고리에 하나도 걸리지 않은 상품은 응답에 나오지 않는다
- **내지 않는 칸**(D-27 · D-30 · 코디 Q5): 진료항목 · 기기 · 약물 객체, `medicineAndMachines`, 공급가 · 부가세 · 면세 · 과세 유형 · 특별가(`additional`) · 프로모션, `caution` · `cautions` · 이미지 URL · `displayChannels` · `badges` · `frequentlyUsedOption` · 노출 · 제공 기간 · deprecated 칸. 이 칸들은 DB `raw` 에만 있다
- 오류는 공통 표(§6.2)뿐이다. 메뉴가 비어 있으면(첫 동기화 전 · 실패) `200` 에 `categories: []` · `syncedAt: null` 이다

### 6.4 `POST /api/ext/customers/lookup` — 고객 조회 (D-11 ② · D-12 ~ D-14 · D-31 · 0.4.0 고침 DEC-012 D-02 · D-03 · D-08 · D-18 · 0.4.1 D-32 · D-33 · D-36 · D-37)

이름 · 이메일을 경로나 질의에 싣지 않으려고 `POST` 본문으로 받는다. 접근 로그에 남지 않게 하기 위해서다(D-24 · 코드 규약: `app/api/public_questionnaire.py:6` 「토큰은 경로 · 쿼리에 싣지 않는다(접근 로그)」).

**요청** `ExtLookupRequest`: `{"name": "<이름>", "email": "a@example.com"}` — 둘 다 필수 string. **(0.4.0) 또는** `{"customerId": <ccc 정수>}` 하나만.

- 두 갈래 중 **정확히 하나**만 받는다: `name` + `email` 둘 다 · 또는 `customerId` 만. 둘을 섞거나(`customerId` + `name` 등) · 셋 다 없거나 · `name` 과 `email` 중 하나만 오면 `400 invalid_request`(DEC-012 D-33). 모르는 키 · 빈 값 규칙은 그대로다(`name` · `email` 은 앞뒤 공백을 지우면 빈 값 400 · `customerId` 는 1 이상 정수). 기존 요청 모양(`name` + `email`)은 바이트까지 그대로 통한다(DEC-012 D-03)
- (0.4.1 · 검수 r1 W12) **바뀌는 것 둘 — 변경 이력 · Swagger 에 행동 변화로 적는다**: ① 요청 스키마에서 `name` · `email` 이 `required` 가 아니게 된다(세 칸 모두 선택 · 갈래 검사는 모델 검사로 한다). ② 틀린 요청의 400 `message` — 지금은 `body.email: Field required` 꼴(`<위치>: <이유>` · 코드 규약: `app/main.py:120-124`)이다. 0.4.1 부터 갈래 오류(섞임 · 한쪽만 · 빈 요청)는 **`body: ` 로 시작하는 한 꼴**이다(문구는 구현이 정하고, 시험은 접두만 단언한다). `code` 는 그대로 `invalid_request` 다. 빈 값 · 타입 · 모르는 키의 message 는 지금 꼴 그대로다
- `customerId` 갈래에는 DEC-010 의 「이름 + 이메일 둘 다」 규칙이 걸리지 않는다(DEC-012 D-02 — 열거 위험 수용)
- (0.4.2 · 검수 r2 N1) **요청 모델을 따로 둔다.** 지금 `ExtCustomerRequest`(과거 시술 §6.7 · 예약 내역 §6.8 의 본문)는 `ExtLookupRequest` 를 **상속**한다(코드 규약: `app/schemas/ext.py:24-30` · `:157-158` 「조회와 같은 칸 · 같은 검증」 · `app/api/ext.py:278-279` · `:285-286`). lookup 갈래를 그 모델에서 고치면 두 기존 경로의 계약(필수 칸 · `customerId` 를 받음 · message)까지 바뀐다. 그래서 ① `ExtCustomerRequest` 는 **지금 칸 · 검증 그대로**(`name` · `email` 필수 · 빈 값 400 · `customerId` 없음 = 모르는 키 400 · message `body.<칸>: …` 꼴) 둔다 — 상속을 끊고 지금 두 칸 · 검증을 그 모델에 직접 둔다(또는 두 칸만 있는 바탕 모델을 두고 lookup 새 모델 · `ExtCustomerRequest` 가 각자 그것을 쓴다). ② lookup 은 새 모델(세 칸 선택 + 갈래 검사)을 쓴다. 두 기존 경로의 Swagger 요청 스키마는 그대로다(DEC-012 D-02 「기존 여섯 그대로」)
- 선택 헤더 `X-Ext-Staff-Id`(§6.10)를 받는다. (0.4.1) **lookup 은 기존 경로라 헤더 꼴이 틀려도 400 을 내지 않는다** — 없는 것으로 본다(`ext_view` 의 `staffId` null · 행위자 `ext:<연동처>` · DEC-012 D-37 ②)

**처리**:

- **이름 + 이메일 갈래**: §5 → 1명이면 고객 사본 덮어쓰기(지금 그대로) → §4.3 시술권 1번 + §4.4 선불카드 1번(동시). 시술권이 실패하면 `502`(지금 그대로), 선불카드만 실패하면 `200` + `prepaidCards: null` + `partialErrors: ["prepaidCards"]`(DEC-012 D-36)
- **(0.4.0) `customerId` 갈래**: ccc 고객 사본에서 `customer.id` → `kos_id` 를 찾는다. 없으면 `404 customer_not_found`(이름+이메일 갈래 404 와 **바이트까지 같은** 본문 · KOS 호출 0). 있으면 내부 `visitor/v2/queries/get-visitor {id: <kos_id>}` 1번으로 고객 칸(이름 · `isNew` · `lastVisitedDateTimeUtc`)을 받아 사본을 덮어쓴다(이름 검색 갈래의 `_keep` 과 같은 `upsert_customer` · email 저장 안 함) → §4.3 + §4.4(동시). `get-visitor` 응답 36키에 `isNew` · `lastVisitedDateTimeUtc` 가 있다(`상담대기.har` #1 키만 · DEC-012 D-32). KOS 가 그 고객을 「없음」으로 주면 — HTTP 404, **또는** 400 + `errorProperties` 의 `id` 가 `NotFound`(0.4.4 · 코드 검수 r1 Q2 · DEC-012 D-45 · 선례 = 문진 읽기의 `visitorId` `NotFound` 판정 `app/service/reservations.py:614`) — `404 customer_not_found`(같은 본문). 실물 꼴은 WORK-014 E2E-LOCAL ① 에서 없는 KOS id 로 1번 본다(읽기), 그 밖 실패 · `data` 가 객체 아님 = `502 kos_unavailable`(코드 규약: `app/service/reservations.py:79` `PATH_VISITOR` · `:1063-1067`(같은 읽기 · 같은 형식 검사) · `app/kos/reservation_sync.py:143-151` `upsert_customer`)
- **열람 기록**: 200 이면 `event_log` `ext_view` 1줄(§3.5 · §6.10)

**응답 200** `ExtLookupResponse`:

| 칸 | 타입 | 뜻 · null | 근거 |
|---|---|---|---|
| `customer.customerId` | int | ccc 고객 id(직원 API 와 같은 체계) | D-31 · 코디 Q2 |
| `customer.name` | string | KOS 고객 이름 | D-31 |
| `customer.isNew` | bool | KOS `isNew`(신규 여부) | D-31 |
| `customer.lastVisitDate` | string \| null | 최근 방문일 — KOS `lastVisitedDateTimeUtc` 의 KST 날짜 `YYYY-MM-DD`. 없으면 null(§4.2) | D-31 |
| `tickets[]` | array | 남은 시술권 — (0.4.2 고침 · 검수 r2 N4) **사용 가능 또는 사용 중 장이 1장 이상인 묶음** 한 줄씩(§4.3 「거르기」 · DEC-012 D-08). ~~사용 가능한 묶음~~ 코드의 칸 설명(`app/schemas/ext.py:148`)도 이 뜻으로 고친다(§4.3 표). **없으면 `[]`** — 「고객은 있는데 남은 시술권 없음」 | D-12 · D-14 · D-31 |
| `tickets[].optionId` · `.optionTitle` | string · string | §4.3 | D-08 · D-31 |
| `tickets[].remainingCount` · `.totalCount` | int · int | §4.3 | D-31 |
| `tickets[].inUseCount` | int | (0.4.0) 사용 중(`IN_USE`) 장수 · §4.3 | DEC-012 D-08 ② |
| `tickets[].purchasedDate` | string \| null | §4.3 | D-31 |
| `tickets[].bundlePrice` | `{value, currency}` | §4.3 · **KOS 묶음 가격 그대로** — 고객이 낸 돈이 아님 · 산 시점 값에서 출발하지만 세트를 쓰면 줄 수 있음 · 부가세 포함 여부 표기 안 함 | D-31 |
| `prepaidCards[]` | array \| null | (0.4.0) 선불카드(§4.4). **없으면 `[]`**. (0.4.1) 선불카드 조회가 실패하면 **null**(「카드 없음」 `[]` 과 다르다) | DEC-012 D-08 ③ · D-36 |
| `prepaidCards[].title` · `.issuedDate` · `.expiresAt` | string · string \| null · string \| null | §4.4 | DEC-012 D-08 ③ |
| `prepaidCards[].balance` · `.point` | `{remaining, total}` · `{remaining, total}` | §4.4 · 현금 잔액 · 포인트 잔액(카드마다). (0.4.1) `remaining` · `total` = 금액 꼴 `{value, currency}` \| null | DEC-012 D-08 ③ · C1 §3-5 · 검수 r1 W3 |
| `partialErrors[]` | string[] | (0.4.1) 실패한 KOS 읽기 — 지금은 `prepaidCards` 하나뿐. 없으면 `[]` | DEC-012 D-36 · D-23(board · 상세와 같은 꼴) |

- 응답에 **넣지 않는** 칸: 전화 · 생년월일 · 국적 · 여권 · 차트번호 · 이메일 · KOS 고객 id · 발음 이름 · 성별(D-13 · D-31 · 코디 Q2). (0.4.0) 칸은 **더하기만** 했다 — 기존 칸의 이름 · 타입 · 뜻은 그대로다(DEC-012 D-03). 시술권 만료일 칸은 없다(DEC-012 D-07). (0.4.1) 더한 칸 = `tickets[].inUseCount` · `prepaidCards` · `partialErrors`

**오류**(§6.2 공통 + 아래):

| HTTP | code | 언제 | 문구(예) | 근거 |
|---|---|---|---|---|
| 404 | `customer_not_found` | §5 갈래 0명(이름 · 이메일이 틀림 · 고객 없음 · email 빈 고객 · 이름 검색 `count` > 1000 모두) · (0.4.0) `customerId` 가 사본에 없음 · KOS `get-visitor` 404 — 모두 같은 본문 | 「일치하는 고객이 없어요」 | D-14 · D-21 · D-22 · 코드 규약: `app/domain/errors.py:27-31`(404 · 코드를 따로 줄 수 있음 — 없는 경로의 `not_found` 와 갈라야 연동처가 「경로 틀림」과 「고객 없음」을 가른다) |
| 409 | `customer_ambiguous` | §5 갈래 2명 이상 | 「고객을 특정할 수 없어요」 | D-20 · 코드 규약: `app/domain/errors.py:34-35` |
| 502 | `kos_unavailable` | 이름 검색 · 시술권 조회 실패(§4.2 · §4.3) · (0.4.0) `customerId` 갈래 `get-visitor` 실패. (0.4.1) 선불카드 조회 실패는 502 가 **아니다**(`200` + `partialErrors` · DEC-012 D-36) | 「KOS 에 연결하지 못했어요」 | 코드 규약: `app/service/kos_errors.py:6` · `:36-39` |

- 문구 칸은 Swagger 설명에 싣는 예다. 연동처는 `code` 로 분기한다(코드 규약: `app/api/docs.py:23-27`)
- **(0.4.0) KOS 비용**(요청 1번당): 이름+이메일 갈래 = 내부 `get-visitors` 1 + 내부 `get-ticket-bundles` 1 + 공개 선불카드 1 = **3**(지금 2 → 3). `customerId` 갈래 = 내부 `get-visitor` 1 + 시술권 1 + 선불카드 1 = **3**. 404 · 409 이면 1(이름 검색만) · `customerId` 가 사본에 없으면 0(C1 §5 표 「2 → 3~4」 · C1 §3-2)

### 6.5 `POST /api/ext/reservations` — 예약 (D-11 ③ · D-32 · D-33)

**요청** `ExtReservationRequest`:

| 칸 | 타입 | 필수 | 뜻 | 근거 |
|---|---|---|---|---|
| `name` | string | ○ | 고객 이름(§5) | D-32 |
| `email` | string | ○ | 고객 이메일(§5) | D-32 |
| `start` | string | ○ | 시작 시각 ISO-8601(오프셋이 없으면 KST). 끝 = 시작 + 기본 그룹 간격 | D-32 · 코드 규약: `app/schemas/reservations.py:704-705` |
| `memo` | string | — | 예약 메모. 비면 보내지 않는다 | D-32 · 코드 규약: `app/schemas/reservations.py:713` |

그룹 · 구역 · 담당자 · 상담사 · 유입 칸은 **없다**. 보내면 모르는 키라서 `400 invalid_request` 이다(D-33).

**처리**:

1. **기본 그룹**: `KOS_EXT_RESERVATION_GROUP_ID` 가 비었거나, 그 kos_id 의 `reservation_group` 행이 없거나 `present = 0` 이거나, **그 그룹에 켜진 구역이 0 이면** → `503 ext_not_configured`. 모두 사본 기준이고 KOS 를 부르기 전에 막는다. 켜진 구역 0 은 지금 `create()` → `_pick_zone()` 이 `400 invalid_request`(「그 그룹에 켜진 구역이 없어요」)로 내는 경우다 — 연동처 요청과 상관없는 우리 설정 문제라 외부에는 503 으로 낸다(D-33 · 코디 Q3 · 코드 규약: `app/service/reservations.py:858-859`)
2. **고객 정하기**: §5 와 같은 함수로 정한다(D-32)
   - **2명 이상** → `409 customer_ambiguous`. 예약하지 않는다(D-20 · D-32)
   - **1명** → 그 고객(ccc `customerId`)으로 지금 `create()` 의 「기존 고객」 갈래를 탄다(D-32)
   - **0명** → 지금 `create()` 의 「새 고객」 갈래를 `{name, email}` 로 탄다. 이름 + 연락 수단 하나(이메일)라서 `identifiable()` 를 통과한다. KOS 고객에는 email 이 저장되고, 다음 조회부터는 찾힌다(D-22 · D-32 · 코드 규약: `app/domain/reservation_rules.py:249-255` · `app/service/reservations.py:913-917`)
   - **0명인데 KOS 중복 검사(`find-duplicated-visitor`)에 걸리면** — 지금 `create()` 는 `409 duplicated_visitor` + `candidate`(고객 이름 · 차트번호 · 생년월일)를 낸다. 외부 API 는 이를 **`409 customer_ambiguous` 로 바꾸고 `candidate` 를 싣지 않는다.** 예약하지 않는다. 무엇이 틀렸는지 밝히지 않는다(코디 Q1 · D-20 · D-21 · D-22 확장 · 코드 규약: `app/service/reservations.py:904-912`)
   - **드러남 수용(D-35)**: 이 갈래에서 중복 검사에 걸리면 409, 아니면 200(예약이 생김)이 나가므로 「그 이메일이 KOS 에 있는지」가 드러난다. 이 위험은 받아들인다(API 키를 가진 연동처만 부름 · 호출 제한 D-34 · 기록 D-24). 이 사실을 예약 엔드포인트 Swagger 설명에 적는다(§8)
3. **지금 예약 생성 로직을 다시 쓴다**(D-11 · D-33): `CreateReservationRequest` 를 서버 안에서 만들어(`groupId` = 기본 그룹 ccc id · `zoneId` 생략 · `customer` · `memo`) `ReservationService.create()` 를 부른다. 따라서 구역은 지금 기본 구역 규칙(SPEC-005 §5.5 — `KOS_ZONE_ID` 의 켜지고 자리 있는 구역 → order 순 첫 자리 있는 구역 → 첫 켜진 구역)을 따르고, 담당자는 KOS 시스템 계정이다. 칸 정원 검사(`slot_full`) · KOS 거절 처리도 지금과 같다(코드 규약: `app/service/reservations.py:773-854` · `:856-871` `_pick_zone` · `:873-881` `_assignee`)
4. 행위자 = `ext:<연동처>` 문자열을 `create()` 에 넘긴다(§3.5 행위자 문자열 겹). 지금 `create()` 가 남기는 `resv_create` · `kos_rejected` 줄과 날짜 캐시 비우기가 그대로 일어난다

**응답 200** `ExtReservationResponse`(지금 `CreateReservationResponse` 와 같은 모양):

| 칸 | 타입 | 뜻 | 근거 |
|---|---|---|---|
| `reservationId` | int | 만든 예약의 ccc id | 코드 규약: `app/schemas/reservations.py:718-722` · 코디 Q2 |
| `customerId` | int | 예약 고객 ccc id(0명 갈래면 새로 만든 고객) | 같음 |

**오류**(§6.2 공통 + 아래):

| HTTP | code | 언제 | 근거 |
|---|---|---|---|
| 409 | `customer_ambiguous` | §5 갈래 2명 이상 · 0명 갈래에서 KOS 중복 검사에 걸림 | D-20 · D-32 · 코디 Q1 |
| 409 | `slot_full` | 그 시간 칸의 정원이 찼다(사본 기준 · KOS 쓰기 직전) | D-33 · 코드 규약: `app/service/reservations.py:817-818` |
| 409 | `kos_rejected` | 중복 검사 · 고객 만들기 · 예약 쓰기 단계에서 KOS 가 4xx(401 제외)로 거절했다(같은 고객의 같은 시간 예약 · 정원 · 정책 등 — 문구는 지금 규칙) | 코드 규약: `app/service/kos_errors.py:9-39` |
| 502 | `kos_unavailable` | KOS 네트워크 · 5xx · 401 · 응답 형식(예약 쓰기 · 고객 만들기 · 중복 검사) · 이름 검색은 4xx 도 502(§4.2) · 예약 응답에 일정 id 없음. 예약 뒤 다시 읽기 실패는 502 가 아니다(사본 행을 직접 만들고 200) | 코드 규약: `app/service/kos_errors.py:36-39` · `app/service/reservations.py:738-747`(다시 읽기 실패 = None) · `:845-852` · 코드 검수 r1 W3 |
| 503 | `ext_not_configured` | 기본 그룹 env 가 비었거나 · 그 그룹이 KOS 에서 사라졌거나 · 그 그룹에 켜진 구역이 0 이다 | D-33 · 코디 Q3 · 코드 규약: `app/service/reservations.py:858-859` |

- 지금 `create()` 의 다른 오류 중 외부 요청으로는 일어날 수 없는 것: `groupId`(서버가 넣음) · `zoneId` · `assigneeStaffId` · `counselorStaffId` · `funnelId` · `desiredDischargeTime` 의 400, 「켜진 구역 없음」 400(1단계가 503 으로 먼저 막음), `404 없는 고객`, `409 not_identifiable`(이름 + 이메일이 늘 있다). 그래서 외부 오류 표에 싣지 않는다
- `duplicated_visitor` 는 외부 응답에 **절대 나가지 않는다**(코디 Q1 — `candidate` 누출 금지 · §9 시험)

### 6.6 `GET /api/ext/availability` — 예약 가능 시간대 (DEC-011 D-02 · D-07 ~ D-09 · D-11 · D-12)

> 0.3.0 더함. 이 절과 §6.7 · §6.8 의 「코드 규약」 줄은 main `e0e4a16` 기준이다.

**요청**: 질의 `date=YYYY-MM-DD`(필수). 이름 · 이메일이 없어서 GET 질의로 받는다(DEC-011 D-06 은 이름 · 이메일만 막는다). 본문은 없다.

**처리**(차례대로):

1. **날짜 검사** — 칸은 `date: str` 필수 질의로 받는다(pydantic `date` 타입으로 받지 않는다 — 숫자 문자열을 너그럽게 날짜로 읽을 수 있어 아래 꼴 검사와 어긋난다). `date` 가 **없으면** FastAPI 칸 검증으로 `400 invalid_request` 이고 message 는 지금 검증 규칙 그대로 **`query.date: …`** 다(본문 칸의 `body.name: …` 과 같은 규칙). 있으면 차례로 — **빈 문자열 → `400`**(먼저 막는다 · `parse_day` 의 「빈 값 = 오늘」 갈래를 타지 않는다) · **`YYYY-MM-DD` 숫자 꼴**(숫자 4 · `-` · 숫자 2 · `-` · 숫자 2)이 아니거나 `date.fromisoformat` 이 받지 않으면 `400` — ISO 주 날짜(`2026-W43-4`) 등 `fromisoformat` 이 받는 다른 ISO 꼴도 `400` 이다(코드 검수 add1 r1 N3) · **오늘(KST) 보다 앞이거나 오늘 + 90일보다 뒤이면 `400`**. 이 세 갈래의 message 는 **`date: <이유>`** 다(DEC-011 D-08 · 코드 규약: `app/main.py:120-124`(message = `loc` 를 `.` 로 이음) · `app/domain/reservation_rules.py:51-60` `parse_day` · 문서 검수 add1 W5)
2. **기본 그룹** — 예약(§6.5 1단계)과 같은 검사다. `KOS_EXT_RESERVATION_GROUP_ID` 가 비었거나 · 그 kos_id 의 `present` 그룹이 사본에 없거나 · 그 그룹에 켜진 구역(`ResvContext.enabled_zones`)이 0 이면 → `503 ext_not_configured`. KOS 를 부르기 전이다(DEC-011 D-09 · 코드 규약: `app/service/ext.py:235-242`)
3. **슬롯 새로 읽기** — KOS 공개 `schedule/open/v2/queries/get-reservation-slots-by-groups` 를 **1번** 부른다. 본문은 하루 조회와 같다 — `reservationGroupIds` = 사본의 `present` 예약 그룹 전부 · 기간 = 그 날짜 KST 하루(`day_range`). 성공하면 공유 슬롯 사본(`reservation_slot`)의 그날 행을 통째로 바꾼다(`replace_slots`). 그래서 이 응답 뒤 예약 생성(§6.5)이 같은 사본을 본다. 실패(네트워크 · 5xx · 4xx · 401 · `data` 가 배열 아님) · KOS 설정 없음이면 `502 kos_unavailable` 이고, 사본은 바꾸지 않는다. 지금 `ResvSync._slots()` 를 그대로 부르는 공개 함수 하나(`refresh_slots(day)`)를 `kos/reservation_sync.py` 에 더해 쓴다. 날짜 캐시(`ensure` · 10초)와 하루 예약 · 공지 · 금액 조회는 부르지 않는다(DEC-011 D-12 · 코드 규약: `app/kos/reservation_sync.py:283-284`(그룹 목록) · `:322-341` `_slots` · `app/repository/repo.py:547-554` `replace_slots`)
4. **후보 시각** — 기본 그룹 시간표의 그날 운영 구간(`open_spans` — 쉬는 시간을 뺀 조각들 · 그 요일이 꺼졌으면 없음) 안에서, 자정부터 그룹 간격(`interval_minutes`)으로 나눈 경계 `m`(`m % 간격 = 0` — `lines()` 와 같은 경계) 가운데 `구간 시작 ≤ m` 이고 `m + 간격 ≤ 구간 끝` 인 것. 오늘이면 **시작 시각이 지금보다 뒤인 것만** 남긴다(지금과 같거나 앞이면 뺀다)(DEC-011 D-02 · D-11 · 코드 규약: `app/domain/reservation_rules.py:103-117` `day_table` · `open_spans` · `:133-138` `lines`)
5. **남은 자리** — 후보 시각마다 기본 그룹의 켜진 구역 각각에 대해 사본 슬롯 (그룹 · 구역 · 그 시각) 행을 본다. 행이 있고 `capacity` 가 null 이 아니면 그 구역 몫 = `max(0, capacity − (reservation_count 또는 0))`. 행이 없거나 `capacity` 가 null 인 구역은 합에 넣지 않는다. **켜진 구역 모두 행이 없거나 `capacity` 가 null 이면 그 시각을 뺀다**(자리 수를 모름 — 목록에 없어도 예약은 될 수 있다). 몫을 더한 값이 `remainingSeats` 이고, **0 이면 그 시각을 뺀다**(DEC-011 D-02 · D-11)
6. 남은 것을 시각 오름차순으로 준다. 하나도 없으면(휴무 요일 · 다 참 · 다 지남) `200` 에 `slots: []` 다

**예약 생성과 같은 규칙인 까닭**(DEC-011 D-02): 예약 생성은 고른 구역의 슬롯 행 하나가 `count ≥ capacity` 일 때만 `409 slot_full` 이고, 구역은 `KOS_ZONE_ID` → order 순으로 **자리 있는 구역**을 고른다(행이 없는 구역도 자리 있음으로 본다). 5단계의 합이 1 이상이면 자리 있는 구역이 적어도 하나 있으므로, 같은 사본을 보는 바로 뒤 예약은 정원 때문에 거절되지 않는다. 틀릴 수 있는 것은 이 응답과 예약 사이에 다른 예약이 끼어드는 경합뿐이다(코드 규약: `app/service/reservations.py:818-819` · `:857-871` `_pick_zone` · `app/domain/reservation_rules.py:154-155` `is_full`). 운영 시간 · 휴무 · 지난 시각 검사는 예약 생성에 없다 — 이 목록이 그 시각을 내지 않을 뿐, 예약을 새로 막지 않는다(DEC-011 「걸리지 않는 것」 · SPEC-005 OQ-713).

**응답 200** `ExtAvailability`:

| 칸 | 타입 | 뜻 · null | 근거 |
|---|---|---|---|
| `date` | string | 요청 날짜 `YYYY-MM-DD`(KST) | DEC-011 D-02 |
| `intervalMinutes` | int | 기본 그룹 시간 간격(분). 칸 끝 = `start` + 이 값. 예약(§6.5)의 끝과 같다 | DEC-011 D-02 · 코드 규약: `app/service/reservations.py:827`(끝 = 시작 + 간격) |
| `slots[]` | array | 예약 가능한 칸. 시각 오름차순. 없으면 `[]` | DEC-011 D-02 |
| `slots[].start` | string | 칸 시작 ISO `+09:00`(초 단위). 이 값을 그대로 예약 `start` 로 보내면 된다 | DEC-011 D-02 · §6.1 「시각」 |
| `slots[].remainingSeats` | int | 남은 자리 수(1 이상) — 5단계 합. 0 인 칸은 나오지 않는다 | DEC-011 D-02 · D-11 |

- 응답에 **넣지 않는** 칸: 그룹 · 구역 id · 이름 · 구역별 정원 · 예약 수(DEC-011 D-02 — 그룹 하나 · 칸마다 시작과 남은 자리만)

**오류**(§6.2 공통 + 아래):

| HTTP | code | 언제 | 근거 |
|---|---|---|---|
| 400 | `invalid_request` | `date` 없음(message `query.date: …` — 지금 검증 규칙) · 빈 문자열 · `YYYY-MM-DD` 꼴 아님 · 오늘(KST) 앞 · 오늘 + 90일 뒤(message `date: <이유>`) | DEC-011 D-08 · 코드 규약: `app/main.py:117-121` · `app/domain/reservation_rules.py:51-60` |
| 502 | `kos_unavailable` | 3단계 슬롯 조회 실패 · KOS 설정 없음 | DEC-011 D-12 · 코드 규약: `app/service/kos_errors.py:36-39` |
| 503 | `ext_not_configured` | 2단계(기본 그룹 env 빔 · 그룹 없음 · 켜진 구역 0) — KOS 를 부르기 전 | DEC-011 D-09 · §6.5 |

- **부작용**: 공유 슬롯 사본의 그날 행을 바꾼다(직원 예약 현황의 정원 표시도 그 값을 본다 — 규칙은 같다). KOS 쓰기 · `event_log` 없음
- **KOS 비용**(요청 1번당): 공개 `get-reservation-slots-by-groups` **1번**. 400 · 503 이면 0번(DEC-011 D-12 · Consequences)

### 6.7 `POST /api/ext/customers/visits` — 고객 과거 시술 (DEC-011 D-03 · D-05 · D-06 · D-10 · D-14 · D-15)

**요청** `ExtCustomerRequest`: `{"name": "<이름>", "email": "a@example.com"}` — `name` · `email` 필수 · 빈 값 · 모르는 키 400 — 0.3.x 그대로. ~~조회(§6.4)의 `ExtLookupRequest` 와 같은 칸 · 같은 검증~~ (0.4.2 · 검수 r3 M4) lookup 새 모델과는 **따로다**(§6.4 「요청 모델을 따로 둔다」 · 상속 없음 · `customerId` 칸 없음). 경로 · 질의에 이름 · 이메일을 싣지 않는다(DEC-011 D-06).

**처리**:

1. **고객 정하기** — §5 와 같은 함수(`ExtService.find`)다. 0명 → `404 customer_not_found`(조회와 **바이트까지 같은** 본문) · 2명 이상 → `409 customer_ambiguous` · 이름 검색 실패 → `502`(DEC-011 D-05 · 코드 규약: `app/service/ext.py:163-190` · `:198-203`)
2. **일정 읽기** — 1명이면 KOS 공개 `schedule/open/v1/queries/get-schedules-by-visitor` 를 `{visitorId: <그 고객 KOS id>}` 로 **1번** 부른다(직원 상세 「이전 방문」과 같은 호출). **`data` 키가 없음(`{}`) · `data: []` = 일정 없음 → 빈 목록**(`200` · `visits: []` · `reservations: []`)이다. **`data` 가 있으면서 배열이 아님** · 호출 실패(네트워크 · 5xx · 4xx · 401) → `502 kos_unavailable`. **일정 원소의 모양이 깨져 처리할 수 없으면**(예: `reservation` · `reservationTime` 이 객체가 아님 · 작업 `title` 이 문자열이 아님) 그 고객 요청 전체를 **`502 kos_unavailable`** 로 낸다 — 원소를 건너뛰지 않고 `500` 으로 두지 않는다. 본문 · 로그에 KOS 원문은 0 이다(message 「KOS 에 연결하지 못했어요」 · 로그는 예외 종류만)(DEC-011 D-16 · 코드 검수 add1 r1 N1). 시술권(§4.3 「결과 없음」)과 같은 규칙이다 — `_data_list` 를 그대로 쓰지 않는다(그것은 키 없음도 실패로 본다). 고객 사본 · 예약 사본에 쓰지 않는다(코드 규약: `app/service/reservations.py:82` · `:593-594` · `:614-615`(직원 「이전 방문」 = `data` 없으면 빈 목록) · `app/service/ext.py:210-212`(`resp.get("data", [])` → 배열 아니면 502) · KDA 182행(`{}` 사례) · 문서 검수 add1 W1)
3. **고르기** — 일정 시작(`schedule_start` — 묶음 시작 중 가장 이른 값 · 없으면 `reservation.startDateTime`)이 **지금보다 앞인** 일정만 남긴다. 시작을 모르는 일정은 뺀다. **`deleted: true` 인 일정은 뺀다**(사본 쓰기 `apply_schedule` 과 같은 규칙 · DEC-011 D-15 · 코드 규약: `app/kos/reservation_sync.py:156`). 그 밖은 상태와 상관없이 남긴다(취소 · 부도도 결과 칸으로 보인다)(DEC-011 D-03 · 코드 규약: `app/domain/reservation_rules.py:336-340`)
4. **최신 순 · 50건** — 시작 내림차순으로 줄 세워 앞 50건만 준다(DEC-011 D-03 · D-10)

**응답 200** `ExtVisits`:

| 칸 | 타입 | 뜻 · null | 근거 |
|---|---|---|---|
| `visits[]` | array | 지금보다 앞선 일정, 최신 순, 최대 50. 없으면 `[]`(고객은 있는데 지난 일정 없음) | DEC-011 D-03 · D-10 |
| `visits[].date` | string | 시작의 KST 날짜 `YYYY-MM-DD` | DEC-011 D-03 · 코드 규약: `app/service/reservations.py:206` |
| `visits[].start` | string | 시작 ISO `+09:00` | DEC-011 D-03 |
| `visits[].result` | `completed` \| `noshow` \| `canceled` \| `other` | 직원 「이전 방문」 분류 그대로 — KOS `reservation.status` 가 `COMPLETED` · `NO_SHOW` · `CANCELED` 면 각각, 그 밖(값 없음 포함)은 `other` | DEC-011 D-03 · 코드 규약: `app/domain/reservation_rules.py:333` `PREV_RESULT` · `app/service/reservations.py:207` |
| `visits[].procedures` | string[] | 그 일정 작업의 `title`(KOS 배열 순서 · 빈 값이면 빈 문자열). 「방 배정」 기타 작업(`type = ETCETERA` 이고 제목이 「방 배정」)은 뺀다 — 직원 「이전 방문」과 같은 거르기. 작업이 없으면 `[]` | DEC-011 D-03 · 코드 규약: `app/service/reservations.py:212-215` |

- 응답에 **넣지 않는** 칸: 예약 메모 · 상담 메모 · 의사 이름 · 작업 상태 · 구역 · 그룹 · 결과 원래 값(`resultRaw`) · KOS 일정 id · 고객 칸(DEC-011 D-03 · DEC-010 D-13)
- **오늘 겹침**(DEC-011 D-14): 오늘 이미 시작 시각이 지난 일정은 여기에도, 예약 내역(§6.8)에도 나온다. Swagger 설명에 적는다

**오류**(§6.2 공통 + 아래): `400 invalid_request`(조회와 같은 칸 검증) · `404 customer_not_found` · `409 customer_ambiguous` · `502 kos_unavailable`(이름 검색 · 일정 읽기 실패 · 일정 원소 모양 오류 — 2단계 · DEC-011 D-16). 문구 · 조건은 §6.4 오류 표와 같다(DEC-011 D-05).

- **KOS 비용**(요청 1번당): 내부 `get-visitors` 1번 + 공개 `get-schedules-by-visitor` 1번 = **2번**. 404 · 409 이면 1번(일정 읽기 안 함)

### 6.8 `POST /api/ext/customers/reservations` — 고객 예약 내역 (DEC-011 D-04 · D-05 · D-06 · D-13 · D-14 · D-15)

**요청** `ExtCustomerRequest`(§6.7 과 같음 — `name` · `email` 필수 · lookup 새 모델과 따로 · 0.4.2).

**처리**:

1. **고객 정하기** — §6.7 1단계와 같다(DEC-011 D-05)
2. **일정 읽기** — §6.7 2단계와 같은 호출 1번 · 같은 규칙(`{}` · `[]` = 빈 목록 · `data` 가 배열 아님 · 원소 모양 오류 = 502)(DEC-011 D-13 · D-16)
3. **고르기** — 일정 시작(§6.7 3단계와 같은 값)이 **오늘(KST) 0시와 같거나 뒤인** 일정만 남긴다. 상태와 상관없이 남긴다(취소 · 부도 포함). 시작을 모르는 일정 · **`deleted: true` 인 일정은 뺀다**(§6.7 3단계와 같은 거르기 — DEC-011 D-04 · D-14 · D-15)
4. **차례** — 시작 오름차순. 개수 상한은 없다(DEC-011 D-04 — KOS 가 준 고객 일정 전부 중 오늘 이후)
5. **예약 id** — 일정 KOS id(`id`)로 ccc 예약 사본을 찾아(`reservation_id_of`) 있으면 그 ccc id, 없으면 null. 사본에 새로 쓰지 않는다. 외부 예약 API(§6.5)로 만든 예약은 예약 생성이 사본에 넣으므로 늘 id 가 있다(DEC-011 D-13 · 코드 규약: `app/repository/repo.py:538-540` · `app/service/reservations.py:847-851`)

**응답 200** `ExtCustomerReservations`:

| 칸 | 타입 | 뜻 · null | 근거 |
|---|---|---|---|
| `reservations[]` | array | 오늘(KST) 이후 일정, 시작 오름차순. 없으면 `[]` | DEC-011 D-04 |
| `reservations[].reservationId` | int \| null | ccc 예약 id(§6.5 응답 `reservationId` 와 같은 체계). ccc 사본에 그 일정이 없으면 null | DEC-011 D-13 · 코디 Q2(DEC-010 부록 B) |
| `reservations[].date` | string | 시작의 KST 날짜 `YYYY-MM-DD` | DEC-011 D-13 |
| `reservations[].start` | string | 시작 ISO `+09:00` | DEC-011 D-13 |
| `reservations[].end` | string \| null | 첫 묶음(`occupiedResources` 를 시작 순으로 놓은 첫 번째)의 끝 ISO `+09:00`. 묶음이 없으면 null | DEC-011 D-13 · 코드 규약: `app/kos/reservation_sync.py:80-99` `resources_of` |
| `reservations[].state` | `reserved` \| `reception` \| `consultation` \| `procedure` \| `home` \| `canceled` \| `noshow` | 직원 판 2계층 주 상태 그대로 — `reservation.status` 가 `CANCELED` · `NO_SHOW` 면 그것, 아니면 `flowStep` 으로 정한다(모르는 단계 = `reserved`) | DEC-011 D-04 · D-13 · 코드 규약: `app/domain/reservation_rules.py:13-22` `FLOW_STATE` · `:41-47` `state_of` |

- 응답에 **넣지 않는** 칸: 그룹 · 구역 이름 · 메모 · 담당자 · 상담사 · 부상태(`sub`) · KOS 일정 id · 고객 칸(DEC-011 D-13)
- **오늘 겹침**(DEC-011 D-14): 오늘 이미 시작 시각이 지난 일정도 여기 나온다(§6.7 에도 나온다)

**오류**: §6.7 과 같다.

- **KOS 비용**(요청 1번당): 내부 `get-visitors` 1번 + 공개 `get-schedules-by-visitor` 1번 = **2번**. 404 · 409 이면 1번

### 6.9 KOS 호출 비용 한눈에 (요청 1번당 · 성공 기준)

| 경로 | KOS 호출 | 근거 |
|---|---|---|
| `GET /api/ext/menu` | 0(DB 만) | §6.3 |
| `POST /api/ext/customers/lookup` | ~~내부 `get-visitors` 1 + 공개 `get-ticket-bundles` 1 = 2~~ (0.4.0) 이름 갈래 = 내부 `get-visitors` 1 + 내부 `get-ticket-bundles` 1 + 공개 선불카드 1 = **3** · `customerId` 갈래 = 내부 `get-visitor` 1 + 같은 둘 = **3**(선불카드가 실패해도 3 · `200`) | DEC-010 Consequences · §6.4 |
| `POST /api/ext/reservations` | 내부 `get-visitors` 1 + (0명이면 `find-duplicated-visitor` 1 + `create-visitor` 1) + `reserve` 1 + 다시 읽기 `get-schedule-detail` 1 = 3 ~ 5 | §6.5 · 코드 규약: `app/service/reservations.py:843-847`(`reserve` → `refresh_schedule` 1번) · `:905` · `:925`(0명 갈래 두 호출) |
| `GET /api/ext/availability` | 공개 `get-reservation-slots-by-groups` 1 | DEC-011 D-12 · §6.6 |
| `POST /api/ext/customers/visits` | 내부 `get-visitors` 1 + 공개 `get-schedules-by-visitor` 1 = 2 | §6.7 |
| `POST /api/ext/customers/reservations` | 내부 `get-visitors` 1 + 공개 `get-schedules-by-visitor` 1 = 2 | §6.8 |
| (0.4.0) `GET /api/ext/reservations/board` | 사본 신선 0 · 낡음 3 ~ 4(날짜 조회) + 내부 이력 **많아야 10**(0.4.2 — 굳지 않은 접수 뒤 일정 중 이번 요청에 사건(§6.11 4 ⓐ ~ ⓓ)이 있는 줄만 · D-17 대안이면 0) ~~(0.4.1 — 마지막 시도가 5분 지난 일정)~~ · (0.4.4) DB 읽기 = `event_log` 는 그날 예약 id 로 걸러 읽음(전체 아님 · §6.11 3) | §6.11 · DEC-012 D-38 · D-45 |
| (0.4.0) `GET /api/ext/reservations/{reservationId}` | 내부 일정 상세 1 + 내부 `get-visitor` 1 + 공개 문진 2 + 공개 고객 일정 1 = **5** | §6.12 |
| (0.4.0) `PUT /api/ext/customers/{customerId}/language` | 내부 `get-visitor` 1 + 내부 개인 정보 쓰기 1 = **2**(같은 값이면 1) | §6.13 |
| (0.4.0) `PUT /api/ext/reservations/{reservationId}/order-memo` | 내부 `change-order-memo` **1** | §6.14 |
| (0.4.0) `PUT /api/ext/reservations/{reservationId}/consultation-memo` | 공개 `update-schedule-consultation-info` **1** | §6.15 |
| (0.4.0) `GET /api/ext/clinic` | 내부 `get-hospital` 1 + 운영 시간 1 + 휴무 1 = **3** | §6.16 |
| (0.4.0) `GET /api/ext/clinics/{clinicId}/staff` | 내부 `account/v2 get-accounts` **1** | §6.17 |

키당 호출 제한(60초 60번)은 **외부 경로 전부**가 함께 쓴다(DEC-011 D-01 · DEC-012 D-01 · DEC-010 D-34). 그래서 board 를 뺀 경로로 한 키가 KOS 에 거는 부담은 60초에 많아야 300번 남짓(예약 60번 × 5 · 예약 상세 60번 × 5)이다. ~~board 의 이력 조회는 일정마다 한 번만이라 이 상한을 바꾸지 않는다.~~ **board 의 이력 조회는 따로 묶인다**(0.4.2 고침 · DEC-012 D-38 · DQ7): 요청 1번당 많아야 10번이고, 일정마다 **사건이 있을 때만**(처음 봄 · 대기를 새로 봄 · 귀가 뒤 · 실패 재시도 ≤ 3 — §6.11 4) 부른다. 겹친 요청은 시도 예약으로 같은 사건을 한 번만 부른다. 그래서 이력 호출은 **board 요청 수에 비례하지 않고**, 하루 합은 **「접수 뒤 일정 수 × 3 + 실패 재시도(일정마다 ≤ 3)」** 를 넘지 않는다(대기 구간이 하나인 보통의 경우 · 재진입 구간마다 그 일정에 1을 더한다 · 찾은 일정은 그 뒤 0). 키 · 연동처가 몇이든 같은 상한이다. ~~(0.4.1) 5분 동안의 이력 호출 합 ≤ 못 찾은 수~~

### 6.10 (0.4.0) 열람 헤더 · 열람 기록 (DEC-012 D-18 · D-19)

| 항목 | 계약 | 근거 |
|---|---|---|
| 헤더 | **`X-Ext-Staff-Id`**(선택) — 연동처 직원 id(centurion 통합 계정) | DEC-012 D-18 · D-37 |
| 읽는 경로 | (0.4.1 고침 · 검수 r1 F2) **헤더를 쓰는 다섯 경로만** 읽는다 — lookup(§6.4) · 예약 상세(§6.12) · 고객 언어 · 오더 메모 · 상담 메모(§6.13 ~ §6.15). 메뉴 · 예약 · 가능 시간대 · 과거 시술 · 예약 내역은 헤더를 **보지 않는다**(의존성을 달지 않는다 · 어떤 값이 와도 지금과 같은 응답). 기존 계약에 새 400 을 만들지 않기 위해서다 | DEC-012 D-37 ① · D-02 |
| 값 · 꼴 | 앞뒤 공백을 지운다. 비면 헤더가 없는 것으로 본다. 꼴 = 1 ~ 64자이고 영문 · 숫자 · `.` · `_` · `-` 로만 이뤄진다(0.4.1 — `@` 뺌 · 이메일 꼴 id 가 `event_log` 에 남지 않게) | DEC-012 D-37 ④ · 검수 r1 참고 R2 |
| 꼴이 틀리면 | **lookup**(기존 경로) = **없는 것으로 본다**(직원 id null · 행위자 `ext:<연동처>` · 400 없음 · 기존 계약 그대로). **새 경로 넷**(상세 · 쓰기 셋) = `400 invalid_request`(message `header.X-Ext-Staff-Id: …` · 코드 규약: `app/main.py:120-124` — message = `<위치>: <이유>`). 그래서 공통 의존성은 둘이다: 너그러운 것(lookup) · 엄격한 것(새 넷) — 꼴 검사 함수는 하나를 같이 쓴다 | DEC-012 D-37 ② ③ |
| 검증 | **하지 않는다.** 연동처가 신고한 값이다. CC 계정 · 직원 사본(`staff`)과 잇지 않는다. 그 값을 그대로 적는다 | DEC-012 D-18 |
| 쓰는 곳 | ① 열람 — lookup(§6.4) · 예약 상세(§6.12)가 **200** 이면 `event_log` `ext_view` 1줄(§3.5 표). ② 행위자 — 고객 언어 · 오더 메모 · 상담 메모(§6.13 ~ §6.15)의 `actor` = `ext:<연동처>:<직원 id>` · 헤더 없으면 `ext:<연동처>`. `ext_view` 줄의 `actor` 도 같은 값이다(DEC-012 D-37 ⑤). ~~다른 외부 경로는 헤더를 받아도 쓰지 않는다(꼴 검사만 한다)~~ | DEC-012 D-18 · D-19 · D-37 |
| 남기지 않는 곳 | `ext_call` · 앱 로그 · 응답 본문 | DEC-012 D-18 · DEC-010 D-24 |
| Swagger | 헤더 칸은 **다섯 경로의 operation 에만** 실린다. 설명에 「연동처가 신고한 값 — CC 가 검증하지 않는다 · 열람 기록 · 쓰기 행위자에 그대로 적는다 · 꼴 = 영문 · 숫자 · `.` `_` `-` 1 ~ 64자」를 적고, lookup 에는 「꼴이 틀리면 없는 것으로 본다」, 새 넷에는 「꼴이 틀리면 400」을 더한다 | DEC-012 D-18 · D-37 |

### 6.11 (0.4.0) `GET /api/ext/reservations/board` — 오늘 접수 목록 (DEC-012 D-09 · D-16 · D-17 · D-23 · D-30 · D-38)

**요청**: 질의 칸 없음. 오늘(KST)만 준다(DEC-012 D-09 「오늘 예약」). 경로 등록 차례: 이 경로를 `GET /api/ext/reservations/{reservationId}`(§6.12)보다 **먼저** 둔다. 그래야 `board` 가 정수 경로 칸 검증(400)에 먼저 걸리지 않는다.

**처리**:

1. **사본 신선도** — 직원 board 와 같이 `ensure_day(오늘)` 를 부른다. 같은 10초 날짜 캐시다. 낡았으면 날짜 조회(내부 하루 예약 · 공개 칸 정원 · 내부 공지 · (오늘) 공개 수납)를 하고, 실패하면 낡은 사본 그대로 + `sync.lastError` 로 낸다. runtime(KOS 설정)이 없으면 `sync.lastError` = 「KOS 설정이 비어 있어요」이고 사본으로 낸다. 어느 경우든 `200` 이다(DEC-012 D-23 · 코드 규약: `app/service/reservations.py:285-297` · `app/kos/reservation_sync.py:267-276`)
2. **줄** — 사본 `tx.reservations(오늘)` 의 예약 **한 건 = 한 줄**이다. 직원 카드는 묶음(resource)마다 한 장이지만, 여기서는 예약 단위로 묶는다(C1 §1-1 함정). 집합은 직원 카드와 같다 — 그날 사본에 있는 예약 전부이고, 상태로 거르지 않는다(취소 · 부도 · 귀가 포함 · DEC-012 D-30)
3. **상담 여부** — 직원 상세 「상담」 칸이 생기는 조건과 **같은 함수**다: ① 지금 단계가 `CONSULTATION_WAITING` · `CONSULTATION`, ② CC 접수 이벤트(`reception`)의 `payload.endStep = CONSULTATION_WAITING`, ③ `consultation_add` 이벤트. 셋 중 하나면 `true` 다. KOS `consultationRequired` 는 읽지 않는다. (0.4.4 · 코드 검수 r1 W5 · DEC-012 D-45) 판정에 쓰는 `event_log`(`reception` · `consultation_add`)는 **그날 예약 id 로 걸러 읽는다**(`reservation_id IN (그날 사본 예약 id)` · 전체 읽기 아님 — board 는 키당 60초 60번까지 불리고 이 두 type 은 접수마다 쌓여 줄지 않는다). (0.4.1 · 검수 r1 W6) **직원 상세와 같은 `after` 문을 먼저 거친다** — `after = state.main not in ("reserved", "canceled", "noshow")` 일 때만 판정하고, 아니면 `false` 다(직원 상세는 그때 `flow` 가 없어 「상담」 칸이 없다 · 코드 규약: `app/service/reservations.py:530-531`). 그래서 상담 대기를 거친 뒤 취소된 예약도 `false` 다. 지금 `_flow()` 안에 있는 이 판정을 `domain/reservation_rules.py` 의 함수 하나로 옮기고, `_flow()` 와 이 경로가 둘 다 그 함수를 부른다(직원 응답 무변경 · T30). 두 벌을 두지 않는다(DEC-012 D-09 · C1 §3-1 · 코드 규약: `app/service/reservations.py:653-656`)
4. **처음 상담 대기 시각**(DEC-012 D-16 · D-38) — (0.4.1 고침 · 검수 r1 F1 · F3 · W1)
   - **대상** = `after` 인 줄(3단계와 같은 문 — 접수 뒤 단계로 간 일정 전부) 중 §3.6 에 `first_at` 이 있는 행이 **없는** 줄. **CC 상담 판정(3단계 결과)으로 가르지 않는다** — KOS 웹에서만 상담 대기를 지나간 일정도 시각을 얻는다(DEC-012 D-16 ③). 그래서 `consultation = false` 인데 시각이 있는 줄이 생길 수 있다(두 칸은 따로 정한다). 하루 대상 상한 = 그날 접수 건수
   - **언제 부르나 — 사건이 있을 때만**(0.4.2 고침 · DEC-012 D-38 · DQ7 · 검수 r2 N3). 굳지 않은 대상 줄은 아래 넷 중 하나가 이번 요청에서 참일 때만 부른다. **「못 찾음」만으로는 다시 부르지 않는다.** ~~못 찾음 · 실패는 5분 간격으로 다시 부른다~~
     - ⓐ **처음 봄** — §3.6 에 그 일정 행이 없다(접수 뒤 단계로 간 것을 처음 봄). 1번. 그때 사본 단계가 `CONSULTATION_WAITING` 이면 이 1번이 ⓑ 몫도 겸한다(`wait_called = 1`). (0.4.4 · 코드 검수 r1 Q1 · DEC-012 D-45) 그때 사본 상태가 이미 귀가(`state.main = home`)면 이 1번이 **ⓒ 몫도 겸한다**(`final_tried = 1` — 시도 예약에 같이 적는다). 그래서 하루 끝에 처음 본 귀가 일정은 1번만 불린다
     - ⓑ **대기를 새로 봄** — 행이 있고 `last_failed = 0`(못 찾음)인데, 사본 단계가 지금 `CONSULTATION_WAITING` 이고 `wait_called = 0`. 같은 대기 구간에서는 1번만(`wait_called = 1`). 사본에서 대기가 아닌 단계를 보면 `wait_called = 0` 으로 되돌린다 — 다시 대기에 들어가면(재진입) 새 사건이다. 이력 반영이 늦은 경우도 이 사건이 받는다. board 가 열리지 않은 사이에 지나간 대기 구간은 보지 못한다(ⓒ 가 받는다)
     - ⓒ **끝난 단계 뒤**(DEC-012 D-40 그대로) — 사본 상태가 더 바뀌지 않는 끝난 단계(`state.main = home` · 귀가 — 취소 · 부도는 애초 대상 밖이라 지금 해당하는 것은 귀가뿐)이고 `final_tried = 0`. 1번 부르고 `final_tried = 1`. 그 뒤 그날 사건으로는 더 부르지 않는다. KOS 웹에서만 지나간 대기 · 이력 지연을 이 1번이 받는다
     - ⓓ **실패 재시도** — `last_failed = 1` 이고 `checked_at` 이 5분 지났고 `retries < 3`. 부를 때 `retries + 1`. 3번이면 그날 더 재시도하지 않는다(null · `last_failed = 1` 이 남아 `partialErrors` 에 보인다 · D-39). 값 근거: 5분 × 3 = 15분 — KOS 일시 장애 · 배포 한 번을 넘길 만큼이고, 장애가 길어져도 일정 하나가 하루에 더하는 호출을 3으로 묶는다. ⓒ 의 1번이 실패한 경우도 이 재시도가 받는다(실패는 사건과 상관없이 ⓓ 규칙 하나 · DEC-012 D-41)
   - **요청당 상한 = 10**(DEC-012 D-38). 부를 줄이 10을 넘으면 「ⓐ → ⓑ → ⓒ → ⓓ(`checked_at` 이 오래된 줄 먼저) → 줄 차례(5단계)」로 10개를 고르고, 나머지는 이번 응답에서 null 이다. 사건 조건은 다음 요청에도 그대로 참이므로(사본 단계가 그새 바뀌지 않으면) 다음 요청에서 차례가 온다. 10개는 **동시에 한 바퀴**로 부른다(동시 상한 = 10). 값 근거: board 응답이 이력 때문에 KOS 왕복 한 번보다 길어지지 않게 한다. 구현 상수 한 곳에 둔다
   - **시도 예약**(0.4.2 · 검수 r2 N2) — 부를 줄을 고르는 순간, **한 트랜잭션 안에서** 그 줄의 §3.6 행에 먼저 적는다: `checked_at = now` · `last_failed = 1`(결과가 오기 전) · 그 사건의 표시(ⓐ 행 만듦 · ⓑ `wait_called = 1` · ⓒ `final_tried = 1` · ⓓ `retries + 1`). 그 뒤에 KOS 를 부른다. **방법**(0.4.2 · 검수 r3 M5): 고르기(읽기)와 적기를 **`BEGIN IMMEDIATE` 한 트랜잭션**으로 한다 — 시작할 때 쓰기 잠금을 잡으므로 두 트랜잭션이 함께 읽은 뒤 둘 다 적는 일이 없다. 이 트랜잭션은 요청 트랜잭션(`connect()` · 「요청 하나 = 트랜잭션 하나」)과 **따로 짧게** 열고 KOS 를 부르기 **전에** 커밋한다. 안에 `await` · KOS 호출을 두지 않는다. 결과 적기는 KOS 응답 뒤 또 다른 짧은 트랜잭션이다. 잠금을 기다리는 쪽은 연결 `timeout=10` 안에서 기다린다(코드 규약: `app/repository/db.py:340-343` `sqlite3.connect(..., timeout=10)` · `:377` `BEGIN` 선례). 그래서 겹친 board 요청(다른 연동처 · 같은 연동처의 다른 화면 · 같은 DB 를 쓰는 다른 프로세스)은 이미 적힌 행을 보고 같은 사건으로 그 일정을 다시 고르지 않는다 — 고르기 조건은 DB 행으로만 판단한다(프로세스 안 잠금을 두지 않는다). ~~같은 DB 를 쓰는 워커 여럿에도 맞는다(방법 없이)~~ 겹친 요청의 응답에는 그 줄이 null 이고 `last_failed = 1` 이라 `partialErrors` 에 보인다. 부르는 도중 프로세스가 죽으면 `last_failed = 1` 이 남아 ⓓ 가 받는다
   - **부르기** — 내부 `schedule/v1/queries/get-schedule-event-logs {scheduleId: <사본 kos_id>}`. 응답 `data[]` 원소(6키 `{scheduleId, version, eventType, payload, raisedDateTimeUtc, initiator}`) 중 **`eventType` 의 마지막 `.` 뒤 조각이 `FlowStepChanged`** 이고(실물은 전체 이름 `protos.schedule.event.FlowStepChanged` — 짧은 이름과 같은 문자열은 오지 않는다 · 끝 조각으로 견줘 패키지 이름 변경에 덜 깨지게 한다) `payload`(JSON 문자열 · 키 `{flowStep, raisedDateTimeUtc}`)의 `flowStep` 이 **문자열** `CONSULTATION_WAITING` 인 것의, **원소** `raisedDateTimeUtc`(payload 안 값이 아님) 최솟값이다. 원소 차례는 시각 순이 아닐 수 있고(데모 12/40) 같은 단계를 두 번 거치면 원소가 둘이라, 첫 원소가 아니라 최솟값을 고른다. 소수 자릿수가 2 ~ 3 으로 바뀌어 오므로 파싱이 둘 다 받아야 한다(계약 아님 · BE3 시험). ~~(숫자 enum 대응은 WORK-014 KOS0 확인 값)~~ — (0.4.3 · KOS0 ① · DEC-012 D-42 · `flowStep` 은 숫자가 아니라 사본 `reservation.flow_step` 과 같은 문자열 enum 이름이다)
   - **결과 적기** — ① 찾음 → `first_at` · `source = kos_event_log` · `last_failed = 0`. 이 행은 굳는다(다시 부르지 않는다). ② 응답은 성공했는데 그 이벤트가 없음(못 찾음) → `last_failed = 0`. **굳히지 않는다** — 다음 사건(ⓑ · ⓒ)을 기다린다. ③ 실패(네트워크 · 5xx · 4xx · 401 · UA 403 · `data` 가 배열 아님 · 원소 · `payload` 모양 깨짐) → `last_failed = 1` 그대로. 굳히지 않는다 — ⓓ 가 받는다. board 는 `200` 그대로다(DEC-012 D-23)
   - **재진입 · 이력 지연** — 못 찾음으로 남은 일정이 그 뒤 상담 대기에 들어가면 ⓑ 로, 대기를 아무도 보지 못하고 귀가하면 ⓒ 로 다시 불려 값을 얻는다. `flowStep` 대응 오류를 고친 뒤에는 그 뒤의 사건부터 바로잡힌다(이미 ⓒ 까지 지난 일정은 null 로 남는다)
   - **날짜가 지나면** — board 는 오늘(KST) 일정만 다루므로, 지난 날 일정은 다시 불리지 않는다. 그날 끝까지 못 찾은 일정은 null 로 남는다(DEC-012 D-38 ⑤)
   - **`partialErrors`** — 이 응답의 대상 줄 중 시각이 null 이고 ⓐ 마지막 시도가 실패(`last_failed = 1` · 이번 요청 실패 포함)이거나 ⓑ **이번 요청에서 사건(ⓐ ~ ⓓ)이 있었는데 요청당 상한 때문에 부르지 못한 줄**이 하나라도 있으면 `consultationHistory` 를 넣는다(「아직 확인하지 못한 시각이 있다」 · DEC-012 D-39 · 0.4.2 넓힘 — 상한으로 미뤄진 「대기를 새로 봄」 줄도 든다 · 검수 r3 참고 P2). ~~ⓑ 요청당 상한 때문에 한 번도 부르지 못한 줄~~ 못 찾음(`last_failed = 0`)만 남은 null 은 넣지 않는다
   - ~~**D-17 대안으로 갈 때**(KOS0 결과가 예상과 다름)~~ (0.4.3 · KOS0 판정 = D-16 그대로 — **쓰지 않음** · DEC-012 D-42. 아래는 기록으로 둔다): 이 단계는 KOS 를 부르지 않는다. 대신 날짜 조회(`reservation_sync.fetch_day`)가 사본을 쓸 때 `flow_step = CONSULTATION_WAITING` 인 일정을 처음 보면 §3.6 행을 쓴다(`source = cc_poll` · 그 시각 = 그 조회의 `now` · `source` 가 다른 행은 덮는다 · §3.6). **이 날짜 조회는 요청이 올 때만 돈다**(직원 · 외부 화면이 그날을 열고 10초 캐시가 낡았을 때 · `kos/runtime.py` 루프에는 예약 날짜 조회가 없다). 그래서 상담 대기 동안 아무도 화면을 열지 않으면 그 일정은 보이지 않고 늦음에 상한이 없다(DEC-012 D-17 · 검수 r1 W2 · 코드 규약: `app/kos/reservation_sync.py:267-276`). 응답 칸 모양은 같다
5. **차례** — 첫 묶음 시작 오름차순 → `reservationId`

**응답 200** `ExtBoard`:

| 칸 | 타입 | 뜻 · null | 근거 |
|---|---|---|---|
| `date` | string | 오늘 KST `YYYY-MM-DD` | DEC-012 D-09 |
| `now` | string | 서버 지금 시각 ISO `+09:00` | 코드 규약: `app/service/reservations.py:359`(직원 board `now`) |
| `sync.lastOkAt` · `sync.lastError` | string \| null · string \| null | 그날 날짜 조회가 마지막으로 성공한 시각 · 마지막 실패 문구(직원 board `sync` 와 같은 값). `lastError` 가 있으면 이 목록은 낡은 사본일 수 있다 | DEC-012 D-23 · 코드 규약: `:360` |
| `partialErrors[]` | string[] | 일부 KOS 읽기가 실패했거나 아직 못 한 칸 이름. 지금은 `consultationHistory`(4단계 「`partialErrors`」 · DEC-012 D-39)만 있다. 없으면 `[]` | DEC-012 D-23 · D-38 |
| `reservations[]` | array | 오늘 예약, 시작 오름차순 | DEC-012 D-09 |
| `.reservationId` | int | ccc 예약 id(§6.12 · §6.14 · §6.15 의 경로 id) | 코디 Q2(부록 B) |
| `.start` · `.end` | string \| null | 첫 묶음 시작 · 묶음 끝 중 가장 늦은 값(ISO `+09:00`). 묶음이 없으면 null | 코드 규약: `app/service/reservations.py:546-547` |
| `.state.main` · `.state.sub` | string · string \| null | 직원 판 2계층 상태 그대로(`state_of`) | 코드 규약: `app/domain/reservation_rules.py:41-47` |
| `.customer` | object | `{customerId(int \| null), name, phoneticName, gender, nationality, isNew}` — 직원 board 카드 고객 칸과 같다 | 코드 규약: `app/service/reservations.py:316-318` |
| `.receptionAt` | string \| null | 접수 시각 = 사본 `reception_at`(KOS `receptionDateTimeUtc`). **귀가한 예약도 준다.** 접수 전이면 null. 접수 뒤인데 KOS 가 비워 준 일정도 null 이다(데모 4/162) | DEC-012 D-09 · C1 §2-4 |
| `.counselor` | `{staffId, name}` \| null | 담당 상담사 = 사본 `reservation.counselor` = KOS `reservation.counselor` — **KOS 스펙 이름은 「희망 상담사」**다(실제 상담한 사람이 아니다). 직원 예약 상세 `reservation.counselor` 와 같은 값이고, `staffId` = ccc 직원 사본 id(없으면 null) | DEC-012 D-09 · C1 §2-1 · 코드 규약: `app/service/reservations.py:681-686` `_staff_ref` |
| `.roomTitle` | string \| null | 관리실 = 사본 `room_title` = 작업에 붙은 방 중 **가장 늦게 배정된 것**. 방이 없으면 null | DEC-012 D-09 · C1 §2-2 |
| `.consultation` | bool | 상담 거침 — 3단계 CC 판정(`after` 가 아니면 `false`) | DEC-012 D-09 · C1 §3-1 · 코드 규약: `app/service/reservations.py:530-531` |
| `.firstConsultationWaitingAt` | string \| null | 처음 상담 대기가 된 시각 ISO `+09:00` — KOS 단계 변경 이력에서 찾은 값(`consultation` 과 따로 정한다 · `consultation = false` 여도 값이 있을 수 있다). null = 접수 전 · 취소 · 부도 · 아직 못 찾음(이력에 없음 · 실패 · 다음 사건 전 · 요청당 상한 · 겹친 요청이 부르는 중 · 그날 끝까지 못 찾음 · 귀가 뒤 마지막 1번에도 못 찾음) · (대안이면) CC 가 보지 못함 | DEC-012 D-16 · D-17 · D-38 · D-40 |

- 응답에 **넣지 않는** 칸: 직원 board 의 열 · 칸 정원 · 공지 · 원내 현황 금액 · 드래그 · 수납 필요 수 · 담당자(`assignee`)
- **오류**: 공통 표(§6.2)뿐이다. KOS 실패는 `sync.lastError` · `partialErrors` 로 보이고 `502` 를 내지 않는다(DEC-012 D-23)
- **KOS 비용**(요청 1번당): 사본이 신선하면 **0**, 낡았으면 날짜 조회 **3 ~ 4**. 여기에 4단계 이력 조회가 **많아야 10** 붙는다(0.4.1). ~~하루 합은 「그날 상담을 거친 일정 수」를 넘지 않는다(실패 · 지연 재시도 제외)~~ ~~(0.4.1) 5분마다 「못 찾은 수」를 넘지 않는다~~ (0.4.2 고침 · DEC-012 D-38 · DQ7) 이력 호출은 일정마다 사건이 있을 때만 붙으므로 **board 를 몇 번 부르든 늘지 않는다.** 일정 하나의 하루 호출 = 처음 봄 1 + 새로 본 대기 구간마다 1(처음 봄이 대기면 겸함) + 귀가 뒤 1 + 실패 재시도 ≤ 3. 그래서 하루 합 ≤ 접수 뒤 일정 수 × 3 + 실패 재시도(대기 구간이 하나인 보통의 경우 · §6.9). 찾은 일정은 그 뒤 0 이다. 대안(D-17)이면 4단계는 0 이다(C1 §1-1 · C3 §0)

### 6.12 (0.4.0) `GET /api/ext/reservations/{reservationId}` — 예약 상세 (DEC-012 D-02 · D-10 · D-18 · D-23 · D-34 · D-37)

**요청**: 경로 `reservationId`(ccc 정수). 선택 헤더 `X-Ext-Staff-Id`(§6.10 · 새 경로라 꼴이 틀리면 400 · DEC-012 D-37 ③).

**처리**:

1. **예약 찾기** — 사본에 그 id 가 없으면 `404 reservation_not_found`(「없는 예약이에요」 · KOS 호출 0). 없는 경로의 `not_found` 와 가르려고 code 를 따로 둔다(DEC-010 §6.4 `customer_not_found` 와 같은 이유 · 코드 규약: `app/service/reservations.py:472-476` · `app/domain/errors.py` `NotFound(message, code)`)
2. **KOS 설정** — runtime 이 없으면 `502 kos_unavailable`(가능 시간대 §6.6 3단계와 같은 규칙)
3. **일정 다시 읽기** — 직원 상세와 같은 `refresh_schedule(kos_id, day, gone=True, sink=raw)`(내부 `get-schedule-detail` 1번 · 캐시 없음). KOS 가 404 면 `404 reservation_gone`(직원 code 그대로). 그 밖 실패면 사본 값으로 내고, 희망 시술 · 희망 의사 · (0.4.1) 지금 오더 메모 · 상담 메모를 null 로 두며 `partialErrors` 에 `schedule` 을 넣는다. 성공하면 사본을 덮어쓴다(직원 상세와 같은 부작용)(코드 규약: `app/service/reservations.py:495-498` · `:730-760`)
4. **고객 읽기** — 직원 `_detail_reads` 와 같은 동시 4번: 내부 `get-visitor` · 공개 문진 양식 · 공개 문진 제출본 · 공개 `get-schedules-by-visitor`. **수납 금액 조회는 부르지 않는다**(정산 칸을 내지 않는다). 방법(0.4.1 · 검수 r1 W7): `_detail_reads(r, cust, main, *, amount: bool = True)` 로 키워드 인자를 더하고 외부는 `amount=False` 로 부른다. 직원 쪽 부르는 곳은 고치지 않는다(기본값 `True` = 지금 동작 · `main` 에 가짜 값을 넘기지 않는다 · 코드 규약: `app/service/reservations.py:595-597` `want_amount`). 하나가 실패해도 나머지를 쓴다. `_detail_reads` 는 지금 이전 방문 조회가 실패하면 조용히 빈 목록을 준다 — 실패를 따로 알리는 값을 하나 더한다(직원 응답 무변경). 고객 사본이 없는 예약이면 네 호출을 하지 않고 셋 다 `partialErrors` 다(코드 규약: `app/service/reservations.py:581-619`)
5. 직원 상세의 `ensure_today` · `ensure_day` 는 부르지 않는다. 방 사용 중 · 상담사 상태 칸을 내지 않기 때문이다(직원 상세와 다른 점)
6. **열람 기록** — 200 이면 `event_log` `ext_view` 1줄(§3.5 · §6.10 · `actor` = `ext:<연동처>[:<직원 id>]`)

**응답 200** `ExtReservationDetail`:

| 칸 | 타입 | 뜻 · null | 근거 |
|---|---|---|---|
| `reservationId` · `day` · `start` · `end` | int · string · string \| null · string \| null | 직원 상세와 같다 | 코드 규약: `app/service/reservations.py:545-547` |
| `state.main` · `state.sub` | string · string \| null | 직원 판 2계층 상태 | 같음 `:550` |
| `customer.customerId` · `.name` · `.phoneticName` · `.gender` · `.nationality` · `.isNew` · `.chartNumber` | — | 기본 정보 = 고객 사본(직원 상세 `customer.*` 와 같은 값). (0.4.4 · 코드 검수 r1 Q3 · DEC-012 D-45) `customerId` 는 `int \| null` — 고객 사본이 없는 예약이면 **null** 이다(직원 상세는 `0` 을 주지만 외부에는 없는 id 를 내지 않는다 · board `customer.customerId` 와 같은 꼴) | DEC-012 D-10 · C1 §1-2 「기본 정보」 · `:552-555` |
| `customer.age` | int \| null | 그 예약 날짜 기준 나이(`age_on` · 내부 `get-visitor` 의 `dateOfBirth`) | C1 §1-2 · `:556` |
| `customer.language` | string \| null | 고객 언어 = 내부 `get-visitor` 의 `language`(KOS 값 그대로 · 공개 `getVisitor` 에는 없다) | DEC-012 D-10 · C1 §1-2 · `:165` |
| `customer.funnel` | `{name, detail}` \| null | 고객 유입 = 내부 `get-visitor` 의 `visitorFunnel`(직원 `visitor_funnel_of` 의 `name` · `detail` · ccc 유입 id 는 내지 않는다) | C1 §1-2 · `:174-181` |
| `reservation.memo` | string \| null | 예약 메모(사본 = KOS `reservationMemo`) | DEC-012 D-10 · C1 §1-2 |
| `reservation.desiredDischargeAt` | string \| null | 귀가 희망 시각 | 같음 |
| `reservation.funnel` | `{name, detail}` \| null | 예약 유입(`funnel_of`) | 같음 · `:184-189` |
| `reservation.counselor` | `{staffId, name}` \| null | 희망 상담사(§6.11 `.counselor` 와 같은 값) | DEC-012 D-09 · C1 §2-1 |
| `reservation.orderMemo` | string \| null | (0.4.1) **지금 오더 메모** = 3단계 원본 `data.orderMemo` 그대로(빈 문자열 그대로 · §6.14 가 통째로 바꾸는 그 칸). null = 3단계 실패 · 키 없음. 호출 0 추가 | DEC-012 D-34 · `상담대기.har` · `상담대기3.har` 일정 상세 키 |
| `reservation.consultationMemo` | string \| null | (0.4.1) **지금 상담 메모** = 3단계 원본 `data.consultation.consultationMemo` 그대로(§6.15 가 통째로 바꾸는 그 칸). null = 3단계 실패 · `consultation` 없음 | DEC-012 D-34 · 같은 HAR 키 |
| `reservation.requestedDoctor` | `{staffId, name}` \| null | 희망 의사 = KOS `reservation.doctor`(3단계 원본 · `_staff_ref`). 데모는 162/162 빈 값이었다 | DEC-012 D-10 · C1 §3-6 · `상담대기.har` 일정 상세 `reservation` 키 |
| `reservation.requestedProcedures` | array \| null | 희망 시술 = KOS `reservation.requestedProcedures[]`(3단계 원본 · 사본에는 없다). 원소 = `{type: OPTION \| TICKET, optionId, optionTitle, productTitle, ticketId, ticketTitle}` — `OPTION` 이면 `optionConfiguration` 칸 · `TICKET` 이면 `ticketConfiguration` 칸을 채우고 나머지는 null. 빈 배열 = 희망 시술 없음 · null = 3단계 실패 | DEC-012 D-10 · C1 §3-6 |
| `health` | object | 문진 — 직원 상세 `health` 와 같은 모양 · 같은 계산(`{state, submittedAt, needCount, items[]}` · 실패면 `state = error`) | DEC-012 D-10 · C1 §1-2 · 코드 규약: `:621-643` `_health` |
| `previousVisits` | array \| null | 이전 방문 = 직원 `previous_visits` 와 같은 칸(`date` · `start` · `result` · `resultRaw` · `zoneTitle` · `groupTitle` · **`reservationMemo` · `consultationMemo`** · `procedures[{title, status, doctors[]}]` — **의사 이름 포함**) + **`counselors[]`**. 그 예약 날짜와 같은 날 일정은 뺀다(직원과 같음). null = 4단계 이전 방문 조회 실패 | DEC-012 D-02 · D-10 · C1 §3-9 · 코드 규약: `:192-218` |
| `previousVisits[].counselors[]` | `{staffId, name}`[] | 그 방문의 상담자 = KOS 일정 `consultations[].counselors[]`(나온 차례 · 같은 KOS id 는 한 번). 그것이 비면 `consultation.counselor` 하나. 둘 다 없으면 `[]`. `staffId` = ccc 직원 사본 id(없으면 null) | DEC-012 D-10 · C1 §3-9(같은 응답 · 호출 0 추가) |
| `partialErrors[]` | string[] | 실패한 KOS 읽기 — `schedule`(3단계 · 희망 시술 · 희망 의사 · 지금 메모 둘이 null) · `visitor`(나이 · 언어 · 고객 유입 null) · `questionnaire`(`health.state = error`) · `previousVisits`. 없으면 `[]` | DEC-012 D-23 · 코드 규약: `:581-619`(`personalError` 선례) |

- 응답에 **넣지 않는** 칸: 개인 정보 묶음의 전화 · 이메일 · 여권 · 주민 · 외국인 등록 번호 · 주소 · SNS · 고객 특이사항(`remark`) · 신분 확인 · 방 목록 · 상담사 목록 · 정산 · 화면 권한(`can`) · 띄우기 · 담당자(`assignee`) · 묶음 의사(`reservation.doctors`) · KOS id. 상담 기록 본문(`consultations[].content.text`)도 내지 않는다(요청에 없다)
- **「상담 여부」 · 「처음 상담 대기 시각」은 상세에 싣지 않는다** — 목록(§6.11)에 있다
- **오류**(§6.2 공통 + 아래):

| HTTP | code | 언제 | 근거 |
|---|---|---|---|
| 400 | `invalid_request` | `reservationId` 가 정수 아님 · 열람 헤더 꼴 틀림(새 경로 · DEC-012 D-37 ③) | §6.2 · §6.10 |
| 404 | `reservation_not_found` | 사본에 그 예약이 없음 | 1단계 |
| 404 | `reservation_gone` | KOS 가 그 일정을 404 로 줌(KOS 에서 지워짐). (0.4.6) 예약을 만든 직후에도 KOS 반영이 늦어 잠깐 날 수 있다 — 다시 부르면 된다(코드로 막지 않음 · 재시도 없음 · Swagger 상세 description 에 한 줄 · 2026-11-16 로컬 e2e 2번째(데모 KOS · 시험 고객의 시험 예약 2건 · 끝나고 취소): 새 예약 2건 중 1건이 첫 호출 404 · 다시 부르면 200) | 3단계 · 직원 code 그대로 · DEC-012 D-47 |
| 502 | `kos_unavailable` | KOS 설정 없음 | 2단계 |

- **KOS 비용**(요청 1번당): 내부 `get-schedule-detail` 1 + 내부 `get-visitor` 1 + 공개 문진 2 + 공개 `get-schedules-by-visitor` 1 = **5**. 404 면 0 · `reservation_gone` 이면 1(C1 §1-2 「5 ~ 6」 — 수납 금액을 부르지 않아 5)

### 6.13 (0.4.0) `PUT /api/ext/customers/{customerId}/language` — 고객 언어 (DEC-012 D-04 · D-11 · D-19)

**요청** `ExtLanguageRequest`: `{"language": "<KOS 언어 값>"}` — 필수 string. 앞뒤 공백을 지운다. **빈 문자열 = 비움**(직원 `PersonalIn.language` 「null/빈 값 = 비움」과 같다 · null 은 타입 오류 400). 선택 헤더 `X-Ext-Staff-Id`(§6.10 · 꼴이 틀리면 400). 값 꼴(데모 HAR 에서 2자 · 5자 두 꼴)은 검사하지 않고 KOS 에 그대로 보낸다(C1 §1-3 · 코드 규약: `app/schemas/reservations.py:841`).

**처리** — 직원 `ReservationService.personal(actor, customerId, PersonalIn(language=…))` 를 **그대로** 부른다(DEC-012 D-11 · 코드 규약: `app/service/reservations.py:1056-1084`):

1. 고객 사본에 없으면 → `404 customer_not_found`(lookup 404 와 같은 본문 — 직원 `NotFound("없는 고객이에요")` 를 외부 code 로 바꾼다). KOS 호출 0
2. 내부 `get-visitor` 로 다시 읽는다(1번). `data` 가 객체가 아니면 `502`
3. 다시 읽은 값과 같으면 KOS 쓰기를 하지 않고 `200`(event 없음)
4. 내부 `update-visitor-personal-information` — 다시 읽은 개인 정보 묶음 17키 중 **있는 키 전부** + `language` 만 바꿔 보낸다(K7)
5. 성공 → `event_log` `visitor_personal`(`fields: ["language"]` · actor = §6.10) · 날짜 캐시 비움. 언어는 사본 열이 없어서 사본 쓰기는 없다(C1 §1-3)

- **덮어쓰기 위험**(DEC-012 D-11 수용): 2단계 읽기와 4단계 쓰기 사이에 KOS 웹에서 다른 칸을 고치면 그 변경이 덮인다. 다시 읽은 응답에 없던 키를 KOS 가 비우는지는 확인하지 않았다(C1 §1-3). Swagger 설명에 적는다
- **응답 200**: `{"ok": true}`(직원 쓰기 응답 `OkResponse` 와 같은 모양 · 코드 규약: `app/schemas/actions.py:99-102`)
- **오류**(§6.2 공통 + 아래): `400 invalid_request`(`customerId` 정수 아님 · `language` 없음 · 타입 · 모르는 키 · 헤더 꼴) · `404 customer_not_found` · `409 kos_rejected`(KOS 4xx · 401 제외 — 문구는 지금 규칙) · `502 kos_unavailable`(네트워크 · 5xx · 401 · 응답 형식) — `kos_write` 규칙 그대로(DEC-012 D-04 · 코드 규약: `app/service/reservations.py:710-721` · `app/service/kos_errors.py:9-39`)
- **KOS 비용**: 내부 2(같은 값이면 1 · 404 면 0)

### 6.14 (0.4.0) `PUT /api/ext/reservations/{reservationId}/order-memo` — 오더 메모 (DEC-012 D-04 · D-05 · D-12 · D-19)

**요청** `ExtOrderMemoRequest`: `{"orderMemo": "<글>"}` — 필수 string. 글 전체를 **통째로 바꾼다**(일정 단위 글 하나 · C1 §4-1). 지금 값은 예약 상세(§6.12) `reservation.orderMemo` 로 읽는다. 빈 문자열은 그대로 보낸다(비움 · DEC-012 D-35). 선택 헤더 `X-Ext-Staff-Id`(§6.10 · 꼴이 틀리면 400).

**처리**:

1. 사본에 예약이 없으면 `404 reservation_not_found`(§6.12 와 같음 · KOS 호출 0)
2. 예약 상태로 막지 않는다 — DEC-012 D-35(직원 예약 메모의 「끝난 예약 409」는 예약 메모 규칙이고 오더 메모 규칙은 없다 · KOS 가 거르면 `409 kos_rejected`)
3. `kos_write(actor, "change-order-memo", client.internal("schedule/v1/commands/change-order-memo", {scheduleId: <사본 kos_id>, orderMemo}), reservation_id=…)` — 내부 1번(HAR `{scheduleId: uuid, orderMemo: str}` → `{}`)
4. 성공 → `event_log` `order_memo`(§3.5) → 사본: 시술 현황 사본 `visit` 에 같은 `kos_id` 행이 있으면 `order_memo` 를 그 값으로 바꾼다(다음 10초 조회가 같은 값을 다시 쓴다) · `after_write(그 날짜)`(코드 규약: `app/repository/db.py:22-25` `visit.order_memo` · `app/kos/sync.py:106` · `:117`). 예약 사본 `reservation` 에는 오더 메모 열이 없다. (0.4.1 · 검수 r1 W9) **visit 행이 있을 때만 `UPDATE visit SET order_memo = ? WHERE kos_id = ?` 한 줄**로 고친다 — `repository/repo.py` 에 이 함수 하나를 더한다. 일반 `tx.upsert("visit", …)` 를 쓰지 않는다(행이 없으면 새 visit 행 = 시술 현황판 유령 행을 만든다). 행이 없으면 사본 쓰기 0
5. 같은 값 건너뛰기는 없다 — 비교할 사본 열이 예약 쪽에 없다. 늘 KOS 를 1번 부른다

- **응답 200**: `{"ok": true}`
- **오류**: `400`(id · 본문 · 헤더) · `404 reservation_not_found` · `409 kos_rejected` · `502 kos_unavailable`(§6.13 과 같은 `kos_write` 규칙)
- 예약 메모(`reservationMemo` · 직원 `PUT /api/reservations/{id}/memo`)와 **다른 칸**이다. Swagger 에 적는다(C1 §4-3 표)
- **KOS 비용**: 내부 1(404 면 0)

### 6.15 (0.4.0) `PUT /api/ext/reservations/{reservationId}/consultation-memo` — 상담 메모 (DEC-012 D-04 · D-05 · D-13 · D-19)

**요청** `ExtConsultationMemoRequest`: `{"consultationMemo": "<글>"}` — 필수 string · 통째로 바꾼다(지금 값 = §6.12 `reservation.consultationMemo`) · ~~빈 문자열 그대로(DEC-012 D-35)~~ (0.4.6 · DEC-012 D-47 고침) **빈 값은 `400 invalid_request`** — 앞뒤 공백을 지운 뒤 빈 문자열이면(`""` · 공백만) message `body.consultationMemo: KOS 는 상담 메모를 비울 수 없어요` 꼴로 거절하고 KOS 를 부르지 않는다(`event_log` 0). KOS 는 상담 메모를 비울 수 없다 — `""` · `null` 을 보내면 200 인데 값이 그대로다(2026-11-16 로컬 e2e 2번째(데모 KOS · 시험 고객의 시험 예약 2건 · 끝나고 취소)). 200 인데 안 바뀌는 것보다 400 이 낫다(코디 기본값). 오더 메모(§6.14)는 빈 값 = 비움 그대로다 · 선택 헤더 §6.10.

**처리**: §6.14 와 같은 차례다. 3단계 호출만 다르다 — **공개** `schedule/open/v1/commands/update-schedule-consultation-info {scheduleId, consultationMemo}`(`KosClient.open` · 스펙 `updateScheduleConsultationInfo` · C1 §4-5). 4단계 = `event_log` `consultation_memo` · `after_write`. 상담 메모를 담는 사본 열은 없다.

- 「차트 메모」 = 이 상담 메모다(DEC-012 D-05). Swagger 에 적는다
- (0.4.6 · 실물 확인 ④ 결과 · 2026-11-16 로컬 e2e 2번째(데모 KOS · 시험 고객의 시험 예약 2건 · 끝나고 취소)) 값이 있으면 KOS 값이 바뀐다(200) · 쓰기 전 · 뒤 같은 일정의 **상담사 · 의사 칸은 그대로**다 · **상담 전(예약 상태) 일정에 써도 200** 이다 · 빈 값은 비워지지 않는다(위 요청 줄 · D-47). 공백 한 칸 같은 공백만 글은 KOS 에 그대로 저장되므로 우리가 400 으로 막는다. 아래 줄은 0.4.0 판의 「모름」 기록이다
- 이 쓰기는 스펙으로만 봤고 HAR · 데모 실호출이 없다(C1 §4-5 「스펙」). 작업 이름이 「info」라 **본문에 없는 상담 칸(상담사 · 의사 · 결과)을 KOS 가 비우는지**, **상담 전 일정(접수 전 · 상담 없음)에 쓰면 무엇이 오는지** 모른다. WORK-014 실물 확인 ④(시험 예약 · 되돌림)에서 둘 다 본다. 다른 칸이 비면 그 사실을 리포트에 적어 코디에게 올린다(검수 r1 W10)
- **응답 · 오류**: §6.14 와 같다. (0.4.6) 더해 빈 값 = `400 invalid_request`(message 위 꼴 · KOS 0)
- **KOS 비용**: 공개 1(404 · 빈 값 400 이면 0)

### 6.16 (0.4.0) `GET /api/ext/clinic` — 병원 정보 (DEC-012 D-14 · D-20 · D-22 · D-24 ~ D-28)

**요청**: 질의 칸 없음.

**처리**:

1. runtime 이 없으면 `502 kos_unavailable`
2. 내부 3번을 **동시에** 부른다(요청마다 · 저장 · 캐시 없음 — DEC-012 D-28):
   - `v1/hospital/queries/get-hospital` 본문 `{}` → `data` 17칸(`병원정보.har` — C3 §2.1)
   - `schedule/default-operation-time/v1/queries/get-default-operation-timetable` 본문 `{}` → `data{monday … sunday: {enabled, startTime, endTime, breaktime{startTime, endTime}}}`(`상담대기2.har` · 시각은 `YYYY-MM-DDTHH:MM:SSZ` 꼴 문자열 · 쉬는 시간이 없으면 빈 문자열)
   - `schedule/default-operation-time/v1/queries/get-default-days-off` 본문 `{startDateTime, endDateTime}`(UTC ISO 밀리초 `Z` 꼴) → `data[]` — (0.4.3 · KOS0 ②) 원소 = `{id, startDateTime, endDateTime}` 3키(UTC ISO 초 `…SSZ` · 끝은 배타로 보임 · 이름 칸 없음). 기간 = 오늘(KST) 0시 ~ 오늘 + 90일 끝(가능 시간대 날짜 범위 DEC-011 D-08 과 같은 폭 · DEC-012 D-27)
3. 셋 중 **하나라도** 실패(네트워크 · 5xx · 4xx · 401 · `data` 모양 틀림)하면 `502 kos_unavailable`(부분 응답을 내지 않는다 · DEC-012 D-28)
4. 운영 시간 = 지금 예약 그룹 시간표를 바꾸는 `timetable_of()` 를 그대로 쓴다(`{"operationTimetable": data}` 로 넘김 · 같은 요일 키 · 같은 칸 모양) → 요일마다 KST `HH:MM`(코드 규약: `app/kos/reservation_sync.py:52-62`)

**응답 200** `ExtClinic`:

| 칸 | 타입 | KOS · 뜻 | 낼지 | 근거 |
|---|---|---|---|---|
| `clinicId` | int | CC 고정 값 **`1`** — CC 서버 하나 = KOS 병원 하나. 직원 목록(§6.17) 경로에 이 값을 쓴다. 전역 유일하지 않다(CC 서버 여럿을 모으면 겹친다 — Swagger 에 적는다) | 냄 | DEC-012 D-20 · D-24 |
| `name` | string \| null | `hospitalName` | 냄 | DEC-012 D-22 · D-25 |
| `phone` | string \| null | `hospitalPhoneNumber` 그대로(국가 번호를 붙이지 않는다 — KOS 웹은 `82` 를 붙여 보여 준다 · C2 §1.2) | 냄 | DEC-012 D-22 · D-25 |
| `address` | `{address, detailed, zipCode}` \| null | `addressContract{address, detailedAddress, zipCode}`. 세 칸 모두 비면 null | 냄 | DEC-012 D-22 · D-25 · C3 §2.1 |
| `operatingHours` | object | 요일(`monday` … `sunday`)마다 `{enabled, start, end, breakStart, breakEnd}`(KST `HH:MM` \| null) — 병원 기본 운영 시간(예약 그룹별 시간표가 아니다) | 냄 | DEC-012 D-14 · D-22 · D-25 |
| `daysOff[]` | array | 병원 기본 휴무 — (0.4.1 고침 · 검수 r1 W11) KOS 원소를 **그대로 주지 않는다.** (0.4.3 · KOS0 ② · DEC-012 D-43) 원소 = **`{startDate, endDate}`** — 둘 다 KST `YYYY-MM-DD`. `startDate` = `startDateTime` 의 KST 날짜, `endDate` = `endDateTime` **직전 시각**의 KST 날짜(끝이 배타라서). 하루 휴무면 둘이 같다. 여러 날 휴무는 한 원소로 그대로 옮긴다(날마다 쪼개지 않는다). KOS `id` 는 내지 않는다. **`name` 칸은 없다** — KOS 에 이름 칸이 없으므로 지어 채우지 않는다. 차례 = KOS 배열 차례. ~~고른 칸 집합은 KOS0 판정 뒤 코디가 넣는다 · 예 `{date, name}`~~ | 냄 | DEC-012 D-14 · D-27 · D-43 · KOS0 ② |
| — | — | (0.4.1) `nationality` · `languages` · `websiteUrl` · `translsMap` · `representativeName`(대표자) · `companyName` · `companyRegistrationNumber`(사업자 번호) · `nursingInstitutionNumber`(요양기관 번호) · `qualifiedInvoiceIssuerNumber` · `taxBillEmail` · `businessLicenseImageUrl` · `logoImageUrl` · `representativeStampImageUrl` · `hospitalMapImageUrl` | **안 냄**(「원하는 데이터만」) | DEC-012 D-25 · C3 §2.1 · §3-4 |

- 빈 문자열로 온 칸은 null 로 준다 — DEC-012 D-26(KOS 는 빈 칸도 빈 문자열로 준다 · 데모는 17칸 중 14칸이 비었다 · C3 §2.1)
- **오류**: 공통 + `502 kos_unavailable`(1 · 3단계)
- **KOS 비용**: 내부 3

### 6.17 (0.4.0) `GET /api/ext/clinics/{clinicId}/staff` — 직원 목록 (DEC-012 D-06 · D-15 · D-20 · D-21 · D-29 · 0.4.7 D-48)

**요청**: 경로 `clinicId`(정수). §6.16 의 `clinicId` 가 아니면 `404 clinic_not_found`(KOS 호출 0).

**처리**:

1. runtime 이 없으면 `502 kos_unavailable`
2. 내부 `account/v2/queries/get-accounts` 본문 `{}` 1번(C2 §2.2 · `상담대기.har` #11). 실패 · `data` 가 배열 아님 · (0.4.7 · 검수 r1 W4) 원소가 객체가 아님 · 원소에 `id` 없음(빈 값) → `502 kos_unavailable`(지금 코드 그대로 적은 것 — 동작 변화 0 · 코드 규약: `app/service/ext.py:884`)
3. 원소마다 한 줄. **KOS 시스템 계정**(`KosClient.system_kos_id()`)과 **제외 목록**(`KOS_EXCLUDE_ACCOUNT_IDS`)의 계정은 뺀다(DEC-012 D-21 · 원장 · 상담사 목록과 같은 기준 · 코드 규약: `app/service/reservations.py:109-115` · `app/kos/sync.py:175` · `app/config.py:81-83`)
4. 칸 결합 — DEC-012 D-29: 이름 · 역할 이름 · 활성은 내부 응답(지금 KOS 값)에서, `staffId` 와 `roleTags` 는 ccc 직원 사본(`staff` · 1시간마다 공개 `getAccounts` 로 덮어씀)에서 KOS 계정 id 로 잇는다. 내부 `role.roleTags` 는 숫자이고, 이름과의 대응은 순서로 맞춘 추정이라(C2 §2.2) 쓰지 않는다. 사본에 없는 계정(1시간 동기화 전 새 계정)은 `staffId = null` · `roleTags = []`. (0.4.7 · DEC-012 D-48) `email` · `realName` · `kosAccountId` 도 **내부 응답**(지금 KOS 값)에서 그대로 옮긴다 — 사본을 읽지 않고 사본에 저장하지도 않는다. `kosAccountId` 는 지금 사본을 잇는 데 쓰는 바로 그 값이다(코드 규약: `app/service/ext.py:894` `str(a["id"])`). 원소에 `id` 가 없으면 지금처럼 2단계의 `502` 다(코드 규약: `app/service/ext.py:884` — 바꾸지 않는다)
5. 차례 = KOS 배열 순서. 비활성 직원도 싣는다

**응답 200** `ExtStaffList`:

| 칸 | 타입 | 뜻 · null | 근거 |
|---|---|---|---|
| `clinicId` | int | 요청 값 | DEC-012 D-20 |
| `staff[]` | array | 직원 | DEC-012 D-15 |
| `.staffId` | int \| null | ccc 직원 사본 id(예약 상세 · 접수 목록의 `counselor.staffId` 와 같은 체계) | DEC-012 D-15 · 4단계 |
| `.name` | string | 내부 `name` | DEC-012 D-15 |
| `.roleName` | string \| null | 내부 `roleName`(KOS 역할 설정 값 · 지점마다 다름 · 예 「CS팀(콜센터)」 = 외주 직원) | DEC-012 D-06 · D-15 · C2 §2.2 |
| `.roleTags` | string[] | 공개 역할 태그(`ADMIN` · `DOCTOR` · `COUNSELOR` · `NURSE` · `SKINCARE` · `CALL_COUNSELOR` · `COORDINATOR`) | DEC-012 D-15 · C2 §2.1 |
| `.active` | bool | 내부 `activate` | DEC-012 D-15 |
| `.email` | string \| null | (0.4.7) 내부 원소 `email` 그대로. `null` · 빈 문자열 · 칸 없음 → null | DEC-012 D-48 · C2 §2.2 |
| `.realName` | string \| null | (0.4.7) 내부 원소 `realName` 그대로. `null` · 빈 문자열 · 칸 없음 → null. **`name` 과 다른 칸이다** — `name`(KOS 표시 이름)은 그대로 둔다 | DEC-012 D-48 · C2 §2.2 |
| `.kosAccountId` | string | (0.4.7) 내부 원소 `id` = KOS 계정 id 를 문자열로. null 이 없다(3 · 4단계가 이미 이 값으로 계정을 거르고 사본을 잇는다). **`staffId` 와 다른 체계다** — 다른 ext 응답의 `staffId`(ccc 정수)와 이 값을 잇는 곳은 이 목록뿐이다 | DEC-012 D-48 · 코드 규약: `app/service/ext.py:884` · `:894` |

- 응답에 **넣지 않는** 칸: ~~이메일 · `realName`~~ · `userId` · `licenseNumber` · `mfaMethods` · `roleId` ~~· KOS 계정 id~~(DEC-012 D-15 · 코디 Q2 · 0.4.7 — 이메일 · `realName` · KOS 계정 id 는 **낸다** · DEC-012 D-48. 남은 넷은 그대로 내지 않는다)
- (0.4.7) **응답 밖에 남기지 않는다**: 세 값(`email` · `realName` · `kosAccountId`)을 `ext_call` · 앱 로그에 쓰지 않는다. CC 직원 사본(`staff`)에 이메일 · 실명을 저장하지 않는다 — 사본 표 · 동기화는 바꾸지 않고 매 호출 KOS 값을 옮긴다(DEC-012 D-48 · DEC-010 D-24)
- Swagger 설명: 「외주 직원은 역할 이름으로 구분한다(예 CS팀(콜센터)). `roleTags` 에 `CALL_COUNSELOR` 가 있다고 외주가 아니다 — 코디 · 관리자에게도 붙는다」(C2 §2.2)
- (0.4.7) Swagger 설명 고침: 지금 `STAFF_DOC` 의 「이메일 · 실명 · KOS id 는 내지 않는다」 를 지우고 「`email` · `realName` · `kosAccountId` 를 낸다 — `kosAccountId` 는 KOS 계정 id 이고 `staffId`(ccc)와 다른 체계다 · `email` · `realName` 은 KOS 에 값이 없으면 null」 로 바꾼다(시험 = §9 T70). 첫 줄의 칸 나열에도 셋을 더한다. `ExtStaff` 의 새 세 칸에 `description` 을 단다(§8 「모든 칸 `description`」 · 코드 규약: `app/api/ext.py:520-529` · `app/schemas/ext.py:491-501` · DEC-012 D-48)
- **오류**: `400`(`clinicId` 정수 아님) · `404 clinic_not_found` · `502 kos_unavailable`
- **KOS 비용**: 내부 1(404 면 0)

### 6.18 (0.4.0) 내부 API 의존 한눈에 (DEC-012 Consequences)

이 표의 「내부」 작업은 시스템 계정 토큰 · 브라우저 UA 조건(2026-11-03~)에 묶인다. 조건이 바뀌면 그 경로가 `502`(쓰기는 `502` 또는 `409`)로 멈춘다. board 는 멈추지 않고 낡은 사본 + `sync.lastError` 를 낸다.

| KOS 작업 | 종류 | 쓰는 외부 경로 | 0.4.0 새로 | 근거 |
|---|---|---|---|---|
| `visitor/v2/queries/get-visitors` | 내부 · 읽기 | lookup(이름 갈래) · 예약 · 과거 시술 · 예약 내역 | — | DEC-010 D-15 |
| `ticket/v1/queries/get-ticket-bundles` | 내부 · 읽기 | lookup | **새로**(공개 → 내부) | DEC-012 D-08 ② · §4.3 |
| `visitor/v2/queries/get-visitor` | 내부 · 읽기 | lookup(`customerId` 갈래) · 예약 상세 · 고객 언어 | **새로** | §6.4 · §6.12 · §6.13 |
| `visitor/v2/commands/update-visitor-personal-information` | 내부 · **쓰기** | 고객 언어 | **새로** | DEC-012 D-11 |
| `schedule/v1/commands/change-order-memo` | 내부 · **쓰기** | 오더 메모 | **새로** | DEC-012 D-12 |
| `schedule/v1/queries/get-schedule-detail` | 내부 · 읽기 | 예약(다시 읽기) · 예약 상세 | 예약 상세 새로 | §6.5 · §6.12 |
| `schedule/v1/queries/get-schedule-event-logs` | 내부 · 읽기 | 접수 목록 | **새로** · (0.4.3) 실응답 확인함(KOS0 ① · 데모 40/40 `200`) ~~실응답 미확인(D-17 대안이면 0)~~ | DEC-012 D-16 · D-17 · D-42 |
| `schedule/v2/queries/get-schedules-for-reservation` · `meta/notice/v1/queries/get-notices` | 내부 · 읽기 | 접수 목록(10초 날짜 조회 · 직원 화면과 같은 캐시) | 외부로는 새로 | §6.11 1단계 |
| `v1/hospital/queries/get-hospital` | 내부 · 읽기 | 병원 정보 | **새로** | DEC-012 D-14 |
| `schedule/default-operation-time/v1/queries/get-default-operation-timetable` · `get-default-days-off` | 내부 · 읽기 | 병원 정보 | **새로** | DEC-012 D-14 |
| `account/v2/queries/get-accounts` | 내부 · 읽기 | 직원 목록 | **새로** | DEC-012 D-15 |
| `schedule/open/v1/commands/update-schedule-consultation-info` | 공개 · **쓰기** | 상담 메모 | **새로** | DEC-012 D-13 |
| `purchase/open/prepaid-card/v1/queries/get-prepaid-card-summaries` | 공개 · 읽기 | lookup | **새로** | DEC-012 D-08 ③ |

- 외부 경로의 KOS 쓰기는 0.3.x 의 예약 생성(고객 만들기 포함) 하나에서 **넷**(예약 · 고객 언어 · 오더 메모 · 상담 메모)으로 는다(C1 §5 「ext 에서 KOS 쓰기가 처음으로 3종 생긴다」)


---

## 7. 인증 · 보안 (D-10 · D-23 ~ D-26 · D-34)

### 7.1 키 (D-23)

- 연동처 = `linky` · `charty` 둘(코드에 고정). 키는 env `PROC_EXT_KEY_LINKY` · `PROC_EXT_KEY_CHARTY` 에서만 읽는다(§2.2). 레포 · 이미지 · 로그 · 응답 · DB 에 키 값이 없다
- 전달 = 요청 헤더 **`X-Api-Key`**. 경로 · 질의 · 쿠키로는 받지 않는다(코드 규약: `app/api/public_questionnaire.py:6` · `app/openapi_docs.py:64-66`)
- 비교 = 들어온 값을 각 연동처 키와 **상수 시간 비교**(`hmac.compare_digest`)로 견준다. 같으면 그 연동처다. 빈 env 인 연동처와는 견주지 않는다
- 키를 바꾸거나 끄는 것은 배포 설정(env · Secret)으로 한다. 앱에 키 관리 API 는 없다(D-23)

### 7.2 직원 API 와의 분리 (D-10)

| 경우 | 결과 | 근거 |
|---|---|---|
| `/api/ext/*` 에 직원 `Authorization: Bearer <ccc 토큰>` 만 | `401 ext_unauthorized`(Bearer 는 보지 않는다) | D-10 · 코드 규약: `app/api/public_questionnaire.py:5` |
| `/api/ext/*` 에 Bearer + 맞는 `X-Api-Key` | 외부 키 권한으로만 동작한다(직원 권한이 더해지지 않음) | D-10 |
| 직원 API(`/api/*` 중 `/api/ext` 밖)에 `X-Api-Key` 만 | 지금처럼 `401 unauthorized`(직원 API 는 `X-Api-Key` 를 보지 않는다) | D-10 · 코드 규약: `app/api/deps.py:17-21` |
| 외부 라우터 | `require_login` · `Actor` 를 쓰지 않는다. 의존성은 `require_ext_key` 하나다 | D-10 · 코드 규약: `app/api/deps.py:17-24` |

`PROC_FAKE_BOARD`(가짜 스냅샷)는 외부 API 에 걸지 않는다. 외부 API 는 가짜 스냅샷을 읽지 않고(메뉴 = 메뉴 표 · 조회 = KOS), 예약은 지금 `create()` 를 그대로 탄다(코드 규약: `app/api/deps.py:27-31` — `require_real_board` 는 직원 조작 라우터에만 걸려 있다).

### 7.3 호출 제한 (D-25 · D-34)

- **키(연동처)당, 최근 60초 안에 60번**. 외부 경로 전부(0.4.0 — 열셋)를 합쳐서 센다(DEC-011 D-01 · DEC-012 D-01). 넘으면 `429 too_many_requests` 다(D-34)
- 창 = 고정 1분이 아니라 **미끄러지는 창**이다. 최근 60초 안의 횟수가 60 밑으로 내려가는 순간 다시 열린다. 막힌 요청은 횟수에 더하지 않는다(코드 규약: `app/api/public_questionnaire.py:45-49` · `app/service/questionnaire.py:73-95` `RateLimiter` 를 다시 쓴다)
- 서버 메모리 카운터다(재시작하면 지워진다). **지금 배포 가정 = 파드 1개**(SQLite 파일 하나 · 코드 규약: `app/repository/db.py:1`)라 파드 사이 공유가 필요 없다
- 키가 틀린 요청(401)은 연동처가 없으므로 이 키당 카운터에는 세지 않는다(아래 IP 카운터가 센다)
- 응답 헤더(`Retry-After` 등)는 싣지 않는다 — 지금 `429` 들과 같다(코드 규약: `app/service/questionnaire.py:243`)

**키 없는 거절 IP 제한**(키 추측 · `ext_call` 쌓기 막기 — 문진 웹 선례를 값까지 그대로 쓴다)

- 센다: `/api/ext` 에서 **키 없는 거절**(§3.4 정의 — 401 · 없는 경로 404 · 깨진 본문 400 · 405)이 나갈 때마다 그 IP 카운터에 1을 더한다. IP 차단 429 자신은 더하지 않는다(아래 「막힌 요청은 더하지 않는다」)(코드 규약: `app/service/questionnaire.py:264-265` — 틀린 · 지난 토큰 404 · 410 이면 `rate.add(("bad", ip))`)
- 막는다: 그 IP 의 이 카운터가 **최근 60초 안에 10번 이상**이면, 그 IP 의 `/api/ext` 요청을 키 검사 전에 `429 too_many_requests` 로 막는다. 미끄러지는 창이라 10 밑으로 내려가는 순간 다시 열린다. 막힌 요청은 더하지 않는다(코드 규약: `app/service/questionnaire.py:40` `WINDOW_SEC = 60.0` · `:42` `LIMIT_BAD_IP = 10` · `:253-256` `_gate` · `app/api/public_questionnaire.py:45-49`)
- 자리: 없는 경로 404 는 라우터 밖이므로 이 판단과 카운트는 `/api/ext` 미들웨어가 한다(§3.4 와 같은 미들웨어)
- IP = `CF-Connecting-IP` → `X-Forwarded-For` 첫 값 → 소켓 주소 순 — 지금 `client_ip()` 를 다시 쓴다. IP 는 메모리 카운터 키로만 쓰고 DB · 로그에 남기지 않는다(코드 규약: `app/api/public_questionnaire.py:21-33`)

### 7.4 기록 (D-24)

- `/api/ext/…` 로 들어온 **모든 요청**(성공 · 401 · 429 · 400 · 404 · 405 · 409 · 500 · 502 · 503)마다 미들웨어가 응답을 낸 뒤 `ext_call` 1줄을 쓴다(§3.4 — `client` · `endpoint` 를 정하는 법도 거기). 다만 키 없는 거절(`client` 가 null 인 모든 `/api/ext` 오류 응답 — 401 · 없는 경로 404 · 깨진 본문 400 · 405 · IP 차단 429 · §3.4)은 같은 IP · 같은 `outcome` 이면 1분에 1줄로 줄인다(§3.4). 쓰기 실패는 응답을 바꾸지 않는다(로그에 예외 종류만)
- **처리하지 못한 예외** = `500 internal_error`. `ext_call` 1줄을 쓴다(1분 1줄 줄이기 없음). 서버 쪽 잘못이므로 `client` 가 null 이어도 「키 없는 거절」(§3.4)로 보지 않고 IP 카운트(§7.3)에 넣지 않는다. 앱 설명의 공통 오류 줄(§8)에도 500 을 적는다
- 이름 · 이메일 원문 · 키 값 · 고객 정보는 `ext_call` · 앱 로그 어디에도 남기지 않는다. 앱 로그에는 연동처 · 엔드포인트 · 상태만 남긴다(D-24 · 코드 규약: `app/service/kos_errors.py:42-44` `describe` — 상태 · 이름만)

### 7.5 그 밖

- 고객 조회 · 예약 응답은 `Cache-Control: no-store`(§6.1)
- KOS 내부 API(시스템 계정 토큰 · 브라우저 UA) 조건이 바뀌면 고객 조회 · 예약이 `502 kos_unavailable` 로 멈춘다. 메뉴는 공개 API 와 DB 라서 영향을 받지 않는다(DEC-010 Consequences · D-15)

### 7.6 협업자 admin 계정 (D-26)

외부 API 를 배포하면 협업자에게 공유한 admin 계정 대신 연동처 키를 쓰도록 **권한다**. 계정 회수 시점은 사용자가 정한다. 이 문서 · WORK 는 회수 작업을 하지 않는다.

---

## 8. Swagger (코드 규약: `app/openapi_docs.py` · `tests/test_openapi_docs.py`)

| 항목 | 계약 | 근거 |
|---|---|---|
| tag | 새 tag **`외부 연동`**(`app/api/docs.py` 에 `T_EXT`). 설명: 「링키 · 차티 같은 외부 연동처용 — `X-Api-Key` 헤더로 연다. 직원 로그인 토큰으로는 열리지 않는다.」 외부 경로 여섯 모두 이 tag 하나만 단다(0.3.0) | D-10 · 코드 규약: `app/api/docs.py:42-44` · `app/openapi_docs.py:98-115` |
| securityScheme | `components.securitySchemes.ExtApiKey = {type: "apiKey", in: "header", name: "X-Api-Key", description: "연동처별 API 키(링키 · 차티 각각). 직원 Bearer 와 다르다."}`. `BearerAuth` 는 그대로 둔다 | D-10 · D-23 · 코드 규약: `app/openapi_docs.py:118` · `:150-152` |
| 보안 표시 | `require_ext_key` 의존성이 있는 operation 에 `security: [{ExtApiKey: []}]` 를 단다. `BearerAuth` 는 달지 않는다. `_patch` 가 `_needs_login` 처럼 의존성을 보고 단다 | 코드 규약: `app/openapi_docs.py:121-159` |
| 앱 설명 | `DESCRIPTION` 에 `## 외부 연동 API` 절을 더한다. **첫 줄**: 「email 이 없는 기존 고객은 조회하면 `404` 다. 그 고객을 처음 예약하면 KOS 에 고객이 하나 더 생길 수 있다(데스크가 정리한다).」(D-22). 이어서 「이름은 KOS 에 저장된 띄어쓰기 그대로 보내야 한다(띄어쓰기가 다르면 찾지 못해 `404`).」(D-17 · R4 §0 #2 · §2.1). 그 뒤에 들어갈 것: 경로 여섯(0.3.0 — 「경로 셋」 줄을 여섯으로) · `X-Api-Key` · 연동처별 키 · 직원 API 와 분리 · 검사 순서(§6.1) · 호출 제한(키당 · IP 당 · §7.3) · 기록(무엇을 남기고 무엇을 안 남기나 · §7.4) · 오류 공통 표(§6.2) · 금액 칸 규칙(§6.1) | D-22 · 코드 규약: `app/openapi_docs.py:19-96` |
| 엔드포인트 | `summary` · `description` · 모든 응답 칸 `description` · 응답 표(`responses=` — `- \`code\` — 언제` 줄 꼴)를 지금 규약대로 단다. 설명에 적을 것: 조회 = §5 의 「없음 = 같은 응답」(이름 정확 일치 · `count` > 1000 포함) · **「이름은 KOS 에 저장된 띄어쓰기 그대로 보내야 한다」**(KOS 이름 검색이 공백을 그대로 비교한다 — 띄어쓰기가 다르면 KOS 가 0건을 돌려줘 404. 「공백은 무시한다」고 약속하지 않는다 · R4 §0 #2 · §2.1) · §4.3 의 KOS 그대로의 성질 셋(`bundlePrice` 는 고객이 낸 돈이 아님 · 세트를 쓰면 줄 수 있음 · 부가세 포함 여부 표기 안 함 / ~~`AVAILABLE` 0 묶음 없음~~ (0.4.0 고침 · 검수 r2 N4 — 사용 중 장만 남은 묶음이 나오므로 이 문장을 **지운다**. 지금 코드 `app/api/ext.py:155-156` 「`AVAILABLE` 이 0장인 묶음은 KOS 가 주지 않는다」도 지우고 §8 엔드포인트(0.4.0) 의 새 문장으로 바꾼다) / `IN_USE` 는 남은 장수에 안 넣음) · 예약 = **D-35 문장**(「0명 갈래에서 KOS 중복 검사에 걸리면 409, 아니면 200 이라 그 이메일이 KOS 에 있는지가 드러난다」) · 메뉴 = `syncedAt` 뜻(D-36) | D-31 · D-35 · D-36 · 코드 규약: `tests/test_openapi_docs.py:33-68` · `:104-107` `_codes` |
| 상태 문구 | `app/api/docs.py` `STATUS_TEXT` 에 **`503: "지금 쓸 수 없음"`** 을 더한다(지금 없어서 응답 표 머리가 「오류」로 나온다). 401 머리 「로그인 필요」는 그대로 두고, 외부 401 은 `errors()` 를 그대로 쓰되 `ext_unauthorized` 의 「언제」 줄을 「직원 로그인이 아니라 `X-Api-Key` 헤더의 연동처 키가 없거나 틀렸을 때 …」로 시작한다 | 코드 규약: `app/api/docs.py:46-47` · `:62-68` · review-doc r1 W12 |
| 문서 경로 | 지금 그대로(`/api/docs` · `/api/redoc` · `/api/openapi.json` · 로그인 없이 열림 — `_RESUME` §2 2026-11-11) | `_RESUME` §2 |
| 시험 고침 | `tests/test_openapi_docs.py` 의 `secured == n_ops - 5` 를 **`n_ops - 5 - 3`**(외부 세 operation 은 Bearer 가 아님)으로 고치고, 주석에 외부 셋을 적는다. **0.3.0: `n_ops - 5 - 6`**(외부 여섯) · `tests/test_ext_docs.py` 의 `OPS` 를 여섯으로. **0.3.1: 같은 파일 끝의 parameters 단언을 지우지 않고 넓힌다** — `/api/ext` 모든 operation 의 parameters = `X-Api-Key`(header) + `GET /api/ext/availability` 의 `date`(query) 하나뿐 · 그 밖 query · path 칸 0(`name` · `email` 이 질의에 생기면 실패해야 한다 — D-24 · DEC-011 D-06 · 문서 검수 add1 W3). 나머지 단언(설명 빠짐 0 · 422 없음 · `unauthorized` ↔ `require_login`)은 그대로 통과해야 한다 | 코드 규약: `tests/test_openapi_docs.py:78-101` |
| 「셋」 문구(0.3.1) | 코드에 남은 「세 경로 합산」(`app/openapi_docs.py:85` 앱 설명 호출 제한 줄) · 「세 엔드포인트 합산」(`app/api/ext.py:100` `EXT_RATE` — `COMMON` 으로 여섯 경로의 429 표에 다 붙는다) 문구를 **「외부 경로 전부 합산」** 으로 바꾼다. 「셋」 · 「세 경로」 · 「세 엔드포인트」를 `app/` 에서 전부 세어 고친다 | §7.3 · DEC-011 D-01 · 문서 검수 add1 W4 |
| 엔드포인트(0.3.0) | 새 셋도 `summary` · `description` · 모든 응답 칸 `description` · 응답 표를 단다. 설명에 적을 것: 가능 시간대 = 기본 그룹 하나 · 운영 구간 안 간격 칸 · 남은 자리 0 · 지난 시각 · 자리 수를 모르는 시각은 나오지 않음(「목록에 없어도 예약이 될 수 있다」) · 「이 목록의 `start` 로 예약하면 정원 때문에 거절되지 않는다 — 그 사이 다른 예약이 끼면 `409 slot_full`」 · 날짜 범위 오늘 ~ 90일 / 과거 시술 = 최근 50 · 메모 · 의사 없음 / 예약 내역 = 오늘 0시 이후 · 취소 포함 · `reservationId` null 뜻 / 둘 다 = 조회와 같은 고객 찾기(이름 띄어쓰기 · 「없음」 같은 응답) · **오늘 겹침 문장**(「오늘 이미 시작한 일정은 과거 시술과 예약 내역 둘 다에 나온다」) · KOS 호출 비용(§6.9) | DEC-011 D-02 ~ D-14 · 코드 규약: `app/api/ext.py:119-169`(`SHARED` · `NAME_RULE` · 설명 꼴) |
| tag · 보안(0.4.0) | 새 일곱도 tag `외부 연동` 하나 · `security [{ExtApiKey: []}]` · 응답 표 `responses=errors(*COMMON, …)` | DEC-012 D-01 · 코드 규약: `app/api/ext.py:100-115` `COMMON` |
| 엔드포인트(0.4.0) | 새 일곱 + lookup 의 `summary` · `description` · 모든 칸 `description` · 응답 표. 설명에 적을 것: lookup = **`customerId` 갈래(이름 + 이메일 없이 열림)** · 「(0.4.0 행동 변화) 사용 중 장만 남은 묶음도 나온다 · `inUseCount` · `totalCount` 는 사용 중 장도 센다」 · **(0.4.1 행동 변화) 「선불카드 조회가 실패해도 `200` — `prepaidCards: null` · `partialErrors: ["prepaidCards"]`」 · 「요청은 `name` + `email` 또는 `customerId` 하나 — 섞이거나 한쪽만이면 `400`(message `body: …`)」** · 선불카드 칸(금액 꼴) · 만료일 칸 없음 / board = 「오늘만 · 예약 단위 · 10초 사본(`sync.lastError` 면 낡음)」 · **「`counselor` = KOS 희망 상담사(실제 상담자 아님)」** · 「`roomTitle` = 가장 늦게 배정된 방」 · 「`consultation` = CC 판정」 · `firstConsultationWaitingAt` null 뜻 · (0.4.1) 「두 칸은 따로 정한다 — `consultation = false` 여도 시각이 있을 수 있다」 · 「아직 못 찾은 시각은 일정의 단계가 바뀔 때(상담 대기 · 귀가) 다시 확인한다 — 화면을 자주 불러도 늘지 않는다」 / 상세 = 이전 방문 메모 · 의사 · 상담자를 준다(「과거 시술 경로와 다르다」) · (0.4.1) 지금 오더 메모 · 상담 메모(쓰기 전에 읽는 곳) · `partialErrors` 뜻 · (0.4.6 · D-47) 「예약을 만든 직후에는 KOS 반영이 늦어 `reservation_gone` 이 잠깐 날 수 있다 · 다시 부르면 된다」 / 언어 = 「다시 읽고 묶음 전체 보냄 — 그 사이 KOS 웹 변경을 덮을 수 있다」 / 오더 메모 = 「예약 메모와 다른 칸 · 통째로 바꿈」 / 상담 메모 = 「= 차트 메모」 · (0.4.6 · D-47) 「KOS 는 상담 메모를 비울 수 없다 — 빈 값(공백만 포함)은 `400`」 · 응답 표 `400` 줄에 빈 값 / 병원 = `clinicId` 뜻(전역 유일 아님) · 운영 시간 = 병원 기본(그룹별 아님) · (0.4.3) 휴무 = 「`{startDate, endDate}` KST 날짜 범위(끝 포함 · 하루면 둘이 같음) · 이름 칸 없음」 / 직원 = 「외주는 역할 이름으로 · `CALL_COUNSELOR` 태그만으로 가르지 않는다」 · (0.4.7 · DEC-012 D-48) 「`email` · `realName` · `kosAccountId` 를 낸다 · `kosAccountId` 는 `staffId` 와 다른 체계 · 값이 없으면 `email` · `realName` 은 null」(옛 문장 「이메일 · 실명 · KOS id 는 내지 않는다」 지움 · §6.17) / 쓰기 셋 = 「KOS 먼저 · KOS 실패 = 그 오류 그대로」 · 각 경로 KOS 호출 수(§6.9) | DEC-012 D-03 · D-09 ~ D-15 · D-23 |
| 열람 헤더(0.4.0) | `X-Ext-Staff-Id` 를 `Header(default=None, alias=…, description=…)` 로 받는 공통 의존성 — (0.4.1) **둘**(lookup 용 너그러운 것 · 새 넷 용 엄격한 것 · 꼴 검사 함수 하나 공유)이고 **다섯 경로에만** 단다. 설명은 §6.10 「Swagger」 줄 | DEC-012 D-18 · D-37 |
| 시험 고침(0.4.0) | `tests/test_openapi_docs.py` 의 `n_ops - 5 - 6` → **`n_ops - 5 - 13`** · `tests/test_ext_docs.py` 의 `OPS` 를 열셋으로. parameters 단언은 지우지 않고 넓힌다 — 허용 = `X-Api-Key`(header) · `X-Ext-Staff-Id`(header — (0.4.1) **lookup · 예약 상세 · 쓰기 셋 다섯 operation 에만** · 그 밖 operation 에 있으면 실패) · availability `date`(query) · 경로 정수 칸 `reservationId` · `customerId` · `clinicId`(path)뿐. `name` · `email` 이 질의 · 경로에 생기면 실패해야 한다(D-24 · DEC-011 D-06) | 코드 규약: `tests/test_openapi_docs.py:87-97` · `tests/test_ext_docs.py:6` · `:61` · §8 시험 고침(0.3.1) |

---

## 9. 시험 기준 (계약 → 고정하는 시험)

KOS 는 지금 시험 방식(`tests/fake_kos.py` 가짜 전송)으로 흉내 낸다. 시험 이름 · 데이터의 사람 이름 · 이메일은 지어낸 값(`<이름>` 꼴 · `a@example.com`)만 쓴다.

| # | 계약 | 시험(새 파일 `tests/test_ext_*.py`) | 근거 |
|---|---|---|---|
| T1 | 메뉴 표 9 · `raw` 원문 보존 | 가짜 KOS 응답(deprecated 칸 · 빈 배열 · 다국어 포함) → 각 표 행 수 · `raw` 를 `json.loads` 하면 원본과 같다(상품 `raw` 에 `options` 없음 · 옵션 `raw` 에 `compositions` 없음) | D-03 · D-04 |
| T2 | 동기화 순서 · ③ 나눠 부르기 | SINGLE N+1 개 → `getProductOptions` 2번 · `medical_service_kos_id` 채움. ③ 응답에서 빠진 옵션은 이전 값 그대로 | D-05 · 코디 Q4 |
| T3 | 「없음」 · 되살림 | 두 번째 동기화에서 상품 1 · 구성 1 · 타겟 국가 1 이 빠짐 → `present = 0`(행 남음) → 세 번째에 다시 나오면 `present = 1` | D-07 |
| T4 | 작업 실패 = 이전 값 | `getProducts` 5xx · `data` 가 배열 아님 → 메뉴 표 그대로 · 다른 작업은 반영 · `sync_state("menu").last_error` 에 이름 · 로그에 본문 · 키 없음 | §4.1 · 코드 규약 |
| T5 | 마스터 루프에 얹힘 | `master_once()` 1번 = 메뉴 작업 호출 · 서버 시작 1회 · 조회 시간 밖에서도 돈다 | D-06 |
| T6 | 메뉴 응답 깊이 · 칸 | SINGLE · GROUP · CONSULTATION 한 개씩 → 칸 목록이 §6.3 과 같다(내지 않는 칸 0 — 응답 JSON 에 `medicalService` · `medicineAndMachines` · `suppliedAmount` · `vatAmount` · `additional` · `displayChannels` · `badges` · `caution` 키가 없다). CONSULTATION 가격 · 횟수 · 단위 · 시술 null · `syncedAt` = 마지막 성공 시각(`+09:00`) · 성공 전 null · **성공 → 다음 바퀴에서 작업 하나 실패 → `syncedAt` 은 앞 성공 시각 그대로**(null 아님 · `last_error` 만 바뀜) | D-27 ~ D-30 · D-36 · 코디 Q5 |
| T7 | 메뉴 「지금 있는 것만」 | `present = 0` · `closed` · `deleted` · `opened:false` 행이 응답에 없음 · 위 층이 빠지면 아래 층도 없음 | D-07 |
| T8 | 정가 = 부가세 별도 · 칸 이름 | `listPriceExVat.value` = KOS `price.amount.value` · 구성 합 = 옵션 | D-09 · D-30 |
| T9 | 이름 검색 한 페이지 · 상한 · 중복 제거 | `get-visitors` 본문 `indexOfPage` 0 · `countInPage` 1000 · 조회 1건당 **1번**(두 번째 페이지 0번) · 같은 KOS id 가 두 번 오면 1명(→ `200`, `409` 아님) · `count` 1001 → `404 customer_not_found`(KOS 호출 1번 · 시술권 조회 0번 · 본문이 T13 「없음」과 바이트까지 같음) | D-16 · D-21 |
| T10 | 이름 다듬기 | 요청 `"  <이름>  "` → KOS 본문 `visitorName` 은 앞뒤 공백 없음 · 가운데 공백 그대로 · 검색 1번(다시 검색 0) | D-17 |
| T11 | 이메일 비교 | 대소문자 · 앞뒤 공백만 다른 이메일 = 맞음 · KOS 쪽 키 없음 · 빈 문자열 = 후보 아님 · `@` 없는 값도 같으면 맞음 | D-18 |
| T12 | 이름 정확 일치 · 갈래 0 · 1 · 2+ | 부분 일치만 맞는 이름(KOS `name` 이 입력을 포함만 함) + 맞는 이메일 → `404` · 발음명(`phoneticName`)만 같음 → `200` · 대소문자만 다름 → `200` · 공백(가운데 포함)만 다름 → **KOS 가 그 고객을 돌려준 경우(가짜 KOS 응답을 직접 지정)에만** `200` · 가운데 공백이 다른 입력 → KOS 0건(지금 `tests/fake_kos.py` 검색 규칙 그대로 — 공백 그대로 · 부분 일치. 이 규칙은 고치지 않는다) → `404` · 0명 → `404 customer_not_found` · 2명 → `409 customer_ambiguous`(본문에 이름 · id · 수 없음) | D-19 · D-20 |
| T13 | 「없음」 하나 | 이름 틀림 · 부분 일치만 맞는 이름 · 이메일 틀림 · email 빈 고객 · 고객 없음 · `count` > 1000 여섯 경우의 응답 본문 · 상태가 **바이트까지 같다** | D-16 · D-19 · D-21 · D-22 |
| T14 | 시술권 · 「없음」 구분 | 묶음 `{}` → `200 tickets: []` · 고객 없음 → `404` · 시술권 조회 실패 → `502`(빈 배열 아님) | D-12 · D-14 |
| T15 | 시술권 한 줄 | 묶음 2(SINGLE · GROUP 세트 둘 · USED · `IN_USE` 섞임) → `remainingCount`(`AVAILABLE` 만 · `IN_USE` 안 셈) · `totalCount` · `purchasedDate`(KST · 가장 이른 값) · `bundlePrice` = KOS `price` · 응답 JSON 에 `purchasePrice` · `VatIncluded` 가 들어간 키 없음 · 메뉴에 없는 `optionId` 도 그대로 · 옵션 이름은 메뉴 값이 아니라 묶음 값 | D-08 · D-31 |
| T16 | 고객 응답 칸 | 키 집합 = `{customerId, name, isNew, lastVisitDate}` · KOS id · 전화 · 생년월일 · 국적 · 여권 · 차트번호 · 이메일 없음 · `lastVisitedDateTimeUtc` 없으면 null | D-13 · D-31 · 코디 Q2 |
| T17 | 예약 1명 · 행위자 | 기존 고객 갈래 · KOS `reserve` 본문의 그룹 = env 그룹 · 구역 = 기본 구역 규칙 · 담당자 = 시스템 계정 · `event_log.resv_create` actor = `ext:linky` 문자열(가짜 `Account` 없음) · KOS 거절 때 `kos_rejected` actor 도 `ext:linky` | D-32 · D-33 · §3.5 |
| T18 | 예약 0명 | `find-duplicated-visitor` → `create-visitor`(본문에 `name` · `email`) → `reserve` · 응답 `customerId` = 새 행 | D-22 · D-32 |
| T19 | 예약 2명 · 중복 검사 걸림 | 둘 다 `409 customer_ambiguous` · `reserve` 0번 · 응답에 `candidate` 없음 · 외부 응답 어디에도 `duplicated_visitor` 없음 | D-20 · 코디 Q1 |
| T20 | 예약 그룹 설정 | env 빔 · 그룹 `present = 0` · 그룹에 켜진 구역 0 → 셋 다 `503 ext_not_configured`(`400 invalid_request` 아님) · KOS 호출 0번 | D-33 · 코디 Q3 |
| T21 | 예약 정원 · KOS 실패 | `slot_full` · `kos_rejected` · `kos_unavailable` 이 지금 규칙 그대로 | D-33 |
| T22 | 예약 요청 칸 | `groupId` · `zoneId` · `assigneeStaffId` 를 보내면 `400 invalid_request` · `start` 형식 오류 400 · 빈 이름 · 이메일 400 | D-32 · D-33 |
| T23 | 키 인증 | 키 없음 · 빈 값 · 틀림 · 꺼진 연동처 · Bearer 만 → `401 ext_unauthorized` · 맞는 키 = 그 연동처(`ext_call.client`) | D-10 · D-23 |
| T24 | 직원 API 분리 | 직원 경로에 `X-Api-Key` 만 → `401 unauthorized` · 외부 경로에 Bearer + 키 → 외부 권한(직원 경로를 대신 열지 못함) | D-10 |
| T25 | 검사 순서 | 키 틀림 + **칸** 틀림(필수 빠짐 · 모르는 키) → 401 · 한도 초과 + 칸 틀림 → 429 · 키 틀림 + JSON 이 아닌 본문 → 400 · 키 없음 + 없는 경로 → 404 · IP 차단 중 + 맞는 키 → 429 | §6.1 |
| T26 | 호출 제한 | 같은 키 60번 200 → 61번째 429(세지 않음) → 시계를 60초 넘기면 다시 200 · 다른 연동처 키는 따로 셈 · 401 은 키당 카운터에 안 셈 | D-25 · D-34 |
| T27 | 기록 | 성공 · 401 · 429 · 404 · 409 · 502 마다 `ext_call` 1줄(`client` · `endpoint` · `status` · `outcome`) · 맞는 키 + 없는 경로 → `client` null · `endpoint` = `"<METHOD> (unknown)"` · **경로에 이메일 꼴 문자열(`/api/ext/customers/a@example.com`) → 표 어디에도 그 문자열 없음** · 키 없는 401 을 같은 IP 에서 5번 → 1분 안 1줄 · 시계를 60초 넘기면 다시 1줄 · 키 없는 깨진 본문 400 · 405 도 같은 IP 에서 5번 → 1분 안 1줄(`client` null) · 테이블 전체 · 앱 로그(caplog)에 요청 이름 · 이메일 · 키 · IP 문자열 0 | D-24 · §3.4 |
| T28 | 캐시 헤더 | `/api/ext` 응답(오류 포함) `Cache-Control: no-store` | §6.1 |
| T29 | Swagger | `외부 연동` tag · `ExtApiKey` scheme · 외부 operation 3(0.3.0: **6** — 새 셋 설명에 오늘 겹침 문장 · 가능 시간대 규칙 문장) = `security [{ExtApiKey: []}]` · Bearer 아님 · 401 표에 `ext_unauthorized`(`unauthorized` 아님) · 그 줄이 `X-Api-Key` 를 말함 · 503 표 머리 = `STATUS_TEXT[503]` · 예약 설명에 D-35 문장 · 앱 설명 외부 절 첫 줄 = email 없는 고객 문장 · **(0.3.1) 여섯 operation 의 429 줄이 「외부 경로 전부 합산」을 말하고 「세 엔드포인트」 · 「세 경로」가 없음 · 앱 설명에도 「세 경로」 없음** · **(0.3.1) parameters = `X-Api-Key`(header) + availability `date`(query)만**(§8 시험 고침) · `test_openapi_docs.py` 전부 통과(개수 단언 고침 뒤) | §8 · D-35 · 문서 검수 add1 W3 · W4 |
| T30 | 직원 API 회귀 | 기존 시험 전부 통과 — 특히 `test_resv_write.py`(예약 생성) · `test_resv_*` · 접수 시험 · `test_openapi_docs.py`. 직원 예약 생성 · 접수의 `event_log.actor` = 그 직원 `login_id`(지금과 같음) | O11 · §3.5 |
| T31 | 키 없는 거절 IP 제한 | 같은 IP 에서 키 없는 401 · 없는 경로 404 · 깨진 본문 400 · 405(있는 경로에 틀린 메서드)를 섞어 합쳐 10번 → 11번째 요청은 맞는 키여도 `429 too_many_requests`(세지 않음) · 시계를 60초 넘기면 다시 열림 · 다른 IP 는 영향 없음 · `CF-Connecting-IP` 가 있으면 그 값으로 셈 · IP 문자열이 `ext_call` · 로그에 0 | §7.3 · D-24 |
| T32 | 가능 시간대 후보 · 남은 자리(0.3.0) | 기본 그룹(간격 30 · 운영 10:00 ~ 20:00 · 쉬는 시간 13:00 ~ 14:00 · 켜진 구역 둘) · 내일 날짜 → 후보 = 10:00 ~ 12:30 · 14:00 ~ 19:30(13:00 · 13:30 · 20:00 없음) · 한 시각에 구역 A 정원 3 · 예약 1, 구역 B 정원 3 · 예약 3 → `remainingSeats` 2 · 구역 B 행 없음 → A 몫만 · 두 구역 다 행 없음(또는 `capacity` null) → 그 시각 없음 · 두 구역 다 참 → 그 시각 없음 · 휴무 요일 → `slots: []` · 응답 키 = `{date, intervalMinutes, slots}` · `slots[]` 키 = `{start, remainingSeats}` · 15분 그룹이면 간격 15 · `start` 가 `+09:00` | DEC-011 D-02 · D-11 |
| T33 | 오늘 지난 시각 | 시계를 오늘 14:10 으로 둠 → 14:00 이하 시각 없음 · 14:30 부터 · 시계를 정확히 14:30 으로 두면 14:30 도 없음 | DEC-011 D-02 |
| T34 | 날짜 검사 | `date` 없음 → `400 invalid_request` · message 가 `query.date:` 로 시작 · `date=`(빈 문자열) · `2026-1-5` · `20261105` · 어제 · 오늘 + 91일 → `400 invalid_request` · message 가 `date:` 로 시작 · 모두 KOS 호출 0 · 오늘 · 오늘 + 90일 → 200 | DEC-011 D-08 |
| T35 | 가능 시간대 설정 | env 빔 · 그룹 `present = 0` · 켜진 구역 0 → `503 ext_not_configured` · KOS 호출 0 | DEC-011 D-09 |
| T36 | 슬롯 새로 읽기 | 요청 1번 = `get-reservation-slots-by-groups` 1번(본문 그룹 = 사본 `present` 그룹 전부 · 그날 KST 하루) · 하루 예약 · 공지 · 금액 조회 0번 · 사본 그날 행이 응답 값으로 바뀜 · KOS 5xx · 4xx · 401 · `data` 배열 아님 → `502 kos_unavailable` · 사본 그대로 · **(0.3.1) runtime 없음(KOS 설정 없음) → `502` · KOS 호출 0** | DEC-011 D-12 · 문서 검수 add1 W6 |
| T37 | 예약과 같은 규칙 | ① 사본에 「참」이 남은 시각을 KOS 가 「자리 있음」으로 바꾼 뒤 가능 시간대 → 그 시각이 나옴 → 곧바로 외부 예약(§6.5) → `slot_full` 아님 ② 목록의 모든 시각에 외부 예약 → `slot_full` 0 ③ 목록에 없는(모든 구역 참) 시각으로 예약 → `409 slot_full` | DEC-011 D-02 |
| T38 | 과거 시술 | 일정 55건(지난 53 · 앞으로 2 · 시작 없는 1 포함) → 지난 것 중 최신 50건 · 시작 내림차순 · `result` = `COMPLETED` → completed · `NO_SHOW` → noshow · `CANCELED` → canceled · `RESERVED` · 값 없음 → other · `procedures` = 작업 title(「방 배정」 ETCETERA 뺌 · 다른 ETCETERA 는 남음) · 응답 JSON 에 `reservationMemo` · `consultationMemo` · `doctors` · `resultRaw` · `zoneTitle` · `groupTitle` 키 없음 · 지난 일정 없음 → `visits: []` · **(0.3.1) `deleted: true` 지난 일정 → 나오지 않음** | DEC-011 D-03 · D-10 · D-15 |
| T39 | 과거 시술 · 예약 내역의 고객 갈래 | 0명 · 이름 틀림 · 이메일 틀림 · `count` > 1000 → `404` 본문 · 상태가 조회(§6.4) 404 와 **바이트까지 같음** · 2명 → `409 customer_ambiguous` · 404 · 409 이면 `get-schedules-by-visitor` 0번 · 일정 읽기 5xx · `data` 가 있으면서 배열 아님 → `502`(빈 목록 아님) · **(0.3.1) 일정 응답 `{}`(`data` 키 없음) · `{"data": []}` → `200` · `visits: []` · `reservations: []`** · **(0.3.1) 이름 검색 5xx → `502` · 일정 읽기 0번**(두 경로 각각 1줄) · 고객 · 예약 사본 행 수 그대로 | DEC-011 D-05 · D-12 · D-13 · 문서 검수 add1 W1 · W6 |
| T40 | 예약 내역 | 오늘 0시 이후 일정만 · 시작 오름차순 · 취소 · 부도 포함 · `state` = 2계층 주 상태(`RECEPTION` → reception · `PROCEDURE_DONE` → home · `CANCELED` → canceled · 모르는 단계 → reserved) · 사본에 있는 일정 = 그 ccc id · 없는 일정 = null(사본 행 늘지 않음) · 외부 예약(§6.5)으로 만든 예약 → 내역에 그 `reservationId` 그대로 · `end` = 첫 묶음 끝 · 묶음 없음 → null · 응답 키 = `{reservationId, date, start, end, state}` · 지난 일정만 있는 고객 → `reservations: []` · **(0.3.1) `deleted: true` 앞으로 일정 → 나오지 않음** | DEC-011 D-04 · D-13 · D-15 |
| T41 | 오늘 겹침 | 오늘 09:00 일정 · 시계 오늘 12:00 → 과거 시술과 예약 내역 둘 다에 나옴 | DEC-011 D-14 |
| T42 | 요청 칸 | 과거 시술 · 예약 내역 본문에 모르는 키 · 빈 `name` · `email` → `400` · 가능 시간대에 `name` 질의를 붙여도 쓰이지 않음(무시 · `ext_call.endpoint` 는 경로 틀만) | DEC-011 D-06 |
| T43 | KOS 비용 | §6.9 표 그대로 — 가능 시간대 1 · 과거 시술 2 · 예약 내역 2(404 · 409 이면 1) · 가짜 KOS 호출 수로 단언 | DEC-011 D-12 · §6.9 |
| T44 | 공유 규칙(새 세 경로) | 키 없음 → `401 ext_unauthorized` · 응답(오류 포함) `Cache-Control: no-store` · `ext_call.endpoint` = `GET /api/ext/availability` · `POST /api/ext/customers/visits` · `POST /api/ext/customers/reservations` · 키당 제한을 여섯 경로가 함께 셈(메뉴 30 + 가능 시간대 30 → 61번째 과거 시술 429) · 표 · 로그에 이름 · 이메일 0 · **(0.3.1) `POST /api/ext/availability` → `405 http_error` · 새 세 operation 의 Swagger 응답 표에 공통 줄(401 · 429 · 405 · 500)이 다 붙음**(`responses=errors(*COMMON, …)`) | DEC-011 D-01 · DEC-010 D-24 · D-34 · 문서 검수 add1 W6 |
| T45 | 경계 시각(0.3.2) | ① 시계 = 일정 시작 정각(오늘 12:00 일정 · 시계 12:00) → 과거 시술에 **없음**(「지금보다 앞」이 아님) · 예약 내역에 **있음** ② 오늘 00:00 정각 시작 일정 → 예약 내역에 **있음**(「0시와 같거나 뒤」) | DEC-011 D-03 · D-04 · 코드 검수 add1 r1 N2 |
| T46 | 일정 읽기 4xx · 401(0.3.2) | `get-schedules-by-visitor` 가 400 · 401 → 과거 시술 · 예약 내역 둘 다 `502 kos_unavailable`(빈 목록 아님 · 경로마다 1줄) | §6.7 2 · 코드 검수 add1 r1 N2 |
| T47 | 일정 원소 모양 오류(0.3.2 · 0.3.3 고침) | 일정 원소 하나의 `reservation` 이 문자열 · `occupiedResources[].reservationTime` 이 문자열 → 과거 시술 · 예약 내역 둘 다 `502 kos_unavailable`(500 아님) · **작업 `title` 이 숫자 → 과거 시술만 `502`**(예약 내역은 작업을 보지 않으므로 `200`) · 본문은 공통 502 본문과 같고 KOS 원문 문자열 0. 로그에 원문 0 은 **코드 검수 재현으로 확인**했다(로그에 예외 종류만 · 시험 단언은 없음 — `caplog` 단언을 넣는 것은 선택) | DEC-011 D-16 · 코드 검수 add1 r1 N1 · r2 M1 |
| T48 | lookup `customerId` 갈래(0.4.0) | `{customerId}` → 내부 `get-visitor` 1 · `get-visitors` 0 · `200` · 고객 칸 키 집합이 이름 갈래와 같음 · 사본 덮어씀 · 사본에 없는 id → `404 customer_not_found` 본문이 이름 갈래 404 와 **바이트까지 같음** · KOS 0 · KOS `get-visitor` 404 → 같은 404 · (0.4.4) KOS 400 + `errorProperties` `id NotFound` → 같은 404(바이트 같음) · 그 밖 400 → 502 · 5xx · `data` 객체 아님 → `502` | DEC-012 D-02 · D-08 ① · §6.4 |
| T49 | lookup 요청 갈래 검사(0.4.0) | `customerId` + `name` · `name` 만 · `email` 만 · `{}` · `customerId` 0 · -1 · `"1"`(문자열) → `400 invalid_request` · (0.4.4 · DEC-012 D-45) 명시 `null` 은 「없음」이다 — 섞임 · 한쪽만 판정은 **값이 있는 칸** 기준(`{customerId: 1, name: null, email: null}` → `customerId` 갈래 `200` · `{name, email, customerId: null}` → 이름 갈래 `200` · `{customerId: null}` → 빈 요청 400) · (0.4.1) 갈래 오류(섞임 · 한쪽만 · `{}`)의 message 는 `body: ` 로 시작 · 기존 `{name, email}` 요청은 그대로 `200` · Swagger 요청 스키마의 `required` 에 `name` · `email` 없음 | DEC-012 D-03 · D-33 · §6.4 · 검수 r1 W12 |
| T50 | 내부 시술권 · `inUseCount`(0.4.0) | 내부 `ticket/v1/queries/get-ticket-bundles` 본문 = `{visitorId, sort: {by: "ticket.createdDateTimeUtc", order: 2}}` · 공개 시술권 경로 0번 · `inUseCount` = `IN_USE` 장수 · `remainingCount` 는 `AVAILABLE` 만 · `totalCount` 는 상태 무관 · **`IN_USE` 만 남은 묶음 → 나옴**(`remainingCount` 0) · `USED` · `CANCELED` 만인 묶음 → 안 나옴 · `tickets[]` 키 집합 = 0.3.x 키 + `inUseCount`(바뀐 키 0) · 만료일 키 없음 · (0.4.5 · DEC-012 D-46) **거르기 먼저**: `price = {currency}` 만인(`value` 없음) `USED` · `CANCELED` 만 묶음이 섞여도 `200` · 그 묶음은 안 나옴 · 걸러진 묶음의 `price` 가 없어도 `200` · **0 값**: `price = {currency}` 만인 산 묶음 → `bundlePrice.value = 0` · `200` · 산 묶음의 `price` 없음 · 문자열 `value` → `502 kos_unavailable` 그대로 · 가짜 내부 시술권 기본 응답에 `value` 없는 다 쓴 묶음 1개를 섞어 둔다(실물 모양 · 2026-11-16 로컬 e2e · 데모 고객 1명의 묶음 12 중 4) | DEC-012 D-03 · D-07 · D-08 ② · D-46 · §4.3 |
| T51 | 선불카드(0.4.0) | 공개 선불카드 본문 `{visitorId, available: true}` · 칸 = `{title, issuedDate, expiresAt, balance{remaining, total}, point{remaining, total}}` · 카드 id · `ownerId` · `description` 키 없음 · `balance` · `point` 의 `remaining` · `total` = `{value: int, currency}` · `{}` · `[]` → `prepaidCards: []` · `partialErrors: []` · (0.4.1) 실패 · `data` 배열 아님 → **`200`** · `prepaidCards: null`(빈 배열 아님) · `partialErrors: ["prepaidCards"]` · 고객 · 시술권 칸은 그대로 · `ext_view` 1줄 · 시술권 실패는 그대로 `502` · 시술권과 동시에 부름 | DEC-012 D-08 ③ · D-36 · §4.4 · 검수 r1 W3 · W4 |
| T52 | lookup KOS 비용 · 열람 기록(0.4.0) | 이름 갈래 3 · `customerId` 갈래 3 · 404(이름) 1 · 404(사본 없음) 0 · 200 이면 `event_log` `ext_view` 1줄(`client` · `staffId` = 헤더 값 · `customerId` · `reservationId` null · `path` · **`actor` = `ext:<연동처>:<직원 id>`**) · 헤더 없음 → `staffId` null · `actor` = `ext:<연동처>` · (0.4.1) **꼴이 틀린 헤더(65자 · 한글 · `@`) → `200` · `staffId` null · `actor` = `ext:<연동처>`(400 아님)** · 404 · 409 · 502 → `ext_view` 0 · `ext_call` 에 직원 id · 고객 id 문자열 0 | DEC-012 D-18 · §6.4 · §6.10 |
| T53 | 열람 헤더 꼴(0.4.0 · 0.4.1 고침) | **새 경로 넷**(상세 · 쓰기 셋 각각): 65자 · 가운데 공백 · 한글 · `:` · `@` → `400 invalid_request`(message `header.X-Ext-Staff-Id:` 로 시작 · KOS 0) · 공백만 → 없는 것으로 봄(`ext:<연동처>`) · 64자 · `a.b_c-d` → 받음. **lookup** 은 같은 틀린 값에 `200`(T52). ~~헤더를 쓰지 않는 경로(메뉴)도 꼴 검사만 함~~ | DEC-012 D-18 · D-37 · §6.10 · 검수 r1 F2 |
| T54 | board 줄(0.4.0) | 한 예약에 묶음 둘 → **한 줄**(`start` = 첫 묶음 · `end` = 가장 늦은 끝) · 응답 키 집합 = §6.11 표 · 취소 · 부도 · 귀가 예약도 나옴 · 귀가 예약 `receptionAt` 있음 · 접수 전 null · `counselor` = 사본 희망 상담사 → `{staffId, name}` · `roomTitle` = 가장 늦게 배정된 방 · 차례 = 시작 → id | DEC-012 D-09 · §6.11 |
| T55 | board 상담 판정(0.4.0) | 지금 상담 대기 → `true` · 접수 이벤트 `endStep = CONSULTATION_WAITING` → `true` · `consultation_add` → `true` · KOS `consultationRequired = true` 만 → `false` · (0.4.1) `consultation_add` 가 있는데 지금 취소 · 부도 · 예약 상태 → `false`(`after` 아님) · **같은 데이터로 직원 상세의 `flow.consultation` 유무와 board `consultation` 이 같다**(판정 함수 하나 · `after` 문 포함 · 취소 예약 포함) · (0.4.4 · W5) 다른 날 예약의 `reception` · `consultation_add` 줄이 많아도 board 결과 같음 · board 가 읽는 `event_log` 는 그날 예약 id 것만(쿼리에 예약 id 조건) | DEC-012 D-09 · D-45 · §6.11 3 · 검수 r1 W6 · 코드 검수 r1 W5 |
| T56 | board 신선도 · 실패(0.4.0) | 10초 안 두 번 → 날짜 조회 1번 · 날짜 조회 5xx → `200` · 사본 그대로 · `sync.lastError` 있음 · runtime 없음 → `200` · `sync.lastError` = KOS 설정 없음 문구 | DEC-012 D-23 · §6.11 1 |
| T57 | 처음 상담 대기 시각(0.4.0 · 0.4.2 · 0.4.3 고침) | (0.4.3 · KOS0 ①) **가짜 이력 응답 모양** = `data[]` 원소 6키 `{scheduleId, version, eventType, payload, raisedDateTimeUtc, initiator{type, id?}}` · `eventType` 은 전체 이름(`protos.schedule.event.FlowStepChanged` · 그 밖 이벤트도 섞음 — 예 `protos.schedule.consultation.events.<이름>`) · `payload` = JSON 문자열 `{flowStep, raisedDateTimeUtc}` · `flowStep` = 문자열 enum 이름 · 원소 차례 섞임(`version` · 시각 순 아님) · 같은 단계 반복 = 원소 둘 · 원소 시각 소수 2자리 · 3자리 섞음 → 원소 `raisedDateTimeUtc` 최솟값(payload 안 값 아님) · 짧은 이름 `eventType = "FlowStepChanged"` 로만 준 원소도 끝 조각 일치로 잡힘 · 이력에 `FlowStepChanged`(상담 대기) 둘 → 이른 값 · `first_at` 행 저장(`source = kos_event_log`) → 그 뒤 board 에서 그 일정 이력 0번(귀가해도 0번) · **대상 = `after` 인 줄 전부**: 예약 · 취소 · 부도 줄은 이력 0번 · `consultation = false` 인 접수 뒤 줄도 부름 → 찾으면 시각 있음 + `consultation false` · **ⓐ 처음 봄** 1번 → 못 찾음 → `first_at` null 시도 행 · `last_failed 0` · **못 찾음 뒤 사건 없이**(단계 그대로) board 를 여러 번(시계를 30분 넘겨도) → 그 일정 이력 0번 · `partialErrors = []`(D-39) · **ⓑ 대기 새로 봄**: 사본 단계가 상담 대기로 바뀜 → 다음 board 1번(`wait_called 1`) → 같은 대기 구간 board 여러 번 → 0번 · 대기 아닌 단계를 본 뒤 다시 대기(재진입) → 1번 더 · 처음 봄 때 이미 대기면 그 1번이 겸함(대기 몫 추가 0) · (0.4.4 · Q1) **처음 봄 = 이미 귀가**: 행 없는 귀가 일정 → 첫 board 1번(`final_tried 1` · `wait_called` 그대로) → 그 뒤 board 여러 번 → 0번(하루 1번) · **ⓒ 귀가**: 못 찾음 일정이 귀가 → 1번(`final_tried 1`) → 그 뒤 board 여러 번 → 0번 · 귀가 뒤 1번에서 찾으면 값 · 굳음 · (D-41) 귀가 뒤 1번이 5xx → 5분 뒤 재시도(`retries 1`) · 귀가 사건으로는 다시 안 부름 · **ⓓ 실패**(이력 5xx · 403 · `data` 배열 아님 · `payload` JSON 깨짐) → 그 줄 null · `partialErrors = ["consultationHistory"]` · `200` · `last_failed 1` · 5분 안 board → 0번 · 5분 뒤 → 재시도 1번(`retries 1`) · 계속 실패 → 재시도 3번에서 멈춤(그 뒤 board 여러 번 · 시계를 넘겨도 0번 · `partialErrors` 남음) · **요청당 상한**: 부를 줄 15 → 첫 board 이력 10번(ⓐ → ⓑ → ⓒ → ⓓ → 줄 차례) · 나머지 5줄 null · `partialErrors` 에 `consultationHistory` · 두 번째 board → 남은 5줄만 · (D-39 넓힘) 미뤄진 5줄이 모두 「대기를 새로 봄」(행 있음 · 못 찾음) 줄이어도 첫 응답 `partialErrors` 에 `consultationHistory` · **겹친 요청**(N2): board 두 요청을 겹쳐 보냄(첫 요청의 이력 호출이 끝나기 전에 둘째 요청) → 같은 일정 이력 **1번** · 둘째 응답의 그 줄 null + `partialErrors` · 시도 예약 행이 KOS 호출보다 먼저 적힘 · **어제 일정**: 오늘 board 에 없음 · 이력 0번 · **합**: 이력이 계속 실패해도 board 를 1분에 60번 30분 동안 불러 일정마다 이력 ≤ 1 + 3 | DEC-012 D-16 · D-23 · D-38 · D-39 · D-40 · D-41 · §3.6 · §6.11 4 · 검수 r1 F1 · F3 · W1 · 검수 r2 N2 · N3 |
| T58 | board 비용 · 경로 차례(0.4.0) | 사본 신선 + 대상 줄 모두 굳음(`first_at` 있음) 또는 사건 없음(ⓐ ~ ⓓ 가 모두 거짓 — 못 찾음 뒤 단계 그대로 · 실패 뒤 5분 안 · 재시도 3번 다 씀 · 귀가 뒤 1번 이미 부름) → KOS 0번(0.4.2 · 검수 r3 M1) · `GET /api/ext/reservations/board` 가 `{reservationId}` 경로의 400 으로 가지 않음 | §6.11 · §6.9 |
| T59 | 예약 상세 칸(0.4.0) | 응답 키 집합 = §6.12 표 · `customer.language` · `age` · 고객 유입 · 예약 유입 · 희망 상담사 · 희망 의사 · `requestedProcedures` `OPTION` · `TICKET` 각 칸(나머지 null) · 빈 배열 · (0.4.1) `reservation.orderMemo` = 일정 상세 `orderMemo` · `reservation.consultationMemo` = `consultation.consultationMemo`(빈 문자열 그대로 · `consultation` 없음 → null · KOS 호출 수 그대로 5) · 이전 방문에 **`reservationMemo` · `consultationMemo` · 의사 이름 있음** · `counselors[]`(`consultations` 둘 · 같은 KOS id 한 번 · 비면 `consultation.counselor` · 둘 다 없으면 `[]`) · 같은 날 일정 뺌 · 응답 JSON 에 전화 · 이메일 · 여권 · `remark` · `content` · `settlement` · `can` 키 없음 | DEC-012 D-02 · D-10 · §6.12 |
| T60 | 예약 상세 부분 실패(0.4.0) | 일정 상세 5xx → `200` · `requestedProcedures` · `requestedDoctor` · (0.4.1) `orderMemo` · `consultationMemo` null · `partialErrors` 에 `schedule` · `get-visitor` 실패 → `language` · `age` · 고객 유입 null · `visitor` · 문진 실패 → `health.state = error` · `questionnaire` · 이전 방문 실패 → `previousVisits = null`(빈 배열 아님) · `previousVisits` | DEC-012 D-23 · §6.12 3 · 4 |
| T61 | 예약 상세 404 · 비용 · 열람(0.4.0) | 사본에 없음 → `404 reservation_not_found`(KOS 0) · KOS 일정 404 → `404 reservation_gone` · 정수 아님 → 400 · runtime 없음 → 502 · 성공 = KOS 5번(수납 금액 0번 — 귀가 · 수납 id 있는 예약으로도 · 날짜 조회 0번) · `ext_view` 1줄(`reservationId` · `customerId` · `staffId` · `actor` = `ext:<연동처>[:<직원 id>]`) · 직원 상세(귀가 · 수납 id)는 지금처럼 수납 금액을 부름(`amount` 기본값) | DEC-012 D-18 · D-37 · §6.12 · 검수 r1 W7 · W8 |
| T62 | 고객 언어(0.4.0) | 다시 읽기 1 → 쓰기 본문 = 다시 읽은 17키 중 있는 키 전부 + 바꾼 `language` · 같은 값 → 쓰기 0 · `event_log` `visitor_personal`(`fields: ["language"]`) actor = `ext:charty:<직원 id>` · 헤더 없음 → `ext:charty` · 사본 없음 → `404 customer_not_found`(lookup 404 와 바이트 같음 · KOS 0) · KOS 4xx → `409 kos_rejected` + `kos_rejected` 줄(같은 actor) · 빈 문자열 → 비움으로 보냄 · null → 400 | DEC-012 D-04 · D-11 · D-19 · §6.13 |
| T63 | 오더 메모(0.4.0) | 내부 `change-order-memo` 본문 `{scheduleId, orderMemo}` · 성공 → `event_log` `order_memo`(`{reservationId, length}` · 글 원문 0) · 시술 현황 `visit` 행이 있으면 `order_memo` 갱신(다른 칸 그대로) · 없으면 사본 쓰기 0 · (0.4.1) **visit 행 수 그대로**(없는 예약에 써도 새 행 0) · 날짜 캐시 비움 · 같은 글을 두 번 → KOS 2번 · 예약 사본 `memo`(예약 메모) 그대로 · 404 · 409 · 502 | DEC-012 D-04 · D-12 · §6.14 |
| T64 | 상담 메모(0.4.0 · 0.4.6 고침) | 공개 `update-schedule-consultation-info` 본문 `{scheduleId, consultationMemo}` · `event_log` `consultation_memo`(`{reservationId, length}`) · 404 · 409 · 502 · (0.4.6 · D-47) `""` · `"  "`(공백만) → `400 invalid_request` · message 가 `body.consultationMemo: ` 로 시작 · KOS 호출 0 · `event_log` 0 · 0.4.0 판의 「빈 값 = 비움」 상담 메모 시험이 있으면 이 단언으로 바꾼다(오더 메모 T63 의 빈 값 = 비움은 그대로) | DEC-012 D-04 · D-13 · D-47 · §6.15 |
| T65 | 쓰기 = KOS 먼저(0.4.0) | 세 쓰기 모두 KOS 실패 → 성공 `event_log` 줄 0 · 사본 변경 0 · `kos_rejected` 1줄 · 응답 = KOS 오류 code 그대로 | DEC-012 D-04 · §6.13 ~ §6.15 |
| T66 | 병원 정보(0.4.0) | 응답 키 = §6.16 표의 「냄」 칸만(안 내는 10칸 키 0) · 빈 문자열 → null · 주소 셋 다 빔 → `address` null · `operatingHours` = `timetable_of` 결과(KST `HH:MM`) · (0.4.3) `daysOff` 원소 키 집합 = `{startDate, endDate}` 뿐(`id` · `name` 키 0) · 가짜 KOS 원소 KST 0시 ~ 다음날 KST 0시(UTC `…T15:00:00Z` 꼴) → `startDate = endDate` · 사흘 휴무 → 한 원소 · `endDate` = 끝 직전 날짜 · ~~KOS 원소 그대로~~ · 국적 · 언어 · 웹사이트 · `translsMap` 키 0 · 세 호출 동시 · 휴무 본문 기간 = 오늘 0시 ~ 90일 끝 · 하나라도 5xx → `502` · runtime 없음 → `502` · `clinicId` = 1 | DEC-012 D-14 · D-20 · D-22 · D-24 ~ D-28 · D-43 · §6.16 · 검수 r1 W11 |
| T67 | 직원 목록(0.4.0) | `clinicId` 다름 → `404 clinic_not_found`(KOS 0) · 정수 아님 → 400 · 시스템 계정 · 제외 목록 계정 빠짐 · 비활성 포함(`active: false`) · `staffId` = 사본 id · 사본에 없는 계정 → `staffId` null · `roleTags` `[]` · `roleTags` = 사본 문자열 태그 · `roleName` = 내부 값 · ~~이메일 · `realName` · KOS id 키 0~~ · (0.4.7 · DEC-012 D-48) **원소 키 집합 = §6.17 표의 여덟**(`staffId` · `name` · `roleName` · `roleTags` · `active` · `email` · `realName` · `kosAccountId`) · `email` = 내부 `email` · `realName` = 내부 `realName`(`name` 은 내부 `name` 그대로 — 둘이 다른 값인 가짜 원소로 본다) · `kosAccountId` = 내부 `id` 문자열(사본에 없는 계정도 값이 있다 · `staffId` null 과 함께) · `email` · `realName` 이 `null` → null · 빈 문자열 → null · 칸 없음 → null(가짜 원소 세 갈래) · `userId` · `licenseNumber` · `mfaMethods` · `roleId` 는 여전히 키 0 · KOS 호출 1 그대로 · `ext_call` 행과 앱 로그에 세 값 0 · 가짜 KOS 원소의 세 칸은 **지어낸 값만**(`…@example.com` · `<실명…>` 꼴) · 실패 · `data` 배열 아님 → 502 · (0.4.7 · 검수 r1 W4) `id` 없는 원소가 하나라도 있음 → 502 | DEC-012 D-06 · D-15 · D-21 · D-29 · D-48 · §6.17 |
| T68 | 새 일곱 공유 규칙(0.4.0) | 키 없음 → `401 ext_unauthorized` · 응답(오류 포함) `no-store` · `ext_call.endpoint` = 경로 틀(예 `GET /api/ext/reservations/{reservationId}` — 실제 id 숫자 없음) · 키당 제한을 열셋 경로가 함께 셈 · 틀린 메서드 405 · Swagger 응답 표에 공통 줄(401 · 429 · 405 · 500) | DEC-012 D-01 |
| T69 | `ext_call` 원칙(0.4.0) | 새 경로 · lookup 호출 뒤 `ext_call` 표 전체와 앱 로그(caplog)에 직원 id 헤더 값 · 고객 id · 예약 id · 이름 · 이메일 문자열 0 | DEC-012 D-18 · DEC-010 D-24 |
| T70 | Swagger(0.4.0) | `n_ops - 5 - 13` · `OPS` 열셋 · parameters = §8 「시험 고침(0.4.0)」 허용 목록뿐(0.4.1 — `X-Ext-Staff-Id` 는 다섯 operation 에만) · board 설명에 「희망 상담사」 · lookup 설명에 사용 중 묶음 행동 변화 문장 · (0.4.2 · N4) lookup 설명 · 응답 스키마에 옛 문장 「`AVAILABLE` 이 0장인 묶음은 KOS 가 주지 않는다」 · 「사용 가능한 묶음」 **없음** · 헤더 설명에 「신고값 · 검증 안 함」 · 언어 설명에 덮어쓰기 위험 · (0.4.7 · 검수 r1 W2 · DEC-012 D-48) 직원 목록 설명에 `kosAccountId` **있음** · 옛 문장 「이메일 · 실명 · KOS id 는 내지 않는다」 **없음**(`tests/test_ext_docs.py`) · `test_openapi_docs.py` 전부 통과 | §8 · §6.17 |
| T71 | 기존 여섯 회귀(0.4.0) | 기존 `tests/test_ext_*.py` 전부 통과. 바꾸는 단언은 lookup 의 시술권 경로(공개 → 내부 · 가짜 KOS) · 비용(2 → 3) · 키 집합(`inUseCount` · `prepaidCards` · (0.4.2 · N6) `partialErrors` 더함) · (0.4.2 · N4) 옛 Swagger 문장 단언(있으면)뿐이고, 그 밖 단언은 그대로 · 과거 시술 응답에 메모 · 의사 키 여전히 0(T38) · (0.4.1 · 검수 r1 F2) **헤더를 읽지 않는 다섯 경로**(메뉴 · 예약 · 가능 시간대 · 과거 시술 · 예약 내역)에 이상한 `X-Ext-Staff-Id`(65자 · 한글 · `@` · `:`)를 실어도 **헤더 없을 때와 같은 응답**(상태 · 본문) · 예약의 `event_log.actor` = `ext:<연동처>` 그대로 · (0.4.2 · 검수 r2 N1) **과거 시술 · 예약 내역 본문 모델 그대로**: ⓐ 두 경로에 `{customerId: 1}` · `{name, email, customerId}` → `400 invalid_request`(모르는 키 · KOS 0) ⓑ `{name}` 만 → 지금과 같은 message(`body.email: …` 꼴 · `body: ` 갈래 문구 아님) ⓒ Swagger 두 경로의 요청 스키마 `required` 에 `name` · `email` 이 있고 `customerId` 칸이 없다 | DEC-012 D-02 · D-03 · D-37 · O14 · 검수 r2 N1 |
| T72 | 직원 API 회귀(0.4.0) | T30 그대로 + 직원 상세 `flow.consultation` 이 판정 함수를 옮기기 전과 같음 · 이전 방문 실패 때 직원 `previousVisits` 는 지금처럼 `[]` · 직원 `personal` 의 `event_log.actor` = `login_id` 그대로 | §2.1 · O11 |
| T73 | ~~(D-17 대안일 때만) CC 조회 시각~~ (0.4.3 · KOS0 판정 D-16 그대로 — **쓰지 않음** · 이 시험은 두지 않는다 · 기록으로 둔다) | KOS0 결과로 대안을 고르면: **요청이 와서 도는 날짜 조회**(`fetch_day` — 직원 · 외부 화면 요청이 캐시를 낡았다고 볼 때)가 `CONSULTATION_WAITING` 을 처음 본 일정에 §3.6 행(`source = cc_poll` · `first_at` = 그 조회의 `now`) · board 이력 호출 0 · 날짜 조회가 돌지 않은 동안 지나간 대기는 null(늦음 상한 없음) · (0.4.2 · 검수 r2 N5) **덮어쓰기**: `source = kos_event_log` 로 굳은 행 · `first_at` null 시도 행이 있는 일정 → 대안이 본 뒤 `source = cc_poll` · `first_at` = 본 시각으로 덮임 · 그 뒤 같은 일정을 다시 보아도 다시 덮지 않음 · 응답 칸 모양 T54 와 같음. D-16 이 서면 이 시험은 두지 않는다 | DEC-012 D-17 · D-38 ⑥ · §3.6 |

**실물 확인**(시험이 아니라 WORK-012 의 완료 조건): 데모 KOS 로 ① 메뉴 동기화 한 바퀴(표 행 수 = R1 §4 와 같은 규모) ② email 이 채워진 데모 고객 1명을 이름 + 이메일로 조회 ③ 이름 + 이메일로 예약(기존 고객 · 새 고객 각 1번)을 실제로 부른다. 값(이름 · 이메일 · id)은 문서에 적지 않는다.

**실물 확인(0.3.0 · WORK-013 의 완료 조건)**: 데모 KOS 로 ① 가능 시간대를 하루 부르고 KOS 웹 예약 현황(기본 그룹)의 정원 · 예약 수와 맞는지 본다 ② 목록의 한 시각으로 외부 예약 1번 → 200 · 그 칸의 `remainingSeats` 가 1 줄어듦(남은 자리 1 이었으면 칸이 빠짐) ③ email 이 채워진 데모 고객으로 과거 시술 · 예약 내역 → 200 · ② 의 예약이 예약 내역에 그 `reservationId` 로 나옴 · 과거 시술에 메모 · 의사 칸 없음 ④ 틀린 이메일 → 두 경로 모두 404 가 조회 404 와 같은 본문. 끝나면 ② 예약을 직원 화면으로 취소한다. 값은 적지 않는다.

**실물 확인(0.4.0 · WORK-014 의 완료 조건)**: 데모 KOS 로 ⓪ Phase 0 — 이력 조회 1번(모양 · `flowStep` 숫자 대응 · 같은 단계 반복 기록) · 휴무 조회 1번(원소 모양 → 고를 칸) · 선불카드 조회 1번(**카드가 있는 고객** · 원소의 잔액 · 포인트가 금액 객체인지) · 내부 `get-ticket-bundles` 가 다 쓴 · 다 취소된 묶음을 주는지(시험 T50 가짜 응답이 실물과 맞는지 · 검수 r1 W15) ① lookup — `customerId` 갈래 · 이름 갈래가 같은 고객이면 같은 응답 · 사용 중 시술권이 있는 고객(있으면)의 `inUseCount` 가 KOS 웹과 맞음 · 선불카드가 있는 고객의 잔액 · 만료일이 KOS 웹과 맞음 ② board — 건수 · 희망 상담사 · 관리실 · 접수 시각이 KOS 웹 접수 목록과 맞음 · 상담 대기를 거친 일정의 `firstConsultationWaitingAt` 이 KOS 웹 「예약 이력」 탭 시각과 맞음 · 곧바로 두 번째 호출 → 이력 조회 0번(찾은 일정 · 5분 안 일정) ③ 예약 상세 1건 — 언어 · 희망 시술 · 이전 방문 상담자가 KOS 웹과 맞음 · `event_log` `ext_view` 1줄 ④ **쓰기 셋은 시험 고객(example.com) 의 시험 예약에만** — 오더 메모 · 상담 메모를 쓰고 KOS 웹에서 보임 · (0.4.1 · 검수 r1 W10) **상담 메모를 쓴 뒤 같은 일정의 상담사 · 의사 · 결과 칸이 그대로인지** 확인 · **상담 전 일정(시험 예약 · 접수 전)에 상담 메모 쓰기 → 응답(200 · 409) 기록** · 예약 상세의 지금 메모 두 칸이 쓴 값과 같음 → **원래 값으로 되돌림** · 언어를 바꾸고 KOS 웹에서 보임 · **다른 개인 정보 칸이 그대로인지** 확인 → 원래 값으로 되돌림 ⑤ 병원 정보 · 직원 목록 — 운영 시간이 KOS 웹 병원 설정과 맞음 · 「CS팀(콜센터)」 역할 이름이 보임 · 시스템 계정 없음 ⑥ 기존 여섯 경로를 1번씩 불러 0.3.3 과 같은 응답(lookup 은 더한 칸만 다름). 값(이름 · 이메일 · id · 메모 글)은 적지 않는다.

**실물 확인 ④ 결과(0.4.6 · 2026-11-16 로컬 e2e 2번째(데모 KOS · 시험 고객의 시험 예약 2건 · 끝나고 취소) · 값 · id 적지 않음)**: 오더 메모 — 쓰기 · 빈 값(`""`) 비움 둘 다 KOS 반영 · 상담 메모 — 값 쓰기 KOS 반영 · **빈 값(`""` · `null`)은 200 인데 값 그대로**(→ D-47 · 400 으로 막음) · 공백 한 칸은 그대로 저장 · 쓴 뒤 같은 일정의 상담사 · 의사 칸 그대로 · **상담 전(예약 상태) 일정에 써도 200** · 언어 — KOS 반영 · 다른 개인 칸 변화 0 · 원래 값으로 되돌림 확인 · 새 예약 직후 예약 상세 — 2건 중 1건이 첫 호출 `404 reservation_gone` 뒤 다시 부르면 200(다른 1건은 곧바로 200 · KOS 반영 지연으로 봄 · 코드로 막지 않음 · D-47) · 시험 예약 2건은 끝나고 직원 API 로 취소함.

---

## 10. 열린 것

**0.3.3 까지는 없음 · 0.4.x 는 아래 「0.4.0 에서 열린 것」.** DEC-010 은 열린 것 0 으로 닫혔고(`_RESUME` §5 2026-11-11), 이 문서가 DEC 와 코드 규약으로 정하지 못한 다섯 가지는 코디 답(부록 B Q1 ~ Q5)으로, doc 검수 r1 의 DEC 질문 셋과 W11 은 DEC-010 고침(D-16 · D-19 · D-31 · D-35 · D-36 · 부록 B Q-A ~ Q-C · W11)으로 닫았다. 부록 B 의 질문은 모두 「답함」이다. 0.3.0(add1)은 DEC-011(열린 것 0)로 닫혔고, DEC-011 승인 결정만으로 정해지지 않은 넷은 코디 답(부록 E Q1 ~ Q4 → DEC-011 D-11 ~ D-14)으로, 0.3.1 의 문서 검수 DEC 질문 Q-add1-A 는 코디 기본값(DEC-011 D-15)으로, 0.3.2 의 코드 검수 N1 은 코디 기본값(DEC-011 D-16)으로 닫았다.

구현 때 실측으로 채우는 **값** 두 개는 정책이 아니라서 열린 것으로 두지 않는다(채우는 자리는 WORK-012 에 있다).
1. `getProductOptions` 한 번에 넣을 옵션 수 N(§4.1 ③ · 코디 Q4 「구현 시 실측」)
2. 공개 메뉴 작업 8개의 실제 경로 문자열(§4.1 — 스펙 operationId 에서 옮김)

**0.4.0 에서 열린 것**(DEC-012 「열림」):

1. ~~**이력 조회 실응답**(§6.11 4 · DEC-012 D-16 · D-17) — WORK-014 Phase 0 이 닫는다~~ (0.4.3 닫힘 — KOS0 판정 D-16 그대로 · DEC-012 D-42). 결과가 예상과 다르면 D-17 대안으로 가고 §6.11 · §3.6 · T57 · T73 을 고친다(칸 모양은 그대로)
2. (0.4.3 닫힘 — KOS0 ② ③ ④ · DEC-012 D-43 · D-44) ~~**휴무 원소 모양 → 고를 칸**(§6.16 `daysOff` · DEC-012 D-27) · **공개 선불카드 요약의 금액 꼴**(§4.4 — 내부 합산 조회는 금액 객체) · 내부 시술권 조회가 다 쓴 · 취소 묶음을 주는지(§4.3) — 같은 Phase 0 에서 데모 조회로 닫는다(조회만 · 쓰기 없음)~~
3. ~~**planner 질문 Q1 ~ Q14**(부록 G) — 답 전~~ (0.4.1 닫힘 → DEC-012 D-24 ~ D-38)
4. ~~**planner 질문 Q15 · Q16**(부록 G · 0.4.1 새로) — 답 전~~ (같은 날 닫힘 → DEC-012 D-39 · D-40)
5. **상담 메모 쓰기의 다른 칸 · 상담 전 일정**(§6.15) — 실물 확인 ④ 에서 본다
6. ~~**planner 질문 Q17**(부록 G · 0.4.2 새로) — 답 전~~ (같은 날 닫힘 → DEC-012 D-41)

---

## 부록 A. DEC-010 대응표 (D-01 ~ D-36 → 이 문서 · 빠짐 0)

| D | 결정(줄임) | 반영한 곳 |
|---|---|---|
| D-01 | 자리 = `procedure/back` · 화면 범위 아님 | 머리말 · §1.1 · §1.2 O1 · §2.1 |
| D-02 | 만드는 것 셋(메뉴 저장 · 외부 API · 인증) | §0 · §1.1 I1 ~ I4 |
| D-03 | KOS 메뉴 전부 · 모든 칸 저장 | §1.1 I1 · §3.1 · §3.2 · §9 T1 |
| D-04 | 단계별 표 + 원본 JSON · SQLite 규약 | §3.1 · §3.2 · §9 T1 |
| D-05 | 원천 작업 · SINGLE 진료항목 붙이기 · 빈 검색어 안 부름 | §4.1 ①~⑧ · §1.2 O9 · §3.2 `menu_option` · §9 T2 (코디 Q4 — `getProductOptions` 추가) |
| D-06 | 마스터 루프(1시간) · 서버 시작 1회 · Webhook 안 받음 | §4.1 「언제」 · §1.2 O9 · §9 T5 |
| D-07 | 사라진 행 = 「없음」 표시 · 되살림 · 응답엔 지금 있는 것만 | §3.1 「없음」 · §3.2 · §4.1 · §6.3 「지금 있는 것」 · §9 T3 · T7 |
| D-08 | 메뉴 = 지금 · 산 것 = KOS 값 그대로 · 메뉴에 없는 옵션도 그대로 | §4.3 표 · §6.4 · §9 T15 |
| D-09 | 정가 = 부가세 별도 · 응답 칸 이름으로 밝힘 · 시술권 가격 = KOS 값 그대로 | §3.3 · §6.1 「금액」 · §6.3 `listPriceExVat` · §6.4 `bundlePrice`(KOS 값 그대로 — 부가세 표기는 D-31 고친 문구대로 안 함) · §9 T8 · T15 |
| D-10 | 경로 분리 `/api/ext` · 토큰 · 키 섞이지 않음 | §6.1 · §7.2 · §8 · §9 T23 · T24 |
| D-11 | 엔드포인트 셋 · 예약은 지금 로직 재사용 | §6.3 · §6.4 · §6.5 · §2.1 |
| D-12 | 남은 시술권 = 조회 때마다 KOS · 복사 안 함 · 다 쓴 것 · 통계 안 줌 | §1.2 O2 · O3 · §4.3 · §9 T14 |
| D-13 | 고객 응답 = 상담 칸만 · 개인 칸 뺌 | §1.2 O5 · §6.4 · §9 T16 |
| D-14 | 「고객 없음」 ≠ 「시술권 없음」 | §4.3 「결과 없음」 · 「실패」 · §6.4 · §9 T14 |
| D-15 | 내부 `get-visitors` 이름 검색 → 우리 쪽 이메일 거르기 | §4.2 · §5 · §7.5 |
| D-16 | 한 페이지(1000)만 · `count` > 1000 = 「없음」 · KOS id 중복 제거 (2026-11-11 고침) | §4.2 「본문」 · 「한 페이지만」 · 「상한」 · 「중복 제거」 · §5 1 · 2 · §6.4 404 · §1.2 O11 · §9 T9 · T13 |
| D-17 | 이름 앞뒤 공백만 · 다시 검색 안 함 | §4.2 · §5 1 · §1.2 O7 · §9 T10 |
| D-18 | 이메일 = 공백 지움 + 소문자 · 정확 일치 · 빈 email 은 후보 아님 | §5 4 · 5 · §9 T11 |
| D-19 | 이름 정확 일치(공백 전부 지움 · 대소문자 무시 · 이름 또는 발음명) 뒤 이메일 (2026-11-11 고침) | §4.2 「응답에서 쓰는 칸」 · §5 3 · §9 T12 · T13 |
| D-20 | 2명 이상 = 「특정할 수 없음」 | §5 6 · §6.4 · §6.5 · §9 T12 · T19 |
| D-21 | 틀린 입력 = 없는 고객 = 같은 「없음」 | §5 「없음」 · §6.4 · §9 T13 |
| D-22 | email 빈 기존 고객 = 「없음」 · 보조 키 없음 · 예약으로 email 쌓임 · 중복 수용 | §1.2 O6 · §5 · §6.5 2 · §9 T13 · T18 |
| D-23 | 연동처별 API 키 · env/Secret · 배포 설정으로 교체 | §2.2 · §7.1 · §9 T23 |
| D-24 | 호출마다 기록 · 이름 · 이메일 원문 없음 | §3.4(미들웨어 · `client` · `endpoint` 고정값 · 줄이기) · §6.4(POST 본문) · §7.3(IP 저장 안 함) · §7.4 · §9 T27 · T31 |
| D-25 | 키별 호출 제한 | §7.3 · §9 T26 · T31(키 없는 거절 IP 제한) |
| D-26 | admin 공유 계정 → 외부 키 권함 · 회수는 사용자 | §1.2 O10 · §7.6 |
| D-27 | 메뉴 응답 깊이 · 진료항목 · 기기 · 약물은 DB 만 | §1.2 O4 · §6.3 · §9 T6 |
| D-28 | 옵션 `type` 그대로 · CONSULTATION 가격 · 구성 없이 | §3.2 `menu_option` · §6.3 `type` · §9 T6 |
| D-29 | `translsMap` 그대로 + 기본 이름 | §3.3 · §6.3 |
| D-30 | 가격 = 정가 `amount` 하나 · 나머지 DB 만 | §1.2 O4 · §6.3 · §9 T6 · T8 |
| D-31 | 고객 응답 칸 · 시술권 한 줄 칸 · 가격 = KOS 묶음 가격(`bundlePrice` · 낸 돈 아님 · 줄 수 있음 · 부가세 표기 안 함) (2026-11-11 고침) | §0 · §4.3 표 · §6.1 「금액」 · §6.4 · §8 · §9 T15 · T16 |
| D-32 | 예약 필수 · 선택 칸 · 1 / 0 / 2+ 갈래 · 신규 규칙을 이메일로 채움 | §5 · §6.5 · §9 T17 ~ T19 · T22 |
| D-33 | 그룹 = 설정값 하나 · 구역 = 기본 규칙 · 담당자 안 받음 · 정원 검사 같음 | §2.2 · §6.5 · §1.2 O8 · §9 T17 · T20 · T21 |
| D-34 | 키당 분당 60 · 넘으면 429 | §7.3 · §6.2 · §9 T26 |
| D-35 | 예약 0명 갈래 409/200 으로 이메일 존재가 드러나는 위험 수용 · Swagger 에 적음 (2026-11-11 추가) | §0 · §6.5 2 「드러남 수용」 · §8 엔드포인트 · §9 T29 |
| D-36 | 메뉴 응답 `syncedAt` 메타 칸 (2026-11-11 추가) | §6.3 `syncedAt` · §8 엔드포인트 · §9 T6 |

## 부록 B. planner 질문 → 코디 답 (2026-11-11)

DEC-010 과 코드 규약으로 정해지지 않아 물은 것(Q1 ~ Q5)과 doc 검수 r1 이 올린 DEC 질문(Q-A ~ Q-C · W11)이다. 모두 답을 받았다. 근거 칸의 「코디 Q1 ~ Q5」는 여기를 가리킨다(근거 표기: **코디 기본값(planner 질문 Q1 ~ Q5 · 2026-11-11)**).

| Q | 물은 것 | 상태 · 답 | 함께 가리키는 D | 반영 |
|---|---|---|---|---|
| Q1 | 0명 → 새 고객 갈래에서 KOS 중복 검사(`find-duplicated-visitor`)에 걸리면 | **답함** · **A** — 예약하지 않고 `409 customer_ambiguous`. `candidate` 를 싣지 않고, 무엇이 틀렸는지 밝히지 않는다 | D-20 · D-21 · D-22 확장 | §6.5 2 · §9 T19 |
| Q2 | 응답 id 체계 | **답함** · **A** — 메뉴 · 시술권의 id = KOS id 문자열 · 고객 id · 예약 id = ccc 정수. **KOS id 는 메뉴 · 시술권 id 에만** 내고, 고객 KOS id 는 내지 않는다 | D-08 · D-12 | §6.1 「id」 · §6.3 · §6.4 · §9 T16 |
| Q3 | 기본 그룹 설정이 비었거나 그룹이 사라졌을 때 | **답함** · **A** — 예약만 `503 ext_not_configured`(새 오류 클래스 1개). 조회 · 메뉴는 그대로 | D-33 | §2.2 · §6.5 1 · §9 T20 |
| Q4 | SINGLE 옵션의 진료항목 잇기(`getProducts` 에 id 가 없음) | **답함** · **A** — `getProductOptions` 를 원천 작업에 더해 SINGLE 진료항목 id 를 채운다. KOS 문서에 개수 상한이 있으면 따르고, 없으면 N개씩 나눠 부른다(N 은 구현 때 실측). 코디가 DEC-010 D-05 문구를 고친다 | D-03 · D-05 | §3.2 · §4.1 ③ · §9 T2 |
| Q5 | 메뉴 응답 칸 목록 | **답함** · **A + 두 칸** — 층마다 id · 기본 이름 · `translsMap` + 카테고리 `order` + 상품 · 옵션 `description` + 옵션 `type` · 정가 · 횟수 + 구성 title · count · 정가. 거기에 **단위 `unit`**(SINGLE = 진료항목 단위를 옵션 칸으로 · 구성 = 구성 단위 · 없으면 null)와 **상품 `isEvent`** 를 더한다. 그 밖(caution · 이미지 · displayChannels · badges 등)은 넣지 않는다 | D-27 · D-30 | §3.3 · §6.3 · §9 T6 |
| Q-A | (doc 검수 r1) 이름 검색의 범위 · 이름 대조 | **답함**(사용자) — 한 페이지(`countInPage` 1000)만 · `count` > 1000 = 「없음」 · KOS id 중복 제거 · 이름(또는 발음명) 정확 일치(공백 전부 지움 · 대소문자 무시) 뒤 이메일 | D-16 · D-19 | §4.2 · §5 · §9 T9 · T12 · T13 |
| Q-B | (doc 검수 r1) 예약 0명 갈래의 409/200 이 이메일 존재를 드러냄 | **답함**(사용자) — 받아들인다 · Swagger 예약 설명에 적는다 | D-35 | §6.5 2 · §8 · §9 T29 |
| Q-C | (doc 검수 r1) 시술권 가격 칸의 이름 · 뜻 | **답함**(사용자) — KOS 묶음 가격 그대로 `bundlePrice` · 낸 돈 아님 · 줄 수 있음 · 부가세 표기 안 함 | D-31 | §4.3 · §6.1 · §6.4 · §9 T15 |
| W11 | (doc 검수 r1) 메뉴 응답 `syncedAt` | **답함**(코디) — 둔다(메타 칸) | D-36 | §6.3 · §9 T6 |

## 부록 C. 조사 리포트의 「정할 것」 → 처분

| 리포트 | 정할 것 | 처분 |
|---|---|---|
| 조사 1 §8 | 1 노출 깊이 · 2 원천 작업 · 3 type 표현 · 4 가격 칸 · 5 다국어 | D-27 · D-05(+ 코디 Q4) · D-28 · D-30 · D-29 |
| 〃 | 6 채널 · 국가 필터 | 질의 칸을 열지 않는다(§6.3 「질의 칸 없음」 · D-27 이 깊이만 정함). 채널 필터는 KOS 가 키에 따라 이미 걸러 준 것을 그대로 저장한다(R1 §2.3) |
| 〃 | 7 캐시 | D-06(1시간 마스터 루프 · Webhook 안 받음) |
| 〃 | 8 id 노출 | 코디 Q2 |
| 〃 | 9 일정과 잇기 | 이번 범위 아님(D-02 · 화면 없음 D-01) |
| 〃 | 10 목록 순서 | KOS 배열 순서(`seq`)를 그대로 쓴다. 정렬해 바꾸지 않는다(§3.2 · §6.3) |
| 〃 | 11 기기/약물 구분 | 응답에 내지 않는다(D-27). DB `raw` 에 있다(§3.2) |
| 〃 | 12 스펙과 실제의 차이 | 실제 응답 기준으로 저장한다(`raw` 그대로). SINGLE 진료항목 누락은 코디 Q4 로 채운다 |
| 조사 2 §5 | 1 나눌 기준 · 3 가격 기준 · 4 삭제된 옵션 | D-08 · D-09 · D-08 |
| 〃 | 2 원천 · 6 남은 장수 · 7 저장 | D-12(묶음만 · 묶음 AVAILABLE 장수 · 매번 KOS) — §4.3 |
| 〃 | 5 같은 이름 · 다른 id | 이름으로 잇지 않는다 — 시술권 `optionId` 를 그대로 준다(D-08 · §4.3) |
| 조사 4 §3 | 1 ~ 8 | D-22 · D-16 · D-17 · D-18 · D-20 · D-19 · D-15 · D-14 |

## 부록 D. DEC-011 대응표 (D-01 ~ D-16 → 이 문서 · 빠짐 0 · 0.3.0 · D-15 는 0.3.1 · D-16 은 0.3.2)

| D | 결정(줄임) | 반영한 곳 |
|---|---|---|
| D-01 | 셋 다 `/api/ext` · 인증 · 제한 · 기록 · no-store · tag · 오류 모양 공유 | §1.1 I6 · §6.2 · §6.6 ~ §6.8 · §7.3 · §8 · §9 T29 · T44 |
| D-02 | 가능 시간대 = 기본 그룹 하나 · 간격 칸 · 시작 · 남은 자리 · 0 뺌 · 지난 시각 뺌 · 예약 정원 검사와 같은 규칙 | §6.6 4 · 5 · 「같은 규칙인 까닭」 · 응답 표 · §9 T32 · T33 · T37 |
| D-03 | 과거 시술 = 지금 앞 · 최신 순 · 날짜 · 시작 · 결과 · 시술 이름 · 메모 · 의사 안 냄 | §6.7 · §9 T38 |
| D-04 | 예약 내역 = 오늘(KST) 이후 · 오름차순 · 상태(취소 포함) | §6.8 3 · 4 · §9 T40 |
| D-05 | 고객 찾기 = DEC-010 조회 규칙 · 404 바이트 같음 | §6.7 1 · §6.8 1 · §9 T39 |
| D-06 | 이름 · 이메일은 본문 POST | §6.6 요청(GET 은 날짜만) · §6.7 요청 · §9 T42 |
| D-07 | 경로 셋(코디 기본값) | §0 · §1.1 I6 · §6.6 ~ §6.8 머리 · §8 |
| D-08 | 날짜 범위 오늘 ~ 90일 · 그 밖 400(코디 기본값) | §6.6 1 · 오류 표 · §9 T34 |
| D-09 | 설정 빔 · 그룹 없음 · 켜진 구역 0 = 503(코디 기본값) | §6.6 2 · 오류 표 · §9 T35 |
| D-10 | 과거 시술 최근 50건(코디 기본값) | §6.7 4 · §9 T38 |
| D-11 | 후보 시각 = 운영 구간 안 간격 줄 · 남은 자리 = 켜진 구역 합 · 행 없는 구역 뺌 · 모두 없으면 시각 뺌(Q1) | §6.6 4 · 5 · §9 T32 |
| D-12 | 요청마다 슬롯 1번 · 공유 사본 바꿈 · 실패 502 · KOS 1번(Q2) | §6.6 3 · 오류 표 · §6.9 · §9 T36 · T43 |
| D-13 | 예약 내역 칸 · 일정 읽기 1번 · 예약 id = 사본 있으면 · 상태 = 2계층 주 상태(Q3) | §6.8 2 · 5 · 응답 표 · §9 T40 |
| D-14 | 오늘 겹침 그대로 · SPEC · Swagger 에 적음(Q4) | §6.7 · §6.8 「오늘 겹침」 · §8 · §9 T41 · T29 |
| D-15 | `deleted: true` 일정은 과거 시술 · 예약 내역에서 뺌(사본 쓰기와 같은 규칙 · Q-add1-A) | §6.7 3 · §6.8 3 · §9 T38 · T40 |
| D-16 | 일정 원소 모양이 깨지면 두 경로 `502 kos_unavailable`(원문 0) | §6.7 2 · §6.7 오류 · §6.8 2(같은 규칙) · §9 T47 |

## 부록 F. DEC-012 대응표 (D-01 ~ D-48 → 이 문서 · 빠짐 0 · 0.4.0 · D-24 ~ D-40 은 0.4.1 · D-41 은 0.4.2 · D-42 ~ D-44 는 0.4.3 · D-45 는 0.4.4 · D-46 은 0.4.5 · D-47 은 0.4.6 · D-48 은 0.4.7)

| D | 결정(줄임) | 반영한 곳 |
|---|---|---|
| D-01 | 전부 연동처 공통 · 인증 · 제한 · 기록 · no-store · tag · 오류 모양 공유 · 권한 분기 없음 | §0 · §6.2 · §6.9 · §7.3 · §8 tag · 보안(0.4.0) · §9 T68 |
| D-02 | 새 경로에 DEC-011 D-03 · 이름+이메일 규칙 안 검 · 기존 여섯 그대로 · ccc id 열거 위험 수용 | §0 · §1.2 O14 · §6.4 `customerId` 갈래 · §6.12 이전 방문 메모 · 의사 · §9 T48 · T59 · T71 |
| D-03 | lookup 은 필드 추가만 · 사용 중 묶음 행동 변화를 이력 · Swagger 에 | 변경 이력 0.4.0 · §4.3 「거르기」 · `totalCount` · §6.4 · §8 엔드포인트(0.4.0) · §9 T49 · T50 · T71 |
| D-04 | 쓰기 = KOS 먼저 → event_log → 사본 · KOS 실패 그대로 | §3.5 · §6.13 ~ §6.15 · §9 T62 ~ T65 |
| D-05 | 차트 메모 = 상담 메모 · 쓰기 둘 | §1.2 O13 · §6.14 · §6.15 · §8 |
| D-06 | 외주 = KOS 계정(CS팀) · CC 저장 없음 · 역할로 구분 | §6.17 `roleName` · Swagger 줄 · §9 T67 |
| D-07 | ① 예산 · 동행자 · 통역 · 진단 제외 · 만료일 칸 없음(사용자) ② 차감 제외(코디) | §1.2 O12 · §4.3 ④ · §6.4 · §9 T50 |
| D-08 | lookup ① `customerId` ② 내부 시술권 · `inUseCount` ③ `prepaidCards` · DEC-010 D-12 고침 | §4.3(머리 고침 줄) · §4.4 · §6.4 · §6.18 · §9 T48 ~ T52 |
| D-09 | board — 예약 단위 · 칸 일곱 · 희망 상담사 뜻 · CC 판정 | §6.11 · §8 · §9 T54 · T55 |
| D-10 | 예약 상세 — 직원 상세 고객 정보 + 희망 시술 · 희망 의사 · 이전 방문 상담자 | §6.12 · §9 T59 |
| D-11 | 고객 언어 — 다시 읽고 묶음 전체 · 덮어쓰기 위험 수용 | §6.13 · §8 · §9 T62 |
| D-12 | 오더 메모 — 내부 `change-order-memo` · 통째 교체 | §6.14 · §6.18 · §9 T63 |
| D-13 | 상담 메모 — 공개 `updateScheduleConsultationInfo` | §6.15 · §6.18 · §9 T64 |
| D-14 | 병원 정보 — `get-hospital` + 운영 시간 + 휴무 | §6.16 · §6.18 · §9 T66 |
| D-15 | 직원 목록 — staffId · 이름 · roleName · roleTags · 활성 · 비활성 포함 · ~~이메일 없음~~ (2026-11-17 고침 → D-48) | §6.17 · §9 T67 |
| D-16 | 처음 상담 대기 — ① 원천 = 단계 이력(사용자) ② 경로 = `get-schedule-event-logs`(코디) ③ 대상 = 접수 뒤 일정 전부 · CC 판정 아님(사용자) · (0.4.2 고침 줄) 「건수 비례 안 함」 → board 요청 수에 비례 안 함 · 하루 합 = 접수 뒤 일정 수의 작은 배수 | §3.6 · §6.11 4 · §6.9 · §8 · §9 T57 · T58 |
| D-17 | 이력 실응답 미확인 → WORK Phase 0 · 대안 = CC 날짜 조회가 본 시각(요청이 와야 돎 · 늦음 상한 없음) · 칸 모양 같음 | §3.6 `source` · §6.11 4 · §9 T73 · §10 0.4.0 · 실물 확인(0.4.0) ⓪ |
| D-18 | 열람 = 선택 헤더 직원 id → event_log 새 type · 두 경로 · ext_call 원칙 그대로 · 신고값 | §3.5 `ext_view` · §6.10 · §6.4 · §6.12 · §9 T52 · T53 · T61 · T69 |
| D-19 | 쓰기 행위자 = `ext:<연동처>:<직원 id>` · 없으면 `ext:<연동처>` | §3.5 · §6.10 · §6.13 ~ §6.15 · §9 T62 |
| D-20 | clinicId — 서버 하나 = 병원 하나 · 병원 정보에 주고 직원 목록은 그 값만 · 다른 값 404 · 값은 질문 | §6.16 `clinicId`(Q1) · §6.17 · §9 T66 · T67 |
| D-21 | 직원 목록에서 시스템 계정 · 제외 목록 뺌 | §6.17 3 · §9 T67 |
| D-22 | 병원 정보 기본 칸(이름 · 주소 · 전화 · 운영 시간) · 나머지는 표 + 질문 | §6.16 표(Q2) · §9 T66 |
| D-23 | board 10초 사본 · 날짜 조회 실패 = 낡은 사본 + 표시 · 상세 부분 실패 = null + 오류 칸 | §6.11 1 · 4 · §6.12 3 · 4 · `partialErrors` · §9 T56 · T57 · T60 |
| D-24 | `clinicId = 1` · 전역 유일 아님 | §6.16 `clinicId` · §8 · §9 T66 |
| D-25 | 병원 칸 = 이름 · 주소 · 전화 · 운영 시간 · 휴무만 | §6.16 표 · §9 T66 |
| D-26 | 병원 빈 문자열 → null | §6.16 · §9 T66 |
| D-27 | 휴무 기간 오늘 ~ +90일 · 원소는 KOS0 뒤 고른 칸만(→ D-43) | §6.16 2 · `daysOff` · §9 T66 · 실물 확인 ⓪ · §10 2 |
| D-28 | 병원 요청마다 3번 · 하나라도 실패 502 | §6.16 2 · 3 · §9 T66 |
| D-29 | 직원 칸 결합(내부 + 사본) | §6.17 4 · §9 T67 |
| D-30 | board = 그날 사본 전부 | §6.11 2 · §9 T54 |
| D-31 | 선불카드 `available: true` | §4.4 · §9 T51 |
| D-32 | `customerId` 갈래 = 내부 `get-visitor` | §6.4 · §9 T48 |
| D-33 | lookup 갈래 섞이면 400 | §6.4 · §9 T49 |
| D-34 | 상세에 지금 오더 · 상담 메모 | §6.12 표 · §6.14 · §6.15 요청 · §8 · §9 T59 · T60 · 실물 확인 ④ |
| D-35 | 메모 쓰기 — 빈 값 = 비움 · 상태로 안 막음 · 건너뛰기 없음 | §6.14 · §6.15 · §9 T63 · T64 |
| D-36 | 선불카드 실패 → lookup 200 · `prepaidCards: null` · `partialErrors` | 변경 이력 0.4.1 · §4.4 · §6.4 · §8 · §9 T51 |
| D-37 | 열람 헤더 = 다섯 경로만 · lookup 은 틀린 헤더 = 없음 · 새 넷은 400 · `@` 뺌 · `ext_view` 행위자 | §3.5 · §6.2 · §6.10 · §6.12 · §6.13 ~ §6.15 · §8 · §9 T52 · T53 · T61 · T70 · T71 |
| D-38 | 처음 상담 대기 — 찾은 값만 굳힘 · (0.4.2) 사건이 있을 때만 다시(처음 봄 · 대기 새로 봄 · 귀가 뒤 · 실패 재시도 ≤ 3) · 시도 예약 · 요청당 상한 10 · 날짜 지나면 멈춤 · 대안 덮어쓰기 | §3.6 · §6.9 · §6.11 4 · §9 T57 · T58 · T73 |
| D-39 | board `partialErrors` 의 `consultationHistory` — 실패 · (0.4.2 넓힘) 이번 요청에서 사건이 있었는데 상한으로 못 부른 null 이 있을 때만 | §6.11 4 · 응답 표 · §9 T57 |
| D-40 | 귀가 등 끝난 단계 뒤 1번 더 부르고 멈춤 | §3.6 `final_tried` · §6.11 4 · §9 T57 |
| D-41 | 귀가 뒤 1번 실패 → 실패 재시도(≤ 3)가 받음 | §6.11 4 ⓓ · §9 T57 |
| D-42 | KOS0 판정 D-16 그대로 · D-17 대안 쓰지 않음 · `eventType` 끝 조각 · `flowStep` 문자열 · 원소 시각 최솟값 | §3.6 `source` · §6.11 4 「부르기」 · D-17 절 취소선 · §6.18 · §9 T57 · T73 · §10 1 |
| D-43 | 휴무 원소 = `{startDate, endDate}` · `name` 없음 | §6.16 2 · `daysOff` · §8 · §9 T66 · §10 2 |
| D-44 | 선불카드 금액 객체 · 내부 시술권 다 쓴 · 취소 묶음 = KOS0 확인(계약 고침 없음) | §4.3 거르기 근거 · §4.4 근거 · §10 2 |
| D-45 | 코드 검수 r1 SPEC 한 줄들 — ⓐ 귀가면 ⓒ 겸함 · KOS 「고객 없음」 400 NotFound 도 404 · 상세 `customerId` null · board `event_log` 그날 예약 id 로 거름 · 명시 null = 없음 | §6.4 · §6.9 · §6.11 3 · 4 ⓐ · §6.12 표 · §9 T48 · T49 · T55 · T57 |
| D-46 | 로컬 e2e — 시술권 거르기 먼저(걸러진 묶음 모양은 502 사유 아님) · 내부 `price` 에 `value` 없음 = 0 · `price` 없음 · 숫자 아닌 `value` 는 502 | §4.3 「거르기」 · 「모양 오류」 · `bundlePrice` · §9 T50 |
| D-47 | 로컬 e2e 2번째 — 상담 메모 빈 값 = `400`(KOS 가 비우지 못함 · KOS 0) · 오더 메모 빈 값 = 비움 그대로 · 예약 직후 `reservation_gone` 은 막지 않고 Swagger 한 줄 | §6.12 오류 표 · §6.15 요청 · 오류 · 실물 결과 · §8 엔드포인트(0.4.0) · §9 T64 · 실물 확인 ④ |
| D-48 | 직원 목록에 칸 셋 더함 — `email` · `realName`(`name` 과 다른 칸) · `kosAccountId`(= 내부 `id`) · `null` · 빈 문자열 · 칸 없음 = null(`email` · `realName`) · 필드 추가만(다섯 칸 · 행 고르기 · KOS 1 그대로) · 사본에 이메일 저장 안 함 · 응답 밖에 세 값 안 남김 | §0 · §4.4 · §6.1 「id」 · §6.17 2 · 4 · 응답 표 · 「넣지 않는 칸」 · 「응답 밖」 · Swagger 설명 · §8 엔드포인트(0.4.0) · §9 T67 · T70 |

## 부록 G. planner 질문 (0.4.0 · 2026-11-16 · Q1 ~ Q17 **답함**)

DEC-012 와 코드 규약만으로 정해지지 않은 것이다. Q1 ~ Q14 는 2026-11-16 답이 와서(사용자 「추천대로」 · Q2 는 사용자가 고친 값 · Q7 · Q14 는 문서 검수 r1 로 코디가 바꾼 값) DEC-012 D-24 ~ D-38 이 되었다. 본문 표기는 그 D 번호로 바꿨다. Q15 · Q16 은 0.4.1 에서 새로 생긴 질문이고, 같은 날 코디 답으로 DEC-012 D-39 · D-40 이 되었다.

| Q | 묻는 것 | 제안 | 다른 길 | 근거 · 반영 | 답 |
|---|---|---|---|---|---|
| Q1 | `clinicId` 값 | CC 고정 정수 **`1`** — 고객 · 예약 id 처럼 ccc 정수 체계이고, KOS 테넌트 id 를 밖에 내지 않는다(코디 Q2 「KOS id 는 메뉴 · 시술권에만」) | KOS 테넌트 id 문자열을 그대로 | DEC-012 D-20 · §6.16 · §6.17 | 제안대로 → D-24 |
| Q2 | 병원 정보 17칸 중 낼 칸 | 기본 넷(이름 · 전화 · 주소 · 운영 시간) + 휴무 + **국적 · 언어 · 웹사이트 · `translsMap`**(다국어 연동처에 쓸 만함) · 안 냄 = 대표자 · 회사명 · 사업자 번호 · 요양기관 번호 · 적격 발행자 번호 · 세금계산서 이메일 · 이미지 URL 넷 | 기본 넷만 · 17칸 전부 | DEC-012 D-22 · C3 §2.1 · §3-4 · §6.16 표 | **기본 넷 + 휴무만**(국적 · 언어 · 웹사이트 · `translsMap` 뺌) → D-25 |
| Q3 | 병원 정보 빈 칸 | 빈 문자열 → null(CC 설정 값으로 채우지 않는다) | 빈 문자열 그대로 · CC env 로 채움 | C3 §3-5 · §6.16 | 제안대로 → D-26 |
| Q4 | 휴무 조회 기간 · 모양 | 오늘 0시 ~ 오늘 + 90일(가능 시간대와 같은 폭) · 원소는 KOS 그대로(Phase 0 에서 모양 확인 뒤 고침) | 기간을 질의 칸으로 받음 · 휴무를 이번에 빼고 원소 모양 확인 뒤 더함 | DEC-011 D-08 · `상담대기2.har`(빈 배열만) · §6.16 | 기간 제안대로 · 원소는 KOS0 뒤 고른 칸만 → D-27 |
| Q5 | 병원 정보 신선도 · 실패 | 요청마다 내부 3번 · 저장 없음 · **하나라도 실패하면 502**(부분 응답 없음) | 마스터 루프(1시간) 사본 · 운영 시간 실패만 null + 오류 칸 | C3 §3-6 · §6.16 2 · 3 | 제안대로 → D-28 |
| Q6 | 직원 목록 칸을 어디서 | 이름 · 역할 이름 · 활성 = 내부 응답(지금 값) · `staffId` · `roleTags` = 직원 사본(공개 태그 문자열) · 사본에 없으면 null · `[]` | 내부 응답만(태그는 숫자 → 이름 순서 대응 · 추정) · 사본만(역할 이름 없음) | C2 §2.2(숫자 태그 대응은 82/82 추정) · §3.1 · §6.17 4 | 제안대로 → D-29 |
| Q7 | 열람 헤더 이름 · 꼴 | `X-Ext-Staff-Id` · 1 ~ 64자 · 영문 · 숫자 · `. _ @ -` · 틀리면 400 | 꼴 검사 없이 받고 길이만 자름 | DEC-012 D-18 · §6.10 | **바뀜** — 이름 그대로 · 다섯 경로만 · lookup 은 틀린 헤더 = 없음 · 새 넷 400 · `@` 뺌 → D-37 |
| Q8 | board 에 넣는 예약 | 그날 사본 전부(취소 · 부도 · 귀가 포함 · 직원 카드와 같은 집합) · 연동처가 `state` 로 거른다 | 접수 뒤 단계만 · 취소 · 부도 뺌 | DEC-012 D-09 · C1 §1-1 · §6.11 2 | 제안대로 → D-30 |
| Q9 | 선불카드 범위 | `available: true`(만료 안 됨 · 잔액 있음 — 시술권 「사용 가능만」 D-12 와 같은 결) | 전부(만료 · 0원 포함) | C1 §3-5 · §4.4 | 제안대로 → D-31 |
| Q10 | `customerId` 갈래의 고객 칸 | 내부 `get-visitor` 1번으로 이름 · `isNew` · 최근 방문일을 받아 이름 갈래와 같은 칸을 채운다(호출 +1 · 사본 덮어씀) | 사본 값만 쓰고 `lastVisitDate` = null(호출 0) | `상담대기.har` `get-visitor` 키 · §6.4 | 제안대로 → D-32 |
| Q11 | lookup 두 갈래가 섞인 요청 | `customerId` 만 · 또는 `name` + `email` 만 — 섞으면 400 | `customerId` 가 있으면 이름 · 이메일 무시 | DEC-012 D-03 · §6.4 | 제안대로 → D-33 |
| Q12 | 예약 상세에 **지금 오더 메모 · 상담 메모**를 넣을지 | **넣는다** — 쓰기가 통째 교체라 연동처가 지금 값을 읽을 곳이 필요하다. 일정 상세 원본(`orderMemo` · `consultation.consultationMemo`)에 이미 있어 호출 0 추가. ~~답 전에는 계약에 넣지 않았다~~ (0.4.1 §6.12 표에 넣음) | 넣지 않음(브리프 목록 그대로) | `상담대기.har` 일정 상세 키 · DEC-012 D-12 · D-13 | **넣는다** → D-34 |
| Q13 | 오더 · 상담 메모 쓰기 세부 | 빈 문자열 = 비움으로 그대로 보냄 · 예약 상태로 막지 않음(KOS 가 거르면 409) · 같은 값 건너뛰기 없음 | 끝난 예약 409(예약 메모 규칙을 빌림) | 코드 규약: `app/service/reservations.py:997-1008`(예약 메모 규칙) · §6.14 · §6.15 | 제안대로 → D-35 |
| Q14 | 처음 상담 대기 저장 규칙 | 이벤트 없음 + 지금 상담 대기 → 저장 안 함(다음에 다시) · 이벤트 없음 + 다른 단계 → null 저장 · 실패 → 저장 안 함 | 이벤트가 없으면 늘 저장 안 함(건수 비례 재호출 위험) | DEC-012 D-16 · §6.11 4 | **바뀜** — 찾은 값만 굳힘 · 5분 간격 · 요청당 상한 → D-38 |
| Q15 | board `partialErrors` 의 `consultationHistory` 를 언제 넣나 | 이 응답의 대상 줄 중 시각이 null 이고 ⓐ 마지막 시도가 실패(5분 안의 지난 실패 포함)이거나 ⓑ 요청당 상한 때문에 한 번도 부르지 못한 줄이 하나라도 있을 때(「아직 확인하지 못한 시각이 있다」). 못 찾음만 남은 null 은 넣지 않는다 | 이번 요청에서 실제로 실패한 호출이 있을 때만(5분 간격 · 상한으로 미룬 null 은 조용히 null) | DEC-012 D-23 · D-38 · §6.11 4 · 검수 r1 「조용히 통과하는 자리」 | 제안대로(코디 기본값) → D-39 · (0.4.2) ⓑ 를 「이번 요청에서 사건이 있었는데 상한으로 못 부른 줄」로 넓힘(코디 기본값 · 검수 r3 참고 P2) |
| Q16 | 귀가 등 그날 더 바뀌지 않을 접수 뒤 일정을 못 찾음이면 그날 끝까지 5분마다 다시 부르나 | 그렇다 — D-38 규칙 그대로(갈래를 늘리지 않는다). 비용 상한은 5분마다 「못 찾은 접수 뒤 일정 수」(§6.9) | 귀가 · 끝난 단계로 간 뒤 1번 더 부르고 그 결과로 그날 멈춤(상담 안 거친 일정이 많은 날 호출을 줄임) | DEC-012 D-38 ② ④ · §6.11 4 · §6.9 | **다른 길**(코디 기본값) — 끝난 단계 뒤 1번 더 부르고 멈춤 → D-40 |
| Q17 | (0.4.2) 귀가 뒤 1번(D-40 · §6.11 4 ⓒ)이 **실패**하면 실패 재시도(ⓓ)가 받나 | 받는다 — 실패는 어느 사건에서 났든 ⓓ 규칙 하나(5분 뒤 · 하루 ≤ 3). D-40 의 「실패여도 그날 더 부르지 않는다」는 사건(ⓒ)을 다시 일으키지 않는다는 뜻으로 읽는다 | D-40 글자 그대로 — 귀가 뒤 1번이 실패면 그날 멈춤(KOS 장애 시각에 귀가한 일정은 null 로 남음) | DEC-012 D-38 ② ⓓ · D-40 · §6.11 4 | 제안대로(코디 기본값) → D-41 |

## 부록 E. planner 질문 → 코디 답 (add1 · 2026-11-12)

코드 사실(main `e0e4a16`)을 보고 DEC-011 승인 결정만으로 정해지지 않아 물은 넷이다. 코디가 「4개 모두 추천대로」로 답했고(msg_ad6deebe3459), DEC-011 에 **코디 기본값(planner 질문 Qn)** 으로 D-11 ~ D-14 가 됐다.

| Q | 물은 것 | 답 | DEC-011 | 반영 |
|---|---|---|---|---|
| Q1 | 가능 시간대 후보 시각 · 슬롯 행이 없을 때 | 운영 구간 안 간격 줄 · 켜진 구역 남은 자리 합 · 행 없는 구역 뺌 · 모두 없으면 시각 뺌 | D-11 | §6.6 4 · 5 |
| Q2 | 신선도 · KOS 비용(사본만 · 날짜 캐시 · 슬롯 직접) | 요청마다 슬롯 1번 → 공유 사본 바꿈 · 실패 502 | D-12 | §6.6 3 · §6.9 |
| Q3 | 예약 내역 칸 · 우리 사본에 없는 KOS 예약 | 일정 읽기 1번 · `reservationId` 사본 있으면 · 없으면 null · 상태 = 2계층 주 상태 | D-13 | §6.8 |
| Q4 | 오늘 지난 일정이 두 목록에 겹침 | 글자 그대로 두고 적는다 | D-14 | §6.7 · §6.8 · §8 |
| Q-add1-A | (문서 검수 add1 W2) KOS 일정 `deleted: true` 를 두 목록에서 뺄지 | 뺀다(사본 쓰기 `apply_schedule` 과 같은 규칙) — 코디 기본값 | D-15 | §6.7 3 · §6.8 3 |
| N1(코드 검수 add1 r1) | 일정 원소 모양이 깨지면 500 그대로 · 원소 건너뜀 · 502 중 무엇 | 502 `kos_unavailable`(원문 0) — 코디 기본값 | D-16 | §6.7 2 · §9 T47 |

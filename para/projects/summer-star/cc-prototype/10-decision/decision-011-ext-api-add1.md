---
type: decision
id: DEC-011
title: "외부 연동 API 2차(add1) — 예약 가능 시간대 · 고객 과거 시술 · 고객 예약 내역(`/api/ext` 세 경로 더함)"
status: accepted
product: cc-prototype
feature: procedure
created_at: 2026-11-12
updated_at: 2026-11-12
tags:
  - product/cc-prototype
  - feature/procedure
  - doc/decision
  - status/accepted
links:
  baselines: []
  decisions:
    - "[[decision-010-product-ext-api|DEC-010]]"
    - "[[decision-006-reservation-board|DEC-006]]"
  specs:
    - "[[spec-008-product-ext-api|SPEC-008]]"
  works:
    - "[[work-013-ext-api-add1|WORK-013]]"
  releases: []
  related: []
up: []
sources:
  - "orchestration/work/api-swagger-docs/add1-spec-instructions.md (협업자 요청 요지 · 사용자 승인 D-01 ~ D-06 · 코디 기본값 · 2026-11-12)"
  - "para/projects/summer-star/cc-prototype/10-decision/decision-010-product-ext-api.md (DEC-010 · 공유하는 인증 · 제한 · 기록 · 오류 · 고객 찾기 규칙)"
  - "cc-prototype procedure/back main e0e4a16 (읽기만 — service/reservations.py · domain/reservation_rules.py · kos/reservation_sync.py · service/ext.py · api/ext.py · schemas/ext.py)"
  - "orchestration/work/api-swagger-docs/add1-review-r1.md (코드 검수 add1 r1 N1 → 코디 기본값 · 아래 D-16)"
  - "orchestration/work/api-swagger-docs/review-doc-add1.md §8 Q-add1-A → 코디 기본값(아래 D-15)"
  - "planner 질문 Q1 ~ Q4 → 코디 답 「4개 모두 추천대로」(2026-11-12 · msg_ad6deebe3459 · 아래 D-11 ~ D-14)"
---

# 외부 연동 API 2차(add1) — 결정

> 기능 계약(경로 · 요청 · 응답 · 오류 표 · 시험)은 **SPEC-008 0.3.2 §6.6 ~ §6.9** 이 갖고, 작업 순서는 **WORK-013** 이 갖는다. 이 문서는 무엇을 정했는지만 적는다.
> 이미 배포된 세 경로(메뉴 · 조회 · 예약)와 공유하는 규칙은 **DEC-010** 이 정본이다. 여기서는 다시 정하지 않고 가리키기만 한다.

## Context

링키 · 차티는 이미 배포된 `/api/ext/*`(메뉴 · 이름+이메일 조회 · 예약)를 쓰고 있다. 협업자가 세 가지를 더 요청했다.

1. 특정일 예약 가능 시간대 — 보내는 값: 날짜 `YYYY-MM-DD` / 받는 값: 그날 예약 가능한 시간대 목록
2. 고객 과거 시술 — 보내는 값: 이름 · 이메일 / 받는 값: 방문 목록(최신 순)
3. 예약 내역 — 보내는 값: 이름 · 이메일 / 받는 값: 그 고객의 예약 목록

코드에서 확인한 사실(main `e0e4a16` · 읽기만):

- 예약 생성의 정원 검사는 사본 `reservation_slot` 의 (그룹 · 구역 · 시작 시각) 행 하나만 본다. `count ≥ capacity` 면 `409 slot_full` 이고, 행이 없으면 꽉 차지 않은 것으로 본다. 구역은 `KOS_ZONE_ID` 에 자리가 있으면 그 구역, 없으면 order 순으로 자리 있는 첫 구역이다(`service/reservations.py` `create()` · `_pick_zone()`)
- 슬롯 사본은 KOS 공개 `get-reservation-slots-by-groups` 를 하루 단위로 불러 통째로 바꾼다(`kos/reservation_sync.py` `_slots` · `repo.replace_slots`). 외부 예약은 이 사본을 새로 읽지 않고 그대로 본다
- 직원 예약 상세의 「이전 방문」은 KOS 공개 `get-schedules-by-visitor` 1번으로 고객 일정 전부를 받는다. 결과 분류는 `PREV_RESULT`(`COMPLETED` → completed · `NO_SHOW` → noshow · `CANCELED` → canceled · 그 밖 → other)이고, 시술 목록은 일정 작업(「방 배정」 기타 작업 뺌)이다(`previous_visits()`)
- 직원 판 예약 상태는 2계층 주 상태(`state_of` — 취소 · 부도가 먼저, 아니면 `flowStep`)다

근거 칸 표기: **사용자 승인** = 코디 추천을 사용자가 그대로 승인(2026-11-12) / **코디 기본값** = 코디가 정하고 이 문서에 그렇게 표시한 값 — D-11 ~ D-14 는 planner 가 코드 사실을 보고 물은 Q1 ~ Q4 에 코디가 「추천대로」 답한 값이라 「코디 기본값(planner 질문 Qn)」으로 적는다.

## 근거 개념

없음. 사용자 승인 · 코디 기본값 · 코드 사실에서 나왔다.

## Decision

### 공통

| ID | 결정 | 근거 |
|---|---|---|
| D-01 | 셋 다 외부 연동 API(`/api/ext/*`)다. 인증(`X-Api-Key`) · 키당 호출 제한 · `ext_call` 기록 · `Cache-Control: no-store` · Swagger tag 「외부 연동」 · 오류 모양은 DEC-010 을 그대로 공유한다(DEC-010 D-10 · D-23 ~ D-25 · D-34) | 사용자 승인 |
| D-05 | 고객 찾기는 DEC-010 조회 규칙을 그대로 쓴다(DEC-010 D-15 ~ D-22 — 이름 검색 한 페이지 · 이름 정확 일치 · 이메일 정확 일치 · 0 / 1 / 2+). 고객 없음과 틀린 입력은 조회와 **바이트까지 같은** `404` 다. 2명 이상은 조회와 같은 `409` 다 | 사용자 승인 |
| D-06 | 이름 · 이메일은 URL 에 두지 않는다. 본문 POST 로 받는다(조회와 같은 이유 — 접근 로그) | 사용자 승인 |
| D-07 | 경로 = `GET /api/ext/availability?date=YYYY-MM-DD` · `POST /api/ext/customers/visits` · `POST /api/ext/customers/reservations` | 코디 기본값 |

### 예약 가능 시간대

| ID | 결정 | 근거 |
|---|---|---|
| D-02 | 가능 시간대 = **외부 예약 기본 그룹(DEC-010 D-33 의 env 그룹) 하나만**. 칸 = 그 그룹의 시간 간격. 칸마다 시작 시각과 남은 자리 수를 준다. 남은 자리가 0 인 칸은 뺀다. 오늘이면 이미 지난 시각은 뺀다. 남은 자리 계산은 **예약 생성의 정원 검사와 같은 규칙**이다 — 이 목록의 시각으로 예약하면 정원 때문에 거절되지 않아야 한다(동시 요청 경합만 예외) | 사용자 승인 |
| D-08 | 날짜 범위 = 오늘(KST) ~ 오늘 + 90일. 지난 날짜 · 범위 밖 · 형식이 틀린 날짜는 `400 invalid_request`(지금 오류 code 체계) | 코디 기본값 |
| D-09 | 기본 그룹 env 가 비었거나 · 그 그룹이 없거나 · 켜진 구역이 0 이면 가능 시간대도 `503 ext_not_configured` 다(KOS 를 부르기 전 · DEC-010 D-33 과 같음) | 코디 기본값 |
| D-11 | **후보 시각과 슬롯 행이 없을 때**: 후보 시각 = 그 그룹 시간표의 그날 운영 구간(쉬는 시간 뺌) 안에서 그룹 간격으로 나눈 줄(시작 + 간격 ≤ 구간 끝). 시각마다 남은 자리 = 켜진 구역별 `max(0, capacity − count)` 의 합이다. 슬롯 행이 없거나 `capacity` 가 null 인 구역은 합에서 빼고, 켜진 구역 모두 행이 없으면 그 시각을 뺀다(자리 수를 모르면 내지 않는다 — 목록에 없어도 예약은 될 수 있다) | 코디 기본값(planner 질문 Q1 · 2026-11-12) |
| D-12 | **신선도 · KOS 비용**: 요청마다 KOS 공개 `get-reservation-slots-by-groups` 를 1번(그날 · 사본의 모든 예약 그룹 — 하루 조회와 같은 본문) 부르고, 공유 슬롯 사본을 바꾼 뒤 계산한다. 그래서 바로 뒤 예약 생성이 같은 사본을 본다(D-02). 실패하면 `502 kos_unavailable` 이다. 요청 1번 = KOS 호출 1번 | 코디 기본값(planner 질문 Q2 · 2026-11-12) |

### 과거 시술 · 예약 내역

| ID | 결정 | 근거 |
|---|---|---|
| D-03 | 과거 시술 = 지금보다 앞선 KOS 일정, 최신 순. 칸 = 날짜 · 시작 시각 · 결과(직원 「이전 방문」의 결과 분류 그대로) · 시술 이름 목록. **예약 메모 · 상담 메모 · 의사 이름은 내지 않는다** | 사용자 승인 |
| D-10 | 과거 시술은 최근 50건까지 준다 | 코디 기본값 |
| D-04 | 예약 내역 = 오늘(KST) 이후 일정, 시각 오름차순, 상태(취소 포함). 지난 일정은 D-03 에서 본다 | 사용자 승인 |
| D-13 | **예약 내역 칸**: KOS 공개 `get-schedules-by-visitor` 1번(과거 시술과 같은 호출). 칸 = 예약 id(ccc 사본에 그 일정이 있으면 그 id · 없으면 null · 사본에 새로 쓰지 않음 · 외부 예약 API 로 만든 예약은 늘 사본에 있다) · 날짜 · 시작 · 끝(첫 묶음) · 상태 = 직원 판 2계층 주 상태 그대로(`reserved` · `reception` · `consultation` · `procedure` · `home` · `canceled` · `noshow`). 그룹 이름 · 메모 · 담당자는 내지 않는다 | 코디 기본값(planner 질문 Q3 · 2026-11-12) |
| D-14 | **오늘 겹침**: D-03(지금 이전)과 D-04(오늘 KST 0시 이후)를 글자 그대로 둔다. 그래서 오늘 이미 시작 시각이 지난 일정은 두 목록에 다 나온다. 이 겹침을 SPEC 과 Swagger 에 적는다 | 코디 기본값(planner 질문 Q4 · 2026-11-12) |
| D-15 | **지워진 일정**: KOS 고객 일정 중 `deleted: true` 인 것은 과거 시술(D-03)과 예약 내역(D-04) **둘 다에서 뺀다**. 사본 쓰기(`apply_schedule`)가 지워진 일정을 건너뛰는 것과 같은 규칙이다 — 지워진 일정이 「살아 있는 예약」으로 읽히지 않게 한다. (2026-11-12 추가 — 문서 검수 add1 W2 · Q-add1-A) | 코디 기본값(Q-add1-A · 2026-11-12) |
| D-16 | **일정 원소 모양 오류**: 과거 시술 · 예약 내역에서 KOS 고객 일정 원소의 모양이 깨져 처리할 수 없으면(묶음 · 시각 · 작업 칸의 타입이 다름) 원소를 건너뛰지 않고 그 요청을 `502 kos_unavailable` 로 낸다. `500` 으로 두지 않는다(서버 잘못이 아니라 KOS 응답 문제라는 뜻을 맞춘다). 본문 · 로그에 KOS 원문은 남기지 않는다. (2026-11-12 추가 — 코드 검수 add1 r1 N1) | 코디 기본값(코드 검수 add1 r1 N1 · 2026-11-12) |

### 이번 결정에 걸리지 않는 것 (열지 않음)

- **여러 그룹의 가능 시간대**: D-02 가 기본 그룹 하나로 정했다. 외부 예약도 그 그룹에만 들어간다(DEC-010 D-33).
- **운영 시간 밖 예약 막기**: 예약 생성은 지금처럼 운영 시간을 검사하지 않는다(SPEC-005 OQ-713 — KOS 가 거른다). 가능 시간대는 운영 구간 안 시각만 내지만, 그 밖 시각의 예약을 새로 막지 않는다.

## Consequences

- 연동처는 「언제 비었나 → 예약 → 예약 확인 · 지난 시술」을 직원 계정 없이 할 수 있다.
- KOS 비용(요청 1번당): 가능 시간대 = 공개 1번 · 과거 시술 = 내부 이름 검색 1번 + 공개 1번 · 예약 내역 = 내부 이름 검색 1번 + 공개 1번. 호출 제한은 키당 60초 60번을 세 경로와 기존 셋이 함께 쓴다(DEC-010 D-34).
- 가능 시간대 요청이 공유 슬롯 사본을 바꾸므로, 직원 예약 현황 판의 정원 표시도 그때 같이 새로워진다(동작 규칙은 바뀌지 않는다).
- 가능 시간대는 동시 요청 경합에서만 틀릴 수 있다. KOS 내부 예약 쓰기가 정원 초과를 거르는지는 확인되지 않았다(SPEC-005 OQ-760).

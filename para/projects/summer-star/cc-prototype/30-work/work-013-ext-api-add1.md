---
type: work
id: WORK-013
title: "외부 연동 API 2차(add1) — BE1 가능 시간대 → BE2 과거 시술 · 예약 내역 → BE3 Swagger · 시험 → REVIEW → 로컬 데모 실물 확인 → 배포 → 운영 실물 확인"
status: draft
product: cc-prototype
feature: procedure
work_type: enhancement
owner: kknaks
progress: 0
created_at: 2026-11-12
updated_at: 2026-11-12
tags:
  - product/cc-prototype
  - feature/procedure
  - doc/work
  - status/draft
links:
  baselines: []
  decisions:
    - "[[decision-011-ext-api-add1|DEC-011]]"
    - "[[decision-010-product-ext-api|DEC-010]]"
  specs:
    - "[[spec-008-product-ext-api|SPEC-008]]"
    - "[[spec-005-reservation-board|SPEC-005]]"
  works:
    - "[[work-012-product-ext-api|WORK-012]]"
  releases: []
  related: []
sources:
  - "para/projects/summer-star/cc-prototype/20-spec/spec-008-product-ext-api.md (0.3.2 · §6.6 ~ §6.9 · §9 T32 ~ T47)"
  - "para/projects/summer-star/cc-prototype/10-decision/decision-011-ext-api-add1.md (D-01 ~ D-16)"
  - "orchestration/work/api-swagger-docs/add1-spec-instructions.md"
  - "cc-prototype procedure/back main e0e4a16 (읽기만 — 대상 파일 · 줄)"
---

# 외부 연동 API 2차(add1) — 빌드 계획

계약은 **SPEC-008 0.3.2 §6.6 ~ §6.9** 에 있다. 이 문서는 빌드 순서만 적고 계약을 다시 쓰지 않는다. 결정은 DEC-011(D-01 ~ D-16)이고, 공유 규칙(인증 · 제한 · 기록 · 오류 · 고객 찾기)은 DEC-010 · WORK-012 로 이미 배포됐다(main `e0e4a16`). 화면은 없다.

## Meta

- **진행**: 문서만 있다. 코드는 아직 손대지 않았다. progress 0
- Covers spec: SPEC-008 0.3.2(§6.6 가능 시간대 · §6.7 과거 시술 · §6.8 예약 내역 · §6.9 KOS 비용 · §8 Swagger 0.3.0 줄 · §9 T29 고침 · T32 ~ T44). 0.2.3 까지의 계약(메뉴 · 조회 · 예약)은 바꾸지 않는다
- 코드 레포: `kknaksss/cc-prototype` — 범위는 **`procedure/back/**`** 하나다. front · app 은 건드리지 않는다
- **infra 없음**: 새 env 가 없다. 가능 시간대는 이미 있는 `KOS_EXT_RESERVATION_GROUP_ID` 를 쓴다. 새 표 · ingress 변경도 없다(`/api/ext/…` 안)
- base: 지금 main(`e0e4a16` 이후 운영본). 워크트리 · 브랜치는 코디가 정한다
- 워커: backend(BE1 ~ BE3 · 한 브랜치에서 차례로) · reviewer · 코디(실물 확인 · 배포)
- **검증 규칙**: WP 마다 **그 WP 의 시험만** 돌린다. 전체 `uv run pytest -q` 는 **BE3 끝에 한 번** 돌린다
- **실물 e2e 없이 done 금지**: 데모 KOS 로 가능 시간대 → 그 시각 예약 → 예약 내역에 보임 · 과거 시술을 실제로 부른다(WP-E2E-LOCAL) · 운영 호스트에서 연동처 키로 1번(WP-E2E-PROD)
- public 레포다 — 리포트 · 커밋 · 시험 데이터에 키 · 실명 · 이메일 · 연락처 · KOS id 값을 쓰지 않는다. 시험 값은 `<이름>` · `a@example.com` 꼴로만 쓴다

## 계약 고정점 (WP 사이에서 바뀌면 멈추고 코디에게)

| 고정점 | SPEC-008 | 쓰는 WP |
|---|---|---|
| 경로 셋 · 메서드(`GET …/availability?date=` · `POST …/customers/visits` · `POST …/customers/reservations`) | §6.6 ~ §6.8 머리 | BE1 · BE2 · BE3 |
| 가능 시간대 응답 `{date, intervalMinutes, slots[{start, remainingSeats}]}` · 후보 시각 · 남은 자리 규칙 · 날짜 범위 | §6.6 | BE1 |
| 슬롯 새로 읽기 = 요청마다 공개 슬롯 1번 → 공유 사본 바꿈 · 실패 502 | §6.6 3 | BE1 |
| 과거 시술 응답 `{visits[{date, start, result, procedures}]}` · 지금 앞 · 최신 순 · 50 | §6.7 | BE2 |
| 예약 내역 응답 `{reservations[{reservationId, date, start, end, state}]}` · 오늘 0시 이후 · 오름차순 | §6.8 | BE2 |
| 고객 찾기 = 지금 `ExtService.find` 하나(404 · 409 본문 조회와 같음) | §6.7 1 · §6.8 1 | BE2 |
| 오류 code(새 code 없음 — `invalid_request` · `customer_not_found` · `customer_ambiguous` · `kos_unavailable` · `ext_not_configured` + 공통) | §6.2 · §6.6 ~ §6.8 | BE1 ~ BE3 |
| 경로별 KOS 호출 수 | §6.9 | BE1 · BE2 · BE3 |

## Work Packages

| WP | 내용 | 계약 | 워커 | 대상 파일(범위) | 완료 조건 | 검증 명령(부분) | 상태 |
|---|---|---|---|---|---|---|---|
| **WP-BE1** | **예약 가능 시간대** — `GET /api/ext/availability`(질의 `date: str = Query(...)` 필수 · pydantic `date` 타입 금지 · 없음 = 지금 검증 규칙 `query.date: …`) · 날짜 검사(빈 문자열 먼저 400 · `YYYY-MM-DD` 숫자 꼴 + `fromisoformat` — ISO 주 날짜 등 400 · 오늘(KST) ~ 오늘 + 90일 · 그 밖 `400 invalid_request` · message `date: …`) · 기본 그룹 검사(예약과 같은 함수로 묶어 씀 — env 빔 · 그룹 없음 · 켜진 구역 0 → `503 ext_not_configured` · KOS 전) · `ResvSync.refresh_slots(day)`(지금 `_slots(groups, start, end, now)` 를 사본 `present` 그룹 전부 · 그날 KST 하루로 부르는 공개 함수 하나 · 실패는 예외 그대로 → 502 · `sync` 가 없으면 502) · 후보 시각(`open_spans` 안 · 자정 기준 간격 경계 · `m + 간격 ≤ 구간 끝` · 오늘이면 지금보다 뒤) · 남은 자리(켜진 구역별 `max(0, capacity − count)` 합 · 행 없음 · `capacity` null 구역 뺌 · 모두 없으면 시각 뺌 · 0 뺌) · `ExtAvailability` 모델(모든 칸 `description`) | SPEC-008 §6.6 · §6.9 | backend | `procedure/back/app/{api/ext.py,service/ext.py,schemas/ext.py,kos/reservation_sync.py}` · `tests/test_ext_availability.py` · `tests/fake_kos.py`(슬롯 응답을 시험이 정할 수 있게 — 이미 있으면 그대로) | SPEC-008 §9 T32 ~ T37 통과(T37 = 목록 시각으로 외부 예약 → `slot_full` 0 · 사본에 「참」이 남은 시각도 새로 읽은 뒤 예약됨) · `reservations.py` · `reservation_rules.py` diff 0(가져다 쓰기만) | `uv run pytest -q tests/test_ext_availability.py tests/test_ext_reserve.py tests/test_resv_board.py` | 대기 |
| **WP-BE2** | **과거 시술 · 예약 내역** — `POST /api/ext/customers/visits` · `POST /api/ext/customers/reservations` · 요청 `ExtCustomerRequest`(조회 요청과 같은 칸 · 같은 검증 — 지금 `ExtLookupRequest` 를 같이 쓰거나 같은 모양으로) · 고객 = `ExtService.find`(0명 → 조회와 같은 `NotFound` · 2명 → `customer_ambiguous` · 사본에 쓰지 않음 — `_keep` 부르지 않음) · 공개 `get-schedules-by-visitor` 1번(`resp.get("data", [])` — 키 없음 · `[]` = 빈 목록 200 · 있으면서 배열 아님 · 호출 실패 → 502 · `_data_list` 그대로 쓰지 않음) · 시작 = `schedule_start` · 원소 모양 오류는 요청 전체 502(원문 0 · DEC-011 D-16) · `deleted: true` 일정 뺌(고르기 함수 한 곳 · DEC-011 D-15) · 과거 시술(지금 앞 · 내림차순 · 50 · `result` = `PREV_RESULT` · `procedures` = 작업 title · 「방 배정」 ETCETERA 뺌 · 메모 · 의사 없음) · 예약 내역(오늘 KST 0시 이후 · 오름차순 · `state` = `state_of(status, flowStep)[0]` · `end` = `resources_of` 첫 묶음 끝 · `reservationId` = `reservation_id_of(일정 id)` 또는 null) · 응답 모델 둘 | SPEC-008 §6.7 · §6.8 · §6.9 | backend | `procedure/back/app/{api/ext.py,service/ext.py,schemas/ext.py}` · `tests/test_ext_history.py` · `tests/fake_kos.py`(고객 일정 — 지금 `history` · `resv` 그대로 쓰거나 시험이 지정) | §9 T38 ~ T43 · T45 ~ T47 통과(T45 경계 시각 · T46 일정 읽기 4xx · 401 → 502 · T47 원소 모양 오류 → 502 — 0.3.2)(T39 = 404 본문이 조회 404 와 바이트 같음 · 404 · 409 이면 일정 읽기 0번 / T40 = 외부 예약으로 만든 예약이 그 `reservationId` 로 나옴 / T41 = 오늘 겹침) · 고객 · 예약 사본 행 수가 요청 앞뒤 같음 | `uv run pytest -q tests/test_ext_history.py tests/test_ext_lookup.py tests/test_resv_detail.py` | 대기 |
| **WP-BE3** | **Swagger · 시험 정리** — 새 셋 `summary` · `description`(§8 0.3.0 줄 — 가능 시간대 규칙 · 「목록에 없어도 예약이 될 수 있다」 · 「그 사이 다른 예약이 끼면 `409 slot_full`」 · 날짜 범위 · 50건 · 메모 · 의사 없음 · `reservationId` null 뜻 · **오늘 겹침 문장** · KOS 호출 비용) · 응답 표(`- \`code\` — 언제`) · `openapi_docs.py` `DESCRIPTION` 「경로 셋」 줄을 여섯으로 · `tests/test_openapi_docs.py` `n_ops - 5 - 6` · `tests/test_ext_docs.py` `OPS` 여섯 · parameters 단언은 지우지 않고 `X-Api-Key`(header) + availability `date`(query)만 허용 · 「세 경로 합산」(`openapi_docs.py:85`) · 「세 엔드포인트 합산」(`api/ext.py:100` `EXT_RATE`) → 「외부 경로 전부 합산」(`git grep -n "셋\|세 경로\|세 엔드포인트" app/` 로 전부) · 새 셋 모두 `responses=errors(*COMMON, …)` · 공유 규칙 시험 T44 · **전체 시험 한 번** | SPEC-008 §8 · §9 T29 · T44 | backend | `procedure/back/app/{api/ext.py,openapi_docs.py,schemas/ext.py}` · `tests/{test_openapi_docs.py,test_ext_docs.py,test_ext_auth.py}` | T29 · T44 통과 · `/api/docs` 에 외부 여섯이 `외부 연동` tag 로 보임 · **전체 `uv run pytest -q` 통과(수치 리포트)** · `ruff`(레포 설정이 있으면) | `uv run pytest -q`(이 WP 끝에 한 번) | 대기 |
| **WP-REVIEW** | reviewer: SPEC-008 §6.6 ~ §6.9 · §8 · §9 T29 · T32 ~ T44 ↔ 코드 · 부록 D(DEC-011 D-01 ~ D-16) · 부록 E · 가능 시간대가 예약 생성과 같은 사본 · 같은 「꽉 참」 규칙을 쓰는지(T37) · 경로별 KOS 호출 수(§6.9) · 과거 시술 응답에 메모 · 의사 0 · 이름 · 이메일이 경로 · 질의 · `ext_call` · 로그에 0 · 404 바이트 같음 · `reservations.py` · `reservation_rules.py` diff 0 · 실명 · 키 grep. FAIL 은 모아서 한 번에 수정 발주 | 전체 | reviewer | 코드 변경 전체 | PASS | — | 대기 |
| **WP-E2E-LOCAL** | 코디: 백엔드 커밋 뒤 로컬 compose 를 재기동한다(옛 코드로 확인 금지) → **데모 KOS 실물**로 SPEC-008 §9 「실물 확인(0.3.0)」 ① ~ ④ — ① 하루 가능 시간대 ↔ KOS 웹 예약 현황(기본 그룹) 정원 · 예약 수 ② 목록 시각으로 외부 예약 1번 → 200 · 그 칸 `remainingSeats` 1 줄어듦 ③ 데모 email 보유 고객의 과거 시술 · 예약 내역 200 · ② 예약이 그 `reservationId` 로 보임 ④ 틀린 이메일 404 = 조회 404 본문. 그 밖에 키 없음 401 · 가능 시간대 어제 날짜 400 · 응답 시간(ms)을 리포트에 적는다. 끝나면 ② 예약을 직원 화면으로 취소한다 · 값은 기록하지 않는다 | SPEC-008 §9 「실물 확인(0.3.0)」 | 코디 · 사용자 | — | ① ~ ④ 확인 | — | 대기 |
| **WP-DEPLOY** | 코디: 코드 PR 머지 → back 이미지 → infra `back.imageTag` PR → sync · `/api/health` · `/api/docs` 에 외부 여섯 확인 | — | 코디 | — | 운영 back = 이 판 | — | 대기 |
| **WP-E2E-PROD** | 코디: **운영 호스트 `https://ccc.medisolveai.xyz`**(운영 조건 · Cloudflare 경유)에서 연동처 키로 가능 시간대 1번 · 과거 시술 · 예약 내역 각 1번(데모 고객) · 키 없음 401 · `ext_call` 행 확인. 예약은 하지 않는다(사용자가 원하면 1번 하고 취소). 협업자에게 새 경로를 알리는 것은 사용자 몫 | SPEC-008 §6.6 ~ §6.8 | 코디 · 사용자 | — | 운영 확인 끝 · 사용자에게 보고 | — | 대기 |

## 병렬

- BE1 ~ BE3 은 **한 워커가 한 브랜치에서 차례로** 한다. 셋 다 `api/ext.py` · `service/ext.py` · `schemas/ext.py` 를 고친다
- infra 작업이 없으므로 코드와 병렬로 할 일은 없다
- WP-REVIEW 는 BE3 끝 · 전체 시험 통과 뒤에 한다

## 주의

- **KOS 쓰기는 WP-E2E-LOCAL ② 에서만** 한다(데모 테넌트 · 운영 지점 키 금지). 새 세 경로는 KOS 를 **읽기만** 한다
- 가능 시간대는 **공유 슬롯 사본을 바꾼다**(DEC-011 D-12). 별도 캐시 · 별도 표를 만들지 않는다 — 예약 생성이 같은 사본을 봐야 D-02 가 선다. 날짜 캐시(`ensure` · 10초)와 하루 예약 조회는 부르지 않는다(비용 1번)
- (권장 · 문서 검수 add1 I2) `refresh_slots(day)` 는 **날짜 잠금 안에서** 부른다 — `ensure` 가 쓰는 같은 `_locks[day]`(`kos/reservation_sync.py:271`) 를 잡아, 같은 날짜의 하루 조회(`fetch_day` → `_slots`)와 사본 바꾸기가 겹치지 않게 한다
- 직원 서비스(`service/reservations.py`) · 규칙(`domain/reservation_rules.py`)은 고치지 않는다. 함수를 가져다 쓴다. `kos/reservation_sync.py` 에는 `_slots` 를 부르는 공개 함수 하나만 더한다(동작 무변경)
- 후보 시각은 운영 구간 안에서만 낸다. 예약 생성에 운영 시간 검사를 새로 넣지 않는다(DEC-011 「걸리지 않는 것」)
- 과거 시술 · 예약 내역은 고객 사본 · 예약 사본에 쓰지 않는다(`_keep` · `apply_schedule` 부르지 않음). 조회(§6.4)의 고객 사본 덮어쓰기와 다르다
- `reservationId` 가 null 인 일정을 사본에서 찾으려고 다른 칸(시각 · 고객)으로 추정해 잇지 않는다. 일정 KOS id 로만 찾는다
- 이름 · 이메일 · 키 값을 응답 · `ext_call` · 로그 · 리포트 어디에도 남기지 않는다(DEC-010 D-24 · public)

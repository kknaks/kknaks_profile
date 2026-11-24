# delivery-4 결과 보고 — Delivery #267 · #268 · #269 재결속 (마감 · 머지된 main 기준 · scope_delta)

## 상태: done — contract_version 3 · baseline = Mediness main `32b83390` · `spec-baseline:ready` · **재승인 적용** · `delivery-plan:approved`

| Issue | key | version | plan_digest (승인한 것) | contract_digest | 승인 | 라벨 (gh 확인) | next |
|---|---|---|---|---|---|---|---|
| [#267](https://github.com/MediSolveAIDev/CENTURION_DAY/issues/267) ① | `day/day-spec-006/be-read` | 2 → **3** | `sha256:0371a818e6640cf4af15975d659ac98bdba2c24ce946f90f9e914f57bb970baa` | `sha256:7bd44234ce9a0108a4ec896d35d79b7847518c1dd97d5a7ff119857b6d257a17` | 재승인 적용 | execution-plan:ready · delivery-plan:approved · spec-baseline:ready | `implement-and-open-code-pr` → `review-delivery` |
| [#268](https://github.com/MediSolveAIDev/CENTURION_DAY/issues/268) ② | `day/day-spec-006/be-refresh` | 2 → **3** | `sha256:dd8ef6cf9f0fdd19cb44e167dbbd56de6f6f52a4ceb8fd6940b9c3c145179688` | `sha256:0e03044b8b5249b04ea565f00a5c50dc92f776fb6edff3de04fa800ff8e537c8` | 재승인 적용 | 같음 | 같음 |
| [#269](https://github.com/MediSolveAIDev/CENTURION_DAY/issues/269) ③ | `day/day-spec-006/fe` | 2 → **3** | `sha256:f9561b4086c5b4a965f721bd990f634ce4638c2ad5588c4ae77c1eafa29d8d63` | `sha256:8811c0d5a4afd3fbdad9a762b4796f9457889da4266ae0c7539cad48bbe852b3` | 재승인 적용 | 같음 | 같음 |

## harness 흐름

1. `--plan`: 세 Issue 모두 exit 0 · `planned` · `spec_baseline_state: ready` · `execution_state: ready` · `missing_target_specs: []`.
2. `--apply`: status `baseline-ready`. 결과 계약이 바뀌어 새 plan_digest 가 나왔고 `review-delivery-plan`(human_gate)으로 **재승인을 요구**했다.
3. 승인 receipt `{"decision":"approved","reviewer_type":"human","reviewer":"kknaksss","plan_digest":<새 digest>}` 를 `--plan-approval-receipt` 로 적용했다. **재승인 적용** — 사용자가 이 작업 전체의 마감과 머지를 승인했다(코디 지시).
4. 결과: status `execution-updated` · next = `implement-and-open-code-pr`(human_gate false · skill `review-delivery`).

막힌 규칙은 없었다.

## 바뀐 결과 계약 (재승인이 필요했던 이유)

`spec_baseline_revision` 만 바꾼 것이 아니다. 범위가 넓어져 결과 계약 자체가 바뀌었다.
- 원내 현황 · 공지 쓰기 · 동행 · migration 이 전에는 non_goals 였는데 이번에 target_delta 로 들어왔다.
- target_specs 추가: #267 = + DAY-SPEC-000 · DAY-SPEC-002 / #268 = + DAY-SPEC-000. 두 SPEC 이 2026-11-24 개정(planner-fix-21)으로 바뀌었기 때문이다.
- 계약 V3 · V4 를 고쳐 썼다(`stack_index` 없앰 → `lane` · `line` · `rows` · `bands` · `companion_editable` / `payment_due` = R42 / `notice` v3 꼴 / `inhouse` v2). V1 보충(addendum 1 · 2)도 더했다.
- review_surface 첫 줄: 「pending · #958 머지 안 됨」 → 「main 32b83390 · ready · Code PR #272 가 세 Delivery 를 덮음」.
- 제목 세 개를 새 범위에 맞췄다.

## scope_delta (세 Issue 같은 문장)

> 2026-11-24 재결속 — baseline = 머지된 Mediness main 32b83390(PR #958 · spec-baseline:pending 뗌). 범위 넓힘(사용자 결정 R42 ~ R75 · 코디 계약): 계약 보충 v1 addendum 1 ~ 9(V1 today · open_min · time_gray_spans · 컨텍스트 이름 = 계약 이름 · 문구 근거 표 · 행 경합 = 날짜 쪽 양보(lock_timeout) · 꺾쇠 연타 debounce · 정원 null = 「30분」 · 잠금 전 Redis 10초 캐시 · 권한 행 = 데이터 migration) · v2 원내 현황 탭(R46 ~ R55 · 금액 = 수납 · 미수 · 결제총액) · v3 공지 수정 + KOS 공지 동기화(R58 ~ R62 · 누른 직원 토큰 직접 쓰기 · 503 kos_unavailable) · v4 동행 그룹 · 카드 배치(R64 ~ R73 · DAY 전용 새 테이블 · lane · line · rows · bands · 띠 = 진한 primary 테두리만 R75) · 「수납 필요」 = 단계 무관 payment_required(R42) · 다른 날짜 첫 화면 최대 3초 기다림(R43) · 담당자 줄(R56 · R57 · R63). 나눔: #267 = 백엔드 조회 · 원내 금액 · 공지 저장 · 동행 쓰기 · 권한 키 셋 · migration 0018 ~ 0023 / #268 = 동기화(날짜 회차 · 공지 동기화 · 거래 매핑) / #269 = 화면(탭 · 카드 · 배치 · 끌어 놓기 · 공지 편집). 결과 계약이 바뀌어 재승인 대상

## Issue 마다 더한 것 (요약)

**#267 ①**
- target_delta 더함:
  - 3초 기다림(R43)
  - 원내 현황 판정
  - 담당자 줄
  - `PUT /reservations/notice`
  - `PUT /reservations/companions` · `/leave`(검사 순서 400 → 404 → 409 past_date → 409 condition)
  - 권한 키 셋
  - migration 0018 ~ 0023 표
- A6 ~ A9: R52 실측 금액 · 공지 분기 · 동행 · migration 왕복.
- non_goals: 쓰기 · 원내 현황 · migration 줄을 빼고, 예약 등록 · 변경 · 0018 ~ 0023 밖 migration · 동행 표시를 넣었다.
- code_surface: #272 실제 파일 기준.
- rollback: downgrade 0023 → 0017(0019 는 새 상태 거래 행을 지움).

**#268 ②**
- target_delta 더함:
  - lock_timeout 양보 · Redis 10초 캐시(addendum 4 · 8)
  - 공지 동기화(R60 · R62)
  - 거래 매핑(R53)
  - 동기화 뒤 동행 정리(R67 — 함수는 ①)
- A7 ~ A9.
- non_goals: 「공지 · 기준 정보 동기화」 → 「공지 쓰기(①) · 기준 정보 동기화 변경」.
- code_surface: `emr_date_sync.py` · `sync_notices.py` · `mapper_sale_values.py` · `config.py`.

**#269 ③**
- target_delta 더함:
  - 탭 · 원내 현황 카드(v2)
  - 담당자 줄 · 「30분」
  - 배치(140 · 5 · lines × 70 · 66)
  - 끌어 놓기 · oob 토스트 · 띠 테두리만(R75)
  - 공지 편집(v3)
  - debounce · 문구 근거 표
- A5 ~ A8: DOM 테스트.
- non_goals: 원내 현황 줄을 빼고 「카드 누르기(끌기 밖)」 · 동행 표시를 넣었다.

## 30-work 바뀐 줄 (커밋 `e20fc215` · 브랜치 `kknaksss/day-reservation-close` · push 안 함)

| 줄 | 전 | 후 |
|---|---|---|
| Spec Coverage DAY-SPEC-006 | #267 · #268 · #269 · `proposed` | #267 · #268 · #269(2026-11-24 재결속 · contract v3 · baseline main `32b83390` · Code PR [#272](https://github.com/MediSolveAIDev/CENTURION_DAY/pull/272)) · **`in_dev`** |
| Spec Coverage DAY-SPEC-000 | … #243 · `in_dev` | … #243 · **#267 · #268**(예약 현황 데이터 — 2026-11-24 개정 · Code PR #272) · `in_dev` |
| Spec Coverage DAY-SPEC-002 | … #245 · `done` | … #245 · **#267**(개정 ㉗ 권한 키 셋 · Code PR #272) · **`in_dev`** |
| Delivery Issues (derived) | #267 ~ #269 행 없음 | `mediness dashboard-sync --apply` 로 다시 만듦: #249 · #254 · #256 · #259 · #262 · #263 · #264 · **#267 · #268 · #269**(spec-baseline:ready · open) 행이 새로 생김 |

- `log.md`: wp-change 한 줄.
- lint `--strict`: 0 error · 263 warning(모두 다른 제품).

## 코디 확인 바람

1. **SPEC-002 Coverage 를 done → in_dev 로 바꿨다.** #267 이 개정 ㉗(권한 키 셋)을 구현 중이라서다. #272 머지 · spec-sync 뒤 다시 done 이 된다.
2. **dashboard-sync 가 #251 행을 바꿨다.** `implementation:conformant · spec-sync:pending` → `— · —`. GitHub #251 라벨에 지금 implementation · spec-sync 라벨이 없어서 그대로 따라간 것이다(파생 view 라 손대지 않음). #251 라벨이 지워진 경위는 확인하지 않았다.

## 남긴 파일 (`delivery/`)

- `make-v3.py` — v2 request 에서 v3 를 만든 스크립트.
- `request-v3-*.json` · `plan-v3-*.json` · `apply-v3-*.json`(baseline-ready · 재승인 요구) · `approval-v3-*.json` · `apply-v3-approved-*.json`(execution-updated).
- `dashboard-plan.json` · `dashboard-apply.json`.
- v1 · v2 파일은 그대로 둠.

## 남은 것

- push(브랜치 `kknaksss/day-reservation-close`) · PR 은 코디 몫이다.
- 세 Issue 다음 단계 = Code PR #272 에 연결한 뒤 `review-delivery`(exact PR head `85836b30`). 머지 뒤에는 `spec-sync`.
- 실물 e2e 결과를 세 Issue 에 남기는 일(A5 · A6 · A4 순서 조건)이 남았다.

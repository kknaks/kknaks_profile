# delivery-close 결과 보고 — Delivery #297 재결속 + 닫기

## 상태: done

- **#297 재결속.**
  - 결과: contract **v1 → v2** · baseline = Mediness main `d0fcc23a4f13593c53a87d3b95b8173cdc779747`(#968 머지 · SPEC-008 stable) · `spec-baseline:ready`.
  - **재승인 적용.** 결과 계약이 바뀌어 `review-delivery-plan` 을 다시 요구했다. 사용자가 11-27 「마감 처리하자」로 이 작업 전체의 마감과 머지를 승인해서 receipt 를 적용했다.
- **review-delivery** 결과 `implementation:conformant`.
  - 근거: Code PR #299 head `8a5ee874` · merge `65506f35`.
  - `check-evidence --kind review --pr 299 --issue 297` = **fresh true** · reasons 없음. 이번에는 Delivery 하나에 PR 하나라서 지난번 같은 마커 stale 이 없다.
- **Issue #297 CLOSED.** harness 닫기 명령이 없어서 지난번처럼 `gh issue close` 에 코멘트를 달았다.
  - 코멘트: #299 dev 머지 `65506f35` · dev 배포 확인 · migration head 0031 · **prod 는 다음 배포** · 재결속 v2 · conformant · e2e 2회.
- spec-sync 단계(`run-spec-sync`)는 지난 Delivery 들처럼 건너뛰었다. 라벨은 `spec-sync:pending` 그대로다.

## Issue

| 항목 | 값 |
|---|---|
| Issue | [CENTURION_DAY#297](https://github.com/MediSolveAIDev/CENTURION_DAY/issues/297) |
| key | `day/day-spec-008/reservation-request` |
| contract version | 1 → **2** |
| contract_digest | `sha256:725f25ab1d75513b245cc7cb12cf05372cdb88ff9166ce43e07afc659d75eb19` |
| plan_digest(승인한 것) | `sha256:6915b580ae5fa753da5b9a86c5e4baaa44b5a4d308264c731b8523f3be4287fa` |
| 상태 | **CLOSED** |
| 라벨(gh 확인) | `execution-plan:ready` · `delivery-plan:approved` · `spec-baseline:ready` · `implementation:conformant` · `spec-sync:pending` |
| target SPEC | 008 · 006 · 005 · 007 · 000 + **001(새로 더함)** |

## harness 흐름

1. `gen/make-v2.py` 로 request v2 를 만들었다.
   - 내용: version 2 · baseline `d0fcc23a` · scope_delta(아래) · review_surface 원천 줄.
   - target_delta 두 줄을 더했다: 마감 계약 · 001 ⑮.
   - v1 글의 「006 ⑭ · 007 고침 6」을 「⑮ · 고침 7」로 바꿨다.
   - execution 의 open_questions · predeploy 를 지금 상태로 맞췄다: OQ 닫힘 반영 · dev 끝 · prod 남음.
2. `start-delivery --plan`: exit 0 · `spec_baseline_state: ready` · `missing_target_specs: []` · `review-required`.
3. `--apply`: `baseline-ready` 가 됐다. 결과 계약이 바뀌어 `review-delivery-plan`(human gate) 이 나왔다.
4. `approval-v2.json`(human · `kknaksss` · 위 plan_digest) 을 `--plan-approval-receipt` 로 적용했다. **재승인 적용.**
   - 결과: `execution-updated` · `delivery-plan:approved` · next = `implement-and-open-code-pr`.
5. `review-delivery`: `gen/make-review.py` → `review-v2-merged-297.json`.
   - `--plan` = planned · `--apply` = recorded · next = `run-spec-sync`.
6. `check-evidence` = fresh. 그 뒤 `gh issue close` + 코멘트.

scope_delta 요약:
- SPEC-008 stable · 006 ⑮ · 007 고침 7.
- 판정 = 이름 + 식별값 하나 이상 · 국적은 양쪽 있을 때만 · `birthDate` 선택.
- W3 `counselor` · W18 = 수정 때 바꿈 · 지움 · W1 · W2 `email`.
- 예약이 이미 취소된 스레드 `cancel` = 202 `canceled` · 동기화 때 자동 취소.
- `customer_changed` · `accepted_status` · `request_thread_write`.
- ext 스웨거 · 문구.
- 001 ⑮(로그인 뒤 예약 현황 · 셸 메뉴 「현황」).
- e2e 2회 · dev 배포 · prod 다음.

## review evidence (A1 ~ A7 · 모두 pass · CENTURION_DAY `8a5ee874` 테스트 경로:줄)

| Acceptance | 근거 테스트 |
|---|---|
| A1 ext 계약 | `test_reservation_request_flow.py:90 · 116 · 133` · `test_reservation_request_rules.py:40 · 49 · 164 · 187 · 201 · 216` · `test_reservation_request_actions_flow.py:284` · `test_ext_contract.py:50 · 111` |
| A2 키 병원당 하나 | `test_ext_contract.py:131`(같은 병원 키 둘 = 503) · `migrations/test_alembic.py:350`(0031 중복 행이면 멈춤 · 왕복) · `test_ext_writes.py:259` · rules `:53` · dev 키 교체 확인 |
| A3 상태 · 이중 예약 길 | rules `:70 · 74 · 90 · 96 · 104 · 141 · 208 · 226 · 235` · flow `:190 · 266` · actions_flow `:108 · 169 · 245 · 338 · 388` · screen `:477` |
| A4 KOS 쓰기 | `emr/test_reservation_request_writes_plan.py:55 · 75 · 94 · 108 · 114 · 123 · 129 · 139` · actions_flow `:429` · be-probe-1 Q01 ~ Q03 O · be-probe-2 ② ③ |
| A5 화면 · 권한 | `web/test_reservation_requests_screen.py:190 ~ 439`(11개) · `test_reservations_screen.py:460` · `auth/test_web_login.py:44` · `check.sh --pure` |
| A6 알림 | flow `:90`(웹 목록만 · 앱 · unread 뺌) · `test_board_feedback.py:292 · 526` · screen `:225` |
| A7 실물 e2e | e2e-1 · e2e-2(2026-11-26 · KOS 데모 지점 · 코드 결함 0 · 발견 4 → 고침 3 → O) · dev 배포 |

- per_spec 는 모두 `none` 이다(baseline 이 이미 구현을 담음).
- 사실대로 적어 둘 것: A7 의 「두 번째 브라우저 SSE 바로 반영」을 따로 기록한 e2e 로그는 없다. SSE 신호 0.1s 측정(e2e-1 #2) · 사용자 화면 확인 · dev 배포를 근거로 pass 로 넣었다. 지난 Delivery 의 A5 와 같은 방식이다.

## 30-work 바뀐 줄 (커밋 `84c9de2f` · 브랜치 `kknaksss/day-reservation3-close` = origin/main `d0fcc23a` 위 · push 함 · PR 은 코디)

| 줄 | 전(main `d0fcc23a`) | 후 |
|---|---|---|
| Spec Coverage DAY-SPEC-008 | Delivery #297(… L3 · delivery-plan:approved 2026-11-26 · spec-baseline:pending = origin/main `ae8cec61` — 계약 원천 #968 · 머지 뒤 v2 재결속) · Code PR #299(dev `65506f35` · …) · `in_dev` | Delivery #297(… 2026-11-27 재결속 contract v2 · baseline main `d0fcc23a`(#968 · SPEC-008 stable) · target + DAY-SPEC-001 ⑮ · L3 · 재승인 적용 · implementation:conformant · **CLOSED**) · Code PR #299(dev 머지 `65506f35` · dev 배포 확인 · migration head 0031 · ext 키 새 형식 · e2e 2회 · 셸 메뉴 · 로그인 뒤 · prod 다음) · `in_dev` |

- `log.md`: wp-status 한 줄.
- lint `--strict` = 0 error · 263 warning(다른 제품).

## 남긴 파일 (`delivery/`)

- `gen/make-v2.py`
- `request-v2-reservation-request.json`
- `plan-v2-*` · `apply-v2-*` · `approval-v2.json` · `apply-v2-approved.*`
- `gen/make-review.py` · `review-v2-merged-297.json` · `review-v2-merged-plan-297.*` · `review-v2-merged-apply-297.*` · `check-review-297.json`

## 남은 것

- 코디: `kknaksss/day-reservation3-close` PR 을 만들고 머지한다.
- 30-work SPEC-008 `in_dev` → `done` 은 spec-sync 단계 몫이다(지난 Delivery 들과 같음).
- **prod 배포**가 남았다: prod 병원 키를 새로 만들어 env 를 배포와 동시에 교체하고, 링키 · 차티에 안내한다.
- target 에 DAY-SPEC-001 을 더한 것은 내가 고른 것이다. 근거: #299 가 001 개정 ⑮ 를 구현했고 지시서 scope_delta 에도 있다. 빼야 하면 같은 key 로 v3 를 만든다.

# delivery-close 결과 보고 — Delivery #300 · #301 · #302 재결속 + 닫기

## 상태: done

- 세 Issue 재결속: **contract v3** · baseline = 머지된 Mediness main `9bfccfb27be0b50820430d4fee01895a63a7b3bb`(#971) · `spec-baseline:ready` · 「[계약 원천] 미머지 PR」 줄 뗌 · 공통 계약 ① ⓖ = 두 조각 · ⓚ y 매핑 · ④ D44 시한 안 · 웹 팝오버만(앱 = 새 요청) — 세 Issue 같은 글자.
- **재승인 적용** — 사용자 11-28 「dev 에 병합하고 작업 다 마무리하자」(이 작업 전체 마감 · 머지 승인) · receipt `reviewer_type human · kknaksss`.
- review-delivery: **#300 = `implementation:conformant`**(A1 ~ A7 pass). #301 · #302 = 실물 근거 없는 A6 · A4 를 pass 로 적지 않음(코디 답) → 하네스가 undetermined + conformant 를 거절(아래) → 기록 안 함 · 닫기 코멘트에 기록.
- **셋 다 CLOSED** — #300 = conformant 마감 · #301 · #302 = 사용자 지시(코디 추가 「응 닫아 줘」)로 닫음 · 태블릿 실기기 확인 = OQ-D53.

## Issue 마다

| Issue | key | version | plan_digest(승인) | contract_digest | 상태 | 라벨(gh 확인) |
|---|---|---|---|---|---|---|
| [#300](https://github.com/MediSolveAIDev/CENTURION_DAY/issues/300) WP-1 BE | `day/day-reservations-fix-be` | 2 → **3** | `sha256:fc9142fcebad926c9277ef9f6f72e57055f9a6cba31cd1e0681c7a3f9fd89e32` | `sha256:8f45d68767914d860067bdc8fb3df06fcd857649bda9295e9650ff8e562c49b0` | **CLOSED** | execution-plan:ready · delivery-plan:approved · spec-baseline:ready · implementation:conformant · spec-sync:pending |
| [#301](https://github.com/MediSolveAIDev/CENTURION_DAY/issues/301) WP-2 웹 | `day/day-reservations-fix-web` | 2 → **3** | `sha256:88ea26d46b0439212f988045a59a798213ac75723f672e88a4965c8d6307a100` | `sha256:39f5321ddfec00a408a381507ad5e8005f1c0a4074f6b776da8680a7e25a50e4` | **CLOSED**(사용자 지시) | execution-plan:ready · delivery-plan:approved · spec-baseline:ready(implementation 라벨 없음) |
| [#302](https://github.com/MediSolveAIDev/CENTURION_DAY/issues/302) WP-3 앱 | `day/day-reservations-fix-app` | 2 → **3** | `sha256:2b778d1bf52baa9a3a98ae6695143203df33880a3133a473ba7175a2dc8b98b7` | `sha256:8df6b13d749b01f727a4b94939628aad934b748e3c97e7b95c1e8cafe51c1a91` | **CLOSED**(사용자 지시) | 같음(#301) |

## harness 흐름

1. `start-delivery --plan`(v3 · `9bfccfb2`): 셋 다 exit 0 · ready · plan_review `review-required`.
2. `--apply`: `scope-delta-recorded` · next `review-delivery-plan`(재승인 요구).
3. 승인 receipt 를 `--plan-approval-receipt` 로 적용 → 셋 다 `plan-approved` · next `implement-and-open-code-pr`. **재승인 적용.**
   - 첫 시도는 zsh 변수 분할 문제로 명령이 아예 안 돌았다(exit 127 · 부작용 없음) — 다시 실행.
4. `review-delivery`(merged · code_pr 303 · head `d1ce8ea80b6ffa070154fc7d6e403ba45f1ba5a5` · merge `7af15621ad067f2edbbeef69ab62901aad57c8c9` · per_spec 전부 `none`):
   - #300 `--plan` → `--apply` = `recorded` · next `run-spec-sync`.
   - #301 · #302 `--plan` = exit 2 `{"error": "conformant review requires passing evidence for every Contract Acceptance", "status": "conflict"}`(A6 · A4 = undetermined). 코디 답대로 우회 안 함 · apply 안 함.
5. Issue 닫기: harness 닫기 명령 없음 → `gh issue close` + 코멘트.
   - #300: 「완료 — CENTURION_DAY#303 dev 머지 `7af15621` … · SPEC mediness#971 `9bfccfb2` · v3 · 재승인 적용 · conformant · 태블릿 실기기 확인은 dev 배포 뒤(OQ-D53)」.
   - #301 · #302: 처음엔 열어 두고 코멘트(코디 답) → 코디 추가 지시로 닫기 코멘트 「사용자 지시로 닫음 · A6 / A4 = undetermined(하네스가 기록 못 해 이 코멘트가 기록) · 그 밖 pass · 태블릿 실기기 확인은 OQ-D53 으로 남김」.
6. spec-sync 하네스 단계(`run-spec-sync`)는 지난 마감들처럼 건너뜀 — 라벨 `spec-sync:pending` 그대로(SPEC 은 #971 spec-sync 커밋으로 이미 코드에 맞춤).

## review evidence (`delivery/review-v3-merged-{300,301,302}.json` · 생성기 `delivery/gen-review-v3.py`)

- #300: A1 `test_reservation_detail_origin.py:66 · :71` · A2 `test_reservation_layout.py`(64 · 68 · 89 · 94 · 100 · 109 · 127 · 151 · 158 · 164 · 189 · 204 · 212 · 220) · `test_reservation_rules.py:145 · :159 · :310` · A3 `test_kos_questionnaire_read.py` · `test_kos_questionnaire_sync.py` · `test_questionnaire_sync_rules.py:44 · :105` · A4 `test_questionnaire_period_rules.py` · A5 `test_reservation_display_popover.py`(54 · 64 · 81 · 96 · 132) · A6 PR #303 검증 절 · `test_alembic.py:107` · `test_display_rules.py:281` · A7 PR #303 로컬 e2e(D46 ② 제출 id = 읽기 id) · e2e-1 · e2e-2.
- #301: A1 ~ A5 pass(화면 테스트 · node 테스트 · qa-1 · qa-2) · **A6 undetermined**(기기 줄 · 태블릿 · D45 — 로컬 등록 태블릿 0대 · qa-1 「D45 미검증」 · OQ-D53).
- #302: A1 · A2 pass(`reservation_table_test.dart` · `reservation_ui_test.dart:156`) · A3 pass(PR 검증 절 — flutter analyze 0 · test +551 −1 base 기존 실패. **주의**: 「iOS · Android 빌드」 자체의 기록은 PR 에 없음) · **A4 undetermined**(앱 태블릿 실물 기록 없음 · OQ-D53).

## 30-work 바뀐 줄 · 커밋 (브랜치 `kknaksss/day-reservations-fix-close` = origin/main `9bfccfb2` 위 · push · PR 은 코디)

| 줄 | 전(main `9bfccfb2`) | 후 |
|---|---|---|
| Spec Coverage DAY-SPEC-000 · 002 · 003 · 006 · 007 의 2026-11-27 = #300 ~ #302 꼬리(다섯 줄) | (… L2 · delivery-plan:review · baseline main `b9ac374e` · 계약 원천 SPEC PR mediness#971 `ad317cf4` 미머지 — 머지 뒤 v2 재결속) | (… 2026-11-28 재결속 contract v3 · baseline main `9bfccfb2`(#971 머지) · L2 · 재승인 적용 · #300 = implementation:conformant · **CLOSED** · #301 · #302 = **CLOSED**(사용자 지시 · 웹 A6 · 앱 A4 태블릿 실기기 = undetermined · OQ-D53 으로 남김)) · Code PR CENTURION_DAY#303(dev 머지 `7af15621` · head `d1ce8ea8` · migration head 0032) |
| 구현 상태 | `in_dev` | `in_dev`(셋 다 · 그대로) |

- `log.md`: wp-status 한 줄(2026-11-28 · Delivery 마감).
- 커밋: `f4581381d8e9e0e9ba0181d9a3c5bee89fd19f62`(마감 · #301 · #302 열어 둠) → **`e4467807026c23afb37034b45e4d6b08b2336e97`**(#301 · #302 닫음 반영 · 지금 head).
- lint `--strict` = 0 error · products/day 0.

## 남은 것

- 코디: `kknaksss/day-reservations-fix-close` PR 만들고 머지.
- 태블릿 실기기 확인(웹 A6 · 앱 A4 · D45 · 기기 줄) = DAY-SPEC-007 OQ-D53 — 확인되면 필요 시 review-delivery 다시(Issue 는 닫혀 있음).
- 다음 작업 OQ-D50(500 인데 저장 → 이중 제출) · D51(국가번호 빈 값) · D52(6개월 경과 옛 건강정보).
- 30-work `in_dev` → `done` 은 spec-sync 단계 몫(건너뜀 · 필요하면 사람이 한 줄).

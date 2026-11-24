# delivery-close 결과 보고 — Delivery #275 · #276 · #277 · #278 재결속 + 닫기

## 상태: done

- 네 Issue 모두 다시 결속했다: contract v2 · baseline = Mediness main `29480cfd9062e4d40ab0d273874ac42193dce98d`(#961 · #962 머지 · SPEC-007 stable) · `spec-baseline:ready`.
- **재승인 적용** — 사용자가 이 작업 전체의 마감과 머지를 승인했다.
- review-delivery 결과는 `implementation:conformant` 다(Code PR #280 head `a0b42a36` · merged `55e60aa4`).
- **네 Issue 모두 CLOSED.** 지난 #267 ~ #269 와 같은 상태다.

## Issue 마다

| Issue | key | version | plan_digest (승인한 것) | contract_digest | 상태 | 라벨 (gh 확인) |
|---|---|---|---|---|---|---|
| [#275](https://github.com/MediSolveAIDev/CENTURION_DAY/issues/275) 1판 예약 | `day/day-spec-007/p1-reservation` | 1 → **2** | `sha256:16981d131fd84ce1755d1e311f0504042fbfc7a9a6abc7b8c374c8b03a7bbd90` | `sha256:39bbb8bc5d5806f1076c8e01a246f2eb35a977ee226d839f67be9666ce894999` | **CLOSED** | execution-plan:ready · delivery-plan:approved · spec-baseline:ready · implementation:conformant · spec-sync:pending |
| [#276](https://github.com/MediSolveAIDev/CENTURION_DAY/issues/276) 2판 접수 → 상담 | `day/day-spec-007/p2-reception` | 1 → **2** | `sha256:39ae9571092f33805f6cd4d93859c01a64526ac05b7270d7f35f751315b745ec` | `sha256:3ac809d731b2151b5c61b9851122f7a4e4603f0c4deecadf21f3048c0e27d7f8` | **CLOSED** | 같음 |
| [#277](https://github.com/MediSolveAIDev/CENTURION_DAY/issues/277) 3판 시술 | `day/day-spec-007/p3-procedure` | 1 → **2** | `sha256:2f031434d723f7157b1acb9cf738efc16e9c9ca02a952905a246c1b04d9fd3a1` | `sha256:7a3dc32daec22ac411453bbe67bb0864067d6b2df7df7f42544c4661557588e9` | **CLOSED** | 같음 |
| [#278](https://github.com/MediSolveAIDev/CENTURION_DAY/issues/278) 4판 귀가 | `day/day-spec-007/p4-discharge` | 1 → **2** | `sha256:495e1cc9c14155cfc77d2ab7083d37a16295a0fd171f25c3ea519640f3fbb3fc` | `sha256:5fdbd54ef6855720ebebb3d70a736f01e41bcb90762854f49c7a54358b8b2c8f` | **CLOSED** | 같음 |

## harness 흐름

1. **앞 판 막힘**: `ea283f0c` 기준으로는 `missing_target_specs = [DAY-SPEC-007]`(draft)였다. 코디 결정 A 로 SPEC-007 을 stable 로 올리는 #962 를 머지해 풀었다.
2. `start-delivery --plan`(`29480cfd`): 넷 다 exit 0 · `spec_baseline_state: ready` · `missing_target_specs: []` · plan_review `review-required`.
3. `--apply`: `baseline-ready`. 결과 계약이 바뀌어(scope_delta · target_delta 고침 4 줄 · ㉙) `review-delivery-plan` 재승인을 요구했다.
4. 승인 receipt(`reviewer_type human` · `kknaksss` · 위 plan_digest)를 `--plan-approval-receipt` 로 적용했다. **재승인 적용.**
   - 결과: #275 = `plan-approved` · #276 ~ #278 = `execution-updated`.
   - next = `implement-and-open-code-pr`.
5. `review-delivery`(merged · code_pr 280 · head `a0b42a3618e7bc271c42b03c3029266a30ac41ec` · merge `55e60aa4d6f3be048bc7e933ee5dbd5f74456bfc`):
   - `--plan`: 넷 다 planned.
   - `--apply`: 275 → 276 → 277 → 278 차례로 했고 넷 다 `recorded`.
   - next = `run-spec-sync`. 라벨 `implementation:conformant` · `spec-sync:pending`.
6. Issue 닫기: harness 닫기 명령이 없다(지난번과 같음). 그래서 `gh issue close` 에 코멘트를 달았다:
   - 「완료 — CENTURION_DAY#280 dev 머지 `55e60aa4` · dev 배포 확인 · migration head `0028_visit_discharge_reason`. 스펙 mediness#961 · #962 main 머지(`29480cfd` · DAY-SPEC-007 stable). 재결속 contract v2 · review-delivery conformant(PR head `a0b42a36`). …」

## 규칙대로 보고 — review evidence 마커는 PR 마다 하나

`check-evidence --kind review --pr 280` 결과:

| Issue | fresh | reasons |
|---|---|---|
| #275 | false | managed review evidence links are stale · contract digest is stale |
| #276 | false | 같음 |
| #277 | false | 같음 |
| #278 | **true** | — |

- PR 댓글 마커 `mediness:delivery-review-evidence:v1` 는 PR 마다 하나만 upsert 된다. 그래서 마지막으로 apply 한 #278 것만 남는다. 순서를 바꿔도 마지막 하나만 fresh 가 된다.
- 지난 review-delivery-3 막힘 ① 과 같은 원인이다. 「1 Delivery = 1 Code PR」 규칙인데 #280 하나가 Delivery 넷을 덮는다.
- 우회(마커 손으로 고치기 · 반복 apply)는 하지 않았다. Issue 쪽 closeout 마커 · 라벨은 넷 다 있다.
- spec-sync harness 단계(`run-spec-sync`)는 지난번(#267 ~ #269)처럼 건너뛰고 닫았다. 라벨은 `spec-sync:pending` 그대로다.

## review evidence (Acceptance A1 ~ A5 · 넷 다 pass)

- A1 ~ A4: CENTURION_DAY `55e60aa4` 의 테스트 경로:줄.
  - `test_reservation_detail_screen.py`
  - `test_reservation_detail_stages_screen.py`
  - `test_reservation_writes_plan.py`
  - `test_outbox_reservation_rules.py`
  - `test_reservation_confirm_loop.py`(D53)
  - `test_reservation_care_rules.py`
  - `test_reservation_stream.py`
  - `test_reservation_signal_rules.py`(B41)
  - `test_detail_permission_migration.py`
  - `test_alembic.py`
  - `test_screen_copy.py`
  - 그리고 `scripts/check.sh` 전체 통과(PR #280 검증 절).
- A5(실물 e2e): 사용자 화면 확인(로컬 KOS 데모 지점 · e2e-1-feedback B1 ~ B41 고침) + PR #280 「검증」 절 + dev 배포 success.
- 사실대로 적어 둘 것: A5 문장의 「두 번째 브라우저 SSE 반영」 · 판마다 「KOS 상세 다시 읽기 expect」를 따로 기록한 e2e 로그는 없다. 사용자 화면 확인과 PR 검증 절을 근거로 pass 로 넣었다.
- per_spec 는 모두 `none` 이다(baseline 이 이미 구현을 담음).
- 생성 스크립트: `delivery/gen/make-review.py`.

## 30-work 바뀐 줄 (커밋 `a487564c` · 브랜치 `kknaksss/day-reservation2-close` = origin/main `29480cfd` 위 · push 함 · PR 은 코디)

| 줄 | 전(main `29480cfd`) | 후 |
|---|---|---|
| Spec Coverage DAY-SPEC-007 | #275 ~ #278(2026-11-24 · L3 · 재결속 = SPEC-007 stable 머지 뒤 새 main 으로(contract v2 · plan 은 `ea283f0c` 로 돌려 봄) · …) · Code PR #280 · `in_dev` | #275 ~ #278(2026-11-24 재결속 · contract v2 · baseline main `29480cfd`(SPEC-007 stable) · L3 · implementation:conformant · **CLOSED** · 1판 화면 확인 B1 ~ B41 …) · Code PR #280(dev 머지 `55e60aa4` · dev 배포 확인 · migration head 0028) · `in_dev` |

- `log.md`: wp-status 한 줄.
- lint `--strict` = 0 error(263 warning 은 다른 제품) · products/day 0 / 0.
- 앞 커밋 `3fe9e1aa`(SPEC-007 stable)는 #962 로 main 에 들어가 있다. 그래서 close 브랜치를 origin/main 위로 다시 세워 이번 변경만 담았다.

## 남긴 파일 (`delivery/`)

- `gen/make-v2.py`(BASE = `29480cfd`) · `request-v2-*.json`.
- `plan-v2-*`(ea283f0c · pending · 참고) · `plan-v2b-*`(29480cfd · ready).
- `apply-v2-*` · `approval-v2-*` · `apply-v2-approved-*`.
- `gen/make-review.py` · `review-v2-merged-{275..278}.json` · `review-v2-merged-plan-*` · `review-v2-merged-apply-*` · `check-review-*.json`.

## 남은 것

- 코디: `kknaksss/day-reservation2-close` PR 을 만들고 머지한다.
- 30-work SPEC-007 `in_dev` → `done` 은 spec-sync 단계 몫이다(지난 SPEC-006 과 같음). 그 단계를 건너뛰었으니, 필요하면 사람이 한 줄 고친다.
- B42(SSE 연결 한도)는 열림이다 · SPEC-007 OQ-D26 · SPEC-006 OQ-R39.

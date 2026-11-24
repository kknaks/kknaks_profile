# delivery-2 결과 보고 — SPEC-006 Delivery 3개 발행 (spec-baseline:pending · 승인 적용)

## 상태: done

## Issue

| # | Issue | 제목 | 라벨(발행 뒤 · gh 확인) | 승인 |
|---|---|---|---|---|
| ① | [CENTURION_DAY#267](https://github.com/MediSolveAIDev/CENTURION_DAY/issues/267) | DAY 예약 현황(조회) ① 백엔드 — 조회 라우트 · 화면 값 · 권한 키 (DAY-SPEC-006) | `delivery-plan:approved` · `execution-plan:ready` · `spec-baseline:pending` | plan_digest `sha256:0025b6be…d267` |
| ② | [CENTURION_DAY#268](https://github.com/MediSolveAIDev/CENTURION_DAY/issues/268) | DAY 예약 현황(조회) ② 백엔드 — 다른 날짜 최신화 중앙 작업(R40 · 잠금 · C1 ~ C3) (DAY-SPEC-006) | 같음 | plan_digest `sha256:380c3926…2a96` |
| ③ | [CENTURION_DAY#269](https://github.com/MediSolveAIDev/CENTURION_DAY/issues/269) | DAY 예약 현황(조회) ③ 화면 — Jinja2 + HTMX 템플릿 · day.js (DAY-SPEC-006) | 같음 | plan_digest `sha256:e0bf7411…a53` |

- 셋 다 `risk_level: L2` · `contract_version: 1` · OPEN.
- 범위 · 의존 · 완료 조건 · BE↔FE 계약은 delivery-1 보고서 그대로(request 의 결과 계약 · execution 을 바꾸지 않음 — baseline SHA 와 review_surface 첫 줄만 바꿈).

## baseline

- `spec_baseline_revision` = Mediness `origin/main` **`8aef9206036d076798242ca66abd30d644762180`**(이번에 fetch) · `spec_baseline_state = pending` · `missing_target_specs = [DAY-SPEC-006]` — harness 가 「target SPEC 이 main 에 없음」으로 판단(DAY 첫 Delivery #224 ~ #226 과 같은 방식 · #226 metadata `spec_baseline_state=pending` · `missing_target_specs.0=DAY-SPEC-000` 확인).
- **SPEC 원천 표기**: 세 Issue 의 Review Surface 첫 줄 — 「SPEC 원천 = DAY-SPEC-006(사용자 승인 · stable) — Mediness PR #958 커밋 `1870f68cd23633776a228d4c28e78f68a593cbca`(브랜치 `kknaksss/day-reservation-spec`). main 에 아직 없어 spec-baseline:pending 으로 시작한다. SPEC-006 이 Mediness main 에 들어가면 같은 idempotency key · contract_version +1 · 새 origin/main SHA 로 재실행해 spec-baseline:ready 로 재결속한다(결과 계약 의미가 같으면 재승인 없음 — requests.md)」. #267 본문에 `1870f68c` · `PR #958` 이 들어간 것 확인.

## 승인 상태

- 사용자 승인(코디 전달 · 2026-11-23)을 receipt 로 적용: `{"decision":"approved","reviewer_type":"human","reviewer":"kknaksss","plan_digest":"<각 Issue 의 plan_digest>"}` → `--plan-approval-receipt` 로 재 apply → `status: plan-approved` · 라벨 `delivery-plan:approved`.
- reviewer 값 = 이 레포 git 사용자 핸들 `kknaksss`(사용자 본인 — 코디가 사용자 승인이라고 전달). 다른 값이어야 하면 같은 receipt 꼴로 다시 적용하면 된다.

## 다음 행동 (harness `next_action`)

- 세 Issue 모두 `prepare-spec-baseline`(human_gate: false · when: stable-spec-ready) — **구현(`implement-and-open-code-pr`)으로 가려면 baseline 을 ready 로 재결속해야 한다.**

## 재결속 조건 (규칙 — `tools/harness/references/requests.md` · `rules/delivery-workflow.md`)

1. DAY-SPEC-006(stable)이 Mediness `origin/main` 에 들어간다(PR #958 은 사용자 결정으로 지금 머지하지 않음 — 들어가는 길은 사용자 · 코디 몫).
2. 그 뒤 같은 request 파일로: `idempotency_key` 그대로(`day/day-spec-006/be-read` · `be-refresh` · `fe`) · `contract_version` = 2(직전 +1) · `spec_baseline_revision` = 새 `origin/main` SHA → `start-delivery --plan` → `--apply`.
3. 결과 계약 의미가 같으면 재승인 receipt 는 필요 없다(「baseline 승격은 결과 계약이 같으면 기존 권한 상태를 유지」). Target Delta · Acceptance · Non-Goals · Review Surface 를 바꾸면 `scope_delta` + 새 승인 필요.
4. 주의: 재결속 전에 구현을 시작하면 harness 상태와 어긋난다 — 코드 착수 순서는 코디 판단.

## 남긴 파일 (`orchestration/work/day-reservation/delivery/`)

| 파일 | 내용 |
|---|---|
| `request-{be-read,be-refresh,fe}.json` | 바뀐 request(baseline = `8aef9206` · Review Surface 첫 줄 = SPEC 원천 · 재결속) |
| `plan-{…}.json` | `--plan`(status planned · pending · review-delivery-plan) |
| `apply-{…}.json` | 첫 `--apply`(status created · Issue 번호) |
| `approval-{…}.json` | 승인 receipt |
| `apply-approved-{…}.json` | receipt 적용 `--apply`(status plan-approved · next = prepare-spec-baseline) |

- 첫 시도에서 셸 변수 분리 실수로 `--plan`/`--apply` 가 옵션 오류(exit 2 · 「No such option」)로 끝났다 — 아무것도 만들어지지 않았고(출력 파일만 덮어씀) 바로 다시 실행했다.

## 문서 변경 (커밋 안 함)

- `products/day/30-work.md` Spec Coverage: `| DAY-SPEC-006 | [Delivery #267] · [#268] · [#269] | proposed |`(구현 전 · lint 값).
- `products/day/log.md` 한 줄(`wp-add` · #267 ~ #269 발행 · pending baseline · 재결속 조건).
- `30-work.md` 의 Delivery Issues(derived) 표는 손대지 않았다 — spec-sync 가 갱신하는 derived view.
- lint `--strict`: exit 0 · 0 error · 263 warning(타 제품 기존 · products/day 0).

## 미결 · 주의

- SPEC-006 이 main 에 들어가는 길(#958 을 언제 · 어떻게)이 재결속의 선행 조건.
- MCP Task projection 은 하지 않음(브리프 범위 밖 · best-effort).

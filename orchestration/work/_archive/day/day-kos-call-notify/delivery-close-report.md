# delivery-close 결과 — 상태: done

## 최종 (코디 답 뒤 · A10 = prod 실물로 pass)

- **3 review-delivery**: A10 evidence 에 세 가지를 적고 A1 ~ A10 전부 pass 로 했다.
  - e2e-1 실물 결과
  - prod 실물: KOS 호출 3건 · kind all · 각 알림 5행 · 사용자 「맞아 · 모니터링 중」
  - 잔여: 푸시 실기기(push_log 0 · 기기 세션 없음 · 기존)
  - 결과: `--plan` planned → `--apply` **recorded** · next `run-spec-sync`.
  - `check-evidence --kind review`: `fresh: true` · reasons [] (`delivery/check-review-283.json`).
- **4 30-work · log**:
  - 바꾼 줄: Spec Coverage DAY-SPEC-002 · 005 의 #283 줄 — 「proposed · 승인 대기」 → 재결속 v2 · baseline `bf440f27` · conformant · CLOSED · Code PR #285(dev `1b5bba22` · prod 배포 · prod 실물 알림 행 · 푸시 실기기 잔여). log 에 wp-status 한 줄을 더했다.
  - 커밋 · push · PR: 커밋 `6f3f807c` · 브랜치 `kknaksss/day-kos-call-notify-close`(origin/main `bf440f27` 위) · push 함 · PR [mediness#966](https://github.com/MediSolveAIDev/mediness/pull/966)(머지 안 함 — 코디).
  - lint `--strict`: 0 error · products/day 0 줄.
  - Delivery derived 블록은 dashboard-sync 몫이라 손대지 않았다.
- **5 #283**: 마감 댓글을 달고 닫았다.
  - 댓글 내용: 코드 #285 · prod 배포 · 스펙 #965 · 재결속 v2 · conformant · e2e-1 · prod 실물 · 잔여 푸시.
  - 상태(gh 확인): **CLOSED(completed)** · 라벨 execution-plan:ready · delivery-plan:approved · spec-baseline:ready · implementation:conformant · spec-sync:pending.
  - 참고: review-delivery `--apply` 가 이미 닫힌 #283 을 다시 OPEN 으로 만들었다. 그래서 이 단계에서 다시 닫았다.
- **남은 것**:
  - spec-sync 단계(`run-spec-sync`)는 선례처럼 건너뛰었다. 라벨은 `spec-sync:pending` 이고, 30-work 의 002 · 005 구현 상태 `in_dev` 도 그대로다.
  - 푸시 실기기 확인.
  - PR #966 머지(코디).

---

(아래는 막혔던 1차 기록)


## 1. 워크트리 — done
- origin/main `bf440f27`(#965 스쿼시) 위에 새 브랜치 `kknaksss/day-kos-call-notify-close` 를 만들었다. 아직 커밋은 없다.

## 2. #283 재결속 v2 — done · 재승인 없음
- 요청: `delivery/wp1-be-request-v2.json`. v1 에서 바꾼 것은 셋뿐이다.
  - `contract_version` 2
  - `spec_baseline_revision` `bf440f270ffdaaabcbed77415ca403df90e4c172`
  - `scope_delta`: #965 머지 · v1 caveat 해소 · sync-1 다듬은 규칙 요약 · 구현 #285
- target_delta · acceptance · non_goals · review_surface · risk 는 그대로다.
  - harness `delivery_plan_digest`(`workflow.py:318-328`)는 이 다섯만 보고 baseline 은 보지 않는다.
  - 그래서 plan_digest = `sha256:61ce7c7084c3cb6f086267e0293161191f0143df3e8d1fe216c699915992c547`(v1 승인값과 같음) → 기존 승인 receipt 가 그대로 이어진다.
  - 결정: 계약 같음 → 재승인 없음.
- `--plan`(`wp1-be-plan-v2.json`): planned · `spec_baseline_state: ready` · `missing_target_specs: []`.
- `--apply`(`wp1-be-apply-v2.json`):
  - `status: scope-delta-recorded` · plan_review `approved`(kknaksss · 같은 digest)
  - contract_digest `sha256:bba7deda30ba1817db8fbaceb0c401f4d46544f70cb276474fe12a333c9c77c6`
  - next `implement-and-open-code-pr`
  - `partial: true`(Task projection 미연결 · v1 과 같음)
- 라벨(gh 확인): `execution-plan:ready` · `delivery-plan:approved` · `spec-baseline:ready`.
- 참고: v2 target_delta 첫 줄 「[계약 원천] … 미머지 · 재결속 예정」 문장은 plan_digest 를 지키려고 그대로 두었다. 해소 사실은 scope_delta 에 적었다.
- 참고: #283 은 이미 **CLOSED(completed)** 다. PR #285 본문의 `Closes #283` 때문에 머지 때(2026-11-25 05:05:20Z) 자동으로 닫혔다.

## 3. 구현 결속 review-delivery — 막힘
- 요청: `delivery/review-v2-merged-283.json`. 생성기는 `gen/make-review.py` 다.
  - code_pr 285 · head `af07e9d765c0de3a7344ca23f9ee73b4791a3601` · merge `1b5bba225e82fa6e0d777752b76d39eb37a44947`
  - per_spec 002 · 005 = none
- A1 ~ A9 = pass. 근거는 merge `1b5bba22` 의 시험 경로:줄이다.
  - 시험 파일: `test_kos_call_rules.py` · `test_kos_calls.py` · `test_kos_calls_flow.py` · `test_kos_calls_races.py`
  - 전체 2909 passed
- **A10 = undetermined.** A10 문장은 「실물 1회 → DAY 알림 행(DB) · 웹 OS 알림 · iPad 시뮬레이터 앱 표시를 증거로」인데, 셋 다 증거가 없다.
  - DAY 알림 행: DEMO 원장 10명 모두 DAY 계정이 없어 받는 사람이 0이었다(e2e-1 「환경 · 미검증」).
  - 웹 OS 알림 · iPad: e2e-1 은 보지 않았다.
  - prod 실물(간호가 KOS 에서 이건학 지정 호출 → 알림): `_RESUME.md` 에 아직 `[ ]` 이다.
  - 호출 생성 · OQ-99 · OQ-106 은 실물로 닫혔다.
- `review-delivery --plan` 결과(exit 2 · `review-v2-merged-plan-283.json`) 원문:
  ```
  {"error": "conformant review requires passing evidence for every Contract Acceptance", "status": "conflict"}
  ```
- A10 을 pass 로 쓰면 지나가지만, 그것은 우회라 하지 않았다. `--apply` · PR #285 evidence 마커 · `implementation:*` 라벨도 하지 않았다.

### 고를 것 (코디 · 사용자)
- ⓐ prod 실물(이건학 지정 호출 → 알림 행 · 앱/웹 알림)을 확인한다. 그 결과를 A10 evidence 로 넣어 pass → `review-delivery --apply`(conformant).
- ⓑ 사람이 A10 을 지금 증거(호출 생성 · call_push 1회 · OQ-99/106 · 받는 사람 계산은 시험이 덮음)로 pass 라고 받아들인다고 명시한다. 그러면 그 문장을 evidence 에 적고 apply 한다.

## 4 · 5 — 하지 않음 (3 결정 뒤 같이)
- `30-work.md` Spec Coverage · `log.md` 마감 줄 · 커밋 · push · PR: review 결과(conformant 여부)를 적을 줄이라 멈췄다.
- #283 마감 댓글: 마감 요약(e2e · 구현 결속)이 3 에 걸려 있어 올리지 않았다. Issue 는 이미 닫혀 있어 닫기 명령은 필요 없다.

## 파일 (`delivery/`)
- `wp1-be-request-v2.json` · `wp1-be-plan-v2.json/.err` · `wp1-be-apply-v2.json/.err`
- `gen/make-review.py` · `review-v2-merged-283.json` · `review-v2-merged-plan-283.json/.err`

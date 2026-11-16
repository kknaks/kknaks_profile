# prod-deploy-re1 — Delivery 마감 (review-delivery · spec-sync) — 2026-11-12 · planner

## 결과 한 줄

- **#243**: review-delivery **conformant · merged 기록됨** → `run-spec-sync`. 문서 sync 패치는 준비했지만 **사람 gate 에서 멈춤** — 커밋 · PR 은 코디 몫이고, sync PR 은 사람이 머지한다. Issue 는 **열어 둠**.
- **#245**: review **적용 안 함** — Acceptance **A6 이 판정 불가(undetermined)**. 사람 판단 gate 에서 멈춤.
- 어느 Issue 도 닫지 않았다.

## 기준값

- mediness `origin/main` = `d7c9b313`(#934 스쿼시).
- 코드 PR:

| PR | head | 머지 | 비고 |
|---|---|---|---|
| #244 | `79e730b5` | `382827d5` → dev | #243 · #245 공통 |
| #246 | `d8d0910f` | `0b2f8cff` → dev | #245 R1 |
| #247 | `2096c92d` | `ad658b1d` | Delivery 범위 밖 · 보지 않음 |

- harness: `mediness review-delivery` · `spec-worktree` · `dashboard-sync`(이 워크트리 `tools/harness`).

## #243 (v2 · PR #244)

### 확인한 것

- **시험 · lint**: PR head `79e730b5` 를 scratchpad 로 `git archive` 해 돌렸다.
  - `uv run pytest -q -m "not infra"` = **897 passed · 1 failed**.
  - 실패 1건(`test_deploy_contract::test_레포에_KOS_실제_주소가_없다`)은 내 사본에 `.git` 이 없어 `git ls-files` 가 실패한 것이다. 같은 검사를 `git grep` 으로 `79e730b5` 에 다시 해 보니 일치 0 · env KOS_*_BASE 0 · example 빈값 → 통과로 판단.
  - `ruff check backend` 통과.
  - infra 시험(317 deselected)은 다시 돌리지 않았다. be-1 격리 스택 · review-code-1/2 근거.
- **migration**: `7b099e8f..79e730b5` 에 `backend/migrations` 변경 0.
- **Acceptance**:

| harness id | 계약 | 결과 | 근거 |
|---|---|---|---|
| A1 | A1 | pass | `register_connection.py` · infra 시험 · prod 등록 실제 |
| A2 | A2 | pass | review-code-2 W1 · W3 닫힘 |
| 「A2b (구현 워커) … (예」 | A2b | pass | `crm_connections.py` 거절 · infra 양방향 |
| A4 | A3 | pass | 데모 시드 is_demo=true 그대로 · 양방향 거절 · import 경계 |
| A5 | A4 | pass | `test_chat_env_contract.py` prod |
| A6 | A5 | pass | 위 시험 · ruff · migration 0 |
| A7 | A6 | pass | _RESUME §5 prod 첫 배포 · 등록 · 첫 동기화 OK · deployment.md 6 · 7 |

- **per_spec**: DAY-SPEC-000 = **none**. OQ-01-2 는 baseline(#933)에 이미 있고, 코드는 그 계약대로다.

### 실행

- review-delivery: --plan exit 0 → --apply exit 0 · `recorded` · Issue open.
- PR #244 에 review 증거 댓글(upsert).
- 라벨: `implementation:conformant` · `spec-sync:pending` · `delivery-plan:approved` · `execution-plan:ready` · `spec-baseline:ready`.
- next_action = `run-spec-sync`(human_gate false).
- request · 결과: `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-mediness-mediness-prod-deploy-re1-spec/8d8c24d2-03ef-495b-b925-3c9c99a3c800/scratchpad/delivery/close.243.review.json` · `close.243.review.plan.json` · `close.243.review.apply.json`.

### spec-sync — 손으로(지난 #932 방식)

- `spec-sync` CLI 는 이 구성에서 닫을 수 없다. mediness#749 「제품 레포 Delivery에서 spec-sync 마감 불가」가 **아직 OPEN** 이다(ledger = CENTURION_DAY · 문서 PR = mediness). #241 마감(#932)과 같은 방식으로 간다: 손 sync PR → 사람 머지 → 마감 댓글 → close.
- `spec-worktree --plan`: base `d7c9b313` · 브랜치 `mediness/delivery-243-spec`. 만들지 않음(커밋 금지).
- `dashboard-sync --view delivery --project-delivery-issue 243 --project-spec-sync synced`(origin/main 사본):
  - plan → apply · changed · content_digest `sha256:21882e312539fa747e6cbcbaea3c5be39709bbdbdfb0e2783e53b0706000318a` · projection #243 closed · spec-sync:synced.
  - 대시보드 변화: #243 행 · #245 행(지금 상태 — open) 추가 · #235 행 closed(원장 그대로).
- Spec Coverage DAY-SPEC-000 에 #243 · log.md 한 행(wp-status) · 최종 수정 2026-11-12.
- **패치** `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-mediness-mediness-prod-deploy-re1-spec/8d8c24d2-03ef-495b-b925-3c9c99a3c800/scratchpad/sync243/sync-243.patch`(30-work.md · log.md · origin/main 에 `patch -p1 --dry-run` 통과). 다 고친 파일 = `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-mediness-mediness-prod-deploy-re1-spec/8d8c24d2-03ef-495b-b925-3c9c99a3c800/scratchpad/sync243/tree/products/day/`.
- origin/main 사본 + 패치로 lint `--strict` = 0 error · `products/day` 0.

### 남은 gate (#243)

1. **코디**: 패치로 브랜치 · 커밋 · mediness PR. 본문에 「제품 동작 기준은 그대로 · 작업 현황만 완료로」를 쓴다.
2. **사람**: sync PR 머지.
3. **머지 뒤**: 머지된 문서로 `dashboard-sync --plan` 을 다시 돌려 `changed:false` · 같은 digest 인지 확인 → #243 마감 댓글 → close. #241 처럼 `spec-sync:pending` 라벨은 남는다(#749).

## #245 (v6 · PR #244 + 마지막 #246) — 멈춤

### 판정을 못 한 것: A6

- **계약 A6** = 「코디 · 데모 지점 dev 실물 1회: 점유 이동 클릭 → 마지막 확인 시각을 event_log · external_outbox 로 재서 **Issue 에 기록** · 복귀 뒤 **KOS 웹에서** 「방 배정」이 사라짐 · 조회에서 빠짐 · **「시술 완료」 탭 원래 방**」.
- 있는 근거:
  - be-2: 데모 테넌트 스크립트 1회 — 연쇄 317ms · DELETE 뒤 일정 조회에서 빠짐 · sequence 재사용 pending.
  - be-3: 로컬 11040(데모 테넌트) 2회 — 클릭 → 띠 0.78초 · 연쇄 확인 · 복귀 쓰기 실패 0.
- 계약과 다른 점:
  - **dev 서버가 아니다**(로컬 · 스크립트).
  - **Issue 에 기록 없음**(#245 댓글은 계약 · 승인뿐).
  - **KOS 웹 눈 확인 · 「시술 완료」 탭 원래 방 확인 기록 없음**.
- 이 근거를 A6 통과로 칠지, dev 실물 1회를 할지, #241 처럼 「다음 작업 검증으로 넘김」으로 할지는 **사람 판단**이다(#241 은 사용자 결정으로 넘겼다). conformant review 는 모든 Acceptance 가 pass 여야 해서 `--apply` 하지 않았다.

### 나머지 근거(판정 가능 · 참고)

- **A1 ~ A5**: W3 · W4 · W5 · 규칙 33 · 시험 → review-code-5 PASS(145 passed) · 6 WARN → 7 PASS(137 passed) · 위 #244 head non-infra 897 passed.
- **A7 · A8**: W6 · W7 → review-code-8 PASS(93) · 9 PASS(168).
- **A9**: P1 공개 페이지 → review-code-12 PASS(44 · 원천 글자 바이트 단위 같음) · prod `/privacy` · `/support` 200(_RESUME).
- **A10**: P2 → review-code-11 PASS(flutter 83) · 실기기 Safari 확인 = 코디 지시(수정 7)로만 근거(앱 세션 리포트 아님).
- **A11**: R1 → PR #246 · review-code-13 PASS(109).
  - `d8d0910f` 에서 non-infra 는 다시 돌리지 않았다(#246 은 3파일). 필요하면 apply 전에 한 번.
- **per_spec(제안)**: DAY-SPEC-002 · 001 · 003 = **none**. ⑱ · 보충 ⑤ ⑥ · ⑲ · ⑦ · ⑫ 가 #934(`d7c9b313`)로 이미 main 에 있다. 다만 be-2 의 「상세 조회 3회 · 0.5초 재읽기」 상수는 스펙(OQ-52)에 없다(내부 상수 · 사용자 동작 아님으로 봄 — 의미 판단이라 같이 확인).
- **harness id**(콜론 앞 자르기): `A1` · `A2 (구현 워커) 「방 배정」 없는 카드 점유 이동` · `A3` · `A4 (구현 워커) 규칙 33` · `A5` · `A6` · `A7 (구현 워커) W6` · `A8 (구현 워커) W7` · `A9 (구현 워커) P1` · `A10 (앱 · 코디) P2` · `A11 (구현 워커) R1`.
- **code_pr**: 마지막 PR #246(head `d8d0910f` · 머지 `0b2f8cff`)을 closing PR 로 쓴다(규칙 「마지막 PR 만 closing」). #244 는 #243 review 댓글이 이미 있다.

### 남은 gate (#245)

1. **사람**: A6 처리 결정(통과로 침 · dev 실물 1회 · 다음 작업으로 넘김).
2. **사람(같이)**: per_spec none 확인.
3. 결정 뒤: review-delivery(#246) --apply → run-spec-sync. sync 는 #243 PR 에 합칠 수 있다(#932 처럼 여러 Delivery 한 PR) — 그 경우 #245 행도 dashboard-sync 로 다시 만든다.

## 발견 — harness (보고만)

- **_acceptance_ids**(`workflow.py:879`): 각 줄의 **첫 콜론 앞**을 id 로 쓴다. 콜론이 없으면 `A{순번}` 이다. 그래서 「A2b … (예: …)」 같은 줄은 긴 문자열 id 가 되고, 콜론 없는 계약 A3 ~ A6 은 순번 A4 ~ A7 로 밀린다. 계약 라벨과 harness id 가 어긋나므로 evidence 첫 줄에 「contract A3 (harness slot 4)」처럼 대응을 적었다. 계약을 「A1: …」 모양으로 쓰면 피할 수 있다(다음 Delivery 부터).
- mediness#749 OPEN — 위 손 sync 의 이유.

## A6 뒤 (2026-11-12 · 사용자 「통과로 쳐 · 내가 확인했어 · 5초 안에 와」)

### #245 review-delivery

- **A6 근거를 Issue 에 기록**: https://github.com/MediSolveAIDev/CENTURION_DAY/issues/245#issuecomment-6815862237
  - 사용자 실물(반영 5초 안) · be-2(연쇄 317ms · DELETE 뒤 조회에서 빠짐) · be-3(띠 0.78초 · 복귀 실패 0) · 비교 19.8 ~ 27.1초 · OQ-53 sequence 재사용은 남음 · 값 없음.
- **시험**: PR #246 head `d8d0910f` 사본에서 non-infra **898 passed** · 1건은 사본 환경 탓(`git grep` 으로 같은 검사 통과) · ruff 통과 · migration · deploy 변경 0.
- **request**: code_pr **#246**(마지막 PR) · head `d8d0910f` · 머지 `0b2f8cff` · contract v6 · Acceptance 11개 전부 pass(harness id 그대로 · 근거 첫 줄에 계약 라벨) · per_spec 002 · 001 · 003 = none.
- **결과**:
  - --plan exit 0 → --apply exit 0 · `recorded` · Issue open · next_action `run-spec-sync`.
  - 라벨 `implementation:conformant` · `spec-sync:pending`.
  - 파일: `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-mediness-mediness-prod-deploy-re1-spec/8d8c24d2-03ef-495b-b925-3c9c99a3c800/scratchpad/delivery/close.245.review.*`.

### spec-sync — 한 mediness PR (#932 방식)

- **PR**: **MediSolveAIDev/mediness#936** https://github.com/MediSolveAIDev/mediness/pull/936
  - 브랜치 `kknaksss/day-delivery-243-245-close-sync` · head `392b9fc11a2aafdb41eef1c2ba12706c391c339a` · base `d7c9b313`.
- **worktree**: `spec-worktree --apply` 는 실패했다 — 로컬 브랜치 `mediness` 가 있어 `mediness/delivery-245-spec` 를 만들 수 없음. mediness#749 의 「브랜치명 충돌」과 같은 일이다. force 하지 않았다.
  - 대신 `git worktree add -b kknaksss/day-delivery-243-245-close-sync` 로 origin/main 위 isolated worktree 를 만들었다: `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-mediness-mediness-prod-deploy-re1-spec/8d8c24d2-03ef-495b-b925-3c9c99a3c800/scratchpad/spec-wt/close-243-245`.
- **dashboard-sync**(`--project-spec-sync synced`) 를 #243 · #245 차례로 plan → apply 했다.
  - 한 번에 한 Issue 만 projection 된다. 그래서 행은 손으로 **마감 뒤 실제 상태**(closed · implementation:conformant · `spec-sync:pending` — #241 과 같음)로 맞췄다.
  - 이유: #749 로 `spec-sync` 가 synced 라벨을 줄 수 없다. 닫은 뒤 projection 없이 다시 돌렸을 때 `changed:false` 가 되게 하려는 것이다.
- **Spec Coverage**: #243 → DAY-SPEC-000 · #245 → DAY-SPEC-001 · 002 · 003.
- 30-work.md 「최종 수정」 2026-11-12 · log.md 한 행.
- 앞 절의 #243 단독 패치(`sync243/sync-243.patch`)는 쓰지 않고 이 PR 로 대체했다.
- lint `--strict` 0 error · `products/day` 0(커밋 hook 도 0 error).

### 머지 뒤 할 일(코디 머지 뒤 — 나에게 지시하면 이어서 함)

1. 머지 SHA 확인.
2. **두 Issue 마감 댓글**(#241 형식): 코드 PR · head · 머지 · baseline · contract_version/digest · plan_digest · review 결과 · 문서 sync = mediness#936 머지 SHA. #245 는 A6 사용자 판단 · OQ-53 남은 것도 적는다.
3. **두 Issue close**. `spec-sync:pending` 라벨은 그대로(#241 선례 · #749).
4. 머지된 main 에서 `dashboard-sync --view delivery` 를 projection 없이 plan → `changed:false` 확인.
   - 순서: close 뒤에 해야 원장과 같아진다.
   - 만약 `changed:true` 면 그 차이를 보고하고 따로 고친다(PR 다시).

### 남은 gate

- **mediness#936 머지(코디)**.
- harness: #749(spec-sync 교차 레포 · spec-worktree 브랜치명) · Acceptance id 파싱 — 보고만.

## 머지 뒤 — 마감 완료 (2026-11-12)

1. **머지 확인**: mediness#936 MERGED · 스쿼시 `fe639680c68e6a8cdde8ac6d20e1e225c046fd99` = `origin/main` · PR head `392b9fc1` 와 `products/day` 차이 0.
2. **마감 댓글**(#241 형식):
   - #243 https://github.com/MediSolveAIDev/CENTURION_DAY/issues/243#issuecomment-6815975851 — #244 head · 머지 · baseline · contract v2 · plan_digest · review conformant · 문서 sync #936 `fe639680` · 배포 · #749 사유 · OQ-01-3 남음.
   - #245 https://github.com/MediSolveAIDev/CENTURION_DAY/issues/245#issuecomment-6815976248 — #244 + closing #246 · contract v6 · plan_digest · review conformant · 문서 sync #936 · **A6 사용자 판단** · **OQ-53 남음** · A1 테두리 = Non-Goal 7 · #749 사유.
3. **close**: #243 · #245 둘 다 CLOSED(completed). 라벨 그대로 — `implementation:conformant` · `spec-sync:pending` · `delivery-plan:approved` · `execution-plan:ready` · `spec-baseline:ready`.
4. **dashboard-sync 재확인**: close 뒤 `fe639680` 의 `products/day/30-work.md` 로 `--view delivery --plan`(projection 없음) → **`status: current` · `changed: false`** · content_digest `sha256:d8614e87b04a9e0c425f1d33cd351814c600923fa5ad68199250e7fa6550e49b`.
   - #936 에 미리 적은 마감 뒤 상태(closed · conformant · spec-sync:pending)가 원장과 같다.

- 정리: scratchpad worktree `close-243-245` 제거(깨끗한 상태 확인 뒤). 원격 브랜치는 그대로.
- 남은 것: 없음(이 slug Delivery 둘 마감). harness 보고 두 건(#749 · Acceptance id 파싱)은 앞 절 그대로.

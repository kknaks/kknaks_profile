# review-delivery-2 — CENTURION_DAY#272 ↔ Delivery #267 · #268 · #269 (contract v3)

- 기준: exact PR head **`85836b300cb729fb9b4923d05ae9d8bf14bd66f8`**(PR #272 · base `dev` · OPEN · CI 2건 SUCCESS) · baseline Mediness main **`32b83390`**(= 지금 `origin/main` · SPEC-006 개정 ⑪ · SPEC-000 2026-11-24 · SPEC-002 개정 ㉗ 들어 있음) · contract v3 digest = `delivery-4-report.md` 표.
- harness: `uv run --project tools/harness mediness review-delivery --github-repo MediSolveAIDev/CENTURION_DAY`(문서 워크트리 `day-reservation-spec`).
- 코드 · 문서 · Issue · PR 은 고치지 않았다. **`--apply` 는 하지 않았다** — 라벨 · 댓글도 남기지 않았다(아래 막힘).

## 판정: 막힘 — 실물 e2e Acceptance 근거 없음(세 Issue 같음)

| Issue | 판정 | Acceptance | 남긴 라벨 | 다음 단계 |
|---|---|---|---|---|
| #267 ① | 미기록(e2e 근거 대기) | A1 ~ A4 · A6 ~ A9 pass · **A5 e2e = 근거 없음** | 없음(그대로: execution-plan:ready · delivery-plan:approved · spec-baseline:ready) | e2e 근거 → conformant `--apply` → `await-human-merge` |
| #268 ② | 같음 | A1 ~ A5 · A7 ~ A9 pass · **A6 e2e = 근거 없음** | 없음 | 같음 |
| #269 ③ | 같음 | A1 ~ A3 · A5 ~ A8 pass · **A4 e2e = 근거 없음** | 없음 | 같음 |

### 막힌 규칙

- harness `review_delivery`: `implementation = conformant` 이면 **모든 Contract Acceptance 가 `pass` + evidence** 여야 한다(아니면 WorkflowConflict). 근거 없이 pass 로 적는 것은 우회라 하지 않았다.
- e2e Acceptance(세 Issue 같은 문장): 오늘 열기 = 최신화 요청 0 · 10초 폴링이 DB 사본만 읽음 / 다른 날짜 = 첫 화면 이전 사본 · 요청 1회 → 다음 폴링에 채워짐 · 폴링 동안 0 / **두 창 동시 = 그 (병원, 날짜) KOS 일정 조회 1회** · 「결과를 세 Issue 에 남긴다」.
- 찾아본 곳: PR #272 본문 「검증」 = 로컬 KOS 데모 e2e(조회 · 원내 금액 · 담당자 줄 · 카드 배치 · 동행 묶기 / 풀기)만 — 요청 수 · 두 창 동시 기록 없음 · 「미확인: 직원 토큰 공지 쓰기 실물 1회」. Issue 세 개 · PR 댓글에 e2e 결과 없음. `e2e-1-feedback.md` · `_RESUME.md` = 1 ~ 3회차 피드백(폴링 멈춤 버그 · 3초 기다림 등)뿐 — 기대 결과 대조 기록 아님. `delivery-4-report.md` 「남은 것」도 「실물 e2e 결과를 세 Issue 에 남기는 일」이 남았다고 적음.
- 순서 조건: 「셋이 다 들어간 뒤 마지막 머지 Issue 에서 1회」 — 세 Issue 가 Code PR #272 하나로 덮이므로 **이 PR head 에서 1회**면 된다.
- 코디에게 `ask`(msg `msg_d8cbde0161d8` · a 근거 주면 apply / b plan 만 / c conflict apply) — 30분 넘게 답 없음 → **(b) 안전한 쪽**으로 마침. conflict 로 apply 하면 `implementation:conflict` 라벨 + `resolve-implementation-conflict`(scope 충돌 뜻)라 사실과 달라 하지 않았다.

## harness `--plan` 결과 (쓰기 없음)

- 세 Issue 모두 exit 0 · `planned` — spec-baseline ready · plan 승인 마커 · L2 execution ready · digest · version 3 · baseline `32b83390` · per_spec 셋/둘/하나 · Acceptance id 개수 전부 통과.
- probe 는 e2e 를 `undetermined` 로 둬서 `implementation = conflict` · next = `resolve-implementation-conflict`(human_gate) — **입력 검증용일 뿐 apply 하지 않음**.
- 파일: `delivery/make-review-v3.py`(요청 만들기) · `delivery/review-v3-probe-{267,268,269}.json` · `delivery/review-v3-probe-plan-*.json`.

## Acceptance 대조 (exact head `85836b30` · 경로:줄)

**#267 ①**
- A1 조각 / 전체 · V1 ~ V4: `tests/day/web/test_reservation_page.py:131` · `test_reservations_screen.py:277` · `test_reservation_rules.py:113` · `test_reservation_inhouse_rules.py:194`
- A2 KOS 0 · 오늘 0 · 다른 날 1 · poll=1 0: `test_reservation_page.py:143 · :152 · :198` · `test_reservation_refresh.py:64`
- A3 권한 기본 · 403: `board/test_reservation_permissions.py:52` · `test_default_permissions.py:75` · `migrations/test_reservation_permission_migration.py:102`
- A4 케이스: `test_reservation_queries.py:256` · `test_reservation_page.py:163` · `test_reservation_rules.py:212 · :194` · `test_reservation_layout.py:90`
- A6 R52 금액: `test_reservation_inhouse_queries.py:232` · `test_reservation_amounts.py:205` · `test_reservation_inhouse_rules.py:107`
- A7 공지: `board/test_reservation_notice.py:167 · :249 · :312 · :358`
- A8 동행 · 배치 R73: `board/test_reservation_companions.py:160 · :231 · :279` · `test_reservation_layout.py:70 · :104`
- A9 migration 왕복 · head 하나 · 기존 행 안 건드림: `migrations/test_*_migration.py`(0018 :102 · 0019 :36 · 0020 :47 · 0021 :84 · 0022 :94 · 0023 :114) · `test_alembic.py:107`

**#268 ②**
- A1 R26 범위: `emr/test_date_sync.py:209` · `test_date_sync_rules.py:106` / A2 C1: `:235` · rules `:147` / A3 C2: `:255 · :278 · :296` / A4 C3: `:320` · rules `:125` / A5 동시 1회 · 오늘 그대로: `:336 · :448` · `test_emr_sync_service.py:177`
- A7 공지 동기화: `emr/test_notice_sync.py:44 · :106` · `test_date_sync_notices.py:49 · :66 · :82`
- A8 거래 5 · 수단 7 · 밖 = 뺌: `emr/test_kos_sale_mapper.py:180` · `test_kos_keys_mapper.py:495` · `test_reservation_amounts.py:243`
- A9 캐시 · 양보: `test_reservation_refresh.py:120` · `test_date_sync.py:362 · :407`

**#269 ③**
- A1 문구 · 뺀 요소: `architecture/test_screen_copy.py:226` · `web/test_reservations_screen.py:358 · :601` / A2 인라인 스크립트 0: `architecture/test_web_rules.py:101`
- A3 날짜 · 폴링 · 필터 · 순서: `scripts/frontend/tests/res-browser.test.mjs:8 · :21` · `res-order.test.mjs:61` · `test_reservations_screen.py:288 · :422`
- A5 원내 현황: `res-inhouse.test.mjs:30 · :67 · :101` · `test_reservations_screen.py:481`
- A6 끌어 놓기 · 띠 테두리만: `res-companion.test.mjs:29 · :56 · :85 · :108 · :134 · :202`
- A7 공지 편집: `res-notice.test.mjs:54 · :73 · :92 · :140 · :169`
- A8 배치 · debounce: `res-companion.test.mjs:165 · :246` · `res-debounce.test.mjs:70`

전체 check.sh 녹색(2584 passed · CI success — 코디 전달 · PR 체크 확인)은 다시 돌리지 않았다.

## per_spec 판단 (세 Issue)

- **DAY-SPEC-006 · DAY-SPEC-000 · DAY-SPEC-002 모두 `none`** — baseline `32b83390` 이 이미 이 구현(개정 ⑪ · 2026-11-24 · ㉗ · migration 0018 ~ 0023 · 칸 이름)을 담고 있고, diff 에서 baseline 밖 사용자 계약 변화를 보지 못했다(검수 13 PASS · 코드 검수 4회).
- 참고(SPEC 영향 아님): 검수 13 W13-1(SPEC-006 L191 옛 순서 사슬 취소선) · W13-2(0019 downgrade 문장) — 문서 정리 몫. all-`none` 이어도 머지 뒤 `spec-sync`(dashboard closeout)는 해야 한다.

## 그 밖 확인

- PR #272 본문에 `GitHub Delivery Issue: #NNN` 줄이 없고 closing issue 연결도 0. harness review 는 이를 검사하지 않지만 nudge 는 이 줄이 있어야 돈다. 「1 Delivery = 1 Code PR」 원칙 밖(세 Delivery = PR 하나)인 것은 delivery-4 가 review_surface 에 적어 둔 그대로다.
- PR 본문 「미확인: 직원 토큰 공지 쓰기 실물 1회」 — Acceptance(#267 A7 = 가짜 어댑터 테스트)에는 걸리지 않지만 남은 위험이다. 머지 판단에 같이 보면 된다.

## 풀어 가는 법 (코디 · 사용자)

1. 이 head(`85836b30`)로 실물 e2e 1회: 오늘 열기(요청 0) · 다른 날짜(요청 1 → 채움 · 폴링 0) · 두 창 동시(KOS 일정 조회 1회) — `.run/api.log` · `worker.log` 줄로 기록.
2. 결과를 세 Issue 에 남긴다(Acceptance 문장 그대로).
3. `python3 delivery/make-review-v3.py final "<e2e 근거 1>" "<근거 2>" …` → `review-final-{267,268,269}.json`(e2e pass · conformant) → `review-delivery --plan` → `--apply`. 결과 = `implementation:conformant` 라벨 + PR #272 review 댓글 + Issue closeout 마커 · next = **`await-human-merge`**(human_gate).
4. 사람 머지 뒤: 같은 요청에 `code_merge_sha` · `merged: true` 로 `review-delivery` 다시 → all-`none` 이라 next = **`run-spec-sync`** → `spec-sync`(dashboard-only sync PR · 30-work 의 DAY-SPEC-006 / 000 / 002 Coverage · SPEC-002 done 되돌림) → fresh evidence 뒤 Issue close.
5. PR head 가 바뀌면 위 1 ~ 3 을 새 head 로 다시(evidence stale).

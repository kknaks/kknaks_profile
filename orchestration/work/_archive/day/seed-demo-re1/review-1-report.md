# seed-demo-re1 리뷰 1 — 데모 시드 스크립트

- 대상: 워크트리 `seed-demo-re1`(브랜치 `kknaksss/seed-demo-re1`) 미커밋 변경 2개
  - `scripts/seed_demo_board.py` (+335/-?) · `backend/tests/scripts/test_seed_demo_board.py` (+319)
- 기준: `seed-demo-re1-be-brief.md` 2절 1 ~ 5 · 7절
- 검증(각 1회): `cd backend && uv run pytest -q tests/scripts/test_seed_demo_board.py` → **62 passed (0.07s)** ·
  `ruff check` → All checks passed · `ruff format --check` → 2 files already formatted ·
  `git diff --name-only origin/dev -- backend/day backend/migrations` → 비어 있음
- 참고: 인박스에서 seed-demo-re1 backend worker_done 은 찾지 못했다(다른 run 의 메시지만 보임). 코드 · 시험만으로 판정했다.

## 종합 판정: **WARN** (FAIL 0 · WARN 2 · 참고 2)

| # | 볼 것 | 판정 |
|---|---|---|
| 1 | 모든 방문에 「방 배정」 + 방 | PASS |
| 2 | 한국어 가짜 이름 · KR 기본 | **WARN** (W1) |
| 3 | 오더 메모 양식 · 시술 줄 = KOS 실제 제목 | PASS (시험 빈틈 W2) |
| 4 | 시술 4 ~ 6 무작위 · 수납 반복 | PASS |
| 5 | 데모 가드 · dry-run 쓰기 0 · 출력 PII 없음 | PASS |
| 6 | 제품 코드 · migration 변경 없음 · 시험이 판정 | PASS |

## 1. 「방 배정」 — PASS

- `scripts/seed_demo_board.py:266-281` `pick_room_assign`: env id(strip) → 목록에서 그 id, 없으면 KosError / env 비면 제목(공백 · `/` 제거 후 「방배정」) → 없으면 KosError. 브리프 2절 1 순서 그대로.
- `:510` `masters()` 안에서 고른다 → 예약 · 쓰기 전에 멈춘다. 시험 `test_no_room_assign_stops_before_writes`(dry-run · 실제 둘 다 쓰기 0).
- `:569-591` 모든 방문에 같은 `m.room_assign` 으로 ETCETERA 추가 → `change-tasks-room`(sequence 1). 예전 목록 순환(`m.etc_tasks[i % …]`) 없어짐.
- `:394-410` `missing_parts` 가 「방 배정」 id + 방 id 둘 다 있는 ETCETERA 를 본다(다른 기타 작업에 방만 있으면 빠짐으로 판정 — 시험 `test_missing_parts` `other_etc`).
- 참고: env id 가 있는데 목록에 없으면 제목으로 내려가지 않고 멈춘다(`:270-273`). 브리프 「없으면」 = env 가 비었을 때로 읽으면 맞고, 잘못된 id 를 조용히 덮지 않아 더 안전하다.

## 2. 이름 · 국적 — WARN

- PASS 부분: `:84-90` 성 15 × 이름 20 무작위 조합 · `korean_names`(`:237`) 가 `rng.sample` 로 실행 안 중복 없음 · `[TEST]` 없음 · `visitorName` = `res.person.name`. 국적 기본 KR(`pick_nationalities` · `NATIONALITIES[0]` = KR), `--mixed-nationality` 로 순환 유지. 시험 `test_korean_names_are_hangul_unique_and_unmarked` · `test_nationalities_default_korea` · 전체 실행에서 `visitorNationality == "KR"`.
- **W1 — 유명인 이름이 후보 풀에 남아 있다** (`scripts/seed_demo_board.py:84-91`, 브리프 2절 2 「실제 인물 · 유명인 이름 피함」)
  - `AVOID_NAMES` 는 6개뿐이고, 300개 조합 안에 널리 알려진 이름이 최소 13개 남는다:
    최지우 · 김선호 · 김재원 · 김지우 · 김민서 · 이현우 · 서현우 · 이채원 · 김승현 · 오승현(배우) · 최현우(마술사) · 조수빈 · 정다은(아나운서).
  - 10명 한 번 돌리면 이 중 하나가 나올 확률 ≈ 1 − (1 − 13/294)^10 ≈ **36%**.
  - 가짜 실장 `CHIEFS` 의 「윤소희」(`:91`)도 배우 이름과 같다(시험 `:221` 에도 쓰임).
  - 고칠 방향: `AVOID_NAMES` 에 위 13개를 더하고 `윤소희` 를 다른 가짜 이름으로 바꾼다. 흔한 한국 이름은 동명이인을 완전히 피할 수 없으니 「유명인 목록 제외」 수준이 현실적인 기준이다.

## 3. 오더 메모 양식 — PASS

- `:313-331` `order_memo` 줄 순서가 브리프 양식과 1:1(상담내용 → N) → H) → 구분선 → 이름/ROOM NO. → 실장/Dr: → [진단기] O → 빈 줄 → OUT TIME → 0. 자가세안 O → - 마취크림 → 1..n 시술 → 빈 줄 → [특이사항] x → [임플란트 여부] x).
- 공백도 브리프 원문과 같다: 이름 뒤 9칸 · 실장 뒤 7칸(브리프 파일에서 세어 확인).
- ROOM NO.: `room_no`(`:284-287`) 「…룸N」 → N, 아니면 방 이름. 시험 `test_room_no`.
- 시술 줄: `finish`(`:681-695`)가 수납 · 시술 작업이 다 끝난 뒤 상세를 읽어 PROCEDURE 제목이 넣은 수만큼 보일 때까지 `DETAIL_RETRY_SECONDS` 로 기다리고, 그 제목으로 메모를 만든다. 옵션 이름이 아니라 KOS 상세 제목을 쓴다(시험에서 옵션 「진료」와 상세 「KOS 시술 n」을 달리 두고 확인 — `test_full_run_room_assign_procedures_and_form_memo`).
- `missing_parts` 의 옛 「테스트 오더 메모」 비교는 없어지고 새 메모 전체와 같은지 본다(`:401`).
- **W2 — 반영 지연 경로가 시험되지 않는다** (`backend/tests/scripts/test_seed_demo_board.py` `FakeKos`)
  - Fake 상세는 시술 작업을 즉시 보여 준다. `finish` 의 「덜 보이면 기다렸다 다시 읽기」와 「끝까지 덜 보이면 `시술 작업 k/n 개만 보임` 으로 실패」(`seed_demo_board.py:687-691`) 두 갈래가 실행되지 않는다.
  - 고칠 방향: Fake 상세가 처음 1 ~ 2번은 시술 작업 일부만 돌려주게 하는 시험 1개 · 끝까지 모자라면 KosError 인 시험 1개.
- 참고 R1: `"order-memo": detail.get("orderMemo") == memo`(`:401`)는 완전 일치다. KOS 가 줄바꿈(`\r\n`) · 끝 공백을 바꿔 저장하면 데이터는 맞는데 「확인 실패: order-memo」 로 끝난다. 코디 실물 1회 때 이 줄이 나오면 비교를 줄 단위 strip 으로 느슨하게 하면 된다(지금은 근거 없음 · 실물로만 확인 가능).

## 4. 시술 수 · 수납 — PASS

- `parse_procedures`(`:290-300`) `N` / `MIN-MAX`, 1 ~ 10. 기본 `4-6`(`DEFAULT_PROCEDURES`). 잘못된 값은 client 만들기 전에 rc 2(`test_bad_procedures_rejected_before_client`).
- `pick_options`(`:303-309`) `rng.choices(k=randint(lo, hi))` — 복원 추출이라 옵션 3개여도 겹쳐서 채운다(브리프 「겹쳐도 된다」).
- `:596-610` 옵션마다 `purchase()`(init → add items → register → add-transaction 현금 → accept) → `tickets(visitor_id, purchase_id)`(그 수납의 시술권만) → `add-flow-tasks`(PROCEDURE) 반복. 수납 id · 거래 id 는 매번 새 uuid.
- 금액: 품목 `item_prices(option["price"])` 와 거래 `price` · `suppliedAmount` · `taxFreeAmount` · `vatAmount` 가 같은 `prices` 에서 나온다(`:625-652`) — 수납마다 품목 = 거래. 계산식은 예전 그대로(`test_item_prices_add_vat_like_har`).
- 시험: 전체 실행에서 PROCEDURE 수 4 ~ 6 · `P_INIT_PURCHASE` · `P_ACCEPT` 횟수 = 시술 수, `--procedures 5` 면 정확히 5.

## 5. 가드 · dry-run · 출력 — PASS

- `check_demo_tenant`(`:830`)가 client 생성 전 · `check_open_key_is_demo` 가 masters 첫 조회 직후(`:480`) — 그대로.
- dry-run(`:859-862`)은 masters 조회 뒤 국적만 출력하고 끝. `test_dry_run_sends_no_writes` 가 호출 경로를 조회 5종(`P_ZONES` · `P_GROUPS` · `P_ROOMS` · `P_ETC_TASKS` · `P_OPTIONS`)으로 한정.
- 출력: `_row`(`:805-816`)는 순번 · 국적 · schedule id 끝 4자리 · 단계 · 시술 수만. 방 배정 id 도 끝 4자리. 이름 · 메모 본문 미출력은 시험 `name not in out and "상담내용" not in out`, 생년월일은 `test_reserve_body_carries_fake_birth_and_run_does_not_print_it`. 실패 사유는 `error_text`(KosError 메시지 · 예외 이름) 그대로.
- 찾는 단서를 이름 접미어에서 예약 메모 `DAY 현황판 테스트 데이터 {tag}-{NN}`(`reservation_memo`)로 옮겼고 실패 줄 안내도 바꿨다 — 이름에 표시가 없어진 것에 맞는 처리.

## 6. 범위 — PASS

- 변경은 `scripts/seed_demo_board.py` · 시험 파일 2개뿐. `backend/day/` · `backend/migrations/` 변경 0. `deploy/local.env.example` 은 이미 `DAY_SEED_KOS_ROOM_ASSIGN_ETC_TASK_ID=`(42행)가 있어 안 건드렸다.
- 시험 62개가 1 ~ 5를 판정한다(W2 의 지연 갈래만 빠짐).

## 코디에게

- 머지 전 W1(유명인 이름 13개 + 실장 「윤소희」 제외) 반영을 권한다 — 목록 몇 줄만 고치면 된다.
- W2 는 시험 보강이라 실물 1회 전에 넣으면 좋고, 늦어도 무방하다.
- 실물 1회 때 「확인 실패: order-memo」 가 나오면 R1(메모 비교 정규화)을 본다.

---

## 재리뷰 (1b · 2026-11-12) — 판정: **PASS** (W1 · W2 해소 · 새 지적 0)

- 검증(각 1회): `uv run pytest -q tests/scripts/test_seed_demo_board.py` → **66 passed (0.08s)**(62 → 66) ·
  `ruff check` All checks passed · `ruff format --check` 2 files already formatted ·
  변경 파일은 여전히 `scripts/seed_demo_board.py` · 시험 파일 2개, `backend/day` · `backend/migrations` 변경 0.

### W1 — 해소
- `scripts/seed_demo_board.py:90-94` `AVOID_NAMES` 에 지적한 13개(최지우 · 김선호 · 김재원 · 김지우 · 김민서 · 이현우 · 서현우 · 이채원 · 김승현 · 오승현 · 최현우 · 조수빈 · 정다은)가 모두 들어갔다(기존 6 + 13 = 19).
- `:95` `CHIEFS` 의 「윤소희」 → 「도하람」. 시험 `:242` · `:250` 의 양식 예시도 도하람으로 바뀌었다.
- 시험: `test_famous_names_never_generated`(`backend/tests/scripts/test_seed_demo_board.py:98`) — `FAMOUS ⊆ AVOID_NAMES`, 풀 전체를 뽑아도 FAMOUS 와 겹침 0, 풀 크기 + 1 이면 ValueError. `test_fake_chiefs_avoid_famous_names`(`:106`) — 윤소희 없음 · CHIEFS ∩ AVOID_NAMES = ∅.

### W2 — 해소
- `FakeKos.visible_procedures`(`:341-342`) · `_visible_tasks`(`:375-380`): 상세를 읽을 때마다 보이는 시술 작업 수 상한을 하나씩 꺼내 반영 지연을 흉내 낸다. 시술 작업이 0개일 때(예약 직후 첫 상세)는 꺼내지 않아 순서가 어긋나지 않는다.
- `test_waits_until_all_procedures_visible_then_writes_memo`(`:691`) — 1/4 → 3/4 → 4/4. 메모 시술 줄이 4개 전부이고, 메모 전 상세 읽기 = 1 + 3회로 「기다렸다 다시 읽기」 갈래를 실행한다.
- `test_fails_when_procedures_stay_missing`(`:712`) — 끝까지 2/4 면 rc 1 · 출력 `procedure-titles: 시술 작업 2/4 개만 보임` · 오더 메모와 시술 대기를 보내지 않는다. `seed_demo_board.py` `finish` 의 실패 갈래까지 시험한다.

### 남은 것
- 참고 R1(오더 메모 완전 일치 비교)은 그대로다. 실물 1회에서만 확인할 수 있어 막는 이유는 아니다.

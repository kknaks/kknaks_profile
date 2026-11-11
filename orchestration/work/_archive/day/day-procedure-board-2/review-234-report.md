# 리뷰 리포트 — CENTURION_DAY#234 데모/운영 연결 구분 없앰 / code (2026-11-09)

대상: 워크트리 `day-procedure-board-2` 의 `git diff`(추적 파일 23개, +328 −269). 미추적 seed_demo_board 는 범위 밖.
근거: Delivery #234 v2(바뀌는 것 (가)(나)(다) · 하지 않는 것 · A1~A3) · 스펙 PR #920(SPEC-000 개정 2026-11-09 · SPEC-001 개정 ⑥ · SPEC-002 개정 ⑫ · §3 KOS 쓰기 표) · 사용자 결정 「`is_demo` 는 표시 데이터 · 어떤 코드도 그 값으로 동작을 가르지 않는다」.
실행:
- `uv run pytest -q -m 'not infra'`: **442 passed** · 163 deselected
- `ruff check backend` · `ruff format --check backend`: 통과
- infra 테스트(실제 PostgreSQL)는 돌리지 않았다. 아래 「확인 못 함」에 적었다.
- KOS · 공유 DB 호출 0회.

## 판정: WARN — FAIL 0 · WARN 3 · 참고 3

---

## 볼 것별 판정

### 1. 동작 분기 0 — PASS
`git grep -n -E 'is_demo|app_env|APP_ENV|trial|demo|live'` 를 `backend/day` · `backend/common` · `backend/runtime` 에 돌렸다. 걸린 자리 전부의 판정:

| 자리 | 판정 |
|---|---|
| `day/models/hospital.py:57` `is_demo` 칸 | 칸 — OK((다) 칸 유지) |
| `day/services/crm_connections.py:75-122` `ensure_demo_connection`(`is_demo=True` 로 넣음) · `day/public.py:15-42` 시드 | 시드 — OK |
| `crm_connections.py:3-6` · `factory.py:93` | docstring — OK |
| `common/config.py:42 · 151-154 · 175-184` APP_ENV 필수 · prod↔day_prod 짝 | Non-Goals(배포 안전장치) — OK |
| `common/logs.py` · `runtime/main.py:38-40` · `runtime/worker.py:15` 로그 칸 · dev 노출 | Non-Goals — OK |
| `day/routers/kit.py:24` · `kit_board.py` `/dev/kit` dev 전용 | Non-Goals — OK |

- `trial` · `TRIAL_STEPS` · `trial_writes` · `kos_trial_writes_on_live` · `KOS_TRIAL_WRITES_ON_LIVE` 는 레포 어디에도 남지 않았다(`git grep` 0).
- **`is_demo` 로 동작을 가르는 자리 0, `APP_ENV` 로 연결을 거르는 자리 0.**
- 어댑터 캐시 지문에서 `is_demo` 를 뺐다(`factory.py:29-36`). (다)와 맞다.
- `Settings` 가 `extra="ignore"`(`config.py:40`)라, VM env · Key Vault 에 옛 `KOS_TRIAL_WRITES_ON_LIVE` 가 남아 있어도 뜨는 데 문제없다.

### 2. 다른 not-supported 경로 · 조용히 열린 쓰기 — PASS

**`OPEN_STEPS = frozenset(KOS_STEPS.values())`**(`writes.py:46`)
- 값은 `PROCEDURE` · `PROCEDURE_WAITING` · `PROCEDURE_DONE` 셋뿐이다. 앞의 둘(예전 OPEN · TRIAL)을 합친 것과 정확히 같다. 새로 열린 단계는 없다.
- 표에 없는 단계는 계획(`:123-124`)과 보내기 직전 `write_open`(`:60-62`) 양쪽에서 막는다.

**`write_open`**(`:53-67`) — 여전히 「경로 + 값」으로 막는다.
- 공개 경로 → False
- `COMPLETE` 는 `isinstance(complete, bool)` 만 통과(`"false"` 문자열 막힘 · 테스트 `test_kos_board_contract.py:146`)
- `CANCEL` 은 `reason == "CANCEL"` 만 통과
- 모르는 경로 → False

`CALL` 은 예전처럼 본문만으로 처음 호출과 다시 호출을 가르지 못한다. 이번에 그 구분이 필요 없어졌다.

**남은 `WriteNotSupportedError` 경로**

| 경로 | 위치 | 테스트 |
|---|---|---|
| 시스템 계정 없음 | `writes.py:87-88` | `test_kos_board_contract.py:102` |
| 표에 없는 단계 | `writes.py:124` | `test_kos_board_contract.py:104` |
| 알 수 없는 쓰기 | `writes.py:150` | `test_kos_board_contract.py:105` |
| writer 미설정 | `kos/__init__.py:185-186` | 코드 그대로(diff 밖) |

→ not_supported 필드 · `board.py:258-260` 기록은 이 경로들을 위해 남아 있다. Delivery 「바뀌는 것」 마지막 항과 맞다.

**SPEC-002 §3 표와 `writes.py` docstring 표** — 7행의 경로 · 값 조건 · 확인 상태가 맞는다. 「시작 취소」는 `방배정.har` 와 데모 실물로 확인됐고, 나머지 4개는 「확인 안 됨」이다(SPEC-002 :533-537 · OQ-23).

### 3. outbox — PASS(회귀 없음)
- `outbox.py` 는 바뀌지 않았다. 지원하지 않는 쓰기는 바로 failed 가 되고 `blocks_later` 로 뒤 쓰기를 막는다(`:222-235 · 307-325 · 484-489`). 이 처리는 남은 not-supported 경로(writer 미설정 · 표 밖)에만 걸린다.
- **예전 trial 거절로 failed(NOT_SUPPORTED) 된 행**: 예전 운영 연결에서는 계획 단계(`_trial`)가 먼저 거절해서 op 자체를 만들지 않았다. 그래서 outbox 에 NOT_SUPPORTED 행이 생기는 길은 사실상 없었다. 혹시 행이 있어도 failed 는 끝 상태라 다시 보내지 않는다. 그러니 이번 변경으로 옛 행이 되살아나 KOS 로 나가는 자리는 없다. migration 도 필요 없다.
- 큐 처리 회차 대상은 `syncable_hospital_ids()`(`tasks/emr.py:43`)와 `syncable_connection()`(`emr_sync.py:114`)가 정한다. 둘 다 같은 `_syncable()` 조건을 쓴다.

### 4. auth — PASS
- `connected_candidates`(`services/auth.py:166-180`)에 남은 조건: `syncable_conditions()`(끊긴 연결 · 지운 병원 · 꺼진 병원 — `crm_connections.py:21-26`), 업체 KOS, 소속 테넌트 `tenant.in_(tenant_ids)`. app_env 하나만 빠졌다.
- 다시 고르기(`_choose`, `:238-245`)는 여전히 두 가지를 확인한다. 고른 병원이 임시 토큰 후보에 있는지, 그리고 지금도 그 테넌트로 연결 조건을 통과하는지(5분 사이 끊김).
- 라우터 두 곳(`routers/api/auth.py:57 · 74` · `routers/login.py:120 · 140`)은 인자 하나만 줄었다. 응답 · 오류 코드는 그대로다.

### 5. 테스트가 A1~A3 을 막나 — 대체로 PASS(WARN 2)
**A1**
- `test_kos_board_contract.py`: CC 5개는 trial 인자 없이 계획되고 `write_open` 을 통과한다(`:127-132`). CLOSED 3개는 계속 거절된다(`:135-138`).
- `test_cc_근거_쓰기의_경로_본문_확인_조건`(`:195-215`)이 경로 · 본문 · 확인 조건까지 고정한다.
- `test_kos_client.py:263-305` 는 5개 명령이 실제 HTTP(가짜 transport)로 그 직원 토큰을 달고 나가는지까지 본다. 표 밖 4개는 요청이 0인지 본다.

**A2** — `test_cc_근거_쓰기는_데모_실제_병원_연결에서_같은_op_을_쌓는다`(`test_board_api.py:394-418`, infra)
- 데모 픽스처와 실제 병원 픽스처(`conftest.py:110-124`, `is_demo = tenant_prefix != "real"`)에서 같은 조작 순서를 돈다. 병원 id 를 `H` 로 바꾼 뒤 op(조작 · 경로 · 본문 · 확인 조건)이 같은지 단언한다.
- not_supported 0 도 단언한다.
- 빈 목록끼리 같아서 통과하는 경우는 `by_kind` 부분집합 단언이 막는다(재호출 · 시작 취소 · 완료 취소 · PROCEDURE_DONE).
- 빈틈 → W2.

**A3**
- `test_emr_rules.py:208-230`(DB 없음): 연결을 고르는 함수 6개의 시그니처와 4개 모듈 · `tasks/emr.py` 소스에 `app_env` 가 없는지 단언한다. 서버 값으로 가를 길 자체가 없다는 구조 증명이다.
- `test_emr_sync_service.py:114-150`(infra): 데모 · 실제 연결 둘 다 동기화 대상이고, dev · prod 모두 실제 연결 회차가 돈다. 끊긴 연결은 dev · prod 모두 돌지 않는다.
- `test_auth_api.py:303-324`(infra): 후보에 둘 다 있고, 실제 병원을 다시 골라도 200, 실제 병원만 소속이어도 signed_in.
- prod 의 로그인 후보는 API 테스트가 없다. 위 구조 테스트가 대신 막는다(참고 2).

### 6. 화면 · API 계약 · 문구 변경 0 — PASS
- diff 에 templates · static · styles · schemas · `routers/`(api 제외 화면) 응답 모양 변경이 없다. `routers/login.py` · `api/auth.py` 는 서비스 호출 인자만 바뀌었다.
- `ActionResult.not_supported` 필드는 그대로이고, 오류 코드 · 경로도 그대로다.

### 7. pytest · ruff — PASS
not infra 442 passed. ruff check · format 통과.

---

## WARN

### W1. dev 에 머지하는 순간 dev 서버가 dev 스키마의 **모든** 연결을 동기화하고 KOS 에 쓴다 — 데이터 전제를 머지 전에 확인
- 바뀐 곳은 `crm_connections.py:21-26` · `board.py:185-191` · `services/auth.py:177` 이다. 이제 dev 가 실제 병원을 건드리지 않는 근거는 「dev 스키마에 데모 병원 연결만 있다」는 **데이터뿐**이다(Delivery (나) · SPEC-000 :218-224). 의도한 설계다.
- 코드로 연결을 만드는 곳은 `ensure_demo_connection`(`crm_connections.py:112`, `is_demo=True`) 하나뿐이다. 하지만 손으로 넣은 행이나 예전 실험 행이 dev 스키마(`day_dev`)에 남아 있으면, `dev` push 직후 worker 가 그 병원을 동기화하고, 판 조작이 그 병원 KOS 에 5개 쓰기까지 보낸다.
- 이건 **확인 못 함**(공유 DB 금지)이다. 머지 · push 전에 사용자 또는 코디가 확인할 것: `day_dev.crm_connection` 에 `is_demo = false` 이거나 데모 테넌트가 아닌 `config.tenant_id` 가 0행인지. 로컬 DB 도 같다.

### W2. A2 API 테스트에 [귀가 대기] 1(`cancel-flow-tasks`)이 빠졌다(조용히 통과하는 자리)
- `_cc_writes`(`test_board_api.py:341-386`)는 모든 시술을 완료한 뒤 [귀가 대기]를 누른다. 그러면 안 끝난 「방 배정」 작업이 없어서 `home_intents` 가 `cancel_room_tasks` 를 만들지 않는다(`board.py:770-774` — `room_tasks` 가 있을 때만).
- 그래서 `demo_ops == real_ops` 는 cancel 이 양쪽 모두 0개인 상태로 같다. `by_kind` 부분집합(`:406-411`)에도 cancel 은 없다.
- Delivery A2 의 「[귀가 대기]」 중 PROCEDURE_DONE 쪽만 API 로 막혀 있다. cancel 은 단위 테스트(`test_kos_board_contract.py` CC · `test_kos_client.py`)만 막는다.
- 계획 · 보내기 경로가 연결 종류를 안 받으므로 실제 위험은 낮다. 그래도 A2 문구대로라면, 방 배정 작업이 남은 판으로 귀가 대기 한 번을 더해 `cancel-flow-tasks` 가 양쪽 op 에 있는지 단언하는 게 맞다.

### W3. 「`is_demo` 로 동작을 가르지 않는다」를 지키는 테스트가 없다(조용히 통과하는 자리)
- 사용자 결정 · Delivery (다)는 「`is_demo` 를 읽는 곳은 칸 · 모델 · 시드 · 그 테스트만」이다. 지금 코드는 그렇다(1번 표).
- 하지만 이것을 막는 테스트가 없다. `test_연결_고르기는_APP_ENV_를_받지_않는다`(`test_emr_rules.py:208-230`)는 `app_env` 만 본다. 누가 나중에 `if connection.is_demo:` 를 서비스 · emr 에 넣어도 테스트는 초록이다.
- 레포 규칙 「경계는 `tests/architecture/` 가 지킨다. 문서로만 두지 않는다」(AGENTS.md 계층 규칙)에 비춰 보면, `tests/architecture/` 에 이 테스트를 두는 게 맞다: `backend/day` 안에서 `is_demo` 가 나오는 파일이 `models/hospital.py` · `services/crm_connections.py`(시드) · `public.py` 뿐인지 확인하는 테스트.

---

## 참고(판정 무관 · 낮음)
1. `writes.py` 모듈 docstring 에서 「확인 조건(`expect`)은 우리 형식이다 … `status` | `status_not` | `status_in` | … 」 단락이 지워졌다(diff `writes.py` 옛 :157-160). #234 와 상관없는 설명이 빠진 것이다. `outbox.py:57-62` `TASK_KEYS` 가 같은 정보를 코드로 갖고 있어 해는 작다. 되살리는 편이 낫다.
2. `test_emr_sync_service.py` 의 `app_env` 파라미터화(`:107-111 · 126-150`)는 `emr_sync` 가 이제 `app_env` 를 읽지 않으므로 dev · prod 가 같은 일을 두 번 하는 셈이다. 막는 힘은 사실상 `test_emr_rules.py` 의 구조 테스트에서 나온다. 해는 없다.
3. 로그인 후보에서 「끊긴 연결 · 꺼진 병원」이 빠지는지를 auth API 로 직접 확인하는 테스트는 예전부터 없다. 조건 함수를 동기화와 같이 쓰므로(`crm_connections.py:30`), `test_emr_sync_service.py:114-123` 의 cut · off 가 간접적으로 막는다. 기존 부채이고 이번 변경과는 무관하다.

## 확인 못 함
- infra 테스트 163개(A2 · A3 의 API · DB 테스트 포함)는 이번에 돌리지 않았다(브리프 지시 — 코드로 읽고 판정). 머지 전에 `scripts/test.sh` 를 돌려야 한다.
- dev 스키마 데이터 전제(W1)
- 확인 안 된 4개 쓰기의 KOS 실물 동작(OQ-23 · A6)

## 직원이 실물에서 만날 자리
- 운영(prod) 병원이 연결되면 시작 취소 · 완료 취소 · 귀가 대기 · 재호출이 첫날부터 KOS 에 나간다. 그중 4개는 아직 KOS 실물 확인 전이다. KOS 가 거절하면 outbox 가 3번 다시 보낸 뒤 failed 가 되고, 같은 방문의 뒤 쓰기까지 막힌다(`outbox.py:215-219 · 307-309`). 예전에는 not_supported 로 기록만 남았다. 지금은 「쓰기 실패」 이벤트 · 반영 대기 칸이 보인다. 의도된 변화이고(Delivery · OQ-23), A6 실물 확인이 먼저다.

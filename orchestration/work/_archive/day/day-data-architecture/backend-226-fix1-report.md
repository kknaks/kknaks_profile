# Delivery #226 fix1 — 검수 WARN W1 ~ W6 + 병원 경계 결과 보고

## 상태: done (커밋 안 함 · 모델 · migration 변경 없음 · KOS 실물 호출 없음 · W7 · W8 손대지 않음)

## 검증

| 명령 | 고치기 전(검수 수치) | 고친 뒤 |
|---|---|---|
| `uv run pytest -q -m "not infra"` | 131 passed · 72 deselected | **153 passed · 67 deselected** (2.7s) |
| `scripts/test.sh -q`(compose postgres · redis, `DAY_REQUIRE_INFRA=1`) | 203 passed | **220 passed** (19.2s) |
| `uv run ruff check backend scripts` | pass | All checks passed |

compose 는 `up -d --wait postgres redis` 로 띄우고 끝나고 `down` 했다(11042 · 11043 만).

### 테스트 이동 전후 (#226 파일 · 전체 / DB 없이)

| 파일 | 전 | 후 |
|---|---|---|
| `test_outbox.py` | 8 / 0 | **3 / 0** — DB 가 보장하는 것만(조건부 UPDATE 경합 · 동시 적재 seq · 막힘 UPDATE + event_log) |
| `test_outbox_rules.py`(새) | — | **12 / 12** — 전이 판단 전부 |
| `test_emr_sync_service.py` | 7 / 0 | **5 / 0** — Redis 잠금 · is_demo SQL 만 남김 |
| `test_emr_rules.py`(새) | — | **9 / 9** — W1 후보 3 · W3 TTL · 상한 · 설정 4 · 오늘 범위 · 주기 라벨(옮김) |
| `test_sync.py` | 7 / 0 | **9 / 0** — W1 infra 1 · 병원 경계 1 추가 |
| `test_kos_client.py` | 9 / 9 | **10 / 10** — W5 로그 1 추가, W1 응답 id 단언 추가 |
| `test_kos_mapper.py` · `test_redis.py` · `test_emr_vendor_boundary.py` | 14/14 · 3/2 · 2/2 | 그대로 |
| 전체 infra / not infra | 72 / 131 | **67 / 153** |

## W 별 고친 곳

### W1 — 매핑 실패로 뺀 기준 정보를 사라짐으로 처리하지 않는다
- `backend/day/emr/normalized.py:125` `NMasterData.response_ids` — 종류별 「응답에 있었던 외부 id」(매핑 실패 포함).
- `backend/day/emr/kos/__init__.py:79-131` `fetch_master.keep()` 가 매핑 전에 응답 id 를 싣는다. 방 · 예약 그룹 조회도
  매핑에 실패한 구역까지 포함해 응답 구역 id 로 부른다(`:96 · :100` — 구역 하나가 매핑에 실패해도 그 방이 사라지지 않게).
- `backend/day/emr/sync.py:260` `absence_keep(response_ids, mapped_ids)` — 순수 함수. 응답 ∪ 매핑된 id, **응답이 비거나
  그 종류가 전부 매핑 실패면 None = 그 회차엔 사라짐 표시 안 함**. `:273` `_mark_absent_master` — 응답엔 있었는데 이번에
  잇지 못한 것(매핑 실패 · 「방 — 구역 모름」)은 기존 연결을 찾아 `seen` 에 합친다. 구역 · 방 · 예약 그룹 · 직무 · 직원 ·
  코드 3종의 `mark_absent` 호출을 전부 이것으로 바꿨다.
- 테스트: DB 없이 `test_emr_rules.py` 3개(후보 계산) · infra `test_sync.py:326`(일부 실패 → 그 직원 그대로 · 전부 실패 →
  3명 그대로) · `test_kos_client.py` 기준 정보 테스트에 「매핑 실패한 group-2 도 response_ids 에」 단언.
- 뜻이 바뀐 것: 외부에서 그 종류 목록이 **정말로 0건**이 되어도 그 회차엔 사라짐 표시를 하지 않는다(코디 결정 문구대로).

### W2 — outbox 전이 판단을 순수 함수로, 상태 전이 테스트를 DB 없이
- `backend/day/emr/outbox.py:144` `Transition` · `:163` `decide_after_send(op, supported, error)` · `:179`
  `decide_on_poll(op, same_visit, received)` — 판단만. `:203` `_apply` 가 조건부 UPDATE 로 저장, `:227` `_block_later`
  가 뒤 pending 막기 + `event_log`. `send_pending`(`:263`) · `confirm`(`:333`)은 판단 → `_apply` 만 부른다. 동작은 전과 같다
  (옛 infra 8개를 리팩터 직후 그대로 돌려 8 passed 확인한 뒤 옮겼다). `OutboxRow` 에 `last_error` 를 더해 「기다림」 전이가
  오류 칸을 건드리지 않게 했다.
- 테스트: `test_outbox_rules.py` 12개(sent · retry · 3번째 failed+막힘 · 지원 안 함 · confirmed · waiting → resend ·
  재전송 소진 failed · 안 보낸 것 무시 · 거절 뒤 맞음/안 맞음 · superseded · 끝난 행 · expect_met 경계). infra 는
  `test_outbox.py:106`(같은 스냅샷 두 쪽 → 하나는 `conflict`) · `:122`(W4) · `:155`(막힘) 3개.
- DB 가 필요 없는데 infra 이던 `today_window` · 주기 라벨 → `test_emr_rules.py` 로 옮김(주기 테스트는 닿지 않는
  `REDIS_URL` 로 브로커만 만든다).

### W3 — 잠금 TTL 일마다 · 회차 상한
- `backend/common/config.py:79-82` `SYNC_SCHEDULE_LOCK_TTL_SECONDS=60` · `SYNC_MASTER_LOCK_TTL_SECONDS=300` ·
  `OUTBOX_LOCK_TTL_SECONDS=60` · `SYNC_LOCK_MARGIN_SECONDS=5`(옛 `SYNC_LOCK_TTL_SECONDS` 는 지움). `:118` TTL 이 여유보다
  짧으면 설정 거절.
- `backend/day/services/emr_sync.py:67` `lock_ttl(job)` · `:79` `run_budget(job)` = TTL − 여유 · `:121`
  `asyncio.timeout(budget)` 이 연결 조회 · 어댑터 · 본문(받기 + 반영 transaction)을 감싼다 → 넘기면 `status="timeout"`.
  잠금은 `SyncDeps.lock` 으로 바꿔 끼울 수 있다(DB · Redis 없는 테스트용).
- 일정 회차 안에서 기준 정보까지 돌던 것을 뺐다 — 55초 상한 안에 300초짜리 일을 넣지 않게. 대신 `RunResult.needs_master`
  (`:49 · :175`)를 세우고 태스크가 `day.emr.sync_master_hospital` 을 따로 발행한다(`backend/day/tasks/emr.py:49`).
  scheduler 시작 때 기준 정보 주기도 바로 한 번 돌므로 평소 경로는 같다.
- 테스트(DB 없이): `test_emr_rules.py` — TTL 60/60/300 · 상한 = TTL−5 · 설정 거절 · 상한 1초로 끝나지 않는 본문 →
  `timeout`(그 잠금 키 · TTL 로 잡았는지도) · 잠금 못 잡으면 외부 안 부르고 `skipped_locked`.

### W4 — 동시 적재 seq
- `backend/tests/day/emr/test_outbox.py:122` — A 세션이 넣고 commit 전인 동안 B 세션이 넣는다 → seq `[1, 2]`.
- **advisory lock 을 지우면 실패하는 것을 직접 확인**: `outbox.py:104` 의 `pg_advisory_xact_lock` 를 잠시 지우고 돌리면
  `assert [1, 1] == [1, 2]` 로 실패, 되돌리면 통과. 유일 제약 migration 은 하지 않았다(첫 실제 쓰기 Delivery).

### W5 — 로그에서 테넌트 id 빼기
- `backend/day/emr/kos/client.py:203 · 237` 토큰 로그는 `hospital=<DAY 병원 id>`(`KosClient(log_label=…)`, `:124-128`,
  `factory.py:47` 가 넘긴다).
- **검수에 없던 누출 하나 더**: httpx 가 INFO 로 요청 URL 을 찍는데 내부 API URL 에 `tenants/{테넌트 id}/…` 가 통째로 있다
  (실물 worker 로그에도 남았을 것). `client.py:32` 에서 httpx 로거를 WARNING 으로 올렸다(cc 와 같은 처리).
- 테스트: `test_kos_client.py::test_토큰_로그에_테넌트_id_를_남기지_않는다` — httpx 포함 모든 로그에 테넌트 id · 끝 4자리
  없음. httpx 줄을 지우면 이 테스트가 실패하는 것도 확인했다.

### W6 — 확인 안 된 대체 칸 이름 지우기
- `backend/day/emr/kos/mapper.py:341` `phone or phoneNumber` → `phone` 만(데모 일정 안 visitor 는 `phone{…}`).
- `mapper.py:318` 유입 채널 `categoryId or funnelCategoryId` 지움 → `category_external_id=None`(데모 `get-codes FUNNEL` 에
  카테고리 칸 없음 — 주석).
- `mapper.py:284` `roleId or role.id` 는 남기고 출처 주석(데모 응답 2026-11-06 · fixture `kos_accounts.json`).

### 병원 경계
- `backend/tests/day/emr/test_sync.py:353` `test_사라짐_표시는_그_병원만` — 두 병원에 같은 고정본(같은 외부 id)을 넣고 A 에서
  `zone-b` · `sch-2` 를 사라짐 처리 → A 는 `is_present_in_source=false`, B 는 true · `deleted_at` null · DAY id 도 서로 다름.

## 하지 않은 것

- W7(outbox 중복 발송 · SENT 정체 · 빈 expect) · W8(공용 계정) — 브리프대로 손대지 않음.
- 모델 · migration · KOS 실물 호출 없음. 로직 변경은 테스트로만 확인했다 — 다음 실물 확인 때 `needs_master` 경로(새로 붙은
  병원)가 한 번 도는지 보면 된다.

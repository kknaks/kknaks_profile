# 리뷰 리포트 — day-data-architecture / code · #226 fix2 재검수 (2026-11-06)

대상: 같은 워크트리의 미커밋 변경(fix2 반영 뒤). 근거 문서는 `backend-226-fix2-instructions.md` · `backend-226-fix2-report.md`, 앞 리포트는 `review-226-fix1-report.md` 다.
읽기 전용으로 봤다. KOS 호출은 하지 않았다. W7 · W8 은 넘긴 것이라 보지 않았다.

## 판정: PASS (FAIL 0 · 이번 범위 WARN 0)

N1 · N2 · N3 은 닫혔다. 아래 「참고」 하나(설정 주석이 실제보다 넓게 말함 · sign-in 반복은 일정 경로에 남음)는 이번 지시 범위 밖이라 판정에 넣지 않았다. 다음 Delivery 로 넘기면 된다.

## 직접 돌린 수치

| 명령 | 결과 |
|---|---|
| compose `up -d --wait postgres redis`(11042 · 11043) → 끝나고 `down` | 했음 |
| `scripts/test.sh -q`(DAY_REQUIRE_INFRA=1) | **222 passed / 15.0s** |
| `uv run pytest -q -m "not infra"` | **155 passed · 67 deselected / 2.6s** |
| `uv run ruff check backend scripts` | All checks passed |
| models · migrations diff · `SUPPORTED_WRITES` | 0줄 · `frozenset()` 그대로 |

수정 리포트 수치(222 · 155/67)와 같다. 새 테스트 2개는 DB 없이 돈다(infra 67 그대로).

## N 별 확인

| | 판정 | 근거 |
|---|---|---|
| N1 | **닫힘** | `emr/kos/__init__.py:95` `self._zone_ids = response_ids["zone"]`(매핑 전 응답 id). `:135-141` 기준 정보 없이 처음 부를 때도 응답 행 `id` 를 `mapper.text` 로만 꺼낸다(매핑 안 함 · 중복 제거). 테스트 `test_kos_client.py` `test_일정은_매핑에_실패한_구역까지_응답의_구역_전부로_부른다` — 두 경로(기준 정보 뒤 · 처음) 모두 `zoneIds == ["zone-a", "zone-broken"]`, 그리고 `master.zones == ["zone-a"]` 로 매핑 실패가 실제로 일어났음을 같이 단언한다. 조용히 통과가 아니다 |
| N2 | **닫힘** | `common/redis.py:62-65` `set_once` = `SET key 1 NX EX ttl`. `services/emr_sync.py:63-72` 키 `day:emr:master_requested:{hospital_id}` → **병원별**. 만료는 `MASTER_REQUEST_COOLDOWN_SECONDS`(`config.py:85` · 기본 300 · `ge=10`) → **만료 있음**. `tasks/emr.py:49` `needs_master and claim` 일 때만 발행. 단락 평가라 `needs_master=False` 면 Redis 를 건드리지 않는다 |
| N3 | **닫힘** | `test_emr_rules.py` `test_needs_master_면_기준_정보를_발행하고_억제_시간_안엔_한_번만` — 가짜 `run_schedules` · `get_redis`(SET NX EX 만) · `kiq` 기록. 같은 병원 2번 → 1번, 다른 병원 → 따로 1번, `False` → 0번, 키의 `ex` 가 설정값. `if result.needs_master` 줄이나 claim 조건을 지우면 `published` 가 달라져 실패한다(수정 리포트의 되돌림 확인과 구조가 맞다) |

### 실패 경로 — 기준 정보가 계속 실패할 때

시간 순서(기본값)로 따라가 봤다.
1. t=0: 일정 회차 `done` · `needs_master=True` → 키를 잡고(EX 300) 기준 정보를 발행한다.
2. 기준 정보 회차가 실패한다(`error` · `timeout` · 구역 0건 `done`).
3. t=10 ~ 290: 일정 회차마다 `needs_master=True` 지만 `SET NX` 가 False → 발행하지 않는다.
4. t≈300: 키가 만료되면 다음 일정 회차가 다시 잡고 발행한다. → **병원마다 5분에 한 번**.

맞물림도 봤다.
- 기준 정보 잠금 TTL(300) · 회차 상한(295)이 억제 시간(300)과 같거나 짧다. 앞 기준 정보 회차가 아직 돌고 있을 때 다음 발행이 들어와도 `skipped_locked` 로 바로 끝난다. 잠금이 엇갈리지 않는다.
- 기준 정보가 성공하면 다음 일정 회차부터 `needs_master=False` 라 키는 그냥 만료된다(지울 필요 없음 — 수정 리포트와 같은 판단).
- 1시간 주기의 `sync_master` 는 억제 키와 무관하게 돈다. 억제가 정상 주기를 막지 않는다.
- 일정 회차가 오류 · 시간 초과면 `needs_master=False`(`counts` 비어 있음)라 발행하지 않는다. 이 경우는 1시간 주기가 메운다(fix1 리포트에서 받아들인 것).
- 작은 틈: 키를 잡은 뒤 `kiq` 가 실패하면(Redis 브로커 장애) 5분 동안 다시 발행하지 않는다. 그 순간엔 브로커도 죽어 있어 어차피 못 보내니 해가 없다. 지적하지 않는다.

## 조용히 통과하는 자리

- 새로 찾은 것 없음.
- `FakeRedis` 는 만료를 흉내 내지 않는다. 그래서 「5분 뒤 다시 발행」은 테스트가 직접 보지 않고, 키에 `ex` 가 설정값으로 실렸다는 단언으로 대신한다. 만료 자체는 Redis 가 보장하는 것이고, `set_once` 가 `ex=` 를 넘기는지는 그 단언이 막는다. 받아들일 만하다.

## 참고 (이번 범위 밖 · 다음 Delivery)

- `config.py:83-84` 주석은 억제 키가 「10초마다 KOS sign-in 을 반복하지 않게」 한다고 말한다. 실제로 막는 것은 **기준 정보 회차의 반복**뿐이다. 일정 회차 자체도 내부 API 를 부르므로, 시스템 계정 sign-in 이 실패하는 동안 `KosClient.internal_token` 은 토큰을 캐시하지 못한다. 그래서 **일정 경로가 10초마다 sign-in 을 다시 시도한다**(`client.py` `internal_token` — 실패하면 `_internal_token` 이 None 으로 남음). fix 전부터 있던 동작이다. 계정 잠금이 걱정되면 클라이언트에 「sign-in 실패 뒤 N분 동안 재시도 안 함」(실패 시각 기억 → 그 동안 바로 `KosError`)을 두고, 주석을 실제 범위로 고친다. 운영(실제 병원) 전에 정할 일이다.
- 기준 정보가 한 번도 안 들어온 상태에서 구역 응답이 비면 `_zone_ids` 가 비어 있다. 그러면 `fetch_schedules` 가 10초마다 공개 `get-zones` 를 한 번 더 부른다. 공개 API 한 번이고 데모 · 실병원 모두 구역이 있으니 실해는 없다.

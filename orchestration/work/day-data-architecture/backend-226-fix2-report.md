# Delivery #226 fix2 — 재검수 N1 · N2 · N3 결과 보고

## 상태: done (커밋 안 함 · 모델 · migration 변경 없음 · KOS 실물 호출 없음)

## 검증

| 명령 | fix1 뒤 | fix2 뒤 |
|---|---|---|
| `uv run pytest -q -m "not infra"` | 153 passed · 67 deselected | **155 passed · 67 deselected** |
| `scripts/test.sh -q`(compose postgres · redis, `DAY_REQUIRE_INFRA=1`) | 220 passed | **222 passed** (16.1s) |
| `uv run ruff check backend scripts` | pass | All checks passed |

compose `up -d --wait postgres redis` 후 돌리고 `down` 했다. 새 테스트 2개는 둘 다 DB 없이 돈다(infra 수 67 그대로).

**고친 줄을 되돌리면 실패하는지 직접 확인**: N1 줄을 옛 「매핑된 구역」으로 → N1 테스트 실패 · N2 억제 조건을 빼면
(`if result.needs_master:`) → N2/N3 테스트 실패 · 발행 줄을 막으면(`if False:`) → 같은 테스트 실패. 되돌린 뒤 전부 통과.

## N 별 고친 곳

### N1 — 일정 조회 `zoneIds` 를 응답에 있던 구역 전부로
- `backend/day/emr/kos/__init__.py:95` — 기준 정보 뒤 `self._zone_ids = response_ids["zone"]`(매핑 성공 여부와 무관).
- `backend/day/emr/kos/__init__.py:136-141` — 기준 정보 없이 처음 일정을 부를 때도 구역 응답 행의 `id` 를 `mapper.text` 로
  꺼내 쓴다(매핑하지 않음).
- 테스트(DB 없이): `backend/tests/day/emr/test_kos_client.py:304` — 구역 하나(`order` · `isDefault` 없음)가 매핑에 실패한
  가짜 응답에서, 기준 정보 뒤 · 기준 정보 없이 처음 두 경로 모두 일정 요청 `zoneIds == ["zone-a", "zone-broken"]`.
  (`FakeKos(overrides=…)` 로 경로별 응답을 바꿀 수 있게 했다.)

### N2 — `needs_master` 발행 억제
- `backend/common/config.py:85` `MASTER_REQUEST_COOLDOWN_SECONDS`(기본 300).
- `backend/common/redis.py:62` `set_once(key, ttl)` = `SET key 1 NX EX ttl`.
- `backend/day/services/emr_sync.py:63-72` `claim_master_request(hospital_id)` — 키 `day:emr:master_requested:{hospital_id}`.
- `backend/day/tasks/emr.py:49` — `needs_master` 이고 키를 잡았을 때만 `sync_master_hospital.kiq`. `has_master_data` 의
  뜻(구역 연결 존재)은 그대로.
- 결과: 구역 응답이 비거나 전부 매핑 실패 · 기준 정보가 빨리 실패(sign-in 401 등)해도 기준 정보 발행은 병원마다 5분에 한 번.

### N3 — 태스크 단계 발행 테스트
- `backend/tests/day/emr/test_emr_rules.py:173`(DB · Redis 없이) — `emr_sync.run_schedules` 를 가짜로, `common.redis.get_redis`
  를 `SET NX EX` 만 하는 가짜로, `sync_master_hospital.kiq` 를 기록 함수로 바꾸고 `sync_schedules_hospital(...)` 를 직접
  await. 같은 병원 연속 두 번 `needs_master=True` → 발행 1번 · 다른 병원은 따로 1번 · `needs_master=False` → 0번 · 억제 키의
  만료가 설정값(300)인지.

## 남은 것

- W7 · W8 — 범위 밖(그대로).
- 억제 키가 남아 있는 5분 안에 기준 정보가 성공해도 키는 그대로 둔다(성공하면 `needs_master` 가 False 라 발행할 일이 없다).

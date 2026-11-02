# WORK-003 backend contract failure audit (read-only)

2026-09-20 · 읽기 전용. 코드·테스트·inventory·docs 수정 없음. checkout/reset/stash 없음.
2차 갱신: 승인을 받아 두 파일만 `-n auto --dist worksteal` 로 재현했다.

## 결론 먼저

**네 실패는 재현된다. 원인은 병렬도(CPU 과다구독)이고, request-material 변경과의 인과는 근거가 없다.**
코드를 고정한 채 병렬도만 바꾸면 실패가 켜지고 꺼진다.

| 실행 (코드 동일) | 결과 |
|---|---|
| 단독 / 파일 단독 / 두 파일 순차 | **20 passed** |
| `-n 2 --dist worksteal` | **20 passed** (35.6s) |
| `-n 4 --dist worksteal` | **20 passed** (25.1s) |
| `-n 8 --dist worksteal` | **2 failed**, 18 passed |
| `-n auto` = **11 workers / 11 cores** | **3~5 failed**, 5회 실행 **전부** 실패 |

`-n auto` 5회: 3·4·4·3·5 failed (63.7s / 35.9s / 40.5s / 36.5s / 39.0s).
원본 출력: `scratchpad/parallel/run1..5.txt`.

## 1. seed — **존재하지 않는다 (정정)**

```
plugins: xdist-3.8.0, anyio-4.15.0
created: 11/11 workers
```

**`pytest-randomly` 가 설치되어 있지 않다.** 따라서 `--randomly-seed` 도 없고 수집 순서는 **결정적**이다.
직전 보고서에서 파일 단독 실행을 「기본 = random 순서」라고 적은 것은 **틀렸다** — `-p no:randomly` 도
무효 옵션이었다. 변동 요인은 순서가 아니라 **병렬 실행의 타이밍** 하나다.

## 2. 실제 실패와 첫 실패 assertion

브리프의 4건에 더해 **다섯 번째 테스트가 함께 깨진다** (브리프 목록에 없던 것):

| 테스트 | 5회 중 실패 |
|---|---|
| `test_material_worker_recovery.py::test_stage_timeout_fences_the_late_parser_result` | **5/5** |
| `test_material_search.py::test_search_returns_bounded_excerpts_only_for_authorized_live_bindings` | **5/5** |
| `test_material_search.py::test_searching_without_naming_the_work_finds_what_this_person_may_read` ← **목록 밖** | **5/5** |
| `test_material_worker_recovery.py::test_long_parse_heartbeats_its_lease_so_a_second_worker_cannot_reclaim_it` | 3/5 |
| `test_material_search.py::test_naming_the_work_still_scopes_the_search_to_it` | 1/5 |

첫 실패 assertion (run2):

```
# test_stage_timeout_fences_the_late_parser_result
>   assert extraction.status == "failed" and extraction.failure_reason == "time_limit_exceeded"
E   failed and 'worker_attempt_lost' == 'time_limit_exceeded'

# test_long_parse_heartbeats_its_lease_so_a_second_worker_cannot_reclaim_it
>   assert extraction.status == "running" and extraction.heartbeat_at is not None and ...
E   assert ('queued' == 'running')

# test_search_returns_bounded_excerpts_only_for_authorized_live_bindings
>   assert search["searched_materials"] == 2 and search["unavailable_materials"] == []
E   assert (1 == 2)

# test_searching_without_naming_the_work_finds_what_this_person_may_read
>   assert {row["name"] for row in theirs_found["results"]} == {"남견적.md"}
E   assert set() == {'남견적.md'}
```

**넷이 한 가지를 말한다: 추출 워커가 제때 CPU 를 받지 못했다.**

- `queued` — `sleep(3.15)` 동안 워커 코루틴이 **claim 조차 못 했다**
- `worker_attempt_lost` — 3초 lease 가 1초 stage timeout 보다 **먼저** 만료됐다
  (`material_queue_visibility_timeout=3`, `material_stage_timeout_seconds=1`)
- `1 == 2`, `set()` — 검색 시점에 추출이 **아직 색인되지 않았다**

## 3. request-material 변경과의 인과 — **근거 없음**

1차 감사의 도달 불가 근거가 그대로 서고, 이번 출력이 그것을 뒷받침한다.

- 두 파일에 work request 가 **0건**이다: `reset_database()` 는 `seed_catalog` 까지이고
  (`bootstrap/reset.py:9-22`), fixture 를 심는 `seed_demo_work` 는 **CLI 전용**이다
  (`reset_demo.py:71-73`). 실측 `work_requests: 0` · `attachment_bindings: 0`.
  두 파일에 문자열 `work_request` / `work-request` **0회**.
- 그래서 `bootstrap/material_sources.py:76-77` 의 `requests.list(principal)` 이 `[]` 를 낸다
  → `modules/work/requests.py:1199 list()` 본문이 돌지 않아 **`_view`(`:1360`, 내가 3키를 더한 곳)가
  실행되지 않고**, `material_sources.py:82-83` 의 루프가 돌지 않아 **`material_bindings`(`:1013`)·
  `_material_bindings_for`(`:926`)도 실행되지 않는다.**
  `open_attachment`(`:1036`, F-2 가드)는 그 라우트를 부르는 테스트가 없어 닿지 않는다.
- 실패 문구 자체가 요청 자료와 무관하다: lease·heartbeat·색인 지연이다.
- **결정적 근거**: 코드를 **한 줄도 바꾸지 않고** 병렬도만 11 → 4 로 낮추면 20/20 통과한다.
  변경 diff 가 원인이라면 병렬도에 따라 켜졌다 꺼졌다 하지 않는다.

이 테스트들에서 실제로 실행되는 내 변경은 둘뿐이고 모두 동작 보존이다:
`materials.py:317` 의 위임 리팩터(본문 그대로 이동), `platform/materials.py::_SAFE_KEY` 의
`work_requests/<uuid>/(?:comments|evidence|materials)` 내부 추가
(업무 자료가 쓰는 `(?:tasks|meetings|material_folders)/<uuid>` 갈래는 불변).

## 4. 남는 사실 — 이건 테스트 쪽 문제다 (수정하지 않음)

이 테스트들은 **벽시계 여유를 직접 단다**: heartbeat 테스트는 3초 lease 에 `sleep(3.15)` 로 **150ms**,
stage timeout 테스트는 `time.monotonic() 차 < 12.0` 예산이다. 11코어에 11 워커를 띄우고 각 테스트가
자기 asyncio 루프와 SQLite 를 돌리면 그 여유가 먼저 사라진다. `make test-contract` 가 `-n auto` 이므로
**이 기계에서는 상시 실패한다** — 이번 변경 이전에도 같았을 것으로 보이나, 그 단정에는 baseline 비교가
필요하고 그것은 금지된 stash/checkout 을 요구하므로 **단정하지 않는다.**

후속 선택지(실행하지 않음): 이 다섯 테스트에 병렬 격리 표식을 주거나, lease/stage 여유를 CPU 부하에
견디게 키우거나, `make test-contract` 의 `-n auto` 를 코어보다 낮게 고정하는 것.
어느 쪽이든 **테스트·설정 변경**이라 이 읽기 전용 브리프 밖이다.

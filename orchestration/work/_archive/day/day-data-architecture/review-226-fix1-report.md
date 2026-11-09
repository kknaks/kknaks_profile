# 리뷰 리포트 — day-data-architecture / code · #226 fix1 재검수 (2026-11-06)

대상: 같은 워크트리의 미커밋 변경(fix1 반영 뒤). 근거 문서는 `backend-226-fix1-instructions.md` · `backend-226-fix1-report.md`, 앞 리포트는 `review-226-report.md` 다.
읽기 전용으로 봤다. KOS 호출은 하지 않았다. W7 · W8 은 넘긴 것이라 보지 않았다.

## 판정: WARN (FAIL 0)

W1 ~ W6 · 병원 경계는 지적대로 닫혔다. 새로 생긴 동작에서 작은 지적이 둘(N1 · N2) 나왔고, 「조용히 통과」가 하나(N3) 있다. N1 은 W1 과 같은 종류의 구멍이 일정 쪽에 남은 것이라 이번에 같이 닫기를 권한다. N2 · N3 는 다음 Delivery 로 미뤄도 된다.

## 직접 돌린 수치

| 명령 | 결과 |
|---|---|
| `uv run pytest -q -m "not infra"` | **153 passed · 67 deselected / 2.8s**(수정 리포트와 같음) |
| `uv run ruff check backend scripts` | All checks passed |
| `scripts/test.sh -q` | **220 passed / 20.1s** — 코디 추가 지시(compose 손대지 말 것)를 받기 **전에** 1회 돌렸다. 그때 실행한 `up -d --wait postgres redis` 는 이미 healthy 이던 backend 워커의 컨테이너에 대해 아무것도 바꾸지 않았다(재생성 없음 · `down` 안 함). 테스트는 `day_test` 스키마와 Redis db 15 를 쓴다. 수치는 수정 리포트 · 코디 확인 220 과 같다 |

## W 별 확인

| | 판정 | 근거 |
|---|---|---|
| W1 | **닫힘** | `sync.py:260-270` `absence_keep`(응답 ∪ 매핑, 비거나 전부 실패하면 None) · `:273-289` `_mark_absent_master`(응답엔 있었지만 잇지 못한 연결을 `lookup` 해 `seen` 에 합친다). `kos/__init__.py:81-131` `keep()` 이 매핑 **전에** 응답 id 를 싣고, 방 · 예약 그룹은 응답 구역 id 로 부른다(`:96 · :100`). DB 없는 테스트 `test_emr_rules.py:29-40` 3개, infra 테스트 `test_sync.py:326-350`. **조용히 통과가 아님을 확인했다**: `master_data()` 가 fixture 원본 id 로 `response_ids` 를 채운다(`test_sync.py:77`). 그래서 첫 단언(acct-doctor 는 응답에 있고 매핑에 없음)은 `held` 경로를 실제로 탄다. 기존 사라짐 테스트도 `only()`(`:92-95 · :230`)로 응답 id 까지 줄이도록 고쳐져, 진짜 사라진 행은 여전히 사라짐 처리되는 것을 확인한다 |
| W2 | **닫힘** | `outbox.py:143-200` `Transition` · `decide_after_send` · `decide_on_poll` 은 순수 함수다. `_apply`(`:203`)가 조건부 UPDATE 를 하고, `_block_later`(`:227`)가 막힘 처리와 event_log 를 맡는다. 옛 코드와 한 줄씩 대조했다(sent 는 attempts 유지 · checks 0 · error None / waiting 은 checks+1 · error 유지 / 지원 안 함은 attempts 그대로 failed + 막힘 / resend 와 failed 의 갈림). 동작은 같다. `test_outbox_rules.py` 12개는 DB 없이 돈다(import 는 `outbox` · `mapper` · `normalized` · enums 뿐). infra 3개(`test_outbox.py:106 · :122 · :155`)는 조건부 UPDATE · advisory lock · 막힘 UPDATE 로, DB 가 보장하는 것만 남았다. `today_window` · 주기 라벨은 `test_emr_rules.py:115-154` 로 옮겨졌다(브로커는 닿지 않는 주소로 import 만 한다). 설정 캐시는 `tests/conftest.py:31-38` autouse 가 테스트마다 지우므로 TTL 을 바꾼 테스트가 다른 테스트에 새지 않는다 |
| W3 | **닫힘**(새 동작은 N2) | `config.py:79-82` TTL 60 / 300 / 60 · 여유 5, `:118-124` TTL ≤ 여유면 설정을 거절한다. `emr_sync.py:67-81` `lock_ttl` · `run_budget`. `:121` `asyncio.timeout(budget)` 이 연결 조회 · 어댑터 · 본문(받기 + 반영 + commit)을 감싸고, 넘기면 `timeout` 이다. 잠금은 `try_lock` 의 `finally` 가 자기 토큰일 때만 푼다. DB 없는 테스트 `test_emr_rules.py:46-109` |
| W4 | **닫힘** | `test_outbox.py:122-150` — A 가 commit 하기 전에 B 를 띄우고 0.3초 기다린 뒤 A 를 commit → `[1, 2]`. 「lock 을 지우면 `[1, 1]`」은 수정 리포트가 직접 확인했다고 적었다. 테스트 구조상 그 주장이 맞다(lock 이 없으면 B 의 `max(seq)` 는 A 의 미커밋 행을 못 본다) |
| W5 | **닫힘** | `client.py:203 · 237` 은 `hospital=<DAY id>` 로 남긴다(`factory.py:47` 이 넘김). `client.py:32` httpx 로거를 WARNING 으로 올렸다. httpx 는 요청 URL 을 INFO 로만 찍으므로 WARNING 이면 URL 이 빠진다. `test_kos_client.py:271-288` 이 DEBUG 로 잡아도 테넌트 id 와 그 끝 4자리가 없는지 본다. 다른 자리도 살폈다: `KosError` 메시지는 상태 · 오류 이름 · 경로 끝 조각뿐, 네트워크 오류는 클래스 이름뿐(`client.py` `_post`), `_run` 로그는 `hospital_id` 뿐, taskiq 태스크 인자는 `hospital_id` 문자열뿐, `ConnectionConfig.__repr__` 은 접속값을 뺀다. httpcore 는 DEBUG 에서도 host 와 단계만 찍고 헤더 · 경로는 찍지 않는다. **새는 자리 없음** |
| W6 | **닫힘** | `mapper.py:341` `phone` 만 남음 · `:309-318` 유입 카테고리는 None 으로 비우고 주석을 달았다 · `:284-286` `roleId or role.id` 에 출처 주석 |
| 병원 경계 | **닫힘** | `test_sync.py:353-373` — 두 병원에 같은 외부 id 를 넣고 A 에서 `zone-b` · `sch-2` 를 사라짐 처리 → B 는 `is_present_in_source=true` · `deleted_at` null · DAY id 도 서로 다르다 |

테스트 분류(2026-11-06 규칙): 전체 infra / not-infra 는 72 / 131 → **67 / 153** 이다. `test_emr_sync_service.py` 에 남은 infra 5개는 Redis 잠금 · `is_demo` SQL 필터 · `needs_master` 판단(`has_master_data` 조회)이다. 모두 DB · Redis 가 있어야 의미가 있다. **규칙에 맞다.**

## WARN

### N1. 일정 조회는 아직 **매핑된** 구역 id 로만 부른다 — 구역 하나가 매핑에 실패하면 그 구역의 오늘 방문이 「사라짐」 처리된다 — `emr/kos/__init__.py:94 · 135-141`
- 근거: W1 에서 방 · 예약 그룹은 응답 구역 id(`response_ids["zone"]`)로 부르게 바꿨다. 그런데 `self._zone_ids` 는 여전히 `tuple(z.external_id for z in zones)`(매핑된 것)이다(`:94`). 일정이 없을 때 다시 받는 경로(`:135-137`)도 매핑된 것만 쓴다. 그 구역의 일정은 요청 자체에 들어가지 않는다. 응답에도 `skipped_external_ids` 에도 없으니, `apply_schedules` 의 오늘 범위 사라짐 처리(`sync.py` `in_window`)가 그 방문들을 `deleted_at` 으로 바꾼다. W1 과 같은 종류의 구멍이다(매핑 실패 → 사라짐).
- 실물: KOS 가 구역 하나의 `order`/`isDefault` 를 빼면 그 층의 오늘 환자가 현황판에서 통째로 사라진다. 구역 응답이 고쳐지면 다음 10초 회차에 되살아난다.
- 고칠 방향: `:94` 를 `self._zone_ids = response_ids["zone"]` 으로, `:135-137` 은 응답 행의 `id` 를 `mapper.text` 로 꺼내 쓴다(매핑 성공 여부와 무관하게). DB 없는 테스트 1개: 구역 하나가 매핑에 실패한 fake 응답에서도 일정 요청 `zoneIds` 에 그 구역이 들어 있는지.

### N2. `needs_master` — 기준 정보가 「완료」돼도 구역 연결이 0이면 일정 회차마다(10초) 기준 정보 회차를 다시 넣는다 — `services/emr_sync.py:159-175` · `tasks/emr.py:46-52` · `services/crm_connections.py` `has_master_data`
- 경로를 따져 봤다:
  - 잠금 엇갈림: **없음**. 일정 회차는 기준 정보를 직접 돌리지 않고 자기 잠금을 푼 뒤 발행만 한다. 기준 정보는 자기 잠금(300초)으로 돌고, 도는 동안 들어온 발행은 `skipped_locked` 로 바로 끝난다.
  - 일정이 계속 미뤄지는가: **아니다**. 첫 일정 회차는 아는 참조만 잇고(모르는 참조는 None · 필수 참조 칸은 뺌), 기준 정보가 들어온 뒤 다음 회차의 upsert 가 참조를 채운다. 일정이 기준 정보를 기다리지 않는다.
  - 일정 회차가 오류 · 시간 초과면 `counts` 가 비어 `needs_master=False` 다. 기준 정보는 1시간 주기와 scheduler 시작 때 한 번 도는 회차로 메워진다. 받아들일 만하다.
- 구멍: `has_master_data` 는 「구역 `external_ref` 가 하나라도 있나」다. 그런데 W1 뒤로는 **구역 응답이 비었거나 전부 매핑에 실패하면** 기준 정보 회차가 `done` 이어도 구역 연결이 생기지 않는다(`link` 할 구역 0). 그러면 `needs_master` 가 영원히 True 다. 기준 정보 회차(내부 sign-in 이 낀 KOS 호출 10여 번)가 **10초마다** 발행된다. 기준 정보가 빨리 실패하는 경우(시스템 계정 sign-in 401 등)도 같다. 그 경우 sign-in 시도가 10초마다 반복돼 KOS 쪽 계정 잠금 위험이 있다. 이 동작은 fix 전(일정 회차 안에서 바로 run_master)에도 같았으니 새 퇴보는 아니다. 다만 이번에 발행 경로가 분리되면서 막기가 쉬워졌다.
- 고칠 방향: 발행 쪽에 짧은 억제 키를 둔다. 예: `SET day:emr:master_requested:{hospital} 1 NX EX 300` 에 성공할 때만 `sync_master_hospital.kiq`. DB 없는 테스트는 「연속 두 번 `needs_master` → 발행 1번」. `has_master_data` 의 뜻(구역 연결 존재)은 그대로 둔다.

## 조용히 통과하는 자리

### N3. 태스크 단계의 `needs_master` → `sync_master_hospital.kiq` 발행에 테스트가 없다 — `tasks/emr.py:46-52`
- `test_emr_sync_service.py:140-145` 는 `RunResult.needs_master` 플래그까지만 본다. 플래그가 True 일 때 실제로 기준 정보 태스크가 발행되는지(그리고 False 일 때는 안 되는지)는 아무 테스트도 보지 않는다. `if result.needs_master:` 줄을 지워도 초록이다. 이번 fix 로 「새 병원의 첫 기준 정보」가 이 한 줄에 달리게 됐다(scheduler 시작 회차를 놓치면 최대 1시간 공백).
- 고칠 방향: DB 없는 테스트 1개. `emr_sync.run_schedules` 를 `needs_master=True/False` 를 돌려주는 가짜로 바꾸고, `sync_master_hospital.kiq` 를 기록 함수로 바꾼 뒤(`monkeypatch`) `sync_schedules_hospital(...)` 을 직접 await → 발행 1회 / 0회. N2 의 억제 키를 넣으면 같은 테스트에서 함께 본다.

그 밖에 새 「조용히 통과」는 찾지 못했다. W1 infra 테스트 · 병원 경계 · W4 동시 적재 · W5 로그 테스트는 각각 고친 줄을 지우면 실패하는 구조임을 확인했다(W4 · W5 는 수정 리포트의 직접 확인 + 구조 확인, W1 은 `response_ids` 를 채우는 helper 확인).

## 참고

- W1 뒤의 뜻: 외부에서 그 종류가 **정말 0건**이 되어도 그 회차엔 사라짐 표시를 하지 않는다. 코디 결정 문구대로다. 데모의 `funnel_category`(응답 0건)는 앞으로도 사라짐이 생기지 않는다. 지적하지 않는다.
- `asyncio.timeout` 이 commit 도중에 걸리면 서버에서 commit 이 됐는지 모를 수 있다. 그래도 반영은 upsert · 조건부 UPDATE 라 다음 회차가 같은 결과로 덮는다. 해 없음(쓰기 큐 쪽 중복 발송은 W7 범위).
- 모델 · migration 변경 0, KOS 쓰기 0(`SUPPORTED_WRITES` 그대로)을 다시 확인했다.

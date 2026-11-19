# 리뷰 리포트 — customer-erd / code 4 (검수 3 반영 + 내부 API 만) (2026-11-19)

- 대상: `sync-fix-2.md` · `sync-fix-3-internal-only.md`(「추가」 포함) 반영분 · 워커 `be-2-report.md` 「검수 3 반영 + 내부 API 만」(diff 로 재확인)
- 기준: `git diff origin/dev`(21 파일) + 미추적 · base `origin/dev` `bbd9220a`
- 앞 리포트: `review-code-3-report.md`

## 판정: **PASS (FAIL 0 · WARN 4)**

| 볼 것 | 판정 |
|---|---|
| 1. FAIL-1 닫힘 | **PASS** |
| 2. WARN-1 별도 태스크 | **PASS**(WARN-B) |
| 3. WARN-2 예외 범위 | **PASS** |
| 4. 5분 회차 삭제 · 죽은 코드 0 | **WARN-A**(죽은 코드 · 낡은 주석 몇 줄) |
| 5. 내부 API 만 | **PASS**(WARN-C — 구역 내부 응답은 데모로만 확인) |
| 6. 메뉴 진료항목 · 기기 · 약물 | **PASS**(WARN-D) |
| 7. 기존 운영 코드 변경 범위 | **PASS** |
| 8. 직접 실행 | **PASS** |
| 직원이 실물에서 만날 자리 | **없음**(단 WARN-C 첫 prod 동기화 때 구역 수 확인 권고) |

---

## 1. FAIL-1 — PASS (닫힘)

- 못 푼 티켓 기억: `services/emr_sale_sync.py:168-179` `_remember_unresolved` — 병원별 키 `day:emr:sale_unresolved_tickets:{병원}`(`:68` · `:159-160`) · 만료 = 병원 현지 오늘 끝까지 남은 초(`today_window` · 최소 60초).
- 넣는 때: 그 고객들의 시술권 · 카드를 **commit 한 뒤** DAY 에 여전히 없는 그 고객의 오늘 작업 티켓(`sync_schedule_sales.py:164-178` `unresolved_tickets` · `emr_sale_sync.py:286-291`). 받기 전에 끊기면 넣지 않음 → 다음 회차가 다시 받음(맞음).
- 제외: `ticket_changed_customers` 가 `t.ticket_id is None and ticketId in unresolved` 인 티켓으로는 고객을 넣지 않는다(`sync_schedule_sales.py:160`). 구매가 바뀐 고객(`result.changed_customers`)은 그대로 합집합(`emr_sale_sync.py:221-224`) · `ticketId` 가 바뀌면 다른 id 라 다시 부름 ✓.
- 테스트 `test_sale_sync_runs.py:183` — 첫 회차 시술권 받음 · 집합 `{tkt-old}` · TTL ≤ 24h · **두 번째 회차 호출 == `["purchases"]`** · 티켓 id 바뀌면 다시 부름 ✓.

## 2. WARN-1 — PASS (WARN-B)

- `tasks/emr.py:73-82` — 일정 태스크는 `run_schedules` 뒤 `sync_sales_hospital.kiq(병원, sales_payload(...))` **발행만**(await 없음 · 발행 실패는 로그만 · 반환 `result.status` 그대로). 새 태스크 `day.emr.sync_sales_hospital`(`:95-103`)가 `_isolated` 로 `run_sales`.
- 일정 태스크 실행 시간 · DB 세션: 새 동기화 전과 같음 — 추가는 `.kiq` 1회(Redis LPUSH)뿐, 세션 0. 반환값 같음(테스트 `test_오늘_구매_발행이_실패해도_일정_태스크_결과는_그대로다` · `test_오늘_일정이_없으면…`).
- 입력: 메시지 = 그 일정 응답의 외부 id · sequence · 기기 이름(`emr_sale_sync.py:101-120` — 이름 · 연락처 없음) → `sales_from_payload`(`:123-150`) 왕복 테스트 ✓. KOS 다시 부르지 않음 ✓.
- 유실: 다음 10초 회차가 새 메시지를 다시 발행 · 대기 고객은 Redis 집합에 남음 → 자기 회복 ✓. 중복 · 밀림: `sales` 잠금(`skipped_locked`)으로 병원당 동시 1개 ✓.
- **WARN-B**: worker 가 밀려 **오래된 메시지가 늦게** 처리되면 그 메시지의 처방 목록 · 작업 참조로 반영한다 — 예) 새로 생긴 처방이 옛 메시지 기준 「사라짐」으로 `deleted_at` → 다음 메시지가 되살림, 작업 `ticket_id` 가 잠깐 옛 값. 10초 안에 스스로 맞춰지고 판에는 안 보이지만, 메시지에 발행 시각을 실어 일정 시각보다 오래된 메시지는 버리는 방법이 있다. 또 `sales_from_payload(sales)` 가 `_isolated` **밖**에서 평가돼(`tasks/emr.py:100-102`) 메시지가 깨지면 그 태스크만 예외로 끝난다(판 무관).
- 참고: 메뉴는 여전히 기준 정보 태스크 안에서 await(`tasks/emr.py:88-91`) — 지시 범위 밖 · 기준 정보 잠금은 이미 풀린 뒤라 판과 무관.

## 3. WARN-2 — PASS

- `emr/kos/__init__.py:195-200` — `except Exception: # noqa: BLE001` + 이유 주석 · 판 반영은 계속 · `NormalizedSchedulesData.sales_skipped` 로 셈.
- 테스트 `test_sale_sync_rules.py:200` — `schedule_sale` 이 `KeyError` 를 내도 `visits` · `skipped_external_ids` 가 정상 때와 **같음**을 직접 비교 ✓(검수 3 WARN-5 도 이걸로 닫힘).

## 4. 5분 회차 삭제 — WARN-A

- 지워짐 ✓: 태스크 `day.emr.sync_sale_changes` · `…_hospital`(테스트 `test_5분_회차는_없다…` 가 `find_task(...) is None`) · `run_sale_changes` · `fetch_sale_changes` · `NormalizedSaleChangesData` · Redis `sale_changes_at` · 설정 5개(`common/config.py` 에 `sync_menu_lock_ttl` · `sync_sales_lock_ttl` 만 남음) · 잠금 `sale_changes`(`Job` 에서 빠짐) · 고정본 `kos_stat_*` · `factory.py` 의 통계 주입(diff 0).
- **WARN-A — 남은 죽은 코드 · 낡은 주석**(지우기만 하면 됨):
  - `day/emr/kos/sale_reads.py:113-115` — `stat_limit` · `stat_max_pages` 속성(어디서도 안 씀).
  - `day/emr/kos/sale_reads.py:66-69` — `_utc()`(안 씀) + 위 주석 「공개 통계(5분 ⑤ ⑥)」.
  - 주석: `sale_reads.py:56`(「· 5분 회차」) · `emr/kos/__init__.py:18`(「· 통계」) · `sync_purchases.py:110`(「5분 회차로 다시 받은 구매」 — 지금은 「이미 DAY 에 있는 구매」 경우만).

## 5. 내부 API 만 — PASS (WARN-C)

- 운영 경로(demo 제외) `"open"` 호출 grep:
  ```
  grep -rn '"open"\|/open/\|open_token\|exchange-token' backend/day/emr backend/day/services backend/day/tasks | grep -v /demo/
  → client.py:5,44,58,252,305-317,411-430 (기능 정의 — 남기라는 지시) · writes.py:31 · __init__.py:4,22 (주석) · services/chat_files.py:285 (무관 — 파일 열기 모드)
  ```
  운영 호출 0 ✓. 새 코드는 `sale_reads.ApiKind = Literal["internal"]` 타입 + AST 테스트(`test_새_동기화_코드는_공개_API_를_부르지_않는다`)로 막힘.
- 공개 토큰 0: `test_kos_client.py:373-384` `test_운영_동기화는_공개_토큰을_받지_않는다` — 기준 정보 뒤 · 기준 정보 없이 처음 두 경우 모두 `exchange-token` 0 · 공개 호스트 요청 0 ✓.
- 구역: `PATH_ZONES = "schedule/zone/v1/queries/get-zones"`(`__init__.py:55`) · 두 곳 `_list("internal", …)`(`:114` · `:168`). `mapper.zone` 은 docstring 만 바뀜(칸 `id · title · order · isDefault` 그대로). 기존 테스트 기대가 `("…/get-zones", "open")` → `"bearer"` 로 바뀐 것 외 결과(구역 · 방 · N1 구역 전부 요청) 그대로 통과.
- **WARN-C**: 테스트는 **공개 고정본(`kos_zones.json`)을 내부 경로에도 그대로** 쓴다(`test_kos_client.py:33-34`) — 내부 응답 모양이 같다는 근거는 조사 리포트 §0(데모 id 2/2) · HAR · 워커 DEMO(구역 2 · 방 41 · 판 해시 같음)뿐이다. 내부 목록이 공개와 달리 **닫힌 · 지운 구역을 함께 줄 수 있는지**는 실 병원에서 확인되지 않았다(데모는 2 = 2). 첫 prod 기준 정보 회차 전후 구역 수 · `skipped.zone` 를 한 번 보길 권고.

## 6. 메뉴 진료항목 · 기기 · 약물 — PASS (WARN-D)

- `sale_reads.py:87-107` — 살아 있는 상품 · 옵션 · 구성의 `medicalService` 에서 모음 · id 중복 제거(`_latest` = 같은 id 면 `updatedDateTimeUtc` 가장 늦은 것) · 기기 · 약물은 `configuration.machines[]` · `medicines[]` id 로 중복 제거 ✓. 공개 3 경로 삭제 ✓.
- 「사라짐 ≠ 삭제」: `sync_menu.py` 의 `_absent` 호출에 `TREATMENT_ITEM` · `MACHINE` · `MEDICINE` 없음(`:169 · 292 · 327 · 379 · 450 · 475 · 499 · 522` 는 다른 표) ✓. 테스트 `test_sale_sync.py:235` `test_시술_항목_기기_약물은_옵션에서_빠져도_지우지_않는다` — `deleted_at` 없음 · `is_present_in_source` 그대로 ✓. `is_present_in_source` 를 안 건드린다는 결정과 이유가 리포트에 있음 ✓.
- **WARN-D**: KOS 가 시술 항목에 `deleted:true` 를 **명시해** 준 경우도 이제 DAY 에 반영되지 않는다(`menu_services` 가 건너뛰기만 · `:98`). 「응답에서 빠짐」은 삭제가 아니지만 「`deleted:true`」는 삭제다 — 명시 삭제만 `deleted_at` 을 채울지 사용자 판단(지금은 KOS 에서 지운 시술 항목이 DAY 에 살아 남는다 · 화면 영향 없음).

## 7. 기존 운영 코드 변경 범위 — PASS

- 기존 파일 diff: `kos/__init__.py`(구역 경로 2곳 · `schedule_sale` 추출 + 예외 · mixin) · `kos/mapper.py`(docstring 1줄) · `services/emr_sync.py`(`Job` 값 · 잠금 TTL · `RunResult.sales` · `captured` · `run_job`) · `tasks/emr.py`(발행 · 새 태스크 · 메뉴 호출) · `normalized.py` · `base.py` · `sync_references.py`(새 유니온 · 읽기 전용 `state`) · `config.py`(설정 2) · `identifiers.py` · 모델. 판 반영(`sync_tasks` · `apply_schedules`) · 쓰기 큐 · 기준 정보 반영 함수의 동작 변경 0. 1단계의 `kos_board.py` 이름 변경 그대로.

## 8. 직접 실행

| 명령 | 결과 |
|---|---|
| `cd backend && uv run pytest -q tests/day -k "sale or menu or prepaid or ticket or purchase or zone or emr"` | **180 passed · 61 skipped**(infra — 아래에서 실제 PG) |
| `./scripts/test.sh -q backend/tests/day/emr backend/tests/migrations backend/tests/day/test_enum_labels.py backend/tests/day/test_constraints.py`(자체 격리 compose · 무작위 포트) | **282 passed** |
| `./scripts/test.sh -q`(전체) | **1825 passed** |
| `uv run ruff check day tests` | All checks passed |

---

## FAIL 고칠 곳

**없음.**

## 정리하면 좋은 것 / 사용자 판단

1. WARN-A — 죽은 코드 · 낡은 주석 5곳 지우기(동작 무관 · 다음 손질 때).
2. WARN-B — 오래된 오늘 구매 메시지를 버릴지(발행 시각 싣기) · `sales_from_payload` 를 `_isolated` 안으로.
3. WARN-C — 첫 prod 기준 정보 회차에서 내부 구역 목록 수가 이전(공개)과 같은지 확인.
4. WARN-D — 시술 항목의 명시 `deleted:true` 만은 `deleted_at` 으로 반영할지.

# 리뷰 리포트: customer-erd / code 6 (백필 스크립트 PR · 브랜치 `kknaksss/customer-erd-backfill`) (2026-11-19)

- 대상: `git diff origin/dev`(11 파일) + 미추적 7(`pacing.py` · `services/emr_backfill.py` · `runtime/backfill.py` · 0011 · 테스트 3)
- base: `origin/dev` `945be39b`(#260 머지 뒤 · fetch 결과 dev 진행 없음) · 커밋 없음
- 발주 `customer-erd-be-4-brief.md` · 워커 `be-4-report.md`(diff 로 재확인). 백필 자체 판정은 이번이 처음이다(검수 5 는 백필 제외).

## 판정: **PASS (FAIL 0 · WARN 4)**

| 볼 것 | 판정 |
|---|---|
| 1. 운영 격리 | **PASS**(WARN-1) |
| 2. 1초 1회 | **PASS**(WARN-4) |
| 3. 세션 | **PASS**(WARN-2) |
| 4. 쓰기 | **PASS** |
| 5. 0011 | **PASS**(WARN-3) |
| 6. 개인정보 | **PASS** |
| 7. 직접 실행 | **PASS** |
| 직원이 실물에서 만날 자리 | **없음**: 판 · 앱 변경 0. 실행 뒤 지난 방문 · 구매 · 시술권 · 카드 이력이 DAY 에 생긴다(화면은 아직 안 씀) |

---

## 1. 운영 격리: PASS (WARN-1)

- 스케줄 · worker 연결 0: 진입점은 `runtime/backfill.py`(`python -m runtime.backfill`)뿐이다. taskiq 태스크 · `schedule=` 이 없다(`tasks/emr.py` diff 0).
- 오늘 창 미접촉: `parse_options`(`services/emr_backfill.py:152-158`)에서 `--to` 기본값은 어제(병원 현지)이고, `end >= today` 면 거부(종료 1)한다. 달 창 끝 = `last_day + 1일 0시`(`:167-182`)라 오늘 0시를 넘지 않는다. 테스트로 확인된다: `test_기본은_어제까지_오늘_이상은_거부한다` · `test_달_창은_병원_현지_달이고_마지막은_어제_끝까지` · infra `test_실행_다시_실행은…오늘은_안_건드린다`(오늘 방문 `updated_at` · `deleted_at` 이 그대로임을 비교).
- 운영 KOS client 불변: `client.py` diff 는 메서드 `revoke_own_sign_ins` 추가와 클래스 `PacedTransport` 추가뿐이다. 기존 메서드와 운영 전송은 그대로다. `factory.build_backfill_adapter` 는 운영 캐시 `adapter_for` 와 따로 있고, 1초 래퍼는 백필 어댑터에만 붙는다. 다른 운영 변경은 `base.py` 기본 메서드 2개(지원 안 함 = `None`/`0`), `kos/__init__` `release_own_sessions`, `sale_reads.fetch_customer_page`, `public.py` 내보내기, `error_codes` 1줄이다. 모두 백필만 부른다.
- 쓰기 부수효과: 운영 `apply_schedules` 를 지난 창에 쓴다. 판 신호 · 「동기화 멈춤」 · 쓰기 큐 확인은 `run_schedules` 쪽에 있어 백필에서는 돌지 않는다. 함수 안의 부수효과는 단계가 바뀐 방문의 `visit_flow_log`(출처 `external`)뿐이다(SPEC-000 OQ-00-3 메모 「flow_log 마지막 단계」와 같다). 알림 · 푸시 · 이벤트 로그는 없다.
- **WARN-1 (달 창 사라짐 = 소프트 딜리트)**: `apply_schedules` 는 그 달 창 안에서 응답에 없던 DAY 방문을 `deleted_at` 처리한다. 일정 API(`get-schedules-grouped-by-zone`)는 페이지가 없다. 데모 달 485건(1.5MB)은 받았지만, 큰 병원의 한 달 응답이 **잘려서 오는지**(서버 상한)는 확인되지 않았다. 잘리면 그 달의 지난 DAY 방문이 잘못 지워진다. 소프트 딜리트라 복구는 된다. 시간 초과라면 실패로 끝나 지움은 없다. 실 병원은 **드라이런의 달별 「받음」 수를 KOS 화면 · 통계의 그 달 예약 수와 한 번 대조한 뒤** 실행할 것을 권고한다.

## 2. 1초 1회: PASS (WARN-4)

- `pacing.KosPacer.wait`: 잠금 안에서 직전 요청 시작 + 1.0초까지 기다린다. `PacedTransport.handle_async_request`(`client.py` 끝)는 **매 시도 전에** `wait` 를 부른다. 429 · 500/502/503/504 · 연결 오류는 `2 · 4 · 8 · 16`초 쉬고 다시 보내며 상한은 4회다. 4xx 는 다시 보내지 않는다.
- 모든 요청이 지나는가: `KosClient` 의 HTTP 클라이언트는 `self._http` 하나다(`client.py:250`). sign-in · 사용자 계정 · 로그인 목록 · 해제 함수도 모두 그 클라이언트를 인자로 받는다(`list_active_sign_ins(self._http, …)` · `revoke_active_sign_in(self._http, …)`). 백필 어댑터는 직원 쓰기 클라이언트(`staff_client` 의 따로 된 `AsyncClient`)를 만들지 않는다(`KosAdapter(client, zone)` · writer 없음). 따라서 토큰 · 재시도 · 세션 해제까지 전부 간격 안에 든다. 공개 API(`exchange-token`)는 새 코드에서 0이다(`"open"` grep 0 · AST 테스트 대상에 백필 2 파일 추가).
- 테스트: `test_요청_사이는_1초_이상이다`(요청에 0.2초 걸려도 시작 간격 1.0) · `test_429_5xx_는_쉬었다_다시_재시도도_1초_간격`(시도 3 · `calls` 3 · 쉰 시간 2 · 4) · 상한 · 4xx · `test_백필_어댑터는_표시_backfill_과_1초_전송을_쓴다`(어댑터의 `_http._transport` 가 같은 pacer 의 `PacedTransport`).
- **WARN-4**: 「sign-in · 해제 요청도 pacer 를 지난다」는 구조(HTTP 클라이언트 하나)로 보장될 뿐, 그 요청들을 세는 끝단 테스트는 없다. infra 테스트는 가짜 어댑터라 HTTP 를 타지 않는다. 지금 구조에서는 문제가 없고, 나중에 HTTP 클라이언트가 늘어날 때 깨질 수 있는 자리다.

## 3. 세션: PASS (WARN-2)

- 표시: `build_backfill_adapter` 는 `kos_client_tag="backfill"` 을 `model_copy` 로 넣는다. 필드 이름이 실제 칸(`KosEndpoints.kos_client_tag`)과 같아 `client_tag` · `user_agent` 에 반영된다(테스트가 `endswith("(backfill)")` 확인). 운영 표시(`dev` · `prod`)와 다르다.
- 기기 제한 자동 해제: 기존 `_revoke_oldest_own`(`client.py:366-374`)은 `user_agent == 자기 UA` 인 것만 고른다. 그래서 `backfill` 표시 세션에만 닿고 운영 · 사람 세션은 건드리지 않는다.
- 끝 해제: `run_backfill` 의 `finally`(`emr_backfill.py`) → `revoke_own_sign_ins(started - 30초)`. 같은 UA **이고** `since` 뒤에 연 것만 해제하고, 표시가 비면 0이다. 테스트 `test_자기_표시_시작_뒤_로그인만_해제한다`(자기 새 것만 · 자기 옛 것 · worker · 사람 것은 둠). 드라이런도 해제한다(infra 테스트).
- **WARN-2**: 판단이 「같은 표시 + 시각」 이라서, **백필 둘을 동시에** 돌리면(같은 시스템 계정을 쓰는 다른 병원 · 같은 병원 두 번) 먼저 끝난 쪽이 다른 실행의 로그인을 해제하거나, 기기 제한 자동 해제가 다른 실행의 세션을 끊을 수 있다. KOS 서버 시계가 30초 넘게 늦으면 자기 세션이 남을 수도 있다(남으면 기기 칸 하나를 차지할 뿐). → 운영 수칙으로 「한 번에 하나」를 적어 두길 권고.

## 4. 쓰기: PASS

- 운영 apply 재사용: `apply_schedules` · `apply_prescriptions` · `purchase_visits` · `apply_purchases` · `apply_tickets` · `apply_task_refs` · `changed_cards` · `apply_cards` · `apply_card_details` · `link_transaction_cards` 만 쓴다. 새 쓰기 길이 없다.
- 소프트 딜리트만: 백필 3 파일 grep `DELETE` · `.delete(` · `session.delete` 0 · AST 테스트 대상에 포함.
- 멱등: infra `test_실행_다시_실행은_새_표_쓴_행_0…`. 두 번째 실행은 단계마다 `written == 0` · 카드 상세 다시 안 받음 · 테이블 건수 같음. DEMO 3회 실측(be-3)도 같다.
- 드라이런: 일정 · 구매 · 시술권 · 카드 모두 `dry_run` 이면 세션 쓰기 없이 돌아간다(읽기 조회만). `save_progress` 도 쓰지 않는다. 테스트로 테이블 전부 0 · 진행 위치 키 없음을 확인한다.
- resume: Redis `day:emr:backfill:{병원}`(30일 만료 · 새 테이블 없음) · 끝난 달 · 고객 순번 · 고객 목록 장을 건너뛴다(테스트 `test_이어_받기는…`). `--resume` 없으면 처음부터다. 단계 사이 메모리 연결(카드 항목 · 카드 결제 거래)은 단계를 나눠 돌리면 비는데, 워커 리포트에 한계로 적혀 있고 다음 오늘 회차 · `--stage all` 재실행이 채운다.
- 고객 목록(`get-visitors`)은 id · 전체 수만 읽는다(`sale_reads.fetch_customer_page`). 고객 행은 만들지 않는다(새 매핑 규칙 없음). DAY 에 없는 고객은 세기만 한다.

## 5. 0011: PASS (WARN-3)

- `migrations/versions/20261119_0011_visit_reserved_index.py`: `down_revision = "0010_sale_tables"`. upgrade 는 `ix_visit_hospital_id_reserved_start_at (hospital_id, reserved_start_at) WHERE deleted_at IS NULL` 하나, downgrade 는 그 drop 하나다. 0010 은 dev 와 byte 동일(diff 0)이다. 모델 `visit.py` 의 `Index` 와 `alembic check` 차이 0이다.
- 테스트: `test_visit_reserved_index_migration.py`(잇기 · upgrade 연산 하나 · downgrade 하나) · `test_alembic.py` HEAD = 0011 · 실제 PG 왕복(base ↔ head) 통과.
- **WARN-3 (운영 잠금)**: 일반 `CREATE INDEX` 는 만드는 동안 `visit` 에 SHARE 잠금을 잡는다. 그동안 판 10초 동기화의 `visit` 쓰기가 막히는데, 대상이 병원 하나가 아니라 **테이블 전체 행 수**만큼이다. `migration_lock_timeout_ms`(기본 5000 · `common/config.py:102` · `migrations/env.py`)는 **잠금을 얻을 때까지 기다리는 시간**만 끊는다. 얻은 뒤 만드는 시간은 끊지 않는다. 지금 규모(방문 수천 ~ 수만)면 1초 안팎이라 문제없다. 5초 안에 잠금을 못 얻으면 migration 이 실패해 배포가 멈추므로 다시 돌리면 된다. CONCURRENTLY 를 쓰지 않은 이유(관례 · INVALID 인덱스 위험 · offline SQL)는 타당하다.
- 워커 이슈 1을 다시 적어 둔다: dev DB 에 임시 패치로 같은 이름의 인덱스를 손으로 만들었다면 0011 이 `already exists` 로 실패한다. 배포 전에 dev 에서 `\d visit` 로 확인할 것.

## 6. 개인정보: PASS

- 출력: 요약은 건수 · 초 · KOS 호출 수 · 해제 수 · DAY 병원 id 뿐이다(`format_summary`). 실패 출력은 `BackfillInputError` 문구(인자 설명) · `EmrError` 이름 + 메시지다. `EmrError` 약속상 메시지에 키 · 토큰 · 본문이 없다. 실제 메시지들(`unexpected response shape: …` · `network …` · `HTTP 401`)을 확인했다. 그 밖의 예외는 이름만 찍는다(`runtime/backfill.py:86-94`).
- 로그: `emr_backfill.py:259 · 304 · 317 · 388 · 415`. 단계 · 달 · 장 · 건수뿐이다.
- 고객 목록 응답에서 이름 · 전화 · 차트번호 · 메모를 읽지 않는다(id · `count` 만).
- 테스트: 가짜 id(`vis-1` 꼴) · 가짜 접속값(`"k"` · `"e"` · `"p"`) · 가짜 호스트(`*.kos.test`)뿐이다. 실 값 · 토큰 패턴 0.

## 7. 직접 실행

| 명령 | 결과 |
|---|---|
| `cd backend && uv run pytest -q tests/day/emr/test_backfill_rules.py tests/day/emr/test_sale_sync_rules.py tests/migrations/test_visit_reserved_index_migration.py` | **43 passed** |
| `./scripts/test.sh -q backend/tests/day/emr/test_backfill.py backend/tests/migrations`(자체 격리 compose · 무작위 포트) | **31 passed**(백필 infra 4 · 0011 왕복 · `alembic check` 0 포함) |
| `./scripts/test.sh -q`(전체) | **1857 passed** |
| grep 백필 3 파일 `DELETE` · `.delete(` · `"open"` | **0** |

---

## FAIL 고칠 곳

**없음.**

## 사용자 판단 · 실행 전 확인

1. WARN-1: 실 병원 실행 전 드라이런 달별 「받음」을 KOS 의 그 달 예약 수와 대조한다(일정 응답 잘림 → 지난 방문 잘못 지움 방지).
2. WARN-2: 백필은 **한 번에 하나**만 돌린다(같은 시스템 계정 세션 해제 겹침).
3. WARN-3: 0011 배포 전 dev 에 같은 이름 인덱스가 있는지 확인한다. prod 는 방문 행 수를 보고 배포 시간대를 고른다.
4. WARN-4: (선택) sign-in · 해제 요청까지 pacer 를 지나는 끝단 테스트 한 개.

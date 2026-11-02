# 리뷰 리포트 r2 — myeongdong-poc-v2 / code · `procedure/` r1 수정 확인 (2026-10-21)

## 판정: WARN — r1 FAIL 3 · WARN 14 모두 처분대로 고쳐짐(PASS 17) · 새 지적 WARN 2 (FAIL 0)

- 기준: r1 리포트 `review-wp1-5-report.md` · 처분 `fix-decisions-r1.md` · SPEC-003 0.2.0(부록 B)
- 돌려 본 것
  - back `uv run ruff check .` → All checks passed · `uv run pytest -q` → **50 passed**(r1 38 → +12, `tests/test_review_r1.py` 등)
  - front `npx tsc --noEmit` → 0 · `npm run lint` → 0
  - `docker compose config` → front 빌드 인자 `NEXT_PUBLIC_API_BASE_URL=http://localhost:8700` · 포트 3700 (빌드 · 기동은 안 함)
  - **실 back 기동**(`uvicorn app.main:create_app --factory --port 8791` · 임시 DB · 사용자 포트 안 씀) → 로그인 → `GET /api/board` 에 `limits:{callMin:5, anesMin:20}` · SSE 7초 동안 `board` 4개(10초 발행을 2초로 줄여 확인) · 접근 로그 `GET /api/board/stream HTTP/1.1 200` — **토큰 문자열 0건**. 끝나고 프로세스를 내렸고 임시 DB · 로그도 지웠다
  - ⚠ 기동 때 env 를 비워 넘겼지만 `env_ignore_empty=True` 때문에 `procedure/.env` 의 KOS 값이 쓰였다. 그래서 데모 KOS **조회**(토큰 · 직원 78 · 방 28 · 일정)가 실제로 나갔다. 조작은 하지 않았고 임시 DB 에서 `kos_op 0` · `event_log 0` 을 확인했다 → **KOS 쓰기 0**. 원장 목록 4명(시스템 계정 · 제외 계정 빠짐)도 실데이터로 확인됐다

## r1 지적 판정

| r1 | 처분 | 판정 | 확인한 곳 |
|---|---|---|---|
| F1 compose 에 front 없음 | compose 가 back + front · build.args | **PASS** | `docker-compose.yml:17-27`(`args: NEXT_PUBLIC_API_BASE_URL: ${…:-http://localhost:8700}`) · `compose config` 결과 · README 「한 줄」 절 |
| F2 front 개별 실행 env | `front/.env.local` 절차 | **PASS** | `README.md` 「따로 — front」(`.env.local` 만들기 · 없으면 404 라는 설명) |
| F3 `?token` 접근 로그 | 쿼리 문자열 지우는 필터 | **PASS** | `back/app/main.py:27-40` `DropQueryString` · 실 uvicorn 로그에 토큰 0건 · `test_review_r1.py:30` |
| W1 failed 뒤 덮어쓰기 | KOS 값을 따른다 · 실패 표시는 뒤 op 이 confirmed 될 때까지 | **PASS** | `back/app/service/board_service.py:102-106`(`seq > last_ok` 인 failed 만) · `repo.py:114`(world 가 confirmed 도 읽음) · `test_review_r1.py` `test_failed_follows_kos_and_keeps_failed_mark` |
| W2 실패 뒤 다음 op | 뒤 op 멈춤 | **PASS**(이름 차이 → N2) | `back/app/kos/ops.py:51-58` · `repo.py:189-196` `block_ops_after` · `test_kos_ops.py:75` |
| W3 시간 경과 값 갱신 | 조회 시간과 상관없이 10초 발행 | **PASS** | `back/app/container.py:54-64` `heartbeat` · `main.py:59` · 실 기동에서 발행 확인 · `test_heartbeat_publishes_without_kos` |
| W4 front 5분 상수 | 스냅샷 `limits` | **PASS** | `front/components/procedures/Aside.tsx:279-280`(`board.limits.callMin`) · front 에 `CALL_LIMIT_MIN` 0건 · `front/lib/types.ts:128-134` |
| W5 마취 빨강 | 카드 마취 `long` | **PASS** | `back/app/domain/rules.py:159-161` · `board_service.py:116` · `front/components/procedures/OrderCard.tsx:146`(`c.anesthesia.long`) · `test_limits_and_anes_long_even_when_need_is_home` |
| — back ↔ front 이름 맞물림 | `limits.callMin` · `limits.anesMin` · `anesthesia.long` | **PASS** | `schemas/board.py:40` · `:64` · `:163` ↔ `front/lib/types.ts:49` · `:128-134` · 가짜 스냅샷에도 있음(`service/fake_board.py:39` · `:145`) · 실 back 응답에서 `limits` 확인 |
| W6 KosError 아닌 예외 | 잡아서 sync 오류 · op 실패로 | **PASS**(구멍 하나 → N1) | `back/app/kos/sync.py:149-160` · `:183-193` · `back/app/kos/ops.py:111-116` · `runtime.py:43-44` · `:71-72`(로그는 클래스만) · `test_non_kos_errors_reach_sync_state_and_op_failure` |
| W7 시스템 id 모를 때 원장 목록 | 갱신 안 함 | **PASS** | `back/app/repository/repo.py:232-242` · `test_doctor_flags_kept_when_system_unknown` · 실데이터 원장 4명 |
| W8 시작 때 직원 · 방 | 조회 시간과 상관없이 1회 | **PASS** | `back/app/kos/runtime.py:45` · `sync.py:149-151`(`force`) |
| W9 방 보호 | 그대로(KOS 가 room 을 안 지움) | **PASS**(처분대로 바꾸지 않음) | WP6 E2E §9 에서 마지막 [종료] 뒤 카드가 남는지는 계속 본다 |
| W10 가짜 KOS 400 | 같은 단계 flow-step · 귀가 대기 call 400 | **PASS** | `back/tests/fake_kos.py:103-116` · `test_same_step_flow_400_then_confirmed_by_kos_value` · `test_call_on_home_schedule_400_fails`. 같은 단계 400 은 거절된 pending 을 다음 조회에서 KOS 값으로 확인하는 경로가 새로 생겼다(`ops.py:64-76`). 재호출 400 은 OQ(E2E) |
| W11 전날 카드 | KST 00:00 에 내림 | **PASS** | `back/app/container.py:46-52` · `repo.py:227-230` · `test_rollover_drops_yesterdays_cards` |
| W12 import 때 앱 생성 | 팩토리 · `--factory` | **PASS** | `main.py` 에 모듈 `app` 없음 · `back/Dockerfile` CMD `app.main:create_app --factory` · README 갱신 · `test_main_import_does_not_build_app` |
| W13 `PROC_FAKE_BOARD` | 개발 전용 · 조작 403 | **PASS** | `back/app/api/actions.py:15`(router 전체 `require_real_board`) · `deps.py:25-29` · `errors.py:22` · `.env.example:22` · README env 표 |
| W14 ① 빌드 인자 기본값 / ② 760px | ① 비우고 비면 실패 ② 그대로 · SPEC 에 적음 | **PASS** | `front/Dockerfile:13-14`(`ARG` 기본값 없음 · `test -n` 실패) |

## 새 지적

| # | 판정 | 파일:줄 | 내용 | 근거 | 고칠 방향 |
|---|---|---|---|---|---|
| N1 | WARN | `back/app/kos/client.py:143-149` · `back/app/kos/sync.py`(`_sync_schedules` → `ScheduleApplier.apply` → `mark_absent_visits`) · `back/tests/test_review_r1.py:187-200` | **2xx 인데 JSON 이 아니거나 `data` 가 없는 일정 응답을 「일정 0건」으로 받아들인다.** 그러면 `mark_absent_visits(빈 집합)` 이 **모든 카드를 내리고** `lastOkAt` 을 갱신하며 `lastError` 는 비운다. 화면은 「동기화 정상 · 시술 대기 중인 고객 없음」이 된다. 확인 대기 중인 op 도 그 조회를 「안 맞음」으로 세어 재전송 · 실패 쪽으로 간다. 시험 이름은 `test_non_json_2xx_is_sync_failure` 인데 실제로는 `lastError is None` 을 단언해 이 동작을 굳혔다. 프록시 · WAF 가 200 으로 HTML 을 돌려주는 경우가 실물에서 이렇게 된다 — r1 W6 의 「조용히 통과」가 이 자리에 남았다 | 처분 W6 「삼키지 않는다」 · SPEC §4.2 「조회 실패는 last_error · 화면은 마지막 값 그대로」 · 브리프 「조용히 통과하는 자리」 | `_call` 에서 JSON 해석 실패를 `KosError("bad response")` 로 올린다. 일정 응답에 `data` 키(목록)가 없을 때도 실패로 친다. 시험은 `lastError` 가 채워지고 카드가 남는 것으로 바꾼다 |
| N2 | WARN | `back/app/kos/ops.py:28` · `:55` · `back/app/repository/repo.py:189-196` ↔ SPEC 0.2.0 §3.2 `kos_op.status` · §4.4 | 멈춘 뒤 op 의 상태값이 SPEC 은 **`blocked`**, 코드는 **`failed` + `last_error="앞 op 실패로 보내지 않음"`** 이다. 화면 동작(「KOS 반영 실패」)은 같지만 DB 계약 값이 다르다. 나중에 복구 · 로그 집계(§10)에서 「진짜 실패」와 「막힘」을 status 로 구분할 수 없다 | SPEC-003 0.2.0 §3.2 · §4.4 · 부록 B S4 | 코드에 `blocked` 상태를 둔다(`world.ops` · board_service 실패 표시 조건에 `blocked` 포함). 또는 SPEC 을 「failed + last_error」로 고친다 — 한쪽으로 맞춘다 |

참고(지적 아님)
- `heartbeat` 이 매초 `rollover()` 쓰기 트랜잭션을 연다(`container.py:58-60`). 바뀐 행이 없으면 빈 UPDATE 이고, SQLite · PoC 규모라 문제는 없다
- `world()` 가 이제 confirmed op 까지 전부 읽는다(`repo.py:114`). 그날 op 수만큼 늘지만 하루 규모라 작다. PG 로 옮길 때(D-15) 「visit 별 마지막 confirmed seq」로 줄이면 된다
- back 설정이 빈 env 를 무시하므로(`config.py` `env_ignore_empty=True`) **env 를 비워서 KOS 를 끌 수 없다** — `procedure/.env` 가 있으면 KOS 가 붙는다. 시험은 `_env_file=None` 이라 영향이 없다. 수동으로 띄울 때 알아 둘 점으로 README 에 한 줄 있으면 좋다

## 남은 것(E2E 몫 · r1 과 같음)
- 이미 WAITING/READY 인 작업 재호출 · [다른 원장에게] 가 실 KOS 에서 400 인지(OQ · W10)
- 마지막 [종료] 뒤 KOS 가 room 을 지우지 않는지(W9)
- 760px 미만은 카드만(SPEC 에 적힘 · W14 ②)

# 리뷰 리포트 — myeongdong-poc-v2 / code · `procedure/` WP1 ~ WP5 (2026-10-21)

## 판정: FAIL — FAIL 3 · WARN 14

- 대상: `cc-prototype/myeongdong-poc-v2` 워크트리의 `procedure/`(미추적 · 커밋 전). 코드 읽기 + 시험만(KOS 쓰기 0 · 사용자 포트 0)
- 돌려 본 것: `cd procedure/back && uv run ruff check .` → All checks passed · `uv run pytest -q` → **38 passed** · `cd procedure/front && npx tsc --noEmit` · `npm run lint` → 오류 0
- FAIL 3건은 모두 **규칙 계산이 아니라 실행 · 보안 쪽**이다. 규칙(D-21 ~ D-33)과 KOS 덮어쓰기 보호(D-09)는 계약대로 들어가 있다(아래 PASS 표)
- 줄 번호는 `procedure/` 기준

## 지적 표

| # | 판정 | 파일:줄 | 내용 | 근거 | 고칠 방향 |
|---|---|---|---|---|---|
| F1 | **FAIL** | `README.md:8` · `README.md:20` · `docker-compose.yml:16-23` | README 는 `docker compose up --build` 로 「back 8700 · front 3700」이 뜬다고 적었지만 compose 의 front 서비스는 주석이다. 적힌 대로 하면 back 만 뜨고 3700 은 열리지 않는다. 주석 안 설정(`environment: NEXT_PUBLIC_API_BASE_URL`)은 런타임 env 라 살려도 번들에 안 들어간다 | SPEC §2.2 「한 줄 실행 = back + front」 · WORK-003 WP6 · 브리프 §3-5 | compose 에 `front: build: { context: ./front, args: { NEXT_PUBLIC_API_BASE_URL: http://localhost:8700 } }` · `ports 3700:3700` · `depends_on: [back]` 추가. 그 전까지 README 의 그 줄을 「back 만」으로 고친다 |
| F2 | **FAIL** | `front/lib/api.ts:5` · `README.md:23-30` | front 를 따로 띄워도 back 에 닿지 않는다. Next 는 `procedure/front/.env*` 만 읽는데, README 는 값을 `procedure/.env`(루트)에만 넣으라고 한다. `front/.env.local` 이 없으면 `API_BASE=''`이 되고 요청이 `localhost:3700/api/...`(rewrites 없음)로 가서 404 가 난다. README 에 front 개별 실행 절도 없다 | SPEC §2.2 개별 실행 `npm run dev`(3700) · §2.3 front env | README 에 「front 만 따로: `cd procedure/front && cp .env.example .env.local`(값 `http://localhost:8700`) → `npm ci && npm run dev`」를 넣는다. 또는 `next.config.ts` 에 `/api/*` → back rewrites |
| F3 | **FAIL** | `back/app/api/board.py:16-18` · `front/lib/api.ts:48` · `back/Dockerfile:21` | SSE 인증 `?token=<ccc 토큰>` 이 uvicorn 접근 로그에 그대로 찍힌다. uvicorn 기본 접근 로그는 쿼리 문자열까지 남긴다. 관리자 토큰은 12시간 유효하고 계정이 하나뿐이다. 연결과 재연결(3초)마다 로그에 쌓이고, 배포(k8s 로그 · ingress 로그)에서도 그대로 남는다 | 브리프 §3-4 「토큰 … 로그에 0」 · SPEC §7.5 인증 · §4.1 「로그에 싣지 않는다」 취지 | 셋 중 하나: ① uvicorn 접근 로그를 `/api/board/stream` 에서 쿼리를 지우는 필터로 바꾼다 ② SSE 전용 단명 토큰(예: 60초 · 1회용)을 `POST /api/board/stream-ticket` 으로 받는다 ③ `--no-access-log`. 배포 WP7 ingress 로그 마스킹은 SPEC 에 적는다 |
| W1 | WARN | `back/app/kos/sync.py:76-77` · `:105-107` · `:124` | `failed` 가 된 op 는 「반영 대기」에서 빠진다. 그래서 다음 조회가 ccc 가 바꾼 KOS 기준 값(`flow_step` · `kos_status` · `doctors`)을 KOS 값으로 덮는다. 예를 들어 [종료]의 `complete` 가 3번 실패하면 시술이 「완료」에서 「진행」으로 돌아간다. [귀가 대기]가 실패하면 카드도 대기 · 진행으로 돌아간다. SPEC §4.4 「failed 뒤 ccc 상태는 되돌리지 않는다」와 D-09 「끝내 실패하면 카드에 KOS 반영 실패」가 이 경우를 어떻게 할지 정하지 않았다 | D-09 · SPEC §4.3 · §4.4 | 정책을 먼저 정한다(→ SPEC 쪽 S3). 「되돌리지 않는다」가 맞으면 `failed` op 도 보호 대상에 넣는다. 「KOS 가 기준으로 돌아온다」가 맞으면 SPEC 문구를 고치고 그대로 둔다 |
| W2 | WARN | `back/app/repository/repo.py:182-187` · `back/app/kos/ops.py:3` · `back/tests/test_kos_ops.py:70` | op 하나가 `failed` 가 되어도 같은 visit 의 다음 op 은 그대로 보낸다(시험이 「실패 뒤 다음 op 은 계속 간다」로 굳혀 둠). 담당자 지정(`assignees`)이 실패해도 `call-tasks-doctors` 는 나간다. SPEC §4.4 「그 뒤 같은 visit 의 op 은 그대로 대기」는 「막힌다」로도, 「평소대로 간다」로도 읽힌다 | SPEC §4.4 · D-24(담당자 → 호출 순서가 필요) | SPEC 에서 한쪽으로 정한다(→ S4). 「막힌다」면 `head_ops` 가 `failed` 를 앞에 두고 멈춘다 |
| W3 | WARN | `back/app/kos/runtime.py:52-59` · `back/app/main.py:33-36` · `back/app/service/board_service.py:70` | 「확인이 필요」(호출 5분 · 마취 20분)와 `sync.inWindow` 는 스냅샷을 **만들 때** 계산한다. 그런데 정기 발행은 조회 시간 안 일정 tick(10초)뿐이다. 조회 시간 밖(21시 이후)이나 KOS env 가 빈 상태에서는 조작이 없으면 `need` · 카드 빨간 테두리 · 「확인」 수 · 「조회 시간 밖」 표시가 바뀌지 않는다. 같은 때 front 호출 탭은 자기 시계로 「5분 · 빨강」을 그려 **두 곳이 어긋난다** | D-20 · SPEC §5.8 · §6.2 · §7.5 「보내는 때」 | 시간으로 바뀌는 값을 위해 hub 가 조회와 상관없이 30 ~ 60초마다 발행한다. 또는 스냅샷에 `since` + `limitMin` 만 주고 front 가 시계로 넘김 여부를 그린다(→ S5) |
| W4 | WARN | `front/components/procedures/view.ts:39` · `front/components/procedures/Aside.tsx:290-291` · `:320` | 호출 미수락 기준 5분을 front 상수로 다시 들고 있다(back `rules.py:22` 와 중복). 규칙 값이 두 곳에 있다. 워커가 이미 밝힌 것 — 재확인 | SPEC §7.2 「규칙 계산은 back 한 곳」 | 스냅샷 `calls[]` 에 `limitMin`(또는 최상위 `limits`)을 싣는다(→ S5) |
| W5 | WARN | `front/components/procedures/OrderCard.tsx:146` | 마취 경과는 `need.why === 'anes'` 일 때만 빨강이다. 시술이 다 끝난 카드(`need = home` 이 먼저)에서 마취를 20분 넘게 켜 두면 보라로 남는다. 스냅샷에 「마취 길어짐」 칸이 없어서 front 가 다른 방법이 없다 | SPEC §5.3 「20분 이상이면 text-red」 · §5.8 우선순위 | 스냅샷 `anesthesia` 에 `long: bool` 을 더한다(→ S5) |
| W6 | WARN | `back/app/kos/client.py:80` · `:98` · `:116` · `back/app/kos/sync.py:118-120` · `back/app/kos/ops.py:100` · `back/app/kos/runtime.py:55-56` · `:71-72` | **KosError 가 아닌 예외를 조용히 삼킨다.** `resp.json()`(2xx 인데 JSON 이 아님) · `int(t["sequence"])` · 모양이 다른 응답에서 나는 `ValueError`/`TypeError` 는 `KosError` 가 아니다. 그래서 ① 조회 실패인데 `sync_state.last_error` 가 비어 화면에 「동기화 실패」가 안 뜬다(마지막 동기화 시각만 멈춤) ② 같은 tick 의 `send_heads` 가 안 돈다 ③ 보내기 중이면 `attempts` 가 안 올라 op 이 `pending` 에 머물고, 「KOS 반영 실패」로도 넘어가지 않는다. `runtime._every` 의 `log.exception` 만 남는다 | SPEC §4.2 「조회 실패는 last_error」 · §4.4 「3회 → failed」 · 브리프 §3-6 | `client._post_raw`/`_call` 에서 JSON 해석 실패를 `KosError("bad response")` 로 바꾼다. `sync_schedules` · `send_heads` 는 `except Exception` 에서도 `set_sync(error)` · `_fail_or_retry` 를 부른다 |
| W7 | WARN | `back/app/kos/sync.py:162` · `:172` · `back/app/repository/repo.py:218-223` | 내부 `sign-in` 이 실패해 시스템 계정 id 를 모르면 `set_doctor_flags(None, …)` 이 돈다. 그러면 시스템 계정(DOCTOR 태그)이 **원장 목록에 들어간다**. 호출 팝오버 · 수락 원장 목록에 시스템 계정이 보인다 | D-11 · SPEC §4.6 | `system_id is None` 이면 원장 목록 갱신을 건너뛰거나, DOCTOR+ADMIN 겹침 같은 가드를 둔다. 또는 `sync_master` 앞에서 `internal_token()` 을 먼저 받는다 |
| W8 | WARN | `back/app/kos/runtime.py:84-86` · `back/app/kos/sync.py:151-152` | 서버를 조회 시간 밖(예: 08:50)에 띄우면 시작 직원 · 방 조회를 건너뛴다. 다음 조회는 시작 + 1시간(09:50)이라 그동안 원장 목록이 비어 있다. 지정 호출 · 수락을 못 하고 시술 줄은 「담당의 미정」으로 보인다 | D-08 · SPEC §2.2 「서버 시작 … 직원 · 방 조회 1회」 | 직원 · 방 루프가 「마지막 성공이 없거나 1시간 지났고, 지금 조회 시간 안」일 때 돌게 한다(일정 tick 에 끼워도 된다) |
| W9 | WARN | `back/app/kos/sync.py:91-102` | 방(`room_id`)은 KOS 값으로 덮기만 하고 보호가 없다. KOS 가 마지막 완료 때 방 배정 작업의 `room` 을 지우면 [귀가 대기] 전에 카드가 사라진다(D-22 「방 있는 일정만」). SPEC §4.3 은 HAR 를 근거로 「KOS 는 지우지 않는다」고 적었다. D-33 은 「KOS 화면은 비워 보인다」라고 해서 둘이 어긋날 여지가 있다 | D-33 · SPEC §4.3 · §5.7 | WP6 E2E §9 에서 「마지막 [종료] 뒤 다음 조회에도 카드가 남는가」를 꼭 본다. 사라지면 `home_requested_at` 없는 visit 은 기존 `room_id` 를 유지한다 |
| W10 | WARN | `back/tests/fake_kos.py:104-123` | **가짜 KOS 가 모든 쓰기를 200 으로 받는다** — 같은 단계 `change-flow-step`(실제 400) · 귀가 대기 일정의 `call-tasks-doctors`(실제 400, 워커 보고) · 이미 WAITING/READY 인 작업 재호출([다른 원장에게] · D-25 재호출)을 거절하지 않는다. 시험이 초록이어도 이 경로들은 실 KOS 에서 3회 실패 → 「KOS 반영 실패」가 될 수 있다 | 브리프 §3-6 · D-25 · D-27 | 가짜 KOS 에 실측된 400 두 가지를 넣고 시험을 하나씩 더한다. 재호출 · [다른 원장에게]는 WP6 실 데모에서 1회 확인 |
| W11 | WARN | `back/app/domain/rules.py:38-39` · `back/app/repository/repo.py:213-216` | 카드 조건에 「오늘 일정」이 없다. `present` 를 끄는 것은 조회뿐이라 21:00 ~ 다음날 09:00 에는 전날 카드(마취 · 호출 기록 포함)가 그대로 보인다. 첫 조회(09:00) 때야 사라진다 | SPEC §5.1-1 · D-08 | `Rules` 의 카드 조건에 「`seen_at` 또는 일정 시각이 오늘(KST)」을 더하거나, 날짜가 바뀌면 `present=0` 으로 만든다 |
| W12 | WARN | `back/app/main.py:75` · `back/tests/conftest.py:5` | `app.main` 을 import 하면 모듈 끝의 `app = create_app()` 이 실제 `procedure/.env` 를 읽고 `back/data/procedure.db` 를 만든다(KOS 루프는 시작 안 함). 시험이 tmp DB 를 쓰더라도 실 env · 실 DB 경로를 건드린다. 셸 env(`PROC_FAKE_BOARD=1` 등)가 있으면 시험 결과도 바뀐다 | 브리프 §3-6 · rules 「비밀값 env 로만」 | `app` 을 `create_app` 지연 생성(uvicorn `--factory`)으로 바꾸거나, conftest 가 import 전에 env 를 비운다 |
| W13 | WARN | `back/app/config.py:38-39` · `back/app/container.py:32-35` | `PROC_FAKE_BOARD` 는 계약 밖 env 다. 켜지면 화면은 가짜 스냅샷인데 조작 API 는 실 DB · 실 KOS 대기열에 쓴다(가짜 visitId 101 등은 404). 배포 env 에 잘못 들어가면 조용히 가짜 화면이 뜬다. 워커가 이미 밝힌 것 — 재확인 | SPEC §2.3(목록에 없음) · §7.4 「데모 · 시드 API 없음」 | SPEC §2.3 에 개발용으로 올리거나(→ S7), 켜져 있으면 조작 API 를 409 로 막고 `/api/health` 에 표시한다 |
| W14 | WARN | `front/Dockerfile:2` · `:13` · `front/app/(main)/procedures/live/page.tsx:224` | ① front 이미지 빌드 인자 기본값이 배포 주소로 박혀 있다. compose 에서 인자를 빼먹으면 로컬 front 가 **배포 back** 을 부른다 ② 760px 미만이면 오른쪽 패널(호출 탭 = 의국 화면)이 아예 없어 수락을 못 한다(워커가 이미 밝힌 것) | rules 「하드코딩된 주소 없음(env 로만)」 · D-27 · SPEC §6.4 | ① 기본값을 지우고 빈 값이면 빌드를 실패시킨다 ② SPEC 에 좁은 화면 범위를 적는다(→ S8) |

### PASS — 규칙 · 연동 · 구조 대조

| 항목 | 판정 | 근거 줄 | 근거 |
|---|---|---|---|
| 유효 호출 = 가장 최근 호출 | PASS | `back/app/domain/rules.py:32-36` · `test_rules.py:58-71` | D-25 |
| 수락 범위 = 유효 호출인 미수락 대기 시술만 · 지정 호출은 지정 원장만 | PASS | `rules.py:134-145` · `service/actions.py:143-164` | D-27 |
| [다른 원장에게] = 같은 받을 시술로 전체 호출 새로 · 기존 호출 남김 | PASS | `actions.py:127-141` | D-27 · D-25 |
| [시작]: 유효 호출 수락 뒤 / 호출 없으면 원장 목록 담당의 · 새 호출이면 꺼짐 | PASS | `rules.py:122-131` · `test_rules.py:64-68` | D-30 |
| [종료] = [시작]한 시술만 | PASS | `actions.py:191-201` | D-31 |
| 첫 [시작] = `changeFlowStep(PROCEDURE)` · 같은 단계로 안 보냄 | PASS | `actions.py:182-187` | D-32 |
| [귀가 대기] = 전부 완료일 때만 · `PROCEDURE_DONE` · 완료로 방을 안 비움 | PASS(W9 확인 필요) | `actions.py:204-216` · `rules.py:88-90` | D-33 |
| 마취 = 고객 상태와 별개 · 동시 1개 · KOS 없음 · 대기 · 진행 어느 때나 | PASS | `actions.py:58-81` · `board_service.py:111-113` | D-23 |
| 카드 = 3 단계 · 방 있음 · 수납 전도 표시 · ETCETERA 숨김 · CANCELED 제외 | PASS | `rules.py:38-39` · `:75-78` · `sync.py:38-44` · `:117-119` | D-21 · D-22 · OQ-506 |
| 진행 · 완료 시술 호출 불가 | PASS | `actions.py:113-114` · `rules.py:119-120` | D-26 |
| 덮어쓰기 보호(대기 중 flow-step · 호출/수락/완료 sequences) | PASS(W1 은 failed 뒤 문제) | `sync.py:105-107` · `:113-133` | D-09 · SPEC §4.3 |
| 토큰: 내부 만료 10분 전 · 401 이면 다시 받기 1회 · 공개는 401 로만 | PASS | `kos/client.py:88-93` · `:122-141` | D-07 · SPEC §4.1 |
| 시스템 계정 id = `get-user-account data.id`(sign-in id 아님) | PASS(SPEC 정정 필요 S1) | `kos/client.py:6-8` · `:104` · `:111-119` | D-11 · D-24 |
| 조회 시간 09~21(시작 포함 · 끝 제외) · 밖에서는 조회 안 함 · 쓰기는 보냄 | PASS | `domain/clock.py:56-60` · `runtime.py:52-56` | D-08 · SPEC §4.4 |
| 4층 · 오늘 KST → UTC 범위 · 직원 공개 / 방 내부 · 1시간 | PASS(W8) | `sync.py:149-197` | D-08 |
| 원장 목록 = DOCTOR · 활성 · 시스템 · 제외 id 빼기 | PASS(W7) | `repo.py:218-223` | D-11 |
| 반영 대기열: visit 마다 seq 순 하나씩 · 2xx = sent · 조회 2번 불일치 → 재전송 · 3회 → failed + `kos_failed` | PASS(W2 · W6) | `repo.py:168-187` · `kos/ops.py:46-109` | SPEC §4.4 |
| 조작 응답은 KOS 를 안 기다림 · event_log 1줄 + op 0 ~ 2 | PASS | `service/actions.py` 전체 | D-13 · SPEC §8 |
| KOS 실패를 성공으로 보지 않음(200 이어도 `expect` 로 확인) | PASS | `kos/ops.py:26-43` · `:57-71` | D-09 |
| 409 코드표 · 404 · 400 `invalid_request` · `{error:{code,message}}` | PASS | `actions.py:15-29` · `main.py:50-62` | SPEC §7.3 |
| SSE: `board` 하나 · 전체 스냅샷 + version · 첫 접속 1개 · `retry: 3000` · 15초 ping · 401 | PASS(F3) | `service/stream.py` · `api/board.py` | SPEC §7.5 |
| front 가 규칙을 다시 계산하지 않음(`pickable` · `canStart` · `canFinish` · `canCall` · `canHome` · `need` · `counts` 를 그대로 씀) | PASS(W4 · W5 예외) | `OrderCard.tsx:44-47` · `:258-299` · `view.ts:29-36` | SPEC §7.2 |
| front SSE: 받으면 통째로 교체 · `version` 이하 버림 · 재연결 때 version 초기화(back 재시작 대비) · 401 → `/login` | PASS | `front/lib/hooks.ts:59-112` | SPEC §7.5 |
| 기능 독립: `procedure/` 밖 import 0(back · front) | PASS | grep 0건 | DEC-001 · D-02 |
| 계층: api → service → repository · sqlite 는 `repository/` 밖에 0 · api 가 repo 를 직접 안 씀 | PASS | grep 0건 | SPEC §2.1 |
| `.env` · `data/` · `.pytest_cache` gitignore · `.env.example` 값 0 · 코드 · 시험 · 가짜 스냅샷에 실 키 · 이메일 · KOS id · 실명 0(가짜 이름 · `*.fake.test` 만) | PASS | `git check-ignore` · grep | WORK-003 주의 · SPEC 머리말 |
| KOS 오류 메시지 = HTTP 상태 + 클래스 이름만 · httpx 로그 WARNING(테넌트 URL 숨김) | PASS | `kos/client.py:39-47` · `main.py:19` | SPEC §4.1 |
| CORS = `PROC_FRONT_ORIGIN` 하나 · credentials 없음 | PASS | `main.py:43-48` | SPEC §2.3 |
| 관리자 로그인: env 가 비면 아무도 못 들어옴 · `compare_digest` · 서명 검증 뒤 만료 · sub 확인 | PASS | `service/auth.py:30-55` | D-05 · SPEC §7.1 |

참고(지적 아님): 조작 API 가 `async def` 안에서 sqlite 를 바로 부른다(`api/actions.py:18-60`). 그래서 이벤트 루프가 잠깐 막히지만, 덕분에 `hub.publish()`(asyncio.Queue) 가 늘 루프 스레드에서 불려 스레드 안전하다. `def` 로 바꾸면 publish 를 `loop.call_soon_threadsafe` 로 감싸야 한다. 또 KOS 토큰은 SQLite 에 평문으로 저장된다(`repository/db.py:69-71`). 볼륨 접근을 막는 것으로 PoC 에서는 충분하다.

## 조용히 통과하는 자리

1. **W6** — KosError 가 아닌 예외: 「동기화 실패」가 안 뜨고, op 이 `pending` 에 영원히 머문다(「KOS 반영 실패」로도 안 감)
2. **W10** — 가짜 KOS 가 실 KOS 가 거절하는 쓰기(같은 단계 flow-step · 귀가 대기 일정 호출 · 재호출)를 200 으로 받는다 → 시험은 초록, 실물은 3회 실패
3. **W1** — `failed` 뒤 조회가 ccc 값을 덮어 「완료」가 「진행」으로 돌아가도 시험이 없다(`test_kos_ops.py:76` 은 ccc 전용 칸 `call` 만 본다)
4. **W3** — 시간으로 바뀌는 「확인이 필요」가 조회 시간 밖 · KOS 없음에서 멈춰도 화면 오류가 없다
5. **W12** — 시험이 실 `.env` 를 읽는 앱을 import 한다(현재 실 DB 파일 `back/data/procedure.db` 는 표만 있고 행 0 — 확인함)
6. `test_contract.py:29-44` 의 스냅샷 모양 시험은 **가짜 스냅샷**(`PROC_FAKE_BOARD`)으로만 본다. 실 스냅샷 모양은 다른 시험이 필드별로 보므로 구멍은 아니지만, 계약 모양 회귀를 실 경로로 묶는 시험은 없다

## 고객이 실물에서 만날 자리

- **F1 · F2** — 사용자가 README 대로 하면 front 가 뜨지 않거나(compose), 떠도 데이터가 없다(개별 실행 → 404). WP6 E2E 첫 단계에서 막힌다
- **W9** — 마지막 [종료] 뒤 카드가 사라질 수 있다(KOS 가 방을 지우면)
- **W10** — [다른 원장에게] · 같은 시술 재호출이 실 KOS 에서 400 이면 카드에 「KOS 반영 실패」가 남고 지울 방법이 없다(§10 복구 미정)
- **W7 · W8** — 아침에 서버를 일찍 켜거나 sign-in 이 흔들리면 원장 목록이 비거나 「시스템」이 원장으로 보인다
- **W14 ②** — 태블릿 세로(760px 미만)에서는 호출 탭이 없어 수락을 못 한다
- 국적이 코드(`KR` · `JP`) 그대로 보인다(워커가 밝힌 것 · 시안은 이름 칩) — SPEC §6.3 이 형식을 정하지 않아 FAIL 아님

## SPEC 쪽을 고쳐야 하는 것

| # | SPEC 자리 | 지금 | 고칠 내용 | 근거 |
|---|---|---|---|---|
| S1 | §4.1 셋째 줄 · §2.3 `KOS_EXCLUDE_ACCOUNT_IDS` | 「내부 `sign-in` 응답 `data.id` = 시스템 계정 id」 | 「`sign-in` 직후 내부 `v1/account/queries/get-user-account` 의 `data.id`(테넌트 계정 id = getAccounts id). `sign-in data.id` 는 사용자 id — 담당자로 넣으면 KOS 가 200 을 주고 무시한다」 | 워커 실호출(2026-10-21) · `kos/client.py:6-8` |
| S2 | §8 `change-flow-step` 줄 · §5.10 | 같은 단계 요청 규칙 없음 | 「지금 단계와 같은 단계로는 보내지 않는다(KOS 400)」. ccc 는 WAITING 인데 KOS 가 이미 PROCEDURE 인 경우(조회 10초 사이)에 무엇을 할지도 적는다 | 워커 실호출 · W10 |
| S3 | §4.4 「failed 뒤 ccc 상태는 되돌리지 않는다」 · §4.3 「반영 대기 중」 정의 | 대기 = `pending`·`sent` 만 | `failed` 뒤 KOS 기준 필드를 ccc 값으로 둘지, KOS 값으로 돌아갈지 하나로 정한다(지금 코드는 KOS 값으로 돌아간다) | W1 · D-09 |
| S4 | §4.4 「그 뒤 같은 visit 의 op 은 그대로 대기」 | 두 가지로 읽힘 | 「뒤 op 은 멈춘다」 또는 「뒤 op 은 평소대로 보낸다」 중 하나로. 담당자 지정 실패 뒤 호출을 보내도 되는지 포함(D-24 순서) | W2 |
| S5 | §7.2 스냅샷 · §7.5 「보내는 때」 | 기준 분이 스냅샷에 없음 · 시간 경과로 바뀌는 값의 발행 시점이 없음 | `calls[].limitMin`(또는 `limits:{callMin, anesMin}`) · `anesthesia.long` 추가. 「조회와 상관없이 N초마다 발행」 또는 「front 가 since + limit 으로 그린다」 중 하나를 적는다 | W3 · W4 · W5 |
| S6 | §2.1 · §2.3 · §2.2 | `back/.env.example` · `front/.env.example` 따로 · compose 가 front 를 띄운다고만 적음 | 지금 구조(루트 `procedure/.env` 하나)를 따를지 정한다. front 는 **빌드 인자**(`NEXT_PUBLIC_*`)와 `front/.env.local`(개별 실행)이 필요하다고 적는다 | F1 · F2 |
| S7 | §2.3 env 표 | `PROC_FAKE_BOARD` 없음 | 개발용으로 올리고 「배포 env 에 넣지 않는다 · 켜지면 조작 막힘」을 적거나, 없앤다 | W13 |
| S8 | §6 화면 | 좁은 화면 규칙 없음 | 「760px 미만 = 카드만(호출 탭 없음) — 의국 화면은 넓은 화면 전제」 같은 범위를 적는다 | W14 ② |
| S9 | §7.5 인증 | `?token=` 만 적음 | 「접근 로그 · ingress 로그에 쿼리 문자열을 남기지 않는다」 또는 SSE 전용 단명 토큰 | F3 |
| S10 | §5.1-1 · §4.2 | 「오늘 일정」이지만 조회 시간 밖에는 판정할 길이 없음 | 「날짜가 바뀌면(KST 00:00) 전날 카드를 내린다」 같은 기준 | W11 |
| S11 | OQ 새로 | — | `call-tasks-doctors` 가 400 을 주는 조건(귀가 대기 일정 · 이미 WAITING/READY 작업 재호출 · [다른 원장에게]) — WP6 실 데모에서 확인 | W10 · 워커 미결 |
| S12 | §4.6 | 시스템 계정 id 를 모를 때 규칙 없음 | 「시스템 계정 id 를 모르면 원장 목록을 갱신하지 않는다(이전 값 유지)」 | W7 |

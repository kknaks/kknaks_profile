# 조사 — 데모 연결 ↔ 운영 연결이 다르게 동작하는 자리 (전수조사)

- 작성: day `researcher` · 2026-11-09 · task_532b7d54cbbf
- read-only. 레포 수정 · 커밋 · KOS 호출 · DB 접속 없음. 결정하지 않는다 — 끝의 「정할 것」.
- 코드 기준: `CENTURION_DAY/day-procedure-board-2` HEAD = `origin/dev` = `91728737`. 아래 `파일:줄` 은 이 ref.
  작업트리에 **미추적 파일 2개**가 있다(origin/dev 에 없음): `scripts/seed_demo_board.py` · `backend/tests/scripts/test_seed_demo_board.py` — 표에는 「(미추적)」으로 따로 적었다.
- 스펙 기준: `mediness-mediness/day-procedure-board-2-spec/products/day/` HEAD `b4cd1a00`(#909).
- HAR 기준: `kknaks_profile/reference/2026-10-12-cc-prototype/*.har` · `reference/2026-10-23-cc-overall-board/har/*.har`. **요청 URL 의 테넌트를 데모 테넌트 id 와 맞춰 봤다 — 모든 HAR 이 데모 테넌트다**(id 는 적지 않음). 본문은 칸 이름 · `step`/`complete`/`reason` 값만 봤다.

## 0. 세는 법

키워드 `is_demo · demo · trial · TRIAL · ON_LIVE · live · APP_ENV · not_supported · WriteNotSupported`(대소문자 무시)를 레포 전체(.git · .venv 제외)에 grep → **69개 파일 · 302줄**(`.py/.sh/.yml/.toml/.env/.md/Dockerfile` 기준). 걸린 자리마다 부르는 쪽을 따라갔다. 키워드 없는 갈림은 `syncable_conditions` · `trial_writes` · `app_env` 를 받는 함수 전부와 설정 기본값 · 배포 config 를 따로 훑었다.

**걸렸지만 갈림이 아닌 것(뺀 것)** — 세었고 표에 넣지 않음:
- `live` 오탐: `runtime/health.py:3,62-63`(`/health/live` = liveness) · compose healthcheck · `day-deploy.sh:10,205` · `models/hospital.py:17,33`(`live_unique` = 안 지운 행 유일) · `templates/partials/kit_page.html:118-119,171-172` · `kit_modal.html:3,5`(견본 요소 id) · `base.html:71`(`aria-live`).
- `not_supported` 오탐: `mfa_not_supported`(`errors.py:51-53` · `routers/login.py:49` · `services/auth.py:9,321`) — 2단계 인증, 데모/운영 무관.
- `APP_ENV` 를 **기록만** 하는 곳: `common/logs.py:3,28-50` · `runtime/worker.py:14-15` · `runtime/main.py:38`(로그 칸 `app_env`). `scripts/test.sh:23`(테스트 전에 env 를 비움). `scripts/deploy/day_vm.py:105`(config 의 `APP_ENV` 가 배포 대상과 같은지 검사 — 배포 실수 방지).
- 모델 · 스키마: `models/hospital.py:57` · `migrations/.../20261105_0002...py:374`(`crm_connection.is_demo` bool not null) — 갈림의 **재료**. 갈림 자체는 아래 표.
- 데모에서 본 응답 모양 주석: `emr/kos/mapper.py:9,52,292,317,325,349,448,463,470,474` — 「응답 모양을 데모 지점 조회로 확인했다」는 근거 주석. 코드 분기는 없다(→ 「정할 것」 F7 에 근거 범위만 적음).

## 1. 갈리는 자리 — 전수 표

### 1-A. 데모 연결 / 운영 연결로 갈림 (`crm_connection.is_demo` → `trial`)

갈림의 뿌리는 한 줄이다: `emr/factory.py:96-98` `trial_writes(is_demo, settings) = is_demo or settings.kos_trial_writes_on_live`. 이 값이 두 곳(계획 · 보내기 직전)으로 흘러간다.

| # | 파일:줄 | 무엇이 갈리나 (데모 / 운영) | 갈리는 이유 | 성격 |
|---|---|---|---|---|
| 1 | `backend/day/emr/factory.py:96-98` | `trial` = 데모면 **항상 True** / 운영이면 `KOS_TRIAL_WRITES_ON_LIVE` 값(기본 False) | 주석 「cc 구현 근거 쓰기를 이 연결에 열까 — 데모 연결이면 늘, 운영 연결은 설정을 켤 때만」 · SPEC-002 §3 「KOS 쓰기 — 동작별」 개정 ⑥ ⑦ · 원천 「결정 — KOS 쓰기」(사용자 2026-11-06) | (가) |
| 2 | `backend/common/config.py:96-99` | 설정 `kos_trial_writes_on_live: bool = False` — 운영 연결에 #1 을 여는 스위치. 데모 연결은 이 값과 무관 | 주석 「데모 지점 실물 확인 뒤에만 켠다(SPEC-002 KOS 쓰기 표 · 원천 「결정 — KOS 쓰기」). 기본 꺼짐 = 데모 연결에만」 | (가) |
| 3 | `deploy/config/prod.env:12-14` | prod 서버 `KOS_TRIAL_WRITES_ON_LIVE=false` | 주석 「첫 배포는 false. 데모 지점 실물 확인 뒤에만 true」 · `docs/development/deployment.md:114` · 40-architecture/deployment.md:32,160 | (가) |
| 4 | `deploy/config/dev.env:13` | dev 서버도 `false` — 다만 dev 는 #13 때문에 운영 연결이 애초에 안 잡혀 **의미 없음** | 40-architecture/deployment.md:160 「(의미 없음 — dev 는 데모 연결만)」 | (가)·(나) 겹침 |
| 5 | `backend/day/emr/factory.py:56-61` (`build_adapter`) | 어댑터 `KosAdapter(trial_writes=…)` 에 #1 값을 박는다 → 보내기 직전 검사(#8)가 연결마다 다름 | 동기화 · 쓰기 큐 worker 가 쓰는 어댑터 | (가) |
| 6 | `backend/day/emr/factory.py:32-37` (`ConnectionConfig.is_demo` · `fingerprint`) | `is_demo` 가 어댑터 캐시 지문에 들어감 — 연결의 데모 여부가 바뀌면 어댑터를 새로 만든다 | #5 를 따라가는 부속 | (가) 부속 |
| 7 | `backend/day/emr/kos/writes.py:85-94,96-174` (`KosWritePlanner`) | `trial=False`(운영)면 아래 5가지가 `WriteNotSupportedError("… opened on demo connections only")` / `trial=True`(데모)면 계획을 만든다: ① 다시 호출 · 재호출 3단계 `call-tasks-doctors`(`:114-125` `recall=True`) ② 시작 취소 `change-flow-step PROCEDURE_WAITING`(`:141-149` · `TRIAL_STEPS :56`) ③ 귀가 대기 2 `change-flow-step PROCEDURE_DONE`(같은 곳) ④ 완료 취소 `change-tasks-complete complete=false`(`:150-159`) ⑤ 귀가 대기 1 `cancel-flow-tasks reason=CANCEL`(`:166-173`) | 모듈 docstring `:17-26` 표 「cc 구현 근거(HAR 없음 · trial) — 데모 연결에만」 · cc D-26 · D-27 · `kos_ops` K2 · K4 · SPEC-002 §3 표 · OQ-08 · OQ-09 · OQ-10 | (가) |
| 8 | `backend/day/emr/kos/writes.py:61-78` (`write_open`) | 보내기 직전 (경로+값) 검사. `trial` 이면 `PROCEDURE_WAITING`/`PROCEDURE_DONE` · `complete=false` · `cancel-flow-tasks(reason=CANCEL)` 통과 / 아니면 False. **다시 호출(①)은 본문이 처음 호출과 같아 여기서 못 가른다** — 계획(#7)만 막는다(`:64-65` 주석) | docstring 「계획이 놓쳐도 여기서 막는다」 | (가) |
| 9 | `backend/day/emr/kos/__init__.py:66-70,182-190` (`KosAdapter.supports_write` · `send`) | #8 을 `self.trial_writes` 로 부른다. False 면 `send` 가 `WriteNotSupportedError` | docstring `:20-24` | (가) |
| 10 | `backend/day/emr/outbox.py:223-233,484-486` (`decide_after_send`) | 쓰기 큐에 이미 들어간 행이 보내는 시점에 #9 로 막히면 **바로 `failed`(`NOT_SUPPORTED`) + `blocks_later=True`**(같은 방문 뒤 op 도 failed). 정상 흐름에선 #7 이 먼저 막아 행이 안 생긴다. 생기는 경우 = 데모 → 운영으로 `is_demo` 가 바뀌거나 `KOS_TRIAL_WRITES_ON_LIVE` 를 true → false 로 되돌린 사이에 남은 pending | docstring 「지원하지 않는 쓰기 → 바로 failed(다시 보내도 안 된다 · 조용히 넘기지 않는다)」 | (가) 부속 |
| 11 | `backend/day/services/board.py:186-203,247-280` (`_connection` · `_queue`) | 조작마다 연결의 `is_demo` 를 읽어 `write_planner(vendor, trial=trial_writes(is_demo, settings))`. 운영이면 #7 의 5가지가 op 을 안 만들고 `event_log.payload.kos` 에 `{"status":"not_supported"}` · `ActionResult.not_supported` 에 남김. **DAY 쪽 값 변경(단계 · started_at · status)은 데모 · 운영 똑같이 한다** | module docstring `:11-15` 「열지 않은 쓰기는 … not_supported 로 남긴다 — 조용히 건너뛰지 않는다(AGENTS.md · W6). DAY 동작은 한다」 | (가) |
| 12 | `backend/day/services/board.py:466-468`(`_call_intents` 재호출분) · `:729-740`(`undo_start`) · `:743-768`(`undo_finish`) · `:771-797`(`home`) | 위 #11 을 타는 화면 동작 4개: [재호출]/다시 호출(이미 WAITING·READY 인 작업분만) · 「시작 취소」 · 「완료 취소」 · [귀가 대기]. 주석 `:730` 「데모 연결에만 · 운영은 계획이 not_supported 로 드러낸다」 · `:788` 「둘 다 cc 근거 쓰기 — 데모 연결에만(OQ-08)」 | SPEC-002 §4 규칙 13 · 14 · 17 · OQ-08 · OQ-09 · OQ-10 | (가) |

> 참고: `ActionResult.not_supported`(`board.py:83`)는 어디서도 응답 · 화면으로 읽지 않는다(`grep '\.not_supported' backend/day` 0건). 운영 연결에서 KOS 쓰기가 빠졌다는 사실은 `event_log.payload.kos` 와 info 로그(`board.py:279`)에만 남는다 — 화면 차이는 없다.

### 1-B. dev 서버 / prod 서버로 갈림 (`APP_ENV`) — 데모 연결 여부를 「거르는」 데 씀

| # | 파일:줄 | 무엇이 갈리나 (dev / prod) | 갈리는 이유 | 성격 |
|---|---|---|---|---|
| 13 | `backend/day/services/crm_connections.py:21-33` (`_syncable` = `syncable_conditions`) | `app_env != "prod"` 면 `CrmConnection.is_demo IS TRUE` 조건 추가 → dev 서버는 데모 연결만 / prod 는 데모+운영 모두 | docstring `:3-5` 「개발 중에 실제 병원 데이터를 건드리지 않게」 · SPEC-000 §3 01 「환경 — 데모 테넌트와 DAY 서버」 · #226 A6 | (나) |
| 14 | `backend/day/services/crm_connections.py:42-62` → `day/tasks/emr.py:41-43`(`_hospitals`) · `services/emr_sync.py:6,111-114`(`_connection`) | 주기 동기화 · 기준 정보 · 쓰기 큐 회차의 대상 병원. dev 에서 운영 연결은 `not_syncable` 로 외부 호출 없이 끝남 | emr_sync docstring `:6` 「여기서도 한 번 더 거른다(#226 A6)」 | (나) |
| 15 | `backend/day/services/board.py:186-203` (`_connection`) | 조작의 KOS 쓰기 대상 연결도 #13 으로 거름 — dev 에서 운영 병원은 KOS 쓰기 0 | docstring `:191` 「dev 서버는 데모 연결만(배포 전 확인 「쓰기 대상 = is_demo 연결만」)」 · module docstring `:16` | (나) |
| 16 | `backend/day/services/auth.py:7,167-180,206,252` · 부르는 쪽 `routers/api/auth.py:58,76` · `routers/login.py:122,144` | 로그인 병원 후보 = 소속 테넌트 ∩ 연결된 병원, dev 면 그중 `is_demo` 만. 다시 고를 때(`:252`)도 같은 조건 | `crm_connections.py:32` 「로그인 병원 후보도 같은 조건(DAY-SPEC-001 규칙 5)」 · SPEC-001 OQ-10 | (나) |
| 17 | `backend/day/routers/kit.py:3,23-28` · `routers/kit_board.py:10,25,31` | `/dev/kit*` 견본 화면: dev 만 열림 / prod 404 | docstring 「prod 는 404(있는지 알리지 않는다)」 · #229 · #231 | (나) — 연결 무관 |
| 18 | `backend/runtime/main.py:40-46` | `/docs` · `/openapi.json`: dev 만 | 코드(주석 없음) | (나) — 연결 무관 |
| 19 | `backend/common/config.py:42,150-158,184-188` | `app_env` 기본 `"dev"` 이지만 앱 프로세스는 env 에 없으면 안 뜸 · prod ↔ `day_prod` 스키마 짝 강제 | docstring `:3-8` · #233 | (나) — 연결 무관 |
| 20 | `deploy/compose.local.yaml:15` · `deploy/local.env.example:5` | 로컬은 `APP_ENV` 기본 dev | 로컬 = dev | (나) |

### 1-C. 그 밖

| # | 파일:줄 | 무엇이 갈리나 | 이유 | 성격 |
|---|---|---|---|---|
| 21 | `backend/day/services/crm_connections.py:80-131` (`ensure_demo_connection`) · `day/public.py:27-45` · `scripts/seed_demo_connection.py` | 코드 안에서 `crm_connection` 행을 만드는 **유일한 길**이 이 시드이고 늘 `is_demo=True` 로 넣는다(`grep 'CrmConnection(' backend scripts` → 이 한 곳). 운영 연결(`is_demo=false`)을 넣는 코드 경로는 없다. 시드는 넣는 테넌트가 실제 데모인지 검사하지 않는다(env 값을 믿음) | docstring 「로컬 시드 — KOS 데모 연결」 · `local.env.example:32` 「데모 지점만. 실제 병원 키를 넣지 않는다」 | (다) — `is_demo` 는 「사람이 붙인 표」. 값이 맞는지 기계 검사 없음 |
| 22 | (미추적) `scripts/seed_demo_board.py:56,110-130,601` | 시험 방문 시드가 테넌트 id 를 하드코딩된 데모 id 와 비교 · 공개 키의 구역이 데모 예약 그룹에 있는지 비교 — 아니면 아무것도 안 보냄. 마지막 단계에서 `change-flow-step PROCEDURE_WAITING` 을 데모에 직접 보냄(`:8,19,105`) | docstring 「테넌트가 데모 지점이 아니면 아무것도 보내지 않고 끝낸다」 | (다) — 시드 도구의 대상 제한. DAY 동작 갈림 아님 |
| 23 | SPEC-002 §3 「권한 — 1차 기본」(`spec-002:338-360`) · 코드 `tests/day/test_default_permissions.py:3,38-41` | 기본 권한 판정 「① 이름 표 → ② 태그」의 이름 표가 **데모 지점 직무 이름** 기준. 다른 병원은 이름이 다르면 태그 규칙만 탄다(log.md 11-08 개정 ⑩). `is_demo` 분기는 아님 — 이름이 같으냐로 갈림 | 사용자 2026-11-08 | (다) — 플래그 분기 아님, 데이터에 따른 사실상 갈림 |

**자리 수: 23** — (가) 12(#1~#12 · #4 는 (나)와 겹침) · (나) 8(#13~#20) · (다) 3(#21~#23).

## 2. (가) 만 모은 표 — 동작 · KOS 경로 · 확인 상태

모든 HAR 은 **데모 테넌트**에서 받은 것이다(§0). 즉 「HAR 확인」= 데모 실물에서 KOS 웹이 그 요청을 보냈다는 뜻이고, 운영 테넌트 HAR 은 하나도 없다. 지금 운영에 열려 있는 6가지도 근거는 데모 HAR 이다(`writes.py:6-15`).

| 동작 | KOS 경로 · 값 | HAR | 데모 실물(DAY 에서 보냄) | 코드 · 스펙의 표기 |
|---|---|---|---|---|
| 다시 호출 · 재호출 3단계 (이미 WAITING·READY 작업에 다시) | `schedule/flow/v1/commands/call-tasks-doctors` `{scheduleId, sequences}` | 경로 · 본문 모양 확인(`의사호출.har` · `의사호출_2.har`, 200). **이미 호출된 작업에 다시 보낸 요청인지는 HAR 로 가를 수 없음 — 확인 안 됨** | 확인 안 됨. `writes.py:117-119` 「수락된(READY) 작업을 다시 부를 때 KOS 가 READY 를 유지하는지 데모 실물로 아직 못 봤다」 | SPEC-002 KOS 쓰기 표 호출 3행 「데모 지점 실물 확인 뒤 운영 병원에 연다(cc OQ-516 미확인)」 |
| 「시작 취소」 → 고객 시술 대기 | `schedule/v1/commands/change-flow-step` `{id, step: PROCEDURE_WAITING}` | **확인됨 — `reference/2026-10-23-cc-overall-board/har/방배정.har` 에 같은 내부 경로 · 같은 칸(`id` · `step`) · 값 `PROCEDURE_WAITING` 요청 1건, 200.** 코드(`writes.py:17` 「HAR 없음」) · SPEC-002(「내부 경로 + 이 값은 … 미확인」)의 표기와 다르다 | **확인됨** — 사용자 2026-11-09 데모에서 정상 동작 확인(브리프). 미추적 `seed_demo_board.py` 도 같은 경로로 데모에 보낸다 | ⚠ 같은 날 사용자 결정 「시작 취소는 KOS 에 쓰지 않는다」(profile #123 · `reference/2026-11-03-cc-day/screen/procedure-board-decisions.md` 「결정 — 시작 취소의 KOS 쓰기」 · 코드 · SPEC 반영은 「다음 작업」) — 코드는 아직 보냄(데모) |
| 「완료 취소」 | `schedule/flow/v1/commands/change-tasks-complete` `{scheduleId, sequences, complete: false}` | 경로 · 칸만 확인(`시술완료*.har` — 값은 전부 `true`). **`false` 요청은 HAR 에 없음 — 확인 안 됨** | 확인 안 됨 | SPEC-002 「데모 지점 실물 확인 전엔 운영 병원에 열지 않는다」 · cc K2 |
| [귀가 대기] 1 — 안 끝난 「방 배정」 작업 취소 | `schedule/v1/commands/cancel-flow-tasks` `{scheduleId, sequences, reason: CANCEL}` | **요청 없음.** 경로 문자열은 `예약그룹.har` 의 KOS 웹 JS 묶음 응답 안에만 있음(요청 아님). 본문 모양 확인 안 됨 | 확인 안 됨 | SPEC-002 「HAR 없음 · cc 구현 근거」 · cc `cancel_tasks_op` |
| [귀가 대기] 2 — 고객 시술 완료 단계 | `schedule/v1/commands/change-flow-step` `{id, step: PROCEDURE_DONE}` | 경로 · 칸 확인 · **값 `PROCEDURE_DONE` 요청은 HAR 에 없음 — 확인 안 됨.** 참고: KOS 웹 「귀가」(`귀가.har`)는 같은 경로로 `step: COMPLETED` 를 보냈다(이건 DAY [귀가 대기]와 다른 동작일 수 있음 — 판단 안 함) | 확인 안 됨 | SPEC-002 「내부 경로 + 이 값은 데모 지점 실물 확인 전 미확인」 |

## 3. 데모/운영 갈림을 단언하는 테스트 (없애면 같이 바뀔 것)

| 파일:줄 | 무엇을 단언 | 갈림 종류 |
|---|---|---|
| `backend/tests/day/emr/test_kos_board_contract.py:84` | `PLANNER = KosWritePlanner()` — 기본 `trial=False`(운영) 플래너를 기준으로 OPEN/CLOSED 를 가름 | (가) |
| `test_kos_board_contract.py:93-100,121-124` (`CLOSED` · `test_닫힌_쓰기는_op_을_만들지_않고_드러낸다`) | 재호출 · 시작 취소 · 귀가 대기 · 완료 취소 · 취소 5개가 `WriteNotSupportedError`(마지막 줄 「시스템 계정 없음」은 trial 무관) | (가) |
| `test_kos_board_contract.py:181-205` (`test_cc_근거_쓰기는_trial_에서만_열린다`) | `live` 는 5개 다 거절 · `demo`(`trial=True`)는 계획 · 본문 · 확인 조건까지 | (가) |
| `test_kos_board_contract.py:208-221` (`test_보내기_직전에도_trial_로_가른다`) | `write_open` 이 trial 없이 4개 False · trial 이면 True | (가) |
| `backend/tests/day/emr/test_kos_client.py:6,262-284` (`test_열지_않은_쓰기는_요청이_나가지_않는다`) | `KosAdapter(...)` 기본(trial False)에서 `PROCEDURE_WAITING` · `complete=false` · `cancel-flow-tasks` 가 `supports_write False` · `send` 거절 · 요청 0 | (가) |
| `backend/tests/day/board/test_board_api.py:338-368` (`test_cc_근거_쓰기는_데모_연결에_열린다`) | 데모 연결(conftest `is_demo=True`)에서 시작 취소 · 완료 취소 · 귀가 대기 op 이 쌓임 | (가) |
| `test_board_api.py:370-` (`test_재호출은_KOS_호출을_다시_보내고_앞_호출은_닫힘`) | 데모 연결에서 재호출 시 `call-tasks-doctors` 가 다시 나감 | (가) — 데모 전제 |
| `test_board_api.py:752-773` (`test_운영_연결은_다시_호출분만_닫히고_처음_호출분은_나간다`) | `trial_writes` 를 False 로 바꿔 재호출분 · 시작 취소가 `not_supported` · op 0 | (가) |
| `backend/tests/day/board/conftest.py:119` · `tests/day/auth/conftest.py:218,231` | 픽스처 연결 기본 `is_demo=True` — 대부분의 판 · 로그인 테스트가 「데모 연결 + trial 열림」 전제로 돈다 | (가)·(나) 전제 |
| `backend/tests/deploy/test_day_vm.py:76-77` | prod config `KOS_TRIAL_WRITES_ON_LIVE == "false"` | (가) |
| `backend/tests/day/emr/test_emr_sync_service.py:86-117` (`test_dev_는_데모_연결만_동기화한다`) | dev = `{demo}` · prod = `{demo, real}` | (나) |
| `test_emr_sync_service.py:120-130` (`test_dev_에서_실제_병원_연결은_한_회차도_돌지_않는다`) | dev 에서 운영 연결 세 회차 `not_syncable` · 외부 호출 0 | (나) |
| `backend/tests/day/auth/test_auth_api.py:303-318` (`test_dev_서버_후보는_데모_연결만`) | dev 로그인 후보 = 데모만 · 운영만이면 `no_connected_hospital` | (나) |
| `backend/tests/day/web/test_kit.py:42,73,116` | dev 에서 열림 · prod 404 | (나) 연결 무관 |
| `backend/tests/common/test_config.py:12-45` · `tests/runtime/test_startup_key.py:39-64` | `APP_ENV` 읽기 · 값 제한 · 스키마 짝 · 없으면 안 뜸 | (나) 연결 무관 |
| (미추적) `backend/tests/scripts/test_seed_demo_board.py:96,261,280` | 시드의 데모 테넌트 · 데모 공개 키 가드 | (다) |

`is_demo=True` 를 값으로만 넣는 테스트(단언 아님): `tests/day/test_constraints.py:153,385` · `test_encryption.py:56` · `test_encryption_canary.py:27` · `test_column_snapshot.py:141`(칸 목록).

## 4. 스펙에서 데모/운영을 나눠 적은 절

| 문서 · 절 | 무엇 |
|---|---|
| `20-spec/spec-000-data-model.md` `crm_connection` 표 `:175` · 「환경 — 데모 테넌트와 DAY 서버」 `:204-217` | `is_demo` 칸 · 「데모도 KOS 운영 호스트, 테넌트만 데모」 · `APP_ENV=dev` 는 `is_demo` 연결만 동기화 — (나) |
| `20-spec/spec-001-login-session.md` U-2 `:75` · S-1 `:153` · 케이스 매트릭스 `:240` · Flow `:267` · 규칙 5 `:304` · OQ-10 `:337` | dev 서버 로그인 후보 = 데모만 — (나) |
| `20-spec/spec-002-procedure-board.md` 머리 개정 ⑥ `:36` · ⑦ `:38` | cc 근거 쓰기를 연다 · 다시 호출 「데모 실물 확인 뒤 운영」 — (가) |
| 〃 §3 「KOS 쓰기 — 동작별」 `:515-533` (호출 3행 · 시작 취소 · 완료 취소 · 귀가 대기 1·2) | 행마다 「데모 지점 실물 확인 전엔 운영 병원에 열지 않는다」 — (가) |
| 〃 §4 규칙 13 · 14 · 17 `:576-580` | 「cc 구현 근거로 연다」(데모/운영 문구 없음 — 표를 가리킴) — (가) |
| 〃 §5 닫은 것 OQ-08 · OQ-10 `:627` · OQ-09 `:628` | 「데모 지점 실물 확인」 · 「데모 지점 실물 확인 뒤 운영」 — (가) |
| 〃 §3 「권한 — 1차 기본」 `:338-360` | 직무 이름 표 = 데모 지점 이름 — (다) |
| `40-architecture/system.md` 「환경」 `:180-183` | dev = 데모만 · 연결에 KOS 환경 칸 없음 — (나) |
| `40-architecture/deployment.md` 결정 요약 `:32` · 그림 `:48-51,76` · 환경별 env `:153,160` · 미결 KOS IP `:195` | `APP_ENV` · `KOS_TRIAL_WRITES_ON_LIVE` 첫 배포 false · 운영 KOS IP 는 prod 때 확인 — (가)(나) |
| `40-architecture/mobile-deployment.md` `:34,55-60,154,227-229,259` · 미결 M-18 `:287` | dev 앱 = 데모 연결 · prod 서버가 데모 연결을 뺄지 미결 — (나) |
| `log.md` `:17,18,27,30,31` | 위 개정 이력 |
| `10-decision.md` | 해당 없음(키워드 0건) |

## 5. 정할 것 (결정하지 않음)

- **F1 — (가) 를 없애는 범위.** 갈림 뿌리는 `factory.trial_writes`(#1) 한 줄 + `KOS_TRIAL_WRITES_ON_LIVE`(#2·#3·#4) + 플래너 · `write_open` 의 `trial` 인자(#7·#8·#9). 없앤다면 5가지 쓰기를 (ㄱ) 모든 연결에 열기 (ㄴ) 모든 연결에서 닫기 (ㄷ) 동작별로 따로 — 중 무엇인가. §2 표의 확인 상태가 동작마다 다르다.
- **F2 — 「시작 취소」 KOS 쓰기.** 같은 2026-11-09 에 두 사실이 있다: 브리프 「데모에서 정상 동작 확인」 vs profile #123 「시작 취소는 KOS 에 쓰지 않는다(코드 · SPEC 반영은 다음 작업)」. 지금 코드는 데모 연결에서 보낸다. 어느 쪽으로 정리하나.
- **F3 — HAR 표기 바로잡기.** `방배정.har`(데모 · 200)에 `change-flow-step {id, step: PROCEDURE_WAITING}` 내부 요청이 있다. `writes.py:17` 「HAR 없음」 · SPEC-002 시작 취소 행 「내부 경로 + 이 값은 미확인」과 다르다(F2 결정에 따라 행 자체가 빠질 수도 있음).
- **F4 — 확인 안 된 4가지(재호출 다시 보내기 · `complete=false` · `cancel-flow-tasks` · `PROCEDURE_DONE`)를 무엇으로 확인하나** — 데모 실물(DAY 에서 눌러 보기) 또는 새 HAR. 그리고 KOS 웹 「귀가」가 `COMPLETED` 를 보낸 것(`귀가.har`)과 DAY [귀가 대기]의 `PROCEDURE_DONE` 관계.
- **F5 — (나) 는 남기나.** dev 서버 = 데모 연결만(#13~#16)은 「dev 가 실제 병원을 안 건드리게」 장치로 연결 차이가 아니다. 유지 여부와, mobile-deployment M-18(prod 서버가 데모 연결을 뺄지)은 열려 있다.
- **F6 — (가) 를 없앤 뒤 `is_demo` 의 쓰임.** 남는 쓰임은 (나) 거르기뿐이 된다. 그리고 `is_demo` 는 시드가 손으로 붙이는 표(#21)라 운영 연결을 넣는 코드 경로가 없다 — 운영 연결 등록 방식은 정해지지 않았다.
- **F7 — 「같은 API」의 근거 범위.** 응답 모양(mapper 주석) · HAR 6+1 가지 모두 데모 테넌트에서만 봤다. 운영 테넌트 응답 · 쓰기는 한 번도 본 적 없다(deployment.md 미결 「운영 KOS 쪽은 prod 때 확인」 포함). 「테넌트만 다르다」를 운영에서 어떻게 확인할지.
- **F8 — 남은 pending 처리(#10).** trial 을 바꾸는 순간 큐에 남은 trial op 은 `failed` + 뒤 op 막힘이 된다. 전환할 때 고려할지.
- **F9 — 테스트 정리.** §3 의 (가) 테스트 8곳 + 픽스처 기본값 `is_demo=True` 가 F1 결정에 따라 같이 바뀐다.

# [backend] Delivery #226 — KOS 연동(폴링 · external_ref · outbox 기반)

너는 day backend 워커다. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/roles/day/backend/` — 특히 `tools.md` 「KOS 확인 (조회만)」 · 프로젝트 설정 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/config/projects/day.json` 의 `repos.reference_kos.notes` · `data_rules`.
워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-data-architecture` — #224 · #225 커밋 위에 이어서(PR #228 하나 · 사용자 결정). 다른 워커 없음.

## 1. SSOT

- **계약 = Issue #226** `gh issue view 226 -R MediSolveAIDev/CENTURION_DAY` — 바뀌는 것 · 하지 않는 것 · 완료 조건 A1 ~ A7.
- 시스템 결정 `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/system/README.md` (프로세스 나눔 · 10초/3600초 interval · 병원별 Redis 잠금 · 버튼 하나의 흐름 · KOS 헤더 위험) · `/Users/kknaks/orca/workspaces/mediness-mediness/day-data-architecture-spec/products/day/40-architecture/system.md` · `code-structure.md`.
- 테이블 정본 DAY-SPEC-000 `/Users/kknaks/orca/workspaces/mediness-mediness/day-data-architecture-spec/products/day/20-spec/spec-000-data-model.md` — 01 `crm_connection` · `config` · 02 `external_ref` · 코드 테이블 · 05 `external_outbox` · 각 표의 「cc」 「KOS」 칸(어느 응답 필드에서 오는지).
- 레포 `AGENTS.md` 「외부 CRM 연동 (emr)」 — 업무 코드는 업체를 모른다 · 매핑은 mapper 에서 · 없는 값을 추정해 채우지 않는다.
- **본 = cc-prototype**(같은 KOS 를 이미 붙인 구현 · 읽기만): `git -C /Users/kknaks/git/toy_pr2/cc-prototype show origin/main:<경로>` — `procedure/back/app/kos/{client,sync,reservation_sync,ops,runtime}.py` · `app/domain/kos_ops.py` · `app/service/kos_errors.py`. 특히 **#20(`77173cf`) 의 내부 API 웹 헤더** · 어떤 토큰(공개 API exchange-token / 시스템 계정 sign-in)으로 무엇을 부르는지. **cc 의 방식을 그대로 따르고, 리포트에 「호출마다 어떤 API · 어떤 토큰」 표를 붙여라.**

## 2. 코디 결정 (Issue 「아직 결정이 필요한 것」 — 기본값)

1. **outbox 실제 발송 = 기반만.** 적재 · 발송 · 확인 · 재전송 상태 전이를 가짜 KOS client 로 단위 테스트(A7). **실제 KOS 로 쓰기(commands)는 한 번도 보내지 않는다** — 데모 지점이어도 금지(KOS 는 조회 · 토큰 받기만). 첫 실제 쓰기는 시술 현황 Delivery.
2. **공식 API 이전 = 이번엔 안 함.** cc 가 내부 API 로 하는 것은 내부 API 로. 리포트에 「공개 API 로 옮길 수 있는 호출」 후보 목록만.
3. **OQ-02-2**(`updatedDateTimeUtc` 로 바뀐 고객만) — 결정하지 않는다. 데모 지점 조회로 그 필드가 응답에 있는지만 확인해 리포트(값 · 개인정보 없이 필드 이름 · 타입만).

## 3. 만들 것

- `backend/day/emr/` — `base.py` · `normalized.py` · `factory.py` · `sync.py` · `outbox.py` · `kos/client.py` · `kos/mapper.py` (AGENTS.md 트리 그대로). `vegas/` 는 만들지 않는다.
- `backend/day/tasks/` — 10초(오늘 일정 + 그 고객) · 3600초(방 · 구역 · 예약 그룹 · 직원 · 코드) · outbox 발송. `day/tasks/__init__.py` 에서 import(#224 W3 · CLI 모듈 인자 등록).
- 병원별 Redis 잠금 — 앞 회차가 안 끝났으면 건너뜀(A2). **#224 W5**: 공용 Redis 클라이언트 timeout 을 헬스 timeout 과 분리(`REDIS_SOCKET_TIMEOUT_SECONDS` 등).
- 동기화 쓰기 — upsert 는 **부분 유일 인덱스라 `ON CONFLICT … WHERE deleted_at IS NULL` 을 반복**(#225). 외부 id 는 `external_ref` 에만. 사라진 행은 `deleted_at` · `is_present_in_source=false`(A3). 필수 bool 은 동기화가 전부 채운다(SPEC 에 기본값 없음 — 응답에 없으면 추정하지 말고 리포트).
- `APP_ENV=dev` → `is_demo` 연결만(A6).
- **#224 W9**: compose worker · scheduler 가 `migrate` 완료를 기다린다(`service_completed_successfully` — compose 그 부분만 허용).
- 데모 연결 넣기 — `scripts/` 에 로컬 시드 스크립트(병원 · 브랜드 · `crm_connection(is_demo=true)`), 접속값은 **env 에서만 읽는다**(`deploy/local.env` — gitignore). `local.env.example` 에 자리표시자 이름만. 값은 `reference_kos.notes` 가 가리키는 곳에서 — **데모 지점 키만 · 명동점 키 금지.** 키 · 토큰 · 테넌트 id · 실명을 코드 · 테스트 · fixture · 리포트에 쓰지 마라.
- KOS mapper contract test(A4) — **응답 고정본은 모양만, 값은 가짜로 만든다**(실명 · 전화 · 테넌트 id 금지). 고정본 위치 `backend/tests/day/emr/fixtures/`.

## 4. allowed_paths

`backend/day/emr/` · `backend/day/tasks/` · `backend/day/services/`(동기화가 쓰는 것만 필요하면) · `backend/day/public.py` · `backend/common/`(redis timeout · 설정) · `backend/runtime/`(진입점 docstring 정도) · `backend/tests/` · `scripts/` · `deploy/compose.local.yaml`(W9 의존 · 새 env 이름) · `deploy/local.env.example` · `pyproject.toml` · `uv.lock` · `AGENTS.md`(실행 명령 · 시드 한 줄만). 모델 · migration 은 바꾸지 마라 — 필요하면 `[질문]`.

## 5. 하지 말 것

Issue 「이번에 하지 않는 것」 전부. KOS commands 금지 · 명동점 키 금지 · 응답 원문/개인정보를 파일 · 리포트에 남기지 마라. 커밋 금지. 포트 11040 · 11042 · 11043 만, 끝나면 `down`.

## 6. 검증 · 보고

- `scripts/test.sh -q` · ruff 각 1회.
- **실물 1회(필수)**: 로컬 compose 에 데모 연결을 시드하고 worker · scheduler 를 띄워 **실제 KOS 데모 지점에서 10초 폴링 · 1시간 기준 정보가 한 번씩 돌아** DAY 테이블 · `external_ref` 에 들어오는 것(A1) — 테이블별 건수 · `external_ref` entity_type 별 건수만 보고. 두 번째 회차에서 같은 행이 중복되지 않는 것(건수 그대로).
- 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/backend-226-report.md` — 완료 조건 A1 ~ A7 증거 · 「호출마다 API · 토큰」 표 · 공개 API 후보 · OQ-02-2 확인 · 응답에 없어 비워 둔 칸 목록 · 남은 것. 완료는 preamble 의 worker_done 절차대로(`orca orchestration send` 와 `orca terminal send` **둘 다**).

# Backend Architecture

규칙: `para/projects/project.md`

> FastAPI 백엔드의 계층·경계·규약. **여기 적힌 것은 「이렇게 한다」다** — 코드 워커가 이 문서만 읽고도 같은 방식으로 쓸 수 있어야 하고,
> 리뷰어는 이 문서를 판정 기준으로 삼는다. 선택지를 남기지 않는다.
>
> 근거 표기: `DEC-00x §y` = `10-decision/`, `§C` = `orchestration/work/docs-v1/design-requests.md`, 「제약」 = 사용자가 못박은 스택·계층.

관련 문서 — `../system/README.md`(구성·흐름) · `../database/README.md`(스키마 정본).

## 1. 스택

| 항목 | 선택 | 근거 |
|---|---|---|
| 웹 프레임워크 | **FastAPI** | 제약 |
| 패키지 관리 | **uv** (`pyproject.toml` + `uv.lock`) | 제약 |
| Python | 3.12+ | `StrEnum` · 기존 레포 기준 |
| ORM | **SQLAlchemy 2.0 async** (`Mapped[...]` 선언형) | 비동기 제약 |
| DB 드라이버 | **`postgresql+psycopg://`** (psycopg3, async) | 비동기 제약. asyncpg 가 아니라 psycopg3 인 이유는 §5 |
| 마이그레이션 | **Alembic** | `../database/README.md` §0-2 |
| 검증·직렬화 | **Pydantic v2** | FastAPI 기본. `schemas/` 전용 |
| 서버 | **uvicorn** | — |
| AI 실행 | **open-kknaks `AgentClient`** (Redis 브로커) + codex 워커 | 제약 |
| STT | **Soniox WebSocket 중계** (백엔드가 키 보유) | DEC-003 §STT |
| 테스트 | pytest + pytest-asyncio(`asyncio_mode=auto`) + httpx `AsyncClient` | §12 |

**금지 — Anthropic·OpenAI 등 LLM SDK 를 직접 import 하지 않는다.** LLM 은 open-kknaks 를 통해서만 쓴다(제약).

## 2. 계층 — router → service → repository

한 방향으로만 내려간다. 위로 부르지 않고, 건너뛰지 않는다.

| 층 | 하는 일 | **하지 않는 일 (위반 시 반려)** |
|---|---|---|
| **router** (`api/`) | HTTP 만. 경로·상태코드·의존성(세션·인증)·`schema ↔ dto` 변환·서비스 호출 | 도메인 규칙 판단 · ORM/SQL · `AsyncSession` 으로 직접 쿼리 · `try/except` 로 도메인 예외 잡기 |
| **service** (`service/`) | 도메인 규칙·불변식·여러 repository 조합·외부 어댑터 호출 | **`fastapi` import 금지**(Request·Response·HTTPException·Depends) · `schemas/` import 금지 · ORM 모델 다루기 · `commit()` |
| **repository** (`repository/`) | ORM/SQL 만. 모델 → dto 변환 | 도메인 규칙 · 다른 repository 호출 · `commit()` (flush 까지) · dto 아닌 ORM 모델 반환 |
| **integrations** (`integrations/`) | 외부 시스템 어댑터 — Soniox WS · open-kknaks · 파일 저장소 | 도메인 규칙 · DB 접근 |
| **core** (`core/`) | 엔진·세션·예외·보안·설정 | 도메인 지식 |

**ORM 모델은 repository 를 넘지 않는다.** service 가 보는 것은 dto 뿐이다. 이것이 계층 규약의 실질적 강제 지점이다 — 모델이 새어 나가면 lazy-load 가 어디서든 터지고 층 구분이 이름만 남는다.

**service 는 다른 service 를 부를 수 있다.** 단 순환을 만들지 않는다 — `task_service ↔ meeting_service` 처럼 양방향이 필요하면 공통 규칙을 아래쪽 service 로 내린다(예: 겹침 검사는 `schedule_service` 하나가 갖고 업무·회의가 부른다).

## 3. `schema` 와 `dto` — 섞지 않는다

| | `schemas/` | `dto/` |
|---|---|---|
| 무엇 | **프론트 ↔ 백 계약** | **백 내부 계층 이동** |
| 타입 | Pydantic `BaseModel` | `@dataclass(frozen=True)` |
| 필드 명명 | **camelCase**(alias). 프론트가 TS 라 그대로 쓴다 | **snake_case** |
| 쓰는 층 | router 만 | router · service · repository |
| 나가는 곳 | HTTP 본문 | 함수 인자·반환값 |

규칙 여섯.

1. **service 는 `schemas/` 를 import 하지 않는다.** router 가 `schema → dto` 로 바꿔 넘긴다.
2. **repository 는 dto 만 돌려준다.** ORM 모델을 밖으로 내지 않는다.
3. **입력도 dto 다.** `body.to_dto()` 로 명시 dto 를 만들어 넘긴다 — `dict` 를 계층 계약으로 쓰지 않는다. dict 는 리뷰어가 판정할 계약이 아니고, 필드 오타가 런타임까지 간다.
4. **부분 수정(PATCH)** 은 `XxxUpdateDTO` 의 필드를 `T | Unset` 로 두고 `model_dump(exclude_unset=True)` 결과만 채운다 — 「보내지 않음」과 「null 로 지움」을 구분해야 한다(인라인 자동 저장이 필드 단위로 오기 때문).
5. **응답에 dto 를 그대로 쓰지 않는다.** `XxxItem.from_dto(dto)` 로 감싼다.
6. Pydantic 설정은 전 모델 공통 — `alias_generator=to_camel`, `populate_by_name=True`, 라우터는 `response_model_by_alias=True`.

명명 — 요청 `XxxCreate` · `XxxUpdate` / 응답 단건 `XxxItem` · 목록 `XxxListResponse` / 내부 `XxxDTO` · `XxxCreateDTO` · `XxxUpdateDTO`.

**ID 는 JSON 에서 number 로 낸다** (PK 가 bigint — `../database/README.md` G-1). 02-data-model 이 `id: string` 으로 그린 것은 디자인 표기이고 계약은 number 다.

## 4. 디렉토리 구조

```text
app/back/
├── pyproject.toml · uv.lock          # uv
├── alembic.ini · alembic/versions/
├── main.py                           # 앱 팩토리 — 조립만. 로직 없음
├── config.py                         # env → Settings (pydantic-settings)
├── core/
│   ├── db.py                         # async engine · SessionLocal · get_db
│   ├── exceptions.py                 # 도메인 예외 + HTTP 매핑 핸들러
│   └── security.py                   # 비밀번호 해시 · JWT 발급/검증
├── api/                              # 1층 — router
│   ├── deps.py                       # get_db · require_account
│   ├── auth_router.py
│   ├── setting_router.py             # 유형 · 프로젝트 · 프로필 · 경력
│   ├── task_router.py
│   ├── meeting_router.py
│   ├── meeting_stream_router.py      # WS — STT 중계
│   ├── schedule_router.py            # 캘린더 조회 · 일정 이동
│   ├── document_router.py
│   └── job_router.py
├── service/                          # 2층 — 도메인 규칙
│   ├── auth_service.py
│   ├── work_type_service.py · project_service.py · profile_service.py
│   ├── task_service.py
│   ├── schedule_service.py           # 겹침 검사는 여기 하나뿐
│   ├── meeting_service.py
│   ├── meeting_stream_service.py     # WS 2단 중계 + 녹음 적재
│   ├── meeting_batch_service.py      # 배치 트리거 · 결과 검증 · 통합
│   ├── document_service.py · folder_service.py
│   └── job_service.py
├── repository/                       # 3층 — ORM/SQL
├── models/                           # SQLAlchemy 선언 — erd 가 정본
├── dto/                              # 내부 계약
├── schemas/                          # 프론트 계약
├── integrations/
│   ├── soniox.py                     # WS 클라이언트
│   ├── agent.py                      # open-kknaks AgentClient 래퍼
│   └── storage.py                    # 녹음·md 파일 경로와 입출력
├── ai_schemas/                       # codex output_schema JSON — 배치·통합
├── seed/                             # 계정 · 기본 유형 3종 · PARA 폴더 4종
└── tests/
```

**한 파일에 한 층.** `api/`의 파일은 `service/`만 import 하고, `service/`의 파일은 `repository/`·`integrations/`만 import 한다.

## 5. 비동기 엔진

| 결정 | 내용 | 근거 |
|---|---|---|
| 드라이버 | **psycopg3 async** (`postgresql+psycopg://`) | 마이그레이션·시드(동기)와 앱(비동기)이 **같은 드라이버**를 쓴다. asyncpg 를 쓰면 alembic 용 동기 드라이버를 따로 물려야 하고 타입 처리 차이가 두 갈래로 갈린다 |
| 세션 | `async_sessionmaker(engine, expire_on_commit=False)` | async 에서 lazy-load 재조회는 `MissingGreenlet` 으로 터진다 — commit 뒤 속성 읽기를 재조회 없이 하려면 필수 |
| 커넥션 | `pool_pre_ping=True` | 서버 재부팅으로 끊긴 커넥션을 재사용하지 않게 |
| 블로킹 금지 | 비동기 경로에서 동기 I/O(파일 쓰기·`requests`·`time.sleep`)를 호출하지 않는다. 파일 적재는 `anyio.to_thread` 로 밀어낸다 | 녹음 중계가 이벤트 루프를 잡으면 오디오가 밀린다 |

### 5-1. STT 중계 (`meeting_stream_service`)

- WS 엔드포인트는 **회의 하나에 하나**다(`WS /api/meetings/{id}/stream`). 브라우저 WebSocket 이 헤더를 못 붙이므로 **접속 직후 첫 텍스트 프레임으로 access 토큰을 보내 인증**하고, 실패하면 즉시 닫는다.
- 업스트림(Soniox) 연결은 **클라이언트 연결 성립 후에** 연다. 미리 열어 두지 않는다 — 스트림 시간이 과금·한도(300분)에 직결된다.
- 오디오 청크는 **① 녹음 파일 append → ② Soniox 전달** 순으로 흐른다. 파일 적재가 실패하면 그 자리에서 끊는다(원본이 남지 않는 녹음을 계속하지 않는다).
- 다운스트림은 **잠정 토큰은 그대로 push, 확정 토큰만 DB 적재**한다(DEC-003 §3).
- **백프레셔** — 클라이언트로 보낼 큐가 상한을 넘으면 잠정 토큰을 버린다(확정 토큰은 버리지 않는다). 잠정은 어차피 다음 응답에서 리셋 렌더된다(soniox).
- 회의 종료·연결 끊김 어느 쪽이든 **업스트림을 반드시 닫는다** — 종료 처리는 `finally` 에 둔다.

### 5-2. AI 작업 (`integrations/agent.py`)

- `AgentClient` 는 **싱글턴**이다. 브로커 연결은 첫 제출 때 한 번 맺는다.
- 배치·통합 제출은 **`options.resume = {"mode": "session", "session_id": meeting.ai_session_id}`** 로 **회의 하나의 세션을 이어 쓴다**(DEC-003 §STT). 웜스타트가 그 세션을 만들고 결과는 버린다.
- 출력은 **`provider_options.output_schema`** 로 강제한다(`ai_schemas/` 의 JSON 파일 경로). **그래도 받은 JSON 을 우리가 다시 검증한다** — 강제와 검증은 다른 층이다(§8 M-16·M-15).
- **codex 실행 옵션은 한 곳(빌더 함수)에서만 만든다.** 새 세션 호출과 resume 호출이 다른 옵션으로 나가는 사고를 구조로 막는다.

### 5-3. 작업 실행

장시간 작업(회의 종료 통합)은 **`job` 행이 정본**이고, 실행은 **back 프로세스의 asyncio 태스크**가 한다.

- 별도 워커 프로세스를 하나 더 두지 않는다 — codex 실행 자체는 이미 open-kknaks 워커가 하고, back 태스크가 하는 일은 대기와 DB 쓰기뿐이다. 단일 사용자 서버 1대에서 프로세스를 늘릴 이득이 없다(`../system/README.md` SYS-1).
- **기동 스윕** — 앱이 뜰 때 `queued`/`running` 으로 남은 job 을 훑어 재개하거나 실패로 마감한다. 재시작으로 끊긴 「생성중」이 영원히 도는 것을 막는다.
- **스윕 실패가 기동을 막지 않는다.** 실패는 로그로 남기고 앱은 뜬다.

## 6. 비동기 API 규약 — 장시간 작업

「회의록 생성중」이 이 규약을 쓴다(DEC-003 §4).

| 단계 | 규약 |
|---|---|
| 시작 | `POST /api/meetings/{id}/end` → **`202 Accepted`** + `{ "jobId": 123 }`. 응답을 기다리는 동안 작업이 도는 구조를 만들지 않는다 |
| 상태 조회 | `GET /api/jobs/{jobId}` → `{ id, kind, status, errorCode, errorMessage, finishedAt }` |
| 완료 통지 | **폴링**이다. 프론트가 2초 간격으로 조회한다 |
| 종료 조건 | `status ∈ {succeeded, failed}` 이면 폴링을 멈춘다. **타임아웃 상한을 둔다 — 무한 대기 금지**(DEC-003 §7). 상한을 넘으면 job 을 `failed` 로 마감한다 |
| 결과 | job 은 결과를 담지 않는다. 프론트는 완료 후 **원 리소스**(`GET /api/meetings/{id}`)를 다시 읽는다 |

**통지 경로를 둘로 두지 않는다.** WS 는 회의 스트림 하나뿐이고 종료와 함께 닫힌다 — 그 뒤를 WS 로도 알리면 재연결·인증 표면이 둘이 된다(`../system/README.md` SYS-7).

**수치(폴링 간격 2초·타임아웃·재시도 2회·배치 임계치)는 spec 이 확정한다** — DEC-003 §7 이 「수치는 spec 에서」로 넘겼다. 여기 적힌 값은 구조를 설명하는 자리값이다.

## 7. 트랜잭션 경계

| 상황 | 경계 |
|---|---|
| HTTP 요청 | **요청 하나 = 트랜잭션 하나.** `get_db` 의존성이 끝에서 commit 하고 예외면 rollback 한다. service·repository 는 **flush 까지만** 하고 commit 을 모른다 |
| 백그라운드 job | 요청 경계가 없다. **단계마다 세션을 새로 열고 그 단계 끝에 commit** 한다. 태스크 수명 내내 세션을 붙들지 않는다 |
| 외부 호출 | **codex·Soniox 호출 중에는 트랜잭션을 열어 두지 않는다.** 읽기 → (커밋) → 외부 호출 → 새 세션에서 쓰기 순으로 자른다. 수 분짜리 외부 대기가 커넥션과 락을 잡고 있으면 안 된다 |
| 겹침 검사 | 검사와 `schedule` 쓰기는 **같은 트랜잭션** 안이다(`../database/README.md` §3) |
| 로그 | 상태 전이와 `task_log` INSERT 는 **같은 트랜잭션**이다. 로그 없는 전이는 없다(DEC-002 §6) |

## 8. 에러 규약

### 8-1. 원칙 — 설계한 실패만 처리한다

> **처리하는 실패는 열거한 것뿐이다. 그 밖의 예외는 fallback 하지 않고 그대로 전파한다** — 광범위한 예외 포착은 어디서 깨졌는지를 가린다. (DEC-003 §7, 사용자 확정. DEC-004 §7 · DEC-005 §7 이 승계)

이것이 코드 규칙으로 뜻하는 것.

- **`except Exception` 을 쓰지 않는다.** 포착은 구체 예외 타입으로만 한다.
- **기본값으로 때우지 않는다.** 「없으면 빈 리스트」·「실패하면 이전 값」 같은 조용한 대체를 만들지 않는다.
- **재시도를 임의로 넣지 않는다.** 재시도는 DEC 가 명시한 두 곳뿐이다 — 회의 중 배치(다음 배치에 합쳐), 통합본 생성(2회). **자동 저장에는 재시도가 없다**(DEC-001 §7 「자동 재시도를 두지 않는다 — 실패를 가린다」).
- 로깅 목적의 포착은 **반드시 재전파**한다(`log; raise`). 로그만 남기고 삼키지 않는다.
- 예외 하나 — 앱 **기동 시 복구 스윕**은 실패해도 기동을 막지 않는다(§5-3). 이건 설계한 실패다.

### 8-2. 도메인 예외 → HTTP

service·repository 는 `fastapi` 를 모른다. 도메인 예외를 던지고, HTTP 로 바꾸는 곳은 `main.py` 에 등록한 핸들러 **하나뿐**이다.

```text
AppError (status=500, code)
├── ValidationError        422
├── UnauthorizedError      401
├── ForbiddenError         403
├── NotFoundError          404
└── ConflictError          409
```

응답 형태는 **`{"detail": "...", "code": "..."}`** 로 고정한다. `detail` 은 사람이 읽는 문구, **`code` 는 프론트가 분기하는 키**다 — 완료 거부·겹침 차단은 문구가 아니라 코드로 갈린다.

| code | HTTP | 언제 | 근거 |
|---|---|---|---|
| `token_expired` | 401 | access 만료 → 프론트가 refresh 1회 재시도 | DEC-001 §4 |
| `invalid_credentials` | 401 | 로그인 실패. **횟수를 세지 않는다** | DEC-001 §4 |
| `task_completion_blocked` | 422 | 결과자료도 완료 결과도 없이 완료 시도 | DEC-002 §4 |
| `invalid_status_transition` | 409 | 전이 그래프 위반(완료→취소 등) | DEC-002 §4 |
| `schedule_overlap` | 409 | 시간 있는 일정끼리 겹침. **종류 불문** | DEC-005 §7 |
| `work_type_locked` | 409 | 기본 유형 3종의 삭제·개명 시도 | DEC-001 §4 |
| `folder_not_empty` | 409 | 문서가 있는 폴더 삭제 시도 | DEC-004 §4 |
| `unsupported_file_type` | 422 | md 아닌 파일 업로드 | DEC-004 §7 |
| `v2_not_available` | 501 | v2 스코프 엔드포인트 호출 | DEC-001 §v2 |

**v2 는 서버에 만들지 않는다.** v2 스코프는 프론트만 그리고 토스트로 끝난다(DEC-001 §v2) — `v2_not_available` 은 프론트 실수로 실제 호출이 샜을 때의 안전망이지 정상 경로가 아니다.

### 8-3. DEC-003 §7 실패 정책 — 코드 대응

| DEC-003 §7 상황 | 구현 위치 | 처리 |
|---|---|---|
| **회의 중 배치 실패** | `meeting_batch_service` | 조용히 넘긴다. `meeting_batch_run.status='failed'` 로 남기고 **그 구간을 다음 배치 범위에 합친다.** 사용자에게 표시하지 않는다 |
| **JSON 스키마 위반** | 〃 | **그 배치 결과 전체 폐기.** 행을 하나도 넣지 않는다(부분 파싱 금지). `status='discarded'` + 구간을 다음 배치로 |
| **없는 업무 참조** | 〃 | 웜스타트 화이트리스트 밖의 `taskId` 는 **거부**. 그 줄은 `taskId` 를 떼고 `kind='action'` 으로 강등하되 **본문은 살린다** |
| **마지막 배치 실패** | 〃 | AI 탭을 **회의 중 증분 상태 그대로 유지**한다. 버리지 않는다 |
| **통합본 생성 실패** | `meeting_service` | **자동 재시도 2회** → 실패면 `status='ended'` + `integration_state='failed'`. 사람 원본·AI 탭·트랜스크립트·녹음이 모두 남아 회의록이 비지 않는다 |
| **스피너 타임아웃** | `job_service` | 상한을 넘으면 job 을 `failed` 로 마감한다. **무한 대기 금지** |
| **자동 저장 실패** | 각 PATCH 라우터 | 서버는 실패를 그대로 응답한다. **재시도하지 않는다.** 토스트 + 필드 표시는 프론트 몫(DEC-001 §7) |

이 표에 없는 예외는 **전파**한다 — 500 으로 나가고 로그에 스택이 남는다. 그게 의도다.

## 9. 인증 · 인가

- 전송은 **`Authorization: Bearer <access>`** (`../system/README.md` §흐름 ①). 쿠키를 쓰지 않으므로 CORS 는 `allow_credentials=False`, `allow_origins` 는 Tauri 웹뷰 origin 목록으로 좁힌다.
- `require_account` 의존성이 토큰을 검증하고 `account_id` 를 돌려준다. **로그인·refresh 를 뺀 모든 라우터에 걸린다** — 라우터 단위 `dependencies=[Depends(require_account)]` 로 걸어 개별 함수에서 빠뜨릴 여지를 없앤다(DEC-001 §2).
- **소유 검사는 service 가 한다.** 모든 조회·수정이 `account_id` 로 먼저 좁힌다. 남의 행을 `404` 로 돌려준다(존재 여부를 흘리지 않는다).
- 비밀번호는 **bcrypt**. 검증은 `auth_service` 안에서만 한다.

## 10. API 표면 — 프론트에 주는 schema 계약의 형태

다음 발주(프론트 아키텍처)가 받아 갈 계약의 **형태**만 고정한다. 엔드포인트 상세·필드 목록은 spec 몫이다.

| 영역 | 표면 | 형태 규약 |
|---|---|---|
| 인증 | `POST /api/auth/login` · `/refresh` · `/logout` | 토큰 3종을 본문으로 주고받는다. 쿠키 없음 |
| 설정 | `/api/work-types` · `/api/projects` · `/api/profile` · `/api/careers` | 유형·프로젝트는 **삭제분을 목록에서 제외**하고, 참조 표시용 조회만 포함한다 |
| 업무 | `/api/tasks` · `/api/tasks/{id}` · `/api/tasks/{id}/status` · 자식 컬렉션 | **상태 전이는 전용 엔드포인트**다 — 게이트 판정이 붙기 때문에 일반 PATCH 에 섞지 않는다 |
| 캘린더 | `GET /api/schedules?from=&to=` · `PATCH /api/schedules/{id}` | 기간은 **UTC** 로 받는다. 응답 항목은 `sourceType`·`sourceId` + 원본의 표시 정보(제목·유형 색·상태)를 함께 담는다 — 캘린더가 조인 결과를 그대로 그린다 |
| 회의록 | `/api/meetings` · `/api/meetings/{id}` · `/start` · `/end` · 줄·안건 컬렉션 | 상세 응답은 **트랙별로 갈라서** 준다(`humanLines` · `aiLines` · `mergedLines`) — 탭이 트랙 하나를 통째로 그린다 |
| 회의 스트림 | `WS /api/meetings/{id}/stream` | 첫 프레임 인증 → 오디오 업 / 토큰·AI 증분 다운 |
| 문서함 | `/api/folders` · `/api/documents` · `/api/documents/{id}/content` | **본문은 별도 엔드포인트**다. 목록·메타에 본문을 싣지 않는다 |
| 작업 | `GET /api/jobs/{id}` | §6 |
| 메시지함 | **없다** | v1 에 저장 대상도 API 도 없다(DEC-006 §3·§5) |

공통 — 목록 응답은 `{ items: [...], ... }` 로 감싼다(총계·집계를 나중에 덧붙일 자리). 응답 키는 camelCase.

## 11. 설정 · 환경변수

전부 env 에서 읽고 `config.py` 의 `Settings`(pydantic-settings) 하나로 모은다. **코드에 상수로 박지 않는다.** 비밀값의 기본값을 두지 않는다 — 없으면 기동에 실패하게 한다.

| 변수 | 용도 | 비고 |
|---|---|---|
| `DATABASE_URL` | Postgres 접속 | `postgresql+psycopg://` |
| `REDIS_URL` | open-kknaks 브로커 | worker 와 같은 값 |
| `AI_NAMESPACE` · `AI_QUEUE` | 브로커 네임스페이스·큐 | **worker 설정과 일치해야 한다** |
| `AI_MODEL` · `AI_TIMEOUT_SEC` | codex 모델·상한 | 미지정이면 codex 기본 |
| `SONIOX_API_KEY` | **long-lived 키. 서버에만 둔다** | 프론트로 절대 내려보내지 않는다 |
| `JWT_SECRET` | 토큰 서명 | 기본값 없음 |
| `ACCESS_TOKEN_TTL_MIN` = 60 · `REFRESH_TOKEN_TTL_DAYS` = 7 | 세션 수명 | DEC-001 §4 |
| `STORAGE_ROOT` | 녹음·md 저장 루트 | 컨테이너 볼륨 |
| `CORS_ORIGINS` | Tauri 웹뷰 origin 목록 | `*` 금지 |

**worker 쪽 env**(`AI_CWD`·`CODEX_HOME`·`PATH`)는 compose 가 잡는다 — back 이 아니라 워커의 설정이다(`../system/README.md` §codex 바인드 마운트).

## 12. 테스트 규약

| 항목 | 규약 |
|---|---|
| 러너 | pytest + `asyncio_mode = "auto"`. httpx `AsyncClient` 로 앱을 직접 태운다 |
| DB | **실제 PostgreSQL**(테스트 DB). **SQLite 금지** — JSONB·`timestamptz`·부분 인덱스가 재현되지 않아 통과해도 의미가 없다 |
| 격리 | 테스트마다 트랜잭션을 열고 끝에서 롤백한다 |
| 외부 호출 | **Soniox·codex 를 테스트에서 실제로 부르지 않는다.** `integrations/` 어댑터를 대역으로 바꾼다 — 대역은 이 경계에서만 만든다(service·repository 를 목으로 바꾸지 않는다) |
| 층별 | repository 는 DB 를 붙여서, service 는 실제 repository 와 대역 어댑터로, router 는 앱 전체로 |

**반드시 있어야 하는 테스트** — 없으면 리뷰 반려다.

1. **완료 게이트** — 결과자료도 완료 결과도 없이 `done` 요청 시 `422 task_completion_blocked` 이고 **상태가 바뀌지 않았다**(DEC-002 §4).
2. **상태 전이** — 완료 → 취소가 `409` (DEC-002 §4).
3. **겹침 차단** — 시간 있는 업무와 회의가 서로 막고, 종일 일정은 안 막고, **경계 접촉(10–11 / 11–12)은 통과**한다(DEC-005 §7).
4. **소프트 딜리트** — 삭제한 유형이 선택 목록에서 빠지고, **참조 중인 업무에는 이름·색이 그대로 보인다**(DEC-001 §4).
5. **`schedule` 단독 소유** — 업무·회의 모델에 시간 컬럼이 없다(모델 리플렉션 검사). 캘린더 드래그와 상세 드로어 수정이 **같은 행**을 고친다(DEC-005 §3).
6. **스키마 위반 폐기** — 잘못된 JSON 배치 결과가 오면 **줄이 하나도 안 들어가고** 구간이 다음 배치로 넘어간다(DEC-003 §7).
7. **화이트리스트 강등** — 목록 밖 `taskId` 가 온 줄이 `action` 으로 강등되고 **본문이 남는다**(DEC-003 §7).
8. **통합 실패** — 2회 재시도 후 `ended` + `integration_state='failed'` 이고 **사람 줄·AI 줄·트랜스크립트가 그대로 남는다**(DEC-003 §7).
9. **고아 `schedule` 없음** — 업무·회의 생성/삭제 경로를 지난 뒤 `schedule` 의 `source_id` 가 전부 살아 있는 행을 가리킨다(FK 를 안 걸었으므로 테스트가 대신 잡는다 — `../database/README.md` §3).

## 13. 결정 요약 — 근거 색인

| # | 결정 | 근거 |
|---|---|---|
| BE-1 | FastAPI · uv · router→service→repository | 제약 |
| BE-2 | schema(pydantic·camel) / dto(dataclass·snake) 를 섞지 않고, **입력도 dto** | 제약 + 계약 명시성 |
| BE-3 | SQLAlchemy 2.0 async + psycopg3 async | 비동기 제약 + alembic 과 드라이버 일치 |
| BE-4 | 장시간 작업은 job 리소스 + 폴링. 실행은 back asyncio 태스크 + 기동 스윕 | DEC-003 §4 · SYS-1 |
| BE-5 | 트랜잭션은 요청 하나. 외부 호출 중에는 열지 않는다 | 장기 락 회피 |
| BE-6 | 도메인 예외 → 핸들러 한 곳에서 HTTP 매핑. 응답에 `code` 를 싣는다 | DEC-002 §4 · DEC-005 §7 |
| BE-7 | **`except Exception` 금지 · 임의 재시도 금지 · 조용한 기본값 금지** | DEC-003 §7 |
| BE-8 | Bearer 인증, 라우터 단위 게이트, 소유 검사는 service | DEC-001 §2 |
| BE-9 | 테스트는 실제 Postgres. 대역은 `integrations/` 경계에서만 | 스키마 특성 재현 |

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| BE-OQ-1 | **회의 중 AI 증분 push 채널** — STT WS 를 겸하도록 정했다. 사람이 회의록 탭만 보고 있어도 AI 줄이 계속 흘러오는데, 프론트가 이걸 버퍼링할지 즉시 반영할지는 화면 규격(DEC-003 OQ-1 AI 탭 렌더)에 걸린다 | 사용자(디자인) | spec 전 |
| BE-OQ-2 | **업무 갱신(`pendingChange`) 의 허용 필드** — 12-meeting-notes 는 `{dueDate, status, note}` 로 그렸는데, `dueDate` 는 이제 `schedule` 소관이고 `note` 는 업무의 어느 필드인지(메모? 배경?) 정책에 없다 | 사용자 | spec 전 |
| BE-OQ-3 | **회의 시작 웜스타트의 컨텍스트 크기** — 「선택 프로젝트 + 그 프로젝트의 업무 + 안건」(DEC-003 §8)인데 무소속 회의는 업무 목록이 비게 된다. 무소속일 때 무엇을 주는지 정책에 없다 | 사용자 | spec 전 |

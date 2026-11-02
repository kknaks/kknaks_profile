# WORK-001 WP1 결과 보고 — back 뼈대 · 로그인 · 용어집

## 상태: done

## 수행 — 파일·모듈 목록
워크트리 `/Users/kknaks/orca/workspaces/interpret-pwa/interpret-pwa-poc` (커밋 없음 · 변경만)

- `back/pyproject.toml` · `uv.lock` · `.python-version`(3.12) · `.dockerignore` · `Dockerfile`(CMD `uvicorn app.main:app --port 8800`)
  - 의존성: fastapi · uvicorn[standard] · pydantic · pydantic-settings · httpx · websockets · opencc-python-reimplemented / dev: pytest · ruff (원형의 pyjwt · bcrypt 는 안 씀 — DB · 해시 없음)
- `back/app/config.py` — SPEC §2.4 env 전부(`SONIOX_API_KEY` · `INTERPRET_LOGIN_ID` · `INTERPRET_LOGIN_PASSWORD` · `INTERPRET_SESSION_SECRET` · `INTERPRET_SESSION_HOURS`=12 · `INTERPRET_FRONT_ORIGIN`=`http://localhost:3800` · `GLOSSARY_MATRIX_URL`=stg 주소 · `GLOSSARY_CONTEXT_MAX_CHARS`=10000) · 레포 루트 `.env` → `back/.env` · `env_ignore_empty`
- `back/app/container.py` — `Container(settings, auth, glossary, glossary_transport)` · `load_glossary()` · `context_for(lang)`
- `back/app/main.py` — `create_app()` · lifespan 에서 용어집 1회 읽기 · CORS = `INTERPRET_FRONT_ORIGIN` · 오류 처리기 `{error:{code,message}}`(DomainError · 검증 400 `invalid_request` · HTTP) · 접근 로그 쿼리 지움(`DropQueryString`) · `app.main:app` 은 모듈 `__getattr__` 로 처음 꺼낼 때 생성(import 만으로 실 env 를 안 읽음)
- `back/app/domain/errors.py` — `DomainError` · `BadRequest` · `Unauthorized` · `TooManyAttempts`
- `back/app/service/auth.py` — env 대조(`hmac.compare_digest` 아이디 · 비번 둘 다 비교 뒤 판정) · 5회/60초 잠금(back 전체 단위) · HMAC-SHA256 토큰 `{sub, exp}` · 검증 = 서명 · 만료 · `sub == 지금 env 아이디`
- `back/app/service/glossary.py` — `load_glossary()`(10초 · 실패 4종 → 빈 용어집 · 경고 1줄 이유 종류만) · `Glossary.menu_rows()` · `build_context(rows, lang, max_chars)`(순수) · `without_terms()`(WP2 재연결용)
- `back/app/service/interpret/langs.py` — 6개 언어 · Soniox 매핑(`yue`→`zh`) 한 곳 · `chinese.py` — 원형 복사 + `to_simplified`(t2s)
- `back/app/schemas/{auth,glossary}.py` · `back/app/api/{deps,auth,glossary}.py` — `POST /api/auth/login` · `GET /api/auth/me` · `GET /api/glossary?lang=` · `GET /api/health`
- `back/tests/{conftest,test_auth,test_glossary,test_context}.py` — 가짜 값 · 모양만 맞춘 가짜 matrix(httpx MockTransport)
- 루트 `docker-compose.yml`(back 8800 · `env_file .env required:false` / front 3800 · `build.args NEXT_PUBLIC_API_BASE_URL: ${NEXT_PUBLIC_API_BASE_URL:-http://localhost:8800}`) · 루트 `.env.example`(이름만 · 값 0 · `INTERPRET_BACK_PORT` 없음)

## 검증 — 명령과 수치
- `cd back && uv run ruff check .` → All checks passed
- `uv run pytest -q tests/test_auth.py tests/test_glossary.py tests/test_context.py` → **56 passed**
- `.env.example` 값 0 — `grep` 으로 `NAME=` 뒤 값 있는 줄 0
- 실물 matrix 1회(8800 · 끝나고 내림 · 로그인 값은 그 자리에서 만든 임시 가짜값을 프로세스 env 로만):
  - 기동 로그: `glossary loaded: version=2026-07-01-reviewed-v5 count=158`
  - `/api/health` → `{"ok":true,"glossary":{"loaded":true,"version":"2026-07-01-reviewed-v5","count":158}}`
  - `/api/glossary?lang=yue` → 158행 · 번체 그대로(예 `필러 → 填充劑` · t2s 로 바뀌는 = 번체 표기 85칸 · 예 `脫毛` · `飛梭鐳射(Fraxel)`) · 토큰 없이 401
  - 기동 로그에 비밀번호 · 세션 비밀 · `token=` 0건
- 실물 matrix 로 잰 context 길이(`json.dumps(ensure_ascii=False)` · general 포함 · 중복 ko 1개 빠져 157쌍): en 9,295 · ja 8,989 · zh 8,572 · th 9,900 · vi 9,579 · yue 8,501자 → **6개 모두 10,000자 안 · terms 줄임 0**. 토큰 기준 한도는 WP2 §9.3 ① 실물에서

## 계약 대조 — SPEC 항목별
- §2.2 포트 8800 고정(Dockerfile CMD · compose) — 같음
- §2.3 compose `env_file required:false` · front `build.args` 치환 — 같음
- §2.4 env 이름 · 기본값 · 루트 → back 순서 — 같음
- §3.1 상수 시간 · 같은 401 · 5회 → 1분 429 · 성공 시 초기화 — 같음(원형처럼 5번째 실패는 401 + 잠금 시작, 6번째부터 429)
- §3.2 토큰 형식 · 검증 · env 아이디 변경 시 401 — 같음
- §3.3 login `{token, expiresAt}`(ISO 8601 · UTC `+00:00`) · 필드 빠짐/그 밖 필드/비문자열 400 `invalid_request` · me `{id}` · health `{ok, glossary:{loaded, version, count}}` — 같음
- §4.2 기동 1회 · 실패 4종 빈 용어집 · 중복 ko 첫 행 · 빈 표기 뺌 — 같음
- §4.3 general 3쌍 · terms ko · translation_terms ko→L · yue target t2s · zh 그대로 · 괄호 병기 그대로 · text 없음 · 역방향 없음 — 같음
- §4.4 1~3 글자 수 · terms 뒤에서부터 · translation_terms 안 줄임 — 같음(4 재연결 · 5 로그는 WP2)
- §4.6 `{loaded, version, count, lang, rows:[{category, ko, term}]}` · yue 번체 원본 · 중복 그대로 · loaded=false 면 rows [] · version null · count 0 — 같음

## 이슈 · 코디가 확인할 것
- `/api/glossary` 는 인증(401) 을 lang 검사(400) 보다 먼저 본다 — 토큰 없이 잘못된 lang 이면 401.
- `count` = 받은 rows 수(matrix 의 `count` 필드가 아니라 실제 행 수 · 실물은 둘 다 158).
- `expiresAt` 는 UTC 오프셋(`+00:00`) — 원형은 KST 오프셋이었다. 둘 다 ISO 8601.
- 실물 로그인 값 · 키는 레포 루트 `.env` 에 없음(파일 없음) — 사용자 계정 로그인 실물은 미확인(계약 모양은 시험으로 고정).

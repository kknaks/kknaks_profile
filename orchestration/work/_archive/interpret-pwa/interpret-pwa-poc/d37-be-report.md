# D-37 결과 보고 — 밖으로는 통역에 필요한 최소 정보만 (backend)

## 상태: done

base main `10b4c38` · 커밋 없음 · `back/**` 만(워크트리의 `design/**` · `front/**` 변경은 다른 워커 것).

## 수행 — 파일·모듈 목록

| # | 파일 | 무엇 |
|---|---|---|
| ① | `back/app/api/glossary.py` · `back/app/schemas/glossary.py` **삭제** | `GET /api/glossary` 와 그 스키마 삭제. `Glossary.menu_rows` 도 삭제(쓰는 곳 0). 시드 로더 · 검사 · context 조립은 그대로 |
| ② | `back/app/api/health.py`(새) · `back/app/schemas/health.py`(새) | `GET /api/health` → **`{"ok": true}`** 만. 사전 판 · 개수는 기동 로그 `glossary seed loaded: version=… terms=… entries=…` 에만(이미 있음) |
| ③ | `back/app/api/auth.py` · `back/app/schemas/auth.py` | `GET /api/auth/me` → **`{"ok": true}`**(아이디 없음 · 토큰이 틀리면 지금처럼 401). front 는 `ok` · 401 만 본다(코디 전달 그대로) — `expiresAt` 은 front 가 이미 로그인 응답으로 갖고 있어 넣지 않았다 |
| ④ | `back/app/service/interpret/session.py` | WS `error` 문구 일반화 — **코드는 그대로**. 문구 상수 4개(아래) · 원인은 back 로그에만(`bad start: <예외 종류>` · `SONIOX_API_KEY 가 비어 있다` 경고 · 기존 soniox 로그) · 받은 값을 되돌려 보내지 않는다(옛 「알 수 없는 type: 'x'」 · 「지원하지 않는 언어예요: 'xx' (가능: …)」 삭제) |
| ④ | `back/app/main.py` · `back/app/service/auth.py` | HTTP 오류 본문도 같은 원칙 — 검증 오류는 필드 경로 · 검증기 문구 없이 `400 invalid_request` 「요청 형식이 맞지 않아요」 · 404 `not_found` 「찾을 수 없어요」(데모 꺼짐 404 도 같은 문구) · 그 밖 HTTP 오류 `http_error` 「요청을 처리하지 못했어요」 · **처리기 밖 예외도 JSON 500 `internal`**(원인 종류는 로그에만). 로그인 401 · 429 문구는 화면에 그대로 쓰는 사용자 문구라 둠 |
| ⑤ | `back/app/main.py` | `FastAPI(docs_url=None, redoc_url=None, openapi_url=None)` — `/docs` · `/redoc` · `/openapi.json` 404 |
| ⑥ | `back/tests/test_api_surface.py`(새) · `test_glossary.py` 삭제 · `test_auth.py` · `test_context.py` · `test_interpret.py` | 아래 |

WS `error` 문구(코드 → 문구):

| 코드 | 전 | 후 |
|---|---|---|
| `bad_request` | 「첫 프레임은 start 텍스트여야 해요」 · 「지원하지 않는 언어예요: 'xx' (가능: en, ja, …)」 · 「알 수 없는 type: 'x'」 등 | **「요청을 처리할 수 없어요」** |
| `no_api_key` | 「SONIOX_API_KEY 가 .env 에 없어요」 | **「통역 서버를 쓸 수 없어요」** |
| `soniox_unavailable`(연결) | 「통역 서버(Soniox)에 연결하지 못했어요」 | **「통역 서버에 연결하지 못했어요」** |
| `soniox_unavailable`(중계 중) | 「통역 서버(Soniox) 오류로 끊겼어요」 · 「통역 중계가 끊겼어요」 | **「통역 연결이 끊겼어요」** |

## 검증 — 명령과 수치

- `cd back && uv run ruff check .` → All checks passed
- `uv run pytest -q` (전체) → **246 passed**(이전 249 − 메뉴 시험 23 + 표면 시험 20)
- `tests/test_api_surface.py`:
  - **경로 목록 고정**: 앱 경로가 정확히 `POST /api/auth/login` · `GET /api/auth/me` · `GET /api/auth/config` · `POST /api/auth/demo` · `GET /api/health` · `WS /api/interpret` 여섯(그 밖 Route 가 있으면 실패 — 새 경로는 DEC 와 함께 목록에 더한다)
  - `/docs` · `/redoc` · `/openapi.json` · `/docs/oauth2-redirect` · `/api/glossary` → 404 일반 문구
  - 응답 최소 모양: health `{"ok": true}` · me `{"ok": true}` · config `{"demoLogin": false}`
  - **시드 내용 0**: 허용 경로 전부(성공 · 401 · 404)를 불러 본 응답에 시드 판 · 시드 낱말(ko · 별칭 · 현지명 · 현지 별칭) 0
  - `app/api` · `app/schemas` 소스에 `glossary` · `.terms` · `.entries` · `menu_rows` · `load_seed` · `build_context` 0
  - 오류 일반 문구: 검증 400 · 405 · 데모 꺼짐 404 · 처리기 밖 예외 500(「secret internal detail」 응답 0 · 로그에 예외 종류) · WS 문구 4개에 `SONIOX` · `Soniox` · `.env` · `API_KEY` · `start` · `type` · `JSON` 0 · WS 에 `lang: "<script>"` 를 보내도 되돌려 보내지 않음
- grep(밖으로 쓰는 곳 전부): HTTP = `response_model` 다섯(Login · AuthConfig · Me · Health) + 오류 JSON 한 곳(`main._error`) · WS = `ready` · `caption` · `audio_start` · PCM · `audio_end` · `error` 뿐. 시드는 `container.context_for` → 세션 → `to_soniox` → Soniox STT 설정으로만 간다(응답 · WS 로 가는 길 0). `app/main.py` 의 「glossary」는 기동 때 읽기 · 로그뿐

## 계약 대조 — DEC-001 D-37

| 항목 | 판정 |
|---|---|
| `GET /api/glossary` 삭제 | 같음 |
| `/api/health` = `{ok}` 만 · 사전 판 · 개수는 서버 로그 | 같음 |
| `/api/auth/me` 에 아이디 없음 | 같음(`{ok}`) |
| WS 는 ready · caption · 오디오 · error(코드 + 일반 문구) | 같음 |
| `/docs` · `/openapi.json` 끔 | 같음(`/redoc` 도) |
| 사전은 이미지 안에서 Soniox context 로만 | 같음 — 시험 · grep |

## 이슈 · 코디가 확인할 것

1. **front 와 맞출 것**: ① `/api/auth/me` 응답이 `{id}` → `{ok}` — front `lib/api.ts` 의 `Me` 타입이 `id` 를 기대하면 고쳐야 한다(front 는 401 만 본다고 전달받음) ② `GET /api/glossary` 는 이제 404 — front 용어집 메뉴 · 창 삭제(D-37)가 같이 들어가야 한다 ③ WS `error.message` 가 위 일반 문구로 바뀜 — front 는 `message` 를 그대로 보여 주므로 화면 문구가 바뀐다.
2. 로그인 401 「아이디 또는 비밀번호가 맞지 않아요」 · 429 「로그인 실패가 많아요. 1분 뒤 다시 시도해 주세요」 · 토큰 401 「로그인이 필요해요」는 사용자 문구라 그대로 뒀다(설정 이름 · 내부 원인 없음).
3. SPEC 갱신(planner): §3.3 me · health 응답 · §4.7 메뉴 API 삭제 · §5.4 WS 오류 문구 · §2.1 폴더(`api/glossary.py` → `api/health.py`).

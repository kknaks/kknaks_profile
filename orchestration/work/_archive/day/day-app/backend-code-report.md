# DAY 앱 D1 로그인 환경 연결 — backend 구현 결과 보고

## 상태: done (단위 · 아키텍처 · ruff 통과 / infra 6건 작성 · 실행 pending — 코디가 day-local 로 실행)

- 기준: mediness `kknaksss/day-app-spec` 78f3ee59 (DAY-SPEC-001 §3 「앱 환경 연결 (데모 계정)」 · 케이스 매트릭스 끝 3줄 · §4 규칙 14, DAY-SPEC-003 세션 · 연결 대상 검증 · A-3~A-8 · A-18~A-23) + 승인된 Delivery #235 D1 · verification · rollback.
- 사용자 2026-11-09 지시(「머지는 마지막인데 코드 구현해」)로 미머지 SPEC 기준 구현. spec-baseline 은 **pending 그대로** — ready 로 쓰지 않았다. 커밋 · push · PR · 머지 · 배포 안 함.
- 코드 트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-app`(HEAD 91728737 = origin/dev). `app/**` 는 읽지도 수정하지도 않음(모바일 워커 소유 · untracked 그대로).

## 수행 — 파일

| 파일 | 변경 |
|---|---|
| `backend/common/config.py` | env 셋 `DAY_PUBLIC_API_BASE` · `DAY_DEMO_LOGIN_EMAILS` · `DAY_DEMO_API_BASE`(SPEC 제안 이름 그대로 확정) + `normalize_origin()` + 속성 `public_api_origin` · `demo_login_emails`(공백 무시 · 소문자) · `demo_api_origin`(틀리면 None). `DAY_PUBLIC_API_BASE` 가 정규화를 못 넘으면 기동 실패(SettingsError), 비면 `api_base_url` 칸 생략 |
| `backend/day/services/environments.py` (신규) | 판별 `is_demo_login`(prod · client=app · 목록 이메일만) · `own_target` · `relay_login`(dev 넘김 · 응답 검사) · `EnvironmentUnavailable`(503 `environment_unavailable`) · `RelayedError`(dev 4xx 그대로) · `RelayDeps`(HTTP transport · 60초 — 테스트 주입점) |
| `backend/day/dtos/environments.py` (신규) | `Target` · `RelayedSignedIn` · `RelayedChooseHospital`(토큰 칸 repr 제외) |
| `backend/day/routers/api/auth.py` | `/login`: `auth.login` **앞**에서 데모 분기 → 넘김 결과 반환. 앱(`client=app`) `signed_in` · `choose_hospital` · `/hospital` 에 `environment` · `api_base_url`, `/me` 에 `environment`. `relay_deps` 의존성 추가 |
| `backend/day/schemas/auth.py` | `SignedIn` · `ChooseHospital` 에 선택 칸 `environment` · `api_base_url`(exclude_none — 웹 응답엔 없음), `MeOut.environment` |
| `backend/tests/day/auth/test_environments.py` (신규 · DB 없음) | 71건 |
| `backend/tests/day/auth/test_environments_api.py` (신규 · infra) | 6건 |
| `backend/tests/day/auth/conftest.py` | `Harness` 에 `app` 칸 하나(dev 더블 주입용) |
| `deploy/local.env.example` | env 셋 placeholder(빈 값) + 롤백 방법 주석 |
| `AGENTS.md` 「앱」 한 줄 | 「고정 로그인 진입점 · 허용 서버 origin 목록 · 환경값은 `--dart-define`, 세션 연결 대상(`api_base_url`)은 검증된 로그인 응답」으로 정합(#235 승인 범위) |

수정 안 함: `services/auth.py` · `services/sessions.py` · `session.py` · `errors.py` · 웹 `routers/login.py` · migration · seed · `deploy/config/*.env` · compose · pyproject/uv.lock(httpx 기존 의존성).

## 구현 요점 — 계약 대조

| SPEC 항목 | 구현 | 같음/다름 |
|---|---|---|
| 판별 = prod · `POST /api/auth/login` · `client=app` · 목록 이메일(공백 · 소문자) | `is_demo_login` · 라우터에서 `auth.login`(KOS · DB) 전에 분기 | 같음 |
| dev 서버 · `client=web` · 웹 `/login` 은 넘기지 않음 | dev 는 설정을 안 봄 · 웹 라우트 무변경 | 같음 |
| 넘김 대상 = `DAY_DEMO_API_BASE` 정규화 origin 하나 · `POST {origin}/api/auth/login {email, password, client:"app"}` | 받은 email · password 그대로 · Authorization/Cookie 안 실음 | 같음 |
| 전체 60초 · 리다이렉트 안 따라감 · 재시도 없음 | `asyncio.timeout(60)` 이 연결~본문 끝 전체 감쌈 · `follow_redirects=False` · 1회 · `trust_env=False`(env 프록시 · netrc 미사용) · 본문 64KiB 상한 · 메모리에서만 | 같음(64KiB 상한 · trust_env 끔은 구현 선택) |
| 응답 없음 · 60초 · 3xx · 5xx · 모르는 응답 · 대상/환경 어긋남 · 주소 정규화 실패 → 503 `environment_unavailable` | 200 이외 2xx · 비JSON · 모르는 status · 필수 칸 누락 · 병원 id 비uuid · dev 가 실은 `environment≠dev` 또는 `api_base_url` 정규화≠대상 → 503 | 같음 |
| dev 4xx → HTTP · 본문 그대로 | `{detail, code(문자열)}` 모양일 때 그대로(추가 칸 포함). 그 모양이 아니면(예: 404 `{"detail":"Not Found"}`) 모르는 응답 → 503 | 같음(모양 검사는 「모르는 응답」 해석) |
| prod 행 0 · prod KOS 0 · 쿠키 · 토큰 재발급 없음 | 넘김 경로는 `auth.login` · DB 세션 · 쿠키 코드에 닿지 않음 | 같음 |
| 일반 앱 로그인 · 병원 고르기 = 자기 `APP_ENV` + 자기 `DAY_PUBLIC_API_BASE` · `/me` environment | `own_target` | 같음. `DAY_PUBLIC_API_BASE` 비면 `api_base_url` 생략(정식 앱은 「환경 칸 필수」로 실패 — fail-closed) |
| 잘못된 `DAY_DEMO_API_BASE` + 목록 유지 → 데모 로그인 503 (일반 인증으로 새지 않음) | 넘김 판별은 목록만 보고, 대상이 None 이면 503 | 같음(Delivery rollback 경로) |
| 빈 비밀번호 | 데모 이메일이어도 넘기지 않고 400 `invalid_request` | SPEC Validation 과 같음 |
| 요청 칸 · 헤더로 환경 고르기 불가 | 요청 스키마 무변경 · 판별은 서버 설정만 | 같음 |
| 로그 = 「데모 로그인 넘김 · 결과 코드」만 | `demo login relay result=<signed_in\|choose_hospital\|dev 오류 code\|redirect\|http_5xx\|timeout\|unknown_body\|target_mismatch\|…>` — 이메일 · 비밀번호 · 토큰 · 주소 없음(테스트로 확인) | 같음 |
| `APP_ENV` · `DB_SCHEMA` 를 요청마다 바꾸지 않음 | 프로세스 설정 읽기만 | 같음 |
| 임시 병원 선택은 dev 담당 | prod 는 dev 의 `pending_token` 을 그대로 넘기고 `/hospital` 은 앱이 dev 로 보냄 | 같음 |

## 검증 — 명령과 수치

| 명령 | 수정 전(baseline) | 수정 후 |
|---|---|---|
| `uv run pytest -q -m "not infra" backend/tests/day/auth` | 17 passed, 30 deselected | **88 passed**, 36 deselected (+71 · D1 단위) |
| `uv run pytest -q -m "not infra"` (전체 단위) | 409 passed, 161 deselected | **480 passed**, 167 deselected |
| `uv run pytest -q backend/tests/architecture` | — | **27 passed** |
| `uv run pytest -q backend/tests/day/auth` (infra env 없음) | — | 88 passed, 36 skipped (infra 는 skip — 실행 아님) |
| `uv run ruff check backend` · `ruff format --check backend` | All checks passed | All checks passed · 158 files already formatted |

증거: `backend-evidence/`(baseline-*.txt · after-*.txt · diff-stat.txt · status.txt).

단위(DB · 네트워크 없음 — dev = `httpx.MockTransport` 더블, 이 서버 KOS = 부르면 기록되는 가짜, DB = 쓰면 AssertionError 인 가짜) 축: 주소 정규화 5+19 · 설정(목록 · 대상 None · 공개 주소 기동 실패) · 판별 6 · 데모 signed_in/choose_hospital(대소문자 · 공백) · dev 대상 칸 일치/불일치 4 · 5xx · 비JSON · 모르는 status · 칸 누락 · 비uuid · 201 · 204 · 404(code 없음) · 4xx 비JSON · 64KiB 초과 13 · 리다이렉트 301/302/303/307/308(요청 1건만) · dev 4xx 4종 그대로 · 연결 실패 · 전체 시간 초과(느린 머리 · 늦게 흐르는 본문) · 기본 60초 · 잘못된/빈 대상 주소 3 · 일반 계정 · client=web · dev 서버 비넘김 · 요청 칸/헤더 무시 · 빈 비밀번호 · 로그 비밀값 없음 · repr.

infra(실행 pending · `@pytest.mark.infra` · 기존 `day_test` fixture · 설정 더블 `model_copy` 로 라우터가 읽는 설정만 prod 흉내 — 프로세스 env · 스키마 · 실제 prod 무변경): ① dev 앱 로그인 environment/api_base_url · `/me` environment · 웹 JSON 응답 칸 그대로 ② 공개 주소 비면 칸 생략 ③ 병원 여럿 choose_hospital · `/hospital` 대상 칸 · web 은 없음 ④ prod 일반 계정 = prod 대상 ⑤ **prod 데모 넘김 성공 · dev 4xx · dev 연결 실패 · dev 500 · 대상 설정 틀림 → 테스트 DB account · staff · login_session · external_session · external_ref 행 수 전후 동일 + 이 서버 KOS 호출 0**(코디 후속 지시 반영) ⑥ prod 웹 JSON · 웹 `/login` 화면은 데모 이메일도 넘기지 않음.

## 이슈 · 코디가 확인할 것

1. **infra 6건 미실행** — 워커는 DB · Docker · 실 env 를 쓰지 않았다. 코디가 기존 day-local 로 `scripts/test.sh -q`(또는 `scripts/test.sh -q backend/tests/day/auth`) 실행 필요. 처음 도는 테스트라 실패 시 테스트 쪽 조정이 필요할 수 있다.
2. `EnvironmentUnavailable` 을 `day/errors.py` 가 아니라 `services/environments.py` 에 뒀다 — errors.py 가 allowed_paths 밖이라서. errors.py 로 옮길지 코디 판단(옮기면 `test_오류_코드는_매트릭스_그대로` 표에 한 줄).
3. `deploy/config/dev.env` · `prod.env`(실제 서버 일반 설정) · `compose.local.yaml`(env 명시 목록) 은 수정하지 않았다 — 「실제 env 수정 금지」. 그래서 로컬 컨테이너는 새 env 를 받지 않는다(빈 값 = `api_base_url` 생략 · 넘김 꺼짐 — 기존 동작). 배포 반영 때 사용자 값: prod `DAY_PUBLIC_API_BASE` · `DAY_DEMO_LOGIN_EMAILS` · `DAY_DEMO_API_BASE`, dev `DAY_PUBLIC_API_BASE` = prod `DAY_DEMO_API_BASE` 같은 origin.
4. 기존 웹 보존: `/login` · `/login/hospital` · `/logout` 무변경, JSON `client=web` 응답 칸 그대로(infra ①③⑥ 로 확인 예정), 기존 앱 응답은 칸이 **더해지기만** 함. `/me` 는 cookie 세션에도 `environment` 를 싣는다(JSON 은 앱 전용 계약이라 추가 칸).
5. 보안 경계: 넘김 대상은 설정 origin 하나 · 리다이렉트 금지 · env 프록시/netrc 미사용 · 재시도 없음 · 비밀번호 · 이메일 · 토큰 로그 없음 · dev 토큰은 응답으로 한 번만 전달(저장 없음). 시간 초과 뒤 dev 의 늦은 성공 세션은 SPEC 대로 dev 에 남고 앱에 전달되지 않는다.
6. 실통합(dev 서버 · prod 배포 뒤 데모 넘김 · prod DB 행 0 사용자 조회) — pending(Delivery 범위 밖). D2 · D3 서버 구현 안 함.

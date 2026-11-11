# DAY 앱 D1 — 독립리뷰 F1 · W1~W4 수정 결과 보고

## 상태: done (단위 · 아키텍처 · ruff · compose shape 확인 / infra 전체 재실행은 코디)

- 입력: `review-backend-code-report.md`(FAIL — F-1 · W-1~W-5 · R-1~R-4), 기존 `backend-code-report.md`, 사용자 지시 `implementation-user-direction.md`(미머지 SPEC 78f3ee59 기준 구현 · baseline pending 유지).
- 커밋 · push · PR · 머지 · 배포 · 컨테이너 기동 · DB · 실 env 읽기 안 함. `app/**` 읽기 · 수정 안 함.

## 수행

| 항목 | 파일 | 변경 |
|---|---|---|
| F-1 | `deploy/compose.local.yaml` | `x-backend.environment` 명시 목록에 `DAY_PUBLIC_API_BASE` · `DAY_DEMO_LOGIN_EMAILS` · `DAY_DEMO_API_BASE` 를 `${VAR:-}` 로 3줄(+주석 1줄). api · worker · scheduler · migrate 가 같은 앵커로 받는다 |
| W-1 | `backend/day/services/environments.py` | `json.loads` 가 `ValueError` 와 `RecursionError` 둘 다 → `not_json` → 503 `environment_unavailable` |
| W-2 | 같은 파일 | `RelaySlots`(프로세스당 하나 · `RELAY_MAX_IN_FLIGHT = 4` 기술 기본값 · 대기열 없음). 자리가 없으면 dev 로 보내지 않고 바로 503(`result=busy` 로그 · 비밀 없음). 자리는 `try/finally` 로 끝 · 실패 · 시간 초과 · 취소(CancelledError) 모두 반환. 60초 전체 timeout · redirect 0 · retry 0 그대로. `RelayDeps.slots` 기본값 = 프로세스 자리(테스트는 새 자리 주입) |
| W-3 | `backend/common/config.py` | `SettingsConfigDict(..., hide_input_in_errors=True)` 한 곳 — 검사 오류 메시지에 받은 값(userinfo · path 등)이 안 실림 |
| W-4 | `deploy/config/dev.env` · `prod.env` | 끝에 세 이름 빈 placeholder + 주석만 추가. 기존 값 무변경 · 새 주소/계정 값 없음. `scripts/deploy/day_vm.py` 금지 키(`FORBIDDEN_CONFIG_KEYS` · `DAY_LOCAL_`/`DAY_SEED_`/`DAY_TEST_` 접두어)에 안 걸림. 서버 manifest(`compose.yaml` env_file)는 수정 불필요 |
| R-2 | `services/environments.py` | 로그 `result=` 는 SPEC-001 로그인 단계 코드 11개만 그대로, 그 밖 dev 4xx `code` 는 `dev_client_error`. 응답 본문은 원본 그대로 넘김(테스트로 확인) |
| R-4 | `backend/tests/day/auth/test_environments.py` | autouse fixture 가 세 새 env 를 `delenv` — 셸 값에 흔들리지 않음(값은 읽지 않음) |

이동 안 함: R-1(오류 클래스 위치 — 동작 문제 없음) · R-3(틀린 `DAY_PUBLIC_API_BASE` 기동 실패 — 정해진 계약 유지).

W-5 판정: 일반 앱 로그인 · `/hospital` · `/me` 새 칸의 성공 경로는 infra 6건이 맡고, 코디의 `scripts/test.sh -q` 전체 **647 passed**(신규 infra 6 포함)로 이미 확인됐다. 성공 경로는 `auth.login` 이 DB 를 써야 나오므로 단위로 중복 작성하지 않았다.

## 새 회귀 테스트 (`test_environments.py` · DB · 네트워크 없음 · +16)

- W-1: 200 · 401 본문이 `[`×30000 깊이 → 503(파라미터 2) · 50겹 중첩 4xx 본문은 그대로 전달.
- W-2: 동시 4개가 dev 에 닿은 상태에서 5번째 → 대기 없이 503 · dev 요청 4건 그대로 · KOS 0 · `busy` 로그 → 풀면 4개 200 · 자리 0 · 다음 요청 200 / 실패 5종(연결 · 시간 초과 · 5xx · 4xx · 깨진 본문)을 상한+2번 연속 → 자리 0 · 이어서 성공 / 진행 중 task 취소 → CancelledError · 자리 0 / 기본 `RelayDeps` 둘이 같은 프로세스 자리(limit 4).
- W-3: 비밀 모양 입력 4종(userinfo · path · 시간대 · 정수 칸)의 `str`/`repr` 에 원값 없음.
- R-2: dev 429 `code="<script>…"` → 본문 그대로 · 로그 `dev_client_error`.
- mutation 확인(scratchpad 백업 후 되돌림 · `cmp` 일치): 자리 반환 제거 → 7 실패 · `RecursionError` 처리 제거 → 3 실패 · `hide_input_in_errors=False` → 4 실패.

## 검증 — 명령과 수치

| 명령 | 이전(backend-code-report) | 지금 |
|---|---|---|
| `uv run pytest -q -m "not infra" backend/tests/day/auth` | 88 passed | **104 passed**, 36 deselected |
| `uv run pytest -q -m "not infra"` | 480 passed | **496 passed**, 167 deselected |
| `uv run pytest -q backend/tests/architecture` | 27 passed | **27 passed** |
| `uv run ruff check backend` · `ruff format --check backend` | 통과 | All checks passed · 158 files already formatted |
| `docker compose -f deploy/compose.local.yaml --env-file <scratchpad 가짜 env> --profile app config --format json` (빈 환경 `env -i` · 세 키만 추출) | — | 가짜 값 env: api · worker · scheduler · migrate 모두 세 값 전달 / 세 값 없는 env: 넷 모두 `""` · postgres · redis 에는 없음 |

증거: `backend-evidence/fix1-verify.txt` · `fix1-compose-config.txt` · `fix1-diff-stat.txt`. compose 확인은 `deploy/local.env` 를 쓰지 않았고 출력에서 세 키만 뽑았다(실값 · 비밀 출력 없음). 컨테이너 기동 없음.

## 계약 대조

결과 계약 무변경 — 판별 위치 · 행 0 · 대상 하나 · redirect 0 · retry 0 · 전체 60초 · dev 4xx 보존 · 그 밖 503 · 웹 무변경 · 롤백 경로 그대로. 새로 더한 503 경우(동시 상한 초과 · 깊은 중첩)는 SPEC-001 「모르는 응답 · dev 넘김 불가 → `environment_unavailable`」 안의 fail-closed 이며 prod 우회 없음.

## 코디가 확인할 것

1. infra 포함 전체(`scripts/test.sh -q`) 재실행 — 코디 몫. infra 파일(`test_environments_api.py`)은 이번에 바꾸지 않았다.
2. `deploy/config/dev.env` · `prod.env` 에 빈 이름만 들어갔다 — dev/prod 배포 시 값이 비어 있으면 `api_base_url` 칸이 빠지고 넘김이 꺼진다(기존 동작). 실제 값 · Key Vault · 서버 설정은 사용자 몫.
3. 상한 4 는 프로세스(uvicorn worker)당이다 — 서버가 worker 를 늘리면 전체 상한도 그 배수.

# 리뷰 리포트 — day-app / code · backend D1 재검수 (2026-11-09)

- 대상: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-app` 미커밋 변경(HEAD 91728737). 1차 리포트 `review-backend-code-report.md` 의 F-1 · W-1~W-4 · R-2 · R-4 해소 확인 + 새 회귀 탐색. `app/**` 읽지 않음.
- 입력: `backend-fix1-report.md` · 실제 `git diff` · 현재 `backend/day/services/environments.py` · `backend/common/config.py` · `deploy/compose.local.yaml` · `deploy/config/{dev,prod}.env`(커밋된 비밀 아닌 일반 설정 — diff 만 봄) · `backend/tests/day/auth/test_environments.py`.
- 코디 확정 사항(브리프): 최대 동시 4 · 대기열 없음 503 · 슬롯 복구는 AGENTS 기술 상한의 기본값(새 업무 정책 아님). compose/config 빈 placeholder 는 승인된 전달 구조. W-5 는 코디 infra 647 PASS 로 종료. R-1(오류 클래스 위치)은 의도적으로 유지.

## 판정: PASS — 차단 없음

1차 FAIL 1 · WARN 4 · 참고 2 가 모두 코드 · 테스트로 해소됐다. 새 회귀는 찾지 못했다. 아래 참고 1건은 차단 아님.

## 직접 실행 (이 재검수에서)

| 명령 | 결과 |
|---|---|
| `uv run pytest -q -m "not infra" backend/tests/day/auth backend/tests/architecture` | **131 passed**, 36 deselected (1차 115 → +16 = 워커 보고와 같음) |
| 셸에 `DAY_DEMO_LOGIN_EMAILS` · `DAY_DEMO_API_BASE` · `DAY_PUBLIC_API_BASE` 를 엉뚱한 값으로 넣고 `test_environments.py` | **87 passed** — 외부 env 에 흔들리지 않음(R-4) |
| `uv run pytest -q -m "not infra" backend/tests/deploy` | **81 passed** — 실제 `deploy/config/dev.env` · `prod.env` 를 읽는 `test_day_vm.py` 가 새 placeholder 줄을 받아들임 |
| `uv run ruff check backend` · `ruff format --check backend` | All checks passed · 158 files already formatted |
| scratchpad probe(네트워크 · DB 없음 — 실제 `auth_router` + `RelayDeps(MockTransport)` + 새 `RelaySlots`) | 아래 표 |

infra · DB · 실 env 읽기 · 서버/컨테이너 조작 · `docker compose config` 는 하지 않음.

## 지적별 확인

| 1차 지적 | 수정 위치 | 확인 방법 · 결과 | 판정 |
|---|---|---|---|
| **F-1** 로컬 manifest 3키 누락 | `deploy/compose.local.yaml:26-29` — `&backend-environment` 에 `DAY_PUBLIC_API_BASE` · `DAY_DEMO_LOGIN_EMAILS` · `DAY_DEMO_API_BASE` 를 `${VAR:-}` 로 | 앵커를 쓰는 곳 확인: `api`(89) · `worker`(115) · `scheduler`(124)는 `<<: *backend` 그대로, `migrate`(78-79)는 `<<: *backend-environment` 로 덮어써도 같이 받음. `postgres` · `redis` 는 자기 `environment` 라 안 받음. 서버 `compose.yaml` 은 `env_file` 그대로(수정 불필요) | PASS |
| **W-1** 깊은 중첩 JSON → 500 | `environments.py:260-263` `except (ValueError, RecursionError)` → `not_json` → 503 | 테스트 `200-deeply-nested` · `4xx-deeply-nested`(402-413행, `[`×30000). probe: 4xx 본문 안 중첩 100 ~ 990 겹(파싱은 되는 깊이)은 실제 라우터에서 **400 + 본문 그대로**(직렬화 단계 500 없음), 64KiB 초과는 503 | PASS |
| **W-2** 동시성 상한 없음 | `environments.py:86-112 · 242-248` — `RelaySlots`(프로세스 하나 · 4 · 대기열 없음), `try_take` 실패 → 바로 503 `result=busy`, `try/finally` 로 반환 | 테스트 587-663행: 4개 진행 중 5번째 503 · dev 요청 4건 · KOS 0 → 풀면 자리 0 / 실패 5종 × (상한+2) 뒤 자리 0 · 이어서 200 / 취소 뒤 자리 0 / 기본 `RelayDeps` 둘이 같은 프로세스 자리. 판별 · 대상 설정 검사 → 자리 → 넘김 순서라 대상 없음(롤백)일 때 자리를 쓰지 않음. probe: 503 · 400 · 500 어느 끝이든 `in_flight == 0` | PASS |
| **W-3** 설정 오류에 원값 | `common/config.py` `SettingsConfigDict(..., hide_input_in_errors=True)` | 테스트 121-126행(userinfo · path · 시간대 · 정수 칸 `str`/`repr` 에 원값 · `user:` 없음). probe: `day_public_api_base` userinfo · `hospital_timezone` · `emr_http_timeout_seconds` · `db_schema` 넷 모두 `str`/`repr` 에 원값 없음 | PASS |
| **W-4** 서버 일반 설정에 이름 없음 | `deploy/config/dev.env:16-21` · `prod.env:17-23` — 세 이름 빈 값 + 주석. 기존 줄 무변경 | 빈 값 = 기존 동작(칸 생략 · 넘김 꺼짐). `scripts/deploy/day_vm.py:45-46` 금지 키 · 접두어에 안 걸리고 `render_env` 빈 값 허용, deploy 테스트 81 통과. prod 주석에 「비우면 정식 앱 로그인 실패」 · 롤백 방법(목록 유지 · 대상만 비움)이 적혀 배포 확인 항목으로 드러남 | PASS |
| **R-2** 임의 dev code 로그 | `environments.py:45-60 · 278-281` — SPEC-001 로그인 단계 코드 11개만 그대로, 그 밖은 `dev_client_error` | 테스트 572-584행(429 `<script>…` → 응답 본문 그대로 · 로그 `dev_client_error`). 응답 본문은 `RelayedError.to_body` 원본 그대로라 SPEC 「4xx HTTP · 본문 그대로」 유지 | PASS |
| **R-4** 셸 env 에 흔들림 | `test_environments.py:39-43` autouse `delenv`(값 읽지 않음) | 위 「엉뚱한 셸 값」 실행 87 passed | PASS |
| W-5 | — | 코디 infra 647 PASS 로 종료(브리프) | 종료 |
| R-1 · R-3 | — | 의도적으로 유지(브리프 · 동작 문제 없음) | 해당 없음 |

## 회귀 확인 (1차 PASS 항목이 그대로인가)

- 판별 위치 · 행 0 · 대상 하나 · redirect 0 · retry 0 · 전체 60초 · 4xx 보존 · 대상/환경 불일치 거절 · 요청 칸/헤더 무시 · 빈 비밀번호 400 · 롤백 503 테스트가 모두 그대로 있고 통과(131). `_relay` 본문(251-282행)은 1차와 같고 자리 처리만 감쌌다.
- 로그 · 비밀: 새 로그 `result=busy` · `dev_client_error` 에 이메일 · 비밀번호 · 토큰 · 주소 없음.
- 라우터 · 스키마 · 웹 경로 · infra 테스트 파일은 이번에 바뀌지 않음(diff stat 상 auth.py · schemas · conftest 줄 수 1차와 같음).
- 새 503 두 경우(동시 상한 초과 · 깊은 중첩)는 SPEC-001 케이스 매트릭스 「dev 넘김 불가 · 모르는 응답 → 503 `environment_unavailable` · prod 우회 없음」 안이다. 새 업무 정책을 더하지 않았다.

## 참고 (차단 아님)

- C-1. httpx 계열이 아닌 예외(예: transport 가 `RuntimeError` 를 던짐)는 여전히 500 이다(probe 확인 — 자리는 0 으로 돌아옴). 실제 `httpx` 기본 transport 는 네트워크 오류를 `httpx.TransportError` 로 바꿔 주므로 현실에서 닿기 어렵고, 1차에서도 지적하지 않은 범위다. 코드 버그성 예외를 503 으로 숨기지 않는 쪽이 오히려 맞을 수 있어 수정 요구하지 않는다.
- C-2. 상한 4 는 uvicorn worker(프로세스)당이다 — 현재 서버는 `--workers 1`(`deploy/compose.yaml`). 늘리면 전체 상한도 배수가 된다(워커 보고 3과 같음).

## 실연동 pending (구현 결함 아님)

- 이번 수정 뒤 infra 포함 전체(`scripts/test.sh -q`) 재실행은 코디 몫 — infra 파일은 안 바뀌었지만 `environments.py` 가 바뀌었다(infra ⑤ 는 기본 `RelayDeps` = 프로세스 자리를 쓴다 — 요청이 차례로라 상한에 닿지 않음).
- 로컬 day-local 에 실제로 3키가 들어가는지(`docker compose config`/기동)는 실행하지 않았다 — yaml 구조로만 확인. 워커가 가짜 env 로 `compose config` 를 돌린 증거(`backend-evidence/fix1-compose-config.txt`)는 인용만 함.
- dev/prod 배포 뒤 실제 데모 넘김 · prod 행 0 실조회 · 실제 env 값은 사용자 · Delivery 범위 밖.
- code · integration 전체 완료를 이 리포트로 선언하지 않는다. mobile 은 검수하지 않았다.

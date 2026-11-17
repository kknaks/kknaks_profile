# kos-signin-limit be-1 결과 보고 (backend)

## 상태: done — 미커밋 · 워크트리 `CENTURION_DAY/kos-signin-limit` (base origin/dev `0c401726`)

## 수행 — 파일

| 파일 | 내용 |
|---|---|
| `backend/day/emr/kos/client.py` | `web_user_agent(tag)` · `KosEndpoints.kos_client_tag`(env `KOS_CLIENT_TAG`) · `.user_agent` · `.active_limit_headers()`(`kos-client-uri = <web>/auth/active-sign-in-limit`) · `is_sign_in_limit(resp)`(401 + `message == SignInLimitExceeded`, 본문 못 읽으면 아님) · 공용 `post_kos` · `list_active_sign_ins` · `revoke_active_sign_in`(4xx → `SignInRevokeRejected`) · `KosClient.internal_token` 시스템 자동 해제(S-8) |
| `backend/day/emr/kos/staff_client.py` | UA 두 곳(로그인 · `KosStaffWriter`) → `endpoints.user_agent` · `sign_in` 기기 제한 → `SignInLimitExceeded` · `sign_in_after_revoke` · `active_sign_ins` · `revoke_sign_in` |
| `backend/day/emr/base.py` | `SignInLimitExceeded(StaffCredentialsRejected)` · `SignInRevokeRejected(EmrError)` · `StaffAuthenticator` 에 비추상 `sign_in_after_revoke` · `active_sign_ins` · `revoke_sign_in`(미지원 = `EmrError` — 조용히 건너뛰지 않음) |
| `backend/day/emr/normalized.py` · `kos/mapper.py` | `NActiveSignIn(external_id, user_agent, ip_address, signed_in_at)` · `mapper.active_sign_in`(id 없으면 뺌) |
| `backend/day/dtos/auth.py` | `DeviceChoice(id, label, ip_address, signed_in_at)` · `PendingDeviceChoice(pending_token, expires_in_seconds, devices, status="choose_device")` · `LoginOutcome` 에 더함 |
| `backend/day/services/auth.py` | `login(..., *, device_choice=True)` · `_after_sign_in`(기존 갈래 추출) · `_device_pending` · `choose_device` · `device_label` · 임시 값 `kind`(`hospital`/`device`) · `choose_hospital` 종류 검사 · `_load`(복호화 실패 = `session_expired`) |
| `backend/day/routers/api/auth.py` | 앱 JSON `login(..., device_choice=False)` |
| `deploy/compose.local.yaml` · `deploy/local.env.example` | `KOS_CLIENT_TAG: ${KOS_CLIENT_TAG:-}` · 예시 `KOS_CLIENT_TAG=local` |
| 테스트 (새로) | `tests/day/emr/test_kos_signin_limit.py`(16) · `tests/day/auth/test_device_choice_rules.py`(25 · DB 없음) · `tests/day/auth/test_device_choice_api.py`(4 · infra) · 고정본 `fixtures/kos_active_sign_ins.json` · `kos_sign_in_limit.json`(값 가짜 · IP 192.0.2.x) · README 두 줄 |
| 테스트 (고침) | `test_kos_client.py` · `test_kos_staff_client.py` — 엔드포인트에 `kos_client_tag=""` 고정(셸 · local.env 의 표시에 기대지 않게) |

frontend 파일(`routers/login.py` · 템플릿 · css · `tests/day/web/*` · `test_screen_copy.py`)은 건드리지 않았다. migration 없음. `common/config.py` 는 안 고침 — 태그는 기존 KOS env 설정(`KosEndpoints`)에 두었다(`common` 은 `day` 를 모름 · KOS 주소 셋과 같은 자리).

## 계약 (be ↔ fe · 스펙 대조)

| 항목 | 구현 | 스펙 |
|---|---|---|
| 설정 | env `KOS_CLIENT_TAG`(비밀 아님) · UA = 웹 UA + ` (<tag>)` · 비면 지금 UA | 같음 (§3 시스템 계정 낱말) |
| UA 적용 범위 | 시스템 계정 · 직원 로그인 · 직원 쓰기 세 곳 | OQ-K2 기본값 = 같음 |
| 판정 | 401 + `message == SignInLimitExceeded` · 그 밖 401/400 지금 그대로 | 공통 1 같음 |
| 시스템(S-8) | 막혔을 때만 · 태그 없으면 경고+실패 · UA 글자까지 같은 것 중 `signedInDateTimeUtc` 가장 오래된 1개(시각 없으면 가장 늦은 것으로) · 해제 4xx = 로그 + 다시 안 함 + 실패 · 다시 sign-in 1회 · 또 막히면 실패 · 목록 5xx = 실패 · 로그 = 병원 id 만 | 시스템 계정 2~7 · OQ-K1 · OQ-K8 ③ 같음 |
| 웹 `login` | `PendingDeviceChoice`(status `choose_device`) · 목록 비면/실패 `kos_unavailable` | U-4 · OQ-K12 같음 |
| `choose_device(session, deps, pending_token, device_id) -> LoginOutcome` | 꺼냄(지움 · 되돌리지 않음) → 종류 · id 검사 → 해제(4xx 여도 계속 · 5xx `kos_unavailable`) → `sign_in_after_revoke` → 다시 막히면 새 `choose_device` · 아니면 `login` 과 같은 갈래 | §3 직원 3~6 · OQ-K8 ① 같음 |
| 만료 · 빈/없는 토큰 · 다른 종류 · 목록 밖/빈 id | `SessionExpired`(`session_expired`) · KOS 안 부름 · 되돌리지 않음 | W-1 · 매트릭스 같음. 빈 토큰은 `invalid_request` 대신 `session_expired`(웹 폼 손댐 = 매트릭스 「없는 토큰」) |
| 기기 선택 토큰 → `choose_hospital` | `session_expired` · 되돌리지 않음(지금 500 막음) · `kind` 없는 옛 값 = 병원 고르기 | §3 직원 2 같음 |
| 비밀번호 | 기기 선택 임시 값 안에만 · 값 통째 `encrypt_value` · Redis 5분 · 꺼내면 지움 · 이어지는 병원 고르기 값엔 없음 · 로그 · 결과 repr 없음 | 「기기 선택 동안 비밀번호」 같음 |
| `label` | `device_label(ua)` — iOS/Android/Windows/macOS/Linux × Edge/Firefox/Chrome/Safari · 못 읽으면 원문 · 환경 표시는 안 보임 | OQ-K6 기본값 같음 |
| 앱 `POST /api/auth/login` | 401 `invalid_credentials`(틀린 비밀번호와 본문까지 같음 — infra 테스트로 비교) · 목록 · 토큰 없음 · 로그 `login blocked by KOS sign-in limit (app)`(이메일 · 비밀번호 없음) | 보충 ④ · OQ-K17 같음 |

## 검증

- `DAY_ENV_FILE=/Users/kknaks/git/CENTURION_DAY/deploy/local.env scripts/test.sh -q backend/tests/day/emr backend/tests/day/auth backend/tests/deploy backend/tests/architecture` → **467 passed**(infra 포함 · `DAY_REQUIRE_INFRA=1` · day_test · Redis db 15 · 컨테이너 안 건드림)
- `uv run pytest -q -m "not infra"`(backend 전체 · KOS_CLIENT_TAG 없는 env) → **1015 passed, 343 deselected**
- `uv run ruff check day tests` → All checks passed
- 새 테스트만: 16 + 25 + 4 = 45 passed. KOS 실호출 없음.

## 앱 영향 판정

- 깔린 앱: 기기 제한이어도 응답이 지금 틀린 비밀번호와 **같다**(401 `invalid_credentials`) → 화면 변화 없음 · `unexpected_response` 없음.
- 데모 넘김(`services/environments.py`): dev 의 `/api/auth/login` 도 앱 라우터라 같은 401 → prod 가 그대로 넘김(`invalid_credentials` 는 `_LOGGED_CLIENT_CODES` 에 있음). 코드 변경 없음.
- `/api/auth/hospital` 에 기기 선택 토큰이 오면 401 `session_expired`(전엔 500 가능).

## 배포 때 서버 env

- `deploy/config/dev.env` 에 `KOS_CLIENT_TAG=dev` · `deploy/config/prod.env` 에 `KOS_CLIENT_TAG=prod`(비밀 아님 · 서버 compose 는 env_file 통째라 compose 수정 불필요). 이 파일들은 allowed_paths 밖이라 **안 넣었다** — 배포 PR 에서(OQ-K15).
- 로컬: 사용자 `deploy/local.env` 에 `KOS_CLIENT_TAG=local` 한 줄(예시엔 넣음).
- 비우면 동작 = 지금과 같음(표시 없음 · 자동 정리 없음).

## 이슈 · 코디가 확인할 것

1. **fe 연결점**: 웹 `POST /login` 은 `auth.login(...)` 그대로(기본 `device_choice=True`) → `isinstance(outcome, PendingDeviceChoice)` 로 조각. `/login/device` 는 `auth.choose_device(...)` → `SessionExpired` 면 `/login?reason=session_expired` · 결과는 `IssuedSession` / `PendingLogin` / `PendingDeviceChoice`. 기존 `routers/login.py:_failed` 에서 `kos_unavailable` 등은 문구표에 이미 있음. 이름은 작업 중 코디 터미널로 알렸으나 주입 확인 응답은 못 받음 — fe 에 전달됐는지 확인 필요.
2. `signed_in_at` 이 None 일 수 있다(KOS 가 시각을 안 주면 지어내지 않음) — 화면이 None 처리 필요.
3. 시스템 자동 해제는 같은 UA 「글자까지」 비교다 — UA 상수(`WEB_USER_AGENT`)를 바꾸는 배포 직후엔 옛 UA 로그인이 대상에서 빠진다(그 뒤 쌓인 것부터 정리). 스펙 의도대로지만 운영 메모.
4. 남는 위험(스펙 §3 시스템 8): 같은 표시 · 같은 계정을 쓰는 클라이언트끼리 서로 끊을 수 있음 — 호출당 해제 1 · 재시도 1 로 묶여 무한 반복 없음.
5. OQ-K11(해제된 KOS 로그인의 토큰을 KOS 가 바로 거절하나)은 실물 확인 몫 — 코드는 기존 S-4 의 2 경로 그대로.

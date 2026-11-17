# kos-signin-limit be-0 조사 결과 (중단 — 스펙 먼저)

## 상태: blocked — 코디 지시(2026-11-17)로 중단: 「스펙 먼저 쓰고 그 뒤 코드」
addendum(`be-1-addendum.md`)은 중단 지시가 바로 뒤따라 와서 **읽지 않았고 반영하지 않았다**.
테스트 · ruff 는 **돌리지 않았다**. 커밋 · push 는 하지 않았다.

## 바꾼 파일 (커밋 안 함 · 워크트리에만)
- `backend/day/emr/kos/client.py` 한 파일만(+151 −9). 반쯤 된 상태 — 아래를 넣었다:
  - `:43-44` `ACTIVE_SIGN_INS_PATH`(`common/user/v1/queries/get-active-sign-ins`) · `REVOKE_SIGN_IN_PATH`(`common/user/v1/commands/revoke-active-sign-in`) · `SIGN_IN_LIMIT = "SignInLimitExceeded"`
  - `:57` `web_user_agent(tag)` — `WEB_USER_AGENT` + ` (<tag>)`, 비면 그대로
  - `:80` `KosEndpoints.kos_client_tag`(env `KOS_CLIENT_TAG`) + `user_agent` 속성
  - `:125` `is_sign_in_limit(resp)` — 401 이고 본문 `message == "SignInLimitExceeded"` · `sign_in_limit_error()`
  - `:166` `list_active_sign_ins(http, base, email, password, headers)` → `ActiveSignIn(id, user_agent)` 목록 · `:192` `revoke_active_sign_in(…, sign_in_id, …)` — 모듈 함수(시스템 · 직원 공용 의도)
  - `internal_headers` UA 를 `self.endpoints.user_agent` 로
  - `internal_token` → `_sign_in()` · 막히면 `:349` `_sign_in_after_revoking_own()`(태그 비면 경고 + 실패 · UA 정확히 같은 세션만 해제 · 해제 0개면 재시도 없이 실패 · 재시도 한 번 · 다시 막히면 실패)
- 손대지 않은 것(계획만): `staff_client.py`(UA 두 곳 · sign_in 분기) · `emr/base.py` 새 예외 · `day/errors.py` 새 오류 · `services/auth.py` · `routers/login.py` 문구 · `services/environments.py` 로그 코드 · `deploy/local.env.example` · `deploy/compose.local.yaml` · 테스트.
- 버릴 거면: `git -C /Users/kknaks/orca/workspaces/CENTURION_DAY/kos-signin-limit checkout backend/day/emr/kos/client.py`

## 코드 사실 (base origin/dev 0c401726 기준 줄 번호)
- `backend/day/emr/kos/client.py:39-42` `WEB_USER_AGENT`(Chrome/150 맥 문자열) · `:154` `internal_headers` 에서 씀 · 헤더는 UA · Origin · `kos-client-uri=<web>/<tenant>/reservation/schedule/`
- `client.py:51-71` `KosEndpoints(BaseSettings)` — env 에서 `KOS_*` 를 읽는 설정 클래스(`factory.py:45` · `:51` · `:85`, `scripts/seed_demo_board.py:853` 가 `KosEndpoints()` 로 만든다) → 태그 설정 자리로 자연스럽다(`common/config.py` 는 `day` 를 모름).
- `client.py:102-112` `_error_of` — `className` 끝 이름만 보고 `message` 는 안 본다 → 기기 제한과 틀린 비밀번호가 같은 `KosError(401 InvalidRequestException)`.
- `client.py:206-238` `internal_token` — `_token_lock` 안에서 sign-in · 2xx 아니면 `_error_of` 로 실패. `:253-271` `call()` 401 이면 `force=True` 로 한 번 다시 sign-in(= 세션 하나 더 생김).
- `staff_client.py:30` `WEB_USER_AGENT` import · `:61` `headers()` · `:165` `KosStaffWriter.send` — UA 두 곳.
- `staff_client.py:88-90` `sign_in` 이 400/401 을 전부 `StaffCredentialsRejected` 로.
- `emr/base.py:150` `StaffCredentialsRejected(EmrError)` · `:171-172` 인터페이스 docstring(거절 → 이 예외).
- `services/auth.py:263-273` `_sign_in` — `StaffCredentialsRejected` → `InvalidCredentials`, 그 밖 `EmrError` → `KosUnavailable`. 새 예외는 `EmrError` 보다 먼저 잡아야 한다.
- `day/errors.py:19-21` `InvalidCredentials` 401 `invalid_credentials`(응답 모양 `detail · code · field`).
- `routers/login.py:41-53` `MESSAGES` · `:58` `INPUT_ERRORS` · `:59-60` 모르는 코드면 `kos_unavailable` 문구로 대체 → 새 코드는 `MESSAGES` 에 넣어야 화면 글자가 나온다.
- `services/environments.py:46-60` `_LOGGED_CLIENT_CODES` · `:280` — 데모 넘김(prod→dev) 로그. 목록 밖 코드는 `dev_client_error` 로 찍힘(응답은 그대로 넘김).
- 앱: `app/lib/core/copy.dart:51` `loginMessage(code) => loginMessages[code] ?? codeOnly(code)` → 모르는 코드는 **코드 문자열 그대로** 빨간 배너(`ui/login_screen.dart:84` · `:100`). `data/day_api.dart:19` `isSessionEnd` 는 401 + `unauthorized`/`session_expired` 만 → 새 코드를 401 로 줘도 세션 종료로 처리되지 않음. 즉 앱 수정 없이 「kos_sign_in_limit」 글자가 보인다(안내 글자는 안 나옴).
- deploy: `deploy/compose.local.yaml:14-23` 은 env 를 이름별로 나열 → `KOS_CLIENT_TAG: ${KOS_CLIENT_TAG:-}` 줄 필요. `deploy/compose.yaml:22-25` 은 `env_file`(`config/<env>.env` + `app.env`) 통째 → compose 수정 불필요, 서버 값은 `deploy/config/dev.env`·`prod.env` 에 `KOS_CLIENT_TAG=dev`/`prod`(비밀 아님 · 브리프 allowed_paths 밖이라 코디 결정 필요).
- 테스트 기존: `tests/day/emr/test_kos_client.py:21` · `:130` · `:164`, `tests/day/emr/test_kos_staff_client.py:25` · `:72` 가 `WEB_USER_AGENT` 와 UA 를 같다고 비교 → 태그를 env 로 두면 개발자 셸에 `KOS_CLIENT_TAG` 가 있을 때 깨질 수 있다(테스트에서 태그를 명시하거나 env 를 지워야). `tests/day/emr/test_kos_staff_client.py:126-135` 틀린 비밀번호 → `StaffCredentialsRejected`. `tests/deploy/test_deploy_contract.py:236-256` 은 `local.env.example` 의 KOS 주소 칸만 본다(태그 칸 추가는 무관).

## 스펙에서 정할 것
- 새 오류 HTTP 상태(401 그대로?) · 코드 이름(`kos_sign_in_limit`?)
- 해제 대상이 0개일 때 재시도 여부(지금 구현: 재시도 안 함)
- 같은 환경 안 api · worker 가 같은 시스템 계정을 쓰면 서로의 세션을 해제할 수 있다 → 상대는 401 → 재-sign-in(세션 1개 새로 생김). 왕복 가능성 확인.
- 목록 · 해제 요청의 `kos-client-uri` 값(KOS 웹 실물 HAR 미확인 — 지금 구현은 시스템 내부 헤더 그대로).
- `deploy/config/<env>.env` 수정 허용 여부.

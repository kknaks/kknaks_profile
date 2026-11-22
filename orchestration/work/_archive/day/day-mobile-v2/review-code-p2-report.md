# 코드 검수 — backend P2 (커밋 `e96b0718`)

**판정: PASS. FAIL 없음, WARN 4건(모두 막지 않음)**

대상: 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-mobile-v2`, 커밋 `e96b0718`. git 은 읽기만 했고 고치거나 커밋하지 않았다.
기준: SPEC-001 개정 ⑩(OQ-K18 ~ K20), SPEC-002 개정 ㉕(OQ-77 · 78), 지시서 `be-p2-instructions.md`, 워커 리포트 `be-p2-report.md`.

## 실행 (1회씩)

- `scripts/test.sh -q backend/tests/day/auth backend/tests/day/board/test_board_api_quick_start.py backend/tests/day/board/test_board_app_fields.py backend/tests/day/web/test_board_feedback.py` 실행 결과 **208 passed**(격리 인프라).
- `ruff check backend scripts` 결과 All checks passed. `ruff format --check backend` 결과 420 files already formatted.
- 웹 라우트(`routers/board.py` · `routers/login.py`), templates, static 은 이 커밋의 diff 에 없다(`git show e96b0718 --stat` 으로 확인).

## 1. 앱 `choose_device` · `POST /api/auth/device` · 데모 넘김 — PASS

| 케이스(스펙) | 구현 | 시험 |
|---|---|---|
| 앱 로그인이 기기 제한이면 200 `choose_device` + `environment`/`api_base_url`(⑩ ① · 표 :299) | `backend/day/routers/api/auth.py:120-124` `device_choice=app` → `_answer` :253-260 | `tests/day/auth/test_device_choice_api.py:123` |
| JSON `client=web` 은 401 `invalid_credentials` 그대로 | `auth.py:122-123` · `services/auth.py:252-257` | `test_device_choice_api.py:95` · `test_device_choice_rules.py:172` |
| 제출 뒤 같은 갈래(`signed_in` · `choose_hospital` · 다시 막힘) | `auth.py:317-330` → `auth.choose_device` → `_answer` | `:123` · `:169` · `:153`(새 토큰 · 새 목록) |
| 만료 · 없음 · 이미 쓰임 | service 공용 | `test_device_choice_rules.py:262` · `test_device_choice_api.py:312`(실제 Redis 1회) |
| 목록 밖 · 빈 `device_id` = 401 `session_expired`, 토큰 되돌리지 않음, KOS 안 부름 | `ExternalSignInId` = NewType str(제약 없음)이라 빈 값도 service 까지 가서 401 | `test_device_choice_api.py:211` · `test_device_choice_rules.py:249` |
| 다른 단계 토큰(양방향) | service | `test_device_choice_api.py:227` |
| 모르는 칸 · 빠진 칸 · 형식 = 400 `invalid_request`(:437) | `auth.py:298-309` + `FROZEN_FORBID_CONFIG` | `test_device_choice_api.py:197` |
| 데모 넘김이 `choose_device` 를 받는다(규칙 9 · OQ-K7) · 대상 어긋남 · 빈 목록 · 모양 틀림이면 503 | `adapters/environments.py:176-181, 228-240` | `tests/day/auth/test_environments_device.py:39, 60` |
| 비밀번호가 응답 · 로그 · URL 에 없음(OQ-K3) | 비밀번호는 Redis 암호문에만 들어간다. `pending_token` 은 POST 본문으로만 오가고 URL 에 실리지 않는다. 검증 실패는 `from None` 으로 입력값을 버린다. `RelayedChooseDeviceData.pending_token` 은 `repr=False`(`dtos/environments.py:44`). 바뀐 로그 줄(`services/auth.py:254-256`)에 이메일 · 비밀번호가 없다 | 응답: `test_device_choice_api.py:136` · `test_environments_device.py:47`. 로그: `test_device_choice_rules.py:142, 172`(caplog) |

**WARN-1 (낮음)** — 위 표의 만료 · 로그 누출 · `kos_unavailable` 은 **service 시험으로만** 확인한다. 앱 JSON 경로(`/api/auth/device`)에서 TTL 만료, caplog 누출, KOS 503 을 끝에서 끝까지 확인하는 시험은 없다. 같은 service 를 그대로 부르므로 결함은 아니다. 다만 매트릭스 행마다 API 시험을 두는 것이 원칙이면 추가할 곳이다.

**WARN-2 (낮음 · 질문)** — `backend/day/routers/api/auth.py:328-330` `/api/auth/device` 가 `client=web` 도 받는다(`schemas/auth.py:466` 기본 app · web 허용). 이때 쿠키 세션을 발급하고, 다시 막히면 web JSON 클라이언트에 `choose_device` 를 준다. 같은 web JSON 이 `/api/auth/login` 에서는 기기 선택 대신 401 을 받으므로 갈래가 비대칭이다. 스펙 :299 의 제출 예는 `client: "app"` 이고 web 금지 문장은 없다. 웹 화면은 `/login/device` 를 쓰므로 실사용 영향은 없다. 그대로 둘지 `client=web` 이면 400 을 줄지는 코디가 판단할 일이다.

## 2. quick-start JSON · `can*` 3칸 — PASS

- 응답 모양: `backend/day/routers/api/board.py:287-302` 가 웹과 같은 `board.quick_start`(`services/board_quick_start.py:37`)를 부르고 `result.body` 를 그대로 `QuickStartResponse` 로 낸다. 일부 거절은 200 + 보낸 순서의 `rejected`(`board_quick_start.py:95`). 전부 거절은 409 + 첫 코드(:96-97)로, OQ-77 기본값과 같다. 400 · 404 · `visit_home` 순서도 스펙 :599 와 같다. 시험: `tests/day/board/test_board_api_quick_start.py:23, 47, 58, 72`.
- 권한: `_allowed(... BOARD_KEY, EDIT)` + `writable_session` 으로 웹과 같다.
- `can*` 판정: `backend/day/presentation/board.py:171-174`
  - `canCancelCall = cancel_call_block(v,t) is None` 은 `services/board_calls.py:317` `_check(rules.cancel_call_block)` 와 같은 함수다.
  - `canQuickStart = not is_home(v) and quick_start_block(t) is None` 은 `board_quick_start.py:68-76`(묶음 `is_home` → 줄 `quick_start_block`)과 같다.
  - `canChangeDoctor = doctor_change_block(v,t) is None` 은 `services/board_tasks.py:316` 과 같다.
  - 시험: `tests/day/board/test_board_app_fields.py:51`(상태별), `:63`(칸 = 거절 규칙 · 귀가 대기 포함), `:74`, `:81`(JSON 직렬화).
- 웹 템플릿과의 차이(㉕ ③ ⓐ ~ ⓒ)는 템플릿을 건드리지 않은 채 그대로 남아 있다. 스펙 ③ 이 허용한 방향이다.
- 참고(결함 아님): service 의 줄별 `conflict`(시스템 계정 KOS id 를 못 구함, `board_quick_start.py:93`)는 `canQuickStart` 에 반영되지 않는다. DB 를 조회해야 알 수 있는 동적 거절이고, 스펙 ③ 은 판정을 「`:655-665` 줄 판정 + 귀가 대기 아님」으로 정했으므로 맞다. 앱은 200 `rejected` 의 `conflict` 로 받는다.

**WARN-3 (스펙 문서 · 코드 아님)** — SPEC-002 :672 스냅샷 주석은 `canChangeDoctor` 를 「accepted · doing · **담당 원장 또는 systemDoctor**」로 적었다. 반면 개정 ㉕ ③ ⓐ와 OQ-78 은 `doctor_change_block` 만 보라고 하고, 담당 원장 · 시스템 계정이 둘 다 없는 줄도 앱은 true 라고 적었다. 같은 문서 안에서 말이 다르다. 구현은 ③/OQ-78 을 따랐으므로 맞다. 스펙 쪽 :672 문장을 고쳐야 한다.

**WARN-4 (낮음 · 시험 공백)** — 「호출 줄이지만 같은 호출이 다른 줄로 이미 수락됨 → `canCancelCall=false`」(`board_rules.py:651` 의 두 번째 조건)를 직접 고정한 사례 시험이 없다. `test_board_app_fields.py:63` 은 함수끼리 같은지만 확인한다.

## 3. 웹 동작 무변경 — PASS

`tests/day/web/test_board_feedback.py:200-211` 에서 바뀐 것은 monkeypatch 한 가짜 `quick_start` 가 돌려주는 `body` 하나다. 원래 `{}` 였는데 `BoardQuickStartState` 의 본문 타입이 `QuickStartResponseData` 로 좁혀지면서(`dtos/board_actions.py:32`) mypy 를 통과하도록 모양을 맞췄다.
- 기대값(assert) 줄 :219-227 은 바뀌지 않았다. status, `X-Day-Version`, OOB, 토스트 2장 순서, 400 모두 그대로다.
- 웹 라우트 `routers/board.py:611-630` 은 `result.rejected` · `visit_id` 만 쓰고 `result.body` 를 그리지 않는다. 바뀐 가짜 값은 웹 출력에 닿지 않는다.
- 결론: 기대값을 바꿔 웹 동작 변화를 덮은 것이 아니다.

## 4. 구현 선택 2개 — PASS

- **`exclude_if` 로 `exclude_none` 대체**: `exclude_if=_omitted` 는 `SignedIn` · `ChooseHospital` · `ChooseDevice` 의 앱 전용 칸 `token` · `environment` · `api_base_url` 에만 붙었다(`schemas/auth.py:130-244`). 이 세 모델은 `routers/api/auth.py` 밖에서 쓰지 않는다(grep 확인. `adapters/environments.py` 는 별도 `_Dev*` 모델을 쓴다). 라우트에서 `exclude_none` 이 빠진 `/login` · `/hospital` 의 나머지 칸은 모두 필수(non-None)다. `HospitalOut` 도 id · name 뿐이라 이전 응답과 모양이 같다. `/me`(`MeOut`)는 원래 `exclude_none` 이 없었고 이번에 바뀌지 않았다. 설치된 pydantic 2.14.2(uv.lock :931)는 `exclude_if` 를 지원한다. `devices[].signed_in_at: null` 이 보존되는 것은 `test_device_choice_api.py:133` 으로 확인된다.
- **`device_id` JSON 별칭**: `DeviceRequest.sign_in_id = Field(alias="device_id")`(`schemas/auth.py:91-95`). `FROZEN_FORBID_CONFIG` 에 `validate_by_name` · `populate_by_name` 이 없어(`common/schema_config.py:6`) 받는 바깥 이름은 `device_id` 하나뿐이다. `sign_in_id` 로 보내면 extra 로 400 이 난다. 이 모델은 요청 전용이라 응답 모양에는 영향이 없다.
- 참고: `/device` 는 FastAPI 본문 파라미터 대신 수동 파싱(`_device_body`)을 쓴다. 그래서 OpenAPI 에 요청 본문 스키마가 나오지 않는다. 기존 `api/board.py:69` `_parse` 와 같은 패턴이다. `_device_body`(`auth.py:298-309`)는 그 `_parse` 의 세 번째 사본(board · chat · auth)이다. 이 작업 범위에서 고칠 것은 아니다.

## 범위 밖 확인

- 호출 취소 알림(SPEC-002 ㉕ 머리말 · DAY-SPEC-005 M-6)은 P2 지시에 없고 구현되지 않았다. 워커 리포트 이슈 4 와 같다. P3 몫인지 코디가 확인해야 한다.
- 실물 KOS 1회는 pending 이다(워커 리포트 사유 그대로).

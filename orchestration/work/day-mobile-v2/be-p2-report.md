# day-mobile-v2 P2 결과 보고 — 앱 기기 선택 JSON · 바로 시작 JSON · 스냅샷 can* 3칸

## 상태: done (실물 KOS 1회만 pending — 사유 아래)

워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-mobile-v2` · P1 커밋 `a7868dc6` 위. 커밋 · push · PR 없음. `app/` · P1 파일(`services/interpret` 등) · 웹 라우트 · 템플릿 · static · migration 손대지 않음.

## 새 경로 · 바뀐 응답

| 경로 | 무엇 | 근거 |
|---|---|---|
| `POST /api/auth/login` (`client=app`) | KOS 기기 제한이면 **200 `choose_device`**(웹과 같은 service `auth.login(device_choice=True)`). `client=web` JSON 은 그대로 401 `invalid_credentials` | SPEC-001 개정 ⑩ ① · 케이스 매트릭스 |
| `POST /api/auth/device` (새) | 기기 선택 제출 → `auth.choose_device`(웹 `/login/device` 와 같은 service) → 로그인과 같은 갈래 `signed_in` · `choose_hospital` · 다시 막히면 새 `choose_device` | 개정 ⑩ · OQ-K18 기본값 |
| 데모 넘김(prod → dev) | `adapters/environments.py` `read_success` 가 dev 의 `choose_device` 를 받아 그대로 넘김(대상 = dev · 대상 어긋남 · 빈 목록 · 모양 틀림 = 503 `environment_unavailable`) | 「앱 환경 연결」 규칙 9 · OQ-K7 |
| `POST /api/visits/{visit_id}/quick-start` (새) | 바로 시작 앱 JSON — 웹과 같은 service `board.quick_start` | SPEC-002 개정 ㉕ ① · OQ-77 기본값 |
| `GET /api/board` · SSE 스냅샷 `cards[].tasks[]` | 새 칸 `canCancelCall` · `canQuickStart` · `canChangeDoctor` | 개정 ㉕ ③ · OQ-78 |

### 요청 · 응답 예시(값은 가짜)

```jsonc
// POST /api/auth/login {"email":"<email>","password":"<pw>","client":"app"} — 기기 제한
200 {"status":"choose_device","pending_token":"<pending>","expires_in_seconds":300,
     "devices":[{"id":"kos-1","label":"macOS Chrome","ip_address":"192.0.2.1","signed_in_at":"2026-01-01T00:00:00Z"},
                {"id":"kos-2","label":"iOS Safari","ip_address":"192.0.2.2","signed_in_at":null}],
     "environment":"dev","api_base_url":"https://dev-day.example.test"}   // 연결 대상 2칸은 설정에 값이 있을 때만(지금과 같은 규칙)

// POST /api/auth/device {"pending_token":"<pending>","device_id":"kos-1","client":"app"}
200 {"status":"signed_in","expires_at":"…","csrf_token":"…","token":"<session>","environment":"dev","api_base_url":"…"}
200 {"status":"choose_hospital","pending_token":"<new>","expires_in_seconds":300,"hospitals":[…],"environment":…}
200 {"status":"choose_device", …새 pending_token · 새 목록…}   // 해제 뒤 다시 막힘

// POST /api/visits/{visitId}/quick-start {"taskIds":["<t2>","<t1>","<t3>"]}
200 {"startedTaskIds":["<t1>","<t3>"],"rejected":[{"taskId":"<t2>","code":"call_not_accepted"}],"flowStepChanged":true}
409 {"detail":"…","code":"call_not_accepted","field":null}   // 전부 거절 — 보낸 순서 첫 거절 코드(OQ-77 기본값)

// GET /api/board — cards[].tasks[] 새 칸
{"…": "…", "canCancelCall": true, "canQuickStart": false, "canChangeDoctor": false}
```

### 오류 코드 표

| 경로 | 경우 | HTTP | code |
|---|---|---|---|
| `/api/auth/device` | 본문 JSON 아님 · 모르는 칸 · `pending_token`/`device_id` 빠짐 · 형식 틀림 | 400 | `invalid_request` |
| `/api/auth/device` | 임시 토큰 만료 · 이미 쓰임 · 없음 · 다른 단계(병원 고르기) 토큰 · 목록 밖 · 빈 `device_id` | 401 | `session_expired`(토큰 되돌리지 않음 · 목록 밖이면 KOS 안 부름) |
| `/api/auth/hospital` | 기기 선택 토큰이 옴 | 401 | `session_expired` |
| `/api/auth/device` | 해제 · 다시 sign-in 중 KOS 장애 | 503 | `kos_unavailable` |
| `/api/auth/device` | 다시 sign-in 비밀번호 틀림 · 계정 막힘 · 연결 병원 없음 등 | 로그인과 같음 | `invalid_credentials` · `account_inactive` · `no_connected_hospital` … |
| `/api/auth/login`(데모) | dev `choose_device` 의 대상 · 환경 어긋남 · 빈 목록 · 모양 틀림 | 503 | `environment_unavailable` |
| `/api/visits/{id}/quick-start` | 빈 · 겹친 `taskIds` · 모르는 칸 | 400 | `invalid_request` |
| 〃 | 카드 없음 · 그 카드 줄 아님 | 404 | `not_found` |
| 〃 | 귀가 대기 카드(묶음 전체 · 줄 판정 전) | 409 | `visit_home` |
| 〃 | 전부 거절 | 409 | 첫 거절 코드(`call_not_accepted` · `task_not_waiting` · `conflict`) |
| 〃 | 권한 없음 · 세션 | 403 · 401 | `forbidden` · `unauthorized` · `session_expired`(기존 그대로) |

### 새 칸 판정(OQ-78 — 서비스 거절 규칙 그대로)

- `canCancelCall` = `cancel_call_block(v, t) is None`(귀가 대기 아님 · 호출(수락 전) 줄 · 그 호출이 수락되지 않음)
- `canQuickStart` = 귀가 대기 아님 ∧ `quick_start_block(t) is None`(준비중)
- `canChangeDoctor` = `doctor_change_block(v, t) is None`(귀가 대기 아님 · 수락 · 진행중)
- 셋 다 권한은 보지 않음(canStart 와 같음). 웹 템플릿은 바꾸지 않음(개정 ㉕ ③ ⓐ ~ ⓒ 차이 그대로).

## 바꾼 파일

- `backend/day/routers/api/auth.py` — 앱 `device_choice=True` · `/device` · 공통 갈래 `_answer` · 데모 `choose_device` 넘김 · 라우트 `response_model_exclude_none` 를 칸별 `exclude_if` 로(아래 주의 1)
- `backend/day/schemas/auth.py` — `DeviceRequest`(바깥 이름 `device_id` · 안 이름 `sign_in_id: ExternalSignInId` — 주의 2) · `DeviceOut` · `ChooseDevice` · 앱 전용 칸 `token`/`environment`/`api_base_url` 에 `exclude_if`
- `backend/day/adapters/environments.py` — `read_success` `choose_device` 받기(`_DevChooseDevice`)
- `backend/day/dtos/environments.py` — `RelayedChooseDeviceData`
- `backend/day/dtos/auth.py` · `backend/day/services/auth.py` — 문서 · 로그 글자만(로직 무변경 — service 는 이미 있었음)
- `backend/day/routers/api/board.py` — `POST /visits/{visit_id}/quick-start`
- `backend/day/schemas/board.py` — `QuickStartBody`
- `backend/day/schemas/responses.py` · `backend/day/dtos/responses.py`(생성기 `scripts.devtools.contracts --write`) — `QuickStartResponse` · `QuickStartRejectedView`
- `backend/day/schemas/board_responses.py` · `backend/day/dtos/board_views.py`(생성) — `TaskView` 새 칸 3
- `backend/day/presentation/board.py` — `task_view` 새 칸 3
- `backend/day/dtos/board_actions.py` — `BoardQuickStartState` 본문 타입 = `QuickStartResponseData`
- 테스트: `tests/day/auth/test_device_choice_api.py`(앱 401 시험 → 앱 `choose_device` 흐름 7건 · `client=web` 401 은 남김) · `test_device_choice_rules.py`(로그 글자) · 새 `test_environments_device.py`(데모 넘김 6건) · 새 `tests/day/board/test_board_app_fields.py`(DB 없이 4건) · 새 `test_board_api_quick_start.py`(끝에서 끝까지 5건) · `tests/day/web/test_board_feedback.py`(가짜 상태의 빈 본문을 모양 맞춘 본문으로 — 웹 기대값 그대로)

## 검증 — 명령과 수치

- `scripts/test.sh -q backend/tests/day/auth backend/tests/day/board backend/tests/day/web` — **524 passed**(격리 인프라)
- `scripts/test.sh -q`(전체 · 격리 인프라) — **2015 passed**(P1 뒤 1985 + 새 30)
- **웹 동작 무변경**: 웹 로그인(`test_web_login.py` · 웹 `/login/device` service 시험) · 웹 바로 시작(`tests/day/web/test_board_feedback.py`) 기존 기대값 그대로 통과 · 웹 라우트 · 템플릿 diff 0
- ruff · format · strict mypy(434) · 구조 검사 · Taut audit/check 통과. `./scripts/check.sh --static` 마지막 frontend 단계만 실패 — 워크트리에 npm 모듈 없음(P1 과 같음 · 프론트 무변경)

## 실물 1회 — pending

실제 KOS 데모 테넌트로 앱 로그인 JSON 을 보내려면 로컬에 마이그레이션된 DB + 데모 테넌트 병원 연결 + 사용자 포트가 아닌 api 를 띄워야 하는데, `day-local`(사용자 포트) 은 금지이고 격리 테스트 인프라는 pytest 안에서만 뜬다. 또 `deploy/local.env` 의 KOS 자격은 **시스템 계정** 하나라, 그것으로 로그인하면 동기화가 쓰는 계정의 KOS 동시 로그인 자리를 하나 더 쓴다(K-2 자동 해제 대상과 섞임). 그래서 실물은 하지 않았다. 대신 브리프의 「목으로」 갈래: 실제 FastAPI 앱 + 실제 PostgreSQL · Redis + 가짜 KOS 경계로 `login(app) → choose_device → /api/auth/device → signed_in → /api/auth/me` 끝에서 끝까지(`test_앱_막힘은_200_choose_device_…`)를 돌렸다. 실물은 직원 계정 · 띄울 포트를 코디가 정해 주면 1회 가능.

## 계약 대조 · 스펙과 다른 곳

- SPEC-001 개정 ⑩ 응답 칸 · 오류 줄 · 규칙 9 · OQ-K18 기본값: 같음.
- SPEC-002 개정 ㉕ ① · ③ · OQ-77 · OQ-78 기본값: 같음.
- 스펙과 어긋난 곳: 없음. 아래는 구현 선택(계약 모양은 스펙 그대로):

## 이슈 · 코디가 확인할 것

1. **`signed_in_at: null` 보존** — 로그인 라우트는 앱 전용 칸을 빼려고 `response_model_exclude_none` 을 썼는데, 그대로면 `devices[].signed_in_at` 의 null 도 칸째 사라진다. 라우트 전체 대신 **칸별 `exclude_if`**(`token` · `environment` · `api_base_url` — 값 없으면 칸 없음)로 옮겼다. 기존 `signed_in` · `choose_hospital` 응답 모양은 같음(기존 시험 그대로 통과).
2. **`device_id` 이름** — 식별자 검사(`scripts/devtools/identifiers.py`)가 `device_id` 칸을 푸시 기기 `DeviceId`(UUID)로 강제한다. 값은 KOS 로그인 id 라 안 이름을 `sign_in_id: ExternalSignInId` 로 두고 **바깥(JSON) 이름은 `device_id`(alias)** — 앱 계약은 스펙 그대로.
3. 바로 시작 응답 스키마를 `schemas/responses.py` 에 둠 — `board_responses.py` 에 두면 700줄을 넘고, 그 파일에서 생성되는 `dtos/board_views.py` 매핑이 `scripts/` 에 있어 나눌 수 없었다.
4. 호출 취소 뒤 알림(DAY-SPEC-005 개정 · M-6)은 이번 범위 밖 — `services/board_calls.py` 「알림 없음」 그대로(P3 몫으로 보임).
5. 워크트리의 `app/` 변경은 mobile 워커 것 — 손대지 않음.

# be-1 결과 보고 — 앱 차트 · 사진 `/api` JSON 짝 6 (Delivery #281)

## 계약 차이 (이름 제안 OQ-99 · OQ-100 대비)

- **없음** — C2 · C3 이름 · 모양을 제안대로 확정했다.
  - OQ-99: 탭 저장 200 = `{saved, lastSavedAt, tasks}` · `tasks[]` = 그 방문 줄 전부 + **요청한 종류 칸 하나만**(`{id, title, assignee}` 또는 `{id, title, doctor}`) · 409 걸린 줄 = **`details.conflicts`**(최상위 아님) · 사진 `title` = 서버 TITLES(「시술 전」 · 「시술 후」).
  - OQ-100: PhotoError(413 `photo_too_large` · 400 `photo_type` · 409/503 `photo_disabled` · 400 `invalid_request`)는 **/api 공용 모양 `{detail, code, field}`** 로 나간다(기존 `photo_error_handler` 가 `is_api` 를 보고 JSON 을 돌려준다 — 새 코드 없음).
- 참고(계약 차이 아님 · 기존 /api 공통 동작): 토큰이 **아예 없으면** 401 `unauthorized`, 세션이 만료됐거나 직원 KOS 토큰이 없으면 401 `session_expired`. C0 의 「401 `session_expired`」는 뒤쪽 경우에 해당한다. 앱은 두 코드를 모두 401 로 다루면 된다.

## 상태: done

## 수행 — 파일

| 파일 | 내용 |
|---|---|
| `backend/day/routers/api/board.py` | `POST /api/visits/{id}/chart` 추가(GET 과 같은 파일). `board.save_chart_tab` 을 그대로 부른다. conflict 이면 `ChartConflict({"conflicts": …})` 로 409. 머리 주석 정리(「JSON 짝 없음(W8)」 → 개정 ㉚). 끝에 사진 라우터 `include_router` |
| `backend/day/routers/api/board_photos.py`(새) | 사진 다섯. 웹과 같은 service 를 부른다(`open_tab` · `request_import` · `wait_imported` · `list_photos` · `upload` · `delete` · `retry` · `open_file`). multipart 본문 상한 · 사진 id 처리는 웹 `routers/board_photos.py` 의 `_form` · `_photo_id` · `FILE_HEADERS` 를 **import 해서 다시 쓴다**(복사하지 않았다 · 웹 파일은 손대지 않음 · `BODY_MAX_BYTES` 하나로 같이 움직인다) |
| `backend/day/schemas/board.py` | 요청 `ChartTabBody{chart, rows}` · `ChartRowBody{taskId, body, staffId, baseLogId, baseBody, baseDoctorStaffId}`(extra=forbid · 칸은 모두 필수 · uuid 칸은 `null` 허용 · 글 칸은 문자열) |
| `backend/day/schemas/board_charts.py`(새) | `ChartTabSaveResponse` · `ChartTabTaskView`(기존 `ChartCellResponse` 재사용) |
| `backend/day/schemas/photos.py`(새) | `PhotoListResponse` · `PhotoActionResponse`(+`kosError`) · `PhotoUploadResponse`(+`kosError` · `rejected`) · `PhotoGroupView` · `PhotoItemView` |
| `backend/day/dtos/photos.py` | `PhotoListViewData` · `PhotoGroupViewData`(TypedDict · id 는 `VisitId` · `PhotoItemData` 그대로. 문자열 변환은 schema 가 한다 — identifier 규칙) |
| `backend/day/presentation/photos.py` | `photos_json()` — 웹 `photos_view` 와 같은 묶음 · 순서 · 제목. `edit` 칸 없음 |
| `backend/day/presentation/board_chart_reads.py` | `chart_conflicts_json()` — 409 `details.conflicts` 항목 |
| `deploy/caddy/Caddyfile` | `@photo_upload` · `@other_body` 두 matcher 의 path 에 `/api/visits/*/photos` 를 더했다 → 100MiB. 다른 경로는 6MiB 그대로이고, 두 matcher 는 여전히 겹치지 않는다 |
| `backend/tests/day/board/test_board_api_chart_photos.py`(새) | 계약 테스트 20개 함수(parametrize 포함 28 케이스) |
| `backend/tests/day/board/test_board_chart_api.py` | `test_A5`: 「api 에 `/chart` POST 없음(W8)」 → 「`/api/visits/{visit_id}/chart` 하나만 · 옛 `/api/tasks/{id}/chart` 없음」(개정 ㉚ 반영) |
| `backend/tests/deploy/test_deploy_contract.py` | Caddy 정규식을 경로 두 개로 |
| `backend/tests/architecture/test_api_contracts.py` | 예시 검사 대상에 `board_charts` · `photos` 추가 |

migration 없음 · 새 업무 규칙 없음 · 웹 라우트 · 템플릿 · static 변경 없음 · `app/` 변경 없음.

## 경로 표

| 메서드 | 경로 | 권한 | 응답 200 | 오류(공용 `{detail, code, field}`) |
|---|---|---|---|---|
| POST | `/api/visits/{visit_id}/chart` | `board` edit | `{saved: [taskId], lastSavedAt, tasks: [{id, title, assignee\|doctor: {body, staffId, author, savedAt, logId, base}}]}` | 400 `invalid_request`(모르는 칸 · 칸 생략 · 타입 · 0줄 · 같은 줄 두 번 · chart 값) · 401 · 403 `forbidden` · 404 `not_found` · 409 `chart_conflict` + `details.conflicts: [{taskId, body, staffId, base{body, doctorStaffId}, baseLogId}]` · 409 `chart_staff_required`(staffId null) · `staff_not_listed` · `doctor_not_listed` |
| GET | `/api/visits/{visit_id}/photos?poll=&tick=` | `board` view | `{visitId, reread, groups: [{category, title, items: [{photoId, shotAt, kosSynced}]}]}` | 401 · 403 · 404 |
| POST | `/api/visits/{visit_id}/photos` (multipart `category` + `file`×N) | `board` edit | 목록 모양 + `kosError` + `rejected: [code]` | 400 `invalid_request` · `photo_type` · 413 `photo_too_large`(본문 100MiB 초과 · 전부 걸린 경우) · 409/503 `photo_disabled` · 401 `session_expired`(직원 KOS 토큰 없음) · 403 · 404 |
| POST | `/api/visits/{visit_id}/photos/{photo_id}/delete` | `board` edit | 목록 모양 + `kosError` | 401 · 403 · 404 |
| POST | `/api/visits/{visit_id}/photos/{photo_id}/kos-retry` | `board` edit | 목록 모양 + `kosError` | 409/503 `photo_disabled` · 401 · 403 · 404 |
| GET | `/api/visits/{visit_id}/photos/{photo_id}/file` | `board` view | 바이트(image/jpeg · png) · `Cache-Control: no-store` · `Content-Disposition: inline` · `X-Content-Type-Options: nosniff` | 401 · 403 · 404 · 409 `photo_disabled` |

- 인증 = /api 공통이다. Bearer 이면 CSRF 를 보지 않는다. 쿠키 세션도 받으며, 쿠키로 쓰는 요청은 `X-CSRF-Token` 이 필요하다(없으면 403 — 테스트로 확인). 웹 사진 GET 둘의 쿠키 전용(`required_web_view`)은 그대로다. 웹 파일 경로에 Bearer 로 요청하면 200 이 아니다(테스트).
- `is_admin` 은 `sessions.require_permission` 을 그대로 쓰므로 전부 통과한다.
- 옛 `POST /api/tasks/{task_id}/chart` 는 없다. `/tasks/{id}/{action}` 이 받아 400 `invalid_request` 를 돌려주고 저장은 0건이다(테스트 두 곳).

## 검증

- 새 테스트 + 관련 회귀(차트 api · 충돌 · 사진 · 사진 가져오기 · loop3 · 웹 차트/사진 화면 · 권한 · architecture · deploy): **479 passed**
- `./scripts/test.sh -q`(격리 PostgreSQL · Redis · 전체): **2902 passed**(실패 0)
- `./scripts/test.sh --pure -q`: **2204 passed**, 698 deselected
- `./scripts/check.sh`: structure · ruff · format · strict mypy · **taut-audit · taut-check 통과**. 이어지는 `frontend` 단계는 **이 워크트리에 `scripts/frontend` npm 의존(`@tailwindcss/postcss`)이 설치되어 있지 않아** 실행되지 못했다(환경 문제 · 내 변경과 무관 · 프론트 파일은 건드리지 않음) → **pending**. 코디가 `./scripts/setup-local.sh` 로 npm 을 설치한 뒤 다시 돌려야 한다.
- 도중에 Taut 가 잡은 두 건은 고쳤다 — ① 응답 모델 mapper 이름 `from_internal` ② 테스트에서 `app_client.post` 직접 호출 → `board.client` 경유로.
- 실행하지 못한 것: A4(로컬 BE + KOS 데모 지점 실물 호출). 브리프 §7 에 따라 코디 몫이다.

## 계약 대조

| 항목 | 결과 |
|---|---|
| C0 인증 · 권한 · 같은 service · 오류 모양 · 코드 | 같음(위 「계약 차이」 참고의 401 `unauthorized` 는 기존 동작) |
| C1 차트 GET | 바꾸지 않음 |
| C2 요청 · null 규칙 · extra=forbid · `staffId=null` → 409 · 200 모양 · 409 `details.conflicts` | 같음 |
| C3 ① ~ ⑤ 경로 · 권한 · 모양 · 머리 · 100MiB | 같음 |
| 집도의 변경 → 판 바뀜 | 서비스가 처리한다(웹과 같은 `_finish` 경로). 앱은 SSE `board` 로 받는다 |

## 코디가 실물 확인할 순서 (A4 · KOS 데모 지점)

1. Bearer 로그인 → `GET /api/visits/{id}/chart` 에서 `tasks[].assignee.{logId, base}` 를 기록한다
2. `POST /api/visits/{id}/chart` `{chart:"assignee", rows:[{taskId, body:"…", staffId:<나>, baseLogId:<1의 logId>, baseBody:<1의 base.body>, baseDoctorStaffId:null}]}` → 200 · `saved` · 새 `logId`. KOS 화면 · outbox 에 메모가 반영됐는지 본다
3. 같은 요청을 옛 `baseLogId` 로 한 번 더 보낸다 → 409 `chart_conflict` · `details.conflicts[0].body` = 이어 붙인 글
4. `POST /api/visits/{id}/photos` multipart `category=before` + JPEG 2장 → 200 · `kosError:null` · `rejected:[]` · `kosSynced:true`
5. `GET /api/visits/{id}/photos` → 두 묶음 · 2장 / `?poll=1` · `?tick=1`
6. `GET …/photos/{photoId}/file` (Bearer) → 바이트 · 머리 셋
7. `POST …/photos/{photoId}/delete` → 그 장이 빠지고 KOS 에서도 삭제됐는지 본다
8. (KOS 미반영 장이 있을 때) `POST …/photos/{photoId}/kos-retry` → `kosError:null` · `kosSynced:true`
9. 배포 시 Caddy: 앱 경로로 6MiB 를 넘는 본문(예: 5MB 2장)이 413 없이 통과하는지 본다

## 이슈 · 주의

- 커밋 · push · PR 은 하지 않았다. 변경은 워크트리에만 있다(`app/` 의 변경은 mobile 워커 것이라 건드리지 않았다).
- 첫 `uv run` 때 워크트리 루트에 `.venv` 가 생겼다(gitignore 대상).
- mediness `40-architecture/deployment.md` 「앞단 본문 상한」 문장에 `/api/visits/*/photos` 를 넣는 일은 spec-sync 몫이다.

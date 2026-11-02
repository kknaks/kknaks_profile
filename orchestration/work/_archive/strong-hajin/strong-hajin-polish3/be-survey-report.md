# 고도화 3차 조사 (backend)

- 대상: `strong-hajin-polish3` 워크트리, base `origin/main`(`d1b5137`)
- 읽기 전용 조사다. 코드 수정, 테스트·빌드 실행, 서버·Tauri 기동, 운영 접속은 하지 않았다.
- 경로 약어: `B/` = `backend/src/ax_workspace/`, `T/` = `backend/tests/`, `F/` = `frontend/src/`, `S/` = `frontend/src-tauri/`
- 줄 번호는 모두 `d1b5137` 기준이다. 2차 리포트의 줄 번호는 옛 값이라 다시 셌다.

## 0. 한 줄 요약

- **R1 로그인**: 서버 몫은 없다. 브랜드 문장을 내는 API 가 없고 `/api/auth/providers` 는 `local`·`oidc`·데모 계정만 준다(`B/entrypoints/http.py:627-644`).
- **R2 내보내기**: `GET /api/meetings/{id}/export?format=html` 하나다. 서버는 `text/html; charset=utf-8` + `Content-Disposition: attachment; filename*=UTF-8''<제목>.html` 로 내린다(`B/entrypoints/http.py:896-912`). 인증은 **쿠키 세션**(`scax_session`, HttpOnly·SameSite=Lax·운영에서 Secure)이고, 같은 origin 의 `<a href>` 이동에도 쿠키가 실린다. **원인 후보(추정)**: 데스크톱 셸이 Tauri 다운로드 핸들러(`on_download`)를 걸지 않는다(`S/src` 에 `download` 0건). 그래서 wry(macOS)는 다운로드로 넘기지 않는다. `text/html` 응답은 `canShowMIMEType=true` 라 **허용(Allow)으로 웹뷰 안에서 열린다**(wry 0.55.1 `navigation.rs:85-103`). 즉 파일로 받는 경로가 셸에 없다. 실기기에서 확인하지 않았다.
- **R3 회의 제목**: `meetings.title` 은 사람만 쓰고, `meetings.title_candidate` 는 회의 합성 잡이 제목이 비었을 때만 채운다(`B/modules/meetings/application.py:942-944`). 제목을 바꾸는 API 는 있다: `PATCH /api/meetings/{id}` 에 `{"title": …}` 만 보내면 된다. 다만 **참석자만**, 그리고 **「예정」·「완료」 상태에서만** 받는다(`:474-532`, `B/modules/meetings/policy.py:233`). 제목을 저장해도 `title_candidate` 는 지워지지 않는다. 「제목 없는 회의」 문구는 서버 상세 응답에 없다(`title: null`). 서버가 그 문구를 쓰는 곳은 내보내기 파일·진행 기록·자료 출처 같은 파생 글자다.
- **R4 업무 수정**: 필드 수정은 `PATCH /api/tasks/{id}` 하나다. 바꾸는 칸은 제목·내용·시작 예정일·마감일·프로젝트·상위·선행·결재자다(`B/modules/work/task_commands.py:46-71`, `:124-163`). **담당·상태·실제 시작일은 이 API 로 바꿀 수 없다.** 업무를 바꾸는 명령은 **전부 `task.version` 을 올린다**(체크리스트·자료·참고 연결 포함, 15+13곳). 회차가 어긋나면 **422 `task version is stale`** 이다(409 아님). 인라인 저장을 연달아 하면 매번 버전이 오르고 이력이 한 줄씩 쌓인다. 앞 응답의 `version` 을 받아 다음 요청에 싣지 않으면 뒤 요청은 422 다. 담당 변경은 별도 명령 `POST /api/tasks/{id}/reassign` 이다(`task.assign` 역량 필요, 새 담당 수락 대기). 업무 상세 응답에는 서버가 정한 「허용 전이/허용 명령」 목록이 **없다**.
- **R5 선행업무**: 서버가 판정한다. `시작 전` 상태에서 나가는 두 전이(`→진행 중`, `→완료`)만 막고, **409** `끝나지 않은 선행업무가 있습니다: A, B, C` 로 거절한다(`B/modules/work/lifecycle.py:130-140`, `B/entrypoints/http.py:558`). 상세 응답에는 막힘 플래그가 없다. `predecessors[]`(task_id·title·state)만 오고, 빨간 박스 문장과 푸터 문장은 **화면이 만든다**(`F/lib/labels.ts:339`, `:446`, `:455`).
- **R6 여백**: 서버 몫은 없다.

---

## 1. R1 로그인 (서버 몫 확인)

- 로그인 화면이 부르는 서버 값은 `GET /api/auth/providers` 하나다. 응답은 `{"local": True, "oidc": False}`, 그리고 데모 지름길이 켜져 있으면 `demo_accounts`·`demo_password` 가 붙는다(`B/entrypoints/http.py:627-644`). 브랜드 h1·설명 문장은 서버 응답에 없다.

## 2. R2 회의 상세 「내보내기」

### 2-1. 라우터·서비스·형식·헤더

| 항목 | 값 | 근거 |
|---|---|---|
| 라우터 | `GET /api/meetings/{meeting_id}/export` | `B/entrypoints/http.py:896-912` |
| `format` | `Literal["html"]`, 기본 `"html"`. **이 값 하나뿐**이고 `pdf`·`docx` 는 422 | `:899`, 테스트 `T/contract/test_meeting_finalize.py:1162-1167` |
| 서비스 | `WorkflowApplication.export_meeting` → `MeetingApplication.export`(최종 벌 안건만) → `render_meeting_html` | `B/bootstrap/application.py:2005-2010`, `B/modules/meetings/application.py:1033-1045`, `B/modules/meetings/export.py` |
| 권한 | `_readable(principal, meeting_id)`. 읽을 수 없으면 404 | `B/modules/meetings/application.py:1041`, 테스트 `T/contract/test_meeting_finalize.py:1175` |
| `Content-Type` | `text/html; charset=utf-8` | `B/entrypoints/http.py:910` |
| `Content-Disposition` | `attachment; filename*=UTF-8''{quote(filename)}` (RFC 5987, **`filename=` 대체값 없음**) | `:911` |
| 파일명 규칙 | 사람 제목 → 없으면 `title_candidate` → 없으면 「제목 없는 회의」. 그중 `isalnum()`·공백·`-`·`_` 만 남긴다. 내부 ID 는 파일명에 넣지 않는다. 확장자 `.html` | `B/modules/meetings/export.py:87-89`, `:343-346`, `B/entrypoints/http.py:907` |
| 한글 인코딩 | `urllib.parse.quote` 퍼센트 인코딩(UTF-8). 한글은 `isalnum()` 이 참이라 살아남는다 | `B/entrypoints/http.py:911`, `export.py:345` |

### 2-2. 인증 — `<a href>` 로 열 때 실리나

- **쿠키 세션이다.** 세션 쿠키 이름은 `scax_session`, 수명은 12시간이다(`B/entrypoints/http_auth.py:21-22`). 판정은 `current_principal`(= `developer_principal`)이 한다. 쿠키를 먼저 보고, 개발·시험 프로파일에서만 `X-Demo-Persona` 헤더를 본다(`:69-79`, `:103`). `Authorization`/Bearer 는 **0건**이다.
- 쿠키 속성은 로그인 시 `set_cookie(httponly=True, samesite="lax", secure=cookie_secure(settings), path="/", max_age=12h)` 다(`B/entrypoints/http.py:653-661`). `secure` 는 `profile == PRODUCTION` 일 때만 참이다(`B/entrypoints/http_auth.py:106-107`).
- **CORS 미들웨어는 없다**(`CORSMiddleware` 0건). 운영에서는 인그레스가 같은 호스트의 `/api` 를 백엔드로 나눈다(`deploy/k8s/nginx.conf:1`, `deploy/k8s/front.Dockerfile:3`). 그래서 화면과 API 는 **같은 origin** 이다.
- 화면의 `fetch` 는 전부 `credentials: "same-origin"` 이다(`F/lib/api.ts:136-143` 외 6곳). 내보내기는 `<a className="scax-button scax-button--outlined-neutral" href={meetingExportUrl(...)}>` 로 연다(`F/features/meetings/MeetingDetailPage.tsx:1005`, URL 은 `F/lib/api.ts:1373`). 같은 origin 의 최상위 이동이므로 SameSite=Lax 쿠키가 실린다. 서버 쪽에서는 인증이 실리는 구조다.

### 2-3. Tauri 데스크톱에서

| 판 | 셸이 여는 곳 | 근거 |
|---|---|---|
| `medi-ax` | `operationalOrigin = https://ax.medisolveai.xyz`. 웹뷰가 **운영 웹을 그대로 연다**(`WebviewUrl::External`). API 도 같은 origin 이다 | `S/flavors/medi-ax/shell.config.json`, `S/src/lib.rs:374` |
| `strong-hajin` | `operationalOrigin = null` → 「서버 주소가 설정되지 않았습니다」 화면. **API 를 부르지 않는다**(브리프의 「origin null」은 이 상태다) | `S/flavors/strong-hajin/shell.config.json`, `S/src/config.rs:55-58`, `S/src/shell_ui.rs:137` |

- 운영 origin 은 항상 네비게이션 허용 목록에 들어간다(`S/src/config.rs:66-75`). 그래서 `/api/meetings/{id}/export` 로의 이동은 `on_navigation` 을 통과한다(`S/src/lib.rs:384-405`).
- 쿠키는 `.incognito(false)` 라 남는다(`S/src/lib.rs:381-383`).
- **다운로드 핸들러가 없다.** `S/src` 에 `download`·`on_download` 가 **0건**이다. Tauri 2.11.6 의 `download_handler` 기본값은 `None` 이다(`~/.cargo/.../tauri-2.11.6/src/webview/mod.rs:357`). 이 경우 tauri-runtime-wry 2.11.4 는 `with_download_started_handler` 를 걸지 않는다(`tauri-runtime-wry-2.11.4/src/lib.rs:5010-5012`).
- wry 0.55.1(macOS)의 동작(`wry-0.55.1/src/wkwebview/navigation.rs`)은 다음과 같다.
  - 이동 액션이 `shouldPerformDownload` 면, 핸들러가 없으니 **Cancel** 이다(`:68-74`). `<a download>` 속성이면 이쪽인데, 지금 단추에는 `download` 속성이 없다.
  - 응답 단계에서는 `canShowMIMEType` 이 거짓일 때만 Download 를 고려하고, 그 밖은 **Allow** 다(`:85-103`). `text/html` 은 표시 가능한 형식이다. `Content-Disposition: attachment` 를 보는 코드는 이 파일에 없다.
  - 이 코드대로라면 셸에서는 내보낸 HTML 이 **파일로 저장되지 않는다.** 웹뷰가 그 문서로 이동하거나(그때 `PageLoadEvent::Started` 로 셸 세션 정리가 돈다, `S/src/lib.rs:407-413`) 아무 일도 일어나지 않는다. 어느 쪽인지는 실행해 보지 않아 확정하지 못했다(§조사 한계).
- 같은 구조라면 아래 2-4 의 다른 `attachment` 다운로드도 셸에서 같은 길을 탄다. 자료 열기(`inline`)는 다운로드가 아니다.

### 2-4. 서버가 파일을 내려주는 엔드포인트 전부 (7개)

모두 같은 쿠키 인증(`Depends(developer_principal)`)이고, 응답은 `fastapi.Response(content=bytes)` 한 번에 싣는다(스트리밍·`FileResponse` 0건).

| # | 엔드포인트 | `Content-Type` | `Content-Disposition` | 근거 |
|---|---|---|---|---|
| 1 | `GET /api/meetings/{id}/export?format=html` | `text/html; charset=utf-8` | `attachment; filename*=UTF-8''…` | `B/entrypoints/http.py:896-912` |
| 2 | `GET /api/meetings/{id}/materials/{mid}/content` | 브라우저가 띄울 수 있는 형식이면 그 형식, 아니면 원본 | **표시 가능하면 `inline`, 아니면 `attachment`** (새 탭에서 연다) | `:1105-1122` |
| 3 | `GET /api/daily-reports/{rid}/materials/{mid}/content` | 원본 `content_type` | `attachment` | `:1540-1547` |
| 4 | `GET /api/material-folders/{fid}/materials/{mid}/content` | 원본 | `attachment` | `:1628-1635` |
| 5 | `GET /api/tasks/{tid}/materials/{mid}/content` | 원본 | `attachment` | `:1994-2006` |
| 6 | `GET /api/work-requests/{rid}/materials/{mid}/content` | 원본 | `attachment` | `:2368-2382` |
| 7 | `GET /api/work-requests/{rid}/attachments/{aid}/content` | 원본 | `attachment` | `:2393-2404` |

- 파일명 인코딩은 7곳 모두 `filename*=UTF-8''{quote(name)}` 다. `inline` 판정은 2번 한 곳뿐이다(`"inline" if inline` 1건).
- 자료 출처 링크(`origin`)도 위 경로를 가리킨다(`B/bootstrap/material_sources.py:72`, `:88`, `:103`, `:128`, `:176`). 회의 전사는 `/api/meetings/{id}/transcript` 인데, 이 경로는 파일 응답이 아니라 JSON 이다(`:147`).

## 3. R3 회의 제목

### 3-1. 필드·생성·저장

| 필드 | 모델 | 누가 언제 채우나 | 근거 |
|---|---|---|---|
| `meetings.title` | `String(300)`, nullable | **사람만 쓴다.** 생성(예약) 입력, 또는 회의 정보 편집 `update_info` 의 `meeting.title = normalize_optional_text(...)` (쓰기 1곳). 빈 문자열은 `None` 이 된다 | `B/platform/persistence.py:298`, `B/modules/meetings/application.py:515-516`, `B/modules/meetings/domain.py:242-248` |
| `meetings.title_candidate` | `String(300)`, nullable. 주석 「사람이 저장해야 제목이 된다」 | **회의 합성 잡**(meeting worker 의 finalize)이 성공을 커밋할 때 `if not meeting.title and notes.title_candidate:` 면 채운다(쓰기 1곳) | `B/platform/persistence.py:300-301`, `B/modules/meetings/application.py:942-944`, 진입 `B/bootstrap/application.py:458-461` |
| AI 출력 | 스키마 필수 키 `title_candidate`. 「제목이 비어 있을 때만 뜻이 있다」. 프롬프트는 「제목이 비어 있으면 한 줄 후보, 이미 있으면 null」 | 제목이 있으면 규칙이 후보를 `None` 으로 버린다 | `B/modules/meetings/schemas/ai_final_output.json:8-13`, `B/modules/meetings/finalize.py:334`, `:253-255` |

- 사람이 제목을 저장해도 `title_candidate` 는 **지워지지 않는다.** `update_info` 에 그 열을 건드리는 줄이 없다(`B/modules/meetings/application.py:474-532`).
- 응답에는 둘이 따로 실린다: 상세 `meeting.title`(`:1777`)·`meeting.title_candidate`(`:1807`), 목록(`:218-219`), 합성 결과(`:1055`).

### 3-2. 제목을 바꾸는 API — 있다

| 항목 | 값 | 근거 |
|---|---|---|
| 경로 | `PATCH /api/meetings/{meeting_id}` | `B/entrypoints/http.py:778-788` |
| 페이로드 | `MeetingInfoPatch`(`extra="forbid"`): `title`(≤300) · `purpose`(≤1000) · `starts_at` · `ends_at` · `location`(≤300) · `attendee_ids` · `external_attendees`. `model_dump(exclude_unset=True)` 라 **`{"title": "…"}` 하나만 보내도 된다.** `title: null`/`""` 은 비우기다 | `B/modules/meetings/commands.py:163-171`, `B/entrypoints/http.py:784` |
| 권한 | `meeting.manage` 역량(구성원·팀장 모두 보유) + **참석자**(`is_attendee`). 참석자가 아니면 `MeetingAccessDenied` → 404 | `B/modules/meetings/application.py:483-489`, `B/modules/organization_access/catalog.py:97`, `:120`, `B/entrypoints/http.py:532` |
| 상태 | `can_edit_info = attendee and status in {scheduled, done}`. 진행 중·정리 중·**실패**·취소에서는 `MeetingStateConflict` → 409 | `B/modules/meetings/policy.py:233`, `B/modules/meetings/domain.py:104`, `application.py:493-494`, `http.py:535` |
| 낙관적 잠금 | HTTP 경로는 `expected_version` 을 **넘기지 않는다**(나중 쓰기가 이긴다). 상세 응답에도 `version` 키가 없다. AX 갈래 `meeting.update` 만 `expected_version` 을 싣는다 | `B/entrypoints/http.py:784-786`, `B/bootstrap/application.py:3695-3705` |
| 버전·이력 | `meeting.version += 1`, 감사 `meeting.updated`(「회의 정보 수정: {제목}」, `before_ref=meeting:{id}@{before}`). 회의에는 업무처럼 스냅샷 표가 없고 감사 한 줄만 남는다 | `B/modules/meetings/application.py:529-532` |
| 시각을 함께 보낼 때 | 시각이 실제로 바뀌면 참석자 겹침을 검사하고(`MeetingTimeOverlap` 409), 커밋 뒤 회의실 예약을 맞춘다. **제목만 보내면 둘 다 건너뛴다** | `application.py:509-514`, `B/bootstrap/application.py:1700-1709` |
| AX 경유 | MCP `meeting_update` → 제안 `meeting.info.update` → 확정 시 같은 `update_info` | `B/modules/ax_execution/tool_catalog.py:85`, `B/entrypoints/mcp.py:840-847`, `B/bootstrap/application.py:3684-3694` |

- 「후보 [적용]」 전용 명령은 **없다.** 지금 코드로 후보를 제목으로 만드는 길은 `PATCH` 에 후보 문자열을 `title` 로 보내는 것 하나다(위 표).
- 회의 수정 계열 API 전부는 다음과 같다. `PATCH /api/meetings/{id}`(정보), `DELETE /api/meetings/{id}`, `POST …/start`·`…/end`·`…/finalize`, 안건 `POST/PATCH/DELETE …/agendas…`(안건 제목은 회의 제목과 별개다, `application.py:1269-1272`), 줄 `POST/PATCH …/lines…`, 다음 할 일 `…/todos/{id}/promote`·`DELETE`, 자료 `POST/DELETE …/materials`, 공유 `POST/DELETE …/shares`(`B/entrypoints/http.py:720-1147`의 `@app.(post|patch|delete)("/api/meetings…` 18건).

### 3-3. 「제목 없는 회의」는 누가 채우나

- **상세·목록 API 는 그 문구를 주지 않는다.** 그대로 `title: null` 과 `title_candidate` 를 준다(`B/modules/meetings/application.py:218-219`, `:1777`, `:1807`). 화면 표시는 프론트가 정한다(`F/lib/labels.ts`, `F/lib/viewModels.ts`, `F/shell/CalendarRail.tsx` 에 문구가 1건씩 있다).
- 서버가 문구를 **글자로 박는 곳**은 파생 표면이다(「제목 없는 회의」 16건).

| 표면 | 규칙 | 근거 |
|---|---|---|
| 내보내기 파일명·본문 | 제목 → 후보 → 「제목 없는 회의」 | `B/modules/meetings/export.py:29`, `:87-89`, `:346` |
| 업무 진행 기록의 회의 이름 | 제목 → 후보 → 문구 | `B/platform/work_tasks.py:93-99` |
| 자료 출처 이름 | 제목 → 후보 → 문구 | `B/platform/native_materials.py:25-29`, `B/bootstrap/material_sources.py:117` |
| 감사 요약 | 제목 → 문구 (**후보는 안 본다**) | `B/modules/meetings/application.py:332`, `:532` |
| 검색·근거 제목 | 제목 → 문구 (후보 안 봄) | `B/bootstrap/application.py:270`, `:327`, `:410` |
| AX 카드 미리보기 | 제목 → 후보 → 문구 | `B/platform/actions.py:1338` |
| 회의실 예약 제목 | 문구 | `B/modules/meetings/rooms.py:27` |

## 4. R4 업무 수정 계약

### 4-1. 업무를 바꾸는 API 전부

공통: `Depends(developer_principal)` 쿠키 인증. 「활성 담당자」는 `repository.task(task_id, owner_id)` = `_held_by` 다. 담당이 아니면 `TaskNotFound` → **404** 다(`B/platform/work_tasks.py:1090-1096`, `B/entrypoints/http.py:532`). 버전 열이 「○」인 명령은 성공하면 `task.version` 이 오른다.

| # | 경로·메서드 | 페이로드 | 응답 | 권한 | 버전 | 근거 |
|---|---|---|---|---|---|---|
| 1 | `PATCH /api/tasks/{id}` | `TaskUpdateInput`(4-2) | `TaskDateMutationResult`(=`_view`+`schedule_release`) | `task.self_manage` + 활성 담당자. 취소된 업무는 거절 | ○ | `http.py:1533-1538`, `B/modules/work/application.py:529-612` |
| 2 | `POST …/start` | `{expected_version}` | 날짜형 | 같음 + 선행 게이트 | ○ | `http.py:2541-2549` |
| 3 | `POST …/block` | `{expected_version, reason}`(필수) | `TaskMutationResult` | 같음 | ○ | `http.py:2551-2553`, `task_commands.py:171-172` |
| 4 | `POST …/resume` | `{expected_version}` | 기본형 | 같음 | ○ | `http.py:2555-2557` |
| 5 | `POST …/complete` | `{expected_version}` | 날짜형 | 같음 + 선행·하위 게이트. 요청 업무는 거절(완료 보고로) | ○ | `http.py:2559-2562` |
| 6 | `POST …/cancel` | `{expected_version, reason}`(필수, ≤4000) | 기본형 | 같음. 수락된 요청 업무는 409 `WORK_CANCEL_REQUIRES_AGREEMENT` | ○ | `http.py:2564-2570`, `task_commands.py:204-219`, `application.py:2107-2125` |
| 7 | `POST …/completion-report` | `{expected_version, summary, output_material_ids}` | `_view`+`delivery`+`schedule_release` | 활성 담당자, **요청 업무만**, `in_progress`/`blocked` 에서만 | ○ | `http.py:1678`, `application.py:1870-1918` |
| 8 | `POST …/reopen` | `{expected_version, reason?}` | 기본형 | `task.read`. 본인 업무는 담당자, 요청 업무는 요청자. `done`/`completion_submitted` 에서만. 상위가 완료면 409 | ○ | `http.py:1863`, `application.py:2127-2185` |
| 9 | `POST …/reassign` | `{expected_version, assignee_id, reason?}` | `TaskAssignmentResult` | **`task.assign`** + 업무 읽기 + 배정 범위 | ○ | `http.py:1933-1944`, `B/modules/work/assignments.py:188-226` |
| 10 | `POST /api/task-assignments/{aid}/accept`·`/decline` | (수락) `expected_task_version?` / (거절) `reason` | 배정 결과 | 제안받은 사람 | ○ | `http.py:1517-1531`, `assignments.py:259-275`, `B/platform/work_tasks.py:2701-2788` |
| 11 | `POST …/proposals` | `{kind: cancellation\|terms_change, expected_version, reason?, payload?}` | `{proposal, task_version}` | **요청자만**. 제안만으로는 아무것도 안 바뀐다 | ✕ | `http.py:1887`, `application.py:2187-2215` |
| 12 | `POST …/proposals/{pid}/respond` | `{expected_version, agree, reason?}` | | **담당자만**. 동의하면 취소 또는 `due_date`·제목·내용 적용 | ○(동의 시) | `http.py:1902`, `application.py:2217-2270`, `:2309-2356` |
| 13 | `POST …/proposals/{pid}/withdraw` | `{expected_version}` | | 제안자 | | `http.py:1918`, `application.py:2272-2296` |
| 14 | 체크리스트 `POST …/checklist` · `PATCH …/checklist/{iid}` · `POST …/checklist/order` · `DELETE …/checklist/{iid}` | 업무 회차 `expected_task_version` 은 **선택**, 항목 회차 `expected_version` 은 수정·보관에 필수 | `ChecklistMutationResult` | 활성 담당자(`_holding`) | ○ | `http.py:2173-2217`, `application.py:2532-2676`, `B/modules/work/checklist_commands.py:6-41` |
| 15 | 참고 `POST …/references` · `DELETE …/references/{rid}` | `{referenced_task_id}` | | 활성 담당자 | ○ | `http.py:1690-1706`, `application.py:2740-2779` |
| 16 | 후행 해제 `DELETE …/successors/{sid}` | 후행의 회차. 어긋나면 **409** | | 둘 중 하나를 고칠 수 있는 사람 | ○(후행) | `http.py:1708`, `application.py:1552-1615` |
| 17 | 자료 `POST …/materials`(파일)·`…/materials/links`·`…/materials/references`·`…/material-bindings/{bid}/detach` | | `…+task_version` | 활성 담당자 | ○ | `http.py:1658`, `:1946`, `:1959`, `:2008`, `B/modules/work/materials.py:168-282` |
| 18 | 시간 배정 `POST …/schedules` · `PATCH /api/task-schedules/{sid}` | 배정 자신의 회차 | | 배정 가능한 사람 | ✕(배정 회차) | `http.py:1736`, `:1764`, `task_commands.py:222-245` |
| 19 | 완료 인정·보완 요청 | 판단함 `POST /api/action-items/{id}/commands/{command}` | | 요청자 | ○ | `B/platform/action_center.py:1444-1446`, `application.py:1920-1951` |

- MCP/AX 도구가 같은 명령을 부른다: `task_update`·`task_start`·`task_block`·`task_resume`·`task_complete`·`task_cancel`(`B/entrypoints/mcp.py:2091-2095`), `task_reassign`·`task_reopen`·`task_completion_submit`·`task_proposal_*`·`task_reference_*`·`task_material_*`(`B/modules/ax_execution/tool_catalog.py:61-76`).
- **선행 연결은 별도 명령이 없다.** `PATCH` 의 `preceding_task_ids` 로 배열 전체를 교체한다(`task_commands.py:66-69`).

### 4-2. 「편집」 저장이 부르는 API 가 실제로 바꾸는 필드

- 화면 `updateTask` → `PATCH /api/tasks/{id}`(`F/lib/api.ts:255-…`).
- HTTP 입력 `TaskUpdateInput`(`extra='forbid'`, `B/modules/work/task_commands.py:124-163`)의 칸은 다음과 같다. `expected_version`(필수, ≥1) · `title` · `description` · `start_date`·`clear_start_date` · `due_date`·`clear_due_date` · `project_id`·`clear_project` · `parent_task_id`·`clear_parent` · `preceding_task_ids` · `approver_id`·`clear_approver`.
- 이 값은 정본 `TaskEditFields`(화이트리스트, `extra='forbid'`, `:46-105`)로 접힌다. 최종 키는 **8개**다: `title`, `description`, `start_date`, `due_date`, `project_id`, `parent_task_id`, `preceding_task_ids`, `approver_id`.
- 규칙:
  - 제목을 `null` 로 비우면 거절한다(`:87-88`).
  - 키가 하나도 없으면 「at least one field is required」로 거절한다(`:98-99`).
  - **값이 바뀌지 않아도 저장하면 버전이 오른다.** 동일 값 검사는 없다(`application.py:606`).
- 서버가 이 API 로 **받지 않는 것**: 담당(`assignee`), 상태, 실제 시작일(`started_at`)·완료일(`completed_at`), 참조자(`cc_member_ids`), 체크리스트, 차단 사유.

### 4-3. 버전

- **올리는 곳**: `task.version += 1` 15곳과 `_moved()` 13곳(`B/modules/work/application.py:2443-2446`, `B/modules/work/materials.py:279-282`).
  - 필드 수정 `:606`
  - 전이 `:2081`(`lifecycle.py:164`)
  - 완료 보고 `:1909`, 인정 `:1929`, 보완 `:1947`, 재개 `:2161`
  - 제안 동의 `:2319`, `:2348`
  - 체크리스트 `:2546`, `:2596`, `:2622`, `:2653`, `:2672`
  - 참고 `:2752`, `:2774`
  - 하위 붙음 `:513`, 후행 해제 `:1599`
  - 자료 `materials.py:168`, `:201`, `:233`, `:271`
  - 배정 제안·첫 지정·거절 `B/platform/work_tasks.py:2439`, `:2683`, `:2766`
  - 요청 수락·종료 `:1927`, `:1963`, `:2822`
- **낙관적 잠금으로 쓰인다.** 업무 행을 `FOR UPDATE` 로 잡은 뒤 `task.version != expected_version` 이면 거절한다(`application.py:538-540`, `lifecycle.py:150-151`).
- **충돌 응답은 422** `{"detail": "task version is stale"}` 이다. `InvalidTaskTransition` 은 `TaskError` 와 함께 422 로 매핑된다(`B/entrypoints/http.py:586-587`). 이 422 가 「현행 계약」이라는 주석이 있고, 후행 해제만 409 로 따로 뒀다(`B/modules/work/errors.py:191-202`). 체크리스트 `_holding` 은 `TaskError("task version is stale")` 로 역시 422 다(`application.py:2682-2683`).
- **전이 판정 순서**: 선행 게이트(409) → 요청 업무 완료(422) → 하위 게이트(409) → **그다음 회차**(422) → 전이표(422)(`lifecycle.py:130-153`). 그래서 회차가 낡았어도 선행이 막혀 있으면 409 가 먼저 나온다.
- **필드 하나씩 연달아 저장하면**(코드에서 읽은 결과):
  - 저장할 때마다 `version` 이 1씩 오른다. 이력에 `activity_events` 1줄(`task.updated` 「업무 내용 수정: 제목 (due_date)」)과 `task_versions` 스냅샷 1행이 쌓인다(`application.py:607-611`, `B/platform/work_tasks.py:980-1010`). `task_activities` 도 1행 늘어난다(`touch`, `:1329-1331`).
  - 응답 본문에 새 `version` 이 온다(`_view` `"version"`, `application.py:2798`). 다음 요청이 그 값을 실어야 통과한다.
  - 같은 `expected_version` 으로 **동시에** 두 요청을 보내면 행 잠금 때문에 하나씩 처리된다. 둘째는 422 다.
  - 체크리스트·자료 조작이 사이에 끼어도 업무 버전이 오르므로, 열어 둔 상세의 `version` 은 그만큼 낡는다.
  - 프론트의 관계 편집은 이미 저장마다 `getTask()` 로 버전을 다시 읽는다(`F/features/work/WorkModals.tsx:1488`, `:1510`).
  - 날짜가 바뀐 저장은 기간 밖 시간 배정을 같은 transaction 에서 닫고 `schedule_release` 로 알린다(`application.py:603-605`).

### 4-4. 담당자 변경

- **필드 수정과 별개 명령**이다. 주석도 「never a field on the Task edit form」이라고 적는다(`assignments.py:191-192`, `B/bootstrap/application.py:3053-3058`). `TaskEditFields` 에 담당 칸이 없다.
- **권한**: `task.assign` 역량이 있어야 한다(`assignments.py:194`). 기본 역할 기준으로 **구성원에게는 없다**(`B/modules/organization_access/catalog.py:77-103`). 팀장(`:105-109`)·인사 담당(`:126-128`)이 갖고, 프로젝트 담당(프로젝트 리드)도 그 프로젝트 안에서 갖는다(`:144`). 새 담당은 「내가 배정할 수 있는 범위」(조직 축 + 프로젝트 축) 안이어야 한다(`assignments.py:92-104`, `:216-217`). 자기 자신은 예외다.
- **동작**: 기존 담당을 닫지 않고 새 `task_assignments` 행을 `pending` 으로 **덧붙인다.** 새 담당이 수락해야 교체된다(`B/platform/work_tasks.py:2658-2699`, `:2701-2788`).
  - 대기 제안이 이미 있으면 409 다(`assignments.py:208-210`).
  - 같은 사람이면 422 다(`:211-212`).
  - 담당 없는 업무에서는 첫 지정 `hand_to` 이고, 거절하면 업무가 취소된다(`work_tasks.py:2422-2451`, `:2763-2770`).
- **이력**: `activity_events` 에 `task.assignment.change_proposed`(사유 포함) → 수락 시 `task.assignment_accepted` + `task.assignment.changed`, 거절 시 `task.assignment_declineed` 가 남는다. `task_versions` 스냅샷도 쌓인다(`work_tasks.py:2690-2697`, `:2771-2786`).
- **수신함**: 새 담당 앞에 판단 항목(`DecisionItem`·`Submission`·`ReviewAssignment`)이 열려 「배정 수락」 inbox 에 뜬다(`work_tasks.py:2453-…`, `assignments.py:249-252`).
- **알림(`notifications`)은 없다.** 알림을 내는 곳은 업무 요청 생성·수락 1곳뿐이다(`work_tasks.py:2099-2120`).
- 자동 프로젝트 초대가 붙는다(`assignments.py:220-226`).
- **담당 후보 목록**: `GET /api/task-assignment-candidates`(`task.assign` 필요, `http.py:1503-1507`, `assignments.py:88-101`). 회의 승격용 `…/promotion-candidates` 는 일부러 다른 목록이다(`http.py:876-893`).

### 4-5. 상태 전이표

상태 값은 `open`·`in_progress`·`blocked`·`completion_submitted`·`done`·`cancelled` 6개다(`B/modules/work/lifecycle.py:20-26`). **밖으로는 `completion_submitted` 가 `done` 으로 접혀 나간다**(`B/modules/work/task_projection.py:50-61`). 「승인 대기」는 `derived.approval = awaiting_review` 로 말한다. **「막힘」은 별도 플래그가 아니라 상태 `blocked`** 다(`block_reason` 열이 사유를 갖는다).

허용표 `_ALLOWED_TRANSITIONS`(`lifecycle.py:93-104`) × API:

| 현재 \ 목표 | `in_progress` | `blocked` | `done` | `cancelled` |
|---|---|---|---|---|
| `open` | `/start`(·`/resume` 도 같은 목표) — **선행 게이트** | ✕ | `/complete` 직행 — **선행 게이트**, 하위 게이트, 요청 업무 거절 | `/cancel` 사유 필수 |
| `in_progress` | — | `/block` 사유 필수 | `/complete` — 하위 게이트, 요청 업무 거절(→ `/completion-report`) | `/cancel` |
| `blocked` | `/resume`(·`/start`) | — | ✕ (요청 업무는 `/completion-report` 가 `blocked` 에서도 된다) | `/cancel` |
| `completion_submitted` | 보완 요청(판단함) · `/reopen` | ✕ | 인정(판단함) | `/cancel` (수락된 요청 업무는 409) |
| `done` | `/reopen`. 표에도 `done→in_progress` 가 있어 `/resume`·`/start` 도 통과한다(아래) | ✕ | — | ✕ |
| `cancelled` | ✕ (편집도 거절 `application.py:541-542`) | ✕ | ✕ | — |

- `/start` 와 `/resume` 은 서버에서 **같은 목표 `IN_PROGRESS`** 다(`B/entrypoints/http.py:2549`, `:2557`). 차이는 docstring 과 응답 타입뿐이다. 그래서 `done` 업무에 `/resume` 을 부르면 `transition_task` 허용표를 지난다. 이 경우 `reopened_at` 을 찍지 않고 `completed_at` 도 지우지 않는다(`application.py:2079-2096`; 재개는 `:2158-2160`). `/reopen` 과 다른 결과다.
- **부수효과**(`application.py:2074-2105`, `lifecycle.py:161-173`):
  - `open→in_progress`: `start_date` 가 비어 있으면 오늘(서울)로 채운다. `started_at` 이 비어 있으면 지금으로 찍는다.
  - `→done`: `completed_at = now`. 비어 있는 `due_date` 를 그날로 채운다(`due_date_on_completion`, `task_projection.py:40-47`). 완료 보고도 같다(`application.py:1905-1908`).
  - `→blocked`: `block_reason` 에 사유를 쓴다. 다른 전이는 `block_reason=None` 으로 비운다.
  - `→cancelled`: `cancel_reason` 이 없으면 `"direct"`. 사유는 이력 `reason` 으로 간다.
  - 재개: `reopened_at = now`, `completed_at = None`. 보완 요청은 `completed_at = None`(`:1946`).
  - 전이마다 `activity_events` `task.state_changed`(「업무 상태 a → b: 제목」) + 스냅샷이 남는다. 날짜가 바뀌면 시간 배정을 정리한다.
- **필수 입력**: 차단·취소는 사유가 필수이고 공백만 있으면 거절한다(`task_commands.py:171-219`, `lifecycle.py:155-160`). 재개 사유는 선택이다. 완료 보고는 `summary` 가 필수다.
- 전이를 바꾸는 사람: 전이 1~6은 **활성 담당자만**이다. 요청자·참조자·배정자는 404 다(`application.py:2041`).

### 4-6. 날짜 검증

- `validate_schedule`: `start_date > due_date` 면 `TaskError("start date cannot be later than the due date")` → **422**(`B/modules/work/task_values.py:29-31`).
- 거는 곳은 3곳이다: 업무 수정 `application.py:599`, 생성 `task_creation.py:35`, 배정 `assignments.py:177`. **수정은 저장 후의 두 값으로 검사한다**(`:597-599`). 한쪽만 보내도 남은 값과 비교한다.
- **검사를 지나지 않는 날짜 쓰기**: 시작 전이의 시작일 채움(`lifecycle.py:165-171`), 완료·완료 보고의 마감일 채움(`task_projection.py:44-46`), 제안 동의의 `due_date`(`application.py:2335-2338`). 이 경로로는 뒤집힌 기간이 생길 수 있다(주석 `:2074-2076`).
- **실제 시작일(`started_at`)은 사람이 바꿀 수 없다.** 쓰기는 전이 1곳뿐이다(`application.py:2086-2087`). 어떤 입력 모델에도 그 칸이 없다. `completed_at`·`reopened_at` 도 같다.

### 4-7. 출처

- 데이터: `tasks.source_action_item_id` → 응답 `lineage.source_action_item_id`(`application.py:2843`). 같은 `lineage` 에 `request_thread_id`·`source_work_request_id`·`source_decision_item_id`·`source_submission_id`·`source_review_decision_id`·`source_task_id` 가 함께 온다(`:2836-2845`).
- 상세의 `origin`(`_origin_projection`, `application.py:2458-2500`)은 아래 우선순위로 **하나만** 고른다.

| 순서 | 조건 | `kind` | `actor_role`/`actor` | `source` |
|---|---|---|---|---|
| 1 | `source_work_request_id` 있음 | `work_request` | 「요청자」 / 요청자 | `{type:"work_request", id, title}` — 요청을 읽을 수 있을 때만 |
| 2 | `source_action_item_id` 있음 | `self_created` | 없음 | `{type:"action_item", id, title}` — `action.read` 가 있고 **그 제안의 주인**일 때만(`:2515-2523`) |
| 3 | 직접 배정 | `direct_assignment` | 「배정자」 / 배정자 | 없음 |
| 4 | 그 밖 | — | — | **`origin` 자체가 없다**(`:2490-2493`) |

- 「AX 제안에서 생성됨」은 **화면 문장**이다. `origin.source` 가 있고 `actor` 가 없을 때 나온다(`F/features/work/WorkModals.tsx:384-390`). 링크는 `source.type === "action_item"` 이면 판단 항목 상세(`pushDetail({kind:"action", actionItemId})`)를, `work_request` 면 요청 상세를 연다(`F/features/work/MyWorkPage.tsx:693-707`).
- **링크가 가리키는 것은 원 AX 초안(ActionItem)이다.** 원 대화나 원 업무가 아니다. ActionItem 행에는 `conversation_id`·`turn_id` 가 있지만(`B/platform/persistence.py:781-782`) `origin.source` 에는 실리지 않는다. `source.title` 은 생성된 업무 이름 라벨이다(`subject_label`, `B/platform/actions.py:437-438`).
- `origin_kind` 열(생성 경로)도 응답에 따로 온다: `direct`·`request_effect`·`meeting`·`project_plan`·`assignment`(`B/platform/work_tasks.py:405`, `:2023`, `:2407`, `:2552`).
  - 회의 승격 업무는 요청을 거치므로 `origin.kind = work_request` 다.
  - 하위 업무는 `origin` 에 따로 표시되지 않고 `parent`(상세 `_hierarchy_view`)로 나온다.
  - 업무 요청에서 나온 업무에 AX 출처가 있어도 `origin` 은 요청 쪽을 고른다(2차 조사와 같다).

### 4-8. 업무 상세 응답(`GET /api/tasks/{id}`) — 개편 화면이 쓸 값

라우트 `B/entrypoints/http.py:2025`. 담당자에게는 `_with_checklist`+`access:"owner"` 를, 관계자에게는 `_related_view`+`access:"read_only"` 를 준다(`application.py:1117-1189`, `:2694-2709`). 타입 `TaskDetailResult`(`B/modules/work/task_results.py:248-270`).

| 화면 값 | 응답 키 | 있나 |
|---|---|---|
| 진행 상태 | `state`(4값 투영) + `derived.approval`·`derived.assignment`·`derived.proposal` | ○ (`application.py:2797`, `:1230-1243`) |
| 막힘 사유 | `block_reason` | ○ |
| 담당 | `assignee{member_id, display_name}` + `assignment{assignment_id, kind, status, assigned_by, accepted_at}` | ○ (`:2701-2702`, `:2895-2915`) |
| 담당 후보 | — | ✕ (별도 `GET /api/task-assignment-candidates`, `task.assign` 필요) |
| 시작 예정일 / 마감일 | `start_date` / `due_date` | ○ |
| 실제 시작일 / 완료일 / 재개일 | `started_at` / `completed_at` / `reopened_at` | ○ (`:2813-2815`) |
| 버전 | `version` | ○ |
| 출처 | `origin`, `origin_kind`, `lineage` | ○ (4-7) |
| 선행 | `preceding_task_ids[]`, `predecessors[{task_id, title, state}]`(읽을 수 없는 것은 `title`·`state` 가 `null`) | ○ (`:2822-2830`, `:1454-1477`) |
| 선행 막힘 여부(불리언·미완 목록) | — | ✕ — 화면이 `predecessors[].state` 로 계산한다 |
| 하위 막힘 | `derived.blocking_children[{task_id,title,why}]` | ○ |
| 결재자·참조자 | `approver_id`, `cc_member_ids` | ○ (id 만, 이름 없음) |
| 상위·하위·후행 | `parent`, `children`, `child_progress`, `successors`, `hidden_successor_count` | ○ |
| 체크리스트·참고·전달 | `checklist`, `checklist_progress`, `references`(owner 갈래만), `delivery` | ○ |
| 지금 할 수 있는 명령(허용 전이·편집 가능 여부) | — | ✕ — 서버가 만들지 않는다(`allowed_commands`·`can_edit` 0건). `access` 하나로 쓰기 범위만 가른다 |
| 업무 취소 가능 여부(수락된 요청 업무) | — | ✕ — 시도하면 409 |

## 5. R5 선행업무 막힘 규칙

### 5-1. 서버 판정

- **판정한다.** 판정 자리는 `transition_task` 하나다(`B/modules/work/lifecycle.py:107-140`). 입력은 application 의 `_predecessor_gate`(`B/modules/work/application.py:1415-1430`, 호출 `:2072`)다. 「미완」은 끝나지도 취소되지도 않은 활성 선행이다. 취소된 선행은 막지 않는다(`:1432-1442`).
- **막는 전이**: `state == open` 이면서 목표가 `in_progress`(시작) 또는 `done`(직행 완료)일 때만 막는다. `in_progress→done`, `blocked→in_progress`, 취소, 완료 보고, 재개는 **막지 않는다**(`lifecycle.py:119-124`, `:130-133`).
- **거부 응답**: `TaskPredecessorsUnfinished`(`B/modules/work/errors.py:175-188`) → **409**(`B/entrypoints/http.py:558`, 409 묶음 `:541-574`).
  - 본문은 `{"detail": "끝나지 않은 선행업무가 있습니다: A, B, C"}` 다. 이름은 **읽을 수 있는 선행만, 앞 3개까지** 싣는다. 읽을 수 있는 것이 없으면 `"끝나지 않은 선행업무가 있습니다"` 다(`lifecycle.py:134-139`, `application.py:1425-1430`).
  - **문장이 서버에서 온다.** 예외에 `blocking`(title 튜플) 속성이 있지만 HTTP 본문에는 실리지 않는다. 매핑이 `detail=str(error)` 다(`http.py:574`).
  - 판정이 회차 검사보다 **먼저** 돈다(4-3).
- **모든 진입이 같은 게이트를 지난다**: HTTP `task_transition`(`http.py:2535-2539`), MCP `transition`(`B/entrypoints/mcp.py:1204`, `:2089`), 시나리오·데모(`B/bootstrap/scenario.py:290`, `B/bootstrap/demo_work.py:50`, `:64`, `:281`) 모두 `TaskApplication.transition` → `transition_task` 다.
- 선행에 걸린 다른 규칙도 있다: 남은 선행이 있으면 프로젝트를 바꿀 수 없다(`TaskProjectLockedByPredecessors` 409, `application.py:554-569`). 같은 프로젝트·자기 자신·중복·순환 검사(`B/modules/work/errors.py:137-165`, `application.py:1341-1413`).

### 5-2. 상세 응답의 막힘 정보

- `preceding_task_ids[]`(활성 선행 id, `application.py:2822-2830`)와 `predecessors[{task_id, title, state}]`(`:1454-1477`)뿐이다. 서버는 「막혔다」 불리언·미완 목록·안내 문장을 **주지 않는다.**
- 그래서 지금 상세의 빨간 박스(「시작할 수 없습니다」 머리글·「끝나지 않은 선행 n건」)와 푸터 문구(「끝나지 않은 선행업무가 있습니다: …」)는 **프론트가 `predecessors[].state` 로 만든 것**이다(`F/lib/labels.ts:339`, `:446`, `:455`; 조건 `F/features/work/WorkModals.tsx:1348`, `:2051`, `:2672`, `F/features/work/workRows.ts:102`). 서버 409 문장과 화면 문장은 글자가 같은데, 출처는 서로 다르다.

### 5-3. 같은 규칙을 판정·노출하는 자리 전부

| 자리 | 판정 / 노출 | 근거 |
|---|---|---|
| 상태 전이(HTTP·MCP·AX 확인 카드) | **판정**(유일) | `lifecycle.py:130-140` |
| 업무 상세 | 노출: `predecessors[]`(제목·상태) | `application.py:1170`, `:2704` |
| 업무 목록·내 업무(`/api/tasks`, `/api/my-work`) | 노출: `preceding_task_ids` 만(상태 없음) | `application.py:1108` |
| 프로젝트 상세 `tasks[]` | 노출: `preceding_task_ids` 만 | `B/modules/work/projects.py:378`, `:445` |
| 판단함·수신함·알림 | **없다** (선행 관련 키 0건) | — |
| AX 지시문 | 생성 때 `preceding_task_ids` 를 「한 후보로 확정될 때만」 채우라는 문장뿐. 막힘 안내 문장은 없다 | `B/platform/codex_cli.py:475`, `B/modules/ax_execution/tool_catalog.py`(필드 나열 2건) |

## 6. 공통 — 계약 테스트·journey

| 요청 | 백엔드 테스트(파일) | 프론트 e2e 스크립트(`frontend/scripts/*-e2e.mjs`, 39개 중) |
|---|---|---|
| R2 내보내기 | `T/contract/test_meeting_finalize.py`(`:1145-1176`, `:1374` — html·content-type·422·404. **`Content-Disposition` 단언은 0건**). 자료 `inline/attachment` 는 `T/contract/test_meeting_materials.py`. 쿠키 `T/contract/test_auth_sessions.py`·`test_authentication.py` | 내보내기를 여는 스크립트 0건 |
| R3 회의 정보 PATCH | `T/contract/test_meeting_core.py`(4) · `test_meeting_rooms.py`(1) · `test_meeting_time_overlap.py`(1) · `test_unified_commands.py`(1, `meeting_update`). 후보: `test_meeting_finalize.py`, `T/unit/test_meeting_domain.py`, `T/unit/test_meeting_finalize_service.py`, `T/contract/test_codex_cli.py`·`test_claude_cli.py` | 「제목 후보/제목 없는 회의」 0건 |
| R4 업무 PATCH | `.patch("/api/tasks/…")` 쓰는 파일 7: `T/contract/test_task_update_contract.py`(2) · `test_answer_resources.py`(2) · `test_assignment_decision_replay.py`(2) · `test_legacy_assignment_confirmation.py` · `test_task_fields_and_materials.py` · `test_task_origin.py` · `test_task_parent_change.py` | PATCH 를 직접 부르는 스크립트: `task-checklist-e2e.mjs`, `task-detail-layout-e2e.mjs` |
| R4 전이 | `/start` 31파일(회의 `/start` 포함) · `/complete` 10 · `/cancel` 11(대화 취소 포함) · `/block` 2(`test_task_history.py`, `test_task_schedule_release.py`) · `/resume` 0. 주요: `T/contract/test_task_lifecycle_v2.py`(+`_support`), `test_task_due_date_fill.py`, `test_task_transition_confirmation.py`, `T/unit/test_task_lifecycle.py`(stale 422) | `access-roles` · `graph-question` · `subtask` · `task-delivery` |
| R4 담당 변경 | `/reassign` 9파일: `test_task_commands.py` · `test_task_lifecycle_v2.py` · `test_assignment_decision_replay.py` · `test_projects.py` · `test_project_membership_follows_work.py` · `test_task_actor.py` · `test_task_checklist_read_scope.py` · `test_task_creation_contract.py` · `test_answer_resources.py`. 후보 목록 6파일(`test_task_assignments.py` 등) | — |
| R4 출처 | `source_action_item_id`: `test_action_center.py` · `test_task_creation_contract.py` · `test_task_origin.py` | `task-origin-e2e.mjs` |
| R4 상세 전반 | `"/api/tasks/{…}"` 를 쓰는 contract 26파일(+ postgres 통합 3) | 업무 상세를 다루는 스크립트 14: `task-detail-layout` · `task-history` · `task-origin` · `task-reference` · `task-checklist` · `task-delivery` · `subtask` · `calendar-tasks` · `chat-checklist` · `chat-lifecycle` · `ax-editable-task` · `ax-action-materials` · `material-search` · `relation-graph` |
| R5 선행 | `T/contract/test_task_predecessors.py`, `T/unit/test_task_predecessor_gate.py`(`TaskPredecessorsUnfinished`), `T/contract/test_project_membership_follows_work.py`(문장). `preceding_task_ids` 13파일 | 선행을 다루는 스크립트 0건(프론트 단위 `F/features/work/Predecessors.test.tsx`, `TaskDetailRelations.test.tsx` 가 박스·문장을 단언) |
| 인벤토리 | `T/architecture/test_operation_inventory.py` ↔ `docs/unified-operations-inventory.json` | — |
| 기타 | `T/legacy_acceptance.py`, `T/integration/postgres/test_postgres_integration.py`·`v2_pg_support.py`(전이·reassign) | — |

## 7. grep 개수표

| 요청 | 심볼 / 패턴 | 범위 | 개수 |
|---|---|---|---|
| R2 | `Content-Disposition` | `B/entrypoints/http.py` | 7 |
| R2 | `attachment; filename*=` | 같음 | 6 |
| R2 | `"inline" if inline` | 같음 | 1 |
| R2 | 파일 응답 라우트(`/export`·`/content`) | 같음 | 7 |
| R2 | `samesite` | `B/entrypoints` | 1 |
| R2 | `CORSMiddleware` | `B/` | 0 |
| R2 | `X-Demo-Persona` | `B/entrypoints` | 4 |
| R2 | `credentials: "same-origin"` 류 | `F/lib/api.ts` | 7 |
| R2 | `download` / `on_download` | `S/src` | 0 / 0 |
| R3 | `title_candidate` | `B/` | 22 |
| R3 | `제목 없는 회의` | `B/` | 16 |
| R3 | `TITLELESS` | `B/` | 10 |
| R3 | `meeting.title =` (회의 제목 쓰기) | `B/` | 1 (+ 플랫폼 지역변수 1건 `work_tasks.py:1464` 은 쓰기 아님) |
| R3 | `meeting.title_candidate =` | `B/` | 1 |
| R3 | `@app.(post\|patch\|delete)("/api/meetings` | `B/entrypoints/http.py` | 18 |
| R3 | `.patch(…"/api/meetings/…")`(안건 제외) | `T/` | 7 (4 파일) |
| R4 | `@app.(post\|patch\|delete)("/api/tasks…` + task-assignments·task-schedules | `B/entrypoints/http.py` | 26 + 2(task-assignments) + 1(task-schedules) |
| R4 | `task.version += 1` | `B/` | 15 |
| R4 | `self._moved(` | `B/modules/work` | 13 |
| R4 | `task version is stale` | `B/` | 12 |
| R4 | `TaskEditFields` | `B/` | 8 |
| R4 | `validate_schedule(` 호출 | `B/` | 3 |
| R4 | `"task.updated"` | `B/` | 2 |
| R4 | `transition_task(` 호출 | `B/` | 8 |
| R4 | `source_action_item_id` | `B/modules/work/application.py` | 6 |
| R4 | `allowed_commands\|can_edit\|allowed_transitions` | `B/modules/work/application.py`·`task_results.py` | 0 |
| R4 | `.patch(…"/api/tasks/…")`(체크리스트 제외) | `T/` | 10 (7 파일) |
| R5 | `TaskPredecessorsUnfinished` | `B/` | 6 |
| R5 | `_predecessor_gate(` | `B/` | 2 (정의 1, 호출 1) |
| R5 | `predecessor_views(` | `B/` | 2 |
| R5 | `"predecessors":` 응답 키 | `B/` | 2 |
| R5 | `끝나지 않은 선행업무가 있습니다` | `B/` · `F/`(테스트 제외) | 1 · 1 (`labels.ts:339`) |
| R5 | `시작할 수 없습니다` | `F/`(테스트 제외) | 3 (`labels.ts:446` + 주석 2) |

## 8. 조사 한계

- **R2 원인은 코드를 읽고 낸 추정이다.**
  - Tauri 앱을 띄우지 않았다(금지). WKWebView 가 `Content-Disposition: attachment` 인 `text/html` 응답에 delegate 가 Allow 를 줄 때, 문서를 웹뷰 안에 띄우는지 무시하는지는 WebKit 쪽 동작이다. 그래서 확정하지 못했다. 확실한 것은 「셸에 다운로드 핸들러가 없고, wry 는 핸들러가 없으면 Download 정책을 내지 않는다」는 것까지다.
  - Windows(WebView2)는 wry 의 `webview2` 경로를 읽지 않았다. WebView2 는 핸들러가 없을 때 자체 다운로드 UI 를 띄울 수 있어 결과가 다를 수 있다.
  - 운영 인그레스 설정(`/api` 분기, 응답 헤더 가공 여부)은 레포 밖이라 보지 못했다.
- 운영의 `Settings.profile` 이 `PRODUCTION` 인지(= 쿠키 `Secure`)는 배포 환경값이라 확인하지 못했다.
- R3: 회의 상세 화면이 `title_candidate` 를 어디에 어떻게 그리는지는 frontend 리포트 몫이라 읽지 않았다. 감사 `append_audit` 가 쓰는 표의 열은 열어 보지 않았다.
- R4: 「편집」 모달 저장 버튼이 한 번에 어떤 키를 묶어 보내는지(제목·내용·날짜를 한 PATCH 로 보내는지)는 frontend 몫이다. `updateTask` 본문 구성만 확인했다(`F/lib/api.ts:255-266`).
- R4: `done` 업무에 `/resume`·`/start` 를 부르면 `transition_task` 허용표를 지난다는 것은 코드 읽기 결과다. 그 경로를 단언하는 테스트가 있는지는 찾지 않았다.
- R4-4: 배정 수락 판단 항목(`_open_assignment_acceptance`)이 판단함 목록 API(`/api/action-items`)에 어떤 모양으로 실리는지는 끝까지 따라가지 않았다(`B/platform/work_tasks.py:2453-` 이후).
- 테스트 개수는 파일 단위 grep 결과다. 헬퍼 함수를 거쳐 같은 API 를 부르는 테스트는 빠졌을 수 있다(예: `_support.py` 경유).
- 테스트·빌드를 돌리지 않았으므로 위 테스트들이 지금 통과하는지는 모른다.

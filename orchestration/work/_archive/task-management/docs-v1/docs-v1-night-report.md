# 밤샘 진행 보고 — 2026-09-07 밤 → 09-08 아침 (코디 자율 진행)

사용자 지시(09-07 밤): 「발주 · 검증 · 수정 · 발주 … 전체 다 끝내고 문제는 한번에 취합해서 아침에 보고」.
순서 WORK-009 → 010 → 011 → 012 → 013 → 014. WP 마다 backend/frontend 발주 → 코디 실물 검증 → 필요 시 수정 발주 → reviewer → 수정.

## 0. 아침에 볼 것 — 한눈에

| WP | 상태 | 커밋 | 테스트 | 사용자 결정 필요 |
|---|---|---|---|---|
| 009 MCP · 토큰 | **done** | `0b3f7b7` | pytest 564 · mcp 40 · compose 5 healthy · Phase 4 실측 | — |
| 010 회의 시작 | **done** | `329fda6` | pytest 595 · /start 7ms | 앱 창 실측(§6 AC) 아침 |
| 011 회의 중 | **done** | `f70a094` | pytest 611 · tsc 0 · vitest 315 · 검수 FAIL 0 WARN 4 | 앱 창 실측 아침 · SPEC-007 U-3 문장 하나(아래) |
| 012 회의 종료 | **done** | `0415290` | pytest 628 · tsc 0 · vitest 327 · 검수 FAIL 0 WARN 4 | SYS-OQ-5 **통과** · §1 항목 셋(errorCode 재진입 · progress.phase 규칙 · 안내 바 시각) · 앱 창·300분 실측 아침 |
| 013 편집 | **done** | `bfde960` | pytest 638 · tsc 0 · vitest 340 · 검수 FAIL 0 WARN 2 | null 키 규칙(§2) · 업무 드로어 「현재 값」 둘 · 본문↔제목 동기화 규칙(§1) · 앱 창 실측 아침 |
| 014 목록·상세 UI | **done** | `5c72c25` | tsc 0 · vitest 360 · 검수 FAIL 0 WARN 2 | 앱 창 네 폭 실측 · 「홈」 라우트(§1) |
| (아침) 스키마 400 | **done** | `dd9d861` | pytest 640 · 실물 회의 9 성공 | — |
| (아침) LineRow 정렬 | **done** | `aa375ed` | tsc 0 · vitest 363 | 앱 창 확인 |
| 015 중간 배치 AI 혼자(MF-71) | **done** | `1ca243e` | pytest 652 · 검수 FAIL 0 WARN 2 | 웜스타트 phase(§1) · 실물 회의로 톤 확인 |

## 1. 사용자 결정이 필요한 것 (코디가 정하지 않고 우회한 것)

- **아침 실물 확인(앱 창)** — 워커들이 `tauri dev` 를 못 띄운다(흰 화면/404 · 브라우저 자동화 없음). 앱 창 항목은 전부 아침에 사용자가: WORK-010 「워커 내린 채 회의 시작」 · **WORK-011 슬래시 5 · 좁혀지는 팝오버 · 배치 교체(실제 Soniox + 워커 필요)** · 이후 WP 도 같음
- **SPEC-007 U-3 「안건 없음」 절에 팝오버 규칙이 없다**(WORK-011 검수 문서 공백 3). 구현은 — 안건 0개면 팝오버 머리에 「안건이 없습니다 · 새 안건을 만들어 기록을 시작합니다」, 항목은 `/새안건` 뿐, 슬래시도 `/새안건 ` 만 칩. 이 문장을 U-3 에 넣으면 되는지 한 줄 확인(코디는 SPEC 을 고치지 않았다 — 결정 아님·문장 추가라 아침에)
- **SPEC-008 U-2 실패 배너 「사유 툴팁 = job.errorCode」 인데 새로고침으로 들어오면 사유를 얻을 길이 없다**(WORK-012 fe 보고). 상세 응답의 `activeJobId` 는 queued/running 만이라 실패 뒤 재진입에는 job 이 없다. 프론트는 사유 없이 배너만 그린다(다른 데서 끌어오지 않음). 답 후보 — (a) 상세에 마지막 종결 job 의 `errorCode` 를 파생값으로 싣는다 (b) 툴팁은 같은 세션에서만. 코디는 정하지 않았다
- **SPEC-008 §4 `progress.phase` 파생 규칙이 「② 가 돌고 있다」를 표현하지 못한다**(WORK-012 검수 W-2). 규칙 = `meeting_batch_run(phase='final')` 행이 생기면 `final` 인데, 그 행은 ② 시도가 **끝날 때**(실패 기록 또는 `_commit_success` 안) 생긴다. 그래서 성공 경로에서 「회의록을 정리하고 있습니다」가 한 번도 안 뜨고 ① 문구가 끝까지 남는다. 코드는 규칙대로다. 답 후보 — (a) ② 첫 시도 **시작** 때 job 에 phase 를 찍는다(파생 → 저장) (b) ① 성공 = `meeting_transcript` 재전사 행이 생긴 시점부터 `final` 로 파생. 코디는 정하지 않았다
- **AI 안내 바 「배치 n회 반영 · HH:MM」의 시각 원천이 상세 응답에 없다**(WORK-012 fe 보고 · 검수 D-3). `integratedAt` 이 MF-56 으로 사라진 뒤 대체가 없어 프론트는 시각 없이 「배치 n회 반영」만 그린다. SPEC-007 U-4 문구를 시각 없이 확정할지, `meeting_batch_run` 최신 행 시각을 파생값으로 실을지
- **업무 payload 드로어의 「현재 값」 둘(프로젝트 · 완료 결과)이 줄의 `task` 요약에 없다**(WORK-013 fe 보고). 기한·상태는 요약에서 그리는데 그 둘은 응답에 없어, 회의록이 업무 상세를 새로 읽지 않고(영역 경계) payload 값이 있을 때만 채우고 없으면 「변경 없음」으로 둔다. 현재 값을 보여 주려면 SPEC-008 §4 줄 `task` 요약에 `projectId` · `completionResult` 를 더해야 한다 — 코디는 정하지 않았다
- **줄 본문과 업무 제목의 동기화 규칙이 SPEC 에 없다**(WORK-013 검수 문서 공백 2). 서버는 업무 제목으로 줄 본문을 덮지 않고(MF-62), 넣기 뒤 업무 제목이 바뀌어도 줄 본문은 그대로다. 코드가 그 자리에 「SPEC 에 없다」고 적어 두었다. 「동기화 없음」을 SPEC-008 §5 에 한 줄로 못박으면 되는지
- **breadcrumb 「홈」이 가리킬 라우트가 없다**(WORK-014 검수 W-2). 지금 `HOME_ROUTE = TASKS_ROUTE = /tasks/` 라 `/tasks/` 목록에서 「홈」이 자기 페이지로 가는 링크로 렌더된다(Breadcrumb 자신의 「자기 링크 없음」 규칙과 어긋남 · 코드에 「홈은 아직 /tasks/ 다」 주석). 홈 화면을 만들지 · 「홈」 칸을 뺄지 · 링크를 안 걸지 — 문서에 없다
- **`tauri dev` 흰 화면 — 워커 넷이 전부 못 띄움**(011 · 012 · 013 · 014). `next dev` 는 200 인데 웹뷰에 React 가 마운트되지 않는 것으로 보인다(`MinWidthGuard` 문구조차 없음). 워커 변경과 무관해 보이나 원인은 안 찾았다 — 아침에 사용자 환경에서 먼저 띄워 보고, 안 뜨면 그것부터
- **웜스타트의 도구 세트(MF-71 이 안 정함)** — WORK-015 는 웜스타트를 `final`(일곱)로 두었다(도구 목록만 알려 주는 자리 · 실제 잠금은 매 제출의 `-c`). 회의 중 역할을 설명하는 자리라 `batch`(셋)가 맞다고 보면 한 자리만 바꾼다
- **입력 레벨을 사용자에게 보여줄 것인가**(버그 3 조사 (a)) — 마이크가 조용하면 전사가 안 나오는데 화면엔 아무 표시가 없다. 프론트 AnalyserNode 레벨 막대는 계약 변경 없이 가능. SPEC-007 U-1 에 자리가 없다
- **60초 무토큰 안내**(버그 3 조사 (b)) — WS 프레임으로 하면 SPEC-007 §4 계약 변경 · 프론트 단독(레벨 기반)이면 변경 없음. 어느 쪽인지
- ~~WORK-010 SPEC-007 §6 AC~~ → 위 항목에 포함. 원문: WORK-010 SPEC-007 §6 AC 「워커를 내린 채 「회의 시작」을 눌러도 즉시 회의 중 화면」: 워커가 앱 창을 못 띄워 REST 7ms 까지만 실측. 앱 창에서 한 번 눌러 보면 끝(Done Criteria 캡처)

## 2. 코디가 판단해서 진행한 것 (뒤집을 수 있다)

- **회의 토큰 allowlist**(WORK-009 검수 F-1 · W-2 · D-7) — 회의 토큰으로 열리는 표면은 여섯뿐(`/current` · `/current/tasks` · 자기 회의 `GET /{id}` · `GET /api/tasks/{id}` · `GET /api/work-types` · `GET /api/auth/session`), 그 밖은 목록·jobs·쓰기 전부 404. 검수가 「문서에 규칙이 없다」고 올린 자리 — WP §Internal Interface · SPEC-007 도구 불릿에 적음
- **도구 인자 이름 = 스네이크**(D-4) — 실물 `project_id` · `agenda_id` · `task_id`. SPEC-007 도구 불릿에 한 구절
- **부분 인덱스는 비유니크**(D-6) — 회의당 하나는 `start()` 상태 게이트가 지킨다. DB README §4 · WP 에 명시
- **「로그에 원문 없음」= back 로그**(D-3) — 워커 JSONL 에는 `-c` 로 남는 게 설계. WP Pre-deploy 에 명시

- **`/finalize` 재시도가 회의 토큰을 새로 발급**(WORK-012 backend 질문 · 09-08 새벽) — WP 「② 종결 시 폐기(성공·실패 무관)」 와 SPEC-008 「/finalize 는 ①부터 다시」 가 부딪혀 재시도 ② 가 토큰 없이 죽는다(워커가 실측). TTL 이 분 단위라 「실패 시 안 지움」은 답이 안 됨. `finalize()` 가 `/start` 와 같은 `issue_meeting_token` 을 부르고, 남은 행이 있으면 지우고 내서 **회의당 하나**(A-13)를 유지. WP-012 §Internal Interface · A-13 발급 불릿에 한 줄씩 적음. 새 결정 아님(MF-69 의 귀결)
- **payload 변경분 키 `null` 은 422**(WORK-013 backend 미결 4 · 09-08) — 「보내지 않음 = 변경 없음」이고 「비운다」는 값이 SPEC-008 §4 에 없어 워커가 막았다. AI 가 저장한 payload 에는 `completionResult: null` 이 들어올 수 있어(SPEC 예시) 사람 쓰기 표면과 AI 저장값의 허용 범위가 다르다. 코디 = 프론트는 채워진 키만 보낸다(013 fe 브리프 §3). SPEC-008 §4 에 「사람 쓰기 표면은 null 키를 받지 않는다」 한 줄이 필요한지는 아침에 — 결정은 아님
- **`PAYLOAD_STATUSES` 가 「모든 상태 − cancelled」 라 `done` 이 스키마 층을 지나고 있었다**(WORK-013 backend 미결 1) — 워커가 `PayloadStatus{todo,in_progress}` 로 좁혀 8-c 구멍을 닫았다. WORK-012 가 만든 상수였고 검수도 놓쳤다
- `/current/tasks` 회의 토큰 전용 표면 신설(WORK-009 워커 질문 3) — 화면용 `GET /api/tasks` 는 기간 기본값이 「오늘」이라 도구에 안 맞았다

## 2-1. 준비된 브리프 (발주 순서대로 쓴다)

`docs-v1-work011-fe-brief.md` · `work012-be` · `work012-fe` · `work013-be` · `work013-fe` · `work014-fe`. 각 WP 는 be → 코디 검증 → fe → 코디 검증 → reviewer → 수정 → 커밋.

## 3. WP 별 검증 기록

### WORK-009

- backend 완료(`task_acf1c6405461`). 코디 실물 검증 — `make test` 557 passed · Errors 0 · `app/mcp` pytest 40 · compose db/redis/api/worker/mcp 전부 healthy · 정적 검사 4종 0건(원문 노출 0 · 옵션 빌더 파일 1 · mcp 의 back import 0 · 쓰기 메서드 0) · `-c` 목록 문자열·순서 = WP 계약 · 리비전 0007 · `/current` · `/current/tasks` 있음
- 워커 미결 6건 — (1)(2)(3) 코디 답 그대로 (4) `dto/account.py` 가 없어 `dto/auth.py` 에 둠 (5) mcp SDK 2.x 상한 · `MCPServer` 가 예외 메시지를 가려 `BackendError`/`AgendaNotFound` 만 `ToolError` 로 통과 (6) 로컬 `.env` 에 env 3줄 + `CODEX_AUTH_JSON` 따옴표(공백 경로 · 기존 문제)
- reviewer 발주 → 결과 뒤 수정 → 커밋
- reviewer 완료 — **FAIL 1**(회의 토큰으로 `GET /api/meetings` 목록 열림 — 범위 검사가 경로 `{meeting_id}` 있을 때만) · WARN 7(404 문구 · jobs 열림 · worker 가 mcp 안 기다림 · `"none"` 센티널 service 까지 · 리비전 왕복 테스트 없음 · 목록 테스트 없음 · Phase 4 증거 파일 없음) · 문서 공백 7. 리포트 `work009-review-report.md`
- 코디 — 문서 공백 D-1~D-7 전부 고침(system·backend 「해시만」→원문 · WP 14줄 · allowlist 규칙 · 로그 범위 · MCP_PORT env · 비유니크 인덱스 · SPEC-007 인자 스네이크). 수정 브리프 `docs-v1-work009-fix-brief.md` → backend 워커 재발주(`task_49eea1287805`)
- 수정 완료(`task_49eea1287805`) · 코디 재검증 — `make test` 564 passed(리비전 왕복 slow 테스트 포함) · service 에 `"none"` 0 · `deps.py` allowlist 여섯 · worker→mcp `service_healthy` · Phase 4 증거 `work009-phase4-evidence.md`(codex 0.147 이 `-c mcp_servers.tm.url` 로 HTTP MCP 를 붙여 `list_agendas` · `list_work_types` 실제 호출 · 도구 밖 0건 · revoke 뒤 401)
- WORK-009 문서 done · 커밋(아래) → WORK-010 발주
- 커밋 `0b3f7b7` feat: WORK-009. `tauri.conf.json`(사용자 실물 확인 변경)은 그대로 둠

### WORK-010
- backend 완료(`task_d346f74a28e3`). 코디 검증 — `make test` 595 passed · `meeting_service.py` `commit(` 0 · `load_warm_start_context|WarmStartContext|_task_rows` 0 · 프롬프트(2,326자 · 여섯 절 · 도구 7 · 용어 다섯 · JSON 0 · 「준비됨」) · `/start` 실측 7ms(옛 5.6초) · `ai_session_id` 응답 뒤 ~4초에 백그라운드가 채움
- 워커 미결 — (1) **앱 창 실측(SPEC-007 §6 AC 「워커 내린 채 회의 시작」)은 REST·DB·워커 로그까지만** — 아침에 사용자가 앱 창에서 확인 (2) `wait_for_tasks` 테스트 격리용 함수가 프로덕션 파일에(프로덕션 경로 미호출) (5) `_run_once` 의 `ai_session_id` 없음 RuntimeError 는 그대로 — SPEC-007 검증 0 「조용한 미제출」로 다듬는 건 WORK-011 브리프에 넣음
- reviewer 완료 — FAIL 0 · WARN 6(`reset_state` 가 `_tasks` 안 비움 · 죽은 import 2 · 단언 · needle · `wait_for_tasks` 프로덕션 파일 · Phase 2 로그 캡처) · 문서 공백 4(코디가 고침 — WP needle · Code Surface 테스트 파일명 · BE §5-3 「웜스타트는 스윕 대상 아님」). 커밋 `329fda6`. WARN 넷은 WORK-011 backend 브리프 첫 항목으로

### WORK-011
- backend 완료(`task_f7b5bf32087b`). 코디 검증 — `make test` 611 passed · `meeting_notes.json` 한 벌(top: headline·termCorrections·agendas / agenda: humanAgendaId·title·lines / line: kind·content·detail·evidence·taskId·payload) · `meeting_batch.json` 폐기 · `_persist` 안에서만 DELETE 2건 · `_load_input` 컨텍스트 조회 0 · `meeting_batch_chars` 1000 · `AiBatchMessage` 최상위 `lines` 0 · 백엔드 슬래시 파싱 0. WORK-010 WARN 4 정리 포함
- 워커 미결 — (1) **프론트가 아직 옛 `ai.batch` 를 본다 → be+fe 를 한 커밋으로** (2) `payload` 이름은 WORK-012 리비전에서 (4) `run_final` 계열은 과도기(옛 컨텍스트) — 012 가 폐기 (5) 워커 로그 실측 안 함 — 프론트 뒤 reviewer 가 본다
- frontend 완료(`task_a99f3ee113d7`). 코디 검증 — tsc 0 · vitest 35 files/315 · `LineRow` `formatClock` 0 · `orphaned` 0(정적 테스트 파일 제외) · `fetch(` 직접 0(`refetch()` 오탐). 앱 창 실측은 워커가 `tauri dev` 흰 화면으로 중단(코디 A 지시) → 아침
- reviewer 발주(be+fe · `task_c67cdeecbd65` · `ctx_c6fcdd4cf827`)
- reviewer 완료 — **FAIL 0 · WARN 4 · 문서 공백 4**. 리포트 `work011-review-report.md`. 축 여섯 전부 PASS(배치 입력 컨텍스트 0 · 검증 0~5 표와 1:1 · 스키마 한 벌 · 과도기 지운 것 0 · 슬래시/통째 교체/줄 시각 · BE §12 6·7·7-a). WARN — (1) `build_final_prompt` 두 문장이 새 스키마로 바뀜(불가피 — 안 바꾸면 최종 100% discarded) (2) `find_ai_agenda_by_source` 호출 0 죽은 함수 (3) `_parse_output(fill_final=True)` 가 `NotImplementedError` (4) 「같은 직렬화 함수」 정적 검사 없음. 문서 공백 — fill_final 뜻 · 초안 §B 「새로 드러난 것만」 정정 표시 없음 · U-3 안건 없음 팝오버 · repository 죽은 함수 폐기 규약
- 코디 — 코드 수정 없이 커밋(막을 무게 없음). WARN (1)(2)(3)(4) 와 fill_final 뜻은 **WORK-012 be 브리프 §2 에 접어 넣음**(구현·삭제·정적 검사·「새로 드러난」 0). 초안 §B 에 정정 블록 추가(MF-53 · 기록용). U-3 는 §1 아침 항목. repository 폐기 규약은 안 만듦(012 가 그 함수를 지우거나 쓰면 끝)
- **커밋 `f70a094`** feat: WORK-011(be+fe 한 커밋). WP-011 done · README done. `tauri.conf.json` 은 그대로 둠

### WORK-012
- backend 발주(Phase 0·1·2 · `task_517a5eaa4f59` · `ctx_38e66c02300e` · `docs-v1-work012-be-brief.md` + WORK-011 검수 WARN 4 접음)
- **워커 질문(새벽)** — ② 종결 폐기 vs `/finalize` 재시도 토큰. 코디 답 = `finalize()` 가 같은 `issue_meeting_token` 으로 재발급 · 남은 행 지우고 · 회의당 하나(§2 에 기록)
- backend 완료(`task_517a5eaa4f59`). **SYS-OQ-5 실물 통과** — 헤더 없는 webm 을 `stt-async-v5` 가 그대로 받음(토큰 307 · 9.1초 · 화자 3 · 블록 6 화자 변경 경계 · 컨테이너 안 바꿈). 코디 검증 — `make test` **626 passed** · 정적 금지 심볼 0(옛 리비전 0005/0006 본문·테스트 제외) · `find_ai_agenda_by_source` 삭제 · `meeting_notes.json` 하나 · `termCorrections` 항목 `{stt,correct,grade}`(SPEC-008 §4 대로 — WORK-011 이 `{from,to}` 로 둬서 최종이 못 지나던 것을 고침) · 블록 상수 한 파일(300 · 2000) · 리비전 0008 왕복 테스트 · `/integrate` → `/finalize` · `finalize()` 재발급(revoke → issue) · 종결 revoke · httpx 런타임 의존
- 워커 미결 — JSONB `none_as_null=True`(없으면 파이썬 None 이 `'null'` 로 들어가 자리 CHECK 가 멀쩡한 줄을 막음 — 실측) · 자리 밖 옛 payload 는 마이그레이션이 먼저 NULL · `job_timeout_sec` → `meeting_job_timeout_sec` · job 상한 테스트는 `test_job.py` 하나(두 벌이면 handler 대역 충돌) · 300분 실물 · 워커 로그 · 앱 창은 안 함(아침)
- 코디 질문 — 증거 파일이 어느 워크트리에도 없어 경로 지정 → `work012-sys-oq5-evidence.md` · `work012-be-report.md` 착지(ACCEPTED · 토큰 307 · 9.1~9.2초 · 화자 3 · sub-word 토큰 확인). 정정 — 블록 수는 실행마다 5~6(Soniox 출력이 결정적이지 않아 2초 공백 경계가 옮겨감 · 규칙 셋은 두 회차 모두 그대로) → 「재전사 결과가 결정적이라고 전제하는 테스트 금지」를 증거 파일에 남김
- frontend 발주(Phase 3 · `task_c18f7fc4ba8a` · `ctx_a72b96fc8a29`)
- frontend 완료(`task_c18f7fc4ba8a`). 코디 검증 — tsc 0 · vitest 35 files/**327** · 정적 `integrateMeeting|pendingChange|integratedAt|final_batch|/integrate` 소스 0(주석 4건뿐) · 보고 `work012-fe-report.md`(scratchpad 에서 복사). 앱 창은 `tauri dev` 흰 화면(011 과 같음) → 아침
- 워커 미결 — 새로고침 재진입 시 errorCode 없음(§1) · AI 안내 바 HH:MM 원천 없어 시각 없이 「배치 n회 반영」만 · `finalBatchState` 백엔드가 아직 내고 프론트 타입에만 남음(spec 은 09-07 에 지움 — reviewer 축 2-7 → 수정 발주)
- reviewer 발주(be+fe · `task_f01dea6947be` · `ctx_0a6680406ec2`)
- reviewer 완료 — **FAIL 0 · WARN 4 · 문서 공백 4**. 리포트 `work012-review-report.md`. 축 여덟 중 fallback 0 · 리비전 0008 · 트랜잭션/원자성 · 검증 함수 하나 · 토큰 PASS. WARN — W-1 `except Exception` 하나(BE §8-1) + 그것을 잠그던 정적 가드가 같은 변경에서 삭제 · W-2 `progress.phase` 규칙(성공 경로에서 ② 문구 안 뜸 — 규칙 쪽 문제) · W-3 `finalBatchState` 14곳 잔재 · W-4 테스트 공백 셋(②의 뿌리 · job 상한 한 벌 · 로그 실측)
- 코디 — W-1 · W-3 → 수정 발주 `docs-v1-work012-fix-brief.md`(backend `task_aa043bf36c7b` → 뒤이어 frontend 4줄). W-2 · errorCode 재진입 · 안내 바 시각 → §1. 비결정 사실 → WP-012 Open Issues
- backend 수정 완료(`task_aa043bf36c7b`) — `except SQLAlchemyError` 로 좁힘 · 정적 가드 복원(`test_no_broad_except_and_no_stream_condition_in_the_close_path`) · 「DB 오류 아닌 예외는 전파」 테스트 추가 · `finalBatchState` 백엔드 0 · 죽은 import 정리 · 워커 628 passed. 코디 grep 둘 0 확인 · make test 재실행 중
- frontend 수정 발주(`task_b6db9c916d46` · 4줄)
- frontend 수정 완료(`task_b6db9c916d46`) — 4줄 + static needle. 코디 검증 tsc 0 · vitest 327 · 소스 0. 코디 `make test` **628 passed**
- **커밋 `0415290`** feat: WORK-012(be+fe 한 커밋). WP-012 done · README done

### WORK-013
- backend 발주(Phase 1·2 · `task_f00bf29f0970` · `docs-v1-work013-be-brief.md`)
- backend 완료(`task_f00bf29f0970`). 코디 정적 — `newTask|new_task|pendingChange|PendingChange` 실행 코드 0 · `meeting_edit_service` 의 `task_service` 는 docstring 2건뿐 · `task_service` 호출은 `meeting_task_link_service` 안 여섯 함수(create · update · change_status · add_memo · add_todo · link_relations) · `.status =` 대입 0 · 리비전 0009 · 시드 description · PATCH …/task 라우트. 워커 638 passed · 코디 `make test` 재실행 중
- 워커 미결 — (1) `PayloadStatus` 로 done 구멍 닫음(§2) (2) PATCH lines 는 kind 가 없어 모양은 title 유무로 · 종류 일치는 service 422 (3) 업무 payload `{}` 유효 (4) null 키 422(§2 · fe 브리프에 반영) (5) 정적 가드 `completion_result` 예외를 link 서비스만 (6) 되감기 목표를 리비전 id 로 · `work_type_repository.update` None → UNSET
- frontend 발주(Phase 3·4·5 · `task_1867bf1689f6`)
- frontend 완료(`task_1867bf1689f6`). 코디 검증 — tsc 0 · vitest 35 files/**340** · `TaskCreateDrawer`·`TaskDetailDrawer` diff 0 · `features/tasks` 변경은 `RelationPopover` mode prop + 배럴 export 뿐 · `isAiLine|line.track ===|LineKindSelector|onChangeKind|pendingChange|newTask` 소스 0(주석 2) · Dialog 직접 import = ConfirmModal 하나. 보고 `work013-fe-report.md`. 앱 창 흰 화면(같은 증상) → 아침
- 워커 판단 셋 — `RelationPopover` 를 tasks 배럴 예외에 추가(U-9 「그대로 재사용」 · 예외 둘) · 셀렉터가 제목 자리라 sr-only 제목 · 삭제된 업무 줄 버튼은 브리프 「비활성」 대신 **SPEC-008 U-6 「업무 갱신 그대로 + 캡션」** — SPEC 이 맞다
- 워커 미결 — 업무 드로어 「현재 값」 둘 없음(§1) · 백·프론트 같이 배포
- reviewer 발주(be+fe · `task_91001cfb8c89` · `ctx_1dce7c9f9b6f`)
- reviewer 완료 — **FAIL 0 · WARN 2 · 문서 공백 2**. 리포트 `work013-review-report.md`. 축 일곱 전부 PASS(게이트 · payload≠업무 · 넣기 두 표면 원자성 · 리비전 0009 · 드로어 둘 · 편집/모달/설명 · 테스트). WARN — W-1 업무 드로어 「현재 값」 둘(§1) · W-2 드로어 파일 이름 둘이 내용과 어긋남(`CreateTaskFromLineDrawer.tsx` · `LinkTaskDrawer.tsx`). 문서 공백 — 현재 값 응답 · 본문↔제목 동기화(§1)
- **코디 실수** — 013 fe 브리프·검수 브리프에 「삭제된 업무 줄 버튼 비활성」이라 적었는데 SPEC-008 U-6 은 「업무 갱신 그대로 + 캡션」. 워커가 SPEC 을 따랐고 검수가 확인. 결과물은 맞다
- 코디 — 코드 수정 없이 커밋. W-2 파일 이름은 WORK-014 fe 브리프 Phase 0 으로 이관(같은 워커 · 동작 변경 0). 커밋 뒤 `tailwind.config.ts`(modal-light 폭)가 빠진 것을 발견해 amend
- **커밋 `bfde960`** feat: WORK-013(be+fe 한 커밋 · amend 포함). WP-013 done · README done

### WORK-014
- frontend 발주(Phase 0·1·2·3 · `task_41aaef06559f` · `ctx_c281b839f794` · `docs-v1-work014-fe-brief.md`)
- frontend 완료(`task_41aaef06559f`). 코디 검증 — tsc 0 · vitest 36 files/**360** · `router.back(` 소스 0(주석·테스트만) · `PageHeader.tsx` 0 · 트리 컴포넌트 1 · `features/tasks` diff = `TaskDetailPage` nav 교체 +3/−9 · 패널 `absolute` 0(주석만) · Phase 0 `git mv` 둘(`ActionPayloadDrawer.tsx` · `TaskPayloadDrawer.tsx`). 보고 `work014-fe-report.md`
- 워커 미결 — **앱 창 흰 화면 네 번째**(1440×900 으로 맞춰도 `MinWidthGuard` 문구조차 없음 → 웹뷰에서 React 가 마운트되지 않는 상태로 보임 · `next dev` 는 200). 네 폭 캡처 없음 — 정적·클래스 단언으로 대체
- reviewer 발주(마지막 · `task_41c42a127c60` · `ctx_70a943044161`)
- reviewer 완료 — **FAIL 0 · WARN 2 · 문서 공백 2**. 리포트 `work014-review-report.md`. 축 여섯 전부 PASS(breadcrumb/「←」 · 헤더 순서 세 화면 · CTA/크기/밀도 · 013 이관 · 금지/범위 · 테스트). WARN — W-1 네 폭 실측 없음(jsdom 은 레이아웃 계산 안 함 → 앱 창만이 길) · W-2 「홈」 자기 링크(§1). 문서 공백 — FE §6-3 부품 이름 `PageHeader` ↔ 실물 `DetailHeaderBar`(**코디가 FE README 4곳 정정**) · 「홈」 라우트(§1)
- **커밋 `5c72c25`** feat: WORK-014. WP-014 done · README done. **밤샘 발주 끝.**

## 4. 마감 상태 (09-08 새벽)

- 코드 워크트리 `kknaksss/docs-v1` HEAD `5c72c25` — 커밋 6(WP 하나에 하나 · be+fe 합침). 미커밋은 `tauri.conf.json`(사용자 CSP 변경 · 그대로 둠)뿐. **PR 안 열었다**(아침 결정이 코드에 닿을 수 있어서)
- 문서 워크트리 `task-management-app` — **미커밋**: WP-009~014 status done · `30-work/README.md` · SPEC-007/008 · 아키텍처(system · backend · database · frontend · account/meeting 도메인) · `Meeting flow.md` · `ai-prompt-draft.md` 정정 · `orchestration/work/docs-v1/`(브리프 · 리포트 · 이 보고 · `_RESUME.md`). 커밋은 아침에 사용자 확인 뒤(work/ 는 archive-work.sh 절차)
- 테스트 최종 — backend `make test` 638 · frontend tsc 0 · vitest 360 · mcp 40(WORK-009 때)
- 워커 터미널 셋 idle(backend `term_fd9fc1ce…` · frontend `term_1c173ed7…` · reviewer `term_be2a2f22…`) — 살아 있는 발주 0

## 5. 아침 실물 진행 (09-08 09:00~)

- 사용자 환경에서 `make up` · `make migrate`(0009 head) · `make app` — **앱 창이 뜬다.** 워커 넷의 흰 화면은 워커 환경 문제였다(§1 항목에서 지운다)
- 실제 회의 id 8(12.4MB webm · 세션 토큰 · 웜스타트 성공 · 안건/줄/전사 정상) — **AI 배치 2회 모두 실패.** 원인: `meeting_notes.json` 의 줄 `payload` 가 `{"type":["object","null"]}` 뿐이라 OpenAI strict 가 `additionalProperties`/`properties` 없다고 400(`invalid_json_schema`) → codex exit 1 빈 출력. **WORK-011·012 검수가 못 잡은 것 — 밤새 실물 codex 호출이 0건이었다.** 종료 ② 도 같은 이유로 실패 예정
- 워커 재시작(사용자가 `.env` 의 codex auth 경로 변경) — worker 만 `--no-deps --force-recreate`
- 녹음 원본은 명명 볼륨 `task-management-local_storage:/data/recordings/8.bin` — 사용자 요청으로 `reference/2026-09-08-real-summit/recordings/8.bin` 에 복사(git 추적 대상 — 12MB · ignore 여부는 사용자)
- backend 발주 `docs-v1-schema-fix-brief.md`(`task_75e1e1f6a5a1` · `ctx_e0c33830749a`) — 스키마 strict 규격 + 전수 테스트 · `STORAGE_HOST_DIR` 바인드 마운트 · 회의 8 `/finalize` 실측(증거 `e2e-01-real-summit-evidence.md`)
- 워커 질문 — 브리프의 `payload.status` enum 「둘+null」 은 SPEC-008 ② 검증 표 ⑤(done·cancelled 는 그 키만 뗀다)를 도달 불가로 만든다. **코디 실수** — SPEC 이 정본이라 enum 넷+null · 규칙 ⑤ 유지(B)로 답함. 사람 표면 422(MF-59)는 그대로
- 회의 9 실측(09:26~) — 웜스타트 성공. **프론트 수정 대기 1건(사용자 지시 · 회의 끝난 뒤)**: 회의 중 화면 줄 행에서 종류 라벨 「논의」와 본문이 세로 가운데 정렬이 안 맞는다(라벨이 위로 붙음 · `LineRow` — 캡처 orca-paste-1788827277530). 회의 중에는 next HMR 이 화면을 갈아끼우므로 프론트도 손대지 않는다
- backend 완료(`task_75e1e1f6a5a1`) — `meeting_notes.json` payload strict(11키 · status 넷+null) · `_final_payload` 종류별 키만 · strict 전수 테스트 · 워커 640 passed · 증거 `e2e-01-real-summit-evidence.md`. 회의 8 실패 배치 16회(전부 400) vs 회의 9 배치 exit 0. **회의 9 실물: 배치 seq 1·2 succeeded · AI 안건 1(미러) · AI 줄 3 — AI 요약이 실제로 쌓인다**
- **회의 9 끝난 뒤 순서**(코디): ① 볼륨의 `/data/recordings/8.bin` · `9.bin` 을 `reference/2026-09-08-real-summit/recordings/` 로 복사 ② `up -d --no-deps api` 로 바인드 마운트 반영(`STORAGE_HOST_DIR`) ③ 코디 `make test` ④ 커밋(스키마 수정 + compose) ⑤ 프론트 `LineRow` 세로 정렬 발주
- **사용자 결정 MF-71(09-08 회의 9 중)** — 중간 배치는 AI 혼자 쓴다(사람 안건·줄 안 봄 · 도구는 업무 셋만 · 미러 없음 · 전부 신설). 최종은 지금대로. `Meeting flow.md` §0 행 + §2-3 본문에 기록. 문서 전파(DEC-003 · SPEC-007 · BE README · WORK-015) → architect 발주 → 회의 끝난 뒤 코드 발주
- architect 발주 `docs-v1-meeting-reflow4-brief.md`(`task_4366ee55e2c1` · `ctx_8d45b434db9c` · 새 터미널 `term_58393ecb…`) — MF-71 전파 + WORK-015. 회의 9 배치 seq 1~4 전부 exit 0(38~45초)
- **회의 9 종료 — 최종 회의록 성공**(00:42): ① 재전사 1분 · ② codex 1회 성공 · `ended · succeeded` · headline 1 · 용어 보정 8(auto 6 · guess 2) · merged 안건 4 · 줄 18(사람 4/8 · AI 3/16). 배치 6회 전부 succeeded
- 회의 끝난 뒤(코디): `9.bin` 복사 → api 재생성(바인드 `/data` = reference/2026-09-08-real-summit · 8·9.bin 보임) → `make test` 640 → **커밋 `dd9d861`**(스키마 + compose)
- frontend 발주 `docs-v1-linerow-align-brief.md`(`task_cb99f9ae8239` · `ctx_9af46c426471`) — 「논의」 라벨 세로 정렬
- architect 완료 — MF-71 전파(DEC-003 · SPEC-007 v0.0.3 · BE README · DB meeting.md · 초안 §B) + **WORK-015** 신설. 리포트 `docs-v1-meeting-reflow4-report.md`. 결정 필요로 올린 셋 중 ① spec-008 L168 미러 배지 문구는 코디가 지움 ③ BE README 「해시만」은 이미 없음. **② 웜스타트 phase — WP 가 `final`(일곱)로 가정 · 사용자 확인 항목(§1)**
- frontend 완료 — LineRow 정렬(라벨에 본문과 같은 줄 상자 · items-start). 코디 검증 tsc 0 · vitest 363 → **커밋 `aa375ed`**. ⚠ 워커가 검증 중 사용자 앱이 물고 있던 `:3000` dev 서버를 내렸다가 다시 띄웠다 — 사용자 화면이 잠깐 스타일 없이 뜬 원인. 워커에게 사용자 포트 금지 지시
- backend 발주 **WORK-015**(`task_cb2bdac467da` · `ctx_fa004e9c10d0` · `docs-v1-work015-be-brief.md`)
- backend 완료(`task_cb2bdac467da`) — `build_codex_options(phase)`(batch 10줄 셋 / final 14줄 일곱 · 기본값 없음) · 배치 프롬프트 조회 절·미러 지시 삭제 · `humanAgendaId` 읽고 버림 · `_persist` 미러 전체를 `mirror_human_agendas` 플래그 안(merged 만 True) · `_run_once` 사람 안건 조회 삭제 · 워커 652 passed. 코디 정적 — 프롬프트에 안건 도구 0 · phase 호출 셋(batch 1 · final 2) · make test 재실행 중
- reviewer 발주(`task_b9b263797335` · `ctx_7585d74e9166`)
- reviewer 완료 — **FAIL 0 · WARN 2 · 문서 공백 2**(`work015-review-report.md`). 축 다섯 전부 PASS. WARN — 옵션 테스트 docstring 「손으로 적는다」가 생성식과 어긋남 · `_run_once` 가 `human_agenda_ids=frozenset()` 을 넘김(안 읽히지만 「빈 집합」은 「사람 안건 0」으로 오독될 자리) → 다음 백엔드 발주에. 문서 공백 둘은 코디가 WP 에서 고침(웜스타트 위치 · get_meeting/get_account Open Issue 닫음)
- **커밋 `1ca243e`** feat: WORK-015. WP-015 done · README done. 코디 `make test` 652
- 앱 창 재기동(코디) — 시스템이 메모리 부족으로 `tauri dev` 를 죽임(여유 ~70MB · 도커 VM 891 · Orca 591 · claude 워커 셋 900). 워커가 남긴 `:3000` next dev 를 내리고 다시 띄움 — **워커 흰 화면의 유력 원인 = :3000 이 이미 점유돼 tauri 의 next 가 3001 로 밀림**
- **실물 버그 2(사용자)** — 새 회의록 드로어 시간 팝오버 스크롤 안 됨(Sheet 스크롤 잠금이 포탈된 Popover 휠을 막는 것으로 추정). frontend 발주 `docs-v1-timepicker-scroll-brief.md`
- frontend 완료 — 원인 확정: Sheet 의 react-remove-scroll 이 잠금 노드 밖 휠을 막음 · 포탈 컨테이너 컨텍스트 한 자리(`lib/overlay/PortalContainer` + `popover.tsx` + `DrawerFrame`)로 해결 · 시간·프로젝트·연관 업무 목록 같이 풀림 · 시간 목록 선택값으로 scrollIntoView · 기본값 SPEC 대로 확인. 코디 검증 tsc 0 · vitest 367 → **커밋 `f0d4d46`**
- **실물 버그 3(회의 12 · 12:50~)** — 시작 뒤 2분 넘게 전사 0 → 사용자가 일시정지·재개 → 90~104초 구간 블록 2개(55자) → 그 뒤 다시 정지(오디오는 11.7MB 까지 계속 저장 · Soniox TCP 1개 유지 · WS `accepted` 3회 · `connection closed` 로그 0). 첫 배치는 succeeded 인데 AI 트랙 빈 목록. 재개/재연결 뒤 업스트림이 토큰을 안 내는 것으로 보임 — `meeting_stream_service` 의 두 번째 WS 는 `stream_active` 로 닫는 규칙 · 재개 시 새 recorder 컨테이너(webm 헤더) 문제 후보. **회의 끝난 뒤 백엔드 조사 발주**(①재전사는 파일 전체를 읽으므로 최종 회의록은 영향 없음)
- **버그 3 조사 완료(`task_dbbe64b7f087` · `stream-stall-investigation.md`) — 코드 정상 · 원인 = 마이크 입력이 회의 11 보다 20~30dB 낮음.** 스트림 셋의 RMS -60/-43/-51 dBFS(정상 회의 -28) · Soniox async 로 재전사해도 토큰 6/0/0 · webm 헤더 3개 = WS 3개 = Soniox 세션 3개 1:1 · 클러스터 타임코드 단조 · 파일 성장은 Opus 고정 비트레이트라 무음이어도 정상. 후보 A~D 전부 아니다. 내용(「고객사 대리님 연결됐습니다」)으로 보아 통화 앱이 마이크를 잡고 있을 가능성
- ② 수정 계획(회의 끝난 뒤) — 스트림 세션 30초 유입량 INFO 로그 · 60초 무토큰 WARNING(세션당 1회). 계약 변경 0
- 곁가지 — 재연결 공백(약 12초)이 파일 시간축에 없어 종료 후 재전사의 at_ms 가 실시간과 어긋난다(M-11 · 근거 칩 매칭) — 별건 기록
- **회의 12 배치 3~11 전부 실패(13:20~13:54)** — worker 컨테이너의 codex 가 `wss://chatgpt.com` DNS 「Name does not resolve」 → 이후 「stream disconnected before completion」. 우리 코드 밖(컨테이너 네트워크 · 호스트 네트워크 변화 추정). 14:00 현재 worker/api 둘 다 chatgpt.com resolve 됨. 회의 12 의 AI 탭은 배치 2 결과에서 멈춤 · 최종 ② 는 네트워크가 살아 있으면 정상
- **09-08 낮 마감(사용자)** — 문서 커밋 `6047d8a`. 다음은 `_RESUME.md` 「다음」

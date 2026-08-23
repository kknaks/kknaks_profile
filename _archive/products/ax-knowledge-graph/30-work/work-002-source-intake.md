---
type: work
id: AXKG-WORK-002
title: "WP1: Source Intake — 수신·수집·요약"
status: done
product: ax-knowledge-graph
work_type: new-feature
owner: kknaks
roles:
  pm: kknaks
  design: kknaks
  fe: kknaks
  be: kknaks
  qa: kknaks
  ops: kknaks
progress: 100
created_at: 2026-07-07
updated_at: 2026-07-08
tags:
  - product/ax-knowledge-graph
  - doc/work
  - status/done
links:
  baselines:
    - "[[baseline-001-ax-knowledge-graph-from-curated-sources|AXKG-BL-001]]"
  decisions:
    - "[[decision-004-mvp-defaults-and-scope|AXKG-DEC-004]]"
    - "[[decision-005-ai-execution-assembly-and-link-context|AXKG-DEC-005]]"
  specs:
    - "[[spec-003-source-inbox|AXKG-SPEC-003]]"
    - "[[spec-012-source-collection-adapter|AXKG-SPEC-012]]"
    - "[[spec-011-ai-execution-pipeline|AXKG-SPEC-011]]"
  works:
    - "[[work-001-mvp-pipeline-scaffold|AXKG-WORK-001]]"
  releases: []
  related: []
---

# WP1: Source Intake — 수신·수집·요약

URL이 들어와서(`Slack`/`manual`) 자동으로 원문이 수집·요약되어 `summarized`가 되기까지를 구현한다. WP0의 AI 실행 골격 위에 요약 스테이지(①)를 첫 실사용 스테이지로 배선한다.

## Meta

- Baseline: AXKG-BL-001
- Covers spec: AXKG-SPEC-003(Source Inbox), AXKG-SPEC-012(Collection Adapter), AXKG-SPEC-011①(요약 스테이지)
- Depends on work: AXKG-WORK-001(WP0 — 실행 골격·auth·마이그레이션)
- Parallel work: AXKG-WORK-003(WP2)과 병렬 가능
- Follow-up work: AXKG-WORK-004(WP3 — summarized 이후 게이트)
- External dependency: open-kknaks client 실 바인딩 확정(HTTP vs Redis broker AgentClient — WP0 잔여 TODO를 이 WP에서 확정), Slack app 슬래시 커맨드 등록 완료(Request URL `https://ax-api.kknaks.cloud/api/v1/slack/commands`), `AXKG_SLACK_SIGNING_SECRET`·`AXKG_SLACK_BOT_TOKEN` 값 사용자 투입

## Scope

포함:

- sources 라우터/서비스/레포지토리: `/sources/manual`, `GET /sources`(status 필터), `GET /sources/{id}`, `queue-collection`(재시도), `GET /sources/{id}/ai-tasks`
- 중복 URL 처리: normalized_url 검사 → metadata.slack_events 누적/duplicate_candidate (SPEC-003 S-2)
- Slack intake: `POST /api/v1/slack/commands`(슬래시 커맨드, 등록 Request URL과 문자 일치) + signing secret 검증(토큰 인증 제외 경로) + 봇 아웃바운드(앵커 메시지·스레드 요약 회신)
- Source Collection Adapter (SPEC-012): type detection → youtube(metadata+transcript, description fallback) → static_web → dynamic_web(Playwright) fallback 체인, SourceMaterial 정규화, canonical_url로 normalized_url 갱신·중복 재검사, SSRF 가드
- 요약 스테이지(①): `source_summary` context builder 구현·등록, `received → summarizing → summarized/collection_failed` 자동 전이, summary_payload 저장, chunk 요약 병합, 재시도 배선
- open-kknaks client 실 바인딩 (fake → 실제)
- FE: Source Inbox 화면 — 큐 목록(상태별), 상세(요약 카드·실패 사유·`요약 재시도`), `Inbox에 넣기` 모달. **기준: `21-html/page-approval.html`의 Source Inbox 영역 — 레이아웃·한국어 카피 모두 시안을 따른다**

제외:

- 분류/문서화 게이트 (WP3)
- PDF/RSS adapter, page_kind=list 후속 UX (SPEC-012 OQ)
- 프롬프트 편집 UI (WP5)

## Code Surface

- Repo / module: ax-graph
- 만질 파일 후보:

| 경로 | 설명 |
|---|---|
| `apps/api/axkg/api/routes/sources.py` · `integrations.py` | sources·Slack 라우터 |
| `apps/api/axkg/services/sources.py` · `repositories/sources.py` | source lifecycle 비즈니스/DB |
| `apps/api/axkg/integrations/source_collection/` | adapter 3종 + selection |
| `apps/api/axkg/integrations/slack.py` | 서명 검증·슬래시 커맨드 payload 파싱·봇 아웃바운드(앵커·스레드 회신) |
| `apps/api/axkg/services/ai/` | source_summary builder 등록, client 실 바인딩 |
| `apps/web/app/(app)/page.tsx` (nav "/") | Source Inbox 화면 — 새 `(inbox)` 그룹은 auth 가드(`(app)` 라우트 그룹)를 우회하므로 기존 홈에 구현 |

## Domain / Schema

| Entity | 이 WP에서 |
|---|---|
| `sources` | 전체 lifecycle 구현 (received→summarizing→summarized/collection_failed, ignored/deleted) |
| `ai_tasks` | `collect_source_summary` 실사용 (골격은 WP0) |

- 상태 / invariant: sources.status SSOT는 SPEC-003 상태도. 수집 실패 시 실패 ai_tasks 보존 + collection_failed.
- Migration 필요 여부: 없음(WP0에서 완료). 필요 시 컬럼 보강만.
- SPEC에 환류해야 하는 외부 resource/status/enum 변경: open-kknaks 바인딩 확정 결과를 40-architecture에 반영.

## Execution

### Phase 1 — sources API + Inbox 화면

- **Status**: DONE
- **작업**:
  - [x] sources 라우터/서비스/레포 (manual 입력, 목록/상세, 중복 처리)
  - [x] FE Inbox 큐/상세/입력 모달 (SPEC-003 UX Contract)
- **검증**:
  - [x] SPEC-003 U-1~U-3·S-2·S-3 AC 통과
- **완료 증거**:
  - BE: `POST /sources/manual`·`GET /sources`(status 필터)·`GET /sources/{id}`·`queue-collection`·`GET /{id}/ai-tasks` 구현. `uv run pytest` **41 passed**(신규 20건). 근거 표는 PLAN-005-T-001 리포트.
    - S-3 수동 URL → `source_channel=manual`·`received` 저장 (`test_manual_create_received`)
    - S-2 중복(링크): 새 row 없이 `metadata.slack_events[]` 누적 + 409 `DUPLICATE_SOURCE` (`test_duplicate_links_to_existing`) / 중복(후보): documented면 `duplicate_candidate` 표시 (`test_duplicate_of_documented_marks_candidate`)
    - U-1 목록 status 필터 + 기본 hidden 제외 (`test_list_filters_by_status`, `test_default_list_hides_documented`)
    - U-2 상세 조회 + collection_failed 시 최신 실패 task `error_message` 동봉 (`test_get_detail_and_missing`, `test_collection_failed_detail_surfaces_error_message`)
  - FE: Source Inbox 화면(큐 목록/상세/직접 입력 모달) — `21-html/page-approval.html` 시안 기준 구현. `tsc --noEmit` exit 0, `npm run build` Compiled successfully. 근거는 PLAN-005-T-002 리포트.
    - U-1 큐 목록(상태 배지·채널 문구·상태별 필터·빈 상태), U-2 상세(요약 카드·실패 사유·`요약 재시도` CTA), U-3 `Inbox에 넣기` 모달(중복/2000자 초과 안내) 시안 1:1 매핑.
  - 비고: 삭제/무시 CTA는 §4 API Contract에 엔드포인트가 없어 미배선(임의 발명 안 함) — admin 별도 논의 대상. Phase 2~4(수집 adapter·요약 실행·Slack intake)는 TODO.

### Phase 2 — Collection Adapter (SPEC-012)

- **Status**: DONE (dynamic 실 렌더 스모크는 chromium 미설치로 admin 후속)
- **작업**:
  - [x] adapter selection + youtube(기존 profile 코드 참고: metadata+transcript, description fallback)
  - [x] static_web → dynamic_web(Playwright) fallback, 공통 추출·후처리·수집 기준
  - [x] SSRF 가드, canonical_url→normalized_url 갱신
- **검증**:
  - [x] SPEC-012 AC 통과 (fixture 2종 포함)
- **완료 증거**:
  - BE: `collect_source` 오케스트레이션(youtube/static_web/dynamic_web + static→dynamic fallback), 공통 `process_web_document`(DOM 제거·metadata·후처리·수집 기준 공유), SSRF 가드(`guard_public_url`/`require_http_url`), `apply_collection_result`(canonical→normalized_url + S-2 병합). `uv run pytest` **73 passed**(신규 32건). SPEC-012 §6 AC 전 항목 근거는 PLAN-005-T-004 리포트.
  - 실 URL 스모크: YouTube transcript·정적 웹(SPEC-012 fixture) 수집 성공. dynamic_web 실 렌더는 chromium 바이너리 미설치로 미실행(주입 renderer 테스트로 커버) — `playwright install chromium` 후 admin 후속.

### Phase 3 — 요약 스테이지 배선 (SPEC-011①)

- **Status**: DONE (라이브 e2e 성공 — `summarized` 실값 도달, claude가 workspace 프로젝트 컨텍스트 실 Read)
- **작업**:
  - [x] open-kknaks client 실 바인딩 확정·구현 — Redis 직결 `AgentClient`(HTTP 아님). `RedisOpenKknaksClient`가 `AgentClient(RedisBroker(url=AXKG_REDIS_URL, namespace="axkg"))`를 감싸 producer, worker(`ClaudeWorker`)가 같은 Redis+`namespace=axkg`+`queue=default` consumer. `submit(..., queue="default", max_retries=0)` 고정 — 재시도는 AXKG가 `retry_of_task_id` 새 row로 소유(SPEC-002/011), broker 자동재시도와 이중 방지.
  - [x] source_summary context builder + 결과 저장(summary_payload). **입력 모델 재정의 완료**(아래 Open Issues): api submit = DB 프롬프트(작업 지시)+output_schema+런타임 원문(`SourceMaterial` 인라인 데이터 블록), 방법 지침은 worker 이미지 내장 프로젝트 컨텍스트(`apps/worker/workspace/`)가 담당·claude가 실행 디렉토리에서 Read. 코드 재배선(profile-be T-008) 완료.
  - [x] received 자동 트리거, 상태 전이, 재시도, chunk 병합
- **검증**:
  - [x] producer 체인 라이브 — manual URL → 라이브 `collect_source`(static_web) → 프롬프트 조립 → 실 Redis submit(`axkg:queue:default`), namespace/queue가 worker와 정합
  - [x] URL 입력 → **최종 `summarized`까지** end-to-end (라이브) — worker claude 실행(토큰+claude 바이너리) 완비 후 docker e2e 성공. `summarized` + summary_payload 실값 도달, 같은 run 트랜스크립트에서 claude가 `/app/workspace/context/source-summary-guide.md`를 실제 Read 확인(profile-be T-008)
- **완료 증거**:
  - BE: 신규 `integrations/redis_open_kknaks.py`·`services/ai/source_summary.py`·`services/summary_execution.py`. 실행 모델 재설계(프로젝트 컨텍스트 이미지 내장 + guide 로드/fallback 제거)까지 반영. `cd apps/api && uv run pytest` **89 passed**(재설계 후: guide 로드 테스트 제거·fence-strip 테스트 추가). SPEC-011① AC(정의→조립→실행→스냅샷, output_schema 검증 실패 시 부분소비 금지, 수집 실패→`collection_failed`+요약 재시도, 프롬프트/템플릿 DB 로드 실패 시 코드 fallback) pytest 커버. 근거는 PLAN-005-T-006·T-008 리포트.
  - 라이브 e2e(docker `up --build worker api`): manual URL → `summarized` + summary_payload 고품질 실값(예: LangChain blog → title/keywords/summary 정확, 네비·광고 배제). worker `provider.check claude=ok`, 프로젝트 컨텍스트(`CLAUDE.md`/`agent.md`/`context/source-summary-guide.md`) 이미지 내장 확인. DB 프롬프트에 "먼저 workspace `context/source-summary-guide.md`를 읽고 요약하라" 최소 지시 추가(headless claude는 참조 파일 자동 추적 안 함) → claude가 실제 Read.
  - credential(`CLAUDE_CODE_OAUTH_TOKEN`)은 worker 측에만(SPEC-007: provider credential은 서버까지, 실행은 worker).
  - 관찰 잔여(정직 보고): agentic 모드 claude의 JSON 출력이 드물게 불안정(미이스케이프 큰따옴표 1회 관찰). `strip_code_fences()` 정규화 + output-contract 프레임 강화로 실패율 저감, 이스케이프 실패는 `OUTPUT_PARSE_FAILED`로 표면화되어 SPEC-011 재시도 대상으로 보존(마스킹/강제복구 안 함).
  - **max_turns 픽스 노트(2026-07-08, T-016)**: 요약 실행 크래시(`error_max_turns` exit 1)의 근본원인 = `provider_options.max_turns=3`이 worker 프로젝트 컨텍스트 guide 파일 Read(agentic turn 증가)를 못 버팀. **3→6 상향**(`resolution.py` DEFAULT + `seeds.py` + DB settings). 최초 요약·피드백 재요약 라이브 정상 도달 확인. max_turns는 SPEC-011 실행 계약의 튜닝 파라미터(provider_options, AXKG-SPEC-007 바인딩) — agentic 실행이 방법 지침을 Read하는 원천 2·3 모델(SPEC-011 Assembly Contract)에서 하한이 3보다 커야 함을 실측으로 확인.

### Phase 4 — Slack intake (슬래시 커맨드)

- **Status**: 코드 DONE (pytest 완료 · 라이브는 Slack 앱 등록 + env 2키 + 공개 배포 후 — admin 후속)
- **작업**:
  - [x] 슬래시 커맨드 수신 `POST /api/v1/slack/commands`(등록 Request URL 문자 일치) + signing secret 검증(토큰 인증 제외) + `text`에서 URL 추출·사용법 ephemeral
  - [x] 3초 내 ephemeral ack + `trigger_id` 합성 키 멱등, source 저장(`received`, `source_channel=slack`, S-2 중복 규칙)
  - [x] 봇 아웃바운드: 앵커 메시지 post → `ts` metadata 저장, `summarized`/`collection_failed` 시 앵커 스레드 회신
  - [x] slack_events metadata 규약 (코드 docstring 명시 — 제품 문서는 읽기전용이라 미수정, DB README §metadata 확장)
- **검증**:
  - [x] Slack 서명 검증 통과/실패, URL 없음→사용법 ephemeral, 더블서밋 멱등, 중복 URL 누적 — pytest 커버(라이브는 앱 등록/배포 후)
  - [x] 앵커 스레드에 요약/실패 회신 도달 — fake bot pytest 커버(라이브 최종 도달은 Slack 앱 등록 + env 2키 + 공개 배포 후)
- **완료 증거**:
  - BE: 신규 `api/routes/slack.py`·`services/slack_intake.py`, `integrations/slack.py`(서명검증 v0·URL 추출·합성 멱등키·`SlackIdempotencyStore`·`SlackBotClient`) 구현. `POST /api/v1/slack/commands`를 문자 그대로 서빙(Bearer 제외, signing secret 소관). `cd apps/api && uv run pytest` **107 passed**(기존 89 + 신규 18). SPEC-003 §4/S-1 AC 근거 표는 PLAN-005-T-010 리포트.
  - 라이브 잔여(admin 후속): ① Slack 앱 등록(Request URL `https://ax-api.kknaks.cloud/api/v1/slack/commands`, 스코프 `commands`·`chat:write`), ② env 2키 투입(`AXKG_SLACK_SIGNING_SECRET`·`AXKG_SLACK_BOT_TOKEN`), ③ 공개 배포. 미설정 시 서명검증 전부 401(안전)·봇 토큰 없으면 앵커/회신 생략(source는 정상 저장).

### Phase 5 — 메모 fallback (수집 실패 시 메모로 요약)

> **후속 확장 스코프** — WP1이 Phase 1~4 기준으로 코드 완료 close(status done)된 뒤 추가된 MVP 결정(2026-07-08, 사용자 확정). 문서 계약은 이 태스크에서 확정, 코드는 BE T-013 / FE T-014 병렬. WP 보드(30-work/README) status는 원 스코프 기준 done을 유지하고, 이 Phase는 문서 계약 완료·코드 대기로 별도 추적한다.

- **Status**: DONE (문서 계약 + 코드 BE T-013 / FE T-014 완결)
- **배경**: medium 등 Cloudflare/봇 방어 사이트는 static·dynamic 모두 원문 수집 불가(진단: static 403 "Just a moment" JS challenge, dynamic도 headless 감지로 본문 미달). 수집 못해도 사용자가 넣은 메모/복붙 텍스트로 요약하도록 수집 체인을 확장한다.
- **작업**:
  - [x] BE: 수집 체인 최종 fallback — youtube/static/dynamic 모두 `CollectionError`이고 메모(trim 후 non-empty) 있으면 `user_note` `SourceMaterial`(adapter/content_format/fetch_method=`user_note`, content_text=메모, canonical_url=원 URL)로 성립. 메모 없으면 `collection_failed` 유지. URL 수집 성공 시 원문 우선(메모 미사용)
  - [x] BE: Slack `text`에서 `<< >>` 안 텍스트를 메모(`raw_text`)로 추출·저장
  - [x] BE: `queue-collection`에 optional `note` → `raw_text` 갱신 후 재큐(재요약). 새 `ai_tasks` row, 기존 실패 task 보존
  - [x] FE: Source Detail에서 `collection_failed` 항목에 `메모 추가`/`메모 수정` → 재요약 UX
- **검증**:
  - [x] URL 수집 실패 + 메모 있음 → 수집 단계 통과(메모 fallback), URL 수집 실패 + 메모 없음 → `collection_failed` — 라이브 A/B 대조 확인
  - [x] URL 수집 성공 시 메모 있어도 원문 우선(메모 미사용) — pytest
  - [x] Slack `<< 메모 >>` 추출, 없으면 메모 없음 — pytest
  - [x] 메모 기반/원문 기반 요약을 상태·payload·UI에서 구분 표기하지 않음(source_basis 플래그/배지 없음)
- **완료 증거**:
  - BE(T-013): `collect_source(url, *, user_note=...)` 최종 fallback(`build_user_note_material`), `queue-collection` optional `note`→`raw_text` 갱신 재큐, Slack `extract_note`(`<<(.+?)>>` 첫 쌍·trim). `cd apps/api && uv run pytest` **124 passed**(신규 17). 라이브 A/B: 메모 있는 medium manual → 수집 user_note 통과 / 메모 없는 대조군 → `CONTENT_FETCH_FAILED`(수집 단계 실패) = 메모가 수집을 구제함을 실증. 근거 PLAN-005-T-013.
  - FE(T-014): `collection_failed` Source Detail 메모 추가/수정 → 단건 `queue-collection {note}` 재요약 UX. `tsc --noEmit`/`npm run build` 통과. 근거 PLAN-005-T-014.
  - 비고: 요약 최종 `summarized` 도달을 막던 워커 실행 크래시(`error_max_turns` exit 1)는 이 Phase가 아니라 **max_turns 3→6 픽스(Phase 6/T-016)**로 근본 해소 — 아래 Phase 3 max_turns 노트 참조. 메모 fallback 자체(수집 구제)는 라이브 확인.
- **문서 계약**: AXKG-SPEC-012(수집 체인 4단계·User Note Fallback·Failure Contract), AXKG-SPEC-011(요약 스테이지① `user_note` 입력·메모 추측 금지), AXKG-SPEC-003(U-2 메모 추가/재요약·U-3 fallback·S-1 `<< >>`·`queue-collection` note) — 이 태스크(PLAN-005-T-012)에서 확정.

### Phase 6 — 요약 초안 게이트 (렌더·피드백 resume·분류 트리거)

> **후속 확장 스코프** — WP1 close(Phase 1~4 코드 완료) 이후 추가된 확정 흐름(2026-07-08, 사용자 확정). 요약이 자동으로 분류까지 넘어가던 흐름을, 요약 초안을 **사용자가 검토→피드백/분류 선택**하는 게이트로 바꾼다. 문서 계약은 이 태스크에서 확정, 코드는 BE T-016 / FE T-017 병렬. WP 보드(30-work/README) status는 원 스코프 기준 done 유지하고, 이 Phase는 문서 계약 완료·코드 대기로 별도 추적한다.

- **Status**: DONE (문서 계약 + 코드 BE T-016 / FE T-017 완결, 세션 resume 재요약 라이브 실증)
- **배경(확정 흐름)**: 요약 → DB 초안(`summary_payload`, 임시) → 렌더(수정 가능 형태) → `[피드백]`(세션 resume 재요약, v2) / `[분류]`(분류 게이트 트리거). **핵심 = 세션 resume**: 요약 결과와 함께 받은 `open_kknaks_session_id`로 claude 세션을 이어서 피드백만 던지면 원문·지침 재전송 없이 재생성된다.
- **작업**:
  - [x] BE: 요약 초안 피드백 재요약 — `POST /sources/{id}/summary-feedback {feedback}`, 직전 succeeded 요약 task의 `open_kknaks_session_id`를 resume로 확보 → `options.resume={mode:session,session_id}` 배선(피드백-only 블록만 인라인, 원문 재수집 없음), 결과로 `sources.summary_payload` v2 갱신 + 직전 v1을 `metadata.summary_versions[]`에 read-only 아카이브. 새 `ai_tasks` row, 요약 lineage에 `retry_of_task_id`로 링크. `task_type`은 `collect_source_summary` 재사용
  - [x] BE: 요약 자동→분류 제거 — 분류기 AI(②)는 `[분류]` 트리거로만(요약에 딸려 자동 실행 안 함). `POST /sources/{id}/classify` **스텁**(501 `CLASSIFICATION_NOT_IMPLEMENTED`) — 실 분류는 WP3
  - [x] FE: 요약 초안 렌더(수정 가능 형태: 문서보기 모달·폼) + `[피드백]`(모달)·`[분류]` CTA. **기준: `21-html/page-approval.html` 요약 초안 카드(분류 게이트와 분리된 표면)**
- **검증**:
  - [x] 요약 초안이 `summarized`에서 수정 가능한 형태로 렌더됨 — FE tsc/build
  - [x] `[피드백]` submit에 `options.resume={mode:session,session_id}` 배선, 원문 미재전송, `summary_payload` v2 갱신 — **라이브 실증**(피드백 payload 2,318자 vs v1 21,052자 ≈ 9배 축소, 반환 session id가 v1과 동일 = 새 세션 아닌 재개, task.done 5.1s exit 0)
  - [x] 요약이 자동으로 분류로 넘어가지 않고 `[분류]`를 눌러야 분류 게이트 생성 — classify 스텁 501로 FE 버튼 배선(실 분류 WP3)
- **완료 증거**:
  - BE(T-016): `POST /sources/{id}/summary-feedback`(summarized 전제, 아니면 `SUMMARY_FEEDBACK_NOT_ALLOWED` 409/`EMPTY_FEEDBACK`), resume 배선(open-kknaks 2.0.2 claude 어댑터가 `options.resume={mode:session,session_id}` 읽어 `claude --resume`), 피드백 감지 시 원문 수집/청킹 skip(피드백 블록만), v1 read-only 아카이브. `cd apps/api && uv run pytest` **133 passed**(신규 9). 라이브 docker e2e 성공. 근거 PLAN-005-T-016.
  - FE(T-017): 요약 초안 문서보기 모달·`[피드백]` 모달·`[분류]` 버튼. `tsc`/`build` 통과. 근거 PLAN-005-T-017.
  - **경로명 정합 대기**: BE는 `[분류]` 스텁을 `POST /sources/{id}/classify`로, 요약 피드백을 `POST /sources/{id}/summary-feedback`로 구현. AXKG-SPEC-001은 분류 트리거를 `POST /sources/{source_id}/classification-gates`로 정의 — 실 분류 구현(WP3=work-004) 시 최종 경로명 정합 필요(스텁이라 리스크 낮음). 요약 피드백 엔드포인트/버전 저장 위치(`metadata.summary_versions[]`)는 SPEC-002/003과 최종 정합 대상.
- **범위 밖(WP3 = work-004)**: `[분류]`를 눌렀을 때 실제 **분류 AI 실행·PARA 분류 생성·md 변환(frontmatter)·문서화 게이트**는 AXKG-WORK-004 소관. 이 Phase는 요약 초안 게이트(렌더·피드백 resume·분류 트리거 자리)까지다.
- **문서 계약**: AXKG-SPEC-003(U-2 요약 초안 렌더·`[피드백]`/`[분류]`·요약 자동분류 제거), AXKG-SPEC-002(요약 초안도 피드백 대상 revision·v1 read-only + resume 규칙 공유), AXKG-SPEC-011(Feedback Regeneration Resume Wiring ①②③ 공통·배선 계약), AXKG-SPEC-001(요약·분류 병합 카드 분리·분류 `[분류]` 트리거로만), `21-html/page-approval.html`(요약 초안 카드 분리) — 이 태스크(PLAN-005-T-015)에서 확정.

## Pre-deploy Check

- [ ] 외부 URL 수집 시 비공개 네트워크 접근 차단 (SSRF)
- [ ] transcript/page_text 전문이 application log에 남지 않음
- [ ] Slack 엔드포인트가 서명 검증 없이 열리지 않음

## Rollback

- 작업 레포 커밋 단위 revert. 문서 변경은 별도 커밋.

## Done Criteria

- [x] 원 스코프 Phase(1~4) DONE (Phase 1~3 라이브 검증 완료, Phase 4 코드+pytest 완료 — **라이브 잔여는 Open Issues 참조**: WP는 코드 완료 기준으로 닫음). **Phase 5(메모 fallback)·Phase 6(요약 초안 게이트)은 close 이후 추가된 후속 확장 — 문서 계약 done·코드 대기(Phase 5 BE T-013/FE T-014, Phase 6 BE T-016/FE T-017), WP 보드 done은 원 스코프 기준 유지**
- [x] SPEC-003/012 AC + SPEC-011 요약 스테이지 AC 반영 (pytest 근거 PLAN-005-T-001/002/004/006/008/010). Phase 5 AC 코드 검증 완료(pytest 124, T-013), Phase 6 AC 코드 검증 완료(pytest 133 + resume 라이브 실증, T-016)
- [x] product `log.md`·`30-work/README.md` 갱신

## Open Issues

- ~~open-kknaks 실 바인딩 방식(HTTP vs Redis broker AgentClient)~~ → **Redis 직결 `AgentClient`로 확정**(Phase 3 해소). api=producer가 `AgentClient(RedisBroker(url=AXKG_REDIS_URL, namespace="axkg"))`를 감싸고 worker(`ClaudeWorker`)가 `namespace=axkg`+`queue=default` consumer. `max_retries=0` 고정, credential(`CLAUDE_CODE_OAUTH_TOKEN`)은 worker 측에만. 40-architecture 환류 완료.
- ~~dynamic adapter 실행 위치(FastAPI 내 vs browser worker 분리)~~ → **api 프로세스 내 background로 확정**(SPEC-011/012 OQ 해소). `collect_source`는 FastAPI api의 BackgroundTask에서 실행(별도 browser worker 분리 안 함). 요약 AI 실행만 open-kknaks worker로 넘어간다.
- ~~**요약 실행 입력 모델 재정의**~~ → **DONE**(2026-07-08, Phase 3 라이브 e2e). 방법·배경 지침을 api 프롬프트 인라인 조립('5블록') → **worker 이미지 내장 프로젝트 컨텍스트**(진입 `CLAUDE.md → agent.md → context/`, claude가 실행 디렉토리에서 읽음)로 이동. api submit 표면 = DB 프롬프트(작업 지시)+output_schema+런타임 원문(`SourceMaterial`)만, `context/source-summary-guide.md` 미로드·파일 fallback 제거. 프로젝트 컨텍스트는 빌드 시점 이미지 내장(마운트/git pull 런타임 의존 회피). 문서 정합 = AXKG-SPEC-011/DEC-005/40-arch(PLAN-005-T-009), 코드 = profile-be PLAN-005-T-008(라이브 e2e 성공·guide 실 Read 확인).
- ~~원문 전달 방식 OQ(SPEC-011 §7: 프롬프트 인라인 vs `WORK_DIR` 파일 드롭)~~ → **submit 프롬프트 인라인으로 확정**(profile-be T-008). builder가 `SourceMaterial` 원문을 데이터 블록(`source`+`content`/`content_chunk_*`)으로 인라인 조립해 submit, workspace 파일로 넘기는 것은 방법 지침(guide)뿐. SPEC-011 §7·§4 정합 갱신.

### 라이브 잔여 (전 Phase 코드 done — **코드 done ≠ 배포 완료**, 잔여는 숨기지 않음)

- **Phase 3 공개 배포**: 요약 스테이지는 docker 라이브 e2e까지 검증됐으나(로컬 스택), 공개 주소 배포는 미완. 최초 요약·피드백 재요약 라이브 정상은 로컬 스택 기준.
- **Phase 4 Slack 실연동·공개 배포**(admin 후속): ① Slack 앱 등록(슬래시 커맨드 Request URL `https://ax-api.kknaks.cloud/api/v1/slack/commands`, 스코프 `commands`·`chat:write`), ② env 2키 투입(`AXKG_SLACK_SIGNING_SECRET`·`AXKG_SLACK_BOT_TOKEN`), ③ 공개 배포. 완비 후 앵커 스레드 요약/실패 회신 라이브 도달 검증 가능. 코드·pytest는 완료.
- **삭제/무시 엔드포인트 실배선**(`DELETE /sources/{id}`·`POST /sources/{id}/ignore`, SPEC-003 §4 계약 추가됨): 계약 정의까지가 이번 WP 범위, 실배선은 후속 태스크(admin 발주). FE 삭제/무시 CTA도 이 배선 대기.
- **경로명/버전 저장 최종 정합**(WP3 병렬): Phase 6 BE의 `[분류]` 스텁 `POST /sources/{id}/classify`·요약 피드백 `POST /sources/{id}/summary-feedback`·v1 아카이브 `metadata.summary_versions[]`를 AXKG-SPEC-001(`classification-gates`)/SPEC-002/003과 실 분류 구현(work-004) 시 최종 정합. 스텁이라 리스크 낮음.
- ~~메모 fallback(Phase 5) 코드~~ → **DONE**(BE T-013 pytest 124 / FE T-014). ~~요약 초안 게이트(Phase 6) 코드~~ → **DONE**(BE T-016 pytest 133 + resume 라이브 실증 / FE T-017).

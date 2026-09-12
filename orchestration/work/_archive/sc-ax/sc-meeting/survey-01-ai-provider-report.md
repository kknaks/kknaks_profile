# 조사 1 — 백엔드 AI 프로바이더(LLM·STT) 사용 현황 전수조사

- 작성: 2026-09-08 / `reviewer_code` (read-only 조사, **판정 없음**)
- 조사 대상 워크트리
  - 코드: `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting` (브랜치 `kknaksss/sc-meeting`, HEAD `663319c`)
  - 스펙: `/Users/kknaks/orca/workspaces/mediness-mediness/sc-meeting-spec` (read-only 참조)
- **아무 파일도 수정·생성하지 않았다.** 산출물은 이 리포트 1개뿐. 테스트 미실행·서버 미기동·DB 미접속·외부 API 미호출 — 근거는 전부 소스와 문서다.
- 표기 규칙: **[사실]** = 인용한 `파일:줄`에서 직접 확인. **[추정]** = 코드/문서에서 유도한 해석이며 확정 아님.
- 환경변수·키·auth 파일의 **값은 하나도 인용하지 않았다.** 이름과 경로만 적었다.
- 경로는 별도 표기가 없으면 `backend/src/ax_workspace/` 기준이다.

---

## 0. 세 줄 요약

1. 백엔드가 부르는 외부 AI 서비스는 **딱 둘이다** — LLM은 **Codex CLI를 subprocess로 띄우는 `CodexCliProviderAdapter`** (`platform/codex_cli.py:69`), STT는 **Soniox REST + websocket 키 발급 `SonioxTranscriptionAdapter`** (`platform/soniox.py:33`). anthropic·openai·litellm 등 어떤 모델 SDK도 의존성에 없고(`backend/pyproject.toml:6-19`), 다른 네트워크 egress도 없다. **[사실]** (§2)
2. **회의 refinement·summary는 일일보고 draft 생성과 완전히 같은 LLM 어댑터 인스턴스를 쓴다** — `WorkflowApplication._report_provider` 하나가 `refine_meeting_transcript`·`summarize_meeting_transcript`·`DailyReportApplication` 셋을 모두 먹인다(`bootstrap/application.py:411, 605, 637, 873`). 코디가 "codex_cli grep에 안 걸렸다"고 본 이유는 `modules/meetings/`가 AI port를 **아예 들고 있지 않기** 때문이다 — `MeetingApplication.__init__`의 의존성은 repository·recording_storage·realtime_key_issuer 셋뿐이고(`modules/meetings/application.py:134-142`), LLM 호출은 전부 bootstrap 층에서 일어난다. **[사실]** (§3·§4)
3. 프로토타입 화면이 요구하는 셋 중 **회의 중 실시간 AI 노트·종료 후 합성 초안·안건 단위 구조는 전부 코드에 없다.** 가장 가까운 것은 (a) 확정 토큰만 적재하는 실시간 전사(`append_live_transcript`), (b) AI 요약 본문을 **그대로** 새 note version으로 붙이는 `adopt_summary`(합성 아님), (c) agenda/안건은 백엔드·프론트 전수 grep **0 hit**. **[사실]** (§5)

---

## 1. 조사 범위와 전수 방법

### 1.1 브리프 §2 표에 없던 파일 — 내가 채운 것

브리프가 준 입구 외에 `backend/src`를 `grep -rniE 'codex|soniox|openai|anthropic|llm|model|transcri|summar|refin|prompt'`로 전수한 결과 **26개 파일**이 걸렸다. 그중 브리프 표에 없던 것들:

| 파일 | 왜 AI 경로에 걸리나 | 브리프 |
|---|---|---|
| `bootstrap/settings.py` | 회의 worker의 lease·attempt·concurrency 설정 원천. **모델·provider 설정은 여기 없다**(§2.3) | 없었음 |
| `platform/reports.py:363-568` | `SqlAlchemyDailyReportDraftWorkflow` — LLM을 실제로 부르는 두 번째 소비자 | 없었음 |
| `platform/persistence.py:343-497, 574` | 회의 transcript/refinement/summary/evidence 테이블 + `provider_calls` | 없었음 |
| `platform/conversations.py` | 대화 turn·tool invocation 투영 | 없었음 |
| `entrypoints/http.py:646-780` | 회의 녹음·실시간 credential·실시간 segment 수신 엔드포인트 | 없었음 |
| `entrypoints/mcp.py:41, 800-824` | MCP가 `AiProvider`를 주입받는 자리 + 회의 read 도구 2개 | 부분 |
| `modules/jobs/domain.py:14-16` | durable job kind 3종 | 없었음 |
| `platform/durable_jobs.py` | lease·fence 전송층 | 없었음 |
| `backend/scripts/soniox_smoke.py` · `live_report_smoke.py` | opt-in 실호출 검증 스크립트 | 없었음 |
| `tests/architecture/test_architecture.py:84-92` | provider 정책 문자열 금지 규칙(**reports 한정**) | 없었음 |
| `frontend/src/liveTranscription.ts:215-226` | 브라우저가 Soniox websocket에 **직접** 붙는 자리 | 없었음 |

**[사실]** 반대로, 브리프가 "회의 AI 모듈"로 지목한 `modules/meetings/application.py`에는 **AI provider 참조가 한 줄도 없다** — 231건의 grep hit은 전부 `transcript`·`refinement`·`summary` 라는 도메인 명사이지 provider 호출이 아니다.

### 1.2 확인한 비-AI 경계 (오탐 제거)

**[사실]** 다음은 외부 AI가 아니다 — 전부 로컬 라이브러리다.
- 문서 파싱: `pypdf`·`python-docx`·`openpyxl`·`python-pptx` (`platform/document_parsers.py:77`, `platform/material_extraction.py:54-155`).
- 한국어 형태소: Kiwi (`platform/korean.py:41-44`), 로컬 프로세스 내 분석기.
- 검색: PostgreSQL full-text + Korean normalization. 임베딩 없음.

**[사실]** `backend/src` 전체에서 외부 네트워크로 나가는 코드는 **`platform/soniox.py`의 `urlopen` 하나**, 외부 프로세스를 띄우는 코드는 **`platform/codex_cli.py`의 `subprocess.Popen` 하나**뿐이다(`platform/codex_cli.py:754`).

---

## 2. Q1 — 프로바이더 목록 (전수 2개)

### 2.1 전수표

| # | 프로바이더 | adapter 파일·클래스 | 호출 방식 | 인증(이름만) | 모델·설정 출처 | 타임아웃 | 재시도 | 취소 |
|---|---|---|---|---|---|---|---|---|
| 1 | **Codex CLI** (LLM) | `platform/codex_cli.py:69` `CodexCliProviderAdapter` | **CLI subprocess** — `codex exec … --json` (`:257`, `:358`) | `~/.codex/auth.json` 파일 존재 여부(`:57`, `:711-736`). 환경변수 아님 | **하드코딩 기본값** `CodexCliProfile`(`:50-57`): model `gpt-5.6-terra`, tier `fast`, reasoning `low` | `timeout_seconds=90` 하드코딩(`:55`) | **어댑터 내 재시도 없음.** durable job 층에서만(`§4.3`) | `converse`만 `CancelToken` 지원(`:146-152`, `:196-197`). **`generate`는 취소 불가**(`:84`) |
| 2 | **Soniox** (STT) | `platform/soniox.py:33` `SonioxTranscriptionAdapter` | **REST**(`urlopen`) + 브라우저가 붙을 **websocket 키 발급** | 환경변수 **`SONIOX_API_KEY`** (`:43`) — 생성 시 `os.getenv`로 1회 읽음 | 하드코딩: 실시간 `stt-rt-v5`(`:69`), 최종 `stt-async-v5`(`:96`), 엔드포인트 `:29-30` | HTTP 요청당 `timeout=30`(`:196`); 폴링 `poll_seconds=1.0 × max_polls=1800` → 최대 약 30분(`:45-46`, `:103-123`) | **어댑터 내 재시도 없음.** `retryable` 플래그만 도메인에 전달(`:202`) | 취소 개념 없음 |

### 2.2 Codex CLI 어댑터 세부

**[사실]** 두 개의 실행 모드가 한 어댑터에 있다.
- `generate(AiGenerationRequest) -> AiGeneration` (`platform/codex_cli.py:84-144`) — 구조화 1-shot. `--output-schema`로 JSON Schema 파일을 넘기고(`:389-390`) `--output-last-message`로 결과 파일을 받는다(`:391-392`). **회의 refinement·summary와 일일보고가 쓰는 것이 이쪽이다.**
- `converse(AiConversationRequest, *, sink, cancel) -> AiConversationResult` (`platform/codex_cli.py:146-212`) — 대화 turn. `codex exec --json` JSONL을 스트리밍으로 소비하며 이벤트를 sink에 밀어넣는다. MCP 서버 바인딩이 없으면 **실패한다**(`:262`, `:282`).

**[사실]** 격리 정책 (`_arguments` `:352-394` · `_conversation_arguments` `:214-257`):
`--sandbox read-only` · `--ignore-user-config` · `--ignore-rules` · `shell_environment_policy.inherit="none"` · `features.plugins=false` · `features.skip_host_skill_discovery=true` · `generate`는 추가로 `--ephemeral`.
`prepare_isolated_codex_home`(`:711-736`)이 `CODEX_HOME`을 `.scax/codex-runtime`(`:56`)으로 갈아끼우고, `auth.json` **심볼릭 링크 하나만** 둔다. `AGENTS.md`·`config.toml`이 있거나 `.system` 밖 skill이 있으면 `ProviderUnavailable`로 **거부한다**(`:717-728`).

**[사실]** 실패 분류(`modules/ax_execution/ai.py:144-161`): `ProviderFailure` → `ProviderUnavailable`(바이너리·인증 없음) / `ProviderRequestFailed`(타임아웃·비정상 종료·스키마 위반) / `ProviderCancelled`. 예외 메시지에 credential이나 raw prompt를 넣지 않는다는 계약이 docstring에 명시돼 있다(`ai.py:145`).

**[사실]** 프로세스 정리: `start_new_session=True`로 **프로세스 그룹**을 띄우고(`:763`), 타임아웃·취소 시 그룹 전체에 시그널을 보낸다(`:813-838`) — Codex가 MCP 자식을 낳기 때문이라고 주석이 밝힌다(`:750-752`).

**[사실]** provenance 수집: stdout JSONL에서 `thread.started`→`provider_session_ref`, `turn.started|turn.completed`→`provider_run_ref`, `model`·`service_tier`·`usage`를 관찰값으로 뽑는다(`:396-424`). 요청값(requested)과 관찰값(observed)을 **따로** 보관한다(`ai.py:117-126`).

### 2.3 ⚠ 모델·프로바이더 설정이 `Settings`에 **없다**

**[사실]** `bootstrap/settings.py:18-36`의 `Settings`에는 모델·티어·타임아웃·API 키 필드가 하나도 없다. `AX_*` 환경변수는 큐 백엔드·lease·concurrency·디렉터리·데모 도메인만 다룬다(`:47-74`).

**[사실]** 결과적으로 모델 선택은 세 군데에 흩어져 있다.
| 자리 | 값 | 근거 |
|---|---|---|
| 어댑터 기본값 | `gpt-5.6-terra` / `fast` / `low` / 90s | `platform/codex_cli.py:52-55` |
| 조립 | `create_codex_cli_provider(settings)`가 **profile을 넘기지 않는다** → 항상 기본값 | `bootstrap/application.py:1705-1716` |
| 모듈 층의 문자열 | `DAILY_REPORT_PROVIDER_PROFILE = "codex-cli:gpt-5.6-terra:fast:low"` | `modules/reports/workflow_metadata.py:18` (검증에도 쓰임 `:72`) |

**[사실]** `AiProviderProfileRequest`(`modules/ax_execution/ai.py:16-23`)로 호출자가 모델·티어를 **요청할 수 있는 통로는 계약에 있으나**, 회의·일일보고 어느 호출자도 `profile=`을 채우지 않는다(`bootstrap/application.py:605-610, 637-642`; `platform/reports.py:510-514`). 즉 현재 실행 경로에서 모델은 **한 종류로 고정**이다. **[사실]**

**[추정]** 아키텍처 테스트 `test_reports_feature_does_not_embed_provider_policy_or_spawn_processes`(`tests/architecture/test_architecture.py:84-92`)는 `modules/reports/application.py`와 `platform/reports.py`만 검사하므로, `modules/reports/workflow_metadata.py:18`의 모델명 문자열과 `modules/meetings/`는 이 규칙의 사각지대다.

---

## 3. Q2 — port ↔ adapter 배선

### 3.1 배선표

| provider | port(Protocol) 위치 | 구현 | 조립 자리 | 테스트 대역 |
|---|---|---|---|---|
| LLM | `modules/ax_execution/ai.py:129` `AiProvider` (`generate`·`converse`) | `platform/codex_cli.py:69` | `bootstrap/application.py:411`(기본), `:1705-1716`(팩터리) / `bootstrap/conversation_worker.py:60` / `bootstrap/meeting_worker.py:39`(→ `WorkflowApplication`) / `entrypoints/mcp.py:90-94`(주입 파라미터) | §3.3 |
| STT 실시간 키 | `modules/meetings/transcription.py:70` `RealtimeTranscriptionKeyIssuer` | `platform/soniox.py:33` | `bootstrap/application.py:408` → `_meetings()` `:877-882`에서 `MeetingApplication`에 주입 | §3.3 |
| STT 최종 전사 | `modules/meetings/transcription.py:74` `FinalTranscriber` | 같은 클래스(`platform/soniox.py:33`이 두 Protocol을 함께 구현) | `bootstrap/meeting_worker.py:42` — **worker만 들고 있다.** API 프로세스는 최종 전사기를 갖지 않는다 | §3.3 |
| 녹음 바이트 저장 | `modules/meetings/recordings.py` `RecordingStorage`/`StoredRecording` | `platform/recordings.py:14` `LocalDirectoryRecordingStorage` | `bootstrap/application.py:407` · `bootstrap/meeting_worker.py:41` | — |

**[사실]** LLM port는 **회의 모듈이 아니라 `modules/ax_execution/ai.py`에 있다.** 회의 도메인은 이 파일을 import하지 않는다 — `modules/meetings/` 어디에도 `ax_execution` import가 없다.

### 3.2 조립 코드 원문 위치

- `bootstrap/application.py:403-411` — `WorkflowApplication.__init__`. `report_provider` 인자가 없으면 `create_codex_cli_provider(settings)`. Soniox는 `:408`에서 **무조건** 생성(키가 없어도 객체는 생성되고, 실제 호출 시점에 `provider_unavailable`로 실패 — `platform/soniox.py:186-187`).
- `bootstrap/application.py:877-882` — `_meetings()`가 요청마다 `MeetingApplication(repository, recording_storage, soniox)`를 만든다. **AI provider는 넘기지 않는다.**
- `bootstrap/application.py:867-875` — `_reports()`가 `SqlAlchemyDailyReportDraftWorkflow(session, source, self._report_provider)`로 LLM을 주입한다.
- `bootstrap/meeting_worker.py:39-42` — worker는 `WorkflowApplication(settings, provider)`를 자기 것으로 만들고, `SonioxTranscriptionAdapter()`를 **따로 한 번 더** 만든다(전사용).
- `bootstrap/conversation_worker.py:60-62` — 대화 worker는 provider와 application을 **분리해서** 들고 있다(`create_workflow_application(settings)`는 provider 인자 없이 호출 → 그 안에서 또 하나의 Codex 어댑터가 만들어진다). **[사실]**

**[추정]** 즉 대화 worker 프로세스 안에는 Codex 어댑터 인스턴스가 두 개 존재한다(`self._provider`와 `self._application._report_provider`). 상태가 없는 어댑터라 동작상 문제로 보이지는 않으나, 사실로 기록해 둔다.

### 3.3 테스트 대역(fake/stub) 전수

| 파일:줄 | 클래스 | 무엇을 대신하나 |
|---|---|---|
| `tests/contract/test_meeting_recordings.py:38` | `RefinementProvider` | LLM. 프롬프트에 금지 문구가 들어있는지 **assert**하고(`:47`, `:54`) 스키마별로 다른 body를 돌려준다. `converse` 호출 시 `AssertionError`(`:73-74`) |
| `tests/contract/test_meeting_recordings.py:77` | `FailingMeetingProvider` | `ProviderUnavailable` 발생 경로 |
| `tests/contract/test_meeting_recordings.py:85` / `:98` / `:108` | `CompleteTranscriber` / `CleanupFailingTranscriber` / `SlowCompleteTranscriber` | STT 최종 전사 성공·정리실패·지연 |
| `tests/contract/test_meeting_recordings.py:118` | `LeaseRejectingQueue` | lease 연장 실패(fence) |
| `tests/contract/test_meeting_followups.py:20` | `FollowupProvider` | 후속업무 승격용 요약 |
| `tests/contract/test_conversation_lifecycle.py:21` | `ScriptedProvider` | `converse` 이벤트 스트림 |
| `tests/contract/test_workflow_metadata_execution.py:31` | `StubProvider` | 일일보고 workflow |
| `tests/contract/test_product_operations.py:33` · `test_mcp.py:31` | `ContractTestAiProvider` | HTTP·MCP 계약 |
| `tests/unit/test_worker_resilience.py:36` | `_NoProvider` | provider 없음 |
| `tests/integration/postgres/test_postgres_integration.py:122` · `:155` | `MeetingPipelineProvider` · `MeetingPipelineTranscriber` | postgres 통합에서의 회의 파이프라인 |

**[사실]** 실제 어댑터를 직접 검증하는 계약 테스트도 있다 — `tests/contract/test_codex_cli.py`, `tests/contract/test_soniox_adapter.py`, `tests/unit/test_codex_stream_ingest.py`, `tests/unit/test_codex_tool_summary.py`. (이번 조사에서 실행하지 않았다.)

---

## 4. Q3 — 회의 도메인의 AI 경로 (가장 중요)

### 4.1 단계별 전수 — 순서대로

#### ① 실시간 전사 — **프론트가 Soniox에 직접 붙는다**

**[사실]** 순서:
1. 브라우저가 `POST /api/meetings/{id}/recordings/start` → `state="recording"`, `provider_client_reference_id`를 `meeting-recording:{id}`로 세팅(`platform/meetings.py:292-302`).
2. 브라우저가 `POST …/recordings/{rid}/realtime-credential`(`entrypoints/http.py:705`) → `MeetingApplication.issue_realtime_credential`(`modules/meetings/application.py:310-334`). 여기서 **회의 권한 재확인**(`_recording_target` `:317`)과 **녹음 개시자 본인 확인**(`:321-322`)을 한 뒤 Soniox 임시키를 발급한다.
3. Soniox `POST /auth/temporary-api-key`(`platform/soniox.py:52-62`): `usage_type=transcribe_websocket`, `expires_in_seconds`는 60~3600으로 clamp, **`single_use: True`**, `max_session_duration_seconds`는 1~18000 검증(`:50-51`).
4. **브라우저가 반환받은 임시키로 `wss://stt-rt.soniox.com/transcribe-websocket`에 직접 연결한다** — `frontend/src/liveTranscription.ts:215-226`(`api_key: options.credential.temporary_key` 를 소켓 첫 메시지로 보냄). **백엔드는 오디오를 중계하지 않는다.**
5. 브라우저가 **확정(settled) 토큰만** 골라 `POST …/recordings/{rid}/realtime-segments`(`frontend/src/api.ts:816` → `entrypoints/http.py:681`)로 되돌려 보낸다. provisional 텍스트는 화면에만 그리고 서버로 보내지 않는다(`liveTranscription.ts:244`가 `onProvisional` 콜백으로만 넘김).
6. 서버는 `append_live_transcript`(`modules/meetings/application.py:548-581`)로 적재한다. 녹음이 열려 있을 때만(`:573-574`), 개시자만(`:571-572`), 확정 구간만(`:561-562`).

**[사실]** 실시간 결과는 `source_kind="realtime"`, `provider_reference=f"realtime:{recording.id}"`로 저장되고(`platform/meetings.py:448-451`), **최종 전사 후보에서 명시적으로 제외된다** — `latest_recorded_raw_transcript`가 `source_kind != "realtime"`으로 거른다(`platform/meetings.py:367`). 주석이 이유를 밝힌다: "The live stream heard the room, not the file"(`modules/meetings/application.py:360`).

**[사실]** ⚠ **이 단계에 LLM은 없다.** 실시간 경로는 STT 전사 텍스트 적재까지가 전부다.

#### ② 최종 전사 (FinalTranscriber)

**[사실]** `POST …/recordings/{rid}/stop`이 오디오를 업로드하면 `stop_recording`(`modules/meetings/application.py:279-308`)이 바이트를 `LocalDirectoryRecordingStorage`에 넣고(`platform/recordings.py:21-49`, sha256·size 고정) `state="uploaded"`로 바꾼 뒤(`platform/meetings.py:799`), `bootstrap/application.py:498`이 `MeetingFinalizationJob`을 durable queue에 넣는다.

**[사실]** worker가 잡을 claim하고 `finalization_input`(`modules/meetings/application.py:336-388`)으로 **stage를 결정**한다 — `transcribe` / `refinement` / `summary` 중 하나. 이미 끝난 단계는 건너뛴다(crash-resume 설계, `:361-379`).

**[사실]** `stage == "transcribe"`이면 `bootstrap/meeting_worker.py:158-163`이 Soniox `transcribe()`를 부른다. Soniox 쪽 흐름(`platform/soniox.py:75-145`): `/files` multipart 업로드 → `/transcriptions` 생성(`model: stt-async-v5`, `enable_speaker_diarization: True`) → 상태 폴링 → `/transcriptions/{id}/transcript` 수령 → **`finally`에서 transcription과 file을 모두 삭제**(`:126-134`). 삭제 실패는 예외가 아니라 `cleanup_warnings`로 도메인에 올라가 감사 이벤트가 된다(`meeting_worker.py:166-170` → `record_finalization_cleanup_warning` `modules/meetings/application.py:420-440`).

**[사실]** 결과는 `record_final_transcript`(`modules/meetings/application.py:447-494`)로 저장. **`provider_reference`가 멱등키**다(`:458-460`, DB 유니크 제약 `platform/persistence.py:349`) — 재배달되면 원본 revision을 그대로 돌려주고 텍스트를 바꾸지 않는다.

#### ③ Refinement (정제·화자) — **Codex CLI, 구조화 생성**

| 항목 | 값 | 근거 |
|---|---|---|
| provider | `WorkflowApplication._report_provider` = `CodexCliProviderAdapter` | `bootstrap/application.py:411`, `:605` |
| 호출 API | `AiProvider.generate` (대화 아님) | `bootstrap/application.py:605-610` |
| 프롬프트 | `build_refinement_prompt(raw_segments)` | `modules/meetings/refinement.py:102-112` |
| 출력 스키마 | `refinement_output_schema()` — `additionalProperties:false`, 8필드 전부 required | `modules/meetings/refinement.py:26-61` |
| 파서 | `parse_refinement` — 타입·범위·enum을 전부 재검증, 위반 시 `ValueError` | `:64-99` |
| 서버 검증 | `_validate_refinement_coverage` — 원본 segment를 **전부** 커버하는지 확인 | `modules/meetings/application.py:1051-1071` |

**[사실]** 프롬프트 원문(`refinement.py:105-111`)이 허용하는 조작은 정확히 여섯 가지다: 완전 반복 제거·띄어쓰기/구두점 수리·turn 병합·분할·명백한 STT 오인식 정정·익명 화자 경계 조정. 금지: **이름·숫자·날짜·결정·참석자·사실의 창작 또는 정규화.** `correction_kind` enum이 이 여섯을 그대로 코드화한다(`:9-11`: `none|deduplicate|merge|split|spacing|stt_correction|speaker_boundary`).

**[사실]** docstring이 안전 경계를 명시한다 — "The schema and server verifier are the safety boundary; prompt makes semantic limits explicit"(`refinement.py:103`). 즉 프롬프트는 보조이고, **정본은 스키마 + `_validate_refinement_coverage`** 다.

**[사실]** 화자는 **자동 label만** 다룬다. 사람이 확정하는 화자 매핑은 완전히 별도 경로다 — `assign_speaker_identity`(`modules/meetings/application.py:685-725`) → `MeetingSpeakerIdentityAssignmentRecord`(`platform/persistence.py:385`), 그리고 표시 시점에 자동 label보다 **우선 적용**된다(`_confirmed_members_for_raw_segments` `:889-907`, `_confirmed_member_for_refined_span` `:909-920`).

#### ④ Summary — 같은 provider, evidence 결박

| 항목 | 값 | 근거 |
|---|---|---|
| provider | 동일 `_report_provider` | `bootstrap/application.py:637` |
| 프롬프트 | `build_summary_prompt(refined_segments, kind=...)` | `modules/meetings/summary.py:77-84` |
| 출력 스키마 | `summary_output_schema()` — `body` + `statements[]` | `:20-42` |
| statement 종류 | `summary` / `decision` / `risk` / `followup` (frozenset) | `:9` |
| evidence | `refinement_start_sequence` ~ `refinement_end_sequence` (**연속 구간**) | `:12-18`, `:36-37` |
| 서버 검증 | `_validate_summary_evidence` | `modules/meetings/application.py:1073-1086` |

**[사실]** `SummaryStatement`는 텍스트와 **refinement segment의 sequence 구간**을 함께 들고 다닌다(`summary.py:12-18`). 프롬프트가 "Each statement must cite a contiguous refinement sequence range that supports it"라고 요구하고(`:81-82`), 서버가 `_validate_summary_evidence`로 존재하지 않는 구간을 거부한다. `followup`에 대해서는 프롬프트가 "A followup is a candidate, not an executed task"라고 못박는다(`:82`).

**[사실]** 저장 시 `content_hash = sha256(generation.body)`와 `provider_call_ref = generation.provider_run_ref`를 함께 남긴다(`bootstrap/application.py:649-650`; refinement도 동일 `:615-616`).

**[사실]** `kind`는 `{"provisional", "final"}`만 허용하지만(`modules/meetings/application.py:584`), **`provisional`을 만드는 호출자가 코드에 없다** — worker는 기본값 `kind="final"`로만 부른다(`bootstrap/application.py:627`, `meeting_worker.py:198-201`). 조회 뷰만 두 종류를 다 훑는다(`modules/meetings/application.py:803`). 테스트에도 `provisional` 생성 사례가 없다(`grep -rn provisional tests/` → 0 hit). **[사실]**

#### ⑤ 채택 (adopt) — 사람이 한다

**[사실]** `adopt_summary`(`modules/meetings/application.py:641-683`)는 요약 본문을 **그대로** 새 note version으로 append하고(`:661-674`), summary에는 evidence 링크를 붙인다(`_summary_source_evidence` `:1021-1033`). 기존 note를 덮어쓰지 않고, 확정된 note에는 채택할 수 없다(`:658-659`). 감사 이벤트 `meeting.summary_adopted`(`:679`).

### 4.2 상태 전이와 durable job·lease

**[사실]** `MeetingRecordingRecord.state` 전이 (`platform/meetings.py:793-842`):

```
(create) recording ──stop_recording──▶ uploaded ──mark_recording_transcribing──▶ transcribing
                                          ▲                                          │
                                          │                                          ├─ complete_recording_finalization ─▶ transcribed
                                          └── mark_recording_retryable ◀─────────────┤
                                                                                     └─ mark_recording_failed ──────────▶ failed
```

**[사실]** fence 구조 3중:
1. **transport lease** — `durable_jobs` 테이블의 `lease_token`. worker가 `claim`으로 얻고(`bootstrap/meeting_worker.py:73-82`), 백그라운드 heartbeat가 `extend_lease`로 연장한다(`:115-134`). 연장 실패 = `lease_lost` → **터미널 상태를 쓰지 않고 조용히 물러난다**(`:101-104`).
2. **recording fence** — 같은 `lease_token`이 `recording.finalization_lease_token`에 박힌다(`platform/meetings.py:808`). 모든 쓰기 지점이 `_require_finalization_lease`로 재검사한다(`modules/meetings/application.py:442-445`, 호출처 `:395`, `:407`, `:417`, `:432`, `:474`, `:535`, `:626`).
3. **stale 재점유** — `transcribing` 상태가 `stale_after_seconds`(= `meeting_queue_visibility_timeout`, 기본 120초)보다 오래 묵으면 재점유하고, 그렇지 않으면 `contended`로 되돌린다(`modules/meetings/application.py:349-356`).

**[사실]** 재시도 정책은 durable job 층에 있다 — `attempt < meeting_queue_max_attempts`(기본 3, `bootstrap/settings.py:33`)이면 `retry`, 아니면 `failed`(`bootstrap/meeting_worker.py:243-267`). 백오프는 `min(30, 2^(attempt-1))`초(`:108`), `contended`는 visibility timeout의 절반(`:110`).

**[사실]** 실패 코드 매핑(`bootstrap/meeting_worker.py:206-241`): `TranscriptionFailure` → 어댑터가 준 stable code(`provider_auth_error`·`provider_quota_error`·`provider_timeout`·`provider_format_error`·`provider_request_failed`, `platform/soniox.py:251-276`) 그대로 / `ProviderFailure`(LLM) → **`meeting_ai_provider_failed`, retryable=True** / 그 외 `Exception` → `meeting_finalization_error`, retryable=True / `MeetingVersionConflict` → `stale`(아무것도 안 씀).

**[사실]** 트랜잭션 경계: provider 호출은 **모든 DB 트랜잭션 바깥**에서 일어난다. `refine_meeting_transcript`는 "read/claim plan (tx), call the provider (no tx), persist a derived revision (tx)" 세 구간으로 나뉜다(`bootstrap/application.py:598-621`, docstring이 명시).

**[사실]** 저장 지점의 멱등성: `save_refinement`·`save_summary` 모두 이미 `completed`인 산출물이 있으면 provider를 부르지 않고 기존 것을 돌려준다(`modules/meetings/application.py:502-503`, `:537-538`, `:590-591`, `:627-629`).

### 4.3 durable job 3종

**[사실]** `modules/jobs/domain.py:14-16` — `conversation.turn` · `material.extraction` · `meeting.recording.finalize`. 회의 job의 `ordering_key`는 `recording_id`, `idempotency_key`는 `meeting.recording.finalize:{recording_id}`(`modules/meetings/jobs.py:20-26`). worker 동시성 기본 1(`bootstrap/settings.py:34`).

### 4.4 프로토타입 화면 요구 3건 대조 — **셋 다 없음**

| 요구 | 코드에 있나 | 가장 가까운 것 | 근거 |
|---|---|---|---|
| (a) 회의 **중** 실시간 AI 노트(자동 요약) | **없음** | ① 확정 STT 토큰 적재(`append_live_transcript`, `modules/meetings/application.py:548`) ② `summary_input(kind="provisional")` 슬롯 — **호출자 없음**(§4.1-④) | 실시간 경로 전체에 LLM 호출 0건. `bootstrap/application.py`의 두 `generate` 호출(`:605`, `:637`)은 모두 녹음 종료 후 worker 경로 |
| (b) 종료 후 **노트 + AI 노트 + 스크립트 합성** 초안 | **없음** | `adopt_summary` — AI summary body를 **그대로** 새 note version으로 append. 사용자가 쓴 기존 note 본문과 **합치지 않는다** | `modules/meetings/application.py:661-674` (`summary.body or ""` 하나만 body로 들어감) |
| (c) 안건(agenda) 단위 구조 | **없음** | 없음 | `grep -rniE 'agenda\|안건' backend/src frontend/src` → **0 hit** |

**[사실]** 회의 상세 응답은 note·recording·raw_transcript·refinement·speaker_assignments·summaries를 **각각 분리된 필드로** 돌려준다(`_recording_records` `modules/meetings/application.py:781-807`, `_view` `:764-780`). 합성된 하나의 초안 필드는 없다.

---

## 5. Q4 — 회의 밖 AI 경로

### 5.1 소비자 전수

| 경로 | LLM을 부르는 자리 | 어떤 API | 같은 어댑터인가 |
|---|---|---|---|
| **회의 refinement** | `bootstrap/application.py:605` | `generate` | ✅ `_report_provider` |
| **회의 summary** | `bootstrap/application.py:637` | `generate` | ✅ 같은 인스턴스 |
| **일일보고 draft** | `platform/reports.py:508-527` (`SqlAlchemyDailyReportDraftWorkflow._generate`) | `generate` | ✅ 같은 인스턴스 (`bootstrap/application.py:873`) |
| **AX 대화 turn** | `bootstrap/conversation_worker.py:176` | `converse` | ⚠ **별도 프로세스의 별도 인스턴스**(`:60`), 같은 클래스·같은 프로필 |
| 액션(action) | **LLM 직접 호출 없음** | — | 대화 turn 안에서 MCP 도구로 preview·confirm이 일어난다 |
| 자료(material) 추출 | **LLM 없음** | — | 로컬 파서 + Kiwi (§1.2) |
| 관계 그래프 | **LLM 없음** | — | 대화가 MCP 도구로 호출할 뿐 |

**[사실]** `ConversationApplication`의 docstring이 경계를 못박는다 — "API-facing command/query service. **It never invokes a provider.**"(`modules/ax_execution/conversations.py:99`).

### 5.2 MCP가 어떻게 끼는가

**[사실]** MCP는 **양방향**이다.
- **안으로**: `entrypoints/mcp.py`가 SCAX operation들을 도구로 노출한다(`_register_action_item_tools` `:652` / `_register_daily_report_tools` `:708` / `_register_work_request_*` `:750`, `:771` / `_register_meeting_tools` `:800` / `_register_task_tools` `:827` …). 회의 도구는 **읽기 2개뿐** — `meeting_list`(`:812`), `meeting_get`(`:823`), 그것도 `MEETING_READ` capability가 있어야 등록된다(`:801-802`). **회의 refinement·summary·녹음 관련 MCP 도구는 없다.** **[사실]**
- **밖으로**: `create_codex_cli_provider`가 Codex CLI에 **SCAX MCP 서버 하나만** 물린다 — `sys.executable -m ax_workspace.entrypoints.mcp`(`bootstrap/application.py:1707-1716`). Codex 쪽 config override는 `_mcp_overrides`(`platform/codex_cli.py:259-273`)가 만들고, 넘어가는 환경변수는 화이트리스트 4개(`AX_MCP_PERSONA`·`AX_MCP_CAUSATION_ID`·`AX_PROFILE`·`DATABASE_URL`, `:270`)로 제한된다. 페르소나는 **프로세스 환경으로만** 전달되며 도구 인자가 아니다(`entrypoints/mcp.py:1-5` docstring, `platform/codex_cli.py:41` `AiDelegatedToolContext` 주석: "it is never prompt content").

**[사실]** `converse`는 MCP 바인딩이 없으면 **명시적으로 실패한다**(`platform/codex_cli.py:262`, `:282`). 반면 `generate`는 MCP를 붙이지 않는다(`_arguments` `:352-394`에 `_mcp_overrides` 호출 없음) — 회의 refinement·summary는 **도구 없이 프롬프트+스키마만으로** 도는 순수 생성이다. **[사실]**

### 5.3 "회의 refinement/summary를 대화 경로로 돌릴 수 있는 구조인가" — 사실만

**[사실]** 구조적 사실 네 가지. (판단은 하지 않는다.)
1. `AiProvider` port 하나에 `generate`와 `converse`가 **둘 다** 있다(`modules/ax_execution/ai.py:129-141`). 같은 어댑터가 둘 다 구현한다.
2. 회의 경로는 현재 `generate`만 쓴다. `converse`는 대화 worker만 쓴다.
3. 회의용 테스트 대역들은 `converse` 호출 시 **일부러 `AssertionError`를 던진다** — "refinement must use structured generation, not chat"(`tests/contract/test_meeting_recordings.py:73-74`), "meeting finalization must use structured generation"(`:81-82`). 즉 현재 계약 테스트가 회의의 chat 경로 사용을 **금지 방향으로 고정**하고 있다.
4. 대화 경로에는 회의를 **읽는** 도구 2개가 있다(`meeting_list`·`meeting_get`) — 즉 대화가 회의 내용을 조회하는 통로는 이미 열려 있다. 회의를 **쓰는** 도구는 없다.

---

## 6. Q5 — 문서 ↔ 코드 대조

### 6.1 일치 확인 (문서가 말한 대로 코드가 있는 것)

| 문서 | 코드 | 근거 |
|---|---|---|
| system.md:65 「Recording은 provider ref·storage key를 API에 노출하지 않는 port」 | 일치 — `_recording_view`가 `storage_key: None`을 명시적으로 박고(`modules/meetings/application.py:834`), `provider_file_ref`·`provider_transcription_ref`는 뷰에 없음 | `modules/meetings/application.py:820-835` |
| system.md:66 「realtime credential은 서버에서 Meeting authorization 뒤 단기 발급」 | 일치 — 권한+개시자 재확인 후 `single_use` 임시키 | `modules/meetings/application.py:317-326`, `platform/soniox.py:52-62` |
| system.md:68 「realtime segment와 stored recording 기반 final transcription은 별도 ingestion path」 | 일치 — `source_kind`로 분리, final 후보에서 realtime 제외 | `platform/meetings.py:367`, `:448-451` |
| system.md:69 「worker는 durable job lease와 fence로 stale completion을 차단」 | 일치 — 3중 fence(§4.2) | `bootstrap/meeting_worker.py:101-134`, `modules/meetings/application.py:442-445` |
| spec-004:60 「refinement는 원본을 덮어쓰지 않고 새 version」 | 일치 | `platform/meetings.py:523-546` (별도 테이블) |
| spec-004:61 「사람 speaker mapping은 자동 label과 별도 revision, 이후 표시에서 우선」 | 일치 | `modules/meetings/application.py:889-920` |
| spec-004:62-63 「summary는 version과 인용 범위를 evidence로. 없는 범위 연결 불가」 | 일치 | `modules/meetings/application.py:1073-1086` |
| spec-004:64 「오래된 worker 결과는 저장하지 않는다」 | 일치 | `_require_finalization_lease` 전 호출처 |
| spec-004:65 「summary는 채택 전 제안」 | 일치 — `adopt_summary`가 사람의 명령 | `modules/meetings/application.py:641` |
| action-execution.md:64 「credential은 server-side 보관 또는 임시 발급, client 응답에 장기 secret 금지」 | 일치 — 장기 키는 프로세스 환경에만(`platform/soniox.py:1-6` docstring), 응답은 임시키 | `platform/soniox.py:43`, `:57` |

### 6.2 어긋나거나 한쪽에만 있는 것

| # | 지점 | 문서 | 코드 | 근거 |
|---|---|---|---|---|
| ① | **provisional summary** | spec-004:34 «아직 제공하지 않거나 미결»에 `provisional live summary`를 명시 | **슬롯은 있고 생산자는 없다.** `kind` 검증(`application.py:584`)·DB 컬럼 주석 `provisional \| final`(`persistence.py:463`)·조회 뷰 순회(`application.py:803`)·프론트 라벨 「실시간 요약 초안」(`frontend/src/MeetingDrawer.tsx:497`)까지 있으나 만드는 호출자가 없다 | `grep -rn 'kind="provisional"' backend/` → 0 hit |
| ② | **provider 이름이 애플리케이션 층에 있다** | system.md:18(spec-004 인용) «특정 provider는 사용자 계약이 아니다» / system.md:67 «Soniox는 adapter detail» | `modules/meetings/application.py:575`가 `provider="soniox"`를 **모듈 층에서 하드코딩**한다. `bootstrap/meeting_worker.py:174`도 동일 | 같은 줄 |
| ③ | **모델명이 모듈 층에 있다** | action-execution.md:62 «model … adapter는 교체 가능하며 domain identity를 소유하지 않는다» | `modules/reports/workflow_metadata.py:18`에 `"codex-cli:gpt-5.6-terra:fast:low"`가 상수로 있고 `:72`에서 **검증 기준**으로 쓰인다 | 같은 줄 |
| ④ | **경계 규칙의 사각지대** | (문서 아님 — 코드 규칙) `tests/architecture/test_architecture.py:84-92`가 provider 정책 문자열을 금지 | 검사 대상이 `modules/reports/application.py`·`platform/reports.py` **둘뿐**. `modules/reports/workflow_metadata.py`와 `modules/meetings/*`는 검사되지 않는다 | 같은 줄 |
| ⑤ | **worker 수** | system.md:69 «transcription·refinement·summary worker» (셋을 나열) | **단일 worker 프로세스**가 한 job 안에서 셋을 순차 실행한다 | `bootstrap/meeting_worker.py:157-205` — [추정] 문서가 논리적 역할을 나열한 것인지 별개 프로세스를 뜻하는지 문서만으로는 갈리지 않는다 |
| ⑥ | **AX 실행 문서에 회의 LLM 언급 없음** | action-execution.md는 Conversation/Turn/tool/durable job만 다룬다 | 회의 refinement·summary가 **AX와 같은 `AiProvider` port·같은 어댑터**를 쓴다는 사실이 어느 문서에도 없다 | `bootstrap/application.py:411`, `:605`, `:637`, `:873` — [추정] 문서 공백(모순은 아님) |
| ⑦ | **취소 계약** | action-execution.md:31 «취소는 현재 Turn의 후속 effect와 final 저장을 막고» | 회의 경로는 취소 불가 — `generate`에 cancel 인자가 없다. 회의 job은 lease 상실로만 물러난다 | `modules/ax_execution/ai.py:130` vs `:132-141` — [추정] 문서 §2는 Conversation 한정이므로 위반은 아니고, 회의 취소는 문서·코드 **양쪽에 없다** |
| ⑧ | **모델 설정의 운영 통로** | action-execution.md:62 «adapter는 교체 가능» | 교체 통로가 **테스트 주입뿐**이다. `Settings`에 모델·프로필 필드가 없고 `create_codex_cli_provider`는 profile을 넘기지 않는다 | `bootstrap/settings.py:18-36`, `bootstrap/application.py:1705-1716` |

**[사실]** ①~④는 코드 인용으로 확인한 사실이다. ⑤~⑦은 문서 해석이 갈릴 수 있어 **[추정]** 으로 표시했다.

---

## 7. Q6 — 실행·검증 환경

### 7.1 실제로 provider를 부르려면

| provider | 필요한 것 | 근거 |
|---|---|---|
| **Codex CLI** | ① `codex` 바이너리가 `PATH`에 있을 것(`shutil.which`) ② **`~/.codex/auth.json` 파일이 존재**할 것 — 없으면 `ProviderUnavailable` ③ 쓰기 가능한 `.scax/codex-runtime` (여기에 `AGENTS.md`·`config.toml`·비-`.system` skill이 있으면 **거부**) | `platform/codex_cli.py:85-88`, `:711-736`, `:56-57` |
| **Soniox** | 환경변수 **`SONIOX_API_KEY`** — 없으면 모든 호출이 `provider_unavailable`(retryable=False) | `platform/soniox.py:43`, `:186-187` |

**[사실]** Soniox 키 로딩 관례: `Makefile:2-5`가 `SONIOX_ENV_FILE ?= $(HOME)/.config/soniox/env`를 `set -a`로 읽어 넣는다. 주석이 정책을 밝힌다 — «Absent file = the feature reports itself unavailable; **it never falls back to a stub that pretends to transcribe.**»(`Makefile:3-4`). 이 로딩은 `api`(`:69`), `meeting-worker`(`:78`), `api-e2e`(`:91`), `soniox-smoke`(`:269`) 타깃에만 붙는다 — `conversation-worker`·`material-worker`에는 붙지 않는다. **[사실]**

**[사실]** 그 외 실행 환경변수(`bootstrap/settings.py:47-74`): `AX_PROFILE`·`DATABASE_URL`·`AX_JOB_QUEUE_BACKEND`(postgres|memory, 기본 postgres)·`AX_MATERIALS_DIR`·`AX_RECORDINGS_DIR`·`AX_MEETING_QUEUE_VISIBILITY_TIMEOUT`·`AX_MEETING_QUEUE_MAX_ATTEMPTS`·`AX_MEETING_WORKER_CONCURRENCY`·`AX_DEMO_EMAIL_DOMAIN`. 제거된 `AX_CONVERSATION_QUEUE_BACKEND`는 **fail-fast**로 거부된다(`:82-87`).

### 7.2 Makefile 타깃

| 타깃 | 하는 일 | 외부 호출 |
|---|---|---|
| `make test` (`Makefile:21`) | `pytest -m 'not integration'` | **없음** — 전부 대역 |
| `make test-postgres` (`:25`) | `AX_POSTGRES_TEST_URL=… pytest -m integration` | DB만. AI는 대역(`MeetingPipelineProvider`·`MeetingPipelineTranscriber`) |
| `make meeting-worker` (`:77-78`) | Soniox env 로드 후 `python -m ax_workspace.entrypoints.meeting_worker` | **Soniox + Codex 실호출** |
| `make api` (`:69`) | Soniox env 로드 후 uvicorn | 실시간 credential 발급만 |
| `make conversation-worker` (`:71-72`) | 대화 worker | **Codex 실호출** |
| `make local-stack` (`:100-127`) | API + 대화·자료·회의 worker + 프론트를 한꺼번에 띄우고 감독 | 전부 |
| `make e2e-meeting-live-transcript` (`:198-199`) | Chrome이 wav를 가짜 마이크로 재생 → Soniox 실시간 전사 → 파일 전사가 대체 | **실 Soniox + 실 마이크.** `acceptance-e2e`에서 **제외됨**(`:96`) |
| `make soniox-smoke` (`:267-269`) | opt-in. `SONIOX_API_KEY` 없으면 **non-zero exit**, 절대 가짜로 대신하지 않음. request id·소요시간만 출력 | 실 Soniox |
| `make live-report-smoke` (`:271-272`) | opt-in 실 Codex 증거. WorkflowRun·NodeRun 4개·ProviderCall provenance 확인. **본문·프롬프트는 출력하지 않음** | 실 Codex |

**[사실]** `backend/scripts/soniox_smoke.py:43-44`가 키 부재 시 stderr에 «the smoke needs a real credential and will not fake one» 을 찍고 종료한다. `:63`은 발급된 임시키가 장기 키와 **같지 않은지** 검증한다.

### 7.3 테스트 격리

**[사실]** pytest 마커 5종(`backend/pyproject.toml:36-42`): `unit`·`contract`·`integration`·`architecture`·`e2e`. `integration`은 «requires an explicit disposable PostgreSQL URL»(`:39`). 기본 `make test`가 `-m 'not integration'`이므로 통합은 **명시적 opt-in**이다.

**[사실]** 의존성(`backend/pyproject.toml:6-19`): fastapi·mcp·pydantic·sqlalchemy·psycopg·uvicorn·pypdf·python-docx·openpyxl·python-pptx·pyyaml·kiwipiepy. dev(`:28-32`): httpx·pytest. **anthropic·openai·litellm·google-genai·soniox SDK 모두 없다** — Soniox는 표준 라이브러리 `urllib`로, Codex는 `subprocess`로 부른다. 코디의 관찰(「httpx만 있고 SDK가 없다」)은 정확하나, `httpx`는 **dev 그룹**이며 FastAPI TestClient용이지 provider 호출에 쓰이지 않는다. **[사실]**

---

## 8. 자기점검

- Q1~Q6 각 절: §2(Q1) · §3(Q2) · §4(Q3) · §5(Q4) · §6(Q5) · §7(Q6) — **전부 비어 있지 않음.**
- 모든 사실 주장에 `파일:줄` 인용을 달았다. 인용 없는 문장은 [추정] 표기이거나 절 제목이다.
- 환경변수 **값**·API 키·auth 파일 내용은 하나도 인용하지 않았다. 이름과 경로만 적었다.
- 테스트·서버·DB·외부 API를 실행하지 않았다.
- 워크트리 상태 (조사 시작·종료 시점 모두 확인):
  - `git -C /Users/kknaks/orca/workspaces/ax-workspace/sc-meeting status --porcelain` → **빈 출력**
  - `git -C /Users/kknaks/orca/workspaces/mediness-mediness/sc-meeting-spec status --porcelain` → **빈 출력**

---

## 9. 코디가 물어봐야 할 것 (내가 판단하지 않는다)

1. **실시간 AI 노트를 어느 provider로 돌릴 것인가.** 현재 실시간 경로에는 LLM이 전혀 없고(§4.4-a), 유일한 LLM 어댑터는 90초 타임아웃의 CLI subprocess다(`platform/codex_cli.py:55`). 회의 중 짧은 주기로 반복 호출하는 용도로 이 어댑터를 그대로 쓸지, 다른 배선이 필요한지는 사용자 결정 사항이다.
2. **`provisional` 슬롯을 쓸 것인가.** 스키마·DB 컬럼·조회 뷰·프론트 라벨까지 이미 있는데 생산자만 없다(§6.2-①). spec-004:34는 이걸 «아직 제공하지 않음»으로 두고 있다 — 슬롯을 채우는 것이 SPEC 개정을 요구하는지 확인 필요.
3. **「합성 초안」의 정의.** 지금 `adopt_summary`는 AI 요약을 **그대로** note version으로 붙인다(§4.4-b). 사람이 쓴 기존 note 본문과 AI 노트와 스크립트를 합치는 것이 (ㄱ) 새 LLM 호출인지 (ㄴ) 서버 측 결합 로직인지 (ㄷ) 프론트 표시 조합인지에 따라 필요한 백엔드 작업이 완전히 달라진다.
4. **안건(agenda) 축을 도메인에 넣을 것인가.** 백엔드·프론트 전수 0 hit(§4.4-c). 새 테이블·새 계약이 필요한 범위이므로 SPEC 선행 여부를 정해야 한다.
5. **모델 설정을 운영에서 바꿀 수 있어야 하는가.** 지금은 `Settings`에 통로가 없고 테스트 주입만 가능하다(§2.3·§6.2-⑧). 회의용과 대화용에 다른 모델·타임아웃을 주고 싶다면 이 통로부터 결정이 필요하다.
6. **`provider="soniox"` 하드코딩(모듈 층)을 이번 작업 범위에 넣을 것인가.** system.md:67의 「adapter detail」 선언과 코드가 어긋나는 지점이다(§6.2-②). 회의 화면 작업과 별개 정리 건인지 확인 필요.
7. **회의 refinement/summary의 실패가 화면에 어떻게 보여야 하는가.** 현재 LLM 실패는 `meeting_ai_provider_failed`로 3회까지 재시도 후 `recording.state="failed"`가 된다(`bootstrap/meeting_worker.py:226-233`, `:253-265`). 프로토타입 화면이 부분 성공(전사는 됐는데 요약만 실패)을 어떻게 보여줄지는 화면 스펙 사항이다.
8. **다음 조사(프론트) 범위 확인.** 이번 조사는 `frontend/`를 Q3-1에 필요한 최소 인용(`liveTranscription.ts:215-226`·`api.ts:804,816`)으로만 봤다. `MeetingDrawer.tsx`(현재 회의 UI)의 전수는 다음 조사 몫으로 남겼다.

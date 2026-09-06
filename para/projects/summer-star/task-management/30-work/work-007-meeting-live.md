---
type: work
id: WORK-007
title: "회의록 — 회의 중 · STT 중계 · 2트랙 · AI 배치 · 일시정지"
status: done
product: "task-management"
work_type: new-feature
owner: ""
roles:
  pm: ""
  design: ""
  fe: ""
  be: ""
  qa: ""
  ops: ""
progress: 100
created_at: 2026-09-06
updated_at: 2026-09-06
tags:
  - product/task-management
  - doc/work
  - status/done
links:
  baselines: [BASE-003]
  decisions: [DEC-003]
  specs: [SPEC-007]
  works: [WORK-006]
  releases: []
  related: [DEC-001, DEC-002, DEC-004, SPEC-006, SPEC-008, SPEC-005, SPEC-001]
---

# 회의록 — 회의 중 · STT 중계 · 2트랙 · AI 배치 · 일시정지

**회의가 시작된 뒤부터 「회의 종료」 직전까지를 세운다.** 내 마이크 소리가 백엔드를 거쳐 Soniox 로 가고 확정 발화가 우측에 쌓이며, 사람은 `/` 프롬프트로 회의록 탭을 채우고 AI 는 배치마다 AI 요약 탭만 채운다. 마이크·스트림이 끊기면 **일시정지 상태로 떨어뜨리고** 사용자가 재개한다. 회의를 만들고 시작하는 것(WORK-006)과 끝내고 통합·편집하는 것(WORK-008)은 만들지 않는다.

> 1 파일 = 1 work = **빌드 계획**. dev가 이 문서만 보고 PR 분리 / 일정 / 작업 시작이 가능해야 한다.
> SPEC의 외부 계약 본문은 복제하지 않고 frontmatter `links.specs`와 index에서 연결한다.

## Meta

- Baseline: BASE-003 — **이 work 가 제품에서 기술 난도가 가장 높다**(L53 「웹소켓 2단 중계·배치 세션 유지·화자 분리 정확도·실패 처리가 얽힌다」). Phase 를 그 축 넷으로 쪼갰다
- Covers spec: **SPEC-007**(회의록 — 회의 중 · 실시간 받아쓰기 · 2트랙 · AI 배치 · 일시정지)
- Depends on work: **WORK-006**(`meeting` 도메인 6 테이블 · `MeetingDetail` · `/start` · 안건 표면 `POST/PATCH/DELETE …/agendas` · 첨부 팝오버·파일 드로어 · 회의 상세 라우트 `/meetings/detail?id=` 의 `scheduled` 분기) · **아키텍처 반영분**(ERD 2026-09-06 개정 — `meeting.recording_started_at` · `meeting_agenda.state` CHECK `active` + NULL · `meeting_agenda.source_agenda_id` · 부분 UNIQUE `active` · `backend/README.md` §8-2 표의 `invalid_meeting_status`·`meeting_stream_active`) · WORK-004(`task_service` 조회 — 웜스타트 업무 목록 · `DrawerFrame` · `AttachmentPopover`) · WORK-001(`integrations/` 뼈대 · compose 의 Redis·worker · `STORAGE_ROOT`)
- Parallel work: **WORK-006 과 리비전 경계를 나눈다** — 이 work 는 WORK-006 리비전이 만들지 않은 컬럼만 보강 리비전으로 낸다(§Domain / Schema)
- Follow-up work: **WORK-008**(회의 종료 · 최종 배치 · 통합본 · AI 한 줄 요약 · 편집 · 업무 연동) — 이 work 의 `AgendaLineTree` · 배치 서비스 · `GET …/transcript` · 근거 칩 스크롤을 그대로 물려받는다
- **External dependency**
  - **코드 레포는 별도다** — `github.com/kknaks/task_management`. 이 워크트리에 코드를 만들지 않는다
  - **Soniox**(`stt-rt-v5` WebSocket) — long-lived 키 `SONIOX_API_KEY` 가 `.env` 에 **이미 들어와 있다.** `.env.example` 에 자리를 추가한다(Phase 1). **값을 문서에 쓰지 않는다**
  - **open-kknaks 워커**(codex CLI) — compose 에 이미 있다(WORK-001). 이 work 는 `AgentClient` 로 **웜스타트·증분 배치**를 제출한다. 최종 배치·통합은 WORK-008
  - **Tauri 웹뷰의 `getUserMedia`** — 별도 스파이크 없이 이 work 에서 실물로 확인한다(DEC-003 OQ-3 · §C-7). macOS 상시, Windows 는 별도 확인 시점

## Work Summary

| Field | Value |
|---|---|
| Type | new-feature |
| Owner |  |
| Status | done |
| Progress | 100% |
| Branch/PR | `kknaksss/docs-v1` — b09a16a · ecb7f07 · ac9ee5b |
| Blocker | WORK-006 Phase(회의 도메인 리비전 · `/start` · `MeetingDetail`) 완료 전에는 Phase 2 이후를 시작하지 않는다 |
| Next | Phase 1 — 스키마 보강 · env · 외부 어댑터 뼈대 |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM |  | 범위 확정 · SPEC-007 §6 Acceptance **26개** 대조 | todo |
| Design |  | AI 요약 탭 트리(시안 없음 — [09] 조립) · 회색 상태 바 사유 4종 · 「재개」 버튼 · 「안건 선택」 상태 · 빈 상태 2종 · 1280 반응형 | todo |
| FE |  | `useMeetingStream` 상태 기계 → `AgendaLineTree`·`TranscriptPanel`·`MeetingStatusBar`·`PromptBar` 공용화 → 회의 중 화면 조립 | todo |
| BE |  | 보강 리비전 · WS 2단 중계 + 녹음 적재 · 줄/안건 상태/트랜스크립트 API · 웜스타트 · 배치 트리거·검증·push | todo |
| QA |  | Phase 검증(앱 창 E2E — 마이크·서버 내리기·워커 멈추기) · 대역 어댑터 테스트 · 정적 검사 | todo |
| Ops |  | `.env.example` `SONIOX_API_KEY` 자리 · NPM 리버스 프록시의 **WS upgrade** 통과 · `STORAGE_ROOT` 볼륨 용량 | todo |

## Scope

포함:

- **스키마 보강 리비전** — WORK-006 리비전에 없는 것만: `meeting.recording_started_at` · `meeting_agenda.state` CHECK(`next|active|done`, NULL 허용) · `meeting_agenda.source_agenda_id` · 부분 UNIQUE `(meeting_id) WHERE track='human' AND state='active'`
- **외부 어댑터 3종** — `integrations/soniox.py`(WS 클라이언트) · `integrations/agent.py`(`AgentClient` 싱글턴 + 옵션 빌더 한 곳) · `integrations/storage.py`(녹음 원본 append)
- **REST 3표면** — `POST …/lines`(`recording` · 사람 줄) · `PATCH …/agendas/{agendaId}` 의 **`state` 축**(WORK-006 의 `title` 표면에 더한다 · `active` 최대 하나 · 전환 이벤트) · `GET …/transcript`
- **`/start` 확장** — WORK-006 의 상태 전이에 **`recording_started_at` 기록 + 웜스타트 제출(`ai_session_id` 저장 · 결과 무시)** 를 같은 요청 안에 더한다
- **WS `/api/meetings/{id}/stream`** — 첫 프레임 인증 · Soniox 중계 · 녹음 append(실패 시 끊음) · 잠정/확정 발화 push · 발화 블록 경계 · `pause`/`resume` · 백프레셔 · close code · **회의당 하나** · **자동 재연결 없음**
- **배치 파이프라인** — 트리거 3종(600자 · 안건 전환 80자 · 180초) · 회의당 세션 하나(동시 실행 금지) · 120초 타임아웃 · `resume` 세션 · `output_schema` 강제 + 재검증 4단(실패 → 다음 배치 / 스키마 위반 → 전체 폐기 / 화이트리스트 밖 → `action` 강등 / 적재) · `meeting_batch_run` 커서 · **WS 즉시 push**
- **프론트 공용 부품** — `AgendaLineTree`(회의록 탭·AI 탭·WORK-008 통합본 탭이 **같은 컴포넌트**) · `EvidenceChip` · `TranscriptPanel`(따라가기 · 하이라이트 · 스크롤 API) · `MeetingStatusBar`(상단 바 한 자리 — 회의 중 5상태) · `PromptBar` + `LineKindPopover`(4종 + 새 안건 + 이동) · `useMeetingStream`(WS 클라이언트 + 상태 기계 + 마이크 캡처)
- **회의 중 화면** — `/meetings/detail?id=` 의 `recording` 분기 · 헤더(일시정지/재개 · 회의 종료 자리) · 회의록 탭 · AI 요약 탭(배치 회차 · 미확인 점) · 실시간 스크립트 · 첨부 탭(WORK-006 재사용) + **회의 중 첨부 열기 드로어** + 로컬 업로드 v2 게이트 · 반응형 3구간
- **일시정지 = 마이크 실패·스트림 끊김의 처리 경로**(DEC-003 §1 표) — 사용자 일시정지 · 마이크 끊김 · WS 끊김(`upstream`/`write_failed`/네트워크) 넷이 같은 상태 기계로 들어간다

제외:

- **회의 종료(`/end`) · 「생성중」 · 최종 배치 · 통합본 · AI 한 줄 요약 바 · 편집(수정 · 종류 전환 · 드로어 3종 · **줄 삭제 · 안건 이름 수정**) · 업무 생성/갱신 버튼** → **WORK-008**. 헤더의 「회의 종료」는 **자리 + 활성 조건만** 그린다
- 회의록 생성 · 목록 · 시작 전 안건 · `/start` 의 상태 전이 자체 · 첨부 추가/제거 계약 · 삭제 → **WORK-006**
- 시스템 오디오 · 300분 초과 · 세션 경계 복원 · 회의 중 md 작성 · 문서 AI 컨텍스트 · 화자 이름 매핑 — v1 에 없다(SPEC-007 §1 Out)
- **오디오 포맷 확정** — 구현 시점 결정(§C-8). 이 문서는 `auth.audio{format,sampleRate,channels}` 선언 계약만 전제한다

## Code Surface

- Repo / module: `github.com/kknaks/task_management` — `app/back`(BE) · `app/front`(FE)
- 만질 파일 후보 — 경로는 `backend/README.md` §4 · `frontend/README.md` §2 의 트리를 따른다

| 경로 후보 | 설명 |
|---|---|
| `app/back/alembic/versions/*_meeting_live.py` | **보강 리비전 1건** — `recording_started_at` · `state` CHECK/NULL · `source_agenda_id` · 부분 UNIQUE. `downgrade` 작성. WORK-006 리비전이 이미 만든 컬럼은 건드리지 않는다 |
| `app/back/models/meeting.py` | 위 컬럼 반영(WORK-006 파일에 **추가**) · `MeetingAgendaState` `StrEnum` 은 `core/enums.py` |
| `app/back/.env.example` | **`SONIOX_API_KEY=` 자리 추가**(값 없음). `AI_TIMEOUT_SEC` 주석에 배치 상한 120초 명시 |
| `app/back/config.py` | `SONIOX_API_KEY`(기본값 없음 — 없으면 기동 실패) · `MEETING_BATCH_*` 5수치(600 · 80 · 180 · 120 · 세션 1)를 env 로 — 실측 조정 가능(DEC-003 §STT) |
| `app/back/integrations/soniox.py` | Soniox WS 클라이언트 — config 전송(`stt-rt-v5` · `ko` · diarization · endpoint off) · 오디오 전달 · 토큰 수신 · 종료 프레임. **키는 여기서만 읽는다** |
| `app/back/integrations/storage.py` | `append_recording(meeting_id, chunk)` — `STORAGE_ROOT/recordings/{id}` · `anyio.to_thread` · 실패는 예외 전파 |
| `app/back/integrations/agent.py` | `AgentClient` 싱글턴 · **옵션 빌더 한 함수**(새 세션 / `resume`) · `output_schema` 경로 |
| `app/back/ai_schemas/meeting_batch.json` | 배치 출력 스키마(SPEC-007 §4 「배치 출력」). WORK-008 최종 배치가 같은 파일을 쓴다 |
| `app/back/service/meeting_stream_service.py` | WS 세션 1개/회의 레지스트리 · 인증 · 업스트림 연결 · 청크 ①append→②전달 · 잠정/확정 분기 · **블록 경계**(화자 변경 · 300자 · 2초) · `pause`/`resume` · 백프레셔 · `finally` 업스트림 닫기 |
| `app/back/service/meeting_batch_service.py` | 트리거 평가 · 단일 실행 락 · 미처리 커서 · 입력 조립(구간 + 사람 안건·줄 + AI 안건 + 화이트리스트) · 제출 · 검증 4단 · 적재 · push 훅 |
| `app/back/service/meeting_service.py` | WORK-006 파일에 **추가** — `/start` 의 `recording_started_at` + 웜스타트 · `add_line`(recording) · `set_agenda_state`(active 유일 · 완료 시 다음 활성 · 전환 이벤트 → 배치 트리거) · `get_transcript` |
| `app/back/repository/meeting_line_repository.py` · `meeting_transcript_repository.py` · `meeting_batch_run_repository.py` | dto 반환. 트랜스크립트는 `(meeting_id, at_ms)` 정렬 |
| `app/back/api/meeting_stream_router.py` | `WS /api/meetings/{id}/stream` — 첫 프레임 인증만 여기서, 나머지는 서비스 |
| `app/back/api/meeting_router.py` | WORK-006 파일에 **추가** — `POST …/lines` · `PATCH …/agendas/{agendaId}` 의 `state` · `GET …/transcript` |
| `app/back/schemas/meeting.py` · `dto/meeting.py` | `LineCreate` · `AgendaPatch`(`title \| Unset` · `state \| Unset`) · `TranscriptResponse` · WS 프레임 모델(`StreamAuth` · `StreamPause` · 서버 프레임 5종) |
| `app/back/tests/test_meeting_stream.py` · `test_meeting_batch.py` · `test_meeting_live_api.py` | 대역 어댑터(Soniox · AgentClient · storage)로 §Execution 검증 항목. **BE §12 필수 테스트 6·7** |
| `app/front/src/lib/api/ws.ts` | WS 열기 + **첫 프레임 토큰** + `4401` 시 refresh 1회 후 재연결 1회(FE §4-2 규약의 WS 판) |
| `app/front/src/features/meetings/hooks/useMeetingStream.ts` | **상태 기계**(`connecting`·`live`·`paused/user`·`paused/mic`·`paused/stream`) · 마이크 캡처(`getUserMedia` · 트랙 `ended` 감지) · 프레임 송수신 · 잠정/확정/AI 증분 분배. **자동 재연결 코드가 없다** |
| `app/front/src/features/meetings/hooks/useMeetingLive.ts` · `useMeetingMutations.ts` | 상세·트랜스크립트 쿼리 · 줄 추가 · 안건 상태 뮤테이션 · 무효화(`['meetings','detail',id]`) |
| `app/front/src/features/meetings/components/AgendaLineTree.tsx` · `AgendaHeader.tsx` · `LineRow.tsx` · `EvidenceChip.tsx` | **트랙 무관 트리 한 벌** — 회의록 탭 · AI 탭 · (WORK-008) 통합본 탭이 props 만 다르게 쓴다 |
| `app/front/src/features/meetings/components/TranscriptPanel.tsx` | 발화 블록 · 잠정 발화 · 따라가기 · `scrollToRange(fromMs,toMs)` + 하이라이트 · 푸터 문구 |
| `app/front/src/features/meetings/components/MeetingStatusBar.tsx` | **상단 바 한 자리** — 회의 중 5상태(연결 중 · 기록 중 · 일시정지 3사유). WORK-008 이 `generating`·실패 배너·한 줄 요약 변형을 같은 컴포넌트에 더한다 |
| `app/front/src/features/meetings/components/PromptBar.tsx` · `LineKindPopover.tsx` | `/` 팝오버 4종 + 새 안건 + 이동 · 활성 안건 칩 · 「안건 선택」 상태 · 전송 중 잠금 |
| `app/front/src/features/meetings/components/MeetingLiveView.tsx` | 회의 중 화면 조립 — 헤더 · 상태 바 · 좌(탭 2) · 우(탭 2) · 반응형 |
| `app/front/src/features/meetings/components/AttachmentViewerDrawer.tsx` | 첨부 열기 드로어(미리보기 / 원문 텍스트, 읽기 전용). WORK-006 이 시작 전 화면에서 먼저 만들었으면 **재사용**(SPEC-007 §7-D D-5) |
| `app/front/src/app/(app)/meetings/detail/page.tsx` | WORK-006 껍데기에 **`status='recording'` 분기** 추가(F-10) |
| `app/front/src/lib/datetime.ts` | `msToWallClock(recordingStartedAt, ms)` 한 곳 — 발화 시각·근거 칩 시각 |

- Domain / schema note: **보강 리비전이 필요하다**(WORK-006 리비전에 없는 컬럼만). 스키마 전문은 코드·migration 이 SoT 이고 이 문서는 범위와 불변식만 적는다

## Domain / Schema

| Entity | 역할 |
|---|---|
| `meeting` | `recording_started_at`(실적 시작 — 경과 시간·`at_ms`·근거 칩 벽시계의 **기준점**) · `ai_session_id`(웜스타트가 만든 codex 세션 — 회의당 하나) · `recording_path` |
| `meeting_agenda` | 사람 트랙 `state`(`next|active|done`, `active` 최대 하나) · AI 트랙 `source_agenda_id`(미러하는 사람 안건, NULL = AI 신설) |
| `meeting_line` | `track='human'`(회의 중 사람 줄 — `detail`·`evidence`·`task_id` 비어 있다) · `track='ai'`(배치 INSERT 만, UPDATE 없음) |
| `meeting_transcript` | 확정 발화 블록 — `speaker_label`(번호 문자열) · `at_ms`/`end_ms`(오프셋) · 잠정 토큰은 **저장하지 않는다** |
| `meeting_batch_run` | `seq` · `from/to_transcript_id` 커서 · `phase='incremental'` · `status ∈ {succeeded, discarded, failed}` · 「배치 n회」는 성공분 최대 `seq` 의 **파생** |

- 상태 / invariant: `domains/meeting.md` **M-1-a**(`recording_started_at` 기준점) · **M-5**(줄은 안건에 · 트랙 동일) · **M-5-a·b·c**(AI 안건 트랙 · `source_agenda_id` · `active` 최대 하나) · **M-5-d·e**(회의 중 안건 삭제·제목 수정 없음) · **M-6**(AI 는 `ai` 에만 INSERT, 사람 안건·줄은 읽기 전용 컨텍스트) · **M-6-a**(증분 즉시 push) · **M-7**(회의 중 증분만) · **M-9**(확정만 저장) · **M-10**(익명 라벨) · **M-11**(오프셋) · **M-12**(세션 하나) · **M-13**(녹음 영구) · **M-14**(사람 `task_id` 는 버튼) · **M-15·M-15-a**(화이트리스트 · 무소속) · **M-16**(스키마 위반 전체 폐기) · **M-18**(300분 미처리)
- Migration 필요 여부: **필요(보강 1건)**. WORK-006 리비전이 이미 `recording_started_at`·`state` CHECK·`source_agenda_id` 를 담았으면 이 리비전은 **부분 UNIQUE 만** 남는다 — Phase 1 첫 작업이 그 대조다
- SPEC 에 환류해야 하는 변경: 없음. 이 work 가 정하는 값(블록 경계 300자·2초 · 프레임 64KB/250ms · 인증 5초)은 SPEC-007 §4 에 이미 있다

## Dependency

| Consumer | Interface | 설명 |
|---|---|---|
| **WORK-008** | `AgendaLineTree` · `EvidenceChip` · `TranscriptPanel.scrollToRange` · `MeetingStatusBar` · `meeting_batch_service`(입력 조립 · 검증 4단 · `ai_schemas/meeting_batch.json`) · `GET …/transcript` · `integrations/agent.py` 옵션 빌더 | 최종 배치는 **같은 검증·같은 스키마로 범위만 전체**, 통합본 탭은 **같은 트리 컴포넌트**, 근거 칩은 **같은 스크롤 규칙**이다. 두 번째 구현을 만들지 않는다 |
| **WORK-006** (역방향) | `/start` 서비스 함수에 이 work 가 웜스타트·`recording_started_at` 을 **끼워 넣는다** | WORK-006 은 상태 전이만 만들고 훅 자리를 비워 둔다(SPEC-006 §4 「WS 연결·마이크·웜스타트는 SPEC-007 순서」) |
| 캘린더 그룹 | 없음 | 회의 일시는 WORK-006 |
| 문서함 그룹 | `GET /api/documents/{id}` · `/content` | 첨부 열기 드로어가 읽는다(SPEC-005 §4). 문서함 work 이전이면 드로어는 **「자료함이 아직 없습니다」** 빈 상태 |

## Internal Interface Contract

외부 계약(WS 프레임 · REST · 검증 · 에러)은 **SPEC-007 §4** 가 정본이다. 후속 work 가 의존하는 내부 접점만 고정한다.

| 접점 | 계약 |
|---|---|
| **`meeting_stream_service`** | 회의당 세션 레지스트리 `{meeting_id → session}` **하나**. `open(meeting_id, ws, audio_decl)` → 인증 통과 후 업스트림 연결 → `ready`. `feed(chunk)` 는 **①`storage.append_recording` → ②Soniox 전달** 순서이고 ①이 예외면 그 자리에서 `error(write_failed)` + close. `pause()`/`resume()` 는 업스트림을 닫지 않는다. `close()` 는 `finally` 에서 반드시 업스트림을 닫는다. **재연결 로직이 없다** — 끊김은 세션 삭제로 끝난다 |
| 발화 블록 경계 | 같은 화자의 확정 토큰을 모아 **화자 변경 · 300자 도달 · 토큰 간 2초 이상 공백** 중 먼저 오는 것에서 닫는다. 닫는 순간 `meeting_transcript` INSERT 와 `transcript.final` push 가 같은 시점. 잠정 토큰은 `transcript.partial` 로만(교체 렌더) |
| 백프레셔 | 클라이언트 송신 큐 상한(기본 200 프레임)을 넘으면 **잠정 프레임만 버린다.** 확정·AI 증분은 버리지 않는다 |
| **`storage.append_recording`** | `STORAGE_ROOT/recordings/{meeting_id}.{ext}` 에 append. 경로는 `meeting.recording_path` 에 첫 청크 때 기록. 일시정지 구간은 기록되지 않는다(파일 타임라인 ≠ `at_ms` — v1 재생 없음) |
| **`meeting_batch_service`** | `evaluate(meeting_id, cause ∈ {transcript, agenda_switch, timer})` 가 트리거 3종을 판정하고 `run(meeting_id)` 를 **회의당 락 하나** 아래에서 돈다. 실행 중이면 `evaluate` 는 아무것도 하지 않는다(다음 트리거 때 커진 구간으로). 커서 = 성공분 `to_transcript_id`. 검증 4단은 SPEC-007 §4 표 순서 그대로이고 **`except Exception` 없이** 워커 오류·타임아웃만 `failed` 로 잡는다. 적재 트랜잭션 커밋 직후 `meeting_stream_service.push_ai_batch(meeting_id, seq, agendas, lines)` 를 부른다 — 세션이 없으면(끊김) 건너뛰고 다음 `ready` 의 `latestBatchSeq` 로 따라잡는다 |
| 배치 입력 조립 | `{ transcript: 미처리 블록[], humanAgendas: 전량, humanLines: 구간 동안의 사람 줄[], aiAgendas: 전량, taskWhitelist: [id…] }`. **사람 안건·줄은 읽기 전용 컨텍스트**(M-6). 무소속 회의면 화이트리스트 = 프로젝트 없는 업무(M-15-a) |
| **`integrations/agent.py` 옵션 빌더** | `build_codex_options(session_id: str \| None, output_schema: Path)` 한 함수. 웜스타트는 `session_id=None`(새 세션), 배치·(WORK-008) 최종 배치·통합은 `resume={mode:"session", session_id}`. **다른 곳에서 옵션 dict 를 만들지 않는다**(BE §5-2) |
| `/start` 훅 | `meeting_service.start()` 안에서 상태 전이 → `recording_started_at=now()` → 웜스타트 제출 → `ai_session_id` 저장. **한 요청 = 한 트랜잭션**이되 codex 대기 중에는 트랜잭션을 열어 두지 않는다(BE §7) — 전이 커밋 → 제출 → 새 세션에서 `ai_session_id` UPDATE |
| `set_agenda_state` | `active` 요청 → 기존 `active` 를 `next` 로 → 대상 `active` → 커밋 → `batch_service.evaluate(cause='agenda_switch')`. `done` 요청 → 활성이었으면 다음 순서 `next` 를 `active` 로. 응답은 `MeetingDetail` |
| **`AgendaLineTree`** | `props: { track: 'human'\|'ai'\|'merged', agendas: AgendaItem[], activeAgendaId?, expandable: boolean, onToggleDone?, onChipClick?(fromMs,toMs), badgeFor(agenda) }`. **트랙별 분기가 컴포넌트 안에 없다** — 회의록 탭은 `expandable=false`, AI 탭은 `expandable=true` + `onChipClick`, WORK-008 통합본은 여기에 줄 버튼 슬롯(`renderLineActions`)만 더한다. 라벨 색·폭 34·기준선은 [09] L660~680 한 벌 |
| **`TranscriptPanel`** | `props: { items, partial, speakerCount, recordingStartedAt, follow: boolean }` + `ref.scrollToRange(fromMs, toMs)`(겹치는 블록 전부 하이라이트 · 따라가기 끔 · `Esc`/다음 호출로 해제). 화자 색은 **라벨 번호 홀짝** 규칙 한 곳 |
| **`MeetingStatusBar`** | `variant ∈ {connecting, live, paused}` + `pauseReason ∈ {user, mic, stream:upstream, stream:write_failed}` + `elapsedFrom`. WORK-008 이 `generating`·`failed`·`headline` variant 를 **같은 컴포넌트에 추가**한다 — 상단 바는 한 자리([09] L733) |
| **`useMeetingStream`** | 반환 `{ state, pause(), resume(), transcript, partial, latestBatchSeq, onAiBatch }`. 상태 전이는 SPEC-007 §4 stateDiagram 그대로. **`resume()` 만이 WS 를 새로 연다** — 마운트·에러·타이머로 여는 코드가 없다(BE-12). 마이크 트랙 `ended` → `pause({reason:'mic'})` + 서버에 `pause{mic}` 프레임 |
| 캐시 키·무효화 | 줄 추가·안건 상태는 `['meetings','detail',id]` 만. AI 증분은 **WS 프레임으로 캐시에 직접 병합**(재조회 없음). 트랜스크립트는 `['meetings','transcript',id]` — 진입 시 1회 + WS 로 append |
| 낙관적 갱신 | **없다.** 줄 전송·안건 상태 모두 서버 응답 후 반영(SPEC-007 §5) |

## Execution

### Phase 1 — 스키마 보강 · env · 외부 어댑터 뼈대

- **Status**: TODO
- **설명**: 화면도 WS 도 없이 **스키마·설정·어댑터가 서는 상태**를 만든다. Soniox 키가 서버에만 있고 프론트로 절대 내려가지 않는 구조가 여기서 잡힌다.
- **작업**(be):
  - [ ] WORK-006 리비전과 대조해 **없는 컬럼만** 보강 리비전 1건 — `recording_started_at` · `state` CHECK/NULL · `source_agenda_id` · 부분 UNIQUE `active`. `downgrade` 작성
  - [ ] `core/enums.py` — `MeetingAgendaState`(`next`·`active`·`done`) · `BatchRunStatus` · `BatchPhase`
  - [ ] `.env.example` 에 `SONIOX_API_KEY=` · `MEETING_BATCH_CHARS=600` · `MEETING_BATCH_SWITCH_MIN_CHARS=80` · `MEETING_BATCH_MAX_WAIT_SEC=180` · `MEETING_BATCH_TIMEOUT_SEC=120` 자리. **키 값은 쓰지 않는다**
  - [ ] `config.py` — 위 항목. `SONIOX_API_KEY` 는 기본값 없음(없으면 기동 실패 — BE §11)
  - [ ] `integrations/soniox.py` · `storage.py` · `agent.py`(옵션 빌더 한 함수) · `ai_schemas/meeting_batch.json`
  - [ ] 테스트 대역 — `tests/fakes/soniox.py`(토큰 시나리오 재생) · `fakes/agent.py`(정상/스키마 위반/타임아웃) · `fakes/storage.py`(append 실패 주입). **대역은 `integrations/` 경계에서만**(BE §12)
- **검증**:
  - [ ] `make migrate` 왕복(`downgrade -1 → upgrade head`)이 되고, WORK-006 데이터가 남는다
  - [ ] 사람 트랙에 `active` 안건을 둘 넣으면 **DB 부분 UNIQUE 로 거부**된다
  - [ ] `SONIOX_API_KEY` 를 비우고 기동하면 **기동이 실패**한다
  - [ ] **정적 검사**: `SONIOX_API_KEY` 를 읽는 코드가 `integrations/soniox.py` 밖에 **0건**, `schemas/`·`api/` 에 `soniox` 문자열 **0건**(프론트로 새는 길이 없다 — grep 결과를 완료 증거에)
  - [ ] **정적 검사**: codex 옵션 dict 를 만드는 코드가 옵션 빌더 함수 밖에 **0건**
- **완료 증거**: 미작성

### Phase 2 — REST 3표면 · `/start` 확장 · 웜스타트

- **Status**: TODO
- **설명**: `curl` 로 **회의를 시작하고 안건을 넘기고 줄을 적고 트랜스크립트를 읽는** 왕복을 닫는다. 안건 전환이 배치 트리거로 이어지는 훅 자리를 여기서 판다(배치 본체는 Phase 4).
- **작업**(be):
  - [ ] `meeting_service.start()` 확장 — 전이 커밋 → `recording_started_at` → 웜스타트 제출(프로젝트 + 업무 + 사람 안건 · 무소속이면 무소속 업무) → `ai_session_id` 저장. 결과 무시
  - [ ] `add_line` — `status='recording'` 검사 · 사람 트랙 안건 검증 · `kind` 4종 · 1~2000자 · `order_index` 끝 + 1 · `detail/evidence/task_id` 비움
  - [ ] `set_agenda_state` — `active` 유일 · 완료 시 다음 활성 · 커밋 후 `batch_service.evaluate('agenda_switch')`(Phase 4 전까지는 no-op 훅). `PATCH …/agendas/{agendaId}` 는 WORK-006 의 `title` 표면에 **`state` 를 더한 한 표면**, 응답 `MeetingDetail`
  - [ ] `get_transcript` — `at_ms` 순 전량 + `speakerCount` + `recordingStartedAt`
  - [ ] `meeting_router` 에 3표면 · `require_account` · 상태 밖은 `409 invalid_meeting_status`
  - [ ] `tests/test_meeting_live_api.py`
- **검증**:
  - [ ] `/start` 뒤 `meeting.recording_started_at` 이 채워지고 `ai_session_id` 가 대역 세션 id 다. 대역 `agent` 가 **정확히 1회** 새 세션 호출을 받았다
  - [ ] `scheduled` 회의에 `POST lines` → **409 `invalid_meeting_status`**. AI 안건 id 로 줄을 넣으면 **422**
  - [ ] 안건 A `active` → B `active` 로 바꾸면 A 가 `next` 로, 응답이 `MeetingDetail` 전체이고 `agendas.human` 에 `active` 가 **하나**다
  - [ ] `active` 안건을 `done` 으로 바꾸면 **다음 순서 `next` 가 `active`** 가 된다. 마지막이면 `active` 없음
  - [ ] `PATCH {title}` 는 WORK-006 동작 그대로(같은 표면)
  - [ ] 트랜스크립트 응답이 `atMs` 오름차순이고 `speakerLabel` 이 `"1"`·`"2"` 문자열이다
  - [ ] **정적 검사**: `service/` 에서 `fastapi`·`schemas` import **0건**, `repository/` 가 ORM 모델을 반환하는 함수 **0건**
  - [ ] `pytest` 통과
- **완료 증거**: 미작성

### Phase 3 — WS 2단 중계 · 녹음 적재 · 일시정지

- **Status**: TODO
- **설명**: **제품에서 가장 어려운 자리.** 브라우저 WS ↔ 백엔드 ↔ Soniox 가 한 세션으로 묶이고, 녹음이 같은 경로에서 남으며, 끊김이 **가려지지 않고** 드러나는 것을 여기서 닫는다. 화면 없이 `wscat`/테스트 클라이언트로 검증한다.
- **작업**(be):
  - [ ] `meeting_stream_router` — 연결 → 첫 텍스트 프레임 5초 대기 → 토큰 검증 실패 `4401` · 회의 없음/남의 것 `4404` · `status≠recording` 또는 이미 세션 있음 `4409`(reason 문자열에 코드)
  - [ ] `meeting_stream_service` — 레지스트리 · 업스트림 연결(클라이언트 인증 **후에**) · `ready{recordingStartedAt, latestBatchSeq, speakerCount}` · 청크 ①append→②전달 · 잠정 `transcript.partial`(교체) · 확정 블록 경계 → INSERT + `transcript.final` · `pause{user|mic}`/`resume`(업스트림 유지 · 잠정 비움 · `ready` 재송신) · 백프레셔 · `finally` 업스트림 닫기
  - [ ] 실패 경로 — `storage.append` 예외 → `error{meeting_stream_disconnected, write_failed}` + close · 업스트림 끊김 → `error{…, upstream}` + close. **재연결 코드 없음**
  - [ ] `push_ai_batch(meeting_id, seq, agendas, lines)` 훅(Phase 4 가 부른다)
  - [ ] `tests/test_meeting_stream.py`(대역 Soniox 로 토큰 시나리오 재생)
- **검증**:
  - [ ] 첫 프레임 없이 5초 → **`4401`**. 만료 토큰 → `4401`. 남의 회의 → `4404`. `scheduled` 회의 → `4409`
  - [ ] 두 번째 클라이언트가 같은 회의에 붙으면 **`4409`** 이고 첫 세션은 영향 없다
  - [ ] 대역 Soniox 가 `is_final:false` 토큰을 3번 보내면 클라이언트는 `transcript.partial` 3개(내용 교체)를 받고 **DB 행은 0**이다
  - [ ] 확정 토큰이 화자 변경/300자/2초 공백에서 블록으로 닫히고 **`meeting_transcript` 행 수 = `transcript.final` 프레임 수**다
  - [ ] 오디오 청크 3개를 보내면 `STORAGE_ROOT/recordings/{id}` 파일 크기가 **정확히 그 합**이고 `recording_path` 가 채워진다
  - [ ] 대역 storage 가 append 에서 예외를 던지면 **그 청크에서 `error{write_failed}` 후 close** 되고, 이후 청크가 Soniox 로 가지 않는다
  - [ ] `pause` 뒤 보낸 오디오는 Soniox 대역에 **도달하지 않고**, `resume` 뒤 `ready` 가 다시 온다. 그 사이 업스트림 연결이 **닫히지 않았다**
  - [ ] 대역 Soniox 가 연결을 끊으면 `error{upstream}` 후 close 되고 **서버가 다시 붙지 않는다**(대역 연결 횟수 = 1)
  - [ ] 클라이언트가 끊기면 `finally` 로 업스트림이 닫힌다(대역 close 호출 1회)
  - [ ] **정적 검사**: `meeting_stream_service` 에 `retry`·`reconnect`·`while True` 재접속 루프 **0건**, `except Exception` **0건**
  - [ ] `pytest` 통과
- **완료 증거**: 미작성

### Phase 4 — 배치 파이프라인 · 검증 4단 · 즉시 push

- **Status**: TODO
- **설명**: 트랜스크립트가 쌓이면 **AI 트랙이 저절로 자라는** 상태. 실패 3종(배치 실패 · 스키마 위반 · 없는 업무)이 **정확히 정책대로만** 처리되고 그 밖은 터지는 것을 테스트로 못박는다 — BE §12 필수 테스트 6·7 이 여기다.
- **작업**(be):
  - [ ] `meeting_batch_service.evaluate` — 3트리거(600자 · 안건 전환 80자 · 180초 타이머) · 회의당 락 · 실행 중이면 무시
  - [ ] `run` — 커서 조회 → 입력 조립(구간 + 사람 안건·줄 + AI 안건 + 화이트리스트) → `resume` 제출(120초) → 검증 4단 → 적재(AI 안건 미러/신설 · 줄 INSERT · `batch_run` `succeeded`+`seq`) → 커밋 → `push_ai_batch`
  - [ ] 실패 처리 — 워커 오류/타임아웃 `failed` · 스키마 위반 `discarded`(행 0) · 화이트리스트 밖 `taskId` 는 **그 줄만** `action` 강등. 커서는 성공분만 전진
  - [ ] 타이머 — 미처리 구간이 생긴 뒤 180초에 `evaluate('timer')`. 비어 있으면 없음
  - [ ] `tests/test_meeting_batch.py`
- **검증**:
  - [ ] 확정 발화 600자에서 배치가 **정확히 1회** 나가고, 대역 `agent` 호출의 `resume.session_id` 가 `ai_session_id` 와 같다
  - [ ] 안건 전환 시 미처리 79자 → 배치 없음, 80자 → 즉시 배치
  - [ ] 미처리 100자 상태로 180초 → 배치. 미처리 0 이면 타이머 배치 없음
  - [ ] 배치 실행 중 600자 트리거가 또 와도 **동시 실행 0**, 끝난 뒤 다음 트리거에서 두 구간이 **한 배치**로 나간다
  - [ ] **BE §12 테스트 6** — 잘못된 JSON 결과가 오면 `meeting_line`·`meeting_agenda(track='ai')` 행이 **하나도 안 들어가고** `batch_run.status='discarded'`, 다음 배치 입력에 **그 구간이 포함**된다
  - [ ] **BE §12 테스트 7** — 화이트리스트 밖 `taskId` 줄이 `kind='action'`·`task_id=NULL` 로 들어가고 **본문·상세·근거가 남는다.** 같은 배치의 다른 줄은 정상
  - [ ] 워커 타임아웃(120초) → `failed`, 사용자 표시 없음, 다음 배치에 합쳐진다
  - [ ] `humanAgendaId` 참조 → `source_agenda_id` 가 그 id 인 AI 안건이 **한 번만** 만들어지고 두 번째 배치는 재사용한다. `newTitle` → `source_agenda_id=NULL`
  - [ ] 성공 배치 뒤 WS 클라이언트가 `ai.batch{seq}` 를 **커밋 직후** 받는다(대역 시계로 버퍼 지연 0). 세션이 없으면 예외 없이 건너뛴다
  - [ ] 대역 워커가 프로토콜 오류(정의 밖 예외)를 내면 **500 으로 전파**되고 `batch_run` 에 `failed` 가 남지 않는다(설계한 실패만 잡는다)
  - [ ] **정적 검사**: `meeting_batch_service` 에 `except Exception` **0건**, 부분 파싱(`try` 안에서 줄 단위 INSERT) **0건**
  - [ ] `pytest` 통과
- **완료 증거**: 미작성

### Phase 5 — 프론트 공용 부품 · 스트림 훅

- **Status**: TODO
- **설명**: **화면보다 먼저** 만든다. `AgendaLineTree` 는 회의록 탭·AI 탭·WORK-008 통합본 탭 셋이 쓰고, `MeetingStatusBar` 는 회의 생애 전체의 상단 바 한 자리다 — 화면부터 만들면 다음 work 가 복제한다.
- **작업**(fe):
  - [ ] `lib/api/ws.ts` — 열기 · 첫 프레임 토큰 · `4401` 시 refresh 1회 → 재연결 1회 → 또 `4401` 이면 로그인
  - [ ] `useMeetingStream` — 상태 기계 5상태 · `getUserMedia`(내 마이크만 · 트랙 `ended` → paused/mic) · 청크 송신(64KB/250ms 이하) · 프레임 분배(잠정 교체 · 확정 append · `ai.batch` 캐시 병합 · `error`/close → paused/stream). **`resume()` 외에 WS 를 여는 코드 없음**
  - [ ] `AgendaLineTree` + `AgendaHeader` + `LineRow` + `EvidenceChip` — props 계약(§Internal Interface Contract). 배지 「논의 중」/「완료」/「대기」/「AI 안건」(종료 후 「다음 논의로」는 WORK-008 이 같은 prop 으로 바꾼다) · 4종 라벨 색 · 펼침 화살표(hover) · 상세 + 칩
  - [ ] `TranscriptPanel` — 블록 · 잠정(회색 + 캐럿) · 따라가기 · `scrollToRange` + 하이라이트 `#F4F5FF` + `Esc` 해제 · 홀짝 화자 색 · 빈 상태 · 푸터 문구 2종
  - [ ] `MeetingStatusBar` — 5상태 문구·색(회색 바 = 시안 L586~592 · 기록 중 = L809~831) · 경과 시간 `now − recordingStartedAt`
  - [ ] `PromptBar` + `LineKindPopover` — `/` 팝오버(논의·결정·**업무**·액션 · 새 안건 · 이동) · 활성 칩 · 「안건 선택」 비활성 · 전송 잠금 · 실패 시 입력 유지
  - [ ] `lib/datetime.ts` — `msToWallClock`
- **검증**:
  - [ ] 스토리/임시 화면에서 같은 `AgendaLineTree` 에 `track='human'`·`'ai'` 데이터를 넣어 **분기 없이** 두 탭 모양이 나온다(컴포넌트 안에 `track ===` 비교 **0건** — grep)
  - [ ] AI 줄 hover 에서만 화살표가 보이고, 펼치면 상세 + 「HH:MM – HH:MM」 칩이 `recordingStartedAt` 기준 벽시계로 찍힌다
  - [ ] `scrollToRange(241000, 247300)` 로 겹치는 블록이 전부 하이라이트되고 `Esc` 로 풀린다
  - [ ] 대역 WS 서버로 `error{upstream}` 을 보내면 훅 상태가 `paused/stream` 이 되고 **네트워크 탭에 재연결 시도가 0건**이다. `resume()` 을 부를 때만 새 연결이 생긴다
  - [ ] 마이크 트랙을 `stop()` 하면 `paused/mic` 로 떨어지고 서버에 `pause{mic}` 프레임이 간다
  - [ ] **정적 검사**: `WebSocket(` 생성이 `lib/api/ws.ts` 밖에 **0건** · `setInterval`/`setTimeout` 으로 재연결하는 코드 **0건** · 인라인 hex 색 **0건** · 컴포넌트 안 `new Date()` 포맷 **0건**
- **완료 증거**: 미작성

### Phase 6 — 회의 중 화면 조립 · 실패 경로 · 첨부 · 반응형 (앱 창 E2E)

- **Status**: TODO
- **설명**: 이 work 의 완성 지점 — **Tauri 앱 창에서 실제 마이크로 회의를 기록한다.** 마이크를 뽑고, 백엔드를 내리고, 워커를 멈추는 세 가지 실패를 사람이 직접 일으켜 **일시정지 경로 하나로 모이는지** 본다.
- **작업**(fe):
  - [ ] `meetings/detail/page.tsx` 의 `recording` 분기 → `MeetingLiveView`
  - [ ] 헤더 — 제목 · 부제(날짜 · 유형명, **장소 없음**) · 「일시정지」/「재개」 토글 · 「회의 종료」 자리(`connecting` 빼고 항상 활성 — 일시정지 3종에서도. 동작은 WORK-008)
  - [ ] 좌 패널 — 탭 dot 규칙([09] L704~723) · 회의록 탭(`AgendaLineTree` + 안내 바 「입력창에서 / 를 입력해 안건 · 논의 · 결정 · 업무 · 액션을 고릅니다」 + 「자동 저장 · HH:MM」) · AI 요약 탭(`AgendaLineTree expandable` + 「첫 배치를 기다리는 중」/「배치 n회 반영 · HH:MM」 + 미확인 점 + 푸터 문구)
  - [ ] 우 패널 — `TranscriptPanel` · 첨부 탭(WORK-006 목록·추가 팝오버 재사용 · PNG/PDF·「회의 중 작성」 없음) · **첨부 열기 드로어**(미리보기 / 원문 텍스트 · 문서함 이동 없음) · 로컬 업로드 영역 **v2 게이트**(SPEC-001 U-2 · 요청 0)
  - [ ] 근거 칩 → 우 패널 스크립트 탭 전환 + `scrollToRange`
  - [ ] 새로고침·재실행 시 `paused/stream` 으로 시작 + 트랜스크립트·트리·`latestBatchSeq` 복원
  - [ ] 반응형 — ≥1440 좌 `1fr` + 우 464→400 · 1280~1439 좌 유동 + 우 400 고정 + 드로어 전체화면 · <1280 안내 화면(스트림 유지)
- **검증**(SPEC-007 §6 순서):
  - [ ] 「회의 시작」 뒤 상태 바 「연결 중」 → 「기록 중 00:00:0n」, **파형·「자동 저장」이 상태 바에 없다**
  - [ ] 말하면 회색 잠정 발화 → 「화자 1 · HH:MM」 블록, 「화자 1명」
  - [ ] 두 사람 → 「화자 2」 다른 색 · 「화자 2명」 · **이름 입력 자리 없음**
  - [ ] 그냥 치고 `Enter` → 활성 안건 아래 논의 줄 + 「자동 저장 · HH:MM」
  - [ ] `/` 팝오버 **4종**, 「업무」 줄은 라벨 `#5F6470` · 배지·버튼 없음
  - [ ] 「새 안건」이 바로 「논의 중」, 이전 안건 「대기」
  - [ ] 안건 체크 → 「완료」 + 취소선, 다음 「대기」 안건이 「논의 중」, 칩 변경
  - [ ] 회의 중 사람 줄 클릭해도 편집되지 않는다
  - [ ] 600자 넘으면 AI 탭 파란 점 → 「배치 1회 반영 · HH:MM」 + **트리(카드 아님)**
  - [ ] 회의록 탭에 AI 안건·줄 없음
  - [ ] 두 번째 배치 「배치 2회 반영」, 기존 AI 줄 그대로
  - [ ] AI 줄 펼침 → 칩 → 스크립트 탭 전환 + `#F4F5FF` 강조 → `Esc` 해제
  - [ ] 웜스타트 밖 업무 참조 줄이 **액션 줄**로 보이고 본문 남음(서버 로그 확인)
  - [ ] 워커를 멈추면 **표시 없음**, 살리면 다음 배치가 합쳐 온다
  - [ ] 「일시정지」 → 회색 바 · 「재개」 · 잠정 사라짐 · 줄 입력 가능 · 「재개」 후 화자 번호 이어짐
  - [ ] 마이크를 뽑으면 **스스로** 「일시정지 · 마이크 연결이 끊겼습니다」, 꽂고 「재개」
  - [ ] 백엔드를 내리면 「일시정지 · 서버 연결이 끊겼습니다」 · 「회의 종료」 여전히 활성 · **자동 재연결 없음**(네트워크 탭 0건) · 올리고 「재개」
  - [ ] 새로고침 → 복원 + 「서버 연결이 끊겼습니다」로 시작, 잠정 없음
  - [ ] 다른 창 → 「다른 창에서 기록 중입니다」, 오디오 안 보냄
  - [ ] 첨부 행 → 드로어(미리보기 / 원문 텍스트), 이동 없음, 스크립트 계속 쌓임
  - [ ] 드롭 영역에 파일 → 「v2에서 제공됩니다」 토스트만, 요청 0
  - [ ] 부제에 장소 없음
  - [ ] 상단 바에 **AI 한 줄 요약이 보이지 않는다**(종료 후 같은 자리 — WORK-008 에서 확인)
  - [ ] 사람 줄·안건 헤더에 **삭제·제목 수정 어포던스 없음**
  - [ ] 안건 3상태(완료 · 논의 중 · 대기)가 새로고침 후 그대로
  - [ ] 1280~1439 좌 유동 + 우 400, 드로어 전체화면
  - [ ] **macOS Tauri 창에서 `getUserMedia` 권한 프롬프트 → 허용 → 캡처**가 실물로 된다(§C-7). Windows 는 별도 확인 시점 기록
- **완료 증거**: 미작성

## Pre-deploy Check

- [ ] `.env` 에 `SONIOX_API_KEY` 가 있고 **서버 컨테이너에만** 주입된다. 프론트 번들·응답·로그에 키 문자열이 **0건**(grep)
- [ ] `.env.example` 에 `SONIOX_API_KEY=` 와 `MEETING_BATCH_*` 5항목 자리가 있다(값 없음)
- [ ] 리버스 프록시(NPM)가 `/api/meetings/*/stream` 의 **WS upgrade** 를 통과시키고 idle timeout 이 회의 길이(≤300분)보다 길다
- [ ] `STORAGE_ROOT` 가 named volume 이고 녹음 파일이 컨테이너 재시작을 넘겨 남는다. 용량 경보 기준을 적어 둔다(영구 보관 — M-13)
- [ ] back 의 `open-kknaks` 핀과 worker 이미지 핀이 **같은 값**이다(SYS §codex 바인드 마운트)
- [ ] `CORS_ORIGINS` 에 Tauri 웹뷰 origin 이 명시돼 있고 WS 인증이 첫 프레임 방식으로 통한다
- [ ] 응답·WS 프레임에 `recording_path`·`ai_session_id`·스택 트레이스가 실리지 않는다

## Rollback

- **스키마**: `alembic downgrade -1` 로 보강 리비전만 되돌린다. WORK-006 의 회의 도메인·데이터는 남는다(컬럼 추가만이라 자식이 없다). 부분 UNIQUE 제거는 데이터 손실 없음
- **백엔드**: `meeting_stream_router` 미등록 + `meeting_router` 의 3표면 제거로 걷어낼 수 있다. `/start` 확장분은 **함께** 되돌린다(웜스타트만 남으면 세션이 고아가 된다). `integrations/` 는 다른 소비자가 없어 그대로 두어도 무해하다 — **단 WORK-008 이 시작된 뒤에는 되돌리지 않는다**(최종 배치·통합이 `agent.py`·`meeting_batch_service` 를 부른다)
- **프론트**: 브랜치 폐기. `detail/page.tsx` 의 `recording` 분기를 빼면 WORK-006 의 `scheduled` 화면으로 돌아간다. **`AgendaLineTree`·`MeetingStatusBar` 는 단독으로 되돌리지 않는다**(WORK-008 이 쓴다)
- 부분 revert 시: Phase 5·6 만 되돌리면 API·WS 는 살아 있고 화면만 없어진다. Phase 4 만 되돌리면 트랜스크립트는 쌓이고 AI 탭이 비어 있는 상태가 된다 — 사용자에게 「첫 배치를 기다리는 중」이 영원히 보이므로 **Phase 4 단독 revert 는 하지 않는다**

## Done Criteria

- [ ] 모든 Phase 가 `DONE` 또는 `SUPERSEDED` 다.
- [ ] **SPEC-007 §6 Acceptance 26개 항목이 앱 창(Tauri)에서 확인**됐다 — Phase 6 검증 목록이 그 순서다. 「AI 한 줄 요약이 종료 후 같은 자리에 뜬다」의 **후반부**(종료 후 확인)는 WORK-008 완료 때 다시 본다
- [ ] BE §12 필수 테스트 **6(스키마 위반 폐기) · 7(화이트리스트 강등)** 이 통과한다.
- [ ] 정적 검사 7종(키 격리 · 옵션 빌더 단일 · 계층 위반 · 재연결 루프 0 · `except Exception` 0 · `WebSocket(` 격리 · 트리 컴포넌트 트랙 분기 0) 결과가 완료 증거에 붙어 있다.
- [ ] `.env.example` 에 `SONIOX_API_KEY` 자리가 있고 **값이 어디에도 커밋되지 않았다**(git log grep).
- [ ] macOS Tauri 창에서 마이크 캡처가 실물로 확인됐고 Windows 확인 시점이 기록됐다.
- [ ] product `log.md` 와 `30-work/README.md` 가 갱신됐다.

## Open Issues

- **WORK-006 과 리비전 경계** — 같은 날 동시에 쓰인 두 WP 가 `meeting_agenda.state`·`source_agenda_id`·`recording_started_at` 을 둘 다 언급한다. **먼저 머지되는 리비전이 만들고 나중 것은 대조 후 생략**한다(Phase 1 첫 작업). 두 리비전에 같은 컬럼이 들어가면 `upgrade` 가 깨진다
- **`backend/README.md` §8-2 표** 가 2026-09-06 개정에서 `invalid_meeting_status`·`meeting_not_recording`(각주 「SPEC 이 통합 판정 중」)·`meeting_stream_active` 세 행을 실었다. **SPEC-007 은 `meeting_not_recording` 을 폐기하고 `invalid_meeting_status` 로 합쳤다**(SPEC-007 §7-A) — 표의 `meeting_not_recording` 행은 코디가 지운다. 구현은 SPEC-007 §4 Case Matrix(`invalid_meeting_status` 409 · WS `4409`)를 따른다
- **오디오 포맷**(§C-8) — Soniox 지원 형식 중 Tauri 웹뷰 `MediaRecorder`/`AudioWorklet` 이 내는 것으로 Phase 3 착수 때 고른다. 결정값은 `auth.audio` 선언 + `integrations/soniox.py` config 두 곳에만 둔다. 이 문서에 미리 적지 않는다
- **일시정지 중 Soniox 유휴 연결 유지 시간**은 조사 문서에 없다(SPEC-007 §7-E 후보 표). Phase 3 에서 실측해 완료 증거에 남긴다 — 끊기면 `upstream` 실패 경로로 흐르므로 코드 변경은 없다
- **배치 수치 5종은 실측 전 값**이다(DEC-003 §STT 「조정 가능 — 계약은 불변」). env 로 빼 두었고 Phase 6 E2E 뒤 조정값을 완료 증거에 적는다. 값이 바뀌어도 SPEC 계약(트리거 3종·단일 실행)은 그대로다
- **첨부 열기 드로어의 소유** — SPEC-007 U-7 과 SPEC-006 U-7 이 같은 드로어(시안 L1349~1393)를 가리킨다. WORK-006 이 먼저 만들면 이 work 는 재사용하고, 아니면 이 work 가 만들고 WORK-006 시작 전 화면이 가져다 쓴다. 두 벌을 만들지 않는다

## Related

- SPEC: SPEC-007 (frontmatter `links.specs`) · 물려받는 것 SPEC-006 §4 `MeetingDetail`·안건·첨부 · SPEC-005 §4 문서 본문 · SPEC-001 U-2 v2 게이트
- Work: WORK-006 (선행) · WORK-008 (후속) · WORK-004 (`task_service`·`DrawerFrame`·`AttachmentPopover`) · WORK-001 (compose · `integrations/` 뼈대)

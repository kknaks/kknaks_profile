---
type: work
id: WORK-007
title: "회의록 회의 중 — WS 2단 중계 · 실시간 스크립트 · 사람 트랙 · AI 배치 파이프라인"
status: todo
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
progress: 0
created_at: 2026-09-06
updated_at: 2026-09-06
tags:
  - product/task-management
  - doc/work
  - status/todo
links:
  baselines: [BASE-003]
  decisions: [DEC-003]
  specs: [SPEC-007]
  works: [WORK-006]
  releases: []
  related: [DEC-001, DEC-002, DEC-004]
---

# 회의록 회의 중 — WS 2단 중계 · 실시간 스크립트 · 사람 트랙 · AI 배치 파이프라인

**말하면 스크립트가 쌓이고 AI 탭이 채워진다.** 오디오는 반드시 백엔드를 지나며 그 길에서 녹음 원본이 적재된다. AI 는 자기 트랙에만 쓰고 사람 회의록에 끼어들지 않는다. 종료·통합은 만들지 않는다 — WORK-008 이다.

> 1 파일 = 1 work = **빌드 계획**. dev가 이 문서만 보고 PR 분리 / 일정 / 작업 시작이 가능해야 한다.
> SPEC의 외부 계약 본문은 복제하지 않고 frontmatter `links.specs`와 index에서 연결한다.

## Meta

- Baseline: BASE-003
- Covers spec: **SPEC-007**(회의록 — 회의 중 · STT 중계 · 2트랙 · AI 배치)
- Depends on work: **WORK-006**(회의 도메인 6 테이블 · `recording` 상태와 `recordingStartedAt` · **`ai_session_id` 웜스타트** · `integrations/agent.py` 옵션 빌더 · 업무 화이트리스트 함수 · 우측 사이드 탭 껍데기 · **회의록 영역 반응형 정본**)
- Parallel work: 없음
- Follow-up work: **WORK-008**(종료 → 최종 배치 → 통합본. 이 work 의 배치 파이프라인과 세션을 그대로 이어 쓴다)
- **External dependency**
  - **코드 레포는 별도다** — `github.com/kknaks/task_management`
  - **Soniox 가 이 work 에서 처음 붙는다** — `SONIOX_API_KEY`(long-lived, **서버에만**) · `wss://stt-rt.soniox.com/transcribe-websocket` · 모델 `stt-rt-v5`. 스트림 한도 **300분**, 동시 접속 10, 요청 100/min
  - **파일 저장소** — `STORAGE_ROOT` 볼륨(녹음 원본 영구 보관). WORK-006 이 env 자리만 만들었다
  - 마이크가 달린 개발기와 **Tauri 앱 창의 마이크 권한**(macOS 시스템 설정)

## Work Summary

| Field | Value |
|---|---|
| Type | new-feature |
| Owner |  |
| Status | todo |
| Progress | 0% |
| Branch/PR |  |
| Blocker | WORK-006 미완 · `SONIOX_API_KEY` 미발급 |
| Next | Phase 1 — WS 2단 중계 · 녹음 적재 · 트랜스크립트 |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM |  | 범위 확정 · SPEC-007 §6 Acceptance 18개 대조 | todo |
| Design |  | 스크립트 패널 · 프롬프트 `/` 팝오버 · **AI 요약 탭 트리**(안건>줄·AI 안건 칩·근거 칩·배치 회차) · 끊김 배너 | todo |
| FE |  | 마이크 캡처 · `useMeetingStream` · 스크립트 렌더(잠정/확정) · 프롬프트 · AI 탭 · 첨부 탭 | todo |
| BE |  | WS 2단 중계 · 녹음 적재 · 확정 토큰 적재 · 줄·안건 표면 · **배치 파이프라인과 결과 검증** | todo |
| QA |  | Phase 검증(앱 창 E2E) · **실패 4종 재현** · 2트랙 격리 확인 | todo |
| Ops |  | `SONIOX_API_KEY` 관리 · `STORAGE_ROOT` 볼륨 · 스트림 한도·과금 확인 | todo |

## Scope

포함:

- **WS 2단 중계** — `WS /api/meetings/{id}/stream` 하나. 첫 프레임 토큰 인증 · 오디오 업 · 토큰 다운 · AI 증분 다운
- **녹음 원본 적재** — `① 파일 append → ② Soniox 중계` 순서. 적재 실패 시 **스트림을 끊는다**
- **확정 토큰만 DB 적재** · 잠정 토큰은 화면으로만 · 백프레셔(**잠정만 버린다**)
- **자동 재연결 없음** — 끊기면 배너 + 「다시 시작」
- 마이크 캡처(`getUserMedia`) · 권한/장치 실패 처리
- 실시간 스크립트 패널 — 잠정 갈아 끼움 / 확정 append / 화자 블록 분리 / 자동 스크롤 정지 + 「최신으로」
- 사람 트랙 프롬프트 — `/` 로 줄 종류 4종 · 「다음 주제로」 · 안건 이동
- **AI 배치 파이프라인** — 트리거 4종(발화량 600자 · 안건 전환 flush · 180초 상한 · 동시 실행 금지) · `resume` 세션 · `output_schema` 강제 · **결과 재검증**
- **AI 요약 탭 렌더** — 안건 > 줄 트리 · 「AI 안건」 칩 · 근거 칩 · **배치 회차 표시**
- 첨부 탭 · 파일 드로어(자료함 md — **스텁**)
- 새로고침 복구(`GET /transcript`) · 상태 바 경과 시간(서버 기준)
- **실패 4종** — 배치 실패 · 스키마 위반 · 없는 업무 참조 · 연결 끊김

제외:

- 회의록 생성·시작 전·목록·삭제·반응형 → **WORK-006**(반응형은 SPEC-006 U-6 이 정본)
- **종료·통합·편집·업무 생성/갱신** → **WORK-008**. 회의 중에는 **업무 버튼이 뜨지 않는다**
- 시스템 오디오 캡처 · 화자 이름 지정 · 2-pass 재전사 — v1 밖
- **300분 초과 회의** — 재연결·세션 경계 처리를 넣지 않는다(M-18)
- **「일시정지」 버튼** — 뺐다(SPEC-007 S007-OQ-1)
- 회의 중 md 작성 — v2
- 첨부의 자료함 md 실동작 → 문서함 work

## Code Surface

- Repo / module: `github.com/kknaks/task_management` — `app/back`(BE) · `app/front`(FE) · 루트 compose
- 만질 파일 후보

| 경로 후보 | 설명 |
|---|---|
| `app/back/config.py` · `.env.example` | `SONIOX_API_KEY`(**기본값 없음**) · `STORAGE_ROOT` |
| `docker-compose.local.yml` | 녹음 저장 볼륨(`STORAGE_ROOT`) |
| `app/back/integrations/soniox.py` | Soniox WS 클라이언트 — config 프레임(`stt-rt-v5` · `language_hints:["ko"]` · `enable_speaker_diarization:true` · **endpoint detection 미사용**) · 종료 프레임 |
| `app/back/integrations/storage.py` | 녹음 파일 경로·append. **동기 I/O 는 `anyio.to_thread` 로 밀어낸다**(BE §5) |
| `app/back/api/meeting_stream_router.py` | `WS /api/meetings/{id}/stream` — 첫 프레임 인증 · 상태 가드 · 동시 접속 1 |
| `app/back/service/meeting_stream_service.py` | **2단 중계 · 녹음 append · 확정 토큰 적재 · 백프레셔 · `finally` 로 업스트림 닫기** |
| `app/back/service/meeting_batch_service.py` | **트리거 판정 · `resume` 제출 · 결과 검증 · `track='ai'` INSERT · `ai.increment` push** |
| `app/back/ai_schemas/meeting_batch.json` | codex `output_schema` — 안건·줄 배열 |
| `app/back/repository/meeting_child_repository.py` | 트랜스크립트 적재·조회 · AI 안건·줄 INSERT · 배치 이력 |
| `app/back/api/meeting_router.py` | `POST /{id}/lines` · `PATCH /{id}/agendas/{agendaId}`(상태) · `GET /{id}/transcript` 추가 |
| `app/back/tests/test_meeting_stream.py` · `test_meeting_batch.py` | 대역 Soniox·codex 로(BE §12) 실패 4종 |
| `app/front/src/features/meetings/hooks/useMeetingStream.ts` | **WS 를 소유하는 유일한 훅.** 컴포넌트가 `WebSocket` 을 만들지 않는다 |
| `app/front/src/features/meetings/hooks/useMicCapture.ts` | `getUserMedia` + 인코딩. **포맷을 고르는 함수 하나로 격리**(§C-8) |
| `app/front/src/features/meetings/components/MeetingLiveScreen.tsx` | 회의 중 화면(상태 바 + 좌 탭 + 우 탭) |
| `app/front/src/features/meetings/components/StatusBar.tsx` · `DisconnectedBanner.tsx` | 「기록 중 00:12:38」·자동 저장 시각 / 끊김 배너 + 「다시 시작」 |
| `app/front/src/features/meetings/components/TranscriptPanel.tsx` · `SpeakerBlock.tsx` | 확정 append · 잠정 갈아 끼움 · 「최신으로」 |
| `app/front/src/features/meetings/components/LinePromptBar.tsx` · `LineKindPopover.tsx` | `/` 팝오버 4종 + 「다음 주제로」·「안건 이동 ▸」 |
| `app/front/src/features/meetings/components/AgendaLineTree.tsx` | **회의록 탭·AI 탭 공용 트리**(§Internal Interface Contract) |
| `app/front/src/features/meetings/components/AiSummaryTab.tsx` · `EvidenceChip.tsx` · `BatchSeqLabel.tsx` | AI 안건 칩 · 근거 펼침 · 「배치 n회 반영」 |
| `app/front/src/features/meetings/components/AttachmentTab.tsx` · `FileDrawer.tsx` | 첨부 목록 · 드로어 840(미리보기/원문) |
| `app/front/src/features/meetings/components/MicPermissionNotice.tsx` | 권한 거부·장치 없음 안내 + 「다시 시도」 |

- Domain / schema note: **마이그레이션 없음.** WORK-006 이 만든 `meeting_transcript`·`meeting_batch_run`·`meeting_agenda`·`meeting_line` 을 이 work 가 처음 쓴다

## Domain / Schema

| Entity | 역할 |
|---|---|
| `meeting_transcript` | **확정 토큰만.** `speaker_label`(익명) · `at_ms`·`end_ms`(**회의 시작 기준 오프셋**) · `content` |
| `meeting_agenda` | 이 work 가 **`track='ai'` 안건을 처음 만든다** |
| `meeting_line` | 사람 줄(`human`) — 프롬프트가 만든다 / AI 줄(`ai`) — 배치가 만든다 |
| `meeting_batch_run` | 배치 이력 — `seq` · 구간 커서(`from/to_transcript_id`) · `phase='incremental'` · `status` |
| `meeting.recording_path` | 이 work 가 처음 채운다. **영구 보관** |

- 상태 / invariant: `domains/meeting.md` **M-5**(줄은 항상 안건에 속하고 **트랙이 같다**) · **M-5-a**(AI 안건은 AI 탭에만) · **M-6**(회의 중 AI 는 `ai` 트랙에만 INSERT) · **M-6-a**(증분 즉시 반영 + 회차는 **성공분 최대 `seq` 에서 파생**) · **M-7**(증분 추가만, 기존 AI 줄 UPDATE 금지) · **M-9**(확정 토큰만 적재) · **M-10**(익명 화자) · **M-11**(오프셋 기준) · **M-12**(회의당 세션 하나) · **M-13**(녹음 영구) · **M-15·M-15-a**(화이트리스트 강등) · **M-16**(스키마 위반 전량 폐기) · **M-18**(300분 초과 미지원) · `system/README.md` §흐름 ③ **불변식 1~10**
- Migration 필요 여부: **없음**
- SPEC 에 환류해야 하는 변경: **`GET /api/meetings/{id}/transcript` 가 아키텍처 §10 표면 목록에 없다**(SPEC-007 S007-OQ-5) — 구현은 SPEC-007 §4 를 따르고 표 갱신은 코디 소관

## Dependency

| Consumer | Interface | 설명 |
|---|---|---|
| **WORK-008** | `meeting_batch_service` 의 제출·검증 경로 · `meeting_batch_run`(`phase` 축) · `AgendaLineTree` · `EvidenceChip` · 스크립트 스크롤·강조 훅 | 종료 시 **최종 배치**가 같은 세션·같은 검증을 쓰고, 통합본 화면이 같은 트리를 그린다 |
| WORK-008 | 스트림 닫기 훅 | 종료 파이프라인의 첫 단계가 **이 work 의 `finally` 경로**를 부른다 |

## Internal Interface Contract

외부 계약(WS 프레임·엔드포인트·검증·에러)은 **SPEC-007 §4** 가 정본이다. 후속 work 가 의존하는 내부 접점만 고정한다.

| 접점 | 계약 |
|---|---|
| **오디오 경로 순서** | **① 녹음 파일 append → ② Soniox 중계.** 순서를 바꾸지 않는다. **적재가 실패하면 그 자리에서 스트림을 끊는다** — 원본이 남지 않는 녹음을 계속하지 않는다(BE §5-1) |
| 업스트림 수명 | **클라이언트 연결이 성립한 뒤에 연다**(스트림 시간이 과금·300분 한도에 직결된다). 종료·끊김 어느 쪽이든 **`finally` 에서 반드시 닫는다** |
| 백프레셔 | 클라이언트 큐가 상한을 넘으면 **잠정 토큰만 버린다.** 확정 토큰과 AI 증분은 버리지 않는다 |
| 동시 접속 | 회의 하나에 **스트림 하나**. 두 번째 접속은 **뒤에 온 쪽을 거부**한다 — 먼저 붙은 녹음을 끊지 않는다 |
| 시각 기준 | `at_ms`·`end_ms`·`evidence` 는 전부 **회의 시작 기준 오프셋(ms)** 이다(M-11). **벽시계와 섞지 않는다.** 화면의 경과 시간은 서버가 준 `recordingStartedAt` 으로 그린다 — 클라이언트 타이머만으로 세지 않는다 |
| 회의 중 줄 표면 | `POST /{id}/lines` 는 **요청에 `track` 을 담지 않고** 서비스가 `human` 을 박는다(M-6). `agendaId` 는 **그 회의의 사람 트랙 안건**이어야 한다 |
| **배치 트리거** | 확정 발화 **600자** · 안건 전환 시 **즉시 flush**(미처리 **80자 미만이면 생략**) · 마지막 배치로부터 **180초** · **동시 실행 금지**(실행 중 트리거는 다음 구간으로) · **배치 타임아웃 120초**. 값은 실측 후 조정되지만 **계약(트리거 4종·동시 금지·구간 이월)은 바뀌지 않는다** |
| 배치 세션 | **WORK-006 의 `ai_session_id` 를 `resume` 한다.** 배치마다 새 세션을 만들지 않는다(M-12). `ai_session_id` 가 비어 있으면(웜스타트 실패) **첫 배치가 세션을 만들고 저장**한다 |
| **결과 검증은 두 겹이다** | `output_schema` 로 강제하고 **받은 JSON 을 우리가 다시 검증**한다(BE §5-2). ① 스키마 위반 → **행 0건, 전량 폐기**(`status='discarded'`) ② 화이트리스트 밖 `taskId` → **`taskId` 를 떼고 `kind='action'` 으로 강등하되 본문은 살린다**. **부분 파싱 금지** |
| 화이트리스트 | **WORK-006 의 산출 함수를 그대로** 쓴다 — 회의의 프로젝트 업무, 무소속이면 무소속 업무. 회의 중 생성된 업무는 **다음 배치 컨텍스트에 반영**된다 |
| AI 증분 push | 배치가 끝나는 **즉시** 같은 WS 로 `ai.increment` 를 보낸다. **버퍼링하지 않고 `seq` 를 함께 싣는다.** `seq` 는 컬럼이 아니라 **`meeting_batch_run` 성공분 최대값에서 파생**한다(M-6-a · G-7) |
| **2트랙 격리** | 회의록 탭 쿼리는 **`human` 만**, AI 탭 쿼리는 **`ai` 만** 읽는다. 회의 중 AI 는 사람 줄·사람 안건을 **읽어 고치지 않고 제안도 하지 않는다.** 기존 AI 줄을 **UPDATE 하지 않는다**(M-6·M-7) |
| `AgendaLineTree` | **회의록 탭과 AI 탭이 같은 컴포넌트**를 쓴다 — 두 탭이 다른 문법이면 종료 후 통합본과 대조가 안 된다(SPEC-007 U-4). 차이는 **props 로만** 준다(AI 안건 칩 · 근거 펼침 · 편집 가능 여부). WORK-008 의 통합본 탭도 같은 컴포넌트다 |
| 자동 재연결 없음 | 끊기면 **배너 + 「다시 시작」**. 「재연결 중…」 문구를 쓰지 않는다. 끊긴 동안에도 **좌측 줄 입력은 살아 있다**(FE §8 · BE-12) |
| 업무 버튼 없음 | **회의 중에는 「업무 생성」·「업무 갱신」 버튼이 뜨지 않는다.** 업무·액션 줄을 적어도 업무가 생기지 않는다(M-14). 버튼은 WORK-008 이 종료 후 상세에만 붙인다 |

## Execution

### Phase 1 — WS 2단 중계 · 녹음 적재 · 트랜스크립트 (백엔드)

- **Status**: TODO
- **설명**: 화면 없이 **오디오가 백엔드를 지나 Soniox 로 가고, 원본이 파일로 쌓이고, 확정 토큰이 DB 에 들어가는** 상태를 만든다. 검증은 오디오 파일을 밀어 넣는 스크립트로 한다 — 마이크를 붙이기 전에 중계가 먼저 서야 한다.
- **작업**:
  - [ ] `config.py`·`.env.example`·compose — `SONIOX_API_KEY`(**기본값 없음, 없으면 기동 실패**) · `STORAGE_ROOT` 볼륨
  - [ ] `integrations/soniox.py` — WS 클라이언트. config 프레임(`stt-rt-v5`·`ko`·diarization on·**endpoint detection off**) · 토큰 수신 · 종료 프레임
  - [ ] `integrations/storage.py` — 녹음 경로 규칙 · append. **`anyio.to_thread` 로 동기 I/O 를 밀어낸다**
  - [ ] `api/meeting_stream_router.py` — WS. **첫 텍스트 프레임 `{type:"auth"}` 인증**, 실패 시 즉시 닫기 · 상태가 `recording` 이 아니면 거부 · **동시 접속 두 번째 거부**
  - [ ] `service/meeting_stream_service.py` — **① append → ② 중계** · 잠정 push · **확정만 적재**(화자 전환마다 블록 분리) · 백프레셔(잠정만 버림) · **`finally` 업스트림 닫기**
  - [ ] 적재 실패 → `meeting_stream_disconnected` 로 **스트림을 끊는다**
  - [ ] `GET /api/meetings/{id}/transcript?afterId=` — 새로고침 복구
  - [ ] `tests/test_meeting_stream.py` — Soniox 어댑터를 **대역**으로(BE §12). 인증·상태 가드·동시 접속·확정만 적재·적재 실패 시 끊김
- **검증**:
  - [ ] `.env` 에서 `SONIOX_API_KEY` 를 지우면 **API 가 기동하지 않는다**
  - [ ] 스크립트로 WS 에 붙어 **토큰 없이 첫 프레임을 보내면 즉시 닫힌다**
  - [ ] `scheduled` 상태 회의에 붙으면 **거부**되고, `recording` 이면 `ready` 프레임이 온다
  - [ ] 오디오 파일을 밀어 넣으면 **`STORAGE_ROOT` 아래 파일이 커지고** `meeting_transcript` 에 **확정 블록만** 쌓인다(잠정은 0건)
  - [ ] 화자가 바뀌면 **블록이 나뉘고** `speaker_label` 이 「화자 1/2」이다. **사람 이름 컬럼이 없다**
  - [ ] `at_ms` 가 **회의 시작 기준 오프셋**이고 벽시계 값이 아니다
  - [ ] **두 번째 접속을 시도하면 뒤에 온 쪽이 거부되고 첫 스트림이 끊기지 않는다**
  - [ ] `STORAGE_ROOT` 를 읽기 전용으로 바꾸면 **스트림이 끊긴다**(조용히 계속되지 않는다)
  - [ ] 스트림을 강제로 끊으면 로그에 **업스트림이 닫힌 기록**이 남는다(`finally` 확인)
  - [ ] **정적 검사**: 프론트 소스에 `soniox` 문자열·주소·키가 **0건**이다(불변식 1 — grep 결과를 완료 증거에)
  - [ ] `pytest` 통과
- **완료 증거**: 미작성

### Phase 2 — 마이크 캡처 · 스트림 훅 · 실시간 스크립트 패널

- **Status**: TODO
- **설명**: **앱 창에서 말하면 스크립트가 쌓이는** 첫 E2E. 여기서 Tauri 웹뷰의 마이크 권한이 실물로 확인된다(SYS-OQ-1 이 「구현 때 확인」으로 닫은 지점).
- **작업**:
  - [ ] `useMicCapture.ts` — `getUserMedia` · **인코딩/포맷 선택을 함수 하나로 격리**(§C-8) · 권한 거부·장치 없음 처리
  - [ ] `useMeetingStream.ts` — **WS 를 소유하는 유일한 훅.** 첫 프레임 토큰 · 잠정/확정/증분/에러 프레임 처리 · **자동 재연결 없음**
  - [ ] `MeetingLiveScreen` — 상태 바 + 좌 탭(회의록·AI 요약) + 우 탭(스크립트·첨부). WORK-006 의 껍데기를 대체
  - [ ] `StatusBar` — 「기록 중 00:12:38」(**서버 `recordingStartedAt` 기준**) + 「자동 저장 09:42」 + 「회의 종료」(**WORK-008 이 동작을 붙인다 — 이 work 에서는 비활성**)
  - [ ] `TranscriptPanel` — 확정 append · **잠정 블록 통째 갈아 끼움**(회색) · 화자 블록 · **자동 스크롤 정지 + 「최신으로」**
  - [ ] 새로고침 복구 — `GET /transcript` 로 확정 블록 복구 후 WS 로 잇는다
  - [ ] `DisconnectedBanner` — 「**녹음이 중단되었습니다**」 + 「끊긴 뒤의 말은 기록되지 않았습니다」 + 「**다시 시작**」
  - [ ] `MicPermissionNotice` — 「마이크를 쓸 수 없어 회의를 시작하지 못했습니다」 + 「다시 시도」. **상태는 `scheduled` 그대로**
  - [ ] Tauri 설정 — 앱 창 마이크 권한(macOS `NSMicrophoneUsageDescription` 등)
- **검증**:
  - [ ] **앱 창에서** 「회의 시작」 뒤 말하면 우측에 **회색 잠정 문장이 나타났다가 확정되면 굳는다**
  - [ ] 다른 목소리가 섞이면 「**화자 2**」 블록으로 나뉘고 **사람 이름이 어디에도 없다**
  - [ ] 위로 올려 읽으면 자동 스크롤이 멈추고 「**최신으로**」가 뜬다
  - [ ] **새로고침해도 확정 스크립트가 남아 있고 경과 시간이 이어진다**(클라이언트 타이머가 0 으로 돌아가지 않는다)
  - [ ] 마이크 권한을 **거부**하면 회의가 시작되지 않고 안내 + 「다시 시도」가 보이며 **상태가 「예정」 그대로**다
  - [ ] **네트워크를 끊으면** 「녹음이 중단되었습니다」 배너가 뜨고 **자동으로 되살아나지 않는다**. **네트워크 탭에 재연결 시도가 0건**이다
  - [ ] 「다시 시작」을 눌러야 스트림이 다시 열린다
  - [ ] **정적 검사**: `new WebSocket(` 을 호출하는 코드가 **`useMeetingStream.ts` 하나**다(FE §8 — grep 결과를 완료 증거에)
  - [ ] **정적 검사**: 「일시정지」 버튼이 화면에 **없다**(S007-OQ-1)
- **완료 증거**: 미작성

### Phase 3 — 사람 트랙 줄 · 안건 전환 (백 + 프롬프트 바)

- **Status**: TODO
- **설명**: 사람이 **자기 회의록을 쓰는** 단계. 「다음 주제로」가 **배치 강제 flush 의 트리거**라 배치 파이프라인(Phase 4)보다 먼저 표면을 세워 둔다.
- **작업**:
  - [ ] `POST /api/meetings/{id}/lines` — **`track` 은 서버가 `human` 으로 박는다** · `agendaId` 필수(사람 트랙 안건) · `kind` 4종 · `content` 1~2000자
  - [ ] `PATCH /api/meetings/{id}/agendas/{agendaId}` — `{state:"done"}`(「다음 주제로」). **배치 flush 훅 자리**를 여기에 둔다(Phase 4 가 채운다)
  - [ ] `AgendaLineTree` — 안건 제목 + 줄(라벨 34 + 본문, 기준선 `border-left:2px #EBEBEB`). **회의록 탭·AI 탭 공용**
  - [ ] `LinePromptBar`·`LineKindPopover` — h52 r16 · `/` 팝오버(논의·결정·업무·액션 + 구분선 + 「다음 주제로」·「안건 이동 ▸」) · 종류 라벨 칩 · **기본값 논의**
  - [ ] `Enter` + **「추가」 버튼 병행**. 저장 실패 시 **줄이 입력창으로 되돌아온다**(줄을 잃지 않는다) + U-7 규격 토스트
  - [ ] **업무·액션 줄에 버튼을 붙이지 않는다**(M-14)
  - [ ] `tests` — 트랙 강제 · 안건 소속 · 다른 트랙 안건 참조 거부
- **검증**:
  - [ ] 프롬프트에 문장을 적고 `Enter` 하면 **현재 안건에 논의 줄**로 붙는다
  - [ ] `/` 로 「결정」을 고르면 라벨 칩이 붙고 결정 줄이 된다
  - [ ] **「업무」·「액션」 줄을 적어도 업무가 생기지 않고 버튼도 없다**(내 업무 목록에 아무것도 늘지 않는다)
  - [ ] `/` → 「다음 주제로」를 고르면 현재 안건이 **완료 표시**가 되고 다음 안건이 현재가 된다
  - [ ] AI 트랙 안건 id 를 줄 요청에 넣으면 **거부**된다(트랙을 넘는 참조 없음 — M-5)
  - [ ] **서버를 내린 채** 줄을 등록하면 **그 줄이 입력창으로 되돌아오고** 토스트가 뜨며 **재요청이 나가지 않는다**(네트워크 탭)
  - [ ] **정적 검사**: 줄 생성 요청 본문에 `track` 을 담는 코드가 **0건**이다
  - [ ] `pytest` 통과
- **완료 증거**: 미작성

### Phase 4 — AI 배치 파이프라인 (백엔드)

- **Status**: TODO
- **설명**: **이 work 에서 가장 무거운 자리.** 트리거·세션·검증·증분 push 가 한 서비스 안에서 닫힌다. **실패 4종 중 셋(배치 실패·스키마 위반·없는 업무 참조)을 이 Phase 에서 재현**한다 — 화면에 아무 표시도 하지 않는 실패라, 여기서 확인하지 않으면 영영 확인할 수 없다.
- **작업**:
  - [ ] `ai_schemas/meeting_batch.json` — 안건·줄 배열의 `output_schema`
  - [ ] `service/meeting_batch_service.py`
    - [ ] 트리거 판정 — **확정 600자 · 안건 전환 즉시(80자 미만 생략) · 180초 상한 · 동시 실행 금지 · 타임아웃 120초**
    - [ ] 구간 커서 — `meeting_batch_run.from/to_transcript_id`. **실패·폐기 구간은 다음 배치에 합친다**
    - [ ] 제출 — **`resume` 로 회의 세션 이어 쓰기**(M-12) + 미처리 구간 + 안건 + **업무 화이트리스트**
    - [ ] 검증 — ① **스키마 위반 시 행 0건 전량 폐기**(`status='discarded'`) ② **화이트리스트 밖 `taskId` → `action` 강등, 본문 유지**
    - [ ] INSERT — **`track='ai'` 에만, 증분 추가만.** 기존 AI 줄을 UPDATE 하지 않는다. AI 안건도 `track='ai'`
    - [ ] push — `ai.increment { seq, appliedAt, agendas, lines }`. **`seq` 는 성공분 최대값에서 파생**
  - [ ] **`except Exception` 을 쓰지 않는다.** 처리하는 실패는 위 목록뿐이고 그 밖은 전파(BE §8-1)
  - [ ] **외부 호출 중에는 트랜잭션을 열어 두지 않는다** — 읽기 → 커밋 → codex 대기 → 새 세션에서 쓰기(BE §7)
  - [ ] `tests/test_meeting_batch.py` — codex 어댑터 대역. BE §12 필수 **6**(스키마 위반 폐기) · **7**(화이트리스트 강등)
- **검증**:
  - [ ] 확정 발화가 600자를 넘으면 배치가 돌고 **`ai` 트랙에 안건·줄이 들어간다**
  - [ ] 「다음 주제로」를 누르면 **즉시 배치가 돈다**. 미처리가 80자 미만이면 **돌지 않는다**
  - [ ] 발화가 없어도 **180초마다** 한 번 돈다
  - [ ] 배치가 도는 중에 트리거가 와도 **동시에 두 개가 돌지 않는다**(로그·이력 확인)
  - [ ] **배치를 한 번 실패시키면**(대역이 예외) `meeting_batch_run.status='failed'` 로 남고 **`seq` 가 오르지 않으며**, **다음 배치의 구간이 그 앞까지 확장**된다
  - [ ] **스키마를 위반한 결과**를 주면 `status='discarded'` 이고 **`meeting_line` 에 행이 0건** 늘어난다(부분 파싱 없음)
  - [ ] **화이트리스트 밖 `taskId`** 를 가진 줄이 오면 **`kind='action'` 으로 내려앉고 `task_id` 가 비며 `content` 는 그대로**다
  - [ ] 모든 배치가 **같은 `ai_session_id` 를 `resume`** 한다(어댑터 대역이 받은 옵션으로 확인)
  - [ ] `meeting_line` 의 **`track='human'` 행이 배치 전후로 하나도 바뀌지 않는다**(불변식 4 — 개수·본문 해시 비교)
  - [ ] 배치가 120초를 넘으면 **실패로 마감**되고 구간이 이월된다
  - [ ] **정적 검사**: `except Exception` **0건**, `track='ai'` 외의 값으로 INSERT 하는 배치 코드 **0건**(grep 결과를 완료 증거에)
  - [ ] `pytest` 통과 — BE §12 필수 6·7
- **완료 증거**: 미작성

### Phase 5 — AI 요약 탭 · 근거 칩 · 배치 회차 · 첨부 탭

- **Status**: TODO
- **설명**: 배치 결과가 **화면에 즉시 나타나는** 단계. 두 탭이 **같은 트리 컴포넌트**를 쓰는 것이 이 Phase 의 구조적 요점이다 — WORK-008 의 통합본 화면이 그대로 이 컴포넌트를 재사용한다.
- **작업**:
  - [ ] `AiSummaryTab` — `AgendaLineTree` 재사용 + AI 전용 props(AI 안건 칩 · 근거 펼침 · 편집 불가)
  - [ ] 「**AI 안건**」 칩 — `#EEF1FE`/`#4A55B8`, h20 r4 11/600(**`TypeBadge` 규격 재사용**). 사람 안건과 순서대로 섞어 그리되 칩으로 구분
  - [ ] 근거 — 줄 hover 시 **우측 화살표**로만 펼친다. 펼치면 상세 설명 + 「09:34 – 09:36」 칩. **줄 전체 클릭은 아무 동작도 하지 않는다**
  - [ ] `EvidenceChip` 클릭 → **우측 스크립트가 그 구간으로 스크롤 + `#F4F5FF`/`#C9D1FB` 강조**
  - [ ] `BatchSeqLabel` — 「**배치 3회 반영 · 09:41**」. 새 증분이 오면 숫자가 오르고 **그 회차 줄이 1.5초 `#F4F5FF` 강조**
  - [ ] 아직 없음 상태 — 「첫 정리는 발화가 쌓이면 시작됩니다」 + 「배치 0회」
  - [ ] 탭 dot 색 — 회의록 `#B3B3B3` · AI 요약 `#338BF6` · 스크립트 `#7181F8` · 첨부 `#D9D9D9`. 진행 dot 에 3px 광륜. **탭 밑줄만 Ink**
  - [ ] `AttachmentTab`·`FileDrawer` — 목록(아이콘·이름·용량·시각·출처) · **`DrawerFrame` 을 쓰기만 하는** 파일 드로어(미리보기/원문 + 「다운로드」·「자료함에서 열기」). **폭을 다시 정하지 않는다**(FE §6-2). **문서함이 없어 빈 상태 스텁**
  - [ ] 「**AI 가 제안합니다**」 같은 문구를 **두지 않는다**
- **검증**:
  - [ ] AI 요약 탭이 **회의록 탭과 같은 「안건 > 줄」 트리**로 보인다(카드 형태가 아니다)
  - [ ] 상단에 「**배치 n회 반영**」이 있고 새 배치가 오면 **숫자가 오르며 새 줄이 잠깐 강조**된다
  - [ ] AI 가 만든 안건에 「**AI 안건**」 칩이 붙는다
  - [ ] **회의록 탭에는 AI 줄도 AI 안건도 보이지 않는다** — 탭을 오가며 확인한다
  - [ ] AI 줄에 hover 해 화살표로 펼치면 근거 칩이 있고, **칩을 누르면 우측 스크립트가 그 구간으로 스크롤·강조**된다
  - [ ] AI 줄을 **클릭해도 아무 일도 일어나지 않는다**(회의 중 AI 줄은 편집 대상이 아니다)
  - [ ] **배치를 한 번 실패시켜도 화면에 아무 경고가 뜨지 않고** 회차만 그대로다. 다음 배치에 **그 구간까지 합쳐서** 들어온다
  - [ ] 스키마 위반 결과 뒤 AI 탭에 **줄이 하나도 늘지 않는다**
  - [ ] 화이트리스트 밖 업무를 참조한 줄이 **액션 줄로 보이고 본문이 남아 있다**. 별도 경고가 없다
  - [ ] **끊긴 동안에도 좌측에서 줄을 계속 적을 수 있다**
  - [ ] **정적 검사**: 화면당 `--tm-ink` 사용처가 **탭 밑줄 하나**다(FE §5-2 — grep 결과를 완료 증거에)
  - [ ] **정적 검사**: 「업무 생성」·「업무 갱신」 버튼이 회의 중 화면에 **0건**이다(M-14)
  - [ ] **정적 검사**: **폭 리터럴(`840`·`w-[840px]`)이 `features/meetings/` 안에 0건**이다(FE §6-2 — 파일 드로어가 `DrawerFrame` 을 쓰기만 한다)
- **완료 증거**: 미작성

## Pre-deploy Check

- [ ] **`SONIOX_API_KEY` 가 서버에만 있고 프론트 번들에 실리지 않는다**(빌드 산출물 grep — 불변식 1)
- [ ] `STORAGE_ROOT` 볼륨이 **컨테이너 재시작을 넘겨 유지**된다(녹음 원본이 사라지지 않는다)
- [ ] WS 응답·에러에 **내부 경로·스택 트레이스가 실리지 않는다**
- [ ] 업스트림이 **클라이언트 연결 뒤에만 열린다**(과금·300분 한도) — 유휴 상태에서 Soniox 연결이 0인지 확인
- [ ] 녹음 파일 권한이 서버 계정으로 제한돼 있다

## Rollback

- **스키마 변경이 없다** — 되돌릴 마이그레이션이 없다. 쌓인 트랜스크립트·AI 줄은 남고, 되돌리면 **읽을 화면만 사라진다**
- **백엔드**: `meeting_stream_router` 미등록으로 WS 표면을 걷어낼 수 있다. 그 순간 「회의 시작」한 회의가 **`recording` 에 갇힌다** — 되돌릴 때는 **남은 `recording` 회의를 `ended` 로 마감하는 일회성 처리**를 함께 한다
- **배치만 되돌리기**: `meeting_batch_service` 의 트리거를 끄면 스트림·스크립트·사람 줄은 그대로 돈다(AI 탭이 「배치 0회」로 남는다). **Phase 4·5 는 이 단위로 부분 revert 가 가능하다**
- **프론트**: 브랜치 폐기. WORK-006 의 시작 전 화면·사이드 탭 껍데기가 남아 있어야 회의 중 화면이 빈 창이 되지 않는다
- **compose**: Soniox 는 외부 서비스라 되돌릴 것이 없다. 키를 회수하면 스트림이 열리지 않고 **끊김 배너로 드러난다**(조용히 실패하지 않는다)

## Done Criteria

- [ ] 모든 Phase 가 `DONE` 또는 `SUPERSEDED` 다.
- [ ] **SPEC-007 §6 Acceptance 18개 항목이 전부 확인**됐다.
- [ ] **실패 4종을 전부 재현한 기록**(배치 실패 · 스키마 위반 · 없는 업무 참조 · 연결 끊김)이 완료 증거에 있다.
- [ ] **2트랙 격리 실측** — 배치 전후로 `track='human'` 행이 하나도 바뀌지 않았다는 비교 결과가 있다.
- [ ] 정적 검사 8종(프론트에 soniox 흔적 0 · `WebSocket` 생성 단일 · 줄 요청에 `track` 없음 · `except Exception` 0 · AI INSERT 트랙 고정 · 회의 중 업무 버튼 0 · Ink 하나 · **드로어 폭 리터럴 0**) 결과가 붙어 있다.
- [ ] BE §12 필수 테스트 **6(스키마 위반 폐기)·7(화이트리스트 강등)** 이 통과한다.
- [ ] product `log.md` 와 `30-work/README.md` 가 갱신됐다.

## Open Issues

- **배치 트리거 수치는 실측 전 값이다**(S007-OQ-2). 600자·180초·120초·80자는 발화 속도와 codex 왕복을 어림한 값으로, **첫 실제 회의 뒤 조정된다.** 계약(트리거 4종·동시 금지·구간 이월)은 그대로 두고 **값만 바꾼다** — 값을 한 곳(상수)에 모아 두어야 한다
- **오디오 전송 포맷을 spec 이 정하지 않았다**(S007-OQ-3 · §C-8). WS 계약은 「Soniox 가 받는 형식 중 하나를 그대로 중계한다」까지다 — **Phase 2 에서 실제로 고르고 그 근거를 완료 증거에 적는다**
- **동시 접속 정책(뒤에 온 쪽 거부)은 spec 판단이다**(S007-OQ-4). 정책서에 근거가 없다
- **`GET /api/meetings/{id}/transcript` 가 아키텍처 §10 표면 목록에 없다**(S007-OQ-5). 표 갱신은 코디 소관
- **「일시정지」를 뺐다**(S007-OQ-1). 스트림을 멈췄다 잇는 것은 세션 경계 처리이고 v1 에서 다루지 않기로 한 부류다 — 필요하면 DEC-003 갱신이 먼저다
- **웜스타트가 실패한 회의에서 첫 배치가 세션을 만든다.** WORK-006 이 「실패해도 시작을 막지 않는다」로 정했으므로 이 경로가 필요한데, **DEC-003 §STT 의 「회의 시작 시 웜스타트」와 결이 다르다** — 실제로는 「세션이 없으면 첫 배치가 만든다」가 된다. 코디 확인이 필요하다
- **회의 중 첨부의 자료함 갈래가 닫혀 있다**(문서함 work 대기 — WORK-006 과 같은 사유). 파일 드로어의 「자료함에서 열기」도 그때 실동작한다
- **Windows 에서 마이크 캡처가 확인되지 않았다.** 이 work 의 검증은 macOS 앱 창 기준이다

## Related

- SPEC: SPEC-007 (frontmatter `links.specs`)
- Work: WORK-006 (선행) · WORK-008 (후속)

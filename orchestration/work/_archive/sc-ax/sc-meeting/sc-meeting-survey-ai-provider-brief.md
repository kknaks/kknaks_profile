# [reviewer_code] 조사 1 — 백엔드 AI 프로바이더(LLM·STT) 사용 현황 전수조사

너는 **sc-ax `reviewer_code` 워커**다. 이번 태스크는 **판정 없는 read-only 조사**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting/orchestration/roles/sc-ax/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting` (branch `kknaksss/sc-meeting`) — **읽기만 한다.**
스펙 워크트리(read-only 참조): `/Users/kknaks/orca/workspaces/mediness-mediness/sc-meeting-spec`

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/mediness-mediness/sc-meeting-spec/products/sc-ax/40-architecture/system.md` — §4 「Meeting provider와 worker」. provider 는 내부 구현 상세이고 사용자 계약이 아니라는 선언.
- `/Users/kknaks/orca/workspaces/mediness-mediness/sc-meeting-spec/products/sc-ax/20-spec/spec-004-meeting-note.md` — §4 Recording·transcript, §5 Refinement·speaker·summary. 회의 AI 가 지켜야 하는 계약(version·evidence·채택 전 제안).
- `/Users/kknaks/orca/workspaces/mediness-mediness/sc-meeting-spec/products/sc-ax/40-architecture/action-execution.md` — AX 실행(대화·액션)의 모델 호출 경계.

선례 리포트 형식: `/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting/orchestration/work/_archive/sc-ax/sc-org/org-chart-survey-report.md` — **[사실]/[추정]** 표기, `파일:줄` 인용, 세 줄 요약 → 전수표 → 상세 순서. 이 형식을 따른다.

## 2. 배경 / 왜 조사하나

회의실 화면(Claude Design 「SCAX 회의록 프로토타입」)을 새로 만든다. 화면은 회의 중 **실시간 스크립트(STT) · AI 노트(자동 요약) · 종료 후 통합 초안(노트+AI 노트+스크립트 합성)** 을 쓴다. 이걸 구현하려면 **지금 백엔드가 AI 를 어디서 어떻게 부르는지**부터 알아야 한다. 이 조사는 후속 SPEC·WP 의 재료다 — 결론을 내리지 말고 **사실을 빠짐없이 표로** 남긴다.

코디가 grep 으로 잡은 입구(출발점이지 전부가 아니다 — **네가 전수조사해서 빠진 것을 채워라**):

| 층 | 파일 | 코디 관찰 |
|---|---|---|
| LLM adapter | `backend/src/ax_workspace/platform/codex_cli.py` | `CodexCliProviderAdapter`(69줄~) — Codex CLI 를 subprocess 로 띄우는 구조. port 는 `modules/ax_execution/ai` 에서 import(24줄) |
| LLM 소비자 | `bootstrap/application.py` · `bootstrap/conversation_worker.py` · `modules/reports/workflow_metadata.py` | codex_cli 를 참조하는 파일 전부 |
| STT adapter | `platform/soniox.py` | `SonioxTranscriptionAdapter(RealtimeTranscriptionKeyIssuer, FinalTranscriber)`(33줄) — REST + websocket 키 발급 |
| STT port | `modules/meetings/transcription.py` | `RealtimeTranscriptionKeyIssuer` · `FinalTranscriber` · `FinalTranscriptSegment` |
| 회의 AI 모듈 | `modules/meetings/refinement.py` · `summary.py` · `jobs.py` · `application.py` | refinement·summary 가 **어느 provider 로** 도는지 코디는 아직 모른다 — codex_cli grep 에 안 걸렸다 |
| 회의 worker | `bootstrap/meeting_worker.py` · `entrypoints/meeting_worker.py` · `platform/meetings.py` · `platform/recordings.py` | 잡 루프·lease |
| 의존성 | `backend/pyproject.toml` | `httpx` 만 있고 anthropic/openai/litellm SDK 가 **없다** |
| 실행 | `Makefile:267` 부근 | `SONIOX_API_KEY` opt-in 통합 테스트 |

## 3. 조사 질문 — 리포트가 답해야 하는 것

### Q1. 프로바이더 목록
백엔드가 부르는 **외부 AI 서비스 전부**. 각각: adapter 파일·클래스, 호출 방식(SDK/REST/CLI subprocess/websocket), 인증(환경변수 이름 — 값은 절대 인용 금지), 모델/설정값이 어디서 오는지(settings·env·하드코딩), 타임아웃·재시도·취소.

### Q2. port ↔ adapter 배선
각 provider 의 **port(Protocol/ABC)** 가 어느 모듈에 있고, 어디서 **조립(bootstrap)** 되는지. `bootstrap/application.py` 와 각 worker bootstrap 의 조립 코드를 `파일:줄` 로. 테스트용 fake/stub adapter 가 있으면 같이(`tests/` 포함).

### Q3. 회의 도메인의 AI 경로 — 가장 중요
`modules/meetings/` 에서 AI 가 개입하는 **모든 단계**를 순서대로:
1. 실시간 전사(websocket 키 발급 → 프론트가 직접 붙나, 백이 중계하나)
2. 녹음 파일 최종 전사(FinalTranscriber)
3. refinement(정제·화자) — **어느 provider? 프롬프트는 어디? 출력 스키마는?**
4. summary — 동일. `SummaryStatement`·evidence 가 어떻게 만들어지는지.
5. 각 단계의 상태 전이(uploaded→transcribing→transcribed…)와 durable job·lease 구조.

현재 프로토타입 화면이 요구하는 것과 대조: (a) 회의 **중** 실시간 AI 노트가 지금 코드에 있는가, 없으면 가장 가까운 것은 무엇인가 (b) 종료 후 노트·AI 노트·스크립트 **합성** 초안에 해당하는 코드가 있는가 (c) 안건(agenda) 단위 구조가 있는가. **없으면 「없음」이라고만 쓴다 — 어떻게 만들지는 쓰지 마라.**

### Q4. 회의 밖 AI 경로
대화(conversation)·액션·자료(material)·리포트가 LLM 을 쓰는 경로. 회의와 **같은 adapter 를 공유하는지**, MCP 서버(`entrypoints/mcp.py`)가 어떻게 끼는지. 회의 refinement/summary 를 이 경로로 돌릴 수 있는 구조인지는 **사실만** (재사용 여부 판단은 코디·사용자 몫).

### Q5. 문서 ↔ 코드 대조
system.md §4·spec-004 §4·§5 가 말하는 것과 코드가 다른 지점. 문서에만 있거나 코드에만 있는 것을 표로.

### Q6. 실행·검증 환경
provider 를 실제로 부르려면 무엇이 필요한가(env 이름, Codex CLI 설치·auth 파일 위치, Makefile 타깃). 통합 테스트가 어떻게 격리돼 있는지(`-m integration`, opt-in 타깃).

## 4. 먼저 읽을 핵심 파일

- `backend/src/ax_workspace/platform/codex_cli.py:24-70` — port import 와 adapter 시그니처
- `backend/src/ax_workspace/modules/ax_execution/ai.py` (또는 패키지) — LLM port 정의
- `backend/src/ax_workspace/platform/soniox.py:19-60` — STT port 구현
- `backend/src/ax_workspace/modules/meetings/application.py:31-135` — `MeetingRepository` Protocol 과 `MeetingApplication.__init__` 의 의존성 목록(여기서 AI port 가 무엇으로 주입되는지 보인다)
- `backend/src/ax_workspace/bootstrap/application.py` · `bootstrap/meeting_worker.py` — 조립
- `backend/src/ax_workspace/modules/meetings/refinement.py` · `summary.py` · `jobs.py`
- `backend/tests/contract/test_meeting_recordings.py` · `test_meeting_realtime.py` — fake provider 가 어떻게 생겼는지
- `backend/tests/architecture/` — 경계 규칙(domain/application 이 provider 를 import 하면 안 되는 규칙)

## 5. allowed_paths — 이 밖은 건드리지 마라

- **리포 파일 수정·생성 금지.** 코드 워크트리·스펙 워크트리 모두 읽기만.
- 산출물은 **단 하나**: `/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting/orchestration/work/sc-meeting/survey-01-ai-provider-report.md`
- 테스트 실행·서버 기동·DB 접속·외부 API 호출 금지. 근거는 소스와 문서뿐.
- 환경변수 **값**·키·auth 파일 내용은 인용 금지(이름만).

## 6. 조사 단계

1. 역할 문서 → §1 SSOT 3개 → 선례 리포트 형식 순으로 읽는다.
2. `backend/src` 전체를 `grep -rniE 'codex|soniox|openai|anthropic|llm|model|transcri|summar|refin|prompt'` 로 훑어 §2 표에 없는 파일을 먼저 추가한다(전수 원칙 — 브리프에 없는 입구를 찾는 것이 네 첫 일이다).
3. Q1→Q6 순으로 답한다. 각 문장에 `파일:줄` 과 **[사실]/[추정]** 을 단다.
4. 리포트 맨 앞에 **세 줄 요약**, 맨 뒤에 **「코디가 물어봐야 할 것」** 절(네가 판단하지 않고 사용자에게 넘길 질문 목록)을 둔다.

## 7. 범위 제약 — 하지 말 것

- 설계 제안·리팩터링 제안·「이렇게 하면 된다」 금지. 사실과 공백만.
- 회의실 화면 자체(프론트)는 이번 범위 밖 — 프론트는 다음 조사에서 따로 한다. 단 Q3-1(실시간 전사가 프론트 직결인지)에 필요한 `frontend/` 참조는 `파일:줄` 한 줄로만.
- 코드·문서 수정 금지. 브랜치·커밋·push 금지.

## 8. 검증

```
리뷰는 read-only — 코드를 고치지 않고 테스트도 돌리지 않는다. 리포트 저장 후 `git -C /Users/kknaks/orca/workspaces/ax-workspace/sc-meeting status --porcelain` 과 스펙 워크트리 status 가 **비어 있음**을 확인하고 보고에 붙인다. Q1~Q6 각 절이 비어 있지 않은지, 모든 인용에 파일:줄이 있는지 자기점검.
```

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.

- **커밋·push·PR 하지 마라.** 산출물은 리포트 파일 1개뿐.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_d9153f79-d709-4d1e-81fd-bbb2e654d75d --from term_a4d2b3a8-30ab-4731-85f2-5ce199bada6b \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_code 완료: 조사 1 AI 프로바이더" \
  --body "리포트 경로 / 세 줄 요약 / 프로바이더 수·회의 AI 단계 수 / 문서≠코드 건수 / 코디가 물어봐야 할 것 / 워크트리 status 비어 있음 확인"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_d9153f79-d709-4d1e-81fd-bbb2e654d75d \
  --text "[worker_done] reviewer_code 완료 — 조사 1 AI 프로바이더 리포트. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_d9153f79-d709-4d1e-81fd-bbb2e654d75d --text "[질문] reviewer_code: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)

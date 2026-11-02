# [backend] 고도화 — 개선 항목의 서버 쪽 현재 코드 전수조사

너는 **strong-hajin `backend` 워커**다. **너는 이 작업의 맥락이 없다** — 아래를 먼저 읽어라:

- 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-2/orchestration/roles/strong-hajin/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)
- 코드 레포 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-enhance/AGENTS.md`
- **개선 목록(이번 조사의 출처)**: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-2/para/projects/summer-star/strong-hajin/improvements/README.md` 와 같은 폴더의 `SH-IMP-0NN-*.md` — 아래 §2 의 항목마다 그 문서의 「사용자 정리」·「조사 항목」·「코드 확인」 을 읽어라. 「코드 확인」 은 코디가 한 **첫 훑기**라 출발점일 뿐이다(줄 번호를 다시 확인하라)
- 관련 SPEC: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-2/para/projects/summer-star/strong-hajin/20-spec/` (회의 = `spec-004-calendar-scheduling.md` 일부 · 외부 채널 = `spec-008-external-channels.md` · 카톡 수집기 = `spec-009-mac-kakao-collector.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-enhance`
base: `origin/main` (`f0ad522` — 운영 반영 코드)

⚠ **같은 워크트리에 frontend 워커가 동시에 탄다.** 둘 다 읽기 전용 조사이고 서로 다른 리포트 파일 하나씩만 쓴다. `backend/` `frontend/` 어느 쪽도 **고치지 마라.** 네 몫이 아닌 쪽도 답에 필요하면 읽어라.

## 0. 이것은 조사다 — 고치지 마라

**읽기 전용 조사다.** 코드를 한 줄도 바꾸지 않는다. 산출물은 리포트 **한 장**뿐이다.
「이렇게 고치면 된다」는 쓰지 마라 — 사용자가 이 리포트를 보고 계약을 정한다. **지금 무엇이 어떻게 도는지만** 적는다.
테스트·빌드를 돌리지 마라. 읽어서 답할 수 있는 것만 답하고, 못 답한 것은 「조사 한계」에 적는다.

## 1. 왜 조사하나

사용자가 운영(`https://ax.medisolveai.xyz`)을 쓰며 낸 개선 17건 중 **조사 뒤 구현**으로 정한 항목의 서버 쪽 근거를 확정한다. 이 리포트가 다음 SPEC·WORK 의 근거다.
빠진 자리가 곧 다음 판의 FAIL 이다 — **시작점에서 멈추지 말고, 같은 심볼·패턴·API 를 쓰는 곳을 grep 으로 전부 세어 숫자로 적어라.**

## 2. 항목별 물음 (네 몫 = 서버 계약·규칙·프롬프트)

### SH-IMP-001 · 017 — AX 업무 생성 흐름 vs AX 회의 생성 흐름

1. **AX 업무 생성**이 대화에서 업무 초안이 되기까지의 서버 경로 — 의도 인식 → 단계(스텝)들 → 초안(action card) → 확정. 단계마다 무엇을 묻고 무엇을 채우는지, 상태 기계·액션 종류·도구 이름·프롬프트 위치(파일:줄)
2. 그 흐름이 **업무가 속할 프로젝트와 연관 업무를 어떻게 찾는지** (SH-IMP-017 핵심 의심) — 호출하는 도구(`task_list`·`project_list` 등)와 그 인자, 프롬프트의 지시 문장, 서버가 **미리 싣는** 맥락. 프로젝트 후보를 전부 보는가 · 일부(페이지·상한)만 보는가 · 이름 일치뿐인가. 같은 프로젝트의 기존 업무·중복 후보·선후행을 보는가. 도구 응답의 상한(limit·필드)
3. 참고자료(첨부·material)를 어떻게 찾고 카드에 붙이는지 — 누가(AI/서버/사람) · 어떤 소스 · 어떤 계약
4. **AX 회의 생성**(`create_current_meeting` 등 MCP 도구 · `action-meeting-card`)의 서버 경로 — 위 1~3 과 같은 물음. 업무 생성과 **어디서 갈라지는지** 표로
5. 이미 만들어진 회의를 **AX 채팅에서 바꾸는 도구가 있나**(시간·참석자·장소) — SH-IMP-016

### SH-IMP-003 · 016 — The Connect 회의실 연동

1. Connect 클라이언트(`room_booking_*`, `TDL_*` env) 위치와 **지금 부르는 Connect API 전부** — 경로·메서드·페이로드·응답·인증(계정 하나? 사용자별?)·timeout(파일:줄)
2. 회의 생성 때 회의실 예약을 실제로 하나 · 가용성 조회를 하나 · 회의 수정·취소 때 Connect 를 부르나. `meeting_room_creation_attempts` 의 역할
3. 코드·주석·테스트·fixture 에서 확인되는 **Connect 가 제공하는 기능**(회의실 목록·가용 조회·예약·수정·취소) — 코드에 없는 것은 「코드에 없음」 이라고만 적는다(지어내지 마라)
4. 회의 수정 API(시간·참석자·장소) 전부 — 경로·페이로드·겹침 검증(`MEETING_TIME_OVERLAP`)·장소 필드 저장 방식

### SH-IMP-005 — 「이전 회의 정보 불러오기」 버그 둘

1. 「이전 회의 정보 불러오기」 가 부르는 API(있으면)와 **복사하는 필드 전부** — 시간이 왜 들어가는가(서버가 주나, 화면이 넣나)
2. 안건 `source`(출처) 값의 종류 전부와 **누가 언제 정하나** — 수기로 쓴 안건이 「지난 회의에서 넘어옴」 이 되는 경로. `carried_from_meeting_id` 가 출처 판정에 어떻게 쓰이나
3. 「지난 회의에서 결론이 안 난 항목」 을 안건으로 가져오는 로직이 지금 있나(`concluded`·최종 벌 기준)

### SH-IMP-006 — 회의록 생성 파이프라인(timeout · 맥락 · 교정 · 누락)

1. **timeout** — `platform/codex_cli.py` 의 `timeout_seconds` 가 쓰이는 호출 전부(대화·배치·웜스타트·종료 합성)와 각 단계의 실제 제한값. env 로 바꿀 수 있는 자리가 있나. Claude provider 쪽도 같은 표로
2. **중간(배치)** — 웜스타트가 싣는 맥락 · 배치 프롬프트가 싣는 것 · 도구 목록(`AX_MEETING_AI_TOOLS`)과 프롬프트가 도구를 쓰라고 시키는 문장 · 실패한 배치 구간의 발화는 다음 배치·최종에 다시 실리나(커서가 어떻게 움직이나)
3. **최종(종료 합성)** — 싣는 재료 전부, 세션 이어 쓰기 vs 콜드 스타트 판정, 전사 전량이 실리는 조건, 근거 없는 줄 거절(`_bind_evidence`)이 시도 전체를 실패시키는 경로, 재시도 상한
4. **교정** — 정정(STT 오인식 보정)에 해당하는 단계·필드가 있나. `results.py` `correction_kind` 가 무엇인가
5. **기한 버그** — `resolve_due` 의 「이어진 다음 회의」 를 무엇으로 고르나(`next_meeting_starts_on` 을 만드는 쿼리, 파일:줄). **회의보다 앞선 날짜가 기한이 될 수 있는 경로**가 있나
6. 머리의 「참석 N명」 은 무엇을 센 값인가(참석자 행 · 화자 수 · 주최자 포함 여부)
7. **메디니스 비교** — 메디니스 앱 레포를 **읽기만** 한다: `git -C /Users/kknaks/git/harness_works/mediness-app show origin/dev:<경로>` 로 읽어라(체크아웃·pull 금지). 볼 것: `back/app/services/meeting_v2_extractor.py` · `meeting_v2_catalog.py` · `meeting_v2_finalize.py` · `back/app/seeds/prompt_seeds.py` · `back/app/config.py`(`meeting_v2_*`). 물음 — **중간 배치는 무엇을 참고하나**(카탈로그·이전 회의록·화자 정정 델타·도구 상한) · **최종은 어떻게 하나**(정정 pass → 다시 쓰기 · 보정 표 · 전체 발화 재주입 여부 · timeout) · 카탈로그에 무엇이 들어가나. strong-hajin 과 **항목별 대조표**로

### SH-IMP-012 — 슬랙 방을 나간 뒤 분배

1. 방 멤버십을 무엇으로 알고 언제 다시 확인하나(재확인 주기·트리거, 파일:줄) · 분배(fan-out) 판정 위치
2. Socket Mode 에서 받는 이벤트 종류 전부 — `member_left_channel`·`channel_left` 등을 처리하나
3. 「나간 뒤 다음 재확인까지 분배가 남는 창」 이 코드상 실제로 있는가 — 있으면 최대 길이

### SH-IMP-013 ① — 카톡 이름 없는 방

1. 방 이름이 서버에 어떻게 들어오고 저장되나 · 이름 없는 방(멤버 0·시스템방)이 목록 API 에 그대로 나가나 · 숨김·필터 규칙이 있나

### SH-IMP-008 · 015 · 010 — 이미 정한 구현의 서버 쪽 시작점 (짧게)

1. 대화 전송의 참고 자료(`context` · `ConversationContextReferenceInput` · `conversation_context_references`)가 받는 `resource_type` 전부와 프롬프트에 붙는 모양(파일:줄) — 「메시지」 종류를 더할 자리
2. 방 메시지 조회(`GET /api/inbox/rooms/{id}/messages`)의 커서 방향 · 「특정 메시지 기준 위아래」 조회가 가능한 저장 구조(정렬 키·인덱스)인가 · 메일 한 통을 꺼내는 서버 함수
3. `/api/inbox/stream` 사건 종류 전부와 사건을 내는 자리 — 연동 상태(설정 화면 숫자: DB 적재 건수 · 마지막 수집 · 백필 진행)를 바꾸는 자리마다 사건이 나가나

### 공통

- 위 각 경로의 계약 테스트·acceptance journey 가 어디 있나(파일) — 다음 판이 고칠 테스트 범위를 세기 위해

## 3. allowed_paths — 이 밖은 건드리지 마라

- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-2/orchestration/work/strong-hajin-enhance/be-survey-report.md` ← **이 파일 하나만 만든다**

코드 워크트리·메디니스 레포는 **읽기만** 한다. 커밋·push·PR 금지.

## 4. 하지 말 것

- 코드·테스트를 고치지 마라. 테스트·빌드를 돌리지 마라
- **서버·프론트·Tauri 를 띄우지 마라. 사용자 포트와 프로세스를 건드리지 마라** (8001·5176·54329)
- 브라우저를 열지 마라. **운영 서버·운영 DB 에 접속하지 마라** (운영 데이터 확인은 코디가 한다 — 필요한 쿼리가 있으면 리포트에 「코디 확인 필요」 로 적어라)
- 메디니스 레포를 체크아웃·pull·수정하지 마라
- 「이렇게 바꾸자」를 쓰지 마라
- 리포트에 사람 실명·메일을 쓰지 마라(공개 레포로 아카이브된다) — 「팀원 A」처럼 쓴다

## 5. 리포트 형식

```
# 고도화 조사 (backend)

## 0. 한 줄 요약 — 항목별 한 줄 (원인이 보이면 원인 한 줄)
## 1~. 항목별 절 — §2 물음 번호대로 답
## N. grep 개수표 — 항목별로 센 심볼과 개수
## N+1. 코디 확인 필요 — 운영 DB·로그로만 갈리는 것(쿼리 초안 포함)
## N+2. 조사 한계
```

**모든 답에 `파일:줄` 근거를 단다.** 근거 없는 문장은 쓰지 않는다.

## 6. 검증

- 리포트가 위 경로에 있다. §2 의 물음이 하나도 빠지지 않았다(못 답한 것은 조사 한계에)
- `git -C /Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-enhance status --short` 가 비어 있다

## 7. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 코디handle 은 브리프 작성 시점 값이다. preamble 과 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.

- **커밋·push·PR 하지 마라.**
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_367ca23a-f846-44c0-afc7-07b6655df214 --from <네 워커handle — preamble 에 있다> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: 고도화 조사" \
  --body "리포트 경로 / 항목별 한 줄 요약 / 코디 확인 필요 / 조사 한계"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_367ca23a-f846-44c0-afc7-07b6655df214 \
  --text "[worker_done] backend 고도화 조사 완료 — <한 줄 요약>. 리포트 be-survey-report.md" --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_367ca23a-f846-44c0-afc7-07b6655df214 --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)

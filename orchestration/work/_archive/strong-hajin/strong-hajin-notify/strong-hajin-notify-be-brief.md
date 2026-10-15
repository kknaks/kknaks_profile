# [backend] 알림 — 알림의 서버 쪽 현재 코드 전수조사

너는 **strong-hajin `backend` 워커**다. **너는 이 작업의 맥락이 없다** — 아래를 먼저 읽어라:

- 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/roles/strong-hajin/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)
- 코드 레포 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-notify/AGENTS.md`
- 알림 경계를 그어 둔 문서(읽기만):
  - `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/para/projects/summer-star/strong-hajin/10-decision/decision-005-tauri-wrapper.md` — D-04 「OS 알림 연결은 래퍼 책임, 알림 시스템은 후속」
  - `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/para/projects/summer-star/strong-hajin/20-spec/spec-006-tauri-wrapper.md` §2.5 — 「이번에 만들지 않는 것」 표
  - `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/para/projects/summer-star/strong-hajin/10-decision/decision-008-external-channels.md` D-37 · D-50 — 설정 알림 메뉴를 미뤘다 · 수집 실패는 배너로
  - `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/para/projects/summer-star/strong-hajin/20-spec/spec-003-task-lifecycle-v2.md` · `spec-008-external-channels.md` — 업무 상태·외부 채널 계약(「알림」 이 언급된 줄만 찾아 읽어도 된다)

작업 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-notify`
base: `origin/main` (`d2a06fa` — 운영 반영 코드)

⚠ **같은 워크트리에 frontend 워커가 동시에 탄다.** 둘 다 읽기 전용 조사이고 서로 다른 리포트 파일 하나씩만 쓴다. `backend/` `frontend/` 어느 쪽도 **고치지 마라.** 네 몫이 아닌 쪽도 답에 필요하면 읽어라.

## 0. 이것은 조사다 — 고치지 마라

**읽기 전용 조사다.** 코드를 한 줄도 바꾸지 않는다. 산출물은 리포트 **한 장**뿐이다.
「이렇게 고치면 된다」는 쓰지 마라 — 사용자가 이 리포트를 보고 계약을 정한다. **지금 무엇이 어떻게 도는지만** 적는다.
테스트·빌드를 돌리지 마라. 읽어서 답할 수 있는 것만 답하고, 못 답한 것은 「조사 한계」에 적는다.

## 1. 왜 조사하나

사용자가 **알림**을 만든다. 이미 정한 것(2026-10-07 사용자):

- **나와 관련된 것만** 알림이 온다 — 업무 상태 변경 · 메일 · 슬랙 · 카톡 등
- 데스크톱 앱(Tauri)이 **켜져 있을 때만** 시스템 알림을 받는다 — 웹이 지금 있는 실시간 연결로 받아 Rust 로 넘겨 띄운다(서버 → 기기 푸시 없음)
- **설정의 알림 메뉴**와 **사이드바(좌측 내비)의 알림**을 이번에 만든다

이 리포트가 다음 BASE·DEC·SPEC 의 근거다. 빠진 자리가 곧 다음 판의 FAIL 이다 — **시작점에서 멈추지 말고, 같은 심볼·패턴·API 를 쓰는 곳을 grep 으로 전부 세어 숫자로 적어라.**

## 2. 물음 (네 몫 = 서버의 알림 원천·저장·전달)

### A. 지금 있는 알림

1. `modules/notifications.py` · `platform/notifications.py` 가 무엇인가 — 테이블(마이그레이션 파일:줄)·컬럼·종류(kind) 값 전부·수신자 결정·읽음 처리
2. **알림을 만드는 자리 전부** — 호출부를 grep 으로 전부 세어 표로(파일:줄 · 어떤 사건 · 누구에게). `work_tasks.py` · `work/application.py` · `actions.py` · `external_pubsub.py` · `mcp.py` · `tool_catalog.py` 는 출발점일 뿐이다
3. 알림을 읽는 API 전부(`entrypoints/http.py`) — 경로·응답 모양·페이지·읽음/전체 읽음. BASE-001 PA-06 이 말한 `http.py:1046,1050` 을 다시 확인하라
4. 수신함(InboxRail · 「참고」 카테고리)과 알림이 **같은 원천인가 다른 원천인가** — 같은 사건이 두 곳에 들어가나

### B. 「나와 관련된」 을 정할 재료 — 사건별로

각 사건에 대해 **지금 코드가 아는 「관련된 사람」** 을 적는다(담당자·요청자·참석자·소유자·멘션 대상 등, 파일:줄). 정책을 정하지 말고 **무엇을 알 수 있는지만.**

1. **업무** — 상태 전이 전부(SPEC-003 의 상태 기계)와 전이를 일으키는 자리. 배정·담당 변경·기한 변경·취소·보완 요청·재개·댓글. 전이마다 행위자와 영향 받는 사람
2. **메일** — 수신이 들어와 저장되는 자리 · 메시지가 **누구의 메시지함**에 쌓이나(계정 소유자) · 읽음 상태가 있나
3. **슬랙** — 이벤트 수신 → 분배(fan-out) 자리 · 분배 판정 · DM·채널·스레드·**나를 멘션**을 구분할 수 있는 필드가 저장되나
4. **카톡** — 수집기 업로드가 들어와 저장되는 자리 · 방·보낸 사람·내가 보낸 것인지 구분 필드
5. **회의** — 회의록 정리 완료 · 회의 초대·변경 등 사람에게 닿는 사건이 있나
6. **연동 수집 실패** — DEC-008 D-50 의 배너 상태를 만드는 자리
7. 시안의 설정 알림 항목(배정됐을 때 · 기한 하루 전 · 내 업무에 댓글 · 회의록 정리 완료 · 연동 수집 실패 · 일일 요약) 각각에 **대응하는 사건이 코드에 있나** — 있음/없음 표. 「기한 하루 전」·「일일 요약」 처럼 **시각에 따라 일어나는 것**을 돌릴 스케줄러·워커가 있나

### C. 실시간 전달

1. `/api/inbox/stream` 등 **서버 → 브라우저 실시간 경로 전부**(SSE·WebSocket) — 경로·인증·사건 종류 전부·사건을 내는 자리(파일:줄)·사람별로 걸러 보내나
2. 여러 프로세스(API·워커들)에서 난 사건이 스트림까지 어떻게 오나(pub/sub · DB 폴링 · 메모리) — 워커 프로세스에서 난 사건도 닿나
3. 끊겼다 다시 붙을 때 놓친 사건을 다시 주나(커서·last-event-id)

### D. 설정

1. 사용자별 설정을 저장하는 자리가 있나(테이블·컬럼) — 알림 설정을 둘 자리 후보로
2. 「받는 경로」 중 **메일·슬랙 DM** 으로 내가 나에게 보낼 수단이 코드에 있나(보내기 API — 외부 채널 답장 경로 재사용 가능성 사실만)

### 공통

- 위 각 경로의 계약 테스트·acceptance journey 위치(파일) — 다음 판이 고칠 테스트 범위를 세기 위해

## 3. allowed_paths — 이 밖은 건드리지 마라

- `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/be-survey-report.md` ← **이 파일 하나만 만든다**

코드 워크트리는 **읽기만** 한다. 커밋·push·PR 금지.

## 4. 하지 말 것

- 코드·테스트를 고치지 마라. 테스트·빌드를 돌리지 마라
- **서버·프론트·Tauri 를 띄우지 마라. 사용자 포트와 프로세스를 건드리지 마라** (8001·5176·54329)
- 브라우저를 열지 마라. **운영 서버·운영 DB 에 접속하지 마라** (운영 데이터 확인이 필요하면 리포트에 「코디 확인 필요」 로 쿼리 초안과 함께 적어라)
- 「이렇게 바꾸자」를 쓰지 마라. 「나와 관련된」 의 범위를 정하지 마라 — 재료만 적는다
- 리포트에 사람 실명·메일을 쓰지 마라(공개 레포로 아카이브된다) — 「팀원 A」처럼 쓴다

## 5. 리포트 형식

```
# 알림 조사 (backend)

## 0. 한 줄 요약 — A~D 각 한 줄
## 1~. A~D 절 — §2 물음 번호대로 답
## N. 사건 × 관련된 사람 표 — 사건 · 발생 자리(파일:줄) · 알 수 있는 관련자 · 지금 알림 생성 여부 · 지금 스트림 사건 여부
## N+1. grep 개수표 — 센 심볼과 개수
## N+2. 코디 확인 필요 — 운영 DB·로그로만 갈리는 것(쿼리 초안 포함)
## N+3. 조사 한계
```

**모든 답에 `파일:줄` 근거를 단다.** 근거 없는 문장은 쓰지 않는다.

## 6. 검증

- 리포트가 위 경로에 있다. §2 의 물음이 하나도 빠지지 않았다(못 답한 것은 조사 한계에)
- `git -C /Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-notify status --short` 가 비어 있다

## 7. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 코디handle 은 브리프 작성 시점 값이다. preamble 과 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.

- **커밋·push·PR 하지 마라.**
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_aa9fb9af-eed1-45ee-baad-95e52082321d --from <네 워커handle — preamble 에 있다> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: 알림 조사" \
  --body "리포트 경로 / A~D 한 줄 요약 / 코디 확인 필요 / 조사 한계"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_aa9fb9af-eed1-45ee-baad-95e52082321d \
  --text "[worker_done] backend 알림 조사 완료 — <한 줄 요약>. 리포트 be-survey-report.md" --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_aa9fb9af-eed1-45ee-baad-95e52082321d --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)

# [frontend] 고도화 — 개선 항목의 화면·데스크톱 셸 쪽 현재 코드 전수조사

너는 **strong-hajin `frontend` 워커**다. **너는 이 작업의 맥락이 없다** — 아래를 먼저 읽어라:

- 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-2/orchestration/roles/strong-hajin/frontend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)
- 코드 레포 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-enhance/AGENTS.md`
- **개선 목록(이번 조사의 출처)**: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-2/para/projects/summer-star/strong-hajin/improvements/README.md` 와 같은 폴더의 `SH-IMP-0NN-*.md` — 아래 §2 의 항목마다 그 문서의 「사용자 정리」·「현재 상태」·「코드 확인」 을 읽어라. 「코드 확인」 은 코디가 한 **첫 훑기**라 출발점일 뿐이다(줄 번호를 다시 확인하라)
- 데스크톱 셸 결정·스펙: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-2/para/projects/summer-star/strong-hajin/10-decision/decision-005-tauri-wrapper.md` · `20-spec/spec-006-tauri-wrapper.md` · 회의록 내보내기 다운로드를 고친 판 `30-work/work-010-*.md`(있으면) · 외부 채널 판 `30-work/work-011-*.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-enhance`
base: `origin/main` (`f0ad522` — 운영 반영 코드)

⚠ **같은 워크트리에 backend 워커가 동시에 탄다.** 둘 다 읽기 전용 조사이고 서로 다른 리포트 파일 하나씩만 쓴다. `backend/` `frontend/` 어느 쪽도 **고치지 마라.** 네 몫이 아닌 쪽도 답에 필요하면 읽어라.

## 0. 이것은 조사다 — 고치지 마라

**읽기 전용 조사다.** 코드를 한 줄도 바꾸지 않는다. 산출물은 리포트 **한 장**뿐이다.
「이렇게 고치면 된다」는 쓰지 마라 — 사용자가 이 리포트를 보고 계약을 정한다. **지금 무엇이 어떻게 도는지만** 적는다.
테스트·빌드를 돌리지 마라. 읽어서 답할 수 있는 것만 답하고, 못 답한 것은 「조사 한계」에 적는다.

## 1. 왜 조사하나

사용자가 운영(`https://ax.medisolveai.xyz`)과 데스크톱 앱(medi-ax)을 쓰며 낸 개선 17건 중 **조사 뒤 구현**으로 정한 항목의 화면·셸 쪽 근거를 확정한다. 사용자는 **데스크톱 앱만** 쓴다 — 앱에서의 동작이 기준이다.
빠진 자리가 곧 다음 판의 FAIL 이다 — **시작점에서 멈추지 말고, 같은 심볼·패턴·API 를 쓰는 곳을 grep 으로 전부 세어 숫자로 적어라.**

## 2. 항목별 물음 (네 몫 = 화면·데스크톱 셸)

### SH-IMP-014 · 011 — 데스크톱 앱 내려받기 · 하위 프레임 이동 (`frontend/src-tauri/`)

사용자 확인: 운영 **웹**에서는 회의록 내보내기 · 메일 · 슬랙 · 카톡 첨부가 모두 받아진다. **앱**에서는 네 갈래 모두 **다운로드 자체가 뜨지 않는다**(실패 토스트도 없음).

1. 셸의 **다운로드 가로채기**(회의록 내보내기를 고친 경로 — 앱 origin `/api/` 를 가로채 쿠키를 실어 받아 다운로드 폴더에 저장) 코드 위치와 동작 순서(파일:줄). 어떤 조건(경로 패턴·origin·`download` 속성·`_blank`·MIME)에서 가로채나
2. `on_navigation` 허용 목록(`guard.rs`·`lib.rs`) — 무엇을 허용·취소하나. **다운로드 이동·새 창(`_blank`)·하위 프레임(about:blank·about:srcdoc) 이동**이 각각 어떻게 판정되나. 가로채기보다 **먼저** 취소될 수 있는 경로가 있나(순서)
3. 외부 채널 판(카톡 수집기 · 창 닫기 = 웹뷰 파괴 · on_navigation · flavor 가르기)에서 바뀐 셸 코드가 가로채기 경로에 닿는 지점 — `git log -p` 로 그 판의 셸 변경을 보고 **회귀 후보**를 적어라
4. **프론트의 다운로드 입구 전부** — `download` 속성 · `target="_blank"` · `window.open` · blob/`createObjectURL` · `location` 이동 · `openExternal` · 셸 invoke. 파일:줄 표로, 각 입구가 셸 가로채기 조건에 들어가는지 열을 둬라. (이미 알려진 넷: 회의록 내보내기 · `/api/inbox/mail/{id}/attachments/…` · `/api/inbox/rooms/{id}/attachments/…`(슬랙·카톡) — **이 넷이 전부라고 가정하지 마라**)
5. 셸 로그가 어디에 남나(앱에서 재현할 때 코디가 볼 자리)

### SH-IMP-001 — AX 회의 생성 카드 vs AX 업무 생성 화면

1. AX 업무 생성의 **스텝 바이 스텝** 화면 흐름 — 컴포넌트·단계·각 단계의 입력/확인/참고자료 표시(파일:줄)
2. AX 회의 생성 확인 카드(`section.scax-actioncard.action-task-card.action-meeting-card`)의 화면 — 필드·참고자료(첨부) 표시·상태(`data-state`)·버튼
3. 둘이 **어디서 갈라지는지** 표로(같은 컴포넌트를 쓰는 곳 · 따로 그리는 곳)

### SH-IMP-002 · 004 — 회의 정보 수정 모달 겹침

1. 모달의 그리드·열 구조(CSS 파일:줄) — 왼쪽 열 `[날짜][시작][종료]` 의 폭 계산, 오른쪽 열 참석자 검색 입력(`input.search-input-box[aria-label="조직도 내 이름 검색"]`)의 위치
2. **검색 입력 뒤에 보이는 「버튼」 의 정체** — 넘친 종료 시간 칸인가, 별도 요소인가. 검색 입력 옆에 실제 버튼 요소가 있나(있으면 역할)
3. 같은 모달을 쓰는 화면 전부(생성·수정·AX 카드 편집 등)

### SH-IMP-003 · 016 — 장소 입력

1. 장소 입력(`input#meeting-head-place`)이 쓰이는 화면 전부와 저장 경로 · 회의실 선택 UI 가 있는 곳이 있나

### SH-IMP-005 — 「이전 회의 정보 불러오기」

1. 버튼 위치와 동작 — 무엇을 불러와 어느 필드에 넣나(**시간을 화면이 넣나**)
2. 안건 출처 문구(`p.scax-agenda-block__source` 「지난 회의에서 넘어옴」)를 어떤 값으로 고르나 · 출처 문구 종류 전부

### SH-IMP-015 · 008 · 010 — 이미 정한 구현의 화면 쪽 시작점 (짧게)

1. 메시지 행(`.scax-imsg`)·스레드 줄·스레드 패널 구조 — 호버 막대를 얹을 자리, 답글 0개 메시지에서 스레드 패널을 여는 데 막히는 것
2. 카톡 대화 화면이 같은 메시지 행 컴포넌트를 쓰나
3. 메일 머리(제목 · [답장] [전체 답장]) 컴포넌트 위치
4. AX 채팅 서랍을 **다른 화면에서 열고 메시지를 보내는** 경로 — `isAxOpen` · `chat.send(...)` · 참고 자료 칩(`ConversationContextReference`)이 말풍선에 어떻게 보이나. 이미 다른 화면에서 서랍을 열며 보내는 사례가 있나(파일:줄)
5. 설정 연동 화면(메일·슬랙·카톡)의 숫자(DB 적재 건수 · 마지막 수집 · 과거 메일 채우는 중 N건)를 어디서 읽나 · `useInboxStream` 을 설정 화면이 구독하나

### SH-IMP-013 ① — 카톡 이름 없는 방

1. 방 목록에서 이름이 없을 때 무엇을 그리나(파일:줄)

## 3. allowed_paths — 이 밖은 건드리지 마라

- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-2/orchestration/work/strong-hajin-enhance/fe-survey-report.md` ← **이 파일 하나만 만든다**

코드 워크트리는 **읽기만** 한다. 커밋·push·PR 금지.

## 4. 하지 말 것

- 코드·테스트·CSS 를 고치지 마라. 테스트·빌드(`cargo`·`npm`)를 돌리지 마라
- **서버·프론트·Tauri 를 띄우지 마라. 사용자 포트와 프로세스를 건드리지 마라** (8001·5176·54329) · 설치된 앱(medi-ax)을 실행하지 마라
- 브라우저를 열지 마라. **운영 서버에 접속하지 마라**
- 「이렇게 바꾸자」를 쓰지 마라
- 리포트에 사람 실명·메일을 쓰지 마라(공개 레포로 아카이브된다) — 「팀원 A」처럼 쓴다

## 5. 리포트 형식

```
# 고도화 조사 (frontend)

## 0. 한 줄 요약 — 항목별 한 줄 (원인이 보이면 원인 한 줄)
## 1~. 항목별 절 — §2 물음 번호대로 답
## N. grep 개수표 — 항목별로 센 심볼과 개수
## N+1. 앱 재현 때 코디가 볼 것 — 014 셸 로그 위치·재현 순서
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
  --subject "frontend 완료: 고도화 조사" \
  --body "리포트 경로 / 항목별 한 줄 요약 / 조사 한계"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_367ca23a-f846-44c0-afc7-07b6655df214 \
  --text "[worker_done] frontend 고도화 조사 완료 — <한 줄 요약>. 리포트 fe-survey-report.md" --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_367ca23a-f846-44c0-afc7-07b6655df214 --text "[질문] frontend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)

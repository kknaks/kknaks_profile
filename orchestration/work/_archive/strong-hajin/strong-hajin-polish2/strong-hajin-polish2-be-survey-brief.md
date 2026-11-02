# [backend] 고도화 2차 — 운영 E2E 요청 5건의 서버 쪽 현재 코드 전수조사

너는 **strong-hajin `backend` 워커**다. **너는 이 작업의 맥락이 없다** — 아래를 먼저 읽어라:

- 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/roles/strong-hajin/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)
- 코드 레포 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish2/AGENTS.md`
- 1차(직전 판) 기록: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/para/projects/summer-star/strong-hajin/30-work/work-008-polish.md`(WORK-008 — 원칙 P-1~P-3, Phase 3b·5 가 이번 요청과 닿는다) · `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/work/_archive/strong-hajin/strong-hajin-polish/be-survey-report.md`(1차 조사 — 출발점, 줄 번호는 옛 값)
- 회고: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/para/projects/summer-star/strong-hajin/log/2026-10-02-strong-hajin-polish.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish2`
base: `origin/main` (`3d47a32` — 1차가 운영에 반영된 코드)

⚠ **같은 워크트리에 frontend 워커가 동시에 탄다.** 둘 다 읽기 전용 조사이고 서로 다른 리포트 파일 하나씩만 쓴다. `backend/` `frontend/` 어느 쪽도 **고치지 마라.** 네 몫은 `backend/` 이지만, 답에 필요하면 반대쪽도 읽어라.

## 0. 이것은 조사다 — 고치지 마라

**읽기 전용 조사다.** 코드를 한 줄도 바꾸지 않는다. 산출물은 리포트 **한 장**뿐이다.
「이렇게 고치면 된다」는 쓰지 마라 — 사용자가 이 리포트를 보고 계약을 정한다. **지금 무엇이 어떻게 도는지만** 적는다.
테스트·빌드를 돌리지 마라. 읽어서 답할 수 있는 것만 답하고, 못 답한 것은 「조사 한계」에 적는다.

## 1. 왜 조사하나

사용자가 운영(`https://ax.medisolveai.xyz`)을 쓰며 요청 다섯을 냈다(E2E-1~5). 사용자는 **전부 논의하고 정하겠다**고 했다.
그 논의의 근거가 이 리포트다. 각 요청이 닿는 코드가 **어디에 몇 군데** 있는지, 지금 **어떻게** 동작하는지를 확정한다.
빠진 자리가 곧 다음 판의 FAIL 이다 — **시작점에서 멈추지 말고, 같은 심볼·패턴을 쓰는 곳을 grep 으로 전부 세어 숫자로 적어라.**

## 2. 요청별 물음

### E2E-1 AX 업무 초안에 체크리스트가 비어 온다
- 사실: 운영에서 「…프로젝트에서 인터뷰 보고서 작성하기 만들어 줘, 명동점 데이터 분석하기 다음 테스크야」 → 초안에 프로젝트·선행 업무는 채워졌고 체크리스트·기한·내용은 비었다. AX 답변: 「기한과 세부 내용은 비워 두었으니 승인 카드에서 보완할 수 있습니다」
- 시작점: `entrypoints/mcp.py` 의 `task_create_self`·업무 요청 도구, `_normalize_ax_draft`, `ActionPresenter._edit_contract`, 라우팅 정책·시스템 프롬프트, 1차 Phase 5 커밋 `33e8f1b`
1. 초안 객체에 체크리스트 필드가 **있나** — 도구 입력 스키마 · 정규화 · 스냅샷 · 편집 계약 · confirm 시 업무 생성 각각에서 체크리스트가 실리는지/버려지는지(파일:줄)
2. AI 에게 필드를 어디까지 채우라고 하나 — 도구 설명·라우팅 정책·프롬프트에서 「대화가 준 것만」「지어내지 말라」「비워 두라」에 해당하는 문장 **전부**(파일:줄, 원문 인용)
3. 생성 명령(`modules/work/creation_commands.py`)이 받는 필드 전체 목록과 초안 객체 필드의 대조표 — 빠진 것·이름이 다른 것
4. 체크리스트 항목을 나중에 넣는 경로(초안 수정·업무 생성 뒤 추가)의 서버 명령

### E2E-2 「수정」 모달의 등록 → 「저장」(초안만 고치고 확정은 카드에서)으로 바꿀 예정
1. 지금 초안을 **확정 없이** 고쳐 저장하는 서버 명령·엔드포인트가 있나(파일:줄). 있으면 회차(revision)·diff 기록이 어떻게 남나
2. confirm + `draft` 경로가 하는 일 전부(회차 증가·diff·업무 생성) — 「저장」과 「확정」을 가르면 이 경로의 어느 부분이 떨어져야 하나를 **지금 코드 기준으로** 적는다(설계는 쓰지 말 것)
3. 초안이 바뀌었을 때 채팅 뷰·판단 대기(`GET /api/action-items`) 응답이 새 값을 주는지 — 채팅 메시지에 초안 스냅샷이 박혀 있나, 매번 현재 초안을 읽나
4. 초안 변경을 알리는 실시간 이벤트(WebSocket 등)가 있나

### E2E-5 업무 날짜 — 시작 예정일 · 실제 시작일 · 실제 종료일 · 마감일 (논의용, 현재 상태만)
1. 업무(`TaskRecord` 등) 의 날짜·시각 컬럼 **전부** — 이름·의미·누가 언제 채우나(생성·시작·완료·재요청·회의 승격 등). 「시작」이 예정일인지 실제 시작인지
2. 상태 전이(시작·완료·막힘·취소…) 때 시각이 이력(이벤트·로그 테이블)에 남나 — 테이블·필드·쓰는 곳(파일:줄)
3. 날짜를 바꾸는 서버 명령 **전부**(기한 변경·기간 변경 등) — 권한 조건 · 결재가 끼나 · 이력이 남나
4. 날짜를 내보내는 API 응답 **전부** — 업무 상세·목록·캘린더·간트/타임라인·홈·보고·AX 도구. 엔드포인트별 어떤 날짜 필드를 주나(표로)
5. SPEC 과의 차이: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/para/projects/summer-star/strong-hajin/20-spec/spec-003-task-lifecycle-v2.md`·`spec-007-task-detail.md`·`spec-004-calendar-scheduling.md` 가 날짜를 어떻게 정의하나 vs 코드

### E2E-3 · E2E-4 — 화면 몫이다. 서버 응답에 「AX 제안에서 생성됨」 출처 정보를 주는 필드만 확인해 한 줄로 적는다

## 3. allowed_paths — 이 밖은 건드리지 마라

- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/work/strong-hajin-polish2/be-survey-report.md` ← **이 파일 하나만 만든다**

코드 워크트리는 **읽기만** 한다. 커밋·push·PR 금지.

## 4. 하지 말 것

- 코드·테스트·CSS 를 고치지 마라
- **서버·프론트를 띄우지 마라. 사용자 포트와 프로세스를 건드리지 마라** (8001·5176·54329)
- 브라우저를 열지 마라. **운영 서버에 접속하지 마라**
- 「이렇게 바꾸자」를 쓰지 마라
- 리포트에 사람 실명·메일을 쓰지 마라(공개 레포로 아카이브된다) — 「팀원 A」처럼 쓴다

## 5. 리포트 형식

```
# 고도화 2차 서버 전수조사

## 0. 한 줄 요약 — 요청별 한 줄 (원인이 보이면 원인 한 줄)
## 1~. 요청별 절 — §2 물음 번호대로 답
## N. grep 개수표 — 요청별로 센 심볼과 개수
## N+1. 조사 한계
```

**모든 답에 `파일:줄` 근거를 단다.** 근거 없는 문장은 쓰지 않는다.

## 6. 검증

- 리포트가 위 경로에 있다. §2 의 물음이 하나도 빠지지 않았다(못 답한 것은 조사 한계에)
- `git -C /Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish2 status --short` 가 비어 있다

## 7. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 코디handle 은 브리프 작성 시점 값이다. preamble 과 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.

- **커밋·push·PR 하지 마라.**
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_b2ea0fd5-1473-4b83-9a04-dcf769fbedba --from term_2cf4fdea-dd6c-411f-b344-41b6d61078de \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: 2차 조사" \
  --body "리포트 경로 / 요청별 한 줄 요약 / 조사 한계"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_b2ea0fd5-1473-4b83-9a04-dcf769fbedba \
  --text "[worker_done] backend 2차 조사 완료 — <한 줄 요약>. 리포트 be-survey-report.md" --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_b2ea0fd5-1473-4b83-9a04-dcf769fbedba --text "[질문] backend: <질문>" --enter`

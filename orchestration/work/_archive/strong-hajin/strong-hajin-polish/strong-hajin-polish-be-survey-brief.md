# [backend] 고도화 1차 — 받은 요청 중 서버에 닿는 것의 현재 코드 전수조사

너는 **strong-hajin `backend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-고도화/orchestration/roles/strong-hajin/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish`
base 브랜치: `origin/main` (015bed2)

⚠ **같은 워크트리에 frontend 워커가 동시에 탄다.** 둘 다 읽기 전용 조사이고 서로 다른 리포트
파일 하나씩만 쓴다. `backend/` `frontend/` 어느 쪽도 **고치지 마라.**

## 0. 이것은 조사다 — 고치지 마라

**읽기 전용 조사다.** 코드를 한 줄도 바꾸지 않는다. 산출물은 리포트 **한 장**뿐이다.
「이렇게 고치면 된다」는 쓰지 마라. **지금 무엇이 어떻게 도는지만** 적는다.
테스트를 돌리지 마라. 읽어서 답할 수 있는 것만 답하고, 못 답한 것은 「조사 한계」에 적는다.

## 1. 왜 조사하나

사용자가 운영을 쓰면서 수정 요청을 냈다. 그중 서버에 닿을 수 있는 셋(A-01 · B-01 · B-02)의
현재 동작을 확정한다. 발주서는 이 리포트를 근거로 쓴다.

## 2. 요청별 물음

**시작점에서 멈추지 말고 grep 으로 넓혀라.** 같은 심볼을 쓰는 곳을 **전부** 세어 숫자로 적는다.

### A-01 AX 제안(초안 action)이 어디에 보이나 (원칙 논의 예정 — 현재 동작만)
- 단서: AX 채팅에서 「업무 만들어 줘」→ 도구 `task_create_self` 가 초안을 만들었고, 그 action 이 홈 「판단 대기」에
  kind `ax.task.create_self`, 문구 「AX가 준비한 변경을 확정할지 결정하세요」로 떴다. 채팅 카드의 action id 와 홈 카드 id 가 같았다
1. AX 도구가 만드는 action(초안)의 모델·테이블·상태 전이 전부(생성·수정·등록(확정)·거절·만료). 파일:줄
2. `ax.*` kind **전부** 목록 — 어느 도구가 무엇을 만드나
3. action item 을 내려 주는 API **전부** — 홈 판단 대기 · 수신함(받은 요청) · 업무 목록 · 채팅 — 각 API 가 어떤 kind·state·수신자 조건으로 거르나. AX 초안이 수신함·업무 목록에 **들어가나 안 들어가나**
4. 홈 카드의 「첫 회차」「○○ 차례」는 무엇으로 계산되나

### B-01 탭 이동 때 화면 깜박임 (서버 쪽 몫만)
1. 사이드 메뉴 주요 화면(홈·내 업무·캘린더·조직·프로젝트·보고·회의)이 진입 때 부르는 목록 API 의 핸들러·서비스·쿼리(파일:줄)
2. 각 API 의 쿼리 수 — N+1 이 보이는 자리, 요청마다 무거운 계산(집계·권한 envelope 계산 등)이 도는 자리
3. 캐시·ETag·Cache-Control 처리 여부
- **실측은 하지 않는다**(서버를 띄우지 않는다). 코드로 보이는 것만

### B-02 새 업무 추가 › 참조자 후보에 팀원 한 명이 빠짐
- 운영 시드는 팀 1개·4명(역할: executive 1 · team-lead 1 · member 2). 로그인한 사람을 빼면 3명이어야 하는데 2명만 나왔다
1. 참조자·결재자·담당자 후보를 내려 주는 API 와 거르는 조건 **전부**(역할·팀·보직·재직·본인 등) — 파일:줄
2. 역할(executive/team-lead/member)이나 소속(보직·추가 소속)에 따라 후보에서 빠질 수 있는 경로
3. 시드 적재 경로(`dataset-import` 등)에서 소속·보직이 어떻게 들어가는지 — 한 명만 다르게 들어갈 수 있는 자리

## 3. allowed_paths — 이 밖은 건드리지 마라

- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-고도화/orchestration/work/strong-hajin-polish/be-survey-report.md` ← **이 파일 하나만 만든다**

코드 워크트리는 **읽기만** 한다. 커밋·push·PR 금지.

## 4. 하지 말 것

- 코드·테스트를 고치지 마라
- **서버·DB 를 띄우지 마라. 사용자 포트와 프로세스를 건드리지 마라** (8001·5176·54329). 로컬 DB 를 조회하지 마라
- 운영 서버·클러스터에 접속하지 마라
- `~/strong-hajin-deploy-data/` 를 열지 마라(운영 인증·시드 dump)
- 「이렇게 바꾸자」를 쓰지 마라
- 리포트에 사람 실명·메일을 쓰지 마라(공개 레포로 아카이브된다)

## 5. 리포트 형식

```
# 고도화 1차 백엔드 전수조사

## 0. 한 줄 요약 — 요청별 한 줄
## 1. A-01   ## 2. B-01   ## 3. B-02   (§2 의 물음 번호대로 답)
## 4. grep 개수표
## 5. 조사 한계
```

**모든 답에 `파일:줄` 근거를 단다.** 근거 없는 문장은 쓰지 않는다.

## 6. 검증

- 리포트가 위 경로에 있다. §2 의 물음이 하나도 빠지지 않았다(못 답한 것은 §5 에)
- `git -C /Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish status --short` 가 비어 있다

## 7. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 코디handle 은 브리프 작성 시점 값이다. preamble 과 다르면 **preamble 이 맞다.**

- **커밋·push·PR 하지 마라.**
- 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_7941dbc9-8078-4818-8d3d-bfd5545cce31 --from <네 워커handle> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "backend 조사 완료: 고도화 1차 A-01·B-01·B-02" \
  --body "리포트 경로 / 요청별 한 줄 요약 / 조사 한계"

# (2) 직접 주입
orca terminal send --terminal term_7941dbc9-8078-4818-8d3d-bfd5545cce31 \
  --text "[worker_done] backend 조사 완료 — <한 줄 요약>. 리포트 be-survey-report.md" --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 물어라:
  `orca terminal send --terminal term_7941dbc9-8078-4818-8d3d-bfd5545cce31 --text "[질문] backend: <질문>" --enter`

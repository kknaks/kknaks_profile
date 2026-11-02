# [frontend] 고도화 1차 — 받은 요청 8건의 현재 코드 전수조사

너는 **strong-hajin `frontend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-고도화/orchestration/roles/strong-hajin/frontend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish`
base 브랜치: `origin/main` (015bed2)

⚠ **같은 워크트리에 backend 워커가 동시에 탄다.** 둘 다 읽기 전용 조사이고 서로 다른 리포트
파일 하나씩만 쓴다. `backend/` `frontend/` 어느 쪽도 **고치지 마라.**

## 0. 이것은 조사다 — 고치지 마라

**읽기 전용 조사다.** 코드를 한 줄도 바꾸지 않는다. 산출물은 리포트 **한 장**뿐이다.
「이렇게 고치면 된다」는 쓰지 마라 — 그건 다음 판(발주)이다. **지금 무엇이 어떻게 돌고 그려지는지만** 적는다.
테스트·빌드를 돌리지 마라. 읽어서 답할 수 있는 것만 답하고, 못 답한 것은 「조사 한계」에 적는다.

## 1. 왜 조사하나

사용자가 운영(`https://ax.medisolveai.xyz`)을 쓰면서 수정 요청 8건을 냈다. 발주서를 쓰기 전에
각 요청이 닿는 코드가 **어디에 몇 군데** 있는지, 지금 **어떻게** 동작하는지를 확정한다.
발주서는 이 리포트를 근거로 쓴다 — 빠진 자리가 곧 다음 판의 FAIL 이다.

## 2. 요청별 물음

각 요청마다 절을 하나씩 뗀다. **시작점은 DOM 클래스다 — 거기서 멈추지 말고 grep 으로 넓혀라.**
클래스·컴포넌트·같은 패턴을 쓰는 곳을 **전부** 세어 숫자로 적는다.

### F-01 업무 상세 › 담당자 변경 폼 → 작은 모달로 바꿀 예정
- 시작점: `.handover`, `.form-stack.link-draft`, id `task-handover-*`, `task-handover-reason-*`, 버튼 「담당자 변경」
1. 이 폼을 그리는 컴포넌트·상태·제출 함수(파일:줄). 어떤 API 를 부르나
2. 같은 「인라인으로 펼치는 폼」(`link-draft` 등) 패턴이 업무 상세 안팎에 **몇 군데** 있나 — 전부 목록
3. 기존 모달 부품(`scax-modal` 등)의 구조. **모달 위에 모달을 띄우는 선례**가 있나(포커스·ESC·오버레이 처리 포함)
4. 작은 크기 모달 변형(size prop 등)이 DS/코드에 있나

### F-02 AX 대화 › 「대화 검색」 입력이 DS 모양이 아니고 Tauri 앱에서 또 다르게 보임
- 시작점: `input.scax-chat__search.search-input-box`, type=search
- 운영 웹 computed: `border: 2px inset`, `border-radius: 0` — 브라우저 기본값으로 보인다
1. `scax-chat__search`·`search-input-box` 의 CSS 정의가 어디 있나. 왜 적용이 안 되나(선택자·로드 순서·누락)
2. `type="search"` 입력과 검색칸 클래스를 쓰는 곳 **전부**. 각각 DS 스타일이 먹는지
3. DS 의 검색 입력 부품(`docs/design/` · 부품 컴포넌트)이 있나, 있다면 어디서 쓰나
4. WebKit(Tauri WebView) 전용 차이를 만들 만한 것(`-webkit-appearance`, `::-webkit-search-*`) 처리 여부

### F-03 프로젝트 상세 › 진행 라인 간트 — 기본 범위를 오늘 기준 W-1~W+3 으로 바꿀 예정
- 시작점: `section.scax-pj-gantt`, `scax-pj-gantt__canvas`, `__axis`, `__day`
1. 표시 날짜 범위를 계산하는 코드(파일:줄)와 지금 규칙(업무 기간만?)
2. 하루 폭(34px)·이름 열(200px)·가로 스크롤·오늘 표시가 어디서 정해지나
3. 같은 범위 계산을 공유하는 다른 화면(내 업무 타임라인 등)이 있나

### D-01 내 업무 › 타임라인 (디자인 논의 예정 — 현재 상태만)
- 시작점: `.timeline.work-timeline`, `calendar-toolbar`, `timeline-grid`, `timeline-bar`
1. 컴포넌트 구조와 범위 규칙(2주 스테퍼), 상태 범례, 막대 배치 계산
2. F-03 간트와 **공유하는 코드**가 있나, 아니면 별도 구현인가

### D-02 AX 대화 › 업무 생성 액션카드 (디자인 논의 예정 — 현재 상태만)
- 시작점: `section.scax-actioncard.action-task-card`, `features/action/`
1. 카드 구조·상태(`data-state`/`data-view` 값 전부)·「수정」「등록」이 하는 일·부르는 API
2. 같은 액션카드 계열(`scax-actioncard`) 종류 **전부** — 업무 생성 외에 무엇이 있나
3. 배지 「SC AX」 문자열이 화면에 나가는 곳 **전부**(배포 때 워드마크를 `MEDISOLVE` 로 바꿨는데 남은 자리)

### A-01 AX 제안(초안 action)이 어디에 보이나 (원칙 논의 예정)
- 단서: 홈 「판단 대기」 카드(`article.task-card`, `data-kind="ax.task.create_self"`, `data-action-item-id`)와 AX 채팅 카드의 `data-action-id` 가 같은 값이었다
1. action item 을 받아 그리는 화면 **전부**(홈·수신함·업무 탭·채팅 등) — 각 화면이 어떤 API·필터(kind·state)로 받나
2. `ax.*` kind 를 따로 다루는 분기가 있나
3. 수신함(받은 요청)과 업무 탭의 분류(칩·탭) 목록과 각 분류의 데이터 출처

### B-01 탭 이동 때 화면 깜박임(스켈레톤 → 응답)
1. 주요 화면(홈·내 업무·캘린더·조직·프로젝트·보고·회의 등 사이드 메뉴 전부)이 데이터를 어떻게 불러오나 — 마운트마다 새로 부르나, 캐시·전역 상태가 있나(파일:줄)
2. 스켈레톤을 띄우는 조건 전부 — 이전 데이터가 있어도 스켈레톤을 띄우나
3. 라우팅 방식과 탭 이동 때 페이지 컴포넌트가 언마운트되는지
4. 화면 하나가 진입 때 부르는 API 개수(직렬·병렬 여부)

### B-02 새 업무 추가 › 참조자 후보에 팀원 한 명이 빠짐
- 시작점: `fieldset.scax-field.cc-picker`, 「새 업무 추가」 모달(`scax-modal--create`, `#create-panel-basic`)
- 운영 시드는 팀 1개·4명(역할: executive 1 · team-lead 1 · member 2). 로그인한 사람을 빼면 3명이어야 하는데 2명만 나왔다
1. 참조자 후보 목록의 출처(API·변수)와 걸러 내는 조건 **전부**(본인·결재자·담당자·역할·팀·재직 등)
2. 결재자 후보 목록의 출처·조건과 참조자 목록의 관계
3. 같은 「사람 고르기」를 하는 다른 자리(담당자 변경 대상 등)와 조건이 같은지

## 3. allowed_paths — 이 밖은 건드리지 마라

- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-고도화/orchestration/work/strong-hajin-polish/fe-survey-report.md` ← **이 파일 하나만 만든다**

코드 워크트리는 **읽기만** 한다. 커밋·push·PR 금지.

## 4. 하지 말 것

- 코드·테스트·CSS 를 고치지 마라
- **서버·프론트를 띄우지 마라. 사용자 포트와 프로세스를 건드리지 마라** (8001·5176·54329)
- 브라우저를 열지 마라. 운영 서버에 접속하지 마라
- 「이렇게 바꾸자」를 쓰지 마라. 조사 리포트에 설계를 섞지 않는다
- 리포트에 사람 실명·메일을 쓰지 마라(공개 레포로 아카이브된다) — 「팀원 A」처럼 쓴다

## 5. 리포트 형식

```
# 고도화 1차 프론트 전수조사

## 0. 한 줄 요약 — 요청별 한 줄
## 1. F-01 … ## 8. B-02   (§2 의 물음 번호대로 답)
## 9. grep 개수표 — 요청별로 센 심볼과 개수
## 10. 조사 한계
```

**모든 답에 `파일:줄` 근거를 단다.** 근거 없는 문장은 쓰지 않는다.

## 6. 검증

- 리포트가 위 경로에 있다. §2 의 물음이 하나도 빠지지 않았다(못 답한 것은 §10 에)
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
  --subject "frontend 조사 완료: 고도화 1차 8건" \
  --body "리포트 경로 / 요청별 한 줄 요약 / 조사 한계"

# (2) 직접 주입
orca terminal send --terminal term_7941dbc9-8078-4818-8d3d-bfd5545cce31 \
  --text "[worker_done] frontend 조사 완료 — <한 줄 요약>. 리포트 fe-survey-report.md" --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 물어라:
  `orca terminal send --terminal term_7941dbc9-8078-4818-8d3d-bfd5545cce31 --text "[질문] frontend: <질문>" --enter`

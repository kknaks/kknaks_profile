# [architect] 설정·수신함 시안 조사 — 외부 채널(Slack·메일·카톡)을 업무로 가져오는 정책의 원료 (read-only)

너는 **strong-hajin `architect` 워커**다. **너는 앞 판의 맥락이 하나도 없다** — 아래 「읽을 것」이 전부다.
먼저 역할 문서를 읽어라 (절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/roles/strong-hajin/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진` — **코디네이터 워크트리다. 코디가 같은 곳에서 일한다. 아래 §5 의 파일 하나 말고는 아무것도 쓰지 마라.**

## 1. SSOT — 먼저 읽을 것

- **Claude Design 프로젝트 `7e839512-977c-4142-b4b5-d992df566ffc`** (TheSC AX Design System) — **확정 시안이 정본이다.** `DesignSync` 도구로 읽는다(너는 사용자 로그인 세션이라 도구가 있다)
  - 설정: `Settings.html` — https://claude.ai/design/p/7e839512-977c-4142-b4b5-d992df566ffc?file=Settings.html
  - 함께 읽을 것: `_ds_bundle.css` · `_ds_bundle.js` (시안이 쓰는 부품·토큰)
  - 수신함: **같은 프로젝트 안, 파일 이름 미확인** — 프로젝트 파일 목록에서 찾아라. 후보가 여럿이면 전부 적어라
- 회고 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/strong-hajin/log/2026-10-05-strong-hajin-polish3.md` §7 — 이 작업이 왜 시작됐나
- 현재 「수신함」이 이미 있다(요청·참조 업무 수신함). 시안의 수신함이 그것과 같은 것인지 다른 것인지 판단 근거:
  - `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/strong-hajin/20-spec/spec-001-work-management.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/strong-hajin/30-work/work-003-inbox-predecessor-and-create-frame.md`
  - 코드(읽기만) `/Users/kknaks/git/toy_pr2/Strong_hajin/frontend/src/shell/InboxRail.tsx` · `/Users/kknaks/git/toy_pr2/Strong_hajin/frontend/src/features/work/requestInbox.ts` · `/Users/kknaks/git/toy_pr2/Strong_hajin/backend/src/ax_workspace/modules/work/requests.py`
- 업무 생성 규칙(외부 메시지 → 업무가 결국 여기로 들어온다): `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/strong-hajin/20-spec/spec-001-work-management.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/strong-hajin/20-spec/spec-007-task-detail.md` · 「AX 초안 = 새 업무 추가를 AI 가 채운 것」(`/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/strong-hajin/30-work/work-008-polish.md`·`work-009-polish2.md` 의 AX 초안 부분)

**기대는 개념** — 해당 없음 (조사 작업).

## 2. 배경 / 무엇을 바꾸나

다음 작업은 **설정 페이지 + 수신함 페이지**, 그리고 외부 채널(**Slack → 메일(회사 Google Workspace) → 카카오톡** 순)을 수집해 업무로 가져오는 것이다.
순서는 **시안 → 정책 확정 → 구현**. 이번 발주는 첫 칸 — **시안이 무엇을 정해 놓았는지 뽑아 정책 논의의 원료를 만드는 것**이다. 정책을 정하지 마라.

사용자가 이미 정한 것(전제로 두고 다시 논의하지 마라):
- 착수 순서는 Slack 먼저
- 카카오톡은 **Tauri 데스크톱 앱(Rust)** 이 켜져 있는 개인 Mac 의 카톡 로컬 DB 를 읽어 가져온다. **서버에는 카톡 연결 정보(복호화 키 · 사용자가 저장한 채팅방 ID)** 를 보관한다
- 시안이 정본 — 시안과 기존 기획이 다르면 고치지 말고 한 줄 차이 목록으로만

## 3. 계약

해당 없음 (조사·보고만).

## 4. 먼저 읽을 핵심 파일

§1 과 같다. 시안부터 읽고, 기존 수신함 코드는 비교할 때만.

## 5. allowed_paths — 이 밖은 건드리지 마라

- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/work/strong-hajin-inbox/design-survey.md` **(새로 만든다 — 이 파일 하나만)**
- 시안 원본을 통째로 이 파일에 붙이지 마라. 필요한 문구·구조만 인용

## 6. 구현 단계

1. DesignSync 로 프로젝트 **파일 목록 전체**를 뽑는다 → 설정·수신함·외부 연동과 관련 있는 파일을 고른다(이름으로 거르지 말고 의심되면 열어 본다)
2. 고른 파일마다 읽고 `design-survey.md` 에 아래 틀로 적는다:
   - **§1 파일 목록** — 전체 목록 + 관련 파일 표시(파일명·한 줄 무엇)
   - **§2 설정 화면** — 영역·탭 구성, 외부 연결 항목(채널별로 무엇을 입력·선택하나: 계정 연결 방식, 채널·방 고르기, 켜기/끄기, 수집 범위·주기, 상태 표시 등), 시안에 있는 문구 그대로
   - **§3 수신함 화면** — 목록 한 행에 뜨는 필드(출처 채널·보낸 사람·본문·시각·방/채널 등), 필터·탭, 한 항목에서 할 수 있는 행동(업무로 만들기·무시·읽음·AX 초안 등)과 그 결과 화면
   - **§4 외부 메시지 → 업무 흐름** — 시안이 보여 주는 대로 단계별로. 시안에 없는 단계는 「시안에 없음」이라고 적는다(메우지 마라)
   - **§5 기존 수신함과의 관계** — 같은 화면을 대체하나·새 화면인가·합쳐지나, 근거(시안 위치·문구)와 함께
   - **§6 기존 기획·코드와 다른 점** — 한 줄씩
   - **§7 정책으로 정해야 할 질문** — 시안이 답하지 않아 사용자가 정해야 하는 것. 채널(Slack·메일·카톡)별로 나눠서. 예: 무엇을 수집 대상으로 삼나 · 메시지 하나 = 업무 하나인가 · 중복·스레드 처리 · 원문 보관 범위 · 누가 보나 — **시안·문서에서 나온 질문만**, 질문마다 근거 위치
3. 각 주장에는 근거(파일명 + 시안 안 위치/문구)를 붙인다

## 7. 범위 제약 — 하지 말 것

- 정책·스펙·WP 를 쓰지 마라. 결정을 내리지 마라 — 질문으로만 남긴다
- 시안(Claude Design)에 **쓰지 마라** — 읽기만
- 코드·문서 레포의 어떤 파일도 고치지 마라. §5 의 파일 하나만
- 외부 API(Slack·Gmail·카톡) 기술 조사는 이번 범위가 아니다
- 커밋·push·PR 금지

## 8. 검증

```
§1~§7 이 모두 채워졌다 · 수신함 시안 파일을 찾았거나 「못 찾음 + 확인한 목록」이 있다 · 모든 주장에 근거 위치 · 시안에 없는 것을 발명하지 않았다
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_6bc57a0a-5025-478d-ae3c-b8ebbfdaa466 --from term_38c0d82e-6e8e-453b-94bc-5c620b56b015 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "architect 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_6bc57a0a-5025-478d-ae3c-b8ebbfdaa466 \
  --text "[worker_done] architect 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_6bc57a0a-5025-478d-ae3c-b8ebbfdaa466 --text "[질문] architect: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)

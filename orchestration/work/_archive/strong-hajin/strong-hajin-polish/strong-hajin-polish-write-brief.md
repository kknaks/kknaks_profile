# [writer] WORK-008 결정을 SPEC 에 반영한다

너는 **strong-hajin `writer` 워커**다. 먼저 역할 문서를 읽어라 (절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-고도화/orchestration/roles/strong-hajin/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 위치: **코디 워크트리에 직접** — `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-고도화`
(문서 워커는 workspace=coordinator. 개별 워크트리 없음)

⚠ 같은 시각 코드 워크트리에서 코드 워커는 돌지 않는다. 이 워크트리의 `orchestration/` 과 `30-work/` 는 코디 것 — 건드리지 마라.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-고도화/para/projects/summer-star/strong-hajin/30-work/work-008-polish.md` ← **이번 결정의 SoT.** 「이 판의 원칙」과 각 Phase 의 「계약」이 반영할 내용이다. **여기 없는 것은 발명하지 마라**
- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-고도화/orchestration/work/strong-hajin-polish/_RESUME.md` §1·§2 — 사용자가 말한 원문과 결정 이력
- 조사 리포트(현재 코드 동작): 같은 폴더 `fe-survey-report.md` · `be-survey-report.md`
- SPEC 들: `…/strong-hajin/20-spec/spec-00{1,2,3,5,7}-*.md` · `20-spec/README.md`

**기대는 개념**: 해당 없음.

## 2. 무엇을 하나

WORK-008 은 사용자와 닫은 결정 여덟 건이다. 그중 **사용자·프론트·QA 에 드러나는 계약이 바뀌는 것**을
그 계약을 소유한 SPEC 에 반영한다. SPEC 에 반영된 뒤 WP 를 고치고 코드를 짠다(문서 → WP → 코드 직렬).

반영 후보 — **각각 「어느 SPEC 의 어느 절이 이 계약을 갖고 있나」를 grep 으로 찾아서** 정한다.
있으면 그 자리를 고치고, 그 계약을 가진 SPEC 이 없으면 **가장 가까운 소유 SPEC 에 새 줄**을 세우고 그 판단을 보고한다.

| 요청 | 반영할 결정 (WORK-008) | 찾을 자리 힌트 — 출발점일 뿐 |
|---|---|---|
| B-02 | 새 업무 추가: 내 업무 담당자 = 본인, 요청 담당자 = 빈칸 시작, 처음엔 두 갈래 모두 참조자 전원, 요청에서 고른 담당자만 참조자에서 동적 제외 | SPEC-001 만들기 창·`cc_member_ids` |
| F-01 | 업무 상세 담당자 변경 = 작은 모달(업무 상세 위) | SPEC-007 「진행과 판단」 · SPEC-001/003 reassign |
| F-03 | 프로젝트 간트 기본 범위 W-1~W+3(월요일 시작 5주), 범위 밖 업무면 넓힘, 오늘 보이게 스크롤 | SPEC-005 §2.4 · D-36 「첫 진입 오늘 기준」 · L-42~L-48 |
| D-01 | 내 업무 타임라인: 범위 = 간트와 같은 규칙, 1주 이동 + 「오늘」, 시작 높이 목록과 맞춤 | 내 업무 화면을 소유한 SPEC(SPEC-003?) · SPEC-001 OQ-K |
| D-02·A-01 | **P-1 AX 초안 = 새 업무 추가를 AI 가 채운 것**(필드·필수·검증 동일) · AX 경로 기한 필수 제거 · 요약 카드(4페이지 읽기 전용) + 「수정」= 새 업무 추가 모달 · 「AX 제안」 칩(내 업무, `ax.task.create_self`·`ax.work_request.create`) · 받은 요청 수신함과 섞지 않음 · 자동 만료 없음 + 만든 시각 | SPEC-002 S-7 · SPEC-001 §1096 근처(AX 제안 편집·필수값) |
| F-02 · B-01 | DS 스타일 · 화면 깜박임 — 계약 변화가 아니면 **반영하지 않는다**. 반영 안 함 판단을 보고에 적는다 | — |

## 3. 규칙

- 각 SPEC 의 기존 형식(결정 ID·근거 열·인수조건 번호·버전·changelog)을 따른다. 버전을 올리고 변경 이력을 남긴다
- 결정의 근거는 「사용자 2026-10-01 (WORK-008)」. **사용자 실명·메일을 쓰지 마라**(공개 레포)
- 기존 SPEC 문장과 **충돌**하면 고친다 — 그리고 무엇과 충돌했는지 보고한다. 예: 「AX 제안은 수신함에 섞지 않는다」는 유지되는 규칙이다(칩은 별도)
- 인수조건(§6 등)이 있는 SPEC 은 바뀐 계약의 인수조건 줄을 함께 고치거나 더한다
- 결정되지 않은 것을 메우지 마라. 애매하면 Open Questions 로 남기고 보고한다
- 린트가 있으면 돌린다(role 문서의 방법대로). 0 ERROR

## 4. allowed_paths

- `para/projects/summer-star/strong-hajin/20-spec/` 의 SPEC 파일과 `20-spec/README.md`
- 그 밖(`30-work/`·`10-decision/`·`orchestration/`·코드 레포)은 **읽기만**

## 5. 하지 말 것

- 커밋·push·PR 금지 · WP(`30-work/`) 수정 금지(코디가 고친다) · 코드 레포 접근 금지(읽기는 조사 리포트로)
- 서버·브라우저 띄우지 마라

## 6. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 코디handle 은 작성 시점 값이다.

```bash
orca orchestration send \
  --to term_7941dbc9-8078-4818-8d3d-bfd5545cce31 --from <네 워커handle> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> --dispatch-id <dispatch context 의 dispatchId> \
  --subject "writer 완료: WORK-008 SPEC 반영" \
  --body "고친 SPEC·절 목록 / 요청별 반영 위치(반영 안 함 포함·사유) / 충돌·고친 문장 / Open Questions / 린트 결과"

orca terminal send --terminal term_7941dbc9-8078-4818-8d3d-bfd5545cce31 \
  --text "[worker_done] writer 완료 — WORK-008 SPEC 반영. 상세는 인박스." --enter
```

막히면: `orca terminal send --terminal term_7941dbc9-8078-4818-8d3d-bfd5545cce31 --text "[질문] writer: <질문>" --enter`

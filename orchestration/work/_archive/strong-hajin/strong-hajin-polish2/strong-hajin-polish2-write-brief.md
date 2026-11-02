# [writer] 고도화 2차 결정(E2E-1~5)을 SPEC 에 반영한다

너는 **strong-hajin `writer` 워커**다. **너는 이 작업의 맥락이 없다** — 먼저 역할 문서를 읽어라 (절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/roles/strong-hajin/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 위치: **코디 워크트리에 직접** — `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3`
(문서 워커는 workspace=coordinator. 개별 워크트리 없음)

⚠ 이 워크트리의 `orchestration/` 과 `30-work/` 는 코디 것 — 건드리지 마라. 같은 시각 코드 워크트리에서 조사 워커가 쉬고 있을 뿐, 코드 변경은 없다.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/work/strong-hajin-polish2/_RESUME.md` §1·§2 ← **이번 결정의 SoT.** §2 의 2026-10-02 행들(E2E-1 ~ E2E-5 ③)이 반영할 내용이다. **여기 없는 것은 발명하지 마라**
- 조사 리포트(지금 코드가 어떻게 도나 — SPEC 문장의 사실 근거): 같은 폴더 `be-survey-report.md`(특히 §1-2 AI 지시문 · §2 초안 명령 · §3 날짜 전부 · §3-5 SPEC 과의 차이) · `fe-survey-report.md`(§2 수정 모달 · §3 채팅 단추 상태 · §4 상세 메타 · §5 날짜 표면)
- 직전 판: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/para/projects/summer-star/strong-hajin/30-work/work-008-polish.md` — 원칙 P-1(AX 초안 = 새 업무 추가를 AI 가 채운 것) · Phase 3b 계약(「수정 모달의 등록 = confirm+draft」 — **이번에 뒤집힌다**)
- SPEC 들: `…/strong-hajin/20-spec/spec-001-work-management.md`(v0.4.0) · `spec-002-action-item-review.md`(v0.3.0) · `spec-003-task-lifecycle-v2.md`(v0.3.2) · `spec-007-task-detail.md`(v0.3.0) · 필요하면 `spec-004-calendar-scheduling.md`·`spec-005-projects.md` · `20-spec/README.md`

**기대는 개념**
- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/para/areas/concept/` 에서 `human-in-the-loop`·`evidence-binding` 노트를 찾아 읽어라 — AX 가 「제안으로 채우되 사람이 검토·확정한다」, 「ID 는 근거가 있을 때만」이 이번 E2E-1 의 판단 기준이다

## 2. 반영할 결정 — 사용자와 닫은 계약

**각 결정이 「어느 SPEC 의 어느 절에 이미 있나」를 grep 으로 전부 찾아** 그 자리를 고친다(같은 계약이 여러 SPEC 에 흩어져 있으면 전부). 없으면 그 계약을 소유한 SPEC 에 새 줄을 세우고 판단을 보고한다. 아래 「자리 힌트」는 출발점일 뿐이다.

| # | 결정 | 자리 힌트 |
|---|---|---|
| E2E-1 | AX 는 업무 생성·요청 초안에 **체크리스트(첫 단계들)·업무 내용을 제안으로 채운다** — 사람이 카드에서 검토하는 초안이기 때문. **ID(프로젝트·업무·사람)·날짜는 지금처럼 대화·조회가 준 것만**(못 찾으면 비우고 말한다, 지어내지 않는다) | SPEC-001 S-9 · SPEC-002 §2.9 · AX 도구·라우팅을 말하는 절 |
| E2E-2 | **「초안 저장」 신설** — AX 초안(`ax.task.create_self`·`ax.work_request.create`)을 **확정 없이** 고쳐 저장한다: 상태 pending 유지 · 회차 +1 · diff 기록(사람이 고친 값). 카드 「수정」→「새 업무 추가」 모달의 하단 단추는 **「저장」**(앱 DS 색 = 파랑 그대로)이고 누르면 저장만 한다. **확정(등록)은 카드 「등록」만** — 마지막 저장 회차를 그대로 confirm. 저장 뒤 카드는 서버의 최신 초안 값을 다시 그린다. 모달 닫기 = 버림(지금처럼). 1차 Phase 3b 「모달 등록 = confirm+draft」 문장은 **뒤집힌다** | SPEC-002 §2.9 · S-7 · §4(confirm 의 고친 초안 예외) · §6 |
| E2E-3 | 채팅 서랍 안의 **사람 행동 단추는 진행 중·disabled·hover 상태까지 검정 계열**(파랑 = AI 진행만, 1차 원칙). 범위는 채팅 서랍 안만 — 서랍 밖 모달(위 「저장」)은 앱 DS | SPEC-002 §2.9(색 원칙이 적힌 자리) |
| E2E-4 | 업무 상세 헤더 메타: 「담당 …」 사실 줄과 「AX 제안에서 생성됨 [링크]」 줄 사이에 DS 간격을 둔다. 링크 문구는 그대로 | SPEC-007 상세 메타(`spec-007:232` 근처) |
| E2E-5 ① | **업무 상세에 날짜 넷**: 순서 **시작 예정일(`start_date`) · 실제 시작일(`started_at`) · 실제 종료일(`completed_at`) · 마감일(`due_date`)**. 시작 예정일·마감일은 지금처럼 상세 「편집」→「변경 저장」으로 고친다. 실제 두 값은 읽기 전용. **목록·캘린더·간트는 지금처럼 시작 예정일~마감일**(바꾸지 않는다) | SPEC-007 상세 메타 · §6 |
| E2E-5 ② | **비어 있는 예정 칸은 실제 값으로 채운다**: 시작 예정일이 없으면 시작 전이 때 실제 시작일로(**지금 동작 유지**, `lifecycle.py:165-171`) · **마감일이 없으면 완료 때 실제 종료일로(신규)** — `completed_at` 이 찍히는 순간(직접 완료 · 요청 업무의 완료 보고 제출). 한 번 채운 값은 보완 요청·재개로 되돌리지 않는다(코디 기본값 — 시작 예정일 동작과 같게) | SPEC-003 전이·시각 절 · SPEC-004 「시작 전이가 시작일을 채운다」(`spec-004:1206`) 와 짝 |
| E2E-5 ③ | 요청 업무의 **실제 종료일 = 완료 보고 제출 시각**(지금 `completed_at` 그대로, 새 데이터 없음) · 기한 라벨을 **「마감일」** 로, 날짜 표시 형식을 **`2026/10/06`** 으로 통일(화면마다 기한·마감일·…마감·희망 기한 / `2026.10.06`·`2026-10-06`·`10월 6일` 이 섞여 있다 — fe-survey §5) · SPEC-001/003 의 **「계획 기한(박제)·실제 기한 두 값(`due_planned`/`due_actual`)」 을 코드에 맞춰 마감일 한 값으로**(담당자가 고친다, 사유 칸 없음 — 지금 코드) | SPEC-001 `:678` `:714` `:736` `:754` `:862-864` `:898` · SPEC-003 `:105` `:326` `:645` `:716` `:746` (be-survey §3-5) |

## 3. 규칙

- 각 SPEC 의 기존 형식(결정 ID·근거 열·인수조건 번호·버전·changelog)을 따른다. 고친 SPEC 마다 버전을 올리고 변경 이력을 남긴다
- 결정의 근거는 「사용자 2026-10-02 (고도화 2차)」. **사용자 실명·메일을 쓰지 마라**(공개 레포)
- 기존 SPEC 문장과 **충돌**하면 고친다 — 무엇과 충돌했는지 보고한다(특히 E2E-2 의 1차 문장, E2E-5 ③ 의 두 값 문장)
- 인수조건(§6 등)이 있는 SPEC 은 바뀐 계약의 인수조건 줄을 함께 고치거나 더한다
- 「마감일」 통일은 **SPEC 이 화면 라벨을 정하는 자리**만 고친다. 서버 필드명(`due_date`)은 바꾸지 않는다
- 결정되지 않은 것을 메우지 마라. 애매하면 Open Questions 로 남기고 보고한다
- 린트가 있으면 돌린다(role 문서의 방법대로). 0 ERROR

## 4. allowed_paths

- `para/projects/summer-star/strong-hajin/20-spec/` 의 SPEC 파일과 `20-spec/README.md`
- 그 밖(`30-work/`·`10-decision/`·`orchestration/`·코드 레포)은 **읽기만**

## 5. 하지 말 것

- 커밋·push·PR 금지 · WP(`30-work/`) 수정 금지(코디가 쓴다) · 코드 레포 수정 금지(읽기는 조사 리포트로, 필요하면 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish2` 를 읽기만)
- 서버·브라우저 띄우지 마라

## 6. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 코디handle 은 작성 시점 값이다. preamble 과 다르면 **preamble 이 맞다.**

```bash
orca orchestration send \
  --to term_b2ea0fd5-1473-4b83-9a04-dcf769fbedba --from term_b2398c0b-255c-4e08-8720-a79a4f839d2b \
  --type worker_done \
  --task-id <dispatch context 의 taskId> --dispatch-id <dispatch context 의 dispatchId> \
  --subject "writer 완료: 고도화 2차 SPEC 반영" \
  --body "고친 SPEC·절·버전 목록 / 결정별 반영 위치 / 충돌·고친 문장 / Open Questions / 린트 결과"

orca terminal send --terminal term_b2ea0fd5-1473-4b83-9a04-dcf769fbedba \
  --text "[worker_done] writer 완료 — 고도화 2차 SPEC 반영. 상세는 인박스." --enter
```

막히면: `orca terminal send --terminal term_b2ea0fd5-1473-4b83-9a04-dcf769fbedba --text "[질문] writer: <질문>" --enter`

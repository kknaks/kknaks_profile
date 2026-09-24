# [frontend] WORK-005 Phase FE-1~FE-3 — 「프로젝트」 화면을 시안대로 다시 그린다

너는 **strong-hajin `frontend` 워커**다. **너는 이 작업의 맥락이 하나도 없다.** 먼저 읽어라:

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/frontend/role.md` (+ 같은 폴더 `rules.md`)
- 코드 레포 `AGENTS.md` (워크트리 루트)
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/30-work/work-005-projects.md` ← **실행 계획. Phase FE-1~FE-3 이 네 몫이다**
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/20-spec/spec-005-projects.md` (1121줄) ← **계약의 SoT**
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/research-fe-structure.md` (500줄) ← **네가 건드릴 자리·살아남는 것·버릴 것이 전부 적혀 있다**
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/design-read-projects.md` ← 시안의 틀·부품·색·기하
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/be-impl-report.md` ← **백엔드가 먼저 끝냈다. 실제로 내려오는 필드를 여기서 확인해라**

**시안 원본** (읽기 전용 — 복사·수정 금지):
`/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/reference/2026-09-10-sc-meeting/package 2/` 의 `Projects.html` · `handoff/projects/**` ·
`handoff/shell/js/scax-ui.jsx` · `handoff/shell/js/work-modal.jsx`

작업 워크트리: **`/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects`**. 문서는 절대경로로 read-only.


⚠ **같은 워크트리에 `backend` 워커가 동시에 붙어 있다.** 그쪽은 `backend/` 만 고친다.
**너는 `frontend/` 만 건드린다.** 백엔드 파일을 열지도 고치지도 마라 — 읽어야 하면
`be-impl-report.md` 를 읽어라(실물 응답이 거기 있다). 커밋·push 금지(둘 다).

## 1-0. 백엔드가 실제로 내려주는 것 — **추측하지 마라**

BE-1·BE-2 가 끝났다. `be-impl-report.md` **§6 에 실물 응답 JSON** 이 찍혀 있다
(추정이 아니라 계약 테스트 하네스에서 찍은 것). **거기를 먼저 읽어라.**

`GET /api/projects/{project_id}` 의 `tasks[]` 한 줄은 이렇게 온다:
`task_id · title · state · start_date · due_date · parent_task_id · preceding_task_ids ·
assignee · checklist_progress{done,total} · span_from · span_to · overdue_days`

**틀리기 쉬운 자리 넷 — BE 가 짚어 준 그대로다:**

1. **`assignee` 는 `null` 이 정상이다.** 「미정」을 서버가 지어내지 않으니 **화면도 지어내지 마라.**
   활성 배정이 없으면 **답을 기다리는 사람**이 거기 선다
2. **`checklist_progress.total == 0` 은 0% 가 아니다.** **fill 도 % 도 그리지 않는다**(D-02).
   0% 막대를 그리면 「아무것도 안 한 일」이라는 거짓이 된다
3. **`span_*` 은 이미 접혀서 온다** — 마감만 있으면 그 날 하루, 뒤집힌 기간은 `[min,max]`.
   **간트 막대는 `span_*` 을 쓴다.** `start_date`·`due_date` 원값도 함께 오지만 그건 표시용이다
4. **`overdue_days` 는 끝난 업무에 안 온다**(완료·취소·승인 대기).
   **「지연」 칸은 값이 온 업무만 센다** — 화면이 「오늘」을 다시 판정하지 마라

**`state` 는 계약의 넷뿐이다**(`open`·`in_progress`·`done`·`cancelled`).
`completion_submitted` 는 서버가 `done` 으로 접어 보낸다. **`blocked` 는 들어올 수 있다** —
M-6 통과값이라 계약 넷에는 없지만 값은 온다. 오면 `labels.ts` 의 **「막힘 / danger」**로 그리고
간트 바는 `--blocked` 규격을 쓴다. **모르는 값이라고 떨어뜨리지 마라.**

## 1. 무엇을 만드나 — **거의 다시 그린다** (사용자 지시)

지금 화면은 **본문 한 칸의 2컬럼 관리 화면**이고 시안은 **3레일 + 간트 + 의존선**이다. 같은 화면이 아니다.

### FE-1 — 틀과 좌 레일
`onRegisterRails` 로 3레일에 올린다 (선례 `MyWorkPage.tsx:941-972` · `CalendarPage.tsx:460-477`).
좌 레일 = 「업무」 헤더 + 건수 배지 + 프로젝트 `Select`(알약 트리거 — 선례 `MyWorkPage.tsx:1410`) +
**기존 `scax-inbox-card` 재사용**(`ScheduleCard.tsx:42-99` 가 사실상 같은 조립이다) + **선택 상태 CSS**.
본문에 요약 스트립 5칸.

### FE-2 — 간트와 의존선 ← **이 판의 가장 어려운 자리**
- **깊이 제한 없는 재귀 트리**다. twisty 는 자식이 있는 **모든 깊이**에 선다
- **접힌 가지에 걸린 의존선은 접힌 부모 바에 끌어붙인다.** 시안 `DepLines` 의
  `if (!a || !b) return`(`projects.v1.jsx:85-106`)을 **그대로 쓰면 선이 조용히 사라진다.**
  **이것이 이 화면의 핵심 인수조건이다** — 사라지는 선이 하나도 없어야 한다
- 들여쓰기는 **깊이당 12px · 최대 5단**. 나머지 기하(행 40 · 하루 34 · 라벨 200 · 바 22/14/18)는 시안 그대로
- 진행률은 **체크리스트 기반**. 체크리스트가 없으면 **% 를 안 그린다**(0% 로 그리지 마라).
  상위 바는 % 를 안 낸다. `cancelled` 는 배경 `fill-weak`·fill 없음·제목 취소선

### FE-3 — 우 레일 · 관리 모달 · 빈 상태
- 우 레일: 메타 · 관계(**후행은 `preceding_task_ids` 를 뒤집어 만든다**) · 체크리스트(읽기) · 하위 업무
- **관리 모달 — 시안이 없다. 자율로 만든다(사용자 위임).**
  지금 `ProjectPage.tsx:206-306` 의 참여자 붙이기/떼기 · 참여 이력 · 새 프로젝트를
  **시안 `work-modal.jsx` 의 어휘**(`Modal`·`Field`·`TextField`·`AutoComplete`)로 옮긴다.
  **새로 발명하지 마라 — 있는 기능을 옮기는 것이다.** 손잡이는 `AppHeader` 의 `actions`
- 빈 상태: 프로젝트 0개 → 「담당 프로젝트가 없습니다」 하나. 업무 미선택 → 우 레일 `Empty`
- **기존 테스트 6개 단언 교체**(`ProjectPage.test.tsx:89-178`) — 관리 UI 단언은 모달을 겨누게 옮긴다

## 2. ⚠ 공유 자산 — 건드리면 다른 화면이 흔들린다

`research-fe-structure.md` §4-3 이 전수 조사해 뒀다. 특히:

- **`.scax-inbox-card` 선택 CSS 는 `[role="button"]` 으로 좁혀라** — 수신함·캘린더 카드에는
  `role` 이 없어서 안 걸린다. 무조건 규칙으로 쓰면 그 둘에 새 CSS 가 얹힌다
- **`Empty` 를 고치지 마라** (20px 유지 — 소비처 29곳)
- **`AppHeader` 에 `titleEnd` 를 더하지 마라** (5개 화면 공유)
- **`.screens-b-lead` 를 건드리지 마라** — 조직·관계탐색·보고가 함께 쓰고 `OrgPage.test.tsx:249` 가 검사한다
- **`.project-layout` 반응형 줄**(`components.css:692`)은 홈·보고와 같은 규칙에 묶여 있다
- **`listProjects`** 는 업무 만들기 모달(`WorkModals.tsx:3672`)도 쓴다
- **`ProgressBar`** 에 `percent` 입력을 더하면 소비처 1곳(`WorkModals.tsx:1590`)과 함께 움직인다
- 화면 전용 CSS 는 **새 파일 한 장**으로 두고 `src/styles/index.css` 에 `@import` 한 줄 (선례 `calendar.css`)
- **`src/ds/GutterList.tsx` 는 이름만 같은 다른 부품이다**(소비처 0건). 시안의 `.scax-gutter-list` 는
  마크업으로 쓴다 (선례 `InboxRail.tsx:103-114` · `ScheduleRail.tsx:81-108`)

## 3. 검증

- `make frontend-test` + `frontend` 에서 `npx tsc --noEmit`. 최종 빌드는 코디가 돌린다
- **같은 검증을 중복 실행하지 마라**
- **첨부(material) 관련 테스트는 범위 밖이다**
- **브라우저 E2E 는 내일 사용자가 한다** — 개발 서버를 띄우지 마라. 사용자 포트·프로세스 금지
- envelope 으로 권한 판단, **`api.ts` 밖에서 fetch 금지**, 기존 부품·viewModel 재사용
- 시안에 없는 자리는 **DS-gaps 로 기록**한다

## 4. allowed_paths

- `frontend/` 만
- **커밋·push·PR 금지.** 리포트는 `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/fe-impl-report.md` 하나
- 시안 폴더는 **읽기 전용**이다

## 5. 리포트

- 바꾼/만든 파일과 **각각이 닫는 인수조건 번호**
- **공유 자산을 건드린 자리**(있다면)와 그 영향 범위
- 테스트 수치(전/후) · tsc 결과
- **DS-gaps** · 막힌 것

## 6. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 과 아래가 다르면 **preamble 이 맞다.**

```bash
orca orchestration send \
  --to term_bdba055b-758b-4dc9-85c3-7836d56b615a --from term_7f9b463c-1c0e-4cf6-8e8d-0e7ccd5a7c93 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch context 에 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch context 에 있다> \
  --subject "frontend 완료: WORK-005 FE-1~FE-3" \
  --body "바꾼 파일 / 닫은 인수조건 / 공유 자산 영향 / 테스트·tsc 수치 / DS-gaps / 막힌 것"

orca terminal send --terminal term_bdba055b-758b-4dc9-85c3-7836d56b615a \
  --text "[worker_done] frontend 완료 — FE-1~FE-3. 상세는 인박스." --enter
```

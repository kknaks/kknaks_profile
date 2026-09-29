# [frontend] WORK-007 Phase F-1 · F-2 · F-3 — 업무 상세 재설계 화면

너는 **strong-hajin `frontend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-디자인/orchestration/roles/strong-hajin/frontend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-design`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

⚠ **backend 워커가 같은 워크트리의 `backend/` 에서 지금 «동시에» 일한다.**
`backend/` 를 한 줄도 건드리지 마라 — 읽기만 해라. 너는 `frontend/` 만이다.
서버 계약은 **이미 구현돼 있다**(아래 §3). 고치는 것은 누출·테스트뿐이라 계약 모양은 안 바뀐다.

## 1. SSOT — **여기 없는 건 발명하지 마라**

- `.../para/projects/summer-star/strong-hajin/20-spec/spec-007-task-detail.md` ← **계약의 SoT (v0.2.0)**
- `.../para/projects/summer-star/strong-hajin/30-work/work-007-task-detail.md` ← **네 단계** Phase F-1(:342) · F-2(:379) · F-3(:416)
- `.../10-decision/decision-006-task-detail.md` — 왜 이렇게 정했나
- `.../orchestration/work/strong-hajin-design/fe-survey-report.md` — 네가 지난 판에 쓴 조사
- `.../orchestration/work/strong-hajin-design/be-report.md` — 서버가 **실제로** 무엇을 내는지

### 확정 시안 — **이것이 화면의 정본이다**

```
/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-디자인/reference/2026-09-10-sc-meeting/package 2/TaskDetail.html
```

A(기본) · B(시작 막힘) · C(연결 편집) 세 상태가 들어 있다. **시안과 다르게 만들지 마라.**
시안에 없는 것이 필요하면 DS-gaps 에 적고 코디에게 묻는다.

## 2. 무엇을 만드나 — WORK-007 의 FE 셋

```
Phase F-1  여섯 덩어리 재구성과 «선행 배선 복구»     work-007:342
Phase F-2  연관 업무 2열 여섯 칸과 막힘 배너          work-007:379
Phase F-3  연결 편집                                   work-007:416
```

**WORK-007 이 단계마다 Acceptance 와 Covers(spec 절번호)를 달았다. 그것이 완료 조건이다.**

### 덩어리 여섯

```
업무 메타      제목·상태·담당·기한·시작·결재·참조 한 줄 + AX 단추(오른쪽)
업무 정보      1열 — 업무 내용 → 체크리스트
연관 업무      2열 — 상위|프로젝트 · 하위|선행 · 참고|후행
자료           2열 — 참고 자료 | 결과 자료   («산출물» 표기를 바꾼다. 이 화면만)
진행과 판단    완료 보고 · 승인/반려 · 취소 제안 · 조건 변경 · 담당 변경
이력           활동 이력
```

목록은 **3행 기본 + 칸 안 스크롤**, 머리(제목·셈·단추)는 스크롤 밖 고정.

### F-1 의 핵심 — 선행 배선 복구

**이것이 이 판에서 제일 중요한 한 줄이다.** 지금 상세 조회 effect 가
`checklist`·`references`·`delivery`·`children`·`parent` **다섯만** 채우고 `predecessors` 를 버린다.
그리는 쪽은 `task` prop 을 읽는데 목록에서 열면 그것이 목록 투영이라 선행이 없다.
**그래서 선행 구획과 시작 게이트가 통째로 안 선다.** 새로 온 `successors` 도 같은 함정에 빠진다.

## 3. 서버가 내는 것 — 이미 구현됐다

- 상세 응답에 `successors`(`task_id`·`title`·`state`·`version`) + `hidden_successor_count`
- **못 읽는 후행은 배열에 자리도 `task_id` 도 없다.** 건수로만 온다
- **못 읽는 선행도 건수만이고 «미완»으로 센다**
- `read_only` 갈래에도 후행이 실린다 — 해제 단추만 없다
- 상위 변경: `PATCH /api/tasks/{id}` 에 `parent_task_id` · `clear_parent`
  - 둘을 함께 보내면 **422**
  - **`parent_task_id` 와 `project_id` 를 한 PATCH 에 함께 보내면 422** — 갈라서 보내라
- 후행 해제: `DELETE /api/tasks/{id}/successors/{successor_id}?expected_version=`
  - 멱등이 아니다. 두 번째는 **404**(동시 해제의 늦은 쪽)
  - B 의 회차만 오른다. A 는 안 움직인다
- 거절은 `detail` **문장 하나**로 온다. 기계용 `code` 가 없다 — **문장을 그대로 보여줘라**

## 4. 사용자가 확정한 것 — 다시 묻지 마라

1. **유효성은 서버가 판정한다.** 화면이 미리 막지 마라. 다 고를 수 있게 두고 거절을 받아 그 칸 아래에 보여준다
   - 예외 둘만 화면이 거른다: **자기 자신** · **이미 걸린 항목**
2. 연결 편집 칸별 조작
   | 칸 | 조작 |
   |---|---|
   | 상위 업무 · 프로젝트 | 셀렉터 (「없음」 포함) |
   | 하위 · 선행 · 참고 | 기존에 **해제** · 아래에 **추가** 셀렉터 |
   | 후행 | **해제**만 |
3. **「추가」는 글자로 쓰고 파란색.** 셀렉터만 두면 추가인지 모른다
4. **비공개 후행은 해제 단추를 주지 않는다**
5. **저장은 칸마다 따로.** 한 칸이 거절돼도 나머지는 남는다. 거절된 칸만 되돌리고 그 칸에 오류를 보여준다
6. **선행은 시작을 막고 하위는 완료를 막는다.** 문구를 갈라 써라. 한 낱말로 뭉개지 마라
7. **못 읽는 선행만 남았을 때 [시작] 을 막지 않는다** (OQ-709) — 단추를 열고 409 를 정상 응답으로 받는다.
   서버가 열어 줄 업무를 화면이 잠그면 안 된다
8. 「편집」 단추는 **A(기본)에만**. B·C 엔 없다

## 5. 전수조사 — 목록으로 끝내지 마라

브리프가 준 것은 **시작점**이다. 손대는 표면을 **전부 grep 으로 세고 시작해라.**

```
predecessors  successors  hidden_successor_count  blockingPredecessors
visiblePredecessors  hiddenPredecessors  startBlockedByPredecessors
parent_task_id  clear_parent  project_id  TaskPatch
drawer-section  section-row  material-list
```

**서랍의 구획을 위에서 아래로 전부 세고 시작해라** — 여섯 덩어리로 재배치하는 판이라 빠뜨리면
있던 기능이 사라진다. 네 조사 리포트 §4 에 그 목록이 있다.

## 6. 같이 고칠 것 — 디자인 항목 둘

시안이 이미 고쳐 놓은 CSS 버그다. 앱 CSS 에 옮겨라.

```css
/* .section-row 가 자식 셋 이상이면 단추 하나가 가운데 뜬다 (components.css:551 space-between) */
.section-row{justify-content:flex-start}
.section-row > h4{margin-right:auto}

/* 목록 첫 칸의 버튼이 칸을 꽉 채워 제목이 가운데로 간다 */
.material-list li > .scax-button--inline{justify-content:flex-start;text-align:left}
```

**쓰는 자리를 전부 grep 으로 확인하고 고쳐라** — `.section-row` 는 `WorkModals.tsx` 5곳 ·
`RelationGraphPage.tsx` 1곳이다. 다른 화면이 깨지지 않는지 확인해라.

## 7. allowed_paths

- `frontend/`
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-디자인/orchestration/work/strong-hajin-design/fe-report.md`

**`backend/` 금지** (다른 워커가 쓰고 있다). 문서 경로 금지.

## 8. 하지 말 것

- 시안과 다르게 만들지 마라 — 필요하면 DS-gaps 에 적고 묻는다
- 화면이 유효성을 선제로 판정하지 마라 (§4-1)
- 알림 UI 를 만들지 마라 (범위 밖)
- `api.ts` 밖에서 fetch 하지 마라
- 기존 부품·viewModels 를 재사용해라. 새 DS 부품을 만들지 마라
- WORK-007 에 없는 단계를 하지 마라
- **서버·프론트를 띄우지 마라. 사용자 포트·프로세스 금지** — `8001`·`5176`·`54329` 가 떠 있다
- 커밋·push·PR 금지

## 9. 검증

```
코드 레포 AGENTS.md 준수: make frontend-test 및 frontend에서 npx tsc --noEmit, 최종 빌드는 make frontend-build 또는 코디의 make verify. 같은 검증 중복 실행 금지. envelope으로 권한 판단, api.ts 밖 fetch 금지, 기존 부품/viewModels 재사용, 시안 부재는 DS-gaps 기록.
```

- 전체 프론트 스위트는 **시간 의존 불안정**이 알려져 있다(2026-09-24 회고). 간헐 실패는
  **기준선과 분리해서** 보고해라 — 네 변경 탓으로 꾸미지도, 무시하지도 마라
- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다

## 10. 리포트

`.../orchestration/work/strong-hajin-design/fe-report.md`

```
## 0. 한 줄 요약
## 1. 표면 전수조사 결과 (§5 심볼별 건수와 처분 · 구획 이사표)
## 2. Phase 별 구현 — F-1 · F-2 · F-3. 각각 변경 파일:줄 · Acceptance 충족 근거
## 3. 시안 대조 — A·B·C 각각 무엇이 어떻게 섰나
## 4. 검증 결과 — 명령과 «수치»
## 5. DS-gaps (시안에 없어서 판단한 것)
## 6. 기준선 실패 (무관한 기존 실패 · 간헐 실패)
## 7. 미결·주의점
```

## 11. 완료 보고 — **문구 변경 금지**

- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다.

```bash
orca orchestration send \
  --to term_e622370a-1f3b-4861-b759-daa3584eace0 --from <네 워커handle> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "frontend F-1·F-2·F-3 완료: <한 줄>" \
  --body "변경 파일 목록 / Phase별 요약 / 검증 결과(수치) / 시안 대조 / DS-gaps / 미결"

orca terminal send --terminal term_e622370a-1f3b-4861-b759-daa3584eace0 \
  --text "[worker_done] frontend F-1·F-2·F-3 완료 — <한 줄>" --enter
```

막히면: `orca terminal send --terminal term_e622370a-1f3b-4861-b759-daa3584eace0 --text "[질문] frontend: <질문>" --enter`

# 루프 2 조사 — 구현 전에 답이 있어야 하는 다섯

**read-only 조사다.** 코드·문서 **한 줄도 고치지 마라.** 테스트·서버·개발서버 **실행 금지.**
**쓰는 파일은 하나**: `orchestration/work/strong-hajin-projects/loop2-survey-report.md`

## 배경

「프로젝트」 화면 1루프가 끝났고(SPEC-005·WORK-005 · BE·FE 구현·검수 완료, **커밋 0건**),
사용자가 브라우저 E2E 1차를 돌려 **수정 지시 9건 + 권한 결정 1건**을 냈다.
그 목록의 정본은 **`loop2-backlog.md`** 다 — **먼저 그것을 읽어라.**

**이번 조사는 그중 「모르면 구현이 헛돌 자리」 다섯만** 답한다. 나머지(B-2·B-4·B-5·B-6·B-7 순서)는
CSS·배치라 조사 없이 간다.

## 답할 것 — 다섯. **각 답에 `파일:줄` 근거를 달아라**

### Q1. B-3 틀고정이 **지금 구조에서 되는가** ← 가장 위험하다

간트 라벨 칸(업무 이름·담당, 200px)이 **가로 스크롤에 고정**되어야 한다.

- 지금 DOM: `.scax-pj-gantt__scroll`(overflow-x) > `.scax-pj-gantt__canvas` >
  `.scax-pj-gantt__plot` > `.scax-pj-gantt__row`(**`position: absolute`**) > `.scax-pj-gantt__name-cell`
- **`position: sticky; left: 0` 이 `absolute` 행 안에서 먹는가?** 안 먹으면 왜인가
- 안 되면 **무엇을 바꿔야 하나** — 행을 `absolute` 에서 빼야 하나, 아니면 **고정 칸과 스크롤
  캔버스를 두 열로 갈라야** 하나. **갈라야 하면 무엇이 깨지나**(의존선 SVG 좌표계 · `anchorIndex()` ·
  행 `top` 계산 · 접힘)
- **범위를 말해 달라**: CSS 몇 줄이면 되는 일인가, 간트를 다시 조립하는 일인가

### Q2. B-8 의 **허용 전이를 어디서 얻는가**

우 레일 메타 정보의 「상태」를 **내 업무면** 드롭다운으로 바꾼다(액션 버튼은 안 옮긴다).

- 업무 화면은 `transitions` 로 드롭다운 목록을 만든다 — **그 값이 어디서 오나**
  (`MyWorkPage.tsx:1383-1416` 주변에서 `transitions` 의 출처를 따라가라)
- **프로젝트 상세 `tasks[]` 에는 `state` 만 온다**(`project_results.py:48-70`) → 선택지 둘 중 어느 쪽인가:
  ⓐ 프로젝트 상세를 넓힌다 / ⓑ 우 레일이 선택한 업무만 **업무 상세를 따로 부른다**
- **「내 업무」 판정을 화면이 무엇으로 하나** — `assignee.member_id` 와 로그인 사용자 비교로 되나,
  아니면 `derived` 같은 서버 판정이 필요한가. **업무 화면은 무엇으로 하나**
- **완료 보고 모달 경로를 재사용할 수 있나** — `CompletionReportModal` 이 프로젝트 화면에서도
  열릴 수 있는 부품인가(의존·prop 확인). 요청 업무의 「완료」는 그 경로로 가야 한다

### Q3. B-7·B-9 의 **설명·체크리스트를 어떻게 가져오나**

- **확인된 사실**: `ProjectTaskView` 에 `description` 없음 · 체크리스트 **항목** 없음(개수만).
  그래서 **지금 우 레일 체크리스트는 언제나 「등록된 항목이 없습니다」** 다 — **그것을 실제로 확인하라**
  (`ProjectTaskPanel` 이 무엇을 읽고 그 블록을 그리는지)
- 선택지 둘의 **비용을 재라**: ⓐ `tasks[]` 확장(업무 수 × 체크리스트 항목 수만큼 응답이 커진다 —
  지금 데모로 실제 크기를 계산해 보라) / ⓑ 선택 업무만 `getTask`(우 레일은 한 번에 한 업무라
  N+1 이 아니다. 호출 지연·깜빡임은?)
- ⚠ `checklist` 는 업무 상세에서도 **`NotRequired`** 다 — `access == "read_only"` 면 안 실린다
  (`application.py:920-930`). **남의 업무를 볼 때 무엇이 오나**
- `description` 은 업무 상세에 오는가

### Q4. B-1 「다른 탭 페이지처럼」이 **무슨 방식인가**

- **다른 화면들이 `AppHeader` 의 `actions` 를 어떻게 등록하나** — 선례를 전수로 찾아라
  (`surfaceActions`, `App.tsx:127` 근처). 프로젝트 화면은 지금 **등록하지 않는다**
- **`POST /api/projects` 가 실제로 받는 필드** — 필수/선택/검증·오류.
  `projects` 표의 `name`·`description`·`starts_on`·`ends_on`·`external_key`(unique) 중
  **API 가 받는 것은 무엇이고 무엇을 거절하나**
- ⚠ **관리 모달 안에 이미 「새 프로젝트」 생성 폼이 있다**(1루프에서 옮긴 것).
  **헤더 버튼과 그것이 둘 다 있으면 안 되는지**, 아니면 헤더 버튼이 그 모달을 여는 것인지 —
  지금 코드가 무엇을 하고 있는지 보고 **선택지를 제시하라**(결정은 코디·사용자가 한다)

### Q5. A-1 **권한 게이트를 빼면 무엇이 함께 움직이나**

자동 초대에서 `may_assign_in` 게이트를 **제거**한다(붙는 kind 는 `member` 그대로).

- 그 게이트를 읽는 자리를 **전부 grep 으로 세어라** — 자동 초대 말고 **다른 곳에서도 쓰는가**
- **깨지는 테스트를 미리 세어라** — `test_the_key_is_assigning_in_that_project_not_managing_it` 처럼
  그 게이트를 증명하는 테스트가 몇 개이고 각각 무엇을 주장하나
- **SPEC-005·WORK-005 에서 고쳐야 할 줄**을 찾아 목록으로 (인수조건 번호까지)
- **DEC-004 D-12** 가 그 결정이다 — 뒤집을 때 함께 손봐야 할 관련 결정(D-11·D-13~D-15)이 있나

## 하지 말 것

- **설계하지 마라.** 「이렇게 만들면 된다」가 아니라 **「지금 이렇고, 선택지는 이것들이고, 각각의
  비용은 이렇다」**까지다. 결정은 코디·사용자가 한다
- 코드·문서·테스트 **수정 0건.** 커밋·push 금지
- **테스트를 돌리지 마라** — Phase 0 후속 워커가 같은 워크트리에서 측정 중이다. 부하를 만들지 마라
- 서버·개발서버·`reset-demo` 금지

## 검증

- 다섯 질문에 **전부** 답이 있다. **모르면 「못 찾았다 + 이렇게 찾아봤다」**로 적어라
- 모든 답에 **`파일:줄`** 근거
- Q1 은 **범위 판정**(CSS 몇 줄 ↔ 재조립)이 결론에 있어야 한다
- Q3·Q4 는 **선택지별 비용**이 수치나 사실로 적혀 있어야 한다

## 역할·맥락

너는 **strong-hajin `reviewer` 워커**다(read-only 조사라 이 역할로 간다). 먼저 읽어라:
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/reviewer/role.md` (+ 같은 폴더 `.md`)
- `loop2-backlog.md` ← **지시 목록의 정본**
- `research-fe-structure.md`(500줄, 1루프 조사 · 공유 자산 지도) · `be-impl-report.md` §6(실물 응답)
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/20-spec/spec-005-projects.md`

코드: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects` (**read-only**)

## 완료 보고 — **문구 변경 금지**

```bash
orca orchestration send \
  --to term_bdba055b-758b-4dc9-85c3-7836d56b615a --from term_33092a23-5b29-4b19-bd96-1b365ed4eb1f \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "reviewer 완료: 루프 2 조사" \
  --body "Q1 범위 판정 / Q2 전이 출처 / Q3 선택지 비용 / Q4 선례와 중복 / Q5 깨지는 테스트 수 / git status"

orca terminal send --terminal term_bdba055b-758b-4dc9-85c3-7836d56b615a \
  --text "[worker_done] reviewer 완료 — 루프 2 조사. 상세는 인박스." --enter
```

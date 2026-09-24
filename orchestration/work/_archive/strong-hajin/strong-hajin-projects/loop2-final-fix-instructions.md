# 루프2 최종 수정 — 사용자 지시 둘 + 검수 FAIL 1 · WARN 6

**allowed_paths**: `frontend/` 만. **`backend/` 0줄.** 커밋·push 금지.
**개발 서버 금지** — `5173`·`8100` 은 **사용자가 지금 보고 있는 E2E 스택**이다.

**읽을 것**: `review-loop2-fe5-report.md`(검수 전문) · `loop2-fe5-report.md`(앞 판) ·
`spec-005-projects.md` v0.2.0 · `.../roles/strong-hajin/frontend/role.md` · 코드 레포 `AGENTS.md`

---

## A. 사용자 지시 둘 — **이것이 우선이다**

### A-1. 셀렉터 글자가 잘린다 (화면에서 확인됨)

**증상**: 레일 머리의 프로젝트 셀렉터가 「하반기 제**풀**」처럼 **글자 중간에서 잘린다.**
말줄임표도 없다. **프로젝트 이름을 읽을 수 없다.**

**원인**: `projects.css:34`
```css
.scax-pj-rail__project{flex:0 1 auto;max-width:60%;min-width:0}
```
레일이 380px 인데 60% = **228px**. 거기서 폴더 아이콘(14)·chevron(12)·좌우 패딩을 빼면
글자에 150px 남짓만 남는다. 게다가 **`text-overflow: ellipsis` 가 없다.**

**고칠 방향** (코디 판단): **제목 쪽을 고정으로 두고 셀렉터가 남는 폭을 다 쓰게** 한다.
제목(「프로젝트」+배지)은 길이가 고정인데 **프로젝트 이름은 가변**이므로 남는 공간을 이름이 가져가야 한다.
- 셀렉터를 `flex:1 1 auto` 로 하고 **`max-width` 제약을 걷어낸다**(또는 훨씬 키운다)
- **`text-overflow: ellipsis`** 를 넣어 **정말 긴 이름은 말줄임표로** 끝나게 한다
- 제목 쪽(`.scax-gutter-list__title`)이 **안 줄어들게** 한다
- ⚠ **32px 헤더 높이를 넘지 마라.** 앞 판이 그 제약을 적어 뒀다
- **아주 긴 이름과 아주 짧은 이름 둘 다** 테스트로 재라

### A-2. 「프로젝트 추가」는 **모든 사람에게 뜬다** — 게이트를 없앤다

**사용자 확정**: 「추가는 **모든 사람이 할 수 있다**」.

지금은 `project.manage` 역량이 있어야 뜬다(`App.tsx` 가 `canCreateProjects` 를 내리고
`ProjectPage` 가 그것으로 가른다). **그 게이트를 없앤다 — 버튼은 항상 선다.**

- `App.tsx` 에서 내리던 **`canCreateProjects` 배선을 걷어낸다**(다른 prop 은 그대로)
- `ProjectPage` 에서 그 값으로 가르던 분기를 **없앤다**. 빈 상태 갈래에서도 그대로 선다
- ⚠ **「프로젝트 관리」 버튼의 `may_manage` 게이트는 그대로 둔다** — 그건 다른 판정이다
- ⚠ **서버가 거절하면 화면이 말해야 한다** — 역량 없는 사람이 만들려 하면 생성 API 가 거절한다.
  그 거절을 **모달 안에서 문구로** 보여라(A-1 과 별개로 이미 거절 네 갈래를 말하게 돼 있다)
- **관련 인수조건(L-14~L-17 계열)이 「역량이 있어야 뜬다」를 재고 있으면 그 테스트도 고쳐라** —
  **삭제·skip 하지 말고 새 계약을 재게 다시 써라**
- ⚠ **문서(SPEC·DEC)는 코디가 고친다. 너는 코드와 테스트만.** 무엇을 고쳤는지 리포트에 적어라

---

## B. 검수 FAIL 1 — **반드시**

### FAIL-1. 완료 보고가 거절되면 화면이 아무 말도 안 한다

`ProjectTaskPanel.tsx:359` 가 완료 보고 모달에 **`onError={() => undefined}`** 를 넘긴다.
그 모달은 **자기 안에 오류를 안 그리고** `WorkModals.tsx:2270` 의 `catch` 가 **`onError` 로만 말한다.**
→ 검수 probe 실측: **서버가 거절해도 `document.body` 어디에도 문구가 없다.** 모달만 열린 채 멈춘다.

**선례가 답이다** — `MyWorkPage.tsx:1115-1116` 은 `onError`·`onNotice` 를 **그대로 넘긴다.**
D-32(「업무 화면 로직 그대로」) 위반이다. **고칠 곳은 prop 두 줄.**

⚠ 이 자리는 **실제로 자주 걸린다** — 완료 거절 갈래가 넷이다(끝나지 않은 **선행업무** ·
끝나지 않은 **하위 업무** · **요청 업무는 완료 보고 필요** · **회차 불일치**).
**사용자가 왜 안 되는지 모르는 상태가 된다.**

**고친 뒤 「거절되면 문구가 보인다」를 재는 테스트를 더해라.**

---

## C. 검수 WARN 여섯

- **WARN-1** — 앞 판이 「관문 **아**(보내는 중 잠금)는 흔들리는 테스트가 된다」고 적었는데 **거짓이다.**
  검수가 **지연 promise + `waitFor`** 로 결정적으로 무는 것을 실증했다(원본 초록 / `disabled={busy}`
  제거하면 빨강). **못 문 게 아니라 안 문 것** → **그 테스트를 더해라**
- **WARN-2** — BE ⑪(**프로젝트를 못 읽으면 목록부터 다시 읽기**, `ProjectPage.tsx:183`)에
  **관측자가 0건**이다(뮤테이션 초록). 테스트를 더해라
- **WARN-3** — **완료 보고 뒤 「다시 읽기」**(`ProjectTaskPanel.tsx:364`)도 **관측자 0건**. 더해라
- **WARN-4** — `ProjectPage.test.tsx:940-942` 의 L-33 둘째 단언이 **자기참조**다(테스트가 자기 픽스처를
  단언한다). **기대값을 리터럴로** 박고 **뮤테이션으로 확인**하라. ⚠ 앞 판에서도 같은 실수가 나왔다
- **WARN-5** — 목이 테스트 사이에 **안 털린다** — `not.toHaveBeenCalled()` 가 **선언 순서에 기댄다.**
  앞 판이 `renderPage()` 에서 `mockClear` 한 방식을 따르라
- **WARN-6** — 한국어 리터럴 하나가 `labels.ts` 밖에 있다. **선례가 똑같다**면 그대로 둬도 된다 —
  **판단해서 적어라**

---

## D. 이 판 «밖» — 고치지 말고 리포트에 옮겨만 적어라

검수가 새 flaky 를 하나 찾았다: `CalendarPage.test.tsx:129`(「뒤집힌 업무의 띠」).
**루프2 가 안 건드린 파일**이고(mtime 09-21), 원인은 **앞 판 FAIL 과 같은 부류** —
`waitFor` 가 API 호출만 기다리고 **DOM 을 동기로 읽는다**. 검수가 「`covered` 계산을 `waitFor` 안으로
넣으면 닫힌다」고 적었다. **이 판에서 고치지 마라.**

## 검증

- **A-1 은 긴 이름·짧은 이름 둘 다** 재라. **A-2 는 역량 없는 세션에서도 버튼이 서는가**를 재라
- **FAIL-1 은 「거절 문구가 보인다」를 재는 테스트**가 있어야 한다
- **새로 더한 단언은 전부 뮤테이션으로 확인하라** — 자기참조 금지, `waitFor` 없는 비동기 읽기 금지
- `make frontend-test` · `npx tsc --noEmit`. ⚠ **기존 흔들림 목록**(이 판 밖):
  `task checklist`(2) · `span/null` · `adjustment and resubmission` · `product surfaces` ·
  `MeetingMaterials` · `ActionCenter` · `CreateWork 멱등키` · **`CalendarPage` 뒤집힌 띠**. **분리해 보고**

## 완료 보고 — **문구 변경 금지**

```bash
orca orchestration send \
  --to term_bdba055b-758b-4dc9-85c3-7836d56b615a --from term_60c20b42-a207-4b79-a724-324ac792c7e5 \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "frontend 완료: 루프2 최종 수정" \
  --body "A-1 셀렉터 / A-2 게이트 제거와 고친 테스트 / FAIL-1 / WARN 여섯 / 뮤테이션 / 테스트 수치(기존 흔들림 분리)"

orca terminal send --terminal term_bdba055b-758b-4dc9-85c3-7836d56b615a \
  --text "[worker_done] frontend 완료 — 루프2 최종 수정. 상세는 인박스." --enter
```

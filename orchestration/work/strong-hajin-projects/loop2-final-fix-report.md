# 루프2 최종 수정 결과 보고 — frontend

**역할** `@sc-ax-fe` · **task-id** `task_cf87c908d6ae` · **워크트리**
`/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects` (브랜치 `kknaksss/strong-hajin-projects`)
**상태: done** — `backend/` **0줄** · 커밋 **0건**(HEAD `e46ce39` 그대로) · 개발 서버 **0회 기동**.

## 만진 파일 — 여섯

```
src/App.tsx                              src/features/project/ProjectPage.tsx
src/styles/projects.css                  src/features/project/ProjectPage.test.tsx
src/features/project/ProjectRail.tsx     src/features/project/ProjectTaskPanel.tsx
```
`find backend/src backend/tests -newermt "15:10"` → **0개**. 공유 자산(`ds/` · `components.css` ·
`WorkModals.tsx` · `MyWorkPage.tsx` · `api.ts`)도 **0줄**이다 — 새 prop 은 전부 «이 화면 쪽»에서 넘긴다.

---

## A-1. 셀렉터 글자가 잘리던 자리 — **남는 폭을 이름이 가져간다**

**원인이 둘이었다.** 하나는 지시서가 짚은 `max-width:60%`, 다른 하나는 그보다 조용하다:
**말줄임표가 애초에 안 걸리는 구조**였다. `projects.css:35` 가 `text-overflow:ellipsis` 를
**트리거 자신**에 걸었는데 그 트리거는 `display:inline-flex` 다 — 그 안의 벌거벗은 글자
(`<Icon/>{label}<Icon/>` 의 가운데)는 **익명 flex item** 이 되고 컨테이너의 `text-overflow` 는
거기 닿지 않는다. 그래서 60% 를 키우기만 했으면 **잘리는 자리만 옮겼을 뿐** 말줄임표는 여전히
안 떴다. (`:35` 의 `>span` 이 그 span 을 이미 기대하고 있었는데 **마크업에 span 이 없었다.**)

**고친 것**
- `ProjectRail.tsx` — 이름을 `<span className="scax-pj-rail__project-name">` 에 담았다.
- `projects.css` — `.scax-pj-rail__title{flex:0 0 auto}`(제목은 **안 줄어든다**) ·
  `.scax-pj-rail__project{flex:1 1 auto;min-width:0}`(**`max-width` 를 걷어냈다**) ·
  `.scax-pj-rail__project-name{…;text-overflow:ellipsis;…}`(말줄임표가 **글자를 담은 요소**에).
- **32px 를 안 넘는다** — 이 파일은 높이를 한 줄도 안 건드린다. 트리거는 `components.css:45` 의
  26px 그대로이고 머리는 `:106` 의 `control-height-sm` 그대로다. 공유 자산 0줄이라
  제목의 `flex:1 1 auto` 를 **덮어쓰는 방식**으로 풀었다(`projects.css` 가 `components.css` 뒤에 실린다).

**테스트 둘**
- 「셀렉터가 프로젝트 이름을 «제 요소 안에» 든다 — **아주 긴 이름도 아주 짧은 이름도**」 —
  62자 이름과 「9월」 둘을 각각 렌더해 이름 요소의 `textContent` 가 **끝까지** 실리는지,
  트리거의 직접 자식에 **벌거벗은 글자 마디가 없는지**, 머리가 여전히 한 줄인지를 잰다.
- 「남는 폭을 «이름» 이 가져간다」 — jsdom 은 레이아웃을 안 계산하므로 **규칙을 읽어** 잰다
  (선례 `ds/HoverContrast.test.tsx:21`): 제목 `flex:0 0 auto` · 셀렉터 `flex:1 1 auto` 이고
  **`max-width` 가 없다** · 이름에 `text-overflow:ellipsis` · **둘 다 `height` 를 안 건다.**

---

## A-2. 「프로젝트 추가」의 역량 게이트 — **없앴다**

- `App.tsx` — `canCreateProjects={has("project.manage")}` **한 줄을 걷어냈다.**
  `canManageOwnTasks` 는 그대로다.
- `ProjectPage.tsx` — prop·prop 문서·분기를 **전부** 없앴다. `add` 는 이제 **언제나 선다**
  (빈 상태 갈래는 같은 노드를 쓰므로 거기서도 그대로다).
- **「프로젝트 관리」의 `may_manage` 는 손대지 않았다** — 게이트는 이제 그 **하나뿐**이다.
- **거절은 이미 모달 «안»에서 말한다** — `createFromHeader` 가 문구를 «돌려주고»
  `ProjectCreateModal` 이 자기 안에 낸다. 역량 없는 사람의 403 도 그 네 갈래와 같은 길이다.

**고친 테스트 — 삭제·skip 0건, 전부 새 계약을 재게 다시 썼다**

| 테스트 | 전 | 후 |
|---|---|---|
| **L-17** 「만들 자격이 없는 세션에는 비활성 버튼도 안 그린다」 | 머리가 **비는 것**을 쟀다 | 「**모든 사람에게 선다**」 — 역량도 관리 권한도 없는 세션에서 버튼이 서고, 머리의 버튼이 **그 하나뿐**이며, **서버가 거절하면 그 문구가 모달 안에 선다**까지 잰다 |
| **L-14 · L-16** | 제목이 「추가는 세션의 자격」 | 「추가는 **게이트가 없다**」. 두 갈래(관리 있음/없음) 단언은 그대로 — 이제 «추가는 늘 있고 관리만 갈린다»를 잰다 |
| 「붙이고 뗄 수 있는지는 서버가 말한 대로」 | `header-actions` 가 **빈 문자열** | `"프로젝트 추가"` — **머리가 비는 게 아니라 관리 하나가 빠진다** |
| Harness · `renderPage` | `canCreateProjects` prop 을 실었다 | 그 prop 이 **사라졌다**(세션 값은 `canManageOwnTasks` 하나) |

⚠ **문서(SPEC·DEC)는 안 건드렸다** — 코디 몫이다. 위 표가 그 목록이다.

---

## B. FAIL-1 — 완료 보고의 거절이 **화면에 뜬다**

`ProjectTaskPanel.tsx` 의 `onError={() => undefined}` 를 **선례대로** 고쳤다
(`MyWorkPage.tsx:1421-1422` 가 `onError`·`onNotice` **둘을 그대로** 넘긴다 — D-32).

- `ProjectPage` → `ProjectTaskPanel` → `TaskStateValue` → `CompletionReportModal` 로
  `onError` 를 내렸다. **`onNotice` 도 함께** 내렸다 — 그 통로가 막혀 있어서
  「완료 보고를 보냈습니다」 **확인 문구도 없었다**(검수가 괄호로 적은 자리).
- 그래서 `App.tsx` 에 **`onNotice={setToast}` 한 줄을 더했다.** 셸이 이미 쥔 값이고
  `sharedWorkProps` 를 통째로 넘기지 않는 규칙은 그대로다. (지시서의 「다른 prop 은 그대로」는
  ~~걷어내는 쪽~~ 을 말한 것으로 읽었다 — 이 한 줄이 없으면 확인 문구가 갈 곳이 없다.)
- `onError` 는 `ProjectTaskPanel` 에서 **선택적**이다 — 안 넘기면 종전대로 조용하다.
  `ProjectPage` 는 **언제나 넘긴다.**

**테스트 둘 (그리고 테스트 하네스가 «문구를 그린다»)**

검수 probe 가 `document.body` 를 본 이유가 여기 있다 — 종전 Harness 는 `onError` 를 **`noop` 스파이**
하나로 받았고, 그러면 「불렸다」는 재도 **「사람이 읽는다」는 못 잰다.** 그래서 Harness 가 이제
셸처럼 **오류를 빨간 띠로, 성공을 토스트로 그린다**(`data-testid="error-banner"` · `"toast"`).
스파이는 그대로 산다 — 기존 `expect(noop).toHaveBeenCalledWith(…)` 단언이 안 깨진다.

- 「완료 보고가 거절되면 «화면이 말한다»」 — `submitTaskCompletion` 이 「끝나지 않은 선행 업무가
  있습니다」로 거절 → **오류 띠에 그 문구 그대로** · 모달은 **열린 채** · **쓴 문장이 안 지워진다.**
- 「완료 보고가 올라가면 확인 문구가 뜨고 프로젝트를 «다시 읽는다»」 — 회차 **리터럴 7** 로
  `submitTaskCompletion("t-5", 7, {...})` · `getProject` **+1** · **전이는 0건** ·
  토스트에 「완료 보고를 보냈습니다. 요청자의 확인을 기다립니다.」

---

## C. WARN 여섯

| # | 처리 |
|---|---|
| **WARN-1** 관문 「아」 무관측 | **테스트를 더했다.** 안 끝나는 promise + `waitFor` 로 트리거의 `disabled` 를 물고, **잠긴 동안 두 번 눌러도 전이가 1건**임을 잰다. 끝나면 **도로 열리는 것**까지 잰다. 검수 말이 맞다 — 흔들리지 않는다(4회 전건 초록) |
| **WARN-2** BE ⑪ 다시 읽기 무관측 | **테스트를 더했다.** 프로젝트 둘을 세우고 둘째의 `getProject` 를 거절시켜 **`listProjects` 가 두 번째로 불리는 것**과 서버 문구가 오는 것을 잰다 |
| **WARN-3** 완료 보고 뒤 다시 읽기 무관측 | **위 §B 의 둘째 테스트가 닫는다**(`getProject` +1) |
| **WARN-4** L-33 의 자기참조 단언 | **걷어내고 «화면이 그린 것»으로 다시 썼다.** 상세를 **영원히 pending** 으로 두고 ①Skeleton 이 서고 ②설명·항목이 **없고** ③집계(`1/4`)는 **이미 있는** 프레임을 잰 뒤, 상세를 **착지시켜** 설명·항목이 **그때 서는 것**을 잰다. 픽스처를 되묻는 줄은 0건이다 |
| **WARN-5** 목이 안 털린다 | `renderPage()` 에서 **`createProject`·`noop`·`notice` 를 함께 턴다**(앞 판이 `getProject`·`getTask` 를 턴 바로 그 자리). `vite.config.ts` 는 **안 건드렸다** — 70개 파일이 공유하는 설정이라 여기서 전역 `clearMocks` 를 켜지 않는다 |
| **WARN-6** `"요청자"` 리터럴 | **그대로 뒀다 — 판단.** 선례 `MyWorkPage.tsx:1427` 과 **글자까지 같은 한 줄**이고, 이 화면은 그 모달을 「가져다 쓰는」 쪽이다(D-32). `labels.ts` 로 옮기면 두 호출부가 **갈라진다** — 규칙(카피는 `labels.ts`)보다 선례 보존이 이 자리에서 더 무겁다고 봤다. 루프3 이 **두 자리를 함께** 옮기는 것이 맞다 |

---

## D. 이 판 «밖» — 옮겨 적기만 한다

`CalendarPage.test.tsx:129`(「뒤집힌 업무의 띠」)의 새 흔들림. **루프2 가 안 건드린 파일**이고
(mtime 09-21 19:33) 원인은 앞 판 FAIL 과 같은 부류 — `:125` 가 **API 호출만** `waitFor` 하고
`:127-129` 가 그 promise 가 그려 낸 DOM 을 **동기로** 읽는다. 검수가 「`covered` 계산을 `waitFor`
안으로 넣으면 닫힌다」고 적었다. **이 판에서 안 고쳤다.**

---

## 뮤테이션 — **13건 전부 빨강**

원본을 백업하고 하나씩 무력화한 뒤 `ProjectPage.test.tsx` 를 돌렸고, 매 회차 끝에 되돌려
`filecmp` 로 **바이트 동일**을 확인했다.

| 뮤테이션 | 결과 |
|---|---|
| M1 셀렉터 이름의 `<span>` 제거(글자를 트리거에 벌거벗겨 둔다) | **빨강 1** |
| M2 `.scax-pj-rail__project` 에 `max-width:60%` 복구 | **빨강 1** |
| M3 이름의 `text-overflow:ellipsis` 제거 | **빨강 1** |
| M4 제목을 줄어들게(`.scax-pj-rail__title{flex:1 1 auto}`) | **빨강 1** |
| M5 제목에서 `scax-pj-rail__title` 클래스 제거 | **빨강 1** |
| M6 「프로젝트 추가」를 다시 게이트 뒤로(`may_manage` 로 가름) | **빨강 4** |
| M7 완료 보고 `onError={() => undefined}` — **검수 FAIL-1 재현** | **빨강 1** |
| M8 완료 보고 `onNotice` 미전달 | **빨강 1** |
| M9 관문 「아」 — `disabled={busy}` 제거 | **빨강 1** |
| M10 BE ⑪ — 못 읽어도 목록 미재조회(`void reload()` 삭제) | **빨강 1** |
| M11 완료 보고 뒤 `onChanged` 제거 | **빨강 1** |
| M12 상세 미도착 프레임의 Skeleton 제거 | **빨강 1** |
| M13 설명을 안 그림 | **빨강 4** |

**M7·M9·M10·M11 은 검수가 「초록」으로 세어 둔 바로 그 뮤테이션이다** — 네 자리 다 닫혔다.
**자기참조 0건 · `waitFor` 없는 비동기 읽기 0건**: 새로 더한 비동기 읽기는 전부 `waitFor`/`findBy*`
안이고, 기대값은 리터럴(`"끝나지 않은 선행 업무가 있습니다"` · `7` · `before + 1` · `"9월"` · 62자 이름)이다.

## 테스트 수치

| 무엇 | 결과 |
|---|---|
| `npx tsc --noEmit` | **exit 0 · 에러 0** |
| `make frontend-test` | **70 파일 · 1016 테스트 전건 통과** — **4회 연속** |
| `ProjectPage.test.tsx` | **56건**(앞 판 50 → **+6**) 전건 통과. 뮤테이션 14회를 더해 약 20회 돌렸고 **이 판 파일의 실패 0회** |
| **기존 흔들림 목록**(이 판 밖) | `task checklist`(2) · `span/null` · `adjustment and resubmission` · `product surfaces` · `MeetingMaterials` · `ActionCenter` · `CreateWork 멱등키` · **`CalendarPage` 뒤집힌 띠** — **4회 중 한 번도 안 났다** |

## 다른 팀 영향

- **BE**: 없다. 새 envelope·응답 변경 요청 0건. 새 API 래퍼 0개.
- **코디**: **문서(SPEC-005 L-14~L-17 · D-31)를 고쳐야 한다** — 「추가는 `project.manage` 게이트」가
  이제 거짓이다. 위 §A-2 의 표가 코드·테스트 쪽 전수다.

## 이슈 / 블로커

- **없다.** `--dispatch-id` 는 못 실었다 — `orca orchestration dispatch-show --task task_cf87c908d6ae`
  가 `No dispatch context found.` 다(앞 판과 같다).

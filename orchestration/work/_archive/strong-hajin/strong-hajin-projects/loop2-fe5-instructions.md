# 루프2 Phase FE-5 — 헤더 생성 · 좌 레일 헤더 · 우 레일(업무 정보 · 상태 · 읽히게)

**allowed_paths**: `frontend/` 만. **`backend/` 0줄** (BE-3 는 끝났고 검수 PASS 다).
커밋·push 금지. **개발 서버 금지** — `5173`·`8100` 은 **사용자 E2E 스택**이다.

## 읽을 것

- 역할: `.../roles/strong-hajin/frontend/role.md` (+ `rules.md`) · 코드 레포 `AGENTS.md`
- **계약**: `spec-005-projects.md` **v0.2.0** — §2.1·2.2·2.6·2.7·**2.10** · §6 의 **FE-5 몫**
- **계획**: `work-005-projects.md` **Phase FE-5** (작업 0 = 배선이 선행이다)
- **결정**: `decision-004-projects.md` — **D-30~D-35 · D-38**
- **백엔드가 실제로 내주는 것**: `loop2-be-report.md` **§3** ← **반드시 읽어라. 아래 §0 이 그 요약이다**
- 앞 판이 남긴 것: `loop2-fe4-report.md` · `loop2-fe4-fix-report.md`
  (**`ProjectRail.tsx`·`projects.css` 구조가 바뀌었다 — 이어받아라**)
- 1루프 지도: `research-fe-structure.md` §4-3(공유 자산) · `review-fe-report.md`

## 0. ⚠ 백엔드 실물 — **상식대로 짜면 정확히 반대로 구현할 자리들**

BE-3 이 실측으로 찍어 준 것이다(`loop2-be-report.md` §3-6). **추측하지 마라.**

1. **`access` 로 체크리스트를 감추지 마라** — `access: "read_only"` **인데 `checklist` 가 실린다.**
   그 조합이 **정상**이다. **`access` 는 이제 「쓰기 범위」만 뜻한다**
2. **`checklist` 키의 «유무»로 갈라라** — 안 실릴 때는 `null`·`[]` 이 아니라 **키 자체가 없다.**
   `body.checklist?.length` 로 써라. `body.checklist.length` 는 **프로젝트 밖 갈래에서 터진다**
3. **`checklist_progress` 도 같이 없다** — 상세에서 항목이 안 오면 집계도 안 온다.
   **미터의 재료는 프로젝트 상세 `tasks[]` 의 `checklist_progress`** 이고 **그쪽은 언제나 실린다**
4. **`references` 는 안 열렸다** — `owner` 전용 키다. 이 판이 연 것은 **체크리스트 둘뿐**
5. **리드라고 더 오지 않는다** — 리드 응답과 참여자 응답이 **완전히 같다.**
   「리드면 쓰기도 되겠지」로 단추를 열면 **404 를 받는다**
6. **쓰기 네 표면은 담당이 아니면 전부 404** (403 아니다) →
   **체크박스를 읽기 전용으로 렌더하라.** 누를 수 있게 두지 마라
7. **`tasks[]` 에는 `checklist` 가 없다** — 우 레일은 **선택된 하나에만** 상세를 부른다
8. **`description` 은 네 갈래 전부에 온다** — 「`read_only` 면 설명이 없겠지」는 틀리다
9. **초대는 `GET /api/projects` 에 한 줄이 «느는» 것으로만 관측된다** — 새 필드·플래그 없다
10. **초대가 붙이는 관계는 `member` 다** — `may_manage` 는 **여전히 `false`** →
    **관리 모달 손잡이가 서면 안 된다**
11. **거절하면 그 프로젝트가 목록에서 «사라진다»** — 목록을 캐시해 두면 **없는 프로젝트를 고른 상태**가
    남는다. **거절 뒤 목록을 다시 읽어라**
12. **배정 거절 문구는 그대로** — `422` + `assignee is not within your assignment scope`. 초대 전용 오류 없다

## 1. 만들 것

### 작업 0 (선행) — 배선
`App.tsx` 가 `ProjectPage` 에 **세션 역량 둘**을 내린다: `project.manage`(생성 버튼 게이트) ·
`task.self_manage`(상태 드롭다운 게이트). ⚠ **`sharedWorkProps` 를 통째로 넘기지 마라. 새 조회를 만들지 마라**
(WORK 의 F9 행이 그렇게 적는다).

### ① 헤더 「프로젝트 추가」 버튼 + 생성 모달
- 게이트는 **`project.manage` capability 보유** — 「관리」 버튼의 `may_manage`(그 프로젝트)와 **다르다**
- ⚠ **빈 상태(프로젝트 0개)에서도 버튼이 서야 한다.** 지금 `noProjects` 갈래는 `Empty` 만 그리고
  레일도 헤더도 안 세운다(`ProjectPage.tsx:230-235·292-298`). **그 자리를 함께 고쳐라**
- 모달 입력은 **넷**: `name`(필수) · `description` · `starts_on` · `ends_on`.
  **`external_key` 는 API 가 받지만 화면은 내지 않는다** (SPEC 이 그렇게 갈라 적었다)
- 거절 네 갈래를 화면이 말해야 한다 — 자격 · 이름 · 기간 역전 · `external_key` 중복
- ⚠ **관리 모달 안의 기존 「새 프로젝트」 폼은 루프3 까지 그대로 둔다.** 지우지 마라

### ② 좌 레일 헤더 한 줄
`[프로젝트 아이콘] 프로젝트 (건수) ──── [셀렉터]`. 건수 배지는 **기존 `Badge variant="count"`**
(수신함·캘린더 레일이 쓰는 그것). ⚠ **`.scax-gutter-list__body` 의 `ref` 를 건드리지 마라** —
FE-4 가 자동 스크롤을 거기 달았다(`loop2-fe4-report.md`). **카드의 `data-task-id` 도 조회 키다. 지우지 마라**

### ③ 우 레일 — 블록 순서와 「업무 정보」
**메타 정보 → 업무 정보(설명 + 체크리스트) → 관계 → 하위 업무**.
체크리스트는 **읽기 전용**(위 §0-6). 설명은 `detail.description`.

### ④ 메타 정보 표 손질
값 **좌측 정렬선을 하나로**(배지·버튼의 자기 padding 상쇄) · **행 높이를 넉넉히 통일**하고 수직 가운데 ·
**버튼임을 테두리나 배경으로** 보이게. ⚠ 시인성은 **`.scax-pj-rel__item` 을 쓰는 두 자리 모두**
(메타의 상위 업무 · 관계 블록의 선행/후행 목록).

### ⑤ 제목·소제목 색
`.scax-pj-side__title` · `.scax-pj-side__block-title` 를 **`ink-strong` 계열**로.

### ⑥ 상태 드롭다운 — **내 업무일 때만**
⚠ **「업무 화면 로직 그대로」는 «그 화면이 상태를 바꿀 때 지나는 모든 관문»을 뜻한다.**
문서 수정 판이 **코드에서 열 개를 세어 SPEC §2.6·§5 와 WORK FE-5 작업 7 에 적어 뒀다.**
**그 표를 그대로 따르라.** 특히 빠지기 쉬운 셋:
- **막힘(block) → `BlockReasonPrompt`** (사유 없이 전이 금지)
- **요청 업무의 완료 → 완료 보고 모달**
- **게이트는 둘** — 세션 역량 `task.self_manage` **그리고** 수락 대기가 아닐 것
그리고 **`version` 동봉**(업무 상세로 읽은 회차 — `tasks[]` 행으로 보내면 409) ·
**성공하면 다시 읽기**(업무 상세 + 프로젝트 상세 — 좌 레일·간트도 같은 상태를 그린다).
**갈 곳이 없으면 드롭다운이 아니라 읽기 배지다.**

## 2. ⚠ 공유 자산

`research-fe-structure.md` §4-3. `projects.css` 는 이 화면 전용이라 자유롭다.
**`components.css`·`shell.css`·`src/ds/`·DS 토큰은 0줄**을 목표로 하고, 불가피하면 리포트에 이유를 적어라.
`Empty`(29곳) · `AppHeader titleEnd`(5화면) · `.screens-b-lead` 는 **건드리지 마라.**

## 3. 검증

- `make frontend-test` · `npx tsc --noEmit`. **기존 실패와 네 실패를 분리**
- ⚠ **검수가 관측한 기존 흔들림**: `task checklist`(2) · `task checklist span/null` ·
  `adjustment and resubmission` · `product surfaces` — **이 판 밖**이다
- **새로 더한 단언이 실제로 잡는지 뮤테이션으로 확인하라.** 앞 판에서 **자기참조 단언**이 나왔다
  (상수를 되계산해 비교해서 그 상수를 바꿔도 통과했다). 같은 실수를 하지 마라
- **비동기 값을 `waitFor` 없이 읽지 마라** — 앞 판의 FAIL 이 그것이었다
- **테스트로 잡은 것 / 눈으로만 확인되는 것**을 갈라 적어라 (사용자 2차 E2E 가 본다)

## 4. 범위 제약

- **루프3 몫 금지**: 관리 모달 정리(생성 폼 제거) · 리드 권한 화면
- `backend/` 0줄 · 개발 서버 금지 · 커밋 금지
- SPEC 에 없는 것을 만들지 마라. 필요하면 리포트에 「막힌 것」으로

## 5. 리포트 (`orchestration/work/strong-hajin-projects/loop2-fe5-report.md`)

- 바꾼 파일과 **각각이 닫는 인수조건(L-)**
- **§0 의 열두 자리를 각각 어떻게 처리했는지** (특히 1·2·5·6·10·11)
- **상태 관문 표를 몇 개 구현했고 무엇을 못 했는지**
- 테스트 수치 · 뮤테이션 결과 · **눈으로만 확인되는 것**
- 막힌 것 · 판단이 필요한 것

## 완료 보고 — **문구 변경 금지**

```bash
orca orchestration send \
  --to term_bdba055b-758b-4dc9-85c3-7836d56b615a --from term_f1eac00c-73be-4324-b384-3f902ccd469a \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "frontend 완료: 루프2 FE-5" \
  --body "바꾼 파일 / 닫은 인수조건 / §0 열두 자리 처리 / 상태 관문 몇 개 / 테스트·뮤테이션 / 눈으로만 볼 것"

orca terminal send --terminal term_bdba055b-758b-4dc9-85c3-7836d56b615a \
  --text "[worker_done] frontend 완료 — 루프2 FE-5. 상세는 인박스." --enter
```

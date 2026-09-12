# [frontend] 4차 — 디자인 시스템 부품 2건 신설: DatePicker 팝오버 · Toast tone 아이콘 (화면 연결 없음)

너는 **sc-ax `frontend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-ax/orchestration/roles/sc-ax/frontend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/ax-workspace/sc-design-system`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

1~3차(`7e6fc53`·`efc4c94`·`d873c00`·`922ed65`)가 커밋돼 있다 — 그 위에서 시작한다.
⚠ **같은 워크트리에서 다른 코디의 backend 워커가 `backend/` 를 고치고 있다.** `git status` 에 backend/·docs/ 변경이 보여도 네 것이 아니다 — 건드리지 말고, `git stash`·`git checkout`·`git add` 등 **git 상태를 바꾸는 명령은 전부 금지**. 미추적 `.design-sync/`·`ds-bundle/`·`.ds-sync/` 는 코디네이터의 claude.ai/design 동기화 파일이다 — 읽기만.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/ax-workspace/sc-design-system/docs/design/design-system-v2.dc.html` ← 시각 규칙의 SoT. 이번 범위: **`14 — OVERLAY`**(Popover: 200–400px · 스크림 없음 · 트리거 바로 아래 좌측 정렬 · 8px 띄움 · 아래 공간 모자라면 위로 · r12 `--radius-popover` · `--shadow-lg`; Toast: 400×56 · 하단 중앙 60px 위 · 4초 · 실행취소), **`09 — FORM`**(Date h38), **`07 — ICON`**(viewBox 16 · stroke 1.5, 14 이하 1.3 · round · fill none · 채운 아이콘 금지), **`16 — RULES`** 2·3·9·11.
- 이 두 부품은 **v2 에 없는 확장**이다. 위 절의 규격 안에서 조합해 만든다. 문서에 없는 색·그림자·간격을 새로 만들지 않는다.

**기대는 개념** — 해당 없음. §3 결정을 따른다.

## 2. 배경 / 무엇을 바꾸나

claude.ai/design 에 이 리포의 프리미티브를 올려 놓고 보니 두 가지가 비어 있다. (a) `DateField` 가 브라우저 기본 달력(`showPicker()`)을 열어서 디자인 시스템 안에 **우리 모양의 달력 피커가 없다.** (b) `Toast` 가 메시지 한 줄뿐이라 **완료·에러를 구분하는 아이콘이 없다.**
이번 작업은 **부품만 만든다.** 어떤 화면에도 꽂지 않는다 — DateField 는 계속 브라우저 달력을 열고, Toast 호출부는 그대로다. 사용자에게 보이는 변화는 0 이어야 한다.

## 3. 계약 (결정 2026-09-07 — 이대로)

### A. `DatePicker` — `frontend/src/DatePicker.tsx` 신설
- 시그니처: `DatePicker({ value, onChange, min?, max?, id?, label })` — `value` 는 ISO `YYYY-MM-DD` 또는 `""`, `onChange(iso)` 는 날짜를 고르거나 지울 때. `label` 은 패널 aria-label.
- **기존 `Popover`(`src/Popover.tsx`) 위에 올린다.** 팝오버를 새로 만들지 않는다. 트리거는 호출부가 주는 방식(`Popover.trigger`)을 그대로 쓰되, DatePicker 자체가 기본 트리거를 하나 가진다: `btn h30 ghost` + `Icon name="calendar" size={14}` (지금 DateField 의 `.date-field-picker` 와 같은 모양).
- 패널 폭 **280**(v2 14 의 200–400 안). 구성: 헤더(「2026년 9월」 `t-item` + 이전/다음 달 `btn h30 icon ghost` with `Icon chevron-right`/좌측은 회전 없이 `chevron-down` 을 쓰지 말고 **`chevron-right` 를 `transform: rotate(180deg)`** 로) · 요일 7열(`calendar-weekdays` 재사용) · 날짜 7×6 격자 · 푸터(좌 「지우기」 `btn link`, 우 「오늘」 `btn h30`).
- 날짜 셀: 30×30 · `--radius-control`. 오늘 = 테두리 `--border-strong`. **선택일 = `--text-primary` 배경 + `--on-fill` 글자**(v2 16-3 「현재 위치 표시는 검정」— 캘린더의 `.calendar-cell.today .calendar-day` 와 같은 규칙). hover = `--surface-sunken`. 이번 달 밖 = `--text-disabled`. `min`/`max` 밖 = disabled(`--text-disabled`, 클릭 불가).
- 키보드: 방향키로 날짜 이동, Enter 선택, Esc 닫기(Popover 가 이미 처리). 열릴 때 포커스는 선택일(없으면 오늘)로.
- 날짜 계산은 `labels.ts` 의 `addDays`·`formatDate`·`seoulToday`·`formatMonth` 를 **재사용**한다. 새 날짜 라이브러리 금지. 카피(「오늘」·「지우기」·요일)는 `labels.ts` 에 둔다.
- `DateField` 는 **손대지 않는다.** (연결은 별도 결정.)

### B. `Toast` tone — `frontend/src/Modal.tsx` 의 `Toast` 에 prop 추가
- `tone?: "success" | "error"` 선택 prop. **없으면 지금과 byte 단위로 같은 렌더.**
- 있으면 메시지 앞에 아이콘 1개(`Icon` size 16, 아이콘–글자 gap 8): `success` → `check` 를 **`--accent`**(#7181F8, v2 16-2 「완료는 accent」— **초록 금지**, 사용자 결정) · `error` → `alert` 를 `--danger-accent`(#E2685B). 다크 배경 위라 대비 확인해서 보고에 수치 적기(WCAG 는 텍스트 기준이라 아이콘은 참고치).
- `alert` 글리프는 이미 있다(`Icon.tsx`). `check` 도 있다. **새 글리프를 만들지 않는다.** 원 안의 x 같은 채운 아이콘은 v2 07 위반이라 만들지 않는다.
- `role`: error 면 `role="alert"`, 아니면 지금처럼 `role="status"`.

### C. 디자인 시스템 엔트리
- `frontend/ds-entry.tsx` 에 `export { DatePicker } from "./src/DatePicker";` 한 줄 추가. (이 파일은 claude.ai/design 번들 엔트리다. 다른 줄은 손대지 않는다.)

### D. 공통
- 스타일은 `styles.css` 에 `/* ---------- date picker (v2 14 Popover 위) ---------- */` 절로 추가. `:root` 토큰 값 변경 금지, 추가도 금지(필요한 색은 전부 있다). 컴포넌트에 hex 리터럴 0.
- `api.ts`·viewModels·envelope·DateField·Popover 불변.

## 4. 먼저 읽을 핵심 파일

- `frontend/src/Popover.tsx` — 트리거/children 렌더 함수 계약, `width`, 위로 열기.
- `frontend/src/DateField.tsx` — 현재 달력 트리거 모양(`.date-field-picker`), ISO 경계 규칙.
- `frontend/src/Modal.tsx` — `Toast` 현재 구현(4초 타이머·실행취소·닫기).
- `frontend/src/Icon.tsx` — 26 글리프와 size/stroke 규칙.
- `frontend/src/labels.ts` — `addDays`·`formatDate`·`formatMonth`·`seoulToday`·`minWidthNotice` 등 카피 모음 방식.
- `frontend/src/styles.css` — `.popover`·`.popover-item`·`.calendar-weekdays`·`.calendar-day`·`.toast`·`.btn` 규칙.
- 옆자리 테스트: `Popover.test.tsx` · `DateField.test.tsx` · `Icon.test.tsx`.

## 5. allowed_paths — 이 밖은 건드리지 마라

- `frontend/src/DatePicker.tsx` (신설) · `frontend/src/DatePicker.test.tsx` (신설) · `frontend/src/Modal.tsx` · `frontend/src/Modal.test.tsx`(없으면 신설) · `frontend/src/labels.ts` · `frontend/src/styles.css` · `frontend/ds-entry.tsx`(한 줄)
- 금지: 그 외 `frontend/src/*` 전부(특히 `DateField.tsx`·`Popover.tsx`·`Icon.tsx`·`api.ts`·`viewModels.ts`) · `frontend/package.json` · `frontend/scripts/` · `backend/` · `docs/` · `.design-sync/` · `ds-bundle/` · `.ds-sync/` · `.gitignore`

## 6. 구현 단계

1. v2 `14`·`09`·`07` 의 수치를 표로 뽑고, `Popover`·`Toast`·`DateField` 의 현재 값을 옆에 붙인다(보고 포함).
2. **B(Toast tone) 먼저** — 작다. RED 테스트(tone 없음 = 기존 스냅샷과 동일 · success/error 아이콘·role) → 구현.
3. **A(DatePicker)** — RED 테스트(열림/선택/onChange ISO/지우기/오늘/min·max/키보드) → 구현. `Popover` 를 조합만 한다.
4. C 엔트리 한 줄.
5. 브라우저(5176, 코디가 띄워 둔 스택. 안 떠 있으면 `cd frontend && npx vite --port 5176` 로 프론트만)에서 DatePicker 를 확인할 화면이 없으므로 **vitest + jsdom 로 검증하고**, 시각 확인은 `DatePicker.test.tsx` 의 렌더 결과를 HTML 로 덤프해 스크린샷 대신 보고에 구조를 적는다. 스택 재시작 금지.

## 7. 범위 제약 — 하지 말 것

- DateField 를 DatePicker 로 바꾸지 않는다. Toast 호출부에 tone 을 넣지 않는다. **화면 변화 0.**
- 새 글리프·새 토큰·새 그림자·초록색 금지. 외부 의존성 추가 금지.
- 시간(HH:mm)·기간(범위 선택)·연/월 점프 UI 는 만들지 않는다 — 별도.
- git 상태 변경 명령 금지(위 ⚠). 다른 워커의 backend/ 변경을 되돌리지 않는다.

## 8. 검증

```
cd frontend && npx tsc --noEmit (0 에러) + npx vitest run src/DatePicker.test.tsx src/Modal.test.tsx src/Popover.test.tsx src/DateField.test.tsx.
grep 게이트: grep -nE '#[0-9a-fA-F]{3,6}' src/DatePicker.tsx src/Modal.tsx → 0 · grep -c 'DatePicker' src/DateField.tsx → 0 · git diff --stat -- frontend/ 가 §5 allowed 파일만.
전체 빌드·acceptance-e2e 금지 — 사용자 방침. 검증은 1회만
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.
- 보고에 v2 수치 대조표 · DatePicker 접근성(role/aria/키보드) 표 · Toast tone 아이콘 대비 수치 · 「디자인 확장 필요(v2 등록 요청)」 항목 2건을 붙인다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_a7a0991a-bec1-41c8-b929-799959da5e7f --from term_e17ed244-1384-4eda-a88c-7c93b1c66ba8 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_a7a0991a-bec1-41c8-b929-799959da5e7f \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_a7a0991a-bec1-41c8-b929-799959da5e7f --text "[질문] frontend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)

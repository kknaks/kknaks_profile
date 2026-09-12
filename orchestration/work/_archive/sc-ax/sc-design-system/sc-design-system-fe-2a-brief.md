# [frontend] 2차-a — 디자인 시스템 v2 적용: 상태·폼·오버레이 프리미티브 (B2·B3·B4+A14·B5·B6)

너는 **sc-ax `frontend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-ax/orchestration/roles/sc-ax/frontend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/ax-workspace/sc-design-system`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

1차 결과는 `7e6fc53` 으로 **이미 커밋돼 있다** — 그 위에서 시작한다. 같은 워크트리에서 코디네이터가 `make local-stack` 을 띄워 둔다(API 8001 · 프론트 5176, Vite HMR). `backend/`·`.venv`·`node_modules`·`.scax/` 는 건드리지 마라.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/ax-workspace/sc-design-system/docs/design/design-system-v2.dc.html` ← 시각 규칙의 SoT. 이번 범위는 섹션 **`09 — FORM`**, **`10 — STATE`**, **`14 — OVERLAY`**(Popover · Status Dropdown), **`06`**(Popover r12 · shadow-lg). 리포트와 디자인이 어긋나면 **디자인이 맞다.**
- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-ax/orchestration/work/sc-design-system/fe-survey-report.md` ← 「바꿔야 할 것」 **B2 · B3 · B4 · B5 · B6** 과 **A14** 가 범위. 각 행의 프론트 사용처(파일:줄)를 출발점으로 쓴다(1차 커밋으로 줄 번호는 밀렸다 — 내용으로 찾아라).
- `/Users/kknaks/orca/workspaces/ax-workspace/sc-design-system/README.md` 「판단 통합」 — Status Dropdown 을 만들어도 **가능한 command 는 서버 envelope(`allowed_commands`) 가 준다.** 드롭다운이 kind·status 로 선택지를 추론하면 안 된다.

**기대는 개념** — 해당 없음. §3 결정을 따른다.

## 2. 배경 / 무엇을 바꾸나

1차로 토큰 아래 CSS 값은 v2 에 맞췄다. 이제 **v2 가 정의했는데 프론트에 없는 상태·폼·오버레이 프리미티브**를 만든다. 지금은 로딩이 빈 화면이고, Empty 블록에 아이콘·CTA 가 없고, 상태 변경이 네이티브 `<select>` 이고, 체크박스가 네이티브이고, 인풋에 에러 상태가 없다. v2 `RULES 10`: "정상만 그린 화면은 미완성".
이번 범위는 **프리미티브를 만들고, 이미 같은 역할을 하는 자리에 교체 적용**하는 것이다. 새 화면·레이아웃·반응형·아이콘 시스템(B7)·토스트(B13)·테이블(B15)·그래프 색(B16)은 2차-b·3차다.

## 3. 계약 (결정 2026-09-07 — 이대로)

- 사람 표기(요청자·담당자·참조)는 유지한다(디자인 확장 결정).
- **v2 가 primitive 표에 없이 컴포넌트 절에서만 준 색**(1차에서 리터럴로 넣은 AI·Danger 상태색 8개, 이번 09·10·14 의 값들)은 `:root` 에 **역할 이름의 시맨틱 토큰**으로 올려 쓴다(예 `--ai-border`, `--ai-bg-hover`). 컴포넌트 규칙에 hex 리터럴을 두지 않는다. `:root` 밖 hex 는 1차 종료 시점 45개에서 **줄어야** 한다.
- **A14**: `--radius-popover: 12px` 를 이번에 넣고 Popover 가 쓴다. 다른 리터럴 12px 는 팝오버가 아니면 손대지 않는다.
- **안 쓰는 프리미티브는 만들지 않는다.** Radio·Toggle·Search 는 프론트에 같은 역할의 네이티브 요소가 있을 때만 만들어 교체한다. 없으면 만들지 말고 「대응 자리 없음」으로 보고한다(v2 `01` "안 쓰는 토큰은 오답 선택지"와 같은 정신).
- BE 계약: 해당 없음. `api.ts`·viewModels·envelope 처리 로직은 바꾸지 않는다.

## 4. 먼저 읽을 핵심 파일

- `frontend/src/styles.css` — 1차 후 상태. `.empty`, `.btn`, 인풋·셀렉트 규칙, focus 링 토큰.
- `frontend/src/Modal.tsx` — 기존 오버레이 패턴(Modal·Toast). Popover 는 이 파일 옆에 새로 만든다.
- `frontend/src/WorkModals.tsx` — 네이티브 체크박스 3곳, 폼 인풋·검증 위치(B5·B6 적용 자리).
- `frontend/src/MyWorkPage.tsx`·`OrgPage.tsx`·`CalendarPage.tsx`·`TodayPage.tsx` — Empty 사용처 11곳과 로딩 상태(B2·B3).
- `frontend/src/ActionCenter.tsx`·`WorkViews.tsx` — 상태 변경 `<select>` 가 있는 자리(B4). **선택지는 envelope 에서 온 것을 그대로 그린다.**
- `frontend/src/*.test.tsx` 중 위 파일들의 옆자리 테스트.

## 5. allowed_paths — 이 밖은 건드리지 마라

- `frontend/src/` (새 컴포넌트 파일·옆자리 테스트 생성 허용)
- 금지: `frontend/src/api.ts` · `frontend/src/viewModels.ts` · `frontend/src/idempotency.ts` · `frontend/scripts/` · `backend/` · `docs/`

## 6. 구현 단계

1. 디자인 `09`·`10`·`14`·`06` 을 읽고 각 프리미티브의 규격(크기·radius·색·상태·간격)을 표로 뽑아 보고에 붙인다. 리포트 B 표와 다르면 디자인을 따른다.
2. **B2 Skeleton** — `Skeleton.tsx`(bar `--border-subtle` r4 h14 gap 10, 실제 콘텐츠와 같은 개수). 로딩 플래그가 있는 리스트·카드 자리(내 업무·오늘·캘린더·조직 등)에 적용. 로딩 상태가 없는 화면엔 억지로 넣지 않는다.
3. **B3 Empty** — 기존 `.empty` 를 v2 규격(아이콘 20 + Headline 2 Bold + Label 1 Meta + CTA 슬롯)으로. variant: 기본 / 필터(「초기화」 CTA) / 에러(「다시 시도」 CTA). 11개 사용처를 각각 어느 variant 로 바꿨는지 보고. 아이콘은 B7 전이라 **아이콘 슬롯만** 두고 비워 둔다(임시 이모지·글리프 금지).
4. **B4 Popover + Status Dropdown + A14** — `Popover.tsx`(폭 200–400 · `--radius-popover` · `--shadow-lg` · 스크림 없음 · 트리거에서 8px · 바깥 클릭·Esc 로 닫힘 · `:focus-visible` 링). Status Dropdown 은 Popover 위에 만든다(현재 값 배경 `#F4F5FF` → 토큰, 지연 없음). 상태 변경 `<select>` 를 이것으로 교체하되 **선택지·활성 여부는 envelope 의 `allowed_commands` 에서 그대로**.
5. **B5 폼 컨트롤** — `FormControls.tsx`: Checkbox(16 r4)는 네이티브 3곳 교체. Radio(16)·Toggle(36×20)·Search(h34 w260)는 §3 규칙대로 대응 자리가 있을 때만.
6. **B6 인풋 에러 상태** — 인풋·텍스트에어리어·셀렉트에 에러 클래스, 헬퍼 텍스트 → 에러 텍스트 **교체**(둘 다 보이지 않게), 필수 `*` `--danger`. 이미 검증 메시지가 있는 폼(WorkModals)에 적용.
7. 새 컴포넌트마다 옆자리 `*.test.tsx`(렌더·상태·키보드 닫힘). 기존 테스트 깨지면 고친다.
8. 5176 에서 7개 화면 + 업무 생성/요청 모달 + 상태 변경 드롭다운을 실제로 눌러 본다. 깨진 곳은 보고.

## 7. 범위 제약 — 하지 말 것

- 레이아웃·그리드·반응형(B8~B12) · 아이콘 시스템(B7) · Toast(B13) · Progress/Log Row(B14) · 테이블(B15) · GraphCanvas(B16) 금지 — 2차-b·3차.
- `:root` 기존 토큰 값 변경 금지. 추가만(§3 시맨틱 토큰 · `--radius-popover`).
- 권한·선택지를 프론트에서 추론하는 코드 금지(`rules.md`). `api.ts` 밖 fetch 금지.
- 외부 라이브러리 추가 금지(`package.json` 변경 금지).
- 대응 자리 없는 프리미티브를 만들어 두지 않는다.

## 8. 검증

```
cd frontend && npx tsc --noEmit (0 에러) + npx vitest run <새로 만든 테스트 + 만진 파일의 옆자리 테스트만>.
grep 게이트: awk 'NR>45' src/styles.css | grep -o -E '#[0-9a-fA-F]{3,6}\b' | wc -l  → 45 미만(줄었는가) · grep -c 'var(--radius-popover)' src/styles.css → 1 이상 · grep -rn '<select' src/*.tsx → 상태 변경 자리에 남은 것 0(다른 용도 select 는 목록으로 보고).
전체 빌드·acceptance-e2e 금지 — 사용자 방침. 검증은 1회만
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.
- 보고에 B2·B3·B4·A14·B5·B6 각각 「적용 / 부분(이유) / 대응 자리 없음」 표 + 새 시맨틱 토큰 목록을 붙인다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_05d3028b-5830-4523-9819-21785ea51f5b --from term_99679654-1a7c-470e-90a8-6978c0aa6c1a \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_05d3028b-5830-4523-9819-21785ea51f5b \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_05d3028b-5830-4523-9819-21785ea51f5b --text "[질문] frontend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)

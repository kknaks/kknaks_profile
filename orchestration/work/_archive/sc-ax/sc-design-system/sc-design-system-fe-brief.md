# [frontend] 1차 — 디자인 시스템 v2 적용: 토큰 아래 CSS 규칙 정리 (버그 2건 + A1~A22)

너는 **sc-ax `frontend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-ax/orchestration/roles/sc-ax/frontend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/ax-workspace/sc-design-system`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

같은 워크트리에서 코디네이터가 `make local-stack` 으로 앱을 띄워 둔다(API 8001 · 프론트 5176, Vite HMR). `backend/.venv`·`frontend/node_modules`·`.scax/` 는 건드리지 마라. 너는 `frontend/src/` 만 고친다.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-ax/orchestration/work/sc-design-system/fe-survey-report.md` ← **이번 작업의 작업 목록.** 「바꿔야 할 것 — 우선순위」의 **A1~A22** 와 **B1** 이 범위다. 각 행의 근거(디자인 섹션 + `styles.css:줄`)를 그대로 따라간다.
- `/Users/kknaks/orca/workspaces/ax-workspace/sc-design-system/docs/design/design-system-v2.dc.html` ← 시각 규칙의 SoT. 리포트와 디자인이 어긋나면 **디자인이 맞다** — 고치고 보고에 적어라.
- `/Users/kknaks/orca/workspaces/ax-workspace/sc-design-system/docs/design/README.md` — 「구현은 styles.css 가 소유」.

**기대는 개념** — 해당 없음. 대신 아래 §3 의 결정 3건을 그대로 따른다.

## 2. 배경 / 무엇을 바꾸나

조사 결과 `:root` 토큰 41개는 v2 와 일치하지만 그 아래 CSS 규칙이 v2 를 따르지 않는다 — 정의 없는 `--surface-default` 16곳, 규칙 없는 className 6개, v2 가 금지한 간격 10·14·18px 57회, 행간·자간 지역 오버라이드 9곳, 스케일 밖 font-size 4곳, 그리고 값이 어긋난 컴포넌트 규칙(버튼 상태색·탭·테이블·툴바 높이 등).
이번 1차는 **마크업을 건드리지 않고 CSS 값·규칙만** v2 에 맞춘다. 새 컴포넌트(Popover·Skeleton·폼 컨트롤·아이콘)와 레이아웃(홈 3열·List 패널·1640·반응형)은 2차·3차다 — 여기서 하지 마라.

## 3. 계약 (사용자 결정 2026-09-07 — 이대로)

- **디자인 v2 의 「요청자·담당자·참조 없음」 전제는 sc-ax 에 맞춰 확장한다.** 카드·리스트의 사람 표기(`.task-card-people`·`.person-chip`·`.person-arrow`)를 걷어내지 않는다. 그 규칙들도 간격·타이포는 v2 스케일로 맞춘다.
- 홈 3열 폭은 **392/600/600** 이 맞다(`05` 가 최신). 이번엔 폭을 바꾸지 않지만(3차) 관련 값을 360 쪽으로 「맞추지」 마라.
- Hero 높이는 **120** 이 맞다(`01` — v1 400 은 오기). A3 적용.
- BE 계약: 해당 없음.

## 4. 먼저 읽을 핵심 파일

- `frontend/src/styles.css:1-45` — `:root` 토큰. **여기는 손대지 않는다** (A1 의 `--surface-default` 정의 1줄, A14 의 `--radius-popover` 1줄 추가만 예외).
- `frontend/src/styles.css:46-901` — 이번 작업의 본체. 리포트 A 표의 줄 번호를 따라간다.
- `frontend/src/ActionCenter.tsx:266,503` — B1 의 `form-grid`. 나머지 5개 클래스(`surface-card-list`·`round-basis`·`conflict`·`final`·`ax-rail-timings`)는 리포트 대조표에서 사용처를 찾는다.

## 5. allowed_paths — 이 밖은 건드리지 마라

- `frontend/src/styles.css`
- `frontend/src/*.tsx`·`frontend/src/chat/*` — **B1 의 className 6개를 마크업에서 제거하는 경우에 한해**, 그리고 해당 줄만. 그 외 tsx 수정 금지.

## 6. 구현 단계

1. 리포트 A 표를 위에서부터 훑어 `styles.css` 의 실제 줄이 리포트와 맞는지 확인한다(줄 번호는 조사 시점 값이라 밀렸을 수 있다 — 내용으로 찾아라).
2. **A1**: `:root` 에 `--surface-default: #fff;` 를 추가하지 말고, 16곳을 이미 있는 `--surface` 로 치환한다(토큰 중복 금지 — `README.md` 「구현은 styles.css 가 소유」·v2 `01` Surface 는 하나).
3. **A2**: 10·14·18px 57회를 각각 가장 가까운 v2 스케일(8·12·16·20)로 바꾼다. 어느 쪽으로 반올림할지는 **그 규칙이 그리는 컴포넌트의 디자인 값**으로 정한다(예: 카드 패딩은 16, 칩 패딩은 8). 판단이 안 서는 곳은 리스트로 보고에 남긴다.
4. **A9·A10**: 행간·자간 오버라이드 9곳 제거, font-size 9→11·10→11·12.5→12.
5. **A3~A8·A11~A22**: 값 교정. 각 항목의 디자인 근거 섹션을 열어 값을 확인하고 바꾼다.
6. **B1**: 규칙 없는 className 6개 — 디자인에 대응 규칙이 있으면 `styles.css` 에 쓰고, 없으면 마크업에서 그 className 만 제거한다. 어느 쪽을 택했는지 6개 각각 보고.
7. 브라우저(5176)로 홈·내 업무·캘린더·조직·관계 탐색·일일보고를 한 번씩 열어 깨진 곳(투명 배경·겹침·잘림)이 없는지 본다. 스크린샷은 불필요, 깨진 화면은 보고에 적는다.

## 7. 범위 제약 — 하지 말 것

- 마크업 구조 변경·새 컴포넌트·새 파일 금지 (B2~B18 은 2차·3차).
- `:root` 토큰 값 변경 금지. `--radius-popover` 추가 외 새 토큰 금지.
- 사람 표기 제거 금지(§3).
- 반응형 브레이크포인트(1100·1024·900·720) 정리는 3차 — 이번엔 손대지 않는다. 단 그 안의 간격 값이 금지 스케일이면 값만 바꾼다.
- `api.ts`·viewModels·테스트 파일 수정 금지. 로컬 스택(.venv·node_modules·docker)에 손대지 않는다.

## 8. 검증

```
cd frontend && npx tsc --noEmit (0 에러 — B1 로 tsx 를 만졌을 때) + npx vitest run <B1 로 만진 tsx 의 옆자리 테스트만> . 그리고 자기 grep 으로 리포트 수치를 0 으로 만든다:
  grep -c 'var(--surface-default)' src/styles.css   → 0
  grep -o -E '\b(10|14|18)px' src/styles.css | wc -l   → 0 (남으면 각각 왜 남겼는지 보고)
  grep -c -E 'line-height|letter-spacing' src/styles.css   → :root 정의 외 0
전체 빌드·acceptance-e2e 금지 — 사용자 방침. 검증은 1회만
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.
- 보고에는 A1~A22·B1 각각 「적용 / 부분(이유) / 미적용(이유)」 표를 붙인다.

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

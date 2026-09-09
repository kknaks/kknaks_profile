# [frontend] 2차-b — 디자인 시스템 v2 적용: 아이콘·Popover·토스트·프로그레스·테이블·그래프 색 (B7·B4+A14·B13·B14·B15·B16)

너는 **sc-ax `frontend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-ax/orchestration/roles/sc-ax/frontend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/ax-workspace/sc-design-system`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

1차 `7e6fc53` · 2차-a `efc4c94` 가 **커밋돼 있다** — 그 위에서 시작한다. 코디네이터가 `make local-stack` 을 띄워 둔다(API 8001 · 프론트 5176). `backend/`·`.venv`·`node_modules`·`.scax/` 는 건드리지 마라.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/ax-workspace/sc-design-system/docs/design/design-system-v2.dc.html` ← 시각 규칙의 SoT. 이번 범위 섹션: **`07 — ICON`**, **`14 — OVERLAY`**(Popover · Toast), **`05`**(툴바 「업무 유형 ▾」 칩+팝오버), **`11 — COMPONENTS`**(Progress bar · Log Row), **`12 — TABLE`**(정렬 chevron · 빈 값). 리포트와 어긋나면 **디자인이 맞다.**
- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-ax/orchestration/work/sc-design-system/fe-survey-report.md` ← 「바꿔야 할 것」 **B7 · B4(+A14) · B13 · B14 · B15 · B16**. 줄 번호는 두 커밋으로 밀렸다 — 내용으로 찾아라.
- 2차-a 보고의 미결 (1): Popover 소비처 = v2 05 툴바 「업무 유형 ▾」 칩(MyWorkPage 의 `task-state-filter`). 이번에 이걸로 Popover 를 세운다.

**기대는 개념** — 해당 없음. §3 결정을 따른다.

## 2. 배경 / 무엇을 바꾸나

2차-a 로 상태·폼 프리미티브가 들어갔다. 남은 것은 (a) 아이콘이 텍스트 글리프(`×`·`▾`·`→`·이모지)라는 것, (b) Popover 가 아직 없고 Empty 의 아이콘 슬롯이 비어 있다는 것, (c) 토스트에 실행취소가 없고 Progress·Log Row·테이블 헤더가 v2 규격과 다르다는 것, (d) GraphCanvas 가 hex 15개를 직접 쓴다는 것이다.
이번은 **디자인 시스템 적용의 마지막 컴포넌트 단계**다. 레이아웃·그리드·반응형(B8~B12)은 3차.

## 3. 계약 (결정 2026-09-07 — 이대로)

- **B7 아이콘**: v2 `07` 은 규격(viewBox 16 · stroke 1.5, ≤14 는 1.3 · round cap/join · fill none · 12/14/16/20)만 주고 세트는 안 준다. **외부 아이콘 라이브러리 금지**(`package.json` 변경 금지). `Icon.tsx` 하나에 **지금 글리프가 쓰이는 자리에 필요한 아이콘만** 손으로 그린다(close · chevron-down · arrow-right · search · check · plus · alert 등 — 실제 사용처를 세어 목록으로 보고). Empty 의 아이콘 슬롯도 여기서 채운다. 장식용 아이콘을 늘리지 않는다.
- **B4 Popover + A14**: `Popover.tsx`(폭 200–400 · `--radius-popover: 12px` 신설 · `--shadow-lg` · 스크림 없음 · 트리거에서 8px · 바깥 클릭·Esc 닫힘 · `:focus-visible`). 소비처는 MyWorkPage 툴바의 상태 필터 `<select>` → v2 05 「업무 유형 ▾」 칩+팝오버. **필터 선택지는 지금 select 가 쓰는 값 그대로**, 권한·command 와 무관한 순수 필터다. 다른 select 8개(사람·역할·범위·참조 피커)는 v2 09 Select 로 그대로 둔다.
- **B13 Toast**: 실행취소 액션 슬롯 추가(400×56 · 하단 중앙 60px · 4초). 실제로 되돌릴 수 있는 호출이 있을 때만 액션을 넘긴다 — 없으면 슬롯만 만들고 「대응 자리 없음」 보고. 새 API 호출 만들지 않는다.
- **B14**: Progress bar · Log Row 를 v2 `11` 규격으로 — 기존 유사물(리포트가 「유사물은 있으나 규격 다름」이라 한 것)을 찾아 그 규칙을 고친다. 새 컴포넌트가 필요하면 만들되 소비처 없이 두지 않는다.
- **B15**: 테이블 정렬 헤더 chevron(아이콘 시스템 사용) + 빈 값 `—`. **반응형 열 숨김 순서는 3차** — 하지 않는다.
- **B16**: GraphCanvas 의 hex 15개를 `:root` 시맨틱 토큰(`--graph-node-*`·`--graph-edge-*` 류)으로. sigma 가 문자열 색을 요구하면 `getComputedStyle` 로 토큰을 읽어 넘긴다. 값은 바꾸지 않는다(디자인이 그래프 팔레트를 정의하지 않았다 — 등록 요청은 코디 몫).
- 사람 표기 유지. `api.ts`·viewModels·envelope 로직 불변.

## 4. 먼저 읽을 핵심 파일

- `frontend/src/styles.css` — 2차-a 후 `:root`(시맨틱 토큰 구역), `.empty`, `.btn.icon`, 테이블 규칙, 토스트 규칙.
- `frontend/src/Modal.tsx` — Toast 구현. Popover 는 이 옆에 새로.
- `frontend/src/Empty.tsx` — 아이콘 슬롯.
- `frontend/src/MyWorkPage.tsx` — 툴바 `task-state-filter` select.
- `frontend/src/GraphCanvas.tsx:19-26,78-80,173,185,220,223` — hex 15개.
- 글리프 사용처: `grep -n -E '[×▾▸✓✕⋯←→]' src/*.tsx src/chat/*.tsx` (테스트 파일 제외) — 이게 B7 의 작업 목록이다.

## 5. allowed_paths — 이 밖은 건드리지 마라

- `frontend/src/` (새 컴포넌트·옆자리 테스트 생성 허용)
- 금지: `frontend/src/api.ts` · `frontend/src/viewModels.ts` · `frontend/src/idempotency.ts` · `frontend/package.json` · `frontend/scripts/` · `backend/` · `docs/`

## 6. 구현 단계

1. 디자인 `07`·`14`·`05`·`11`·`12` 규격을 표로 뽑아 보고에 붙인다.
2. **B7**: 글리프 사용처를 전수 세고(테스트 파일 제외) → 필요한 아이콘 이름 목록 → `Icon.tsx` → 사용처 교체. `.btn.icon` 정사각 규칙이 아이콘 크기와 맞는지 확인. Empty 아이콘 슬롯 채움(variant 별 1개).
3. **B4+A14**: `Popover.tsx` + 옆자리 테스트(열림·바깥 클릭·Esc·포커스). MyWorkPage 상태 필터를 칩+팝오버로. `--radius-popover` 신설.
4. **B13**: Toast 액션 슬롯 + 되돌릴 수 있는 호출 조사 → 있으면 연결, 없으면 보고.
5. **B14**: Progress bar · Log Row 규격 맞춤.
6. **B15**: 정렬 가능한 헤더에 chevron, 빈 셀 `—`(labels.ts 경유).
7. **B16**: GraphCanvas 색 토큰화. 관계 탐색 화면에서 색이 그대로인지 눈으로 확인.
8. 새/수정 컴포넌트 테스트. 5176 에서 7개 화면 + 필터 팝오버 + 토스트 + 그래프를 실제로 눌러 본다.

## 7. 범위 제약 — 하지 말 것

- 레이아웃·그리드·반응형·사이드바(B8~B12) 금지 — 3차.
- 아이콘 라이브러리·기타 의존성 추가 금지. 필요한 아이콘만 그린다.
- 상태 변경 UI(TaskQuickActions)는 손대지 않는다 — BE envelope 선행 미결.
- `:root` 기존 토큰 값 변경 금지, 추가만.
- 프론트에서 권한·command 추론 금지. `api.ts` 밖 fetch 금지.

## 8. 검증

```
cd frontend && npx tsc --noEmit (0 에러) + npx vitest run <새 테스트 + 만진 파일의 옆자리 테스트만>.
grep 게이트: grep -o -E '#[0-9a-fA-F]{3,6}\b' src/*.tsx src/chat/*.tsx | wc -l → 0 · awk 'NR>60' src/styles.css | grep -o -E '#[0-9a-fA-F]{3,6}\b' | wc -l → :root 밖 3 이하 유지 · grep -c 'var(--radius-popover)' src/styles.css → 1 이상 · 비테스트 tsx 의 글리프 [×▾▸✓✕⋯←→] → 0 (남으면 각각 왜 남겼는지 — 본문 텍스트의 화살표는 아이콘이 아니다, 목록으로 보고).
전체 빌드·acceptance-e2e 금지 — 사용자 방침. 검증은 1회만
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.
- 보고에 B7·B4·A14·B13·B14·B15·B16 각각 「적용 / 부분(이유) / 대응 자리 없음」 표 + 아이콘 목록 + 새 토큰 목록을 붙인다.

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

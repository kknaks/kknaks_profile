# [frontend] 3차 — 디자인 시스템 v2 적용: 레이아웃·그리드·반응형 (B8·B9·B10·B11·B12·B15 반응형)

너는 **sc-ax `frontend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-ax/orchestration/roles/sc-ax/frontend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/ax-workspace/sc-design-system`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

1차 `7e6fc53` · 2차-a `efc4c94` · 2차-b `d873c00` 이 **커밋돼 있다** — 그 위에서 시작한다. 코디네이터가 API 8001 · 프론트 5176 을 띄워 둔다(백그라운드 워커 없음 — AX turn·업로드는 pending 에 머문다, 정상). `backend/`·`.venv`·`node_modules`·`.scax/` 는 건드리지 마라.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/ax-workspace/sc-design-system/docs/design/design-system-v2.dc.html` ← 시각 규칙의 SoT. 이번 범위 섹션: **`04 — LAYOUT & SPACING`**, **`05 — GRID & PAGE ARCHETYPE`**(Dashboard · List · 8컬럼 그리드 · 세로 리듬), **`15 — RESPONSIVE`**(1920/1440/1280 3단 · 1280 미만 최소폭 안내 · 햄버거 오버레이 · 드로어 전체화면 · 테이블 열 숨김 순서), **`14 — OVERLAY`**(Drawer 840). 리포트와 어긋나면 **디자인이 맞다.**
- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-ax/orchestration/work/sc-design-system/fe-survey-report.md` ← 「바꿔야 할 것」 **B8 · B9 · B10 · B11 · B12 · B15(반응형 열 숨김만)** 와 「디자인이 정의한 것」 (e)·(f). 줄 번호는 세 커밋으로 밀렸다 — 내용으로 찾아라.

**기대는 개념** — 해당 없음. §3 결정을 따른다.

## 2. 배경 / 무엇을 바꾸나

토큰·규칙·컴포넌트는 v2 에 맞췄다. 남은 것은 **화면 골격**이다. 홈이 2열(v2 는 3열 392/600/600), 내 업무가 2열 360+1fr(v2 List 아키타입은 단일 8col 패널), 콘텐츠 최대폭 1640 과 좌우 여백 240/80/48 3단 규칙이 없고, v2 가 지원하지 않는다고 못박은 1100·1024·900·720 브레이크포인트가 있으며 900 에서 사이드바가 v2 `15` 가 금지한 축소형(가로 레일)으로 변한다.
이번이 **디자인 시스템 적용의 마지막 단계**다. 새 화면(설정·캘린더 일/주·자료함)은 만들지 않는다 — 별도 스펙.

## 3. 계약 (결정 2026-09-07 — 이대로)

- **사람 표기 유지**(디자인 확장 결정). 홈 카드·리스트·테이블의 요청자·담당자·참조 열/칩을 없애지 않는다. 열이 늘어 v2 8컬럼에 안 맞으면 **디자인 확장 필요 항목**으로 보고하고, 현재 열을 유지한 채 폭만 맞춘다.
- **B8 홈 3열 392/600/600**, Hero 120(이미 적용). 현재 TodayPage 의 섹션 전부를 v2 `05` Dashboard 의 3열 구성에 **매핑**한다(어느 섹션이 어느 열로 갔는지 표로 보고). 기능·섹션을 지우지 않는다. v2 가 정의한 열에 대응 섹션이 없으면 빈 채로 두지 말고 그 열을 접거나 「디자인엔 있으나 제품엔 없음」으로 보고.
- **B9 List 아키타입 = 단일 8col 패널.** 현재 우측 1fr 이 상세 뷰라면 v2 `14` Drawer(840 · 스크림 · shadow-drawer · p24)로 옮긴다 — 이 리포엔 이미 드로어 패턴(MeetingDrawer · ax-drawer)이 있으니 그 방식을 따른다. 상세 뷰가 아니라 다른 것이면 먼저 물어라.
- **B10**: 사이드바 200 · 콘텐츠 max 1640 · 여백 1920→240 / 1440→80 / 1280→48. 세로 리듬(breadcrumb 38 → 타이틀 66 → 툴바 108 → 패널 140)은 있는 요소 기준으로 맞춘다 — 없는 breadcrumb 을 만들지 않는다.
- **B11**: 1280 미만은 지원하지 않는다 — 최소폭 안내 화면(문구는 `labels.ts`) 하나로 대체하고 1100·1024·900·720 미디어쿼리는 **제거**. 단 그 안에 있던 규칙 중 1280 단에 필요한 것은 1280 쿼리로 옮긴다.
- **B12**: 1280 단에서 사이드바 숨김 + 좌상단 햄버거 → 오버레이(스크림) 로 여는 사이드바. 아이콘만 남기는 축소형 금지(v2 `15`). 드로어는 1280 에서 전체화면 + 스크림 제거. 칸반은 가로 스크롤.
- **B15 반응형**: 테이블 열 숨김 순서 v2 `15`(시작일 → 업무 유형 순, 업무명·상태는 끝까지) — 사람 열은 §3 첫 줄대로 유지하되 어디에 끼울지 보고.
- `api.ts`·viewModels·envelope 로직 불변. 권한·선택지 추론 금지.

## 4. 먼저 읽을 핵심 파일

- `frontend/src/styles.css` — `.app`·`.rail`·`.content`(여백 48 고정), `.home-columns`, `.work-layout`, 미디어쿼리 전부(`grep -n '@media'`), `.ax-drawer`·드로어 규칙.
- `frontend/src/App.tsx` — 앱 셸·사이드바·네비 7개.
- `frontend/src/TodayPage.tsx` — 홈 섹션 목록(B8).
- `frontend/src/MyWorkPage.tsx` · `WorkViews.tsx` · `WorkModals.tsx` — List 2열과 우측 패널의 정체(B9), 칸반·타임라인 뷰.
- `frontend/src/MeetingDrawer.tsx` · `chat/ChatDrawer.tsx` — 기존 드로어 패턴.
- 옆자리 테스트: `App.test.tsx` · `MyWorkPage.test.tsx` · `TodayPage` 관련.

## 5. allowed_paths — 이 밖은 건드리지 마라

- `frontend/src/` (새 컴포넌트·옆자리 테스트 생성 허용)
- 금지: `frontend/src/api.ts` · `frontend/src/viewModels.ts` · `frontend/src/idempotency.ts` · `frontend/package.json` · `frontend/scripts/` · `backend/` · `docs/`

## 6. 구현 단계

1. 디자인 `04`·`05`·`15`·`14` 의 수치를 표로 뽑고, 현재 `@media` 전부와 `.content`·`.home-columns`·`.work-layout` 의 현재값을 옆에 붙인다(보고에 포함).
2. **B10 먼저**: 앱 셸·콘텐츠 폭·여백 3단·1280 쿼리 골격. 이 위에 나머지를 올린다.
3. **B11**: 1100·1024·900·720 쿼리 제거(필요 규칙은 1280 으로 이관) + 최소폭 안내 화면(<1280).
4. **B12**: 1280 사이드바 햄버거 오버레이 + 드로어 전체화면 + 칸반 가로 스크롤.
5. **B8**: 홈 3열 매핑 + 구현.
6. **B9**: 내 업무 단일 패널 + 상세 → 드로어. 우측 패널 정체가 애매하면 **먼저 질문**.
7. **B15**: 테이블 열 숨김 순서.
8. 테스트 갱신·추가. 브라우저에서 **1920 · 1440 · 1280 · 1279** 네 폭으로 7개 화면을 열어 가로 오버플로·겹침·잘림·사이드바 동작·드로어를 확인한다(뷰포트 폭은 Playwright 스크립트나 devtools 로 — 결과는 표로).

## 7. 범위 제약 — 하지 말 것

- 새 화면·새 뷰(설정·캘린더 일/주·자료함·캘린더 좌측 레일 260) 금지 — 별도 스펙.
- 기능·섹션·열 삭제 금지. 사람 표기 삭제 금지.
- 상태 변경 UI(TaskQuickActions) 불변 — BE envelope 선행 미결.
- `:root` 토큰 값 변경 금지, 추가만. 외부 의존성 추가 금지.
- 1280 미만 「지원」을 만들지 않는다 — 안내 화면뿐.

## 8. 검증

```
cd frontend && npx tsc --noEmit (0 에러) + npx vitest run <만진 파일의 옆자리 테스트 + 새 테스트만>.
grep 게이트: grep -n '@media' src/styles.css → 1280 계열과 <1280 안내용 외 0 (남으면 각각 이유) · grep -c '1640' src/styles.css → 1 이상 · 콘텐츠 여백 240/80/48 이 3단에 각각 있는가 · 1920/1440/1280/1279 네 폭 화면 표(가로 스크롤 0).
전체 빌드·acceptance-e2e 금지 — 사용자 방침. 검증은 1회만
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.
- 보고에 B8 열 매핑표 · B9 우측 패널 처리 · 제거한 미디어쿼리와 이관 규칙 목록 · 「디자인 확장 필요」 목록을 붙인다.

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

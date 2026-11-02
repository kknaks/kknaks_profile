# @sc-ax-fe — 기술 스택

## 언어 및 프레임워크
- React 19 + TypeScript 5.9 (strict · isolatedModules · noEmit) + Vite 7
- vitest 3 + @testing-library/react + jsdom · Playwright(e2e 스크립트)
- react-markdown + remark-gfm (본문 렌더) · sigma 3 + graphology (관계 그래프)
- 라우터·상태 라이브러리 없음 — `App.tsx` 가 화면을 나누고, 상태는 컴포넌트·viewModels 에 둔다

## 구조 (frontend/src/)
- 페이지: `TodayPage` · `MyWorkPage` · `CalendarPage` · `OrgPage` · `ProjectPage` · `RelationGraphPage` · `DailyReportPage` · `LoginPage`
- 공용: `Modal` · `DateField` · `Checklist` · `WorkViews` · `WorkModals` · `ActionCenter` · `ActionPreview` · `MeetingDrawer` · `GraphCanvas`
- 계약층: `api.ts`(서버 호출) · `viewModels.ts` · `labels.ts` · `idempotency.ts` · `liveTranscription.ts`
- `chat/` — AX 대화 UI
- 테스트는 옆자리 `*.test.tsx` · e2e 는 `frontend/scripts/`

## 도메인 지식
- 화면·기능 SSOT 는 spec 리포 `products/sc-ax/`(20-spec · 21-screen · 21-html). 이 파일에 요약을 복사하지 않는다 — 낡는다
- 디자인 시스템 참조본은 `docs/design/` — 토큰·컴포넌트 이름을 여기서 가져온다

## 핵심 원칙
- 테스트 먼저 · 최소 변경 · 기존 컨벤션 우선
- 권한은 서버 envelope 가 결정한다. 프론트는 제시된 command 만 그린다

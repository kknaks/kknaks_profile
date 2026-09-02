# Handoff: 태스크 (칸반/테이블 + 상세)

## 읽는 순서 (토큰 절약)
1. 이 README (사양 전부 — 이것만으로 구현 가능)
2. `SPEC_state.md` — 상태 모델·전이·모달 규칙
3. `SPEC_screens.md` — 화면별 레이아웃·컴포넌트 치수
4. HTML은 **필요할 때 해당 구간만** 열어보세요. 통독 불필요.
   - `screens/task-board.dc.html` (445줄) — 칸반/테이블
   - `screens/task-detail.dc.html` (740줄) — 상세

## Overview
mediness 내부 도구 "내 업무 › 태스크"의 2개 화면.
- **보드**: 4열 칸반(대기·진행 중·완료·중단) + 테이블 뷰 토글. 완료가 무한히 쌓이는 문제를 월 이동(‹ 2026년 8월 ›)으로 해결.
- **상세**: 배경/목표 → 할일 목록(체크리스트) → 댓글·진행 로그, 우측 레일에 일정·참고자료·제출자료. WP-126 5상태 모델의 전이 UI와 완료 요약 모달 포함.

## About the Design Files
번들의 `.dc.html`은 **HTML로 만든 디자인 레퍼런스**입니다 — 의도한 외형과 동작을 보여주는 프로토타입이며 그대로 이식할 프로덕션 코드가 아닙니다. 타깃 코드베이스(React 등)의 기존 컴포넌트·패턴으로 **재구현**하세요. 파일은 자체 런타임(`support.js`)에 의존하므로 로직 참고용으로만 읽으면 됩니다.

## Fidelity
**High-fidelity.** 색·타이포·간격·상호작용이 확정값입니다. 아래 토큰과 치수를 그대로 쓰세요.

## Design Tokens
| 용도 | 값 |
|---|---|
| Primary | `#476CFF` / hover `#3554CC` / 연한 배경 `#F0F4FF` / 보더 `#A9BEFF` / 배지 `#DDE6FF` |
| Danger | `#FF4E51` / 배경 `#FFEFEF` / 보더 `#FFD7D7` |
| Success | `#22C55E`, 텍스트 `#15803D`, 배경 `#E7F8EE`, 보더 `#C7EBD6` |
| Warning | 텍스트 `#B45309`, 배경 `#FFF9EC`, 보더 `#FFE6B8` |
| 텍스트 | 본문 `#000` / 서브 `#3E3E3E` / 보조 `#6E6E6E` / 흐림 `#9F9F9F` / 최흐림 `#CFCFCF` |
| 라인·면 | 보더 `#E3E3E3`, 얇은 구분선 `#F3F3F3`, 서브틀 배경 `#FBFBFB` |
| 폰트 | Pretendard Variable (fallback: system-ui) |
| 타입 스케일 | 페이지 타이틀 26/700/-0.02em · 섹션 15/600 · 섹션 라벨 11/600/0.06em/uppercase · 본문 14/1.75 · UI 13.5·13·12.5 · 메타 11.5·11 |
| radius | 카드 12·10, 컨트롤 6, 작은 버튼 5, pill 9999 |
| shadow | 메뉴 `0 8px 24px rgb(0 0 0/.10)` · 모달 `0 20px 60px rgb(0 0 0/.22)` · 오버레이 `rgb(0 0 0/.28)` |
| spacing | 4의 배수. 페이지 좌우 패딩 40, 컬럼 gap 40, 카드 내부 15~16 |
| 셸 | 헤더 52px, 좌측 사이드바 224px, 우측 레일 320px |

## Interactions & Behavior
- 상태 전이: `SPEC_state.md` 참조. 사유 필수 전이(완료·중단·취소)는 모달, 사유 없으면 CTA 비활성(`#DDE6FF`).
- 모든 전이는 진행 로그에 최신순 추가(`상태 변경 · 대기 → 진행 중 · 사유`). 탭 카운트 연동.
- [시작] → 일정의 "시작"에 오늘 날짜 기록(재개해도 최초 시작일 유지). [완료] → "완료" 기록.
- 체크리스트 토글 즉시 진행률 반영(bar `width .25s ease`).
- 완료 컬럼은 선택된 월(‹ ›)로 필터. 화살표는 연/월 롤오버 처리.
- 카드 상태 칩 클릭 → 인라인 상태 변경 메뉴(보드).
- 호버: 리스트 행 `#FBFBFB`, 삭제 아이콘 `#E3E3E3` → `#FFEFEF`/`#FF4E51`.
- 반응형은 범위 밖(데스크톱 전용 내부 도구, 최소 높이 760px).

## State Management
보드: `view('board'|'list')`, `menu(열린 카드 id)`, `y`, `mo`(표시 연·월).
상세: `status`, `done(number[])`, `tab('comments'|'log')`, `modal(null|'done'|'blocked'|'canceled')`, `reason`, `note`(확정된 사유), `startedAt`, `doneAt`, `menuOpen`, `logs[]`.
서버 연동 시 `status/started_at/done_at/logs/checklist`는 서버 소유, 나머지는 로컬 UI 상태.

## Assets
아이콘은 모두 인라인 SVG(stroke 1.6~2, `currentColor`, 12~17px). 외부 이미지·아이콘 폰트 없음. 폰트는 Pretendard CDN.

## Files
```
design_handoff_task/
├─ README.md            ← 사양 (여기부터)
├─ SPEC_state.md        ← 상태 모델·전이·모달
├─ SPEC_screens.md      ← 화면별 레이아웃·컴포넌트
└─ screens/
   ├─ task-board.dc.html   (칸반/테이블)
   ├─ task-detail.dc.html  (상세)
   └─ support.js           (프리뷰 런타임 — 구현 대상 아님)
```

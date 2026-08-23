# Spec Index

규칙: `rules/product-doc-pipeline.md`

> 기능, UX, 정책, acceptance criteria 계약으로 들어가는 map이다.

최종 수정: 2026-07-14

## Data / Domain Boundary

- SPEC에 둠: 사용자-facing 게임 용어, 게임 룰, UX 상태, acceptance criteria.
- SPEC에 두지 않음: 구현 파일 경로, 내부 상태 관리 방식, 작업 순서.

## Scope

### In Scope

- 모바일 웹 로그인/참여/결과 저장.
- DB 기반 daily game registry.
- 12:30 참여 cutoff와 참여 완료 후 꼴찌 탐색.
- 첫 게임인 윷놀이 게이지 게임.

### Out Of Scope

- admin UI.
- 결제/정산/커피 주문 연동.
- PC 전용 최적화.
- 멀티게임 동시 운영.

## Terms

| 용어 | 의미 |
|---|---|
| DailyGame | 날짜별 active game registry record |
| GameResult | 사용자별 당일 게임 결과 |
| `rankValue` | 꼴찌 탐색에 쓰는 게임 공통 순위값 |
| YutGauge | 첫 게임 타입. 게이지 정확도로 윷 결과 확률을 보정 |

## Spec Bundle

| 묶음 | 포함 Spec | 파일 |
|---|---|---|
| Daily Platform | SPEC-001 | [spec-001-daily-game-platform.md](spec-001-daily-game-platform.md) |
| First Game | SPEC-002 | [spec-002-yut-gauge-game.md](spec-002-yut-gauge-game.md) |

## Spec List

| ID | Title | Area | Status | Decision | File |
|---|---|---|---|---|---|
| SPEC-001 | Daily game platform | Platform | draft | DEC-001 | [spec-001-daily-game-platform.md](spec-001-daily-game-platform.md) |
| SPEC-002 | Yut gauge game | Game | draft | DEC-001, DEC-002 | [spec-002-yut-gauge-game.md](spec-002-yut-gauge-game.md) |

## Reading Order

| Area | Spec |
|---|---|
| Platform | SPEC-001 |
| Game | SPEC-002 |

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
|  |  |  |  |

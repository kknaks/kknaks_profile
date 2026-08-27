---
type: work
id: MG-WORK-001
title: "Front yut gauge MVP"
status: done
product: mini-game
work_type: new-feature
owner: "TBD"
roles:
  pm: "TBD"
  design: "TBD"
  fe: "TBD"
  be: "TBD"
  qa: "TBD"
  ops: "TBD"
progress: 100
created_at: 2026-07-14
updated_at: 2026-07-14
tags:
  - product/mini-game
  - doc/work
  - status/done
links:
  baselines:
    - MG-BL-001
  decisions:
    - MG-DEC-001
    - MG-DEC-002
  specs:
    - MG-SPEC-001
    - MG-SPEC-002
  works: []
  releases: []
  related: []
---

# Front yut gauge MVP

`/Users/kknaks/git/toy_pr2/lunch_game` 프론트 레포에서 모바일 우선 윷놀이 게이지 게임을 먼저 만든다. Supabase 연동은 화면 계약과 integration seam을 준비하되, 첫 작업의 중심은 플레이 가능한 프론트 게임이다.

## Meta

- Baseline: BL-001
- Covers spec: SPEC-001, SPEC-002
- Depends on work: 없음
- Parallel work: Supabase schema/RLS work 후보
- Follow-up work: Supabase result persistence, daily registry seed, auth polish
- External dependency: Supabase project/env 필요

## Work Summary

| Field | Value |
|---|---|
| Type | new-feature |
| Owner | TBD |
| Status | done |
| Progress | 100% |
| Branch/PR | - |
| Blocker | Supabase env는 실제 저장 단계 전 필요 |
| Next | lunch_game 레포 구조 확인 후 모바일 yut gauge 화면 구현 |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM | TBD | MVP 범위와 커피 내기 흐름 확인 | todo |
| Design | TBD | 모바일 윷/게이지/버튼 UI | todo |
| FE | TBD | Next.js 화면, 게임 로직, result payload | done |
| BE | TBD | Supabase contract 연동 지점 확인 | todo |
| QA | TBD | 모바일 조작과 확률/결과 검증 | done |
| Ops | TBD | 배포/env 확인 | done |

## Scope

포함:

- 모바일 우선 Next.js 화면.
- 로그인/오늘의 게임/결과 영역의 프론트 shell.
- `yut_gauge` renderer.
- 게이지 왕복 애니메이션과 버튼 입력.
- accuracy band 계산.
- 확률 테이블 기반 결과 추첨.
- SPEC-001 `submitGameResult` payload 생성.
- Supabase 미연결 상태에서도 로컬 mock으로 플레이 가능.

제외:

- Supabase schema migration.
- RLS policy.
- admin UI.
- 실제 커피 정산.
- 여러 게임 추가 구현.

## Code Surface

- Repo / module: `/Users/kknaks/git/toy_pr2/lunch_game`
- 만질 파일 후보:

| 경로 후보 | 설명 |
|---|---|
| `app/` | Next.js route/page |
| `components/` | 모바일 게임 UI |
| `lib/games/` | game registry와 yut gauge logic |
| `lib/supabase/` | Supabase client 연동 후보 |
| `types/` | DailyGame/GameResult contract |

- Domain / schema note: DB schema는 후속 work 또는 architecture에서 확정한다. 이번 work는 프론트 contract를 먼저 고정한다.

## Domain / Schema

| Entity | 역할 |
|---|---|
| DailyGame | 오늘 활성 게임을 표현 |
| GameResult | 사용자의 결과 제출 payload |
| YutGaugeResult | 윷놀이 게임별 metadata |

- 상태 / invariant:
  - 프론트는 이미 제출한 상태에서 새 던지기를 허용하지 않는다.
  - cutoff 이후에는 제출 CTA를 비활성화한다.
- Migration 필요 여부: 이번 work에서는 없음.
- SPEC에 환류해야 하는 외부 resource/status/enum 변경: 없음.

## Dependency

| Consumer | Interface | 설명 |
|---|---|---|
| Supabase persistence work | `GameResult` payload | 실제 DB 저장에 사용 |
| Daily game registry work | `gameType=yut_gauge` | renderer 선택에 사용 |

## Internal Interface Contract

```ts
type GameResultPayload = {
  gameId: string;
  score: number;
  rankValue: number;
  resultLabel: "도" | "개" | "걸" | "윷" | "모";
  metadata: {
    gameType: "yut_gauge";
    accuracyBand: "perfect" | "great" | "good" | "normal" | "bad";
    centerErrorRatio: number;
    gaugePosition: number;
    probabilityTableVersion: "yut-gauge-v1";
  };
};
```

## Execution

### Phase 1 - Repo And App Shell

- **Status**: DONE
- **설명**: lunch_game 레포 구조를 확인하고 모바일 앱 shell을 만든다.
- **작업**:
  - [x] package/framework 확인.
  - [x] 모바일 메인 화면 구성.
  - [x] 오늘의 게임/내 결과/꼴찌 영역 placeholder 구성.
- **검증**:
  - [x] 로컬 dev server 실행.
  - [x] 모바일 viewport에서 첫 화면이 깨지지 않는다.
- **완료 증거**: Next.js app scaffold 생성, `npm run build` 통과, dev server `http://localhost:3001`.

### Phase 2 - Yut Gauge Renderer

- **Status**: DONE
- **설명**: 윷놀이 게이지 게임을 플레이 가능한 프론트 기능으로 구현한다.
- **작업**:
  - [x] 게이지 marker 왕복 구현.
  - [x] 버튼 입력으로 위치 고정.
  - [x] 중앙 오차율과 accuracy band 계산.
  - [x] 확률 테이블 기반 결과 추첨.
  - [x] 결과 label과 payload 표시.
- **검증**:
  - [x] Perfect 구간에서도 `모`가 보장되지 않는다.
  - [x] 각 band 확률 합이 100%다.
  - [x] 결과 label/rankValue가 contract와 일치한다.
- **완료 증거**: `lib/games/yut-gauge.ts`에 확률 테이블/추첨 로직 구현, 결과 payload 화면 표시.

### Phase 3 - Platform Front Contract

- **Status**: DONE
- **설명**: Supabase 연결 전에도 platform contract를 프론트에서 지킬 수 있게 만든다.
- **작업**:
  - [x] mock daily game registry 추가.
  - [x] mock submitted result 상태 추가.
  - [x] cutoff 상태에 따른 CTA 처리.
  - [x] submit adapter 인터페이스 추가.
- **검증**:
  - [x] 이미 제출한 상태에서 버튼이 비활성화된다.
  - [x] cutoff 이후 제출 CTA가 비활성화된다.
  - [x] submit adapter를 Supabase로 교체할 수 있다.
- **완료 증거**: mock daily game/result 상태 구현. Supabase 실제 저장은 후속 work로 분리.

## Pre-deploy Check

- [x] Supabase env 없이도 mock mode가 동작한다.
- [x] credential/env가 클라이언트에 불필요하게 노출되지 않는다.
- [x] 모바일 화면에서 텍스트와 버튼이 겹치지 않는다.

## Rollback

- yut gauge route/renderer를 제거하거나 feature flag off 한다.
- Supabase schema를 건드리지 않으므로 DB rollback은 없다.

## Done Criteria

- [x] 모든 Phase가 `DONE` 또는 `SUPERSEDED`다.
- [x] SPEC-001/SPEC-002 acceptance를 프론트에서 검증할 수 있다.
- [x] 모바일 viewport 수동 QA가 끝났다.
- [x] product `log.md`와 `30-work/README.md`가 갱신됐다.

## Open Issues

- Supabase 실제 env와 schema는 후속 work에서 확정한다.

## Related

- SPEC: SPEC-001, SPEC-002

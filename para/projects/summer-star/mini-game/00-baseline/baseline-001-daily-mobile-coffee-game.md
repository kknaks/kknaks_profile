---
type: baseline
id: MG-BL-001
title: "매일 바뀌는 모바일 커피 내기 미니게임"
status: captured
product: mini-game
created_at: 2026-07-14
updated_at: 2026-07-14
tags:
  - product/mini-game
  - doc/baseline
  - status/captured
links:
  baselines: []
  decisions:
    - MG-DEC-001
    - MG-DEC-002
  specs:
    - MG-SPEC-001
    - MG-SPEC-002
  works:
    - MG-WORK-001
  releases: []
  related: []
---

# 매일 바뀌는 모바일 커피 내기 미니게임

회사에서 매일 점심 전 커피 내기를 하기 위한 모바일 웹 미니게임 플랫폼 아이디어다. 매일 다른 게임을 열 수 있는 구조가 핵심이고, 첫 게임 후보는 윷놀이 기반 게이지 게임이다.

## Raw Input

- 회사에서 커피 내기를 하려고 매일 새로운 미니게임을 한다.
- 기본 흐름:
  1. 로그인
  2. 게임 참여
  3. 게임 결과 기록
  4. 꼴찌 탐색
  5. 매일 점심 12시 30분에 게임 종료
- 첫 게임은 윷놀이 게임이다.
- 모바일로만 쓴다고 보면 된다.
- 프론트는 Next.js, DB는 Supabase를 후보로 본다.
- 게임은 매일 바뀌는 구조로 설계해야 한다.

## First Game Idea: 윷놀이 게이지 게임

화면 구성 초안:

```text
[윷 화면]

[게이지]
[버튼]
```

플레이 방식:

- 사용자는 버튼을 눌러 게이지를 멈춘다.
- 게이지 가운데를 맞출수록 높은 결과(`걸`, `윷`, `모`)가 나올 확률이 커진다.
- 가운데를 잘 맞춰도 `모`가 보장되지는 않는다.
- 결과는 `도`, `개`, `걸`, `윷`, `모` 중 하나다.
- 결과는 당일 게임 결과로 기록된다.

## Product Shape

### Daily Game Platform

- 하루에 하나의 active game이 열린다.
- 게임은 매일 바뀔 수 있어야 한다.
- 게임별 룰과 UI는 달라도, 로그인/참여/결과 기록/꼴찌 탐색/일일 종료는 공통 흐름이다.
- 일일 참여 마감 시각은 12:30이다.

### Mobile First

- 사용 환경은 모바일 웹을 우선한다.
- PC 대응은 필수 범위가 아니다.
- 버튼, 게이지, 결과 확인은 한 손 조작을 기준으로 설계한다.

### Result And Loser Detection

- 참여자의 게임 결과를 저장한다.
- 참여 완료 후 전체 결과와 꼴찌를 볼 수 있어야 한다.
- 꼴찌 판정 기준은 게임별 점수/랭크 규칙이 필요하다.

## Candidate Tech Stack

아직 결정이 아니라 baseline 단계의 후보로 둔다.

| Area | Candidate | Notes |
|---|---|---|
| Frontend | Next.js | 모바일 웹 앱 |
| Database/Auth | Supabase | 로그인, 참여 기록, 결과 저장 후보 |
| Hosting | TBD | Next.js 배포 방식 추후 결정 |

## Questions To Decide Later

| ID | Question | Notes |
|---|---|---|
| Q-001 | 로그인 방식은 무엇인가? | 사내 사용자만, 초대 링크, 이메일, 소셜 로그인 등 |
| Q-002 | 하루 한 번만 참여 가능한가? | 재시도 허용 여부 필요 |
| Q-003 | 12:30 종료 기준 timezone은 무엇인가? | 현재 사용 맥락상 Asia/Seoul 후보 |
| Q-004 | 꼴찌 판정 기준은 낮은 점수인가, 낮은 등급인가? | 게임별 공통 rank contract 필요 |
| Q-005 | 윷놀이 결과는 실제 확률+게이지 보정인가? | 도/개/걸/윷/모 확률 테이블 필요 |
| Q-006 | 매일 바뀌는 게임은 admin이 등록하는가? | 게임 registry/admin 필요 여부 |

## Decision Mapping

| Question | Decision | Status |
|---|---|---|
| Q-001 로그인 방식은 무엇인가? | DEC-001 | resolved |
| Q-002 하루 한 번만 참여 가능한가? | DEC-001 | resolved |
| Q-003 12:30 종료 기준 timezone은 무엇인가? | DEC-001 | resolved |
| Q-004 꼴찌 판정 기준은 낮은 점수인가, 낮은 등급인가? | DEC-001 | resolved |
| Q-005 윷놀이 결과는 실제 확률+게이지 보정인가? | DEC-002 | resolved: 정확도별 확률 테이블 채택 |
| Q-006 매일 바뀌는 게임은 admin이 등록하는가? | DEC-001 | resolved: DB 기반 daily registry 채택, admin UI는 후속 |

## Possible Directions

| 방향 | 설명 | 메모 |
|---|---|---|
| Game registry | 날짜별 active game과 게임 타입을 등록한다 | 매일 바뀌는 구조의 중심 |
| Shared result model | 모든 게임이 공통 result/rank를 반환한다 | 꼴찌 탐색을 단순화 |
| Game-specific UI | 게임별 UI 컴포넌트를 분리한다 | 첫 게임은 yut gauge |
| Daily cutoff job | 12:30에 당일 게임을 종료한다 | Supabase/cron/서버 액션 검토 필요 |

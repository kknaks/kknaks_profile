---
type: decision
id: MK-DEC-005
title: "설정 리디자인 방식 — transfer UI + 백그라운드 수집 큐 + 트레이 오너드로우"
status: accepted
product: mykakao
created_at: 2026-09-03
updated_at: 2026-09-03
tags: [product/mykakao, platform/windows, doc/decision, status/accepted]
links:
  baselines: ["[[baseline-006-settings-redesign-collection-queue]]"]
  decisions: ["[[decision-004-login-state-tracking]]"]
  specs: ["[[spec-005-settings-collection-queue]]"]
  works: []
  releases: []
  related: []
up: []
---

# 설정 리디자인 방식

승인된 목업을 어떻게 구현하고, 수집을 어떻게 큐로 돌리며, 트레이 메뉴를 어떻게 그릴지 정한다.

## Context
- 관련 baseline: [[baseline-006-settings-redesign-collection-queue]]. 승인 목업 = artifact 7340ba99.
- 결정 필요: UI 구조·큐 아키텍처·트레이 렌더 방식.

## 결정 1 — 설정 UI: **카톡 스타일 2탭 + transfer**
- 전체 폭. 탭 `채팅방 설정`(transfer 좌→우) / `채팅방 + 채팅목록`(2-pane).
- 아이콘 = 인라인 SVG. **이모지 금지**. vanilla HTML/JS(빌드 도구 없음). axum 정적 서빙.
- 저장 = 우측 dirty 시 활성화. 취소 = 되돌림.

## 결정 2 — 수집: **DB 백그라운드 큐 (상태 폴링)**
| Option | Pros | Cons | 판정 |
|---|---|---|---|
| A. DB 큐 + 백그라운드 워커 + 상태 폴링 | 저장/수집 분리·재시작 지속·진행 가시화 | 큐 상태기계 필요 | **채택** |
| B. 저장 시 동기 수집 | 단순 | UI 블록·큰 방에서 멈춘 듯 | 기각 |

- 상태: `idle → collecting → done` / 닫힌 방은 `waiting`(BASE-005 트래커가 열림 감지 시 collecting 로) / 실패 `error`.
- 큐는 DB 영속(앱 재시작 후 재개). 세션 키 캐시(DEC-004) 활용해 반복 harvest 회피.
- 수집 = import(main+WAL 델타). "대기 중"은 강제 안 함 — 트래커가 자동 재개.

## 결정 3 — 트레이 메뉴: **오너드로우(owner-draw)**
- MF_GRAYED 는 무조건 회색 → 요구(까만 글씨 + 색 점 + 비선택)를 못 맞춘다. → **MF_OWNERDRAW**.
- WM_MEASUREITEM/WM_DRAWITEM 로 직접 그림:
  - 정보 3항목(로그인 상태 / 로그인 유저 : <닉> / 상태) = **까만(메뉴 기본) 글씨**, 클릭 비활성(하이라이트·커맨드 없음).
  - 상태 점 = **초록 #17B26A(로그인) / 빨강 #E5484D(로그아웃)** 원. 이모지 금지.
- `환경설정`·`종료`는 일반(클릭) 항목 유지.

## 결정 4 — 본인 닉네임 소스 조사
- Profile.nickname 비어있음. 대안 조사: 본인 userId 특정(UserAccounts/로그인 데이터/내 메시지 authorId) → TalkUserDB nickName. 못 구하면 계정 이메일 또는 "(이름 없음)".

## Rationale
- SAC 미건드림·기존 인프라 재사용·이모지 금지(사용자 방침)·키 RAM only.
- 리스크: 본인 닉네임 소스 불확실(best-effort), 오너드로우 다크/하이DPI 렌더.

## Open Questions
| ID | Q | Next |
|---|---|---|
| OQ-1 | 본인 닉네임 견고한 소스 | 구현 중 조사 |
| OQ-2 | 큐 대기→열림 재시도 즉시 vs 배치 | 구현에서 |

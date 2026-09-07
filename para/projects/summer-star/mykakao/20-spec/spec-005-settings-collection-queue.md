---
type: spec
id: MK-SPEC-005
title: "설정 UI 리디자인 + 수집 큐 + 트레이 오너드로우"
status: draft
product: mykakao
created_at: 2026-09-03
updated_at: 2026-09-03
tags: [product/mykakao, platform/windows, doc/spec, status/draft]
links:
  baselines: ["[[baseline-006-settings-redesign-collection-queue]]"]
  decisions: ["[[decision-005-settings-collection-queue]]"]
  specs: ["[[spec-004-login-state-tracking]]"]
  works: []
  releases: []
  related: []
---

# 설정 UI 리디자인 + 수집 큐 + 트레이 오너드로우

승인 목업(artifact 7340ba99)을 win_app 에 구현. 카톡 스타일 2탭 + transfer 선택 + 백그라운드 수집 큐 + 트레이 오너드로우 메뉴 + 본인 닉네임. win_app 확장(SPEC-003/004 위).

> 구현 = Rust `win_app/`. 새 crate 금지(SAC). 커밋·PR 코디.

## Context
- 관련: [[decision-005-settings-collection-queue]] / [[baseline-006-settings-redesign-collection-queue]].
- In: 설정 UI(transfer 2탭) / 수집 큐(상태 폴링) / 트레이 오너드로우 + 색 점 + 본인 닉네임.
- Out: 대화 패턴 추출(후속).

## UX Contract (목업대로)
- 전체 폭. 헤더(옐로우): mykakao + `로그인 유저 · 상태점`.
- **탭1 채팅방 설정** = transfer: 좌"내 카톡 대화방"(클릭→우측 추가) / 우"추적 중인 방"(× 해제 + 상태 뱃지). 하단 `[취소][저장]`, 저장 dirty 활성. 대기 안내 문구.
  - 우측 상태 뱃지: 수집 중(스피너) / 완료(체크·행수) / 대기 중(시계). 아이콘 = SVG, 이모지 금지.
- **탭2 채팅방+채팅목록** = 2-pane. 좌 추적 방(상태 미니표시) / 우 대화. 수집 중이면 스피너("수집 중입니다"), 대기 중이면 안내, 완료면 말풍선 렌더.

## 수집 큐 (DEC-005 결정2)
- 저장(POST) → 새로 추적된 방마다 큐 행 생성 → 백그라운드 처리:
  - 열린 방 → `collecting` → import(main+WAL 델타) → `done`(행수).
  - 닫힌 방 → `waiting` → BASE-005 트래커의 방 열림 이벤트 시 `collecting`.
  - 실패 → `error`(사유).
- 큐 DB 영속(재시작 재개). 세션 키 캐시 활용.

## FE/API Contract
- `GET /api/rooms` 확장: 각 방에 `tracked`(bool) + `collect_status`(idle|collecting|waiting|done|error) + `collected_rows`.
- `POST /api/rooms/select` (기존): 추적 집합 저장 + 새 방 큐 enqueue.
- UI 는 `/api/rooms`(또는 `/api/queue`)를 **폴링**해 상태 뱃지 갱신. SSE(P2) 는 실시간 append 유지.
- 기존 API 계약 불변.

## 트레이 (DEC-005 결정3)
- MF_OWNERDRAW 3정보 항목: 까만(메뉴 기본) 글씨, 비선택. 상태 점 = 초록/빨강 원(WM_DRAWITEM 직접 그림). 환경설정/종료는 일반 항목.
- 본인 닉네임: 소스 조사(userId→TalkUserDB nickName). 못 구하면 이메일/"(이름 없음)".

## Data Contract
- 큐: `room` 확장(`collect_status`,`collected_rows`) 또는 `collect_job(chat_id,status,rows,updated_at)`. 구현 택1. 키 저장 금지.
- 기존 `room.selected`·`last_synced_id` 재사용.

## Validation (개수/유무만, 값 미출력)
- transfer: 좌클릭→우측 추가, dirty 시 저장 활성, 취소 되돌림(육안).
- 저장 → 큐 생성 → 열린 방 수집 완료(행수↑) → UI 상태 뱃지 전이. 닫힌 방 waiting 유지 후 열림 시 자동 collecting(로그).
- 트레이: 까만 글씨 + 초록/빨강 점 + 본인 닉네임(있으면), 정보항목 클릭 안 됨(육안, 코디/사용자).
- 안전: 키/닉/본문 로그·커밋 비노출, 원본 읽기전용, 카톡 무변조, SAC 미변경, 새 crate 0.

## Work Handoff
- **WORK-007**: win_app 확장 — ui/(transfer 2탭, 목업 반영) · 수집 큐(store/server 백그라운드 + /api/rooms 상태 + /api/rooms/select enqueue) · tray.rs 오너드로우(까만 글씨·색 점·비선택) · 본인 닉네임 조사.
- allowed_paths `win_app/`. 커밋·PR 코디.

## Open Questions
| ID | Q | Next |
|---|---|---|
| OQ-1 | 본인 닉네임 소스 | 구현 조사 |
| OQ-2 | 큐 재시도 즉시 vs 배치 | 구현 |

---
type: spec
id: MK-SPEC-004
title: "로그인 상태 트래킹 + 자동 재조정 + 트레이 상태 메뉴"
status: draft
product: mykakao
created_at: 2026-09-03
updated_at: 2026-09-03
tags:
  - product/mykakao
  - platform/windows
  - doc/spec
  - status/draft
links:
  baselines:
    - "[[baseline-005-login-state-tracking]]"
  decisions:
    - "[[decision-004-login-state-tracking]]"
  specs:
    - "[[spec-003-windows-v2]]"
  works: []
  releases: []
  related: []
---

# 로그인 상태 트래킹 + 자동 재조정 + 트레이 상태 메뉴

카톡 3상태(DOWN / UP·로그아웃 / UP·로그인)를 이벤트로 감지하고, 등록된 추적 방을 접근 가능해질 때마다 델타로 자동 따라잡으며, 트레이 메뉴에 로그인 상태를 실시간 표시한다. win_app 확장(SPEC-003 위).

> 구현 = Rust `win_app/`. P1~P3 코드 확장. 새 crate 금지(SAC). 커밋·PR 은 코디.

## Context

- 관련 decision/baseline: [[decision-004-login-state-tracking]] / [[baseline-005-login-state-tracking]]
- 범위(In): 3상태 감지(파일감시/프로세스wait) · 재조정 루프(자동 델타 import) · 세션 키 캐싱 · 트레이 상태 메뉴 + 본인 닉네임 · 웹 ①섹션 상태 반영.
- 범위(Out): 오프라인 파생식(BASE-004 셸빙) · 대화 패턴 추출(후속).

## 상태 모델

```
DOWN         : 카톡 프로세스 없음
UP_LOGGED_OUT: 프로세스 O, 세션 X (계정 DB 미열림)
UP_LOGGED_IN : 프로세스 O, 세션 O (계정 DB 열림, 키 회수 가능)
  room: OPEN(키 회수 가능) / CLOSED
```

## 감지 (DEC-004 결정1·2)

- **로그인/로그아웃**: 계정 폴더(`chatListInfo.edb`·`TalkUserDB.edb` + `-wal`/`-shm`) 파일 감시(notify, P2 확장) + 잠금/키회수 교차검증. 로그인 = 계정 DB 열림. 로그아웃 = 닫힘.
- **방 열림/닫힘·새 메시지**: chat_data 파일 감시(P2).
- **DOWN**: 카톡 프로세스 핸들 `WaitForSingleObject` → 종료 즉시 감지.
- **UP(시작)**: 가벼운 프로세스 존재 체크(수 초) 또는 WMI.
- **harvest(키 회수)는 로그인/방열림 이벤트에서만.** 폴링 금지.
- ⚠ OQ-1: 로그아웃 시 계정 DB close/파일이벤트 발생 여부 **실측 확인** 후 신호 확정.

## 재조정 루프

```
앱 시작       → room.selected 로드 → 상태 판정 → UP_LOGGED_IN 이면 OPEN 방 델타 import + 감시
로그인 이벤트 → 추적 방 중 OPEN 델타 import + 감시 재개
방열림 이벤트 → 그 방(추적 대상이면) 델타 import
방 열린 동안  → 실시간 append (P2)
로그아웃/DOWN → 감시 일시정지 (상태 갱신). 다음 로그인 때 델타로 자동 메꿈
```
- 델타 = `logId > room.last_synced_id`. 커서로 중복 없이 밀린 만큼만(= backfill).
- 추적 방(`room.selected=1`)에만 적용.

## 세션 키 캐싱 (DEC-004 결정3)

- harvest 결과(후보 집합/회수 키)를 **세션 메모리에 캐싱**해 재조정 반복 harvest 회피. 키는 RAM only(디스크 금지).
- 무효화: 카톡 재시작·로그아웃 시 캐시 비움.

## 트레이 상태 메뉴 (DEC-004 결정4)

우클릭마다 재생성, 현재 상태 반영:
```
로그인 상태              (MF_GRAYED)
  로그인 유저 : <본인 닉네임>  (MF_GRAYED, 로그아웃이면 "-")
  상태 : 🟢 로그인 / ⚪ 로그아웃  (MF_GRAYED)
─────
환경설정                 (클릭 → ShellExecuteW 웹페이지)
─────
종료
```
- dot 이모지 우선, 렌더 불량 시 오너드로우(WM_DRAWITEM).
- **본인 닉네임**: `UserAccounts` 로 본인 userId 특정 → TalkUserDB 닉네임. 못 구하면 "-".

## FE/API Contract

- `GET /api/state` 확장: 기존(kakao_running/logged_in/recoverable_rooms) + `state`("DOWN"|"UP_LOGGED_OUT"|"UP_LOGGED_IN") + `me`(본인 닉네임, 있으면). 웹 ①섹션이 이 값 표시.
- 재조정은 서버 내부 자동 — FE 는 상태만 보여주고, ③은 축적된 것 렌더(기존).
- 나머지 API 계약 불변.

## Data Contract

- 신규 스키마 없음 — 기존 `room.selected`(추적 집합)·`room.last_synced_id`(커서) 재사용(DEC-004 결정5). 키는 어디에도 저장 안 함.

## Validation (개수/유무만, 값 미출력)

- 앱 시작 시 추적 방 자동 델타 import 되는지(수동 버튼 없이 행수 증가).
- 카톡 로그아웃→로그인(또는 종료→시작) 후 자동 따라잡기 동작.
- 트레이 우클릭 메뉴에 본인 닉네임 + 상태 dot 표시(육안, 코디/사용자).
- 재조정 반복 시 세션 캐시로 harvest 재실행 안 함(로그/타이밍).
- 안전: 키/닉네임/본문 로그·커밋 비노출, 원본 읽기전용, 카톡 무변조, SAC 미변경.

## Work Handoff

- **WORK-006**: win_app 확장 — state.rs(3상태 감지: 계정 파일감시 + 프로세스 wait + 시작 체크) · 재조정(events → 추적 방 델타 import + 감시) · 세션 키 캐시 · tray.rs 상태 메뉴 + 본인 닉네임 · /api/state 확장 · 웹 ①섹션.
- allowed_paths = `win_app/`. 커밋·PR 코디.

## Open Questions

| ID | Question | Next |
|---|---|---|
| OQ-1 | 로그아웃 시 계정 DB close/파일이벤트 발생? | 구현 중 실측 |
| OQ-2 | 카톡 시작 감지 폴링 vs WMI | 구현에서 택 |
| OQ-3 | dot 이모지 vs 오너드로우 | 구현 실측 |

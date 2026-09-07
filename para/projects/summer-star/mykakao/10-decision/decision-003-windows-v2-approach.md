---
type: decision
id: MK-DEC-003
title: "Windows V2 방식 — 메모리 키 회수 + SQLite 축적 + 파일감시 실시간 + Rust/트레이/HTML"
status: accepted
product: mykakao
created_at: 2026-09-02
updated_at: 2026-09-02
tags:
  - product/mykakao
  - platform/windows
  - doc/decision
  - status/accepted
links:
  baselines:
    - "[[baseline-003-windows-tray-realtime-accumulation]]"
  decisions:
    - "[[decision-001-extraction-approach]]"
  specs:
    - "[[spec-003-windows-v2]]"
  works: []
  releases: []
  related:
    - "[[baseline-004-offline-key-derivation]]"
up: []
---

# Windows V2 방식 — 메모리 키 회수 + SQLite 축적 + 파일감시 실시간 + Rust/트레이/HTML

Windows 카톡 대화를 선택 방 단위로 과거 복호·가져오고 실시간으로 축적하기 위한 네 갈래 방식을 확정한다.

> baseline 의 날것 입력을 spec 으로 내리기 전에 적용 방향을 정하는 문서.

## Context

- 관련 baseline: [[baseline-003-windows-tray-realtime-accumulation]]
- 결정이 필요한 이유: Windows 는 macOS(DEC-001)와 저장구조·키·플랫폼 제약이 달라(spike 1·2·3),
  키 획득·저장소·실시간·UI 를 새로 정해야 코드로 내릴 수 있다.

## 근거 개념

없음 — 실측(spike)에 기반한 방식 선택이다. 실측 상세는 baseline-003 §Context.

## 결정 1 — 키 획득: **실행 중 메모리 회수**

| Option | Pros | Cons | 판정 |
|---|---|---|---|
| A. 메모리 raw key 회수 (passive VM_READ) | SAC 안전·실증됨(1455행) | **카톡 실행 중** 전제, 방 열림 필요 | **채택** |
| B. 오프라인 파생식 유도 | 카톡 미실행도 가능 | 파생식 미회수·RE 무거움 | 백로그([[baseline-004-offline-key-derivation]]) |
| C. Frida 등 주입 후킹 | 직접 포착 | **SAC 차단(확증)** | 기각 |

- 채택 A. 트레이 앱이 카톡과 상주하는 전제라 실행 중 회수로 충분. macOS 도 기기 종속이었으니 동급.

## 결정 2 — 축적 저장소: **로컬 SQLite**

| Option | Pros | Cons | 판정 |
|---|---|---|---|
| A. 로컬 SQLite | 의존성 0·단일 파일·SQL 분석 즉시·트레이 앱에 적합 | 대규모 동시성엔 약함(무관) | **채택** |
| B. Postgres + Docker | 견고 | 이 머신 docker 미설치·과임 | 기각 |

- 원본 mykakao 는 결과 DB 저장을 **명시적으로 제외**(WORK-002)했으나, V2 는 **영속 축적이 핵심**이라 저장소를 새로 도입한다.
- 우리 저장소는 카톡 원본과 분리된 별도 SQLite. 원본은 **읽기 전용**.

## 결정 3 — 실시간: **파일 변경 감지(-wal watch) → 델타 복호 → SQLite append → SSE**

| Option | Pros | Cons | 판정 |
|---|---|---|---|
| A. 파일 변경 감지(FileSystemWatcher) | 이벤트 기반·저지연·주입 아님(SAC 무관) | WAL 커밋 타이밍 의존 | **채택** |
| B. 고정 간격 폴링 | 단순 | 둔함·헛돌기 | 보조(폴백) |
| C. 함수 주입 후킹 | 즉시성 | **SAC 차단** | 기각 |

- 채택 A. `chatLogs_<chatId>.edb-wal` 변경 시 `logId` 커서 이후 새 행만 복호해 append.
- B 는 감시가 불안정한 환경의 폴백으로만.

## 결정 4 — UI: **트레이 앱 + localhost HTML** (Rust axum 서빙)

- 트레이 아이콘 클릭 → 로컬 **Rust axum** 이 서빙하는 HTML 을 기본 브라우저로 연다.
- 설정 페이지 3섹션(로그인 상태 감지 / 대화방 설정 / 채팅 내역 2-pane). baseline-003 §UX 구조.
- HTML/JS 프론트는 macOS mykakao `frontend/` 꼴 재사용(언어 무관).

## 결정 5 — 구현 언어·배치: **Rust**, 같은 레포 **`win_app/`**

| Option | Pros | Cons | 판정 |
|---|---|---|---|
| A. Rust (axum·rusqlite bundled-sqlcipher·notify·windows·tray-icon) | 단일 네이티브 exe(~5MB)·정적 SQLCipher·트레이 상주에 유리·의존성 0 | 초기 구현 비용, spike 코드 포팅 | **채택** |
| B. Python + PyInstaller | spike 코드 재사용 | exe ~100MB·느린 시작·AV 오탐·휠 의존 | 기각 |

- **배치**: 별도 레포 아님. mykakao 레포 안 **`win_app/`** 디렉토리(Rust). macOS 원본은 `backend/`(Python) 그대로 — 두 플랫폼이 한 레포에 나란히.
- **복호**: `rusqlite` + `bundled-sqlcipher` 로 SQLCipher 를 exe 에 정적 링크(Python 의 sqlcipher3-wheels 휠 의존 제거).
- **spike 코드**(Python `key_recover.py` 등)는 **참조**로만 — 알고리즘(VM_READ 스캔·SQLCipher v4 HMAC 검증·compat4 파라미터)을 Rust 로 포팅.
- ⚠ **SAC 는 언어로 안 풀린다**: 서명 없는 exe 는 Python/Rust 무관하게 SAC/SmartScreen 이 경고·차단. 본인 기기 개인용이라 직접 allow-list. Rust 이점은 서명 면제가 아니라 작고 평판 좋은 네이티브 exe.

## Rationale

- 판단 기준: **SAC 을 안 건드리고**(끄면 클린설치), **실증된 방법 우선**, **의존성 최소**.
- 리스크:
  - 카톡 버전 업데이트 시 키 상주 위치·스키마 변화 → 회수기·모델을 spec 에 격리.
  - 방이 닫히면 키 zeroize → 대상 방 열림 유지 필요(운영 주의, spec Open Questions).
  - 파일감시가 놓치는 커밋 → 주기 재동기(폴백 폴링)로 보정.

## Open Questions

| ID | Question | Next |
|---|---|---|
| OQ-1 | 여러 방 동시 축적 시 키 상주 타이밍(닫힘 zeroize) 대응 | Phase 2(실시간) 설계 시 |
| OQ-2 | 카톡 미실행 시 UX — 안내만 vs 파생식 독립(BASE-004) | 축적 운영 후 |
| OQ-3 | 대화 패턴 추출의 구체 산출(빈도·시간대·감정·토픽) | 축적 데이터 쌓인 뒤 별도 baseline |

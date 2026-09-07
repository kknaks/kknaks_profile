---
type: spec
id: MK-SPEC-003
title: "Windows V2 — 방 선택·과거 복호·실시간 축적·트레이 UI"
status: draft
product: mykakao
created_at: 2026-09-02
updated_at: 2026-09-02
tags:
  - product/mykakao
  - platform/windows
  - doc/spec
  - status/draft
links:
  baselines:
    - "[[baseline-003-windows-tray-realtime-accumulation]]"
  decisions:
    - "[[decision-003-windows-v2-approach]]"
  specs:
    - "[[spec-001-message-extraction]]"
  works: []
  releases: []
  related:
    - "[[baseline-004-offline-key-derivation]]"
---

# Windows V2 — 방 선택·과거 복호·실시간 축적·트레이 UI

본인 Windows 카카오톡의 로컬 SQLCipher 대화 DB에서, 선택한 방의 과거 히스토리를 복호해 로컬
SQLite에 저장하고, 파일 변경 감지로 새 메시지를 실시간 축적하며, 트레이 앱이 여는 localhost HTML로
로그인 상태·방 선택·채팅 내역을 다룬다. 목적은 대화 패턴 추출의 원천 데이터 축적이다.

> 구현 = **Rust**, 같은 레포 **`win_app/`** 디렉토리(DEC-003 결정5). 백엔드 axum, 복호·저장 rusqlite(bundled-sqlcipher), 파일감시 notify, 메모리 windows crate.
> 본 제품의 "백엔드"는 키 회수·복호·축적 메커니즘 그 자체이므로, 그 방법을 BE Contract에 상세히 둔다(SPEC-001과 동일 방침).
> 키는 실행 중 카톡 메모리에서 회수한다(DEC-003). 오프라인 파생식은 범위 밖([[baseline-004-offline-key-derivation]]).

## Context

- 관련 decision/baseline: [[decision-003-windows-v2-approach]] / [[baseline-003-windows-tray-realtime-accumulation]]
- 범위(In/Out):
  - In: 방 목록·선택 / 선택 방 과거 히스토리 복호·저장 / 파일감시 실시간 축적 / 채팅 내역 뷰(우리 SQLite) / 로그인 상태 감지 / 트레이 앱.
  - Out: 오프라인 파생식(BASE-004), 대화 패턴 추출 알고리즘(후속 baseline), AI 요약(BASE-002는 macOS 계열), 일정 파싱/캘린더.
- 플랫폼: Windows 11, 카톡 26.4.0.5128. 구현 **Rust**(axum·rusqlite+bundled-sqlcipher·notify·windows·tray-icon), 배치 `win_app/`. SAC ENFORCE(끄지 않음 — 서명없는 exe 는 직접 allow-list).

## 단계 (Phase)

- **P1 — 방 선택 + 과거 복호·저장**: 방 목록, 선택, 선택 방 chatLogs 복호 → SQLite upsert, 채팅 내역 뷰.
- **P2 — 실시간 축적**: `-wal` 파일감시 → 델타 복호 → SQLite append → SSE 스트림.
- **P3 — 트레이 앱 + 패턴 추출 진입**: 트레이 아이콘→설정, 로그인 상태 감지 상시화, (패턴 추출은 후속).

## UX Contract

트레이 아이콘 클릭 → 로컬 FastAPI 서빙 HTML을 기본 브라우저로 연다. 설정 페이지 3섹션:

1. **로그인 상태 감지** — 카톡 실행/로그인 여부, 현재 키 회수 가능한(열린) 방 수. 미실행이면 안내 배너("카톡을 실행하세요").
2. **대화방 설정** — 방 목록(제목·chatId·선택 토글). 선택 방 = 과거 import 대상 + 실시간 감시 대상. 선택 상태는 우리 저장소에 영속.
3. **채팅 내역** — 우리 SQLite 축적본. "대화방 | 대화기록" 2-pane(좌 방 목록 / 우 말풍선·시간·작성자). macOS index.html 꼴, 소스만 우리 DB.

## User Scenario

1. 사용자가 카톡 로그인 상태로 트레이 아이콘 클릭 → 설정 페이지 열림.
2. ①에서 "카톡 실행 중, 방 N개 키 회수 가능" 확인.
3. ②에서 여친 방을 선택 → "과거 가져오기" → 그 방 chatLogs 복호되어 SQLite에 저장, 진행률 표시.
4. ③에서 저장된 대화가 2-pane으로 보임.
5. 이후 카톡에 새 메시지가 오면(그 방) 파일감시가 잡아 SQLite에 append + 화면에 실시간 반영(P2).

## FE Contract

정적 HTML + vanilla JS(빌드도구 없음, 원본 mykakao 규약). **Rust axum 이 `win_app/ui/` 를 정적 서빙**. API:

| Method · Path | 용도 | 응답(요지) |
|---|---|---|
| GET `/api/state` | 로그인/실행 상태 감지 | `{kakao_running, logged_in, recoverable_rooms:[chatId], account?}` |
| GET `/api/rooms` | 방 목록(카톡 원본) | `[{chat_id, title, member_count?, selected}]` |
| POST `/api/rooms/select` | 수집 방 설정 | body `{chat_ids:[...]}` → `{ok, selected:[...]}` |
| POST `/api/import` | 선택(또는 지정) 방 과거 복호·저장 | body `{chat_id?}` → `{ok, imported:{chat_id:count}}` (진행은 SSE 가능) |
| GET `/api/messages?chat_id=&after=&limit=` | 우리 SQLite 축적본 조회 | `[{log_id, author_id, author_name?, type, sent_at, text}]` |
| GET `/api/stream?chat_id=` | 실시간 새 메시지(P2) | SSE `event: message` payload=위 행 shape |

- SSE 이벤트명·페이로드 키는 위를 계약으로 고정. FE는 BE를 추측해 우회하지 않는다(원본에서 겪은 함정).
- 값(대화 본문)은 로컬에서만 렌더. 외부 전송 없음.

## BE Contract (메커니즘 상세 — 이 제품의 핵심)

### 경로·대상
- 계정 폴더: `%LOCALAPPDATA%\Kakao\KakaoTalk\users\<40hex>\` (계정 해시는 **자동 탐색** — 하드코딩 금지).
- 방 DB: `chat_data\chatLogs_<chatId>.edb` (+ `-wal`/`-shm`). 방 목록: `chatListInfo.edb`/`chatRooms`. 유저: `TalkUserDB.edb`/`talkUser`.

### 키 회수 (DEC-003 결정1) — 실행 중 메모리, passive
- Rust `windows` crate 로 카톡 PID의 PRIVATE RW 메모리를 `ReadProcessMemory`로 **읽기만**(주입·쓰기 없음 → SAC 무관).
- 고엔트로피 32B 윈도우를 후보 키로 수집 → 각 DB의 **page1(4096B)** 로 **SQLCipher v4 page-1 HMAC-SHA512**(Rust `hmac`+`sha2`, PBKDF2 `pbkdf2`) 검증(후보당 HMAC 1회)으로 진짜 키 판정.
- 회수 키는 **파일(방)별 raw key(32B)**. 공유 마스터 키 아님. 키는 **저장하지 않는다**(세션 메모리만, 필요 시 즉시 재회수).
- 알고리즘은 spike3 Python `key_recover.py` 를 **참조로 Rust 포팅**.

### 복호 파라미터 (spike 3 실측 확정)
- **`rusqlite` + feature `bundled-sqlcipher`**(SQLCipher exe 정적 링크): `PRAGMA key="x'<64hex raw>'"`, `PRAGMA cipher_compatibility=4`, page 4096, reserve 80(IV16+HMAC-SHA512 64).
- 원본은 **읽기 전용**. 복호 작업은 **사본**(임시)으로. 사본은 작업 후 삭제.

### 과거 import (P1)
- 대상 방: 키 회수 → `chatLogs_<chatId>.edb` 복호 → `SELECT ... FROM chatLogs WHERE logId > <last_synced>` → 우리 SQLite에 upsert → 커서 갱신.

### 실시간 축적 (P2) — DEC-003 결정3
- 선택 방들의 `chat_data` 경로를 Rust **`notify`** crate(내부 `ReadDirectoryChangesW`)로 감시.
- `chatLogs_<chatId>.edb-wal` 변경 이벤트 → 델타 복호(logId > 커서) → SQLite append → `/api/stream` SSE push.
- 감시 누락 보정: 주기적 재동기(폴백 폴링) 옵션.

### 로그인 상태 감지
- 카톡 프로세스 존재 + 계정 폴더 존재 → `logged_in`. `recoverable_rooms` = 현재 키가 메모리에 상주(=열린) 방.

### 안전 (불변)
- 카톡 크래시·변조·종료 **금지**. SAC **미변경**. 원본 DB/레지스트리 **읽기만**.
- 키·user_id·device UUID·**대화 본문**을 로그·리포트·커밋에 남기지 않는다. 우리 SQLite는 로컬 저장이며 외부 전송 없음.

## Data Contract (우리 SQLite 축적 스키마 — 초안, rusqlite)

```sql
CREATE TABLE room(
  chat_id        INTEGER PRIMARY KEY,
  title          TEXT,
  selected       INTEGER DEFAULT 0,       -- 수집 대상 여부
  last_synced_id  INTEGER DEFAULT 0,      -- 마지막으로 가져온 logId(커서)
  updated_at     TEXT
);
CREATE TABLE message(
  chat_id    INTEGER,
  log_id     INTEGER,                     -- 카톡 logId
  author_id  INTEGER,
  msg_type   INTEGER,
  sent_at    INTEGER,                     -- 카톡 sendAt(epoch)
  text       TEXT,
  PRIMARY KEY(chat_id, log_id)            -- 멱등 upsert(중복 방지)
);
CREATE TABLE author(
  chat_id   INTEGER, author_id INTEGER, nickname TEXT,
  PRIMARY KEY(chat_id, author_id)
);
```

- 카톡 원본 스키마는 `chatLogs(logId, chatId, authorId, type, sendAt, message…)` — 컬럼 매핑은 구현에서 확정(복호 후 실제 컬럼 확인).
- 키는 **어디에도 저장하지 않는다**.

## Validation

- P1: 선택 방 `/api/import` → `/api/messages`가 저장 행수 반환. 복호 사본은 삭제됨. 원본 mtime은 카톡 자신 외 변화 없음.
- P2: 카톡에서 그 방에 새 메시지 → 파일감시 이벤트 → `/api/stream`에 신규 행 도착 + SQLite 행 증가.
- 키·본문이 로그/응답 헤더/커밋에 노출되지 않음(마스킹 확인).

## Work Handoff

- **WORK-003 (P1)**: Rust BE = 키 회수(spike3 참조 포팅) + rusqlite 복호 + SQLite 저장 + axum `/api/state|rooms|rooms/select|import|messages`. FE = 설정 3섹션 + 2-pane 뷰(`win_app/ui/`).
- **WORK-004 (P2)**: Rust BE = notify 파일감시 → 델타 복호 → append + `/api/stream` SSE. FE = 실시간 반영.
- **WORK-005 (P3)**: 트레이 앱(`tray-icon` crate) + 로그인 상태 상시화. (패턴 추출은 후속 baseline.)
- 코드 레포 = mykakao, 디렉토리 = **`win_app/`**(Rust). macOS `backend/`(Python)는 불변. 워커 allowed_paths = `win_app/`. 문서는 코디 소유.
- 디렉토리 초안: `win_app/Cargo.toml` · `win_app/src/`(main·server·kakao(mem key·decrypt)·store·watch) · `win_app/ui/`(html/js).

## Open Questions

| ID | Question | Next |
|---|---|---|
| OQ-1 | 방 닫힘 시 키 zeroize → 여러 방 동시 축적 유지 방법 | P2 설계 |
| OQ-2 | 트레이 프레임워크 선택(pystray vs 기타) + 패키징 | P3 |
| OQ-3 | 카톡 원본 chatLogs 실제 컬럼/타입(type 코드·삭제 메시지) 매핑 | P1 복호 직후 확정 |

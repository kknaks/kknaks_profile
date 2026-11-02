---
type: baseline
id: MK-BASE-003
title: "Windows V2 — 트레이 앱 + 방 선택 + 과거 히스토리 + 실시간 축적 (대화 패턴 추출)"
status: accepted
product: mykakao
source:
  type: idea
  ref: "사용자 구두 요청 2026-09-02 (Windows 이식 + V2 설계)"
links:
  baselines:
    - "[[baseline-001-kakao-message-extraction]]"
    - "[[baseline-004-offline-key-derivation]]"
  decisions:
    - "[[decision-003-windows-v2-approach]]"
  specs:
    - "[[spec-003-windows-v2]]"
  works: []
  releases: []
  related: []
created_at: 2026-09-02
updated_at: 2026-09-02
tags:
  - product/mykakao
  - platform/windows
  - doc/baseline
  - status/accepted
---

# Windows V2 — 트레이 앱 + 방 선택 + 과거 히스토리 + 실시간 축적

Windows 카카오톡의 로컬 암호화 대화 DB에서, 선택한 방의 **과거 히스토리를 복호해 가져오고** +
**실시간으로 새 메시지를 감지해 로컬 DB에 계속 축적**하는 트레이 앱. 목적은 특정 방(예: 연인)
대화를 지속 수집해 **대화 패턴을 추출**하는 것이다.

> 아직 결정하지 않은 날것의 입력이다. 정리보다 보존이 우선이다.
> BASE-001(macOS 추출)의 Windows 판이자 확장이다 — 추출을 넘어 **영속 축적 + 실시간**이 새 축.

## Raw

- 상태 표시줄(트레이)에 앱이 상주. 설정을 열면 **localhost HTML** 이 뜬다.
- HTML 에서 **가져올 카톡 방을 선택**한다.
- 기능 두 축:
  1. **로그인/기동 시 선택된 방의 과거 히스토리 가져오기** (일괄 복호).
  2. **실시간 채팅 로그 감지 → 우리 DB에 축적** (새 메시지가 오면 계속 쌓기).
- 목적: 나와 여자친구 대화를 계속 쌓아 **대화 패턴을 추출**한다.
- 본인 기기에서 본인만 쓴다. 외부 배포/공유 없음.

## Context — Windows 실측 (spike 1·2·3, 2026-09-02)

이 머신(Windows 11)에서 카톡 **26.4.0.5128** 을 대상으로 3회 탐색해 확정한 사실:

- **대화는 로컬에 있다** (spike 1의 "로컬 미영속" 가설은 오답으로 정정됨).
  - 로그인 후 계정 폴더 `%LOCALAPPDATA%\Kakao\KakaoTalk\users\<40hex>\chat_data\` 에
    **방별 DB** `chatLogs_<chatId>.edb` 로 존재. 한 방 **1455행**(과거 히스토리) 실복호 확인.
  - 그 외 `chatListInfo.edb`·`TalkUserDB.edb`·`CalendarDB.edb`.
- **암호화 = SQLCipher v4** (엔트로피 7.997). 파라미터 확정: `cipher_compatibility=4`, page 4096,
  reserve 80(IV16 + HMAC-SHA512 64), **raw-key(32B) 모드**.
- **스키마는 macOS 와 다르다**: `chatRooms`/`chatLogs`(logId·chatId·authorId·type·sendAt…)/`talkUser`.
  (macOS 는 `NTChatRoom`/`NTChatMessage`/`NTUser`, 단일 78-hex DB.)
- **키는 방(파일)마다 다르다** — 공유 마스터 키 아님.
- **키 획득 방법 = 실행 중 메모리 회수**: 카톡이 켜져 그 방 DB 가 열려 있으면, 그 SQLCipher raw
  key(32B)가 프로세스 메모리에 상주 → **passive `VM_READ`(주입 없음, SAC 안전)** 로 회수 →
  디스크 `.edb` 전체 복호. (spike 3에서 8개 DB 키 회수 + 실복호 실증.)
- **Frida 등 코드 주입은 불가** — Smart App Control(SAC ENFORCE)이 서명 없는 DLL 로드를 차단
  (CodeIntegrity 3077/3033 로그 확증). SAC 은 끄지 않는다(끄면 클린 설치 전까지 못 켬).
- **오프라인 파생식(device/user → key)은 미회수** — ground-truth 8쌍으로 PBKDF2/해시 가설
  전수했으나 전부 불일치. → 별도 백로그 [[baseline-004-offline-key-derivation]].

## Why It Matters

- macOS 데모(BASE-001)는 단발 추출이었다. V2 는 **지속 축적 + 실시간**이라 "대화 패턴 추출" 같은
  분석의 원천 데이터가 시간에 따라 쌓인다 — 이게 새 가치다.
- 이식 가능성은 이미 실증됐다(1455행 복호). "된다/안 된다"는 **된다**로 닫혔고, 단
  **카톡 실행 중** 전제가 붙는다(macOS 도 기기 종속이었으니 동급).

## Possible Direction (확정된 결정 — decision 으로 내림)

사용자와 2026-09-02 문답으로 아래를 확정 (decision-003 에서 정식화):

- **키 = 실행 중 메모리 회수** (파생식은 백로그 BASE-004 로 분리, 이번 범위 밖).
- **축적 저장소 = 로컬 SQLite** (원본 mykakao 는 DB 저장 제외였으나 V2 는 영속 저장이 핵심).
- **실시간 = 파일 변경 감지** — `chatLogs_<chatId>.edb-wal` 을 OS 파일시스템 감시로 지켜보다
  변경 이벤트 시 새 행만 복호해 SQLite 에 축적 → SSE 로 화면 push. (폴링보다 이벤트 기반이 우수,
  주입 아니라 OS 알림이라 SAC 무관. 함수 주입 후킹은 SAC 로 불가.)
- **구현 = Rust** (백엔드 axum + rusqlite(bundled-sqlcipher) + notify + windows crate), **같은 레포 `win_app/` 디렉토리**. 단일 네이티브 .exe.
- **UI = 트레이 앱 + localhost HTML** — Rust axum 이 localhost HTML+API+SSE 서빙, 트레이 아이콘 클릭 시 기본 브라우저로 연다. HTML/JS 프론트는 macOS mykakao 꼴 재사용(언어 무관).
- **범위 = 단계 진행** (1: 방 선택 + 과거 복호·저장 / 2: 실시간 파일감시 축적 / 3: 트레이 + 패턴 추출).

## UX 구조 (사용자 확정 2026-09-02)

설정 = **별도 localhost HTML 페이지** (로컬 **Rust axum** 서빙). 트레이 앱은 아이콘 클릭 시 이 페이지를 기본 브라우저로 연다. HTML/JS 프론트는 macOS mykakao `frontend/` 꼴 재사용.

```
작업표시줄(트레이) 아이콘 클릭
   └─▶ localhost HTML (설정 페이지)
         ├─ ① 로그인 상태 감지 — 카톡 실행·로그인 여부 + 현재 키 회수 가능한 방(DB 열림). 미실행이면 안내("카톡 켜세요").
         ├─ ② 대화방 설정      — 방 목록에서 수집할 방 선택. 선택 방 = 과거 import 대상 + 실시간 파일감시 대상.
         └─ ③ 채팅 내역        — 우리 SQLite 축적본 보기. "대화방 | 대화기록" 2-pane(macOS index.html 꼴, 소스만 우리 DB).
```

- ③ 채팅 내역의 소스는 **우리 축적 SQLite** (카톡 원본 실시간 복호 뷰가 아님) — import 된 과거 + 실시간 append 가 쌓인 것.
- 방 목록(②)은 카톡 `chatRooms`/`chatListInfo` 에서 읽어 표시(선택 UI). 선택 상태는 우리 설정에 저장.

## 아직 안 정한 것

- 대화 패턴 추출의 구체 산출(무엇을 뽑나 — 빈도·시간대·감정·토픽?) — 축적이 돌아간 뒤 별도 baseline.
- 카톡이 닫혀 있을 때(키 없음)의 UX — 안내만 할지, 파생식(BASE-004)로 독립할지.
- 여러 방 동시 축적 시 키 상주 타이밍(방이 닫히면 SQLCipher 가 키 zeroize) 대응.

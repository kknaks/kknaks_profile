---
type: baseline
id: MK-BASE-004
title: "오프라인 SQLCipher 키 파생식 회수 (고도화 백로그 — RE)"
status: deferred
product: mykakao
source:
  type: observation
  ref: "spike 3 (poc-windows-key-recover) 2026-09-02"
links:
  baselines:
    - "[[baseline-003-windows-tray-realtime-accumulation]]"
  decisions: []
  specs: []
  works: []
  releases: []
  related: []
created_at: 2026-09-02
updated_at: 2026-09-02
tags:
  - product/mykakao
  - platform/windows
  - doc/baseline
  - status/deferred
  - kind/research
---

# 오프라인 SQLCipher 키 파생식 회수 (고도화 백로그)

Windows 카톡 `chatLogs_*.edb` 의 SQLCipher 키를 **device/user 식별자에서 오프라인으로 유도**하는
파생식(공식)을 회수하는 과제. **이번 V2 범위 밖 — 로그성 보존.** V2 는 실행 중 메모리 회수로 간다.

> 관찰·미결의 보존이 목적. 착수하려면 별도 decision 으로 승격한다.

## 왜 미뤘나

- V2(BASE-003)는 트레이 앱이 카톡과 함께 상주하는 전제 → **실행 중 메모리 키 회수로 충분**하고 이미 실증됨.
- 파생식은 **오프라인 이식**(카톡 꺼진 채 파일만으로 복호)에만 필요. 지금 필요 없음.
- 회수 비용이 크다(언패킹·RE·서명 도구). 가치 대비 후순위.

## 무엇을 관찰했나 (spike 3, 재현 가능)

- 실행 중 카톡 메모리에서 각 `.edb` 의 **raw key(32B)** 회수 성공 → 실복호 실증(1455행).
- 그러나 **파생식은 미회수**: ground-truth 8쌍 (salt, key) + 식별자(dev_id·sys_uuid·hdd_serial·
  MachineGuid·계정폴더 40hex 해시)로 아래 가설 전수 → **전부 불일치**.
  - `key == PBKDF2-{SHA512/256/1}(passphrase=식별자, salt=file[:16], iter∈{256000,64000,4000})`
  - `key == sha256/sha512/hmac(식별자 ⊕ salt 조합)`, 식별자 2원 조합 포함.
- 결론: 키는 이 식별자들의 단순 KDF/해시가 **아니다**. passphrase 조립 루틴이 더 복잡(추가 상수·
  순서·중간 해시)하거나, 카톡이 자체 계산한 raw key.

## 남은 두 경로 (착수 시)

1. **정적 RE** — `KakaoTalk.exe` 는 디스크상 패킹(SQLite 문자열 0개). **실행 중 메모리에서 언패킹
   코드를 passive VM_READ 로 덤프**(SAC 안전) → **Ghidra** 로 `sqlite3_key` 인자 조립부 역추적.
2. **서명 계측** — **WinDbg**(Microsoft 서명 → SAC 이 Frida 처럼 막지 않을 가능성)로 `sqlite3_key`
   호출부 BP → passphrase 원값 포착 후 그 값을 만든 코드 추적.

둘 다 무거운 도구 설치 필요(설치 전 사용자 승인). **Frida 등 서명 없는 주입은 SAC 로 불가**(확증).

## 착수 조건

- 오프라인 복호가 실제 요구로 올라올 때 (예: 다른 기기로 DB 옮겨 분석, 카톡 미실행 상태 수집).
- 그때 이 문서를 decision 으로 승격하고 spike 4 를 발주한다.

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


## spike 4 진전 (2026-09-03) — 메커니즘 규명, 정적 RE 는 막힘

passive 메모리 RE 로 **파생 메커니즘을 규명**했다(값 비노출):
- 언패킹 코드 문자열: `sqlite3_key`·`PBKDF2`·`AES-256`·`PRAGMA key`·`cipher_compatibility`·`%s%s`·`CryptUnprotectData`.
- **키 = SQLCipher raw-key + PBKDF2**, **passphrase 는 `%s%s` 로 두 조각 조립**(한 조각이 미상), 그리고 **DPAPI(`CryptUnprotectData`) 사용**.
- 확장 배터리(UTF-8/UTF-16LE/hex × PBKDF2 SHA256/512 × iter{1..256000} × salt 변형 + HKDF + HMAC + sha 조합, 단일 27 + 조합 60폼)로 **단순 식별자 KDF 전부 배제** — spike3 재확인.
- **미회수 이유**: passphrase 의 미상 성분이 **DPAPI 보호값 or 런타임 조립값**이라 정적 문자열론 안 잡힌다. DPAPI blob 은 디스크/레지스트리에 없음(런타임 조립 추정).

→ 판정 (C) 정적 막힘. **남은 유일 경로 = WinDbg**(MS 서명 → SAC 안전, Frida 와 달리 통과)로 `sqlite3_key`·`CryptUnprotectData` BP 걸어 **런타임 passphrase/DPAPI 값 포착**. (2026-09-03 사용자 승인 → 진행.)


## spike 4b 결론 (2026-09-03) — anti-debug 벽, 파생식 셸빙

WinDbg(cdb) 설치·attach 는 됐으나 **KakaoTalk 이 강력한 anti-debug 를 갖고 있다**: BP 상주 시
EmbeddedBrowserWebView 에서 second-chance AV 로 **자폭(3회 재현)**. anti-debug 우회는 안전규칙상
금지 → passphrase/DPAPI 미포착. 값유출 0.

**정리**: 카톡은 **DPAPI 보호 + anti-debug 자폭** 두 겹으로 키 추출을 방어한다(하드닝된 타겟).
정적(문자열)·동적(WinDbg) 두 경로 모두 막힘. 남은 건 Ghidra 정적 RE 이나, DPAPI 런타임 값이
정적으론 안 잡혀 마지막 조각이 안 닫힐 공산.

**결정(사용자 2026-09-03)**: 파생식 **셸빙**. 속도는 **세션 키 캐싱**(스캔 1회 재사용)으로 챙긴다.
착수 조건은 그대로 — anti-debug 를 우회할 정당한 사유/도구가 생기거나, 다른 추출 벡터가 나올 때 재개.

## 착수 조건

- 오프라인 복호가 실제 요구로 올라올 때 (예: 다른 기기로 DB 옮겨 분석, 카톡 미실행 상태 수집).
- 그때 이 문서를 decision 으로 승격하고 spike 4 를 발주한다.

---
type: baseline
id: MK-BASE-008
title: "오래된 사진 .cng 로컬 복호 (백로그 — RE)"
status: deferred
product: mykakao
source:
  type: observation
  ref: ".cng spike 2026-09-04"
links:
  baselines:
    - "[[baseline-007-photo-collection]]"
  decisions: []
  specs: []
  works: []
  releases: []
  related:
    - "[[baseline-004-offline-key-derivation]]"
created_at: 2026-09-04
updated_at: 2026-09-04
tags:
  - product/mykakao
  - platform/windows
  - doc/baseline
  - status/deferred
  - kind/research
---

# 오래된 사진 .cng 로컬 복호 (백로그)

URL 만료(410)된 오래된 채팅 사진은 URL 로 못 받는다. 유일 오프라인 소스 = 로컬 암호화 캐시 `.cng`. 그러나 복호 키가 힙 메모리에 없어(하드코드/다른 구성 추정) 정적 RE(Ghidra) 필요. **이번 범위 밖.**

## spike 결과 (2026-09-04)
- harvest 2.3M RW키 + 계정키 + user_id 파생키 × AES-128/256 × CBC(IV앞16/0)·ECB 전수 + 강검증(매직+SHA1) → **10개 .cng 전부 실패**.
- chatLogs 키는 힙에 있었으나 **.cng 키는 힙에 없음** → .rdata 하드코드 or 별도 구성 추정.
- 다음 경로 = KakaoTalk 미디어 복호 루틴 **정적 RE(Ghidra passive 덤프)**. 무거움·불확실([[baseline-004-offline-key-derivation]] 와 유사 벽). anti-debug 주의.

## 착수 조건
- 오래된 사진 오프라인 복원이 실제 요구로 올라올 때. 그때 decision 승격 + spike 발주.

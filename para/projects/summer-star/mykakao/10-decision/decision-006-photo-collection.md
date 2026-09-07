---
type: decision
id: MK-DEC-006
title: "사진 수집 방식 — talkmedia URL 다운로드 + 로컬 미디어 서빙"
status: accepted
product: mykakao
created_at: 2026-09-04
updated_at: 2026-09-04
tags: [product/mykakao, platform/windows, doc/decision, status/accepted]
links:
  baselines: ["[[baseline-007-photo-collection]]"]
  decisions: ["[[decision-004-login-state-tracking]]"]
  specs: ["[[spec-006-photo-collection]]"]
  works: []
  releases: []
  related: ["[[baseline-008-cng-old-photo-decrypt]]"]
up: []
---

# 사진 수집 방식

채팅 사진을 어떻게 확보·저장·표시할지 정한다.

## Context
- 관련 baseline: [[baseline-007-photo-collection]]. URL 생존 실증(최근 200 / 오래됨 410).

## 결정 1 — 확보: **talkmedia URL 다운로드** (.cng 복호 아님)
| Option | Pros | Cons | 판정 |
|---|---|---|---|
| A. URL 다운로드(talkmedia→url) | 신선하면 200·확실·구현 쉬움 | URL 만료 창(오래된 것 불가) | **채택** |
| B. .cng 로컬 복호 | 오프라인·만료 무관 | 키 힙에 없음→Ghidra RE·무거움·불확실 | 백로그([[baseline-008-cng-old-photo-decrypt]]) |

- 매핑: `talkmedia.edb` (chatMsgTokenJunction: logId→token / tokenInfo: token→url,fileSize,checkSum). memory harvest 키로 복호(기존 경로).

## 결정 2 — 저장: **로컬 미디어 스토어(바이트 보유)**
- 다운로드한 이미지를 로컬에 저장 → URL 만료돼도 우리가 바이트 보유해 계속 표시.
- checkSum(SHA1)·fileSize 로 무결성 검증.

## 결정 3 — 서빙·표시: **/api/media + 탭2 <img>**
- `GET /api/media/<chatId>/<logId>` → 로컬 저장 이미지 바이트 서빙(Content-Type mime).
- 탭2 대화창: 사진 메시지를 "사진" 텍스트 대신 `<img src=/api/media/...>` 렌더. 로딩/유실 상태 표시.

## 결정 4 — 커버 경계: **best-effort, 유실은 정직하게**
- 수집 시 URL 살아있으면 확보(영구). **수집 전 만료(오래 오프라인)=유실됨 표시, 복구 안 함**(.cng 범위 밖).
- 즉 "우리가 켜져 있을 때 받은 것만 확실" — 설계상 수용된 한계.

## Rationale
- SAC 미건드림·기존 복호/키캐시 재사용·무거운 RE 회피. 개인 사진 = 로컬 저장·외부 전송 없음.
- 리스크: URL 만료 창(짧으면 실시간 놓친 것 유실↑) → 실시간 폴링(3s)이 신선할 때 잡게. checkSum 불일치 시 재시도/유실.

## Open Questions
| ID | Q | Next |
|---|---|---|
| OQ-1 | URL 유효기간 실측값 | 운영 관찰 |
| OQ-2 | 썸네일 vs 원본(용량) | 구현에서(원본 우선, 큰 것 지연로드) |

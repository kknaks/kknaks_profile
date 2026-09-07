---
type: baseline
id: MK-BASE-007
title: "사진 수집 — 실시간 URL 다운로드 + 로컬 미디어 서빙"
status: accepted
product: mykakao
source:
  type: idea
  ref: "사용자 지시 + URL 생존 실증 2026-09-04"
links:
  baselines:
    - "[[baseline-005-login-state-tracking]]"
    - "[[baseline-008-cng-old-photo-decrypt]]"
  decisions:
    - "[[decision-006-photo-collection]]"
  specs:
    - "[[spec-006-photo-collection]]"
  works: []
  releases: []
  related: []
created_at: 2026-09-04
updated_at: 2026-09-04
tags:
  - product/mykakao
  - platform/windows
  - doc/baseline
  - status/accepted
---

# 사진 수집 — 실시간 URL 다운로드

채팅 사진 메시지를 실시간 수집 파이프에서 URL 로 내려받아 로컬에 저장하고, 앱이 서빙해 대화창에 이미지로 표시한다. .cng 복호는 이번 범위 밖(오래된 사진 전용, 후속).

## Raw / 배경 — '차이'의 정답 = 사진 나이

- 채팅 사진은 `talk.kakaocdn.net` 에 올라가 **일정 기간만 URL 유효**. 최근=HTTP 200(생존), 오래된 것=410 Gone(만료).
- 사용자 실증(2026-09-04): 이건학 방에 사진 전송 → 최근 6건(1~11분) **전부 200 + 유효 이미지**(png/jpeg), fileSize DB값 정확 일치, 다운로드 성공.
- 앞선 410 은 오래된 샘플이었을 뿐. → **실시간 수집은 URL 다운로드로 성립**(.cng 복호 불필요).

## 확정 경로

```
새 사진 메시지(logId)
  → talkmedia.edb (chatMsgTokenJunction: logId→token / tokenInfo: token→url,fileSize,checkSum)
  → URL 다운로드(신선하니 200)
  → 로컬 미디어 저장(우리가 바이트 보유 → 만료돼도 계속 표시)
  → /api/media/<chatId>/<logId> 서빙 → 탭2 대화창 <img>
```

## 범위

- In: 실시간 사진 수집(URL 다운로드·로컬 저장) / 미디어 서빙 / 탭2 <img> 렌더 / **유실(수집 전 만료) placeholder**.
- Out: 오래된 사진 .cng 복호([[baseline-008-cng-old-photo-decrypt]] 후속). 동영상/파일 등 다른 미디어(후속).

## 아직 안 정한 것

- URL 유효기간 정확값 → "실시간 우선, 미수집분 best-effort".

## 커버 범위 경계 (사용자 확정 2026-09-04)

- **커버**: 수집이 돌 때(실시간/근접) URL 이 살아있는 사진 → 다운로드·저장 → 바이트 보유 → 만료돼도 영구 표시.
- **커버 못 함**: 오래 로그인 안 해 재수집이 늦게 돌았고 그 사이 URL 이 만료된 사진 → **"유실됨"으로 정직하게 표시**. 우리가 제때 못 받은 것이므로 복구 시도 안 함(.cng 는 범위 밖, [[baseline-008-cng-old-photo-decrypt]]).
- 즉 사진 보존은 **best-effort** — "우리가 켜져 있을 때 받은 것만 확실". 이건 설계상 수용된 한계다.

---
type: baseline
id: BASE-010
title: "직원 앱 내부 채팅 — 텔레그램처럼 메시지 · 사진만(Mattermost 참고)"
status: raw
product: cc-prototype
feature: procedure
source:
  type: conversation
  ref: "사용자 대화 2026-10-29 · researcher 리포트 orchestration/work/internal-chat/research-mattermost-report.md"
links:
  baselines:
    - "[[baseline-008-procedure-board|BASE-008]]"
  decisions:
    - "[[decision-009-internal-chat|DEC-009]]"
  specs: []
  works: []
  releases: []
  related: []
created_at: 2026-10-29
updated_at: 2026-10-29
tags:
  - product/cc-prototype
  - feature/procedure
  - doc/baseline
  - status/raw
---

# 직원 앱 내부 채팅

## 들어온 것

사용자 (2026-10-29): **「mattermost 참고하고, 지금 cc-prototype 에서 앱에 내부 채팅을 넣을 건데 텔레그램처럼 그냥 메신저, 사진, 이런 것만 보내면 돼」**

이어서 사용자가 고른 것:

- 방 = 1:1 + 그룹방(사람을 골라 만든다 · 참여자 추가 · 나가기)
- 새 메시지 푸시(APNs)를 넣는다
- 앱(iOS Flutter)만. 웹 화면은 없다
- 지금은 역할마다 계정이 하나뿐이지만 **「나중에 전체 직원들이 다 채팅을 한다」**
- 잠금 화면 푸시 = 보낸 사람 + 본문 앞부분
- 앱 디자인 = **claude design 시안을 먼저** 만든다

## 원천

| 무엇 | 어디 |
|---|---|
| Mattermost 조사(모델 · 흐름 · 라이선스 · procedure 에 붙일 자리 · 정할 것 41건) | `orchestration/work/internal-chat/research-mattermost-report.md` (Mattermost `8a53d645decc` · procedure `dbf0b53`) |
| 지금 앱 계약 | [SPEC-004](../20-spec/spec-004-procedure-app.md) |
| 앱 시안 | claude design `dda9a931` 「Ceramique 의료진 앱 (구현 v3)」 |

## 조사에서 나온 사실 (요약)

- Mattermost 의 그룹 DM(G)은 멤버가 고정이다(추가 · 나가기가 400). 「추가 · 나가기」는 비공개 채널(P) 동작이다
- 참고한 모델 정의는 Apache 2.0 구역이고, 동작 흐름은 AGPL 구역이다. 코드는 옮기지 않는다
- procedure SSE 허브에 이미 계정 단위 전송(`send_to_account`)이 있다. 앱은 백그라운드로 가면 SSE 를 닫는다
- APNs 는 계정 → 기기 발송을 이미 한다. 다만 `apns-expiration: 0` 이 고정이고, 앱은 모르는 푸시 종류를 버린다
- 로그인한 사람이 볼 수 있는 계정 목록 API 가 없다(공개 목록은 A-16 으로 없앰)
- 앱에 앨범 선택 패키지가 없고, 사진 보관함 권한 문구도 없다

---
type: concept
id: outbound-event-connection
title: 공개 엔드포인트 없는 실시간 수신 (Outbound Event Connection)
aliases:
  - Socket Mode
  - 소켓 모드
  - Pub/Sub pull
  - 풀 구독
  - 바깥으로 여는 연결
  - 공개 엔드포인트 없이
up:
  - 2026-10-07-strong-hajin-inbox
tags:
  - 실시간
  - 연동
  - 배포
  - 이벤트
---

# 공개 엔드포인트 없는 실시간 수신

외부 서비스의 이벤트를 받을 때 **상대가 우리 URL 을 부르게 하지 않고, 우리가 상대에게 연결을 열어 두고 받는 방식.** 슬랙 Socket Mode(웹소켓)와 Gmail watch + Pub/Sub **pull** 구독이 이 모양이다. [[webhook]]·push 구독의 반대편이다.

## 정의

1. 서버가 기동할 때 바깥으로 연결을 연다(웹소켓을 열거나 구독을 당겨 온다)
2. 이벤트는 그 연결로 들어온다 — 공개 HTTPS 주소·터널·인증서가 필요 없다
3. 받은 이벤트를 확인(ack)해야 상대가 다시 보내지 않는다

## 왜 중요한가

- **로컬과 운영이 같은 방식이다** — 웹훅은 로컬에서 받으려면 터널이 필요해 로컬 확인과 운영이 갈린다. 바깥으로 여는 연결은 로컬에서 본 동작이 운영에 그대로 통한다
- 내부망 서버도 받을 수 있다 — 들어오는 문을 열지 않는다

## 경계와 오해

- **대가 1 — 연결은 하나가 소유해야 한다.** 레플리카가 여럿이면 각자 연결을 열어 같은 이벤트를 여러 번 받거나 나눠 받는다. 레플리카 1 · 배포 전략 Recreate(옛 파드가 내려간 뒤 새 파드) · DB advisory lock 으로 소유자를 하나로 묶었다 → [[distributed-lock]]
- **대가 2 — 같은 앱 토큰을 나눠 쓰면 경합한다.** 로컬 스택과 운영이 같은 앱 자격으로 연결을 열면 상대가 이벤트를 연결들에 나눠 준다. 로컬을 내려야 운영이 다 받는다. 로컬 확인 뒤 정리가 절차에 들어가야 한다
- **pull ≠ [[polling]]** — pull 구독은 대기 중인 메시지를 받아 오는 장기 요청이고, 상대 쪽 큐가 메시지를 보관한다 → [[message-broker]]
- 확인(ack) 없이 처리하다 죽으면 재전송된다 — 받는 쪽은 중복을 전제로 → [[idempotency]]

## 함께 보는 개념

- [[webhook]] — 상대가 우리 URL 을 부르는 반대편
- [[websocket]] — Socket Mode 가 쓰는 통로
- [[slack-bot]] — Events API 와 Socket Mode 의 갈래
- [[kubernetes-workload]] — 레플리카 수·배포 전략이 소유를 정하는 자리

## 출처

- [[2026-10-07-strong-hajin-inbox]] §2 — Strong Hajin WORK-011 실시간 수신(infra-deploy-steps · be2-report)

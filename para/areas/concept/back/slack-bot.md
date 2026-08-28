---
type: concept
id: slack-bot
title: 슬랙봇
aliases:
  - 슬랙 봇
  - Slack bot
  - Slack 앱 봇
up:
  - C-035-building-slack-bots-for-workflow-automation
tags:
  - Slack API
  - 업무 자동화
  - 메시징 인터페이스
  - 봇
---

# 슬랙봇

슬랙봇은 반복 작업을 수행하는 프로그램의 명령과 결과를 Slack에서 주고받게 만든 업무 인터페이스다. Slack 앱은 사용자·채널과 서버를 연결하고, 실제 업무 규칙과 외부 시스템 연동은 애플리케이션 서버가 수행한다.

## 정의

슬랙봇은 다음 요소로 구성된다.

1. **Slack 앱** — 워크스페이스에 설치되어 봇 사용자, 권한과 이벤트 구독 설정을 소유한다.
2. **봇 사용자** — 채널에서 이름과 아이콘을 가지고 메시지를 보내거나 멘션을 받는 앱의 대표 사용자다.
3. **토큰과 권한 범위** — 봇 토큰은 Web API 호출 권한을, 앱 레벨 토큰은 Socket Mode 같은 앱 수준 연결 권한을 나타낸다. 각 토큰에는 필요한 최소 OAuth scope만 부여한다.
4. **이벤트 입력** — 공개 HTTPS 요청 URL을 등록하는 Events API나 서버가 Slack에 연결을 여는 Socket Mode로 메시지·멘션·채널 사건을 받는다.
5. **애플리케이션 서버** — 입력을 검증하고 업무 명령으로 해석한 뒤 데이터베이스나 외부 API를 호출한다.
6. **응답 출력** — Web API나 [[webhook]]을 사용해 처리 결과를 채널 또는 스레드에 게시한다.

단방향 알림만 필요하면 Incoming Webhook으로 충분하다. 사용자 입력을 받거나 채널 생성·구성원 초대처럼 양방향 동작을 해야 하면 Bolt 프레임워크나 Slack SDK로 서버를 구성한다. Bolt는 서버와 이벤트 처리 골격을 함께 제공하고, SDK는 기존 Express·NestJS·Spring·Django 같은 서버에 Slack API 기능만 결합할 때 적합하다.

## 사용 예시

휴가 안내 봇은 스케줄러가 매일 인사 시스템에서 당일 휴가자를 조회하게 하고 결과를 지정 채널에 게시한다. 예약 조회 봇은 사용자가 입력한 날짜와 노선을 검증한 뒤 예약 시스템에서 잔여 좌석을 찾아 스레드로 답한다. 운항 관리 봇은 비행편별 채널 생성, 승무원 초대, 운항 후 채널 보관과 평가 링크 전달을 자동화할 수 있다.

다음은 Bolt for JavaScript에서 앱 멘션을 받아 같은 스레드에 답하는 최소 골격이다.

```javascript
const { App } = require('@slack/bolt');

const app = new App({
  token: process.env.SLACK_BOT_TOKEN,
  appToken: process.env.SLACK_APP_TOKEN,
  socketMode: true,
});

app.event('app_mention', async ({ event, client }) => {
  await client.chat.postMessage({
    channel: event.channel,
    thread_ts: event.ts,
    text: `요청을 받았습니다: ${event.text}`,
  });
});

app.start();
```

실제 업무 명령은 `event.text`를 곧바로 실행하지 않는다. 요청자와 채널의 권한, 허용된 명령과 인자를 검증한 뒤 별도의 서비스 계층에서 처리한다.

## 왜 중요한가

조직 구성원이 항상 사용하는 메신저를 공통 인터페이스로 삼으면 각 업무 시스템을 직접 찾아가거나 사용법을 따로 익히는 비용이 줄어든다. 알림 수신과 간단한 조작이 한곳에서 이어져 맥락 전환이 감소하고, 개발자가 아닌 사용자도 승인된 업무 기능에 접근할 수 있다.

슬랙봇의 효과는 봇의 기능 수가 아니라 반복 단계, 처리 시간과 오류가 얼마나 감소했는지로 판단한다. 여러 사람이 자주 수행하고 오류 비용이 큰 흐름을 자동화할수록 조직 전체의 생산성 개선으로 이어진다.

## 경계와 오해

- **Slack 앱 ≠ 애플리케이션 서버** — Slack 앱은 권한과 통신 접점을 정의하지만 복잡한 업무 규칙을 대신 실행하지 않는다.
- **슬랙봇 ≠ 단순 알림** — 알림은 한 사용 방식일 뿐이며, 이벤트를 받아 외부 시스템에 명령을 전달하는 양방향 자동화도 포함한다.
- **봇 토큰 ≠ 앱 레벨 토큰** — Web API를 봇 사용자 권한으로 호출할 때와 Socket Mode 연결을 맺을 때 사용하는 토큰이 다르다.
- **앱 생성 ≠ 운영 준비 완료** — 이벤트 구독, 필요한 OAuth scope, 앱 재설치, 서버 접근 경로와 비밀 관리까지 갖춰야 동작한다.
- **자동화 ≠ 무검증 실행** — Slack 입력도 외부 입력이다. 권한 검사, 중복 이벤트 방지, 멱등성, 타임아웃과 실패 복구가 필요하다.

## 함께 보는 개념

- [[webhook]] — 서버 없이 단방향 Slack 알림을 보낼 때 사용할 수 있는 가장 단순한 통합 방식이다.
- [[idempotency]] — Slack의 이벤트 재전송이나 외부 API 재시도가 업무를 중복 실행하지 않게 하는 성질이다.
- [[exponential-backoff]] — Slack API의 rate limit이나 일시적 외부 API 실패를 안전하게 재시도하는 방식이다.
- [[websocket]] — 공개 수신 URL 없이 서버가 먼저 지속 연결을 여는 Socket Mode의 기반 통신 방식이다.

## 출처

- [[C-035-building-slack-bots-for-workflow-automation]] — Slack을 공통 업무 인터페이스로 삼고 Incoming Webhook, Bolt, SDK, Events API와 Socket Mode로 자동화하는 구성을 설명한다.

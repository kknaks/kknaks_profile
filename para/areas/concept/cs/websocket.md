---
type: concept
id: websocket
title: WebSocket · STOMP
aliases:
  - WebSocket
  - 웹소켓
  - STOMP
  - SockJS
  - 메시지 브로커
up:
  - 2025-01-02-Day03
tags:
  - web
  - 통신
  - 실시간
---

# WebSocket · STOMP

**연결 하나를 열어 두고 양쪽이 아무 때나 보내는 통신.** HTTP 로 시작해 프로토콜을 바꿔 잡고(업그레이드), 그 뒤로는 요청-응답이 아니다.

## 정의

세 층으로 쌓인다.

| 층 | 무엇 |
|---|---|
| **WebSocket** | 양방향 연결 자체. 바이트/텍스트를 주고받는 통로 |
| **STOMP** | 그 위에 얹는 **메시징 규약** — 구독(subscribe)·발행(publish) 같은 개념을 준다 |
| **SockJS** | WebSocket 을 못 쓰는 환경을 위한 **대체 수단(fallback)** |

```javascript
const socket = new SockJS("/ws");            // 연결 (안 되면 다른 방법으로 대체)
const stompClient = Stomp.over(socket);      // 그 위에 STOMP 를 입힌다

stompClient.connect({}, frame => {
  stompClient.subscribe("/topic/chat/writeMessage", data => { ... });   // 구독
});
```

### 주소가 두 갈래다

```java
@Configuration
@EnableWebSocketMessageBroker
public class WebSocketConfig implements WebSocketMessageBrokerConfigurer {
  @Override
  public void registerStompEndpoints(StompEndpointRegistry registry) {
    registry.addEndpoint("/ws").withSockJS();
  }
  @Override
  public void configureMessageBroker(MessageBrokerRegistry registry) {
    registry.enableSimpleBroker("/topic");                // 서버 → 구독자들
    registry.setApplicationDestinationPrefixes("/app");   // 클라이언트 → 서버
  }
}
```

```
클라이언트 ──/app/…──▶ @MessageMapping 메서드 ──/topic/…──▶ 그 주소를 구독한 모두
```

- **`/app`** — 클라이언트가 서버에게 보낼 때. `@MessageMapping` 이 달린 메서드로 라우팅된다
- **`/topic`** — 브로커가 **구독자 전부에게** 뿌릴 때 (1:N)

**「누구에게 보낼지」를 주소로 표현한다**는 것이 이 규약의 핵심이다 — `/topic/chat/room/1` 을 구독한 클라이언트만 그 방의 메시지를 받는다.

## 왜 중요한가

**채팅처럼 양쪽이 말하는 것에는 이것이 맞는 모양이다.** [[polling]] 은 클라이언트가 계속 묻고, [[server-sent-events]] 는 서버만 보낼 수 있다. **둘 다 반쪽**인데 여기서는 한 연결로 양방향이 된다.

**그리고 「받을 사람」을 서버가 관리하지 않아도 된다.** SSE 구현에서는 열린 연결을 리스트에 모아 두고 직접 순회했는데, 브로커를 쓰면 **구독 목록을 브로커가 갖는다** — 애플리케이션 코드에서 연결 관리가 사라진다 → [[observer-pattern]]

## 경계와 오해

- **WebSocket ≠ STOMP** — 웹소켓은 **통로**일 뿐 메시지의 의미를 모른다. 구독·발행·목적지 같은 개념은 전부 STOMP 가 얹은 것이라, 웹소켓만 쓰면 그 규약을 직접 만들어야 한다 → [[network-protocol]]
- **`enableSimpleBroker` 는 메모리 브로커다** — 서버 프로세스 안에 구독 정보를 들고 있으므로 **서버를 여러 대로 늘리면 서로의 구독자를 모른다.** 그때는 외부 브로커가 필요하다 → [[distributed-processing]]
- **연결이 상태를 갖는다** — HTTP 의 무상태와 정반대다. 어느 서버에 붙었는지가 의미를 가지므로, 로드밸런서·세션·재접속 처리가 전부 새 문제가 된다 → [[http-message]] · [[http-session]]
- **SockJS 는 성능이 아니라 호환을 위한 것이다** — 웹소켓이 되면 그것을 쓰고, 안 되면 폴링 계열로 떨어진다. **떨어졌을 때의 성질은 폴링의 것**이라는 점을 알고 써야 한다 → [[polling]]
- **`@MessageMapping` 은 `@RequestMapping` 이 아니다** — 같은 컨트롤러 안에 있어도 HTTP 요청이 아니라 STOMP 메시지를 받는다. 인증·인터셉터·예외 처리가 **웹 쪽 장치와 별개**로 돈다 → [[request-mapping]] · [[handler-interceptor]]
- **연결 수가 곧 자원이다** — 사용자마다 연결 하나가 계속 열려 있으므로, 동시 접속자가 서버 자원의 상한을 정한다 → [[socket]] · [[thread]]

## 함께 보는 개념

- [[polling]] · [[server-sent-events]] — 같은 문제의 앞선 답들
- [[socket]] — 그 아래에 있는 것
- [[network-protocol]] — 층을 쌓는다는 성질
- [[observer-pattern]] — 구독-발행의 구조
- [[distributed-processing]] — 서버가 여럿일 때의 문제
- [[request-mapping]] — 이름이 닮은 HTTP 쪽 장치

## 출처

- [[2025-01-02-Day03]] — 「WebSocket(STOMP)방식 구현」 절이 **주소 두 갈래의 흐름을 한 줄로 그렸다**: 「클라이언트 → `/app/*` → `@MessageMapping` → `/topic/*` → 구독 클라이언트들」. `enableSimpleBroker("/topic")` 과 `setApplicationDestinationPrefixes("/app")` 을 각각 네 줄씩 풀어 **브로커가 1:N 전달을 맡고 `/app` 은 클라이언트→서버 단방향**이라는 것을 명시했고, `/topic/chat/room/1` 예로 방별 구독까지 짚었다. 자바스크립트 쪽은 `new SockJS("/ws")` → `Stomp.over(socket)` → `subscribe(...)` 세 줄이 층을 쌓는 순서를 그대로 보이고, **SockJS 가 「WebSocket 을 지원하지 않는 브라우저를 위한 폴백」**이라는 설명도 붙어 있다. 같은 노트가 SSE 구현을 먼저 하고 이쪽으로 넘어오므로, **연결 관리를 직접 하던 것(`CopyOnWriteArrayList<SseEmitter>`)이 브로커로 넘어가는 대비**가 코드로 남았다 → [[server-sent-events]]

# AgentKit의 Human-in-the-Loop 구현

> 출처: https://agentkit.inngest.com/advanced-patterns/human-in-the-loop · 2026-08-28

## 요지

- AgentKit 네트워크를 Inngest 함수 안에서 실행하면 에이전트가 사람의 응답을 기다리는 동안 실행을 일시 중지할 수 있다.
- Human-in-the-Loop 도구는 Inngest의 `step.waitForEvent()`를 사용해 특정 이벤트가 도착할 때까지 대기한다.
- 요청과 응답은 티켓 ID 같은 상관관계 키로 연결하며, 예시에서는 `data.ticketId`를 사용한다.
- 사람의 응답이 도착하면 도구의 결과로 에이전트에 반환되어 중단했던 작업을 이어 간다.
- 이 패턴은 지원, 코딩, 리서치처럼 사람의 감독이나 추가 맥락이 필요한 에이전트에 적합하다.

## 무엇에 대한 문서인가

이 문서는 AgentKit과 Inngest를 결합해 사람의 입력을 기다릴 수 있는 에이전트 도구를 만드는 방법을 설명한다. 핵심은 AgentKit 네트워크를 이벤트 기반 Inngest 함수로 감싸고, 도구 내부에서 `step.waitForEvent()`를 호출하는 것이다.

예제로는 고객 지원 에이전트와 기술 지원 에이전트, 티켓을 적절한 에이전트로 보내는 감독 에이전트로 구성된 지원 네트워크를 다룬다. 기술 지원 에이전트가 복잡한 문제를 만났을 때 개발자에게 맥락을 요청하고, Slack 등의 외부 채널에서 전달된 답변을 받은 뒤 처리를 계속하도록 구성한다.

## 핵심 개념·절차

### AgentKit 네트워크를 Inngest 함수로 감싸기

사람의 입력을 기다리는 동안 네트워크 실행을 중단하고 나중에 재개하려면 `network.run()`을 일반 애플리케이션 코드에서 직접 호출하지 않고 Inngest 함수 안에서 실행해야 한다.

먼저 Inngest 클라이언트를 만들고, `app/support.ticket.created` 이벤트로 실행되는 함수를 정의한다. 이 이벤트에는 이후 응답을 연결하는 데 사용할 `data.ticketId`가 포함되어야 한다. 정의한 함수는 `createServer`의 `functions` 속성에도 등록한다.

### 사람에게 질문하는 도구 만들기

기술 지원 에이전트가 추가 정보가 필요하면 `ask_developer` 도구를 호출한다. 이 도구는 `step.waitForEvent()`를 사용해 최대 4시간 동안 `developer.response` 이벤트를 기다리며, 대기 중에는 AgentKit 네트워크의 실행도 일시 중지된다.

### 요청과 응답 연결하기

새 티켓 이벤트와 개발자 응답 이벤트는 동일한 `data.ticketId`를 가져야 한다. `waitForEvent()`의 일치 조건은 처음 네트워크를 실행한 이벤트의 티켓 ID와 들어오는 응답 이벤트의 티켓 ID를 비교한다. 이를 통해 동시에 여러 티켓이 처리되더라도 올바른 응답만 해당 실행에 전달된다.

### 응답을 받아 실행 재개하기

개발자는 Slack 같은 외부 채널을 통해 답할 수 있으며, 연동 계층은 그 답변을 `developer.response` 이벤트로 전송한다. 일치하는 이벤트가 도착하면 대기가 끝나고 응답 내용이 `ask_developer`의 결과로 기술 지원 에이전트에 반환된다. 에이전트는 받은 맥락을 이용해 티켓 분류나 해결 작업을 계속한다.

## 코드·설정 예시

아래 코드는 문서에 설명된 구성 관계를 압축한 개략 예시다. 실제 인자와 반환 형식은 사용하는 AgentKit 및 Inngest 버전의 API를 확인해야 한다.

```ts
const inngest = new Inngest({ id: "support-agent" });

const supportTicketHandler = inngest.createFunction(
  { id: "support-ticket-handler" },
  { event: "app/support.ticket.created" },
  async ({ event, step }) => {
    return network.run(event.data, { step });
  },
);
```

사람의 응답을 기다리는 도구는 다음과 같은 구조를 갖는다.

```ts
const askDeveloper = createTool({
  name: "ask_developer",
  handler: async ({ question }, { event, step }) => {
    const response = await step.waitForEvent("developer-response", {
      event: "developer.response",
      timeout: "4h",
      match: "data.ticketId",
    });

    return response?.data;
  },
});
```

시작 이벤트와 응답 이벤트에는 같은 티켓 ID를 넣는다.

```json
{
  "name": "app/support.ticket.created",
  "data": {
    "ticketId": "ticket-123",
    "message": "서비스 연결이 반복해서 끊깁니다."
  }
}
```

```json
{
  "name": "developer.response",
  "data": {
    "ticketId": "ticket-123",
    "answer": "해당 고객 계정의 연결 로그를 먼저 확인하세요."
  }
}
```

마지막으로 생성한 Inngest 함수를 서버에 등록해야 실제 이벤트를 받을 수 있다.

```ts
createServer({
  client: inngest,
  functions: [supportTicketHandler],
});
```

## 함정·주의

- AgentKit 네트워크를 Inngest 함수로 감싸지 않으면 `waitForEvent()`를 이용한 중단과 재개 흐름을 적용할 수 없다.
- 시작 이벤트와 응답 이벤트 모두에 안정적인 상관관계 키가 필요하다. `ticketId`가 없거나 값이 다르면 응답이 해당 실행과 일치하지 않는다.
- `ask_developer`의 대기 시간은 최대 4시간으로 설정되어 있으므로, 그 안에 응답이 없을 때의 타임아웃 처리와 에이전트의 대체 행동을 설계해야 한다.
- Inngest 함수를 만들기만 하고 `createServer`의 `functions`에 등록하지 않으면 이벤트가 함수를 실행하지 않는다.
- Slack 등 외부 채널의 답변을 `developer.response` 이벤트로 변환해 보내는 연동 계층은 별도로 필요하다.
- 사람의 입력은 신뢰할 수 없는 외부 데이터로 취급하고, 에이전트나 후속 도구에 전달하기 전에 권한 확인과 입력 검증을 적용하는 편이 안전하다.
- 위 코드 블록은 크롤링 본문의 설명을 바탕으로 재구성한 개략 예시이므로 정확한 API 서명은 원문의 전체 코드와 현재 버전 문서를 기준으로 확인해야 한다.

## 참고

- Inngest `step.waitForEvent()` 문서: 이벤트 대기, 제한 시간, 이벤트 일치 조건의 상세 사용법과 추가 예제를 제공한다.
- 원문은 두 에이전트와 감독 에이전트로 구성된 Human-in-the-Loop 지원 에이전트 예제를 함께 소개한다.

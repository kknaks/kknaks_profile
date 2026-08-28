# OpenAI Agents JS 승인 기반 Human-in-the-loop

> 출처: https://openai.github.io/openai-agents-js/guides/human-in-the-loop/ · 2026-08-28

## 요지

- 승인이 필요한 도구 호출이 발생하면 SDK는 실행을 중단하고 `interruptions`를 반환하며, 결정이 반영된 동일한 `RunState`로 실행을 재개한다.
- 승인 흐름은 최상위 에이전트뿐 아니라 handoff 대상과 중첩된 `agent.asTool()` 내부 도구까지 실행 계층 전체에 적용된다.
- 각 요청은 `state.approve()` 또는 `state.reject()`로 처리하며, 일부 요청만 결정한 채 나머지를 보류할 수도 있다.
- 장시간 중단에는 상태를 직렬화해 저장할 수 있지만, 재개 시 같은 에이전트 그래프와 안전한 출력 소유권 경계를 복원해야 한다.
- 일시 중단 중 도착한 사용자 입력은 `RunState.addInput()`으로 다음 모델 호출 전에 합류시킬 수 있다.

## 무엇에 대한 문서인가

OpenAI Agents SDK for JavaScript에서 도구 실행 전 사람의 승인을 받는 방법을 설명하는 문서다. 승인 규칙 선언, 중단 항목 처리, 실행 재개, 스트리밍과 세션 연동, 상태 직렬화까지 수동 승인 흐름의 전체 생명주기를 다룬다.

로컬 셸과 hosted MCP처럼 코드 콜백으로 즉시 결정할 수 있는 도구도 언급하지만, 중심 주제는 `interruptions`와 `RunState`를 사용하는 수동 승인이다. 특히 handoff 및 `agent.asTool()`로 구성된 중첩 실행에서도 승인을 최상위 실행 결과를 통해 일관되게 다룬다는 점이 핵심이다.

## 핵심 개념·절차

### 승인 규칙과 중단

도구의 `needsApproval`을 `true` 또는 비동기 불리언 함수로 설정한다. 도구 호출 직전에 SDK가 규칙을 평가하고, 승인이 필요하지만 저장된 결정이 없으면 호출을 실행하지 않고 `RunToolApprovalItem`을 기록한다. 턴이 끝나면 모든 미결 요청이 결과의 `interruptions`에 담기고 실행이 일시 중단된다.

`needsApproval` 함수는 인수가 검사 가능한 객체로 파싱된 뒤에만 호출된다. 잘못된 JSON이나 객체가 아닌 값은 안전하게 실패하도록 콜백과 도구 실행 없이 승인을 요청한다. 이를 승인해도 인수 파싱 오류 경로가 계속되며 도구가 실행되지는 않는다.

### 승인 또는 거절 후 재개

각 interruption을 `result.state.approve(interruption)` 또는 `result.state.reject(interruption)`로 처리한다. 거절 시 `{ message: '...' }`로 모델에 전달할 문구를 지정할 수 있다. 생략하면 `toolErrorFormatter`를 거쳐 기본 거절 문구가 사용된다.

결정이 반영된 상태를 `runner.run(rootAgent, result.state)`에 넘겨 원래 최상위 에이전트에서 재개한다. 미결 요청을 한꺼번에 모두 처리할 필요는 없다. 일부만 결정하고 재실행하면 해결된 호출은 진행되고, 나머지는 다시 `interruptions`에 남아 실행을 중단한다.

### 지속 결정과 호출별 예외

`{ alwaysApprove: true }` 또는 `{ alwaysReject: true }`를 사용하면 같은 도구의 이후 호출에 적용되는 기본 결정을 상태에 저장한다. 특정 호출 ID에 대한 개별 결정은 이 기본값보다 우선하므로, 지속 승인 중 한 호출만 거절하거나 지속 거절 중 한 호출만 승인할 수 있다. 지속 결정은 상태 직렬화와 복원을 거쳐서도 유지된다.

### 중첩 에이전트의 승인

승인 표면은 실행 전체에 걸쳐 있다. 현재 에이전트, handoff로 도달한 에이전트, 중첩 `agent.asTool()` 내부에서 발생한 요청 모두 외부 실행의 `interruptions`로 나타난다. `agent.asTool()` 자체의 `needsApproval`과 중첩 실행이 시작된 뒤 내부 도구가 요구하는 승인은 서로 다른 계층이지만 동일한 외부 상태에서 처리한다.

### 승인 전에 입력 guardrail 실행

기본적으로 로컬 function tool의 입력 guardrail은 승인 후 실제 실행 직전에 작동한다. `toolExecution: { preApprovalInputGuardrails: true }`를 설정하면 승인 요청을 표시하기 전에도 같은 guardrail로 입력을 검사한다.

사전 검사에서 거절되면 interruption을 만들지 않고 guardrail 메시지를 도구 출력으로 모델에 반환한다. 통과하면 승인 단계에서 중단되고, 대기 중 입력의 안전성이 달라졌을 가능성에 대비해 승인 후 다시 검사한다.

### 중단 중 새 사용자 입력 추가

실행이 멈춘 동안 도착한 입력을 다음 모델 호출에 반영하려면 승인 결정을 처리하고 재개하기 전에 `state.addInput()`을 호출한다. 문자열 또는 입력 항목 배열을 받을 수 있고, 대기 입력은 직렬화된 상태에도 포함된다.

`state.pendingInput`으로 복제된 스냅샷을 확인하고 `state.clearPendingInput()`으로 제거할 수 있다. 실행이 종료됐거나 남은 턴이 없거나 도구 결과가 실행을 끝낼 수 있어 다음 모델 호출을 안전하게 보장하지 못하면 `UserError`가 발생한다. 수용된 입력은 `newItems`의 `RunInputItem`과 history에 반영된다.

### 자동 승인, 스트리밍, 세션

로컬 `shellTool()`과 `applyPatchTool()`은 `onApproval`로, hosted MCP 도구는 `requireApproval`과 `onApproval`의 조합으로 코드에서 즉시 승인 또는 거절할 수 있다. 이 경우 사람의 응답을 기다리는 중단 없이 실행이 계속된다. 일반 function tool은 이 문서의 수동 interruption 흐름을 사용한다.

스트리밍 실행에서는 `stream.completed`를 기다린 뒤 `stream.interruptions`를 처리하고, 재개 시 다시 `{ stream: true }`를 지정한다. 세션을 사용했다면 동일한 `RunState`와 함께 같은 세션을 계속 전달해야 재개된 턴이 입력 재준비 없이 세션 메모리에 추가된다.

### 장시간 중단과 상태 복원

`result.state.toString()` 또는 `JSON.stringify(result.state)`로 상태를 저장하고, 나중에 `RunState.fromString(rootAgent, serializedState)`로 복원한다. 재개 프로세스는 원래의 handoff 및 `Agent.asTool()` 관계를 포함한 같은 에이전트 그래프를 다시 구성해야 한다. SDK는 안정적인 에이전트 식별자를 사용해 이름이 같은 서로 다른 에이전트도 그래프 안에서 해석한다.

대체 모델이나 래퍼가 적용된 그래프로 바꾸려면 원본 그래프로 먼저 역직렬화하고 다시 직렬화한 다음 대체 루트로 복원한다. `setCurrentAgent()`는 활성 에이전트만 바꾸며 이미 해석된 중첩 참조를 다시 쓰지 않는다.

새 context를 주입하려면 `RunState.fromStringWithContext()`를 사용한다. 기본 `merge` 전략은 새 `RunContext`를 유지하면서 직렬화된 승인 상태를 합치고 필요한 `toolInput`을 복원한다. `replace`는 제공된 context를 그대로 사용한다.

### 버전이 달라지는 장기 작업

승인 대기 중 에이전트 정의나 SDK 버전이 크게 바뀔 수 있다면 애플리케이션 코드 버전을 직렬화 상태와 함께 저장한다. SDK의 두 버전을 package alias로 병렬 설치하고, 저장한 버전에 따라 맞는 코드와 SDK로 역직렬화하는 분기 로직을 애플리케이션에서 구현하는 방식이 권장된다.

## 코드·설정 예시

```ts
import { Agent, Runner, RunState, tool } from '@openai/agents';
import { z } from 'zod';

const deleteRecord = tool({
  name: 'delete_record',
  description: 'Delete a record',
  parameters: z.object({ id: z.string() }),
  needsApproval: true,
  execute: async ({ id }) => `Deleted ${id}`,
});

const agent = new Agent({
  name: 'operator',
  instructions: 'Help the user manage records.',
  tools: [deleteRecord],
});

const runner = new Runner();
let result = await runner.run(agent, 'Delete record customer-42');

for (const interruption of result.interruptions) {
  result.state.approve(interruption);
  // 또는:
  // result.state.reject(interruption, { message: 'Deletion was denied.' });
}

result = await runner.run(agent, result.state);
```

승인이 필요한 호출은 첫 `run()`에서 실행되지 않고 `result.interruptions`에 나타난다. 결정을 같은 `result.state`에 기록한 뒤 반드시 원래 루트 `agent`로 재개한다.

```ts
// 일시 중단 중 새 입력을 다음 모델 호출에 합류시킨다.
result.state.addInput('삭제 대신 보관 처리해 주세요.');

// 장기 보관 후 같은 에이전트 그래프로 복원한다.
const serialized = result.state.toString();
const restored = await RunState.fromString(agent, serialized);
const resumed = await runner.run(agent, restored);
```

실제 저장소나 메시지 큐에 상태를 보관할 때는 상태와 함께 애플리케이션 및 SDK 버전을 기록해야 한다. 새 context가 필요하면 일반 `fromString()` 대신 `fromStringWithContext()`와 적절한 `contextStrategy`를 선택한다.

## 함정·주의

- 직렬화 상태에는 앱 context, 승인 정보, 사용량, 중첩 `toolInput`, 중첩 에이전트 도구의 재개 정보가 포함될 수 있다. `runContext.context`를 영속 데이터로 취급하고 의도하지 않은 비밀을 넣지 않는다.
- tracing API key는 기본적으로 직렬화에서 제외된다. 자격 증명까지 이동할 의도가 명확할 때만 `toString({ includeTracingApiKey: true })`를 사용한다.
- 승인된 function tool 결과가 최종 출력이 될 수 있으면 output guardrail의 복원 경계가 더 엄격하다. 직렬화된 체크포인트가 출력 소유권을 증명하지 못하거나 세션과 함께 모호한 체크포인트를 복원하면 SDK는 부작용 전에 `UserError`로 실패한다. 이때는 안전한 입력으로 새 실행을 시작한다.
- 에이전트 그래프와 원래 `toolUseBehavior`를 보존해야 하며, 출력 가능성이 있는 모든 부분 승인 상태가 직렬화를 왕복할 수 있다고 가정하면 안 된다.
- computer tool의 한 interruption은 GA 모델에서 `move + click` 같은 여러 action을 담을 수 있다. UI가 `interruption.rawItem`을 읽는다면 GA의 `actions` 배열과 레거시 단일 `action` 필드를 모두 처리해야 한다.
- 직렬화 상태는 현재 computer tool 이름과 레거시 `computer_use_preview` 이름의 승인을 함께 보존하므로 preview에서 GA로 이전하는 재개 경로도 고려해야 한다.
- 외부 provider가 요청을 이미 수락했을 가능성이 있으면 SDK는 새 입력을 조용히 재전송하지 않고 안전하게 실패한다. 명시적인 unsafe replay는 별도의 모델 재시도 정책으로 다뤄야 한다.
- `needsApproval` 콜백은 인수 파싱에 성공한 경우에만 실행되므로, 콜백 자체를 입력 유효성 검사의 유일한 수단으로 삼으면 안 된다.

## 참고

- Tools guide — `agent.asTool()` 설정
- Human in the loop while streaming — 스트리밍 승인 흐름
- Sessions guide — 세션 생명주기와 재개
- Voice agents build guide — Realtime session 승인 흐름
- Model retries — 명시적인 unsafe replay 설정
- Full example script — 터미널 승인과 파일 기반 상태 저장의 전체 예제

# Mastra 워크플로 개요

> 출처: https://mastra.ai/docs/workflows/overview · 2026-08-28

## 요지

- Mastra 워크플로는 여러 작업을 명시적인 단계와 실행 순서로 구성해, 단일 에이전트의 추론에만 의존하지 않고 데이터 흐름을 제어한다.
- 각 단계는 `createStep()`으로 입출력 스키마와 실행 로직을 정의하고, `createWorkflow()`와 `.then()`, `.commit()`으로 조합한다.
- 실행은 최종 결과를 기다리는 `start()`와 진행 이벤트를 내보내는 `stream()`을 지원하며, 중단·재개·재시작 기능도 제공한다.
- 상태 공유, 하위 워크플로 재사용, 복제, 에이전트·도구 호출, 요청별 컨텍스트 처리 등 복잡한 실행 시나리오를 지원한다.
- 실행 결과는 `status`로 구분되는 판별 유니온이므로, 상태를 확인한 뒤 해당 상태 전용 속성에 접근해야 한다.

## 무엇에 대한 문서인가

이 문서는 Mastra에서 순서가 정해진 다단계 작업을 워크플로로 정의하고 등록·참조·실행하는 전체 흐름을 설명한다. 단계별 입출력 스키마, 실행 로직, 제어 흐름, 공유 상태, 중첩과 복제 같은 구성 요소부터 동기 실행과 스트리밍 실행, 중단된 실행의 재개와 활성 실행의 재시작까지 다룬다.

처리 절차와 데이터 변환을 사전에 명확히 정의할 수 있고 각 단계에서 호출할 에이전트·도구·함수를 통제해야 할 때 유용하다. 기본 내장 실행 엔진을 사용하거나 Inngest 같은 워크플로 러너에 배포할 수 있으며, Studio에서 실행 그래프와 상태·입출력·로그를 관찰할 수 있다.

## 핵심 개념·절차

### 단계 정의

`createStep()`에 고유 `id`, `inputSchema`, `outputSchema`, `execute`를 전달한다. 스키마는 Zod, Valibot, ArkType 등 Standard JSON Schema 호환 도구로 정의할 수 있다. `execute`에서는 애플리케이션 함수, 외부 API, 등록된 에이전트 또는 도구를 호출하고 출력 스키마에 맞는 값을 반환한다.

### 워크플로 구성

`createWorkflow()`로 워크플로의 입출력 스키마를 선언하고 `.then()`으로 단계를 연결한 뒤 `.commit()`으로 구성을 확정한다. 선택한 제어 흐름 방식에 따라 인접 단계의 출력과 입력 스키마가 호환되어야 한다.

워크플로 자체를 상위 워크플로의 단계로 넣어 로직을 재사용할 수도 있다. 동일한 로직을 별도 ID와 관측 단위로 실행하려면 `cloneWorkflow()`를 사용한다.

### 상태 공유

여러 단계가 값을 공유하되 모든 단계의 입출력에 그 값을 전달하고 싶지 않을 때 `stateSchema`를 정의한다. 단계의 `execute`에서 `state`를 읽고 `setState()`로 갱신하며, 진행 상황 추적, 결과 누적, 공통 설정 공유에 활용한다. 상태는 중단·재개와 중첩 워크플로에서도 고려해야 한다.

### 등록과 참조

워크플로를 `new Mastra({ workflows: { ... } })`에 등록하면 로깅, 텔레메트리, 저장소, 등록된 에이전트와 벡터 저장소 같은 공유 자원에 접근할 수 있다. 실행할 때는 직접 import하기보다 등록 키를 사용한 `mastra.getWorkflow()`가 권장된다. 이 방식은 Mastra 인스턴스 설정과 완전한 TypeScript 입출력 타입 추론을 제공한다.

`getWorkflowById()`도 `id` 속성으로 워크플로를 찾을 수 있지만 등록 키 기반 `getWorkflow()`만큼 정밀한 타입 추론을 제공하지 않는다.

### 실행과 결과 처리

`createRun()`으로 실행 인스턴스를 만든 뒤 다음 두 모드 중 하나를 선택한다.

- `start()`: 모든 단계가 끝날 때까지 기다린 뒤 최종 결과를 반환한다.
- `stream()`: 실행 중 이벤트를 방출한다. `fullStream`으로 진행 상황을 순회하고 `stream.result`로 최종 결과를 받는다.

두 방식의 최종 결과는 `status`가 `success`, `failed`, `suspended`, `tripwire`, `paused` 중 하나인 판별 유니온이다. 모든 상태에서 `status`, `input`, `steps`와 선택적인 `state`를 확인할 수 있다. 상태별 전용 값은 다음과 같다.

| 상태 | 전용 속성 | 의미 |
|---|---|---|
| `success` | `result` | 워크플로 최종 출력 |
| `failed` | `error` | 실패 원인 |
| `tripwire` | `tripwire` | 중단 이유와 선택적 재시도·메타데이터 정보 |
| `suspended` | `suspendPayload`, `suspended` | 재개 데이터와 중단된 단계 경로 |
| `paused` | 없음 | 공통 속성만 제공 |

### 스트리밍·재개·재시작

스트림 청크에는 이벤트 유형, 중간값, 단계별 데이터 같은 실행 이벤트가 포함될 수 있다. 중단된 워크플로는 `resumeStream({ resumeData })`으로 데이터와 함께 재개할 수 있고, 연결만 끊어진 스트림은 인자 없는 `resumeStream()`으로 새 `ReadableStream`을 얻어 계속 관찰할 수 있다.

서버 연결이 끊긴 장기 실행은 마지막 활성 단계부터 `run.restart()`로 재시작한다. 워크플로의 모든 활성 실행을 되살리려면 `restartAllActiveWorkflowRuns()`를 사용하고, `listActiveWorkflowRuns()`로 `running` 또는 `waiting` 상태의 실행을 찾는다. 로컬 Mastra 서버는 시작할 때 활성 워크플로 실행을 자동으로 재시작한다.

### Studio와 요청 컨텍스트

Studio의 Workflows 탭에서는 그래프 뷰, 스키마 기반 입력 폼, 실시간 단계 상태, 입출력·상태·로그를 확인할 수 있다. 완료된 실행의 개별 단계를 재생해 검사하거나 재시도하는 타임 트래블 기능도 제공한다.

`RequestContext`는 사용자 등급처럼 요청별 값을 단계에 전달할 때 사용한다. 값에 따라 처리량이나 동작을 조건부로 바꿀 수 있으며, 별도의 스키마 검증을 적용하면 타입 안전성을 높일 수 있다.

## 코드·설정 예시

다음은 문자열을 대문자로 바꾸는 단계를 정의하고 워크플로로 등록·실행하는 최소 예시다.

```ts
import { Mastra } from '@mastra/core/mastra'
import { createStep, createWorkflow } from '@mastra/core/workflows'
import { z } from 'zod'

const formatStep = createStep({
  id: 'format-message',
  inputSchema: z.object({ message: z.string() }),
  outputSchema: z.object({ formatted: z.string() }),
  execute: async ({ inputData }) => ({
    formatted: inputData.message.toUpperCase(),
  }),
})

const messageWorkflow = createWorkflow({
  id: 'message-workflow',
  inputSchema: z.object({ message: z.string() }),
  outputSchema: z.object({ formatted: z.string() }),
})
  .then(formatStep)
  .commit()

const mastra = new Mastra({
  workflows: { messageWorkflow },
})

const workflow = mastra.getWorkflow('messageWorkflow')
const run = await workflow.createRun()
const result = await run.start({
  inputData: { message: 'Hello world' },
})

if (result.status === 'success') {
  console.log(result.result.formatted)
}
```

스트리밍할 때는 청크 소비와 최종 결과 확인을 분리한다.

```ts
const run = await workflow.createRun()
const stream = run.stream({
  inputData: { message: 'Hello world' },
})

for await (const chunk of stream.fullStream) {
  console.log(chunk)
}

const result = await stream.result
if (result.status === 'success') {
  console.log(result.result)
}
```

단계 사이의 공유 상태는 다음처럼 읽고 갱신한다.

```ts
const countedStep = createStep({
  id: 'counted-step',
  inputSchema: z.object({ message: z.string() }),
  outputSchema: z.object({ formatted: z.string() }),
  stateSchema: z.object({ counter: z.number() }),
  execute: async ({ inputData, state, setState }) => {
    setState({ ...state, counter: state.counter + 1 })
    return { formatted: inputData.message.toUpperCase() }
  },
})
```

## 함정·주의

- 워크플로는 단계와 실행 순서를 미리 정의할 수 있는 작업에 적합하다. 목표 달성 경로를 에이전트가 자율적으로 탐색해야 하는 문제와는 성격이 다르다.
- 각 단계의 반환값은 선언한 `outputSchema`와 일치해야 하며, 연결 방식에 따라 이전 단계의 출력과 다음 단계의 입력 스키마도 호환되어야 한다.
- `.commit()`을 호출해야 워크플로 구성이 완성된다.
- `result.result`, `result.error`, `result.suspendPayload`처럼 상태별 속성은 반드시 `result.status`를 검사한 뒤 접근해야 한다.
- 워크플로 참조에는 선언 시의 `id`가 아니라 Mastra 등록 객체에 사용한 키를 `getWorkflow()`에 전달한다. `getWorkflowById()`는 타입 추론 수준이 다르다.
- 공유 상태는 편리하지만 단계의 명시적 데이터 흐름을 감출 수 있다. 진행 추적, 누적 결과, 전역 설정처럼 여러 단계가 실제로 공유해야 하는 값에 제한하는 편이 좋다.
- 스트리밍 실행에서는 이벤트 소비와 최종 결과 획득이 별도 과정이다. 진행 이벤트가 필요하지 않다면 단순한 `start()`가 적합하다.
- `restart()`는 처음부터 다시 실행하는 기능이 아니라 마지막 활성 단계에서 실행을 이어가는 기능이다. 단계의 외부 부작용과 재실행 안전성을 함께 설계해야 한다.
- 에이전트의 `textStream`을 단계의 `writer`에 연결하면 부분 출력이 전파되고 사용량도 워크플로 실행에 합산된다. 이때 선택적 값으로 제공되는 에이전트와 writer가 실제로 존재하는지 확인해야 한다.

## 참고

- Mastra Step 구성 옵션
- Mastra Workflow Class 구성 옵션
- Workflow Guide
- Workflow State
- Control Flow
- Suspend and Resume
- Error Handling
- Streaming
- Using Tools
- Request Context
- Schema Validation
- Workers: 전용 백그라운드 프로세스에서 워크플로 실행
- Agentic workflows with Mastra workshop

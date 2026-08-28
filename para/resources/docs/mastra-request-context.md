# Mastra RequestContext로 요청별 런타임 값 전달하기

> 출처: https://mastra.ai/docs/server/request-context · 2026-08-28

## 요지

- `RequestContext`는 에이전트, 도구, 네트워크, 워크플로에 요청별 값을 전달하고 하위 구성 요소에서 공유하게 한다.
- 대화 기록과 호출 간 상태를 보존하는 메모리와 달리, 현재 요청의 사용자 등급·언어·테넌트 같은 런타임 조건을 다룬다.
- 애플리케이션 데이터는 타입이나 `requestContextSchema`에 선언하고, 스키마 밖의 인프라 값에만 raw 메서드를 쓰는 것이 권장된다.
- 서버 미들웨어에서 인증 및 요청 헤더를 해석해 컨텍스트를 채우면 개인화, 현지화, 모델·도구 선택과 사용자 격리를 일관되게 적용할 수 있다.
- 에이전트, 도구, 워크플로, 스텝은 모두 스키마 검증을 지원하지만 검증 시점과 실패 방식은 서로 다르다.

## 무엇에 대한 문서인가

이 문서는 Mastra의 `RequestContext`를 생성하고 값을 설정한 뒤, 에이전트·도구·워크플로와 그 하위 구성 요소에서 읽는 방법을 설명한다. 요청 헤더 기반 값 주입, Studio 프리셋, 동적 지시문과 프롬프트 레지스트리 연동, 예약 키를 이용한 멀티테넌트 사용자 격리도 다룬다.

사용자 속성이나 실행 환경에 따라 모델, 스토리지, 지시문, 도구 또는 응답 언어를 바꿔야 할 때 읽을 문서다. 장기간 유지할 대화 상태가 아니라 한 요청의 실행 전반에만 필요한 데이터를 전달하는 데 초점이 있다.

## 핵심 개념·절차

### 요청 컨텍스트와 메모리의 구분

`RequestContext`는 특정 호출에 주입되는 런타임 데이터다. 사용자 등급, 로케일, 실험군, 인증 사용자 ID처럼 현재 실행의 동작을 바꾸는 값에 적합하다. 반면 에이전트 메모리는 여러 호출에 걸친 대화 기록과 지속 상태를 관리한다.

### 값 생성과 전파

제네릭 타입으로 허용할 키와 값의 타입을 선언하고 `.set(key, value)`로 값을 넣는다. 완성된 `requestContext`를 에이전트의 `generate()`·`network()`, 워크플로의 `start()`·`resume()`, 또는 도구의 `execute()`에 전달하면 실행 중인 하위 프리미티브에서도 같은 값을 사용할 수 있다.

선언된 애플리케이션 키에는 `.get()`, `.set()`, `.has()`, `.delete()`를 쓴다. 타입이나 스키마에 포함되지 않는 미들웨어·인프라 전용 키에는 `.getRaw()`, `.setRaw()`, `.hasRaw()`, `.deleteRaw()`를 사용한다. raw 값은 `unknown`이므로 읽은 뒤 타입을 좁혀야 한다.

### 서버 미들웨어에서 값 설정

서버 미들웨어는 인증 결과나 요청 헤더를 읽어 `context.get('requestContext')`로 컨텍스트를 얻고 값을 설정할 수 있다. 예를 들어 Cloudflare의 `CF-IPCountry` 헤더가 `US`이면 온도 단위를 화씨로, 아니면 섭씨로 지정할 수 있다. 이 방식은 클라이언트 입력에 의존하지 않고 서버가 검증한 값을 모든 하위 실행에 전달한다.

### 구성 요소에서 값 사용

에이전트의 `instructions`, `model`, `tools`, `memory`를 비롯해 agents, workflows, scorers, input/output processors 같은 동적 옵션에서 `requestContext.get()`을 호출할 수 있다. 이 함수들은 동기 또는 비동기일 수 있다.

워크플로 스텝은 `execute({ requestContext })`에서, 도구는 `execute(inputData, context)`의 `context.requestContext`에서 값을 읽는다. 도구에서는 컨텍스트가 없을 가능성을 고려해 선택적 접근을 사용할 수 있다.

### 동적 지시문과 프롬프트 선택

에이전트 지시문을 비동기 함수로 정의하면 사용자 등급에 따른 답변 깊이, 로케일에 따른 언어와 말투, A/B 테스트용 프롬프트 변형을 런타임에 결정할 수 있다. 외부 프롬프트 레지스트리에 실험 변형과 사용자 ID를 전달해 프롬프트를 가져오면 재배포 없이 내용을 갱신하고 사용 이력을 추적할 수도 있다.

### Studio 프리셋

로컬 개발에서는 `mastra dev --request-context-presets ./presets.json`으로 JSON 프리셋을 불러올 수 있다. Studio의 요청 컨텍스트 편집기에 프리셋 선택 메뉴가 생기며, 프리셋을 고르면 JSON 값이 채워진다. 값을 직접 수정하면 선택 상태가 `Custom`으로 바뀐다.

### 예약 키와 사용자 격리

`MASTRA_RESOURCE_ID_KEY`와 `MASTRA_THREAD_ID_KEY`는 보안을 위해 예약된 키다. 서버가 설정한 예약 키는 클라이언트 값보다 우선한다.

`MASTRA_RESOURCE_ID_KEY`는 모든 메모리 작업의 리소스 ID를 강제하고, 접근한 스레드가 해당 리소스 소유인지 검사한다. 인증 설정의 `mapUserToResourceId`로 사용자 ID를 매핑하는 방법이 가장 간단하다. `MASTRA_THREAD_ID_KEY`는 스레드 ID를 서버가 검증한 값으로 강제한다. 두 키 모두 멀티테넌트 애플리케이션의 사용자 격리에 쓰인다.

### 타입과 런타임 스키마 검증

`RequestContext<MyContext>`처럼 타입 매개변수를 주면 키, 설정 값, 반환 값, `keys()`와 `entries()`가 정적으로 타입화된다. 이는 잘못된 키나 값 타입을 컴파일 단계에서 발견하는 장치다.

`requestContextSchema`에는 Zod, Valibot, ArkType 등 Standard JSON Schema 호환 스키마를 지정할 수 있다. 이 검증은 누락되거나 잘못된 런타임 값을 실제 실행 전에 차단하고, 구성 요소 내부에서 타입 추론도 제공한다.

| 구성 요소 | 검증 시점 | 실패 방식 |
|---|---|---|
| Agent | `generate()` 또는 `stream()` 시작 시 | LLM 호출 전에 `MastraError` 발생 |
| Tool | `execute()` 실행 전 | 예외 대신 검증 오류 객체 반환 |
| Workflow | `run.start()` 시작 시 | 스텝 실행 전에 오류 발생 |
| Step | 스텝의 `execute()` 실행 전 | 해당 스텝이 오류로 실패 |

미들웨어가 반드시 설정하는 필드는 같은 필수 필드로 스키마에 선언하고, 조건부 값은 `.optional()`로 표시한다. 스텝도 자체 `requestContextSchema`를 선언해 스텝별 검증과 타입 추론을 적용할 수 있다.

## 코드·설정 예시

다음은 사용자 등급을 타입으로 제한해 에이전트 호출에 전달하는 기본 형태다.

```ts
import { RequestContext } from '@mastra/core/request-context'

type UserContext = {
  'user-tier': 'enterprise' | 'pro'
  locale?: string
}

const requestContext = new RequestContext<UserContext>()
requestContext.set('user-tier', 'enterprise')
requestContext.set('locale', 'ko')

const agent = mastra.getAgent('supportAgent')
await agent.generate('결제 내역을 설명해 줘', { requestContext })
```

에이전트에서는 요청 값을 이용해 지시문을 동적으로 구성할 수 있다.

```ts
import { Agent } from '@mastra/core/agent'

export const supportAgent = new Agent({
  id: 'support-agent',
  name: 'Support Agent',
  instructions: async ({ requestContext }) => {
    const tier = requestContext?.get('user-tier')
    const locale = requestContext?.get('locale')

    const detail =
      tier === 'enterprise'
        ? '기술적 근거와 절차를 자세히 설명한다.'
        : '핵심만 간결하게 설명한다.'

    return locale === 'ko' ? `${detail} 한국어로 답한다.` : detail
  },
  model: 'openai/gpt-5.6-sol',
})
```

런타임 값까지 검증해야 한다면 구성 요소에 스키마를 붙인다.

```ts
import { z } from 'zod'
import { Agent } from '@mastra/core/agent'

const contextSchema = z.object({
  userId: z.string(),
  tenantId: z.string(),
  experimentVariant: z.string().optional(),
})

export const validatedAgent = new Agent({
  id: 'validated-agent',
  name: 'Validated Agent',
  requestContextSchema: contextSchema,
  instructions: ({ requestContext }) => {
    const { userId, tenantId } = requestContext.all
    return `User ${userId} in tenant ${tenantId}를 지원한다.`
  },
  model: 'openai/gpt-5.6-sol',
})
```

미들웨어에서는 인증으로 확인한 값을 설정해 클라이언트가 임의로 테넌트나 리소스 범위를 바꾸지 못하게 한다.

```ts
import {
  MASTRA_RESOURCE_ID_KEY,
  MASTRA_THREAD_ID_KEY,
} from '@mastra/core/request-context'

requestContext.set('userId', user.id)
requestContext.set('tenantId', tenant.id)
requestContext.set(MASTRA_RESOURCE_ID_KEY, user.id)
requestContext.set(MASTRA_THREAD_ID_KEY, validatedThreadId)
```

## 함정·주의

- `RequestContext`를 대화 기록이나 호출 간 지속 상태의 저장소로 사용하지 않는다. 그런 상태는 에이전트 메모리의 책임이다.
- 애플리케이션 값을 raw 메서드로 우회하면 선언 키 검사와 타입 안전성을 잃는다. raw 메서드는 스키마 밖에 남아야 하는 인프라 키에만 제한한다.
- raw 값의 타입은 `unknown`이므로 속성에 접근하기 전에 `typeof`, null 검사, 키 존재 검사 등으로 타입을 좁혀야 한다.
- 예약 키는 클라이언트 제공 값보다 서버 값이 우선한다. 메모리를 사용하는 요청에 본문과 요청 컨텍스트 어느 쪽에도 리소스 ID가 없으면 서버가 400을 반환할 수 있다.
- 사용자가 소유하지 않은 리소스에 접근하면 소유권 검증으로 403이 반환된다. 예약 키는 인증된 사용자와 검증된 스레드에서 서버 측으로 설정해야 한다.
- 도구의 스키마 검증 실패는 에이전트나 워크플로처럼 예외를 던지지 않고 오류 객체를 반환한다. 도구 실행이 필수라면 호출 측에서 오류 객체를 명시적으로 처리해야 한다.
- 미들웨어가 넣는 필수 값과 구성 요소 스키마가 어긋나면 실행이 시작되기 전에 검증에 실패한다. 양쪽을 하나의 명시적 계약으로 함께 관리해야 한다.
- 워크플로를 재개할 때도 `requestContext`를 `resume()` 호출에 전달해야 재개 실행에서 요청별 값을 사용할 수 있다.

## 참고

- Mastra Middleware 문서: 서버 미들웨어에서 요청 컨텍스트를 구성하는 방법
- Mastra Agent 문서: 요청 컨텍스트를 사용할 수 있는 전체 에이전트 구성 옵션
- Mastra `createStep()` 문서: 워크플로 스텝의 실행 인자와 구성 옵션
- Mastra `createTool()` 문서: 도구 실행 컨텍스트와 구성 옵션
- Mastra Authorization middleware 문서: 예약 키를 이용한 리소스 소유권 검증과 사용자 격리 예시

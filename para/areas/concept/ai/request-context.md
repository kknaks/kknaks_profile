---
type: concept
id: request-context
title: 요청 컨텍스트 (Request Context)
aliases:
  - 요청 컨텍스트
  - 요청별 컨텍스트
  - RequestContext
up:
  - mastra-request-context
tags:
  - 런타임 컨텍스트
  - 요청 범위
  - 컨텍스트 전파
  - 에이전트
  - 스키마 검증
---

# 요청 컨텍스트 (Request Context)

요청 컨텍스트는 한 번의 요청을 실행하는 여러 구성 요소가 사용자·테넌트·로케일 같은 런타임 값을 공유하도록 전달하는 요청 범위 데이터 컨테이너다. 실행 동작을 요청별로 바꾸되, 여러 호출에 걸친 지속 상태와는 분리한다.

## 정의

요청 컨텍스트는 다음 과정으로 사용한다.

1. 현재 요청에 필요한 키와 값의 타입 또는 런타임 스키마를 선언한다.
2. 인증 결과, 요청 헤더, 사용자 속성처럼 서버가 알고 있는 값을 실행 전에 설정한다.
3. 컨텍스트를 에이전트, 도구, 워크플로 같은 최상위 호출에 전달한다.
4. 하위 구성 요소는 같은 컨텍스트에서 값을 읽어 지시문, 모델, 도구, 저장소 또는 응답 형식을 선택한다.
5. 스키마가 있다면 각 구성 요소가 실행되기 전에 필수 값과 값의 형식을 검증한다.

애플리케이션 데이터는 선언된 키로 다뤄 정적 타입 검사와 런타임 검증을 받게 한다. 스키마 밖에 남아야 하는 미들웨어·인프라 값은 별도 raw 접근 경로로 다루며, 읽을 때 `unknown`에서 실제 타입으로 좁힌다.

보안 경계를 나타내는 사용자 ID, 리소스 ID, 스레드 ID는 클라이언트 입력을 그대로 신뢰하지 않고 인증 미들웨어가 설정한다. 서버가 검증한 값이 클라이언트 제공 값보다 우선해야 요청 컨텍스트를 멀티테넌트 격리 경계로 사용할 수 있다.

## 사용 예시

Mastra에서는 타입이 지정된 `RequestContext`를 만든 뒤 에이전트 호출에 전달할 수 있다.

```ts
import { RequestContext } from '@mastra/core/request-context'

type UserContext = {
  userId: string
  tenantId: string
  locale?: string
}

const requestContext = new RequestContext<UserContext>()
requestContext.set('userId', user.id)
requestContext.set('tenantId', tenant.id)
requestContext.set('locale', 'ko')

await agent.generate('계정 상태를 설명해 줘', {
  requestContext,
})
```

하위 구성 요소는 전달된 값을 읽어 요청별 동작을 결정한다.

```ts
const agent = new Agent({
  id: 'support-agent',
  instructions: ({ requestContext }) => {
    const locale = requestContext?.get('locale')
    return locale === 'ko'
      ? '한국어로 답한다.'
      : 'Respond in English.'
  },
  model: 'openai/gpt-5.6-sol',
})
```

`requestContextSchema`를 선언하면 필수 컨텍스트가 없거나 형식이 잘못된 실행을 구성 요소 진입점에서 차단할 수 있다.

```ts
requestContextSchema: z.object({
  userId: z.string(),
  tenantId: z.string(),
  locale: z.string().optional(),
})
```

## 왜 중요한가

요청별 값을 함수마다 개별 인자로 전달하면 호출 계층이 깊어질수록 서명이 오염되고 값 누락 가능성이 커진다. 반대로 요청 컨텍스트를 전역 상태처럼 지속시키면 서로 다른 사용자나 테넌트의 값이 섞일 수 있다. 요청 범위와 전달 경로를 명시하면 하위 구성 요소가 같은 실행 조건을 공유하면서도 요청 간 상태는 격리된다.

또한 인증 미들웨어가 채운 값과 구성 요소 스키마를 하나의 계약으로 맞추면, LLM·도구·워크플로가 실행되기 전에 누락된 인증 정보나 잘못된 테넌트 값을 발견할 수 있다. 이는 개인화와 동적 라우팅뿐 아니라 멀티테넌트 환경의 소유권 검증에도 직접 영향을 준다.

## 경계와 오해

- **요청 컨텍스트 ≠ 에이전트 메모리** — 요청 컨텍스트는 현재 호출의 실행 조건을 전달하고, 메모리는 여러 호출에 걸친 대화 기록과 지속 상태를 보존한다.
- **요청 컨텍스트 ≠ 무제한 전역 저장소** — 값의 수명은 요청 실행에 묶여야 하며, 장기 상태나 프로세스 전체 설정을 보관하는 장소가 아니다.
- **타입 선언 ≠ 런타임 검증** — 제네릭 타입은 컴파일 단계의 오류를 찾지만 외부에서 들어온 실제 값은 스키마로 별도 검증해야 한다.
- **컨텍스트에 값이 있음 ≠ 값이 신뢰됨** — 사용자·리소스·스레드 식별자는 인증과 소유권 검증을 거쳐 서버 측에서 설정해야 보안 경계가 된다.
- **raw 키 ≠ 일반 애플리케이션 키** — raw 접근은 스키마 밖의 인프라 데이터에 한정하고, 애플리케이션 값의 타입 검사를 우회하는 수단으로 쓰지 않는다.

## 함께 보는 개념

- [[thread-local]] — 둘 다 실행 흐름에 부가 데이터를 전달할 수 있지만, 요청 컨텍스트는 호출 경계에서 명시적으로 전달할 수 있고 스레드 로컬은 실행 스레드에 값이 결합된다.

## 출처

- [[mastra-request-context]] — Mastra에서 요청별 값을 에이전트·도구·워크플로로 전파하고 타입, 스키마, 예약 키로 검증·격리하는 방법을 설명한다.

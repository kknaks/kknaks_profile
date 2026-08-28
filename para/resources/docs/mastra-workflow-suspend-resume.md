# Mastra 워크플로 일시 중단과 재개

> 출처: https://mastra.ai/docs/workflows/suspend-and-resume · 2026-08-28

## 요지

- `suspend()`는 특정 단계에서 워크플로 실행을 멈추고 상태를 스냅샷으로 저장한다.
- `resume()`은 저장된 상태를 복원하고, 중단된 단계에 `resumeData`를 전달해 실행을 이어 간다.
- 스냅샷은 설정된 스토리지 공급자에 보관되므로 배포와 애플리케이션 재시작 이후에도 유지된다.
- `suspendData`로 중단 당시의 맥락을 재개 시점까지 전달할 수 있다.
- 시간 기반 대기인 `sleep()`·`sleepUntil()`은 `waiting`, 단계 내부의 `suspend()`는 `suspended` 상태를 만든다.

## 무엇에 대한 문서인가

Mastra 워크플로를 승인 요청, 외부 API 콜백, 사용자 입력, 비용이 큰 작업의 속도 제한처럼 즉시 완료할 수 없는 상황에서 중단하고 재개하는 방법을 설명한다.

중단 조건과 재개 데이터의 스키마 정의, 중단 경로 식별, 저장소에서 실행 상태를 복구하는 절차까지 다룬다. 사람의 승인을 기다리는 워크플로처럼 프로세스와 배포 수명을 넘어 실행 상태를 보존해야 할 때 읽을 문서다.

## 핵심 개념·절차

### 단계 중단

단계의 `execute`에서 `resumeData`를 검사하고 조건이 충족되지 않으면 `suspend()`를 반환한다. 이때 현재 실행 상태가 스냅샷으로 저장되고 실행 결과의 상태는 `suspended`가 된다. 재개 입력은 단계의 `resumeSchema`로 검증한다.

### 단계 재개

중단된 실행의 `run.resume()`에 `resumeData`와 대상 단계를 전달한다. 단계 객체를 전달하면 `resumeData`에 대한 타입 안전성을 얻고, 사용자 입력이나 데이터베이스에서 대상이 결정될 때는 단계 ID 문자열을 사용할 수 있다. 중단된 단계가 하나뿐이면 `step`을 생략해 마지막 중단 단계를 재개할 수 있다.

기존 `runId`만 가지고 있다면 `workflow.createRun({ runId })`로 실행 인스턴스를 먼저 복원한 뒤 `resume()`을 호출한다. 재개 호출은 HTTP 엔드포인트, 이벤트 처리기, 사용자 입력 처리 코드 또는 타이머 안에 둘 수 있다.

### 중단 데이터 유지

`suspend()`에 전달한 값은 재개된 단계의 `suspendData`에 그대로 제공된다. `suspendSchema`를 정의하면 중단 사유나 검토 대상 정보의 구조를 검증하면서 재개 이후에도 그 맥락을 사용할 수 있다.

### 중단 경로 식별

실행 결과의 `status`가 `suspended`인지 확인하고 `result.suspended` 배열에서 멈춘 단계 또는 중첩 워크플로의 ID를 찾는다. 이 값을 `resume()`의 `step`에 전달하면 해당 실행 경로를 지정해 재개할 수 있다.

### 저장소에서 실행 복구

`workflow.getWorkflowRunById()`로 저장된 실행 상태를 읽고 `createWorkflowStateReader()`로 감싸면 원시 스냅샷 구조를 직접 해석하지 않고도 중단 단계, 재개 레이블, 단계 입력과 출력을 조회할 수 있다. 중첩 워크플로는 `suspendedStep.path`를 재개 경로로 사용하며, `foreach` 반복의 특정 항목은 재개 레이블의 `foreachIndex`를 함께 전달한다.

### 시간 기반 대기

워크플로 수준의 `.sleep(ms)`는 지정된 밀리초 동안, `.sleepUntil(date)`은 지정 시각까지 실행을 미룬다. 두 메서드는 상태를 `waiting`으로 설정한다. 특정 단계 안에서 외부 입력을 기다리는 `suspend()`의 `suspended` 상태와 구분해야 한다.

## 코드·설정 예시

승인 전에는 중단하고 승인 데이터가 들어오면 같은 단계의 나머지 로직을 실행한다.

```ts
const approvalStep = createStep({
  id: 'user-approval',
  inputSchema: z.object({ userEmail: z.string() }),
  resumeSchema: z.object({ approved: z.boolean() }),
  suspendSchema: z.object({ reason: z.string() }),
  outputSchema: z.object({ output: z.string() }),
  execute: async ({ inputData, resumeData, suspend, suspendData }) => {
    if (!resumeData?.approved) {
      return await suspend({ reason: 'User approval required' })
    }

    return {
      output: `${inputData.userEmail}: ${suspendData?.reason}`,
    }
  },
})
```

실행 결과에서 중단된 경로를 찾아 재개할 수 있다.

```ts
const workflow = mastra.getWorkflow('testWorkflow')
const run = await workflow.createRun()
const result = await run.start({
  inputData: { userEmail: 'alex@example.com' },
})

if (result.status === 'suspended') {
  await run.resume({
    step: result.suspended[0],
    resumeData: { approved: true },
  })
}
```

프로세스 재시작 뒤에는 저장된 `runId`로 실행을 복원한다.

```ts
import { createWorkflowStateReader } from '@mastra/core/workflows'

const workflow = mastra.getWorkflow('testWorkflow')
const state = await workflow.getWorkflowRunById('run-123')

if (state?.status === 'suspended') {
  const reader = createWorkflowStateReader(state)
  const suspendedStep = reader.getSuspendedStep()
  const approvalLabel = reader.getResumeLabel('approve')
  const run = await workflow.createRun({ runId: state.runId })

  await run.resume({
    step: approvalLabel?.stepId ?? suspendedStep?.path,
    resumeData: { approved: true },
    forEachIndex: approvalLabel?.foreachIndex,
  })
}
```

## 함정·주의

- `resumeData`는 대상 단계의 `resumeSchema`와 일치해야 한다.
- 예시처럼 `if (!approved)`를 중단 조건으로 사용하면 `approved: false`도 다시 중단된다. 승인과 거절을 모두 최종 결정으로 처리하려면 값의 존재 여부와 승인 여부를 분리해 검사해야 한다.
- 여러 단계나 중첩 워크플로가 중단될 수 있다면 `step`을 생략하지 말고 `result.suspended` 또는 상태 리더로 정확한 경로를 지정하는 편이 안전하다.
- 단계 객체는 타입 안전성이 높지만, 런타임에 읽은 단계 ID를 사용할 때는 오타와 유효하지 않은 경로를 별도로 검증해야 한다.
- 스냅샷의 영속성은 구성된 스토리지 공급자에 의존한다. 저장소 설정 없이 배포나 프로세스 재시작을 넘는 복구를 기대해서는 안 된다.
- `waiting`과 `suspended`는 의미와 복구 방식이 다르므로 시간 지연에는 `sleep` 계열, 외부 데이터 입력에는 `suspend()`를 사용한다.

## 참고

- 문서 내 별도 참고 링크 명시 없음.
- 관련 API: `suspend()`, `resume()`, `createRun()`, `getWorkflowRunById()`, `createWorkflowStateReader()`, `.sleep()`, `.sleepUntil()`.

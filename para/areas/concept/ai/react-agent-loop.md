---
type: concept
id: react-agent-loop
title: ReAct 에이전트 루프
aliases:
  - ReAct
  - ReAct 패턴
  - 리액트 패턴
  - 추론 행동 관찰
  - 수동 툴 호출 루프
up:
  - C-039-implementing-react-tool-calling-loop-with-langchain
tags:
  - AI
  - 에이전트
  - 도구 호출
  - 실행 루프
---

# ReAct 에이전트 루프

**모델의 판단, 도구 실행, 실행 결과의 관찰을 반복해 답에 필요한 정보를 모으는 에이전트 실행 구조다.** 모델이 더 이상 도구를 요청하지 않고 텍스트를 반환하면 루프가 끝난다.

## 정의

ReAct 루프는 다음 세 동작을 순환한다.

1. **추론(Reason)** — 모델이 사용자 요청과 지금까지의 도구 실행 결과를 바탕으로 다음 행동을 정한다.
2. **행동(Act)** — 모델이 도구 이름과 인자를 구조화된 호출 요청으로 만들고, 애플리케이션이 실제 도구를 실행한다.
3. **관찰(Observe)** — 애플리케이션이 실행 결과를 원래 호출 ID와 연결해 메시지 기록에 추가하고 모델을 다시 호출한다.

```text
사용자 요청
    ↓
모델 판단 ── 도구 호출 없음 ──▶ 최종 텍스트
    │
    └─ 도구 호출 요청
             ↓
       이름·인자 검증
             ↓
          도구 실행
             ↓
 호출 ID가 붙은 결과 메시지
             └──────────────▶ 모델 판단으로 반복
```

도구가 독립적이면 한 번의 모델 응답에 여러 호출이 담길 수 있다. 뒤 도구의 입력이 앞 도구의 결과에 의존하면 관찰 결과를 모델에 돌려준 뒤 다음 호출을 받는 순차 반복이 필요하다.

## 사용 예시

다음은 LangChain 메시지 구조로 표현한 최소 실행 골격이다. 실제 환경에서는 도구별 입력 스키마 검증, 권한 검사, 타임아웃과 오류 분류를 더해야 한다.

```python
from langchain_core.messages import HumanMessage, ToolMessage


def run_agent(model_with_tools, tools_by_name, query, max_steps=8):
    messages = [HumanMessage(content=query)]

    for _ in range(max_steps):
        response = model_with_tools.invoke(messages)
        messages.append(response)

        if not response.tool_calls:
            return response.content

        for call in response.tool_calls:
            tool = tools_by_name[call["name"]]
            result = tool.invoke(call["args"])
            messages.append(
                ToolMessage(
                    content=str(result),
                    tool_call_id=call["id"],
                )
            )

    raise RuntimeError("도구 호출 횟수 제한을 초과했습니다.")
```

“LangChain 변경 사항을 검색해 팀 채널에 공지해 줘”라는 요청은 순차 호출의 예다. 모델은 먼저 웹 검색을 요청하고, 검색 결과를 관찰한 뒤 그 내용을 요약해 Slack 전송 도구의 인자로 사용한다.

## 왜 중요한가

도구 호출 기능만으로는 [[ai-agent]]가 완성되지 않는다. 모델이 만든 호출 요청을 누가 실행하는지, 결과를 어떤 메시지로 돌려주는지, 언제 반복을 끝내는지가 있어야 여러 도구를 조합한 작업이 실제로 진행된다.

루프를 직접 구현해 보면 모델과 실행기의 책임도 분리된다. 모델은 도구 선택과 인자 생성을 담당하고, 실행기는 허용 목록·권한·입력·예외·반복 한도를 통제한다. 이 구분은 프레임워크를 바꾸더라도 유지된다.

또한 호출과 결과의 기록은 에이전트의 실제 경로를 재구성하는 자료가 된다. 모델의 행동이 비결정적이어도 각 단계의 도구 이름, 인자, 호출 ID, 결과와 소요 시간을 남기면 실패 지점을 관찰하고 평가할 수 있다.

## 경계와 오해

- **도구 등록 ≠ 도구 실행** — 모델에 스키마를 바인딩하는 것은 호출 후보를 알려 주는 일이다. 요청된 함수를 실행하고 결과를 다시 넣는 루프는 별도 책임이다.
- **ReAct ≠ 내부 추론 전문 공개** — 애플리케이션이 필요로 하는 것은 구조화된 도구 호출과 관찰 결과이지, 모델의 비공개 사고 과정을 출력하는 일이 아니다.
- **`tool_call_id` ≠ 장식용 메타데이터** — 여러 호출이 있을 때 요청과 결과를 잇는 상관관계 키다. 누락하거나 바꾸면 결과의 주인이 불명확해진다.
- **반복 ≠ 무제한 재시도** — 최대 단계 수, 시간과 비용 한도, 동일 호출 감지 같은 종료 장치가 없으면 루프가 끝나지 않을 수 있다.
- **모델 선택 ≠ 업무 규칙 보장** — 모델은 복합 요청에서 필요한 도구를 빠뜨리거나 너무 일찍 답할 수 있다. 반드시 지켜야 하는 계산과 승인 규칙은 결정적 코드로 검증한다.
- **도구 결과 ≠ 신뢰된 명령** — 웹 검색이나 티켓에서 돌아온 문자열은 외부 입력이다. 그 안의 지시를 시스템 명령으로 따르지 않도록 경계를 둔다.
- **수동 루프 ≠ 워크플로우 오케스트레이션 전체** — 짧은 모델·도구 왕복을 제어하는 구조이며, 장기 상태 저장·승인 대기·보상 작업까지 다루는 [[workflow-orchestration]]과 범위가 다르다.

## 함께 보는 개념

- [[ai-agent]] — 이 루프가 도구를 선택하고 사용하는 실행 주체
- [[workflow-orchestration]] — 장기 실행과 여러 업무 단계를 명시적으로 조율하는 구조
- [[human-in-the-loop]] — 부작용이 크거나 되돌리기 어려운 도구 앞에 두는 승인 경계
- [[monitoring]] — 호출과 결과를 추적해 실제 실행 경로를 관찰하는 장치

## 출처

- [[C-039-implementing-react-tool-calling-loop-with-langchain]] — LangChain의 `bind_tools()` 이후 모델 판단, 도구 실행, 호출 ID가 붙은 `ToolMessage`, 재호출과 종료 조건을 직접 구현해 ReAct 사이클을 설명한다

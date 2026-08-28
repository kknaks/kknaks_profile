# LangChain 도구 호출과 ReAct 루프 직접 구현하기

> 출처: https://m.youtube.com/watch?v=OqSiCQKT1nU&ra=m · 판다스 스튜디오 · 13:33 · 2026-04-28

## 요지

- LLM은 외부 시스템을 직접 조작하지 않고, 도구의 이름·설명·입력 스키마를 바탕으로 어떤 도구를 어떤 인자로 호출할지 결정한다.
- LangChain의 `@tool`은 타입 힌트와 docstring이 있는 파이썬 함수를 LLM이 이해할 수 있는 도구 스키마로 변환한다.
- `bind_tools()`는 도구의 명세를 모델에 알려 줄 뿐이며, 요청된 함수를 실제로 실행하고 결과를 모델에 돌려주는 루프는 애플리케이션이 담당한다.
- 수동 ReAct 루프는 모델 판단, 도구 실행, `ToolMessage` 추가, 재호출을 반복하다가 도구 호출이 없는 최종 텍스트 응답에서 끝난다.
- 도구 실행 결과는 요청의 `tool_call_id`와 정확히 연결해야 모델이 여러 호출과 결과의 대응 관계를 파악할 수 있다.
- 복합 업무 자동화의 신뢰성은 도구 정의뿐 아니라 모델의 추론 능력, 반복 제어, 입력 검증, 예외 처리에도 좌우된다.

## 개요

이 교안은 LangChain의 `@tool`과 `bind_tools()`를 이용해 사내 일정 조회, 잔여 연차 확인, 휴가 일수 계산, Slack 공지, 헬프데스크 검색 같은 업무 함수를 LLM 도구로 만드는 방법을 다룬다. Tavily 웹 검색처럼 외부 API를 사용하는 도구도 같은 인터페이스로 결합할 수 있다.

핵심은 완성된 에이전트 함수를 사용하는 것이 아니라 도구 호출 과정을 직접 구현해 보는 데 있다. 이 과정을 이해하면 LLM이 실제로 함수를 실행하는 것이 아니라 호출 요청을 생성한다는 점, 애플리케이션이 그 요청을 실행해 관찰 결과를 다시 제공해야 한다는 점, 그리고 이 사이클이 ReAct의 추론·행동·관찰에 어떻게 대응하는지를 알 수 있다.

## 배경 / 사전 지식

LLM은 자연어를 생성하는 두뇌에 가깝고, 사내 데이터베이스 조회나 Slack 메시지 전송 같은 외부 작업을 자체적으로 수행하지는 못한다. 이런 기능은 일반 파이썬 함수나 API 클라이언트로 구현한 뒤 모델이 선택할 수 있는 ‘도구’로 공개해야 한다.

LangChain 도구에는 보통 다음 정보가 포함된다.

- 도구 이름: 모델이 호출 대상으로 식별하는 이름
- 설명: 언제 이 도구를 사용해야 하는지 알려 주는 docstring
- 입력 스키마: 인자 이름, 자료형, 필수 여부 등의 명세
- 실행 로직: 애플리케이션 환경에서 실제로 수행되는 코드

모델에는 주로 이름, 설명, 입력 스키마가 전달된다. 함수 내부 구현과 비밀 키를 모델이 읽는 것은 아니다. 다만 모델이 만든 인자가 실행 로직으로 들어오므로, 도구 경계에서 입력을 검증하고 권한을 통제해야 한다.

예제를 따라 하려면 Python 함수와 타입 힌트, LangChain의 메시지 구조(`HumanMessage`, `AIMessage`, `ToolMessage`), JSON과 API 호출에 대한 기본 지식이 필요하다. Tavily 검색을 실제로 실행하려면 인증 키를 환경 변수 또는 `.env` 파일에 설정해야 한다.

## 핵심 개념

### `@tool`로 함수와 스키마 정의하기

`@tool`은 일반 함수를 LangChain 도구 객체로 변환한다. 함수 이름은 기본 도구 이름이 되고, 타입 힌트는 입력 스키마를 만드는 데 쓰이며, docstring은 모델이 도구의 용도와 인자 형식을 판단하는 설명이 된다.

따라서 docstring에는 단순한 구현 설명보다 ‘어떤 요청에 사용해야 하는가’를 명확히 적어야 한다. 날짜를 받는다면 `YYYY-MM-DD`처럼 기대 형식도 함께 알려 주는 편이 좋다. 함수 본문은 실제 시스템 연동 전에는 하드코딩한 모의 데이터로 검증할 수 있다.

### `invoke()`와 `bind_tools()`의 역할 차이

`tool.invoke({...})`는 코드가 도구를 직접 실행하는 메서드다. 반면 `model.bind_tools(tools)`는 모델이 응답을 만들 때 참고하도록 도구 스키마를 등록한다. `bind_tools()`만 호출했다고 해서 모델이 요청한 함수가 자동 실행되지는 않는다.

바인딩된 모델은 필요하다고 판단하면 텍스트 대신 `tool_calls`를 포함한 `AIMessage`를 반환한다. 애플리케이션은 그 배열에서 도구 이름과 인자를 읽고, 이름에 해당하는 실제 도구를 찾아 실행해야 한다.

### `ToolMessage`와 `tool_call_id`

도구 실행 결과는 `ToolMessage`로 대화 기록에 추가한다. 이때 모델이 생성한 호출 ID를 `tool_call_id`에 그대로 넣어야 한다. 호출이 여러 개라면 이 ID가 각 요청과 결과를 연결하는 상관관계 키가 된다.

ID를 누락하거나 잘못 연결하면 모델은 어떤 실행 결과가 어느 요청에 대한 것인지 판단하기 어렵다. 이는 단일 도구 예제에서는 드러나지 않을 수 있지만 병렬 또는 연속 호출에서 중요한 오류 원인이 된다.

### ReAct: 추론, 행동, 관찰

ReAct 사이클은 다음 세 요소로 이해할 수 있다.

1. 추론(Reason): 모델이 현재 메시지와 관찰 결과를 보고 다음 작업을 판단한다.
2. 행동(Act): 모델이 도구 이름과 인자를 담은 호출을 요청하고 애플리케이션이 실행한다.
3. 관찰(Observe): 실행 결과를 `ToolMessage`로 모델에 돌려준다.

필요한 정보가 부족하면 모델이 다시 도구를 선택하고, 충분하면 도구 호출 없이 최종 텍스트를 생성한다. 실제 추론 전문이 외부에 노출되어야 한다는 뜻은 아니며, 애플리케이션 관점에서는 모델의 도구 선택과 메시지 흐름으로 이 구조를 관찰한다.

### 여러 도구를 조합하는 업무 자동화

한 요청이 여러 도구를 필요로 할 수 있다. 예를 들어 직원의 휴가 후 잔여 연차를 계산하려면 현재 잔여 연차 조회와 기간의 영업일 계산이 모두 필요하다. LangChain 변경 사항을 검색해 Slack에 알리는 요청은 웹 검색 결과를 먼저 얻은 뒤 그 내용을 요약하여 공지 도구에 전달해야 한다.

도구가 독립적이면 모델이 한 응답에서 여러 호출을 요청할 수 있지만, 두 번째 호출의 입력이 첫 번째 결과에 의존하면 순차적인 루프가 필요하다. 모델 성능에 따라 필요한 도구를 빠뜨리거나 너무 일찍 최종 답변을 만들 수 있으므로 업무 규칙을 프롬프트와 코드 양쪽에서 보강해야 한다.

## 작동 원리

수동 도구 호출 루프는 다음 순서로 동작한다.

1. 사용할 도구 목록을 만들고 이름을 키로 하는 매핑 테이블을 준비한다.
2. `bind_tools()`로 도구 스키마가 등록된 모델을 만든다.
3. 사용자 요청을 메시지 목록에 넣고 모델을 호출한다.
4. 반환된 `AIMessage`를 메시지 목록에 추가한다.
5. `tool_calls`가 없다면 메시지의 텍스트를 최종 답변으로 반환한다.
6. 호출이 있다면 각각의 이름과 인자를 검증하고 매핑된 도구를 `invoke()`로 실행한다.
7. 실행 결과를 원래 호출 ID가 포함된 `ToolMessage`로 만들어 메시지 목록에 추가한다.
8. 갱신된 전체 메시지를 모델에 다시 전달한다.
9. 모델이 최종 답변을 생성할 때까지 3~8단계를 반복한다.

예를 들어 “4월 15일 일정을 알려 줘”라는 요청을 받은 모델은 `get_schedule`과 날짜 인자를 담은 호출을 만든다. 애플리케이션이 일정을 조회해 결과를 돌려주면 모델은 관찰 결과를 자연어 답변으로 정리한다.

“LangChain의 변경점을 검색해 팀 채널에 공지해 줘”라는 요청에서는 먼저 웹 검색 도구가 실행된다. 그 결과를 본 모델이 요약된 메시지와 채널을 인자로 Slack 공지 도구를 호출하고, 공지 결과까지 확인한 후 최종 완료 응답을 생성한다.

## 코드 예시

다음 코드는 외부 서비스 없이도 구조를 확인할 수 있는 최소 예제다. `ChatGroq` 부분은 사용 중인 LangChain 호환 채팅 모델로 바꿀 수 있으며, 실행하려면 해당 공급자의 패키지와 인증 설정이 필요하다.

```python
from datetime import date
from typing import Any

from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool
from langchain_groq import ChatGroq


@tool
def get_schedule(day: str) -> list[str]:
    """지정한 날짜의 사내 일정을 조회한다. day는 YYYY-MM-DD 형식이다."""
    schedules = {
        "2026-04-15": ["10:00 제품 회의", "15:00 보안 교육"],
        "2026-04-16": ["14:00 분기 리뷰"],
    }
    return schedules.get(day, [])


@tool
def calculate_leave_days(start_date: str, end_date: str) -> int:
    """시작일과 종료일을 포함해 평일 기준 휴가 일수를 계산한다.

    날짜는 YYYY-MM-DD 형식이다. 이 예제는 주말만 제외하며 공휴일은 제외하지 않는다.
    """
    start = date.fromisoformat(start_date)
    end = date.fromisoformat(end_date)
    if start > end:
        raise ValueError("start_date는 end_date보다 늦을 수 없습니다.")

    return sum(
        1
        for offset in range((end - start).days + 1)
        if date.fromordinal(start.toordinal() + offset).weekday() < 5
    )


def run_tool_loop(user_query: str, max_steps: int = 8) -> str:
    tools = [get_schedule, calculate_leave_days]
    tool_map = {item.name: item for item in tools}

    model = ChatGroq(model="qwen-qwq-32b", temperature=0)
    model_with_tools = model.bind_tools(tools)
    messages = [HumanMessage(content=user_query)]

    for _ in range(max_steps):
        ai_message = model_with_tools.invoke(messages)
        messages.append(ai_message)

        if not ai_message.tool_calls:
            return str(ai_message.content)

        for call in ai_message.tool_calls:
            tool_name = call["name"]
            selected_tool = tool_map.get(tool_name)
            if selected_tool is None:
                result: Any = {"error": f"허용되지 않은 도구: {tool_name}"}
            else:
                try:
                    result = selected_tool.invoke(call["args"])
                except Exception as exc:
                    result = {"error": type(exc).__name__, "message": str(exc)}

            messages.append(
                ToolMessage(
                    content=str(result),
                    tool_call_id=call["id"],
                )
            )

    raise RuntimeError("도구 호출 최대 횟수를 초과했습니다.")


if __name__ == "__main__":
    print(run_tool_loop("2026년 4월 15일의 사내 일정을 알려 줘."))
```

`tool_map`은 모델이 반환한 문자열 이름을 실제 도구 객체로 연결한다. 루프는 `AIMessage`를 먼저 기록한 뒤 각 실행 결과를 동일한 호출 ID의 `ToolMessage`로 추가한다. `max_steps`는 모델이 같은 도구를 계속 호출하는 상황을 막는 안전장치다. 예제의 휴가 계산은 주말만 제외하므로 실제 사내 규정에 적용하려면 공휴일 달력과 반차·시간차 규칙을 별도로 반영해야 한다.

## 함정·실수

- `bind_tools()`가 도구 실행까지 해 준다고 오해하기 쉽다. 이 메서드는 명세만 모델에 전달하므로 실행기와 반복 루프가 별도로 필요하다.
- 모호하거나 부정확한 docstring, 빠진 타입 힌트, 날짜 형식 미지정은 잘못된 도구 선택과 인자를 유발한다. 각 인자의 의미와 허용 형식을 구체적으로 적는다.
- `ToolMessage`에 `tool_call_id`를 넣지 않거나 다른 호출의 ID를 넣으면 요청과 결과의 연결이 깨진다. 모델이 반환한 ID를 변경하지 않고 사용한다.
- 모델이 만든 도구 이름과 인자를 그대로 신뢰하면 존재하지 않는 도구 호출, 잘못된 날짜, 권한 밖 채널 전송 같은 문제가 생긴다. 허용 목록, 스키마 검증, 업무 권한 검사를 실행 직전에 적용한다.
- 종료 조건이나 최대 반복 횟수가 없으면 오류 결과를 받은 모델이 같은 호출을 무한히 반복할 수 있다. 호출 횟수, 시간, 비용 한도를 설정한다.
- 휴가 일수 계산에서 주말만 제외하고 공휴일을 무시하면 실제 규정과 다른 결과가 나온다. 회사 캘린더와 휴일 API를 명시적으로 연동한다.
- 도구가 반환한 웹 문서나 티켓 내용은 신뢰할 수 없는 외부 입력이다. 그 안의 지시를 시스템 명령처럼 따르지 않도록 프롬프트 인젝션 방어와 출력 필터링이 필요하다.
- 모델의 성능에 따라 복합 요청에 필요한 도구 하나를 누락할 수 있다. 영상의 휴가 계산 사례처럼 잔여 연차만 조회하고 공휴일이나 영업일 계산을 빠뜨리는 결과가 나올 수 있다.
- Slack 전송처럼 부작용이 있는 도구를 연습용 하드코딩 함수에서 실서비스 API로 교체할 때는 중복 실행과 오발송 위험이 생긴다. 미리보기와 사용자 승인을 거치는 편이 안전하다.

## 베스트 프랙티스

- 도구는 한 가지 책임만 갖도록 작게 설계하고, 이름을 `get_schedule`, `calculate_leave_days`처럼 동작이 드러나게 정한다.
- docstring은 사용 조건, 입력 형식, 반환 의미, 중요한 제한을 포함하도록 작성하고 실제 실행 로직과 항상 일치시킨다.
- 모델이 사용할 도구 집합을 요청과 사용자 권한에 따라 최소화한다. 모든 사용자에게 모든 사내 도구를 바인딩하지 않는다.
- 읽기 전용 도구와 쓰기 도구를 구분한다. Slack 발송, 결재, 데이터 변경 같은 작업은 최종 실행 전에 명시적 승인 단계를 둔다.
- 도구 출력은 가능한 한 구조화된 JSON 형태로 반환한다. 오류도 예외 문자열만 던지기보다 오류 코드와 재시도 가능 여부를 포함한 구조로 제공한다.
- 호출 횟수, 실행 시간, API 비용, 재시도 횟수에 상한을 두고 타임아웃과 예외 처리 경로를 마련한다.
- 도구 이름, 인자, 호출 ID, 소요 시간, 성공 여부를 관측 가능하게 기록하되 인증 키와 개인정보는 로그에서 제거한다.
- 단일 호출, 순차 호출, 병렬 호출, 결과 없음, 잘못된 인자, 외부 API 실패를 각각 테스트한다. 특히 복합 업무는 필요한 도구 목록과 최종 답을 기준으로 평가한다.
- 모델이 반드시 확인해야 할 업무 규칙은 자연어 프롬프트에만 맡기지 말고 결정적 코드로 검증한다. 예를 들어 잔여 연차는 `현재 잔여 연차 - 검증된 휴가 일수`로 애플리케이션이 계산할 수 있다.
- 직접 만든 루프로 원리를 익힌 뒤에는 LangChain의 에이전트 생성 기능을 사용해 상태 관리와 실행 제어를 단순화할 수 있다. 그래도 권한, 검증, 승인, 관측성 같은 운영 책임은 애플리케이션에 남는다.

## 참고

- LangChain `@tool` 데코레이터와 도구의 `invoke()` 인터페이스
- LangChain 채팅 모델의 `bind_tools()` 메서드
- LangChain `AIMessage.tool_calls`와 `ToolMessage`
- Tavily 웹 검색 API 및 LangChain 검색 도구
- LangChain의 에이전트 생성 함수(`create_agent`)
- ReAct 패턴: Reason, Act, Observe 사이클
- 영상에서는 다음 차시에서 완성형 에이전트 기능을 더 자세히 다룰 예정이라고 안내한다.

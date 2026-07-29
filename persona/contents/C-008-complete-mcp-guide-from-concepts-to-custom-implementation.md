---
concept:
- LLM은 다음 단어를 예측하는 언어 모델일 뿐이므로, 실시간 정보(날씨 등)가 필요한 경우 할루시네이션이 발생한다.
- 도구 호출(Tool Calling)로 LLM이 필요한 작업을 외부 API에 위임하고 그 결과를 기반으로 정확한 답변을 생성할 수 있다.
- MCP는 AI와 도구를 연결하는 표준 프로토콜로, USB-C처럼 각 도구가 표준 규격을 따르면 새로운 개발 없이 바로 연동 가능하다.
- FastMCP 같은 라이브러리를 사용하면 @MCP.tool 어노테이션으로 Python 함수를 MCP 표준에 맞추는 것이 매우 간단하다.
- stdio(로컬 명령어 기반)와 streamable HTTP(원격 웹 서비스)의 두 가지 연결 방식으로 로컬 또는 클라우드 MCP 서버를 구성할
  수 있다.
date: 2026-05-07
day: Day 08
duration: '25:24'
enriched_at: '2026-05-07T09:53:55+09:00'
id: C-008
kind: tutorial
speaker: 조코딩 JoCoding
status: published
summary:
  en: 'Master connecting LLMs with external tools: understand MCP fundamentals, integrate
    existing protocols, and build custom MCP servers with FastMCP'
  ko: LLM의 할루시네이션 극복부터 MCP 표준 프로토콜 개념, 기존 MCP 연결, 직접 구현까지 AI와 외부 도구 통합의 모든 것
tags:
- '#mcp'
- '#llm'
- '#fastmcp'
- '#ai-integration'
- '#claude-desktop'
- '#api'
- '#python'
title:
  en: 'Complete MCP Guide: From Concepts to Custom Implementation'
  ko: 'MCP(Model Context Protocol) 완벽 가이드: 개념부터 직접 구현까지'
transcript: true
type: content
youtubeId: 46HxP7kO9oY
---

## 개요

AI 모델의 놀라운 성능에도 불구하고, 실시간 정보나 개인화된 데이터에 접근해야 하는 순간 한계에 부딪힌다. 이 한계를 극복하기 위해 등장한 것이 **MCP(Model Context Protocol)**이다. 2024년 11월 Anthropic이 발표한 MCP는 AI 모델과 외부 도구(API, 서비스, 데이터베이스 등)를 표준화된 방식으로 연결하는 프로토콜이다. 이 교안을 통해 MCP의 개념부터 실제 사용, 그리고 직접 MCP를 만드는 방법까지 체계적으로 학습할 수 있다.

## 배경 / 사전 지식

### Large Language Model (LLM)
LLM은 엄청난 양의 텍스트 데이터로 훈련된 신경망 모델로, 주어진 입력에 대해 다음에 올 가능성이 높은 단어를 예측하는 방식으로 작동한다. 예를 들어, "오늘 날씨"라는 질문이 들어오면 LLM은 학습된 패턴을 바탕으로 "맑습니다", "흐립니다" 같은 그럴듯한 답변을 생성할 수 있지만, 이는 실제 날씨 정보가 아니라 단순한 확률 기반 예측일 뿐이다.

### 할루시네이션 (Hallucination)
할루시네이션은 LLM이 학습 데이터에 없는 정보를 마치 사실인 것처럼 생성하는 현상이다. LLM이 "12도, 맑음"이라고 답하더라도 그것이 오늘의 실제 날씨는 아닐 수 있다는 뜻이다. 이는 모델의 근본적 한계가 아니라, 실시간 정보나 개인 데이터에 대한 접근 부족 때문이다.

### API (Application Programming Interface)
API는 외부 서비스나 데이터에 접근하기 위한 규칙 집합이다. 날씨 API, 이메일 API, 캘린더 API 등이 있으며, 이들을 이용하면 AI가 실시간 정보나 개인 데이터에 접근할 수 있다.

### 프로토콜 (Protocol)
프로토콜은 통신 방식의 표준 규약이다. 우편 봉투의 예를 들면, 보내는 사람 주소는 왼쪽 위, 받는 사람 주소는 오른쪽 아래, 우표는 오른쪽 위라는 정해진 규칙이 있다. 마찬가지로 통신 프로토콜도 "어떤 형식으로", "어떤 데이터를 포함해서", "어떻게 응답할 것인지" 같은 규칙을 정한다.

## 핵심 개념

### 1. Tool Calling (도구 호출)
LLM이 자신의 능력만으로는 답할 수 없는 작업을 인식하고, 외부 도구(함수, API)를 호출하여 그 결과를 받아 최종 답변을 구성하는 메커니즘이다. 예를 들어:

```
사용자: "오늘 날씨 알려줘"
→ LLM: "날씨를 알아야 하니 날씨 API를 호출하겠습니다"
→ 날씨 API 호출 → 응답: "15도, 맑음"
→ LLM: "오늘 날씨는 15도로 맑습니다"
```

Tool Calling 덕분에 LLM의 할루시네이션을 크게 줄이고 정확한 정보를 제공할 수 있다.

### 2. MCP (Model Context Protocol)
MCP는 AI 모델(Claude 등)과 외부 도구를 연결하기 위한 **표준화된 프로토콜**이다. Anthropic이 2024년 11월에 발표했으며, 다음과 같은 특징이 있다:

- **표준화**: 각 도구가 MCP 표준을 따르면 새로운 개발 없이 바로 AI와 연동 가능
- **확장성**: 누구든 MCP를 따르는 새로운 도구를 만들고 AI에 연결할 수 있음
- **단순성**: USB-C처럼 하나의 규격으로 모든 도구를 통일

**비유**: USB-C가 나오기 전에는 삼성은 USB-B, 애플은 30핀 커넥터 같이 제각각이었다. 하지만 USB-C라는 표준이 생기자 "어떤 기기든 USB-C 케이블만 있으면 된다"는 편의성이 생겼다. MCP도 마찬가지다.

### 3. MCP 클라이언트 vs MCP 서버

**MCP 클라이언트**: MCP 표준을 따르는 도구들과 연결할 수 있는 대상
- Claude Desktop (Anthropic)
- Visual Studio Code (확장 프로그램)
- Cursor

**MCP 서버**: MCP 표준을 따르는 도구
- ContextEL (개발 문서 접근)
- Blender (3D 제작)
- Notion (노트 앱)
- 직접 만드는 커스텀 MCP

클라이언트가 서버를 "꽂아서" 사용하는 구조다.

## 작동 원리

### 1단계: 사용자 입력
사용자가 Claude에 질문이나 요청을 입력한다.
```
"Next.js로 새 앱을 만드는 명령어를 찾아줘"
```

### 2단계: MCP 필요성 판단
Claude가 답변에 외부 정보가 필요함을 인식한다.
```
→ "개발 문서가 필요하니 ContextEL MCP를 호출하겠습니다"
```

### 3단계: MCP 도구 호출
Claude가 MCP 서버의 도구를 호출한다.
```
ContextEL MCP에 "Next.js 앱 초기화 방법" 요청
```

### 4단계: 응답 수신
MCP 서버가 최신 공식 문서를 조회하여 응답한다.
```
ContextEL MCP → "npx create-next-app@latest my-app"
```

### 5단계: 최종 답변 생성
Claude가 MCP의 응답을 바탕으로 사용자에게 정확한 답변을 준다.
```
"Next.js 공식 문서에 따르면 다음 명령어를 사용하세요: npx create-next-app@latest my-app"
```

## 코드 예시

### FastMCP를 이용한 간단한 MCP 구현

MCP는 복잡할 것처럼 보이지만, **FastMCP** 라이브러리를 사용하면 매우 간단하다. 다음은 두 수를 더하는 간단한 MCP 서버다:

```python
from fastmcp import FastMCP

# MCP 인스턴스 생성
mcp = FastMCP("add-tool")

# @MCP.tool 데코레이터로 도구 정의
@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """두 수를 더한다"""
    return a + b

# 다른 기능도 추가 가능
@mcp.tool()
def get_weather(location: str) -> str:
    """location의 날씨를 반환한다"""
    # 실제로는 날씨 API를 호출
    return f"{location}의 날씨: 맑음, 15도"

# 서버 실행
if __name__ == "__main__":
    mcp.run()
```

**코드 설명:**
- `FastMCP("add-tool")`: MCP 서버 인스턴스 생성 (이름: add-tool)
- `@mcp.tool()`: 이 함수를 MCP 표준 도구로 등록
- `add_numbers(a: int, b: int)`: 매개변수 타입 정의 (MCP가 AI에게 어떤 파라미터를 받아야 할지 알려줌)
- `mcp.run()`: 로컬 호스트의 특정 포트(기본 8000)에서 MCP 서버 시작

### 서버 실행 및 Claude와 연결

```bash
# 1. FastMCP 설치
pip install fastmcp

# 2. 위 코드를 app.py로 저장하고 실행
python app.py
# 출력: MCP 서버가 localhost:8000에서 실행 중
```

### Claude Desktop에서 연결

Claude Desktop의 설정 파일(`claude_desktop_config.json`)에 다음을 추가:

```json
{
  "mcpServers": {
    "add-tool": {
      "command": "python",
      "args": ["/path/to/app.py"]
    }
  }
}
```

또는 Visual Studio Code에서:
1. Cmd+Shift+P (또는 Ctrl+Shift+P) 입력
2. "MCP Connect" 검색
3. "Add Server" 선택
4. HTTP 방식으로 `http://localhost:8000` 연결

연결 후 Claude에서 다음처럼 사용 가능:
```
"add_numbers 도구를 사용해서 5 + 3을 계산해줘"
→ Claude가 자동으로 add_numbers(5, 3) 호출 → 결과: 8
```

## 함정·실수

### 1. MCP 표준을 무시하고 직접 API를 구현하기
**실수**: "그냥 내가 API를 직접 AI에 통합하면 되지 않을까?"

**문제점**:
- 각 API마다 다른 형식으로 통합해야 함
- API 변경 시 AI 코드도 수정해야 함
- 팀 전체에서 표준이 없어 유지보수 어려움

**해결책**: MCP 표준을 따르면 "Slack MCP, Notion MCP, 날씨 MCP"를 동일한 방식으로 다룰 수 있다.

### 2. 잘못된 연결 방식 선택
**실수**: "HTTP 방식이 항상 더 좋지 않을까?"

**실제로**:
- **stdio**: 로컬, 보안 필요, 빠른 응답 → 로컬 MCP에 적합
- **HTTP**: 원격 서버, 공개 서비스, 수평 확장 필요 → 클라우드 배포 MCP에 적합

**해결책**: 사용 사례에 따라 신중히 선택

### 3. MCP 도구의 매개변수 타입을 명시하지 않기
**실수**:
```python
@mcp.tool()
def calculate(x, y):  # 타입 명시 없음
    return x + y
```

**문제점**: Claude가 "x와 y가 무엇인지" 알 수 없음 → 도구를 제대로 호출하지 못함

**해결책**:
```python
@mcp.tool()
def calculate(x: int, y: int) -> int:  # 타입 명시
    return x + y
```

### 4. 도구 설명(docstring)이 불명확함
**실수**:
```python
@mcp.tool()
def fetch_data(url: str) -> str:
    """데이터를 가져온다"""  # 너무 모호
    return requests.get(url).text
```

**해결책**:
```python
@mcp.tool()
def fetch_data(url: str) -> str:
    """HTTP GET 요청으로 웹사이트 내용을 텍스트로 반환한다. 타임아웃: 10초"""
    return requests.get(url, timeout=10).text
```

## 베스트 프랙티스

### 1. 어떤 도구를 MCP로 만들 가치가 있는가?
MCP를 만들기 전에 다음을 확인하세요:

- **AI가 단독으로 할 수 없는 일인가?** (예: 실시간 데이터 조회, 파일 생성, 외부 시스템 제어)
- **여러 AI 모델이 사용할 가능성이 있는가?** (예: 회사 내부 도구)
- **API가 안정적인가?** (변경 빈도가 적어야 함)

예: 블렌더(3D 도구)는 "사용 방법이 복잡하지만 AI가 자동화할 수 있다"는 점에서 MCP로 만들 가치가 높다.

### 2. 문서화는 필수
MCP 도구를 공개할 계획이라면 다음을 포함하세요:
- 도구의 목적과 사용 사례
- 각 매개변수의 설명 및 제약사항
- 반환값의 형식
- 에러 처리 방식

### 3. 보안 고려사항

**stdio 방식**:
- 로컬 실행이므로 상대적으로 안전
- 하지만 로컬 파일 접근 권한 제한 필요

**HTTP 방식**:
- 원격 호출이므로 인증(API 키 등) 필수
- HTTPS 사용 강제
- 요청 검증 필수 (예: 허용된 매개변수 범위 확인)

예시:
```python
import os
from functools import wraps

API_KEY = os.getenv("MCP_API_KEY")

def require_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 인증 검증 로직
        return func(*args, **kwargs)
    return wrapper

@mcp.tool()
@require_auth
def sensitive_operation(param: str) -> str:
    return f"결과: {param}"
```

### 4. 성능 최적화
- **캐싱**: 반복 호출이 많은 도구는 결과를 캐시
- **타임아웃**: 오래 걸리는 작업은 적절한 타임아웃 설정
- **에러 처리**: 부분 실패를 명확히 표시

```python
from functools import lru_cache

@mcp.tool()
@lru_cache(maxsize=128)
def get_documentation(framework: str) -> str:
    """개발 프레임워크 문서를 캐시하여 조회"""
    # API 호출
    return fetch_docs(framework)
```

### 5. 테스트 중요성
MCP 도구는 AI를 통해서만 테스트하지 말고, 직접 단위 테스트를 작성하세요:

```python
import unittest

class TestAddTool(unittest.TestCase):
    def test_add_positive(self):
        result = add_numbers(5, 3)
        self.assertEqual(result, 8)
    
    def test_add_negative(self):
        result = add_numbers(-5, 3)
        self.assertEqual(result, -2)

if __name__ == "__main__":
    unittest.main()
```

## 참고

**공식 자료:**
- [Anthropic MCP 공식 문서](https://modelcontextprotocol.io)
- [Claude Desktop 다운로드](https://claude.ai/download)
- [FastMCP GitHub](https://github.com/jina-ai/fastmcp)

**MCP 디렉토리:**
- [Smithery](https://smithery.ai) - 6,300개 이상의 공개 MCP 서버 검색 가능
- [MCP 서버 배포 가이드](https://docs.getporter.ai/ko/mcp)

**영상에서 언급된 추가 자료:**
- Node.js MCP 예제: https://github.com/cloudtype-examples/mcp-server-node
- Python FastMCP 예제: https://github.com/cloudtype-examples/fastmcp
- Porter AI 문서: https://docs.getporter.ai/ko/mcp
- [Slack과 MCP 연결 가이드](https://youtu.be/Y3AK40FVCbw)
- [Notion MCP + Slack 자동화](https://youtu.be/p-N5MEBmu3o)

**커뮤니티 & 학습:**
- Blender 3D MCP 예시
- Figma 디자인 도구 MCP
- Notion 노트 앱 MCP
- 캘린더/일정 관리 MCP
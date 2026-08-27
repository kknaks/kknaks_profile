---
type: content
id: C-011
date: 2026-05-13
duration: '24:17'
speaker: 개발동생
kind: study
youtubeId: y5cze4tAXZU
title:
  en: 'OpenCode: Open-Source AI Coding Agent Supporting Any LLM Model'
  ko: 'OpenCode: 어떤 LLM이든 쓸 수 있는 오픈소스 코딩 에이전트'
summary:
  en: Learn OpenCode, an open-source CLI coding agent supporting any LLM, and extend it with Oh-My-OpenCode orchestration plugin
  ko: CLI 기반 오픈소스 코딩 에이전트 OpenCode로 Claude, GPT, Gemini 등 모든 LLM을 자유롭게 사용하고, Oh-My-OpenCode 플러그인으로 에이전트를 오케스트레이션하는 방법
tags:
- '#opencode'
- '#coding-agent'
- '#llm'
- '#cli'
- '#open-source'
- '#ai-development'
- '#claude-alternative'
---

## 요지

- OpenCode는 Claude Code의 오픈소스 대체제로 CLI 기반이면서도 Claude, GPT, Gemini, 로컬 모델 등 어떤 LLM이든 통합 사용 가능하다.
- Cursor는 IDE 내장형 에이전트, Claude Code는 CLI 기반 에이전트인데, OpenCode는 Claude Code의 사용성을 유지하면서 모델 제약을 제거했다.
- OpenCode의 핵심 기능은 LSP 지원, 서브 에이전트 병렬 실행, 세션 공유(Share Link), 플랜/빌드 모드 전환, MCP 통합이다.
- Oh-My-OpenCode는 한국 개발자가 24,000달러 토큰 비용으로 검증한 플러그인으로, 작업 특성에 맞게 최적 모델을 자동 선택하는 오케스트레이션을 제공한다.
- OpenCode Genie 프로바이더는 OpenCode가 검증한 모델들을 한 곳에 모아두어 여러 API 키 대신 단일 프로바이더로 모든 모델에 접근할 수 있게 한다.

## 개요

OpenCode는 최근 개발자 커뮤니티에서 주목받는 새로운 코딩 에이전트입니다. Claude Code의 탁월한 CLI 인터페이스와 기능성을 갖춘 오픈소스 대체제이면서, **어떤 LLM 모델이든 자유롭게 사용할 수 있다는 핵심 장점**을 제공합니다. 기존에는 모델 제약으로 불편했던 개발자들이 OpenCode를 통해 프로젝트 특성에 맞춰 최적의 모델을 선택할 수 있게 되었습니다. 더불어 한국 개발자가 만든 Oh-My-OpenCode 플러그인을 활용하면 여러 모델을 상황에 맞게 조합하여 사용할 수 있어, 현대적인 에이전트 기반 개발의 새로운 표준이 되고 있습니다.

## 배경 / 사전 지식

### 코딩 에이전트란?
코딩 에이전트는 LLM(Large Language Model)을 기반으로 개발자의 명령을 받아 자동으로 코드를 작성, 수정, 검토하는 AI 도구입니다. 터미널, IDE, 웹 브라우저 등 다양한 인터페이스로 제공됩니다.

### 주요 코딩 에이전트 비교

**Cursor**: IDE 형태의 에이전트로, VS Code를 기반으로 코드 에디터 내부에서 AI와 채팅하며 실시간으로 코드 변경을 시각적으로 확인할 수 있습니다. 장점은 직관적인 UI이지만, 고정된 에디터에 종속되고 더 많은 CPU/메모리를 필요로 합니다.

**Claude Code**: Anthropic이 만든 CLI 기반 에이전트로, 터미널에서 동작하므로 어떤 코드 에디터에도 함께 사용 가능하고 리소스 효율이 좋습니다. Claude 모델의 뛰어난 성능과 함께 클로드 스킬, 서브 에이전트 등 강력한 기능을 제공합니다. 다만 **Anthropic의 Claude 모델만 사용 가능**하다는 단점이 있습니다.

**OpenCode**: Claude Code와 유사한 CLI 기반 구조를 갖추면서, **OpenAI, Google, 로컬 모델 등 어떤 LLM이든 사용할 수 있는 유연성**을 제공하는 오픈소스 프로젝트입니다.

### 용어 정의

- **LSP (Language Server Protocol)**: 코드 에디터가 변수, 함수, 클래스의 위치, 타입, 설명 등을 빠르게 인식하고 자동완성, 오류 검출을 수행하도록 하는 프로토콜
- **프로바이더 (Provider)**: LLM 서비스를 제공하는 회사/플랫폼 (OpenAI, Anthropic, Google 등)
- **서브 에이전트 (Sub-agent)**: 복잡한 작업을 병렬로 처리하기 위해 여러 에이전트를 동시에 실행하는 기능
- **MCP (Model Context Protocol)**: LLM이 외부 도구나 데이터에 접근할 수 있도록 해주는 표준 프로토콜

## 핵심 개념

### 1. OpenCode의 정의와 특징

OpenCode는 오픈소스 기반의 CLI 코딩 에이전트로, Claude Code의 강점을 유지하면서 모델 선택의 자유도를 극대화합니다.

**핵심 특징:**
- **오픈소스**: GitHub에서 소스코드 공개 및 커뮤니티 기여 가능
- **CLI 기반**: 터미널에서 실행되므로 특정 에디터에 종속되지 않음
- **멀티 LLM 지원**: Claude, GPT, Gemini, 로컬 모델 등 모든 LLM 통합 가능
- **터미널 UI**: 클로드 코드 수준의 깔끔한 인터페이스 (제어+P 커맨드 검색 포함)
- **리소스 효율**: IDE 방식보다 CPU/메모리 소비 적어 대규모 병렬 작업에 유리

### 2. 플랜 모드 vs 빌드 모드

OpenCode는 두 가지 작업 모드를 제공합니다.

**플랜 모드 (Plan Mode)**
- 에이전트가 작업을 즉시 수행하지 않음
- 사용자의 프롬프트 분석 → 프로젝트 구조 분석 → 개발 계획 수립 → 승인 후 실행
- 복잡하거나 대규모 작업에 적합
- 계획 단계에서 사용자가 수정·피드백 가능

**빌드 모드 (Build Mode)**
- 사용자의 명령을 바로 실행
- 계획 수립 없이 즉시 개발 진행
- 간단한 수정이나 빠른 프로토타이핑에 적합
- Tab 키로 모드 전환 가능

### 3. 프로바이더 (Provider) 시스템

OpenCode는 다양한 LLM 프로바이더를 통합하는 프로바이더 시스템을 갖추고 있습니다.

**주요 프로바이더:**

| 프로바이더 | 지원 모델 | 방식 |
|----------|---------|------|
| **OpenCode Genie** | GPT-4o/5.1/5.2, Claude 4.5/Opus/Haiku, Gemini, MiniMax, GLM 등 | 단일 API 키로 모든 모델 접근 (추천) |
| **Anthropic** | Claude Pro/Max, API 키 | Claude 구독 또는 API 기반 |
| **OpenAI** | GPT 시리즈 | API 키 기반 |
| **Google** | Gemini 시리즈 | API 키 기반 |
| **GitHub Copilot** | Copilot 모델 | GitHub 계정 연동 |

**OpenCode Genie의 장점:**
- OpenCode가 직접 검증한 모델들만 선별
- 여러 프로바이더의 API 키를 하나로 통합
- 원본 프로바이더의 가격 유지 (종량제)
- 프로바이더별 API 키 관리 없이 통일된 인터페이스 제공

### 4. Oh-My-OpenCode 플러그인

Oh-My-OpenCode는 한국 개발자 영규님이 만든 OpenCode 오케스트레이션 플러그인입니다.

**개발 배경**: 작성자가 OpenCode로 24,000달러 규모의 토큰 비용을 사용하며 다양한 LLM을 실험한 경험을 바탕으로 제작

**핵심 기능**:
- **모델 오케스트레이션**: 작업 유형에 따라 최적의 모델을 자동 선택
  - 프론트엔드 개발 → Gemini (시각 능력 우수)
  - 문서 작성 → Claude (글쓰기 능력 우수)
  - 빠른 프로토타이핑 → GPT (속도 우수)
- **비용 최적화**: 작업 복잡도에 맞춰 저가 모델부터 고가 모델까지 활용
- **프리셋 제공**: 일반적인 개발 작업용 미리 설정된 모델 조합

**커뮤니티 영향**: GitHub에서 10,000+ 스타를 받으며 개발자들의 큰 관심을 받고 있음

## 작동 원리

### OpenCode 설치 및 초기 설정 단계

**1단계: 설치**
```bash
# 공식 웹사이트 (https://opencode.ai/) 방문
# 설치 명령어 선택 (curl, npm, pnpm, yarn 중 선택)

curl -fsSL https://opencode.ai/install.sh | bash
# 또는
npm install -g opencode
```

**2단계: OpenCode 실행**
```bash
opencode
```
터미널에서 깔끔한 CLI UI가 나타나 대기 상태로 진입합니다.

**3단계: 프로바이더 연결**
```bash
/connect
```
OpenCode Genie, Anthropic, OpenAI, Google, GitHub Copilot 등 원하는 프로바이더 선택 및 API 키 설정

**4단계: 모델 확인**
```bash
/models
```
현재 사용 가능한 모델 목록 확인 및 기본 모델 설정

### 작업 흐름

**플랜 모드 워크플로우:**
1. Tab 키로 플랜 모드 활성화
2. 프롬프트 입력 (예: "React 컴포넌트 만들어줘")
3. OpenCode가 프로젝트 구조 분석 및 개발 계획 수립
4. 생성된 계획 검토 및 수정
5. Enter로 실행 승인
6. 에이전트가 단계별 구현 진행

**빌드 모드 워크플로우:**
1. Tab 키로 빌드 모드 활성화
2. 프롬프트 입력
3. 즉시 에이전트 실행 (계획 단계 생략)
4. 터미널에서 실시간 작업 진행 모니터링

### 주요 명령어 체계

| 명령어 | 기능 |
|-------|------|
| `/models` | 사용 가능한 모델 목록 조회 |
| `/connect` | 프로바이더 연결/설정 |
| `/init` | 프로젝트 구조 자동 분석 및 CLAUDE.md 생성 |
| `/share` | 현재 세션을 URL로 공유 (브라우저에서 타인과 공동 작업) |
| `/new` | 새 세션 시작 |
| `/session` | 기존 세션 목록 조회 및 재진입 |
| `/mcp` | MCP 도구 관리 |
| Ctrl+P | 커맨드 검색 및 빠른 실행 (사이드바 표시/숨김 등) |
| Tab | 플랜/빌드 모드 전환 |

### OpenCode Genie 프로바이더 연결 절차

**1단계: OpenCode Genie 계정 생성**
- https://genie.opencode.ai 방문
- 계정 가입 및 로그인

**2단계: API 키 발급**
- 대시보드에서 API 키 생성
- 클립보드에 복사

**3단계: OpenCode에서 설정**
```bash
/connect
# OpenCode Genie 선택
# 발급받은 API 키 입력
```

**4단계: 모든 모델 접근 확인**
```bash
/models
# GPT, Claude, Gemini 등 모든 모델이 나열됨
```

## 코드 예시

### 예시 1: OpenCode CLI 기본 사용

```bash
# OpenCode 실행
opencode

# 터미널 UI에서 프롬프트 입력
> React useState를 사용하는 카운터 컴포넌트를 TypeScript로 만들어줘

# Tab 키로 플랜 모드로 전환
[Plan Mode]

# 에이전트가 다음과 같은 계획을 제시
1. src/Counter.tsx 파일 생성
2. useState 훅 임포트
3. 카운터 로직 구현 (증가/감소 버튼)
4. TypeScript 타입 정의
5. 테스트 작성

# Enter로 실행
```

**해석:**
- `opmeoncode` 명령: OpenCode 에이전트 시작
- 자연어로 작업 요청: "React useState를 사용하는 카운터 컴포넌트를 TypeScript로 만들어줘"
- 플랜 모드 전환: Tab 키로 즉시 실행 대신 계획 먼저 검토
- 단계별 계획: 에이전트가 파일 생성 → 라이브러리 임포트 → 로직 구현 → 타입 정의 → 테스트 작성 순서로 계획

### 예시 2: OpenCode 프로바이더 설정 시나리오

```bash
# 현재 설정된 모델 확인
opencode
> /models

# 출력 결과 (프로바이더 미연결 상태)
No providers connected

# Anthropic 프로바이더 연결
> /connect
Select provider:
1. OpenCode Genie
2. Anthropic
3. OpenAI
4. Google
5. GitHub Copilot

# 옵션 2 선택 (Anthropic)
> 2

Choose connection method:
1. Claude Pro/Max (OAuth)
2. API Key

# 옵션 2 선택 (API 키 방식 권장)
> 2

Enter your Anthropic API key:
> sk-ant-xxxxxxxxxxxxx

# 연결 성공
AnthropicProvider connected successfully!

# 다시 모델 확인
> /models

# 출력 결과 (Anthropic 연결 후)
Available Models:
- claude-opus-4
- claude-sonnet-4
- claude-haiku-4
```

**해석:**
- `Claude Pro/Max(OAuth)` 방식: Claude 구독 계정을 직접 연결하는 방식 (약관 위반 위험)
  - ⚠️ 실제로 이 방식으로 연결한 개발자들의 Claude 계정이 정지된 사례 다수
- `API Key` 방식: Anthropic API 대시보드에서 발급받은 키 사용 (권장)
  - ✅ 안전한 방식
  - ✅ 종량제로 비용 관리 가능

### 예시 3: Oh-My-OpenCode 플러그인 활용 시나리오

```bash
# Oh-My-OpenCode 설치
git clone https://github.com/code-yeongyu/oh-my-opencode.git
cd oh-my-opencode
./install.sh

# 설치 후 OpenCode 재시작
opencode

# 일반적인 작업 명령
> 로그인 폼을 React로 만들어줘

# Oh-My-OpenCode가 자동으로 모델 선택
[Auto-selecting model for frontend task...]
[Selected: gpt-4o with vision] ← 시각 능력 필요한 UI 작업용

# 다른 작업 명령
> 프로젝트 구조 문서를 마크다운으로 작성해줘

# Oh-My-OpenCode가 자동으로 모델 선택
[Auto-selecting model for documentation task...]
[Selected: claude-opus-4] ← 글쓰기 능력 우수

# 또 다른 작업 명령
> 간단한 util 함수를 JavaScript로 만들어줘

# Oh-My-OpenCode가 자동으로 모델 선택
[Auto-selecting model for quick prototyping...]
[Selected: gpt-4-turbo] ← 빠른 실행 속도
```

**해석:**
- Oh-My-OpenCode는 사용자가 모델을 지정하지 않아도 작업 유형을 인식해 최적 모델 선택
- 프론트엔드(UI) 작업 → 시각 능력 우수한 모델 (GPT-4o with vision)
- 문서 작성 → 글쓰기 능력 우수한 모델 (Claude Opus)
- 간단한 작업 → 빠른 속도의 모델 (GPT-4-turbo)
- 결과: 개발 효율 향상 + 토큰 비용 최적화

## 함정·실수

### 1. Claude 구독 계정을 직접 연결하려는 시도

**문제:**
```bash
/connect
# Anthropic 선택 후 Claude Pro/Max(OAuth) 방식으로 구독 계정 직접 연결
```

**위험성:**
- Anthropic 이용약관 위반 (Claude 구독은 공식 Claude Code에서만 사용 가능)
- 실제로 이렇게 연결한 개발자들의 Claude 계정이 정지됨
- 약간의 편의를 위해 전체 구독 계정을 잃을 수 있음

**올바른 방법:**
```bash
# 방법 1: Anthropic API 키 사용 (권장)
/connect → Anthropic → API Key → sk-ant-xxxxxxx

# 방법 2: OpenCode Genie 프로바이더 사용
/connect → OpenCode Genie → Genie API 키
```

### 2. 프로바이더 연결 없이 모델 사용 시도

**문제:**
```bash
opencode
> React 컴포넌트 만들어줘

# 오류: No provider connected
```

**원인:**
- `/connect` 명령으로 최소한 하나의 프로바이더를 먼저 설정하지 않음

**해결책:**
```bash
> /connect
# 원하는 프로바이더 선택 및 API 키 설정
> /models  # 설정된 모델 확인
> React 컴포넌트 만들어줘  # 이제 작동
```

### 3. 빌드 모드에서 대규모 작업 시도

**문제:**
- 빌드 모드에서 계획 없이 복잡한 프로젝트 생성 요청
- 에이전트가 예상과 다른 방향으로 진행
- 중간에 수정하려 해도 이미 많은 코드가 생성됨

**해결책:**
```bash
# Tab으로 플랜 모드로 전환
Tab  # 플랜 모드 활성화

# 복잡한 작업은 플랜 모드에서
> 마이크로서비스 아키텍처 프로젝트 설정해줘

# 계획을 검토하고 수정한 후 실행
```

### 4. Oh-My-OpenCode 플러그인 과신

**문제:**
- 플러그인이 완벽하게 모든 작업에 최적 모델을 선택한다고 기대
- 특수한 작업의 경우 자동 선택이 부정확할 수 있음

**예시:**
```bash
# 자동 선택
> 딥러닝 모델 최적화 코드 작성
# Oh-My-OpenCode가 일반적인 코딩 작업으로만 인식
# 적절한 선택: Claude Opus (수학/알고리즘 강점)
# 잘못된 선택: GPT-4 (속도 최적화)

# 해결: 명시적 지정
> Claude Opus 사용, 딥러닝 모델 최적화 코드 작성
```

### 5. LSP 기능 미활용

**문제:**
- OpenCode의 LSP 지원 기능을 모르고 문법 오류를 수동으로 수정
- 타입 검사나 자동완성을 활용하지 않음

**활용 방법:**
```bash
# OpenCode가 자동으로 LSP 지원
# → 타입 오류 자동 감지
# → 함수/변수 정의 위치 자동 추적
# → 문법 오류 빠른 캐치
# → IDE와 유사한 경험 (터미널에서)
```

### 6. 세션 공유(Share Link) 기능 보안 간과

**문제:**
```bash
> /share
# 생성된 URL: https://share.opencode.ai/s/xxxxx
# 회사 내부 프로젝트나 민감한 코드 공유
```

**위험성:**
- Share Link는 공개 가능성이 있음
- 민감한 API 키, 비즈니스 로직이 노출될 수 있음

**안전한 사용:**
```bash
# 방법 1: 신뢰하는 팀원하고만 공유
> /share → URL 생성 → 신뢰 가능한 채널로만 전달 (이메일, 메시지, 직접 말)

# 방법 2: 세션 종료 후 공유
> /new  # 새 세션 시작 (기존 공유 링크 무효화)
```

## 베스트 프랙티스

### 1. 올바른 프로바이더 선택 전략

**상황별 권장 설정:**

```
초급 개발자
└─ OpenCode Genie 프로바이더 단일 사용
   └─ 여러 모델을 자동으로 활용
   └─ API 키 관리 복잡도 낮음

중급 개발자
└─ 주 모델: Anthropic API (Claude Opus/Sonnet)
└─ 보조 모델: OpenAI API (GPT-4o) 
└─ 프론트엔드 작업: Google Gemini
   └─ 각 프로바이더별 장점 활용

고급 개발자
└─ 모든 주요 프로바이더 연결
   ├─ Anthropic (Claude)
   ├─ OpenAI (GPT)
   ├─ Google (Gemini)
   └─ 로컬 모델 (Ollama, llama.cpp)
└─ Oh-My-OpenCode 플러그인으로 오케스트레이션
   └─ 작업별 최적 모델 자동 선택
```

**기본 추천:**
```bash
# API 키 안전성과 비용 효율성 균형
# 1단계: OpenCode Genie 프로바이더 연결
/connect → OpenCode Genie → API 키 입력

# 2단계: 필요시 Anthropic API 추가 연결
/connect → Anthropic → API Key 방식 → sk-ant-xxx

# 결과: 기본은 OpenCode Genie (다양한 모델), 필요시 Claude API 직접 사용
```

### 2. 플랜 모드 vs 빌드 모드 선택 기준

```
플랜 모드 사용 시기
├─ 새로운 프로젝트 시작
├─ 복잡한 아키텍처 결정 필요
├─ 팀 협업이 필요한 경우
├─ 대규모 리팩토링
└─ 중요한 기능 구현
   → 미리 계획을 검토하고 수정 가능

빌드 모드 사용 시기
├─ 간단한 버그 수정
├─ 함수/유틸리티 추가
├─ 테스트 코드 작성
├─ 문서 작성
└─ 빠른 프로토타이핑
   → 즉시 실행으로 빠른 피드백
```

**구체적 예시:**
```bash
# 예1: 새 기능 추가 (플랜 모드)
Tab  # 플랜 모드
> 사용자 인증 기능을 JWT 기반으로 추가해줘
# → DB 스키마 변경, API 엔드포인트, 미들웨어 등 계획 수립
# → 검토 후 실행

# 예2: 간단한 수정 (빌드 모드)
> 로그인 버튼의 색상을 파란색으로 변경해줘
# → 즉시 실행
```

### 3. 효율적인 모델 조합 활용

```
프론트엔드 작업
├─ UI 설계/레이아웃: GPT-4o with Vision (시각 능력)
├─ React 컴포넌트: Claude (코드 품질)
└─ 스타일링: GPT-4-turbo (빠른 실행)

バックエンド 작업
├─ 데이터베이스 설계: Claude Opus (복잡한 설계)
├─ API 개발: Claude Sonnet (균형잡힌 성능)
└─ 간단한 CRUD: GPT-4-turbo (속도)

문서화
├─ 상세 가이드: Claude Opus (글쓰기)
├─ API 문서: Claude Sonnet (명확한 구조)
└─ README: GPT-4o (빠른 생성)
```

**구현 방법:**
```bash
# Oh-My-OpenCode를 사용한 자동 최적화
# (플러그인이 자동으로 위 규칙 적용)

# 또는 수동으로 모델 지정
> --model claude-opus React 대시보드 UI 설계 문서를 상세하게 작성해줘
```

### 4. 세션 관리 전략

```bash
# 오래된 세션 확인
/session

# 새 프로젝트마다 새 세션 시작
/new
# → 컨텍스트 초기화
# → 이전 프로젝트와 독립적으로 동작

# 중단된 작업 재개
/session → 원하는 세션 선택
# → 이전 컨텍스트에서 계속 작업

# 팀원과 협업
/share → URL 생성
# → 신뢰하는 채널로만 공유
```

### 5. 로컬 모델 통합 (고급)

```bash
# Ollama를 통한 로컬 모델 실행 (GPU 필요)
# 1단계: Ollama 설치 (https://ollama.ai)

# 2단계: 로컬 모델 다운로드
ollama pull mistral  # 또는 llama2, neural-chat 등

# 3단계: OpenCode에서 설정
/connect → Custom LLM → localhost:11434

# 4단계: 사용
/models  # mistral 모델이 나열됨

# 장점: API 비용 0 (로컬 실행), 개인 정보 보호
# 단점: GPU 리소스 필요, 모델 성능이 클라우드보다 낮을 수 있음
```

### 6. 비용 최적화 팁

```
토큰 비용 구조
├─ Claude Opus: 가장 비쌈, 가장 똑똑함
├─ Claude Sonnet: 중간 가격, 균형잡힌 성능
├─ GPT-4o: Claude와 유사 가격, 시각 능력 우수
├─ GPT-4-turbo: 중간 가격, 빠른 속도
└─ 오픈소스 모델: 무료 (로컬 실행)

최적화 전략
1. 복잡한 작업: Claude Opus (한 번에 맞춤)
   → 여러 번 수정하는 것보다 초기에 비용 투자

2. 반복적 작업: Claude Sonnet (자주 사용해도 저렴)
   → 안정적이고 경제적

3. 빠른 프로토타이핑: GPT-4-turbo (빠름)
   → 초기 아이디어 검증

4. 간단한 작업: 오픈소스 모델 (로컬)
   → 비용 0, 속도는 약간 느림
```

**실제 운영 예시:**
```bash
# 비용 절감 세팅
/connect → OpenCode Genie
# → Genie가 자동으로 작업 복잡도에 맞는 모델 선택
# → 불필요한 고가 모델 사용 방지

# 또는
Oh-My-OpenCode 설치
# → 자동 모델 오케스트레이션
# → 월 토큰 비용 20~30% 절감 가능
```

## 참고

### 공식 리소스
- **OpenCode 공식 웹사이트**: https://opencode.ai/
- **Oh-My-OpenCode GitHub**: https://github.com/code-yeongyu/oh-my-opencode
- **OpenCode Genie**: https://genie.opencode.ai/

### 관련 정보
- **뉴스**: https://news.hada.io/topic?id=24978 (OpenCode 관련 커뮤니티 논의)

### 개발 커뮤니티
- OpenCode GitHub Discussions: 기능 요청, 버그 리포트
- Oh-My-OpenCode GitHub Issues: 플러그인 관련 이슈

### 추가 학습
**Claude Code와의 비교:**
- Claude Code 공식 문서: https://claude.ai/code
- Claude Code는 Anthropic의 공식 제품, OpenCode는 커뮤니티 프로젝트
- 기능상 거의 동일하나, OpenCode가 더 많은 모델 지원

**LLM 모델 성능 비교:**
- 각 모델의 장단점: 영상 내에서 언급
- 프론트엔드 작업: Gemini 시각 능력 우수
- 문서 작성: Claude 글쓰기 능력 우수
- 속도: GPT-4-turbo 가장 빠름

**관련 용어:**
- LSP (Language Server Protocol): https://microsoft.github.io/language-server-protocol/
- MCP (Model Context Protocol): 외부 도구 연동 표준
- 프로바이더: Claude/GPT/Gemini 등 LLM 서비스 제공사
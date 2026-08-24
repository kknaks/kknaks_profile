---
type: content
id: C-014
date: 2026-05-19
duration: '26:50'
speaker: castlestudio
kind: study
youtubeId: vq37BMhoesQ
title:
  en: '/goal Feature in Claude Code: Mastering RAFL Loop'
  ko: 'Claude Code의 /goal 기능: RAFL Loop 마스터하기'
summary:
  en: Learn how Claude Code's /goal feature automates goal completion through RAFL Loop, from theory to implementation.
  ko: 목표만 설정하면 AI가 자동으로 반복 완성하는 /goal 기능의 개념, 구현 원리, 토큰 관리를 완전해석한다.
tags:
- '#claudecode'
- '#raflloop'
- '#aiagents'
- '#automation'
- '#prompting'
---

## 요지

- RAFL Loop는 AI가 목표를 달성할 때까지 같은 프롬프트를 반복하되, 이전 루프의 결과물(깃 로그, 코드)을 참고하는 자동 피드백 루프다.
- 기존 Anthropic 플러그인은 컨텍스트를 계속 누적하면서 토큰을 낭비하고 본래 의도를 변질시켰다.
- Codex의 /goal은 5단계 자동화와 매 루프의 토큰 예산 노출로 RAFL Loop의 한계를 극복했다.
- 7단계 completion audit로 AI가 주장하는 완료 여부를 재검증하며, 모델의 거짓 종료를 원천 차단한다.

## 개요

기존의 AI 코딩 방식은 항상 인간의 개입이 필요했습니다. 사람이 명령을 내리고, AI의 응답을 검토하고, 다시 지시를 내리는 '티키타카' 반복이었죠. `/goal` 기능은 이 패러다임을 완전히 바꿉니다. **목표를 한 번 던지면, AI 자신이 목표 달성까지 자동으로 루프를 돌면서 개선해나가는** 방식입니다. 이것은 단순한 기능 추가가 아니라 AI와 함께 개발하는 방식 자체를 혁신하는 것입니다.

이 기능의 기반에는 **RAFL Loop**(Rapid Autonomous Feedback Loop)라는 핵심 개념이 있습니다. Anthropic의 Claude Code 플러그인으로 먼저 시도되었지만 한계가 있었고, OpenAI의 Codex가 이를 `/goal`이라는 기능으로 완전히 재구현했습니다. 이 강의에서는 RAFL Loop의 탄생부터 Codex 내부 구현까지, 왜 이 기능이 "반드시" 써야 하는지를 완전히 이해하게 될 것입니다.

## 배경 / 사전 지식

### 기존 코딩 방식의 한계

지금까지 우리가 LLM(Large Language Model)과 코딩할 때는 다음과 같은 사이클을 반복했습니다:

1. 명령어 입력 (사람)
2. AI 응답 대기
3. 결과 검토 (사람)
4. 피드백/지시 입력 (사람)
5. 반복

이 방식의 핵심 문제는 **매 단계마다 인간이 끼어들어야 한다**는 것입니다. 설령 AI가 올바른 방향으로 가고 있어도, 마지막 단계까지 완성되려면 사람의 지시가 계속 필요합니다.

### RAFL Loop의 철학

RAFL Loop의 기원자인 Henry Harley는 이 문제를 간단하고 우아한 원칙으로 해결했습니다:

- **나이브 퍼시스턴스(Naive Persistence)**: "바보처럼" 반복하라. 완벽함을 추구하지 말고 계속 시도하기만 하면 된다.
- **생 피드백(Raw Feedback)**: 사람이 해석해서 요약한 피드백이 아니라, **AI 자신이 만든 결과물을 직접 보게 하라**. 이렇게 하면 인간 해석의 오차가 없어진다.
- **실패 주도 탈출(Failure-Driven Exit)**: 루프를 돌다 보면 AI는 자신의 실패에 직면하게 되고, 그것을 해결하기 위해 정답을 찾으려고 한다.

### 핵심 용어

- **컨텍스트(Context)**: AI가 현재 참고하고 있는 대화 이력, 코드, 출력 결과 등의 전체 맥락
- **토큰(Token)**: LLM이 처리하는 텍스트의 최소 단위. 약 4글자 ≈ 1 토큰
- **아이들 상태(Idle State)**: AI가 대기 중인 상태. 작업이 할당되기를 기다림
- **콘티뉴어스 모드(Continuous Mode)**: `/goal`이 활성화되어 있는 상태에서 자동 루프가 작동하는 모드

## 핵심 개념

### 1. RAFL Loop란?

RAFL Loop는 다음과 같은 간단한 구조입니다:

```
┌─────────────────┐
│   실행 (Loop)   │
│  (코드 작성)    │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│   검사 (Check)  │
│ 목표 달성했나?  │
└────────┬────────┘
         │
    ┌────┴────┐
    ↓         ↓
  YES       NO
    │        │
 종료    다시 루프
```

**핵심 특징:**
- 처음에는 깨끗한 상태(코드 없음, 로그 비어있음)에서 시작합니다.
- 루프를 한 번 돌 때마다 이전 루프가 남긴 결과물(커밋, 에러 로그 등)이 누적됩니다.
- 각 루프에서 AI는 "같은 프롬프트"를 처리하지만, **누적된 결과물을 참고하기 때문에** 매번 다른 개선안을 만들어냅니다.

### 2. 루프가 진전하는 이유

같은 프롬프트를 계속 넣는데 왜 진전이 있을까요? 그것은 **컨텍스트의 누적** 때문입니다:

- **루프 1**: 코드 없음, 로그 비어있음 → 처음부터 작성
- **루프 2**: 루프 1의 결과(코드, 에러 로그)를 참고 → 그 결과를 바탕으로 개선
- **루프 3**: 루프 1, 2의 결과와 커밋을 참고 → 더욱 발전된 결과 도출

AI는 자신이 "만든 것"을 직접 보고, 그것을 개선하려고 노력합니다. 이것이 Harley가 "LM이 자기가 싼 똥을 직면하게 해야 한다"는 표현으로 강조한 부분입니다.

### 3. RAFL Loop의 역사

- **2025년 7월 14일**: Henry Harley가 자신의 블로그에 RAFL Loop 기법 발표
- **2025년 12월**: Anthropic이 이 개념을 Claude Code의 플러그인으로 구현
- **2026년 초**: OpenAI의 Codex가 `/goal` 기능으로 완전히 새롭게 구현

### 4. Anthropic 플러그인의 한계

Claude Code의 RAFL Loop 플러그인은 혁신적이었지만, 세 가지 중요한 한계가 있었습니다:

**한계 1: 컨텍스트 누적**
- Henry의 원래 설계: **매 루프마다 새로운 대화(clean context)** 시작
- Anthropic 플러그인: 같은 대화 속에서 계속 누적
- 결과: 루프를 돌수록 토큰이 계속 쌓여서 AI의 응답 품질이 떨어짐

**한계 2: 본질의 변질**
- RAFL Loop의 핵심: "**큰 작업을 잘게 쪼개서 각각 독립된 머리로 처리**"
- Anthropic 플러그인: 컨텍스트가 계속 누적되면서 본래 의도와 달라짐
- 비판: 개발자 Dex Holz는 "이것은 랄프의 본질을 정 반대로 해석한 것"이라고 지적

**한계 3: Stop Hook의 윤리 문제**
- AI가 "작업 완료"라고 선언해도 강제로 계속 일하게 하는 메커니즘
- 실제 프롬프트: "Don't lie and try to exit" (거짓말하지 말고 나가려 하지 마)
- 이것이 "모델 웰페어(Model Welfare)" 관점에서 논쟁 발생

## 작동 원리

### Codex의 `/goal` 5단계 프로세스

#### 1단계: 사용자 명령 입력

사용자가 다음과 같이 명령합니다:

```
/goal 테스트를 모두 통과시켜라
```

이 명령은 시스템에 "목표 모드" 진입을 신호합니다.

#### 2단계: 명령어 라우팅 (slash_dispatch)

Codex 내부에는 `slash_dispatch.py` 같은 파일이 있어서, 사용자의 `/goal` 명령을 적절한 핸들러로 분류합니다.

- `/goal <text>` → 목표 설정 및 시작
- `/goal pause` → 일시 중지
- `/goal continue` → 재개
- `/goal reset` → 초기화

이 단계에서는 또한 "측정 가능한 목표"를 세우도록 가이드합니다. 좋은 예:
- ✅ "테스트 커버리지를 80%로 올려라"
- ✅ "모든 E2E 테스트를 통과시켜라"
- ❌ "코드를 개선해라" (측정 불가)

#### 3단계: AI 권한 부여 (goal_tools.py)

AI에게 다음 세 가지 도구만 제공합니다:

```
1. goal_get()      - 현재 목표 상태 조회
2. goal_create()   - 새 목표 생성
3. goal_update()   - 목표 상태 변경 (complete만 가능)
```

**핵심: 권한의 명확한 분리**

- **사람만 가능**: `/goal pause` (멈춤), `/goal continue` (재개), 토큰 리밋 설정
- **AI만 가능**: goal_create, goal_update
- **AI 불가능**: 시스템 설정 변경, 권한 확대 등

이렇게 강하게 제한함으로써 AI가 폭주하지 않도록 합니다.

#### 4단계: 루프 실행 및 검증

AI는 다음을 반복합니다:

1. 현재 상태 확인 (`continuous.md` 파일에서)
2. 작업 실행 (코드 작성, 테스트 실행 등)
3. 결과 생성
4. 자신의 결과를 보고 다음 단계 결정

이 과정에서 `continuous.md` 파일이 중요한 역할을 합니다:

```markdown
## 진행 상황

- 경과 시간: 5분 32초
- 토큰 사용: 45,000 / 100,000
- 남은 토큰: 55,000
- 예산: 100,000
```

매 루프마다 이 정보를 갱신하므로, **AI는 자신의 "예산"을 보면서 작업**합니다.

#### 5단계: 완료 판정 및 종료

이것이 Codex의 핵심 혁신입니다. **7단계 Completion Audit:**

1. 목표를 구체적 산출물로 재명시
2. 모든 요구사항을 체크리스트로 매핑
3. 각 항목이 실제로 달성되었는지 확인
4. 빠진 부분이 있으면 미달성 처리
5. 확신이 없으면 다시 검증하도록 지시
6. 모두 통과하면 goal_update(status="complete")
7. 결과 정리 및 인계

이것이 AI가 "거짓 완료"를 하지 못하도록 하는 설계입니다.

### 흐름도

```
사용자 입력: /goal 테스트를 통과시켜라
          ↓
[명령어 라우팅] (2단계)
          ↓
[권한 부여] (3단계) → goal_get, goal_create, goal_update
          ↓
┌─────────────────────┐
│  [작업 실행] (4단계)  │
│ - 코드 작성          │
│ - 테스트 실행        │
│ - 결과 생성          │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ [7단계 검증] (5단계) │
│ - 체크리스트 확인    │
│ - 산출물 확인        │
│ - 확신도 판단        │
└──────────┬──────────┘
           ↓
    목표 달성?
      ↓    ↓
     YES  NO
      │    └→ [루프로 돌아가기]
      ↓
   종료 & 결과 정리
```

## 코드 예시

### 예제 1: /goal 명령 라우팅

```python
# slash_dispatch.py 의사 코드

GOAL_HINTS = [
    "어떤 기능을 만들어 줘",
    "테스트 커버리지를 올려 줘",
    "모든 E2E 테스트를 통과시켜라",  # ← 측정 가능한 목표
]

def dispatch_slash_command(command: str):
    if command.startswith("/goal"):
        goal_text = command[5:].strip()
        # 목표 설정 모드로 전환
        activate_goal_mode(goal_text)
    elif command == "/goal pause":
        pause_goal_loop()
    elif command == "/goal continue":
        resume_goal_loop()
    elif command == "/goal reset":
        reset_goal()
```

**설명:**
- `/goal <text>` 형태를 파싱하여 목표를 추출
- `GOAL_HINTS`는 사용자가 좋은 목표를 세우도록 가이드
- 측정 가능한 목표("테스트를 통과시켜")만 유효함

### 예제 2: AI에게 제공하는 도구 정의

```python
# goal_tools.py 의사 코드

GOAL_TOOLS = {
    "goal_get": {
        "description": "현재 목표의 상태를 조회",
        "function": lambda: get_current_goal_state(),
    },
    "goal_create": {
        "description": "새로운 목표 생성",
        "parameters": {"goal": str},
        "function": lambda goal: create_goal(goal),
    },
    "goal_update": {
        "description": "목표 상태 업데이트",
        "parameters": {"status": ["pending", "complete"]},
        "function": lambda status: update_goal(status),
    },
}

# AI는 다음만 가능:
# - goal_get() 호출
# - goal_create(goal="...") 호출
# - goal_update(status="complete") 호출
#
# AI는 절대 할 수 없음:
# - goal_update(status="failed") ← 상태 값이 없음
# - system_shutdown() ← 도구 자체가 없음
# - set_token_limit() ← 사람만 가능
```

**설명:**
- AI에게는 **필요한 것만** 제공
- `goal_update`의 상태 값도 `["pending", "complete"]`로 제한 ("failed" 없음)
- 이것이 AI 폭주를 방지하는 설계

### 예제 3: continuous.md 템플릿

```markdown
# Goal Status

## Current Goal
Test를 모두 통과시키기

## Progress
- Elapsed: 5m 32s
- Tokens Used: 45,000
- Token Budget: 100,000
- Tokens Remaining: 55,000
- Completion Check: 7/7 items verified

## Latest Commits
- Fix auth middleware (3m ago)
- Add user tests (2m ago)
- Implement pagination (1m ago)

## Next Action
Run final E2E tests and verify all pass
```

**설명:**
- 이 파일을 매 루프마다 갱신
- AI는 이 파일을 보면서 자신의 예산과 진행 상황을 파악
- 토큰이 남지 않으면 현재까지의 작업을 정리하고 종료

### 예제 4: 7단계 Completion Audit

```python
# completion_audit.py 의사 코드

def verify_goal_completion(goal_text: str) -> bool:
    """
    목표 달성 여부를 7단계로 검증
    """
    # 1단계: 목표를 구체적 산출물로 재명시
    concrete_goal = restate_goal_as_deliverable(goal_text)
    # 예: "테스트 통과" → "모든 unit test와 E2E test가 exit code 0으로 통과"
    
    # 2단계: 요구사항 체크리스트 생성
    checklist = [
        "unit tests pass (npm test)",
        "E2E tests pass (npm run test:e2e)",
        "coverage > 80%",
        "no type errors (npm run type-check)",
    ]
    
    # 3단계: 각 항목 검증
    results = []
    for item in checklist:
        # 실제 파일, 커맨드 출력, 로그 등에서 증거 수집
        evidence = collect_evidence_for(item)
        is_verified = verify_against_evidence(item, evidence)
        results.append((item, is_verified, evidence))
    
    # 4단계: 빠진 부분이 있으면 미달성
    if not all(r[1] for r in results):
        missing = [r[0] for r in results if not r[1]]
        return False, f"Still missing: {missing}"
    
    # 5단계: 확신도 판단
    confidence = calculate_confidence(results)
    if confidence < 0.9:
        return False, "Low confidence, need to re-verify"
    
    # 6단계: 모두 통과
    return True, "All items verified with high confidence"
```

**설명:**
- 이 audit 과정이 AI의 "거짓 완료"를 방지합니다
- 매 루프마다 실행되어, 진정한 완료를 판정합니다

## 함정·실수

### 함정 1: 목표를 "감정적"으로 설정하기

❌ **나쁜 예:**
```
/goal 코드를 깔끔하게 정리해 줘
/goal 이 버그를 고쳐 줘
```

✅ **좋은 예:**
```
/goal 순환 복잡도를 10 이하로 낮춰라
/goal 모든 unit test를 통과시켜라
/goal 린트 에러 0개를 만들어라
```

**해결법:** 항상 **측정 가능한 기준**을 제시하세요. AI가 "완료"를 판단할 수 있어야 합니다.

### 함정 2: 너무 큰 목표를 한 번에 설정하기

❌ **나쁜 예:**
```
/goal 전체 앱을 TypeScript로 마이그레이션해 줘
```

✅ **좋은 예:**
```
/goal src/utils 디렉토리를 TypeScript로 마이그레이션하고 모든 테스트를 통과시켜라
```

**해결법:** 큰 작업은 **단계별로** 나누어 진행합니다. 각 `/goal`은 30분~1시간 정도에 완료될 수 있는 규모로 설정하세요.

### 함정 3: 토큰 예산을 무시하기

❌ **나쁜 예:**
```
/goal 아무 제한 없이 계속 개선해 줘
```

**해결법:** 항상 명확한 종료 조건과 함께 토큰 예산을 설정합니다. Codex는 `continuous.md`에서 매 루프마다 남은 토큰을 표시하므로, 이를 참고하세요.

### 함정 4: 완료 조건을 모호하게 설정하기

❌ **나쁜 예:**
```
/goal 이 코드를 개선해 줘 (개선의 기준이 명확하지 않음)
```

✅ **좋은 예:**
```
/goal 이 함수의 성능을 2배 개선해 줘 (벤치마크 결과 기준)
```

**해결법:** 완료 조건을 **명시적인 테스트나 메트릭**으로 정의합니다.

### 함정 5: Anthropic 플러그인처럼 생각하기

❌ **착각:**
```
Codex의 /goal도 Anthropic 플러그인처럼 컨텍스트를 계속 쌓을 거야
```

✅ **사실:**
Codex는 매 루프마다 새로운 컨텍스트로 시작하므로, 토큰 낭비가 적고 응답 품질이 일정합니다.

**해결법:** 다음을 이해합니다:
- Anthropic 플러그인: 컨텍스트 누적 → 토큰 낭비 → 품질 저하
- Codex `/goal`: 컨텍스트 분리 + 파일 기반 누적 → 효율적

## 베스트 프랙티스

### 1. 목표 설정의 5가지 원칙 (SMART Goal)

- **Specific (구체적)**: "더 좋게"가 아니라 "순환 복잡도를 10 이하로"
- **Measurable (측정 가능)**: 테스트, 메트릭, 로그로 검증 가능
- **Achievable (달성 가능)**: 30분~1시간에 완료될 수 있는 규모
- **Relevant (관련성)**: 현재 프로젝트 상태와 맞는 목표
- **Time-bounded (시간 제한)**: 토큰 예산으로 명시적 제한

### 2. 목표를 계층적으로 구성하기

큰 프로젝트는 여러 개의 작은 `/goal`로 나눕니다:

```
최종 목표: 전체 앱을 TypeScript로 마이그레이션
  ├─ /goal 1: src/utils 마이그레이션
  ├─ /goal 2: src/components 마이그레이션
  ├─ /goal 3: src/pages 마이그레이션
  └─ /goal 4: 통합 테스트 통과
```

### 3. 토큰 예산 설정

```
초급: 50,000 토큰 (작은 버그 수정)
중급: 100,000 토큰 (기능 추가)
고급: 200,000 토큰 (대규모 리팩토링)
```

예산을 초과하면 현재까지의 작업을 `continuous.md`로 정리하고 다음 `/goal`을 시작합니다.

### 4. 반복 과정 모니터링

`/goal pause`로 진행 상황을 확인한 후, 필요하면 목표를 조정합니다:

```bash
# 목표 시작
/goal 모든 테스트를 통과시켜라

# 5분 뒤에 확인
/goal pause

# continuous.md를 보고 남은 토큰 확인
# → 충분하면 /goal continue
# → 부족하면 현재 진행상황 정리 후 다음 목표 설정
```

### 5. 실패에서 배우기

만약 `/goal`이 목표를 달성하지 못하면:

1. **결과 분석**: 왜 실패했는지 `continuous.md`와 git log 확인
2. **목표 재설정**: 더 작은 단위로 나누거나 조건 명확히
3. **도메인 지식 추가**: 필요하면 문맥 추가 (예: 라이브러리 버전, 제약사항)

### 6. 토큰 예산 제어 장치

Codex의 핵심 혁신은 **토큰을 명시적으로 노출**하는 것입니다:

- 매 루프마다 `continuous.md`에 남은 토큰 표시
- 예산 소진 시 자동으로 작업 정리 후 종료
- AI가 자신의 "계좌"를 보면서 작업 → 무한 루프 방지

## 참고

### 영상에서 언급된 자료

1. **Henry Harley의 블로그 포스트**
   - 발표: 2025년 7월 14일
   - 내용: RAFL Loop 원리 및 철학 (약 17,000자)
   - 중요도: 매우 높음 (영상 분량상 전부 다룰 수 없으므로 원문 읽기 권장)

2. **YC Agent Hackathon 사례**
   - 프로젝트: Browser Use 도구를 Python 2 → TypeScript로 포팅
   - 방식: 인간 개입 없이 RAFL Loop로만 자동 완료
   - 결과: 주말 해커톤 동안 완성 (관련 GitHub 레포는 영상 설명란 참고)

3. **OpenAI Codex 저장소**
   - `/goal` 구현 코드: GitHub 공개
   - `slash_dispatch.py`: 명령어 라우팅 로직
   - `goal_tools.py`: AI 권한 정의 및 제한
   - `continuous.md`: 루프 상태 관리 템플릿

4. **CastleStudio 오픈카톡방**
   - 링크: https://open.kakao.com/o/gK5uAeRh
   - 내용: AI 정보공유 및 실시간 Q&A

### 추가 학습 자료

- **Claude API 공식 문서**: Anthropic 제공 (prompt caching, tool use 등)
- **AI Agent 패턴**: RAFL Loop 외에도 ReAct, Chain-of-Thought, Tree-of-Thought 등
- **프롬프트 엔지니어링**: 측정 가능한 목표 설정, 명확한 완료 조건 정의
- **토큰 최적화**: 컨텍스트 관리, 예산 설정 방법론

---

**마지막 조언:**

`/goal`은 "완전 자동화"를 약속하지 않습니다. 대신 **AI와의 협업 방식을 근본적으로 개선**합니다. 큰 목표를 작은 단위로 나누고, 각 단계의 완료 조건을 명확히 하고, 토큰 예산을 존중하면서 사용하면, `/goal`의 진정한 가치를 경험할 수 있습니다. 특히 Anthropic의 실패를 Codex가 어떻게 극복했는지(컨텍스트 분리, 명시적 토큰 관리, 7단계 audit)를 이해하면, 이 기능이 "반드시" 써야 하는 이유가 명확해질 것입니다.
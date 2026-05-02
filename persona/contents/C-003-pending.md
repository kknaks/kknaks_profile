---
concept:
- 프롬프트 엔지니어링은 AI와 효과적으로 소통하기 위해 명확한 지시와 상세한 정보를 제공하는 기초 기술이다.
- 컨텍스트 엔지니어링은 AI가 업무 맥락을 이해하도록 회사 히스토리, 규칙, 환경 정보를 체계적으로 제공하는 것이다.
- 하네스 엔지니어링은 단순한 지침이 아닌 린트, CI/CD 같은 기술적 제어로 AI의 실수를 사전에 방지하고 자기 수정을 가능하게 한다.
- 가시성 확보(로깅, 스크린샷)는 AI가 자신의 행동 결과를 스스로 볼 수 있게 해서 인간 개입 없이 자동 수정을 가능하게 한다.
- 점진적 컨텍스트 공개는 한 문서에서 모든 정보를 주지 말고 AI가 필요에 따라 검색할 수 있는 목차 구조로 설계하는 방식이다.
- 워크트리와 CI/CD 강제를 통해 AI가 규칙을 어길 수 없게 기술적으로 만듦으로써 인간의 반복적인 검증 과정을 제거한다.
date: 2026-05-03
day: Day 03
duration: '25:07'
enriched_at: '2026-05-03T02:27:32+09:00'
id: C-003
kind: study
speaker: 코딩알려주는누나
status: published
summary:
  en: Learn harness engineering principles that enable AI to work autonomously with
    automated control, beyond prompt and context engineering, with OpenAI case study.
  ko: 프롬프트·컨텍스트 엔지니어링을 넘어 AI의 자동화를 완성하는 하네스 엔지니어링의 원리와 OpenAI 사례, 실제 구현 방법을 배운다.
tags:
- '#ai-engineering'
- '#harness-engineering'
- '#prompt-engineering'
- '#context-engineering'
- '#claude'
- '#automation'
title:
  en: 'Harness Engineering: Controlling AI Within Boundaries'
  ko: '하네스 엔지니어링: AI를 경계 내에서 제어하는 기술'
transcript: true
type: content
youtubeId: 3yyLg1xbQSs
---

## 개요

AI 기술의 발전으로 개발 속도는 비약적으로 증가했지만, 많은 개발자들은 여전히 "AI가 코드를 작성하면 이를 일일이 테스트하고 수정하는" 무한 반복에 빠져 있습니다. AI는 빠르지만 인간이 검증하는 속도가 느려서 전체 생산성이 병목되는 상황입니다. **하네스 엔지니어링**은 이 문제를 근본적으로 해결하는 방법론입니다. OpenAI 팀은 이 기술을 적용해 5개월간 개발자가 코드 한 줄도 직접 작성하지 않고도 완전한 서비스를 개발하고 배포했습니다. 핵심은 인간의 개입을 제거하고 AI가 스스로 계획, 구현, 테스트, 피드백을 반복하는 자동 루프를 구축하는 것입니다.

## 배경 / 사전 지식

### AI와 상호작용하는 방식의 진화

**프롬프트 엔지니어링**(Prompt Engineering)은 AI에게 "무엇을" 해야 하는지 명확하게 지시하는 방법론입니다. 상세한 설명, 요구사항 정의, 필요한 정보를 제공하여 AI의 이해도를 높입니다. "버튼을 만들어"라고 하면 AI가 못 알아듣지만, "파란색 배경에 흰 텍스트로 된 높이 40px, 너비 200px의 버튼을 만들어"라고 하면 훨씬 정확한 결과를 얻습니다.

**컨텍스트 엔지니어링**(Context Engineering)은 AI가 작업을 수행하기 전에 필요한 배경 정보를 체계적으로 제공하는 것입니다. 신입 사원이 회사의 6개월 히스토리를 알면 첫날 신입보다 훨씬 효율적인 것처럼, AI도 작업 맥락(회사의 기술 스택, 기존 코드 패턴, 아키텍처, 규칙)을 이해하면 더 나은 결과를 만듭니다.

### AI 개발의 현재 병목 지점

대부분의 개발자가 현재 겪고 있는 워크플로우:

1. **요청**: "이 기능을 구현해 줘"
2. **구현**: AI가 코드를 작성 완료
3. **테스트**: 개발자가 코드 검증 시작
4. **발견**: 버그나 요구사항 미충족 발견
5. **수정 요청**: "이거 다시 고쳐 줘"
6. **반복**: 2번으로 돌아감

이 무한 반복의 문제는 **AI의 작업 속도(매우 빠름) vs 인간의 검증 속도(느림) = 전체 생산성 저하**입니다. OpenAI 팀이 깨닫은 핵심 통찰은 "**인간이 AI의 생산성을 방해하고 있다**"는 것입니다. 따라서 인간의 개입을 최소화하고 AI가 스스로 검증하고 피드백하는 자동 루프를 만들어야 합니다.

### 하네스(Harness)의 의미

하네스는 강아지 산책할 때 사용하는 목걸이 모양의 안전장치입니다. 개를 완전히 자유롭게 놔두면 차에 치일 수 있으니, 경계를 정하고 그 안에서만 움직이게 하는 도구죠. 마찬가지로 AI도 "네가 원하는 대로 해도 된다"고 하면 의도와 다르게 만들기 때문에, 명확한 경계를 정하고 그 범위 내에서만 움직이도록 강제해야 합니다.

## 핵심 개념

### 1. 하네스 엔지니어링의 정의

하네스 엔지니어링은 단순히 "빨간색을 사용해야 한다" 또는 "이 파일을 건드리지 마"라는 **말로만 하는 지침이 아니라**, AI가 규칙을 어길 때 **자동으로 차단하고 피드백하는 기술적 메커니즘**을 구축하는 것입니다.

- ❌ **나쁜 예**: "console.log를 쓰지 마"
- ✅ **좋은 예**: ESLint로 console.log를 사용하면 빌드 자체가 실패하도록 설정

AI가 "아, 이건 규칙 위반이네"라고 스스로 판단하고 수정하게 만드는 것이 핵심입니다.

### 2. 3가지 핵심 요소

#### 가시성 (Visibility)

AI가 자신의 행동 결과를 **볼 수 있어야** 스스로 문제를 발견하고 수정할 수 있습니다.

**로깅**: 모든 작업 결과를 기록합니다. 개발자들은 보통 "불필요한 로그를 지워"라는 지적을 받지만, 하네스 엔지니어링에서는 오히려 로그를 충분히 남깁니다. 왜냐하면:
- AI가 결과를 볼 수 있어야 "아, 이게 내가 원하는 결과가 아니네"라고 판단할 수 있기 때문
- 테스트 통과/실패를 명확히 알아야 다음 단계를 결정할 수 있기 때문

**스크린샷/시각적 피드백**: UI 변경 사항을 캡처하여 AI가 의도한 결과와 실제 결과를 비교할 수 있게 합니다.

**테스트 결과**: 단순히 "통과" "실패"가 아니라, 어떤 테스트가 실패했는지, 왜 실패했는지 상세 정보를 제공합니다.

#### 컨텍스트 관리 (Context Management)

모든 정보를 한 번에 주면 AI가 "대충 읽고" 넘어갑니다. 신입 사원에게 회사 100년 역사서를 한 권 줘도 첫날은 읽지 않죠. 대신 **점진적으로 공개**합니다.

**목차화**: 한 거대한 문서 대신 구조화된 목차를 제공합니다.
```
## 컨텍스트 가이드
- 프로젝트 구조: docs/overview.md
- 아키텍처: docs/architecture.md  
- API 명세: docs/api.md
- 스타일 가이드: docs/style.md
```

**필요에 따른 검색**: AI가 필요한 부분만 스스로 찾아 참조하도록 설계합니다. "지금 API를 구현해야 하니까 docs/api.md를 참조해야겠다"는 식으로.

**부담 없는 진입점**: 처음부터 모든 정보를 읽지 않아도 시작할 수 있는 명확한 진입점(예: "먼저 main.py 파일을 만들어")을 제공합니다.

#### CI/CD 강제 (CI/CD Enforcement)

기술적으로 강제하는 규칙을 설정합니다. **말이 아닌 코드로 강제**합니다.

**ESLint**: 코드 스타일 규칙을 위반하면 빌드 실패
```javascript
// .eslintrc.js
module.exports = {
  rules: {
    'no-console': 'error',      // console.log 금지
    'eqeqeq': 'error',          // === 강제
    'no-var': 'error',          // var 금지
  },
};
```

**커밋 메시지 검증**: 커밋 전 메시지 형식 검증 (husky + commitlint)

**자동 테스트**: 테스트 통과 전 병합 불가

**빌드 검사**: TypeScript 타입 체크, 번들 크기 검사 등

이 모든 것들이 "하네스"를 형성합니다. AI가 규칙을 어길 수 없게 만듭니다.

### 3. OpenAI가 구축한 시스템의 특징

OpenAI 팀은 이 3가지 요소를 결합해 다음을 가능하게 했습니다:

- AI가 스스로 계획을 세웁니다
- 계획에 따라 구현합니다
- 구현한 것을 자동으로 테스트합니다
- 테스트 결과(로그)를 읽고 스스로 버그를 발견합니다
- 다시 수정하고 재테스트합니다
- 모든 규칙(린트, 타입 체크, 테스트)을 통과할 때까지 반복합니다

**결과**: 개발자는 "이 기능을 만들어"라고 요청하기만 하면, AI가 완벽하게 만들어 낸 코드를 받습니다. 중간에 "이거 고쳐 줘", "테스트해 봤어?" 같은 개입이 없습니다.

## 작동 원리

### 하네스 엔지니어링의 동작 흐름

```
개발자: "이 기능을 만들어"
         ↓
AI: "계획을 먼저 세우겠습니다"
  (CLAUDE.md 읽고, 구조 설계)
         ↓
AI: "워크트리에서 구현합니다"
  (메인 브랜치와 분리된 환경)
         ↓
AI: "자동 테스트 실행"
  (npm test, 린트 검사, 빌드 확인)
         ↓
검증 통과?
  ├─ NO: 로그 분석 → 버그 발견 → 수정 → 다시 테스트
  │      (이 과정이 자동으로 반복)
  └─ YES: 완성 → 개발자에게 보고
```

### 단계별 상세 설명

**1단계: 계획 수립 (Planning)**
- AI는 작업을 시작하기 전에 먼저 "어떻게 할 것인가"를 계획합니다
- CLAUDE.md 파일을 읽어 프로젝트 규칙, 아키텍처, 제약을 파악합니다
- 경험: "계획 없이 구현하지 않는다"는 규칙이 명시되어 있으면 AI가 따릅니다

**2단계: 격리된 환경 (Isolated Execution)**
```bash
git worktree add ../feature-dev feature
cd ../feature-dev
# 이 디렉토리에서만 작업 → 메인 영향 없음
```
- 각 작업마다 새로운 워크트리(독립적인 브랜치 작업 공간)를 생성합니다
- 메인 브랜치는 항상 안정적으로 유지됩니다
- AI의 실수가 프로덕션에 영향을 주지 않습니다

**3단계: 자동 테스트 및 검증**
```bash
npm run lint    # 스타일 규칙 검사
npm run test    # 단위 테스트
npm run build   # 빌드 검사
```
- 모든 검증이 **자동으로** 실행됩니다
- 실패하면 AI가 오류 메시지를 읽습니다
- 규칙을 위반하면 진행이 불가능합니다 (강제)

**4단계: 피드백 루프 (Self-Correction)**
- 테스트 결과(로그)를 AI가 읽습니다
- "아, 이 부분이 규칙을 어겼네"
- "아, 이 테스트가 실패했네"
- "아, 이 파일의 색상이 명시된 규칙과 다르네"
- AI가 스스로 원인을 파악하고 수정합니다
- 다시 테스트를 실행합니다
- 모든 검증을 통과할 때까지 반복합니다

**5단계: 완성 및 병합**
- 모든 규칙을 통과하면 워크트리를 메인 브랜치와 병합합니다
- 개발자는 완성된 코드를 받습니다
- 추가 검증이 거의 필요 없습니다 (이미 자동으로 검증되었으므로)

### 왜 이것이 5배 이상 빠른가?

**기존 방식의 병목**:
```
AI 구현 (1시간) → 개발자 테스트 (2시간) 
→ 버그 발견 → 개발자 요청 (1시간) 
→ AI 수정 (1시간) → 개발자 재테스트 (2시간)
→ 반복...

총 시간: 매우 길음 (인간의 검증이 병목)
```

**하네스 엔지니어링 방식**:
```
AI 계획 (30분) → AI 구현 (1시간) 
→ AI 자동 테스트 (5분) → 실패 시 AI 자동 수정 (20분)
→ AI 재테스트 (5분) → 통과

총 시간: 2시간 (모두 자동, 인간 개입 없음)
```

인간의 개입이 가장 느린 부분이므로, 이를 제거하는 것만으로도 생산성이 극대화됩니다.

## 코드 예시

### CLAUDE.md: 프로젝트 규칙 문서

이 파일은 AI가 **항상 먼저 읽는** 규칙서입니다. Claude Code는 어떤 명령을 실행하기 전에 먼저 이 파일을 로드합니다.

```markdown
# 프로젝트 개발 가이드

## 핵심 원칙
1. 계획 없이 구현하지 않는다
   - 복잡한 작업은 항상 계획(plan)부터 시작
   - 계획을 사용자가 승인한 후 구현 시작

2. 격리된 환경에서만 작업한다
   - 항상 git worktree로 새 작업 공간 생성
   - main 브랜치는 절대 직접 수정하지 않음

3. 검증 없이 커밋하지 않는다
   - 모든 변경사항은 자동 검증 통과 필수
   - 테스트, 린트, 타입 체크 모두 통과

## 금지 규칙
- console.log를 프로덕션 코드에 남기지 않음
- var 키워드 사용 금지 (const/let만 사용)
- 미사용 변수 방치 금지
- 타입 정의 없이 any 사용 금지
- 테스트 없이 로직 변경 금지

## 필수 검증 단계
```bash
npm run lint    # ESLint 통과
npm run test    # Jest 테스트 100% 통과  
npm run build   # TypeScript 타입 체크 및 빌드 성공
npm run preview # 프리뷰 서버 구동 확인
```

## 컨텍스트 로드맵
(필요할 때마다 이 문서에서 참조)

- **아키텍처**: docs/architecture.md
- **API 명세**: docs/api.md  
- **컴포넌트 가이드**: docs/components.md
- **스타일 규칙**: docs/style-guide.md
- **데이터베이스**: docs/database.md
```

**설명**:
- AI가 항상 먼저 읽으므로, 가장 중요한 규칙을 여기 배치합니다
- "계획부터 시작" 규칙이 명시되면 AI는 무계획적 구현을 하지 않습니다
- "워크트리에서만 작업" 규칙이 있으면 메인 브랜치 오염을 방지합니다
- 금지 규칙들은 다음의 자동 검증(ESLint 등)으로 기술적으로 강제됩니다

### ESLint 설정: 기술적 강제

```javascript
// .eslintrc.js
module.exports = {
  extends: ['eslint:recommended', 'next/core-web-vitals'],
  rules: {
    // 명시적 규칙 위반 시 에러
    'no-console': 'error',           // console.log 금지 → AI가 써도 빌드 실패
    'no-var': 'error',               // var 금지 → const/let만 가능
    'eqeqeq': 'error',               // === 강제 → == 사용 불가
    'no-unused-vars': 'error',       // 미사용 변수 금지
    '@typescript-eslint/no-explicit-any': 'error',  // any 금지
    
    // 경고 (수정하도록 유도)
    'prefer-const': 'warn',          // const 사용 권장
    'no-commented-code': 'warn',     // 주석 처리된 코드 제거
  },
};
```

**동작**:
1. AI가 `console.log('test')`를 작성합니다
2. `npm run lint` 실행
3. ESLint가 에러 감지: "no-console rule violated"
4. 빌드 실패
5. AI가 로그에서 에러 메시지를 읽습니다: "line 42: console.log is not allowed"
6. AI가 자동으로 console.log를 제거합니다
7. 다시 `npm run lint` 실행 → 통과

"console.log를 쓰지 마"라고 말하는 것이 아니라, **기술적으로 불가능하게 만드는** 것입니다.

### package.json: 검증 자동화

```json
{
  "scripts": {
    "lint": "eslint src --max-warnings 0",
    "test": "jest --coverage --testPathIgnorePatterns=e2e",
    "build": "tsc --noEmit && next build",
    "preview": "next start",
    "validate": "npm run lint && npm run test && npm run build"
  }
}
```

**설명**:
- `npm run lint`: 코드 스타일 검증 (위반 시 빌드 실패)
- `npm run test`: 단위 테스트 (커버리지 기준 미충족 시 실패)
- `npm run build`: TypeScript 타입 체크 + 프로덕션 빌드
- `npm run validate`: 모든 검증을 한 번에 실행

AI가 이 명령들을 실행하면:
- 한 단계라도 실패하면 다음으로 진행 불가
- AI가 오류 로그를 읽고 수정
- 모든 단계를 통과할 때까지 반복

### 워크트리 워크플로우

```bash
# AI가 새 작업을 시작할 때
git worktree add ../fix-login feature/login
cd ../fix-login

# 이 디렉토리에서만 작업
echo 'export function Login() { return ... }' > src/Login.tsx

# 자동 검증
npm run lint     # 통과
npm run test     # 통과
npm run build    # 통과

# 성공하면 병합
cd ..
git checkout main
git merge fix-login
git worktree remove ../fix-login

# 실패하면?
# AI가 로그를 읽고 원인을 파악해 수정
# 다시 검증 실행
# 성공할 때까지 반복
```

**장점**:
- 메인 브랜치는 항상 안정적 (자동 검증 통과한 것만 병합)
- AI의 실수가 프로덕션에 영향 없음
- 여러 작업을 동시에 진행 가능
- 실패 시 손쉽게 롤백 가능

## 함정·실수

### 함정 1: 문서 과다로 인한 무시

**상황**: 100KB 분량의 한 거대한 문서에 모든 정보를 집어넣음

**문제**: 
```
[AI가 문서를 읽기 시작]
첫 10KB: "좋아, 이건 이런 프로젝트구나"
다음 20KB: "음... 이것도 중요한가?"
50KB 지점: "아, 이거 너무 많은데... 대충 훑어봐야겠다"
70KB 이후: "뭐가 중요한지 모르겠으니 무시하고 진행해야지"

결과: 중요한 규칙을 무시하고 작업 → 실수 발생
```

**해결책**:
```markdown
# 컨텍스트 가이드 (이 구조로 분리)

## 시작
→ docs/overview.md (꼭 읽어야 할 것)

## 개발 중
→ docs/architecture.md (필요할 때 참조)

## 세부사항
→ docs/api/endpoints.md
→ docs/database/schema.md
→ docs/style/guide.md
```

AI가 "지금 API를 구현해야 하니까 docs/api/endpoints.md를 봐야겠다"는 식으로 필요한 것만 찾게 합니다.

### 함정 2: 말로만 강제하기

**나쁜 예**:
```markdown
# 색상 규칙
- 버튼은 파란색(#007BFF)을 사용합니다
- 테두리는 회색(#CCCCCC)을 사용합니다
- 경고는 빨간색(#FF0000)을 사용합니다
```

**문제**: AI가 이를 무시할 수 있습니다
```javascript
// AI가 규칙을 무시하고 작성
const buttonColor = '#FF6B6B';  // 규칙과 다른 색
```

**좋은 예**:
```javascript
// colors.ts - 색상을 상수로 정의
export const COLORS = {
  button: '#007BFF',
  border: '#CCCCCC',
  warning: '#FF0000',
} as const;

// ESLint 규칙: 색상은 상수에서만 참조
rules: {
  'no-hardcoded-color': 'error',  // 하드코딩된 색상 금지
}

// AI가 작성해야 하는 코드
const buttonStyle = { color: COLORS.button };  // 상수 사용 강제
```

이제 AI가 규칙을 어길 수 없습니다 (강제).

### 함정 3: 로깅 없이 진행

**나쁜 예**:
```javascript
// 테스트 결과를 AI에게 보여주지 않음
$ npm test
✓ test passed
$ npm run build
✓ build succeeded
```

**문제**: AI가 자신의 작업 결과를 모르므로, 실수를 발견할 수 없습니다.

**좋은 예**:
```javascript
// 상세한 로그를 남김
$ npm test
Test Suites: 5 passed, 5 total
Tests:       42 passed, 3 failed, 45 total
  ✓ src/Login.test.tsx: renders login form
  ✗ src/Login.test.tsx: submits form with correct data
    Expected: username='admin', password='secret'
    Actual: username='', password=''
  ✗ src/Auth.test.tsx: refreshes token on expiry

$ npm run lint
ERROR in src/Login.tsx:5:1
  no-unused-vars: 'handleChange' is defined but never used
```

AI가 로그를 읽으면:
- "아, 폼 제출 테스트가 실패했네"
- "아, handleChange 변수를 정의했는데 안 쓰고 있네"
- 자동으로 수정

### 함정 4: 한 번에 너무 많은 작업 요청

**나쁜 예**:
```
사용자: "전체 채팅 애플리케이션을 만들어. 
        웹소켓 연결, 메시지 저장소, UI 컴포넌트, 
        인증, 알림 기능, 다크모드, 번역 기능 포함."
```

**문제**: AI가 계획 없이 무작정 코딩을 시작합니다. 중간에 무엇을 해야 할지 헷갈리고, 실수가 많아집니다.

**좋은 예**:
```
사용자: "1단계: 웹소켓 연결 구조를 설계해 줘"
AI: "이렇게 설계하겠습니다" (계획 제시)
사용자: "좋아, 진행해"
AI: "완성했습니다"

사용자: "2단계: 메시지 저장소를 구현해"
...
```

큰 작업을 작은 단계로 나누면 AI가 각 단계에 집중할 수 있고, 실수가 줄어듭니다.

### 함정 5: 컨텍스트 없이 규칙만 강제

**나쁜 예**:
```
린트만 통과하면 됨 → 
AI가 형식적으로만 규칙을 맞추고 동작은 무시
```

**좋은 예**:
```
린트 + 테스트 + 실제 동작 검증 →
AI가 기술적으로 올바른 코드만 작성 가능
```

규칙만으로는 부족하고, 테스트(동작 검증)가 함께 있어야 합니다.

## 베스트 프랙티스

### 1. 단계적 작업 요청

복잡한 작업을 여러 단계로 나누어 요청합니다.

**단계 1: 설계**
```
"다음 기능의 아키텍처를 설계해 줘:
- 실시간 메시지 전송
- 메시지 저장 및 조회
- 사용자 온라인 상태

다음을 포함해서 설계해:
- 데이터 구조
- 웹소켓 메시지 포맷
- 데이터베이스 스키마"
```

**단계 2: 구현**
```
"설계한 대로 웹소켓 연결 로직을 구현해."
```

**단계 3: 테스트**
```
"웹소켓 연결, 메시지 전송, 에러 처리에 대한 테스트를 작성해."
```

**단계 4: 통합**
```
"프론트엔드에서 이 웹소켓을 사용하는 UI 컴포넌트를 만들어."
```

각 단계가 완료되고 테스트를 통과해야 다음 단계로 진행합니다.

### 2. 명확한 성공 기준 정의

"완료"의 정의를 명확히 합니다.

```
이 기능이 완료되었다 = 다음을 모두 만족:

✓ 모든 ESLint 검사 통과 (경고 0개)
✓ 모든 TypeScript 타입 에러 0개
✓ 100% 테스트 커버리지 (라인 기준)
✓ 성능: 초기 로딩 < 2초
✓ 접근성: WCAG 2.1 AA 기준 통과
✓ 크로스 브라우저 호환성: Chrome, Firefox, Safari 최신 버전
✓ README 및 코드 주석 작성 완료
```

이 기준을 CLAUDE.md에 명시하면, AI가 이를 목표로 작업합니다.

### 3. 정기적인 컨텍스트 갱신

프로젝트가 진행되면서 CLAUDE.md를 업데이트합니다.

```markdown
## 최근 변경사항 (지속적 갱신)

- [2024-01] 웹소켓 아키텍처 확정
- [2024-02] 마이크로프론트엔드로 변경
- [2024-03] 새로운 색상 팔레트 도입

## 사용 중단된 패턴
- Redux → Zustand로 마이그레이션 완료
- REST API → GraphQL 마이그레이션 진행 중

## 진행 중인 작업
- Dark mode 구현
- 다국어 지원
```

AI가 최신 상태를 반영해 작업할 수 있습니다.

### 4. 자동화 도구 적극 활용

**코드 품질**:
- ESLint: 스타일 규칙
- Prettier: 자동 포매팅
- TypeScript: 타입 안정성
- SonarQube: 복잡성 분석

**테스트**:
- Jest: 단위 테스트
- Cypress: E2E 테스트
- Playwright: 크로스 브라우저 테스트

**성능**:
- Lighthouse: 성능 스코어
- Bundle Analyzer: 번들 크기
- Lighthouse CI: 자동화된 성능 체크

**배포**:
- GitHub Actions: CI/CD 자동화
- Pre-commit hooks: 커밋 전 검증

이 모든 것이 **AI를 제어하는 하네스**입니다.

### 5. 점진적 정보 공개 전략

```
## 컨텍스트 진입점

### 새로운 작업 시작 시 (필수 읽음)
- docs/overview.md
- 현재 프로젝트의 5줄 요약

### 프론트엔드 작업 시
- docs/frontend/components.md
- docs/frontend/styling.md
- docs/frontend/data-fetching.md

### 백엔드 작업 시
- docs/backend/api.md
- docs/backend/database.md
- docs/backend/authentication.md

### 깊이 있는 작업 시
- docs/architecture.md (전체 시스템 아키텍처)
- docs/design-decisions.md (중요한 기술 결정)
```

필요에 따라 AI가 적절한 문서를 참조하도록 구조화합니다.

### 6. 자동 수정 메커니즘 설정

일부 규칙은 AI가 위반하면 자동으로 수정되도록 설정합니다.

```javascript
// .eslintrc.js
"semi": ["error", "always"],  // 세미콜론 강제
"quotes": ["error", "single"], // 싱글 쿼트 강제

// npm run lint:fix로 자동 수정 가능
// 또는 CI/CD에서 자동 수정
```

AI가 규칙을 어기면:
1. 첫 시도: 린트 에러
2. AI가 로그를 읽음
3. `npm run lint:fix` 자동 실행
4. 자동 수정됨
5. 재테스트 → 통과

이렇게 하면 AI의 자동 수정 주기가 더 빨라집니다.

## 참고

### 영상에서 언급된 자료
- **OpenAI 하네스 엔지니어링 문서**: 영상에서 구체적 URL 제시 없음 (공개된 OpenAI 연구 논문 참조)
- **Claude Code 플랫폼**: Anthropic에서 제공하는 AI 코딩 도구

### 외부 링크
- [바이브코딩 스터디 지원](https://forms.gle/2d67DKoFWRsKNA5g7)
- [바이브코딩 강의](https://codingnoona.thinkific.com/courses/vibe-coding)

### 추가 학습 자료

**Git 워크트리**:
- 공식 문서: `git help worktree`
- 개념: 메인 브랜치와 분리된 독립적인 작업 공간

**ESLint**:
- 공식 사이트: https://eslint.org
- 룰 목록: https://eslint.org/docs/rules/

**CI/CD 파이프라인**:
- GitHub Actions 문서
- GitLab CI 문서
- Jenkins 문서

**프롬프트 엔지니어링**:
- OpenAI Prompt Engineering Guide
- Anthropic Claude 프롬프트 가이드

### 관련 개념

**프롬프트 엔지니어링**: AI에게 "무엇을" 해야 할지 명확히 알려주는 기술

**컨텍스트 엔지니어링**: AI가 작업 맥락을 이해하도록 정보를 제공하는 기술

**하네스 엔지니어링**: AI가 정해진 경계를 벗어나지 않도록 기술적으로 강제하는 기술

**Agentic AI**: AI 에이전트가 목표를 스스로 계획하고 실행하도록 하는 방식

**자동화 테스트**: 코드 실행 후 결과를 자동으로 검증하는 방식

**CI/CD**: 지속적 통합(Continuous Integration)과 지속적 배포(Continuous Deployment)

---

## 요약

하네스 엔지니어링은 단순한 "지침"이 아닌 **기술적 강제**를 통해 AI의 작업을 자동화하는 방법론입니다.

**핵심 3가지**:
1. **가시성**: AI가 자신의 작업 결과를 볼 수 있게 (로깅, 스크린샷)
2. **컨텍스트 관리**: 필요한 정보만 점진적으로 공개
3. **CI/CD 강제**: 규칙을 기술적으로 강제 (위반 불가)

이를 통해 **인간의 개입을 제거**하고 **AI의 자동 루프**(계획 → 구현 → 테스트 → 수정)를 가능하게 합니다.

결과: 개발자는 요청만 하고, AI가 완벽하게 완성된 코드를 만들어 냅니다.
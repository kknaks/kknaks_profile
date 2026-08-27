---
type: content
id: C-016
date: 2026-05-22
duration: '27:59'
speaker: 빌더 조쉬 Builder Josh
kind: tutorial
youtubeId: gNgHnkJc29M
title:
  en: Building High-Quality UI Prototypes with Claude Design Systems
  ko: 클로드 디자인 디자인 시스템으로 고품질 UI 프로토타입 만들기
summary:
  en: Maximize Claude Design performance with design systems, then build interactive prototypes using PRD-based workflow and Claude Code integration
  ko: 디자인 시스템 세팅으로 클로드 디자인의 성능을 극대화하고, PRD 기반 워크플로우로 인터랙티브 프로토타입을 제작하는 완전한 실무 가이드
tags:
- '#claude-design'
- '#design-system'
- '#ui-kit'
- '#figma'
- '#prototyping'
- '#product-design'
- '#interactive-prototype'
---

## 요지

- 디자인 시스템은 AI의 성능을 끌어올리는 '하네스 엔지니어링'이며, 사전 설정된 컴포넌트와 스타일로 일관된 고품질 디자인을 보장한다.
- 피그마 커뮤니티의 검증된 UI 키트(Apple iOS, Google Material Design, Wanted 등)를 .fig 파일로 다운로드하여 클로드 디자인에 업로드할 수 있다.
- PRD(제품 요구사항 문서)는 AI에게 문맥을 제공하는 기초로, 대상 사용자·핵심 기능·구체적 시나리오를 명시해야 고품질 결과물이 나온다.
- 클로드 디자인에서 생성된 HTML/CSS 코드는 클로드 코드로 직접 옮겨 실제 개발 코드로 구현하고 수정할 수 있다.

## 개요

Claude Design은 2024년 출시된 AI 디자인 도구로, 기존 디자이너들이 Figma에 의존하던 영역을 공략하며 시장에 큰 충격을 주고 있습니다. 단순히 UI를 생성하는 수준을 넘어 **일관된 고품질의 인터랙티브 프로토타입**을 빠르게 제작할 수 있게 해주는 도구입니다. Claude Design을 만든 디자이너가 Figma 출신이라는 점도 흥미로우며, 현재 코딩, 디자인, 커뮤니케이션의 경계가 허물어지는 새로운 작업 방식이 정착되고 있습니다.

본 가이드는 Claude Design을 **제대로 활용하는 방법**을 다룹니다. 99%의 사용자가 무계획적으로 접근하지만, **디자인 시스템을 먼저 세팅**하고 **PRD 기반 워크플로우**를 따르면 주니어 디자이너 수준의 화면을 순식간에 제작할 수 있습니다. 이 교안은 초기 세팅부터 인터랙티브 프로토타입 제작, 클로드 코드 연동까지의 **완전한 실무 워크플로우**를 다룹니다.

## 배경 / 사전 지식

### Claude Design이란?

Claude Design은 Anthropic의 Claude AI 기반 디자인 생성 도구입니다. Figma처럼 벡터 기반 도형을 직접 그리는 것이 아니라, **텍스트 프롬프트와 디자인 시스템을 입력받아 interactive HTML/CSS 프로토타입을 자동 생성**합니다. 생성된 결과물은 실제로 클릭 가능하고 상호작용하며, Claude Code로 직접 옮겨 실제 개발 코드로 전환할 수 있습니다.

### 디자인 시스템 (Design System)

UI 컴포넌트(버튼, 카드, 폼, 네비게이션 등), 색상 팔레트, 타이포그래피, 아이콘 세트, 여백 규칙(spacing), 그림자, 라운드 정도 등을 일관되게 정의한 가이드라인 문서입니다. 브랜드와 제품의 시각적 일관성을 보장하며, 모든 팀원이 같은 기준으로 디자인하도록 합니다.

**실제 사례**:
- Apple의 iOS Design System: iPhone/iPad 앱들의 통일된 모습
- Google의 Material Design: Android 및 Google 서비스들의 일관된 디자인
- Wanted의 한국식 디자인 시스템: 로컬 문화와 정서를 반영

### UI 키트 (UI Kit)

디자인 시스템을 Figma 파일로 구현한 것입니다. 사용 가능한 모든 컴포넌트(버튼 4가지, 카드 3가지 등)와 스타일이 이미 만들어져 있어서, 디자이너가 이를 복사·조합하면 일관된 결과물을 얻을 수 있습니다. Figma 커뮤니티에서 대기업과 개발사가 **무료로 공개**한 UI 키트를 다운로드할 수 있습니다.

### PRD (Product Requirement Document)

제품이 **무엇을 해야 하는지** 정의하는 문서입니다. 기능, 대상 사용자, 사용 시나리오, 성공 기준, 특수 요구사항 등을 명시합니다. AI에게 "홈 화면 만들어"라고 하면 일반적인 결과가 나오지만, PRD를 제공하면 구체적이고 맥락 있는 디자인이 생성됩니다.

### 하네스 엔지니어링 (Harness Engineering)

AI 모델의 성능을 극대화하기 위한 **사전 설정 작업**입니다. 개발자들의 경우 프롬프트 작성, 컨텍스트 제공, few-shot 예제 제공 등이 하네스 엔지니어링입니다. **디자인 분야에서는 디자인 시스템이 바로 이것**입니다. 미리 정의된 색상, 폰트, 컴포넌트를 AI가 학습하도록 제공하면, AI가 이를 자동으로 적용하여 고품질 결과물을 생성합니다.

## 핵심 개념

### 1. 디자인 시스템 = 디자이너의 하네스

개발자들이 AI 성능을 높이기 위해 하네스 엔지니어링을 하듯이, 디자이너들도 **디자인 시스템을 미리 설정**하여 AI의 출력 품질을 제어합니다.

**작동 원리**:
- 폰트(예: 본문 14px Sans-serif, 제목 24px Bold), 컬러(주 색상 #0066FF, 배경 #F5F5F5), 버튼 스타일 등이 사전에 정의되어 있으면
- Claude Design이 새로운 화면을 만들 때 이 규칙들을 **자동으로 적용**하여 일관되고 전문적인 결과물을 생성
- 수동으로 각 버튼마다 색상, 크기, 폰트를 지정할 필요가 없음

**예시**:
- ❌ 디자인 시스템 없음: AI가 매번 다른 컬러, 폰트, 버튼 크기를 선택 → 결과물이 매번 달라짐
- ✅ 디자인 시스템 있음: Material Design 키트를 업로드 → AI가 Material의 색상과 컴포넌트를 자동으로 적용 → 일관된 전문적 결과물

### 2. Figma 커뮤니티 리소스 활용

Figma 커뮤니티(figma.com/community)에는 Apple, Google, Wanted 등 대기업과 개발사가 공개한 **검증된 UI 키트**가 있습니다. 이들은 수년간 사용자 테스트를 거친 검증된 디자인 기준입니다. 무료로 다운로드하여 Claude Design에 업로드할 수 있습니다.

**주요 UI 키트**:

| 이름 | 특징 | 추천 대상 |
|------|------|----------|
| Apple iOS Design System | iPhone/iPad 표준, 깔끔하고 세련됨 | iOS 앱 개발자 |
| Google Material Design 3 | Android 표준, 접근성 뛰어남, 풍부한 색상 | 안드로이드/웹 개발자 |
| Wanted Design System | 한국식 정서, 현지화된 타이포그래피 | 한국 서비스 디자이너 |
| Ant Design (중국) | B2B 시스템 중심, 복잡한 UI 컴포넌트 | 대시보드, 관리자 페이지 |

### 3. PRD → 시나리오 → 디자인 → 프로토타입의 흐름

Claude Design에 단순히 "홈 화면 만들어"라고 명령하는 것이 아니라, **구체적인 PRD를 제공**하고 사용 사례를 설명해야 고품질 결과물이 나옵니다.

**비교**:
```
❌ 나쁜 프롬프트: "택시 앱 UI 만들어"
→ AI가 일반적인 택시 앱(Uber, 카카오T 비슷)을 만듦
→ 특수성 없음, 팀 맥락 반영 안 됨

✅ 좋은 프롬프트:
"시니어 사용자(65세 이상)를 위한 택시 앱 '카카오T 시니어'를 만들어주세요.
- 시각 약화를 고려해 텍스트는 최소 16px
- 복잡한 메뉴 제거, '탑승하기' 큰 버튼 1개 강조
- 자녀와의 실시간 위치 공유 기능 (안전)
- 도착 시 자녀에게 자동 알림 전송

필요한 화면:
1. 홈: '탑승하기' 큰 버튼 + 지도
2. 탑승 중: 택시 정보 + 실시간 위치
3. 자녀 앱: 엄마의 위치 + '도착 확인' 버튼
4. 도착: '안전하게 도착' 메시지

각 화면 간 상호작용을 추가하세요."
```

→ AI가 시니어 정서를 반영한 구체적인 화면 생성
→ 팀의 기획과 일치하는 결과물

### 4. Claude Design → Claude Code 연동

Claude Design에서 생성된 시안은 단순 이미지가 아니라 **실행 가능한 HTML/CSS/JavaScript 코드**입니다. 이 코드를 Claude Code로 옮기면 실제 개발 코드로 구현하고 수정할 수 있습니다.

**파이프라인**:
1. Claude Design: "테스트 디자인" → 프로토타입 생성
2. 코드 복사 또는 파일 다운로드
3. Claude Code: 코드 붙여넣기 → 실시간 수정 가능
4. 개발 팀: 최종 코드를 실제 프로젝트에 통합

## 작동 원리

### Step 1: 디자인 시스템 세팅 (5~10분)

#### 1-1. Figma 커뮤니티에서 UI 키트 찾기

1. **figma.com 접속** (로그인 필요)
2. 좌측 사이드바에서 **"Community"** 탭 클릭
3. **"Design Resources"** 선택
4. **"UI Kits"** 필터 적용
5. 원하는 키트 선택
   - Material Design 3 (구글)
   - Wanted Design System (한국)
   - Apple iOS Design System (애플) 등

#### 1-2. 파일 복사 및 다운로드

1. 선택한 UI 키트 페이지에서 **"Open in Figma"** 클릭
2. "Open a copy" 또는 "Make a copy" 선택
3. 자신의 Figma 계정으로 복사됨
4. Figma 편집 화면에서 **File** 메뉴 → **"Save local copy"**
5. `.fig` 확장자 파일 다운로드

#### 1-3. Claude Design에 업로드

1. **claude.ai** 접속 → **Design** 탭
2. **"Create new design system"** 클릭
3. **"Upload Figma file"** → 위에서 다운로드한 `.fig` 파일 선택
4. **"Attach file"** 클릭
5. 파일 분석 대기 (약 5~10분)
   - 화면에 "Processing..." → "Review draft design system" 표시
   - 누락된 폰트나 요소가 있으면 표시됨 (무시 가능)
6. **"Publish"** 클릭하여 저장

### Step 2: PRD 작성 (10~20분)

Claude Design에서 새로운 디자인을 만들기 전에 문서로 PRD를 작성합니다. 이를 프롬프트에 붙여넣게 됩니다.

**PRD 필수 포함 항목**:

```
## 제품 개요
- 제품명: [서비스 이름]
- 한 줄 설명: [무엇을 하는 앱/웹인가]

## 대상 사용자
- 나이대: [예: 60세 이상]
- 기술 수준: [스마트폰 기본 사용 가능 수준]
- 특수한 요구사항: [예: 시각 약화 고려]

## 핵심 기능 (3~5개)
1. [기능 1]: [설명]
2. [기능 2]: [설명]
3. [기능 3]: [설명]

## 사용 시나리오 (2~3가지)
### 시나리오 1: [상황 설명]
- 사용자가 [액션]
- 그러면 [결과]
- 그 후 [다음 액션]

## 디자인 요구사항
- 폰트 최소 크기: [16px 등]
- 색상 톤: [밝음/어두움]
- 언어: [한국어 등]
- 기타 특수 요구사항: [예: 버튼 크기, 복잡도 등]

## 필요한 화면 목록
1. [화면명]: [구성 요소 설명]
2. [화면명]: [구성 요소 설명]
```

### Step 3: 프로토타입 생성 (3~5분)

1. Claude Design의 **Design System** 탭에서 위에서 publish한 시스템 선택
2. **"New design"** 클릭
3. 프로젝트 이름 입력 (예: "카카오T 시니어")
4. **"Create"** 클릭
5. **프롬프트 입력창**에 위의 PRD를 붙여넣기
   ```
   [PRD 전체 텍스트]
   
   필요한 화면:
   1. [화면명]: [설명]
   2. [화면명]: [설명]
   
   각 화면 간 상호작용을 포함하세요.
   ```
6. **"Generate"** 또는 **"Send"** 클릭
7. 생성 대기 (약 1~3분)
8. 결과 확인
   - 캔버스에 화면들이 표시됨
   - 오른쪽 패널에서 각 화면의 구성 요소 확인 가능

### Step 4: 인터랙티브 프로토타입 추가

Claude Design은 자동으로 상호작용(버튼 클릭, 화면 전환 등)을 만들 수 있습니다.

**프롬프트 예시**:
```
화면 간 상호작용을 추가해주세요:

1. 홈 화면의 "탑승하기" 버튼 클릭 → 탑승 중 화면으로 전환
2. 탑승 중 화면의 "취소" 버튼 클릭 → 홈 화면으로 돌아가기
3. 자녀 앱에서 "도착 확인" 버튼 클릭 → 확인 완료 메시지 표시
4. 홈 화면의 "마이페이지" 버튼 클릭 → 설정 화면으로 이동
```

→ AI가 자동으로 버튼에 상호작용 추가

### Step 5: Claude Code로 연동 (2~5분)

#### Option A: 코드 복사

1. Claude Design 화면 오른쪽 상단 **"Code"** 버튼 클릭
2. 생성된 HTML/CSS/JavaScript 코드 표시
3. **"Copy"** 클릭하여 클립보드에 복사
4. claude.ai의 **"Code"** 탭으로 이동
5. 새 파일 생성 후 코드 붙여넣기
6. Claude Code가 자동으로 프리뷰 제공

#### Option B: 파일 다운로드

1. Claude Design 화면 오른쪽 상단 **"Download"** 버튼
2. 압축 파일로 다운로드 (HTML, CSS, 이미지 포함)
3. 압축 해제 후 프로젝트 폴더에 추가

## 코드 예시

### 예시 1: PRD 템플릿 (실제 작성 예시)

```
## 제품 개요
- 제품명: 카카오T 시니어
- 한 줄 설명: 시니어 사용자를 위한 안전한 택시 탑승 및 자녀 연동 앱

## 대상 사용자
- 나이대: 60세 이상
- 기술 수준: 스마트폰 기본 조작 가능 (전화, 문자 정도)
- 특수 요구사항: 시각 약화 고려, 복잡한 메뉴 제거, 큰 터치 영역

## 핵심 기능
1. 간단한 탑승 요청: 중앙의 "탑승하기" 큰 버튼 1개로 택시 호출
2. 실시간 위치 공유: 탑승 중 자녀에게 자동 알림
3. 도착 확인: 목적지 도착 시 자녀에게 알림, 자녀가 확인 버튼 클릭
4. 응급 상황: 길게 누르면 상담원 자동 연결

## 사용 시나리오
### 시나리오 1: 할머니의 탑승
- 할머니가 앱을 켜서 "탑승하기" 큰 버튼을 클릭
- 시스템이 가장 가까운 택시 매칭 (자동 선택, 확인 불필요)
- 택시 번호와 기사 사진, 도착 시간 표시
- 자녀 지영이에게 "엄마가 택시를 탔습니다" 자동 알림

### 시나리오 2: 도착 및 자녀 안심
- 택시가 목적지에 도착
- 할머니가 "도착했습니다" 버튼 클릭
- 지영이에게 "엄마가 안전하게 도착했습니다" 알림
- 지영이가 "안내 감사합니다" 버튼 클릭

## 디자인 요구사항
- 폰트 최소 크기: 16px (큰 텍스트)
- 버튼 크기: 최소 44x44px (터치하기 쉬움)
- 색상: 명도 대비 높음 (검은색 텍스트 + 흰색 배경)
- 복잡한 메뉴: 제거 (홈 화면 1개, 설정 1개만)
- 언어: 한국어 ("탑승하기", "도착했습니다" 등)

## 필요한 화면 목록
1. 홈 화면: 지도 배경 + 중앙 "탑승하기" 초록 버튼 (매우 큼) + 현재 위치 마커
2. 탑승 중 화면: 택시 번호 크게 표시, 기사 사진, 도착 예상 시간, "취소" 버튼
3. 자녀 앱 - 알림 화면: 엄마의 실시간 위치 지도, "도착 확인" 파란 버튼
4. 도착 후 화면: "안전하게 도착했습니다" 큰 텍스트 + 확인 버튼
5. 마이페이지: 최근 이용 내역, 자녀 연동 설정
```

**설명**: 이것이 Claude Design 프롬프트에 붙여넣을 PRD의 실제 예시입니다. "시니어 사용자"라는 명확한 타겟과 "큰 텍스트, 간단한 메뉴" 같은 구체적 요구사항이 있으면, AI가 해당 정서를 반영하여 디자인합니다.

### 예시 2: Claude Design 프롬프트 (실제 입력값)

```
위의 Material Design 3 시스템을 사용하여 다음 프로토타입을 만들어주세요:

## 제품: 쇼핑 모바일 앱
- 목적: 30~50대 직장인 여성을 위한 패션 쇼핑 앱
- 대상: 온라인 쇼핑 경험 많음, 모바일 친숙
- 톤: 세련되고 현대적

## 핵심 기능
1. 추천 상품 피드 (인스타그램 스타일)
2. 상품 상세 페이지 (가격, 리뷰, 사진)
3. 장바구니 관리
4. 결제 프로세스

## 화면 설명

### 홈 화면
- 상단: 검색 바 + 필터 (색상, 가격, 사이즈)
- 중앙: 상품 카드 그리드 (2열)
  - 각 카드: 상품 사진 + 브랜드명 + 가격 + 찜 버튼
- 하단: 네비게이션 (홈, 검색, 장바구니, 마이페이지)

### 상품 상세 페이지
- 상단: 상품 사진 슬라이드
- 브랜드명 + 상품명 + 가격 + 평점
- 사이즈 선택 (S, M, L, XL)
- 색상 선택 (검은색, 흰색, 회색, 파란색)
- "장바구니 추가" 버튼 (Material Design 파란색)
- 리뷰 섹션 (별점 + 코멘트)

### 장바구니
- 상품 목록 (상품 사진 + 가격 + 수량 조절)
- 총액 계산
- "결제하기" 버튼

## 인터랙션
1. 홈 화면의 상품 카드 클릭 → 상세 페이지로 이동
2. 상세 페이지 "장바구니 추가" 클릭 → 작은 팝업 "추가되었습니다" 표시
3. 하단 "장바구니" 아이콘 클릭 → 장바구니 화면으로 이동
4. 장바구니 "결제하기" 클릭 → 결제 화면으로 이동

Material Design 3의 색상(primary blue, surface colors)과 타이포그래피를 일관되게 적용해주세요.
```

**설명**:
- 첫 번째 코드 블록(예시 1)은 **PRD를 별도 문서로 작성**하는 템플릿입니다.
- 두 번째 코드 블록(예시 2)은 이 PRD를 **Claude Design의 프롬프트 입력창에 직접 붙여넣는 형태**입니다.
- "Material Design 3 시스템을 사용하여"라는 표현이 중요합니다. 이렇게 명시하면 AI가 해당 디자인 시스템을 자동으로 적용합니다.

### 예시 3: 생성된 HTML/CSS 코드 (Claude Code로 옮기는 코드)

```html
<!-- Claude Design에서 생성되어 Claude Code로 옮기는 코드 예시 -->
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>카카오T 시니어</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background-color: #ffffff;
        }
        
        /* 홈 화면 */
        .home-screen {
            height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }
        
        .map-container {
            width: 100%;
            height: 60%;
            background-color: #f0f0f0;
            border-radius: 20px;
            margin-bottom: 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #999;
        }
        
        /* 탑승하기 버튼: 시니어를 위해 매우 크고 명확함 */
        .ride-button {
            width: 200px;
            height: 200px;
            border-radius: 50%;
            background-color: #00cc66;  /* 초록색 */
            border: none;
            font-size: 32px;  /* 매우 큼 */
            font-weight: bold;
            color: white;
            cursor: pointer;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
        }
        
        .ride-button:hover {
            transform: scale(1.05);
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
        }
        
        .ride-button:active {
            transform: scale(0.95);
        }
        
        /* 탑승 중 화면 */
        .riding-screen {
            display: none;  /* 기본 숨김 */
            flex-direction: column;
            height: 100vh;
            padding: 20px;
            background-color: #f9f9f9;
        }
        
        .taxi-info {
            background-color: white;
            padding: 30px;
            border-radius: 20px;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        
        .taxi-number {
            font-size: 48px;  /* 매우 큼 */
            font-weight: bold;
            color: #333;
            margin-bottom: 20px;
        }
        
        .taxi-driver {
            font-size: 18px;
            color: #666;
            margin-bottom: 20px;
        }
        
        .estimated-time {
            font-size: 24px;
            color: #00cc66;
            font-weight: bold;
        }
        
        .cancel-button {
            background-color: #ff6b6b;
            color: white;
            padding: 16px 32px;
            border: none;
            border-radius: 12px;
            font-size: 18px;
            cursor: pointer;
            margin-top: auto;
        }
    </style>
</head>
<body>
    <!-- 홈 화면 -->
    <div class="home-screen" id="homeScreen">
        <div class="map-container">지도 영역</div>
        <button class="ride-button" onclick="showRidingScreen()">탑승</button>
    </div>
    
    <!-- 탑승 중 화면 -->
    <div class="riding-screen" id="ridingScreen">
        <div class="taxi-info">
            <div class="taxi-number">서울 64가 1234</div>
            <div class="taxi-driver">기사: 김영철</div>
            <div class="estimated-time">5분 후 도착</div>
        </div>
        <button class="cancel-button" onclick="showHomeScreen()">취소</button>
    </div>
    
    <script>
        function showRidingScreen() {
            document.getElementById('homeScreen').style.display = 'none';
            document.getElementById('ridingScreen').style.display = 'flex';
        }
        
        function showHomeScreen() {
            document.getElementById('ridingScreen').style.display = 'none';
            document.getElementById('homeScreen').style.display = 'flex';
        }
    </script>
</body>
</html>
```

**코드 설명**:
- `class="ride-button"`: 탑승하기 버튼. 시니어 사용자를 위해 **200x200px로 매우 크게** 설정
- `font-size: 32px`: 텍스트도 크게 (일반 웹은 14~16px)
- `background-color: #00cc66`: 초록색 (신호등의 초록색과 같이 "진행" "안전"을 의미)
- `onclick="showRidingScreen()"`: 버튼 클릭 시 JavaScript 함수 실행 → 탑승 중 화면으로 전환
- `display: none`: 기본적으로 탑승 중 화면은 숨겨짐 (홈 화면만 표시)

이 코드를 Claude Code에 붙여넣으면, 실시간 프리뷰에서 **실제로 클릭 가능한 앱**처럼 작동합니다.

## 함정·실수

### 1. 디자인 시스템 없이 시작하기

**문제**:
- "홈 화면 만들어"라고만 하면 AI가 임의로 스타일 정함
- 첫 번째 생성: 파란색 버튼, 세리프 폰트
- 두 번째 생성: 빨간색 버튼, 산세리프 폰트
- 세 번째 생성: 초록색 버튼, 다른 폰트
- **일관성 없음** → 팀이 혼란

**해결**:
- 항상 디자인 시스템을 **먼저 세팅**하고 시작
- 프롬프트에 "[선택한 디자인 시스템]을 사용하여"라고 명시

### 2. 너무 짧은 프롬프트

**문제**:
```
❌ "택시 앱 UI 만들어"
→ AI가 Uber나 Grab처럼 일반적인 택시 앱 만듦
→ 시니어 정서, 자녀 연동 기능 전혀 반영 안 됨
```

**해결**:
```
✅ "시니어 사용자(65세 이상)를 위한 택시 앱.
    - 시각 약화 고려, 텍스트 최소 16px
    - 복잡한 메뉴 제거 ("탑승하기" 1개 버튼 강조)
    - 자녀와의 실시간 위치 공유 기능
    - 도착 시 자녀에게 자동 알림
    
    필요한 화면: 홈, 탑승 중, 자녀 알림, 도착 확인"
```

### 3. 폰트와 아이콘 누락

**문제**:
- Material Design 키트를 업로드했는데 Claude Design에서 "missing font" 표시됨
- 폰트가 정의되지 않아 기본 서체 사용
- 아이콘도 일반 텍스트로 표시됨

**해결**:
- Google Material Design 3는 **Roboto 폰트** 사용 (설정에서 명시하기)
- 폰트 파일(.ttf, .otf)을 별도로 준비하면 더 정확함
- 현재로는 "Roboto 폰트를 사용해주세요"라고 프롬프트에 명시하면 됨
- 아이콘은 Material Icons 라이브러리의 이름으로 명시 (예: "home, search, shopping_cart")

### 4. 한국식 정서 무시

**문제**:
- Google Material Design(너무 깔끔하고 국제적)을 한국 앱에 바로 적용
- 한국 사용자가 "너무 차갑고 낯설다"고 피드백
- 토스, 당근, 오늘의집 등 한국 앱의 따뜻함 부재

**해결**:
- **Wanted 디자인 시스템** (한국 기업)을 사용하기
- Material Design 사용 시 색상, 라운드 값, 여백을 "따뜻하게" 조정하도록 프롬프트에 명시
  - 예: "한국식 정서를 반영하여 따뜻하고 친근한 톤으로"

### 5. 프로토타입 후 수정 미흡

**문제**:
- 1차 결과물이 마음에 안 드는데 "처음부터 다시 만들어야 한다"고 생각
- 시간 낭비

**해결**:
- Claude Design **내에서 직접 수정** ("버튼 색상을 파란색으로", "텍스트 크기 32px로")
- 대대적 수정이 필요하면 Claude Code로 옮겨서 코드 수정
- Iteration을 여러 번 하는 것이 정상 (완벽한 1차는 드무ㅣ 삼

### 6. 클로드 디자인과 클로드 코드 연동 실패

**문제**:
- 디자인 파일을 PNG로 저장하려고 함
- HTML 코드를 어떻게 추출하는지 몰라 헤맴

**해결**:
- Claude Design은 **이미지 export가 아님**
- 우측 상단 "Code" 버튼 → HTML/CSS/JavaScript 코드 자동 생성
- "Copy" 또는 "Download (ZIP)" 선택
- Claude Code에 직접 붙여넣기

## 베스트 프랙티스

### 1. 디자인 시스템 선택 전략

**한국 서비스**:
- ✅ **Wanted Design System** (추천)
  - 한국 토양에서 검증됨
  - 타이포그래피, 컬러가 한국식
  - 현지화 요소 풍부

**글로벌 서비스**:
- ✅ **Google Material Design 3** (추천)
  - 접근성 최고 (WCAG AAA)
  - 안드로이드/웹 모두 호환
  - 컴포넌트 풍부

**iOS 앱**:
- ✅ **Apple iOS Design System**
  - iPhone/iPad 표준
  - App Store 심사 통과 용이

**B2B 대시보드**:
- ✅ **Ant Design** (중국 오픈소스)
  - 복잡한 UI 컴포넌트 풍부
  - 관리 페이지에 최적화

### 2. PRD 작성 체크리스트

```
[ ] 제품 이름과 한 줄 설명 작성
[ ] 대상 사용자 명확히 (나이, 직업, 기술 수준)
[ ] 3~5개 핵심 기능 나열
[ ] 2~3가지 구체적 사용 시나리오 작성
[ ] 특수 디자인 요구사항 명시
    - 폰트 크기 (예: 최소 16px)
    - 색상 톤 (밝음/어두움, 따뜻함/차가움)
    - 복잡도 (간단/복잡)
    - 언어 (한국어, 영문 등)
[ ] 필요한 화면 목록 및 각 화면의 구성 요소 설명
[ ] 화면 간 상호작용 흐름 작성
[ ] 예외 상황 고려
    - 오류 상황 (네트워크 끊김 등)
    - 로딩 상태
    - 빈 상태 (데이터 없음)
```

### 3. 점진적 개선 워크플로우

**사이클**:
```
1차 생성 (전체 흐름 확인)
    ↓
2차 미세 조정 (Claude Design 내)
    ↓
3차 코드 이동 (Claude Code)
    ↓
4차 팀 피드백 (실제 사용자 테스트)
    ↓
최종 개발 (프로젝트에 통합)
```

**각 단계의 목표**:
- **1차**: 전체 구조와 흐름이 맞는가?
- **2차**: 색상, 크기, 여백이 적절한가?
- **3차**: 코드가 실행 가능하고 버그는 없는가?
- **4차**: 실제 사용자가 혼란 없이 사용할 수 있는가?

### 4. 팀 협업 시 프로세스

```
PD (기획) → PRD 작성
    ↓
Designer (디자이너) → PRD 검토 및 Claude Design에서 프로토타입 생성
    ↓
Developer (개발) → Claude Code로 실제 코드 구현
    ↓
PM (프로덕트 매니저) → 실제 사용자 테스트 및 피드백
    ↓
Designer + Developer → 피드백 반영하여 수정
```

**협업 팁**:
- PRD를 **Google Docs** 또는 **Notion**에서 팀과 함께 작성
- Claude Design 프로토타입을 **링크로 공유** (팀원이 클릭해보도록)
- 피드백은 **구체적으로** ("이상해요" X, "버튼이 너무 작아서 누르기 힘들어요" O)

### 5. 성능 최적화

**프롬프트에 명시하기**:
```
"다음 프로토타입을 만들어주세요:
- 먼저 간단한 버전부터 시작
- 점진적으로 기능 추가
- 불필요한 애니메이션은 제외
- 핵심 상호작용에만 집중"
```

**성공적인 화면 저장**:
- Claude Design에서 만든 화면 중 잘 만든 것은 프롬프트와 함께 **별도로 저장**
- 나중에 유사한 화면 제작할 때 참고 가능
- "이전 홈 화면 스타일을 참고하여..." 같이 활용

### 6. 검증 방법

**자신 검증**:
- ✅ 프로토타입을 직접 여러 번 클릭해보기
- ✅ 버튼 누르기, 화면 전환 확인
- ✅ 모바일 화면 크기로 보기 (반응형 확인)

**사용자 검증**:
- ✅ **타겟 사용자 테스트**: 시니어 앱이면 실제 60대 이상에게 보여주기
- ✅ **Think Aloud Protocol**: 사용자가 클릭하면서 생각을 말하도록 ("이 버튼이 뭐예요?" 같은 피드백 수집)
- ✅ **경쟁사 벤치마킹**: 카카오T, 당근, 네이버 지도 등과 비교

**기술 검증**:
- ✅ Claude Code에서 실제 작동하는가?
- ✅ 로딩 시간이 빠른가?
- ✅ 오류 상황에서도 작동하는가?

## 참고

### 영상에서 언급된 자료 및 링크

**Figma 커뮤니티** (UI 키트 다운로드)
- https://www.figma.com/community
- 검색어: "Material Design 3", "Wanted Design System", "iOS Design System"

**Google Material Design 공식** (가이드라인)
- https://material.io
- Material Design 3 최신 가이드라인

**조쉬 (강사) 연락처**
- 뉴스레터 (1만명 이상 구독): https://maily.so/josh
- LinkedIn: https://www.linkedin.com/in/uxjosh/
- Threads: https://www.threads.com/@joshproductletter
- 프로젝트 협업: https://joshua.site

### 추가 학습 자료

**Claude Design 공식**
- Claude Design 탭: claude.ai/design (로그인 필요)
- 기본 튜토리얼: Claude Design 처음 시작할 때 제공되는 "Samples" 섹션

**Figma 가이드**
- Design Systems 구축: https://help.figma.com/en/articles/360045207033
- Component Variants: Figma 공식 문서

**관련 개념**
- **Design Tokens**: 색상, 크기, 폰트 같은 디자인의 기본 단위 (Figma Variables로 관리 가능)
- **Component Variants**: 한 컴포넌트의 여러 상태 (예: 버튼의 "normal", "hover", "disabled")
- **Interactive Prototyping**: 클릭, 드래그, 스와이프 같은 실제 사용자 상호작용 구현
- **Handoff**: 디자인에서 개발로의 인수인계 프로세스
- **Design QA**: 디자인이 실제로 개발과 일치하는지 확인하는 과정

### 참고할 관련 기술

- **HTML/CSS**: Claude Design에서 생성하는 코드의 기초 (프롬프트 단계에서는 몰라도 됨)
- **JavaScript**: 상호작용(클릭, 애니메이션) 구현 (Claude Code에서 수정할 때)
- **Responsive Design**: 모바일, 태블릿, 데스크톱에서 모두 작동하도록 (Claude Design이 자동으로 생성)
- **Accessibility (a11y)**: 색맹, 시각 약화 등 장애인도 사용할 수 있도록 (Material Design 3가 WCAG 준수)

### 영상 내 미언급 부분 (보충)

- **Claude Design의 한계**: 매우 복잡한 데이터 시각화(복잡한 차트, 표 등)는 아직 생성이 미흡
- **팀 협업 기능**: Claude Design은 현재 개인용 주로 사용되며, 팀 협업 기능은 추가 개발 예정
- **디자인 품질**: 1~3차 정도는 AI 보조로, 최종 4~5차는 사람이 검증 권장 (완벽함을 보장하지 않음)
- **비용**: Claude API 사용량에 따라 비용 발생 (무료 트라이얼 제한 후)
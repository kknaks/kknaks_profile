# kknaks.dev — Portfolio Project Memory

> 이 파일은 새 세션이 열릴 때마다 컨텍스트를 빠르게 잡기 위한 메모입니다.
> Claude는 이 파일을 자동으로 읽습니다. 사람도 읽을 수 있게 작성.

---

## 프로젝트 한 줄 요약

**kknaks.dev** — 1년차 백엔드 엔지니어(이건학)의 개인 포트폴리오 사이트 디자인.
다크 + 모노스페이스 톤, 엔지니어링 무드. Next.js + Python(FastAPI) 백엔드로 추후 구현 예정.

## 주인 정보

- **이름**: 이건학
- **표기명**: kknaks
- **직무**: 1년차 백엔드 엔지니어 (AI 회사)
- **이메일**: kknaks@gmail.com
- **GitHub**: 추후 입력
- **위치**: 서울

## 디자인 결정 (확정)

- **랜딩 방향**: A안 — Terminal (좌측 카피 + 우측 라이브 터미널)
- **컬러**: bg-0 `#0a0b0d`, 액센트는 oklch 터미널 그린 1색
- **타입**: Inter (sans) + JetBrains Mono (mono)
- **네비게이션 5개**: About / Career / Projects / **Notes** / **Contents** (Products는 뺌 — 1년차라 회사 케이스보다 공부 노트가 차별점)
- **언어**: 한/영 토글 (기본 한국어)

## 현재 파일 구조

```
prototype.html              ← 메인 진입. 라우팅(home/about/career/projects/notes/contents)
                              서브라우트: contents/C-001 형태로 상세 진입
js/
  proto-shell.jsx           ← TopNav, PageFooter, useI18n
  proto-home.jsx            ← 랜딩 (A안 Terminal 히어로 + 5개 섹션 미리보기 — About/Career/Projects/Notes/Contents)
  proto-subpages.jsx        ← About, Career, Projects 페이지
  proto-notes.jsx           ← Notes 페이지 (포스 그래프 + 본문 패널)
  proto-contents.jsx        ← Contents 페이지 (스터디 영상+교안. 리스트/상세)
canvas.html                 ← 초기 v0.1 design canvas (참고용 보존)
```

---

## 🚧 다음 세션 — API 명세 작업

**디자인은 v0.5에서 동결.** 다음 작업은:

### Step 1. 모든 mock 데이터를 `{{...}}` 슬롯으로 교체
JSX 안에 박혀있는 한국어/영어 mock 텍스트와 데이터를 `{{namespace.field}}` 형태의 슬롯으로 바꾼다.
이 슬롯 모음이 곧 백엔드가 내려줘야 할 필드 명세.

### Step 2. i18n 정책 — A안 (확정)
- **슬롯은 단일 키만 쓴다.** 예: `{{user.intro}}`
- **백엔드가 `?lang=ko` / `?lang=en` 쿼리 파라미터를 받아서 해당 언어 값을 내려준다.**
- 슬롯에는 `.ko` / `.en` 접미사 붙이지 않는다 — 프론트는 lang 상태만 들고 서버에 요청.
- DB 스키마에는 양쪽 다 저장 (예: `intro_ko`, `intro_en` 컬럼) 하지만 API 응답은 lang에 따라 하나만.

### Step 3. 슬롯 → API 명세로 변환
모든 슬롯을 모아 엔드포인트별 응답 스키마로 정리:
- `GET /api/me?lang=ko` → About + Hero
- `GET /api/career?lang=ko`
- `GET /api/projects?lang=ko`
- `GET /api/notes/graph` (텍스트 거의 없음)
- `GET /api/notes/{id}?lang=ko`
- `GET /api/notes/search?q=...&lang=ko`
- `GET /api/contents?lang=ko` (리스트)
- `GET /api/contents/{id}?lang=ko` (상세)

### 슬롯 네이밍 규칙 (제안 — 새 세션에서 확정)
```
{{user.name}}            {{user.role}}            {{user.location}}
{{user.email}}           {{user.github}}          {{user.tagline}}
{{user.intro}}           {{user.stack[]}}         {{user.notesCount}}
{{user.cards[].title}}   {{user.cards[].body}}

{{career[].period}}      {{career[].title}}       {{career[].org}}
{{career[].bullets[]}}

{{projects[].title}}     {{projects[].summary}}   {{projects[].stack[]}}
{{projects[].status}}    {{projects[].links}}

{{notes.graph.nodes[]}}  {{notes.graph.edges[]}}
{{notes[].title}}        {{notes[].body}}         {{notes[].tags[]}}
{{notes[].backlinks[]}}

{{contents[].id}}        {{contents[].date}}      {{contents[].day}}
{{contents[].title}}     {{contents[].youtubeId}} {{contents[].duration}}
{{contents[].concept}}   {{contents[].application}}
```

> **주의**: 랜딩 터미널 출력(`whoami`, `cat stack.txt` 등)은 슬롯화하지 않고 프론트에 박아둠 — 데모용 연출이라 서버에서 내려줄 필요 없음.

---

## 페이지별 상태 (mock 데이터로 채워져 있음)

### About — 채워둠
- 88px 원형 자리(이모지/아바타 미정)
- "호기심으로 시작해서, 도전으로 만들고, 개발로 풀어냅니다" 카피
- 4개 카드: 지금 일하는 곳 / 만들고 있는 것 / 관심 있는 기술 / 일하는 방식
- 사이드바: email / github / role / location + stack 박스

### Career — 1년차 컨텍스트로 mock 채움
- 2025.06 — present · Backend @ Stealth AI Co. (RAG/임베딩)
- 2025.01 — 05 · SSAFY 12기 백엔드 부트캠프 (가계부 우수상)
- 2024.07 — 12 · 독학 (CS 기초 + 토이 5개)
- — 2024.06 · 비전공 학사 졸업

### Projects — 6개 mock
Homelab Console / Vault Sync / Receipt OCR / Daily Standup Bot / algoboard / Tide(부트캠프)

### Notes — 옵시디언 스타일 그래프 (핵심 차별점)
- **메인**: 포스-디렉티드 그래프. 18개 노드, 5개 클러스터(AI/Python/Infra/CS/Daily)
- **인터랙션**: 노드 클릭 → 그래프가 좌측으로 줄어들고 우측에 본문 패널 슬라이드 인
- **본문**: 마크다운 + `[[위키링크]]` 클릭 시 다른 노트로 점프
- **부가**: ESC로 닫기, 검색(제목/태그), 백링크 자동 표시
- 모든 노트 mock 본문 채워둠

### Contents — 매일 업로드 스터디 로그
- 5개 회차 mock (Day 01~05)
- 영상(YouTube placeholder) + 교안(개념/적용예시 2단)
- 랜딩 05 섹션에서 최신 1개 카드 + 최근 4개 리스트 미리보기

---

## 작업 톤

- 1년차 백엔드 + AI 회사 + 홈서버 셀프호스팅 컨텍스트 유지
- 데이터 슬롯, 추상적 통계, AI 슬롭 피하기
- 실제 정보 받기 전엔 자연스러운 한국 컨텍스트의 mock으로 채움
- 각 페이지는 같은 헤더 패턴(`56px 80px 32px` + `01/02/03/04/05` 인덱스 + 큰 제목) 공유

## v0.x 진행 상황

- ✅ v0.1 — design canvas (컴포넌트, 랜딩 4안, 서브페이지 시안)
- ✅ v0.2 — A안 풀 페이지 클릭 가능 프로토타입
- ✅ v0.3 — 실제 mock 데이터로 채우기
- ✅ v0.4 — 5개 섹션 헤더 영어 고정 + 05 Contents 페이지 신규 추가
- ✅ v0.5 — 모바일 대응(햄버거 메뉴 + 1단 스택) + 랜딩에 05 Contents 미리보기 섹션 추가
- ⬜ **v1.0-pre — 모든 mock을 `{{slot}}`으로 교체 → API 명세 도출** ← 다음 세션

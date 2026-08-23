---
type: concept
id: npm
title: npm · Vite (자바스크립트 쪽 빌드 도구)
aliases:
  - npm
  - Node.js
  - Vite
  - package.json
up:
  - 2025-01-03-Day04_2
tags:
  - javascript
  - 빌드
  - 도구
---

# npm · Vite (자바스크립트 쪽 빌드 도구)

**브라우저에서 도는 코드를 만들기 위한 도구가 서버(Node.js) 위에서 돈다.** 의존성을 내려받고, 개발 서버를 띄우고, 배포용 파일을 만드는 일을 명령 몇 개가 맡는다.

## 정의

```bash
npm create vite@latest    # 프로젝트 뼈대 만들기 (템플릿을 고른다)
npm install               # package.json 에 적힌 의존성 내려받기
npm run dev               # 개발 서버 띄우기
```

- **Node.js** — 자바스크립트를 브라우저 밖에서 실행하는 런타임. **도구들이 여기서 돈다**
- **npm** — 의존성을 내려받고 스크립트를 실행하는 관리자
- **Vite** — 뼈대를 만들어 주고 개발 서버·번들링을 맡는 도구

`npm create vite@latest` 는 **무엇을 만들지 물어본다** — 프로젝트 이름, 패키지 이름, 프레임워크(React 등), 변형(JavaScript/TypeScript).

[[gradle]] 과 역할이 겹친다.

| | 자바 | 자바스크립트 |
|---|---|---|
| 선언 파일 | `build.gradle` | `package.json` |
| 의존성 받기 | `gradle build` 가 겸함 | `npm install` |
| 실행 | `bootRun` 등 | `npm run <스크립트>` |
| 결과물 | JAR/WAR | 번들된 정적 파일 |

## 왜 중요한가

**프런트엔드가 「HTML 파일을 열면 되는 것」이 아니게 된 이유가 여기 있다.** 브라우저는 `.jsx` 를 모르고 모듈 시스템도 옛 브라우저에서는 안 돌므로, **누군가 변환해 줘야 한다** — 그 변환기가 Node.js 위에서 돈다 → [[script-loading]] · [[compilation]]

**그리고 서버와 화면이 다른 도구·다른 저장소로 갈린다.** REST 로 넘어오면서 서버는 데이터만 주고 화면은 따로 빌드되므로, **배포도 실행도 둘이 된다** → [[rest-api]] · [[web-application-deployment]]

## 경계와 오해

- **`npm run dev` 로 뜨는 것은 개발용 서버다** — 파일이 바뀌면 바로 반영되도록 만들어진 것이라, **배포에는 빌드 결과물(정적 파일)을 쓴다.** 둘을 같은 것으로 알면 배포에서 막힌다
- **Node.js 가 필요하다고 서버가 Node 인 것은 아니다** — 여기서는 **빌드 도구를 돌리기 위해서만** 쓴다. 완성된 결과물은 그냥 HTML·CSS·JS 파일이다
- **`package.json` 은 선언이고 실제 버전은 잠금 파일이 정한다** — `^4.0` 같은 범위 표기 때문에 **같은 선언으로도 다른 버전이 깔린다.** 잠금 파일(`package-lock.json`)을 저장소에 넣는 이유가 그것이다 → [[gradle]]
- **`node_modules` 는 크고, 저장소에 넣지 않는다** — 선언에서 다시 만들 수 있는 것이라 결과물 취급이다 → [[git]]
- **`npm create ...@latest` 는 실행 시점마다 다른 것을 받는다** — 편하지만 **재현되지 않는다.** 오늘 만든 뼈대와 반년 뒤 만든 뼈대가 다르다

## 함께 보는 개념

- [[gradle]] · [[build]] — 자바 쪽의 같은 자리
- [[script-loading]] — 결과물이 브라우저에서 실행되는 방식
- [[rest-api]] — 서버와 화면이 갈리는 계기
- [[web-application-deployment]] — 배포 대상이 둘이 되는 축
- [[javascript-type]] — 그 코드가 쓰는 언어
- [[git]] — 무엇을 넣고 무엇을 뺄지의 문제

## 출처

- [[2025-01-03-Day04_2]] — 「프로젝트 세팅」 절이 **세 명령과 네 번의 선택**을 그대로 남겼다 — `npm create vite@latest` 가 묻는 Project name(`.` 으로 현재 디렉토리)·Package name·framework(React)·variant(JavaScript), 그리고 `npm install` → `npm run dev`. 이어 `App.jsx` 를 `return <>Hello world</>` 한 줄로 줄여 **컴포넌트가 JSX 를 돌려주는 함수**라는 최소 모양을 보인다. 다만 「TODO List 구조」 절부터는 제목만 있고 비어 있어, 리액트 자체는 이 노트에서 시작만 한다

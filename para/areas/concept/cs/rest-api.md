---
type: concept
id: rest-api
title: REST API
aliases:
  - REST
  - RESTful
  - REST API
  - 리소스 중심 URL
up:
  - 2025-01-03-Day04
  - 2025-01-03-Day04_1
tags:
  - web
  - api
  - 설계
---

# REST API

**URL 은 「무엇」을 가리키고, 「무엇을 할지」는 HTTP 메서드가 말한다.** 행위를 주소에 적던 것을 메서드로 옮기는 것이 이 방식의 전부에 가깝다.

## 정의

| | 기존 방식 | REST |
|---|---|---|
| 쓰는 메서드 | GET·POST 둘 | GET·POST·PUT·PATCH·DELETE |
| 행위를 적는 곳 | **URL** (`/write`·`/modify`·`/delete`) | **메서드** |
| URL 구조 | 행위 중심 (`/article/1/modify`) | **리소스 중심** (`/articles/1`) |
| 폼 | `GET /write` 로 폼을 주고 `POST /write` 로 처리 | **폼 엔드포인트가 없다** — 데이터만 오간다 |
| 목적 | 브라우저에서 사람이 직접 접근 | **시스템 간 통신** |

```
[기존]  GET  /article/write         폼 화면
        POST /article/write         등록 처리
        GET  /article/1/modify      수정 폼
        GET  /article/1/delete      삭제

[REST]  POST   /articles            등록
        GET    /articles            전체 조회
        GET    /articles/1          하나 조회
        PUT    /articles/1          수정
        DELETE /articles/1          삭제
```

**같은 URL 에 메서드만 바꿔 여러 일을 한다** → [[http-method]] · [[url]]

## 왜 중요한가

**화면을 서버가 그리지 않게 되면서 필요해진 방식이다.** 서버가 JSP·Thymeleaf 로 HTML 을 만들어 보낼 때는 「폼을 주는 요청」과 「처리하는 요청」이 둘 다 필요했다. 화면을 브라우저(React 등)가 그리면 **서버가 줄 것은 데이터뿐**이고, 그러면 폼 엔드포인트가 사라진다 → [[template-engine]] · [[json]]

**그리고 규칙이 문서를 대신한다.** `/articles/1` 에 `DELETE` 를 보내면 무슨 일이 일어날지 설명이 없어도 안다 — **약속을 공유하는 만큼 설명이 줄어든다** → [[response-body]]

## 경계와 오해

- **PUT 과 PATCH 가 필기에 뒤바뀌어 적혀 있다** — 표준은 **PUT 이 전체 교체, PATCH 가 부분 수정**이다. 필기는 「PUT : 수정(일부 수정) / PATCH : 수정(모든 데이터 수정)」으로 반대로 적었다. 실질적 차이는 **안 보낸 필드를 어떻게 할 것인가**다 — PUT 은 없는 것으로 보고 비우는 것이 원칙이고, PATCH 는 그대로 둔다 → [[http-method]]
- **GET 으로 삭제하면 안 된다** — 기존 방식의 `GET /article/1/delete` 가 위험한 이유는 취향이 아니라 **GET 이 안전한 메서드라는 약속** 때문이다. 브라우저·크롤러·프리페치가 마음대로 부를 수 있고, 실제로 그렇게 데이터가 지워진 사고가 있다
- **URL 에 동사가 없다고 REST 가 되는 것은 아니다** — 상태 코드·표현 형식·캐시 같은 것이 함께 따라야 하고, 원래 정의는 훨씬 넓다. **실무에서 REST 라 부르는 것은 대개 이 표 정도까지**이고, 그것을 알고 쓰면 된다
- **복수형 명사는 관례이지 규칙이 아니다** — `/articles` 가 흔하지만 강제되지 않는다. **팀 안에서 일관된 것**이 규칙 자체보다 중요하다
- **상태 코드를 안 쓰면 절반만 REST 다** — 성공에 200, 생성에 201, 없는 것에 404 를 돌려주는 것까지가 한 벌이다. 본문에 `{"success": false}` 만 넣고 전부 200 을 주면 **약속의 절반을 버린 것**이다 → [[response-body]]
- **브라우저는 PUT·DELETE 폼을 못 보낸다** — HTML `<form>` 은 GET·POST 만 지원한다. 그래서 REST 는 **자바스크립트로 요청을 만드는 환경**을 전제한다 → [[html-form]]

## 함께 보는 개념

- [[http-method]] — 행위를 옮겨 담는 곳
- [[url]] — 리소스를 가리키는 이름
- [[response-body]] — 데이터만 돌려주는 자리
- [[json]] — 그 데이터의 형식
- [[template-engine]] — 서버가 화면을 그리던 반대편
- [[request-mapping]] — 스프링에서 이 규칙을 적는 표식
- [[html-form]] — 메서드가 둘뿐인 제약의 출처
- [[dto]] — 주고받을 모양을 따로 정의하는 것
- [[api-response-envelope]] — 응답 껍데기를 통일하는 선택
- [[api-documentation]] — 계약을 문서로 뽑는 자리

## 출처

- [[2025-01-03-Day04_1]] — 같은 날. **표로 배운 것을 그대로 만들어 본다** — `GET/POST /articles`, `GET/PUT/PATCH/DELETE /articles/1` 로 요청 체계를 먼저 적고 `@RestController` + `@RequestMapping("/api/v1/articles")` 로 구현한다. 경로에 **버전(`/api/v1`)** 이 붙는 것이 이 회차에서 처음 나오는데, 계약이 바뀔 때를 대비한 관례다. 다만 요청 체계 목록에서도 **PATCH 를 「전체」, PUT 을 「부분」**으로 적어 앞 노트의 뒤바뀜이 그대로 이어진다 → [[dto]] · [[api-response-envelope]]
- [[2025-01-03-Day04]] — 「REST API」 절이 정의를 **한 줄로 압축**했다: 「행위를 HTTP 매서드로 구분」. 그리고 「SSR방식과 REST API의 차이」 표가 다섯 축(HTTP 메서드 · 행위를 적는 곳 · URL 구조 · 용도 · 목적)으로 둘을 대비하는데, 특히 **「별도의 폼 엔드포인트 없이 데이터만 처리」**와 **「행위중심의 구조 ↔ 리소스 중심의 구조」**가 이 방식이 바꾸는 것을 정확히 짚었다. 앞 회차들의 `/board/list`·`/board/add` 같은 주소가 왜 그런 모양이었는지, 그리고 왜 바뀌는지가 이 표 하나로 설명된다. 다만 메서드 설명에서 **PUT 과 PATCH 의 뜻이 서로 바뀌어** 적혀 있고, 상태 코드는 다루지 않는다

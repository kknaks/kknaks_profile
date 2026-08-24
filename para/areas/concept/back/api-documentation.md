---
type: concept
id: api-documentation
title: API 문서 자동화 (Swagger · OpenAPI)
aliases:
  - Swagger
  - OpenAPI
  - springdoc
  - API 문서
up:
  - 2025-01-03-Day04_1
tags:
  - api
  - 도구
  - 문서
---

# API 문서 자동화 (Swagger · OpenAPI)

**코드에서 API 명세를 뽑아 문서와 시험 화면을 자동으로 만드는 것.** 문서를 따로 쓰는 대신 **코드에 표식을 달아 둔다.**

## 정의

의존성 하나로 시작한다.

```groovy
implementation 'org.springdoc:springdoc-openapi-starter-webmvc-ui:2.1.0'
```

문서에 넣을 설명은 애노테이션으로 붙인다.

```java
@RestController
@RequestMapping(value = "/api/v1/articles",
                produces = APPLICATION_JSON_VALUE,
                consumes = APPLICATION_JSON_VALUE)
@Tag(name = "ApiV1ArticleController", description = "게시글 CRUD API")
public class ApiV1ArticleController {

    @Operation(summary = "게시글 다건 조회")
    @GetMapping
    public RsData<List<ArticleDto>> list() { ... }
}
```

| 표식 | 문서에서 |
|---|---|
| `@Tag(name, description)` | **클래스 단위** 묶음의 제목과 설명 |
| `@Operation(summary)` | **메서드 단위** 설명 |
| `produces` · `consumes` | 응답·요청의 Content-Type → [[request-mapping]] |

**이미 코드에 있는 것(경로·메서드·파라미터 타입·반환 타입)은 읽어서 채운다** — 사람이 적는 것은 「무엇을 하는지」뿐이다.

## 왜 중요한가

**문서가 코드와 어긋나지 않는다.** 따로 쓴 문서는 코드가 바뀌면 낡고, 낡은 문서는 **없는 것보다 나쁘다.** 코드에서 뽑으면 경로·타입은 언제나 맞는다 → [[refactoring]]

**그리고 프런트와의 계약이 눈에 보인다.** REST 로 넘어오면서 화면과 서버가 나뉘었으므로, **무엇을 보내면 무엇이 오는지**를 공유할 자리가 필요해졌다 — Swagger UI 는 그 자리를 **바로 호출해 볼 수 있는 화면**으로 준다 → [[rest-api]] · [[dto]]

## 경계와 오해

- **자동으로 채워지는 것과 사람이 적어야 하는 것이 갈린다** — 경로·타입은 자동이지만 **「이 필드가 무슨 뜻인지」·「언제 실패하는지」는 아무도 안 적어 준다.** 표식만 붙이고 설명을 안 쓰면 **목록만 있는 문서**가 된다
- **`consumes = APPLICATION_JSON_VALUE` 를 클래스 전체에 걸면 GET 도 걸린다** — 본문이 없는 요청에 Content-Type 을 요구하게 되어 **매핑이 안 잡히는** 일이 생긴다. 필기의 설정이 그 모양이다 → [[request-mapping]]
- **문서 화면을 운영에 열어 두면 안 된다** — 모든 엔드포인트와 파라미터가 공개된다. **개발·스테이징에서만 켜는 설정**이 따로 필요하다 → [[externalized-configuration]]
- **DTO 가 곧 문서다** — 요청·응답 모양이 DTO 클래스에서 나오므로, 엔티티를 그대로 내보내면 **문서에도 내부 구조가 그대로 실린다** → [[dto]]
- **Swagger 는 명세의 한 구현이다** — 표준은 OpenAPI 이고, 그 명세를 JSON/YAML 로 뽑으면 클라이언트 코드 생성이나 계약 시험에 쓸 수 있다. **화면이 목적의 전부는 아니다** → [[json]]

## 함께 보는 개념

- [[rest-api]] — 문서화 대상이 되는 계약
- [[dto]] — 요청·응답 모양의 출처
- [[request-mapping]] — `produces`·`consumes` 가 붙는 자리
- [[annotation]] — 코드에 설명을 다는 장치
- [[api-response-envelope]] — 응답 모양이 하나로 고정되는 것과의 짝
- [[spring-boot]] — 스타터로 붙이는 환경

## 출처

- [[2025-01-03-Day04_1]] — 「스웨거 도입」 절이 **붙이는 순서 그대로** 적혔다 — `build.gradle` 의존성 한 줄, `@RequestMapping` 에 `produces`/`consumes` 추가(각각 「응답의 Content-Type」·「받아들일 수 있는 요청의 Content-Type」으로 설명), 클래스에 `@Tag(name, description)`, 메서드에 `@Operation(summary)`. **문서의 제목·설명이 어느 단위에 붙는지**(클래스 ↔ 메서드)를 갈라 적은 것이 이 절의 요점이고, 생성된 화면 스크린샷이 결과로 붙어 있다. 다만 `consumes` 를 클래스 전체에 거는 것의 부작용, 운영 환경에서 문서를 여는 문제는 다루지 않았다

---
type: concept
id: http-message
title: HTTP 메시지 (요청 줄·상태 줄·헤더·본문)
aliases:
  - HTTP 메시지
  - HTTP message
  - 요청 줄
  - request line
  - 상태 줄
  - status line
  - HTTP 헤더
up:
  - 2024-09-04-Day69
tags:
  - web
  - 프로토콜
  - 메시지
  - 헤더
---

# HTTP 메시지 (요청 줄·상태 줄·헤더·본문)

HTTP 요청과 응답이 선 위로 오갈 때의 형식. 시작 줄이 메시지의 종류와 결과를, 헤더가 처리 규칙을, 본문이 실제 전송할 내용을 맡는다 → [[network-protocol]] · [[request-response]]

## 정의

요청과 응답은 같은 네 구획을 공유하지만 시작 줄의 질문이 다르다.

| 구획 | 요청 | 응답 |
|---|---|---|
| 시작 줄 | 메서드 · 대상 URL · HTTP 버전 | HTTP 버전 · 상태 코드 · 상태 문구 |
| 헤더 | 클라이언트가 보낼 조건·능력 | 서버가 보낸 결과의 성질·처리 지시 |
| 빈 줄 | 헤더의 끝 | 헤더의 끝 |
| 본문 | 보낼 데이터가 있을 때 | 돌려줄 표현이 있을 때 |

```http
POST /members HTTP/1.1
Host: example.test
Content-Type: application/json

{"name":"Kim"}
```

`Content-Type`은 본문을 **어떻게 해석할지** 알려 주고, `Content-Length`는 바이트 길이를 알린다. `Accept`·`Accept-Language`·`Accept-Encoding`은 요청자가 받을 수 있는 표현을 말하며, 응답의 `Content-Type`·`Content-Encoding`은 실제로 보낸 표현을 말한다.

## 왜 중요한가

**본문만 읽으면 데이터의 뜻을 잃고, 헤더만 읽으면 데이터 자체가 없다.** 예를 들어 같은 바이트열도 `Content-Type: text/html; charset=UTF-8`이면 문서·문자셋으로 해석하고, `application/json`이면 JSON으로 해석한다. 이 규약을 컨테이너가 먼저 파싱하므로 서블릿에서는 [[request-parameter]]와 `getPart()` 같은 API로 접근할 수 있다.

상태 코드는 본문 속 오류 문장보다 먼저 **요청의 성공·실패를 기계에 알린다.** `200 OK` 본문에 "오류 발생"을 적는 것과 4xx/5xx 상태로 실패를 보내는 것은 모니터링·캐시·재시도에서 전혀 다르게 취급된다 → [[exception-handling]] · [[request-response]]

## 경계와 오해

- **헤더 ≠ 본문** — 헤더는 본문에 대한 규칙과 협상 정보를 담고, 본문은 실제 표현을 담는다. `Content-Type`을 데이터 자체로 여기면 왜 바이트열을 별도로 읽어야 하는지 설명되지 않는다.
- **Payload ≠ HTTP 본문 전체** — 일상적으로 본문을 payload라고 부르지만, 엄밀히는 전달하려는 의미 있는 내용이다. 헤더·상태 줄은 payload가 아니며, 본문이 비어도 메시지는 완전할 수 있다. Day69의 "HEAD 요청은 응답 본문이 없지만 헤더는 포함"은 이 구분을 보여 준다.
- **General·Entity 헤더라는 분류 ≠ 현재 HTTP의 완전한 분류** — Day69은 HTTP/1.1 시대의 표현으로 `Date`·`Cache-Control`·`Content-*`를 나눠 소개한다. 현대 명세는 그 낡은 범주 대신 각 필드의 의미를 정의한다. 그래서 `Content-Type`이 요청과 응답 양쪽에 나타나는 사실을 "어느 한 범주만의 헤더"로 외우면 틀린다.
- **`Cache-Control: no-cache` ≠ 저장 금지** — 캐시를 전혀 저장하지 못하게 하는 것은 `no-store`이고, `no-cache`는 저장할 수는 있지만 재사용 전에 원 서버에 유효성을 확인하라는 뜻이다. 이름이 비슷해서 "캐시를 안 한다"로 읽기 쉽다.
- **`Content-MD5` ≠ 전송 보안·현대의 무결성 보장** — Day69이 무결성 예로 들지만 이 필드는 더는 HTTP에서 권장되는 일반 검증 수단이 아니다. HTTPS는 전송 중 보호를 맡고, 콘텐츠 검증은 별도 무결성 메커니즘이 맡는다.

## 함께 보는 개념

- [[network-protocol]] — 메시지 형식을 미리 합의하는 상위 규칙
- [[request-response]] — 컨테이너가 이 메시지를 객체로 바꿔 넘기는 자리
- [[http-method]] — 요청 줄의 메서드가 뜻하는 작업
- [[character-encoding]] — `Content-Type`의 `charset`이 정하는 문자 해석
- [[url]] — 요청 줄의 대상과 쿼리 문자열
- [[multipart-form-data]] — 본문을 여러 파트로 나누는 표현

## 출처

- [[2024-09-04-Day69]] — 요청 줄·상태 줄·헤더·본문의 구조를 먼저 세우고, General·Entity·Request·Response 헤더별로 `Cache-Control`·`Content-Type`·`Accept`·`Location` 등 예를 넓게 모았다. `Payload vs. Body` 절이 둘의 구분을 묻는 빈자리를 남겼고, `no-cache`·`Content-MD5`·낡은 헤더 분류의 범위는 교정이 필요하다.

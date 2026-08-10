---
type: concept
id: api-response-envelope
title: 응답 봉투 (RsData 같은 공통 응답 형식)
aliases:
  - RsData
  - 공통 응답
  - 응답 봉투
  - response envelope
up:
  - 2025-01-03-Day04_1
tags:
  - api
  - 설계
  - web
---

# 응답 봉투 (RsData 같은 공통 응답 형식)

**모든 API 응답을 같은 껍데기로 감싸는 것.** 실제 데이터를 `data` 에 넣고, 결과 코드와 메시지를 함께 담아 **응답의 모양을 하나로 고정한다.**

## 정의

```java
@Getter @Setter @AllArgsConstructor
public class RsData<T> {
    private String resultCode;
    private String msg;
    private T data;

    public static <T> RsData<T> of(String resultCode, String msg, T data) {
        return new RsData<>(resultCode, msg, data);
    }
    public static <T> RsData<T> of(String resultCode, String msg) {
        return of(resultCode, msg, null);
    }

    @JsonIgnore public boolean isSuccess() { return resultCode.startsWith("200"); }
    @JsonIgnore public boolean isFail()    { return !isSuccess(); }
}
```

세 조각이 각각 일을 한다.

- **제네릭 `T`** — 안에 담는 것은 무엇이든 된다. 목록이든 단건이든 같은 껍데기 → [[generics]]
- **정적 팩토리 `of`** — 데이터가 있는 응답과 없는 응답을 **오버로딩으로** 갈랐다 → [[method]]
- **`@JsonIgnore`** — `isSuccess()` 는 **서버 안에서 쓰는 판단**이라 JSON 에 나가면 안 된다 → [[json]]

```json
{ "resultCode": "200-1", "msg": "성공", "data": { "id": 1, "title": "..." } }
```

## 왜 중요한가

**클라이언트가 응답을 푸는 코드를 한 번만 쓰면 된다.** 어떤 API 든 `resultCode` 를 보고 `data` 를 꺼내므로, **성공·실패 분기가 한 곳**에 모인다.

**그리고 HTTP 상태 코드만으로 부족한 것을 담는다.** 「실패했다」는 404·400 으로 말할 수 있지만 **「왜」는 못 말한다.** 자체 코드(`200-1`·`400-3`)와 메시지가 그 자리를 채운다 → [[response-body]]

## 경계와 오해

- **HTTP 상태 코드를 대체하면 안 된다** — 전부 200 으로 내려보내고 봉투 안에서만 성공·실패를 말하면, **HTTP 를 이해하는 도구들이 전부 무력해진다** — 브라우저·프록시·모니터링·재시도 로직이 다 200 만 본다. **봉투는 상태 코드를 보완하는 것이지 대신하는 것이 아니다** → [[rest-api]] · [[http-message]]
- **`resultCode.startsWith("200")` 은 문자열 판정이다** — 코드 체계가 문자열이라 **오타가 조용히 실패**로 이어진다. 상수나 enum 으로 두면 컴파일러가 잡는다 → [[type-alias]]
- **봉투가 있으면 응답이 한 겹 깊어진다** — 클라이언트가 매번 `res.data.xxx` 를 써야 하고, 타입 정의도 한 겹 늘어난다. **일관성의 대가**다
- **`@JsonIgnore` 를 빼먹으면 내부 판단이 노출된다** — `isSuccess()` 가 getter 로 보여 `success: true` 가 응답에 섞인다. **의도하지 않은 필드가 계약이 되는** 흔한 자리다 → [[dto]]
- **예외 처리와 이어 두지 않으면 반쪽이다** — 정상 흐름만 봉투에 담고 예외는 스프링 기본 오류 형식으로 나가면, **응답 모양이 두 가지**가 된다. 전역 예외 처리에서도 같은 봉투로 감싸야 한다 → [[exception-handler]]

## 함께 보는 개념

- [[dto]] — 봉투 안에 담기는 것
- [[response-body]] — 봉투가 실려 나가는 통로
- [[rest-api]] — 상태 코드와의 역할 분담
- [[generics]] — 어떤 데이터든 담게 하는 장치
- [[json]] — 직렬화될 때의 모양
- [[exception-handler]] — 실패 응답도 같은 모양으로 만드는 자리

## 출처

- [[2025-01-03-Day04_1]] — 「RsData 클래스를 도입 - 조회」 절이 **클래스 전문**을 실었다. 제네릭 `T` 로 데이터 타입을 열어 두고, `of(...)` 를 두 벌 오버로딩해 데이터 없는 응답을 지원하며, `isSuccess()`/`isFail()` 에 **`@JsonIgnore` 를 붙여 「서버 내부에서 사용하는 값」임을 명시**한 것이 코드에 그대로 있다. 필기가 붙인 주석 두 줄(「반환값에 data 를 동적으로 관리」·「`@JsonIgnore` : JSON 데이터 변환 무시, 서버 내부에서 사용하는 값」)이 각 장치의 의도를 짚는다. 다만 `resultCode` 체계를 문자열 `\"200\"` 접두어로 판정하는 것의 위험, HTTP 상태 코드와의 역할 분담은 다루지 않았다

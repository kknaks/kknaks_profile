---
type: concept
id: jsp-scripting-element
title: JSP 스크립팅 요소 (Scripting Element)
aliases:
  - 스크립팅 요소
  - scripting element
  - 스크립틀릿
  - scriptlet
  - 템플릿 데이터
  - template data
  - 표현식 태그
  - 선언부
  - declaration element
up:
  - 2024-09-10-Day73
tags:
  - web
  - jsp
  - servlet
---

# JSP 스크립팅 요소 (Scripting Element)

JSP 파일의 각 조각이 **번역된 서블릿의 어느 자리에 놓이는지**를 정하는 문법. 네 갈래(템플릿 데이터·스크립틀릿·표현식·선언)가 있고, **셋은 `_jspService()` 안에, 하나는 그 밖에** 들어간다.

## 정의

| 요소 | 표기 | 번역 결과 | 놓이는 자리 |
|---|---|---|---|
| 템플릿 데이터 | (그냥 텍스트) | `out.write("...")` | `_jspService()` 안 |
| 스크립틀릿 | `<% %>` | 자바 코드 그대로 복사 | `_jspService()` 안 |
| 표현식 | `<%= %>` | `out.write(식)` | `_jspService()` 안 |
| 선언 | `<%! %>` | 클래스 멤버 | **`_jspService()` 밖** |

앞의 셋은 **파일에 적힌 순서대로** `_jspService()` 본문에 이어 붙는다. 그래서 JSP 파일의 위아래가 곧 실행 순서다.

선언만 규칙이 다르다 — **적힌 위치와 무관하게** 클래스 멤버가 된다. 필기의 예시가 그것을 정확히 보인다: 파일에서는 `jspInit()` → `<body>` → `interest`/`calculate()` → 인스턴스 블록 순인데, 번역된 클래스에서는 인스턴스 블록·`jspInit()`·`calculate()`·`interest` 가 전부 `_jspService()` **앞으로** 끌려 나간다.

그래서 `<body>` 안에서 `<%=calculate(100000000)%>` 를 부르는데 `calculate()` 의 선언이 파일 **아래쪽**에 있어도 된다. 스크립틀릿의 지역 변수였다면 「선언 전 사용」으로 컴파일 오류다.

## 사용 예시

선언 태그는 필드·메서드를, 스크립틀릿은 지역 변수를, 표현식은 출력을 맡는다.

```jsp
<%!
double interest = 0.025;              // 인스턴스 변수

private String calculate(long money) { // 인스턴스 메서드
  return String.format("%.2f", money + (money * interest));
}
%>
<body>
<h1>선언부(declaration element)</h1>
  100,000,000 입금 = <%=calculate(100000000)%>
</body>
```

번역하면 이렇게 갈린다.

```java
double interest = 0.025;

private String calculate(long money) {
  return String.format("%.2f", money + (money * interest));
}

protected void _jspService() {
  out.write("<body>");
  out.write("<h1>선언부(declaration element)</h1>");
  out.write("100,000,000 입금 = " + calculate(100000000));
  out.write("</body>");
}
```

## 왜 중요한가

**JSP 를 읽을 때 「이 조각이 메서드 안인가 밖인가」를 먼저 봐야 한다.** 문법이 네 개라서 어려운 게 아니라, 같은 파일 안에서 **사는 곳이 갈리기 때문**에 어렵다. `<% int i = 5; %>` 의 `i` 는 요청마다 새로 생기는 지역 변수고, `<%! double interest %>` 의 `interest` 는 인스턴스가 하나뿐인 서블릿의 필드라 **모든 요청이 공유한다** → [[variable-scope]] · [[thread]]

에러 메시지를 읽을 때도 이 매핑이 필요하다. 컴파일러가 가리키는 줄 번호는 JSP 파일이 아니라 **번역된 `.java` 의 줄 번호**다. 어느 조각이 어디로 갔는지 알아야 원래 자리를 되짚을 수 있다.

## 경계와 오해

- **표현식 ≠ 스크립틀릿의 축약** — `<%= %>` 안에는 **식**만 온다. 세미콜론을 붙이면 `out.write(name;)` 이 되어 문법 오류다. 「출력하는 스크립틀릿」이 아니라 **다른 문법**이다 → [[expression-vs-statement]]
- **선언 태그에 필드를 두면 쓰레드 안전하지 않다** — 필기의 `interest` 는 상수처럼 쓰여 문제가 없지만, 값이 바뀌는 필드라면 모든 요청이 같은 변수를 만진다. 서블릿 인스턴스가 하나라는 사실이 그대로 적용된다 → [[servlet-lifecycle]] · [[servlet-container]]
- **템플릿 데이터는 「그냥 HTML」이 아니라 출력 코드다** — 번역기가 `out.write()` 로 감싸므로, JSP 안의 빈 줄·공백도 응답 본문에 실려 나간다. 지시자의 `trimDirectiveWhitespaces` 가 이걸 줄이려는 옵션이다 → [[jsp-directive]]
- **`<%! %>` 안의 `{ }` 는 인스턴스 블록이지 메서드가 아니다** — 필기 예시의 `{ System.out.println("ex06 인스턴스 생성!"); }` 는 객체가 만들어질 때 한 번 실행된다. 생김새가 비슷해 스크립틀릿으로 착각하기 쉽다 → [[instance]]
- **스크립팅 요소는 지시자·액션 태그와 다른 갈래다** — `<%@ %>` 는 번역 방법을 지시하고, `<jsp: />` 는 실행 중 동작한다. `<% %>` 계열만 「자바 코드를 어디에 놓을까」의 문제다 → [[jsp-directive]] · [[jsp-action-tag]]

## 함께 보는 개념

- [[jsp]] — 이 요소들이 모여 이루는 기술
- [[jsp-directive]] — 번역 시점에 작용하는 다른 갈래
- [[jsp-action-tag]] — 실행 시점에 작용하는 또 다른 갈래
- [[expression-language]] — 표현식 태그를 대체하는 표기법
- [[servlet-lifecycle]] — `jspInit()`·`jspDestroy()` 가 대응하는 자리
- [[variable-scope]] — 지역 변수와 필드가 갈리는 축

## 출처

- [[2024-09-10-Day73]] — 「JSP의 구성요소」 절이 Template Data · Scriptlet · Expression element · Declaration element 를 **JSP 코드와 번역된 Java.class 를 나란히 놓아** 설명한다. 이 대조가 이 개념의 핵심이다 — 특히 선언부에서 「선언되는 위치에 상관없이 `_jspService()` 전에 삽입된다」를 명시하고, 파일 순서와 뒤바뀐 번역 결과를 그대로 보였다. 표현식에 세미콜론을 쓰지 않는 이유도 적혀 있다. 다만 선언 태그의 필드가 요청 사이에 공유된다는 것(쓰레드 문제)과, 컴파일 오류의 줄 번호가 번역된 `.java` 기준이라는 것은 다루지 않았다

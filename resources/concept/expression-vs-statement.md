---
type: concept
id: expression-vs-statement
title: 표현식과 문장 (Expression / Statement)
aliases:
  - 표현식
  - 문장
  - expression
  - statement
up:
  - 2024-06-07-Day10
tags:
  - java
  - 문법
  - 기초
---

# 표현식과 문장 (Expression / Statement)

**문장(statement)** 은 작업을 수행시키는 명령이고, **표현식(expression)** 은 작업을 수행한 뒤 **결과를 돌려주는** 문장이다.

## 정의

포함 관계다.

```plaintext
statement (문장)
 └─ expression (표현식)   ← 결과를 리턴하는 statement
```

**모든 표현식은 문장이지만, 모든 문장이 표현식은 아니다.** 값을 돌려주는지가 그 경계다.

| 코드 | 무엇인가 |
|---|---|
| `a + b` | 표현식 — 값을 돌려준다 |
| `age > 18 ? a : b` | 표현식 → [[ternary-operator]] |
| `System.out.println("x")` | 문장 — 값을 돌려주지 않는다(`void`) |
| `if (조건) { ... }` | 문장 |

## 사용 예시

이 구분이 실제로 걸리는 자리가 [[ternary-operator]] 다. 값이 필요한 자리에는 **표현식만** 올 수 있다.

```java
int age = 20;

// (age > 18) ? "성년" : "미성년";
// 결과를 받을 변수를 선언하지 않으면 문법 오류

// age > 18 ? System.out.println("성인이다.") : System.out.println("미성년자이다.");
// println 은 값을 돌려주지 않으므로 표현식이 아니다 → 문법 오류

// String str = age > 18 ? System.out.println("성인") : System.out.println("미성년");
// 결과 값이 없으니 왼편 변수 타입과 맞출 수 없다 → 문법 오류
```

세 경우 모두 원인이 하나다 — **값이 필요한 자리에 값 없는 것을 놓았다.**

## 왜 중요한가

**"여기에 이 코드를 쓸 수 있는가"를 판단하는 기준이 이것이다.** 대입의 오른쪽, 조건 연산자의 양쪽, 메서드 인자 자리에는 표현식이 와야 한다. 이 규칙을 모르면 문법 오류를 케이스별로 외우게 되는데, 알면 하나로 설명된다.

그리고 언어를 옮겨 다닐 때 차이가 드러나는 지점이다. 어떤 언어는 `if` 도 값을 돌려주는 표현식이라 `val x = if (c) a else b` 가 되는데, Java 의 `if` 는 문장이라 그렇게 쓸 수 없고 그 자리를 조건 연산자가 메운다.

## 경계와 오해

- **대입도 표현식이다** — `b = true` 가 값을 돌려주기 때문에 `a || (b = true)` 같은 코드가 성립한다 → [[short-circuit-evaluation]]
- **`void` 메서드 호출은 표현식이 아니다** — 호출 자체는 문장이지만 돌려줄 값이 없다. 이것이 위 예시들이 오류인 이유다.
- **세미콜론이 문장을 끝낸다** — 표현식만 써 두고 세미콜론을 붙이면 문장이 되지만, 결과를 아무도 받지 않으면 대개 의미가 없다. 조건 연산자를 그렇게 쓰면 Java 는 오류로 막는다.

## 함께 보는 개념

- [[ternary-operator]] — 이 구분이 실제로 걸리는 자리
- [[operator]] — 연산이 값을 돌려주는 문장이라는 것
- [[short-circuit-evaluation]] — 대입이 표현식임을 이용하는 예

## 출처

- [[2024-06-07-Day10]] — statement 중 결과를 리턴하는 것이 expression 이라는 포함 관계와, 조건 연산자를 쓸 수 없는 세 경우가 모두 이 구분 때문이라는 것을 배웠다

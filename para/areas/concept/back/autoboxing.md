---
type: concept
id: autoboxing
title: 오토박싱 · 오토언박싱 (Autoboxing)
aliases:
  - 오토박싱
  - 오토 박싱
  - 오토언박싱
  - 오토 언박싱
  - autoboxing
  - auto-boxing
  - unboxing
  - 박싱
  - 언박싱
up:
  - 2024-06-25-Day22
tags:
  - java
  - 자료형
  - 컴파일
  - 문법
---

# 오토박싱 · 오토언박싱 (Autoboxing)

기본 타입과 [[wrapper-class]] 사이의 변환을 **컴파일러가 코드에 끼워 넣어 주는** 것. 개발자는 대입만 쓰고, `valueOf` 와 `intValue()` 호출은 컴파일 결과에 들어간다.

## 정의

두 방향에 각각 이름이 붙어 있다.

| 이름 | 방향 | 컴파일러가 끼워 넣는 것 |
|---|---|---|
| **오토박싱** | 기본 타입 → 래퍼 | `Integer.valueOf(...)` |
| **오토언박싱** | 래퍼 → 기본 타입 | `.intValue()` 같은 꺼내는 메서드 |

박싱은 이렇게 생긴다.

```java
int i1 = 100;
Integer obj1 = Integer.valueOf(i1);
Integer obj2 = 100; // ==> Integer.valueOf(100)
```

언박싱은 그 반대다.

```java
Integer obj = Integer.valueOf(100);
int i2 = obj.intvalue()
int i3 = obj;  // ==> obj.intvalue()
```

**두 예제의 마지막 줄이 요점이다.** 위아래 줄이 하는 일이 같고, 아래쪽은 그것을 안 쓴 것이다. 필기가 `// ==>` 로 「컴파일하면 이렇게 된다」를 적어 둔 것이 정확한 이해다.

## 왜 중요한가

**기본 타입과 참조 타입의 경계가 코드에서 사라진다.** 두 계층은 조상도 다르고 담는 방식도 다른데, 대입 한 줄로 오갈 수 있게 되면 그 구분을 의식하지 않고 쓸 수 있다 → [[data-type]]

**그래서 경계가 드러나는 순간에만 이것의 존재를 알게 된다.** 아래 세 가지가 그 순간이고, 셋 다 **컴파일 오류가 아니라 실행 결과의 이상**으로 나타난다. 문법이 감춰 준 것이 있다는 사실을 모르면 원인을 찾을 곳이 없다.

**그리고 이것이 컴파일 시점의 일이라는 것이 중요하다.** 실행 중에 JVM 이 알아서 하는 마법이 아니라 컴파일러가 소스에 코드를 추가하는 것이므로, 비용도 컴파일된 그 코드가 그대로 낸다 → [[compilation]]

## 경계와 오해

- **필기의 `intvalue()` 는 오타다** — 실제 이름은 `intValue()` 다. `long`·`double` 은 `longValue()`·`doubleValue()` 이고, **꺼내는 메서드 이름이 타입마다 다르다.** 오토언박싱을 쓰면 이 이름을 아예 몰라도 되므로 실수가 드러날 기회도 없다.
- **`null` 을 언박싱하면 터진다** — 가장 아프게 걸리는 자리다. `Integer obj = null; int i = obj;` 는 컴파일이 되고 실행 시점에 `NullPointerException` 이 난다. **`int` 로 받는 코드에서 NPE 가 나는 것**이라 원인을 찾기 어렵다. `Integer` 는 `null` 이 될 수 있고 `int` 는 될 수 없다는 차이가 여기서만 드러난다 → [[wrapper-class]] · [[exception-handling]]
- **`==` 가 값 비교로 보이지만 아니다** — `Integer a = 1000, b = 1000; a == b` 는 `false` 다. 박싱된 두 인스턴스의 주소를 비교하기 때문이다. 그런데 `Integer a = 100, b = 100` 은 `valueOf` 가 작은 값을 재사용하므로 `true` 다. **작은 수로 테스트하면 통과하고 큰 수에서 깨진다** — 같은 회차 1.1 의 문자열 풀과 완전히 같은 함정이다 → [[string-comparison]] · [[object-equality]]
- **오토박싱은 승격과 함께 일어나지 않는다** — `int` 를 `Long` 변수에 대입할 수 없다. `int` → `long` 승격과 `long` → `Long` 박싱을 **컴파일러가 한 번에 두 단계 하지는 않는다.** 「알아서 맞춰 준다」로 읽으면 이 컴파일 오류가 설명되지 않는다 → [[type-promotion]] · [[type-casting]]
- **루프 안에서는 인스턴스가 쌓인다** — `Integer sum = 0; for (...) sum += i;` 는 한 바퀴마다 언박싱·덧셈·박싱이 일어나고 인스턴스가 하나씩 버려진다. 코드에 `valueOf` 가 안 보이니 비용도 안 보인다 → [[garbage-collection]]
- **박싱된 것은 원본과 연결되어 있지 않다** — `Integer obj = i1` 이후 `i1` 을 바꿔도 `obj` 는 그대로다. 값을 복사해 담은 것이고 참조를 만든 것이 아니다 → [[call-by-value]] · [[immutability]]

## 함께 보는 개념

- [[wrapper-class]] — 변환의 상대편
- [[data-type]] — 오토박싱이 감추는 경계
- [[compilation]] — 이 변환이 일어나는 시점
- [[type-promotion]] — 같이 일어날 것 같지만 안 되는 변환
- [[type-casting]] — 명시적으로 쓰는 쪽
- [[object-equality]] — `==` 가 어긋나는 자리
- [[string-comparison]] — 같은 구조의 함정
- [[exception-handling]] — `null` 언박싱이 남기는 것
- [[garbage-collection]] — 안 보이는 인스턴스가 쌓이는 문제

## 출처

- [[2024-06-25-Day22]] — 「컴파일 시 Wrapper 클래스가 적용된 객체에 대해서는 자동으로 객체로 변환한다」와 「컴파일 시 오토 언박싱도 수행한다」로 두 방향을 배웠다. `Integer obj2 = 100; // ==> Integer.valueOf(100)` 처럼 컴파일 결과를 주석으로 나란히 적어 둔 것이 이 회차의 설명 방식이고, 그래서 이것이 **문법 설탕**이라는 것이 코드에 남아 있다

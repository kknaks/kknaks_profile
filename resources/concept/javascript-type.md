---
type: concept
id: javascript-type
title: 자바스크립트의 값과 typeof
aliases:
  - typeof
  - 자바스크립트 타입
  - undefined
  - NaN
  - Infinity
  - 동적 타입
up:
  - 2024-10-24-Day101
tags:
  - javascript
  - 자료형
  - 언어비교
---

# 자바스크립트의 값과 typeof

**변수에 타입이 없고 값에만 타입이 있다.** 그래서 「이 값이 무엇인가」를 실행 중에 물어봐야 하고, 그 물음이 `typeof` 다.

## 정의

`typeof` 가 돌려주는 문자열이 여덟 갈래인데, **셋이 함정**이다.

| 값 | `typeof` |
|---|---|
| `"문자열"` · `'문자열'` | `"string"` — **문자와 문자열을 구분하지 않는다** |
| `100` · `3.14` · `314E-2` | `"number"` — **정수·실수를 구분하지 않는다** |
| `true` · `false` | `"boolean"` |
| `undefined` | `"undefined"` |
| **`null`** | **`"object"`** ← 함정 |
| **`NaN`** | **`"number"`** ← 함정 |
| `Infinity` · `-Infinity` | `"number"` |
| `new Object()` | `"object"` |
| `function f(){}` · `(a) => {}` | `"function"` |

**`undefined` 와 `null` 이 다른 것**이 이 언어의 특징이다.

- `undefined` — **변수는 있는데 값이 없다**
- `null` — **객체가 없다**(사람이 「없음」을 넣은 것)

`NaN` 은 「숫자가 아니다」인데 타입은 `number` 다 — **잘못된 숫자 연산의 결과도 숫자 자리에 있어야 하기 때문**이다 → [[floating-point]]

### 숫자 표기

```javascript
100          // 10진수
0x64, 0X64   // 16진수
0o144, 0O144 // 8진수 — 옛 표기 0144 는 strict 모드에서 금지
0b01100100   // 2진수

let a = 100;
a.toString(16);   // "64" — 진법을 바꿔 문자열로
```

**리터럴은 읽는 쪽, `toString(radix)` 은 쓰는 쪽**이다 → [[literal]] · [[number-parsing]]

### 검사에 쓰기

```javascript
var v = function() {};

if ("function" == typeof v) {
  console.log("함수입니다!");
}
```

## 왜 중요한가

**타입 검사가 컴파일러에서 코드로 내려온다.** 자바는 `String s = 100;` 을 컴파일러가 막지만, 여기서는 무엇이든 들어가므로 **필요할 때 내가 확인해야 한다** → [[data-type]] · [[type-casting]]

**그리고 「값이 없다」가 두 가지라는 것이 실전에서 갈린다.** 서버가 안 준 필드는 `undefined`, 서버가 `null` 로 준 필드는 `null` 이다 — **두 경우를 같이 처리하려면 그것을 알고 써야 한다** → [[json]] · [[sql-null]]

## 경계와 오해

- **`typeof null === "object"` 는 언어의 오래된 결함이다** — 「`null` 이 객체다」는 뜻이 아니라 **초기 구현의 흔적**이고, 고치면 기존 코드가 깨져서 그대로 남았다. `null` 검사는 `typeof` 가 아니라 `x === null` 로 해야 한다
- **`NaN` 은 자기 자신과 같지 않다** — `NaN === NaN` 이 `false` 다. 그래서 「숫자가 아닌지」는 비교가 아니라 `Number.isNaN(x)` 으로 확인한다. **타입이 `number` 라는 것과 겹쳐 두 번 헷갈리는 자리**다 → [[floating-point]]
- **`typeof` 는 배열을 구별하지 못한다** — 배열도 `"object"` 다. 자바의 [[instanceof-operator]] 처럼 쓸 수 있는 것이 아니다
- **숫자가 하나의 타입이라는 것이 정밀도 문제로 이어진다** — 정수와 실수를 나누지 않고 전부 부동소수점이라, 자바에서 `int` 로 안전하던 계산이 여기서는 다르게 나올 수 있다 → [[floating-point]] · [[overflow]]
- **`'문자열'` 과 `"문자열"` 이 같다는 것은 자바와 다른 지점이다** — 자바의 `'a'` 는 `char` 라 타입 자체가 다르다. **작은따옴표를 쓰던 습관이 여기서는 아무 차이도 만들지 않는다**
- **`"use strict"` 는 문법을 좁힌다** — `0144` 같은 옛 8진수 표기를 금지하는 식이다. **되던 것이 안 되게 만드는 선언**이고, 그것이 목적이다

## 함께 보는 개념

- [[data-type]] — 자바 쪽의 같은 자리
- [[literal]] — 값을 소스에 적는 표기
- [[floating-point]] — `NaN`·`Infinity` 가 나오는 근거
- [[type-casting]] — 검사 뒤에 오는 변환
- [[instanceof-operator]] — 자바에서 타입을 묻는 다른 방법
- [[script-loading]] — 이 값들이 실행되는 환경
- [[json]] — `null` 과 `undefined` 가 갈리는 실전 자리

## 출처

- [[2024-10-24-Day101]] — 「리터럴」과 「Typeof 연산자」 두 절이 **`console.log` 한 줄씩으로 값을 나열하고 그 옆에 `typeof` 결과를 주석으로 단** 형태다. 그 나열 자체가 이 개념의 내용이다 — 문자와 문자열을 구분하지 않는다는 것, 부동소수점에 `f` 를 안 붙인다는 것, `undefined`(변수는 있는데 값이 없음)와 `null`(객체가 없음)이 다르다는 것, 그리고 **「`null` 도 `object` 타입임을 기억하라! `undefined` 와 다르다!」**와 **`NaN` 의 타입이 `number`** 라는 것을 주석으로 못 박았다. 진수 표기는 `0x`·`0o`·`0b` 와 `toString(radix)` 를 짝으로 보이고, **`"use strict"` 에서 옛 8진수 표기(`0144`)가 금지된다**는 것까지 적었다. 마지막의 `if ("function" == typeof v)` 가 이 연산자를 실제로 쓰는 모양이다. 다만 `typeof null` 이 왜 `"object"` 인지, `NaN !== NaN` 인 것은 다루지 않았다

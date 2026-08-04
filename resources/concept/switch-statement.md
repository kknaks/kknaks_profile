---
type: concept
id: switch-statement
title: switch 문
aliases:
  - switch
  - switch 문
  - fall-through
  - 폴스루
up:
  - 2024-06-05-Day09
tags:
  - java
  - 제어문
  - 문법
---

# switch 문

하나의 값을 여러 `case` 와 견주어 맞는 곳부터 실행하는 조건문. 맞는 `case` 가 없으면 `default` 를 실행한다.

## 정의

```java
switch (식 또는 변수) {
    case 값1:
        // 변수가 값1에 해당하면 실행할 코드
        break;
    case 값2:
        // 변수가 값2에 해당하면 실행할 코드
    case 값3:
        // 값3에 해당하면 실행할 코드
        // case 값2 에 break 가 없어서 값2일 때도 여기까지 실행된다
        break;
    default:
        // 어느 것에도 해당하지 않을 때 실행되는 코드
}
```

**`break` 가 없으면 다음 `case` 로 흘러 내려간다.** 이것을 fall-through 라 한다. `switch` 는 "맞는 `case` 를 실행한다"가 아니라 **"맞는 `case` 로 뛰어들어 `break` 를 만날 때까지 계속한다"** 가 정확한 설명이다.

## 사용 예시

메뉴 번호로 분기한다. 각 `case` 마다 `break` 를 둬서 하나만 실행되게 한다.

```java
switch (menuNo) {
    case 1:
        System.out.println("회원");
        break;
    case 2:
        System.out.println("팀");
        break;
    case 6:
        System.out.println("종료합니다.");
        scanner.close();
        break;
    default:
        System.out.println("메뉴 번호가 옳지 않습니다.");
}
```

`default` 가 맨 끝에 있으므로 `break` 를 생략해도 된다 — 흘러 내려갈 곳이 없다.

## 왜 중요한가

**값 하나로 갈리는 분기가 `if-else` 사슬보다 읽힌다.** "이 변수를 보고 있다"가 한 줄로 드러나고, 어떤 값들을 다루는지가 나란히 보인다.

fall-through 는 **의도해서 쓰면 도구, 실수로 두면 버그**다. 여러 값을 같게 처리할 때는 `case` 를 나란히 두는 방식으로 쓰이지만, `break` 를 잊은 것과 생김새가 같아서 구분되지 않는다. 그래서 의도한 fall-through 에는 주석을 남긴다.

## 경계와 오해

- **`break` 는 `case` 를 끝내는 것이 아니라 `switch` 를 빠져나오는 것이다** — 그래서 없으면 다음 `case` 의 코드까지 실행된다. `case` 가 블록이 아니라 **뛰어들 지점(label)** 이기 때문이다.
- **`switch` 안의 `break` 와 루프의 `break` 는 대상이 다르다** — 루프 안의 `switch` 에서 `break` 를 쓰면 `switch` 만 빠져나오고 루프는 계속 돈다. 루프를 끝내려면 다른 방법이 필요하다.
- **`case` 에는 상수만 온다** — 범위나 조건식을 쓸 수 없다. 그런 분기는 `if` 로 간다.
- **`default` 는 맨 끝에 있어야 하는 것이 아니다** — 관례로 끝에 두지만 중간에 둘 수도 있고, 그 경우 `break` 가 필요하다.

## 함께 보는 개념

- [[do-while-loop]] — 분기를 감싸는 반복
- [[standard-input]] — 분기할 값을 받는 곳

## 출처

- [[2024-06-05-Day09]] — `case`·`default` 구조와, `break` 가 없으면 다음 `case` 도 실행된다는 것을 배웠다

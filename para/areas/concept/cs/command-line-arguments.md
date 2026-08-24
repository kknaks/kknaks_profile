---
type: concept
id: command-line-arguments
title: 실행 인자 (Command-line Arguments)
aliases:
  - 실행 인자
  - args
  - application argument
  - command line arguments
up:
  - 2024-05-30-Day05
tags:
  - java
  - 실행
  - cli
---

# 실행 인자 (Command-line Arguments)

프로그램을 실행할 때 밖에서 넘겨 주는 값. Java 에서는 [[main-method]] 의 `String[]` 파라미터로 들어온다.

## 정의

실행 명령 뒤에 붙인 값들이 순서대로 배열에 담긴다.

```bash
$ java Test6 하나 둘 셋
```

- 클래스 이름 뒤의 `하나`·`둘`·`셋` 이 인자다
- `args[0]`·`args[1]`·`args[2]` 로 들어온다
- 넘긴 것이 없으면 배열이 **비어 있다** (`null` 이 아니다)

**전부 `String` 이다.** 숫자를 넘겨도 문자열로 들어오므로 쓰려면 변환해야 한다.

## 사용 예시

넘어온 인자를 하나씩 출력한다.

```java
class Test6 {
    public static void main(String[] args) {
        for (String it : args) {
            System.out.println("'" + it + "'");
        }
    }
}
```

따옴표로 감싸 출력하면 **어디까지가 한 인자인지** 보인다. 공백으로 인자가 갈리기 때문에, 공백이 든 값을 하나로 넘기려면 실행할 때 따옴표로 묶어야 한다.

## 왜 중요한가

**코드를 고치지 않고 동작을 바꾸는 가장 작은 수단이다.** 파일 경로나 옵션을 소스에 박아 두면 값이 바뀔 때마다 다시 컴파일해야 하는데, 인자로 받으면 실행할 때 정한다.

그래서 [[cli]] 도구는 대부분 이 방식으로 만들어진다. `javac -encoding UTF-8 Hello.java` 에서 `-encoding` 과 파일명이 `javac` 의 실행 인자다 — 우리가 쓰는 도구도 같은 자리로 값을 받는다.

## 경계와 오해

- **인자 ≠ 파라미터** — 넘기는 쪽의 값이 인자(argument), 받는 쪽의 변수가 파라미터(parameter)다. `args` 는 파라미터이고 거기 담긴 값이 인자다.
- **`args[0]` 은 프로그램 이름이 아니다** — C 계열에서는 `argv[0]` 이 실행 파일 이름인데, Java 는 **넘긴 값부터** 0번이다. C 를 먼저 배웠으면 한 칸 어긋나게 센다.
- **비어 있는 것과 `null` 은 다르다** — 인자를 안 넘겨도 배열 자체는 있다. 그래서 `args.length` 를 먼저 확인하면 되고, `null` 검사는 필요 없다.

## 함께 보는 개념

- [[main-method]] — 인자를 받는 자리
- [[cli]] — 인자를 넘기는 방식

## 출처

- [[2024-05-30-Day05]] — 실행할 때 넘긴 값이 `String[]` 파라미터로 들어오고, for-each 로 순회해 출력하는 것을 배웠다

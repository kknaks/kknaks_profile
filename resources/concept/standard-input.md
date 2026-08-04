---
type: concept
id: standard-input
title: 표준 입력 (Standard Input)
aliases:
  - 표준 입력
  - standard input
  - System.in
  - Scanner
  - InputStream
up:
  - 2024-06-05-Day09
tags:
  - java
  - 입출력
  - cli
---

# 표준 입력 (Standard Input)

프로그램이 사용자로부터 값을 받는 기본 통로. Java 에서는 `System.in` 이고, 그대로는 **바이트**만 읽히므로 타입 있는 값으로 읽으려면 감싸야 한다.

## 정의

두 층으로 되어 있다.

| | 무엇 | 읽는 단위 |
|---|---|---|
| `java.io.InputStream` | 바이트 기반 입력 스트림을 나타내는 **추상 클래스** | 바이트 |
| `java.util.Scanner` | 표준입력·파일·문자열 등 다양한 소스에서 데이터를 읽는 클래스 | `int`·`String` 등 **타입 있는 값** |

`System.in` 이 표준 입력 스트림이고, 그것을 `Scanner` 로 감싸면 원하는 타입으로 읽을 수 있다.

```java
java.io.InputStream keyboard = System.in;                        // 바이트 통로
java.util.Scanner scanner = new java.util.Scanner(keyboard);     // 타입 있는 값으로 읽게 감싼다

int menuNo = scanner.nextInt();                                  // 숫자로 읽는다

scanner.close();                                                 // 다 쓰면 닫는다
```

`nextInt()` 는 입력을 정수로 해석해 돌려준다. 다 쓴 뒤 `close()` 로 자원을 돌려주는 것까지가 한 벌이다.

## 사용 예시

메뉴 번호를 받아 처리하는 반복 구조다.

```java
java.io.InputStream keyboard = System.in;
java.util.Scanner scanner = new java.util.Scanner(keyboard);

int menuNo;
do {
    System.out.print("> ");
    menuNo = scanner.nextInt();
    switch (menuNo) {
        case 1: System.out.println("회원"); break;
        case 6:
            System.out.println("종료합니다.");
            scanner.close();
            break;
        default: System.out.println("메뉴 번호가 옳지 않습니다.");
    }
} while (menuNo != 6);
```

→ [[do-while-loop]] · [[switch-statement]]

### Gradle 로 실행할 때는 설정이 필요하다

`gradle run` 으로 실행하면 키보드 입력이 프로그램에 닿지 않아 오류가 난다. [[gradle]] 의 `run` 태스크가 표준 입력을 넘겨주도록 `build.gradle` 에 적어야 한다.

```groovy
run {
    standardInput = System.in
}
```

## 왜 중요한가

**"바이트 통로"와 "값을 읽는 도구"가 갈려 있다는 것이 Java 입출력의 기본 구조다.** 스트림은 바이트만 알고, 그것을 문자·숫자로 해석하는 일은 감싸는 쪽이 한다. 이 구조를 알면 파일이든 네트워크든 같은 방식으로 읽힌다는 것이 이해된다 — 통로만 바뀌고 감싸는 쪽은 그대로다.

그리고 **실행 환경이 표준 입력을 넘겨주지 않으면 코드가 맞아도 동작하지 않는다.** `gradle run` 문제가 그 예다. 코드가 아니라 실행 방식을 보러 가야 하는 종류의 오류다.

## 경계와 오해

- **`Scanner` 는 키보드 전용이 아니다** — 파일·문자열도 읽는다. 무엇을 읽는지는 생성할 때 넘긴 것이 정한다. `System.in` 을 넘겼으니 키보드인 것이다.
- **`close()` 는 `Scanner` 를 닫는 것이지만 `System.in` 도 닫힌다** — 감싼 것을 닫으면 안쪽 스트림까지 닫혀서, 그 뒤에 다시 읽으려 하면 실패한다. 위 예시가 종료 직전에 닫는 이유다.
- **`nextInt()` 는 숫자가 아닌 입력에서 예외를 던진다** — 사용자가 문자를 넣으면 프로그램이 멈춘다. 실제로는 검사가 필요하다.
- **IDE 에서는 되고 `gradle run` 에서는 안 되는 일이 생긴다** — 표준 입력을 넘기는 방식이 달라서다. 같은 코드가 실행 방법에 따라 갈리는 대표적인 자리다.

## 함께 보는 개념

- [[do-while-loop]] · [[switch-statement]] — 입력을 받아 처리하는 흐름
- [[gradle]] — 실행 시 표준 입력을 넘기는 설정
- [[cli]] — 표준 입력이 오는 환경
- [[command-line-arguments]] — 실행할 때 미리 주는 값 (실행 중에 받는 것과 갈린다)

## 출처

- [[2024-06-05-Day09]] — `System.in` 을 `Scanner` 로 감싸 `nextInt()` 로 읽고 `close()` 하는 흐름, 그리고 `gradle run` 에서 `standardInput = System.in` 설정이 없으면 오류가 난다는 것을 배웠다

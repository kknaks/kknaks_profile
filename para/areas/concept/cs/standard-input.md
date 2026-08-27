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
  - nextLine
  - 입력 버퍼
  - 키보드 버퍼
up:
  - 2024-06-05-Day09
  - 2024-06-11-Day12
  - 2024-07-19-Day39
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

`System.in` 은 프로그램이 기본으로 받는 세 통로 중 하나다 → [[io-stream]]. 그것을 `Scanner` 로 감싸면 원하는 타입으로 읽을 수 있다.

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

### Scanner 는 버퍼에서 끊어 온다 — `nextLine()` 과 `next()`

키보드 입력은 곧바로 프로그램에 오지 않고 **입력 버퍼에 줄 단위로 쌓인다.** `Scanner` 는 그 버퍼에서 필요한 만큼 끊어 오는 도구이고, 무엇을 부르는지에 따라 **끊는 단위와 남기는 것**이 다르다.

| 메서드 | 읽는 범위 | 버퍼에 남는 것 |
|---|---|---|
| `nextLine()` | 다음 LF 까지 | 없음 (LF 를 먹고 버린다) |
| `next()` · `nextInt()` … | 앞쪽 공백을 건너뛰고 다음 **토큰** 하나 | 토큰 뒤의 공백과 **LF** |

세 줄을 입력하고 `nextLine()` 을 세 번 부르면 한 줄씩 그대로 들어온다.

```java
//키보드 입력
aa bb
cc
a b

//Scanner 코드
java.util.Scanner keyboardScan = new Scanner(System.in);

String s1 = keyboardScan.nextLine();   // "aa bb"
String s2 = keyboardScan.nextLine();   // "cc"
String s3 = keyboardScan.nextLine();   // "a b"
```

`nextLine()` 은 LF 까지 스캔한 뒤 **LF 를 떼고** 문자열을 만든다 → [[newline-character]]. 반대로 `next()` 류는 토큰만 가져가고 LF 를 남기므로, `nextInt()` 뒤에 `nextLine()` 을 부르면 **남아 있던 LF 만 읽고 빈 문자열이 돌아온다.** 섞어 쓰는 순간 생기는 함정이 이것이다.

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

세 번째는 **버퍼가 호출 사이에 살아 있다**는 것이다. `Scanner` 는 한 번 읽고 끝나는 도구가 아니라 "어디까지 읽었는지"를 들고 있는 인스턴스이고([[static-member]]), 그래서 앞의 호출이 남긴 것이 뒤의 호출을 망칠 수 있다. 입력 오류가 **다음 회차에** 나타나는 버그가 여기서 온다.

## 경계와 오해

- **`Scanner` 는 키보드 전용이 아니다 — 여섯 주 뒤에 그것이 코드로 확인된다** — 파일·문자열도 읽는다. 무엇을 읽는지는 생성할 때 넘긴 것이 정한다. `System.in` 을 넘겼으니 키보드인 것이다. Day39 는 같은 클래스에 `new Scanner(new FileReader("user.csv"))` 로 **파일을 넘긴다** — `nextLine()` 도 그대로다. 「통로만 바뀌고 감싸는 쪽은 그대로」가 이 노트의 논거였고 그것이 실제로 성립하는 자리다 → [[character-stream]]
- **같은 `nextLine()` 이 통로에 따라 「기다림」과 「끝」으로 갈린다** — 키보드에서는 입력이 없으면 **기다리므로** 「더 읽을 것이 없다」가 나오지 않는다. 파일에서는 끝이 있어서 `nextLine()` 이 `NoSuchElementException` 을 던진다. 그래서 Day39 의 CSV 로딩은 이 예외를 잡아 루프를 나가는데(`catch (Exception e) { break; }`), **키보드 코드에는 있을 수 없던 종료 조건**이다. 호출이 같다는 것이 성질까지 같다는 뜻은 아니고, 끝을 물으려면 `hasNextLine()` 이 있다 → [[exception-handling]] · [[csv]]
- **`close()` 는 `Scanner` 를 닫는 것이지만 `System.in` 도 닫힌다** — 감싼 것을 닫으면 안쪽 스트림까지 닫혀서, 그 뒤에 다시 읽으려 하면 실패한다. 위 예시가 종료 직전에 닫는 이유다.
- **`nextInt()` 는 숫자가 아닌 입력에서 예외를 던진다** — 사용자가 문자를 넣으면 프로그램이 멈춘다. 실제로는 검사가 필요하다.
- **IDE 에서는 되고 `gradle run` 에서는 안 되는 일이 생긴다** — 표준 입력을 넘기는 방식이 달라서다. 같은 코드가 실행 방법에 따라 갈리는 대표적인 자리다.
- **`nextLine()` 은 버퍼를 초기화하는 명령이 아니다** — 이 필기는 "Scan 종료시, nextLine() 을 통해 초기화가 필요하다"로 배웠다. 실제로 하는 일은 **다음 LF 까지 읽어 버리는 것**이고, 버퍼에 여러 줄이 남아 있으면 한 줄만 없어진다. "초기화"로 외우면 왜 어떤 때는 정리가 되고 어떤 때는 안 되는지 설명할 수 없다.
- **`next()` 는 「공백 전까지」가 아니라 「공백을 건너뛴 다음 토큰」이다** — 이 필기는 "시작점에 공백부터(있을시) ~ 다음 공백직전까지"라 적었는데, 앞쪽 공백은 **결과에 포함되지 않는다.** 구분자는 토큰을 가르는 데만 쓰이고 돌아오는 값에는 들어가지 않으며, 개행도 공백으로 취급되어 건너뛴다. 그래서 빈 줄을 여러 번 눌러도 `next()` 는 기다린다.
- **`next()` 로 버퍼를 비우는 것은 한 토큰만 비운다** — 잘못된 입력이 `abc def` 였다면 `def` 가 남아 다음 회차에서 같은 예외가 또 난다. 줄 전체를 버리려면 `nextLine()` 이어야 한다 → [[exception-handling]]
- **읽는 단위를 줄로 통일하면 이 함정이 전부 사라진다** — 이 필기가 실습에서 택한 방향이다. `nextLine()` 으로만 받고 숫자는 나중에 해석하면 버퍼에 남는 것이 없다 → [[number-parsing]]

## 함께 보는 개념

- [[io-stream]] — `System.in` 이 속한 세 통로와 스트림 구조
- [[do-while-loop]] · [[switch-statement]] — 입력을 받아 처리하는 흐름
- [[gradle]] — 실행 시 표준 입력을 넘기는 설정
- [[cli]] — 표준 입력이 오는 환경
- [[command-line-arguments]] — 실행할 때 미리 주는 값 (실행 중에 받는 것과 갈린다)
- [[newline-character]] — `nextLine()` 이 잘라 내는 것
- [[number-parsing]] — 줄로 받은 뒤 숫자로 해석하는 방법
- [[static-member]] — `Scanner` 가 인스턴스여야 하는 이유
- [[character-stream]] — 통로가 파일이 될 때 안쪽에 오는 층
- [[csv]] — 그 파일을 줄 단위로 읽어 형식을 해석하는 쪽

## 출처

- [[2024-06-05-Day09]] — `System.in` 을 `Scanner` 로 감싸 `nextInt()` 로 읽고 `close()` 하는 흐름, 그리고 `gradle run` 에서 `standardInput = System.in` 설정이 없으면 오류가 난다는 것을 배웠다
- [[2024-06-11-Day12]] — 키보드 입력이 버퍼에 줄 단위로 쌓이고 `nextLine()` 은 LF 까지 먹고 버리는 반면 `next()` 류는 LF 를 남긴다는 것, 그래서 섞어 쓰면 다음 읽기가 어긋난다는 것을 버퍼 그림으로 배웠다
- [[2024-07-19-Day39]] — `new Scanner(new FileReader("user.csv"))` 로 **같은 `Scanner` 에 키보드 대신 파일을 넘긴다** — 「`Scanner` 는 키보드 전용이 아니다」가 코드로 확인되는 자리다. 대신 파일에는 끝이 있어서 `nextLine()` 이 `NoSuchElementException` 을 던지고, 그것을 잡아 루프를 나가는 종료 조건이 처음 등장한다(`hasNextLine()` 은 쓰지 않았다). `Scanner` 를 닫으면 안쪽 `FileReader` 까지 닫히는 성질은 Day09 의 `System.in` 사례와 같다

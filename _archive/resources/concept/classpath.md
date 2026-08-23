---
type: concept
id: classpath
title: 클래스패스 (Classpath)
aliases:
  - 클래스패스
  - classpath
  - cp
up:
  - 2024-05-29-Day04
  - 2024-05-31-Day06
  - 2024-10-01-Day86
tags:
  - java
  - jvm
  - 빌드
---

# 클래스패스 (Classpath)

[[jvm]] 이 `.class` 파일을 찾을 위치. 실행할 클래스가 어디 있는지 JVM 은 스스로 알지 못하므로 알려줘야 한다.

## 정의

컴파일 결과물의 위치를 정하는 옵션과 그것을 알려주는 옵션이 짝이다.

| 옵션 | 쓰는 도구 | 하는 일 |
|---|---|---|
| `-d` | `javac` | 컴파일해 만든 `.class` 파일을 어느 폴더에 둘지 정한다 |
| `-classpath` (`-cp`) | `java` | `.class` 파일의 위치를 JVM 에 알려준다 |

이 짝이 필요한 이유는 **표준 디렉토리 구조**에서 소스와 컴파일 결과물을 다른 폴더에 두기 때문이다. 소스 파일과 컴파일 파일을 섞어 두지 않으면 관리가 쉬워지는데, 대신 결과물이 소스 옆에 없으니 위치를 지정하는 일이 생긴다.

## 사용 예시

`bin` 폴더에 [[bytecode]] 를 만들고, 실행할 때 그 폴더를 알려준다.

```bash
$ javac -d bin Hello.java      # .class 를 bin/ 에 만든다
$ java -classpath bin Hello    # bin/ 에서 Hello.class 를 찾아 실행
```

두 번째 줄에서 `Hello` 는 파일명이 아니라 **클래스 이름**이다. `Hello.class` 라고 쓰지 않는다 — 파일을 지정하는 게 아니라 클래스패스 안에서 그 이름의 클래스를 찾으라고 하는 것이다.

[[package]] 에 속한 클래스라면 패키지를 붙인 **전체 이름**을 준다. 클래스패스는 최상위 폴더까지고, 그 아래 경로는 이름에서 나온다.

```bash
$ java -cp app/build/classes/java/main study2.lang2.Test
```

`study2.lang2` 의 `.` 이 폴더 구분으로 바뀌어 `app/build/classes/java/main/study2/lang2/Test.class` 를 찾는다.

## 왜 중요한가

**`ClassNotFoundException`·`NoClassDefFoundError` 의 자리가 여기다.** 코드가 맞아도 클래스패스가 틀리면 실행되지 않고, 반대로 클래스패스만 맞춰 주면 코드를 고치지 않고 해결된다. 그래서 "코드 문제인가 경로 문제인가"를 먼저 가르는 것이 진단의 첫 단계가 된다.

라이브러리를 쓰기 시작하면 이 문제가 커진다. 내 클래스뿐 아니라 남의 `.jar` 도 전부 클래스패스에 들어가야 하므로, 손으로 관리할 규모를 금세 넘어선다 — 그것을 대신하는 것이 [[build]] 도구다.

## 경계와 오해

- **클래스패스 ≠ 파일 경로** — 클래스패스는 **찾을 후보 위치의 목록**이고, 그 안에서 클래스는 이름으로 찾힌다. 그래서 실행 인자에 확장자를 붙이지 않는다.
- **`-d` 와 `-cp` 는 다른 도구의 옵션이다** — `-d` 는 컴파일할 때(`javac`), `-cp` 는 실행할 때(`java`)다. 같은 폴더를 가리키지만 역할이 반대다(쓰는 쪽 / 읽는 쪽).
- **`PATH` 와 다르다** — `PATH` 는 OS 가 실행파일을 찾는 목록이고, 클래스패스는 JVM 이 클래스를 찾는 목록이다. 층이 다르다.

## 함께 보는 개념

- [[jvm]] — 클래스패스를 보고 클래스를 찾는 주체
- [[bytecode]] — 클래스패스에서 찾는 대상
- [[build]] — 클래스패스 관리를 대신하는 도구
- [[package]] — 클래스 이름을 폴더 경로로 바꾸는 규칙

## 출처

- [[2024-10-01-Day86]] — 넉 달 뒤. **클래스패스가 `.class` 만의 것이 아니라는 것이 드러난다.** `ClassPathXmlApplicationContext("com/eomcs/spring/ioc/ex01/a/application-context.xml")` 는 설정 **XML** 을 같은 경로 규칙으로 찾고, 이것이 `FileSystemXmlApplicationContext` 의 절대 경로(`file:///Users/...`)와 갈리는 지점이다 — 필기가 뒤쪽을 두고 「XML 파일의 위치가 바뀌면, 코드를 다시 수정해야 한다. 사용빈도는 낮다」고 적은 이유가 그것이다. 같은 논리가 스프링의 `classpath:` 접두어 전반에 걸린다 → [[java-config]] · [[externalized-configuration]]
- [[2024-05-29-Day04]] — `-d` 로 `.class` 경로를 정하고 `-classpath` 로 JVM 에 알려준다는 짝, 그리고 소스와 컴파일 파일을 분리하는 표준 디렉토리 구조를 배웠다
- [[2024-05-31-Day06]] — 패키지에 속한 클래스는 `-cp` 에 최상위만 주고 전체 이름으로 지정한다는 것을 배웠다


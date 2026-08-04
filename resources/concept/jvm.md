---
type: concept
id: jvm
title: JVM (Java Virtual Machine)
aliases:
  - JVM
  - 자바 가상 머신
  - Java Virtual Machine
  - WORA
  - Write once Run anywhere
up:
  - 2024-05-28-Day03
tags:
  - java
  - 실행모델
  - jvm
---

# JVM (Java Virtual Machine)

[[bytecode]] 를 OS 위에서 실행하는 가상 인터프리터. OS 마다 그 OS 용 JVM 이 따로 있고, 그 위에서 도는 바이트코드는 어느 OS 인지 모른다.

## 정의

Java 프로그램이 도는 경로는 두 단계로 갈라져 있다.

```text
소스(.java) ──javac──▶ 바이트코드(.class) ──▶ [ OS별 JVM ] ──▶ 실행
                        (어디서 만들어도 동일)      (환경마다 다름)
```

**"Write once, Run anywhere"(WORA)** 가 이 구조를 부르는 이름이다. 근거는 둘이다.

- 어떤 OS 용 컴파일을 쓰든 **생성된 바이트코드는 같다**
- 그 바이트코드를 OS 별 JVM 이 구동하므로 **실행 결과도 같다**

## 왜 중요한가

**[[platform-dependency]] 를 흡수하는 층이 JVM 이다.** 컴파일 방식에서는 CPU 종류 × OS 종류만큼 실행파일을 만들어야 했는데, 그 부담이 개발자에게서 JVM 배포자에게로 넘어간다. 개발자는 바이트코드 하나만 만든다.

이 구조가 Java 를 서버에서 오래 쓰게 한 이유이기도 하다. 개발은 맥에서 하고 배포는 리눅스에 하는 식이 자연스럽게 성립한다.

## 경계와 오해

- **JVM 은 플랫폼 독립이 아니다** — **바이트코드가** 플랫폼 독립이고, JVM 자체는 OS·CPU 별로 따로 만들어져 배포된다. 의존성이 없어진 게 아니라 한 층 아래로 내려간 것이다. 이걸 뒤집어 이해하면 "Java 는 아무데서나 돈다"는 말만 남고 왜 그런지는 설명하지 못한다.
- **JVM ≠ [[jdk]]** — JVM 은 실행만 한다. 컴파일하는 `javac` 는 JDK 에 들어 있다. 그래서 JRE 만 깔린 서버에서는 프로그램을 돌릴 수 있어도 컴파일은 못 한다.
- **JVM ≠ Java 전용** — 바이트코드 규격을 지키면 어느 언어든 JVM 위에서 돈다. Kotlin·Scala 가 그렇다.

## 함께 보는 개념

- [[bytecode]] — JVM 이 실행하는 입력
- [[platform-dependency]] — JVM 이 흡수하는 문제
- [[jdk]] — JVM 을 포함하는 개발 꾸러미

## 출처

- [[2024-05-28-Day03]] — "Write once, Run anywhere" 의 두 근거(바이트코드 동일 · OS별 JVM 구동)를 배웠다

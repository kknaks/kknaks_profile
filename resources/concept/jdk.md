---
type: concept
id: jdk
title: JDK와 JRE (Java Development Kit / Runtime Environment)
aliases:
  - JDK
  - JRE
  - Java Development Kit
  - Java Runtime Environment
up:
  - 2024-05-28-Day03
tags:
  - java
  - 개발도구
  - 설치
---

# JDK와 JRE (Java Development Kit / Runtime Environment)

Java 를 실행하는 데 필요한 것과 개발하는 데 필요한 것을 갈라 놓은 두 꾸러미. **JRE 가 실행용, JDK 는 그것을 포함한 개발용**이다.

## 정의

바깥에서 안으로 세 겹이다.

| 꾸러미 | 구성 | 할 수 있는 일 |
|---|---|---|
| [[jvm]] | 바이트코드 실행 | 실행 |
| **JRE**(Java Runtime Environment) | JVM + 실행할 때 쓰는 도구 | 실행 |
| **JDK**(Java Development Kit) | JRE + 개발도구 | 실행 + **컴파일** |

JDK 가 더하는 개발도구는 컴파일러(`javac`)·디버거·프로파일러·문서생성기 등이다.

Java 제품군에서 이 꾸러미가 속한 곳은 **Java SE**(Standard Edition)다. 그 밖에 웹 애플리케이션 패키지·분산관리도구·웹서버 개발도구를 담은 **Java EE**(Enterprise Edition)가 있고, 임베디드용 **Java ME**(Micro Edition)는 옛 필기에 "망함"으로 적어 둔 대로 사실상 쓰이지 않는다.

## 사용 예시

설치한 뒤 두 명령으로 확인한다. 실행 쪽과 컴파일 쪽이 따로 답한다.

```bash
java -version    # JRE(실행) 쪽 버전
javac -version   # 컴파일러 쪽 버전
```

여러 버전이 깔려 있으면 어느 것을 쓸지 정해 줘야 한다. macOS 에서는 `JAVA_HOME` 을 잡고 그 아래 `bin` 을 `PATH` 앞에 둔다.

```bash
JAVA_HOME=$(/usr/libexec/java_home -v 21)
PATH=$JAVA_HOME/bin:$PATH
```

## 왜 중요한가

**서버에 무엇을 깔아야 하는지가 이 구분에서 나온다.** 배포된 바이트코드만 돌리는 서버에는 JRE 로 충분하고, 그 편이 설치 용량도 작다. 반대로 빌드하는 기계에는 JDK 가 있어야 한다 — JRE 만 있는 곳에서 `javac` 를 찾으면 없다.

버전이 여러 개 깔릴 수 있다는 점도 여기서 중요해진다. 어느 JDK 를 기본으로 쓰는지가 `PATH` 로 정해지므로, 같은 코드가 기계마다 다른 버전으로 컴파일될 수 있다.

## 경계와 오해

- **JDK ≠ JVM** — JVM 은 JDK 안에 든 실행 엔진 하나다. "JDK 를 깔았다"는 것은 컴파일러까지 함께 깔았다는 뜻이다.
- **`java -version` 이 답한다고 컴파일이 되는 것은 아니다** — JRE 만 깔린 환경이 그렇다. 두 명령을 따로 확인하는 이유다.
- **Java SE·EE 는 버전이 아니라 제품군이다** — 21 같은 숫자와 다른 축이다. Java EE 는 SE 를 대체하는 것이 아니라 그 위에 서버용 규격을 더한 것이다.

## 함께 보는 개념

- [[jvm]] — JRE 안에 든 실행 엔진
- [[bytecode]] — JDK 의 컴파일러가 만들어 내는 것
- [[cli]] — 버전 확인과 `PATH` 설정을 하는 방식

## 출처

- [[2024-05-28-Day03]] — JRE = JVM + 실행 도구, JDK = JRE + 개발도구라는 구성과 Java SE/EE/ME 제품군, 그리고 JDK 21 설치·`JAVA_HOME` 설정을 배웠다

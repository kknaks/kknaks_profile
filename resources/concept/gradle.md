---
type: concept
id: gradle
title: Gradle
aliases:
  - gradle
  - 그래들
  - gradlew
  - Gradle Wrapper
up:
  - 2024-05-29-Day04
  - 2024-06-04-Day08
  - 2024-06-05-Day09
tags:
  - gradle
  - 빌드
  - java
  - 개발도구
---

# Gradle

Java 프로젝트에서 쓰는 [[build]] 도구. 컴파일·실행·정리 같은 단계를 **태스크**로 두고 명령 하나로 부른다.

## 정의

Gradle 이 하는 일은 태스크 단위로 나뉘어 있다.

| 명령 | 하는 일 |
|---|---|
| `gradle init` | 프로젝트의 표준 디렉토리 구조와 설정 파일을 만든다 |
| `gradle compileJava` | 컴파일만 한다 |
| `gradle build` | 빌드 전체(컴파일 → 테스트 → 산출물 묶기)를 한다 |
| `gradle run` | 빌드한 것을 실행한다 |
| `gradle clean` | 빌드 산출물을 지운다 |

`gradle init` 이 처음에 오는 이유는, 표준 구조를 사람이 만들지 않아도 되게 해 주기 때문이다. 소스와 컴파일 결과물이 어느 폴더에 가는지가 정해지면 [[classpath]] 를 손으로 지정할 일이 없어진다.

### 플러그인이 태스크를 더한다

**태스크 목록은 고정이 아니다.** `build.gradle` 의 `plugins` 에 무엇을 넣었는지에 따라 쓸 수 있는 태스크가 달라진다.

```groovy
plugins {
    id 'java'      // 자바 컴파일 도구. .classpath, .settings/* 생성에도 쓰인다
    id 'eclipse'   // 이클립스 관련 파일(.project) 을 다루는 도구
}

eclipse {
    project {
        name = "java-lang"   // 지정하지 않으면 폴더 이름(예: app)을 쓴다
    }
    jdt {
        sourceCompatibility = 21
        targetCompatibility = 21
        javaRuntimeName = "JavaSE-21"
    }
}
```

`eclipse` 플러그인을 넣었기 때문에 `gradle eclipse`·`gradle cleanEclipse` 태스크가 생긴다. 지금 무엇을 쓸 수 있는지는 `gradle tasks` 로 확인한다.

| 명령 | 하는 일 |
|---|---|
| `gradle tasks` | 지금 쓸 수 있는 태스크 목록 |
| `gradle eclipse` | IDE 설정 파일(`.project`·`.classpath`·`.settings/*`) 생성 |
| `gradle cleanEclipse` | 그 설정 파일 삭제 (설정이 잘못됐을 때) |

### 실행 환경도 빌드 스크립트가 정한다

`gradle run` 이 무엇을 어떻게 실행할지가 `build.gradle` 에 적혀 있다.

```groovy
application {
    mainClass = 'bitcamp.myapp.App'   // 어느 클래스의 main() 을 실행할지
}

run {
    standardInput = System.in         // 키보드 입력을 프로그램에 넘긴다
}
```

`gradle init` 이 만들어 준 기본값은 `mainClass = 'org.example.App'` 이라, 패키지를 바꿨으면 여기도 고쳐야 실행된다 → [[main-method]]

`standardInput` 설정이 없으면 [[standard-input]] 을 읽는 프로그램이 `gradle run` 에서 오류가 난다. **코드가 맞아도 실행 설정 때문에 안 되는 종류의 오류다.**

## 사용 예시

macOS 에서는 Homebrew 로 깐다.

```bash
$ brew install gradle
$ gradle init          # 프로젝트 초기화
$ gradle build         # 빌드
$ gradle run           # 실행
```

**Gradle 이 깔려 있지 않은 컴퓨터**에서는 프로젝트에 함께 들어 있는 래퍼(wrapper)를 쓴다.

```bash
$ ./gradlew [task]
```

`gradlew` 는 프로젝트가 쓰는 Gradle 을 필요하면 내려받아 실행해 주는 스크립트다. 그래서 받는 사람이 Gradle 을 미리 깔지 않아도 되고, **모두가 같은 Gradle 버전으로 빌드하게 된다.**

## 왜 중요한가

**빌드 방법이 프로젝트 안에 들어온다.** `gradlew` 까지 포함해 저장소에 커밋되므로, 코드를 받은 사람은 `./gradlew build` 한 줄로 같은 결과를 얻는다. "먼저 뭘 깔아야 하나"를 문서로 설명하지 않아도 되는 것이 여기서 나오는 값이다.

버전이 프로젝트에 고정된다는 점도 크다. 각자 깐 Gradle 버전이 다르면 같은 코드가 다르게 빌드될 수 있는데, 래퍼를 쓰면 그 변수가 사라진다.

## 경계와 오해

- **`gradle` ≠ `./gradlew`** — 앞은 내 컴퓨터에 깐 Gradle 이고, 뒤는 프로젝트가 지정한 Gradle 이다. 팀 작업에서는 `./gradlew` 를 쓰는 것이 기본이다.
- **`gradle build` ≠ `gradle run`** — 빌드는 산출물을 만드는 것까지고, 실행은 그 다음이다. 빌드가 됐다는 것이 동작한다는 뜻은 아니다.
- **Gradle 이 컴파일하는 것이 아니다** — [[jdk]] 의 `javac` 를 대신 호출한다. JDK 없이 Gradle 만 깔면 빌드되지 않는다.
- **IDE 설정 파일은 빌드 산출물로 볼 수 있다** — `.project`·`.classpath` 를 손으로 만들지 않고 `gradle eclipse` 로 생성한다. 그러면 IDE 설정의 원천이 `build.gradle` 한 곳이 되고, 잘못되면 `cleanEclipse` 후 다시 만들면 된다.

## 함께 보는 개념

- [[build]] — Gradle 이 구현하는 개념
- [[classpath]] — 표준 구조로 Gradle 이 대신 관리하는 것
- [[jdk]] — Gradle 이 호출하는 컴파일러가 든 곳

## 출처

- [[2024-05-29-Day04]] — `brew install gradle` 설치, `init`/`build`/`run`/`compileJava`/`clean` 태스크, 그리고 Gradle 없는 컴퓨터에서 쓰는 `./gradlew` 를 배웠다
- [[2024-06-04-Day08]] — `plugins` 에 넣은 것에 따라 태스크가 늘어난다는 것(`eclipse` 플러그인 → `gradle eclipse`), `gradle tasks` 로 확인한다는 것을 배웠다
- [[2024-06-05-Day09]] — `mainClass` 기본값이 `org.example.App` 이라 고쳐야 실행된다는 것, `run { standardInput = System.in }` 이 없으면 키보드 입력이 닿지 않는다는 것을 실습에서 겪었다

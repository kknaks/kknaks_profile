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
  - 2024-07-22-Day40
  - 2024-07-24-Day42
  - 2024-08-14-Day56
  - 2024-10-18-Day96
tags:
  - spring
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

### 남의 코드를 쓸 수 있게 하는 것도 여기다

Day40 이 Gson 을 쓰려고 한 일이 **줄 하나**다.

```gradle
dependencies {
    implementation 'com.google.code.gson:gson:2.11.0'
}
```

`그룹:이름:버전` 세 조각이 **좌표**이고, 그것으로 Gradle 이 중앙 저장소에서 `.jar` 를 내려받아 컴파일·실행 [[classpath]] 에 넣는다. 손으로 할 일이 **없다** — 파일을 찾아 내려받고 어디에 두고 클래스패스에 어떻게 적을지가 전부 사라진다.

| 조각 | 예 | 뜻 |
|---|---|---|
| group | `com.google.code.gson` | 누가 만들었나 (대개 역순 도메인) |
| name | `gson` | 무엇인가 |
| version | `2.11.0` | **어느 것인가** — 이 자리가 재현성을 만든다 |

버전을 적는 것이 래퍼(`gradlew`)와 같은 논리다 — **누가 언제 빌드해도 같은 라이브러리를 쓴다.**

`implementation` 은 라이브러리를 **어디에 놓을지**를 고르는 자리(구성, configuration)다.

| 구성 | 컴파일할 때 | 실행할 때 | 이 라이브러리를 쓰는 남에게 |
|---|---|---|---|
| `implementation` | 있다 | 있다 | **안 보인다** |
| `api` | 있다 | 있다 | 보인다 |
| `compileOnly` | 있다 | 없다 | 안 보인다 |
| `testImplementation` | 테스트만 | 테스트만 | 안 보인다 |

**기본으로 `implementation` 을 쓰는 이유는 「내가 무엇을 쓰는지」가 남의 클래스패스로 새지 않게 하는 것**이고, 이것이 빌드 도구가 [[coupling]] 을 다루는 방식이다.

#### 좌표는 어디서 오고, 넣은 다음에 한 가지가 더 있다

이틀 뒤 Day42 가 그 좌표를 **찾아오는 절차**를 적는다 — 「maver repo에서 apachi-poi를 검색하여 필요한 버전에 gradle정보를 읽어온다」. `mvnrepository.com` 에서 라이브러리를 찾으면 버전별로 `implementation '…'` 한 줄이 그대로 표시되므로, **좌표를 외우거나 만들어 쓰는 것이 아니라 복사해 오는 것**이다. Day40 의 Gson 좌표도 같은 곳에서 왔다 → [[apache-poi]]

그리고 넣은 뒤에 IDE 쪽 한 걸음이 남는다. Day42 가 두 갈래로 적었다.

| IDE | 하는 일 | 이유 |
|---|---|---|
| IntelliJ | Gradle 새로고침(코끼리 아이콘) | IDE 가 `build.gradle` 을 다시 읽어 `.jar` 를 인덱스에 넣는다 |
| Eclipse | 프로젝트 폴더에서 `gradle eclipse` 실행 | `.classpath` 를 다시 **생성**한다 |

**둘이 하는 일이 다르다** — IntelliJ 는 빌드 스크립트를 직접 모델로 읽어 들이고, Eclipse 는 `.classpath` 라는 파일을 통해서만 안다. 위의 「IDE 설정 파일은 빌드 산출물로 볼 수 있다」가 이 차이의 결과이고, **`build.gradle` 만 고치고 이 단계를 빼먹으면 Gradle 빌드는 되는데 편집기에는 빨간 줄이 남는다** → [[classpath]]

#### 세 주 뒤 Day56 — 같은 절차를 그대로 다시 쓴다

Day56 은 [[jdbc]] 드라이버를 들이면서 **Day42 와 똑같은 두 걸음**(좌표 한 줄 → IDE 반영)을 반복한다. 새로 배운 것이 아니라 **이 절차가 라이브러리 종류와 무관하게 같다**는 것이 그 회차에서 확인된 것이다 — Gson(Day40)·Apache POI(Day42)·JDBC 드라이버(Day56) 셋이 전부 `implementation '그룹:이름:버전'` 한 줄이다.

한 가지가 달라졌다. Day56 은 **한 자리에 좌표 넷을 주석으로 구분해 나열**한다.

```groovy
//MySQL JDBC Driver
implementation 'com.mysql:mysql-connector-j:8.4.0'

//Maria JDBC Driver
implementation 'org.mariadb.jdbc:mariadb-java-client:3.4.1'
```

목록으로 적힌 것은 **참고표**이고 `dependencies` 는 **선언**이다 — 넷을 다 남기면 쓰지 않는 jar 셋이 컴파일·실행 클래스패스와 배포 산출물에 그대로 실린다. 주석이 「이 중 하나를 고른다」는 뜻을 갖지 않으므로, **필기의 목록과 빌드 스크립트의 내용은 같은 것이 아니다** → [[jdbc]]

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

**무엇을 쓸 수 있는지도 이 파일이 정한다.** Day40 에서 `import com.google.gson.Gson;` 이 되느냐 안 되느냐가 `build.gradle` 한 줄에 달려 있다 — **코드가 아니라 빌드 스크립트가 컴파일 가능 범위를 정하는 것**이고, 그래서 남의 프로젝트를 받아 처음 읽어야 하는 파일이 이것이다 → [[classpath]] · [[json]]

## 경계와 오해

- **`gradle` ≠ `./gradlew`** — 앞은 내 컴퓨터에 깐 Gradle 이고, 뒤는 프로젝트가 지정한 Gradle 이다. 팀 작업에서는 `./gradlew` 를 쓰는 것이 기본이다.
- **`gradle build` ≠ `gradle run`** — 빌드는 산출물을 만드는 것까지고, 실행은 그 다음이다. 빌드가 됐다는 것이 동작한다는 뜻은 아니다.
- **Gradle 이 컴파일하는 것이 아니다** — [[jdk]] 의 `javac` 를 대신 호출한다. JDK 없이 Gradle 만 깔면 빌드되지 않는다.
- **IDE 설정 파일은 빌드 산출물로 볼 수 있다** — `.project`·`.classpath` 를 손으로 만들지 않고 `gradle eclipse` 로 생성한다. 그러면 IDE 설정의 원천이 `build.gradle` 한 곳이 되고, 잘못되면 `cleanEclipse` 후 다시 만들면 된다.
- **Day40 필기의 `{ implementation '...' }` 는 그대로 붙이면 안 된다** — 중괄호는 **`dependencies` 블록**의 것이고 넣을 것은 그 안의 한 줄이다. 필기가 「dependencies에 gson 라이브러리를 추가한다」로 위치를 설명했으니 뜻은 맞지만, 코드 블록만 떼어 보면 어디에 무엇을 넣는지 알 수 없다.
- **`build.gradle` ≠ `gradle.build` — 세 회차에 걸쳐 뒤바뀐 채였다** — Day40(07-22)이 「gradle.build」, Day42(07-24)가 「gradlebuild」, **Day56(08-14)이 다시 「gradle.build」**로 적었다. 처음 두 건만 보고 「연속 두 회차의 실수」로 적어 두었는데, 세 주 뒤 같은 표기가 또 나왔으므로 **일회성 오타가 아니라 굳은 습관**으로 다시 본다. 확장자가 `.gradle` 이고 파일 이름이 `build` 인 것 — 즉 **`gradle` 이 뒤에 온다** — 을 잡아 두면 고정된다. 뒤바뀐 이름으로는 파일을 찾을 수 없으므로 남에게 위치를 설명할 때 그대로 새어 나간다.
- **`gradle esclipse` 는 존재하지 않는 태스크다** — Day42 와 Day56 이 같은 오타를 냈고, **Day56 은 그것을 코드로 감싸 명령처럼 적었다**(`$> gradle esclipse`). 그대로 실행하면 컴파일 오류도 접속 오류도 아닌 `Task 'esclipse' not found in root project` 가 나온다. 태스크 이름은 `eclipse` 플러그인이 만든 것이라 **플러그인 id 와 글자가 같아야** 하고, 그래서 이 오타는 「IDE 반영이 안 된다」가 아니라 **아무 일도 일어나지 않는다**로 나타난다 → [[cli]]
- **`Implementation` 이 아니라 `implementation` 이다** — Day42 가 「gradlebuild에 Implementation에 해당 값을 삽입한다」로 적었는데, 이것은 Groovy 스크립트 안에서 **호출되는 메서드 이름**이라 대소문자를 구분한다. 첫 글자를 대문자로 쓰면 「설정 이름을 못 찾겠다」는 빌드 실패가 나고, 그 오류 메시지가 자바 컴파일 오류처럼 생기지 않아 처음에는 어디를 봐야 할지 알기 어렵다. **`build.gradle` 안의 낱말은 문서의 라벨이 아니라 실행되는 코드**다.
- **의존성을 적어도 저장소가 없으면 못 받는다** — `repositories { mavenCentral() }` 가 있어야 좌표를 찾아갈 곳이 정해진다. `gradle init` 이 만들어 주기 때문에 안 보이는 것이고, **없는 것이 아니라 이미 있는 것**이다.
- **의존성을 추가한 뒤에는 IDE 설정을 다시 만들어야 한다** — `build.gradle` 만 고치면 Gradle 빌드는 되는데 IDE 는 새 `.jar` 를 모른 채 빨간 줄을 보여 준다. `gradle eclipse` 를 다시 돌리는 것이 그것을 맞추는 일이고, 위의 「IDE 설정은 빌드 산출물」이 여기서 실제로 쓰인다.
- **`implementation` 은 「구현에 쓴다」는 이름값이 있다** — 아무 뜻 없는 키워드가 아니라 **이 라이브러리를 내 API 에 노출하지 않는다**는 선언이다. 반환 타입이나 `public` 메서드 시그니처에 그 라이브러리 타입이 나오면 `api` 가 맞고, 그렇지 않은 이상 `implementation` 이다 → [[encapsulation]]

## 함께 보는 개념

- [[spring-boot]] — 스타터와 버전 관리 플러그인이 쓰이는 자리

- [[build]] — Gradle 이 구현하는 개념
- [[classpath]] — 표준 구조로 Gradle 이 대신 관리하는 것
- [[jdk]] — Gradle 이 호출하는 컴파일러가 든 곳
- [[json]] — 의존성 한 줄로 들여온 첫 외부 라이브러리
- [[apache-poi]] — 좌표를 `mvnrepository` 에서 찾아 들인 두 번째 라이브러리
- [[jdbc]] — 같은 절차로 들인 세 번째 것. 「설치」가 좌표 한 줄로 바뀌는 자리
- [[coupling]] — 구성(`implementation`·`api`)이 다루는 문제
- [[cli]] — 태스크 이름을 그대로 쳐야 하는 자리

## 출처

- [[2024-10-18-Day96]] — **의존성 선언이 두 가지로 달라진다.** 하나는 `spring-boot-starter-*` 처럼 **묶음 하나가 여러 라이브러리를 끌고 오는 것**이고, 다른 하나는 `io.spring.dependency-management` 플러그인이 **버전을 대신 정해 줘서 스타터에 버전을 안 적는 것**이다. 그리고 `implementation`·`runtimeOnly`·`developmentOnly`·`annotationProcessor`·`testImplementation` 다섯 범위가 한 파일에 나란히 나와, 「언제 필요한 의존성인가」가 선언에 적힌다는 것이 드러난다 → [[spring-boot]]
- [[2024-05-29-Day04]] — `brew install gradle` 설치, `init`/`build`/`run`/`compileJava`/`clean` 태스크, 그리고 Gradle 없는 컴퓨터에서 쓰는 `./gradlew` 를 배웠다
- [[2024-06-04-Day08]] — `plugins` 에 넣은 것에 따라 태스크가 늘어난다는 것(`eclipse` 플러그인 → `gradle eclipse`), `gradle tasks` 로 확인한다는 것을 배웠다
- [[2024-06-05-Day09]] — `mainClass` 기본값이 `org.example.App` 이라 고쳐야 실행된다는 것, `run { standardInput = System.in }` 이 없으면 키보드 입력이 닿지 않는다는 것을 실습에서 겪었다
- [[2024-07-22-Day40]] — 외부 라이브러리를 처음 들인다. 「App에 위치한 gradle.build의 dependencies에 gson 라이브러리를 추가한다」로 위치를 적고 `implementation 'com.google.code.gson:gson:2.11.0'` 좌표 한 줄로 Gson 을 쓸 수 있게 만든다 — **의존성 관리가 빌드 도구의 일이라는 것을 실습으로 만난 자리.** 필기는 좌표의 세 조각이 무엇인지, `implementation` 이 다른 구성과 어떻게 다른지, `repositories` 가 있어야 한다는 것은 다루지 않았다
- [[2024-07-24-Day42]] — 이틀 뒤 두 번째 라이브러리(Apache POI)를 들이며 **좌표를 얻는 절차**를 적는다 — 「maver repo에서 apachi-poi를 검색하여 필요한 버전에 gradle정보를 읽어온다」로 `mvnrepository.com` 을 출처로 밝히고, 실제 링크는 `org.apache.poi/poi-ooxml` 을 가리킨다. 넣은 뒤 IDE 반영을 두 갈래로 나눈 것이 Day40 에 없던 내용이다 — 「IntelliJ의 경우 gradle 새로고침」·「Esclipse의 경우 터미널에서 해당 폴더 까지 이동후 gradle esclipse를 실행」. 다만 파일 이름을 「gradlebuild」로, 구성 이름을 대문자 「Implementation」으로 적어 **둘 다 그대로는 동작하지 않는 표기**이며, 검색어(`apachi-poi`)와 실제 좌표(`poi-ooxml`)가 다른 것도 짚지 않았다
- [[2024-08-14-Day56]] — 세 주 뒤 [[jdbc]] 드라이버를 들이며 **같은 두 걸음을 그대로 반복한다** — 「gradle.build에 해당 라이브러리 추가」 + 「gradle.build 업데이트」(IntelliJ 는 IDE 에서, Eclipse 는 터미널에서). 새 문법은 없고, **절차가 라이브러리 종류와 무관하다는 확인**과 벤더 넷의 좌표 실물(`ojdbc11-production`·`mssql-jdbc:12.8.0.jre11`·`mysql-connector-j:8.4.0`·`mariadb-java-client:3.4.1`)이 이 회차의 값이다. 다만 넷을 **한 자리에 다 나열해** 「목록은 참고표이고 `dependencies` 는 선언」이라는 구분이 필기에 없고, 파일 이름 「gradle.build」가 **세 번째로** 뒤바뀌었으며 태스크 이름은 Day42 와 같이 「esclipse」다 — 이번에는 코드로 감싸 명령처럼 적혀 있어 복사하면 곧바로 실패한다. `repositories`·구성(`implementation`) 의 뜻은 여기서도 다루지 않는다

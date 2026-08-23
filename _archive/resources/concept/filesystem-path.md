---
type: concept
id: filesystem-path
title: 파일 경로 (상대·절대·정규)
aliases:
  - 파일 경로
  - 경로
  - file path
  - 상대 경로
  - 절대 경로
  - 정규 경로
  - canonical path
  - absolute path
  - relative path
  - 작업 디렉토리
  - working directory
  - user.dir
up:
  - 2024-07-23-Day41
tags:
  - java
  - 파일
  - 경로
  - 실행환경
---

# 파일 경로 (상대·절대·정규)

**파일을 가리키는 이름이고, 같은 파일을 가리키는 이름이 여러 개일 수 있다.** 그 이름이 완결됐는지(절대) 어딘가를 기준으로 읽어야 하는지(상대), 그리고 군더더기를 걷어 낸 유일한 형태인지(정규)로 갈린다.

## 정의

Day41 이 같은 `File` 하나에서 이름을 세 번 꺼내 본다.

```java
    File currentDir = new File("./src/main/jave");
    System.out.printf("경로: %s\n", currentDir.getPath());
    System.out.printf("절대경로: %s\n", currentDir.getAbsolutePath());
    System.out.printf("계산된 절대경로: %s\n", currentDir.getCanonicalPath());
```

| 메서드 | 돌려주는 것 | `./src/main/jave` 일 때 |
|---|---|---|
| `getPath()` | **넘긴 문자열 그대로** | `./src/main/jave` |
| `getAbsolutePath()` | 작업 디렉토리를 앞에 붙인 것 | `/Users/…/project/./src/main/jave` |
| `getCanonicalPath()` | 거기서 `.`·`..`·심볼릭 링크까지 **풀어낸 것** | `/Users/…/project/src/main/jave` |

세 값이 다르다는 것이 이 개념의 몸통이다. **절대 경로는 「앞이 채워졌다」는 뜻일 뿐 「깔끔하다」는 뜻이 아니다** — `./` 가 그대로 남아 있다. 필기가 정규 경로를 「계산된 절대경로」라 부른 것이 그 차이를 정확히 가리킨다.

상대 경로가 기준으로 삼는 것은 **JVM 의 작업 디렉토리**(`user.dir` 시스템 프로퍼티)이고, 그것은 **`java` 를 실행한 위치**다 — 소스 파일의 위치도 아니고 클래스 파일의 위치도 아니다 → [[classpath]]

## 사용 예시

Day41 의 `new File(".")` 가 상대 경로의 가장 짧은 형태다.

```java
    File dir = new File(".");
    File[] files = dir.listFiles();
```

필기가 「현재 폴더의 디렉토리 탐색은 생성자에 "."를 추가한다」로 적은 그대로인데, **「현재 폴더」가 어디인지는 이 코드에 없다.** IDE 에서 실행하면 프로젝트 루트, `cd build/classes && java Test` 로 실행하면 그 디렉토리다. 같은 코드가 다른 목록을 찍고, 둘 다 정상 동작이다 → [[file-class]] · [[cli]]

## 왜 중요한가

**「파일을 못 찾는다」의 절반이 경로 문제이고, 어느 종류인지 알면 볼 곳이 달라진다.** 상대 경로가 문제면 고칠 곳은 코드가 아니라 **실행 위치**이고, 절대 경로가 문제면 고칠 곳은 코드다. `getAbsolutePath()` 를 한 번 찍어 보는 것이 이 구분을 즉시 준다 — Day41 의 첫 예제가 하는 일이 정확히 그것이다.

**같은 파일의 이름이 여럿이라는 것이 비교를 깨뜨린다.** `new File("./a.txt")` 와 `new File("a.txt")` 는 같은 파일을 가리키는데 `equals` 가 거짓이다(→ [[file-class]]). 「이 파일을 이미 처리했나」를 경로 문자열로 판정하는 코드는 정규 경로로 정규화하지 않으면 같은 파일을 두 번 센다 → [[object-equality]]

**빌드·배포에서 이 문제가 다시 나온다.** 개발 중에는 IDE 가 작업 디렉토리를 프로젝트 루트로 맞춰 주지만, jar 로 묶어 다른 위치에서 실행하면 상대 경로가 다른 곳을 가리킨다. **코드는 한 줄도 안 바뀌었는데 동작이 바뀌는** 종류의 문제 → [[gradle]] · [[platform-dependency]]

## 경계와 오해

- **절대 경로 ≠ 정규 경로** — 이 노트가 가르는 첫 축이다. `getAbsolutePath()` 는 **문자열을 이어 붙이기만 한다** — `.`·`..` 를 풀지 않고 파일 시스템을 들여다보지도 않는다. `getCanonicalPath()` 는 실제로 디스크를 조회해 심볼릭 링크까지 따라가므로 **`IOException` 을 던질 수 있다.** 같은 줄에 나란히 적혀 있는 두 메서드 중 하나만 예외를 던지는 이유가 이것이고, Day41 의 `main` 에 `throws` 가 없어 **이 예제는 컴파일되지 않는다** → [[exception-handling]]
- **`getPath()` 는 「경로를 계산해 준다」가 아니라 「내가 넣은 것을 돌려준다」다** — `File` 은 생성자에 받은 문자열을 거의 그대로 들고 있다(구분자 정규화만 한다). 그래서 `getPath()` 의 값을 보고 파일 위치를 판단하려 하면 상대 경로일 때 아무 정보가 없다 → [[file-class]]
- **작업 디렉토리 ≠ 클래스가 있는 위치** — 상대 경로의 기준은 `java` 를 실행한 디렉토리이고, `.class` 파일이나 jar 가 놓인 위치와 무관하다. Day41 이 `"./src/main/jave"` 라고 **소스 트리 안쪽 경로**를 쓴 것은 「IDE 가 프로젝트 루트에서 실행한다」를 전제한 것인데, 그 전제가 코드에 적혀 있지 않다. 리소스를 읽을 때 이 문제를 피하는 표준 방법은 경로가 아니라 클래스패스로 찾는 것(`getResourceAsStream`)이다 → [[classpath]] · [[jvm]]
- **`user.dir` 를 바꿔도 상대 경로의 기준은 바뀌지 않는다** — `System.setProperty("user.dir", …)` 는 값만 바뀌고, 이미 만들어진 `File` 의 해석에도 새로 만드는 `File` 의 해석에도 반영되지 않는다(구현이 프로세스의 실제 작업 디렉토리를 쓴다). **JVM 은 프로세스의 작업 디렉토리를 바꾸는 API 를 주지 않는다** — 바꿀 수 있는 것은 실행하는 쪽뿐이다.
- **구분자는 `/` 로 써도 되지만 결과에는 OS 것이 나온다** — Windows 에서도 생성자에 `/` 를 넣으면 동작하는데, `getPath()` 는 `\` 로 바꿔 돌려준다. 그래서 **경로를 문자열로 조립하거나 `split("/")` 로 쪼개는 코드가 한쪽 OS 에서만 맞는다.** 이어 붙일 때는 `new File(parent, child)` 나 `File.separator` 를 쓴다 → [[platform-dependency]] · [[string-comparison]]
- **경로가 있다는 것이 파일이 있다는 뜻이 아니다** — Day41 의 `"./src/main/jave"` 는 `java` 의 오타이고 그런 디렉토리는 없다. 그래도 세 메서드는 모두 값을 돌려준다. **경로는 이름이고 이름은 대상이 없어도 만들어진다** → [[file-class]]
- **경로 문자열을 사용자 입력에서 받으면 `..` 이 공격 통로가 된다** — 정규화하지 않은 상대 경로는 `../../etc/passwd` 처럼 의도한 디렉토리 밖으로 나갈 수 있다(path traversal). `getCanonicalPath()` 로 풀어낸 뒤 **허용한 루트로 시작하는지 확인하는 것**이 표준 방어이고, 이것이 정규 경로가 「깔끔한 표기」가 아니라 **보안 장치**인 자리다.
- **`java.io.File` 의 경로 API 는 Java 7 의 `Path`·`Files` 로 대체됐다** — `Paths.get("./src")` · `path.toAbsolutePath()` · `path.normalize()`(디스크를 안 보고 `.`·`..` 만 푼다) · `path.toRealPath()`(정규 경로)가 같은 자리를 더 잘게 나눠 갖는다. **`normalize()` 와 `toRealPath()` 가 갈리는 것이 `File` 에는 없던 구분**이다 — 존재하지 않는 경로도 정리하고 싶을 때가 있기 때문이다.

## 함께 보는 개념

- [[file-class]] — 이 경로를 들고 있는 객체
- [[classpath]] — 실행 위치와 무관하게 리소스를 찾는 다른 축
- [[cli]] — 작업 디렉토리를 정하는 쪽
- [[platform-dependency]] — 구분자와 루트 표기가 갈리는 축
- [[object-equality]] — 같은 파일의 이름이 여럿이라 비교가 깨지는 자리
- [[gradle]] — 배포 후 작업 디렉토리가 바뀌는 자리
- [[jvm]] — `user.dir` 를 들고 있는 실행 환경
- [[exception-handling]] — 정규 경로만 예외를 던지는 이유

## 출처

- [[2024-07-23-Day41]] — 「현재디렉토리 조회」 절에서 `new File("./src/main/jave")` 하나로 `getPath()`·`getAbsolutePath()`·`getCanonicalPath()` 를 나란히 찍어 **세 이름이 다르다는 것**을 보여 준다. 정규 경로를 「계산된 절대경로」라 불러 절대 경로가 `.` 을 그대로 남긴다는 차이를 정확히 가리켰지만, **`getCanonicalPath()` 만 `IOException` 을 던진다는 것은 다루지 않아 `main` 에 `throws` 가 없고 예제가 컴파일되지 않는다.** 「현재 폴더의 디렉토리 탐색은 생성자에 "."를 추가한다」로 상대 경로를 쓰면서 그 기준이 실행 위치라는 것은 적히지 않았고, 예제 경로의 `jave` 는 `java` 의 오타여서 존재하지 않는 디렉토리다

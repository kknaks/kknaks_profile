---
type: concept
id: file-class
title: 파일·디렉토리 객체 (java.io.File)
aliases:
  - File 클래스
  - java.io.File
  - 파일 객체
  - file class
  - 디렉토리 조회
  - listFiles
  - mkdirs
  - createNewFile
up:
  - 2024-07-23-Day41
tags:
  - java
  - 파일
  - 입출력
  - 표준 라이브러리
---

# 파일·디렉토리 객체 (java.io.File)

**파일이나 디렉토리 자체가 아니라 「그것을 가리키는 이름」을 담은 객체.** Day41 의 한 줄이 쓰임을 말한다 — 「File클래스는 디렉토리나 파일을 다룰 때 사용하는 클래스이다」. 여기서 다루는 것은 **내용이 아니라 존재·속성·목록**이고, 내용을 읽고 쓰는 것은 스트림의 일이다 → [[io-stream]]

## 정의

`File` 이 답해 주는 것은 세 종류다.

| 무리 | 메서드 | 대상이 없으면 |
|---|---|---|
| **이름** | `getName()` · `getPath()` · `getAbsolutePath()` · `getCanonicalPath()` | 그래도 값이 나온다 → [[filesystem-path]] |
| **속성** | `isDirectory()` · `isFile()` · `isHidden()` · `exists()` · `canExecute()` · `length()` · `lastModified()` | `false` 또는 `0` |
| **조작** | `mkdir()` · `mkdirs()` · `createNewFile()` · `delete()` · `listFiles()` | `false` 또는 `null` |

**첫 무리와 나머지가 갈리는 것이 이 클래스를 읽는 요령이다.** 이름은 문자열 계산이라 디스크를 안 보고, 속성·조작은 실제로 파일 시스템을 조회한다. Day41 이 주석으로 정확히 그 경계를 적었다 — 「없는 디렉토리/파일일 경우 false를 return」.

디렉토리를 만드는 두 메서드가 갈리는 축은 **중간 경로를 만들어 주는가**다.

```java
    File dir = new File("temp2");
    if(dir.mkdir()) { /* 디렉토리 생성 : 지정된 경로가 존재해야함 */ }
    else if (dir.mkdirs()){ /*디렉토리 생성 : 지정된 경로가 없으면 경로를 만들고 생성 */}
```

## 사용 예시

**파일을 만들 때는 부모 디렉토리를 먼저 확보한다.** Day41 이 그 순서를 코드로 남겼다.

```java
    File file = new File("temp2/b/test.txt");
    
    File dir = file.getParentFile();
    // 디렉토리가 없으면 먼저 생성
    dir.mkdirs();
    
    // 이후 파일을 생성
    file.createNewFile();
    
    //이후 파일을 지우기
    file.delete();
```

`getParentFile()` 로 부모를 `File` 로 꺼내고 `mkdirs()` 로 두 단계(`temp2`·`temp2/b`)를 한 번에 만든다. **두 줄을 빼면 `createNewFile()` 이 실패한다** — 그리고 필기가 그 실패 방식을 잘못 적었다(아래 「경계와 오해」).

**디렉토리 목록은 `File[]` 로 돌아온다** — 문자열이 아니라 객체 배열이라 그 자리에서 속성을 물어볼 수 있다.

```java
    File dir = new File(".");
    
    //현재 디렉토리 정보 전체 출력
    File[] files = dir.listFiles();
    for (File file : files) {
      System.out.printf("%s   %s %12d %s\n", file.isDirectory() ? "d" : "-", 
          new Date(file.lastModified()), file.length(), file.getName());
    }
```

**`ls -l` 한 줄을 손으로 조립하는 코드다.** `isDirectory()` 를 삼항 연산자로 `d`/`-` 로 바꾸고, `lastModified()` 가 돌려준 밀리초를 `Date` 로 감싸 사람이 읽는 형태로 만든다 → [[ternary-operator]] · [[date-time]]

그리고 **목록을 걸러 받을 수 있다.**

```java
    File[] files = dir.listFiles(file -> file.getName().endWith(".java") && file.isFile());
```

주석 처리된 클래스 판이 바로 위에 남아 있어 **인터페이스 구현 → 람다**의 사다리가 그대로 보인다. Day36 이 손으로 만든 인터페이스에 람다를 넣던 것이 여기서 **표준 라이브러리 API 의 인자 자리**로 처음 옮겨 온다 → [[lambda-expression]] · [[functional-interface]]

## 왜 중요한가

**「파일이 있나」를 묻는 것과 「파일을 읽는 것」이 갈린다.** 스트림은 열면서 없으면 예외를 던지므로 「없으면 만들고 있으면 읽는다」 같은 분기를 짤 수 없다. `exists()`·`isFile()` 이 그 판단을 예외 없이 하게 해 주고, 그래서 저장 파일이 처음 없는 첫 실행을 정상 경로로 다룰 수 있다 → [[exception-handling]] · [[serialization]]

**디렉토리를 데이터로 다룰 수 있게 된다.** `listFiles()` 가 `File[]` 을 주므로 배열·컬렉션의 도구가 그대로 통하고, 필터를 넘기면 조건을 값으로 다루게 된다. 「폴더를 훑는 프로그램」이 별도의 API 를 배우는 일이 아니라 **배열 다루기**로 내려온다 → [[array]]

**경로 계산과 파일 시스템 접근이 한 타입 안에서 갈린다.** `new File(...)` 은 어떤 문자열이든 받아들이므로 **객체를 만드는 데 성공한 것이 대상이 있다는 뜻이 아니다.** 그 구분을 알고 나면 `exists()` 를 왜 매번 물어야 하는지가 설명된다.

## 경계와 오해

- **`File` 객체 ≠ 파일** — `new File("a.txt")` 는 **아무것도 만들지 않는다.** 이름을 담은 객체만 생기고 디스크는 그대로다. 실제로 만드는 것은 `createNewFile()`·`mkdir()` 이거나 출력 스트림을 여는 일이다. Day41 의 `"./src/main/jave"` 가 오타로 존재하지 않는 경로인데도 생성자가 성공하는 것이 이 성질 그대로다 → [[filesystem-path]]
- **「파일 생성경로에 디렉토리가 없다면 false를 반환한다」는 틀렸다 — `IOException` 이 난다** — Day41 이 `createNewFile()` 의 실패를 두 가지로 적었는데 하나만 맞다. **이미 있으면** `false` 를 돌려주지만, **부모 디렉토리가 없으면** OS 가 「No such file or directory」로 거절하므로 `IOException` 이 던져진다. 차이가 큰 이유는 다루는 코드가 달라지기 때문이다 — `false` 는 `if` 로 받고 예외는 `catch` 로 받는다. **`if (!file.createNewFile()) { … }` 로만 짜 두면 부모가 없는 경우가 그 분기에 들어오지 않고 프로그램이 끊긴다.** 필기가 바로 다음 예제에서 `mkdirs()` 를 먼저 부른 것이 실무적으로 맞는 순서인데, 그것이 필요한 이유는 「`false` 를 피하려고」가 아니라 「예외를 피하려고」다 → [[exception-handling]]
- **`else if (dir.mkdirs())` 는 이 예제에서 절대 실행되지 않는 분기다** — `new File("temp2")` 는 부모 경로가 없으므로 `mkdir()` 이 실패하는 이유가 **「이미 있다」뿐**이고, 그 경우 `mkdirs()` 도 `false` 다. 두 메서드의 차이는 `temp2/b/c` 처럼 **중간 경로가 빈 경우에만** 나타난다. 필기의 설명(「지정된 경로가 존재해야함」/「없으면 경로를 만들고」)은 정확한데 **그 차이가 드러나지 않는 예제에 붙어 있다.**
- **`mkdir()` 이 `false` 를 준 이유를 알 수 없다** — 이미 있는 것인지, 권한이 없는 것인지, 부모가 없는 것인지 한 값으로 뭉쳐 온다. 조작 메서드가 전부 `boolean` 인 것이 이 클래스의 구조적 한계이고, Java 7 의 `Files.createDirectories(path)` 는 **실패 이유마다 다른 예외**를 던져 이 문제를 없앤다.
- **`delete()` 는 빈 디렉토리만 지운다** — 안에 무엇이 있으면 `false` 를 돌려주고 아무 일도 하지 않는다. Day41 의 예제는 방금 만든 빈 `temp2` 를 지우므로 성공하지만, **`temp2/b/test.txt` 를 만든 뒤 `temp2` 를 지우려 하면 조용히 실패한다.** 재귀로 훑어 내려가며 지우는 것이 답이고, 여기서도 실패 이유는 안 온다.
- **`listFiles()` 는 `null` 을 돌려줄 수 있다** — 대상이 디렉토리가 아니거나 읽을 권한이 없으면 **빈 배열이 아니라 `null`** 이다. Day41 의 `for (File file : files)` 는 그 경우 `NullPointerException` 이고, 검사가 없다. `new File(".")` 은 늘 존재하므로 이 예제에서는 드러나지 않지만 **경로를 인자로 받는 코드로 바꾸는 순간 나타난다** → [[object-reference]]
- **`listFiles()` 의 순서는 정해져 있지 않다** — 이름순도 아니고 OS·파일 시스템에 따라 다르다. 출력이 정렬돼 보이는 것은 우연일 수 있으므로 순서가 필요하면 직접 정렬한다 → [[platform-dependency]]
- **`getTotalSpace()` 는 디렉토리의 크기가 아니라 파티션의 크기다 — Day41 필기의 오류다** — 주석이 「디렉토리에 전체 크기를 나타낸다」로 적혀 있지만 이 메서드가 돌려주는 것은 **그 경로가 속한 볼륨(디스크 파티션)의 총 바이트 수**다. `getFreeSpace()`·`getUsableSpace()` 도 같은 파티션의 남은 용량이고 그 디렉토리와 무관하다. **디렉토리 안의 내용을 합산하는 메서드는 `File` 에 없다** — `length()` 는 파일 하나의 크기이고 디렉토리에 대해서는 의미 있는 값이 아니라, 폴더 용량은 재귀로 훑어 직접 더해야 한다.
- **그 오류가 드러나지 않은 이유가 같은 줄의 오타다** — `"./src/main/jave"` 는 존재하지 않는 경로이고, `getTotalSpace()` 는 **경로가 파티션을 지목하지 못하면 `0` 을 돌려준다.** 그래서 필기의 관찰(「없는 디렉토리의 경우 0」)은 맞고, 세 값이 전부 `0` 으로 나왔기 때문에 **「디렉토리 크기라서 빈 디렉토리는 0」으로 읽어도 화면과 어긋나지 않았다.** `jave` 를 `java` 로 고치면 곧바로 수백 GB 가 찍혀 설명이 깨진다 — **오타가 잘못된 해석을 검증에서 숨긴 자리**이고, 「없으면 0」과 「디렉토리 크기」 두 문장이 우연히 같은 화면을 낸다 → [[filesystem-path]]
- **`length()` 는 디렉토리에 쓸 수 없고, 없는 파일에도 `0` 을 준다** — 그래서 `length() == 0` 은 「빈 파일」과 「없는 파일」과 「디렉토리」를 구별하지 못한다. `exists()`·`isFile()` 을 먼저 물어야 하는 이유다.
- **`lastModified()` 는 `Date` 가 아니라 `long` 이다** — 에포크(1970-01-01 UTC) 이후 밀리초이고, `0` 은 「1970년」이 아니라 **「모른다/없다」**를 뜻한다. Day41 이 `new Date(file.lastModified())` 로 감싸는 것이 그것을 사람이 읽는 값으로 바꾸는 자리이고, 없는 파일이면 `Thu Jan 01 09:00:00 1970` 이 찍힌다 → [[date-time]]
- **`equals()` 가 「같은 파일인가」를 답하지 않는다** — `File.equals` 는 **경로 문자열**을 비교하므로 `new File("./a.txt")` 와 `new File("a.txt")` 가 다르다고 나온다. 반대로 대소문자를 구별하지 않는 파일 시스템에서는 다른 문자열이 같은 파일이다. **`File` 을 `HashSet` 이나 `Map` 의 키로 쓰면 같은 파일이 두 번 들어간다** → [[object-equality]] · [[hash-based-collection]]
- **속성을 물은 시점과 쓰는 시점 사이에 파일이 바뀔 수 있다** — `if (file.exists()) { /* 읽는다 */ }` 사이에 다른 프로세스가 지울 수 있다. **`File` 은 스냅샷을 주는 것이 아니라 물을 때마다 조회하는 것**이고, 검사와 사용 사이의 틈은 문법으로 막을 수 없다. 그래서 「검사 후 사용」보다 **「해 보고 예외를 받는」** 쪽이 안전한 경우가 많다 → [[exception-handling]]
- **`java.io.File` 은 Java 7 의 `java.nio.file` 로 대체된 API 다** — `Path`·`Files` 가 같은 일을 하면서 실패 이유를 예외로 알려 주고, 심볼릭 링크·권한·파일 속성을 제대로 다루며 디렉토리 목록을 스트림으로 준다(`Files.list`). Day41 이 배우는 것은 **여전히 널리 쓰이지만 새 코드의 첫 선택은 아닌 층**이다.

## 함께 보는 개념

- [[filesystem-path]] — 이 객체가 들고 있는 이름의 종류
- [[io-stream]] — 파일의 내용을 다루는 쪽
- [[array]] — `listFiles()` 가 돌려주는 그릇
- [[lambda-expression]] — 필터를 인자로 넘기는 문법
- [[functional-interface]] — 그 필터의 타입
- [[date-time]] — `lastModified()` 의 밀리초를 감싸는 타입
- [[ternary-operator]] — `d`/`-` 를 고르는 자리
- [[exception-handling]] — `boolean` 과 예외로 실패가 갈리는 축
- [[object-equality]] — 같은 파일이 다르다고 나오는 자리
- [[hash-based-collection]] — 그 비교를 키로 쓰면 깨지는 곳
- [[object-reference]] — `listFiles()` 의 `null`
- [[platform-dependency]] — 목록 순서와 대소문자 구별이 갈리는 축
- [[serialization]] — 저장 파일의 존재 여부를 먼저 묻는 자리

## 출처

- [[2024-07-23-Day41]] — 「File클래스는 디렉토리나 파일을 다룰 때 사용하는 클래스이다」로 시작해 이름·속성·조작 세 무리를 예제로 훑는다. 속성 조회에 「없는 디렉토리/파일일 경우 false를 return」을 적어 대상이 없을 때의 동작을 정확히 관찰했지만, **`getTotalSpace()`·`getFreeSpace()`·`getUsableSpace()` 를 「디렉토리에 전체 크기」로 적어 파티션 용량을 디렉토리 용량으로 읽었다** — 예제 경로 `"./src/main/jave"` 가 오타로 존재하지 않아 세 값이 모두 `0` 으로 나오는 바람에 그 해석이 화면과 어긋나지 않았다. `mkdir()`/`mkdirs()` 의 차이를 정확히 설명하고도 차이가 나타나지 않는 예제(`new File("temp2")`)에 붙였고, `createNewFile()` 의 실패를 「디렉토리가 없다면 false」로 적었으나 그 경우는 `IOException` 이다. `listFiles()` 로 `ls -l` 형태를 조립하며 `new Date(file.lastModified())` 와 삼항 연산자를 쓰고, 필터 인자에 람다를 넘기는데 `null` 반환 검사는 없다

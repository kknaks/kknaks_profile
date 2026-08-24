---
type: concept
id: character-stream
title: 문자 스트림 (Reader / Writer)
aliases:
  - 문자 스트림
  - character stream
  - Reader
  - Writer
  - FileReader
  - FileWriter
  - 문자 기반 스트림
up:
  - 2024-07-19-Day39
  - 2024-07-22-Day40
  - 2024-07-23-Day41
tags:
  - java
  - 입출력
  - 인코딩
  - 파일
---

# 문자 스트림 (Reader / Writer)

**흐르는 단위가 바이트가 아니라 `char` 인 스트림.** 통로 자체는 여전히 바이트를 나르지만, 이 층이 **인코딩 규칙을 적용해 바이트↔문자 변환을 대신한다.** 그래서 위에서는 `String` 을 그대로 쓰고 읽는다 → [[io-stream]] · [[character-encoding]]

## 정의

Java 입출력은 같은 모양의 계열이 **두 벌** 있고, 갈리는 축이 「무엇이 흐르는가」다.

| | 바이트 계열 | 문자 계열 |
|---|---|---|
| 최상위 타입 | `InputStream` · `OutputStream` | `Reader` · `Writer` |
| 흐르는 단위 | `byte` (0~255) | `char` (UTF-16 코드 단위) |
| 파일 구현 | `FileInputStream` · `FileOutputStream` | `FileReader` · `FileWriter` |
| 인코딩 변환 | **없다** — 부르는 쪽이 `getBytes(...)` 로 한다 | **이 층이 한다** |
| 쓸 곳 | 이미지·`user.data` 같은 바이너리 | `user.csv` 같은 텍스트 |

`read()` 의 반환 타입은 두 계열 다 `int` 인데 담는 것이 다르다 — 바이트 계열은 0~255 와 `-1`, 문자 계열은 **0~65535 와 `-1`** 이다. 「값 하나 넓혀서 끝을 표시한다」는 방식은 같고 범위만 올라간 것이다.

Day39 는 이 계열을 쓰면서 **바이트 계열에서 하던 일이 없어지는 것**을 보여 준다.

| | Day38 (바이트 계열) | Day39 §3 (문자 계열) |
|---|---|---|
| 문자열 쓰기 | `out.write(name.getBytes(UTF_8))` | `out.write(user.toCsvString())` |
| 문자열 읽기 | `new String(buffer, 0, len, UTF_8)` | `in.nextLine()` |
| 인코딩 지정 | 코드에 있다 | **없다** (아래 「경계와 오해」) |

## 사용 예시

읽는 쪽은 `FileReader` 를 만들고 그 위에 `Scanner` 를 한 겹 더 끼운다.

```java
    try (Scanner in = new Scanner(new FileReader("user.csv"))) {
      while (true) {
        try {
          String csv = in.nextLine();
          userList.add(User.valueOf(csv));
        } catch (Exception e) {
          break;
        }
      }
```

**겹이 세 층이다** — 파일(바이트) → `FileReader`(문자) → `Scanner`(줄·토큰). Day09 에서 `new Scanner(System.in)` 으로 키보드를 감쌌던 것과 **같은 도구인데 안쪽만 바뀌었다** — `Scanner` 는 자기가 감싼 것이 키보드인지 파일인지 모른다 → [[standard-input]] · [[decorator-pattern]]

쓰는 쪽은 `FileWriter` 에 문자열을 그대로 넘긴다.

```java
    try (FileWriter out = new FileWriter("user.csv")) {
      for (User user : userList) {
        out.write(user.toCsvString() + "\n");
      }
    }
```

**`getBytes` 가 없다.** 바이트 계열이었다면 문자열을 바이트로 바꾸는 줄이 반드시 하나 있어야 했고, 그 줄에 인코딩을 적어야 했다 → [[binary-io]]

### 사흘 뒤 — `Scanner` 대신 `BufferedReader`, 그리고 끝 판정이 바뀐다

Day40 은 같은 자리를 다른 껍데기로 감싼다.

```java
    try (BufferedReader in = new BufferedReader(new FileReader("board.json"))) {
        StringBuilder strBuilder = new StringBuilder();
        String line;
        while ((line = in.readLine()) != null) {
            strBuilder.append(line);
        }
```

| | Day39 (`Scanner`) | Day40 (`BufferedReader`) |
|---|---|---|
| 한 줄 읽기 | `in.nextLine()` | `in.readLine()` |
| 파일 끝을 알리는 방법 | **예외** (`NoSuchElementException`) | **`null` 반환** |
| 끝 판정 코드 | `while (true) { try { … } catch (Exception e) { break; } }` | `while ((line = in.readLine()) != null)` |
| 값을 잘라 주는 기능 | 있다 (`nextInt` 등) | 없다 (줄만 준다) |

**Day39 의 「끝을 예외로 판정하면 끝과 깨짐이 같아진다」가 이 회차에서 사라진다.** `readLine()` 이 파일 끝을 `null` 로 알려 주므로 정상 종료와 오류가 같은 `catch` 로 들어오지 않는다 — 다만 그렇게 된 것은 설계를 고쳐서가 아니라 **JSON 을 쓰면서 도구가 바뀐 부수 효과**다 → [[exception-handling]] · [[json]]

그리고 이번에는 **버퍼를 감쌌다.** `FileReader` 를 그대로 쓰면 읽기가 잘게 나가는데, `BufferedReader` 가 덩어리로 읽어 두고 그 안에서 줄을 끊는다 — 「줄」이라는 개념이 이 껍데기에서 생기는 것이라 `readLine()` 이 `FileReader` 에는 없다 → [[decorator-pattern]] · [[io-stream]] · [[buffered-stream]]

### 하루 더 뒤 — 인코딩 인자가 코드로 돌아온다

**Day39·Day40 이 비워 둔 자리를 Day41 이 채운다.** 이 노트가 두 회차에 대해 「인코딩을 지정하지 않는다」로 지적한 것은 문법이 없어서가 아니라 쓰지 않았기 때문이었고, Day41 은 그 인자를 실제로 넘긴다.

```java
    Charset charset_MS949 = Charset.forName("MS949");
    FileWriter out = new FileWriter("temp/test2.txt", charset_MS949); 
```

```java
    FileReader in = new FileReader("sample/ms949.txt", Charset.forName("MS949"));
```

그리고 규칙까지 문장으로 적어 둔다 — 「파일 데이터를 읽을 때 인코더 정보를 알려줘야 한다」·「객체를 생성할 때 파일의 문자 집합을 지정하면, JVM 환경 변수 'file.encoding'에 설정된 문자집합을 무시한다」.

**두 문장이 이 노트의 「경계와 오해」 첫 항목의 답 그대로다.** 지정하면 환경 기본값을 밟지 않는다는 것, 그래서 같은 코드가 OS·JDK 버전에 따라 다르게 동작하는 경로가 닫힌다는 것 → [[character-encoding]] · [[platform-dependency]]

다만 **이 회차 안에서도 절반만 그렇다.** `Charset` 을 넘기는 것은 위의 두 예제뿐이고, `char[]` 을 쓰는 예제와 `read(buf)` 를 보는 예제는 여전히 `new FileWriter("temp/test2.txt")`·`new FileReader("temp/test2.txt")` 다. 그래서 그 예제들의 주석은 「JVM 환경 변수 'file.encoding'에 설정된 문자 코드표에 따라 변환하여 출력한다」로 **기본값에 맡긴 것을 자각한 채로** 적혀 있다 — 이 회차의 진짜 소득은 「항상 지정했다」가 아니라 **「지정하는 자리가 있고, 지정하면 기본값을 이긴다」를 알게 된 것**이다.

읽는 쪽 예제는 **바이트가 문자로 접히는 것을 한 줄씩 보여 준다.**

```java
    FileReader in = new FileReader("sample/ms949.txt", Charset.forName("MS949")); // 41 42 b0 a1 b0
    int ch1 = in.read(); // 41 => 0041('A')
    int ch2 = in.read(); // 42 => 0042('B')
    int ch3 = in.read(); // b0 a1 => ac00 => '가'
    int ch4 = in.read(); // b0 a2 => ac01 => '각'
```

**`read()` 를 네 번 불러 문자 네 개를 얻는데 파일에서는 6바이트가 소비됐다.** 이 층이 대신하는 일이 이 비대칭 하나로 다 보인다 — 바이트 계열이었다면 `read()` 여섯 번이고 어디서 끊어 붙일지를 부르는 쪽이 알아야 했다 → [[io-stream]] · [[character-encoding]]

## 왜 중요한가

**문자열을 형식으로 만드는 일과 저장하는 일이 분리된다.** `toCsvString()` 은 `String` 을 만들고, 그것이 몇 바이트인지·어떤 인코딩인지는 이 층이 정한다. Day38 이 「길이를 바이트로 세야 하는」 문제와 씨름한 이유의 절반이 이 층을 쓰지 않았기 때문이다 → [[csv]] · [[length-prefix-framing]]

**사람이 열어 고칠 수 있는 파일이 된다.** `user.data` 는 열어도 알 수 없었지만 `user.csv` 는 편집기로 보고 손으로 고칠 수 있다. 형식이 어긋났을 때 **어디가 어긋났는지 눈으로 찾을 수 있다**는 것이 바이너리 형식과 갈리는 실질적인 차이다.

**줄이 레코드 단위가 될 수 있다.** 문자 층에는 「줄」이라는 개념이 있어 `nextLine()`·`readLine()` 이 성립한다. 바이트 층에서는 `0x0A` 를 직접 찾아야 하고, 그 바이트가 멀티바이트 문자의 일부일 수 있는지까지 따져야 한다 → [[newline-character]]

## 경계와 오해

- **`new FileReader("user.csv")` 는 인코딩을 지정하지 않는다 — Day38 보다 뒤로 갔고, 나흘 뒤 Day41 이 되돌린다** — Day38 은 `StandardCharsets.UTF_8` 을 양쪽에 명시해서 규칙이 코드에 있었다. `FileReader`·`FileWriter` 를 이름만 넘겨 만들면 **기본 문자집합**을 쓰는데, 그 기본값은 JDK 18 이전에는 **실행 환경의 값**(Windows 면 MS949)이고 18 이후에는 UTF-8 로 고정됐다. 즉 **같은 코드가 OS 와 JDK 버전에 따라 다른 파일을 만들고 다르게 읽는다** — Windows 에서 저장한 `user.csv` 를 mac 에서 읽으면 한글이 깨지고, **코드는 한 줄도 다르지 않다.** 답은 `new FileReader(f, charset)`(Java 11+) 또는 `new InputStreamReader(new FileInputStream(f), UTF_8)` 이고, **Day41 이 그 형태를 쓰면서 「지정하면 `file.encoding` 을 무시한다」까지 문장으로 적는다** — 즉 Day39·Day40 에서 빠져 있던 것은 문법이 아니라 그 문법을 쓸 이유였고, 나흘 만에 필기 자체가 그것을 채운다. 다만 Day41 도 예제 절반은 이름만 넘기며, 그쪽에서는 「'file.encoding'에 설정된 문자 코드표에 따라」라고 **기본값에 맡긴 것을 자각한 채로** 적는다 → [[character-encoding]] · [[platform-dependency]]
- **`Writer.write(int)` 는 「2바이트를 출력한다」가 아니다 — Day41 필기의 오류다** — 필기가 그렇게 적고 예제 결과도 각각 2바이트(`b0 a1`·`ac 00`)라 확인처럼 보인다. 하지만 이 메서드가 하는 일은 **문자 하나를 내보내는 것**이고, 파일에 남는 바이트 수는 **문자집합이 정한다.** 예제가 고른 두 문자집합(MS949·UTF-16BE)이 한글을 우연히 둘 다 2바이트로 적는 것뿐이고, 같은 노트의 기본 문자집합(UTF-8) 예제에서는 「한글은 3바이트로 변환되어 출력될 것이고」라고 **필기가 직접 3바이트라 적어 놓았다.** 즉 두 문장이 같은 노트 안에서 어긋난다. 「2바이트」의 실체는 **`char` 하나의 크기**이지 출력 바이트 수가 아니고, 그것이 이 층의 정의(흐르는 단위가 `char`)와 「파일에 몇 바이트가 남나」를 가르는 자리다 → [[character-encoding]] · [[unicode]]
- **「buf가 full상태 일때 까지 읽어드린다」는 틀렸다 — 그리고 같은 예제가 그것을 반증한다** — `read(char[])` 는 **최대 배열 크기까지** 읽고 실제로 읽은 개수를 돌려준다. 다 채운다는 보장은 없다. 필기의 예제가 `char[] buf = new char[100]` 에 읽고 `count` 를 찍는데 **주석에 적힌 값이 `4`** 다 — 100을 채우지 않았다. 바로 다음 줄의 「리턴 값은 읽은 문자의 개수이다」가 맞는 설명이고 그 앞 줄이 틀린 것인데, **두 줄이 붙어 있어 모순이 눈에 보이는 상태로 남아 있다.** 바이트 계열에서 같은 오해가 더 위험한 것(파일·네트워크에서 짧게 읽힌다)과 같은 뿌리다 → [[io-stream]]
- **`read(buf, offset, len)` 로 읽으면 앞자리는 채워지지 않는다** — Day41 의 마지막 예제가 `in.read(buf, 10, 40)` 로 10번 자리부터 채우고서 **`for (int i = 0; i < 20; i++)` 로 0번부터 찍는다.** 앞의 10칸은 `char` 배열의 기본값 `\u0000`(널 문자) 이라 화면에 `(0000)` 열 줄이 먼저 나온다. 오프셋을 준 이유(앞자리에 다른 것을 넣으려고)와 출력 범위가 어긋난 것이고, **배열의 「채워진 구간」을 코드가 따로 들고 있어야 한다**는 것이 여기서도 같다 → [[array]] · [[default-initialization]]
- **`FileWriter` 를 다시 대입하면 앞의 것은 닫히지 않고 쓴 것도 남지 않는다** — Day41 의 `Charset` 예제가 정확히 그 형태다. `out` 에 MS949 스트림을 담아 `write(0xac00)` 을 부르고, 같은 변수에 UTF-16BE 스트림을 **덮어씌운다.** 사고가 세 겹으로 겹친다 — ① 첫 스트림을 아무도 닫지 않아 인코딩 버퍼의 `b0 a1` 이 디스크로 나가지 않고, ② 나갔다 해도 두 번째 `new FileWriter("temp/test2.txt", …)` 가 **같은 파일을 여는 순간 0바이트로 비우고**, ③ 두 번째 것도 닫지 않아 `ac 00` 마저 안 나간다. 그래서 주석이 적어 둔 두 결과(「text 파일 : b0 a1」·「text 파일 : ac 00」)는 **둘 다 나올 수 없고, 실행하면 빈 파일 하나가 남는다.** 예외는 없다. **인코딩을 비교하려던 예제가 인코딩이 아니라 자원 관리 때문에 결과를 못 보여 주는 자리**이고, `try (…)` 로 둘을 따로 쓰거나 파일 이름을 달리 주면 그대로 관찰된다 → [[try-with-resources]] · [[variable]]
- **문자 스트림에 바이너리를 흘리면 데이터가 되돌아오지 않는다** — 바이트 계열은 규칙을 모르니 아무 바이트나 옮기지만, 문자 계열은 **읽은 바이트를 문자로 해석**한다. 인코딩 규칙에 맞지 않는 바이트는 예외가 아니라 `U+FFFD`(�)로 **치환**되고, 그러면 원래 바이트가 무엇이었는지 알 수 없다. 이미지를 `FileReader` 로 읽어 `FileWriter` 로 복사하면 **크기도 내용도 다른 파일**이 나오고 예외는 없다. 「텍스트면 Reader, 아니면 Stream」이 취향이 아니라 규칙인 이유 → [[binary-io]]
- **`char` 하나가 글자 하나는 아니다** — `char` 는 UTF-16 **코드 단위** 16비트이고, 이모지처럼 보조 평면 문자는 두 개(서로게이트 쌍)로 표현된다. 그래서 문자 층으로 올라와도 「글자 수 = `char` 수」가 아니고, 한 글자 중간에서 자를 수 있다. **바이트 층의 「1바이트 ≠ 1문자」가 한 칸 올라와 같은 모양으로 남아 있다** → [[unicode]]
- **`Scanner` 는 `Reader` 가 아니다** — `Scanner` 는 `Readable` 을 감싸 **토큰·줄로 끊어 주는** 별개 층이고 `Reader` 계열을 상속하지 않는다. 그래서 「`Scanner` 를 쓰면 문자 스트림을 쓴 것」이 아니라 **문자 스트림 위에 파서를 하나 더 얹은 것**이다. `BufferedReader.readLine()` 이 같은 일을 더 얇게 한다 → [[standard-input]]
- **`Scanner` 를 닫으면 안쪽 `FileReader` 도 닫힌다** — 그래서 이 코드는 `Scanner` 하나만 `try (...)` 에 넣고도 파일 핸들이 남지 않는다. 반대로 **감싼 것을 안 닫고 안쪽만 닫으면** 껍데기가 들고 있던 것이 유실될 수 있다. Day09 에서 「`Scanner.close()` 가 `System.in` 까지 닫는다」로 만난 성질이 여기서는 이득이 된다 → [[try-with-resources]]
- **`FileWriter` 는 닫지 않으면 파일에 나가지 않을 수 있다** — 안에 인코딩 버퍼가 있어 `write()` 가 곧 디스크 쓰기가 아니다. `close()`(또는 `flush()`)가 남은 것을 내보내고, 그것을 잊으면 **예외도 없이 빈 파일이나 잘린 파일**이 남는다. `try (...)` 가 그 실수를 문법으로 막는 자리이고, **「닫기」가 자원 반납이 아니라 데이터 완결인 경우**다 → [[try-with-resources]]
- **문자 층에서는 길이 접두사 형식을 쓸 수 없다** — 이 층은 바이트 개수를 다루지 않으므로 「내용 앞에 바이트 길이를 적는다」가 성립하지 않는다(문자 수를 적어도 인코딩에 따라 바이트가 달라진다). 그래서 텍스트 형식은 **경계를 구분자로** 잡을 수밖에 없고, CSV 의 이스케이프 문제가 이 선택에서 따라온다. **통로를 문자 층으로 올린 것이 형식의 종류까지 정한 셈** → [[csv]] · [[length-prefix-framing]]
- **`FileWriter` 도 여는 순간 파일을 비운다** — 바이트 계열과 같다. 두 번째 인자로 `true` 를 주면 이어 쓴다. 이 코드는 매번 전체를 다시 쓰므로 문제가 없지만, **한 줄 추가로 저장할 수 있는 형식(CSV)인데도 그 이점을 쓰지 않는다** → [[csv]]
- **`Writer` 계열이라고 버퍼가 있는 것은 아니다 — 사흘 뒤 읽는 쪽만 고쳐진다** — 인코딩 버퍼는 성능 버퍼가 아니다. 줄마다 `write` 를 부르는 Day39 의 코드는 회원 수만큼 쓰기가 나가므로 `BufferedWriter` 를 한 겹 더 끼우는 것이 표준이다. **Day40 은 읽는 쪽에 `BufferedReader` 를 끼우면서 쓰는 쪽은 `new FileWriter(filename)` 그대로 둔다** — 대신 그 회차는 목록 전체를 한 문자열로 만들어 `write` 를 **한 번만** 부르므로 쓰기 횟수 문제 자체가 없어졌다. **버퍼가 필요한지는 「몇 번 부르는가」가 정하고, 형식을 바꾸면 그 답도 바뀐다** → [[io-stream]] · [[decorator-pattern]] · [[json]]
- **`BufferedReader` 는 `InputStream` 이 아니다 — Day40 필기의 오류다** — 필기가 「BufferedReader : 한줄 씩 읽어들이는 InputStream」이라고 적었는데 이것은 **`Reader` 계열**이다. 이름에 `Stream` 이 없는 것이 표시이고, 위 표의 두 계열이 갈리는 그 축이다. 바이트 쪽의 짝은 `BufferedInputStream` 이고 그쪽에는 `readLine()` 이 없다 — **「줄」은 문자 층에서만 성립하는 개념**이다 → [[io-stream]]
- **`readLine()` 이 `null` 을 주는 것은 빈 줄일 때가 아니라 파일이 끝났을 때다 — Day40 필기의 오류다** — 필기는 「빈 문자열 일 경우 null을 return한다」고 적었지만 빈 줄은 **길이 0 인 `String`**(`""`)이고 `null` 은 **더 읽을 것이 없을 때**만 나온다. 이 둘이 같다면 파일 중간의 빈 줄에서 읽기가 멈춰 **그 뒤 전부가 유실**된다 — Day39 의 「끝과 깨짐이 같아지는」 사고와 같은 모양이다. Day40 이 읽는 것은 한 줄로 된 JSON 이라 이 착각이 증상을 내지 않았고, **여러 줄 텍스트를 다룰 때 처음 드러날 종류의 오해**다 → [[json]] · [[string-comparison]]
- **`readLine()` 은 줄바꿈을 떼어 내고 준다 — 이어 붙이면 사라진다** — Day40 의 `strBuilder.append(line)` 은 줄바꿈을 넣지 않으므로 파일의 모든 줄이 **한 줄로 이어진다.** JSON 은 토큰 사이 공백이 의미가 없어 문제가 없지만, **줄이 레코드 경계인 형식(CSV)에 같은 코드를 쓰면 레코드가 전부 붙어 버린다.** 「줄을 읽어 모은다」가 「파일을 그대로 읽는다」가 아니라는 것 → [[newline-character]] · [[csv]]

## 함께 보는 개념

- [[io-stream]] — 바이트 계열과 이 계열이 갈리는 뿌리
- [[character-encoding]] — 이 층이 안에서 적용하는 규칙
- [[unicode]] — `char` 가 글자와 1:1 이 아닌 이유
- [[csv]] — 이 층 위에 올라가는 형식
- [[json]] — 사흘 뒤 같은 층에 올라가는 다음 형식
- [[binary-io]] — 이 층을 쓰면 안 되는 쪽
- [[data-io-stream]] — 바이트 계열에서 같은 「타입을 아는 층」 역할
- [[standard-input]] — 같은 `Scanner` 가 키보드를 감싸던 자리
- [[decorator-pattern]] — 세 겹으로 조립되는 구조
- [[try-with-resources]] — 닫기가 데이터 완결인 자리
- [[newline-character]] — 줄이 레코드 경계가 될 때 걸리는 것
- [[platform-dependency]] — 기본 문자집합이 갈리는 축
- [[buffered-stream]] — `BufferedReader` 가 속도 쪽에서 하는 일
- [[array]] — 오프셋을 주고 읽을 때 채워지는 구간
- [[default-initialization]] — 채우지 않은 앞자리에 남는 값

## 출처

- [[2024-07-19-Day39]] — csv 로 저장하는 절에서 `new Scanner(new FileReader("user.csv"))` 와 `new FileWriter("user.csv")` 를 써서 **바이트 계열에서 문자 계열로 통로를 갈아탄다.** `out.write(user.toCsvString() + "\n")` 처럼 문자열을 그대로 넘기고 `in.nextLine()` 으로 줄 단위로 되읽어 **Day38 의 `getBytes`·`new String(...)` 두 줄이 사라진다.** 다만 인코딩을 인자로 넘기지 않아 Day38 이 명시했던 `StandardCharsets.UTF_8` 이 코드에서 없어졌고(기본 문자집합에 맡겨진다), 버퍼 스트림도 끼우지 않는다 — 필기는 이 두 가지를 다루지 않았다
- [[2024-07-22-Day40]] — JSON 저장·로딩에서 같은 문자 계열을 쓰면서 껍데기가 `Scanner` 에서 `BufferedReader` 로 바뀐다. `new BufferedReader(new FileReader("board.json"))` 와 `while ((line = in.readLine()) != null)` 이 **파일 끝을 예외가 아니라 `null` 로 판정**하게 만들어 Day39 의 「끝과 깨짐이 같아지는」 구조가 없어졌고, 읽는 쪽에 처음으로 버퍼가 끼워졌다. 쓰는 쪽은 `new FileWriter(filename)` 그대로이며 인코딩을 명시하지 않는 것도 Day39 와 같다. 필기는 `BufferedReader` 를 「한줄 씩 읽어들이는 InputStream」이라 적고 `readLine()` 이 「빈 문자열 일 경우 null을 return한다」고 적었는데 **둘 다 어긋난다** — `Reader` 계열이고, `null` 은 파일 끝의 표시다
- [[2024-07-23-Day41]] — 실습이 아니라 강의로 이 계열을 다시 훑으면서 **인코딩 인자를 코드에 되돌린다** — `new FileWriter(path, Charset.forName("MS949"))`·`new FileReader(path, Charset.forName("MS949"))` 를 쓰고 「지정하면 'file.encoding'에 설정된 문자집합을 무시한다」로 규칙까지 적어, Day39·Day40 에서 빠져 있던 것이 문법이 아니라 그것을 쓸 이유였음을 스스로 채운다(예제 절반은 여전히 이름만 넘기며, 그쪽 주석은 기본값에 맡긴 것을 자각하고 있다). `read()` 를 네 번 불러 6바이트를 소비하며 `b0 a1 => ac00 => '가'` 로 **바이트가 문자로 접히는 과정**을 한 줄씩 적어 이 층이 하는 일을 눈에 보이게 했다. 어긋난 것 셋 — `write(int)` 를 「2바이트를 출력한다」로 적었으나 나가는 바이트 수는 문자집합이 정하고 같은 노트가 UTF-8 에서는 3바이트라 적어 두었다, 「buf가 full상태 일때 까지 읽어드린다」는 바로 다음 줄의 「리턴 값은 읽은 문자의 개수」와 모순이며 예제의 `count` 가 `4` 로 그것을 반증한다, `Charset` 비교 예제는 `FileWriter` 를 닫지 않고 같은 파일에 다시 대입해 **주석에 적힌 두 결과가 둘 다 나올 수 없다.** 마지막 예제는 `read(buf, 10, 40)` 로 채우고 0번부터 출력해 앞 열 칸의 기본값을 함께 찍는다

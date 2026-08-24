---
type: concept
id: csv
title: CSV (구분자 기반 텍스트 형식)
aliases:
  - CSV
  - csv 포맷
  - 구분자
  - 구분자 형식
  - 구분자 기반 형식
  - delimiter
  - comma-separated values
up:
  - 2024-07-19-Day39
tags:
  - 데이터
  - 파일
  - 형식
  - 입출력
---

# CSV (구분자 기반 텍스트 형식)

**값 사이에 약속한 글자를 끼워 넣어 경계를 표시하는 텍스트 형식.** Day39 의 한 줄이 정의 전부다 — 「객체 정보를 ","로 구분한다」. 레코드는 줄바꿈으로, 필드는 콤마로 가른다. **길이를 적는 대신 끝을 표시하는 쪽**이고, 그 선택이 이 형식의 장점과 함정을 모두 만든다 → [[length-prefix-framing]]

## 정의

레코드 하나가 한 줄이고, 필드 순서가 곧 사양이다.

```text
user.csv
1,홍길동,hong@test.com,1111,010-1111-2222
2,이건학,lee@test.com,2222,010-2222-3333
└┬┘└─┬─┘└────┬─────┘└─┬─┘└──────┬──────┘
 no  name    email  password    tel        ← 이 순서가 유일한 사양서다
```

Day38 의 바이너리 형식과 같은 자리에 무엇이 오는지 나란히 보면 이 형식의 정체가 드러난다.

| | Day38 (길이 접두사) | Day39 §3 (구분자) |
|---|---|---|
| 필드 경계 | 앞에 **길이 2바이트** | 사이에 **`,`** |
| 레코드 경계 | 앞에 **길이 2바이트** | 끝에 **`\n`** |
| 전체 개수 | 맨 앞에 2바이트 | **없다** — 끝까지 읽는다 |
| 읽는 방법 | 「그만큼 떼어 낸다」 (계산) | 「구분자를 찾는다」 (탐색) |
| 내용에 구분자가 오면 | 상관없다 | **형식이 무너진다** |

그리고 대칭 구조는 그대로 남는다 — 형식이 코드 두 개에 흩어져 있고 그 둘이 거울이어야 한다.

| 방향 | 메서드 |
|---|---|
| 직렬화 | `String toCsvString()` |
| 역직렬화 | `static User valueOf(String csv)` |

**`valueOf` 라는 이름이 Day38 에서 돌아왔다.** Day38 의 `valueOf(byte[])` 는 §1 에서 지워졌고 여기서 `valueOf(String)` 이 들어온다 — **같은 정적 팩토리 이름이 형식마다 오버로드되는 자리**다 → [[serialization]] · [[method]]

## 사용 예시

내보내는 쪽은 필드를 콤마로 이어 붙인다.

```java
  public String toCsvString() {
    return new StringBuilder().append(no).append(",").append(name).append(",").append(email)
        .append(",").append(password).append(",").append(tel).toString();
  }
```

`no` 가 `int` 인데 `append` 로 그대로 들어가는 것이 이 형식의 성격을 보여 준다 — **모든 값이 문자열로 평평해진다** → [[string-builder]]

되읽는 쪽은 잘라서 순서대로 꽂는다.

```java
  public static User valueOf(String csv) {
    String[] values = csv.split(","); // csv: "1,홍길동,hong@test.com,1111,010-1111-2222"
    User user = new User();
    user.setNo(Integer.parseInt(values[0]));
    user.setName(values[1]);
    user.setEmail(values[2]);
    user.setPassword(values[3]);
    user.setTel(values[4]);
    return user;
  }
```

**`Integer.parseInt` 가 첫 필드에만 있다.** 텍스트 형식에는 타입이 적혀 있지 않으므로 **어느 칸이 숫자인지는 읽는 코드만 안다** — 바이너리에서 `readInt` 가 대신해 주던 일이 여기서는 손으로 돌아온다 → [[number-parsing]] · [[data-io-stream]]

파일 층은 줄을 세는 것이 전부다.

```java
    try (FileWriter out = new FileWriter("user.csv")) {
      for (User user : userList) {
        out.write(user.toCsvString() + "\n");
      }
    }
```

```java
      while (true) {
        try {
          String csv = in.nextLine();
          userList.add(User.valueOf(csv));
        } catch (Exception e) {
          break;
        }
      }
```

**Day38 이 회원 수를 맨 앞에 적었던 것과 달리 개수가 없다** — 「더 읽을 것이 없을 때까지」로 끝을 잡고, 그것을 판정하는 수단이 이 코드에서는 **예외**다(아래 「경계와 오해」) → [[exception-handling]] · [[character-stream]]

## 왜 중요한가

**파일을 열어서 확인하고 손으로 고칠 수 있다.** Day38 의 `user.data` 는 형식이 어긋나면 「틀린 값만 보이고 어디가 틀렸는지 안 보이는」 상태였다. CSV 는 편집기로 열면 어느 줄 어느 칸이 잘못됐는지 눈에 보이고, 시험 데이터를 손으로 만들어 넣을 수도 있다. **디버깅 비용이 형식 선택으로 정해진다** → [[binary-io]]

**다른 도구와 교환된다.** 엑셀·DB 임포트·쉘 도구(`cut`·`sort`)가 전부 이 형식을 읽는다. 손으로 만든 바이너리 형식은 **그 형식을 아는 코드가 내 코드뿐**이라 다른 도구에 넘길 방법이 없다.

**한 줄만 덧붙이는 저장이 가능해진다.** 개수를 앞에 적지 않았으므로 회원 한 명이 늘 때 파일 끝에 한 줄을 이어 붙이면 되고, 앞을 고칠 필요가 없다. Day38 의 형식은 맨 앞 개수 때문에 매번 전체를 다시 써야 했다. **형식이 정하는 것은 읽는 방법만이 아니라 갱신하는 방법**이고, 다만 Day39 의 코드는 여전히 전체를 다시 쓴다 → [[character-stream]]

## 경계와 오해

- **구분자 ≠ 길이 접두사 — 그리고 이 코드는 내용에 콤마가 오는 경우를 막지 않는다** — 이름이 `홍,길동` 이면 저장된 줄이 `1,홍,길동,hong@test.com,1111,010-1111-2222` 가 되고 `split(",")` 이 **6조각**을 준다. `values[1]`=`홍`, `values[2]`=`길동`, `values[3]`=`hong@test.com`, `values[4]`=`1111` — **이름 뒤 모든 필드가 한 칸씩 밀려 이메일 자리에 이름 조각이, 전화번호 자리에 비밀번호가 들어간다.** 조각이 5개 이상이라 **예외도 나지 않고**, 그 상태로 다시 저장하면 마지막 필드가 잘려 **왕복 한 번에 전화번호가 영구히 사라진다.** 길이 접두사 형식이 「내용을 검사하지 않는다」였던 것의 정확한 반대편이다 → [[length-prefix-framing]]
- **표준 CSV 에는 이스케이프 규칙이 있고 `split(",")` 은 그것을 모른다** — RFC 4180 은 값에 콤마·따옴표·줄바꿈이 있으면 **값 전체를 `"` 로 감싸고 안의 `"` 는 `""` 로 겹쳐 쓰도록** 정한다. 그래서 엑셀이 만든 CSV 를 이 코드로 읽으면 따옴표째 필드에 들어오고, 콤마가 든 값은 위 항목의 경로로 무너진다. **「CSV 를 만들었다」와 「CSV 를 지켰다」가 다르고**, 구분자 방식이 「단순하다」는 인상은 이 규칙을 빼놓았을 때만 성립한다.
- **`split` 은 끝에 있는 빈 필드를 버린다 — 빈 값 하나가 로딩 전체를 끊는다** — 전화번호를 입력하지 않은 회원의 줄은 `5,홍길동,hong@test.com,1111,` 이고 `split(",")` 은 **4조각**을 준다(뒤쪽 빈 문자열이 잘린다). `values[4]` 가 `ArrayIndexOutOfBoundsException` 이고, 그것이 아래 항목의 `catch (Exception e) → break` 로 들어가 **그 줄부터 뒤의 모든 회원이 목록에서 사라진다.** `csv.split(",", -1)` 로 한계를 풀거나 조각 수를 검사해야 하는데 둘 다 없다 → [[array]]
- **끝을 예외로 판정하면 「끝」과 「깨짐」이 같아진다** — `while (true) { try { in.nextLine(); … } catch (Exception e) { break; } }` 는 파일 끝(`NoSuchElementException`)에서 나오려고 쓴 것인데, **`Integer.parseInt` 실패·조각 부족도 같은 `catch` 로 들어와 똑같이 `break`** 한다. 중간 한 줄이 깨지면 **거기서 읽기를 멈추고 뒤를 버리며 아무 메시지도 남지 않는다.** 그리고 다음 저장이 그 잘린 목록으로 파일을 덮어써 **손실이 확정된다.** `while (in.hasNextLine())` 으로 끝을 판정하고 줄 단위 오류는 따로 다루는 것이 답이다 — 「끝났는가」와 「틀렸는가」는 다른 물음이다 → [[exception-handling]] · [[while-loop]]
- **값 안의 줄바꿈은 레코드 경계를 부순다** — 필드에 개행이 들어가면 한 회원이 두 줄이 되고 양쪽 다 조각 수가 안 맞는다. **레코드 경계와 필드 경계가 둘 다 「내용에 나올 수 있는 글자」**라는 것이 이 형식의 근본 성질이고, 그래서 표준이 따옴표 규칙을 둔 것이다 → [[newline-character]]
- **`"\n"` 을 직접 적은 것은 OS 기본 줄바꿈과 다를 수 있다** — `System.lineSeparator()` 는 Windows 에서 `\r\n` 이다. 읽는 쪽 `Scanner` 는 `\n`·`\r\n` 을 모두 줄 구분으로 보므로 **이 프로그램 안에서 왕복은 성립하지만**, 그 파일을 줄바꿈을 하나로 가정한 다른 도구에서 열면 한 줄로 보이거나 마지막 필드에 `\r` 이 붙어 들어온다. 형식이 프로그램 밖으로 나가는 순간 걸리는 축 → [[newline-character]] · [[platform-dependency]]
- **필드 순서 말고 사양이 아무것도 없다** — 헤더 줄도, 버전도, 타입 표시도 없다. `User` 에 필드를 하나 더하면 옛 파일은 조각이 하나 부족한 상태로 위의 예외 경로로 들어가고, **읽는 쪽은 「형식이 다르다」와 「데이터가 깨졌다」를 구별할 수 없다.** Day38 의 바이너리 형식이 갖고 있던 문제가 텍스트로 옮겨 와도 그대로다 — **사람이 읽을 수 있게 된 것이 형식이 자기를 설명하게 된 것은 아니다** → [[serialization]]
- **사람이 읽을 수 있다는 것은 비밀번호도 읽힌다는 뜻이다** — `user.csv` 를 열면 `1111` 이 그대로 보인다. `user.data` 에도 평문으로 들어 있었지만 도구 없이는 안 보였고, 형식을 텍스트로 바꾸면서 **같은 데이터의 노출 수준이 올라갔다.** 형식 선택이 보안 결정이 되는 자리이고, 애초에 비밀번호를 그대로 저장하는 것이 문제라는 것은 이 실습 범위 밖에 남아 있다.
- **개수를 안 적은 것의 대가는 「몇 명인지 미리 모른다」다** — Day38 은 `for (int i = 0; i < userLength; i++)` 로 돌 수 있었고 배열을 미리 잡을 수도 있었다. 여기서는 끝까지 읽어 봐야 알고, **파일이 중간에서 잘려도 그것이 잘린 것인지 원래 그만큼인지 알 방법이 없다.** 이어 붙이기가 가능해진 것과 같은 성질의 뒷면이다 → [[length-prefix-framing]]
- **`maxUserNo` 를 세는 방식은 Day38 그대로라 지운 번호가 되살아난다** — 로딩 끝에 `User.initSeqNo(maxUserNo)` 로 발급기를 되살리지만, 남아 있는 회원의 최댓값을 세는 것이라 5번을 지운 뒤 저장하면 다음 실행에서 새 회원이 5번을 다시 받는다. **형식을 세 번 바꿨는데(손코드 → Data I/O → CSV) 이 결함은 세 번 다 같은 모양으로 남아 있다** — 형식의 문제가 아니라 **카운터를 저장하지 않은 문제**라서 그렇다 → [[surrogate-key]] · [[static-member]]

## 함께 보는 개념

- [[length-prefix-framing]] — 같은 문제에 반대로 답하는 형식
- [[character-stream]] — 이 형식이 올라가는 통로
- [[serialization]] — 이 형식을 만들고 되돌리는 작업
- [[binary-io]] — 사람이 못 읽는 쪽과의 대비
- [[data-io-stream]] — 타입을 형식이 들고 있던 쪽
- [[number-parsing]] — 텍스트에서 숫자를 되살리는 비용
- [[string-builder]] — 줄을 만드는 도구
- [[exception-handling]] — 끝 판정을 예외에 맡긴 자리
- [[newline-character]] — 레코드 경계가 걸리는 축
- [[array]] — `split` 결과의 조각 수가 형식 검사가 되는 자리
- [[surrogate-key]] — 형식을 바꿔도 남는 발급기 복원 문제

## 출처

- [[2024-07-19-Day39]] — 「객체 정보를 ","로 구분한다」 한 줄로 형식을 정하고, `User.toCsvString()`(`StringBuilder` 로 콤마 연결)과 `User.valueOf(String csv)`(`split(",")` 후 순서대로 setter)로 왕복을 짰다. 파일 층은 `FileWriter` 에 줄마다 `toCsvString() + "\n"` 을 쓰고 `Scanner.nextLine()` 으로 되읽으며, **회원 수 접두사가 없어지고 끝 판정을 `catch (Exception e) → break` 가 맡는다.** 필기는 콤마가 값에 들어오는 경우·빈 필드·표준 CSV 의 따옴표 규칙을 다루지 않았고, 로딩 끝의 `User.initSeqNo(maxUserNo)` 는 Day38 과 같은 「남은 회원의 최댓값을 센다」 방식으로 그대로 남아 있다

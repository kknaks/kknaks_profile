---
type: concept
id: json
title: JSON (JavaScript Object Notation)
aliases:
  - JSON
  - json
  - json 포맷
  - Gson
  - gson
  - toJson
  - fromJson
  - GsonBuilder
up:
  - 2024-07-22-Day40
tags:
  - 데이터
  - 형식
  - 입출력
  - 라이브러리
---

# JSON (JavaScript Object Notation)

**이름과 값을 짝으로 적고 중괄호·대괄호로 중첩을 표현하는 텍스트 형식.** [[csv]] 가 「값 사이에 구분자를 끼우는」 쪽이었다면 이쪽은 **각 값에 이름을 붙이는** 쪽이고, 그 하나의 차이가 형식의 성질을 전부 갈라 놓는다. Day40 은 이 형식을 손으로 만들지 않고 **Gson** 에 맡긴다 — 필기의 정의는 「구글에서 만든 Json포맷 입출력 라이브러리」다.

## 정의

같은 데이터를 세 형식으로 놓으면 이 형식이 무엇을 사서 무엇을 지불하는지 한눈에 보인다.

```text
Day38 (길이 접두사)   [00 00 00 01][00 09]홍길동...      ← 사람이 못 읽는다
Day39 (CSV)          1,홍길동,hong@test.com,1111        ← 순서가 유일한 사양서다
Day40 (JSON)         {"no":1,"name":"홍길동","email":"hong@test.com","password":"1111"}
                      └─ 이름이 값과 함께 파일에 들어간다 ─┘
```

| | Day39 (CSV) | Day40 (JSON) |
|---|---|---|
| 필드를 식별하는 것 | **위치** | **이름** |
| 필드 순서가 바뀌면 | 무너진다 | 상관없다 |
| 필드가 하나 늘면 | 옛 파일이 조각 부족으로 깨진다 | 없는 필드는 기본값으로 남는다 |
| 값에 `,`·줄바꿈이 있으면 | 형식이 무너진다 | 이스케이프로 처리된다 |
| 중첩 구조 (객체 안의 객체·목록) | **표현할 수 없다** | 표현된다 |
| 형식을 짜는 코드 | `toCsvString`/`valueOf` 두 개 | **없다** (라이브러리가 한다) |
| 파일 크기 | 작다 | 이름이 레코드마다 반복돼 크다 |

**마지막에서 두 번째 줄이 Day40 이 실제로 얻은 것이다.** Day38 부터 세 번 손으로 짜 온 「형식을 만드는 코드」가 이 회차에 **사라진다** → [[serialization]]

Gson 의 표면은 메서드 두 개다.

| 방향 | 호출 |
|---|---|
| 직렬화 | `gson.toJson(객체)` → `String` |
| 역직렬화 | `gson.fromJson(문자열, 타입)` → 객체 |

되돌릴 때 **타입을 넘겨야 한다**는 것이 이 API 의 핵심이다. 문자열만 봐서는 `List<Board>` 인지 `List<User>` 인지 알 수 없고, 실행 시점에는 제네릭 타입 인자가 지워져 있어 `List<Board>.class` 같은 것도 없다. 그래서 `TypeToken` 이 등장한다 → [[type-erasure]]

## 사용 예시

라이브러리를 쓰겠다는 선언이 먼저다.

```gradle
{ implementation 'com.google.code.gson:gson:2.11.0' }
```

**`그룹:이름:버전` 좌표 한 줄이 전부다** → [[gradle]]

저장하는 쪽은 세 줄이다.

```java
    private void saveBoards() {
        try (FileWriter out = new FileWriter("board.json")) {
        Gson gson = new Gson();
        out.write(gson.toJson(boardList));
        } catch (IOException e) {
        System.out.println("게시글 정보 저장 중 오류 발생!");
    }
}
```

**`for` 문이 없다.** CSV 는 레코드마다 줄을 만들어 썼는데(`for (User user : userList) out.write(...)`) 여기서는 **목록 전체가 한 문자열**이 된다 → [[csv]] · [[character-stream]]

읽는 쪽은 파일 전체를 문자열로 모은 뒤 되돌린다.

```java
private void loadBoards() {
    try (BufferedReader in = new BufferedReader(new FileReader("board.json"))) {
        StringBuilder strBuilder = new StringBuilder();
        String line;
        while ((line = in.readLine()) != null) {
            strBuilder.append(line);
        }
        boardList.addAll(new Gson().fromJson(strBuilder.toString(), new TypeToken<List<Board>>() {
        }));
        ...
```

**`new TypeToken<List<Board>>() {}` 의 빈 중괄호가 「무엇으로 되돌릴지」를 넘기는 수단이다** → [[type-erasure]] · [[anonymous-class]]

기본 설정으로는 날짜가 사람용 영어 표기로 나간다. 필기가 그것을 보고 형식을 지정한다.

```text
json파일에 데이터 타입이 "createdDate":"Jul 22, 2024, 5:13:25 PM"으로 출력이 된다.
```

```java
new GsonBuilder().setDateFormat("yyyy-MM-dd HH:mm:ss").create()
```

**JSON 표준에 날짜 타입이 없기 때문에 생기는 일이다.** 숫자·문자열·불리언·`null`·객체·배열이 전부이므로 시각은 **문자열로 적고 형식을 약속**해야 한다 → [[date-time]]

그리고 세 벌로 복사돼 있던 저장·로딩이 제네릭 메서드 한 벌로 합쳐진다.

```java
  private <E> void loadJson(List<E> list, String filename, Class<E> elementType) {
      ...
      list.addAll((List<E>) new GsonBuilder().setDateFormat("yyyy-MM-dd HH:mm:ss").create()
          .fromJson(strBuilder.toString(),
              TypeToken.getParameterized(List.class, elementType).getType()));

      for (Class<?> type : elementType.getInterfaces()) {
        if (type.equals(InitSeqNo.class)) {
          intintSeqNo(list, elementType);
        }
      }
```

```java
  private void loadData() {
    loadJson(userList, "user.json", User.class);
    loadJson(projectList, "porject.json", Project.class);
    loadJson(boardList, "board.json", Board.class);
  }
```

**형식이 라이브러리로 넘어가자 남은 코드가 타입만 다른 세 벌이 되었고, 그것을 제네릭이 하나로 접었다** — 이 회차의 두 주제가 여기서 만난다 → [[generics]] · [[class-metadata]]

## 왜 중요한가

**형식을 짜는 코드가 통째로 사라진다.** Day38 의 `getBytes`/`valueOf(byte[])`, Day39 의 `toCsvString`/`valueOf(String)` 이 하던 일이 `toJson`/`fromJson` 두 호출로 대체되고, **필드를 하나 더할 때 고칠 곳이 없다.** 손으로 짠 형식에서 「양쪽을 거울로 유지해야 한다」가 가장 큰 비용이었는데 그 비용이 0 이 된다 → [[serialization]]

**필드 이름이 파일에 들어가서 형식이 자기를 설명한다.** CSV 에서 「필드 순서 말고 사양이 아무것도 없다」가 문제였고, 필드를 더하면 옛 파일이 깨졌다. JSON 은 없는 필드를 기본값으로 두고 모르는 필드를 무시하므로 **옛 파일과 새 코드가 같이 살 수 있다.** 스키마가 조금씩 변하는 데이터에 이 형식이 쓰이는 이유다 → [[csv]]

**구분자 사고가 형식 차원에서 없어진다.** 이름이 `홍,길동` 이어도 문자열이 따옴표 안에 있고 라이브러리가 이스케이프를 처리하므로 필드가 밀리지 않는다. Day39 의 `split(",")` 이 **값에 콤마가 있으면 전화번호를 영구히 잃던** 경로가 사라진다 — **직접 쓴 파서를 버리는 것으로 얻는 것이 이것이다.**

**중첩을 표현할 수 있다.** 게시글 안에 작성자 객체를, 프로젝트 안에 팀원 목록을 넣을 수 있다. CSV 는 표 한 장이라 관계를 표현하려면 파일을 나누고 번호로 잇는 수밖에 없었다 → [[db-normalization]]

## 경계와 오해

- **JSON ≠ Gson** — 앞은 형식(문법 규칙)이고 뒤는 그 형식을 다루는 구글의 라이브러리다. 필기가 Gson 부터 시작해서 둘이 붙어 보이는데, 같은 JSON 을 Jackson·org.json 으로도 다루고 다른 언어에서도 읽는다. **`toJson`·`TypeToken`·`GsonBuilder` 는 Gson 의 이름이고 JSON 의 개념이 아니다** — 라이브러리를 갈아 끼우면 이 이름들이 전부 바뀐다.
- **`saveJson` 의 날짜 형식이 소문자 `mm` 이다 — 저장할 때마다 연도가 1년씩 밀린다** — 합쳐진 메서드 두 개가 형식 문자열을 따로 들고 있고 **`loadJson` 은 `"yyyy-MM-dd HH:mm:ss"`, `saveJson` 은 `"yyyy-mm-dd HH:mm:ss"`** 다. `mm` 은 월이 아니라 **분**이므로 2024-07-22 17:13:25 은 `"2024-13-22 17:13:25"` 로 저장된다(월 자리에 분 13 이 들어간다). 되읽는 쪽은 그것을 `MM` 으로 읽어 **13월** 로 해석하고, `SimpleDateFormat` 은 기본이 lenient 라 예외 없이 **다음 해 1월** 로 넘긴다 → `2025-01-22`. **다음 저장은 그 값을 다시 `2025-13-22` 로 적고, 그것이 2026-01-22 이 된다** — **프로그램을 켜고 끌 때마다 작성일이 1년씩 미래로 가고 월은 1월에 고정된다.** 예외도 경고도 없고, 형식 문자열의 대소문자 한 글자다. 그리고 이 결함은 **「JSON 포맷 입출력」의 `saveBoards` 에는 없다** — 세 벌을 한 벌로 접는 그 리팩터링에서 새로 들어왔다. **중복을 없애는 작업이 오히려 양쪽 형식을 갈라 놓은 것**이고, 형식을 상수 하나로 뽑았다면 생길 수 없는 종류의 사고다 → [[date-time]] · [[refactoring]]
- **`fromJson` 은 빈 파일에 `null` 을 돌려주고, 그 `null` 이 `addAll` 에서 터진다** — 파일이 있는데 내용이 비면(저장이 중간에 실패한 경우) `strBuilder.toString()` 이 `""` 이고 `fromJson("")` 은 예외가 아니라 **`null`** 이다. `boardList.addAll(null)` → **`NullPointerException`.** `loadBoards` 의 `catch` 는 **`IOException` 뿐**이라 이 예외는 잡히지 않고 프로그램을 죽인다. 「Generic 적용하기」의 `loadJson` 이 `catch (Exception e)` 로 넓혀진 것이 그 구멍을 (의도했든 아니든) 덮는다. **「예외가 나지 않는다」가 「성공했다」가 아닌 자리** → [[exception-handling]]
- **없는 필드는 오류가 아니라 `null` 로 남는다 — CSV 와 반대 방향의 위험이다** — CSV 는 조각이 부족하면 `ArrayIndexOutOfBoundsException` 으로 **시끄럽게** 실패했다. JSON 은 `{"no":1}` 만 있어도 통과하고 `name`·`email` 이 `null` 인 객체가 만들어진다. **깨진 데이터가 조용히 프로그램 안으로 들어오고**, 터지는 곳은 그것을 쓰는 먼 코드다. 「형식이 견고하다」와 「데이터가 유효하다」는 다른 문제이고, 후자는 여전히 손으로 검사해야 한다 → [[csv]]
- **`fromJson` 은 생성자를 부르지 않을 수도 있다** — Gson 은 기본 생성자가 있으면 쓰고, 없으면 JVM 내부 수단으로 **생성자를 건너뛰고** 객체를 만든다. Day39 의 `readObject` 에서 만난 성질이 라이브러리를 바꿔도 그대로 남는 것이고, **생성자에 넣어 둔 검사가 역직렬화 경로에서는 실행되지 않는다** → [[constructor]] · [[serialization]]
- **파일 전체를 문자열로 만드는 층이 필요 없다** — `BufferedReader` + `StringBuilder` + `while` 이 하는 일을 `fromJson(Reader, Type)` 한 호출이 대신한다(`new Gson().fromJson(in, type)`). 지금 코드는 **파일 크기만큼의 문자열을 메모리에 한 번 더 만들고** 그 위에 파서를 돌린다. 대형 파일에서는 이 층이 그대로 비용이고, 스트리밍 파서를 쓰면 아예 필요가 없다 → [[character-stream]] · [[string-builder]]
- **`Gson` 인스턴스를 호출마다 새로 만든다** — `new GsonBuilder()...create()` 가 `loadJson`·`saveJson` 안에 있어 파일 세 개를 다루면 여섯 번 만들어진다. Gson 인스턴스는 **타입별 어댑터를 안에 캐시하고 스레드 안전**해서 한 번 만들어 재사용하는 것이 정석이다. 「매번 만들어도 동작은 같다」가 「매번 만들어도 된다」는 뜻이 아닌 자리 → [[caching]] · [[singleton-pattern]]
- **`porject.json` 오타가 저장·로딩 양쪽에 있다** — 그래서 왕복은 성립하고 아무 증상도 없다. **양쪽이 같이 틀려서 드러나지 않는 종류의 오류**이고, 파일 이름이 두 곳에 문자열로 박혀 있는 구조가 원인이다(상수 하나였다면 오타가 있어도 이름은 하나였다).
- **JSON 은 주석도 후행 콤마도 허용하지 않는다** — 「사람이 열어 고칠 수 있다」가 CSV 만큼 자유롭지 않다. 손으로 고치다 콤마를 하나 남기면 `JsonSyntaxException` 이고, 어느 줄인지 찾아야 한다. 반대로 형식이 엄격해서 **깨진 것이 깨진 것으로 드러난다** — CSV 가 조용히 필드를 밀던 것과 대비된다.
- **파일이 커진다** — 필드 이름이 레코드마다 반복되므로 같은 데이터가 CSV 보다 몇 배 크고 Day38 의 바이너리보다 훨씬 크다. **사람이 읽을 수 있음과 크기를 맞바꾼 것**이고, 그래서 대량 전송에는 Protobuf 같은 바이너리 형식이 쓰인다 → [[binary-io]] · [[length-prefix-framing]]
- **비밀번호가 여전히 평문으로 보인다** — CSV 에서 지적된 것이 그대로다. 형식을 바꾼 것은 **표현**이고 저장하는 **내용**은 세 회차 동안 한 번도 바뀌지 않았다.
- **발급기 복원 문제가 네 번째 형식에서도 그대로다** — `Board.initSeqNo(maxBoardNo)` 는 여전히 「남아 있는 것의 최댓값」을 세므로 5번을 지우고 저장하면 다음 실행에서 5번이 재발급된다. `loadJson` 은 그것을 `getInterfaces()` + `getMethod("initSeqNo", int.class)` 로 **일반화까지** 했는데, 일반화된 것은 「어떻게 부르는가」이고 **「무엇을 세는가」의 결함은 함께 복사됐다.** 그 위에 `getInterfaces()` 는 **직접 구현한 인터페이스만** 돌려주므로 `InitSeqNo` 를 부모 클래스가 구현했다면 조건문이 거짓이 되어 **복원 자체가 조용히 건너뛰어진다** → [[surrogate-key]] · [[class-metadata]] · [[static-member]]

## 함께 보는 개념

- [[csv]] — 위치로 식별하던 앞 형식
- [[serialization]] — 이 형식이 대신하는 작업
- [[type-erasure]] — `TypeToken` 이 필요한 이유
- [[generics]] — 형식이 라이브러리로 간 뒤 남은 코드를 접은 문법
- [[wildcard-type]] — `toJson(List<?>)` 의 매개변수 선언
- [[class-metadata]] — 되돌릴 타입을 값으로 넘기는 통로
- [[date-time]] — 표준에 없어서 약속해야 하는 값
- [[character-stream]] — 이 텍스트가 오가는 통로
- [[gradle]] — 라이브러리를 프로젝트에 들이는 자리
- [[exception-handling]] — `null` 과 예외가 갈리는 지점
- [[binary-io]] — 크기를 위해 가독성을 버리는 반대편
- [[string-builder]] — 파일 전체를 문자열로 모으는 층
- [[db-normalization]] — 중첩을 표현할 수 있게 되면서 열리는 다음 이야기
- [[surrogate-key]] — 형식을 네 번 바꿔도 남아 있는 발급기 문제

## 출처

- [[2024-07-22-Day40]] — Gson 을 「구글에서 만든 Json포맷 입출력 라이브러리」로 정의하고 `build.gradle` 에 `com.google.code.gson:gson:2.11.0` 을 넣는 것부터 시작한다. `gson.toJson(boardList)` 로 목록 전체를 한 문자열로 내보내고, `BufferedReader` 로 파일을 모아 `fromJson(문자열, new TypeToken<List<Board>>() {})` 로 되돌린다. 기본 출력이 `"createdDate":"Jul 22, 2024, 5:13:25 PM"` 인 것을 보고 `new GsonBuilder().setDateFormat("yyyy-MM-dd HH:mm:ss").create()` 로 형식을 지정한다. 마지막에 세 벌로 복사돼 있던 저장·로딩을 `<E> loadJson(List<E>, String, Class<E>)`·`<E> saveJson(List<E>, String)` 으로 합치면서 `TypeToken.getParameterized(List.class, elementType)` 와 리플렉션(`getInterfaces`·`getMethod`·`invoke`)을 쓴다. **그 합치는 과정에서 `saveJson` 의 날짜 형식이 `yyyy-mm-dd` 로 어긋났고**, 빈 파일이 `fromJson` → `null` → `addAll` 로 이어지는 경로와 `Gson` 인스턴스를 매번 새로 만드는 것은 다루지 않았다

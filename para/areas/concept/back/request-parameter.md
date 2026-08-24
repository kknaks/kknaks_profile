---
type: concept
id: request-parameter
title: 요청 파라미터 (Request Parameter)
aliases:
  - 요청 파라미터
  - request parameter
  - getParameter
  - getParameterValues
  - 쿼리 파라미터
up:
  - 2024-09-04-Day69
  - 2024-08-28-Day65
tags:
  - web
  - java
  - JavaEE
  - HTTP
---

# 요청 파라미터 (Request Parameter)

**클라이언트가 「이름 = 값」 쌍으로 실어 보낸 것을 서블릿이 이름으로 꺼내는 통로.** Day65 가 두 자리에서 이것을 쓴다 — 조회 화면이 「req를 통해 조회할 no를 받아온다」로 한 값을, 등록 화면이 「query string에서 값을 받아오는 방법」과 「`req.getParameterValuse("memeber")`을 통해서 user_id의 배열 받아온다」로 여러 값을 꺼낸다 → [[request-response]] · [[url]] · [[html-form]]

## 정의

**메서드는 둘이고, 갈리는 것은 「이름 하나에 값이 몇 개인가」다.**

| 메서드 | 돌려주는 것 | 언제 |
|---|---|---|
| `getParameter(String name)` | `String` — 값 **하나** (없으면 `null`) | 이름 하나에 값 하나 |
| `getParameterValues(String name)` | `String[]` — 값 **여럿** (없으면 `null`) | 같은 이름이 여러 번 온 경우 (체크박스) |

그리고 **값이 어디로 실려 왔는지는 이 통로에 나타나지 않는다.**

| 보낸 방식 | 값이 실린 자리 | 꺼내는 코드 |
|---|---|---|
| 주소창의 링크 · `method="GET"` 폼 | URL 의 쿼리 스트링 → [[url]] | `req.getParameter("no")` |
| `method="POST"` 폼 | 요청 본문 | **똑같다** |

**이 표의 마지막 칸이 이 개념의 성격 전부다** — 서블릿은 「쿼리 스트링에서 읽는」 것이 아니라 「요청에서 이름으로 찾는」 것이고, 그래서 폼의 `method` 를 바꾸어도 서버 코드가 그대로다→ [[html-form]].

### 값은 언제나 문자열로 온다

HTTP 가 실어 오는 것은 바이트열이므로 **타입이라는 것이 없다.** 그래서 숫자가 필요하면 경계에서 되돌려야 한다.

```java
int userNo = Integer.parseInt(req.getParameter("no"));
```

**이 한 줄에 실패할 수 있는 것이 셋 들어 있다** — 이름이 틀렸거나(`null`), 값이 숫자가 아니거나, 값이 `int` 범위를 넘거나. 셋 다 같은 예외(`NumberFormatException`)로 나온다 → [[number-parsing]] · [[data-type]]

## 사용 예시

Day65 의 조회 화면이 **URL 에 실려 온 번호로 한 건을 찾는다.**

```java
int userNo = Integer.parseInt(req.getParameter("no"));

User user = userDao.findBy(userNo);
if (user == null) {
  out.println("<p>없는 회원입니다.</p>");
  ...
  return;
}
```

필기가 그 흐름을 정확히 적었다 — 「웹브라우저에서 `/user/view?no=xx`를 컨테이너에 request하면 컨테이너는 /user/view url을 가진 클래스를 호출 하고 no를 매개변수로 넘긴다」.

등록 화면은 **폼의 `name` 넷을 그대로 다시 부른다.**

```java
User user = new User();
user.setName(req.getParameter("name"));
user.setEmail(req.getParameter("email"));
user.setPassword(req.getParameter("password"));
user.setTel(req.getParameter("tel"));
```

팀원 선택만 **같은 이름이 여러 번** 오므로 배열로 받는다.

```java
String[] memberNos = req.getParameterValues("member");
if (memberNos != null) {
  ArrayList<User> members = new ArrayList<>();
  for (String memberNo : memberNos) {
    members.add(new User(Integer.parseInt(memberNo)));
  }
  project.setMembers(members);
}
```

**`new User(Integer.parseInt(memberNo))` 가 이 코드에서 가장 많은 것을 말한다** — 필요한 것은 회원 번호뿐이므로 이름도 이메일도 없는 `User` 를 만들어 넘긴다. 화면에서 온 값이 곧바로 도메인 객체가 되는 자리이고, 그 객체는 **DB 에 넣을 외래 키 하나만 든 껍데기**다 → [[foreign-key]] · [[dao-pattern]]

## 왜 중요한가

**바깥에서 온 값이 프로그램 안으로 들어오는 유일한 문이고, 그 문에서 타입 검사가 사라진다.** Day31 까지의 프로그램은 `Prompt.inputInt()` 처럼 **입력 함수가 타입을 책임졌다.** 웹에서는 모든 값이 `String` 으로 오므로 「무엇이어야 하는가」를 아는 것은 받는 코드뿐이고, 그 지식이 `Integer.parseInt` 한 줄로만 표현된다. **경계에서 한 번 변환하고 안에서는 타입으로 다루는** 구조가 여기서 시작된다 → [[type-casting]] · [[standard-input]]

**그리고 이름이 계약이라 어긋남이 조용하다.** 없는 이름을 물으면 예외가 아니라 `null` 이 돌아온다 — 즉 **오타는 오류가 아니라 「값이 안 온 것」으로 나타난다.** [[servlet-context]] 의 문자열 키, [[html-form]] 의 `name` 속성과 같은 문제의 세 번째 얼굴이고, 셋이 한 요청 안에서 이어져 있어 **어느 층에서 끊겼는지를 값으로는 구별할 수 없다** → [[literal]]

**같은 이름에 값이 여럿 올 수 있다는 것이 두 메서드가 있는 이유다.** 이 사실을 모르면 체크박스 다섯 개를 고르고 하나만 저장되는 것을 보게 되는데, **오류가 없으므로 데이터를 나중에 확인할 때까지 모른다.**

## 경계와 오해

- **`Integer.parseInt(req.getParameter("no"))` 는 URL 을 손으로 치는 것만으로 깨진다** — 목록의 링크를 눌러 들어오면 `?no=3` 이 있지만, `/user/view` 를 그냥 열면 `getParameter` 가 `null` 을 돌려주고 `Integer.parseInt(null)` 은 **`NumberFormatException`**(NPE 가 아니다 — `parseInt` 가 `null` 을 직접 검사해 던진다)이다. `?no=abc` 도 같은 예외다. 그리고 그 예외는 `catch (Exception e)` 에 걸려 **「조회 중 오류 발생!」 한 줄로 200 응답**이 되므로, **없는 회원 · 잘못된 요청 · DB 장애 셋이 같은 화면 한 줄로 덮인다.** 바로 위의 `if (user == null)` 이 「없는 회원입니다」를 따로 안내하려고 애쓴 것이 무의미해지는 자리다 — 그 분기까지 가지 못하는 입력이 더 흔하다 → [[exception-handling]] · [[number-parsing]]
- **필기의 `req.getParameterValuse("memeber")` 는 두 군데가 틀렸고, 둘의 결과가 정반대다** — 메서드 이름 `getParameterValuse`(→ `getParameterValues`)는 **컴파일에서 즉시 걸린다.** 파라미터 이름 `memeber`(→ `member`)는 **컴파일된다** — 그 이름의 파라미터가 없으므로 `null` 이 돌아오고, `if (memberNos != null)` 이 조용히 통과해 **팀원 없이 등록이 성공한다.** 오류도 경고도 없고 화면에는 「등록 성공입니다」가 찍힌다. (실습 코드 블록에는 `member` 로 맞게 적혀 있고 설명 줄만 틀렸다.) **문자열 이름의 오타가 컴파일에서 걸리는 것과 안 걸리는 것이 한 줄 안에 나란히 있는** 예다 → [[literal]] · [[string-comparison]]
- **`getParameter` 로 체크박스를 읽으면 첫 값만 조용히 저장된다** — 같은 이름이 여럿일 때 `getParameter` 는 **첫 값 하나**를 돌려준다(예외도 경고도 없다). 팀원 다섯을 골랐는데 한 명만 들어가고, 화면은 성공이라고 말한다. 반대로 값이 하나인 파라미터에 `getParameterValues` 를 써도 되며 **길이 1 인 배열**이 온다 — 즉 **의심스러우면 배열 쪽이 안전한 비대칭**이다.
- **선택되지 않은 체크박스는 빈 배열이 아니라 `null` 이다** — 켜지지 않은 체크박스는 이름 자체가 전송되지 않는다(→ [[html-form]]). 그래서 `for (String s : getParameterValues("member"))` 를 그냥 쓰면 **팀원을 고르지 않은 첫 등록에서 NPE** 다. Day65 의 코드는 `if (memberNos != null)` 로 맞게 감쌌지만 그 대가가 있다 — **팀원 0 명일 때 `project.setMembers(...)` 가 아예 불리지 않아** 필드가 초기값(`null`)으로 남고, 뒤에서 그 목록을 도는 코드가 있으면 등록이 거기서 터진다. 「방어했다」와 「빈 값으로 채웠다」는 다른 일이고, 후자여야 뒤쪽 코드가 한 가지 경우만 다룬다 → [[default-initialization]] · [[dynamic-array]]
- **요청 파라미터 인코딩은 응답 인코딩과 다른 축이고, GET 과 POST 는 고치는 자리마저 다르다** — `res.setContentType("text/html;charset=UTF-8")` 은 **나가는 것**을 정한다(→ [[request-response]]). 폼에서 온 한글을 제대로 읽으려면 POST 는 `req.setCharacterEncoding("UTF-8")` 을 **첫 `getParameter` 앞에서** 불러야 하고, GET 은 값이 URL 에 있으므로 그 호출이 **아무 효과가 없다** — 컨테이너 설정(톰캣의 `URIEncoding`)이 정한다. 이 회차의 폼이 GET 이므로 정확히 그 함정 위에 있고, 필기에는 요청 쪽 인코딩이 한 번도 나오지 않는다. **「인코딩을 UTF-8 로 맞췄는데 한글만 깨진다」의 대부분이 이 세 자리 중 어느 것을 고쳤는지의 문제**다 → [[character-encoding]] · [[url]] · [[servlet-filter]]
- **파라미터 ≠ 속성 — 같은 객체에 있고 이름이 닮아서 섞인다** — `getParameter` 는 **클라이언트가 보낸 값**을 읽고, `getAttribute`/`setAttribute` 는 **서버가 담아 둔 객체**를 다룬다. 파라미터는 문자열이고 읽기만 되며 요청과 함께 사라진다. 속성은 아무 객체나 되고 내가 넣는다. `req.setParameter(...)` 라는 메서드는 **없다** — 클라이언트가 준 것을 서버가 고쳐 쓸 수 없게 만든 것이고, 값을 다음 컴포넌트에 넘기려면 속성을 써야 한다 → [[servlet-context]] · [[http-session]]
- **파라미터 이름이 겹치면 뒤에 온 것이 이기지 않는다 — 둘 다 남는다** — `?no=3&no=7` 이면 값 두 개가 있는 상태이고 `getParameter` 는 첫 것을, `getParameterValues` 는 둘 다 준다. 그리고 **GET 으로 보낸 것과 POST 본문에 있는 것이 같은 이름이면 그것도 합쳐진다** — 즉 「하나만 올 것」이라는 가정은 규격이 보장해 주지 않는다. 값 하나를 기대하는 코드에 여럿을 보내는 것으로 검증을 우회하는 공격이 여기서 나온다 → [[html-form]]
- **`getParameter` 가 돌려주는 빈 문자열과 `null` 은 다르다** — 폼의 빈 칸은 **이름은 오고 값은 `""`** 이다(체크박스와 반대다). 그래서 「입력하지 않았다」를 `null` 검사로만 판정하면 빈 칸이 통과해 **이름이 `""` 인 회원**이 생긴다. Day65 는 어느 값도 검사하지 않으므로 빈 폼을 그대로 제출하면 빈 문자열 넷이 `insert` 된다 → [[sql-null]] · [[string-comparison]]

## 함께 보는 개념

- [[html-form]] — 이 값들을 만들어 보내는 쪽
- [[url]] — 쿼리 스트링이 사는 자리와 그 인코딩 규칙
- [[request-response]] — 이 메서드들이 붙어 있는 객체
- [[http-session]] — 요청보다 오래 살아야 하는 값을 담는 곳
- [[servlet-context]] — 파라미터와 헷갈리는 속성 저장소
- [[number-parsing]] · [[data-type]] · [[type-casting]] — 문자열을 되돌리는 자리
- [[character-encoding]] · [[servlet-filter]] — 요청 인코딩을 정하는 층
- [[exception-handling]] — 변환 실패가 나타나는 형태
- [[literal]] · [[string-comparison]] — 이름이 문자열인 대가
- [[sql-null]] · [[default-initialization]] — 「값이 없음」의 여러 얼굴
- [[dao-pattern]] · [[foreign-key]] — 받은 값이 도메인 객체가 되는 자리
- [[standard-input]] — 입력의 타입을 함수가 책임졌던 이전 방식

## 출처

- [[2024-09-04-Day69]] — 이레 뒤. 「클라이언트가 보낸 값 꺼내기」가 `ServletRequest.getParameter("파라미터명")`을 다시 적는다. Servlet 기본 API의 multipart 처리에서는 일반 폼 필드를 `getParameter`로, 파일을 `getPart`로 읽고, Apache Commons 예제에서는 `FileItem.isFormField()` 뒤 일반 필드를 `getString("UTF-8")`으로 읽는다. POST 한글을 읽기 전에 `req.setCharacterEncoding("UTF-8")`을 둬야 한다는 시점은 맞게 짚었지만, **POST의 인코딩을 ISO-8859-1로 일반화한 것은 틀렸다.** 요청의 실제 `Content-Type`과 바이트를 기준으로 읽어야 한다.
- [[2024-08-28-Day65]] — 세 자리에서 이 개념이 나온다. ① 「ViewServlet 만들기」의 「req를 통해 조회할 no를 받아온다」와 「웹브라우저에서 `/user/view?no=xx`를 컨테이너에 request하면 컨테이너는 /user/view url을 가진 클래스를 호출 하고 no를 매개변수로 넘긴다」 — 코드는 `int userNo = Integer.parseInt(req.getParameter("no"));` 다. ② 「AddServlet만들기」의 「query string에서 값을 받아오는 방법은 다음과 같다」 — 폼의 `name` 넷을 `req.getParameter` 로 그대로 꺼내 `User` 에 담는다. ③ 「project member 받아오기」의 「`AddServlet에서는 req.getParameterValuse("memeber")`을 통해서 user_id의 배열 받아온다」 — 체크박스 여러 개를 `String[]` 으로 받아 `new User(Integer.parseInt(memberNo))` 로 번호만 든 객체를 만든다. **설명 줄의 `getParameterValuse`·`memeber` 는 오기이고**(코드 블록에는 `member` 로 맞게 적혀 있다) 앞은 컴파일 오류, 뒤는 컴파일되어 **팀원 없이 등록이 성공하는** 조용한 결과를 낸다. 없는 파라미터가 `null` 로 온다는 것, 그래서 `Integer.parseInt` 가 `NumberFormatException` 을 던지고 그것이 「조회 중 오류 발생!」 한 줄로 덮인다는 것, `getParameter` 로 체크박스를 읽으면 첫 값만 조용히 저장된다는 것, 선택하지 않은 체크박스는 `null` 이라 `setMembers` 가 아예 불리지 않는다는 것, 요청 쪽 인코딩(`setCharacterEncoding`)은 응답과 별도이고 GET 은 그것으로도 안 된다는 것, 파라미터와 속성(`getAttribute`)이 다른 것이라는 것, 빈 칸은 `null` 이 아니라 `""` 로 온다는 것은 다루지 않았다

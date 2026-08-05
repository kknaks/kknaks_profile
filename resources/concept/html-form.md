---
type: concept
id: html-form
title: HTML 폼 (form)
aliases:
  - HTML 폼
  - HTML form
  - form 태그
  - 폼 태그
  - input 태그
up:
  - 2024-08-28-Day65
tags:
  - web
  - HTML
  - 기초
---

# HTML 폼 (form)

**사용자가 채운 입력들을 이름표를 달아 한 번에 한 URL 로 보내는 묶음 — 브라우저가 요청을 만들어 주는 유일한 표준 장치.** Day65 가 속성 넷을 한 줄씩 적었다 — 「`<form atction="url" method="GET|POST">` : 폼이 완료되면 액션 메서드가 실행된다」·「`<input name="name" type="type">` : 입력창을 만드는 태그이다」·「name : 태그가 req로 반환될 때 파라미터 명이다」·「`<input type="submit" value="등록">` … 클릭하면 폼의 액션이 호출된다」 → [[url]] · [[request-parameter]]

## 정의

**속성 넷이 「어디로 · 어떻게 · 무슨 이름으로 · 언제」를 하나씩 정한다.**

| 어디에 | 속성 | 정하는 것 | Day65 의 값 |
|---|---|---|---|
| `<form>` | `action` | **어디로** 보내나 (URL) | `/user/add` · `/auth/login` |
| `<form>` | `method` | **어떻게** 실어 보내나 | (적지 않았다 → 기본 `GET`) |
| `<input>` | `name` | 값에 붙는 **이름표** | `name`·`email`·`password`·`tel` |
| `<input>` | `type` | 입력창의 **모양과 브라우저의 도움** | `text`·`email`·`password`·`tel`·`checkbox` |
| `<input type="submit">` | — | **언제** 보내나 | 「등록」·「로그인」 버튼 |

### `method` 가 정하는 것은 「값이 어디에 실리나」다

Day65 의 두 줄이 이 축의 전부다.

| `method` | Day65 의 설명 | 값이 남는 곳 |
|---|---|---|
| `GET` | 「데이터가 URL의 쿼리 스트링(예: `?name=value`)으로 전송된다」 | **URL 이 가는 모든 곳** — 주소창·히스토리·북마크·액세스 로그·리퍼러 |
| `POST` | 「데이터가 HTTP 요청의 본문에 포함되어 전송된다」 | 요청 본문 (기록으로 남지 않는다) |

**받는 쪽 코드는 둘을 구별하지 않는다** — `req.getParameter("name")` 이 어느 쪽에서 왔는지 묻지 않는다(→ [[request-parameter]]). 그래서 **폼을 GET 에서 POST 로 바꾸어도 서블릿을 고치지 않아도 되고, 반대로 잘못된 쪽을 골라도 아무 증상이 없다.** 편함과 위험이 같은 사실에서 나온다.

## 사용 예시

Day65 의 등록 폼 전문. **정적 파일 하나로 화면 하나가 된다.**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <link href="/css/common.css" rel="stylesheet">
</head>
<body>
    <header>
        <a href="/"><img src="/images/home.png"></a>
        프로젝트 관리 시스템
    </header>
    <h1>회원 등록</h1>
    <form action="/user/add">
        이름: <input name="name" type="text"><br>
        이메일: <input name="email" type="email"><br>
        암호: <input name="password" type="password"><br>
        연락처: <input name="tel" type="tel"><br>
        <input type="submit" value="등록">
    </form>
</body>
</html>
```

받는 쪽에서 **`name` 속성의 문자열이 그대로 다시 나타난다.**

```java
User user = new User();
user.setName(req.getParameter("name"));
user.setEmail(req.getParameter("email"));
user.setPassword(req.getParameter("password"));
user.setTel(req.getParameter("tel"));
```

**두 파일 사이에 같은 문자열 넷이 짝을 이루고, 그 짝을 검사하는 것은 아무것도 없다.**

그리고 폼이 **동적으로 만들어지기도 한다** — 팀원 선택은 회원 목록을 읽어야 하므로 정적 파일로 둘 수 없다.

```java
out.println("        <ul>");
List<User> users = userDao.list();
for (User user : users) {
  out.printf("          <li><input name='member' value='%d' type='checkbox'> %s</li>\n",
          user.getNo(), user.getName());
}
out.println("        </ul>");
```

**여기서 `name` 이 회원마다 같고 `value` 만 다르다** — 같은 이름의 입력이 여럿이라는 상태가 처음 생기고, 그것이 받는 쪽에 `getParameterValues` 가 필요해지는 이유다 → [[request-parameter]]

## 왜 중요한가

**Day61 까지 콘솔이 하던 일을 브라우저가 대신하게 되는 자리다.** 소켓 프로젝트에서 입력을 받는 일은 「무엇을 물을지 순서대로 출력하고 한 줄씩 읽는」 코드였다(→ [[command-loop]] · [[standard-input]]). 폼은 그 순서를 없앤다 — **네 칸을 한 번에 보여 주고 한 번에 받는다.** 그 결과 서버 코드에서 대화의 흐름이 사라지고 「요청 하나에 값 넷이 함께 온다」만 남는다. 클라이언트 프로젝트를 만들지 않기로 한 Day63 의 결정이 실제로 값을 치르는 자리이기도 하다 → [[client-server-model]]

**그리고 입력의 이름이 화면과 코드를 잇는 계약이 된다.** `name="email"` 을 `name="mail"` 로 고치면 화면은 그대로이고 **서버에서 값이 `null` 로 온다.** [[servlet-context]] 의 「키가 문자열이라 넣는 쪽과 꺼내는 쪽이 어긋난 것을 아무도 말해 주지 않는다」가 여기서 **HTML 파일과 자바 파일 사이**로 한 번 더 나타나고, 이번에는 두 파일이 언어도 다르다 → [[literal]]

**`method` 하나가 보안·중복·기록을 동시에 정한다.** 아래 「경계와 오해」의 앞 세 항목이 전부 이 회차가 그 속성을 적지 않은 결과이고, 셋 다 **오류 없이** 나타난다.

## 경계와 오해

- **필기의 `atction` 은 `action` 의 오기이고, 그 오타는 화면을 「아무 일도 안 일어난 것처럼」 만든다** — 실습 코드에는 `action="/user/add"` 로 맞게 적혀 있고 설명 줄만 틀렸다. 그런데 만약 실제로 그렇게 적으면 증상이 조용하다 — **브라우저는 모르는 속성을 무시하고, `action` 이 없는 폼은 「현재 페이지의 URL」로 제출한다.** 즉 `/user/form.html` 이 `?name=…&email=…` 을 달고 다시 열려서 **빈 폼이 다시 뜬다.** 오류도 404 도 없고 「등록 버튼이 안 먹는다」로만 보이므로, 원인을 서블릿 쪽에서 찾게 된다 → [[url]]
- **두 폼 모두 `method` 를 적지 않았다 — 기본값이 `GET` 이므로 암호가 URL 에 실려 나간다** — 필기가 **바로 위 줄에** 「method="POST": 데이터가 HTTP 요청의 본문에 포함되어 전송된다」고 적어 두고 두 폼 어디에도 쓰지 않았다. 끝까지 세면 이렇다 — 등록 버튼을 누른 순간 주소창이 `/user/add?name=홍길동&email=…&password=1234&tel=…` 이 되고, 그 문자열이 **브라우저 히스토리와 자동완성 · 북마크 · 톰캣 액세스 로그 · 다음 요청의 리퍼러 헤더 · 중간 프록시의 캐시**에 그대로 남는다. 로그인 폼(`/auth/login`)도 같으므로 **암호가 두 번 새고**, 사용자는 화면에서 아무 이상을 보지 못한다. 더 나쁜 것은 `type="password"` 가 **화면에서만 별표로 가려 준다**는 점이다 — 가려진 것과 안전한 것이 같아 보이므로 이 문제가 눈에 걸릴 계기가 없다 → [[url]] · [[http-session]]
- **`GET` 으로 등록하면 새로고침·뒤로가기·크롤러가 다시 등록한다** — GET 은 「가져오는 것」이라 브라우저·프록시·검색 봇이 **마음대로 다시 보내도 된다고 가정한다.** 그런데 이 회차의 `/user/add` 는 `userDao.insert(user)` 를 한다. 그래서 등록 뒤 F5 를 누르면 같은 회원이 또 생기고, 링크를 미리 읽어 두는 도구가 URL 을 훑기만 해도 데이터가 늘어난다. **`insert` 를 하는 URL 은 GET 이면 안 된다**는 것이 규약이고, 필기에는 그 축(안전·멱등)이 없다. 우연히 이 코드는 절반쯤 가려져 있다 — 응답 끝의 `setHeader("Refresh", "1;url=/user/list")` 가 1 초 뒤 주소창을 목록으로 바꿔 놓으므로 그 뒤의 새로고침은 목록 조회가 된다. **가린 것이지 고친 것은 아니다** — 뒤로가기로 등록 결과 화면에 돌아가면 그대로 다시 등록된다 → [[request-response]] · [[transaction]]
- **`<input type="submit">` 은 입력창이 아니다 — 필기가 앞 항목의 설명을 그대로 붙였다** — 「입력창을 만드는 태그이고, 클릭하면 폼의 액션이 호출된다」에서 뒷절만 맞다. 이것은 버튼이고 `value` 는 **입력값이 아니라 버튼에 찍히는 글자**다(다만 `name` 을 주면 그 값도 함께 전송된다 — 버튼이 둘인 폼에서 어느 것을 눌렀는지 구별하는 방법이 그것이다) → [[request-parameter]]
- **`<link href="url" rel='stylesheet">` 는 인용부호 짝이 맞지 않는다** — `rel='stylesheet"` 가 `'` 로 열고 `"` 로 닫았다. 실습 코드에는 맞게 적혀 있고 설명 줄만 그렇다. 이렇게 적으면 브라우저는 닫히지 않은 속성값에 **뒤따르는 텍스트를 계속 삼켜** 스타일시트가 붙지 않고, 심하면 그 뒤 태그 몇 개가 사라진다. HTML 은 이런 실수에 오류를 내지 않고 **최선을 다해 해석하는** 언어라 증상이 「스타일이 안 먹는다」로만 나온다.
- **`type` 은 검증이 아니다 — 서버는 아무것도 보장받지 않는다** — 필기의 「type에 따라 입력창이 다르게 출력된다. (특히 모바일)」은 정확하다. `type="email"` 이 하는 일은 **모양(모바일 키보드가 `@` 를 보여 준다)과 브라우저의 제출 전 검사**까지이고, 요청 자체는 폼 없이도 만들 수 있으므로(주소창에 쿼리 스트링을 직접 치면 된다) **서버에는 어떤 문자열이든 올 수 있다.** Day65 의 AddServlet 은 받은 값을 검사 없이 그대로 `insert` 한다 — `email` 자리에 이메일이 아닌 것이, `tel` 자리에 글자가 들어갈 수 있다. [[prepared-statement]] 가 막아 주는 것(문법 침범)과 값이 규칙에 맞는지 보는 것은 **다른 축**이라 하나로 다른 하나를 대신할 수 없다 → [[sql-injection]] · [[request-parameter]]
- **선택하지 않은 체크박스는 「값이 없음」으로 오지 않고 아예 오지 않는다** — 체크박스는 켜졌을 때만 `name=value` 쌍이 전송된다. 그래서 팀원을 하나도 고르지 않으면 `member` 라는 이름이 요청에 없고, 받는 쪽은 `null` 을 본다(빈 배열이 아니다). Day65 의 코드가 `if (memberNos != null)` 로 감싼 것이 정확히 그 성질을 다룬 자리인데 **필기에 이유가 적혀 있지 않다** — 그래서 다음에 `radio`·`select` 를 다룰 때 같은 방어를 할 근거가 남지 않는다 → [[request-parameter]] · [[sql-null]]
- **폼이 값을 실어 보내는 방식도 URL 인코딩이다** — `enctype` 을 정하지 않으면 `application/x-www-form-urlencoded` 이고, 그것은 **`GET` 이든 `POST` 든 「이름=값&이름=값」을 퍼센트 인코딩해 보낸다**는 뜻이다(POST 는 그 문자열을 본문에 담는다). 즉 두 방식의 차이는 「실리는 자리」뿐이고 **표기법은 같다.** 파일 업로드만 이 규칙에서 벗어나 `multipart/form-data` 를 쓰는데, 그것이 별도 처리가 필요한 이유다 → [[url]] · [[character-encoding]]
- **폼 하나에 `action` 은 하나다** — 「등록」과 「취소」처럼 갈 곳이 둘이면 폼 두 개로 나누거나 버튼에 `name` 을 주어 서버에서 갈라야 한다. 「폼이 완료되면 액션 메서드가 실행된다」의 「액션 메서드」라는 표현이 **자바 메서드처럼 읽히는데** 실제로는 URL 이고, 그 URL 뒤에 어느 클래스가 있는지는 폼이 모른다 → [[url]] · [[dispatch-table]]

## 함께 보는 개념

- [[request-parameter]] — 폼이 보낸 값을 서블릿에서 꺼내는 쪽
- [[url]] — `action` 과 쿼리 스트링이 사는 층
- [[http-session]] — 로그인 폼이 만들어 내는 상태
- [[static-and-dynamic-content]] — 정적 폼과 동적으로 그리는 폼이 갈리는 자리
- [[request-response]] — 폼 제출이 만드는 요청과 그 응답
- [[servlet]] · [[servlet-lifecycle]] — `action` 이 가리키는 쪽
- [[client-server-model]] · [[command-loop]] · [[standard-input]] — 입력을 받던 이전 방식
- [[sql-injection]] · [[prepared-statement]] — 받은 값을 그대로 쓰는 것의 위험
- [[character-encoding]] — 폼 값이 바이트가 되는 규칙
- [[literal]] — 이름표가 문자열인 대가
- [[transaction]] — 중복 제출이 데이터에 남기는 결과

## 출처

- [[2024-08-28-Day65]] — 「AddServlet 만들기 > form.html만들기」 절이 이 개념이다. 「정적HTMl을 만들어서 브라우저에 보낼수도 있다」로 시작해 `<form atction="url" method="GET|POST">`·`<link>`·`<input name type>`·`<input type="submit">` 을 한 줄씩 설명하고, **`method` 두 값의 차이를 「URL의 쿼리 스트링으로 전송」 대 「HTTP 요청의 본문에 포함되어 전송」으로 정확히 적었다.** `name` 에 대한 「태그가 req로 반환될 때 파라미터 명이다」와 `type` 에 대한 「type에 따라 입력창이 다르게 출력된다. (특히 모바일)」도 정확하다. 등록 폼(`/user/add`)과 로그인 폼(`/auth/login`) 두 개의 전문이 실려 있고, 「project member 받아오기」 절에서 회원 목록을 돌며 `<input name='member' value='%d' type='checkbox'>` 를 찍어 **폼을 동적으로 만드는** 형태가 나온다. 다만 **두 폼 모두 `method` 를 적지 않아 기본값 GET 으로 제출되며, 그래서 암호가 쿼리 스트링에 실려 히스토리·로그·리퍼러에 남는다** — 바로 위 줄에 POST 의 설명을 적어 두고 쓰지 않은 자리다. 등록을 GET 으로 하면 새로고침·뒤로가기·크롤러가 재등록한다는 것(안전·멱등), 설명 줄의 `atction` 오기가 「현재 URL 로 제출」이라는 조용한 증상을 낸다는 것, `<input type="submit">` 은 입력창이 아니라 버튼이라는 것, `type="email"` 은 검증이 아니라 브라우저의 도움일 뿐이라는 것, 선택되지 않은 체크박스는 아예 전송되지 않아 `null` 이 온다는 것(코드는 `if (memberNos != null)` 로 맞게 다뤘지만 이유가 없다), `enctype` 의 기본값이 폼 값에도 퍼센트 인코딩을 적용한다는 것은 다루지 않았다

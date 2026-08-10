---
type: concept
id: jstl-format-tag
title: JSTL Formatting 태그 (fmt:)
aliases:
  - fmt 태그
  - Formatting 태그
  - fmt:formatDate
  - fmt:parseDate
up:
  - 2024-09-11-Day74
tags:
  - web
  - jsp
  - jstl
  - 시간
---

# JSTL Formatting 태그 (fmt:)

[[jstl]] 의 형식 지정 모듈. **문자열 ↔ 값** 을 오가게 하고, 값을 사람이 읽는 모양으로 만든다. 날짜·시간·숫자가 대상이고, 로케일과 시간대를 함께 다룬다.

## 정의

방향이 둘이고 서로 반대다.

| 태그 | 방향 |
|---|---|
| `fmt:parseDate` | **문자열 → 날짜 객체** (읽어 들이기) |
| `fmt:formatDate` | **날짜 객체 → 문자열** (내보내기) |

### `fmt:parseDate`

| 속성 | 하는 일 |
|---|---|
| `value` | 파싱할 날짜/시간 문자열 |
| `var` | 변환 결과를 담을 이름 |
| `pattern` | 입력 문자열의 형식 (`dd/MM/yyyy`) |
| `type` | `date` · `time` · `both` (기본 `date`) |
| `timeZone` | 적용할 시간대. 생략하면 **서버의 시간대** |

### `fmt:formatDate`

| 속성 | 하는 일 |
|---|---|
| `value` | 포맷할 `java.util.Date` 또는 날짜 문자열 |
| `pattern` | 출력 형식. `SimpleDateFormat` 의 패턴을 쓴다 |
| `type` | `date` · `time` · `both` |
| `dateStyle` · `timeStyle` | `default`·`short`·`medium`·`long`·`full` |
| `timeZone` | 출력에 적용할 시간대 |

**`pattern` 과 `dateStyle` 은 서로 다른 방식이다** — 앞은 모양을 직접 적는 것이고, 뒤는 **로케일에 맡기는 것**이다. `pattern` 을 주지 않으면 로케일에 따라 형식이 정해진다.

## 사용 예시

```jsp
<fmt:parseDate value="11/09/2024" pattern="dd/MM/yyyy" var="parsedDate"/>
<fmt:formatDate value="${parsedDate}" pattern="yyyy-MM-dd HH:mm:ss" timeZone="Asia/Seoul"/>
```

## 왜 중요한가

**「저장과 표시를 가른다」는 원칙이 화면 쪽에서 실현되는 자리다.** 값은 `Date` 로 담고, 보여 줄 때 형식을 입힌다 → [[date-time]]

그렇지 않으면 형식이 자바 코드 안으로 들어간다. `String.format("%1$tY-%1$tm-%1$td", date)` 를 서블릿에 쓰면 **날짜를 어떻게 보일지가 로직 파일에 박히고**, 같은 값을 다른 화면에서 다르게 보이려면 그 코드를 또 만들어야 한다 → [[format-string]] · [[mvc-pattern]]

**시간대를 태그가 받는다는 것**도 크다. 서버가 어디에 있든 출력은 `Asia/Seoul` 로 고정할 수 있다 — 이 속성을 안 쓰면 배포한 서버의 시간대가 화면에 그대로 나온다.

## 경계와 오해

- **`parseDate` 와 `formatDate` 의 `pattern` 은 대상이 다르다** — 앞의 패턴은 **입력이 어떻게 생겼는지**를 알려 주는 것이고, 뒤의 패턴은 **출력을 어떻게 만들지**를 정하는 것이다. 같은 속성 이름이라 헷갈리는 자리다
- **패턴 문자는 대소문자가 다른 것을 뜻한다** — `MM` 은 월, `mm` 은 분이다. `yyyy-mm-dd` 로 쓰면 월 자리에 분이 나온다. `SimpleDateFormat` 의 규칙을 그대로 따르므로 이 함정도 그대로 따라온다
- **`timeZone` 을 생략하면 「없음」이 아니라 「서버 것」이다** — 필기가 정확히 짚었다. 개발 PC 와 배포 서버의 시간대가 다르면 **같은 코드가 다른 시각을 보인다.** 값이 UTC 밀리초 하나라는 것을 알면 왜 그런지가 보인다 → [[date-time]]
- **국제화는 형식만의 일이 아니다** — 이 모듈이 「다국어 지원」을 표방하지만 `fmt:formatDate` 가 하는 것은 **로케일에 맞는 표기**까지다. 문구 자체를 번역하는 것은 메시지 번들 쪽의 일이고 이 회차에는 나오지 않는다
- **날짜 문자열을 그냥 출력하는 것과 다르다** — DB 에서 문자열로 읽어 그대로 찍으면 형식이 DB 의 것이 된다. 한 번 `parseDate` 로 값으로 만들어야 형식을 이쪽에서 정할 수 있다 → [[sql-date-function]]

## 함께 보는 개념

- [[jstl]] — 이 태그들이 속한 라이브러리
- [[jstl-core-tag]] — 같은 라이브러리의 기본 모듈
- [[date-time]] — 저장과 표시를 가르는 원칙
- [[format-string]] — 자바 쪽에서 같은 일을 하던 방법
- [[expression-language]] — `value` 에 값을 넘기는 표기법
- [[sql-date-function]] — DB 쪽에서 형식을 다루는 자리

## 출처

- [[2024-09-11-Day74]] — 「Internationalization 태그」 절이 `fmt:parseDate` 다섯 속성과 `fmt:formatDate` 여섯 속성을 타입·예시와 함께 정리했다. **`pattern` 이 `SimpleDateFormat` 의 패턴이라는 것**, `type` 의 값이 `date`·`time`·`both` 라는 것, `dateStyle`/`timeStyle` 이 다섯 단계라는 것, 그리고 **`timeZone` 을 생략하면 서버의 시간대가 쓰인다**는 것이 명시돼 있다. `pattern` 을 주지 않으면 로케일이 형식을 정한다는 것도 적었다. 다만 패턴 문자의 대소문자 함정(`MM`/`mm`)과, 국제화가 형식 지정에서 끝나지 않는다는 것은 다루지 않았다

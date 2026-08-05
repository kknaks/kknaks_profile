---
type: concept
id: annotation-retention
title: 애노테이션 보존 정책 (@Retention)
aliases:
  - "@Retention"
  - RetentionPolicy
  - 보존 정책
  - retention policy
  - 애노테이션 유지 정책
up:
  - 2024-08-21-Day60
tags:
  - java
  - 메타데이터
  - 컴파일
  - 리플렉션
---

# 애노테이션 보존 정책 (@Retention)

**내가 만든 애노테이션이 어느 단계까지 살아남을지를 선언해 두는 것.** 애노테이션은 소스 → `.class` 파일 → 메모리로 내려가는 동안 **아무 때나 버려질 수 있고**, 어디서 버릴지는 애노테이션을 만들 때 정한다. 그래서 「누가 이 애노테이션을 읽는가」가 곧 「어디까지 남겨야 하는가」다 → [[annotation]] · [[compilation]]

## 정의

값이 셋이고, **버려지는 지점의 사다리**다.

| 값 | 소스 | `.class` 파일 | 실행 중 메모리 | 읽는 주체 |
|---|---|---|---|---|
| `SOURCE` | 있다 | **없다** | 없다 | 컴파일러 · 애노테이션 프로세서 |
| `CLASS` **(기본값)** | 있다 | 있다 | **없다** | `.class` 파일을 읽는 도구 |
| `RUNTIME` | 있다 | 있다 | **있다** | 리플렉션 — 즉 **프레임워크** |

필기가 세 값을 정확히 적었다 — 「**CLASS** : .class파일 까지는 유지되지만, runtime에서는 메모리에 로딩되지 않는다.」·「**SOURCE** : 컴파일할때 제거된다. 소스파일에서 어노테이션 값을 추출하여 다른 소스를 생성할때 사용한다.」·「**RUNTIME** : runtime에 메모리에 로딩된다. 실행 중 어노테이션을 참조해야 할 경우에 많이 사용한다.」 그리고 「RetentionPolicy는 annotation을 만들때 설정한다」 — **쓰는 쪽이 아니라 만드는 쪽의 선택**이라는 것이 이 문장이다.

```java
import java.lang.annotation.RetentionPolicy;

@Retention(RetentionPolicy.RUNTIME)
public @interface MyAnnotation {
  String value();
}
```

### 표준 애노테이션들이 이 셋에 흩어져 있다

지금까지 써 온 것들을 이 축에 놓으면 **왜 어떤 것은 실행 중에 보이지 않는지**가 정해진다.

| 애노테이션 | 정책 | 그래서 |
|---|---|---|
| `@Override` · `@SuppressWarnings` | `SOURCE` | 컴파일이 끝나면 흔적이 없다 |
| `@Deprecated` · `@FunctionalInterface` | `RUNTIME` | 실행 중에도 물어볼 수 있다 |
| `@Entity` · `@Component` 류 프레임워크 애노테이션 | `RUNTIME` | 그래야 프레임워크가 찾을 수 있다 |

[[annotation]] 노트가 Day06 기준으로 「읽는 시점이 애노테이션마다 다르다 — `@Override` 는 컴파일할 때만 쓰이고 실행 시점에는 남지 않는다」고 적어 둔 관찰이, **Day60 에서 선언할 수 있는 문법이 된다.** 그때는 「애노테이션마다 다르더라」였고 여기서는 **내가 그것을 정한다** → [[reflective-annotation-access]]

### 필기의 세 활용이 이 세 값과 짝이다 — 그런데 잇지 않았다

같은 노트의 앞 절(「annotation 사용」)이 활용을 셋 적었다.

| 필기의 활용 | 대응하는 정책 |
|---|---|
| 「소스코드에서 주석을 읽어 다른 소스파일을 생성할 수 있다」 | `SOURCE` |
| 「컴팡일 할 때 주석을 추출하여 사용할수 있다」 | `SOURCE`(또는 `CLASS`) |
| 「실행 중에 주석을 추출하여 사용할 수 있다」 | `RUNTIME` |

**두 절이 같은 삼분법을 각자 적어 놓고 서로를 가리키지 않는다.** 그리고 가운데 줄의 대응이 애매한 것이 우연이 아니다 — `CLASS` 는 「컴파일할 때 쓰는 것」이 아니라 **컴파일이 끝난 파일을 나중에 읽는 도구**를 위한 것이고, 그 도구가 컴파일러가 아니라는 것이 이 정책이 왜 있는지의 답이다(아래 「경계와 오해」) → [[class-file-format]] · [[bytecode]]

## 사용 예시

Day60 의 「property 값 추출」 절이 `RUNTIME` 을 실제로 쓴다.

```java
@Retention(RetentionPolicy.RUNTIME)
public @interface MyAnnotation {
  String v1() default "가나다";
  int v2() default 100;
  float v3() default 3.14f;
}
```

```java
@MyAnnotation
public class MyClass {
}
```

```java
Class<?> clazz = MyClass.class;
MyAnnotation obj = clazz.getAnnotation(MyAnnotation.class);
System.out.println(obj.v1());  // 가나다
```

**이 예제가 `@Retention(RetentionPolicy.RUNTIME)` 을 붙인 이유가 필기에 적혀 있지 않다.** 지우면 컴파일도 실행도 되는데 `getAnnotation` 이 **`null`** 을 돌려주고 다음 줄이 `NullPointerException` 이다 — 기본값이 `CLASS` 이므로 애노테이션이 파일에는 있고 메모리에는 없다. **이 한 줄이 예제가 도는지 안 도는지를 정하는데 설명이 없는 자리**이고, 같은 노트의 `@Target` 절 예제들에는 그 줄이 없다(그쪽은 읽지 않으니 필요 없다) — **그 비대칭도 설명되지 않는다** → [[reflective-annotation-access]] · [[exception-handling]]

## 왜 중요한가

**애노테이션이 「아무 일도 하지 않는」 첫 번째 원인이 이것이다.** [[annotation]] 이 「아무도 안 읽는 애노테이션은 정말 아무 일도 하지 않는다」고 적었는데, 그보다 앞선 실패가 있다 — **읽으려는 쪽이 있는데도 볼 수 없는 상태.** 직접 만든 애노테이션에 `@Retention` 을 안 붙이면 프레임워크가 아무리 찾아도 없고, 오류 메시지에는 애노테이션 이야기가 한 줄도 나오지 않는다(`null` 이거나 「해당 없음」으로 조용히 지나간다). **「붙였는데 안 먹는다」의 첫 확인 지점**이 이 한 줄이다 → [[reflective-annotation-access]]

**그리고 세 값이 각각 다른 비용을 갖는다.** `RUNTIME` 으로 하면 클래스를 로딩할 때 애노테이션 정보까지 메모리에 올라가고, 그 애노테이션 타입이 **실행 시점 클래스패스에 있어야** 한다. `SOURCE` 는 아무 흔적도 남지 않으므로 배포물에 그 애노테이션 라이브러리를 넣지 않아도 된다. **「전부 `RUNTIME` 으로 해 두면 되지」가 아니라, 남기는 것은 곧 실행 시점 의존이 된다** → [[classpath]]

**셋 중 무엇을 고를지는 「읽는 주체가 언제 도는가」로 결정된다.** 소스를 읽어 코드를 생성하는 도구는 컴파일 전에 돌고, 바이트코드 분석기는 컴파일 후에 돌고, 프레임워크는 실행 중에 돈다. **정책은 취향이 아니라 그 시각을 적는 것**이다 → [[compilation]] · [[jvm]]

## 경계와 오해

- **기본값이 `RUNTIME` 이 아니라 `CLASS` 다 — 이것이 이 문법의 유일한 함정이다** — 필기가 `<default>` 표시로 그것을 적어 두었고 맞다. 그런데 **직접 애노테이션을 만드는 사람이 원하는 것은 거의 언제나 `RUNTIME`** 이므로, 기본값이 원하는 것과 다르다는 뜻이다. 「안 적으면 다 남겠지」로 읽으면 `getAnnotation()` 이 `null` 인 이유를 애노테이션 밖에서 찾게 된다 — 이름 오타도 아니고 `@Target` 위반도 아니고 컴파일 오류도 없으므로, **틀렸다는 신호가 어디에도 없는 실패**다.
- **`CLASS` 는 쓸모없는 값이 아니다 — 읽는 주체가 컴파일러도 JVM 도 아니다** — 「메모리에 로딩되지 않는다」로만 읽으면 존재 이유가 없어 보인다. 이 정책이 쓰이는 자리는 **`.class` 파일을 직접 읽는 도구**다 — 정적 분석기가 `@Nullable` 을 보고 널 검사를 하거나, 커버리지 도구가 생성된 코드를 표시한 애노테이션을 걸러내는 식이다. 그리고 이득이 하나 더 있다: **애노테이션 타입이 실행 시점 클래스패스에 없어도 된다.** 라이브러리가 소비자에게 자기 애노테이션 의존을 강제하지 않는 방법이 이것이다 → [[class-file-format]] · [[classpath]]
- **실행 시점에 애노테이션 타입이 없으면 예외가 아니라 무시다** — `RUNTIME` 으로 남겨 두고 그 애노테이션 클래스를 배포물에서 빼면, `getAnnotations()` 는 **터지지 않고 그 항목만 건너뛴다.** 「없으면 오류가 나겠지」로 기대하면 안 되고, 그래서 위의 `CLASS` 항목이 성립한다. 클래스 로딩이 실패하지 않는 몇 안 되는 「없는 것을 참조하는」 자리다 → [[class-loading]]
- **`SOURCE` 는 「컴파일러가 검사한다」와 같은 말이 아니다** — `@Override` 는 `SOURCE` 이면서 컴파일러가 검사하고, `@SuppressWarnings` 도 `SOURCE` 이지만 검사가 아니라 **경고를 끄는** 일을 한다. 반대로 내가 만든 애노테이션을 `SOURCE` 로 해도 컴파일러는 그것을 **아무 일도 하지 않고 버린다** — 애노테이션 프로세서를 등록하지 않았다면 읽는 주체가 없다. **정책은 「남는가」만 정하고 「검사되는가」는 정하지 않는다** → [[annotation]]
- **로컬 변수에 붙인 애노테이션은 `RUNTIME` 이어도 리플렉션으로 읽을 수 없다** — 클래스 파일에 로컬 변수 선언의 애노테이션을 담는 자리가 없다. 같은 노트의 `@Target` 절이 `LOCAL_VARIABLE` 을 정식 값으로 가르치므로 **「`@Target(LOCAL_VARIABLE)` + `@Retention(RUNTIME)`」이 문법적으로는 되지만 읽을 방법이 없는 조합**이 되는데, 필기는 두 메타 애노테이션을 각각 배우고 **조합에 금지 구역이 있다는 것**은 다루지 않았다. 그 자리의 애노테이션을 쓰는 쪽은 컴파일 시점 도구뿐이다 → [[annotation-target]] · [[variable-scope]]
- **`@Retention` 은 애노테이션에만 붙는다 — 그리고 하나만 붙는다** — 클래스나 메서드에 `@Retention` 을 붙이면 컴파일 오류다(`@Target(ANNOTATION_TYPE)` 으로 스스로를 제한하고 있다). **메타 애노테이션이 자기 자신을 같은 문법으로 제약한다**는 것이 이 문법의 재귀적인 자리이고, 그래서 `@Retention` 자체도 `RUNTIME` 으로 선언되어 있다 — 그러지 않으면 JVM 이 「이 애노테이션이 어디까지 남는가」를 실행 중에 알 수 없다 → [[annotation-target]]
- **필기의 코드는 문법이 아니라 자리표시자다** — `@RETENTION(value = RetentionPolicy."PolicySetting")` 에 두 가지가 섞여 있다. ① 이름이 `@RETENTION` 으로 전부 대문자인데 실제는 **`@Retention`** 이다(자바는 대소문자를 구분하므로 그대로는 컴파일되지 않는다). ② `RetentionPolicy."PolicySetting"` 은 **「여기에 값을 넣어라」는 표시**이지 문법이 아니다 — `RetentionPolicy` 는 열거 타입이므로 `RetentionPolicy.RUNTIME` 처럼 **상수 이름을 그대로** 적는다. 문자열이 아니라 상수라는 것이 중요한 이유는 **오타가 컴파일 오류로 잡히기 때문**이다 — MyBatis 의 문장 id 처럼 문자열이면 실행 시점까지 간다 → [[literal]] · [[mybatis]]
- **`RetentionPolicy.CLASS` 를 「클래스에 붙이는 정책」으로 읽으면 어긋난다** — 값 이름이 `CLASS` 라서 `@Target(ElementType.TYPE)` 과 헷갈리는 자리다. 여기서 `CLASS` 는 **`.class` 파일**을 가리키고 붙이는 대상과 아무 관계가 없다. 두 메타 애노테이션이 각각 「어디까지 남는가」와 「어디에 붙는가」를 정하는데 값 이름이 서로의 영역처럼 들린다 → [[annotation-target]]

## 함께 보는 개념

- [[annotation]] — 이 정책이 붙는 대상
- [[annotation-target]] — 같은 회차의 짝이 되는 메타 애노테이션
- [[reflective-annotation-access]] — `RUNTIME` 이어야 성립하는 읽기
- [[class-file-format]] · [[bytecode]] — `CLASS` 정책이 남기는 자리
- [[classpath]] — 남긴 것이 실행 시점 의존이 되는 이유
- [[compilation]] — 세 값이 가리키는 시각들
- [[class-loading]] — 없는 애노테이션이 조용히 무시되는 지점
- [[jvm]] — `RUNTIME` 정보를 들고 있는 주체
- [[exception-handling]] — `null` 이 `NullPointerException` 으로 오는 자리
- [[literal]] — 열거 상수와 문자열의 차이
- [[comment]] — 「컴파일할 때 제거된다」를 공유하는 쪽

## 출처

- [[2024-08-21-Day60]] — 「RetentionPolicy」 절이 이 개념이다. `CLASS`·`SOURCE`·`RUNTIME` 세 값의 뜻을 각각 한 줄로 정확히 적고 **`CLASS` 가 기본값**임을 `<default>` 로 표시했으며, 「RetentionPolicy는 annotation을 만들때 설정한다」로 이것이 쓰는 쪽이 아니라 **만드는 쪽의 선택**이라는 것을 짚었다. 같은 노트의 「property 값 추출」·「배열 property 추출」 예제가 실제로 `@Retention(RetentionPolicy.RUNTIME)` 을 달고 있어 이 절이 그 예제들의 전제인데, **왜 붙였는지는 적혀 있지 않고**(빼면 `getAnnotation` 이 `null` 이다) `@Target` 절 예제에는 없는 비대칭도 설명되지 않는다. 코드로 실린 `@RETENTION(value = RetentionPolicy."PolicySetting")` 은 이름이 전부 대문자인 오기이고 값 자리는 문법이 아니라 자리표시자다. `CLASS` 정책을 읽는 주체가 누구인지, 애노테이션 타입이 실행 시점에 없으면 조용히 무시된다는 것, 로컬 변수 애노테이션은 `RUNTIME` 이어도 읽을 수 없다는 것은 다루지 않았다

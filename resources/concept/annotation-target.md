---
type: concept
id: annotation-target
title: 애노테이션 적용 대상 (@Target)
aliases:
  - "@Target"
  - ElementType
  - 적용 대상 제한
  - 애노테이션 적용 대상
up:
  - 2024-08-21-Day60
tags:
  - java
  - 메타데이터
  - 컴파일
  - 문법
---

# 애노테이션 적용 대상 (@Target)

**내가 만든 애노테이션을 어떤 선언에 붙일 수 있는지 미리 못 박아 두고, 그 밖에 붙이면 컴파일 오류가 나게 하는 것.** 필기의 한 줄이 그대로다 — 「@Target을 사용하여 애노테이션을 붙일 수 있는 범위를 제어할 수 있다」. **애노테이션이 「무엇을 만들어 주는 것」이 아니라 검사받는 표시라는 성질이, 여기서 만드는 쪽에도 적용된다** → [[annotation]] · [[compilation]]

## 정의

값이 `ElementType` 의 열거 상수이고, 여러 개를 배열로 준다. 필기가 같은 뜻의 세 표기를 나란히 적었다.

```java
@Target(value = {ElementType.TYPE}) // 클래스나 인터페이스 선언에만 붙일 수 있다.
@Target(value = ElementType.TYPE)   // 한 개의 값만 설정할 경우 중괄호 생략 가능하다.
@Target(ElementType.TYPE)           // 프로퍼티 이름이 'value'일 경우 이름 생략 가능하다
```

**셋이 같은 것을 가리킨다** — 그리고 이 세 줄이 애노테이션 프로퍼티의 일반 규칙을 그대로 보이는 예다(값 하나면 중괄호 생략, 프로퍼티 이름이 `value` 면 이름 생략) → [[annotation]]

필기가 다섯 값을 들고 「등」으로 나머지를 남겼다.

| `ElementType` | 붙는 자리 | 필기의 소절 |
|---|---|---|
| `TYPE` | class · interface · enum · record · **애노테이션 선언** | 「TYPE」 |
| `FIELD` | 필드 (인스턴스·`static` 둘 다) | 「FIELD」 |
| `METHOD` | 메서드 선언 | 「METHOD」 |
| `PARAMETER` | 매개변수 | 「PARAMETER」 |
| `LOCAL_VARIABLE` | 지역 변수 선언 | 「LOCAL_VARIABLE」 |
| `CONSTRUCTOR` | 생성자 | **없다** |
| `ANNOTATION_TYPE` | 애노테이션 선언만 | 없다 |
| `PACKAGE` · `MODULE` | `package-info.java` · 모듈 선언 | 없다 |
| `TYPE_PARAMETER` · `TYPE_USE` | 타입 매개변수 · **타입이 나오는 모든 자리** | 없다 |

**빠진 것 중 `CONSTRUCTOR` 가 눈에 걸린다** — 하루 전 Day59 가 `getDeclaredConstructors()` 로 생성자를 리플렉션의 정식 대상으로 다뤘는데, 애노테이션을 붙일 자리 목록에서는 빠져 있다 → [[reflective-instantiation]]

### 검사 시점이 컴파일이다 — 애노테이션이 오류를 만드는 유일한 자리

필기의 다섯 소절이 전부 **주석으로 막아 놓은 줄**로 되어 있고, 그 주석이 곧 실험 결과다.

```java
// TYPE 타입(인터페이스와 클래스)에만 붙일 수 있다.
@MyAnnotation // OK!
public class MyClass {

  //  @MyAnnotation
  // int i; // 컴파일 오류!

  //  @MyAnnotation
  // public void m(/*@MyAnnotation*/ int p) { 컴파일 오류!
    /*@MyAnnotation
    int a;  컴파일 오류!*/
  }

}
```

**「컴파일 오류!」라고 적힌 줄들이 이 문법의 값 전부다.** [[annotation]] 노트가 「애노테이션이 코드를 바꾸는 것은 아니다 — 누군가 읽어야 효과가 생긴다」고 적었는데, `@Target`·`@Retention` 같은 메타 애노테이션에서는 **그 「누군가」가 컴파일러로 고정되어 있다.** 아무 프레임워크를 붙이지 않아도 효과가 나는 것이 이 둘뿐이다 → [[annotation-retention]]

## 사용 예시

Day60 이 다섯 값에 각각 클래스를 하나씩 만들어 「어디에 붙고 어디에 안 붙는가」를 대비시켰다. `METHOD` 쪽이 가장 또렷하다.

```java
// @MyAnnotation3는 메서드에만 붙일 수 있다.
//@MyAnnotation3
public class MyClass3 {

  /*@MyAnnotation3*/ int i;
  /*@MyAnnotation3*/ static int i2;


  @MyAnnotation3
  public void m(/*@MyAnnotation3*/ int p) {
    /*@MyAnnotation3*/ int a;
  }

}
```

**한 클래스 안에 다섯 자리를 놓고 하나만 살려 둔 형태**다 — 클래스 선언·필드 둘·매개변수·지역 변수가 주석이고 메서드 선언만 살아 있다. `LOCAL_VARIABLE` 쪽은 같은 배치에서 지역 변수만 살아 있다.

```java
// @MyAnnotation4는 로컬 변수에만 붙일 수 있다.
//@MyAnnotation4
public class MyClass4 {

  /*@MyAnnotation4*/ int i;
  /*@MyAnnotation4*/ static int i2;


  //@MyAnnotation4
  public void m(/*@MyAnnotation4*/ int p) {
    @MyAnnotation4 int a;
  }

}
```

**같은 골격을 다섯 번 반복해 살아 있는 줄만 옮기는 방식**이라, 다섯 소절을 나란히 놓고 **어느 줄이 주석이 아닌지**만 보면 그 값이 무엇을 허용하는지가 읽힌다. 필기가 설명을 한 줄로 줄인 것(「메서드 타입만 가능하다」·「지역변수만 사용 가능하다」)이 그래서 부족하지 않다 — 다만 다섯 중 하나(`FIELD`)는 코드가 옮겨지지 않았다(아래) → [[access-modifier]] · [[variable-scope]]

## 왜 중요한가

**애노테이션을 잘못 붙이는 실수가 실행 시점에서 컴파일 시점으로 올라온다.** `@Target` 이 없으면 내 애노테이션을 필드에도 메서드에도 클래스에도 붙일 수 있고, 그중 **프레임워크가 읽는 자리는 하나뿐**이다. 나머지에 붙은 것은 조용히 무시되므로 「붙였는데 아무 일도 안 일어난다」가 되고, 원인이 「엉뚱한 자리에 붙였다」라는 것은 코드만 봐서는 드러나지 않는다. `@Target` 은 **그 무시를 오류로 바꾼다** → [[annotation-retention]]

**그리고 애노테이션을 만드는 사람이 계약을 문법으로 적을 수 있게 된다.** 「이것은 메서드에 붙이는 애노테이션이다」를 문서에 쓰면 아무도 확인하지 않지만, `@Target(ElementType.METHOD)` 로 쓰면 컴파일러가 확인한다 — [[annotation]] 이 `@Override` 에 대해 적어 둔 「검사받는 설명과 검사받지 않는 설명의 차이」가 **내가 만드는 애노테이션에도 그대로 적용되는 자리**다.

**기본값이 「제약 없음」이라는 점이 이 문법의 방향을 정한다.** `@Target` 은 무언가를 켜는 것이 아니라 **좁히는** 것이다. 그래서 안 쓰면 넓게 열려 있고, 쓰면 그 순간부터 목록에 없는 자리는 전부 막힌다 — **값을 하나 추가할 때마다 문법이 넓어지는 방향**이고, 좁게 시작해 필요할 때 넓히는 것이 안전한 순서다.

## 경계와 오해

- **`@Target` 을 안 붙이면 「아무 데도 못 붙는다」가 아니라 「거의 어디에나 붙는다」다** — 필기가 「범위를 제어할 수 있다」로만 적어 기본 상태가 무엇인지 나오지 않는데, 없으면 **타입 매개변수를 뺀 모든 선언 자리**에 붙는다. 그래서 필기 앞 절(「annotation 사용」)의 `@MyAnnotation` 이 클래스·필드·메서드·매개변수·지역 변수에 **전부** 붙는 것은 자유롭게 만든 애노테이션이 아니라 **`@Target` 을 안 적은 결과**다 — **두 절이 같은 애노테이션 이름으로 정반대 상태를 보이면서 그 차이를 말하지 않는다.**
- **`@Target({})` 은 어디에도 붙일 수 없다는 뜻이다** — 빈 배열이 「제한 없음」이 아니라 「전부 금지」다. 쓸모가 있는 자리가 있다 — 다른 애노테이션의 **프로퍼티 타입으로만** 쓰이는 애노테이션이 그렇다. 「빈 값 = 기본값」으로 읽으면 정반대가 되는 자리이고, 이것이 「없는 것」과 「비어 있는 것」이 다르다는 그 구분의 문법 사례다.
- **`TYPE` 은 클래스와 인터페이스만이 아니다 — 애노테이션 선언도 포함한다** — 필기가 「class, interface, enum에 붙일 수 있다」로 셋을 들었는데(record 는 이 시점에 안 배웠다), **애노테이션 선언도 인터페이스의 한 종류라 `TYPE` 에 들어간다.** 애노테이션에만 붙게 하려면 `ANNOTATION_TYPE` 을 써야 하고, `@Retention`·`@Target` 자신이 바로 그렇게 선언되어 있다 — **그래서 `@Retention` 을 클래스에 붙이면 컴파일 오류다** → [[annotation-retention]] · [[interface]]
- **`TYPE_USE` 는 「선언에 붙인다」는 정의를 깨는 값이다** — [[annotation]] 이 애노테이션을 「클래스·변수·메서드 선언에 붙이는 표시」로 정의하는데, `TYPE_USE` 는 **타입이 나오는 모든 자리**에 붙는다 — `List<@NonNull String>`·`(@NonNull String) obj` 처럼 선언이 아닌 곳이다. 필기의 「등」이 가린 값 중 정의를 넓히는 것이 이것이고, 널 검사 도구들이 쓰는 자리다.
- **`FIELD` 소절의 코드가 `TYPE` 소절의 코드와 완전히 같다 — 주석까지 그대로다** — 「// TYPE 타입(인터페이스와 클래스)에만 붙일 수 있다.」로 시작하고 살아 있는 애노테이션도 클래스 선언에 붙은 것이다. **즉 다섯 소절 중 `FIELD` 만 예시가 없다** — 붙여넣기하고 살릴 줄을 옮기지 않은 자리이고, 그래서 「필드 타입에만 가능하다」는 한 줄만 남는다. 이 노트가 그 자리를 채운다: `@Target(ElementType.FIELD)` 이면 `int i;`·`static int i2;` 앞의 애노테이션이 살아나고 **클래스 선언 쪽이 컴파일 오류**가 된다 — `static` 인지는 상관없다.
- **그 두 소절의 코드는 그대로 컴파일되지 않는다 — 중괄호가 하나 남는다** — `// public void m(…) {` 의 여는 중괄호가 **주석 안에** 있어서, 뒤따르는 `}` 가 클래스를 닫고 마지막 `}` 가 짝 없이 남는다. 「컴파일 오류!」를 보이려고 주석 처리한 것이 **의도하지 않은 컴파일 오류**를 만든 자리다 — 메서드 선언 전체를 주석으로 막을 때 닫는 중괄호까지 함께 막지 않으면 이렇게 된다.
- **`PARAMETER` 소절의 주석과 소제목이 어긋난다** — 「@MyAnnotation5는 로컬 변수, 파라미터, 필드에만 붙일 수 있다」라고 적혀 있는데 **필드와 지역 변수 쪽은 주석으로 막혀 있고** 매개변수만 살아 있다. 즉 주석이 말하는 셋 중 둘이 「붙일 수 없다」로 표시된 상태다. 셋 다 허용하려면 `@Target({ElementType.FIELD, ElementType.PARAMETER, ElementType.LOCAL_VARIABLE})` 이고 그러면 그 두 줄이 살아 있어야 한다 — **주석은 여러 값을 준 경우를 말하고 코드는 하나만 준 경우를 보이는** 어긋남이다. 그리고 소제목 「매개만 사용 가능하다」는 「매개변수」가 잘린 것이다.
- **`@Target` 은 붙일 자리만 정하고 「누가 읽는가」는 정하지 않는다** — `@Target(ElementType.METHOD)` 로 좁혀도 실행 중에 읽으려면 [[annotation-retention]] 이 `RUNTIME` 이어야 한다. 두 메타 애노테이션은 **직교하는 두 축**이고, 그래서 둘 다 붙는 것이 보통이다. 필기가 두 절을 이어 배우면서 둘을 함께 쓴 예를 한 번도 보이지 않아 **둘 중 하나만 있으면 되는 것처럼 읽힌다** → [[reflective-annotation-access]]
- **`ElementType.TYPE` 과 `RetentionPolicy.CLASS` 는 서로의 낱말을 쓴다** — 하나는 「붙는 자리가 타입 선언」이고 하나는 「`.class` 파일까지 남는다」인데, 이름만 보면 앞의 것이 파일 이야기 같고 뒤의 것이 클래스 선언 이야기 같다. 두 메타 애노테이션을 나란히 배우는 자리에서 값 이름이 교차하는 함정이다 → [[annotation-retention]]

## 함께 보는 개념

- [[annotation]] — 이 제약이 붙는 대상
- [[annotation-retention]] — 직교하는 다른 축
- [[reflective-annotation-access]] — 붙인 것을 실제로 읽는 쪽
- [[compilation]] — 이 검사가 일어나는 시점
- [[interface]] — 애노테이션 선언이 `TYPE` 에 들어가는 이유
- [[reflective-instantiation]] — 목록에서 빠진 `CONSTRUCTOR` 자리
- [[access-modifier]] · [[variable-scope]] — 소절들이 놓고 비교하는 자리들
- [[static-member]] — 필드 둘을 나란히 둔 이유
- [[method-overriding]] — `@Override` 가 `METHOD` 로 좁혀진 실례
- [[comment]] — 「컴파일 오류!」를 보이는 데 쓰인 도구

## 출처

- [[2024-08-21-Day60]] — 「target」 절과 그 아래 다섯 소절(`TYPE`·`FIELD`·`METHOD`·`LOCAL_VARIABLE`·`PARAMETER`)이 이 개념이다. 「@Target을 사용하여 애노테이션을 붙일 수 있는 범위를 제어할 수 있다」로 목적을 적고, `@Target(value = {ElementType.TYPE})`·`@Target(value = ElementType.TYPE)`·`@Target(ElementType.TYPE)` 세 표기가 같다는 것으로 **중괄호 생략·`value` 이름 생략** 규칙을 다시 보였다. 다섯 소절이 **같은 골격의 클래스에 다섯 자리(클래스 선언·필드 둘·매개변수·지역 변수)를 놓고 허용되는 줄만 살려 두는 방식**이라 「어디에 붙고 어디에 안 붙는가」가 주석 처리 여부로 읽힌다 — 「컴파일 오류!」라고 적힌 주석들이 이 문법의 검사 시점이 컴파일이라는 것을 그대로 보인다. 다만 **`FIELD` 소절의 코드가 `TYPE` 소절의 것과 주석까지 똑같이 복사되어 필드 예시가 아예 없고**, 그 두 소절의 코드는 메서드 선언의 여는 중괄호가 주석 안에 있어 중괄호가 하나 남아 컴파일되지 않으며, `PARAMETER` 소절은 주석이 「로컬 변수, 파라미터, 필드에만」이라 말하면서 그중 둘을 막아 두었다. `@Target` 을 안 붙이면 거의 모든 선언에 붙는다는 기본 상태, `@Target({})` 의 뜻, 목록에서 빠진 `CONSTRUCTOR`·`ANNOTATION_TYPE`·`TYPE_USE`, `@Retention` 과 함께 써야 실행 중에 읽힌다는 것은 다루지 않았다

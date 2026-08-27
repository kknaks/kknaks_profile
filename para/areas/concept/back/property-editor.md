---
type: concept
id: property-editor
title: PropertyEditor (설정 문자열을 값으로 바꾸기)
aliases:
  - PropertyEditor
  - CustomEditor
  - PropertyEditorSupport
  - 프로퍼티 에디터
up:
  - 2024-10-04-Day88
  - 2024-10-16-Day94
tags:
  - spring
  - 설정
  - 형변환
---

# PropertyEditor (설정 문자열을 값으로 바꾸기)

**설정 파일에 문자열로 적은 값을 자바 타입으로 바꾸는 변환기.** 설정은 언제나 텍스트인데 필드는 타입이 있으므로, 그 사이에 반드시 무언가가 있어야 한다.

## 정의

스프링에는 기본 변환기들이 내장돼 있다.

```xml
<property name="name"    value="소나타"/>   <!-- String  — 그대로 -->
<property name="year"    value="2024"/>     <!-- int     — 변환됨 -->
<property name="used"    value="true"/>     <!-- boolean — 변환됨 -->
<property name="madeAt"  value="2024-10-04"/>  <!-- java.sql.Date — 못 한다 -->
```

**기본형과 그 래퍼, 문자열까지는 자동이고 그 밖은 없다.** 없으면 두 가지 길이 있다.

### 1. 팩토리로 객체를 만들어 넣는다

```xml
<property name="madeAt">
  <bean class="java.sql.Date" factory-method="valueOf">
    <constructor-arg value="2024-10-04"/>
  </bean>
</property>
```

값 하나를 넣기 위해 **빈 하나를 만드는** 셈이라 같은 타입이 여러 곳에 나오면 반복된다 → [[factory-bean]]

### 2. 변환기를 등록한다

```java
public class CustomDateEditor extends PropertyEditorSupport {
  @Override
  public void setAsText(String text) throws IllegalArgumentException {
    this.setValue(Date.valueOf(text));   // 바꿔서 내부에 저장하면 컨테이너가 꺼내 쓴다
  }
}
```

```xml
<bean class="org.springframework.beans.factory.config.CustomEditorConfigurer">
  <property name="customEditors">
    <map>
      <entry key="java.sql.Date" value="com.eomcs...CustomDateEditor"/>
    </map>
  </property>
</bean>
```

**한 번 등록하면 그 타입의 모든 프로퍼티에 적용된다** — 첫 번째 방법이 자리마다 반복되는 것과 갈린다.

## 왜 중요한가

**설정은 문자열이고 프로그램은 타입이 있다 — 그 경계가 어디인지 알아야 오류를 읽을 수 있다.** 「`"소나타"` 를 `int` 로 못 바꾼다」는 예외는 코드가 아니라 **설정과 필드가 안 맞는다**는 뜻이고, 볼 곳이 자바가 아니라 XML 이다 → [[type-casting]] · [[number-parsing]]

**그리고 이 자리가 확장점이라는 것이 스프링의 성격을 보인다.** 프레임워크가 모르는 타입을 쓰는 것은 당연한데, 그때마다 프레임워크를 고칠 수는 없다. **바꾸는 방법을 끼워 넣게 열어 둔** 것이 답이다 → [[bean-post-processor]] · [[open-closed-principle]]

## 경계와 오해

- **`java.sql.Date` 가 안 되는 것은 「날짜라서」가 아니다** — 그 타입의 변환기가 기본에 없을 뿐이다. 무엇이 되고 무엇이 안 되는지는 **목록의 문제**이지 성질의 문제가 아니다 → [[date-time]]
- **변환은 실행이 아니라 기동에서 일어난다** — 싱글턴 빈은 컨테이너가 뜰 때 만들어지므로 설정 값이 틀리면 **거기서 멈춘다.** 늦게 아는 것보다 낫다 → [[bean-scope]]
- **`setAsText` 가 값을 「돌려주지」 않는다** — `setValue()` 로 내부에 저장하면 컨테이너가 꺼내 간다. 반환값을 쓰는 모양이 아니라 헷갈리는 자리다
- **에디터는 타입당 하나다** — 같은 `java.sql.Date` 를 어떤 곳에서는 `yyyy-MM-dd` 로, 다른 곳에서는 다른 형식으로 받고 싶으면 이 방법으로는 안 된다. **전역 규칙**이다
- **지금은 `Converter`/`ConversionService` 가 이 자리를 대체했다** — `PropertyEditor` 는 원래 자바빈 규격의 것이고 상태를 갖는(쓰레드 안전하지 않은) 설계라, 이후 스프링이 대체 장치를 내놓았다. 여기서 배울 것은 **문자열↔타입 경계에 변환기가 있다**는 구조다

## 함께 보는 개념

- [[bean-definition]] — 값이 문자열로 적히는 자리
- [[factory-bean]] — 변환기 없이 객체를 만들어 넣는 방법
- [[bean-post-processor]] — 같은 방식으로 등록되는 확장점
- [[externalized-configuration]] — 문자열로 들어오는 값의 출처
- [[type-casting]] · [[number-parsing]] — 같은 문제의 자바 쪽 이름
- [[date-time]] — 기본 변환기가 없어 문제가 드러난 타입
- [[handler-method-argument]] — 웹 요청 쪽에서 이 변환이 필요한 자리

## 출처

- [[2024-10-16-Day94]] — 열이틀 뒤. **같은 장치가 웹 계층에서 다시 필요해진다.** 요청 파라미터도 결국 문자열이라, `Date` 나 값 객체를 아규먼트로 받으려면 변환기가 있어야 한다. 등록 방법이 IoC 쪽과 다르다 — `@InitBinder` 를 붙인 메서드에서 `WebDataBinder.registerCustomEditor(타입, 에디터)` 를 부르고, **핸들러를 부르기 전에 매번 실행된다.** 컨트롤러마다 쓰는 대신 `@ControllerAdvice` 클래스로 빼면 전역이 된다. `CarPropertyEditor` 가 콤마로 구분된 문자열(`"소나타,5,true,2024-10-16"`)을 객체로 만드는 예가 이 장치의 쓸모를 잘 보인다
- [[2024-10-04-Day88]] — 「property 설정」 절이 **「Spring IoC 는 property Editor 가 내장되어 있어 String 과 Primitive Type 을 자동 형 변환한다 / Editor 에 등록되어 있지 않으면 CustomEditor 에 등록해야 한다」**로 이 개념의 경계를 한 줄에 담았다. XML 예시가 String·int·boolean 은 되고 **`Date` 는 주석 처리해 두어** 안 된다는 것을 보이고, 이어서 두 가지 해법을 순서대로 제시한다 — `factory-method` 로 객체를 만들어 넣는 방법과 `PropertyEditorSupport` 를 상속한 `CustomDateEditor` 를 `CustomEditorConfigurer` 에 등록하는 방법. 등록 XML 의 주석이 **key 는 「어떤 타입으로 바꿀 것인지」, value 는 「변환기 클래스 이름」**이라고 정확히 적혀 있다. 다만 두 방법 중 어느 쪽이 언제 맞는지, 에디터가 타입당 하나라는 제약은 다루지 않았다

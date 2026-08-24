---
type: concept
id: class-file-format
title: class 파일 구조 (Class File Format)
aliases:
  - class 파일 구조
  - class file format
  - CAFEBABE
  - javap
up:
  - 2024-05-30-Day05
tags:
  - java
  - jvm
  - bytecode
---

# class 파일 구조 (Class File Format)

`.class` 파일이 지켜야 하는 바이트 배치 규격. [[jvm]] 은 이 순서대로 읽으므로, 규격을 벗어나면 파일로는 존재해도 클래스로 인식되지 않는다.

## 정의

파일 앞부터 정해진 순서로 읽힌다. Java Specification 이 규격 원본이다.

| 자리 | 값(예) | 뜻 |
|---|---|---|
| 매직 넘버 | `CAFE BABE` | "이것은 Java class 파일이다" |
| 버전 | `0000 0034` | 클래스 파일 버전 (Java 8) |
| [[constant-pool]] 크기 | `0000` | 뒤따르는 상수 풀 항목 수 |
| 접근 플래그 | `0021` | `public` + `super` |
| this_class | 상수 풀 인덱스 | 이 클래스가 무엇인가 |
| super_class | 상수 풀 인덱스 | 부모가 무엇인가 → [[inheritance]] |
| interfaces / fields / methods | 각 개수 | 없으면 `0000` |

**이름이 직접 적히지 않는다.** 클래스 이름도 부모 이름도 [[constant-pool]] 의 몇 번째 항목인지를 가리키는 인덱스로만 들어간다.

## 사용 예시

상수 풀을 비운 채 헤더만 만들면 `javap` 가 클래스를 못 찾는다.

```plaintext
Java File: CAFE BABE
Version 8: 0000 0034
Constant Pool Size of ZERO: 0000
Super Public: 0021
Unknown index of class in constant pool: 0000
Unknown index of super class in constant pool: 0000
zero interfaces: 0000
zero fields: 0000
zero methods: 0000
```

`javap` 로 열어 보면 **class 를 설정하지 않았다**는 결과가 나온다 — 헤더는 맞지만 this_class 가 가리킬 상수 풀 항목이 없기 때문이다. 부모를 채우려면 상수 풀에 `java/lang/Object` 문자열을 넣고 그 인덱스를 super_class 에 적는다.

## 왜 중요한가

**컴파일러가 무엇을 만드는지가 이 규격이다.** [[bytecode]] 를 "중간 코드"라고만 알면 실체가 흐린데, 열어 보면 정해진 자리에 정해진 바이트가 들어간 파일이다. JVM 이 왜 어느 OS 에서든 같게 실행하는지도 여기서 분명해진다 — 읽는 규격이 하나로 고정되어 있기 때문이다.

`javap` 로 클래스를 열어 볼 수 있다는 것도 여기서 나온다. 라이브러리만 있고 소스가 없을 때 메서드 시그니처를 확인하는 실제 수단이다.

## 경계와 오해

- **손으로 쓰는 것은 학습용이다** — 옛 필기의 결론이 "하지마라, 걍 java로 소스파일을 만들어라"였다. 맞는 결론이다. 다만 **한 번 해 보면 `.class` 가 마법이 아니라는 것이 남는다** — 그게 이 실습의 값이고, 실무에서 쓸 기술은 아니다.
- **class 파일 ≠ 실행파일** — 규격을 지켜도 OS 가 직접 실행하지 못한다. JVM 이 읽어야 한다.
- **버전은 숫자 그대로가 아니다** — `0034`(52)가 Java 8 이다. 파일 버전과 Java 버전 번호가 어긋나므로 표를 봐야 한다.

## 함께 보는 개념

- [[constant-pool]] — 이름과 참조가 실제로 사는 자리
- [[bytecode]] — 이 규격을 따르는 산출물
- [[jvm]] — 이 규격대로 읽는 주체

## 출처

- [[2024-05-30-Day05]] — 16진수로 class 파일을 직접 만들며 매직 넘버·버전·접근 플래그·this_class/super_class 배치를 배웠고, `javap` 로 확인했다

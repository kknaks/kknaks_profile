---
type: concept
id: string-manipulation
title: 문자열 다루기 (substr · find · reverse)
aliases:
  - 문자열 처리
  - string manipulation
  - substr
  - split
up:
  - 2025-05-07-Pr9996
  - 2025-05-03-Pr10988
tags:
  - 문자열
  - 알고리즘
  - 구현
---

# 문자열 다루기 (substr · find · reverse)

**자르고 찾고 뒤집는 몇 개의 연산으로 대부분의 문자열 문제가 끝난다.** 아는 만큼 코드가 짧아지고, 모르면 직접 만들게 된다.

## 정의

| 연산 | 하는 일 |
|---|---|
| `substr(시작, 길이)` | 시작 위치부터 길이만큼 **잘라 낸다** |
| `find(찾을 것, 시작)` | 시작 이후 **첫 위치**를 돌려준다 (없으면 `npos`) |
| `reverse(begin, end)` | 구간을 **뒤집는다** |

### 패턴 매칭 — 자르고 비교하기

`앞*뒤` 형태의 패턴에 파일명이 맞는지 보는 문제는 **정규식 없이** 풀린다.

```
1. 패턴을 * 기준으로 앞·뒤로 나눈다        ← find + substr
2. 파일명 길이가 앞+뒤보다 짧으면 탈락      ← 겹침 방지
3. 앞부분이 파일명 앞과 같은가
4. 뒷부분이 파일명 뒤와 같은가
```

**2번을 빠뜨리면 짧은 이름에서 앞뒤가 겹쳐 통과**한다 — 이 문제의 함정이다.

### 직접 만드는 split

C++ 에는 `split` 이 없어서 `find` + `substr` 로 만든다.

```cpp
vector<string> split(string& input, string delimeter) {
    vector<string> result;
    int start = 0;
    int end = input.find(delimeter);
    while (end != string::npos) {
        result.push_back(input.substr(start, end - start));
        start = end + delimeter.size();     // 구분자 길이만큼 건너뛴다
        end = input.find(delimeter, start);
    }
    result.push_back(input.substr(start));   // 마지막 조각
    return result;
}
```

**마지막 조각을 반복문 밖에서 넣는 것**과 **구분자 길이만큼 건너뛰는 것**이 이 함수의 두 요점이다.

## 왜 중요한가

**문자열은 배열인 동시에 값이다.** 인덱스로 접근하면 배열이고, 통째로 비교·복사하면 값이다 — 두 성질을 오가는 것이 문자열 문제의 감각이다 → [[array]] · [[string-comparison]]

**그리고 라이브러리를 아는 것이 실력의 일부다.** 뒤집기 한 줄이면 될 팰린드롬 판별을 반복문으로 짜면 **경계에서 틀릴 여지**가 생긴다.

## 경계와 오해

- **`find` 는 없을 때 `npos` 를 돌려준다** — `-1` 과 비교하는 코드가 흔한데, `npos` 는 부호 없는 최댓값이라 **타입에 따라 비교가 어긋날 수 있다**
- **`substr` 은 복사본을 만든다** — 반복문 안에서 자주 부르면 **복사 비용이 쌓인다** → [[time-complexity]]
- **인덱스와 길이를 헷갈린다** — `substr(start, end - start)` 에서 두 번째 인자가 **끝 위치가 아니라 길이**다. 가장 흔한 실수 자리
- **문자열 복사는 값 복사다** — 이 문제집이 「string 의 복사 : **deep copy** 를 사용하여 문자열을 복사한다」로 적어 둔 대로, 원본과 사본이 서로 영향을 주지 않는다 → [[object-cloning]]
- **문자 하나와 문자열은 다른 타입이다** — `'a'` 와 `"a"` 를 섞으면 컴파일이 막히거나 다르게 동작한다. 자바스크립트가 이 구별을 없앤 것과 대비된다 → [[javascript-type]]

## 함께 보는 개념

- [[simulation]] — 문자열 문제가 대개 속하는 부류
- [[array]] — 인덱스로 접근할 때의 성질
- [[character-encoding]] — 문자를 숫자로 다룰 때
- [[string-comparison]] — 값으로 비교할 때
- [[time-complexity]] — 자르고 복사하는 비용

## 출처

- [[2025-05-07-Pr9996]] — 패턴 매칭 문제. **주요 메서드를 표로 정리해 둔 것**이 이 노트의 값이다 — 「`substr(int start_pos, int len_size)` : start_pos 부터 len_size 만큼 문자열 추출 / `find(string delimeter, int start_pos)` : start_pos 이후 첫 번째 delimeter 의 위치 반환」. 그리고 **C++ 에 없는 `split` 을 `find`+`substr` 로 직접 만드는 코드**가 실려 있어, 「없으면 만든다」의 표준형을 남겼다
- [[2025-05-03-Pr10988]] — 팰린드롬 판별. `std::reverse` 로 뒤집어 비교하는 세 줄 풀이이고, **문자열 복사가 deep copy 라는 것**을 함께 적어 두었다 → [[simulation]]

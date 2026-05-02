---
concept:
- rand() 함수는 0부터 약 42억까지의 난수를 생성하며, 게임 개발에서 확률 계산의 기초가 된다.
- 모듈로 연산(%)으로 난수 범위를 축소할 때, 원래 범위가 축소 범위의 배수가 아니면 일부 숫자가 다른 숫자보다 높은 확률로 나타난다.
- 메이플스토리는 rand() % 10억을 사용했는데, 42억÷10억 ≈ 4.29이므로 0~2억 9천만 범위의 숫자가 25% 더 높은 확률로 나타난다.
- 이로 인해 29% 이하의 드롭률 아이템들이 표기된 확률보다 실제로 더 높은 드롭 확률을 갖게 된다.
- 작은 드롭률 버프(5%, 10%)는 이 편향 때문에 반영되지 않고, 17% 이상 증가할 때만 변화가 감지된다.
date: 2026.05.02
day: Day 02
duration: '5:54'
enriched_at: '2026-05-02T22:03:06+09:00'
id: C-002
intent: ''
kind: study
speaker: 코딩애플
status: published
summary:
  en: Modulo bias in C's rand() function distorts game drop rates, causing probability
    calculation errors.
  ko: C언어 rand() 함수의 모듈로 연산은 편향을 일으켜 게임의 드롭률을 왜곡시킨다.
tags:
- '#modulo-bias'
- '#random-number-generation'
- '#probability'
- '#c-programming'
- '#bug-analysis'
- '#game-development'
title:
  en: Modulo Bias in Game Probability Systems
  ko: 모듈로 편향으로 인한 게임 확률 버그
transcript: true
type: content
youtubeId: RVngRYqs7kA
---

## 개요

게임의 확률 시스템은 플레이어 경험의 핵심이며, 표기된 확률과 실제 확률이 일치해야 합니다. 메이플스토리에서는 아이템 드롭률이 실제로는 표기된 것보다 훨씬 높게 나타나는 버그가 발견되었습니다. 이 버그의 원인은 **모듈로 편향(Modulo Bias)**이라는 프로그래밍 개념으로, 난수 생성과 범위 조정 과정에서 발생합니다. 작은 기술적 선택이 어떻게 전체 게임 경제에 영향을 미치는지 이해함으로써, 프로그래밍의 세부 사항이 얼마나 중요한지 배울 수 있습니다.

## 배경 / 사전 지식

### rand() 함수란?

C 언어의 표준 라이브러리에 포함된 `rand()` 함수는 난수(random number)를 생성합니다. 게임을 포함한 대부분의 프로그램에서 확률적 이벤트를 구현할 때 사용됩니다. 초기 게임들, 특히 메이플스토리가 개발되던 시대에는 이것이 표준적인 난수 생성 방법이었습니다.

- **반환 값**: 0부터 RAND_MAX(대략 약 42억 9천만)까지의 정수
- **특성**: 매 호출마다 다른 값을 반환하며, 이론적으로는 각 값이 동일한 확률로 나타나야 함

### 모듈로(modulo) 연산이란?

모듈로는 `%` 기호로 표현되는 연산으로, 나눗셈의 나머지를 구합니다.

- **예시**: `10 % 3 = 1` (10을 3으로 나눈 나머지는 1)
- **용도**: 큰 범위의 숫자를 더 작은 범위로 변환하는 데 사용됨

### 균등 분포(Uniform Distribution)

난수가 모든 가능한 값에 동일한 확률로 나타나야 한다는 개념입니다. 예를 들어 주사위는 1~6이 각각 1/6의 확률로 나타나야 합니다.

## 핵심 개념

### 1. rand() 함수의 범위 문제

게임에서 확률을 계산하려면 보통 0~99(백분율) 또는 0~1000(천분율) 같은 작은 범위의 난수가 필요합니다. 하지만 `rand()`는 0~42억 범위의 매우 큰 숫자를 반환합니다. 따라서 개발자들은 이 큰 범위를 필요한 작은 범위로 변환해야 합니다.

### 2. 모듈로 편향(Modulo Bias)의 정의

모듈로 연산을 사용하여 난수의 범위를 조정할 때, 만약 `rand()`의 최댓값(RAND_MAX)이 원하는 범위의 배수가 아니면, 일부 숫자들이 다른 숫자보다 더 높은 확률로 나타나는 현상입니다. 이를 모듈로 편향이라고 합니다.

### 3. 편향이 발생하는 원리

예를 들어 `rand()`가 0~8 범위의 값을 반환한다고 가정하고, 우리는 이를 0~5(주사위처럼) 범위로 변환하고 싶다면:

`rand() % 6`을 사용합니다.

**모든 경우의 수:**
- 0 % 6 = 0
- 1 % 6 = 1
- 2 % 6 = 2
- 3 % 6 = 3
- 4 % 6 = 4
- 5 % 6 = 5
- 6 % 6 = 0
- 7 % 6 = 1
- 8 % 6 = 2

결과를 정리하면: 0이 2번, 1이 2번, 2가 2번, 3이 1번, 4가 1번, 5가 1번 나타납니다. 즉, 0, 1, 2는 각각 33.3%의 확률인 반면, 3, 4, 5는 각각 16.7%의 확률입니다. **일부 숫자가 다른 숫자보다 2배 더 높은 확률로 나타나게 됩니다.**

## 작동 원리

### 메이플스토리의 확률 계산 과정

**1단계: 난수 생성**

메이플스토리는 `rand()` 함수를 사용해 0~42억 9천만 범위의 난수를 생성했습니다.

```
난수 = rand()  // 범위: 0 ~ 4,294,967,295
```

**2단계: 범위 축소**

확률 계산을 위해 더 작은 범위로 축소합니다. 메이플은 미세한 확률도 계산하기 위해 10억을 사용했습니다.

```
정규화_난수 = rand() % 1,000,000,000  // 범위: 0 ~ 1,000,000,000
```

**3단계: 확률 비교**

정규화된 난수를 드롭율 값과 비교합니다.

```
if (정규화_난수 < 드롭률_값) {
    // 아이템 드롭
}
```

예를 들어, 1% 드롭률을 구현하려면:
```
if (rand() % 1000000000 < 10000000) {  // 10000000 / 1000000000 = 1%
    drop_item();
}
```

### 편향이 발생하는 이유

- **RAND_MAX**: 약 42억 9천만 (4,294,967,295)
- **나누는 값**: 10억 (1,000,000,000)
- **나눗셈 결과**: 4,294,967,295 ÷ 1,000,000,000 ≈ **4.29** (정수가 아님)

이것이 핵심입니다. 42억을 10억으로 나눈 몫이 4.29이므로, 실제로는:
- 처음 10억에서 4번 반복 가능 → 0~39억 9천만: 각 범위가 4번씩 대응
- 마지막 부분 → 40억~42억 9천만: 추가적으로 5번씩 대응

따라서 0~2억 9천만 범위의 숫자는 다른 범위보다 **25% 더 높은 확률**로 나타나게 됩니다.

### 드롭률 버프의 버그

게임에는 드롭률을 증가시키는 버프가 있습니다. 예를 들어 20% 드롭률을 10% 올리려면:

```
원래: if (rand() % 1000000000 < 200000000)  // 20%

버프 적용 후: if (rand() % 1000000000 < 300000000)  // 30% 로 수정?
또는: if (rand() % 1000000000 < 200000000 + 100000000)  // 직접 더하기?
```

메이플이 실제로 어떤 방식을 사용했든, 모듈로 편향 때문에 **작은 변화가 감지되지 않습니다**. 이유는 각 값의 "실제 무게"가 편향으로 인해 달라지기 때문입니다.

- 5% 증가 (5천만 증가) → 편향 범위가 같으므로 거의 변화 없음
- 10% 증가 (1억 증가) → 여전히 거의 변화 없음
- **17% 이상 증가** → 편향 범위를 벗어나므로 그제야 변화 감지

이것이 메이플의 버프 시스템에서 "17% 이상 올려야 적용된다"는 이상한 문제가 발생한 이유입니다.

## 코드 예시

### 예제 1: 모듈로 편향 시뮬레이션

다음 Python 코드는 편향이 실제로 어떻게 발생하는지 보여줍니다:

```python
def demonstrate_modulo_bias():
    """
    rand()가 0~8을 반환할 때, % 6으로 0~5 범위로 변환하면
    어떤 숫자들이 더 자주 나타나는지 보여줌
    """
    results = {i: 0 for i in range(6)}
    
    # 모든 가능한 rand() 값 순회
    for rand_value in range(9):  # 0~8
        result = rand_value % 6
        results[result] += 1
    
    print("각 숫자의 등장 횟수:")
    for num, count in sorted(results.items()):
        percentage = (count / 9) * 100
        print(f"  {num}: {count}회 ({percentage:.1f}%) {'← 편향!' if count == 2 else ''}")

demonstrate_modulo_bias()
# 출력:
# 각 숫자의 등장 횟수:
#   0: 2회 (22.2%) ← 편향!
#   1: 2회 (22.2%) ← 편향!
#   2: 2회 (22.2%) ← 편향!
#   3: 1회 (11.1%)
#   4: 1회 (11.1%)
#   5: 1회 (11.1%)
```

이 코드는 0, 1, 2가 3, 4, 5보다 정확히 2배 높은 확률(22.2% vs 11.1%)로 나타남을 보여줍니다.

### 예제 2: 올바른 확률 구현 (편향 없음)

```python
import random

def drop_item_correct(drop_rate_percent):
    """
    부동소수점을 사용한 올바른 확률 구현
    편향이 발생하지 않음
    """
    # drop_rate_percent: 0.0 ~ 100.0
    return random.random() < (drop_rate_percent / 100.0)

def drop_item_large_range(drop_rate_percent):
    """
    충분히 큰 범위를 사용하는 구현
    부동소수점이 없을 때 사용 가능
    """
    # 0 ~ 999,999 범위로 변환 (충분히 큼)
    rand_val = random.randint(0, 999999)
    threshold = int(drop_rate_percent * 10000)  # 0.01% 단위
    return rand_val < threshold

# 검증
test_count = 100000
drop_count = sum(drop_item_correct(1.0) for _ in range(test_count))
actual_rate = (drop_count / test_count) * 100
print(f"1% 드롭률 테스트: {actual_rate:.2f}% (목표: 1.00%)")
```

### 예제 3: 모듈로 편향을 피하는 C 코드

```c
#include <stdlib.h>
#include <stdio.h>

// 방법 1: 편향 회피 함수 (재시도 로직)
int rand_unbiased(int max) {
    // RAND_MAX를 max로 나눈 나머지가 일어나는 범위를 피함
    int limit = RAND_MAX - (RAND_MAX % max);
    int value;
    
    do {
        value = rand();
    } while (value >= limit);  // 편향된 범위면 재시도
    
    return value % max;
}

// 방법 2: 큰 범위 차이 확보
int has_drop_safe(int drop_rate_out_of_billion) {
    // rand() % 1000000000의 편향을 피하기 위해
    // 더 큰 범위를 사용하거나 여러 번 호출
    long long combined = ((long long)rand() << 16) | rand();
    return combined % 1000000000 < drop_rate_out_of_billion;
}

// 테스트
int main() {
    int drop_count = 0;
    int total = 100000;
    int target = 10000000;  // 1% of 1000000000
    
    for (int i = 0; i < total; i++) {
        if (rand_unbiased(1000000000) < target) {
            drop_count++;
        }
    }
    
    printf("1%% 드롭률 검증: %.2f%%\n", (double)drop_count / total * 100);
    return 0;
}
```

## 함정·실수

### 함정 1: "통계적으로 보면 거의 같으니까 괜찮다"

모듈로 편향은 통계적 차이이기 때문에, 작은 샘플이나 짧은 시간에는 드러나지 않을 수 있습니다. 메이플스토리의 경우 수년간 운영하면서 누적된 데이터를 전수 조사해야 발견되었습니다.

**회피법**: 
- 게임 출시 전에 확률 시스템을 철저히 검증합니다
- 대규모 시뮬레이션(최소 백만 번 이상)으로 실제 분포를 확인합니다
- 게임 운영 중에도 실제 드롭율 데이터를 주기적으로 모니터링합니다

### 함정 2: "RAND_MAX가 크니까 편향은 무시해도 된다"

RAND_MAX(약 42억)를 작은 수(예: 100)로 나눌 때는 편향이 매우 작습니다. 하지만 나누는 수가 커질수록 편향이 의미 있는 수준이 됩니다.

**회피법**:
- 나누는 수가 RAND_MAX의 약 1% 이상이면 편향을 고려해야 합니다
- 실제로는 최신 난수 생성 함수를 사용하는 것이 안전합니다

### 함정 3: "편향이 작은 증가를 감지 못한다"

メイプル의 버프 버그처럼, 확률을 약간만 변경할 때 편향이 문제가 될 수 있습니다.

**회피법**:
- 확률 계산에 정수 비교 대신 부동소수점을 사용합니다
- 버그 보고와 모니터링을 통해 비정상적인 패턴을 감지합니다

### 함정 4: "내 코드에는 이런 편향이 없을 거야"

레거시 코드나 서드파티 라이브러리에서 모듈로 편향이 숨어있을 수 있습니다.

**회피법**:
- 코드 리뷰 때 난수 생성 부분을 특별히 점검합니다
- 정기적으로 확률 분포를 검증합니다

## 베스트 프랙티스

### 1. 최신 난수 생성 함수 사용 (최우선)

현대의 프로그래밍 언어들은 모두 고품질 난수 생성 함수를 제공합니다. 이들은 모듈로 편향 문제를 이미 해결했습니다.

**Python:**
```python
import secrets
import random

# 보안 난수 (권장)
value = secrets.randbelow(100)  # 0~99 균등분포

# 일반 난수 (간편함)
value = random.randint(0, 99)  # 0~99 균등분포

# 확률 구현 (가장 간단)
if random.random() < 0.01:  # 1% 확률
    drop_item()
```

**JavaScript:**
```javascript
// 균등분포 난수
const value = Math.floor(Math.random() * 100);  // 0~99

// 1% 확률
if (Math.random() < 0.01) {
    dropItem();
}
```

**Java:**
```java
// ThreadLocalRandom 사용 (효율적)
int value = ThreadLocalRandom.current().nextInt(0, 100);  // 0~99

// 또는 Random 클래스
Random random = new Random();
int value = random.nextInt(100);  // 0~99
```

**C++:**
```cpp
#include <random>

std::mt19937 gen(std::random_device{}());
std::uniform_int_distribution<> dis(0, 99);
int value = dis(gen);  // 0~99 균등분포
```

### 2. 부동소수점으로 확률 표현

정수 비교 대신 0.0~1.0 범위의 부동소수점으로 확률을 표현하면 모듈로 편향을 완전히 피할 수 있습니다.

```python
# 나쁜 예
if rand() % 1000 < 50:  # 5% (편향 가능성)
    drop_item()

# 좋은 예
if random.random() < 0.05:  # 5% (편향 없음)
    drop_item()
```

**장점**:
- 직관적이고 읽기 쉬움
- 모듈로 편향 없음
- 확률을 쉽게 조정할 수 있음

### 3. 필요시 재시도 로직 구현

레거시 코드를 수정할 수 없다면, 편향된 범위를 감지하고 재시도하는 로직을 추가합니다.

```c
int get_random_unbiased(int max) {
    int limit = RAND_MAX - (RAND_MAX % max);
    int value;
    
    do {
        value = rand();
    } while (value >= limit);  // 편향 범위는 버림
    
    return value % max;  // 이제 균등분포
}
```

**원리**: 편향이 발생하는 범위(RAND_MAX % max 이상)의 값들을 버리고 재시도하여, 결과적으로 완벽한 균등분포를 만듭니다.

### 4. 충분히 큰 범위 확보

나누는 수가 RAND_MAX의 0.1% 미만이면 편향이 무시할 수 있는 수준이 됩니다.

```c
// RAND_MAX ≈ 42억
// 안전한 사용: 42억의 0.1% = 4,200만 이상 범위

// 좋은 예: 100으로 나눔 (RAND_MAX의 0.000002%)
int dice = rand() % 6;  // 편향 무시할 수 있음

// 나쁜 예: 10억으로 나눔 (RAND_MAX의 23%)
int large = rand() % 1000000000;  // 편향 심각
```

### 5. 테스트와 검증

확률 시스템은 반드시 통계적으로 검증해야 합니다.

```python
def verify_drop_rate(drop_function, expected_rate, trials=100000):
    """
    실제 드롭 확률이 기대값과 일치하는지 검증
    """
    drops = sum(drop_function() for _ in range(trials))
    actual_rate = drops / trials
    error = abs(actual_rate - expected_rate)
    
    # 기대값 ± 5% 범위 내인지 확인
    is_valid = error < (expected_rate * 0.05)
    
    print(f"기대: {expected_rate*100:.2f}%, 실제: {actual_rate*100:.2f}%, "
          f"오차: {error*100:.2f}% {'✓' if is_valid else '✗'}")
    
    return is_valid

# 사용 예
verify_drop_rate(lambda: random.random() < 0.01, 0.01)
```

## 참고

- **원본 영상**: 코딩애플 유튜브 채널, "드디어 밝혀진 메이플 확률문제의 원인" (길이 약 6분)
- **배경 음악**: Maple Leaf Rag - E's Jammy Jams
- **관련 개념**: 
  - 난수 생성(Random Number Generation, RNG)
  - 확률 분포(Probability Distribution)
  - 균등 분포(Uniform Distribution)
  - 모듈로 연산(Modulo Operation)

- **모던 난수 생성 대안**:
  - **C**: `<random>` 헤더 (C++11+), Mersenne Twister
  - **C (POSIX)**: `arc4random()` (OpenBSD, macOS, BSD)
  - **Python**: `random` 모듈, `secrets` 모듈 (Python 3.6+)
  - **Java**: `java.util.Random`, `ThreadLocalRandom`
  - **JavaScript**: `Math.random()`, `crypto.getRandomValues()`

- **추가 학습**:
  - 메이플스토리 공식 버그 리포트 (네이버 공식 카페 등)
  - 난수 생성 알고리즘: Linear Congruential Generator, Mersenne Twister
  - 통계적 검증: Chi-squared test, Kolmogorov-Smirnov test
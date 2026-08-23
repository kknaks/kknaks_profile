---
created: '2026-05-29'
date: '2026-05-29'
day: Day 25
difficulty: medium
id: A-025
source:
  curated_in:
  - neetcode150
  number: 739
  platform: leetcode
  slug: daily-temperatures
  url: https://leetcode.com/problems/daily-temperatures/
status: draft
tags:
- array
- stack
- monotonic-stack
title:
  en: Daily Temperatures
  ko: 일일 기온
today: false
type: algorithm
updated: '2026-05-29'
visible: true
---

# 일일 기온

## Data

```yaml
problem:
  title:
    ko: 일일 기온
    en: Daily Temperatures
  statement:
    ko: 정수 배열 temperatures가 주어지며, 각 요소는 매일의 기온입니다. i번째 날 이후로 더 따뜻한 기온을 얻을 때까지 기다려야 하는 날의 개수를 answer[i]에 넣은 배열 answer를 반환합니다. 그러한 날이 없으면 answer[i]는 0으로 유지합니다.
    en: Given an array of integers temperatures represents the daily temperatures, return an array answer such that answer[i] is the number of days you have to wait after the ith day to get a warmer temperature. If there is no future day for which this is possible, keep answer[i] == 0 instead.
  constraints:
  - 1 ≤ temperatures.length ≤ 10^5
  - 30 ≤ temperatures[i] ≤ 100
  io:
  - input: '[73,74,75,71,69,72,76,73]'
    output: '[1,1,4,2,1,1,0,0]'
  - input: '[30,40,50,60]'
    output: '[1,1,1,0]'
  - input: '[30,60,90]'
    output: '[1,1,0]'
clarifying:
  items:
  - q:
      ko: 다음 날의 기온이 현재 기온과 같으면 '더 따뜻한' 것으로 간주할까요?
      en: If the next day's temperature equals the current day's, is that considered 'warmer'?
    type: good
    why:
      ko: 아니요. '더 따뜻한'은 엄격히 크다는 의미입니다 (=이 아닌 >).
      en: No. 'Warmer' means strictly greater than (>, not >=).
  - q:
      ko: 더 따뜻한 날이 없으면 answer[i]에 무엇을 넣나요?
      en: If no warmer day exists, what should answer[i] contain?
    type: good
    why:
      ko: 0으로 유지합니다. 이는 초기값이며 조건을 만족합니다.
      en: Keep it as 0, which is the default initialization value.
  - q:
      ko: answer[i]에는 따뜻한 기온의 값을 넣나요, 아니면 대기 일수를 넣나요?
      en: Does answer[i] contain the warmer temperature's value or the number of days to wait?
    type: good
    why:
      ko: 대기 일수입니다. 인덱스의 차이이지, 기온 값이 아닙니다.
      en: The number of days to wait (the difference between indices), not the temperature value itself.
  - q:
      ko: 모든 기온이 결국 더 따뜻한 날을 만날 것으로 보장할 수 있나요?
      en: Can we assume every day is guaranteed to eventually have a warmer day?
    type: distractor
    why:
      ko: 아니요. 마지막 날이나 일부 날들은 더 따뜻한 미래 날이 없을 수 있습니다.
      en: No. Days like the last one, or any day without a future warmer temperature, will remain 0.
  - q:
      ko: 왼쪽에서 오른쪽으로 반드시 처리해야 하나요?
      en: Must we process temperatures strictly left-to-right?
    type: distractor
    why:
      ko: 오른쪽에서 왼쪽으로도 가능하지만, 제공된 해법은 왼쪽에서 오른쪽입니다.
      en: Right-to-left is also possible, but left-to-right with a monotonic stack is the standard efficient approach.
  - q:
      ko: 매 날마다 모든 미래 날들을 확인하는 단순 탐색으로 충분할까요?
      en: Is a naive scan checking all future days for each day sufficient?
    type: good
    why:
      ko: 맞지만 비효율적입니다 (O(n²)). 스택으로 O(n)을 달성할 수 있습니다.
      en: It's correct but inefficient (O(n²)). A stack-based approach achieves O(n).
  - q:
      ko: 같은 기온 값이 여러 번 나타날 수 있나요?
      en: Can the same temperature value appear multiple times in the array?
    type: good
    why:
      ko: 네. 문제는 중복을 제한하지 않으며, 각 날의 첫 번째 더 따뜻한 날을 여전히 추적합니다.
      en: Yes. Duplicates are allowed, and we still track each day's first warmer day correctly.
approach:
  items:
  - name:
      ko: 단조 감소 스택
      en: Monotonic Decreasing Stack
    complexity: O(n) time / O(n) space
    type: good
    why:
      ko: 스택에 감소하는 순서로 온도를 유지합니다. 현재 온도가 스택 상단보다 높을 때 답을 계산합니다. 각 요소는 정확히 한 번 추가/제거되므로 O(n)입니다.
      en: Maintain temperatures in decreasing order in a stack. When current temperature exceeds the stack top, we immediately calculate the answer. Each element is pushed and popped exactly once, yielding O(n) total.
  - name:
      ko: 단순 탐색 (완전 탐색)
      en: Brute Force
    complexity: O(n²) time / O(1) space
    type: distractor
    why:
      ko: 각 날마다 모든 미래 날들을 스캔하여 첫 번째 따뜻한 날을 찾습니다. 정확하지만 큰 입력에서 매우 느립니다.
      en: For each day, scan all future days to find the first warmer temperature. Correct but inefficient for large inputs.
  - name:
      ko: 미리계산된 최댓값 (비효율적)
      en: Precomputed Suffix Maximums
    complexity: O(n²) time / O(n) space
    type: distractor
    why:
      ko: 각 위치 이후의 최댓값을 미리 계산할 수 있지만, 첫 번째 더 따뜻한 날을 찾기 위해 여전히 스캔이 필요하므로 개선이 없습니다.
      en: While we could precompute suffix maximums, we still need to scan for the first warmer day, so this doesn't reduce complexity.
  - name:
      ko: 우에서 좌로 역순 처리
      en: Right-to-Left Monotonic Stack
    complexity: O(n) time / O(n) space
    type: good
    why:
      ko: 오른쪽에서 왼쪽으로 순회하면서 더 따뜻한 날들을 추적합니다. 같은 O(n) 효율이지만 때로 더 직관적일 수 있습니다.
      en: Process right-to-left, maintaining warmer days as we go backward. Same O(n) efficiency with a potentially more intuitive flow.
logic:
  format: slot
  slots:
  - label:
      ko: 결과 배열 초기화
      en: Initialize Result Array
    indent: 0
    options:
    - code: res = [0] * len(temperatures)
      type: good
      why:
        ko: 모든 요소를 0으로 초기화합니다. 더 따뜻한 날이 없으면 0으로 유지됩니다.
        en: Pre-allocate result array with all zeros. Days with no warmer future remain 0.
    - code: res = []
      type: distractor
      why:
        ko: 동작하지 않습니다. res[stackInd]에 접근할 때 인덱스 에러가 발생합니다.
        en: Fails when accessing res[stackInd]; index out of bounds without pre-allocation.
    - code: res = [-1] * len(temperatures)
      type: distractor
      why:
        ko: 잘못된 기본값입니다. 0은 '더 따뜻한 날이 없음'을 의미하며, -1은 이를 표현하지 못합니다.
        en: Wrong default; 0 means 'no warmer day found', not -1.
  - label:
      ko: 스택 초기화
      en: Initialize Stack
    indent: 0
    options:
    - code: 'stack = []  # pair: [temp, index]'
      type: good
      why:
        ko: 빈 스택을 생성합니다. 스택은 (온도, 인덱스) 쌍을 저장하여 처리되지 않은 날들을 추적합니다.
        en: Create empty stack to store (temperature, index) pairs for unresolved days.
    - code: stack = None
      type: distractor
      why:
        ko: stack.pop()과 stack.append()를 호출할 수 없습니다.
        en: Cannot call .pop() and .append() on None; will crash immediately.
    - code: stack = {}
      type: distractor
      why:
        ko: 딕셔너리는 LIFO 순서를 보장하지 않으므로 스택 의미론이 손실됩니다.
        en: Dictionary doesn't provide LIFO stack semantics; order is unreliable.
  - label:
      ko: 주 반복문
      en: Main Loop
    indent: 0
    options:
    - code: 'for i, t in enumerate(temperatures):'
      type: good
      why:
        ko: enumerate로 인덱스와 온도를 동시에 얻습니다. 인덱스는 대기 일수를 계산하는 데 필수입니다.
        en: Enumerate gives both index and temperature. Index is essential to calculate days waited.
    - code: 'for t in temperatures:'
      type: distractor
      why:
        ko: 인덱스를 잃어버립니다. i - stackInd를 계산할 수 없습니다.
        en: Loses index information; cannot compute i - stackInd.
    - code: 'for i in range(len(temperatures)-1, -1, -1):'
      type: distractor
      why:
        ko: 우에서 좌로 순회합니다. 제공된 해법은 좌에서 우 순회를 기대합니다.
        en: Right-to-left iteration; the given solution expects left-to-right processing.
  - label:
      ko: 팝 조건
      en: Pop Condition
    indent: 1
    options:
    - code: 'while stack and t > stack[-1][0]:'
      type: good
      why:
        ko: 현재 온도가 스택 상단보다 높으면, 스택 상단의 날에 대한 답을 찾은 것입니다. 스택이 비어있지 않은지 확인하고, 엄격한 부등호(>)를 사용합니다.
        en: When current temperature exceeds stack top, we found the answer for that day. Check stack non-empty and use strict > for 'warmer'.
    - code: 'while t > stack[-1][0]:'
      type: distractor
      why:
        ko: 스택 안전 검사가 없습니다. 스택이 비어있으면 스택 언더플로우 에러가 발생합니다.
        en: Missing 'stack and' check; will crash on empty stack.
    - code: 'while stack and t >= stack[-1][0]:'
      type: distractor
      why:
        ko: '''>='' 연산자는 같은 온도를 팝합니다. ''더 따뜻한''은 엄격히 크다는 의미이므로 잘못됩니다.'
        en: '''>='' would pop equal temperatures; we need strictly warmer (>), not equal.'
  - label:
      ko: 스택에서 꺼내기
      en: Pop from Stack
    indent: 2
    options:
    - code: stackT, stackInd = stack.pop()
      type: good
      why:
        ko: 스택에서 (온도, 인덱스) 쌍을 꺼내고 풀어쓥니다. 두 값을 모두 필요로 합니다.
        en: Pop the (temperature, index) pair and unpack both values. We need both for the calculation.
    - code: stackInd, stackT = stack.pop()
      type: distractor
      why:
        ko: 언팩 순서가 잘못되었습니다. 온도와 인덱스가 뒤바뀝니다.
        en: Wrong unpacking order; temperature and index are swapped.
    - code: stackT = stack.pop()[0]
      type: distractor
      why:
        ko: 온도만 추출하고 인덱스를 잃습니다. res[stackInd] = i - stackInd에서 인덱스가 필요합니다.
        en: Extracts only temperature; loses index which is essential for res[stackInd] = i - stackInd.
  - label:
      ko: 답 기록
      en: Record Answer
    indent: 2
    options:
    - code: res[stackInd] = i - stackInd
      type: good
      why:
        ko: 꺼낸 인덱스의 결과에 대기 일수를 저장합니다. 차이는 i (현재 인덱스) - stackInd (꺼낸 인덱스)입니다.
        en: Store wait days in res at the popped index. The difference i - stackInd is the number of days to wait.
    - code: res[i] = i - stackInd
      type: distractor
      why:
        ko: 잘못된 위치입니다. res[i]가 아니라 res[stackInd]에 저장해야 합니다.
        en: Wrong index; should update res[stackInd], not res[i].
    - code: res[stackInd] = i
      type: distractor
      why:
        ko: 차이를 계산해야 합니다. i는 현재 인덱스이며, 대기 일수는 i - stackInd입니다.
        en: Should be the difference i - stackInd, not just i directly.
  - label:
      ko: 스택에 추가
      en: Append to Stack
    indent: 1
    options:
    - code: stack.append((t, i))
      type: good
      why:
        ko: 현재 (온도, 인덱스) 쌍을 스택에 추가합니다. 미래 더 높은 온도와 비교하기 위한 후보가 됩니다.
        en: Add current (temperature, index) pair to stack as a candidate for future comparisons. Maintain decreasing order for efficiency.
    - code: stack.append(t)
      type: distractor
      why:
        ko: 인덱스를 잃습니다. 나중에 res[stackInd] = i - stackInd를 계산할 수 없습니다.
        en: Loses index information; cannot compute i - stackInd when popping.
    - code: stack.insert(0, (t, i))
      type: distractor
      why:
        ko: 앞에 삽입하면 큐 동작이 됩니다. 스택의 LIFO 의미론이 손상되고 O(n)이 됩니다.
        en: Insert at front creates queue behavior; breaks LIFO semantics and makes operations O(n).
trace:
  code:
  - 'class Solution:'
  - '    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:'
  - '        res = [0] * len(temperatures)'
  - '        stack = []  # pair: [temp, index]'
  - ''
  - '        for i, t in enumerate(temperatures):'
  - '            while stack and t > stack[-1][0]:'
  - '                stackT, stackInd = stack.pop()'
  - '                res[stackInd] = i - stackInd'
  - '            stack.append((t, i))'
  - '        return res'
  cases:
  - input: '[73,74,75,71,69,72,76,73]'
    expected: '[1,1,4,2,1,1,0,0]'
  - input: '[30,40,50,60]'
    expected: '[1,1,1,0]'
  - input: '[30,60,90]'
    expected: '[1,1,0]'
  worked_example:
    input: '[73,74,75,71,69,72,76,73]'
    steps:
    - ko: '처음 두 온도 73→74: 74는 73보다 따뜻하므로 스택에서 73을 팝하고 res[0]=1-0=1을 기록합니다.'
      en: 'First two temps 73→74: 74 is warmer, so pop 73 from stack and record res[0]=1.'
    - ko: '감소하는 온도 75→71→69: 이들은 스택에 추가되어 대기합니다. 스택은 [(75,2), (71,3), (69,4)]가 됩니다.'
      en: 'Decreasing temps 75→71→69: Added to stack. Stack becomes [(75,2), (71,3), (69,4)].'
    - ko: '온도 72: 69와 71을 팝하고 res[4]=1, res[3]=2를 기록합니다. 75보다는 낮으므로 스택에 남습니다.'
      en: 'Temp 72: Pops 69 and 71 (res[4]=1, res[3]=2). Still lower than 75, so appended.'
    - ko: '온도 76: 75를 팝하고 res[2]=6-2=4를 기록합니다. 최종 배열은 [1,1,4,2,1,1,0,0]입니다.'
      en: 'Temp 76: Pops 75 (res[2]=4). Unresolved elements at end (73,76) default to 0. Final: [1,1,4,2,1,1,0,0].'
    answer: '[1,1,4,2,1,1,0,0]'
solution:
  code: "class Solution:\n    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:\n        res = [0] * len(temperatures)\n        stack = []  # pair: [temp, index]\n\n        for i, t in enumerate(temperatures):\n            while stack and t > stack[-1][0]:\n                stackT, stackInd = stack.pop()\n                res[stackInd] = i - stackInd\n            stack.append((t, i))\n        return res\n"
  complexity:
    time: O(n)
    space: O(n)
  followup:
  - ko: 배열이 순환적이라면 (마지막 뒤에 처음이 오는), 어떻게 수정할까요?
    en: How would the solution change if the array was circular (end wraps to beginning)?
  - ko: 스택을 사용할 수 없다면, 다른 O(n) 해법이 있을까요?
    en: If you couldn't use a stack, is there another O(n) solution?
  - ko: 오른쪽에서 왼쪽으로 순회하는 방식으로는 어떻게 풀까요?
    en: How would you solve this by traversing from right to left instead?
```
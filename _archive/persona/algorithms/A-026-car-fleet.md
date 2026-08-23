---
created: '2026-05-30'
date: '2026-05-30'
day: Day 26
difficulty: medium
id: A-026
source:
  curated_in:
  - neetcode150
  number: 853
  platform: leetcode
  slug: car-fleet
  url: https://leetcode.com/problems/car-fleet/
status: draft
tags:
- array
- stack
- sorting
- monotonic-stack
title:
  en: Car Fleet
  ko: 자동차 떼
today: false
type: algorithm
updated: '2026-05-30'
visible: true
---

# 자동차 떼

## Data

```yaml
problem:
  title:
    ko: 자동차 떼
    en: Car Fleet
  statement:
    ko: 'n대의 자동차가 주어진 거리에서 시작하여 목표 거리에 도달하려고 합니다.


      두 개의 정수 배열 position과 speed가 주어집니다. 둘 다 길이가 n이며, position[i]는 i번째 자동차의 시작 거리, speed[i]는 i번째 자동차의 시간당 거리 속도입니다.


      자동차는 다른 자동차를 추월할 수 없지만, 따라잡은 후 더 느린 자동차의 속도로 나란히 이동할 수 있습니다.


      자동차 떼는 단일 자동차 또는 나란히 움직이는 자동차 그룹입니다. 자동차 떼의 속도는 그 안에 있는 모든 자동차 중 최소 속도입니다.


      자동차가 목표 거리에서 자동차 떼를 따라잡으면, 그 자동차도 자동차 떼의 일부로 간주됩니다.


      목표 지점에 도달하는 자동차 떼의 개수를 반환하세요.'
    en: 'There are n cars at given miles away from the starting mile 0, traveling to reach the mile target.


      You are given two integer arrays position and speed, both of length n, where position[i] is the starting mile of the ith car and speed[i] is the speed of the ith car in miles per hour.


      A car cannot pass another car, but it can catch up and then travel next to it at the speed of the slower car.


      A car fleet is a single car or a group of cars driving next to each other. The speed of the car fleet is the minimum speed of any car in the fleet.


      If a car catches up to a car fleet at the mile target, it will still be considered as part of the car fleet.


      Return the number of car fleets that will arrive at the destination.'
  constraints:
  - 1 ≤ n ≤ 10⁵
  - 0 < target ≤ 10⁶
  - 0 ≤ position[i] < target
  - All position values are unique
  - 0 < speed[i] ≤ 10⁶
  io:
  - input: '12

      [10,8,0,5,3]

      [2,4,1,1,3]'
    output: '3'
  - input: '10

      [3]

      [3]'
    output: '1'
  - input: '100

      [0,2,4]

      [4,2,1]'
    output: '1'
clarifying:
  items:
  - q:
      ko: 왜 자동차를 위치 순서로 내림차순 정렬해야 하나요?
      en: Why do we need to sort cars by position in descending order?
    type: good
    why:
      ko: 목표에 가장 가까운 자동차부터 처리해야 뒤의 자동차가 앞의 자동차를 따라잡을 수 있는지 판단할 수 있습니다. 내림차순 정렬은 이 순서를 보장합니다.
      en: We process from the car closest to target backward, allowing us to check if faster cars behind can catch up. Descending order ensures correct evaluation of catch-up potential.
  - q:
      ko: 자동차가 떼를 이루는지 판단하는 핵심 지표는 무엇인가요?
      en: What is the key metric to determine if a car joins a fleet?
    type: good
    why:
      ko: 도착 시간 (target - position) / speed를 비교합니다. 뒤의 자동차 도착 시간이 앞의 자동차보다 크면 따라잡지 못하므로 새로운 떼를 형성합니다.
      en: Arrival time (target - position) / speed. If a car's arrival time exceeds the car ahead, it cannot catch up and forms a new fleet.
  - q:
      ko: 스택에서 요소를 제거하는 조건은 무엇인가요?
      en: When do we remove an element from the stack?
    type: good
    why:
      ko: 현재 자동차의 도착 시간이 스택 맨 위의 도착 시간보다 작거나 같으면, 현재 자동차가 이전 자동차(또는 떼)를 따라잡았으므로 스택에서 제거합니다.
      en: When current arrival time ≤ top of stack, the current car catches the previous car/fleet, so we remove it since they merge into one fleet.
  - q:
      ko: 자동차들을 속도 순서로 정렬하면 어떻게 될까요?
      en: What if we sorted cars by speed instead of position?
    type: distractor
    why:
      ko: 위치 관계가 무시되어 어느 자동차가 어느 자동차를 따라잡을 수 있는지 판단할 수 없습니다. 속도만으로는 공간적 순서를 알 수 없습니다.
      en: Position relationships are lost. Speed alone doesn't tell us which cars are ahead or behind, making catch-up logic impossible.
  - q:
      ko: 도착 시간이 정확히 같은 두 자동차는 반드시 같은 떼를 이루나요?
      en: Do two cars with the exact same arrival time always form the same fleet?
    type: good
    why:
      ko: 예. 도착 시간이 같으면 한 자동차가 다른 자동차를 정확히 따라잡은 것이므로 같은 떼를 이룹니다. 조건 stack[-1] <= stack[-2]에서 등호가 필요한 이유입니다.
      en: Yes. Equal arrival times mean one catches the other exactly, merging them. This is why the condition uses ≤, not just <.
  - q:
      ko: 처음 자동차부터 처리하면 어떻게 될까요?
      en: What happens if we process cars from position 0 forward instead of backward?
    type: distractor
    why:
      ko: 가장 뒤의 자동차부터 처리하게 되어, 그 자동차가 앞의 자동차를 따라잡을 수 있는지 판단하기 전에 앞의 자동차들의 떼를 확정하게 됩니다. 알고리즘이 정확하게 작동하지 않습니다.
      en: We'd process from the rear forward, deciding fleet membership before knowing all the cars that might catch up. Logic breaks.
approach:
  items:
  - name:
      ko: 정렬 + 단조 스택 (Monotonic Stack)
      en: Sort by position + Monotonic stack
    complexity: O(n log n) time / O(n) space
    type: good
    why:
      ko: 위치 내림차순으로 정렬한 후 도착 시간을 스택에 추가하면서, 뒤의 자동차가 앞의 자동차를 따라잡을 때마다 스택 맨 위를 제거합니다. 각 자동차는 최대 한 번 추가되고 제거되므로 효율적입니다.
      en: Sort descending, then track arrival times. When a car catches up, remove the previous fleet from stack. Each car is pushed/popped at most once, yielding O(n log n) overall.
  - name:
      ko: 시뮬레이션 (Simulation)
      en: Time-based simulation
    complexity: O(n × T) where T is max arrival time / O(n) space
    type: distractor
    why:
      ko: 시간을 단위별로 진행하면서 각 자동차의 위치를 추적할 수 있지만, 시간복잡도가 매우 높고 부동소수점 계산의 정밀성 문제가 있습니다.
      en: Simulate minute-by-minute, tracking positions. With targets up to 10⁶, this is prohibitively slow and suffers floating-point precision issues.
  - name:
      ko: 완전 탐색 (Brute Force)
      en: Brute force O(n²) check
    complexity: O(n²) time / O(n) space
    type: distractor
    why:
      ko: 각 자동차에 대해 모든 뒤의 자동차와 비교하여 따라잡을 수 있는지 확인할 수 있지만, n이 10⁵에 가까우면 시간 제한을 초과합니다.
      en: For each car, check all cars behind it. Correct logic but O(n²) is too slow for n up to 10⁵.
  - name:
      ko: 도착 시간 배열 + 역순 순회
      en: Arrival time array with backward iteration
    complexity: O(n log n) time / O(n) space
    type: good
    why:
      ko: 정렬 후 도착 시간 배열을 만들고 역순으로 순회하면서, 시간이 증가하는 지점들을 새로운 떼로 세어줍니다. 스택과 동일한 아이디어지만 배열 기반입니다.
      en: After sorting, build arrival time array and iterate backward, counting points where time increases. Equivalent to monotonic stack but using explicit iteration.
logic:
  format: slot
  slots:
  - label:
      ko: 위치와 속도 쌍 생성
      en: Create (position, speed) pairs
    indent: 0
    options:
    - code: pair = [(p, s) for p, s in zip(position, speed)]
      type: good
      why:
        ko: position[i]와 speed[i]를 함께 묶어서 이후 정렬 시에도 두 값이 연결되도록 유지합니다.
        en: Pairs position and speed together so they remain associated during sorting.
    - code: pair = list(zip(position, speed))
      type: distractor
      why:
        ko: 기술적으로는 동일하지만, 명시적으로 리스트로 변환하는 것이 더 명확합니다. (작은 차이)
        en: Functionally equivalent but less idiomatic than list comprehension.
    - code: pair = [(s, p) for p, s in zip(position, speed)]
      type: distractor
      why:
        ko: (speed, position) 순서로 쌍을 만들면, 다음 줄의 정렬에서 속도를 기준으로 정렬되어 잘못된 결과입니다.
        en: Swapped order causes sort to use speed as the primary key instead of position, breaking the algorithm.
  - label:
      ko: 위치 내림차순으로 정렬
      en: Sort pairs by position (descending)
    indent: 0
    options:
    - code: pair.sort(reverse=True)
      type: good
      why:
        ko: 목표에 가장 가까운 자동차부터 처리해야, 뒤의 자동차들이 앞의 자동차를 따라잡을 수 있는지 올바르게 판단할 수 있습니다.
        en: We process from target backward. This order ensures we correctly determine catch-up relationships.
    - code: pair.sort()
      type: distractor
      why:
        ko: 기본 오름차순 정렬은 거리가 먼 자동차부터 처리하게 되어, 뒤의 자동차가 앞의 자동차를 따라잡을 수 있는지 판단할 수 없습니다.
        en: Ascending order processes from rear, making catch-up logic impossible.
    - code: 'pair.sort(key=lambda x: x[1], reverse=True)'
      type: distractor
      why:
        ko: 속도 기준(x[1])으로 정렬하면 위치 관계가 무시되어 알고리즘이 작동하지 않습니다.
        en: Sorting by speed ignores position relationships, completely breaking the algorithm.
  - label:
      ko: 스택 초기화
      en: Initialize stack
    indent: 0
    options:
    - code: stack = []
      type: good
      why:
        ko: 도착 시간을 저장할 스택을 준비합니다. 스택의 각 요소는 독립적인 떼의 도착 시간을 나타냅니다.
        en: Initialize empty stack to track arrival times. Each element represents one fleet head.
    - code: stack = 0
      type: distractor
      why:
        ko: 정수는 여러 도착 시간을 저장할 수 없으므로 append, pop 같은 연산이 작동하지 않습니다.
        en: Integer cannot store multiple values or support push/pop operations.
    - code: stack = set()
      type: distractor
      why:
        ko: 집합은 순서를 보장하지 않으며, 같은 도착 시간을 가진 여러 떼를 구분할 수 없습니다.
        en: Set has no order and doesn't support the pop semantic we need.
  - label:
      ko: 도착 시간 계산 및 스택에 추가
      en: Calculate arrival time and push to stack
    indent: 1
    options:
    - code: stack.append((target - p) / s)
      type: good
      why:
        ko: 현재 자동차의 도착 시간 (target - position) / speed를 계산하여 스택에 추가합니다. 이 값이 이전 자동차를 따라잡을 수 있는지 판단하는 기준이 됩니다.
        en: Arrival time = distance to target / speed. Push to stack to compare with previous car's arrival time.
    - code: stack.append(target / s)
      type: distractor
      why:
        ko: 분자에서 position을 빼지 않았으므로 도착 시간 계산이 완전히 잘못됩니다.
        en: Missing (target - position) in numerator; this calculates incorrect time values.
    - code: stack.append((target - p) * s)
      type: distractor
      why:
        ko: 곱셈을 사용하면 물리적으로 의미 없는 값이 나옵니다. 시간 = 거리 / 속도입니다.
        en: Multiplication is wrong; time = distance / speed, not distance × speed.
  - label:
      ko: 현재 자동차가 이전 떼에 합류하는지 확인
      en: Check if current car catches the previous fleet
    indent: 1
    options:
    - code: 'if len(stack) >= 2 and stack[-1] <= stack[-2]:'
      type: good
      why:
        ko: 현재 자동차의 도착 시간이 스택 맨 위(이전 자동차/떼)의 도착 시간보다 작거나 같으면, 현재 자동차가 따라잡은 것이므로 다음 줄에서 스택을 제거합니다.
        en: If current arrival time ≤ previous, the current car catches the previous fleet, so it doesn't remain independent.
    - code: 'if len(stack) >= 2 and stack[-1] > stack[-2]:'
      type: distractor
      why:
        ko: 비교 부호를 반대로 사용하면, 따라잡지 못한 경우에 pop하게 되어 완전히 반대의 동작을 합니다.
        en: 'Flipped comparison: removes fleet when car doesn''t catch up, opposite of intended behavior.'
    - code: 'if stack[-1] <= stack[-2]:'
      type: distractor
      why:
        ko: len(stack) >= 2 체크가 없으므로, 스택에 요소가 1개 이하일 때 IndexError가 발생합니다.
        en: Missing length check causes IndexError when stack has fewer than 2 elements.
  - label:
      ko: 따라잡힌 떼 제거
      en: Remove the caught fleet
    indent: 2
    options:
    - code: stack.pop()
      type: good
      why:
        ko: 현재 자동차가 이전 자동차/떼를 따라잡았으므로, 이전 자동차는 더 이상 독립적인 떼가 아닙니다. 스택에서 제거합니다.
        en: The previous fleet is caught, so it's no longer independent. Remove it from the count.
    - code: 'stack.pop()

        stack.append((target - p) / s)'
      type: distractor
      why:
        ko: 현재 자동차의 도착 시간은 이미 line [4]에서 스택에 추가되었으므로, pop한 후 다시 append하면 중복입니다.
        en: 'Redundant: we already added the current arrival time at line [4].'
    - code: stack.clear()
      type: distractor
      why:
        ko: 전체 스택을 초기화하면 모든 이전 떼 정보가 사라져 최종 답이 완전히 잘못됩니다.
        en: Clearing the entire stack loses all fleet information, producing wrong answer.
  - label:
      ko: 떼의 개수 반환
      en: Return the number of fleets
    indent: 0
    options:
    - code: return len(stack)
      type: good
      why:
        ko: 스택에 남은 요소의 개수가 바로 최종적으로 목표에 도달하는 떼의 개수입니다. 스택의 각 요소는 독립적으로 도착하는 한 개의 떼를 나타냅니다.
        en: Each element in the final stack represents one independent fleet. Stack size = answer.
    - code: return len(pair)
      type: distractor
      why:
        ko: 정렬된 자동차 쌍의 개수(= n)를 반환합니다. 이는 떼의 개수가 아닙니다.
        en: Returns total number of cars, not fleets. These are different.
    - code: return stack[-1] if stack else 0
      type: distractor
      why:
        ko: 스택의 마지막 요소(도착 시간 값)를 반환합니다. 이는 떼의 개수가 아니라 수치일 뿐입니다.
        en: Returns the last arrival time value, not the count of fleets.
trace:
  code:
  - 'class Solution:'
  - '    def carFleet(self, target: int, position: List[int], speed: List[int]) -> int:'
  - '        pair = [(p, s) for p, s in zip(position, speed)]'
  - '        pair.sort(reverse=True)'
  - '        stack = []'
  - '        for p, s in pair:  # Reverse Sorted Order'
  - '            stack.append((target - p) / s)'
  - '            if len(stack) >= 2 and stack[-1] <= stack[-2]:'
  - '                stack.pop()'
  - '        return len(stack)'
  cases:
  - input: '12

      [10,8,0,5,3]

      [2,4,1,1,3]'
    expected: '3'
  - input: '10

      [3]

      [3]'
    expected: '1'
  - input: '100

      [0,2,4]

      [4,2,1]'
    expected: '1'
  worked_example:
    input: '12

      [10,8,0,5,3]

      [2,4,1,1,3]'
    steps:
    - ko: '입력: target=12, position=[10,8,0,5,3], speed=[2,4,1,1,3]'
      en: 'Input: target=12, position=[10,8,0,5,3], speed=[2,4,1,1,3]'
    - ko: '쌍 생성: [(10,2), (8,4), (0,1), (5,1), (3,3)] → 내림차순 정렬: [(10,2), (8,4), (5,1), (3,3), (0,1)]'
      en: 'Create pairs and sort descending: [(10,2), (8,4), (5,1), (3,3), (0,1)]'
    - ko: '(10,2): 도착=1.0, stack=[1.0] | (8,4): 도착=1.0≤1.0, pop, stack=[1.0] | (5,1): 도착=7.0>1.0, stack=[1.0,7.0] | (3,3): 도착=3.0≤7.0, pop, stack=[1.0,7.0] | (0,1): 도착=12.0>7.0, stack=[1.0,7.0,12.0]'
      en: 'Process each: (10,2)→1.0, stack=[1.0] | (8,4)→1.0≤1.0 pop, stack=[1.0] | (5,1)→7.0, stack=[1.0,7.0] | (3,3)→3.0≤7.0 pop, stack=[1.0,7.0] | (0,1)→12.0, stack=[1.0,7.0,12.0]'
    - ko: '최종: 스택 크기 = 3'
      en: 'Final: stack size = 3'
    answer: '3'
solution:
  code: "class Solution:\n    def carFleet(self, target: int, position: List[int], speed: List[int]) -> int:\n        pair = [(p, s) for p, s in zip(position, speed)]\n        pair.sort(reverse=True)\n        stack = []\n        for p, s in pair:  # Reverse Sorted Order\n            stack.append((target - p) / s)\n            if len(stack) >= 2 and stack[-1] <= stack[-2]:\n                stack.pop()\n        return len(stack)\n"
  complexity:
    time: O(n log n)
    space: O(n)
  followup:
  - ko: 각 떼가 목표에 도착하는 시간(도착 시간)을 알려면 어떻게 수정할까요?
    en: How would you modify this to return the arrival times of each fleet?
  - ko: 만약 배열이 이미 정렬되어 있다면 알고리즘의 시간복잡도는 어떻게 될까요?
    en: If the input position array was already sorted, what would the time complexity be?
  - ko: '자동차가 도중에 멈춰야 할 지점(예: 주유소)이 있다면 알고리즘에 어떤 변화가 필요할까요?'
    en: How would the algorithm change if cars had mandatory stops at certain waypoints?
```
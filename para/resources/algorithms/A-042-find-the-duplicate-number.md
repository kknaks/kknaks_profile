---
created: '2026-06-17'
date: '2026-06-17'
day: Day 42
difficulty: medium
id: A-042
source:
  curated_in:
  - neetcode150
  number: 287
  platform: leetcode
  slug: find-the-duplicate-number
  url: https://leetcode.com/problems/find-the-duplicate-number/
tags:
- array
- two-pointers
- binary-search
- bit-manipulation
title:
  en: Find the Duplicate Number
  ko: 중복된 숫자 찾기
today: false
type: algorithm
updated: '2026-06-17'
visible: true
---

# 중복된 숫자 찾기

## Data

```yaml
problem:
  title:
    ko: 중복된 숫자 찾기
    en: Find the Duplicate Number
  statement:
    ko: 'n + 1개의 정수를 포함하는 정수 배열 nums가 주어지며, 각 정수는 [1, n] 범위 내에 있습니다.


      nums에는 정확히 하나의 중복된 숫자가 있습니다. 이 중복된 숫자를 반환해야 합니다.


      배열 nums를 수정하지 않고 O(1) 상수 추가 공간만을 사용하여 문제를 풀어야 합니다.'
    en: 'Given an array of integers nums containing n + 1 integers where each integer is in the range [1, n] inclusive.


      There is only one repeated number in nums. Return this repeated number.


      You must solve the problem without modifying the array nums and using only constant extra space.'
  constraints:
  - 1 ≤ n ≤ 10^5
  - nums.length == n + 1
  - 1 ≤ nums[i] ≤ n
  - Precisely one integer appears two or more times
  io:
  - input: '[1,3,4,2,2]'
    output: '2'
  - input: '[3,1,3,4,2]'
    output: '3'
  - input: '[3,3,3,3,3]'
    output: '3'
clarifying:
  items:
  - q:
      ko: 중복된 숫자가 2번만 나타날까요, 아니면 더 많이 나타날 수 있을까요?
      en: Can the duplicate number appear more than twice, or only twice?
    type: good
    why:
      ko: 제약 조건에서 '정확히 하나의 정수가 두 번 이상 나타남'이라고 명시되어 있습니다. 중복 횟수에 제한이 없으므로 이를 이해하는 것이 중요합니다.
      en: The constraints state 'precisely one integer appears two or more times,' so the duplicate can appear any number of times ≥ 2. Understanding this clarifies the scope of possible inputs.
  - q:
      ko: 왜 배열을 수정하지 않아야 할까요?
      en: Why is it important not to modify the input array?
    type: good
    why:
      ko: 실제 인터뷰나 프로덕션 코드에서는 입력 데이터를 변경하면 다른 처리나 외부 호출자에게 부작용을 일으킬 수 있습니다. 이 제약은 안전하고 신뢰성 있는 코드 작성의 중요성을 강조합니다.
      en: In real-world scenarios, modifying input data can cause unexpected side effects for callers or other operations. This constraint enforces defensive coding practices.
  - q:
      ko: '''O(1) 추가 공간''은 무엇을 의미하나요?'
      en: What does 'constant extra space' mean in this context?
    type: good
    why:
      ko: '입력 배열 크기와 무관하게 고정된 개수의 변수(예: 몇 개의 포인터)만 사용한다는 뜻입니다. 해시 집합이나 다른 크기 조정 가능한 자료구조는 사용할 수 없습니다.'
      en: It means you can only use a fixed number of variables (like a few pointers) regardless of input size. Hash sets or dynamic data structures that scale with input are not allowed.
  - q:
      ko: 배열에 반드시 중복이 존재한다고 보장할 수 있나요?
      en: Is it guaranteed that at least one duplicate must exist?
    type: good
    why:
      ko: 네. 각 정수가 [1, n] 범위 내이고 배열 길이가 n + 1이므로, 비둘기집 원리(비둘기집 원리)에 의해 반드시 하나 이상의 중복이 존재합니다.
      en: Yes. Since the array has n + 1 elements and each is in [1, n], the pigeonhole principle guarantees at least one duplicate.
  - q:
      ko: 해시 집합을 사용하면 O(n) 시간에 풀 수 있나요?
      en: Can we solve this using a hash set in O(n) time?
    type: distractor
    why:
      ko: 해시 집합은 O(n) 공간을 요구하므로 'O(1) 추가 공간' 제약을 위반합니다. 이 문제에서는 O(1) 공간이어야 합니다.
      en: A hash set requires O(n) space, violating the constant space constraint. This problem specifically demands O(1) extra space.
  - q:
      ko: 배열을 정렬한 후 인접한 원소를 비교하면 안 될까요?
      en: Can we sort the array and check for adjacent duplicates?
    type: distractor
    why:
      ko: 정렬은 배열을 수정하므로 문제의 '배열을 수정하지 않는다' 제약을 위반합니다.
      en: Sorting modifies the input array, which violates the 'without modifying the array' constraint.
  - q:
      ko: 배열 인덱스를 연결 리스트 포인터처럼 생각할 수 있을까요?
      en: Can we treat array indices as pointers in a linked list?
    type: good
    why:
      ko: 네. 각 위치 i의 값 nums[i]를 '다음 위치'로 생각하면, 중복이 있으면 반드시 사이클이 생깁니다. Floyd 사이클 감지 알고리즘이 이를 이용합니다.
      en: Yes. If we treat nums[i] as a pointer to the next node, the presence of a duplicate creates a cycle. Floyd's cycle detection leverages this insight.
  - q:
      ko: 느린 포인터와 빠른 포인터가 만나는 지점이 정확히 중복이 위치한 인덱스일까요?
      en: Does the meeting point of slow and fast pointers directly give us the duplicate?
    type: distractor
    why:
      ko: 아니요. 첫 번째 만남의 장소는 사이클 내의 임의의 지점입니다. 두 번째 단계에서 한 포인터를 처음부터 시작하여 다시 만날 때의 위치가 사이클 진입점(즉, 중복)이 됩니다.
      en: No. The first meeting is at an arbitrary point in the cycle. We must reset one pointer to the start and move both at the same speed to find the cycle entrance (the duplicate).
approach:
  items:
  - name:
      ko: Floyd 사이클 감지 (거북이와 토끼)
      en: Floyd's Cycle Detection (Tortoise & Hare)
    complexity: O(n) time / O(1) space
    type: good
    why:
      ko: 배열을 연결 리스트로 해석하여 두 포인터로 사이클을 감지하고, 두 번째 단계에서 사이클 진입점을 찾습니다. 모든 제약을 만족하면서 최적 시간복잡도를 달성합니다.
      en: 'Treats the array as a linked list where duplicates create cycles. Two phases: (1) detect cycle with slow/fast pointers, (2) find cycle entrance with two same-speed pointers. Achieves optimal O(n) time with O(1) space.'
  - name:
      ko: 이진 탐색 (값 범위에서)
      en: Binary Search on Value Range
    complexity: O(n log n) time / O(1) space
    type: good
    why:
      ko: 값이 [1, n] 범위에 있으므로, 범위를 이진 탐색하고 각 중간값보다 작거나 같은 원소의 개수를 센다면 중복을 찾을 수 있습니다. 수정이나 추가 공간 없이 작동합니다.
      en: Since all values are in [1, n], we can binary search the range and count how many elements are ≤ mid. If count > mid, the duplicate is in the lower half. No modification or extra space needed.
  - name:
      ko: 해시 집합 (일반적인 접근)
      en: Hash Set
    complexity: O(n) time / O(n) space
    type: distractor
    why:
      ko: 각 숫자를 순회하며 해시 집합에 추가하고 이미 있으면 반환합니다. 시간복잡도는 최적이지만 O(n) 공간을 사용하므로 이 문제의 제약에 맞지 않습니다.
      en: 'Simple and intuitive: iterate through nums, add to set, return if already present. Optimal time but uses O(n) space, violating the constraint.'
  - name:
      ko: 음수 마킹 (배열 수정)
      en: Negation Marking
    complexity: O(n) time / O(1) space
    type: distractor
    why:
      ko: 각 숫자를 인덱스로 사용해 배열의 해당 위치를 음수로 표시합니다. 음수가 이미 있으면 그것이 중복입니다. O(1) 공간이지만 배열을 수정하므로 문제 요구사항을 위반합니다.
      en: Mark positions as negative to track visited indices. Efficient but modifies the input array, violating a key constraint.
  - name:
      ko: 정렬 + 두 포인터
      en: Sorting + Two Pointers
    complexity: O(n log n) time / O(1) space (excluding sort overhead)
    type: distractor
    why:
      ko: 배열을 정렬한 후 인접한 같은 값을 찾습니다. 효율적이지만 배열을 수정하므로 '배열을 수정하지 않음' 제약을 위반합니다.
      en: Sort the array and check for adjacent duplicates. Efficient but modifies the array, which violates the problem's no-modification constraint.
logic:
  format: slot
  slots:
  - label:
      ko: 두 포인터 초기화
      en: Initialize two pointers
    indent: 0
    options:
    - code: slow, fast = 0, 0
      type: good
      why:
        ko: slow와 fast 포인터를 모두 배열의 시작(인덱스 0)에 배치합니다. 배열의 값을 다음 인덱스로 해석하는 연결 리스트 모델에서 시작점이 됩니다.
        en: Both slow and fast pointers start at index 0, treating array values as pointers to the next position in a linked list structure.
    - code: slow, fast = 0, 1
      type: distractor
      why:
        ko: 다른 시작 위치는 포인터의 상대적 위치를 깨뜨려 알고리즘이 제대로 작동하지 않습니다.
        en: Different starting positions break the relative positioning needed for the algorithm to detect cycles correctly.
    - code: slow, fast = 1, 1
      type: distractor
      why:
        ko: 1부터 시작하면 인덱스 0(값 1)을 놓칩니다. 배열의 모든 원소는 [1, n]이므로 시작은 반드시 0이어야 합니다.
        en: Starting at 1 skips index 0. Since values are in [1, n], index 0 is always a valid starting point.
  - label:
      ko: '사이클 감지: 포인터 이동'
      en: 'Phase 1: Detect cycle with speed difference'
    indent: 1
    options:
    - code: fast = nums[nums[fast]]
      type: good
      why:
        ko: slow는 1칸씩(nums[slow]), fast는 2칸씩(nums[nums[fast]]) 이동합니다. 사이클이 있으면 빠른 포인터가 느린 포인터를 따라잡아 결국 만납니다.
        en: Slow advances by 1 step (nums[slow]), fast by 2 steps (nums[nums[fast]]). In a cycle, fast will eventually catch slow, proving a duplicate exists.
    - code: slow = nums[slow]; fast = nums[fast]
      type: distractor
      why:
        ko: 둘 다 같은 속도(1칸씩)로 이동하면 사이클을 감지하기는 하지만 매우 비효율적입니다. 2칸씩 이동하는 것이 필수적입니다.
        en: Both moving at the same speed is less efficient and may not guarantee meeting quickly. The speed difference is key to the algorithm.
    - code: slow = nums[slow]; fast = nums[nums[nums[fast]]]
      type: distractor
      why:
        ko: fast가 3칸씩 이동하면 만나는 지점의 수학적 관계가 깨져 알고리즘이 작동하지 않습니다.
        en: Moving fast 3 steps breaks the mathematical relationship needed to find the cycle entrance correctly.
  - label:
      ko: 사이클 감지 조건
      en: Check if cycle is detected
    indent: 2
    options:
    - code: 'if slow == fast:'
      type: good
      why:
        ko: slow와 fast가 같은 값에 도달하면 사이클 내에서 만난 것입니다. Floyd 알고리즘의 첫 번째 단계가 완료되어 제2단계로 진행할 수 있습니다.
        en: When slow == fast, they have met within the cycle, guaranteeing a duplicate exists. This completes phase 1 and allows us to find the entrance.
    - code: 'if slow < fast:'
      type: distractor
      why:
        ko: 크기 비교는 사이클 감지와 무관합니다. 포인터들의 값이 아니라 위치가 같은지를 확인해야 합니다.
        en: Size comparison doesn't detect cycles. We need equality check for positions, not less-than.
    - code: 'if slow != fast:'
      type: distractor
      why:
        ko: 조건을 반대로 하면 포인터가 만나기 전에 루프를 빠져나갑니다.
        en: Inverted logic exits the loop before pointers meet, preventing cycle detection.
  - label:
      ko: '사이클 진입점 찾기: 포인터 초기화'
      en: 'Phase 2: Reset pointer for entrance detection'
    indent: 0
    options:
    - code: slow2 = 0
      type: good
      why:
        ko: slow2를 0으로 초기화합니다. slow는 사이클 내의 현재 위치에서, slow2는 시작점에서 동시에 1칸씩 이동하면 두 포인터가 사이클 진입점에서 만납니다. 이것이 중복된 숫자입니다.
        en: Initialize slow2 to 0 while slow stays at its current position. Moving both at speed 1 brings them to the cycle entrance, where the duplicate value resides.
    - code: slow = 0; slow2 = slow
      type: distractor
      why:
        ko: slow를 0으로 리셋하면 fast가 가진 사이클 내의 위치 정보가 손실됩니다. slow2로 새 포인터를 만들어야 합니다.
        en: Resetting slow loses the cycle position. We need a new pointer (slow2) to simultaneously track from both locations.
    - code: slow2 = fast
      type: distractor
      why:
        ko: slow2를 fast의 현재 위치로 설정하면 처음부터 시작하지 않아 알고리즘이 작동하지 않습니다.
        en: Starting slow2 at fast's position doesn't give us the two simultaneous references needed from start and current position.
  - label:
      ko: 사이클 진입점에서 중복 찾기
      en: 'Phase 2: Find and return duplicate'
    indent: 1
    options:
    - code: return slow
      type: good
      why:
        ko: slow와 slow2가 같은 값에 도달하면, 그들이 만난 곳이 사이클의 진입점입니다. 이 위치의 값이 중복된 숫자입니다.
        en: When slow and slow2 converge to the same value, that value is the cycle entrance—the position where multiple array indices point to it, creating the duplicate.
    - code: return slow2
      type: distractor
      why:
        ko: slow2도 같은 값을 가지지만, slow를 반환하는 것이 알고리즘적으로 더 명확합니다.
        en: Both hold the same duplicate value, but returning slow is clearer semantically from the algorithm's perspective.
    - code: return fast
      type: distractor
      why:
        ko: fast는 1단계(사이클 감지)에서의 포인터이며, 2단계(진입점 찾기)에서는 갱신되지 않습니다. 잘못된 포인터입니다.
        en: fast is from phase 1 and is not updated in phase 2. Returning it would give an incorrect or stale value.
trace:
  code:
  - 'class Solution:'
  - '    def findDuplicate(self, nums: List[int]) -> int:'
  - '        slow, fast = 0, 0'
  - '        while True:'
  - '            slow = nums[slow]'
  - '            fast = nums[nums[fast]]'
  - '            if slow == fast:'
  - '                break'
  - ''
  - '        slow2 = 0'
  - '        while True:'
  - '            slow = nums[slow]'
  - '            slow2 = nums[slow2]'
  - '            if slow == slow2:'
  - '                return slow'
  cases:
  - input: '[1,3,4,2,2]'
    expected: '2'
  - input: '[3,1,3,4,2]'
    expected: '3'
  - input: '[3,3,3,3,3]'
    expected: '3'
  worked_example:
    input: '[1,3,4,2,2]'
    steps:
    - ko: '배열 [1, 3, 4, 2, 2]를 연결 리스트로 해석: 0→1→3→2→4→2→... (사이클)'
      en: 'Interpret array [1, 3, 4, 2, 2] as linked list: 0→1→3→2→4→2→... (cycle at 2↔4)'
    - ko: '1단계: slow와 fast가 같은 속도로 출발. slow=1, fast=3 → slow=3, fast=4 → slow=2, fast=4 → slow=4, fast=4 (만남)'
      en: 'Phase 1: Start both at 0. Iteration 1: slow=1, fast=3. Iteration 2: slow=3, fast=4. Iteration 3: slow=2, fast=4. Iteration 4: slow=4, fast=4 (meet)'
    - ko: '2단계: slow2=0 초기화. slow=4, slow2=0에서 출발하여 모두 1칸씩 이동. slow=2, slow2=1 → slow=4, slow2=3 → slow=2, slow2=2 (만남)'
      en: 'Phase 2: Reset slow2=0. Both advance 1 step: slow=2, slow2=1 → slow=4, slow2=3 → slow=2, slow2=2 (meet)'
    - ko: 두 포인터가 값 2에서 만남. 이것이 중복된 숫자입니다.
      en: Pointers converge at value 2. This is the duplicate.
    answer: '2'
solution:
  code: "class Solution:\n    def findDuplicate(self, nums: List[int]) -> int:\n        slow, fast = 0, 0\n        while True:\n            slow = nums[slow]\n            fast = nums[nums[fast]]\n            if slow == fast:\n                break\n\n        slow2 = 0\n        while True:\n            slow = nums[slow]\n            slow2 = nums[slow2]\n            if slow == slow2:\n                return slow\n"
  complexity:
    time: O(n)
    space: O(1)
  followup:
  - ko: 어떻게 중복이 반드시 존재함을 증명할 수 있을까요?
    en: How can you prove that at least one duplicate must exist?
  - ko: O(n log n) 시간에 해결할 수 있는 다른 방법이 있을까요?
    en: Can you solve this in O(n log n) time with a different approach?
  - ko: 배열을 수정할 수 있다면 더 간단한 O(n) 해법이 있을까요?
    en: If you could modify the array, what's a simpler O(n) solution?
```
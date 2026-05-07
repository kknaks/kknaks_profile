---
created: '2026-05-07'
date: '2026-05-07'
day: Day 03
difficulty: easy
id: A-003
source:
  curated_in:
  - neetcode150
  number: 1
  platform: leetcode
  slug: two-sum
  url: https://leetcode.com/problems/two-sum/
status: draft
tags:
- array
- hash-table
title:
  en: Two Sum
  ko: 두 수의 합
today: true
type: algorithm
updated: '2026-05-07'
visible: true
---

# 두 수의 합

## Data

```yaml
problem:
  title:
    ko: 두 수의 합
    en: Two Sum
  statement:
    ko: 배열에서 합이 목표값이 되는 두 원소의 인덱스를 찾기
    en: Find indices of two array elements that sum to a target value
  constraints:
  - 2 ≤ nums.length ≤ 10^4
  - -10^9 ≤ nums[i] ≤ 10^9
  - -10^9 ≤ target ≤ 10^9
  - Exactly one valid answer exists
  - Cannot reuse the same element twice
  io:
  - input: '[2,7,11,15]

      9'
    output: '[0,1]'
  - input: '[3,2,4]

      6'
    output: '[1,2]'
  - input: '[3,3]

      6'
    output: '[0,1]'
clarifying:
  items:
  - q:
      ko: 같은 원소를 두 번 사용할 수 있나요?
      en: Can we use the same element twice?
    type: good
    why:
      ko: 문제에서 명시적으로 같은 원소를 두 번 사용할 수 없다고 했으므로, 한 인덱스는 한 번만 사용 가능합니다.
      en: The problem explicitly states we cannot use the same element twice; each index can only appear once.
  - q:
      ko: 배열에 중복된 숫자가 있을 수 있나요?
      en: Can the array contain duplicate numbers?
    type: good
    why:
      ko: 예제 3 [3,3]에서 보듯이 중복이 가능하며, 각각 다른 인덱스로 취급됩니다.
      en: Example 3 shows [3,3] where duplicates are allowed; each is treated as a separate element by index.
  - q:
      ko: 반환 값의 인덱스 순서가 중요한가요?
      en: Does the order of indices in the return matter?
    type: good
    why:
      ko: 문제에서 임의의 순서로 반환 가능하다고 했으므로, [0,1]과 [1,0] 모두 유효합니다.
      en: The problem states 'you can return the answer in any order,' so both [0,1] and [1,0] are valid.
  - q:
      ko: 배열이 정렬되어 있다고 가정할 수 있나요?
      en: Can we assume the array is sorted?
    type: good
    why:
      ko: 입력 배열은 정렬되어 있지 않습니다. 정렬하면 원본 인덱스 정보가 손실됩니다.
      en: The input array is not sorted. Sorting would lose the original indices we need to return.
  - q:
      ko: 음수도 포함될 수 있나요?
      en: Can negative numbers be included?
    type: good
    why:
      ko: 제약 조건에서 -10^9 ≤ nums[i]이므로 음수도 가능합니다.
      en: Constraints show -10^9 ≤ nums[i], so negative numbers are possible.
  - q:
      ko: 입력 배열을 수정할 수 있나요?
      en: Can we modify the input array?
    type: distractor
    why:
      ko: 기술적으로는 가능하지만, 원본 인덱스가 필요하므로 배열을 정렬하면 해결하기 어려워집니다.
      en: While modifying is possible, sorting or changing the array would lose original indices.
  - q:
      ko: 값 자체를 반환해야 하나요, 인덱스를 반환해야 하나요?
      en: Should we return the values or the indices?
    type: distractor
    why:
      ko: 문제에서 명확히 인덱스를 반환하라고 했습니다. 값을 반환하는 것은 잘못된 이해입니다.
      en: The problem explicitly asks for indices, not values. Returning values would be incorrect.
approach:
  items:
  - name:
      ko: 해시맵 활용 (한 번의 패스)
      en: Hash map (one-pass)
    complexity: O(n) time / O(n) space
    type: good
    why:
      ko: 배열을 한 번 순회하면서 필요한 값이 이미 해시맵에 있는지 확인합니다. 최적의 시간복잡도를 달성합니다.
      en: Single pass through array, checking if complement exists in hash map at each step. Achieves optimal time complexity.
  - name:
      ko: 해시맵 활용 (두 번의 패스)
      en: Hash map (two-pass)
    complexity: O(n) time / O(n) space
    type: good
    why:
      ko: 첫 번째 패스에서 모든 값을 해시맵에 저장한 후, 두 번째 패스에서 필요한 값을 찾습니다. 같은 복잡도이지만 로직이 더 직관적입니다.
      en: First pass builds the hash map, second pass finds answer. Same complexity but more straightforward.
  - name:
      ko: 브루트 포스 (중첩 루프)
      en: Brute force (nested loops)
    complexity: O(n²) time / O(1) space
    type: distractor
    why:
      ko: 모든 쌍을 비교하는 방법으로 간단하지만 효율이 떨어집니다. 면접에서는 이 방법부터 시작해 최적화로 나아가는 것이 좋습니다.
      en: Checks all pairs; simple but inefficient. Good starting point to show optimization thinking.
  - name:
      ko: 정렬 + 두 포인터
      en: Sort + two pointers
    complexity: O(n log n) time / O(1) space
    type: distractor
    why:
      ko: 정렬하면 원래 인덱스 정보가 손실되므로 이 문제에는 부적합합니다.
      en: Sorting loses original indices that we need to return. Not suitable for this problem.
logic:
  format: slot
  slots:
  - label:
      ko: 해시맵 초기화
      en: Initialize hash map
    indent: 0
    options:
    - code: 'prevMap = {}  # val -> index'
      type: good
      why:
        ko: 빠른 검색을 위해 값과 인덱스의 매핑을 저장할 빈 딕셔너리를 준비합니다.
        en: Create empty hash map to store value-to-index mappings for O(1) lookups.
    - code: prevMap = []
      type: distractor
      why:
        ko: 배열은 값으로 빠른 검색이 불가능하므로 O(n) 시간이 걸립니다.
        en: Arrays don't support O(1) value-based lookup.
    - code: prevMap = set()
      type: distractor
      why:
        ko: set은 키만 저장하고 인덱스 정보를 저장할 수 없습니다.
        en: Sets don't store indices, only whether values exist.
    - code: prevMap = defaultdict(int)
      type: distractor
      why:
        ko: 이는 값의 빈도를 세는 용도이며, 인덱스 저장에는 적합하지 않습니다.
        en: This structure counts frequencies, not stores indices.
  - label:
      ko: 배열 순회
      en: Iterate through array
    indent: 0
    options:
    - code: 'for i, n in enumerate(nums):'
      type: good
      why:
        ko: 각 원소와 그 인덱스를 동시에 얻기 위해 enumerate를 사용합니다.
        en: Use enumerate to access both value and index in one pass.
    - code: 'for i in range(len(nums)):'
      type: distractor
      why:
        ko: 이 방식도 작동하지만 enumerate보다 더 복잡합니다.
        en: Works but more verbose than enumerate.
    - code: 'for n in nums:'
      type: distractor
      why:
        ko: 인덱스 정보가 없으므로 나중에 인덱스를 반환할 수 없습니다.
        en: Without index, we cannot return indices in the result.
    - code: 'for i, n in reversed(enumerate(nums)):'
      type: distractor
      why:
        ko: 역순으로 순회하면 미리 본 원소를 찾을 수 없게 됩니다.
        en: Reverse iteration breaks the algorithm's logic of finding previously-seen elements.
  - label:
      ko: 필요한 값 계산
      en: Calculate complement
    indent: 1
    options:
    - code: diff = target - n
      type: good
      why:
        ko: 현재 원소 n이 주어질 때, target - n이 우리가 찾아야 할 여집합입니다.
        en: Given current element n, the complement we need is target - n.
    - code: diff = n - target
      type: distractor
      why:
        ko: 뺄셈의 순서가 반대이므로 잘못된 여집합을 찾게 됩니다.
        en: Reversed subtraction gives the wrong complement.
    - code: diff = target + n
      type: distractor
      why:
        ko: 더하기는 여집합의 반대이며 합을 구하는 데 도움이 되지 않습니다.
        en: Addition is opposite of what we need; we need subtraction.
    - code: diff = target // n
      type: distractor
      why:
        ko: 나눗셈은 덧셈의 여집합과 무관하므로 부정확합니다.
        en: Division has no relation to finding a sum's complement.
  - label:
      ko: 여집합 존재 확인
      en: Check if complement exists
    indent: 1
    options:
    - code: 'if diff in prevMap:'
      type: good
      why:
        ko: 계산한 diff가 이미 본 원소(prevMap)에 있는지 확인합니다. O(1) 시간에 검색 가능합니다.
        en: Check if complement exists in hash map. O(1) lookup finds it instantly.
    - code: 'if n in prevMap:'
      type: distractor
      why:
        ko: 현재 원소 자체를 확인하는 것은 필요한 여집합을 확인하지 않습니다.
        en: Checking current element doesn't verify the complement exists.
    - code: 'if i in prevMap:'
      type: distractor
      why:
        ko: 인덱스 i는 prevMap의 값이지 키가 아니므로 항상 false입니다.
        en: Indices are values in prevMap, not keys; this always returns false.
    - code: 'if diff in nums:'
      type: distractor
      why:
        ko: 배열에서 선형 검색하므로 O(n) 시간이 걸려 해시맵의 이점을 잃습니다.
        en: Searching in array is O(n); loses O(1) benefit of hash map.
  - label:
      ko: 답 반환
      en: Return result
    indent: 2
    options:
    - code: return [prevMap[diff], i]
      type: good
      why:
        ko: 여집합의 인덱스를 먼저, 현재 인덱스를 뒤에 배치하여 답을 반환합니다.
        en: Return indices as [complement_index, current_index].
    - code: return [i, prevMap[diff]]
      type: distractor
      why:
        ko: 인덱스 순서가 반대입니다. 문제에서는 임의의 순서를 허용하지만 관례상 작은 값을 먼저 반환합니다.
        en: Indices in reverse order. While any order is accepted, convention puts smaller index first.
    - code: return (prevMap[diff], i)
      type: distractor
      why:
        ko: 튜플 형태로 반환하면 리스트가 아니므로 타입이 잘못됩니다.
        en: Returns tuple instead of list; wrong type.
    - code: return [prevMap[diff], n]
      type: distractor
      why:
        ko: 현재 값 n을 인덱스 대신 반환하므로 잘못된 답입니다.
        en: Returns value instead of current index.
  - label:
      ko: 현재 원소 저장
      en: Store current element
    indent: 1
    options:
    - code: prevMap[n] = i
      type: good
      why:
        ko: 현재 원소를 해시맵에 저장하여 다음 반복에서 여집합으로 사용될 수 있도록 합니다.
        en: Store current value with its index so future iterations can find it as a complement.
    - code: prevMap[i] = n
      type: distractor
      why:
        ko: 인덱스와 값의 위치가 바뀌어 있으면 나중에 값으로 인덱스를 찾을 수 없습니다.
        en: Swapped key-value; can't look up index by value later.
    - code: prevMap[n] = prevMap.get(n, 0) + 1
      type: distractor
      why:
        ko: 값의 빈도를 세는 것은 불필요하고 인덱스 정보를 덮어씁니다.
        en: Counting frequency loses index information we need.
    - code: prevMap.add(n)
      type: distractor
      why:
        ko: set의 add 메서드는 인덱스를 저장할 수 없으며 dict이 아닙니다.
        en: Sets can't store value-to-index mappings.
trace:
  code:
  - 'class Solution:'
  - '    def twoSum(self, nums: List[int], target: int) -> List[int]:'
  - '        prevMap = {}  # val -> index'
  - ''
  - '        for i, n in enumerate(nums):'
  - '            diff = target - n'
  - '            if diff in prevMap:'
  - '                return [prevMap[diff], i]'
  - '            prevMap[n] = i'
  cases:
  - input: '[2,7,11,15]

      9'
    expected: '[0,1]'
  - input: '[3,2,4]

      6'
    expected: '[1,2]'
  - input: '[3,3]

      6'
    expected: '[0,1]'
  worked_example:
    input: '[2,7,11,15]

      9'
    steps:
    - ko: 'prevMap = {}, i=0, n=2: diff = 9-2 = 7, 7이 prevMap에 없음 → prevMap = {2: 0}'
      en: 'Step 1: i=0, n=2, diff=7. 7 not in prevMap. Store {2: 0}.'
    - ko: 'i=1, n=7: diff = 9-7 = 2, 2가 prevMap에 있음! prevMap[2] = 0'
      en: 'Step 2: i=1, n=7, diff=2. Found! 2 exists in prevMap at index 0.'
    - ko: return [prevMap[2], 1] = [0, 1]
      en: 'Step 3: Return [0, 1] — indices of elements that sum to 9.'
    answer: '[0,1]'
solution:
  code: "class Solution:\n    def twoSum(self, nums: List[int], target: int) -> List[int]:\n        prevMap = {}  # val -> index\n\n        for i, n in enumerate(nums):\n            diff = target - n\n            if diff in prevMap:\n                return [prevMap[diff], i]\n            prevMap[n] = i\n"
  complexity:
    time: O(n)
    space: O(n)
  followup:
  - ko: 만약 여러 개의 유효한 쌍이 존재한다면, 모두 반환하도록 코드를 수정할 수 있을까요?
    en: How would you modify the code if multiple valid pairs existed and you needed to return all of them?
  - ko: 추가 공간을 사용하지 않고 O(n) 시간으로 풀 수 있을까요?
    en: Can you solve this in O(n) time without using extra space for a hash map?
  - ko: 배열이 정렬되어 있다면, 두 포인터로 더 효율적으로 풀 수 있을까요?
    en: If the array were sorted, could you use two pointers for a more space-efficient solution?
```
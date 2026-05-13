---
created: '2026-05-13'
date: '2026-05-13'
day: Day 11
difficulty: medium
id: A-011
source:
  curated_in:
  - neetcode150
  number: 167
  platform: leetcode
  slug: two-sum-ii-input-array-is-sorted
  url: https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/
status: draft
tags:
- array
- two-pointers
- binary-search
title:
  en: Two Sum II - Input Array Is Sorted
  ko: 두 수의 합 II - 입력 배열이 정렬됨
today: true
type: algorithm
updated: '2026-05-13'
visible: true
---

# 두 수의 합 II - 입력 배열이 정렬됨

## Data

```yaml
problem:
  title:
    ko: 두 수의 합 II - 입력 배열이 정렬됨
    en: Two Sum II - Input Array Is Sorted
  statement:
    ko: '1부터 인덱싱되는 정수 배열 numbers가 비내림차순으로 정렬되어 있을 때, 특정 target 값으로 더해지는 두 수를 찾으세요. 이 두 수를 numbers[index1]과 numbers[index2]라 하면 1 <= index1 < index2 <= numbers.length를 만족합니다.


      두 수의 인덱스 index1과 index2를 각각 1씩 증가시킨 정수 배열 [index1, index2]로 반환하세요.


      테스트는 정확히 하나의 해가 존재하도록 생성됩니다. 같은 원소를 두 번 사용할 수 없습니다.


      당신의 솔루션은 상수 크기의 추가 공간만 사용해야 합니다.'
    en: 'Given a 1-indexed array of integers numbers that is already sorted in non-decreasing order, find two numbers such that they add up to a specific target number. Let these two numbers be numbers[index1] and numbers[index2] where 1 <= index1 < index2 <= numbers.length.


      Return the indices of the two numbers index1 and index2, each incremented by one, as an integer array [index1, index2] of length 2.


      The tests are generated such that there is exactly one solution. You may not use the same element twice.


      Your solution must use only constant extra space.'
  constraints:
  - 2 ≤ numbers.length ≤ 3 × 10⁴
  - -1000 ≤ numbers[i] ≤ 1000
  - Array is sorted in non-decreasing order
  - -1000 ≤ target ≤ 1000
  - Exactly one solution exists
  io:
  - input: '[2,7,11,15]

      9'
    output: '[1,2]'
  - input: '[2,3,4]

      6'
    output: '[1,3]'
  - input: '[-1,0]

      -1'
    output: '[1,2]'
clarifying:
  items:
  - q:
      ko: 반환하는 인덱스는 0부터 시작인가요, 1부터 시작인가요?
      en: Should the returned indices be 0-based or 1-based?
    type: good
    why:
      ko: 문제에서 '1-인덱싱된 배열'이라고 명시되어 있고, 각 인덱스에 1을 더해 반환해야 합니다.
      en: The problem explicitly states '1-indexed array' and requires each index incremented by one.
  - q:
      ko: 같은 배열 원소를 두 번 사용할 수 있나요?
      en: Can we use the same array element twice?
    type: good
    why:
      ko: 문제에서 '같은 원소를 두 번 사용할 수 없습니다'라고 명시되어 있으므로 index1과 index2는 다른 위치여야 합니다.
      en: The problem states 'You may not use the same element twice', so the two indices must be different.
  - q:
      ko: 배열이 정렬되어 있다는 사실을 왜 중요하게 사용해야 할까요?
      en: Why does the sorted property matter for the solution?
    type: good
    why:
      ko: 정렬된 배열에서는 두 포인터를 양쪽 끝에서 시작하여, 합의 크기에 따라 안전하게 이동할 수 있습니다.
      en: In a sorted array, two pointers from opposite ends can safely move based on the sum comparison.
  - q:
      ko: 상수 공간만 사용한다는 조건이 없다면?
      en: What if the constant space constraint didn't exist?
    type: good
    why:
      ko: 해시맵을 사용하면 O(n) 시간에 한 번의 패스로 해를 찾을 수 있지만 O(n) 공간이 필요합니다. 정렬된 성질을 활용하면 공간을 절약할 수 있습니다.
      en: A hash map allows O(n) one-pass solution but requires O(n) space. The sorted property lets us achieve O(1) space.
  - q:
      ko: 음수가 배열에 포함될 수 있나요?
      en: Can the array contain negative numbers?
    type: good
    why:
      ko: 제약 조건에서 -1000 ≤ numbers[i] ≤ 1000이므로 음수도 포함됩니다. 두 포인터 알고리즘은 음수에도 동일하게 작동합니다.
      en: Yes, constraints show -1000 ≤ numbers[i] ≤ 1000. The two-pointer algorithm works identically with negative numbers.
  - q:
      ko: 여러 개의 해가 존재할 수 있나요?
      en: Could there be multiple valid solutions?
    type: distractor
    why:
      ko: 문제에서 '정확히 하나의 해가 존재하도록 생성됩니다'라고 명시되어 있습니다.
      en: The problem states 'The tests are generated such that there is exactly one solution.'
  - q:
      ko: 실제 두 수의 값을 반환해야 하나요?
      en: Should we return the actual numbers instead of indices?
    type: distractor
    why:
      ko: 문제는 명확히 '두 수의 인덱스'를 반환하도록 요구합니다.
      en: The problem explicitly asks to 'Return the indices', not the values themselves.
approach:
  items:
  - name:
      ko: 투 포인터
      en: Two Pointers
    complexity: O(n) time / O(1) space
    type: good
    why:
      ko: 양 끝에서 포인터를 시작하여 합을 비교하며 이동합니다. 상수 공간 제약을 만족하는 최적 솔루션입니다.
      en: Start pointers at both ends, move based on sum comparison. Optimal for the constant space requirement.
  - name:
      ko: 해시맵
      en: Hash Map
    complexity: O(n) time / O(n) space
    type: good
    why:
      ko: 각 원소를 순회하며 (target - 현재값)을 해시맵에서 찾습니다. 구현이 간단하지만 추가 공간이 필요합니다.
      en: For each element, check if (target - element) exists in the hash map. Simple but requires O(n) extra space.
  - name:
      ko: 이진 탐색
      en: Binary Search
    complexity: O(n log n) time / O(1) space
    type: distractor
    why:
      ko: 각 원소에 대해 complement를 이진 탐색으로 찾을 수 있지만, 투 포인터보다 느리고 정렬 성질을 충분히 활용하지 못합니다.
      en: For each element, binary search for its complement. Works but slower than two-pointers and underutilizes the sorted property.
  - name:
      ko: 중첩 루프 (브루트 포스)
      en: Brute Force (Nested Loops)
    complexity: O(n²) time / O(1) space
    type: distractor
    why:
      ko: 모든 쌍을 확인합니다. 정렬 성질을 활용하지 못하며 시간 복잡도가 나쁩니다.
      en: Check all pairs. Ignores the sorted property entirely with poor time complexity.
logic:
  format: slot
  slots:
  - label:
      ko: 포인터 초기화
      en: Initialize Pointers
    indent: 0
    options:
    - code: l, r = 0, len(numbers) - 1
      type: good
      why:
        ko: 왼쪽 포인터는 배열의 시작(0), 오른쪽 포인터는 끝(len-1)에 배치하여 양쪽 끝에서 시작합니다.
        en: Left pointer at start (0), right pointer at last valid index (len-1) to search from both ends.
    - code: l, r = 0, len(numbers)
      type: distractor
      why:
        ko: len(numbers)는 배열 범위를 벗어납니다. 유효한 마지막 인덱스는 len(numbers)-1입니다.
        en: len(numbers) is out of bounds. The last valid index is len(numbers) - 1.
    - code: l, r = 1, len(numbers) - 1
      type: distractor
      why:
        ko: 1부터 시작하면 첫 번째 원소(인덱스 0)를 검사할 수 없어 정답을 놓칠 수 있습니다.
        en: Starting from 1 skips the first element at index 0, potentially missing the answer.
  - label:
      ko: 루프 조건
      en: Loop Condition
    indent: 0
    options:
    - code: 'while l < r:'
      type: good
      why:
        ko: l < r을 유지하면 같은 원소를 두 번 사용하지 않으면서 모든 가능한 쌍을 탐색합니다.
        en: l < r ensures we don't use the same element twice while exploring all possibilities.
    - code: 'while l <= r:'
      type: distractor
      why:
        ko: l == r인 경우 같은 위치의 원소를 두 번 사용하게 되므로 문제 조건을 위반합니다.
        en: l == r means using the same element twice, violating the constraint.
    - code: 'while l < r - 1:'
      type: distractor
      why:
        ko: 조건이 너무 빨리 종료되어 인접한 두 원소의 유효한 쌍을 놓칠 수 있습니다.
        en: Terminates too early and might miss valid pairs of adjacent elements.
  - label:
      ko: 현재 합 계산
      en: Calculate Current Sum
    indent: 1
    options:
    - code: curSum = numbers[l] + numbers[r]
      type: good
      why:
        ko: 양 포인터가 가리키는 원소의 합을 계산하여 target과 비교합니다.
        en: Calculate the sum of elements at both pointers to compare against target.
    - code: curSum = numbers[r] - numbers[l]
      type: distractor
      why:
        ko: 두 수를 더해야 하는데 빼고 있습니다.
        en: We need addition, not subtraction.
    - code: curSum = numbers[l + 1] + numbers[r]
      type: distractor
      why:
        ko: l 인덱스를 미리 증가시켜서는 안 됩니다. 현재 위치 numbers[l]을 정확히 사용해야 합니다.
        en: Should use numbers[l] directly, not numbers[l+1].
  - label:
      ko: 합이 크면 오른쪽 포인터 왼쪽으로 이동
      en: If Sum Too Large, Move Right Pointer Left
    indent: 1
    options:
    - code: r -= 1
      type: good
      why:
        ko: 합이 target보다 크면 더 작은 합을 만들기 위해 오른쪽 포인터를 왼쪽으로 이동합니다.
        en: If sum is too large, decrease the right pointer to reduce the sum.
    - code: l += 1
      type: distractor
      why:
        ko: 합이 크면 왼쪽 포인터를 증가시키면 합이 더 커집니다. 오른쪽을 감소시켜야 합니다.
        en: Increasing left pointer makes the sum even larger. Should decrease right.
    - code: r -= 2
      type: distractor
      why:
        ko: 2칸씩 이동하면 유효한 정답을 건너뛸 수 있습니다. 1칸씩 이동해야 합니다.
        en: Skipping two positions might miss the correct answer. Move one position at a time.
  - label:
      ko: 합이 작으면 왼쪽 포인터 오른쪽으로 이동
      en: If Sum Too Small, Move Left Pointer Right
    indent: 1
    options:
    - code: l += 1
      type: good
      why:
        ko: 합이 target보다 작으면 더 큰 합을 만들기 위해 왼쪽 포인터를 오른쪽으로 이동합니다.
        en: If sum is too small, increase the left pointer to increase the sum.
    - code: r -= 1
      type: distractor
      why:
        ko: 합이 작을 때 오른쪽 포인터를 감소시키면 합이 더 작아집니다. 왼쪽을 증가시켜야 합니다.
        en: Decreasing right pointer makes the sum even smaller. Should increase left.
    - code: l = l + 2
      type: distractor
      why:
        ko: 큰 폭으로 이동하면 정답을 건너뛸 수 있습니다. 1칸씩 이동해야 합니다.
        en: Large jumps might skip the correct answer. Move one position at a time.
  - label:
      ko: 정확한 합을 찾아 1-인덱싱된 인덱스 반환
      en: Found Exact Sum - Return 1-Indexed Indices
    indent: 1
    options:
    - code: return [l + 1, r + 1]
      type: good
      why:
        ko: 합이 정확히 target과 같으면, 각 인덱스에 1을 더하여 1-인덱싱된 배열로 반환합니다.
        en: When sum equals target, return indices incremented by 1 to match the 1-indexed requirement.
    - code: return [l, r]
      type: distractor
      why:
        ko: 문제가 1-인덱싱을 요구하므로 각 인덱스에 1을 더해야 합니다.
        en: Problem requires 1-indexed output. Must add 1 to each index.
    - code: return [numbers[l], numbers[r]]
      type: distractor
      why:
        ko: 문제는 인덱스를 반환해야 하며, 실제 원소의 값이 아닙니다.
        en: Must return indices, not the actual number values.
trace:
  code:
  - 'class Solution:'
  - '    def twoSum(self, numbers: List[int], target: int) -> List[int]:'
  - '        l, r = 0, len(numbers) - 1'
  - ''
  - '        while l < r:'
  - '            curSum = numbers[l] + numbers[r]'
  - ''
  - '            if curSum > target:'
  - '                r -= 1'
  - '            elif curSum < target:'
  - '                l += 1'
  - '            else:'
  - '                return [l + 1, r + 1]'
  cases:
  - input: '[2,7,11,15]

      9'
    expected: '[1,2]'
  - input: '[2,3,4]

      6'
    expected: '[1,3]'
  - input: '[-1,0]

      -1'
    expected: '[1,2]'
  worked_example:
    input: '[2,7,11,15]

      9'
    steps:
    - ko: l=0, r=3 초기화. numbers[0]=2, numbers[3]=15.
      en: Initialize l=0, r=3. numbers[0]=2, numbers[3]=15.
    - ko: '합 = 2+15=17 > 9이므로 r을 왼쪽으로 이동: r=2.'
      en: 'Sum = 2+15=17 > 9, move right left: r=2.'
    - ko: '합 = 2+11=13 > 9이므로 r을 왼쪽으로 이동: r=1.'
      en: 'Sum = 2+11=13 > 9, move right left: r=1.'
    - ko: 합 = 2+7=9 == 9이므로 [0+1, 1+1] = [1, 2]를 반환합니다.
      en: Sum = 2+7=9 == 9, return [0+1, 1+1] = [1, 2].
    answer: '[1,2]'
solution:
  code: "class Solution:\n    def twoSum(self, numbers: List[int], target: int) -> List[int]:\n        l, r = 0, len(numbers) - 1\n\n        while l < r:\n            curSum = numbers[l] + numbers[r]\n\n            if curSum > target:\n                r -= 1\n            elif curSum < target:\n                l += 1\n            else:\n                return [l + 1, r + 1]\n"
  complexity:
    time: O(n)
    space: O(1)
  followup:
  - ko: 배열이 정렬되어 있지 않다면 어떻게 해결할까요?
    en: How would you solve this if the array wasn't sorted?
  - ko: 세 개의 수의 합을 target으로 하는 문제(3-sum)로 확장한다면?
    en: How would you extend this to find three numbers that sum to a target (3-sum problem)?
  - ko: target을 만족하는 모든 쌍의 개수를 찾아야 한다면?
    en: What if you needed to count all pairs that sum to target, not just find one?
```
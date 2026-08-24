---
created: '2026-06-03'
date: '2026-06-03'
day: Day 28
difficulty: easy
id: A-028
source:
  curated_in:
  - neetcode150
  number: 704
  platform: leetcode
  slug: binary-search
  url: https://leetcode.com/problems/binary-search/
tags:
- array
- binary-search
title:
  en: Binary Search
  ko: 이진 탐색
today: false
type: algorithm
updated: '2026-06-03'
visible: true
---

# 이진 탐색

## Data

```yaml
problem:
  title:
    ko: 이진 탐색
    en: Binary Search
  statement:
    ko: '오름차순으로 정렬된 정수 배열 nums와 정수 target이 주어졌을 때, nums에서 target을 찾는 함수를 작성하세요. target이 존재하면 그 인덱스를 반환합니다. 존재하지 않으면 -1을 반환합니다.


      O(log n) 시간 복잡도의 알고리즘을 작성해야 합니다.'
    en: 'Given an array of integers nums which is sorted in ascending order, and an integer target, write a function to search target in nums. If target exists, then return its index. Otherwise, return -1.


      You must write an algorithm with O(log n) runtime complexity.'
  constraints:
  - 1 ≤ nums.length ≤ 10⁴
  - -10⁴ < nums[i], target < 10⁴
  - All integers in nums are unique
  - nums is sorted in ascending order
  io:
  - input: '[-1,0,3,5,9,12]

      9'
    output: '4'
  - input: '[-1,0,3,5,9,12]

      2'
    output: '-1'
clarifying:
  items:
  - q:
      ko: 반환 값이 0-based 인덱스인가요?
      en: Is the return value 0-based indexing?
    type: good
    why:
      ko: 배열의 인덱싱 체계를 명확히 하여 올바른 위치를 이해할 수 있습니다.
      en: Clarifies the indexing system to correctly interpret the expected output.
  - q:
      ko: target이 배열에 없으면 정확히 무엇을 반환해야 하나요?
      en: What should be returned if the target is not in the array?
    type: good
    why:
      ko: 검색 실패 시의 특정 값(−1)을 반환하는 핵심 동작을 정의합니다.
      en: Defines the specific return value (-1) for the failure case.
  - q:
      ko: O(log n) 복잡도 요구사항은 무엇을 의미하나요?
      en: What does the O(log n) complexity requirement imply?
    type: good
    why:
      ko: 이진 탐색 알고리즘이 필수이며, 선형 탐색(O(n))은 불가능함을 의미합니다.
      en: This constraint mandates binary search and rules out linear search approaches.
  - q:
      ko: 배열에 중복된 값이 포함될 수 있나요?
      en: Can the array contain duplicate values?
    type: good
    why:
      ko: 제약 조건에서 모든 정수가 유일하다고 명시되어 있으므로 중복 처리 로직이 불필요합니다.
      en: The constraints guarantee all elements are unique, eliminating the need for duplicate handling.
  - q:
      ko: 배열을 먼저 정렬해야 하나요?
      en: Do we need to sort the array first?
    type: distractor
    why:
      ko: 문제에서 배열이 이미 정렬되어 있다고 명시했으므로, 추가 정렬은 낭비입니다.
      en: The problem guarantees the array is already sorted; sorting would waste time.
  - q:
      ko: 모든 요소를 순차적으로 확인하는 선형 탐색이 충분한가요?
      en: Is linear search (checking every element) acceptable?
    type: distractor
    why:
      ko: 선형 탐색은 O(n) 시간 복잡도를 가지므로 O(log n) 요구사항을 만족하지 못합니다.
      en: Linear search is O(n), which violates the O(log n) requirement.
  - q:
      ko: target과 일치하는 모든 인덱스를 반환해야 하나요?
      en: Should we return all indices where the target appears?
    type: distractor
    why:
      ko: 문제는 하나의 인덱스 또는 -1만 반환하도록 요구하며, 모든 요소가 유일하므로 관련 없습니다.
      en: The problem asks for a single index or -1, and uniqueness is guaranteed.
approach:
  items:
  - name:
      ko: 이진 탐색 (반복)
      en: Binary Search (Iterative)
    complexity: O(log n) time / O(1) space
    type: good
    why:
      ko: 두 포인터가 검색 범위를 매번 절반으로 줄이므로 O(log n) 요구사항을 정확히 충족하며, 추가 메모리를 사용하지 않습니다.
      en: Divides the search space by half each iteration, meeting O(log n) exactly with constant space.
  - name:
      ko: 이진 탐색 (재귀)
      en: Binary Search (Recursive)
    complexity: O(log n) time / O(log n) space
    type: good
    why:
      ko: 재귀로 구현해도 같은 시간 복잡도를 달성하지만, 호출 스택으로 인해 O(log n) 공간을 사용합니다.
      en: Same time complexity as iterative, but uses O(log n) space for the recursion call stack.
  - name:
      ko: 선형 탐색
      en: Linear Search
    complexity: O(n) time / O(1) space
    type: distractor
    why:
      ko: 모든 요소를 순차적으로 확인하는 방식이지만, O(n) 복잡도로 O(log n) 요구사항을 만족하지 못합니다.
      en: Checks every element sequentially; O(n) violates the O(log n) requirement.
  - name:
      ko: 해시맵 조회
      en: Hash Map Lookup
    complexity: O(n) preprocessing / O(1) lookup
    type: distractor
    why:
      ko: 해시맵을 미리 구성해야 하므로 전체 복잡도가 O(n)이 되며, 정렬된 배열의 성질을 활용하지 못합니다.
      en: Requires O(n) preprocessing; doesn't leverage the sorted array property.
logic:
  format: slot
  slots:
  - label:
      ko: 포인터 초기화
      en: Initialize Pointers
    indent: 0
    options:
    - code: l, r = 0, len(nums) - 1
      type: good
      why:
        ko: 왼쪽과 오른쪽 포인터를 배열의 첫 인덱스와 마지막 인덱스로 설정하여 검색 범위를 정의합니다.
        en: Sets the left and right boundaries at array start (0) and end (len(nums) - 1).
    - code: l, r = 0, len(nums)
      type: distractor
      why:
        ko: 오른쪽 경계가 len(nums)로 설정되면 배열 범위를 벗어나 인덱스 오류가 발생합니다.
        en: Right boundary at len(nums) is out of bounds; must be len(nums) - 1.
    - code: l, r = 1, len(nums) - 1
      type: distractor
      why:
        ko: 왼쪽을 1부터 시작하면 첫 번째 요소(인덱스 0)가 검색되지 않을 수 있습니다.
        en: Starting left at 1 skips the first element, which could be the target.
  - label:
      ko: 반복 조건
      en: Loop Condition
    indent: 0
    options:
    - code: 'while l <= r:'
      type: good
      why:
        ko: l <= r은 두 포인터가 만나거나 교차할 때까지 검색을 계속함을 의미하며, 탐색 공간이 유효함을 나타냅니다.
        en: l <= r ensures we continue while the search space is valid; loop exits when pointers cross.
    - code: 'while l < r:'
      type: distractor
      why:
        ko: l < r 조건이면 l == r일 때 루프가 종료되어, 중간에 남은 마지막 요소를 확인하지 못합니다.
        en: Exits before l == r, missing the last potential element when l == r.
    - code: 'while l <= r and nums[l] != target:'
      type: distractor
      why:
        ko: 반복 조건에 탐색 로직을 섞으면 이진 탐색 구조가 흐트러지고 복잡도 분석이 어렵습니다.
        en: Mixing search logic with the loop condition complicates the algorithm structure.
  - label:
      ko: 중간값 계산
      en: Calculate Middle Index
    indent: 1
    options:
    - code: 'm = l + ((r - l) // 2)  # (l + r) // 2 can lead to overflow'
      type: good
      why:
        ko: l + ((r - l) // 2) 형태는 정수 오버플로우를 방지하면서 안전하게 중간값을 계산합니다. (l + r) // 2는 큰 수에서 오버플로우 위험이 있습니다.
        en: l + ((r - l) // 2) avoids overflow by computing the offset safely, unlike (l + r) // 2.
    - code: m = (l + r) // 2
      type: distractor
      why:
        ko: l과 r이 모두 크면 l + r이 정수 범위를 초과할 수 있으므로 오버플로우 위험이 있습니다.
        en: When l and r are large, l + r can overflow in languages with fixed integer sizes.
    - code: m = (r - l) // 2
      type: distractor
      why:
        ko: l의 오프셋을 더하지 않으면 범위 [l, r]의 중간값이 아니라 잘못된 인덱스를 계산합니다.
        en: Without adding l, this calculates the wrong index; missing the +l offset.
  - label:
      ko: 중간값이 target보다 크면 좌측 탐색
      en: If Middle > Target, Search Left
    indent: 1
    options:
    - code: 'if nums[m] > target:'
      type: good
      why:
        ko: nums[m] > target이면 target은 중간값의 왼쪽(더 작은 값)에만 있을 수 있으므로, 오른쪽 경계를 중간값 왼쪽으로 이동합니다.
        en: If nums[m] > target, the target must be to the left; move the right boundary left.
    - code: 'if nums[m] >= target:'
      type: distractor
      why:
        ko: '>= 조건은 target과 같을 때도 포함하므로, target을 찾았음에도 계속 탐색하여 의도하지 않은 동작이 발생합니다.'
        en: Using >= would exclude the case nums[m] == target, missing the found element.
    - code: 'if nums[m] > target: l = m + 1'
      type: distractor
      why:
        ko: 비교 조건은 맞지만 조정 방향이 반대이므로, 제외해야 할 쪽으로 계속 탐색합니다.
        en: Correct comparison but wrong direction; should move right pointer, not left.
  - label:
      ko: 중간값이 target보다 작으면 우측 탐색
      en: If Middle < Target, Search Right
    indent: 1
    options:
    - code: 'elif nums[m] < target:'
      type: good
      why:
        ko: nums[m] < target이면 target은 중간값의 오른쪽(더 큰 값)에만 있을 수 있으므로, 왼쪽 경계를 중간값 오른쪽으로 이동합니다.
        en: If nums[m] < target, the target must be to the right; move the left boundary right.
    - code: 'elif nums[m] < target: r = m - 1'
      type: distractor
      why:
        ko: 비교는 맞지만 조정 방향이 반대이므로, 탐색 범위가 계속 줄어들어 target을 놓칩니다.
        en: Correct comparison but wrong direction; should move left pointer, not right.
    - code: 'elif nums[m] <= target:'
      type: distractor
      why:
        ko: <= 조건을 사용하면 nums[m] == target인 경우 두 개의 분기에서 처리되어 모호해집니다.
        en: Using <= overlaps with the found case, creating ambiguity in logic flow.
  - label:
      ko: 결과 반환
      en: Return Result
    indent: 0
    options:
    - code: 'else:'
      type: good
      why:
        ko: else 블록에서 nums[m] == target일 때 인덱스 m을 반환하고, 루프를 벗어나면 -1을 반환하여 target이 배열에 없음을 나타냅니다.
        en: Return m when found (else block), and -1 after loop if not found.
    - code: 'else: return -1'
      type: distractor
      why:
        ko: 이렇게 하면 target을 찾았을 때(-1이 아닐 때) -1을 반환하는 논리 오류가 발생합니다.
        en: This would return -1 even when nums[m] equals target, which is wrong.
    - code: 'if nums[m] == target: return m

        else: continue'
      type: distractor
      why:
        ko: 루프 밖에서 다시 -1을 반환해야 하므로 구조가 부자연스럽고, else 블록이 더 이진 탐색 패턴과 일치합니다.
        en: Less idiomatic than using the final return -1 outside the loop.
trace:
  code:
  - 'class Solution:'
  - '    def search(self, nums: List[int], target: int) -> int:'
  - '        l, r = 0, len(nums) - 1'
  - ''
  - '        while l <= r:'
  - '            m = l + ((r - l) // 2)  # (l + r) // 2 can lead to overflow'
  - '            if nums[m] > target:'
  - '                r = m - 1'
  - '            elif nums[m] < target:'
  - '                l = m + 1'
  - '            else:'
  - '                return m'
  - '        return -1'
  cases:
  - input: '[-1,0,3,5,9,12]

      9'
    expected: '4'
  - input: '[-1,0,3,5,9,12]

      2'
    expected: '-1'
  worked_example:
    input: '[-1,0,3,5,9,12]

      9'
    steps:
    - ko: '초기: l=0, r=5 (배열의 양 끝)'
      en: 'Initialize: l=0, r=5 (array bounds)'
    - ko: '반복 1: m=2, nums[2]=3, 3<9 → l=3 (오른쪽 탐색)'
      en: 'Iteration 1: m=2, nums[2]=3, 3<9 → l=3 (search right half)'
    - ko: '반복 2: m=4, nums[4]=9, 9==9 → 찾음! 인덱스 4 반환'
      en: 'Iteration 2: m=4, nums[4]=9, 9==9 → found! Return 4'
    answer: '4'
solution:
  code: "class Solution:\n    def search(self, nums: List[int], target: int) -> int:\n        l, r = 0, len(nums) - 1\n\n        while l <= r:\n            m = l + ((r - l) // 2)  # (l + r) // 2 can lead to overflow\n            if nums[m] > target:\n                r = m - 1\n            elif nums[m] < target:\n                l = m + 1\n            else:\n                return m\n        return -1\n"
  complexity:
    time: O(log n)
    space: O(1)
  followup:
  - ko: 배열이 내림차순으로 정렬되어 있다면 알고리즘을 어떻게 수정할까요?
    en: How would you modify the algorithm if the array were sorted in descending order?
  - ko: target보다 크거나 같은 가장 작은 요소의 인덱스를 찾으려면?
    en: How would you find the smallest element that is greater than or equal to the target?
  - ko: 중복된 요소가 있을 때, target의 가장 왼쪽 위치와 가장 오른쪽 위치를 찾으려면?
    en: How would you find the leftmost and rightmost positions of the target if duplicates exist?
```
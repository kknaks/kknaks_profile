---
created: '2026-06-07'
date: '2026-06-07'
day: Day 32
difficulty: medium
id: A-032
source:
  curated_in:
  - neetcode150
  number: 33
  platform: leetcode
  slug: search-in-rotated-sorted-array
  url: https://leetcode.com/problems/search-in-rotated-sorted-array/
tags:
- array
- binary-search
title:
  en: Search in Rotated Sorted Array
  ko: 회전된 정렬 배열에서 검색
today: false
type: algorithm
updated: '2026-06-07'
visible: true
---

# 회전된 정렬 배열에서 검색

## Data

```yaml
problem:
  title:
    ko: 회전된 정렬 배열에서 검색
    en: Search in Rotated Sorted Array
  statement:
    ko: '정수 배열 nums가 오름차순으로 정렬되어 있습니다 (모든 값이 서로 다릅니다).


      함수에 전달되기 전에, nums는 미지의 인덱스 k (1 <= k < nums.length)에서 왼쪽으로 회전된 상태일 수 있습니다. 회전된 배열은 [nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]] 형태입니다 (0-인덱싱). 예를 들어, [0,1,2,4,5,6,7]을 3만큼 왼쪽으로 회전하면 [4,5,6,7,0,1,2]가 됩니다.


      회전된 후의 배열 nums와 정수 target이 주어질 때, target이 nums에 있으면 그 인덱스를, 없으면 -1을 반환하세요.


      O(log n) 시간 복잡도로 작동하는 알고리즘을 작성해야 합니다.'
    en: 'There is an integer array nums sorted in ascending order (with distinct values).


      Prior to being passed to your function, nums is possibly left rotated at an unknown index k (1 <= k < nums.length) such that the resulting array is [nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]] (0-indexed). For example, [0,1,2,4,5,6,7] might be left rotated by 3 indices and become [4,5,6,7,0,1,2].


      Given the array nums after the possible rotation and an integer target, return the index of target if it is in nums, or -1 if it is not in nums.


      You must write an algorithm with O(log n) runtime complexity.'
  constraints:
  - 1 ≤ nums.length ≤ 5000
  - -10⁴ ≤ nums[i] ≤ 10⁴
  - All values in nums are unique
  - nums is an ascending array that is possibly rotated
  - -10⁴ ≤ target ≤ 10⁴
  io:
  - input: '[4,5,6,7,0,1,2]

      0'
    output: '4'
  - input: '[4,5,6,7,0,1,2]

      3'
    output: '-1'
  - input: '[1]

      0'
    output: '-1'
clarifying:
  items:
  - q:
      ko: 배열이 '회전될 가능성'이 있다는 것이 무엇을 의미하나요?
      en: What does it mean that the array is 'possibly rotated'?
    type: good
    why:
      ko: 배열이 회전되지 않을 수도 있습니다 (k=0). 알고리즘은 이 경우도 처리해야 합니다.
      en: The array might not be rotated at all. The algorithm must handle the unrotated case (k=0).
  - q:
      ko: 회전된 배열에서 이진 탐색이 어떻게 작동하나요?
      en: How does binary search work on a rotated array despite the rotation?
    type: good
    why:
      ko: 회전점을 기준으로 배열의 양쪽 부분이 각각 정렬되어 있습니다. 이를 이용하여 검색 공간을 반으로 줄일 수 있습니다.
      en: Both halves of the array (split by mid) remain partially sorted. We can identify the sorted half and eliminate half the search space.
  - q:
      ko: 중점을 기준으로 배열의 어느 쪽이 정렬되어 있는지 어떻게 판단하나요?
      en: How do we determine which half of the array (left or right of mid) is sorted?
    type: good
    why:
      ko: 왼쪽 끝과 중점을 비교하여 왼쪽이 정렬되었는지 판단합니다. 왼쪽이 정렬되지 않았으면 오른쪽이 반드시 정렬되어 있습니다.
      en: 'Compare the left boundary with mid: if nums[l] ≤ nums[mid], the left half is sorted. Otherwise, the right half must be sorted.'
  - q:
      ko: 정렬된 부분을 파악한 후 다음 단계는 무엇인가요?
      en: Once we identify which half is sorted, what should we do next?
    type: good
    why:
      ko: 타겟이 정렬된 부분의 범위 내에 있는지 확인합니다. 범위 내에 있으면 그쪽으로 탐색하고, 없으면 반대쪽을 탐색합니다.
      en: Check if the target lies within the range of the sorted half. If yes, search that half; otherwise search the other half.
  - q:
      ko: 배열이 반드시 회전되어 있다고 보장되나요?
      en: Is the array guaranteed to be rotated?
    type: distractor
    why:
      ko: 문제에서 '회전될 가능성'이라고 했으므로 회전되지 않은 경우도 있습니다.
      en: The problem says 'possibly rotated', so there may be unrotated arrays (k could be 0).
  - q:
      ko: 배열 크기가 작으므로 선형 탐색을 사용해도 되나요?
      en: Since the array has at most 5000 elements, can we just use linear search?
    type: distractor
    why:
      ko: 문제에서 명시적으로 O(log n) 시간 복잡도를 요구합니다. 선형 탐색은 요구사항을 만족하지 않습니다.
      en: The problem explicitly requires O(log n) complexity. Linear search would violate this constraint.
  - q:
      ko: 배열에 중복된 값이 있을 수 있나요?
      en: Can the array contain duplicate values?
    type: distractor
    why:
      ko: 문제에서 모든 값이 서로 다르다고 명시했습니다. 따라서 중복을 고려할 필요가 없습니다.
      en: The problem guarantees that all values are unique, so duplicates are not a concern.
approach:
  items:
  - name:
      ko: 회전 인식형 이진 탐색
      en: Binary search with rotation awareness
    complexity: O(log n) time / O(1) space
    type: good
    why:
      ko: 각 단계에서 정렬된 부분을 파악하고 검색 공간을 절반으로 줄입니다. 로그 시간 복잡도를 달성합니다.
      en: Identify the sorted half at each step and eliminate half the search space, achieving logarithmic time complexity.
  - name:
      ko: '두 단계 접근: 회전점 찾기 후 이진 탐색'
      en: 'Two-phase approach: find pivot, then binary search'
    complexity: O(log n) time / O(1) space
    type: good
    why:
      ko: 먼저 O(log n)에 회전점을 찾은 후 표준 이진 탐색을 수행합니다. 개념적으로는 명확하지만 속도는 동일합니다.
      en: First find the rotation point in O(log n), then use standard binary search. Conceptually cleaner but same complexity.
  - name:
      ko: 선형 탐색
      en: Linear search
    complexity: O(n) time / O(1) space
    type: distractor
    why:
      ko: O(log n) 요구사항을 위반하고 배열이 정렬되어 있다는 정보를 낭비합니다.
      en: Violates the O(log n) requirement and ignores the sorted structure of the array.
  - name:
      ko: 배열 복원 후 이진 탐색
      en: Unrotate array, then binary search
    complexity: O(n) time / O(1) space
    type: distractor
    why:
      ko: 배열을 원래 상태로 복원하는 데 O(n) 작업이 필요하므로 이진 탐색의 이점을 잃습니다.
      en: Restoring the array requires O(n) work, negating the benefit of binary search.
logic:
  format: slot
  slots:
  - label:
      ko: 포인터 초기화
      en: Initialize pointers
    indent: 0
    options:
    - code: l, r = 0, len(nums) - 1
      type: good
      why:
        ko: 왼쪽과 오른쪽 포인터를 배열의 양 끝에 설정하여 전체 배열을 검색 범위로 시작합니다.
        en: Set left and right pointers at the array boundaries to start searching the entire array.
    - code: l, r = 0, len(nums)
      type: distractor
      why:
        ko: 오른쪽 포인터가 배열 범위를 벗어납니다.
        en: Right pointer goes beyond array bounds.
    - code: l, r = 1, len(nums) - 1
      type: distractor
      why:
        ko: 첫 번째 요소를 제외하여 검색 공간을 불필요하게 줄입니다.
        en: Unnecessarily excludes the first element from the search space.
  - label:
      ko: 이진 탐색 루프
      en: Binary search loop
    indent: 0
    options:
    - code: 'while l <= r:'
      type: good
      why:
        ko: 포인터가 교차할 때까지 계속 반복합니다. l <= r 조건은 단일 요소 케이스도 포함합니다.
        en: Continue while pointers haven't crossed. The l <= r condition includes the single-element case.
    - code: 'while l < r:'
      type: distractor
      why:
        ko: l == r인 경우 마지막 요소를 확인하지 않아 타겟을 놓칠 수 있습니다.
        en: Fails to check the last element when l == r, potentially missing the target.
    - code: 'while l < len(nums) and r >= 0:'
      type: distractor
      why:
        ko: 포인터 교차 조건을 제대로 확인하지 않습니다.
        en: Doesn't properly check if pointers have crossed.
  - label:
      ko: 중점 계산
      en: Calculate midpoint
    indent: 1
    options:
    - code: mid = (l + r) // 2
      type: good
      why:
        ko: 중점을 정수 나눗셈으로 계산합니다. 이는 음수 값에서도 안전합니다.
        en: Calculate the midpoint using integer division. This is safe for negative values.
    - code: mid = (l + r) / 2
      type: distractor
      why:
        ko: 실수 나눗셈은 배열 인덱스로 사용할 수 없습니다.
        en: Float division cannot be used as an array index.
    - code: mid = r - (r - l) // 2
      type: distractor
      why:
        ko: 중점을 오른쪽으로 편향되게 계산합니다.
        en: Biases the midpoint towards the right.
  - label:
      ko: 타겟 발견 확인
      en: Check if target found
    indent: 1
    options:
    - code: 'if target == nums[mid]:'
      type: good
      why:
        ko: 중점의 값이 타겟과 같으면 즉시 인덱스를 반환합니다.
        en: If the middle element equals the target, immediately return its index.
    - code: 'if target < nums[mid]:'
      type: distractor
      why:
        ko: 잘못된 비교 연산자로 인해 타겟을 찾아도 반환하지 않습니다.
        en: Wrong comparison operator; won't return even when target is found.
    - code: 'if target >= nums[mid]:'
      type: distractor
      why:
        ko: 타겟 일치 조건을 잘못 이해하여 부정확한 결과를 낼 수 있습니다.
        en: Misinterprets the target match condition and may return incorrect results.
  - label:
      ko: 정렬된 부분 판단
      en: Determine sorted portion
    indent: 1
    options:
    - code: 'if nums[l] <= nums[mid]:'
      type: good
      why:
        ko: 왼쪽 끝이 중점 이하이면 왼쪽이 정렬되어 있습니다. 그렇지 않으면 오른쪽이 정렬되어 있습니다.
        en: If the left boundary is ≤ mid, the left half is sorted. Otherwise, the right half is sorted.
    - code: 'if nums[mid] <= nums[r]:'
      type: distractor
      why:
        ko: 반대쪽 (오른쪽)의 정렬 여부를 확인하므로 이후 로직이 반대가 됩니다.
        en: Checks the opposite half (right instead of left), reversing subsequent logic.
    - code: 'if nums[l] > nums[mid]:'
      type: distractor
      why:
        ko: 조건을 반대로 설정하여 검색 방향이 뒤바뀝니다.
        en: Reverses the condition, causing incorrect search direction.
  - label:
      ko: 검색 범위 조정
      en: Adjust search range
    indent: 2
    options:
    - code: 'if target > nums[mid] or target < nums[l]:'
      type: good
      why:
        ko: 왼쪽이 정렬되었을 때, 타겟이 정렬된 범위 내에 없으면 오른쪽 절반을 검색합니다.
        en: When left is sorted, if target is outside the sorted range [nums[l], nums[mid]], search the right half.
    - code: 'if target > nums[mid] or target > nums[l]:'
      type: distractor
      why:
        ko: 두 번째 조건이 잘못되어 검색 범위를 잘못 설정합니다.
        en: Second condition is wrong; sets incorrect search range.
    - code: 'if target < nums[mid] or target < nums[l]:'
      type: distractor
      why:
        ko: 첫 번째 조건이 잘못되어 검색 방향을 반대로 설정합니다.
        en: First condition is wrong; reverses the search direction.
  - label:
      ko: 검색 실패 반환
      en: Return not found
    indent: 0
    options:
    - code: return -1
      type: good
      why:
        ko: 루프가 끝나면 타겟을 찾지 못한 것이므로 -1을 반환합니다.
        en: If the loop completes without finding the target, return -1 to indicate absence.
    - code: return 0
      type: distractor
      why:
        ko: 잘못된 반환값입니다. 찾지 못했을 때는 -1을 반환해야 합니다.
        en: Wrong return value; should return -1 when target is not found.
    - code: return None
      type: distractor
      why:
        ko: 타입이 맞지 않습니다. 함수는 정수를 반환해야 합니다.
        en: Wrong type; the function must return an integer, not None.
trace:
  code:
  - 'class Solution:'
  - '    def search(self, nums: List[int], target: int) -> int:'
  - '        l, r = 0, len(nums) - 1'
  - ''
  - '        while l <= r:'
  - '            mid = (l + r) // 2'
  - '            if target == nums[mid]:'
  - '                return mid'
  - ''
  - '            # left sorted portion'
  - '            if nums[l] <= nums[mid]:'
  - '                if target > nums[mid] or target < nums[l]:'
  - '                    l = mid + 1'
  - '                else:'
  - '                    r = mid - 1'
  - '            # right sorted portion'
  - '            else:'
  - '                if target < nums[mid] or target > nums[r]:'
  - '                    r = mid - 1'
  - '                else:'
  - '                    l = mid + 1'
  - '        return -1'
  cases:
  - input: '[4,5,6,7,0,1,2]

      0'
    expected: '4'
  - input: '[4,5,6,7,0,1,2]

      3'
    expected: '-1'
  - input: '[1]

      0'
    expected: '-1'
  worked_example:
    input: '[4,5,6,7,0,1,2]

      0'
    steps:
    - ko: '초기화: l=0, r=6. 중점 mid=3, nums[3]=7. 타겟 0과 불일치.'
      en: 'Initialize: l=0, r=6. Calculate mid=3, nums[3]=7. Target 0 not found.'
    - ko: '왼쪽 [4,7]이 정렬됨. 타겟 0이 범위 [4,7] 밖이므로 우측 탐색: l=4.'
      en: 'Left portion [4,7] is sorted. Target 0 is outside range, so search right: l=4.'
    - ko: l=4, r=6. 중점 mid=5, nums[5]=1. 타겟과 불일치.
      en: l=4, r=6. Calculate mid=5, nums[5]=1. Target not found.
    - ko: '왼쪽 [0,1]이 정렬됨. 타겟 0이 범위 [0,1] 내에 있으므로 좌측 탐색: r=4.'
      en: 'Left portion [0,1] is sorted. Target 0 is in range, so search left: r=4.'
    - ko: l=4, r=4. 중점 mid=4, nums[4]=0. 타겟과 일치! 인덱스 4 반환.
      en: l=4, r=4. Calculate mid=4, nums[4]=0. Matches target! Return 4.
    answer: '4'
solution:
  code: "class Solution:\n    def search(self, nums: List[int], target: int) -> int:\n        l, r = 0, len(nums) - 1\n\n        while l <= r:\n            mid = (l + r) // 2\n            if target == nums[mid]:\n                return mid\n\n            # left sorted portion\n            if nums[l] <= nums[mid]:\n                if target > nums[mid] or target < nums[l]:\n                    l = mid + 1\n                else:\n                    r = mid - 1\n            # right sorted portion\n            else:\n                if target < nums[mid] or target > nums[r]:\n                    r = mid - 1\n                else:\n                    l = mid + 1\n        return -1\n"
  complexity:
    time: O(log n)
    space: O(1)
  followup:
  - ko: 만약 배열의 요소들이 중복된다면 어떻게 처리할까요?
    en: How would you handle this problem if the array could contain duplicate values?
  - ko: 주어진 시간에 최대 몇 개의 배열을 검색할 수 있습니까?
    en: What is the maximum number of rotated arrays you could search in a given time limit?
  - ko: 배열이 오른쪽으로 회전된 경우에도 같은 알고리즘을 적용할 수 있나요?
    en: Can the same algorithm be applied if the array were right-rotated instead of left-rotated?
```
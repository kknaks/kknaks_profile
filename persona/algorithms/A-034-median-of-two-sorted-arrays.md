---
created: '2026-06-09'
date: '2026-06-09'
day: Day 34
difficulty: hard
id: A-034
source:
  curated_in:
  - neetcode150
  number: 4
  platform: leetcode
  slug: median-of-two-sorted-arrays
  url: https://leetcode.com/problems/median-of-two-sorted-arrays/
status: draft
tags:
- array
- binary-search
- divide-and-conquer
title:
  en: Median of Two Sorted Arrays
  ko: 두 정렬 배열의 중앙값
today: true
type: algorithm
updated: '2026-06-09'
visible: true
---

# 두 정렬 배열의 중앙값

## Data

```yaml
problem:
  title:
    ko: 두 정렬 배열의 중앙값
    en: Median of Two Sorted Arrays
  statement:
    ko: '크기가 각각 m과 n인 두 개의 정렬된 배열 nums1과 nums2가 주어질 때, 두 배열의 중앙값을 반환하세요.


      전체 실행 시간 복잡도는 O(log (m+n))이어야 합니다.'
    en: 'Given two sorted arrays nums1 and nums2 of size m and n respectively, return the median of the two sorted arrays.


      The overall run time complexity should be O(log (m+n)).'
  constraints:
  - 0 ≤ m ≤ 1000, 0 ≤ n ≤ 1000
  - 1 ≤ m + n ≤ 2000
  - -10^6 ≤ nums1[i], nums2[i] ≤ 10^6
  io:
  - input: '[1,3]

      [2]'
    output: '2.00000'
  - input: '[1,2]

      [3,4]'
    output: '2.50000'
clarifying:
  items:
  - q:
      ko: 중앙값(median)은 정확히 무엇을 의미하나요?
      en: What exactly is the median?
    type: good
    why:
      ko: 중앙값은 정렬된 데이터의 중간 값입니다. 요소 개수가 홀수면 중간 요소, 짝수면 중간 두 요소의 평균입니다.
      en: The median is the middle value of sorted data. For odd-length data, it's the middle element; for even-length, it's the average of the two middle elements.
  - q:
      ko: 배열 중 하나 또는 둘 다 비어있을 수 있나요?
      en: Can one or both arrays be empty?
    type: good
    why:
      ko: 제약 조건에서 m + n ≥ 1이므로 항상 최소 한 개의 요소가 있습니다. 하지만 개별 배열은 비어있을 수 있습니다.
      en: According to constraints, m + n ≥ 1, so there's always at least one element total. However, either individual array can be empty.
  - q:
      ko: 왜 시간 복잡도가 O(log(m+n))이어야 하나요?
      en: Why must the time complexity be O(log(m+n))?
    type: good
    why:
      ko: 이것은 문제의 핵심 제약 조건으로, 단순히 두 배열을 합치고 정렬하는 것은 불가능하며 이진 탐색을 사용해야 함을 의미합니다.
      en: This is the core constraint of the problem, which means we cannot simply merge and sort the arrays; we must use binary search.
  - q:
      ko: 배열이 음수를 포함할 수 있나요?
      en: Can the arrays contain negative numbers?
    type: distractor
    why:
      ko: 네, 제약 조건에서 -10^6 이상의 값이 허용되므로 음수가 포함될 수 있습니다. 하지만 이는 중앙값 계산에 영향을 주지 않습니다.
      en: Yes, negative numbers are allowed per constraints (-10^6 ≤ nums[i] ≤ 10^6). However, this doesn't affect the median calculation logic.
  - q:
      ko: 중복된 값이 있을 수 있나요?
      en: Can there be duplicate values?
    type: good
    why:
      ko: 네, 배열 내에 중복 값이 있을 수 있으며, 이는 중앙값 계산을 정상적으로 처리합니다.
      en: Yes, duplicate values are allowed and the median calculation handles them correctly.
  - q:
      ko: 중앙값이 항상 정수인가요?
      en: Is the median always an integer?
    type: distractor
    why:
      ko: 아니요. 요소 개수가 짝수일 때는 중간 두 요소의 평균이 정수가 아닐 수 있습니다. 예를 들어 [1,2,3,4]의 중앙값은 2.5입니다.
      en: No. When the total count is even, the average of the two middle elements can be a non-integer. For example, [1,2,3,4] has median 2.5.
  - q:
      ko: 두 배열을 항상 그대로 사용해야 하나요?
      en: Must we use the arrays in their original order?
    type: distractor
    why:
      ko: 아니요. 효율성을 위해 더 작은 배열에 이진 탐색을 수행하도록 배열을 재할당할 수 있습니다.
      en: No. For efficiency, we can reassign the arrays so we binary search on the smaller one.
approach:
  items:
  - name:
      ko: 무차별 대입 - 합치고 정렬
      en: Brute Force - Merge and Sort
    complexity: O(m + n) time / O(m + n) space
    type: distractor
    why:
      ko: 두 배열을 합쳐서 정렬한 후 중간값을 찾으면 작동하지만, O(log(m+n))의 시간 복잡도 요구사항을 만족하지 않습니다.
      en: Merging both arrays and finding the median works, but violates the O(log(m+n)) time complexity requirement.
  - name:
      ko: 투 포인터 - 선형 탐색
      en: Two Pointers - Linear Scan
    complexity: O(m + n) time / O(1) space
    type: distractor
    why:
      ko: 두 포인터로 중앙값까지만 진행하면 O(1) 공간으로 가능하지만, 여전히 O(m + n) 시간이 필요하므로 요구사항을 만족하지 않습니다.
      en: Using two pointers to advance only to the median achieves O(1) space, but still requires O(m + n) time.
  - name:
      ko: 이진 탐색 - 분할점 찾기
      en: Binary Search - Find Partition
    complexity: O(log(min(m, n))) time / O(1) space
    type: good
    why:
      ko: 더 작은 배열에서 이진 탐색으로 올바른 분할점을 찾으면, O(log(m+n)) 시간 복잡도를 달성하면서 O(1) 공간만 사용합니다.
      en: Binary search on the smaller array to find the correct partition achieves O(log(m+n)) time with O(1) space.
  - name:
      ko: 이진 탐색 - 통합 배열에서
      en: Binary Search - On Merged Virtual Array
    complexity: O(log(m + n)) time / O(1) space
    type: distractor
    why:
      ko: 이론상 가능하지만 구현하기 더 복잡하고, 더 작은 배열에서의 이진 탐색만큼 직관적이지 않습니다.
      en: Theoretically possible but more complex to implement and less intuitive than partitioning the smaller array.
logic:
  format: slot
  slots:
  - label:
      ko: 총 길이와 목표 위치 계산
      en: Calculate total length and target position
    indent: 0
    options:
    - code: total = len(nums1) + len(nums2)
      type: good
      why:
        ko: 합쳐진 배열에서 왼쪽에 있어야 할 요소의 개수를 계산합니다. 이는 올바른 분할점을 결정하는 데 필수적입니다.
        en: Calculate total length to determine how many elements should be on the left side of the partition.
    - code: total = len(nums1) + len(nums2) + 1
      type: distractor
      why:
        ko: off-by-one 오류로, 분할점을 잘못 계산합니다.
        en: Off-by-one error that miscalculates the partition point.
    - code: total = max(len(nums1), len(nums2))
      type: distractor
      why:
        ko: 더 긴 배열의 길이만 사용하여 중앙값을 잘못 계산합니다.
        en: Uses only the longer array's length, giving incorrect total.
  - label:
      ko: 더 작은 배열 선택
      en: Ensure A is the smaller array
    indent: 0
    options:
    - code: 'if len(B) < len(A):'
      type: good
      why:
        ko: 더 작은 배열에 이진 탐색을 수행하면 반복 횟수가 최소화되어 효율성이 높아집니다.
        en: Binary searching the smaller array minimizes iterations and improves efficiency.
    - code: 'if len(A) < len(B): A, B = B, A'
      type: distractor
      why:
        ko: 조건을 반대로 하여 더 큰 배열에 이진 탐색을 수행하게 됩니다.
        en: Reversed condition causes binary search on the larger array.
    - code: A, B = B, A
      type: distractor
      why:
        ko: 항상 스왑하면 입력이 이미 최적화된 경우에 비효율적입니다.
        en: Always swapping is inefficient if input is already optimized.
  - label:
      ko: 이진 탐색 범위 초기화
      en: Initialize binary search bounds
    indent: 0
    options:
    - code: l, r = 0, len(A) - 1
      type: good
      why:
        ko: 더 작은 배열 A의 전체 범위를 검색 범위로 설정하여 이진 탐색을 시작합니다.
        en: Set the search range to the entire smaller array A for binary search.
    - code: l, r = 0, len(B) - 1
      type: distractor
      why:
        ko: 잘못된 배열 B에서 이진 탐색을 시도합니다.
        en: Searches on the wrong array B instead of A.
    - code: l, r = 0, half
      type: distractor
      why:
        ko: 배열 크기를 무시하고 잘못된 범위를 설정합니다.
        en: Sets an incorrect range ignoring array bounds.
  - label:
      ko: 배열 B의 분할점 계산
      en: Calculate partition index in B
    indent: 1
    options:
    - code: 'j = half - i - 2  # B'
      type: good
      why:
        ko: j는 배열 B에서 분할점의 왼쪽에 있어야 할 요소의 개수입니다. 공식 half - i - 2는 두 배열의 분할을 유지합니다.
        en: j represents how many elements from B should be left of the partition. The formula maintains balance between the arrays.
    - code: j = half - i - 1
      type: distractor
      why:
        ko: off-by-one 오류로 분할점이 정확하지 않습니다.
        en: Off-by-one error makes the partition incorrect.
    - code: j = half - i
      type: distractor
      why:
        ko: 공식이 잘못되어 A와 B 사이의 분할이 유효하지 않습니다.
        en: Incorrect formula breaks the partition balance.
  - label:
      ko: 분할점의 경계값 추출
      en: Extract boundary values at partition
    indent: 1
    options:
    - code: Aleft = A[i] if i >= 0 else float("-infinity")
      type: good
      why:
        ko: 배열 A에서 분할점의 왼쪽 끝값을 가져옵니다. 범위 밖이면 음의 무한대를 사용하여 비교를 간단히 합니다.
        en: Get the rightmost element on the left of partition in A. Use -infinity for out-of-bounds to simplify comparisons.
    - code: Aleft = A[i] if i >= 0 else float('infinity')
      type: distractor
      why:
        ko: 무한대 부호를 반대로 하면 부등식 비교가 실패합니다.
        en: Wrong infinity sign breaks comparison logic.
    - code: Aleft = A[i - 1] if i > 0 else float('-infinity')
      type: distractor
      why:
        ko: 인덱스가 잘못되어 다른 요소를 비교하게 됩니다.
        en: Wrong index accesses the wrong element.
  - label:
      ko: 분할의 유효성 검증
      en: Validate partition correctness
    indent: 1
    options:
    - code: 'if Aleft <= Bright and Bleft <= Aright:'
      type: good
      why:
        ko: 두 조건을 모두 만족해야 분할이 올바릅니다. AND 연산자로 두 조건을 모두 확인합니다.
        en: Both conditions must hold for a valid partition. Both must pass (AND), not just one (OR).
    - code: 'if Aleft <= Bright or Bleft <= Aright:'
      type: distractor
      why:
        ko: OR 연산자를 사용하면 잘못된 분할도 통과할 수 있습니다.
        en: Using OR instead of AND accepts invalid partitions.
    - code: 'if Aleft < Bright and Bleft < Aright:'
      type: distractor
      why:
        ko: 부등호를 <= 에서 < 로 바꾸면 경계값이 같은 경우를 놓칩니다.
        en: Strict inequality misses cases where boundary values are equal.
  - label:
      ko: 이진 탐색 범위 조정
      en: Adjust binary search range
    indent: 1
    options:
    - code: 'elif Aleft > Bright:'
      type: good
      why:
        ko: 분할이 유효하지 않으면, A의 왼쪽 끝값이 B의 오른쪽 끝값보다 크면 A의 오른쪽 범위를 줄여야 합니다.
        en: If Aleft is too large, narrow the search range to the left half of A.
    - code: 'elif Aleft < Bright: r = i - 1'
      type: distractor
      why:
        ko: 부등호 방향을 반대로 하면 검색 범위가 잘못된 방향으로 조정됩니다.
        en: Reversed comparison adjusts range in the wrong direction.
    - code: 'elif Aleft > Bright: l = i + 1'
      type: distractor
      why:
        ko: 조건과 동작이 맞지 않아 잘못된 범위 조정이 발생합니다.
        en: Mismatched condition and action adjust in the wrong direction.
trace:
  code:
  - '# Time: log(min(n, m))'
  - ''
  - ''
  - 'class Solution:'
  - '    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:'
  - '        A, B = nums1, nums2'
  - '        total = len(nums1) + len(nums2)'
  - '        half = total // 2'
  - ''
  - '        if len(B) < len(A):'
  - '            A, B = B, A'
  - ''
  - '        l, r = 0, len(A) - 1'
  - '        while True:'
  - '            i = (l + r) // 2  # A'
  - '            j = half - i - 2  # B'
  - ''
  - '            Aleft = A[i] if i >= 0 else float("-infinity")'
  - '            Aright = A[i + 1] if (i + 1) < len(A) else float("infinity")'
  - '            Bleft = B[j] if j >= 0 else float("-infinity")'
  - '            Bright = B[j + 1] if (j + 1) < len(B) else float("infinity")'
  - ''
  - '            # partition is correct'
  - '            if Aleft <= Bright and Bleft <= Aright:'
  - '                # odd'
  - '                if total % 2:'
  - '                    return min(Aright, Bright)'
  - '                # even'
  - '                return (max(Aleft, Bleft) + min(Aright, Bright)) / 2'
  - '            elif Aleft > Bright:'
  - '                r = i - 1'
  - '            else:'
  - '                l = i + 1'
  cases:
  - input: '[1,3]

      [2]'
    expected: '2.00000'
  - input: '[1,2]

      [3,4]'
    expected: '2.50000'
  worked_example:
    input: '[1,3]

      [2]'
    steps:
    - ko: '초기 설정: nums1=[1,3], nums2=[2]. total=3, half=1'
      en: 'Initialize: nums1=[1,3], nums2=[2]. total=3, half=1'
    - ko: 'len(B)=1 < len(A)=2이므로 스왑: A=[2], B=[1,3]'
      en: 'len(B) < len(A), so swap: A=[2], B=[1,3]'
    - ko: '첫 번째 반복 (l=0, r=0): i=0, j=-1. Aleft=2, Aright=∞, Bleft=-∞, Bright=1. 조건 실패 (2≤1 거짓), r=-1로 설정'
      en: 'First iteration (l=0, r=0): i=0, j=-1. Aleft=2, Aright=∞, Bleft=-∞, Bright=1. Invalid (2>1), set r=-1'
    - ko: '두 번째 반복 (l=0, r=-1): i=-1, j=0. Aleft=-∞, Aright=2, Bleft=1, Bright=∞. 조건 만족! (−∞≤∞ ✓, 1≤2 ✓)'
      en: 'Second iteration (l=0, r=-1): i=-1, j=0. Aleft=-∞, Aright=2, Bleft=1, Bright=∞. Valid! Both conditions pass.'
    - ko: total=3 (홀수)이므로 min(Aright, Bright) = min(2, ∞) = 2.0 반환
      en: total=3 is odd, return min(Aright, Bright) = min(2, ∞) = 2.0
    answer: '2.0'
solution:
  code: "# Time: log(min(n, m))\n\n\nclass Solution:\n    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:\n        A, B = nums1, nums2\n        total = len(nums1) + len(nums2)\n        half = total // 2\n\n        if len(B) < len(A):\n            A, B = B, A\n\n        l, r = 0, len(A) - 1\n        while True:\n            i = (l + r) // 2  # A\n            j = half - i - 2  # B\n\n            Aleft = A[i] if i >= 0 else float(\"-infinity\")\n            Aright = A[i + 1] if (i + 1) < len(A) else float(\"infinity\")\n            Bleft = B[j] if j >= 0 else float(\"-infinity\")\n            Bright = B[j + 1] if (j + 1) < len(B) else float(\"infinity\")\n\n            # partition is correct\n            if Aleft <= Bright and Bleft <= Aright:\n                # odd\n                if total % 2:\n                    return min(Aright, Bright)\n                # even\n                return (max(Aleft, Bleft) + min(Aright, Bright)) / 2\n            elif Aleft\
    \ > Bright:\n                r = i - 1\n            else:\n                l = i + 1\n"
  complexity:
    time: O(log(min(m, n)))
    space: O(1)
  followup:
  - ko: 한 배열이 다른 배열보다 훨씬 크면 시간 복잡도는 어떻게 변하나요?
    en: How does time complexity behave if one array is much larger than the other?
  - ko: 배열이 정수 대신 부동소수점 수를 포함할 수 있다면 코드가 어떻게 변경될까요?
    en: How would the code change if arrays could contain floating-point numbers?
  - ko: O(log(m+n)) 제약이 없다면 더 간단한 접근법을 사용할 수 있나요?
    en: Without the O(log(m+n)) constraint, could you implement a simpler solution?
```
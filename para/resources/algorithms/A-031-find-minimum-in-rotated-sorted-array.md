---
created: '2026-06-06'
date: '2026-06-06'
day: Day 31
difficulty: medium
id: A-031
source:
  curated_in:
  - neetcode150
  number: 153
  platform: leetcode
  slug: find-minimum-in-rotated-sorted-array
  url: https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/
tags:
- array
- binary-search
title:
  en: Find Minimum in Rotated Sorted Array
  ko: 회전된 정렬 배열에서 최솟값 찾기
today: false
type: algorithm
updated: '2026-06-06'
visible: true
---

# 회전된 정렬 배열에서 최솟값 찾기

## Data

```yaml
problem:
  title:
    ko: 회전된 정렬 배열에서 최솟값 찾기
    en: Find Minimum in Rotated Sorted Array
  statement:
    ko: '길이 n인 오름차순 정렬 배열이 1번에서 n번 사이로 회전되었다고 하자. 예를 들어, 배열 [0,1,2,4,5,6,7]은 4번 회전되면 [4,5,6,7,0,1,2]가 된다.


      배열 [a[0], a[1], a[2], ..., a[n-1]]을 1번 회전하면 [a[n-1], a[0], a[1], a[2], ..., a[n-2]]가 된다.


      고유한 원소들로 이루어진 정렬되고 회전된 배열 nums가 주어졌을 때, 이 배열의 최솟값을 구하시오.


      O(log n) 시간 복잡도의 알고리즘을 작성해야 한다.'
    en: 'Suppose an array of length n sorted in ascending order is rotated between 1 and n times. For example, the array nums = [0,1,2,4,5,6,7] might become [4,5,6,7,0,1,2] if it was rotated 4 times.


      Notice that rotating an array [a[0], a[1], a[2], ..., a[n-1]] 1 time results in the array [a[n-1], a[0], a[1], a[2], ..., a[n-2]].


      Given the sorted rotated array nums of unique elements, return the minimum element of this array.


      You must write an algorithm that runs in O(log n) time.'
  constraints:
  - 1 ≤ n ≤ 5000
  - -5000 ≤ nums[i] ≤ 5000
  - All elements are unique
  - Array is sorted and rotated between 1 and n times
  io:
  - input: '[3,4,5,1,2]'
    output: '1'
  - input: '[4,5,6,7,0,1,2]'
    output: '0'
  - input: '[11,13,15,17]'
    output: '11'
clarifying:
  items:
  - q:
      ko: 최솟값 그 자체를 반환해야 하나요, 아니면 그 인덱스를 반환해야 하나요?
      en: Should we return the minimum value itself or its index?
    type: good
    why:
      ko: 문제에서는 명확히 최솟값을 반환하도록 요구하고 있습니다.
      en: The problem statement explicitly asks for the minimum value, not the index.
  - q:
      ko: '배열이 회전되지 않은 경우(예: [11,13,15,17])도 처리해야 하나요?'
      en: Do we need to handle the case where the array is not rotated (e.g., [11,13,15,17])?
    type: good
    why:
      ko: 문제에서 "1번에서 n번 사이로 회전"이라고 명시했으므로, n번 회전(완전 회전)도 포함됩니다.
      en: The problem states 1 to n rotations, where n rotations means effectively no rotation.
  - q:
      ko: 배열에 중복된 원소가 있을 수 있나요?
      en: Can the array contain duplicate elements?
    type: good
    why:
      ko: 이 문제에서는 명시적으로 모든 원소가 고유하다고 명시되어 있습니다.
      en: The constraint explicitly states all integers are unique.
  - q:
      ko: 파이썬의 내장 min() 함수를 사용하면 안 되나요?
      en: Why can't we just use Python's built-in min() function?
    type: distractor
    why:
      ko: 내장 min()은 O(n) 시간이 걸리므로 O(log n) 요구사항을 만족하지 못합니다.
      en: Built-in min() takes O(n) time, which doesn't satisfy the O(log n) requirement.
  - q:
      ko: 선형 탐색으로도 O(log n) 성능을 얻을 수 있나요?
      en: Can we achieve O(log n) with linear scanning?
    type: distractor
    why:
      ko: 선형 탐색은 최소 O(n) 시간이 필요하므로 O(log n)을 달성할 수 없습니다.
      en: Linear scan inherently requires O(n) time and cannot achieve O(log n).
  - q:
      ko: 배열을 두 부분으로 나누면, 항상 한 쪽은 정렬되어 있나요?
      en: In a rotated sorted array, is one half always fully sorted?
    type: good
    why:
      ko: 네, 회전된 정렬 배열을 중간에서 나누면 항상 한쪽은 완전히 정렬된 상태입니다.
      en: Yes, one half of the midpoint split is always sorted, which we can exploit.
approach:
  items:
  - name:
      ko: 이진 탐색
      en: Binary Search
    complexity: O(log n) time / O(1) space
    type: good
    why:
      ko: 배열을 반으로 나누어 최솟값이 있는 쪽을 판단하여 탐색 범위를 절반으로 줄입니다.
      en: Divide the array in half, determine which side contains the minimum, and discard the other half.
  - name:
      ko: 선형 탐색
      en: Linear Scan
    complexity: O(n) time / O(1) space
    type: distractor
    why:
      ko: 배열의 모든 원소를 확인하므로 O(log n) 요구사항을 만족하지 못합니다.
      en: Checking all elements exceeds the O(log n) time constraint.
  - name:
      ko: 내장 min() 함수
      en: Built-in min() Function
    complexity: O(n) time / O(1) space
    type: distractor
    why:
      ko: 내장 함수도 내부적으로 모든 원소를 확인하므로 O(log n) 요구사항을 만족하지 못합니다.
      en: Built-in functions scan all elements internally, not achieving O(log n).
logic:
  format: slot
  slots:
  - label:
      ko: 탐색 범위와 최솟값 초기화
      en: Initialize search boundaries and minimum tracker
    indent: 0
    options:
    - code: 'start , end = 0, len(nums) - 1 '
      type: good
      why:
        ko: 이진 탐색을 위해 양쪽 포인터를 배열의 양 끝에 설정하고, 최솟값을 추적하기 위해 무한대로 초기화합니다.
        en: Set left and right pointers to array bounds and initialize minimum to infinity.
    - code: start, end = 1, len(nums) - 2
      type: distractor
      why:
        ko: 경계 인덱스를 제외하면 배열의 양 끝 원소를 놓칠 수 있습니다.
        en: Excluding boundaries skips potential minimum values at array edges.
    - code: start, end = 0, len(nums)
      type: distractor
      why:
        ko: end 포인터가 배열 범위를 초과하여 인덱스 오류가 발생합니다.
        en: End index exceeds array bounds, causing an index out of range error.
  - label:
      ko: 이진 탐색 루프
      en: Binary search loop condition
    indent: 0
    options:
    - code: 'while start  <  end :'
      type: good
      why:
        ko: start < end 조건으로 유효한 탐색 범위가 남아있는 동안만 반복합니다.
        en: Loop continues while there is a search space (start is before end).
    - code: 'while start <= end:'
      type: distractor
      why:
        ko: start == end일 때도 반복하여 불필요한 중복 계산이 발생합니다.
        en: Processing when start equals end causes redundant operations.
    - code: 'while start < end - 1:'
      type: distractor
      why:
        ko: 마지막 두 원소를 제대로 확인하지 않아 최솟값을 놓칠 수 있습니다.
        en: Skipping the last elements may miss the minimum value.
  - label:
      ko: 중간값 계산 및 최솟값 업데이트
      en: Calculate midpoint and track minimum
    indent: 1
    options:
    - code: mid = start + (end - start ) // 2
      type: good
      why:
        ko: 오버플로우 없이 중간점을 계산한 후, 현재까지 본 모든 값 중 최솟값을 유지합니다.
        en: Calculate midpoint using safe arithmetic, then track the smallest value found.
    - code: mid = (start + end) // 2
      type: distractor
      why:
        ko: start와 end가 매우 클 때 두 수의 합에서 오버플로우가 발생할 수 있습니다.
        en: Direct sum can overflow with large index values.
    - code: 'mid = start + (end - start) // 2

        curr_min = nums[mid]'
      type: distractor
      why:
        ko: 현재 mid 값만 저장하여 이전 반복에서 본 더 작은 값을 버립니다.
        en: Only stores current mid, losing smaller values from previous iterations.
  - label:
      ko: 탐색 방향 결정
      en: Determine which half contains minimum
    indent: 1
    options:
    - code: 'if nums[mid] > nums[end]:'
      type: good
      why:
        ko: nums[mid] > nums[end]이면 최솟값은 회전점 이후 오른쪽에 있으므로 왼쪽 경계를 올립니다.
        en: If mid value > end value, the minimum must be to the right; search right half.
    - code: 'if nums[mid] > nums[start]:'
      type: distractor
      why:
        ko: start와 비교하면 회전점을 기준으로 올바른 방향을 결정할 수 없습니다.
        en: Comparing with start doesn't correctly identify which half has the minimum.
    - code: 'if nums[mid] < nums[end]:'
      type: distractor
      why:
        ko: 조건이 반대라서 탐색 방향이 뒤바뀌어 최솟값을 찾지 못합니다.
        en: Reversed condition leads to searching the wrong half.
  - label:
      ko: 왼쪽 경계 이동
      en: Move left boundary forward
    indent: 2
    options:
    - code: start = mid + 1
      type: good
      why:
        ko: 최솟값이 mid의 오른쪽에 있으므로, mid를 포함한 왼쪽 부분은 제외하고 start를 mid+1로 옮깁니다.
        en: Since minimum is to the right, skip left half including mid.
    - code: start = mid
      type: distractor
      why:
        ko: mid로만 이동하면 두 원소 배열에서 무한 루프에 빠질 수 있습니다.
        en: Moving to mid (not mid+1) can cause infinite loop on 2-element arrays.
    - code: start = mid - 1
      type: distractor
      why:
        ko: mid 이전으로 이동하면 최솟값이 있는 오른쪽 방향과 반대로 갑니다.
        en: Moving backwards goes opposite to where minimum is located.
  - label:
      ko: 오른쪽 경계 이동
      en: Move right boundary backward
    indent: 2
    options:
    - code: 'end = mid - 1 '
      type: good
      why:
        ko: 최솟값이 mid의 왼쪽(또는 mid 자체)에 있으므로, mid보다 오른쪽은 제외하고 end를 mid-1로 옮깁니다.
        en: Since minimum is at mid or to the left, exclude right half and move end backward.
    - code: end = mid
      type: distractor
      why:
        ko: mid로만 이동하면 최솟값을 확인한 후에도 반복이 계속되어 비효율적입니다.
        en: Stopping at mid can cause unnecessary iterations even after finding minimum.
    - code: end = mid + 1
      type: distractor
      why:
        ko: mid 이후로 이동하면 최솟값이 있는 왼쪽 방향과 반대로 갑니다.
        en: Moving forward goes opposite direction where minimum is.
  - label:
      ko: 최종 최솟값 반환
      en: Return final minimum value
    indent: 0
    options:
    - code: return min(curr_min,nums[start])
      type: good
      why:
        ko: 루프를 벗어난 후 반복 중에 추적한 curr_min과 마지막 위치 nums[start] 중 더 작은 값을 반환합니다.
        en: Return the minimum of the tracked value and the final position, ensuring accuracy.
    - code: return curr_min
      type: distractor
      why:
        ko: 루프 종료 후 nums[start]를 확인하지 않아 최솟값을 놓칠 수 있습니다.
        en: Skipping the final check of nums[start] may miss the actual minimum.
    - code: return nums[start]
      type: distractor
      why:
        ko: 루프 중간에 본 더 작은 값들을 무시하고 마지막 위치의 값만 반환합니다.
        en: Ignoring the tracked minimum loses smaller values found during search.
trace:
  code:
  - 'class Solution:'
  - '    def findMin(self, nums: List[int]) -> int:'
  - '        start , end = 0, len(nums) - 1 '
  - '        curr_min = float("inf")'
  - '        '
  - '        while start  <  end :'
  - '            mid = start + (end - start ) // 2'
  - '            curr_min = min(curr_min,nums[mid])'
  - '            '
  - '            # right has the min '
  - '            if nums[mid] > nums[end]:'
  - '                start = mid + 1'
  - '                '
  - '            # left has the  min '
  - '            else:'
  - '                end = mid - 1 '
  - '                '
  - '        return min(curr_min,nums[start])'
  cases:
  - input: '[3,4,5,1,2]'
    expected: '1'
  - input: '[4,5,6,7,0,1,2]'
    expected: '0'
  - input: '[11,13,15,17]'
    expected: '11'
  worked_example:
    input: '[3,4,5,1,2]'
    steps:
    - ko: '초기 상태: start=0, end=4, curr_min=∞, nums=[3,4,5,1,2]'
      en: 'Initialize: start=0, end=4, curr_min=∞, nums=[3,4,5,1,2]'
    - ko: '반복 1: mid=2, nums[2]=5, curr_min=5. 5 > nums[4]=2이므로 최솟값이 오른쪽에 있음 → start=3'
      en: 'Iteration 1: mid=2, nums[2]=5, curr_min=5. Since 5 > 2, minimum is right → start=3'
    - ko: '반복 2: mid=3, nums[3]=1, curr_min=1. 1 > nums[4]=2가 거짓이므로 최솟값이 왼쪽에 있음 → end=2'
      en: 'Iteration 2: mid=3, nums[3]=1, curr_min=1. Since 1 ≤ 2, minimum is left → end=2'
    - ko: '루프 종료: start=3, end=2 (3 < 2는 거짓). 반환 값 = min(1, nums[3]) = min(1, 1) = 1'
      en: 'Loop exits: start=3, end=2. Return min(1, nums[3]) = min(1, 1) = 1'
    answer: '1'
solution:
  code: "class Solution:\n    def findMin(self, nums: List[int]) -> int:\n        start , end = 0, len(nums) - 1 \n        curr_min = float(\"inf\")\n        \n        while start  <  end :\n            mid = start + (end - start ) // 2\n            curr_min = min(curr_min,nums[mid])\n            \n            # right has the min \n            if nums[mid] > nums[end]:\n                start = mid + 1\n                \n            # left has the  min \n            else:\n                end = mid - 1 \n                \n        return min(curr_min,nums[start])\n"
  complexity:
    time: O(log n)
    space: O(1)
  followup:
  - ko: '배열에 중복된 원소가 있다면 시간 복잡도는 어떻게 되나요? (예: [3,1,3] 또는 [1,3,1,1,1])'
    en: What happens if the array has duplicate elements? How does time complexity change?
  - ko: '회전되지 않은 배열(예: [1,2,3,4,5])을 어떻게 감지하고 처리할 수 있나요?'
    en: How can you detect and optimize for a non-rotated (fully sorted) array?
  - ko: 시작점(첫 원소)과 끝점(마지막 원소)을 비교하여 회전 여부를 먼저 확인하는 것이 도움될까요?
    en: Would comparing first and last elements to detect rotation early improve efficiency?
```
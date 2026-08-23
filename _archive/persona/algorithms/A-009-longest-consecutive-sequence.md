---
created: '2026-05-11'
date: '2026-05-11'
day: Day 09
difficulty: medium
id: A-009
source:
  curated_in:
  - neetcode150
  number: 128
  platform: leetcode
  slug: longest-consecutive-sequence
  url: https://leetcode.com/problems/longest-consecutive-sequence/
status: draft
tags:
- array
- hash-table
- union-find
title:
  en: Longest Consecutive Sequence
  ko: 최장 연속 수열
today: false
type: algorithm
updated: '2026-05-11'
visible: true
---

# 최장 연속 수열

## Data

```yaml
problem:
  title:
    ko: 최장 연속 수열
    en: Longest Consecutive Sequence
  statement:
    ko: 정렬되지 않은 정수 배열 nums가 주어질 때, 연속된 정수들로 이루어진 최장 수열의 길이를 반환하세요. O(n) 시간에 실행되는 알고리즘을 작성해야 합니다.
    en: Given an unsorted array of integers nums, return the length of the longest consecutive elements sequence. You must write an algorithm that runs in O(n) time.
  constraints:
  - 0 ≤ nums.length ≤ 10⁵
  - -10⁹ ≤ nums[i] ≤ 10⁹
  - 배열에는 중복된 원소가 포함될 수 있음 / Array may contain duplicate elements
  io:
  - input: '[100,4,200,1,3,2]'
    output: '4'
  - input: '[0,3,7,2,5,8,4,6,0,1]'
    output: '9'
  - input: '[1,0,1,2]'
    output: '3'
clarifying:
  items:
  - q:
      ko: 연속 수열에서 각 원소는 정확히 몇씩 차이가 나야 하나요?
      en: What is the difference between consecutive elements in the sequence?
    type: good
    why:
      ko: 연속 수열은 각 원소가 정확히 1씩 차이나야 함을 명확히 해야 문제를 올바르게 풀 수 있습니다.
      en: Understanding that consecutive means a difference of exactly 1 between adjacent elements is fundamental to solving this problem correctly.
  - q:
      ko: 수열이 배열 내에서 연속된 위치에 있어야 하나요?
      en: Must the sequence appear in consecutive positions within the array?
    type: good
    why:
      ko: 아니요. 우리는 배열의 값만으로 수열을 찾으므로, 배열 내 위치는 상관없습니다.
      en: No—we only care about the values themselves, not their positions in the input array. For example, [100, 4, 1, 2, 3] contains the sequence [1, 2, 3, 4].
  - q:
      ko: 배열에 중복된 숫자가 있으면 어떻게 처리해야 하나요?
      en: How should duplicate numbers in the array be handled?
    type: good
    why:
      ko: Set으로 변환하면 자동으로 중복이 제거되어, 각 고유한 숫자를 한 번씩만 고려하게 됩니다.
      en: Converting to a set automatically removes duplicates, ensuring each unique number is considered only once in the analysis.
  - q:
      ko: 배열을 정렬하면 쉽게 풀 수 있는데, 왜 O(n) 제약이 있나요?
      en: Why is the O(n) time constraint necessary if sorting would be simpler?
    type: distractor
    why:
      ko: 정렬은 O(n log n) 시간이 필요하므로 문제의 O(n) 요구사항을 만족하지 못합니다. 문제 자체가 O(n) 알고리즘 발견을 목표로 하고 있습니다.
      en: Sorting takes O(n log n) time, which violates the O(n) requirement. The problem is specifically designed to test whether you can find a linear-time algorithm.
  - q:
      ko: 해시 집합(set)을 사용하지 않고도 O(n) 시간에 풀 수 있나요?
      en: Can you solve this in O(n) time without using a hash set?
    type: distractor
    why:
      ko: 일반적으로는 어렵습니다. 해시 집합은 O(1) 조회를 제공하므로 이 문제의 O(n) 해결책에 필수적입니다.
      en: In general, no. A hash set provides O(1) lookups, which is essential for achieving the O(n) solution without sorting.
approach:
  items:
  - name:
      ko: 해시 집합 + 스마트 반복
      en: Hash Set + Smart Iteration
    complexity: O(n) time / O(n) space
    type: good
    why:
      ko: '각 숫자를 최대 두 번만 방문합니다: 외부 루프에서 한 번, 내부 while 루프에서 한 번. 수열의 시작점에서만 확장하므로 불필요한 작업을 피합니다.'
      en: 'Each number is visited at most twice: once in the outer loop and once in the while loop. By only extending sequences from their starting points, we avoid redundant work.'
  - name:
      ko: 정렬 + 선형 스캔
      en: Sorting + Linear Scan
    complexity: O(n log n) time / O(1) space
    type: distractor
    why:
      ko: 정렬 단계가 O(n log n)이므로 O(n) 요구사항을 위반합니다.
      en: The sorting step takes O(n log n) time, violating the problem's O(n) time constraint.
  - name:
      ko: 완전 탐색
      en: Brute Force
    complexity: O(n²) time / O(1) space
    type: distractor
    why:
      ko: 각 숫자에서 가능한 모든 수열을 확인하면 O(n²) 시간이 소요되어 비효율적입니다.
      en: Checking all possible sequences from each number results in O(n²) time, making it too slow for the required O(n) solution.
  - name:
      ko: Union-Find
      en: Union-Find (Disjoint Set Union)
    complexity: O(n α(n)) time / O(n) space
    type: distractor
    why:
      ko: 이론적으로 가능하지만 더 복잡하고, 해시 집합 접근 방식이 더 직관적이고 구현하기 쉽습니다.
      en: While theoretically viable, it's more complex and less intuitive than the hash set approach, making it impractical for this problem.
logic:
  format: slot
  slots:
  - label:
      ko: 배열을 집합으로 변환
      en: Convert array to set
    indent: 0
    options:
    - code: numSet = set(nums)
      type: good
      why:
        ko: 중복을 제거하고 O(1) 조회를 가능하게 합니다.
        en: Removes duplicates and enables O(1) lookups for the sequence validation.
    - code: numSet = sorted(nums)
      type: distractor
      why:
        ko: 정렬은 O(n log n)이므로 O(n) 요구사항을 위반합니다.
        en: Sorting violates the O(n) time requirement.
    - code: 'numSet = {n: True for n in nums}'
      type: distractor
      why:
        ko: 딕셔너리는 작동하지만 set이 더 효율적이고 의도를 명확하게 표현합니다.
        en: A dictionary works but set is more efficient and expresses intent more clearly.
  - label:
      ko: 최장 수열 길이 초기화
      en: Initialize longest sequence length
    indent: 0
    options:
    - code: longest = 0
      type: good
      why:
        ko: 0에서 시작하여 발견된 모든 수열과 비교할 기준값을 설정합니다.
        en: Starting at 0 provides a baseline to compare against all discovered sequences.
    - code: longest = 1
      type: distractor
      why:
        ko: 배열이 비어있을 수 있으므로 최소 길이는 0이어야 합니다.
        en: Empty arrays should return 0, not 1.
    - code: longest = float('-inf')
      type: distractor
      why:
        ko: 작동하지만 불필요하게 복잡하며 0을 초기값으로 사용하는 것이 더 자연스럽습니다.
        en: Works but unnecessarily complex; 0 is the natural starting point.
  - label:
      ko: 집합의 각 숫자 반복
      en: Iterate through each number in the set
    indent: 0
    options:
    - code: 'for n in numSet:'
      type: good
      why:
        ko: 모든 고유한 숫자를 확인하여 수열의 시작점을 찾습니다.
        en: Examines every unique number to identify potential sequence starting points.
    - code: 'for n in nums:'
      type: distractor
      why:
        ko: 중복된 숫자를 여러 번 처리하여 불필요한 작업을 반복합니다.
        en: Processes duplicate numbers multiple times, causing unnecessary redundant work.
    - code: 'for i in range(len(numSet)):'
      type: distractor
      why:
        ko: Set에 인덱싱이 없어서 인덱스 기반 반복은 작동하지 않습니다.
        en: Sets are unordered and don't support index-based iteration.
  - label:
      ko: 수열 시작점 확인
      en: Check if number is sequence start
    indent: 1
    options:
    - code: 'if (n - 1) not in numSet:'
      type: good
      why:
        ko: n-1이 없으면 n이 수열의 첫 번째 원소입니다. 이렇게 하면 각 수열을 한 번씩만 확장하므로 O(n) 시간을 보장합니다.
        en: If (n-1) is not in the set, n is the start of a sequence. This ensures we only expand each sequence once, guaranteeing O(n) time.
    - code: 'if (n + 1) not in numSet:'
      type: distractor
      why:
        ko: 수열의 끝을 확인하므로 중복 확장이 발생합니다.
        en: Checks for sequence end, causing duplicate expansions.
    - code: 'if n not in visited:'
      type: distractor
      why:
        ko: visited 집합이 정의되지 않았으므로 작동하지 않습니다.
        en: A visited set is not defined, so this would cause a NameError.
  - label:
      ko: 수열 길이 초기화 및 확장
      en: Initialize and extend sequence length
    indent: 2
    options:
    - code: length = 1
      type: good
      why:
        ko: 시작점 n 자신을 길이 1로 계산한 후, while 루프에서 1씩 증가시키며 연속된 숫자들을 세어갑니다.
        en: Counts the starting point itself (length = 1), then increments to count consecutive following numbers.
    - code: length = 0
      type: distractor
      why:
        ko: 시작점 n을 세지 않으므로 결과가 1씩 적게 나옵니다.
        en: Fails to count the starting point n itself.
    - code: length = len([x for x in numSet if x >= n])
      type: distractor
      why:
        ko: 연속성을 확인하지 않고 n 이상의 모든 숫자를 세므로 잘못된 결과를 줍니다.
        en: Counts all numbers ≥ n without checking consecutiveness.
  - label:
      ko: 연속된 숫자 세기
      en: Count consecutive numbers
    indent: 2
    options:
    - code: 'while (n + length) in numSet:'
      type: good
      why:
        ko: n, n+1, n+2, ... 가 집합에 존재하는 동안 계속 세어갑니다.
        en: Continues counting as long as n, n+1, n+2, ... exist in the set.
    - code: 'while (n + length) in numSet and length < 100:'
      type: distractor
      why:
        ko: 임의의 제한이 정확성을 해칠 수 있습니다.
        en: An arbitrary limit can produce incorrect results.
    - code: 'while (n - length) in numSet:'
      type: distractor
      why:
        ko: 역방향을 확인하므로 논리가 뒤바뀝니다.
        en: Checks backwards, reversing the intended logic.
  - label:
      ko: 최대값 업데이트
      en: Update maximum
    indent: 2
    options:
    - code: longest = max(length, longest)
      type: good
      why:
        ko: 각 수열의 길이를 비교하여 지금까지 발견한 최장 수열을 추적합니다.
        en: Tracks the longest sequence found so far by comparing lengths.
    - code: longest = length
      type: distractor
      why:
        ko: 이전 최대값을 고려하지 않아 마지막 수열만 반환합니다.
        en: Always overwrites with the current sequence, potentially discarding longer ones.
    - code: longest += length
      type: distractor
      why:
        ko: 누적합을 계산하므로 완전히 잘못된 결과를 줍니다.
        en: Accumulates lengths instead of tracking the maximum.
trace:
  code:
  - 'class Solution:'
  - '    def longestConsecutive(self, nums: List[int]) -> int:'
  - '        numSet = set(nums)'
  - '        longest = 0'
  - ''
  - '        for n in numSet:'
  - '            # check if its the start of a sequence'
  - '            if (n - 1) not in numSet:'
  - '                length = 1'
  - '                while (n + length) in numSet:'
  - '                    length += 1'
  - '                longest = max(length, longest)'
  - '        return longest'
  cases:
  - input: '[100,4,200,1,3,2]'
    expected: '4'
  - input: '[0,3,7,2,5,8,4,6,0,1]'
    expected: '9'
  - input: '[1,0,1,2]'
    expected: '3'
  worked_example:
    input: '[100,4,200,1,3,2]'
    steps:
    - ko: numSet = {100, 4, 200, 1, 3, 2}로 변환. longest = 0.
      en: Convert to numSet = {100, 4, 200, 1, 3, 2}. Initialize longest = 0.
    - ko: 'n=100: 99가 없으므로 시작점. 101도 없으므로 길이=1. longest=1. n=4: 3이 있으므로 건너뜀.'
      en: 'n=100: Start of sequence (99 not in set). No 101, so length=1, longest=1. n=4: Skip (3 exists).'
    - ko: 'n=200: 199가 없으므로 시작점. 201도 없으므로 길이=1. longest=1. n=1: 0이 없으므로 시작점.'
      en: 'n=200: Start (199 not in set). No 201, length=1, longest=1. n=1: Start (0 not in set).'
    - ko: 'n=1에서 길이 확장: 2 있음→3, 3 있음→4, 4 있음→5, 5 없음→중지. 길이=4. longest=4.'
      en: 'From n=1: 2 exists→3, 3 exists→4, 4 exists→5, 5 missing→stop. length=4, longest=4.'
    answer: '4'
solution:
  code: "class Solution:\n    def longestConsecutive(self, nums: List[int]) -> int:\n        numSet = set(nums)\n        longest = 0\n\n        for n in numSet:\n            # check if its the start of a sequence\n            if (n - 1) not in numSet:\n                length = 1\n                while (n + length) in numSet:\n                    length += 1\n                longest = max(length, longest)\n        return longest\n"
  complexity:
    time: O(n)
    space: O(n)
  followup:
  - ko: Union-Find를 사용하여 이 문제를 풀 수 있을까요? 복잡도는 어떻게 될까요?
    en: Could you solve this using Union-Find? What would the time complexity be?
  - ko: 배열이 이미 정렬되어 있다면, O(n) 시간과 O(1) 공간으로 풀 수 있을까요?
    en: If the array were already sorted, could you solve it in O(n) time with O(1) space?
  - ko: 이 알고리즘의 핵심 통찰력은 무엇인가요? 왜 수열의 시작점에서만 확장하는 것이 중요할까요?
    en: What is the key insight of this algorithm? Why is it important to only expand from sequence starting points?
```
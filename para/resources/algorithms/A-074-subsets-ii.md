---
created: '2026-07-30'
date: '2026-07-30'
day: Day 74
difficulty: medium
id: A-074
source:
  curated_in:
  - neetcode150
  number: 90
  platform: leetcode
  slug: subsets-ii
  url: https://leetcode.com/problems/subsets-ii/
tags:
- array
- backtracking
- bit-manipulation
title:
  en: Subsets II
  ko: 부분집합 II
today: false
type: algorithm
updated: '2026-07-30'
visible: true
---

# 부분집합 II

## Data

```yaml
problem:
  title:
    ko: 부분집합 II
    en: Subsets II
  statement:
    ko: '중복을 포함할 수 있는 정수 배열 nums가 주어질 때, 모든 가능한 부분집합(멱집합)을 반환하세요.


      해 집합에는 중복된 부분집합이 포함되어서는 안 됩니다. 답을 어떤 순서로든 반환할 수 있습니다.'
    en: 'Given an integer array nums that may contain duplicates, return all possible subsets (the power set).


      The solution set must not contain duplicate subsets. Return the solution in any order.'
  constraints:
  - 1 ≤ nums.length ≤ 10
  - -10 ≤ nums[i] ≤ 10
  io:
  - input: '[1,2,2]'
    output: '[[],[1],[1,2],[1,2,2],[2],[2,2]]'
  - input: '[0]'
    output: '[[],[0]]'
clarifying:
  items:
  - q:
      ko: 배열의 중복된 원소는 결과에서도 중복된 부분집합을 만들어야 하나요?
      en: Should duplicate elements in the input create duplicate subsets in the output?
    type: good
    why:
      ko: 아니요. 이것이 문제의 핵심입니다. 정렬 후 중복 원소를 건너뛰는 전략이 필요합니다.
      en: No. This is the core constraint requiring a strategy to skip duplicates after sorting.
  - q:
      ko: 결과 부분집합의 순서가 정해져 있나요?
      en: Does the order of subsets in the output matter?
    type: good
    why:
      ko: 문제에서 '어떤 순서로든' 반환할 수 있다고 명시합니다.
      en: The problem explicitly states 'Return the solution in any order.'
  - q:
      ko: 모든 원소가 같은 경우([1,1,1])에는 몇 개의 부분집합이 반환되나요?
      en: If all elements are identical (e.g., [1,1,1]), how many unique subsets exist?
    type: good
    why:
      ko: '[[], [1], [1,1], [1,1,1]] 총 4개입니다. 배열 크기와 다른 결과를 이해하는 것이 중요합니다.'
      en: '4 subsets: [[], [1], [1,1], [1,1,1]]. Recognizing that duplicates reduce subset count is key.'
  - q:
      ko: 입력 배열을 수정해도 되나요?
      en: Can we modify the input array?
    type: good
    why:
      ko: 네, 정렬을 위해 입력을 수정하는 것이 일반적으로 허용됩니다.
      en: Yes, modifying the input for sorting is typically acceptable in interviews.
  - q:
      ko: 공집합도 결과에 포함되어야 하나요?
      en: Should the empty subset be included in the output?
    type: good
    why:
      ko: 네, 멱집합의 정의상 공집합은 항상 포함됩니다.
      en: Yes, by definition of power set, the empty subset is always included.
  - q:
      ko: 백트래킹 대신 반복적 방법으로 구현할 수 있나요?
      en: Can we solve this iteratively instead of recursively?
    type: good
    why:
      ko: 네, 반복적으로도 가능합니다. 각 반복에서 기존 부분집합들에 새 원소를 추가하면 됩니다.
      en: Yes, iterative approaches work too by incrementally adding new elements to existing subsets.
  - q:
      ko: 결과의 부분집합들이 각각 정렬되어야 하나요?
      en: Must elements within each subset be sorted?
    type: distractor
    why:
      ko: 문제에서 요구하지 않습니다. 예시에서는 그렇게 나타나지만 이는 요구사항이 아닙니다.
      en: Not required. Examples show sorted subsets, but this is a side effect of the algorithm, not a requirement.
  - q:
      ko: 최대 2^n개의 부분집합 때문에 특별한 최적화가 필요한가요?
      en: Do we need special optimizations because there can be at most 2^n subsets?
    type: distractor
    why:
      ko: 제약 조건 (nums.length ≤ 10)에서 최대 1024개 부분집합이므로, 추가 최적화는 불필요합니다.
      en: With nums.length ≤ 10, at most 1024 subsets—no special optimizations needed.
approach:
  items:
  - name:
      ko: 정렬 + 백트래킹 (중복 건너뛰기)
      en: Sorting + Backtracking (skip duplicates)
    complexity: O(2^n) time / O(n) space (excluding output)
    type: good
    why:
      ko: 입력을 정렬한 후, 원소를 제외할 때 모든 중복 원소를 건너뜁니다. 중복 부분집합을 원천적으로 방지합니다.
      en: Sort input, then when excluding an element, skip all its duplicates at once. Prevents duplicate subsets at the source.
  - name:
      ko: 반복적 구축 (Iterative build)
      en: Iterative Build
    complexity: O(2^n) time / O(2^n) space (for output)
    type: good
    why:
      ko: 정렬 후, 기존 부분집합들에 새 원소를 차례로 추가하여 새로운 부분집합을 만듭니다.
      en: After sorting, iteratively add new elements to existing subsets to build new ones step-by-step.
  - name:
      ko: 비트 마스크 생성 후 중복 제거
      en: Bit Manipulation + Dedup
    complexity: O(2^n * n) time / O(2^n * n) space
    type: distractor
    why:
      ko: 모든 2^n개 조합을 생성한 후 해시셋으로 중복을 제거해야 하므로 비효율적입니다.
      en: Generates all 2^n combinations then deduplicates using a set, requiring O(n) space per subset.
  - name:
      ko: 해시맵으로 결과 추적
      en: HashMap tracking
    complexity: O(2^n * n) time / O(2^n * n) space
    type: distractor
    why:
      ko: 모든 부분집합을 생성한 후 해시 함수로 중복을 체크하는 것은 불필요하게 복잡합니다.
      en: Checking each subset with hashing is unnecessary compared to preventing duplicates upfront via sorting.
logic:
  format: slot
  slots:
  - label:
      ko: 결과 리스트 초기화
      en: Initialize result list
    indent: 0
    options:
    - code: res = []
      type: good
      why:
        ko: 모든 부분집합을 저장할 빈 리스트를 생성합니다.
        en: Create an empty list to store all subsets.
    - code: res = set()
      type: distractor
      why:
        ko: 집합은 중복을 자동으로 제거하지만, 리스트 형태의 부분집합을 해시 가능한 형태로 변환해야 합니다.
        en: Sets auto-deduplicate, but lists aren't hashable—would need to convert subsets to tuples.
    - code: result = {}
      type: distractor
      why:
        ko: 딕셔너리는 부분집합 데이터를 저장하기에 적합한 구조가 아닙니다.
        en: Dictionaries need key-value pairs, which doesn't match our subset storage needs.
  - label:
      ko: 배열 정렬 (중복 원소를 인접하게)
      en: Sort array (group duplicates together)
    indent: 0
    options:
    - code: nums.sort()
      type: good
      why:
        ko: 정렬하면 중복된 원소들이 연속으로 배치되어, 같은 값의 모든 원소를 한 번에 건너뛸 수 있습니다.
        en: Sorting places duplicates adjacent, enabling us to skip all copies of an element at once.
    - code: nums = sorted(nums)
      type: distractor
      why:
        ko: sorted()를 사용하면 새 리스트를 만들고 nums를 재할당합니다. 동작하지만 nums.sort()가 더 직접적입니다.
        en: Works but creates a new list; in-place sort via .sort() is more direct for this use case.
    - code: '# 정렬 스킵'
      type: distractor
      why:
        ko: 정렬 없이는 중복 원소들이 흩어져 있어, 효율적인 중복 제거가 불가능하고 중복 부분집합이 생깁니다.
        en: Without sorting, duplicates are scattered; we can't efficiently skip them and duplicates appear in output.
  - label:
      ko: '기저 사례: 배열 끝에 도달'
      en: 'Base case: reached end'
    indent: 2
    options:
    - code: 'if i == len(nums):'
      type: good
      why:
        ko: 인덱스가 배열의 끝(len(nums))에 도달하면, 지금까지 구축한 부분집합이 완성되므로 결과에 추가합니다.
        en: When index reaches array length, the current subset is complete—add it to results.
    - code: 'if i >= len(nums):'
      type: distractor
      why:
        ko: i는 len(nums)를 초과할 수 없으므로 동작하지만, == 이 조건의 의도를 더 명확하게 표현합니다.
        en: Works but less clear; i should equal, not exceed, len(nums) in a well-formed recursion.
    - code: 'if len(subset) == len(nums):'
      type: distractor
      why:
        ko: 부분집합의 크기가 배열의 크기와 같은 경우만 기저사례로 처리하는데, 이는 크기가 작은 부분집합들을 놓칩니다.
        en: Only captures subsets equal to array size, missing smaller subsets like [1] and [].
  - label:
      ko: 현재 원소 포함 및 탐색
      en: Include current element and explore
    indent: 2
    options:
    - code: subset.append(nums[i])
      type: good
      why:
        ko: 현재 원소를 부분집합에 추가한 후, 다음 인덱스부터 백트래킹을 진행하여 현재 원소를 포함하는 모든 부분집합을 탐색합니다.
        en: Add current element to subset, recurse from next index to explore all subsets including it.
    - code: subset.append(nums[i]); backtrack(i, subset)
      type: distractor
      why:
        ko: 같은 인덱스 i로 재귀하면, 같은 원소를 계속 추가하여 무한 루프가 발생합니다.
        en: Recursing at the same index creates infinite recursion—same element added repeatedly.
    - code: subset.append(nums[i]); backtrack(i + 2, subset)
      type: distractor
      why:
        ko: i + 2로 건너뛰면, 일부 원소가 처리되지 않아 유효한 부분집합을 놓치게 됩니다.
        en: Skipping elements misses valid subsets.
  - label:
      ko: 원소 제외 시 중복 건너뛰기
      en: Skip duplicates when excluding
    indent: 2
    options:
    - code: 'while i + 1 < len(nums) and nums[i] == nums[i + 1]:'
      type: good
      why:
        ko: 현재 원소를 제외하는 경로를 탐색할 때, 같은 값의 모든 다음 원소들을 건너뜁니다. 이렇게 하면 같은 부분집합이 여러 번 생성되지 않습니다.
        en: When excluding an element, skip ALL consecutive duplicates. Prevents the same subset from being generated via different paths.
    - code: 'if nums[i] == nums[i + 1]: i += 1'
      type: distractor
      why:
        ko: if를 사용하면 하나의 중복만 건너뜁니다. 세 개 이상의 같은 원소가 있으면 남은 중복들을 처리하지 못합니다.
        en: Using 'if' skips only one duplicate; with three identical elements, one duplicate remains.
    - code: 'while nums[i] == nums[i + 1]: i += 1  # 범위 체크 없음'
      type: distractor
      why:
        ko: 범위 체크 (i + 1 < len(nums))가 없으면, 배열의 끝에서 인덱스 범위를 초과할 수 있습니다.
        en: Without bounds checking (i + 1 < len(nums)), causes index out of bounds at array end.
  - label:
      ko: 제외 경로에서 재귀
      en: Exclude and recurse from skip position
    indent: 2
    options:
    - code: backtrack(i + 1, subset)
      type: good
      why:
        ko: 현재 원소와 그 모든 중복을 건너뛴 후, 남은 배열로부터 탐색을 계속합니다.
        en: Recurse from after all duplicates, continuing the search from where duplicates ended.
    - code: backtrack(i, subset)
      type: distractor
      why:
        ko: 같은 i에서 재귀하면, 백트래킹 스택에서 제거되지 않은 원소를 다시 처리하게 됩니다.
        en: Would re-process the same element since it wasn't incremented.
    - code: backtrack(len(nums), subset)
      type: distractor
      why:
        ko: 배열의 끝으로 직접 이동하여, 남은 원소들의 조합을 모두 건너뜁니다.
        en: Jumps to end, skipping all remaining elements' combinations.
trace:
  code:
  - 'class Solution:'
  - '    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:'
  - '        res = []'
  - '        nums.sort()'
  - ''
  - '        def backtrack(i, subset):'
  - '            if i == len(nums):'
  - '                res.append(subset[::])'
  - '                return'
  - ''
  - '            # All subsets that include nums[i]'
  - '            subset.append(nums[i])'
  - '            backtrack(i + 1, subset)'
  - '            subset.pop()'
  - '            # All subsets that don''t include nums[i]'
  - '            while i + 1 < len(nums) and nums[i] == nums[i + 1]:'
  - '                i += 1'
  - '            backtrack(i + 1, subset)'
  - ''
  - '        backtrack(0, [])'
  - '        return res'
  cases:
  - input: '[1,2,2]'
    expected: '[[],[1],[1,2],[1,2,2],[2],[2,2]]'
  - input: '[0]'
    expected: '[[],[0]]'
  worked_example:
    input: '[1,2,2]'
    steps:
    - ko: '입력: [1,2,2] → 정렬 후: [1,2,2]'
      en: 'Input: [1,2,2] → after sort: [1,2,2]'
    - ko: 'backtrack(0, []): nums[0]=1 포함 → backtrack(1, [1]). 이 경로에서 1을 포함하는 모든 부분집합을 만듭니다.'
      en: 'backtrack(0, []): include 1 → recurse to backtrack(1, [1]). Build all subsets containing 1.'
    - ko: 'backtrack(1, [1]): 1) nums[1]=2 포함 → backtrack(2, [1,2]). 2) 1을 유지하고 2 제외하되, nums[2]=2도 건너뜀 → backtrack(3, [1]).'
      en: 'backtrack(1, [1]): include 2 → backtrack(2, [1,2]), exclude 2 and skip nums[2] → backtrack(3, [1]).'
    - ko: 'backtrack(2, [1,2]): nums[2]=2 포함하면 [1,2,2]을 만들고, 제외하면 [1,2]. 인덱스 3에 도달하여 백트래킹. 이후 [2], [2,2], []도 생성됨.'
      en: 'backtrack(2, [1,2]): include 2 → [1,2,2], exclude → [1,2]. Continue exploring remaining paths to generate [2], [2,2], [].'
    answer: '[[],[1],[1,2],[1,2,2],[2],[2,2]]'
solution:
  code: "class Solution:\n    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:\n        res = []\n        nums.sort()\n\n        def backtrack(i, subset):\n            if i == len(nums):\n                res.append(subset[::])\n                return\n\n            # All subsets that include nums[i]\n            subset.append(nums[i])\n            backtrack(i + 1, subset)\n            subset.pop()\n            # All subsets that don't include nums[i]\n            while i + 1 < len(nums) and nums[i] == nums[i + 1]:\n                i += 1\n            backtrack(i + 1, subset)\n\n        backtrack(0, [])\n        return res\n"
  complexity:
    time: O(2^n)
    space: O(n) for recursion depth (excluding output)
  followup:
  - ko: 반복적(iterative) 방법으로 이 문제를 풀 수 있나요? 이 경우 시간/공간 복잡도는 어떻게 되나요?
    en: Can you solve this iteratively instead of recursively? What would the time/space complexity be?
  - ko: 특정 크기 k의 부분집합만 반환하도록 수정하려면 코드를 어떻게 변경해야 할까요?
    en: How would you modify this to return only subsets of a specific size k?
  - ko: 부분집합의 합이 특정 목표값 이상인 경우만 반환하려면?
    en: How would you return only subsets whose sum exceeds a given target?
```
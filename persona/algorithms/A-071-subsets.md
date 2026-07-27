---
created: '2026-07-27'
date: '2026-07-27'
day: Day 71
difficulty: medium
id: A-071
source:
  curated_in:
  - neetcode150
  number: 78
  platform: leetcode
  slug: subsets
  url: https://leetcode.com/problems/subsets/
status: draft
tags:
- array
- backtracking
- bit-manipulation
title:
  en: Subsets
  ko: 부분집합
today: true
type: algorithm
updated: '2026-07-27'
visible: true
---

# 부분집합

## Data

```yaml
problem:
  title:
    ko: 부분집합
    en: Subsets
  statement:
    ko: '중복되지 않는 정수 배열 nums가 주어질 때, 모든 가능한 부분집합(멱집합)을 반환하세요.


      결과 집합에는 중복되는 부분집합이 포함되지 않아야 합니다. 결과는 어떤 순서로든 반환할 수 있습니다.'
    en: 'Given an integer array nums of unique elements, return all possible subsets (the power set).


      The solution set must not contain duplicate subsets. Return the solution in any order.'
  constraints:
  - 1 ≤ nums.length ≤ 10
  - -10 ≤ nums[i] ≤ 10
  - All elements in nums are unique
  io:
  - input: '[1,2,3]'
    output: '[[1,2,3],[1,2],[1,3],[1],[2,3],[2],[3],[]]'
  - input: '[0]'
    output: '[[0],[]]'
clarifying:
  items:
  - q:
      ko: 부분집합(subset)의 정의가 무엇인가요?
      en: What is the definition of a subset?
    type: good
    why:
      ko: 부분집합은 원본 배열에서 0개 이상의 원소를 포함하는 모든 가능한 조합입니다.
      en: A subset includes zero or more elements from the original array in any combination.
  - q:
      ko: 결과의 순서가 중요한가요?
      en: Does the order of subsets in the output matter?
    type: good
    why:
      ko: 문제에서 명시적으로 '어떤 순서로든 반환'할 수 있다고 했으므로, 부분집합들의 순서는 자유롭습니다.
      en: The problem explicitly states 'return the solution in any order', so the arrangement of subsets is flexible.
  - q:
      ko: 각 원소를 여러 번 사용할 수 있나요?
      en: Can we use each element multiple times in a single subset?
    type: good
    why:
      ko: 부분집합의 정의상 각 원소는 포함되거나 포함되지 않거나 둘 중 하나이며, 반복 사용은 불가능합니다.
      en: Each element in a subset is either included once or not at all; repetition is not allowed.
  - q:
      ko: 왜 subset.copy()를 사용하나요? append(subset)으로는 안 되나요?
      en: Why use subset.copy() instead of directly appending the list?
    type: good
    why:
      ko: Python 리스트는 참조 타입이므로, 같은 객체를 계속 추가하면 나중의 수정이 모든 저장된 결과에 영향을 줍니다.
      en: Lists in Python are references; appending the same object multiple times means all stored results point to the same changing list.
  - q:
      ko: 시간 복잡도는 얼마나 되나요?
      en: What is the time complexity of this solution?
    type: distractor
    why:
      ko: 2^n개의 부분집합이 존재하고, 각각을 복사하는 데 O(n)이 필요하므로 총 O(n·2^n)입니다.
      en: There are 2^n subsets to generate, and copying each takes O(n), resulting in O(n·2^n) total.
  - q:
      ko: 입력 배열의 원소들이 미리 정렬되어야 하나요?
      en: Must the input array be pre-sorted?
    type: distractor
    why:
      ko: 부분집합 생성에는 배열의 순서가 영향을 주지 않습니다. 문제에서 정렬을 요구하지 않습니다.
      en: The order of input elements does not affect subset generation. The problem does not require sorting.
  - q:
      ko: 중복된 원소가 입력에 포함될 수 있나요?
      en: Can the input contain duplicate elements?
    type: distractor
    why:
      ko: 문제에서 '모든 숫자는 고유합니다(unique)'라고 명시되어 있으므로, 중복은 없습니다.
      en: The problem explicitly states 'all the numbers of nums are unique', so duplicates are not a concern for this version.
approach:
  items:
  - name:
      ko: 백트래킹 재귀 (Backtracking DFS)
      en: Backtracking Recursion
    complexity: O(n·2^n) time / O(n) space
    type: good
    why:
      ko: 각 원소에 대해 포함과 제외의 두 선택을 재귀적으로 탐색하면서, 결정을 되돌리는 백트래킹을 사용합니다. 직관적이고 이해하기 쉬운 방식입니다.
      en: For each element, recursively explore both inclusion and exclusion branches, undoing choices via backtracking. This naturally expresses the problem structure.
  - name:
      ko: 비트 조작 (Bit Manipulation)
      en: Bit Manipulation
    complexity: O(n·2^n) time / O(1) space
    type: good
    why:
      ko: 0부터 2^n-1까지의 각 숫자의 비트 패턴을 이용하여, 어떤 원소를 포함할지 결정합니다.
      en: Iterate through all numbers from 0 to 2^n-1, using each bit position to determine whether to include the corresponding element.
  - name:
      ko: 반복적 빌드 (Iterative Build)
      en: Iterative Build-Up
    complexity: O(n·2^n) time / O(2^n) space
    type: distractor
    why:
      ko: 크기가 작은 부분집합부터 시작하여 각 새 원소를 추가하면서 확장하는 방식이지만, 코드가 더 복잡합니다.
      en: Start with small subsets and iteratively add elements, but this requires more careful indexing and is less intuitive.
  - name:
      ko: 조합 생성 (Combination Generation by Size)
      en: Combinations by Size
    complexity: O(n·2^n) time / O(n) space
    type: distractor
    why:
      ko: 크기별로 조합을 따로 생성하는 방식도 가능하지만, 일반적인 부분집합 문제로는 백트래킹이 더 간단합니다.
      en: While generating combinations of each size separately works, it requires more boilerplate than a general backtracking approach.
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
        ko: 생성된 모든 부분집합을 저장할 빈 리스트를 만듭니다.
        en: Create an empty list to store all generated subsets.
    - code: res = [[]]
      type: distractor
      why:
        ko: 공집합을 미리 추가하면, 나중에 재귀에서 다시 추가되어 중복이 발생합니다.
        en: Pre-adding the empty subset causes duplication when the recursion naturally produces it.
    - code: res = set()
      type: distractor
      why:
        ko: 집합(set)은 변경 가능한 리스트를 요소로 저장할 수 없으므로, 부분집합을 저장하는 데 적합하지 않습니다.
        en: Sets cannot contain lists as elements, so they cannot store subsets.
  - label:
      ko: 현재 부분집합 초기화
      en: Initialize current subset
    indent: 0
    options:
    - code: subset = []
      type: good
      why:
        ko: 재귀 과정에서 현재 구성 중인 부분집합을 추적하는 빈 리스트를 만듭니다.
        en: Create an empty list to track the subset being built during the recursion.
    - code: subset = nums[:]
      type: distractor
      why:
        ko: 전체 배열로 시작하면, 원소를 제외하는 로직이 복잡해지고 원하는 부분집합을 놓칠 수 있습니다.
        en: Starting with all elements makes the exclusion logic complicated and misses subsets.
    - code: subset = [nums[0]]
      type: distractor
      why:
        ko: 첫 원소를 미리 포함하면, 그 원소를 제외한 부분집합들을 생성할 수 없습니다.
        en: Starting with an element misses all subsets that exclude that element.
  - label:
      ko: 재귀 종료 조건 확인
      en: Check base case condition
    indent: 1
    options:
    - code: 'if i >= len(nums):'
      type: good
      why:
        ko: 모든 원소를 고려했을 때 (인덱스가 배열 길이 이상), 현재 부분집합이 완성되었으므로 결과에 추가합니다.
        en: When the index reaches or exceeds the array length, all include/exclude decisions are made for one complete subset.
    - code: 'if i == len(nums) - 1:'
      type: distractor
      why:
        ko: 마지막 원소의 인덱스에서만 종료하므로, 마지막 원소를 포함한 경로들을 처리하지 못합니다.
        en: Stopping one index too early misses paths that process the last element.
    - code: 'if i > len(nums):'
      type: distractor
      why:
        ko: 인덱스가 길이를 한 번 초과해야만 종료하므로, 정확한 경계를 놓칩니다.
        en: Requiring > instead of >= means the condition isn't caught at the right boundary.
  - label:
      ko: 완성된 부분집합 저장
      en: Add current subset to result
    indent: 2
    options:
    - code: res.append(subset.copy())
      type: good
      why:
        ko: subset.copy()로 현재 부분집합의 독립적인 복사본을 만들어 결과에 추가합니다. 이렇게 해야 나중의 수정이 이미 저장된 결과에 영향을 주지 않습니다.
        en: Use .copy() to add an independent copy so that later modifications to subset don't change stored results.
    - code: res.append(subset)
      type: distractor
      why:
        ko: 같은 객체 참조를 추가하므로, subset을 수정하면 모든 저장된 결과가 함께 변경됩니다.
        en: Without copy(), all results reference the same list; modifications affect all stored subsets.
    - code: res.append(tuple(subset))
      type: distractor
      why:
        ko: 튜플로 변환하면 작동하지만, 문제에서 리스트 형태로 반환하기를 기대하므로 복사가 더 직관적입니다.
        en: While tuple conversion works, the problem expects list results, so .copy() is more appropriate.
  - label:
      ko: 현재 원소 포함 및 재귀
      en: Include element and recurse
    indent: 1
    options:
    - code: subset.append(nums[i])
      type: good
      why:
        ko: 현재 원소를 부분집합에 추가한 후, 다음 원소를 고려하도록 재귀 호출합니다.
        en: Add the current element to the subset, then recurse to make decisions on remaining elements.
    - code: subset = subset + [nums[i]]
      type: distractor
      why:
        ko: 새로운 리스트를 생성하므로, 이후 백트래킹의 pop()이 작동하지 않습니다.
        en: This creates a new list instead of modifying the existing one, breaking the backtrack mechanism.
    - code: subset.insert(0, nums[i])
      type: distractor
      why:
        ko: 앞에 삽입하면 불필요한 시간 복잡도가 증가하며, append와 동일한 로직입니다.
        en: Inserting at the front is O(n) instead of O(1), and the position doesn't matter for subsets.
  - label:
      ko: 백트래킹으로 원소 제거
      en: 'Backtrack: remove element'
    indent: 1
    options:
    - code: subset.pop()
      type: good
      why:
        ko: 이전 단계의 포함 선택을 취소하기 위해 추가했던 원소를 제거합니다. 그 후 이 원소를 제외한 부분집합들을 탐색합니다.
        en: Remove the element to undo the include decision, then explore the branch where this element is excluded.
    - code: subset = subset[:-1]
      type: distractor
      why:
        ko: 슬라이싱으로 새로운 리스트를 생성하므로, 원본 subset 객체가 업데이트되지 않아 재귀 로직이 깨집니다.
        en: Slicing creates a new list instead of modifying the existing one, breaking the backtracking flow.
    - code: subset.remove(nums[i])
      type: distractor
      why:
        ko: remove()는 값으로 검색하므로, 배열에 동일한 값이 있으면 의도하지 않은 원소를 제거할 수 있습니다.
        en: remove() searches by value; if duplicates existed, it might remove the wrong element.
  - label:
      ko: 재귀 탐색 시작
      en: Start recursion
    indent: 0
    options:
    - code: dfs(0)
      type: good
      why:
        ko: 인덱스 0부터 시작하여 모든 원소에 대한 포함/제외 결정을 탐색합니다.
        en: Initiate the recursive exploration from index 0 to explore all possible combinations.
    - code: dfs(1)
      type: distractor
      why:
        ko: 인덱스 1부터 시작하면 첫 번째 원소(인덱스 0)를 건너뛰므로, 그것을 포함한 부분집합들을 생성할 수 없습니다.
        en: Starting from index 1 skips the first element, missing all subsets that include it.
    - code: dfs(len(nums) - 1)
      type: distractor
      why:
        ko: 마지막 인덱스부터 시작하면, 대부분의 원소를 고려하지 않게 됩니다.
        en: Starting from the last index only considers the last element, ignoring the rest.
trace:
  code:
  - 'class Solution:'
  - '    def subsets(self, nums: List[int]) -> List[List[int]]:'
  - '        res = []'
  - ''
  - '        subset = []'
  - ''
  - '        def dfs(i):'
  - '            if i >= len(nums):'
  - '                res.append(subset.copy())'
  - '                return'
  - '            # decision to include nums[i]'
  - '            subset.append(nums[i])'
  - '            dfs(i + 1)'
  - '            # decision NOT to include nums[i]'
  - '            subset.pop()'
  - '            dfs(i + 1)'
  - ''
  - '        dfs(0)'
  - '        return res'
  cases:
  - input: '[1,2,3]'
    expected: '[[1,2,3],[1,2],[1,3],[1],[2,3],[2],[3],[]]'
  - input: '[0]'
    expected: '[[0],[]]'
  worked_example:
    input: '[1,2,3]'
    steps:
    - ko: 'dfs(0) 호출: 첫 원소 1을 포함하는 경로 탐색. subset=[1]로 설정하고 dfs(1) 호출'
      en: 'Call dfs(0): explore including element 1. Set subset=[1], recurse to dfs(1)'
    - ko: 'dfs(2) 도달: 세 번째 원소 3을 포함하는 경로에서 subset=[1,2,3] 완성. 기본 케이스 도달하여 결과에 추가.'
      en: 'Reach dfs(2): complete subset [1,2,3]. Hit base case (i=3), add to result'
    - ko: '백트래킹: 3 제거 → subset=[1,2]. dfs(3) 호출하면 기본 케이스로 [1,2] 추가. 계속 백트래킹하며 [1,3], [1] 등 추가'
      en: 'Backtrack: remove 3 → subset=[1,2]. Recurse, save [1,2]. Continue backtracking to save [1,3], [1], etc.'
    - ko: '1 제거 후 제외 경로 탐색: subset=[]부터 시작하여 [2,3], [2], [3], [] 순서로 추가. 총 8개 부분집합 생성 완료'
      en: 'Exclude element 1: explore without it. Generate [2,3], [2], [3], []. Complete with 8 subsets total'
    answer: '[[1,2,3],[1,2],[1,3],[1],[2,3],[2],[3],[]]'
solution:
  code: "class Solution:\n    def subsets(self, nums: List[int]) -> List[List[int]]:\n        res = []\n\n        subset = []\n\n        def dfs(i):\n            if i >= len(nums):\n                res.append(subset.copy())\n                return\n            # decision to include nums[i]\n            subset.append(nums[i])\n            dfs(i + 1)\n            # decision NOT to include nums[i]\n            subset.pop()\n            dfs(i + 1)\n\n        dfs(0)\n        return res\n"
  complexity:
    time: O(n·2^n)
    space: O(n)
  followup:
  - ko: 크기가 정확히 k인 부분집합만 생성하려면 어떻게 수정할까요?
    en: How would you generate only subsets of exactly size k?
  - ko: 비트 조작(bit manipulation)을 사용하여 반복문으로 구현할 수 있을까요?
    en: How would you generate all subsets iteratively using bit manipulation?
  - ko: 만약 입력에 중복된 원소가 있다면, 코드를 어떻게 변경해야 중복 부분집합을 피할 수 있을까요?
    en: If the input contained duplicate elements, how would you modify the code to avoid duplicate subsets in the output?
```
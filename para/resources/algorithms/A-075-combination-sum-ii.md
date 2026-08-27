---
created: '2026-07-31'
date: '2026-07-31'
day: Day 75
difficulty: medium
id: A-075
source:
  curated_in:
  - neetcode150
  number: 40
  platform: leetcode
  slug: combination-sum-ii
  url: https://leetcode.com/problems/combination-sum-ii/
tags:
- array
- backtracking
title:
  en: Combination Sum II
  ko: 조합의 합 II
today: false
type: algorithm
updated: '2026-07-31'
visible: true
---

# 조합의 합 II

## Data

```yaml
problem:
  title:
    ko: 조합의 합 II
    en: Combination Sum II
  statement:
    ko: '후보 숫자들의 배열(candidates)과 목표 숫자(target)가 주어질 때, candidates에서 합이 target이 되는 모든 고유한 조합을 찾으세요.


      candidates의 각 숫자는 한 조합에서 최대 한 번만 사용할 수 있습니다.


      주의: 결과 집합은 중복된 조합을 포함해서는 안 됩니다.'
    en: 'Given a collection of candidate numbers (candidates) and a target number (target), find all unique combinations in candidates where the candidate numbers sum to target.


      Each number in candidates may only be used once in the combination.


      Note: The solution set must not contain duplicate combinations.'
  constraints:
  - 1 ≤ candidates.length ≤ 100
  - 1 ≤ candidates[i] ≤ 50
  - 1 ≤ target ≤ 30
  io:
  - input: '[10,1,2,7,6,1,5]

      8'
    output: '[[1,1,6],[1,2,5],[1,7],[2,6]]'
  - input: '[2,5,2,1,2]

      5'
    output: '[[1,2,2],[5]]'
clarifying:
  items:
  - q:
      ko: 같은 인덱스의 숫자를 한 조합에서 여러 번 사용할 수 있나요?
      en: Can we use the same element multiple times in a single combination?
    type: good
    why:
      ko: 각 숫자는 정확히 한 번만 사용 가능합니다. 배열의 각 위치는 한 조합에서 최대 한 번만 선택될 수 있습니다.
      en: No. Each element can only be used once per combination. Every index in the input array can be selected at most once.
  - q:
      ko: 입력 배열에 중복된 숫자가 있으면 결과에 중복된 조합이 나타날 수 있나요?
      en: If the input array has duplicate values, can the output contain duplicate combinations?
    type: good
    why:
      ko: 아니요. 입력에 중복된 값이 있어도 결과는 고유한 조합만 포함해야 합니다. 이는 정렬 후 중복된 후보자를 건너뛰어 달성합니다.
      en: No. Even if the input has duplicates, the output must only contain unique combinations. We achieve this by skipping duplicate candidates during recursion.
  - q:
      ko: 결과에 포함된 각 조합이 정렬된 순서여야 하나요?
      en: Should each combination in the result be in sorted order?
    type: good
    why:
      ko: 문제에서 명시적으로 요구하지는 않지만, 입력을 먼저 정렬하면 자동으로 각 조합도 정렬된 상태로 생성됩니다.
      en: While not explicitly required, sorting the input first ensures that all combinations are generated in sorted order, which helps avoid duplicates.
  - q:
      ko: 입력 배열에 같은 값이 두 개 있으면 각각을 다른 요소로 취급하나요?
      en: If the input has two elements with the same value at different indices, are they treated as distinct?
    type: good
    why:
      ko: 네. 같은 값이라도 배열의 서로 다른 위치에 있으면 서로 다른 요소입니다. 하지만 중복 조합을 피하기 위해 같은 값의 요소를 건너뜁니다.
      en: Yes, elements at different indices are distinct, even if they have the same value. However, we skip using duplicate values to avoid generating duplicate combinations.
  - q:
      ko: 한 번의 재귀 호출에서 이전에 선택한 숫자를 다시 선택할 수 있나요?
      en: Can we revisit a previously selected element in the same recursive branch?
    type: distractor
    why:
      ko: 아니요. 각 재귀 호출에서 `pos`를 증가시켜서 이전 위치로는 돌아가지 않습니다. 이것이 각 요소를 최대 한 번만 사용하는 것을 보장합니다.
      en: No. We pass `i + 1` in the recursive call to ensure we only consider candidates after the current position, preventing reuse.
  - q:
      ko: 정렬하지 않은 배열도 이 알고리즘으로 올바른 답을 얻을 수 있나요?
      en: Would the algorithm produce correct results without sorting the input?
    type: distractor
    why:
      ko: 정렬 없이는 중복 조합을 효율적으로 제거할 수 없습니다. 정렬은 같은 값의 요소들을 인접하게 배치하여 중복을 감지하고 건너뛸 수 있게 합니다.
      en: No. Sorting groups identical values together, allowing us to skip duplicates efficiently. Without sorting, duplicate elimination becomes much harder.
  - q:
      ko: '`cur.copy()` 대신 `cur`를 직접 추가해도 되나요?'
      en: Can we append `cur` directly to results without calling `copy()`?
    type: distractor
    why:
      ko: 아니요. `cur`는 재귀 과정에서 계속 수정되므로, 직접 추가하면 모든 조합이 같은 참조를 가지게 되어 최종 결과가 잘못됩니다.
      en: No. The `cur` list is modified throughout the recursion, so appending it directly would store references to the same mutable object. We must copy it.
approach:
  items:
  - name:
      ko: 백트래킹 + 정렬 + 중복 건너뛰기
      en: Backtracking with Sorting and Duplicate Skipping
    complexity: O(2^n * k) time, O(n) space (where k = avg combination length)
    type: good
    why:
      ko: 정렬 후 중복된 후보자를 건너뛰는 방식으로 백트래킹합니다. 이는 중복 제거를 효율적으로 하면서 모든 유효한 조합을 찾습니다.
      en: Sort the input first, then use backtracking while skipping duplicate candidates. This efficiently eliminates duplicates while exploring all valid combinations.
  - name:
      ko: 브루트포스 + 필터링
      en: Brute Force with Post-filtering
    complexity: O(2^n * k) time, O(2^n) space
    type: distractor
    why:
      ko: 모든 부분집합을 생성한 후 결과에서 중복을 제거합니다. 정렬 전략보다 효율성이 떨어지고 구현이 복잡합니다.
      en: Generate all subsets first, then remove duplicates from results. Less efficient and harder to implement than the sorted approach.
  - name:
      ko: 빈도 맵 기반 백트래킹
      en: Backtracking with Frequency Map
    complexity: O(n log n + k!) time, O(n) space
    type: distractor
    why:
      ko: 요소의 빈도를 세어서 중복을 추적합니다. 정렬 방식과 비슷하게 작동하지만 추가 맵 자료구조가 필요합니다.
      en: Count frequencies and track duplicate usage. Achieves the same result as sorting but requires extra data structures and is slightly more complex.
  - name:
      ko: 동적 프로그래밍
      en: Dynamic Programming
    complexity: O(n * target) time, O(n * target) space
    type: distractor
    why:
      ko: DP로 각 (인덱스, 남은 합) 상태를 추적할 수 있지만, 실제 조합들을 구성하기가 복잡하고 조합 생성에는 백트래킹이 더 자연스럽습니다.
      en: DP can track states but reconstructing actual combinations becomes complex. Backtracking is more natural for generating all combinations.
logic:
  format: slot
  slots:
  - label:
      ko: 입력 정렬
      en: Sort the input
    indent: 0
    options:
    - code: candidates.sort()
      type: good
      why:
        ko: 같은 값을 가진 요소들을 인접하게 배치하여 중복 조합을 효율적으로 감지하고 건너뛸 수 있게 합니다.
        en: Sorting groups identical values together, allowing us to detect and skip duplicates during recursion.
    - code: candidates.reverse()
      type: distractor
      why:
        ko: 역순 정렬은 중복 검사를 복잡하게 만들고 올바른 효율성을 제공하지 않습니다.
        en: Reversing doesn't help with duplicate detection and complicates the algorithm.
    - code: sorted_candidates = sorted(candidates)
      type: distractor
      why:
        ko: 새 변수를 만들 필요가 없습니다. 직접 candidates를 정렬하는 것이 더 효율적입니다.
        en: Creating a new sorted list is unnecessary and wastes space. Modify in-place instead.
  - label:
      ko: '기저 경우: 유효한 조합 발견'
      en: 'Base case: valid combination found'
    indent: 1
    options:
    - code: res.append(cur.copy())
      type: good
      why:
        ko: 목표값이 0이 되면 현재 조합이 유효합니다. 복사본을 결과에 추가해야 합니다 (원본 리스트가 계속 수정되기 때문).
        en: When target reaches 0, the current combination is valid. We must append a copy since `cur` will be modified in future iterations.
    - code: res.append(cur)
      type: distractor
      why:
        ko: 복사본을 만들지 않으면 모든 결과가 같은 리스트 참조를 가지게 되어 잘못된 결과가 됩니다.
        en: Without copying, all results would point to the same list object, which is modified later. The output would be incorrect.
    - code: 'if target == 0: return res.append(cur.copy())'
      type: distractor
      why:
        ko: '`append()`는 None을 반환하므로 이렇게 작성할 수 없습니다. return 전에 append하고 따로 return해야 합니다.'
        en: This is syntactically incorrect. `append()` returns None. We must append first, then return separately.
  - label:
      ko: '가지 제거: 합 초과'
      en: 'Pruning: target exceeded'
    indent: 1
    options:
    - code: 'if target <= 0:'
      type: good
      why:
        ko: 남은 합이 음수가 되면 이 경로는 더 이상 탐색할 필요가 없습니다. 조기에 종료하여 불필요한 재귀를 방지합니다.
        en: If target becomes negative, no valid solution exists in this branch. Early termination saves unnecessary recursion.
    - code: 'if target < 0: res.append(cur.copy()); return'
      type: distractor
      why:
        ko: 음수일 때 결과를 추가하는 것은 잘못된 로직입니다. 단순히 종료하기만 해야 합니다.
        en: Adding an invalid combination when target is negative is incorrect. Just terminate without saving.
    - code: 'if target <= 0: return'
      type: distractor
      why:
        ko: target == 0은 유효한 경우이므로 > 0이 아닌 경우에 종료하면 안 됩니다. < 0에서만 종료해야 합니다.
        en: This would skip the valid case when target == 0. We should only prune when target < 0.
  - label:
      ko: 중복 후보자 건너뛰기
      en: Skip duplicate candidates
    indent: 2
    options:
    - code: 'if candidates[i] == prev:'
      type: good
      why:
        ko: 같은 값의 후보자를 건너뛰어 중복 조합을 방지합니다. `prev` 변수는 이전에 시도한 값을 추적합니다.
        en: Skip candidates with the same value as the previous one to avoid duplicate combinations. The `prev` variable tracks what we just tried.
    - code: 'if i > 0 and candidates[i] == candidates[i-1]: continue'
      type: distractor
      why:
        ko: 같은 값을 비교하지만, `prev` 방식이 더 명확하고 효율적입니다. `prev`는 반복 내에서 건너뛴 값들도 추적합니다.
        en: This checks previous index but misses cases where we skip multiple duplicates in one iteration. The `prev` approach is clearer.
    - code: 'if candidates[i] in cur: continue'
      type: distractor
      why:
        ko: 현재 조합에 있는지 확인하는 것은 잘못된 검사입니다. 다른 조합에서는 같은 값을 사용할 수 있으므로, 루프 내에서의 중복을 건너뛰어야 합니다.
        en: Checking if a value is in the current combination is wrong. We need to skip duplicates within the current loop level, not based on what's already selected.
  - label:
      ko: 탐색과 백트래킹
      en: Explore and backtrack
    indent: 2
    options:
    - code: cur.append(candidates[i])
      type: good
      why:
        ko: 현재 후보자를 추가하고 재귀적으로 탐색한 후, 다시 제거합니다. 이를 통해 모든 조합을 탐색하면서 경로를 재사용할 수 있습니다.
        en: Add the current candidate, explore recursively with the next position, then remove it. This allows us to explore all combinations while reusing the path.
    - code: cur.append(candidates[i]); backtrack(cur, i, target - candidates[i]); cur.pop()
      type: distractor
      why:
        ko: 위치를 `i + 1`이 아닌 `i`로 전달하면 같은 요소를 여러 번 사용할 수 있게 되어 문제 조건을 위반합니다.
        en: Passing `i` instead of `i + 1` allows reusing the same element, which violates the problem constraint.
    - code: cur.append(candidates[i]); backtrack(cur, i + 1, target - candidates[i])
      type: distractor
      why:
        ko: '`cur.pop()`이 없으면 백트래킹이 이루어지지 않아 다음 반복에서 경로가 잘못됩니다.'
        en: Without `cur.pop()`, the path isn't restored for the next iteration, causing incorrect combinations.
  - label:
      ko: 재귀 시작
      en: Start recursion
    indent: 0
    options:
    - code: backtrack([], 0, target)
      type: good
      why:
        ko: 빈 경로와 위치 0에서 재귀를 시작하여 모든 조합을 탐색합니다.
        en: Initiate backtracking with an empty path from position 0 to explore all combinations.
    - code: backtrack([], 1, target)
      type: distractor
      why:
        ko: 위치 1에서 시작하면 candidates[0]을 절대 사용할 수 없습니다.
        en: Starting at position 1 skips the first candidate. We must start at position 0.
    - code: backtrack([candidates[0]], 1, target - candidates[0])
      type: distractor
      why:
        ko: 첫 번째 요소를 미리 선택하는 것은 백트래킹 과정을 거치지 않으므로 올바르지 않습니다.
        en: Pre-selecting the first element bypasses the backtracking process and skips some combinations.
trace:
  code:
  - 'class Solution:'
  - '    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:'
  - '        candidates.sort()'
  - ''
  - '        res = []'
  - ''
  - '        def backtrack(cur, pos, target):'
  - '            if target == 0:'
  - '                res.append(cur.copy())'
  - '                return'
  - '            if target <= 0:'
  - '                return'
  - ''
  - '            prev = -1'
  - '            for i in range(pos, len(candidates)):'
  - '                if candidates[i] == prev:'
  - '                    continue'
  - '                cur.append(candidates[i])'
  - '                backtrack(cur, i + 1, target - candidates[i])'
  - '                cur.pop()'
  - '                prev = candidates[i]'
  - ''
  - '        backtrack([], 0, target)'
  - '        return res'
  cases:
  - input: '[10,1,2,7,6,1,5]

      8'
    expected: '[[1,1,6],[1,2,5],[1,7],[2,6]]'
  - input: '[2,5,2,1,2]

      5'
    expected: '[[1,2,2],[5]]'
  worked_example:
    input: '[10,1,2,7,6,1,5]

      8'
    steps:
    - ko: '입력 정렬: [10,1,2,7,6,1,5] → [1,1,2,5,6,7,10]'
      en: 'Sort input: [10,1,2,7,6,1,5] → [1,1,2,5,6,7,10]'
    - ko: '위치 0에서 시작: 첫 번째 1 선택, 남은 합 7로 재귀'
      en: 'Start at position 0: select first 1, recurse with remaining sum 7'
    - ko: '위치 1: 두 번째 1 선택 (다른 인덱스), 남은 합 6으로 재귀'
      en: 'At position 1: select second 1 (different index), recurse with sum 6'
    - ko: '위치 2: 합 6을 만들기 위해 6 선택, [1,1,6] 완성 → 결과에 추가'
      en: 'At position 2: select 6 to complete sum, [1,1,6] found → add to results'
    - ko: '백트래킹하여 다른 경로 탐색: [1,2,5], [1,7], [2,6] 등을 발견'
      en: 'Backtrack and explore other paths: find [1,2,5], [1,7], [2,6], etc.'
    - ko: '최종 결과: [[1,1,6], [1,2,5], [1,7], [2,6]]'
      en: 'Final result: [[1,1,6], [1,2,5], [1,7], [2,6]]'
    answer: '[[1,1,6],[1,2,5],[1,7],[2,6]]'
solution:
  code: "class Solution:\n    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:\n        candidates.sort()\n\n        res = []\n\n        def backtrack(cur, pos, target):\n            if target == 0:\n                res.append(cur.copy())\n                return\n            if target <= 0:\n                return\n\n            prev = -1\n            for i in range(pos, len(candidates)):\n                if candidates[i] == prev:\n                    continue\n                cur.append(candidates[i])\n                backtrack(cur, i + 1, target - candidates[i])\n                cur.pop()\n                prev = candidates[i]\n\n        backtrack([], 0, target)\n        return res\n"
  complexity:
    time: O(2^n * k) where n = len(candidates), k = average combination length
    space: O(n) for recursion stack depth (not counting output space)
  followup:
  - ko: 각 숫자를 여러 번 사용할 수 있다면 어떻게 수정할까요? (Combination Sum I)
    en: How would you modify the solution if each number could be used multiple times? (Combination Sum I)
  - ko: 실제 조합 대신 유효한 조합의 '개수'만 반환해야 한다면 어떻게 최적화할까요?
    en: How would you optimize if you only needed to return the COUNT of valid combinations, not the combinations themselves?
  - ko: '각 후보자를 정확히 한 번 사용해야 하는 경우라면 (예: 집합의 분할) 알고리즘이 어떻게 달라질까요?'
    en: How would the algorithm change if every candidate must be used exactly once (like a partition problem)?
```
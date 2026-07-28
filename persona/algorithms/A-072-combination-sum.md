---
created: '2026-07-28'
date: '2026-07-28'
day: Day 72
difficulty: medium
id: A-072
source:
  curated_in:
  - neetcode150
  number: 39
  platform: leetcode
  slug: combination-sum
  url: https://leetcode.com/problems/combination-sum/
status: draft
tags:
- array
- backtracking
title:
  en: Combination Sum
  ko: 조합의 합
today: true
type: algorithm
updated: '2026-07-28'
visible: true
---

# 조합의 합

## Data

```yaml
problem:
  title:
    ko: 조합의 합
    en: Combination Sum
  statement:
    en: 'Given an array of distinct integers candidates and a target integer target, return a list of all unique combinations of candidates where the chosen numbers sum to target. You may return the combinations in any order.


      The same number may be chosen from candidates an unlimited number of times. Two combinations are unique if the frequency of at least one of the chosen numbers is different.


      The test cases are generated such that the number of unique combinations that sum up to target is less than 150 combinations for the given input.'
    ko: '서로 다른 정수로 이루어진 배열 candidates와 정수 target이 주어졌을 때, candidates에서 선택한 수들의 합이 target이 되는 모든 고유한 조합의 리스트를 반환하세요. 조합은 어떤 순서로든 반환할 수 있습니다.


      같은 수를 candidates에서 무제한으로 선택할 수 있습니다. 두 조합은 선택된 수 중 적어도 하나의 빈도가 다르면 서로 다른 조합입니다.


      테스트 케이스는 주어진 입력에 대해 target을 만드는 고유한 조합의 개수가 150개 미만이 되도록 생성됩니다.'
  constraints:
  - 1 ≤ candidates.length ≤ 30
  - 2 ≤ candidates[i] ≤ 40
  - All elements of candidates are distinct
  - 1 ≤ target ≤ 40
  io:
  - input: '[2,3,6,7]

      7'
    output: '[[2,2,3],[7]]'
  - input: '[2,3,5]

      8'
    output: '[[2,2,2,2],[2,3,3],[3,5]]'
  - input: '[2]

      1'
    output: '[]'
clarifying:
  items:
  - q:
      ko: 같은 숫자를 여러 번 사용할 수 있나요?
      en: Can we use the same number multiple times?
    type: good
    why:
      ko: 이것은 이 문제의 핵심입니다. 무제한으로 재사용할 수 있다는 것이 단순 조합과 다른 점입니다.
      en: This is the core distinction of this problem. The ability to reuse numbers unlimited times separates it from standard combination problems.
  - q:
      ko: 두 조합이 '고유하다'는 것의 정의는 무엇인가요?
      en: What makes two combinations 'unique'?
    type: good
    why:
      ko: '조합의 순서가 아니라 각 숫자의 빈도가 다르면 다른 조합입니다. 예: [2,3]과 [3,2]는 같은 조합입니다.'
      en: Uniqueness is defined by the frequency of each number, not by order. For example, [2,3] and [3,2] represent the same combination.
  - q:
      ko: 결과 조합들을 정렬된 순서로 반환해야 하나요?
      en: Should the output combinations be in sorted order?
    type: good
    why:
      ko: 문제에서 '어떤 순서로든 반환할 수 있다'고 명시되어 있습니다. 정렬 여부는 자유롭습니다.
      en: The problem explicitly states 'any order' is acceptable for the result.
  - q:
      ko: 각 후보 숫자가 최대 몇 번까지 사용될 수 있나요?
      en: What is the maximum number of times each candidate can be used?
    type: distractor
    why:
      ko: 제약사항에 명시된 제한은 없습니다. 문제는 같은 수를 무제한으로 선택할 수 있다고 명시되어 있습니다.
      en: There is no explicit limit mentioned in the constraints. The problem clearly states 'unlimited' reuse.
  - q:
      ko: candidates 배열에 중복된 값이 있을 수 있나요?
      en: Can the candidates array contain duplicate values?
    type: distractor
    why:
      ko: 문제에서 '서로 다른 정수'라고 명시되어 있습니다. 모든 원소가 고유합니다.
      en: The problem explicitly states 'distinct integers', so there are no duplicates in the input.
  - q:
      ko: 조합 [2,2,3]과 [2,3,2]는 다른 조합으로 간주되나요?
      en: Are [2,2,3] and [2,3,2] considered different combinations?
    type: distractor
    why:
      ko: 아니요. 두 조합 모두 2가 2개, 3이 1개이므로 같은 조합입니다. 순서는 상관없습니다.
      en: No, both have the same frequency of 2 (twice) and 3 (once), so they are the same combination. Order doesn't matter.
  - q:
      ko: target을 정확히 만들 수 없으면 빈 리스트를 반환하나요?
      en: If target cannot be reached, should we return an empty list?
    type: good
    why:
      ko: '맞습니다. 유효한 조합이 없으면 함수는 빈 리스트를 반환합니다. 예: candidates=[2], target=1'
      en: 'Correct. If no valid combination exists, return an empty list. Example: candidates=[2], target=1 returns [].'
approach:
  items:
  - name:
      ko: 백트래킹 (결정 트리)
      en: Backtracking (Decision Tree)
    complexity: O(N^(T/M)) time / O(T/M) space (where N = length of candidates, T = target, M = minimum element)
    type: good
    why:
      ko: 각 단계에서 현재 숫자를 포함하거나 포함하지 않을 선택을 함으로써 모든 가능한 조합을 탐색합니다. 무제한 재사용을 자연스럽게 표현합니다.
      en: Explores all combinations by deciding at each step to include or exclude a candidate. Naturally expresses unlimited reuse by revisiting the same index.
  - name:
      ko: 동적 프로그래밍
      en: Dynamic Programming
    complexity: O(T × N) time / O(T) space
    type: distractor
    why:
      ko: DP로 풀 수 있지만 결과 조합을 추적하기 어렵고 백트래킹보다 직관적이지 않습니다.
      en: While DP can solve the problem, tracking actual combinations becomes cumbersome and is less intuitive than backtracking.
  - name:
      ko: 중첩 루프 (브루트 포스)
      en: Nested Loops (Brute Force)
    complexity: Infeasible
    type: distractor
    why:
      ko: 무제한 재사용을 고정된 루프 깊이로 표현할 수 없습니다. 루프를 미리 얼마나 깊게 해야 할지 알 수 없습니다.
      en: Cannot express unlimited reuse with a fixed number of nested loops. Required depth is unknown in advance.
  - name:
      ko: 탐욕 알고리즘
      en: Greedy Approach
    complexity: O(N log N) time
    type: distractor
    why:
      ko: 탐욕적 선택은 일부 유효한 조합을 놓칩니다. 모든 가능성을 탐색해야 하므로 탐욕 알고리즘은 적합하지 않습니다.
      en: Greedy choices eliminate valid solutions. We must explore all possibilities, making greedy approaches unsuitable.
logic:
  format: slot
  slots:
  - label:
      ko: 결과 저장소 초기화
      en: Initialize result container
    indent: 0
    options:
    - code: res = []
      type: good
      why:
        ko: 모든 유효한 조합을 저장할 리스트를 만듭니다.
        en: Creates a list to store all valid combinations found during the search.
    - code: res = None
      type: distractor
      why:
        ko: None은 컬렉션이 아니어서 조합을 저장할 수 없습니다.
        en: None is not a collection and cannot store combinations.
    - code: res = set()
      type: distractor
      why:
        ko: 세트는 리스트를 저장할 수 없고 순서를 보장하지 않습니다.
        en: A set cannot store lists as elements and doesn't preserve order.
  - label:
      ko: '기저 조건: 목표값 도달 검사'
      en: 'Base case: Check if target is reached'
    indent: 1
    options:
    - code: 'if total == target:'
      type: good
      why:
        ko: 현재 합이 목표와 정확히 같으면 유효한 조합을 찾은 것입니다.
        en: When the current sum equals the target, we've found a valid combination.
    - code: 'if total > target:'
      type: distractor
      why:
        ko: 이 조건은 불충분합니다. total이 정확히 target과 같을 때를 확인해야 합니다.
        en: This only checks overflow but misses the success condition when total exactly equals target.
    - code: 'if total >= target:'
      type: distractor
      why:
        ko: total이 target보다 크면 유효하지 않은 조합입니다. 정확히 같을 때만 유효합니다.
        en: This would incorrectly accept sums greater than the target as valid solutions.
  - label:
      ko: 조합을 결과에 추가
      en: Append current combination to result
    indent: 2
    options:
    - code: res.append(cur.copy())
      type: good
      why:
        ko: cur.copy()로 현재 조합의 독립적인 복사본을 저장합니다. 나중의 수정으로부터 보호합니다.
        en: Using copy() ensures we store an independent snapshot, protecting it from future modifications to cur.
    - code: res.append(cur)
      type: distractor
      why:
        ko: 참조를 저장하면 나중에 cur이 수정될 때 이미 저장된 조합도 함께 변합니다.
        en: Storing the reference means all stored combinations will be modified when cur changes later.
    - code: res.append(tuple(cur))
      type: distractor
      why:
        ko: 튜플로 변환할 필요가 없습니다. 리스트로 복사하는 것이 충분합니다.
        en: While this would work, converting to tuple is unnecessary when a list copy suffices.
  - label:
      ko: '가지 자르기: 유효하지 않은 상태 제거'
      en: 'Pruning: Stop exploring invalid states'
    indent: 1
    options:
    - code: 'if i >= len(candidates) or total > target:'
      type: good
      why:
        ko: 합이 목표를 초과하거나 모든 후보를 검토했으면 더 이상 탐색할 필요가 없습니다.
        en: If total exceeds target or we've exhausted all candidates, further search is futile.
    - code: 'if i >= len(candidates) or total >= target:'
      type: distractor
      why:
        ko: 조건이 잘못되었습니다. total == target인 경우는 이미 위에서 처리되었으므로 여기서는 total > target만 확인해야 합니다.
        en: The equality case is already handled above, so we should only check total > target here.
    - code: 'if i > len(candidates) or total > target:'
      type: distractor
      why:
        ko: i >= len(candidates)가 아니라 i > len(candidates)만 확인하면 마지막 후보를 놓칠 수 있습니다.
        en: Using > instead of >= would incorrectly process the last valid candidate.
  - label:
      ko: 현재 후보 포함하기
      en: Include current candidate
    indent: 2
    options:
    - code: cur.append(candidates[i])
      type: good
      why:
        ko: 현재 후보의 값을 조합에 추가합니다. 이 숫자를 포함하는 경로를 탐색하게 됩니다.
        en: Adds the current candidate value to the combination, exploring paths that include this number.
    - code: cur.append(i)
      type: distractor
      why:
        ko: 인덱스가 아니라 실제 값 candidates[i]를 추가해야 합니다.
        en: Should append the actual value candidates[i], not the index i.
    - code: candidates.append(cur)
      type: distractor
      why:
        ko: 방향이 반대입니다. candidates에 cur을 추가하는 것이 아니라 cur에 candidates[i]를 추가해야 합니다.
        en: The direction is reversed. We append to cur, not to candidates.
  - label:
      ko: '재귀: 같은 후보를 재사용하도록'
      en: 'Recursive call: Reuse same candidate'
    indent: 2
    options:
    - code: dfs(i, cur, total + candidates[i])
      type: good
      why:
        ko: 인덱스 i를 유지한 채로 재귀하여 같은 숫자를 다시 선택할 수 있게 합니다. 무제한 재사용의 핵심입니다.
        en: By keeping the same index i, we allow the same candidate to be considered again in deeper recursion. This is the key to unlimited reuse.
    - code: dfs(i + 1, cur, total + candidates[i])
      type: distractor
      why:
        ko: i를 증가시키면 다음 후보로 넘어가므로 현재 숫자를 다시 사용할 수 없습니다.
        en: Incrementing i moves to the next candidate, preventing reuse of the current number.
    - code: dfs(i, cur, total)
      type: distractor
      why:
        ko: total에 candidates[i]를 더하지 않으면 합계가 업데이트되지 않습니다.
        en: Forgetting to add to total means the sum doesn't progress toward the target.
  - label:
      ko: 백트래킹 후 다음 후보로 이동
      en: Backtrack and explore next candidate
    indent: 2
    options:
    - code: dfs(i + 1, cur, total)
      type: good
      why:
        ko: 인덱스를 증가시켜 다음 후보를 탐색합니다. 현재 숫자를 더 이상 포함하지 않는 대안적 경로를 탐색합니다.
        en: Increments the index to move to the next candidate, exploring alternative paths that exclude the current number or use different candidates.
    - code: dfs(i, cur, total)
      type: distractor
      why:
        ko: i를 증가시키지 않으면 같은 후보를 계속 탐색하여 무한 루프에 빠집니다.
        en: Without incrementing i, we'd explore the same candidate infinitely.
    - code: dfs(i + 2, cur, total)
      type: distractor
      why:
        ko: i를 2 증가시키면 일부 후보를 건너뛰게 됩니다.
        en: Incrementing by 2 would skip intermediate candidates.
trace:
  code:
  - 'class Solution:'
  - '    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:'
  - '        res = []'
  - ''
  - '        def dfs(i, cur, total):'
  - '            if total == target:'
  - '                res.append(cur.copy())'
  - '                return'
  - '            if i >= len(candidates) or total > target:'
  - '                return'
  - ''
  - '            cur.append(candidates[i])'
  - '            dfs(i, cur, total + candidates[i])'
  - '            cur.pop()'
  - '            dfs(i + 1, cur, total)'
  - ''
  - '        dfs(0, [], 0)'
  - '        return res'
  cases:
  - input: '[2,3,6,7]

      7'
    expected: '[[2,2,3],[7]]'
  - input: '[2,3,5]

      8'
    expected: '[[2,2,2,2],[2,3,3],[3,5]]'
  - input: '[2]

      1'
    expected: '[]'
  worked_example:
    input: '[2,3,6,7]

      7'
    steps:
    - ko: dfs(0, [], 0)에서 시작합니다. 첫 번째 후보는 2입니다.
      en: Start with dfs(0, [], 0). First candidate is 2.
    - ko: '2를 포함: dfs(0, [2], 2). 다시 2 포함: dfs(0, [2,2], 4). 한 번 더: dfs(0, [2,2,2], 6).'
      en: 'Include 2: dfs(0, [2], 2). Include 2 again: dfs(0, [2,2], 4). Once more: dfs(0, [2,2,2], 6).'
    - ko: '[2,2] 상태로 돌아가서 i=1(숫자 3)로 이동: dfs(1, [2,2], 4). 3 포함 시 [2,2,3], 합=7 → 결과에 추가. 계속 탐색하여 [7]도 발견.'
      en: 'Backtrack to [2,2] and move to i=1 (candidate 3): dfs(1, [2,2], 4). Adding 3 gives [2,2,3] with sum=7 → add to result. Continue to find [7].'
    answer: '[[2,2,3],[7]]'
solution:
  code: "class Solution:\n    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:\n        res = []\n\n        def dfs(i, cur, total):\n            if total == target:\n                res.append(cur.copy())\n                return\n            if i >= len(candidates) or total > target:\n                return\n\n            cur.append(candidates[i])\n            dfs(i, cur, total + candidates[i])\n            cur.pop()\n            dfs(i + 1, cur, total)\n\n        dfs(0, [], 0)\n        return res\n"
  complexity:
    time: O(N^(T/M)) where N = length of candidates, T = target, M = minimum candidate value
    space: O(T/M) for recursion stack depth (excluding output space)
  followup:
  - ko: 만약 각 숫자를 최대 k번까지만 사용할 수 있다면 어떻게 수정할까요?
    en: What if each candidate can be used at most k times instead of unlimited?
  - ko: candidates 배열이 정렬되지 않은 경우 알고리즘을 어떻게 최적화할 수 있을까요?
    en: How would you optimize the algorithm if the candidates array is not sorted?
  - ko: 동일한 조합이 중복으로 나타나지 않도록 어떻게 보장할 수 있을까요?
    en: How can you ensure no duplicate combinations appear if candidates contains duplicate values?
```
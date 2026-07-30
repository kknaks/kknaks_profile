---
created: '2026-07-29'
date: '2026-07-29'
day: Day 73
difficulty: medium
id: A-073
source:
  curated_in:
  - neetcode150
  number: 46
  platform: leetcode
  slug: permutations
  url: https://leetcode.com/problems/permutations/
status: draft
tags:
- array
- backtracking
title:
  en: Permutations
  ko: 순열
today: false
type: algorithm
updated: '2026-07-29'
visible: true
---

# 순열

## Data

```yaml
problem:
  title:
    ko: 순열
    en: Permutations
  statement:
    ko: 고유한 정수들로 이루어진 배열 nums가 주어질 때, 가능한 모든 순열을 반환하세요. 답은 어떤 순서로든 반환할 수 있습니다.
    en: Given an array nums of distinct integers, return all the possible permutations. You can return the answer in any order.
  constraints:
  - 1 ≤ nums.length ≤ 6
  - -10 ≤ nums[i] ≤ 10
  - All integers in nums are unique
  io:
  - input: '[1,2,3]'
    output: '[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]'
  - input: '[0,1]'
    output: '[[0,1],[1,0]]'
  - input: '[1]'
    output: '[[1]]'
clarifying:
  items:
  - q:
      ko: 순열이란 정확히 무엇인가요?
      en: What is a permutation exactly?
    type: good
    why:
      ko: 순열은 모든 원소를 정확히 한 번씩 사용하여 만든 배열이므로, 순서가 다르면 다른 순열입니다.
      en: A permutation arranges all elements exactly once, so different orders are different permutations (e.g., [1,2] ≠ [2,1])
  - q:
      ko: 모든 입력 정수는 고유한가요?
      en: Are all input integers guaranteed to be unique?
    type: good
    why:
      ko: 제약 조건에서 명시하고 있으므로, 중복을 처리할 필요가 없습니다.
      en: Yes, constraints guarantee distinct integers, so no need to handle duplicates in the algorithm
  - q:
      ko: 출력 순열들의 순서가 정해져 있나요?
      en: Must the output permutations be in a specific order?
    type: good
    why:
      ko: 문제에서 '어떤 순서로든' 반환 가능하다고 명시하여, 사전식 순서를 유지할 필요가 없습니다.
      en: The problem explicitly allows 'any order', simplifying the solution without lexicographic constraints
  - q:
      ko: 한 순열 내에서 같은 원소를 여러 번 사용할 수 있나요?
      en: Can a single permutation use the same element multiple times?
    type: distractor
    why:
      ko: 아니요. 순열은 배열의 모든 원소를 정확히 한 번씩 사용해야 합니다.
      en: No, permutation means each element appears exactly once per arrangement
  - q:
      ko: 입력 배열을 수정해도 괜찮나요?
      en: Can we modify the input array during processing?
    type: distractor
    why:
      ko: 이 해법은 pop/append로 배열을 회전시키므로 입력을 수정하지만, 복원하기 때문에 최종적으로는 원래대로 돌아옵니다.
      en: This solution modifies the array with pop/append but restores it each iteration, which works but may violate LeetCode expectations
  - q:
      ko: 반환된 배열들이 원본 참조여도 되나요?
      en: Can we return references to the original arrays?
    type: distractor
    why:
      ko: 아니요. 각 순열은 독립적인 배열이어야 하므로, 참조를 반환하면 모든 순열이 같은 배열을 가리키게 됩니다.
      en: No, returning references would cause all permutations to point to the same array—each must be a copy
approach:
  items:
  - name:
      ko: 백트래킹 (제거-재귀-복원)
      en: Backtracking (Remove-Recurse-Restore)
    complexity: O(n! × n) time / O(n) space
    type: good
    why:
      ko: 배열의 첫 원소를 제거하고 나머지에서 순열을 구한 뒤, 그 순열들에 제거한 원소를 추가합니다. 각 순열 생성에 O(n), 총 n!개의 순열을 만들어 O(n!×n)입니다.
      en: Pop first element, recursively get permutations of remainder, append that element to each. O(n!) permutations × O(n) to build each = O(n!×n) total
  - name:
      ko: 백트래킹 (사용 추적 배열)
      en: Backtracking (Used Boolean Array)
    complexity: O(n! × n) time / O(n) space
    type: good
    why:
      ko: 사용된 원소를 boolean 배열로 추적하면서, 인덱스 순서대로 순열을 구성합니다. 다른 방법이지만 같은 시간/공간 복잡도입니다.
      en: Track used elements with a boolean array and build permutations by choosing unused elements. Same complexity, different structure
  - name:
      ko: 조합 생성 (잘못된 접근)
      en: Generating Combinations (Wrong Approach)
    complexity: O(2^n) time
    type: distractor
    why:
      ko: 조합은 순서가 없고 일부 원소만 선택하므로, 순열과 다릅니다. 이 문제에는 맞지 않습니다.
      en: Combinations don't account for order and use subsets—fundamentally different from permutations which use all elements
  - name:
      ko: 내장 함수 itertools.permutations 사용
      en: Built-in itertools.permutations()
    complexity: O(n!) time
    type: distractor
    why:
      ko: 작동하지만 인터뷰에서는 백트래킹 알고리즘의 이해를 보이기 위해 직접 구현하는 것이 중요합니다.
      en: Works correctly but interviews require demonstrating backtracking logic, not using library shortcuts
  - name:
      ko: 스왑 기반 (Heap's Algorithm)
      en: Swap-based (Heap's Algorithm)
    complexity: O(n! × n) time / O(1) space
    type: distractor
    why:
      ko: 유효하지만 구현이 복잡하고 인터뷰에서 설명하기 어렵습니다. 제거-복원 방식이 더 직관적입니다.
      en: Valid but more complex to implement and explain; remove-restore is more intuitive for interviews
logic:
  format: slot
  slots:
  - label:
      ko: 결과 초기화
      en: Initialize result list
    indent: 0
    options:
    - code: res = []
      type: good
      why:
        ko: 모든 순열을 저장할 빈 리스트를 생성합니다.
        en: Create empty list to accumulate all permutations
    - code: res = {}
      type: distractor
      why:
        ko: 딕셔너리는 리스트 확장에 사용할 수 없습니다.
        en: Dictionary cannot be extended like a list
    - code: res = None
      type: distractor
      why:
        ko: None에 extend() 메서드를 호출할 수 없습니다.
        en: Cannot call extend() on None
    - code: res = nums[:]
      type: distractor
      why:
        ko: 입력 배열의 복사본은 아직 순열들이 아닙니다.
        en: Copying input doesn't give us permutations yet
  - label:
      ko: '기저 사례: 원소 1개'
      en: Base case – single element
    indent: 0
    options:
    - code: 'if len(nums) == 1:'
      type: good
      why:
        ko: 배열의 길이가 1이면, 그 원소 하나로만 순열을 만들 수 있으므로 재귀를 멈춥니다.
        en: When array has 1 element, only one permutation exists; stop recursion and return it
    - code: 'if len(nums) == 0:'
      type: distractor
      why:
        ko: 조건이 오프바이원 오류입니다. 빈 배열이 아니라 1개 원소일 때 기저 사례입니다.
        en: Off-by-one error; base case is 1 element, not 0
    - code: 'if len(nums) <= 1:'
      type: distractor
      why:
        ko: 빈 배열도 포함하게 되어, 빈 배열일 때 잘못된 동작을 합니다.
        en: Includes empty array case, which causes incorrect behavior
    - code: 'if len(nums) > 1:'
      type: distractor
      why:
        ko: 조건이 반대입니다. 기저 사례는 작은 경우일 때 적용되어야 합니다.
        en: Inverted condition; base case applies when array is small
  - label:
      ko: 각 원소마다 반복
      en: Loop through each element
    indent: 0
    options:
    - code: 'for i in range(len(nums)):'
      type: good
      why:
        ko: 배열의 모든 원소를 차례대로 처리합니다. 각 원소를 맨 앞에서 제거하고 나머지 원소들의 순열을 구합니다.
        en: Iterate through all positions; each iteration processes a different element as the next to append
    - code: 'for n in nums:'
      type: distractor
      why:
        ko: 값을 직접 순회하면, pop/append로 배열을 수정할 때 인덱스가 맞지 않습니다.
        en: Direct value iteration doesn't work with pop/append rotation logic
    - code: 'for i in range(len(nums) - 1):'
      type: distractor
      why:
        ko: 마지막 원소를 건너뛰므로, 마지막 원소로 시작하는 순열들이 빠집니다.
        en: Skips last element, missing permutations starting with it
    - code: 'while i < len(nums):'
      type: distractor
      why:
        ko: for 루프 대신 while을 사용하면 i 증가를 직접 관리해야 합니다.
        en: While loop requires manual increment management
  - label:
      ko: 맨 앞 원소 제거
      en: Remove first element
    indent: 1
    options:
    - code: n = nums.pop(0)
      type: good
      why:
        ko: 배열의 첫 원소를 변수에 저장하고 배열에서 제거하여, 나머지 원소들로 순열을 구성합니다.
        en: Pop from front so we can work with reduced array and append this element to each sub-permutation
    - code: n = nums[i]
      type: distractor
      why:
        ko: 값만 얻고 배열을 수정하지 않으므로, 나머지 배열이 올바르지 않습니다.
        en: Just gets value without removing; remainder array stays full
    - code: n = nums.pop()
      type: distractor
      why:
        ko: 배열의 끝에서 제거하므로 회전 로직이 깨집니다.
        en: Pops from end instead of front, breaking rotation pattern
    - code: n = nums.pop(i)
      type: distractor
      why:
        ko: 현재 인덱스에서 제거하므로, 회전하지 않고 무작위로 선택합니다.
        en: Removes from arbitrary position, not front, breaking the algorithm
  - label:
      ko: 재귀 호출로 부분 순열 구하기
      en: Recursively get sub-permutations
    indent: 1
    options:
    - code: perms = self.permute(nums)
      type: good
      why:
        ko: 현재 원소를 제거한 나머지 배열에서 순열을 재귀적으로 구합니다. 이를 통해 작은 문제로 축소합니다.
        en: Recursively solve for the reduced array; each call returns permutations of n-1 elements
    - code: perms = self.permute([])
      type: distractor
      why:
        ko: 빈 배열로 호출하면 빈 결과만 반환됩니다.
        en: Empty array returns empty result, losing information
    - code: perms = self.permute(nums[1:])
      type: distractor
      why:
        ko: 배열 슬라이싱으로 복사본을 만들면 회전 로직이 깨집니다.
        en: Slicing creates new array, breaking the pop/append rotation mechanism
    - code: perms = permute(nums)
      type: distractor
      why:
        ko: self를 빠뜨리면 메서드 호출이 실패합니다.
        en: Missing self; method call fails
  - label:
      ko: 부분 순열에 현재 원소 추가
      en: Append element to each sub-permutation
    indent: 1
    options:
    - code: perm.append(n)
      type: good
      why:
        ko: 각 부분 순열의 끝에 제거했던 원소를 추가하여, 완전한 순열을 만듭니다.
        en: Add removed element to end of each sub-permutation to build complete permutations
    - code: perms.append(n)
      type: distractor
      why:
        ko: 개별 순열(perm)이 아닌 전체 리스트(perms)에 추가합니다.
        en: Appends to perms list instead of each individual perm—wrong target
    - code: perm.insert(0, n)
      type: distractor
      why:
        ko: 맨 앞에 추가하므로 순열의 순서가 잘못됩니다.
        en: Inserts at front instead of back, giving wrong order
    - code: perm.extend([n, n])
      type: distractor
      why:
        ko: 원소를 여러 번 추가하므로 순열이 잘못됩니다.
        en: Adds element multiple times, corrupting the permutation
  - label:
      ko: 다음 반복을 위해 원소 복원
      en: Restore element for next iteration
    indent: 1
    options:
    - code: nums.append(n)
      type: good
      why:
        ko: 제거한 원소를 배열의 끝에 다시 추가하여, 다음 반복에서 모든 원소를 다시 처리할 수 있도록 합니다.
        en: Append removed element back so next iteration has all original elements to rotate through
    - code: nums.pop()
      type: distractor
      why:
        ko: 제거하는 것이므로 복원이 아닙니다.
        en: Removes element instead of restoring it
    - code: nums.insert(0, n)
      type: distractor
      why:
        ko: 맨 앞에 추가하면 회전 순서가 틀립니다.
        en: Inserts at front breaks rotation order; should be at back
    - code: pass
      type: distractor
      why:
        ko: 아무것도 하지 않으면 배열이 계속 줄어들어 다음 반복이 실패합니다.
        en: No restoration means array shrinks each iteration, breaking the algorithm
trace:
  code:
  - 'class Solution:'
  - '    def permute(self, nums: List[int]) -> List[List[int]]:'
  - '        res = []'
  - ''
  - '        # base case'
  - '        if len(nums) == 1:'
  - '            return [nums[:]]  # nums[:] is a deep copy'
  - ''
  - '        for i in range(len(nums)):'
  - '            n = nums.pop(0)'
  - '            perms = self.permute(nums)'
  - ''
  - '            for perm in perms:'
  - '                perm.append(n)'
  - '            res.extend(perms)'
  - '            nums.append(n)'
  - '        return res'
  cases:
  - input: '[1,2,3]'
    expected: '[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]'
  - input: '[0,1]'
    expected: '[[0,1],[1,0]]'
  - input: '[1]'
    expected: '[[1]]'
  worked_example:
    input: '[1,2,3]'
    steps:
    - ko: 'permute([1,2,3]) 호출. 기저 사례 아님. i=0: 1을 제거 → permute([2,3]) 호출'
      en: 'Call permute([1,2,3]). Not base case. i=0: Remove 1, call permute([2,3])'
    - ko: 'permute([2,3]): i=0 제거 2 → permute([3])=[[3]] → [[3]]에 2 추가 → [[3,2]]. i=1 제거 3 → permute([2])=[[2]] → [[2]]에 3 추가 → [[2,3]]. 반환 [[3,2],[2,3]]'
      en: 'permute([2,3]): i=0 removes 2, permute([3])=[[3]], add 2→[[3,2]]; i=1 removes 3, permute([2])=[[2]], add 3→[[2,3]]. Returns [[3,2],[2,3]]'
    - ko: '다시 permute([1,2,3])로: [[3,2],[2,3]]의 각 원소에 1을 추가 → [[3,2,1],[2,3,1]]. i=1: 2를 제거 → permute([3,1]) 호출하면 [[1,3],[3,1]], 각각에 2 추가 → [[1,3,2],[3,1,2]]'
      en: 'Back to permute([1,2,3]): add 1 to each→[[3,2,1],[2,3,1]]. i=1: Remove 2, permute([3,1])→[[1,3],[3,1]], add 2→[[1,3,2],[3,1,2]]'
    - ko: 'i=2: 3을 제거 → permute([1,2]) → [[2,1],[1,2]], 각각에 3 추가 → [[2,1,3],[1,2,3]]. 모두 합치면 [[3,2,1],[2,3,1],[1,3,2],[3,1,2],[2,1,3],[1,2,3]]'
      en: 'i=2: Remove 3, permute([1,2])→[[2,1],[1,2]], add 3→[[2,1,3],[1,2,3]]. Combine all: [[3,2,1],[2,3,1],[1,3,2],[3,1,2],[2,1,3],[1,2,3]]'
    answer: '[[3,2,1],[2,3,1],[1,3,2],[3,1,2],[2,1,3],[1,2,3]]'
solution:
  code: "class Solution:\n    def permute(self, nums: List[int]) -> List[List[int]]:\n        res = []\n\n        # base case\n        if len(nums) == 1:\n            return [nums[:]]  # nums[:] is a deep copy\n\n        for i in range(len(nums)):\n            n = nums.pop(0)\n            perms = self.permute(nums)\n\n            for perm in perms:\n                perm.append(n)\n            res.extend(perms)\n            nums.append(n)\n        return res\n"
  complexity:
    time: O(n! × n)
    space: O(n)
  followup:
  - ko: 반복적인 방식으로 푼다면? 스택을 사용해 재귀를 시뮬레이션하여 하향식으로 순열을 생성할 수 있습니다.
    en: Can you solve iteratively? Use a stack to simulate recursion and build permutations bottom-up
  - ko: 입력 배열에 중복이 있다면? 배열을 정렬한 후, 각 재귀 단계에서 중복 값을 건너뛰면 됩니다.
    en: If input has duplicates? Sort first, then skip duplicate values at each recursion level
  - ko: 공간을 O(1)로 줄일 수 있을까? 스왑 기반 Heap's Algorithm을 사용하되, 입력 배열을 수정해야 합니다.
    en: Can you achieve O(1) space? Yes, using swap-based Heap's Algorithm, but it modifies the input array
```
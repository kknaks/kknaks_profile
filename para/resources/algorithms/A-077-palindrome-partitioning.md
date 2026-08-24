---
created: '2026-08-03'
date: '2026-08-03'
day: Day 77
difficulty: medium
id: A-077
source:
  curated_in:
  - neetcode150
  number: 131
  platform: leetcode
  slug: palindrome-partitioning
  url: https://leetcode.com/problems/palindrome-partitioning/
tags:
- string
- dynamic-programming
- backtracking
title:
  en: Palindrome Partitioning
  ko: 팰린드롬 분할
today: false
type: algorithm
updated: '2026-08-03'
visible: true
---

# 팰린드롬 분할

## Data

```yaml
problem:
  title:
    ko: 팰린드롬 분할
    en: Palindrome Partitioning
  statement:
    en: Given a string s, partition s such that every substring of the partition is a palindrome. Return all possible palindrome partitioning of s.
    ko: 문자열 s가 주어졌을 때, s를 분할하여 분할된 모든 부분 문자열이 팰린드롬이 되도록 하세요. s의 모든 가능한 팰린드롬 분할을 반환하세요.
  constraints:
  - 1 ≤ s.length ≤ 16
  - s contains only lowercase English letters
  - Every substring in the partition must be a non-empty palindrome
  io:
  - input: '"aab"'
    output: '[[''a'',''a'',''b''],[''aa'',''b'']]'
  - input: '"a"'
    output: '[[''a'']]'
clarifying:
  items:
  - q:
      en: Do we need to return all possible partitions or just one valid partition?
      ko: 가능한 모든 분할을 반환해야 하나요, 아니면 하나의 유효한 분할만 반환해야 하나요?
    type: good
    why:
      en: The problem explicitly asks for all possible palindrome partitionings, which determines whether to use exhaustive search.
      ko: 문제에서 명시적으로 모든 가능한 팰린드롬 분할을 요구하므로, 전체 탐색을 사용해야 한다는 것을 의미합니다.
  - q:
      en: Can a substring be used multiple times in different positions of a partition?
      ko: 한 부분 문자열이 분할의 다른 위치에서 여러 번 사용될 수 있나요?
    type: good
    why:
      en: Yes, each partition divides the string sequentially, so the same character or substring can appear multiple times (e.g., 'a' appears twice in ['a','a','b']).
      ko: 네, 각 분할은 문자열을 순차적으로 나누기 때문에 같은 문자나 부분 문자열이 여러 번 나타날 수 있습니다.
  - q:
      en: Must the substrings within each partition appear in consecutive order from the original string?
      ko: 분할의 부분 문자열들이 원본 문자열에서 연속된 순서로 나타나야 하나요?
    type: good
    why:
      en: Yes, partition means we split the string into consecutive, non-overlapping segments from left to right.
      ko: 네, 분할은 문자열을 왼쪽에서 오른쪽으로 연속되고 겹치지 않는 세그먼트로 나누는 것을 의미합니다.
  - q:
      en: Can we use a greedy approach, always picking the longest palindrome first?
      ko: 탐욕적 접근을 사용하여 항상 가장 긴 팰린드롬을 먼저 선택할 수 있나요?
    type: good
    why:
      en: No, greedy fails because it misses valid partitions (e.g., 'aab' → greedy picks 'aa' then 'b', but misses ['a','a','b']).
      ko: '아니요, 탐욕적 접근은 유효한 분할을 놓칩니다 (예: ''aab'' → [''a'',''a'',''b'']를 놓침).'
  - q:
      en: Do we need to deduplicate partitions in the result?
      ko: 결과에서 중복된 분할을 제거해야 하나요?
    type: distractor
    why:
      en: No, by construction of sequential partitioning, each valid partition is inherently unique.
      ko: 아니요, 순차적 분할 구조로 인해 각 유효한 분할은 본질적으로 고유합니다.
  - q:
      en: Should we sort the partitions before returning them?
      ko: 반환하기 전에 분할들을 정렬해야 하나요?
    type: distractor
    why:
      en: The problem does not require sorting; the natural backtracking order is acceptable.
      ko: 문제에서 정렬을 요구하지 않으며, 백트래킹의 자연스러운 순서가 허용됩니다.
approach:
  items:
  - name:
      en: Backtracking with palindrome validation
      ko: 팰린드롬 검증을 통한 백트래킹
    complexity: O(N * 2^N) time / O(N) space
    type: good
    why:
      en: Explores all possible partitions (2^N branches) by recursively trying each split point. Validates palindromes on-the-fly. Space is recursion depth.
      ko: 각 분할 지점을 재귀적으로 시도하여 모든 가능한 분할(2^N)을 탐색합니다. 즉시 팰린드롬을 검증합니다.
  - name:
      en: DFS with precomputed palindrome table
      ko: 미리 계산된 팰린드롬 테이블을 통한 DFS
    complexity: O(N * 2^N) time / O(N^2) space
    type: good
    why:
      en: Precomputes all palindrome pairs (i, j) in O(N²) using DP, then uses table lookups during backtracking. Same worst-case but faster constants.
      ko: 모든 팰린드롬 쌍을 O(N²)에 미리 계산하여 백트래킹 중 O(1) 조회를 합니다.
  - name:
      en: Generate all subsets and filter
      ko: 모든 부분집합 생성 후 필터링
    complexity: O(2^N * N) time / O(2^N) space
    type: distractor
    why:
      en: Generates all 2^N ways to place separators, then validates each as a palindrome partition. Explores invalid branches without early pruning.
      ko: 모든 2^N개의 분리자 배치를 생성한 후 검증합니다. 유효하지 않은 분기를 조기에 제거하지 않습니다.
  - name:
      en: Dynamic programming bottom-up
      ko: 동적 프로그래밍 상향식
    complexity: O(N^2) time / O(N^2) space
    type: distractor
    why:
      en: DP can find the minimum number of cuts, but doesn't naturally return all partitions. The problem requires listing all solutions.
      ko: DP는 최소 분할 개수를 찾을 수 있지만, 모든 분할을 반환하는 데 자연스럽지 않습니다.
  - name:
      en: 'Greedy: always pick longest palindrome'
      ko: '탐욕적: 항상 가장 긴 팰린드롬 선택'
    complexity: O(N^2) time / O(N) space
    type: distractor
    why:
      en: 'Fast but incomplete: misses valid partitions by committing to greedy choices. E.g., ''aab'' skips [''a'',''a'',''b''] in favor of [''aa'',''b''].'
      ko: 빠르지만 불완전합니다. 탐욕적 선택으로 유효한 분할을 놓칩니다.
logic:
  format: slot
  slots:
  - label:
      en: Initialize result list and current partition
      ko: 결과 리스트 및 현재 분할 초기화
    indent: 0
    options:
    - code: res, part = [], []
      type: good
      why:
        en: res stores all completed valid partitions; part tracks the partition being built during recursion.
        ko: res는 모든 완성된 유효한 분할을 저장하고, part는 재귀 중 구축 중인 분할을 추적합니다.
    - code: res = {}; part = {}
      type: distractor
      why:
        en: Dictionaries require keys for insertion; we need to append substrings, making lists more natural.
        ko: 딕셔너리는 삽입 시 키가 필요하므로 리스트가 더 자연스럽습니다.
    - code: res = []; part = None
      type: distractor
      why:
        en: Setting part to None prevents appending substrings during partition building.
        ko: part를 None으로 설정하면 분할 구축 중 부분 문자열을 추가할 수 없습니다.
  - label:
      en: 'Base case: check if entire string is partitioned'
      ko: '기저 사례: 전체 문자열이 분할되었는지 확인'
    indent: 1
    options:
    - code: 'if i >= len(s):'
      type: good
      why:
        en: When i reaches len(s), we have successfully partitioned the entire string into palindromes.
        ko: i가 len(s)에 도달했을 때, 전체 문자열을 팰린드롬으로 분할했습니다.
    - code: 'if i > len(s):'
      type: distractor
      why:
        en: Using > instead of >= skips the exact endpoint, potentially missing valid partitions.
        ko: '> 를 사용하면 정확한 끝점을 건너뛰어 유효한 분할을 놓칠 수 있습니다.'
    - code: 'if i == len(s) - 1:'
      type: distractor
      why:
        en: This only triggers at the last character position, not when all characters are partitioned.
        ko: 이는 마지막 문자 위치에서만 트리거되며, 모든 문자가 분할된 후가 아닙니다.
  - label:
      en: Record the valid partition
      ko: 유효한 분할 기록
    indent: 2
    options:
    - code: res.append(part.copy())
      type: good
      why:
        en: Use part.copy() to save a snapshot; part itself will be modified by backtracking.
        ko: part.copy()를 사용하여 스냅샷을 저장합니다. part는 백트래킹으로 수정됩니다.
    - code: res.append(part)
      type: distractor
      why:
        en: Appending without copy means all res entries point to the same list, which changes during backtracking.
        ko: 복사 없이 추가하면 res의 모든 항목이 같은 리스트를 가리키며, 백트래킹 시 변경됩니다.
    - code: res += [part]
      type: distractor
      why:
        en: Same issue as append(part)—no copy is made, leading to aliasing bugs.
        ko: append(part)와 같은 문제입니다.
  - label:
      en: Try all possible next partition endpoints
      ko: 다음 분할 끝점의 모든 가능성 시도
    indent: 1
    options:
    - code: 'for j in range(i, len(s)):'
      type: good
      why:
        en: Loop from i to len(s) enumerates all substrings starting at i as potential partition segments.
        ko: i에서 len(s)까지의 루프는 위치 i에서 시작하는 모든 부분 문자열을 열거합니다.
    - code: 'for j in range(i + 1, len(s)):'
      type: distractor
      why:
        en: Starting from i+1 skips single-character substrings at position i, which are always palindromes.
        ko: i+1에서 시작하면 위치 i의 단일 문자를 건너뜁니다(항상 팰린드롬).
    - code: 'for j in range(0, len(s)):'
      type: distractor
      why:
        en: Starting from 0 re-examines already-processed substrings, wasting computation.
        ko: 0에서 시작하면 이미 처리한 부분 문자열을 재검토하여 계산을 낭비합니다.
  - label:
      en: Validate substring is a palindrome
      ko: 부분 문자열이 팰린드롬인지 확인
    indent: 2
    options:
    - code: 'if self.isPali(s, i, j):'
      type: good
      why:
        en: Only proceed if s[i:j+1] is a palindrome; this prunes invalid branches early in the search tree.
        ko: s[i:j+1]이 팰린드롬인 경우에만 진행합니다. 이는 탐색 트리에서 유효하지 않은 분기를 조기에 제거합니다.
    - code: 'if s[i:j]:'
      type: distractor
      why:
        en: This only checks if the substring is non-empty, not whether it's a palindrome.
        ko: 이는 부분 문자열이 비어있지 않은지만 확인하며, 팰린드롬 여부를 확인하지 않습니다.
    - code: 'if i < j:'
      type: distractor
      why:
        en: This only ensures the range is valid; it doesn't verify the substring is palindromic.
        ko: 이는 범위의 유효성만 보장하며, 팰린드롬 여부를 확인하지 않습니다.
  - label:
      en: Add substring to partition and explore further
      ko: 부분 문자열을 분할에 추가하고 계속 탐색
    indent: 3
    options:
    - code: 'part.append(s[i : j + 1])'
      type: good
      why:
        en: Add the palindromic substring to the current partition, then recursively partition the remaining string starting from j+1.
        ko: 팰린드롬 부분 문자열을 현재 분할에 추가한 후, j+1부터 나머지를 재귀적으로 분할합니다.
    - code: 'part.append(s[i : j])'
      type: distractor
      why:
        en: Using s[i:j] excludes the character at index j, truncating the palindrome.
        ko: s[i:j]는 인덱스 j의 문자를 제외하여 팰린드롬을 자릅니다.
    - code: 'part.append(s[i : j + 1]); dfs(j)'
      type: distractor
      why:
        en: Calling dfs(j) instead of dfs(j+1) causes overlapping partitions and infinite loops.
        ko: dfs(j+1) 대신 dfs(j)를 호출하면 분할이 겹치고 무한 루프가 발생합니다.
  - label:
      en: Backtrack by removing the last added substring
      ko: 마지막 추가한 부분 문자열 제거로 백트래킹
    indent: 3
    options:
    - code: part.pop()
      type: good
      why:
        en: After exploring all partitions with the current substring, remove it to try alternative partitions at this position.
        ko: 현재 부분 문자열로 모든 분할을 탐색한 후, 이 위치에서 대안을 시도하기 위해 제거합니다.
    - code: part.clear()
      type: distractor
      why:
        en: Clearing the entire list destroys previous choices and breaks the recursion structure.
        ko: 전체 리스트를 지우면 이전 선택이 삭제되고 재귀 구조가 깨집니다.
    - code: part = part[:-1]
      type: distractor
      why:
        en: Reassigning part creates a new local variable and doesn't modify the list used by recursion.
        ko: part를 재할당하면 새 로컬 변수를 만들며, 재귀에서 사용하는 리스트를 수정하지 않습니다.
trace:
  code:
  - 'class Solution:'
  - '    def partition(self, s: str) -> List[List[str]]:'
  - '        res, part = [], []'
  - ''
  - '        def dfs(i):'
  - '            if i >= len(s):'
  - '                res.append(part.copy())'
  - '                return'
  - '            for j in range(i, len(s)):'
  - '                if self.isPali(s, i, j):'
  - '                    part.append(s[i : j + 1])'
  - '                    dfs(j + 1)'
  - '                    part.pop()'
  - ''
  - '        dfs(0)'
  - '        return res'
  - ''
  - '    def isPali(self, s, l, r):'
  - '        while l < r:'
  - '            if s[l] != s[r]:'
  - '                return False'
  - '            l, r = l + 1, r - 1'
  - '        return True'
  cases:
  - input: '"aab"'
    expected: '[[''a'',''a'',''b''],[''aa'',''b'']]'
  - input: '"a"'
    expected: '[[''a'']]'
  worked_example:
    input: '"aab"'
    steps:
    - en: Start dfs(0). Substring 'a' (s[0:1]) is a palindrome. Add 'a' to part → ['a'], call dfs(1).
      ko: dfs(0) 시작. 부분 문자열 'a' (s[0:1])는 팰린드롬. part에 추가 → ['a'], dfs(1) 호출.
    - en: 'dfs(1): ''a'' (s[1:2]) is palindrome, add ''a'' → [''a'',''a''], call dfs(2). dfs(2): ''b'' (s[2:3]) is palindrome, add ''b'' → [''a'',''a'',''b''], call dfs(3). Base case (i=3 ≥ 3): record [''a'',''a'',''b''] to res.'
      ko: 'dfs(1): ''a''는 팰린드롬, 추가 → [''a'',''a''], dfs(2) 호출. ''b''는 팰린드롬, 추가 → [''a'',''a'',''b''], dfs(3). 기저 사례: res에 [''a'',''a'',''b''] 기록.'
    - en: 'Backtrack to dfs(1). Try ''ab'' (s[1:3]): not a palindrome, skip. Backtrack to dfs(0). Try ''aa'' (s[0:2]): palindrome, add ''aa'' → [''aa''], call dfs(2).'
      ko: 'dfs(1)로 백트래킹. ''ab''는 팰린드롬 아님, 스킵. dfs(0)로: ''aa''는 팰린드롬, 추가 → [''aa''], dfs(2) 호출.'
    - en: 'dfs(2): ''b'' is palindrome, add ''b'' → [''aa'',''b''], call dfs(3). Base case: record [''aa'',''b''] to res. Final result: [[''a'',''a'',''b''], [''aa'',''b'']].'
      ko: 'dfs(2): ''b''는 팰린드롬, 추가 → [''aa'',''b''], dfs(3). 기저 사례: res에 [''aa'',''b''] 기록. 최종 결과: [[''a'',''a'',''b''], [''aa'',''b'']].'
    answer: '[[''a'',''a'',''b''], [''aa'',''b'']]'
solution:
  code: "class Solution:\n    def partition(self, s: str) -> List[List[str]]:\n        res, part = [], []\n\n        def dfs(i):\n            if i >= len(s):\n                res.append(part.copy())\n                return\n            for j in range(i, len(s)):\n                if self.isPali(s, i, j):\n                    part.append(s[i : j + 1])\n                    dfs(j + 1)\n                    part.pop()\n\n        dfs(0)\n        return res\n\n    def isPali(self, s, l, r):\n        while l < r:\n            if s[l] != s[r]:\n                return False\n            l, r = l + 1, r - 1\n        return True\n"
  complexity:
    time: O(N * 2^N)
    space: O(N)
  followup:
  - en: How would you optimize for repeated queries on the same string? (Precompute a 2D palindrome table in O(N²) to replace isPali() calls with O(1) lookups.)
    ko: 같은 문자열에 대한 반복 쿼리를 최적화하려면? (2D 팰린드롬 테이블을 O(N²)에 미리 계산하여 O(1) 조회 사용)
  - en: 'What if instead of all partitions, you needed the minimum number of cuts to partition into palindromes? (Use DP: dp[i] = min cuts for s[0:i]; reconstruct path if needed.)'
    ko: 모든 분할 대신 팰린드롬으로 분할하는 최소 자르기 개수가 필요하면? (dp[i] = s[0:i]의 최소 자르기 수 사용)
  - en: Can you modify the solution to return partitions in lexicographic order? (Sort the result list after generation, or explore branches in sorted order during recursion.)
    ko: 분할을 사전식 순서로 반환하도록 수정할 수 있나요? (생성 후 결과 정렬 또는 재귀 중 정렬된 순서로 탐색)
```
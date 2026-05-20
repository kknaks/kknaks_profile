---
created: '2026-05-20'
date: '2026-05-20'
day: Day 18
difficulty: medium
id: A-018
source:
  curated_in:
  - neetcode150
  number: 567
  platform: leetcode
  slug: permutation-in-string
  url: https://leetcode.com/problems/permutation-in-string/
status: draft
tags:
- hash-table
- two-pointers
- string
- sliding-window
title:
  en: Permutation in String
  ko: 문자열의 순열
today: true
type: algorithm
updated: '2026-05-20'
visible: true
---

# 문자열의 순열

## Data

```yaml
problem:
  title:
    ko: 문자열의 순열
    en: Permutation in String
  statement:
    ko: 두 문자열 s1과 s2가 주어질 때, s2가 s1의 순열을 부분문자열로 포함하면 true를, 그렇지 않으면 false를 반환하세요. 다시 말해, s1의 순열 중 하나가 s2의 부분문자열이면 true를 반환하세요.
    en: Given two strings s1 and s2, return true if s2 contains a permutation of s1, or false otherwise. In other words, return true if one of s1's permutations is the substring of s2.
  constraints:
  - 1 ≤ s1.length, s2.length ≤ 10⁴
  - s1 and s2 consist of lowercase English letters
  io:
  - input: '"ab"

      "eidbaooo"'
    output: 'true'
  - input: '"ab"

      "eidboaoo"'
    output: 'false'
clarifying:
  items:
  - q:
      ko: 순열(permutation)은 문자의 순서가 중요한가요?
      en: Does order matter in a permutation?
    type: good
    why:
      ko: 순열은 같은 문자의 모든 가능한 배열을 의미합니다. 순서는 상관없고, 각 문자의 빈도가 같아야 합니다.
      en: A permutation is any rearrangement of the same characters. Order doesn't matter; character frequencies must match.
  - q:
      ko: 왜 두 개의 frequency 배열을 사용해야 하나요?
      en: Why maintain two separate frequency arrays?
    type: good
    why:
      ko: 하나는 s1의 고정된 빈도를 저장하고, 다른 하나는 슬라이딩 윈도우의 변하는 빈도를 저장합니다. 이 둘을 비교해서 순열을 찾습니다.
      en: One tracks s1's constant frequencies; the other tracks the sliding window in s2. We compare them to find a match.
  - q:
      ko: matches 변수는 정확히 무엇을 세나요?
      en: What does the 'matches' variable count?
    type: good
    why:
      ko: s1과 현재 윈도우에서 같은 빈도를 가진 문자의 개수입니다. matches가 26이 되면 모든 문자 빈도가 일치해서 순열을 발견한 것입니다.
      en: The number of characters where both frequencies are equal. When matches reaches 26, all characters match—we found a permutation.
  - q:
      ko: 왜 루프를 len(s1)부터 시작하나요?
      en: Why does the main loop start at r = len(s1)?
    type: good
    why:
      ko: 처음 len(s1)개 문자는 이미 s2Count에 포함되어 있고, matches도 계산했습니다. 이제 오른쪽 끝을 추가하고 왼쪽을 제거하며 슬라이드합니다.
      en: The first len(s1) characters are already in s2Count and matches is calculated. Now we slide by adding right and removing left.
  - q:
      ko: 정렬을 사용하면 더 빠를까요?
      en: Would sorting each substring be faster?
    type: distractor
    why:
      ko: 아니요, 정렬은 O(n·m·log m) 시간이 필요합니다. 슬라이딩 윈도우의 O(n)이 훨씬 빠릅니다.
      en: No, sorting each substring would be O(n·m·log m). Sliding window is O(n)—much faster.
  - q:
      ko: 조기 종료 조건 if matches == 26이 반드시 필요한가요?
      en: Is the early exit 'if matches == 26' strictly necessary?
    type: distractor
    why:
      ko: 기술적으로는 루프 끝의 return matches == 26만으로도 충분합니다. 조기 종료는 평균 성능만 개선할 뿐 최악의 경우를 바꾸지 않습니다.
      en: The final return already checks this. Early exit is an optimization that helps average cases but doesn't change worst-case complexity.
  - q:
      ko: 만약 s1 = 'ab'이고 s2 = 'aba'라면, 결과는?
      en: If s1 = 'ab' and s2 = 'aba', should the function return true?
    type: distractor
    why:
      ko: 예, true입니다. 위치 1~2의 부분문자열 'ba'가 'ab'의 순열입니다.
      en: Yes, true. The substring 'ba' (positions 1–2) is a permutation of 'ab'.
approach:
  items:
  - name:
      ko: 배열 기반 슬라이딩 윈도우 빈도 계산
      en: Sliding Window with Array Frequency Counting
    complexity: O(n) time / O(1) space
    type: good
    why:
      ko: 소문자 26개로 고정된 문자 집합이므로 상수 크기 배열로 O(1) 공간에 풀 수 있습니다. 슬라이딩 윈도우로 단일 패스에 O(n) 시간 달성.
      en: Fixed 26-letter alphabet allows constant-space arrays. Sliding window with match counter updates gives O(n) single pass—optimal.
  - name:
      ko: 해시맵 기반 슬라이딩 윈도우
      en: Sliding Window with Hash Map
    complexity: O(n) time / O(k) space
    type: good
    why:
      ko: 임의의 문자 집합에 적용 가능하고 O(n)에 풀 수 있습니다. 배열보다 유연하지만 해시맵 오버헤드로 약간 느립니다.
      en: Works for any character set and runs in O(n). More flexible than arrays but slower due to hash map overhead.
  - name:
      ko: 전체 순열 생성 (무차별 탐색)
      en: 'Brute Force: Generate All Permutations'
    complexity: O(m! × n) time / O(m!) space
    type: distractor
    why:
      ko: s1의 모든 m! 순열을 생성 후 각각 s2에 있는지 확인합니다. 지수 시간 복잡도로 TLE 확정입니다.
      en: Generate all m! permutations, check each in s2. Exponential time—guaranteed TLE for reasonable inputs.
  - name:
      ko: 정렬 기반 부분문자열 비교
      en: 'Sorting-Based: Compare Sorted Substrings'
    complexity: O(n·m·log m) time / O(m) space
    type: distractor
    why:
      ko: 각 부분문자열을 정렬해서 정렬된 s1과 비교합니다. 반복 정렬 비용으로 O(n) 슬라이딩 윈도우보다 훨씬 느립니다.
      en: Sort s1, then for each substring of s2, sort and compare. Repeated sorting makes it slower than O(n) sliding window.
  - name:
      ko: 이중 루프 부분문자열 확인
      en: 'Nested Loop: Character Counting'
    complexity: O(n·m) time / O(1) space
    type: distractor
    why:
      ko: 각 시작 위치마다 m개 문자를 세어서 빈도 비교합니다. O(n×m)으로 O(n) 최적 풀이보다 느립니다.
      en: For each position, count m characters. O(n×m) is slower than O(n) sliding window.
logic:
  format: slot
  slots:
  - label:
      ko: 길이 검사 - 불가능한 경우 제거
      en: 'Boundary Check: Length Validation'
    indent: 0
    options:
    - code: 'if len(s1) > len(s2):'
      type: good
      why:
        ko: s1이 s2보다 길면 어떤 부분문자열도 s1의 순열이 될 수 없으므로 false를 반환합니다.
        en: If s1 is longer than s2, no substring of s2 can be a permutation of s1. Return false immediately.
    - code: 'if len(s1) >= len(s2):'
      type: distractor
      why:
        ko: '>= 연산자는 잘못되었습니다. 길이가 같으면 문자열 전체가 순열인지 확인해야 합니다.'
        en: Wrong operator. Length equality is possible (e.g., 'ab' vs 'ba').
    - code: 'if len(s1) < len(s2): return False'
      type: distractor
      why:
        ko: 비교 연산자가 반대입니다. s1이 더 짧을 때 계속 진행해야 합니다.
        en: Logic is inverted. We proceed when s1 is shorter.
  - label:
      ko: 빈도 배열 초기화 및 첫 윈도우 채우기
      en: Initialize Frequency Arrays and First Window
    indent: 0
    options:
    - code: s1Count, s2Count = [0] * 26, [0] * 26
      type: good
      why:
        ko: 26개 문자의 빈도를 추적하는 두 배열을 만듭니다. s1의 빈도와 s2의 처음 len(s1)개 문자 빈도를 저장합니다.
        en: Create two 26-element arrays to track each character's count. Fill with frequencies from s1 and the first len(s1) chars of s2.
    - code: s1Count, s2Count = [0] * 25, [0] * 25
      type: distractor
      why:
        ko: 크기 25는 부족합니다. 'z' 문자를 추적할 수 없습니다.
        en: Size 25 misses 'z' (the 26th letter).
    - code: 's1Count = [0] * 26  # s2Count는 없음'
      type: distractor
      why:
        ko: s2의 윈도우를 추적할 배열이 없으면 비교할 수 없습니다.
        en: Without s2Count, we can't compare frequencies.
  - label:
      ko: 초기 일치 횟수 계산
      en: Count Initial Character Matches
    indent: 1
    options:
    - code: matches += 1 if s1Count[i] == s2Count[i] else 0
      type: good
      why:
        ko: s1과 첫 윈도우에서 같은 빈도를 가진 문자의 개수를 센다. 이 값은 윈도우가 슬라이드될 때마다 업데이트됩니다.
        en: Count how many of 26 characters have equal frequency in s1 and the initial window. This variable will be incremented/decremented as we slide.
    - code: matches += 1 if s1Count[i] != s2Count[i] else 0
      type: distractor
      why:
        ko: 비교 연산자가 반대입니다. 일치하는 경우(==)를 세어야 합니다.
        en: 'Inverted: != counts mismatches, not matches.'
    - code: '# 초기 matches 계산을 건너뜀'
      type: distractor
      why:
        ko: 초기 matches를 모르면 슬라이딩 중 changes를 추적할 수 없습니다.
        en: Can't track match changes if we don't know the initial state.
  - label:
      ko: 슬라이딩 윈도우 메인 루프
      en: Main Sliding Window Loop
    indent: 0
    options:
    - code: 'for r in range(len(s1), len(s2)):'
      type: good
      why:
        ko: r을 len(s1)부터 len(s2)까지 반복합니다. 각 반복에서 오른쪽에 새 문자를 추가하고 왼쪽에서 문자를 제거합니다.
        en: Iterate r from len(s1) to len(s2). Each iteration adds a character on the right and removes one on the left.
    - code: 'for r in range(len(s1)):'
      type: distractor
      why:
        ko: 범위가 너무 좁습니다. 처음 len(s1)개는 이미 세었으므로, len(s1)부터 슬라이드를 시작해야 합니다.
        en: Range is too small. We already counted the first len(s1) chars; we start sliding from there.
    - code: 'for r in range(len(s2)):'
      type: distractor
      why:
        ko: 범위가 너무 넓습니다. 처음 len(s1)-1은 초기화 루프에서 이미 세었습니다.
        en: Range includes the initial window again, causing duplicate counting.
  - label:
      ko: 오른쪽 끝 문자 추가 및 일치 횟수 업데이트
      en: Add Character at Right and Update Matches
    indent: 1
    options:
    - code: s2Count[index] += 1
      type: good
      why:
        ko: 위치 r의 문자를 s2Count에 추가합니다. 그 후 s1Count[index]와 새로운 s2Count[index]를 비교하여 matches를 조정합니다.
        en: Increment s2Count for character at r. Then check if this makes the frequency equal or unequal to s1, adjusting matches.
    - code: s2Count[ord(s2[r]) - ord('a')] += 1
      type: distractor
      why:
        ko: 문자는 추가하지만 matches는 업데이트하지 않으므로 일치 상태 변화를 추적할 수 없습니다.
        en: Adds character but doesn't update matches; frequency changes go untracked.
    - code: "if s1Count[index] == s2Count[index] - 1:\n    matches += 1\ns2Count[index] += 1"
      type: distractor
      why:
        ko: 비교 순서가 잘못되었습니다. 증가 후에 비교해야 정확합니다.
        en: Checks before incrementing, comparing wrong values.
  - label:
      ko: 왼쪽 끝 문자 제거 및 일치 횟수 업데이트
      en: Remove Character at Left and Update Matches
    indent: 1
    options:
    - code: s2Count[index] -= 1
      type: good
      why:
        ko: 위치 l의 문자를 s2Count에서 제거합니다. 그 후 s1Count[index]와 새로운 s2Count[index]를 비교하여 matches를 조정합니다. 마지막으로 l을 증가시킵니다.
        en: Decrement s2Count for character at l. Check if this changes the match status. Then increment l to slide the window forward.
    - code: 's2Count[ord(s2[l]) - ord(''a'')] -= 1

        l += 1'
      type: distractor
      why:
        ko: 문자는 제거하지만 matches는 업데이트하지 않으므로 일치 상태 변화를 추적할 수 없습니다.
        en: Removes character but doesn't update matches; misses frequency changes.
    - code: 's2Count[ord(s2[l]) - ord(''a'')] -= 1

        # l += 1이 없음'
      type: distractor
      why:
        ko: l이 증가하지 않으면 윈도우가 슬라이드되지 않고 같은 문자가 반복적으로 제거됩니다.
        en: Without incrementing l, the window doesn't slide; same position is reprocessed.
trace:
  code:
  - 'class Solution:'
  - '    def checkInclusion(self, s1: str, s2: str) -> bool:'
  - '        if len(s1) > len(s2):'
  - '            return False'
  - ''
  - '        s1Count, s2Count = [0] * 26, [0] * 26'
  - '        for i in range(len(s1)):'
  - '            s1Count[ord(s1[i]) - ord("a")] += 1'
  - '            s2Count[ord(s2[i]) - ord("a")] += 1'
  - ''
  - '        matches = 0'
  - '        for i in range(26):'
  - '            matches += 1 if s1Count[i] == s2Count[i] else 0'
  - ''
  - '        l = 0'
  - '        for r in range(len(s1), len(s2)):'
  - '            if matches == 26:'
  - '                return True'
  - ''
  - '            index = ord(s2[r]) - ord("a")'
  - '            s2Count[index] += 1'
  - '            if s1Count[index] == s2Count[index]:'
  - '                matches += 1'
  - '            elif s1Count[index] + 1 == s2Count[index]:'
  - '                matches -= 1'
  - ''
  - '            index = ord(s2[l]) - ord("a")'
  - '            s2Count[index] -= 1'
  - '            if s1Count[index] == s2Count[index]:'
  - '                matches += 1'
  - '            elif s1Count[index] - 1 == s2Count[index]:'
  - '                matches -= 1'
  - '            l += 1'
  - '        return matches == 26'
  cases:
  - input: '"ab"

      "eidbaooo"'
    expected: 'true'
  - input: '"ab"

      "eidboaoo"'
    expected: 'false'
  worked_example:
    input: '"ab"

      "eidbaooo"'
    steps:
    - ko: '길이 검사: len(''ab'')=2 ≤ len(''eidbaooo'')=8이므로 계속. 빈도 배열 초기화: s1Count에 a→1, b→1 저장. s2의 첫 2자 ''ei''로 s2Count 초기화: e→1, i→1.'
      en: 'Length check: 2 ≤ 8 ✓. Initialize: s1Count[a]=1, s1Count[b]=1. s2Count from ''ei'': e=1, i=1.'
    - ko: '초기 matches 계산: s1Count[i] == s2Count[i]인 경우는 a, b, e, i를 제외한 모든 문자(24개). matches = 24.'
      en: 'Count initial matches: all except a, b, e, i are equal (both 0). matches = 24.'
    - ko: 슬라이딩 시작. r=2,3일 때 matches=24 유지. r=4일 때 s2[4]='a'를 추가하면 a→1이 되어 s1Count[a]=s2Count[a]. r=4일 때 s2[0]='e'를 제거하면 e→0이 되어 s1Count[e]=s2Count[e]. 이제 matches=26.
      en: 'Slide window: at r=4, add ''a'' (now s2Count[a]=1 matches s1Count[a]=1). Remove ''e'' (now s2Count[e]=0 matches s1Count[e]=0). matches=26.'
    - ko: matches == 26이므로 true를 반환합니다.
      en: matches reaches 26 → return true.
    answer: 'true'
solution:
  code: "class Solution:\n    def checkInclusion(self, s1: str, s2: str) -> bool:\n        if len(s1) > len(s2):\n            return False\n\n        s1Count, s2Count = [0] * 26, [0] * 26\n        for i in range(len(s1)):\n            s1Count[ord(s1[i]) - ord(\"a\")] += 1\n            s2Count[ord(s2[i]) - ord(\"a\")] += 1\n\n        matches = 0\n        for i in range(26):\n            matches += 1 if s1Count[i] == s2Count[i] else 0\n\n        l = 0\n        for r in range(len(s1), len(s2)):\n            if matches == 26:\n                return True\n\n            index = ord(s2[r]) - ord(\"a\")\n            s2Count[index] += 1\n            if s1Count[index] == s2Count[index]:\n                matches += 1\n            elif s1Count[index] + 1 == s2Count[index]:\n                matches -= 1\n\n            index = ord(s2[l]) - ord(\"a\")\n            s2Count[index] -= 1\n            if s1Count[index] == s2Count[index]:\n                matches += 1\n            elif s1Count[index] - 1 ==\
    \ s2Count[index]:\n                matches -= 1\n            l += 1\n        return matches == 26\n"
  complexity:
    time: O(n) where n = len(s2)
    space: O(1) (two fixed-size arrays of 26)
  followup:
  - ko: 유니코드나 여러 언어의 문자를 포함할 수 있도록 일반화하려면 어떻게 수정해야 할까요?
    en: How would you generalize this for Unicode characters or any character set, not just lowercase English?
  - ko: s2에서 발견된 순열의 시작 인덱스를 반환하도록 수정할 수 있을까요?
    en: Modify the algorithm to return the starting index of the first permutation found in s2.
  - ko: matches 변수 대신 두 배열을 매 반복마다 직접 비교하면 어떨까요? 시간/공간 트레이드오프를 분석해보세요.
    en: Instead of matches, what if you compared the arrays directly each iteration? Analyze the time/space tradeoffs.
```
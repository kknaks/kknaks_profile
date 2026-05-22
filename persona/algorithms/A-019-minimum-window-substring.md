---
created: '2026-05-21'
date: '2026-05-21'
day: Day 19
difficulty: hard
id: A-019
source:
  curated_in:
  - neetcode150
  number: 76
  platform: leetcode
  slug: minimum-window-substring
  url: https://leetcode.com/problems/minimum-window-substring/
status: draft
tags:
- hash-table
- string
- sliding-window
title:
  en: Minimum Window Substring
  ko: 최소 윈도우 부분문자열
today: false
type: algorithm
updated: '2026-05-21'
visible: true
---

# 최소 윈도우 부분문자열

## Data

```yaml
problem:
  title:
    ko: 최소 윈도우 부분문자열
    en: Minimum Window Substring
  statement:
    ko: '길이가 각각 m과 n인 두 문자열 s와 t가 주어졌을 때, t의 모든 문자(중복 포함)를 포함하는 s의 최소 윈도우 부분문자열을 반환하세요. 그러한 부분문자열이 없으면 빈 문자열 ""을 반환하세요.


      테스트 케이스는 답이 유일하도록 생성됩니다.'
    en: 'Given two strings s and t of lengths m and n respectively, return the minimum window substring of s such that every character in t (including duplicates) is included in the window. If there is no such substring, return the empty string "".


      The testcases will be generated such that the answer is unique.'
  constraints:
  - 1 ≤ m, n ≤ 10^5 (lengths of s and t)
  - s and t consist of uppercase and lowercase English letters
  - Answer is guaranteed to be unique
  io:
  - input: '"ADOBECODEBANC"

      "ABC"'
    output: BANC
  - input: '"a"

      "a"'
    output: a
  - input: '"a"

      "aa"'
    output: ''
clarifying:
  items:
  - q:
      ko: t에 없는 문자가 s에 포함되어 있으면 어떻게 되나요?
      en: What if s contains characters not in t?
    type: good
    why:
      ko: 그러한 문자들은 윈도우의 일부가 될 수 있지만, 요구사항을 충족하는 데는 영향을 주지 않습니다. 오직 t의 문자만 중요합니다.
      en: Those characters can be part of the window but do not count toward meeting the requirement. Only characters in t matter for validation.
  - q:
      ko: 결과가 빈 문자열일 수 있나요?
      en: Can the result be an empty string?
    type: good
    why:
      ko: 네, s가 t의 모든 문자를 포함하지 못하면 (또는 s가 너무 짧으면) 빈 문자열을 반환합니다.
      en: Yes, if no valid window exists (e.g., t contains characters absent from s, or s is shorter than t), return empty string.
  - q:
      ko: 문자의 정확한 빈도를 일치시켜야 하나요?
      en: Must we match exact character frequencies?
    type: good
    why:
      ko: '네, t의 각 문자는 윈도우에서 최소 t에서의 빈도만큼 나타나야 합니다. 예: t="AA"면 윈도우에 최소 2개의 A가 필요합니다.'
      en: 'Yes, every character in t must appear in the window with at least the same frequency. Example: if t="AA", the window must contain at least 2 A''s.'
  - q:
      ko: 가능한 모든 부분문자열을 확인해야 하나요?
      en: Should we check all possible substrings?
    type: distractor
    why:
      ko: 아니오. O(n²) 이상의 복잡도가 필요하기 때문에 비효율적입니다. 슬라이딩 윈도우 접근은 O(m+n) 시간 안에 해결합니다.
      en: No, that would be O(n²) or worse. The sliding window approach solves it efficiently in O(m+n) time.
  - q:
      ko: t에 속하지 않은 s의 모든 문자를 추적해야 하나요?
      en: Must we track all characters in s, even those not in t?
    type: distractor
    why:
      ko: 아니오. 'have' 카운터에는 t의 문자만 영향을 줍니다. t에 없는 문자는 윈도우에 포함될 수 있지만 요구사항 충족에는 영향을 주지 않습니다.
      en: No, only characters in t matter for the 'have' counter. Characters not in t can be in the window but don't help satisfy requirements.
  - q:
      ko: t가 s보다 길면 어떻게 되나요?
      en: What if t is longer than s?
    type: good
    why:
      ko: 즉시 빈 문자열을 반환합니다. 유효한 윈도우가 존재할 수 없기 때문입니다.
      en: Return empty string immediately. No valid window can exist.
  - q:
      ko: '''have'' 변수는 무엇을 나타내나요?'
      en: What does the 'have' variable represent?
    type: good
    why:
      ko: '''have''는 윈도우에서 올바른 빈도를 갖춘 t의 고유 문자 개수입니다. need에 도달하면 윈도우가 유효합니다.'
      en: '''have'' counts the number of unique characters in t that have reached their required frequency in the window. When have equals need, the window is valid.'
approach:
  items:
  - name:
      ko: 슬라이딩 윈도우 (두 포인터) + 해시맵
      en: Sliding Window (two-pointer) + Hash Maps
    complexity: O(m + n) time / O(1) space
    type: good
    why:
      ko: 오른쪽 포인터로 확장하여 유효한 윈도우를 찾고, 왼쪽 포인터로 축소하여 최소화합니다. 각 포인터는 s를 최대 한 번씩 순회합니다. 공간은 최대 52개 문자(영문 대소문자)로 상수입니다.
      en: Expand right to find a valid window, contract left to minimize it. Each pointer traverses s once. Space is O(1) since we store at most 52 unique characters (26 lowercase + 26 uppercase).
  - name:
      ko: '브루트 포스: 모든 부분문자열 확인'
      en: 'Brute Force: Check All Substrings'
    complexity: O(m²·n) time / O(n) space
    type: distractor
    why:
      ko: 각 부분문자열에 대해 t의 모든 문자가 포함되었는지 확인합니다. 매우 느립니다.
      en: For each substring, check if it contains all of t's characters. Extremely slow for large inputs.
  - name:
      ko: 해시맵 (확장만 사용)
      en: Hash Map (Expansion Only)
    complexity: O(m) time / O(1) space
    type: distractor
    why:
      ko: 오른쪽으로만 확장하면 윈도우를 최소화할 수 없습니다. 최소값을 찾으려면 좌측 축소가 필수입니다.
      en: Expanding right only cannot minimize the window. Left contraction is necessary to find the minimum.
  - name:
      ko: 슬라이딩 윈도우 + 결과 최적화
      en: Sliding Window with Result Tracking
    complexity: O(m + n) time / O(1) space
    type: good
    why:
      ko: 접근 1과 동일합니다. 윈도우 확장, 축소, 결과 추적을 결합하는 최선의 방법입니다.
      en: Same as Approach 1. Combines window expansion, contraction, and result tracking—the optimal solution.
  - name:
      ko: t의 고유 문자에 대한 중첩 루프
      en: Nested Loops on Unique Characters
    complexity: O(m·|unique(t)|) time
    type: distractor
    why:
      ko: 여전히 비효율적입니다. 겹치는 범위를 반복해서 확인해야 하므로 슬라이딩 윈도우보다 느립니다.
      en: Still inefficient; rechecks overlapping ranges repeatedly. Slower than sliding window.
logic:
  format: slot
  slots:
  - label:
      ko: 기본 경우 확인
      en: Early Termination Check
    indent: 0
    options:
    - code: 'if len(s) < len(t):'
      type: good
      why:
        ko: s가 t보다 짧으면 유효한 윈도우가 존재할 수 없으므로 즉시 빈 문자열을 반환합니다.
        en: If s is shorter than t, no valid window can exist. Immediate return avoids unnecessary work.
    - code: 'if len(s) == len(t): return ""'
      type: distractor
      why:
        ko: 너무 제한적입니다. 길이가 같은 경우는 유효할 수 있습니다.
        en: Too restrictive; s can have the same length as t and still contain a valid window.
    - code: 'if len(t) == 0: return s'
      type: distractor
      why:
        ko: 잘못됨. 빈 t에 대해서는 빈 문자열을 반환해야 합니다.
        en: Wrong; empty t should return empty string, not s.
    - code: 'if len(s) > len(t) * 2: continue'
      type: distractor
      why:
        ko: 임의의 조건이며 필요 없습니다.
        en: Arbitrary condition; not needed.
  - label:
      ko: 목표 문자 빈도 맵 구성
      en: Build Target Frequency Map
    indent: 0
    options:
    - code: countT[c] = 1 + countT.get(c, 0)
      type: good
      why:
        ko: t의 각 문자가 정확히 몇 번 나타나는지 저장합니다. 이것이 유효한 윈도우가 충족해야 할 기준입니다.
        en: Stores the frequency of each character in t. This defines what the window must contain to be valid.
    - code: countT = set(t)
      type: distractor
      why:
        ko: 중복 정보가 손실됩니다. 'AB'와 'AAB'를 구별할 수 없습니다.
        en: Loses frequency information; cannot distinguish 'AB' from 'AAB'.
    - code: countT[c] = 1
      type: distractor
      why:
        ko: '덮어쓰기 때문에 중복을 잃습니다. ''AA''를 {''A'': 1}로 계산합니다.'
        en: 'Overwrites instead of accumulating; ''AA'' becomes {''A'': 1} incorrectly.'
    - code: 'countT = {c: 1 for c in set(t)}'
      type: distractor
      why:
        ko: 중복을 무시하므로 'AAB'의 A 빈도가 2가 아닌 1로 계산됩니다.
        en: Ignores duplicates; 'AAB' would incorrectly count A as 1 instead of 2.
  - label:
      ko: 추적 변수 초기화
      en: Initialize Tracking Variables
    indent: 0
    options:
    - code: have, need = 0, len(countT)
      type: good
      why:
        ko: '''have''는 올바른 빈도를 갖춘 고유 문자 개수 (0에서 시작), ''need''는 도달해야 할 목표값(t의 고유 문자 개수)입니다. 일치할 때 윈도우가 유효합니다.'
        en: '''have'' counts unique chars in t that reached their required frequency (starts at 0); ''need'' is the target. Window is valid when have equals need.'
    - code: have, need = 0, len(t)
      type: distractor
      why:
        ko: 잘못됨. need는 t의 고유 문자 개수여야 하며, 총 길이가 아닙니다.
        en: Wrong; need should be the count of unique characters in t, not the total length.
    - code: have, need = len(countT), 0
      type: distractor
      why:
        ko: 순서가 바뀌었습니다. 0에서 시작해서 need까지 증가해야 합니다.
        en: Reversed; we start at 0 and increase toward need.
    - code: have, need = len(s), len(t)
      type: distractor
      why:
        ko: 의미가 없습니다. 올바른 초기값이 아닙니다.
        en: Meaningless initialization; not correct.
  - label:
      ko: 오른쪽 포인터로 윈도우 확장 및 카운트 업데이트
      en: Expand Window and Update Counts
    indent: 1
    options:
    - code: window[c] = 1 + window.get(c, 0)
      type: good
      why:
        ko: 새로운 문자를 윈도우에 추가할 때마다 window 맵에서 해당 문자의 빈도를 증가시킵니다. 이는 현재 윈도우의 상태를 정확히 추적합니다.
        en: For each new character added to the window, increment its count in the window map. Tracks the current window state accurately.
    - code: window[c] = countT[c]
      type: distractor
      why:
        ko: 덮어쓰므로 중복된 문자를 누적하지 못합니다.
        en: Overwrites instead of accumulating; fails with repeated characters.
    - code: 'if c in countT: window[c] = 1 + window.get(c, 0)'
      type: distractor
      why:
        ko: t에 없는 문자를 추적하지 않아 윈도우가 불완전합니다.
        en: Skips characters not in t; window tracking becomes incomplete.
    - code: window[s[r-1]] += 1
      type: distractor
      why:
        ko: off-by-one 오류. 이전 문자를 보므로 현재 문자를 놓칩니다.
        en: Off-by-one error; looks at previous character instead of current.
  - label:
      ko: 문자 요구사항 충족 확인
      en: Check if Character Requirement Met
    indent: 1
    options:
    - code: 'if c in countT and window[c] == countT[c]:'
      type: good
      why:
        ko: 방금 추가된 문자가 t의 빈도 요구사항에 정확히 도달했을 때만 'have'를 증가시킵니다. 이후 초과해도 다시 증가하지 않습니다.
        en: Increment 'have' only when a character in t reaches its exact required frequency. Subsequent excess doesn't re-increment.
    - code: 'if window[c] == countT[c]: have += 1'
      type: distractor
      why:
        ko: c가 t에 없으면 countT[c]에서 KeyError가 발생합니다.
        en: Crashes if c is not in countT; missing the in-check.
    - code: 'if c in countT and window[c] >= countT[c]: have += 1'
      type: distractor
      why:
        ko: 여러 번 증가합니다. 초과할 때마다 증가하므로 정확하지 않습니다.
        en: Increments repeatedly; should only increment once when reaching the exact match.
    - code: 'if c in countT: have += 1'
      type: distractor
      why:
        ko: 빈도를 무시합니다. 모든 t 문자를 동등하게 처리하므로 잘못된 로직입니다.
        en: Ignores frequency; counts all chars in t regardless of actual count.
  - label:
      ko: 모든 요구사항이 충족되면 윈도우 축소
      en: Shrink Window While Valid
    indent: 1
    options:
    - code: 'while have == need:'
      type: good
      why:
        ko: have == need일 때, 윈도우가 모든 필수 문자를 포함합니다. while 루프는 왼쪽에서 축소하여 최소 윈도우를 찾고, 루프 내에서 결과를 업데이트합니다.
        en: When have equals need, the window contains all required characters. This loop contracts from the left to find the minimum window and updates the result inside.
    - code: 'while have < need:'
      type: distractor
      why:
        ko: 반대 조건입니다. 불완전한 윈도우를 축소해봐야 의미가 없습니다.
        en: Opposite condition; shrinking an incomplete window is pointless.
    - code: 'while have > 0:'
      type: distractor
      why:
        ko: 잘못된 조건. need와 비교해야만 합니다.
        en: Wrong condition; must compare to need, not just check if positive.
    - code: 'if have == need:'
      type: distractor
      why:
        ko: 한 번만 확인합니다. while은 계속 축소하며 최소값을 갱신합니다.
        en: Only checks once per r; while loops to continuously optimize.
  - label:
      ko: 왼쪽 문자 제거 및 추적 조정
      en: Remove Left Character and Adjust Tracking
    indent: 2
    options:
    - code: window[s[l]] -= 1
      type: good
      why:
        ko: 윈도우의 맨 왼쪽 문자를 제거합니다. 이 문자가 t의 요구사항을 깨뜨리면 (빈도가 필요한 수 아래로 내려가면) 'have'를 감소시킵니다.
        en: Removes the leftmost character from the window. If its removal breaks a requirement (count drops below needed), decrement 'have'.
    - code: window[s[l]] -= 1; l += 1
      type: distractor
      why:
        ko: 윈도우는 업데이트하지만 'have'를 조정하지 않아 상태 추적이 부정확합니다.
        en: Updates window but doesn't adjust 'have'; state tracking becomes incorrect.
    - code: l += 1; window[s[l]] -= 1
      type: distractor
      why:
        ko: 포인터를 먼저 이동하면 잘못된 인덱스의 문자를 감소시킵니다.
        en: Moves pointer first, then decrements the wrong index.
    - code: 'if window[s[l]] < countT[s[l]]: have -= 1'
      type: distractor
      why:
        ko: s[l]이 t에 없으면 countT[s[l]]에서 KeyError가 발생합니다.
        en: Crashes if s[l] is not in countT; missing the in-check.
trace:
  code:
  - 'class Solution:'
  - '    def minWindow(self, s: str, t: str) -> str:'
  - '        if len(s) < len(t):'
  - '            return ""'
  - ''
  - '        countT, window = {}, {}'
  - '        for c in t:'
  - '            countT[c] = 1 + countT.get(c, 0)'
  - ''
  - '        have, need = 0, len(countT)'
  - '        res, resLen = [-1, -1], float("infinity")'
  - '        l = 0'
  - '        for r in range(len(s)):'
  - '            c = s[r]'
  - '            window[c] = 1 + window.get(c, 0)'
  - ''
  - '            if c in countT and window[c] == countT[c]:'
  - '                have += 1'
  - ''
  - '            while have == need:'
  - '                # update our result'
  - '                if (r - l + 1) < resLen:'
  - '                    res = [l, r]'
  - '                    resLen = r - l + 1'
  - '                # pop from the left of our window'
  - '                window[s[l]] -= 1'
  - '                if s[l] in countT and window[s[l]] < countT[s[l]]:'
  - '                    have -= 1'
  - '                l += 1'
  - '        l, r = res'
  - '        return s[l : r + 1] if resLen != float("infinity") else ""'
  cases:
  - input: '"ADOBECODEBANC"

      "ABC"'
    expected: BANC
  - input: '"a"

      "a"'
    expected: a
  - input: '"a"

      "aa"'
    expected: ''
  worked_example:
    input: '"ADOBECODEBANC"

      "ABC"'
    steps:
    - ko: 'countT 구성: {''A'': 1, ''B'': 1, ''C'': 1}; need = 3'
      en: 'Build countT: {''A'': 1, ''B'': 1, ''C'': 1}; need = 3'
    - ko: r=5에서 'C' 추가 → have=3 도달, 첫 유효 윈도우 [0,5]='ADOBEC' (길이 6)
      en: At r=5, add 'C' → have=3 reached, first valid window [0,5]='ADOBEC' (length 6)
    - ko: '왼쪽에서 축소: A, D, O, B, E, C, O, D, E 제거 → have<3 재달성 후 재확장'
      en: 'Shrink left: remove A, D, O... until have < 3, then expand right again'
    - ko: r=12에서 최종 문자 'C' 처리, 'BANC' [9,12] (길이 4) = 최소값
      en: At r=12, find minimum window 'BANC' at [9,12] (length 4)
    answer: BANC
solution:
  code: "class Solution:\n    def minWindow(self, s: str, t: str) -> str:\n        if len(s) < len(t):\n            return \"\"\n\n        countT, window = {}, {}\n        for c in t:\n            countT[c] = 1 + countT.get(c, 0)\n\n        have, need = 0, len(countT)\n        res, resLen = [-1, -1], float(\"infinity\")\n        l = 0\n        for r in range(len(s)):\n            c = s[r]\n            window[c] = 1 + window.get(c, 0)\n\n            if c in countT and window[c] == countT[c]:\n                have += 1\n\n            while have == need:\n                # update our result\n                if (r - l + 1) < resLen:\n                    res = [l, r]\n                    resLen = r - l + 1\n                # pop from the left of our window\n                window[s[l]] -= 1\n                if s[l] in countT and window[s[l]] < countT[s[l]]:\n                    have -= 1\n                l += 1\n        l, r = res\n        return s[l : r + 1] if resLen != float(\"infinity\")\
    \ else \"\"\n"
  complexity:
    time: O(m + n)
    space: O(1)
  followup:
  - ko: 같은 t에 대해 여러 s의 최소 윈도우를 찾아야 한다면? → countT를 한 번 미리 계산해서 각 s마다 재사용하면 O(n)를 절약할 수 있습니다.
    en: If you needed to find minimum windows for multiple strings s with the same t? → Precompute countT once and reuse it across all strings.
  - ko: 부분 문자열이 아닌 부분 시퀀스를 찾는다면? → 슬라이딩 윈도우는 연속성을 요구하므로, 동적 프로그래밍으로 재설계해야 합니다.
    en: What if you needed a subsequence instead of a substring (non-contiguous)? → Sliding window requires contiguity; use dynamic programming instead.
  - ko: 정확히 t와 같은 빈도를 가져야 한다면 (초과 불가)? → 추가 카운터로 초과분을 추적하고 have/need 로직을 수정해야 합니다.
    en: What if the window must have exactly t's character frequencies, no extras? → Track excess characters separately and modify the have/need logic accordingly.
```
---
created: '2026-05-18'
date: '2026-05-18'
day: Day 16
difficulty: medium
id: A-016
source:
  curated_in:
  - neetcode150
  number: 3
  platform: leetcode
  slug: longest-substring-without-repeating-characters
  url: https://leetcode.com/problems/longest-substring-without-repeating-characters/
tags:
- hash-table
- string
- sliding-window
title:
  en: Longest Substring Without Repeating Characters
  ko: 중복 없는 최장 부분 문자열
today: false
type: algorithm
updated: '2026-05-18'
visible: true
---

# 중복 없는 최장 부분 문자열

## Data

```yaml
problem:
  title:
    ko: 중복 없는 최장 부분 문자열
    en: Longest Substring Without Repeating Characters
  statement:
    ko: 문자열 s가 주어질 때, 중복된 문자가 없는 최장 부분 문자열의 길이를 구하세요.
    en: Given a string s, find the length of the longest substring without duplicate characters.
  constraints:
  - 0 ≤ s.length ≤ 5 × 10⁴
  - s consists of English letters, digits, symbols and spaces
  io:
  - input: '"abcabcbb"'
    output: '3'
  - input: '"bbbbb"'
    output: '1'
  - input: '"pwwkew"'
    output: '3'
clarifying:
  items:
  - q:
      ko: 부분 문자열은 반드시 연속되어야 하나요?
      en: Must the substring be contiguous?
    type: good
    why:
      ko: 네, 부분 문자열은 원래 문자열에서 연속된 문자들로 이루어져야 합니다. 예를 들어 'abcabcbb'에서 'abc'는 부분 문자열이지만 'acd'는 아닙니다.
      en: Yes, a substring must consist of consecutive characters from the original string. For example, 'abc' is a substring of 'abcabcbb' but 'acd' is not.
  - q:
      ko: 빈 문자열을 입력받으면 어떤 값을 반환해야 하나요?
      en: What should we return for an empty string?
    type: good
    why:
      ko: 길이 0을 반환합니다. 빈 문자열에는 부분 문자열이 없으므로 최장 길이는 0입니다.
      en: Return 0. An empty string has no substrings, so the maximum length is 0.
  - q:
      ko: 같은 길이의 유효한 부분 문자열이 여러 개 있으면 어떻게 하나요?
      en: What if there are multiple valid substrings of the same maximum length?
    type: good
    why:
      ko: 문제는 길이만 요구하므로, 어느 부분 문자열이든 상관없습니다. 'abcabcbb'의 경우 'abc', 'bca', 'cab' 모두 길이 3이며, 답은 3입니다.
      en: The problem only asks for the length, so it doesn't matter which substring we find. For 'abcabcbb', 'abc', 'bca', and 'cab' are all valid with length 3.
  - q:
      ko: 문자의 종류가 최대 26개(영문)라는 것이 왜 중요한가요?
      en: Why is the maximum 26 unique characters (English letters) important?
    type: good
    why:
      ko: 이는 공간 복잡도의 상한을 제한합니다. 문자 집합이 최대 26개 크기이므로, 최악의 경우 O(26) = O(1) 공간만 필요합니다.
      en: It bounds our space complexity. Since the character set has a maximum size of 26, we only need O(26) = O(1) space in the worst case.
  - q:
      ko: '''bca''는 ''abcabcbb''의 유효한 부분 문자열이 될 수 있나요?'
      en: Could 'bca' be a valid substring for 'abcabcbb'?
    type: distractor
    why:
      ko: 아니요, 'bca'는 'abcabcbb'에서 연속된 부분으로 나타나지 않습니다. 각 위치에서 찾으면 항상 같은 두 문자 또는 다른 문자열을 얻습니다.
      en: No, 'bca' does not appear as a contiguous substring in 'abcabcbb'. Each occurrence is separated or interrupted.
  - q:
      ko: 결과로 부분 문자열 자체를 반환해야 하나요?
      en: Should we return the substring itself?
    type: distractor
    why:
      ko: 아니요, 문제는 최장 부분 문자열의 "길이"를 요구하며, 부분 문자열 자체가 아닙니다.
      en: No, the problem asks for the length of the longest substring, not the substring itself.
approach:
  items:
  - name:
      ko: 슬라이딩 윈도우 (해시 집합)
      en: Sliding Window with Hash Set
    complexity: O(n) time / O(min(n, 26)) space
    type: good
    why:
      ko: 두 포인터로 윈도우를 유지하면서 중복을 확인합니다. 각 문자는 최대 두 번 방문되므로 O(n) 시간 복잡도를 달성합니다.
      en: Two pointers maintain a window while checking for duplicates. Each character is visited at most twice, achieving O(n) time complexity.
  - name:
      ko: 슬라이딩 윈도우 (해시 맵)
      en: Sliding Window with Hash Map
    complexity: O(n) time / O(min(n, 26)) space
    type: good
    why:
      ko: 문자의 마지막 위치를 저장하여 중복 발견 시 왼쪽 포인터를 직접 이동할 수 있습니다.
      en: Store the last position of each character to directly jump the left pointer when a duplicate is found.
  - name:
      ko: 무차별 대입 (모든 부분 문자열)
      en: Brute Force (Check All Substrings)
    complexity: O(n²) or O(n³) time / O(min(n, 26)) space
    type: distractor
    why:
      ko: 모든 가능한 부분 문자열을 확인하므로 비효율적입니다. 슬라이딩 윈도우가 훨씬 더 빠릅니다.
      en: Checks all possible substrings, which is inefficient. Sliding window is much faster.
  - name:
      ko: 동적 계획법
      en: Dynamic Programming
    complexity: O(n) time / O(n) space
    type: distractor
    why:
      ko: 이 문제에서 동적 계획법은 필요하지 않습니다. 슬라이딩 윈도우가 더 간단하고 공간 효율적입니다.
      en: Dynamic programming is unnecessary here. Sliding window is simpler and more space-efficient.
logic:
  format: slot
  slots:
  - label:
      ko: 문자 집합 초기화
      en: Initialize character set
    indent: 0
    options:
    - code: charSet = set()
      type: good
      why:
        ko: Set은 O(1) 멤버십 확인을 제공하므로 중복 감지에 필수적입니다.
        en: Set provides O(1) membership checking, which is essential for duplicate detection.
    - code: charSet = {}
      type: distractor
      why:
        ko: 빈 딕셔너리는 작동하지만, 문자 존재 확인만 필요할 때는 set이 더 명확합니다.
        en: Empty dict works but set is clearer for just checking character existence.
    - code: charSet = []
      type: distractor
      why:
        ko: 리스트의 멤버십 확인은 O(n)으로 알고리즘을 O(n²)로 악화시킵니다.
        en: List membership checking is O(n), degrading the algorithm to O(n²).
  - label:
      ko: 왼쪽 포인터 초기화
      en: Initialize left pointer
    indent: 0
    options:
    - code: l = 0
      type: good
      why:
        ko: 왼쪽 포인터는 현재 윈도우의 시작을 표시합니다. 중복 제거 시 증가합니다.
        en: Left pointer marks the start of the current window and increments when removing duplicates.
    - code: l = 1
      type: distractor
      why:
        ko: 1부터 시작하면 인덱스 0의 첫 번째 문자를 건너뜁니다.
        en: Starting at 1 skips the first character at index 0.
    - code: l = -1
      type: distractor
      why:
        ko: 음수는 파이썬에서 특별한 의미를 가지며 윈도우를 올바르게 표현하지 못합니다.
        en: Negative index has special meaning in Python and doesn't correctly represent the window.
  - label:
      ko: 결과 변수 초기화
      en: Initialize result variable
    indent: 0
    options:
    - code: res = 0
      type: good
      why:
        ko: 최대 길이를 0부터 시작하여 각 유효한 윈도우와 비교하여 업데이트합니다.
        en: Start with 0 and update with the length of each valid window found.
    - code: res = 1
      type: distractor
      why:
        ko: 1부터 시작하면 빈 문자열에 대해 잘못된 결과를 반환합니다.
        en: Starting with 1 gives wrong results for empty strings.
    - code: res = len(s)
      type: distractor
      why:
        ko: 문자열 전체 길이로 시작하면 최댓값을 올바르게 추적할 수 없습니다.
        en: Starting with full length prevents correctly tracking the actual maximum.
  - label:
      ko: 오른쪽 포인터 반복
      en: Iterate with right pointer
    indent: 0
    options:
    - code: 'for r in range(len(s)):'
      type: good
      why:
        ko: 오른쪽 포인터가 문자열 전체를 순회하면서 각 문자를 처리합니다.
        en: Right pointer traverses the entire string, processing each character.
    - code: 'for r in range(1, len(s)):'
      type: distractor
      why:
        ko: 1부터 시작하면 첫 번째 문자를 건너뜁니다.
        en: Starting at 1 skips the first character.
    - code: 'for r in s:'
      type: distractor
      why:
        ko: r에 문자가 할당되므로 s[r]을 사용할 수 없습니다.
        en: This assigns characters to r, not indices, so s[r] won't work.
  - label:
      ko: 중복 감지 조건
      en: Detect duplicate condition
    indent: 1
    options:
    - code: 'while s[r] in charSet:'
      type: good
      why:
        ko: while 루프는 중복이 완전히 제거될 때까지 계속 실행되어야 합니다.
        en: While loop continues until the duplicate is completely removed from the window.
    - code: 'if s[r] in charSet:'
      type: distractor
      why:
        ko: if는 한 번만 확인하므로 완전한 중복 제거를 보장하지 못합니다.
        en: If only checks once; we need while to fully resolve the duplicate.
    - code: 'while s[l] in charSet:'
      type: distractor
      why:
        ko: 문제는 s[r]이지 s[l]이 아닙니다.
        en: The problem character is s[r], not s[l].
  - label:
      ko: 현재 문자 추가
      en: Add current character to set
    indent: 1
    options:
    - code: charSet.add(s[r])
      type: good
      why:
        ko: 중복을 해결한 후 새로운 오른쪽 문자를 집합에 추가합니다.
        en: After resolving duplicates, add the new right character to the set.
    - code: charSet.add(s[l])
      type: distractor
      why:
        ko: s[l]이 아닌 새로운 문자 s[r]을 추가해야 합니다.
        en: Should add the new character s[r], not s[l].
    - code: charSet.update([s[r]])
      type: distractor
      why:
        ko: update는 이터러블을 기대하지만, 단일 문자는 add가 더 적절합니다.
        en: Update expects an iterable; add is more appropriate for a single character.
  - label:
      ko: 최대 길이 업데이트
      en: Update maximum length
    indent: 1
    options:
    - code: res = max(res, r - l + 1)
      type: good
      why:
        ko: 현재 윈도우 길이(r - l + 1)를 이전 최댓값과 비교하여 최댓값을 갱신합니다.
        en: Compare the current window length (r - l + 1) with the previous maximum and update.
    - code: res = max(res, r - l)
      type: distractor
      why:
        ko: r - l은 길이가 아니라 길이 - 1입니다. 정확한 길이는 r - l + 1입니다.
        en: r - l is one less than the actual length; the correct formula is r - l + 1.
    - code: res = r - l + 1
      type: distractor
      why:
        ko: max와 비교하지 않으면 이전의 더 큰 값을 덮어씁니다.
        en: Without comparing with max, this overwrites any larger previous value.
trace:
  code:
  - 'class Solution:'
  - '    def lengthOfLongestSubstring(self, s: str) -> int:'
  - '        charSet = set()'
  - '        l = 0'
  - '        res = 0'
  - ''
  - '        for r in range(len(s)):'
  - '            while s[r] in charSet:'
  - '                charSet.remove(s[l])'
  - '                l += 1'
  - '            charSet.add(s[r])'
  - '            res = max(res, r - l + 1)'
  - '        return res'
  cases:
  - input: '"abcabcbb"'
    expected: '3'
  - input: '"bbbbb"'
    expected: '1'
  - input: '"pwwkew"'
    expected: '3'
  worked_example:
    input: '"abcabcbb"'
    steps:
    - ko: '초기: charSet = {}, l = 0, res = 0. 인덱스 0부터 오른쪽 포인터 시작.'
      en: 'Start: charSet = {}, l = 0, res = 0. Right pointer begins at index 0.'
    - ko: 'r = 0~2: ''a'', ''b'', ''c''를 순차 추가. 윈도우는 ''abc''이고 res = 3.'
      en: 'r = 0~2: Add ''a'', ''b'', ''c'' sequentially. Window is ''abc'', res = 3.'
    - ko: 'r = 3: ''a'' 감지, 왼쪽에서 ''a'' 제거(l=1), 새 ''a'' 추가. 윈도우 ''bca''(길이 3).'
      en: 'r = 3: Detect ''a'', remove left ''a'' (l=1), add new ''a''. Window is ''bca'' (length 3).'
    - ko: 'r = 4~7: 계속 슬라이딩하며 중복 처리. 윈도우가 3을 초과하지 않으므로 res = 3 유지. 최종 답: 3.'
      en: 'r = 4~7: Slide and handle duplicates. Window never exceeds 3, res stays 3. Final answer: 3.'
    answer: '3'
solution:
  code: "class Solution:\n    def lengthOfLongestSubstring(self, s: str) -> int:\n        charSet = set()\n        l = 0\n        res = 0\n\n        for r in range(len(s)):\n            while s[r] in charSet:\n                charSet.remove(s[l])\n                l += 1\n            charSet.add(s[r])\n            res = max(res, r - l + 1)\n        return res\n"
  complexity:
    time: O(n)
    space: O(min(n, 26))
  followup:
  - ko: 부분 문자열 자체를 반환해야 한다면?
    en: What if we need to return the actual substring instead of its length?
  - ko: 최대 길이 갱신 시 윈도우 시작 인덱스를 기록하면, 마지막에 s[start:start+max_len]으로 반환할 수 있습니다.
    en: Track the starting index whenever you update the maximum length, then return s[start:start+max_len] at the end.
```
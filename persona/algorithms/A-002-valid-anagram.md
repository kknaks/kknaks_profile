---
created: '2026-05-07'
date: '2026-05-07'
day: Day 02
difficulty: easy
id: A-002
source:
  curated_in:
  - neetcode150
  number: 242
  platform: leetcode
  slug: valid-anagram
  url: https://leetcode.com/problems/valid-anagram/
status: draft
tags:
- hash-table
- string
- sorting
title:
  en: Valid Anagram
  ko: 유효한 애너그램
today: true
type: algorithm
updated: '2026-05-07'
visible: true
---

# 유효한 애너그램

## Data

```yaml
problem:
  title:
    ko: 유효한 애너그램
    en: Valid Anagram
  statement:
    ko: 두 문자열 s와 t가 주어졌을 때, t가 s의 애너그램인지 판단하세요. 애너그램은 같은 문자들을 같은 개수로 포함하되 순서만 다른 단어입니다.
    en: Determine if two strings contain the same characters with identical frequencies, regardless of their order.
  constraints:
  - 1 ≤ s.length, t.length ≤ 5×10⁴
  - s and t consist of lowercase English letters only
  - Different lengths cannot be anagrams
  io:
  - input: '"anagram"

      "nagaram"'
    output: 'true'
  - input: '"rat"

      "car"'
    output: 'false'
clarifying:
  items:
  - q:
      ko: 길이가 다른 두 문자열도 애너그램이 될 수 있나요?
      en: Can strings of different lengths be anagrams?
    type: good
    why:
      ko: 애너그램은 같은 문자를 같은 개수로 포함해야 하므로, 길이가 같아야 합니다.
      en: By definition, anagrams must contain identical characters with same counts, requiring equal length.
  - q:
      ko: 문자 개수가 같으면 애너그램입니까?
      en: If two strings have the same number of distinct characters, are they anagrams?
    type: good
    why:
      ko: '아니요. 예: ''ab''와 ''cd''는 각각 2개의 문자를 가지지만 애너그램이 아닙니다.'
      en: No. We need the actual character frequencies to match, not just the count of distinct characters.
  - q:
      ko: 애너그램 판단에서 문자의 순서가 중요합니까?
      en: Does the order of characters matter when checking if strings are anagrams?
    type: good
    why:
      ko: 아니요. 같은 문자를 같은 개수로 포함하면 순서와 관계없이 애너그램입니다.
      en: No. Order is irrelevant; only character frequencies and counts matter.
  - q:
      ko: 입력이 빈 문자열일 수 있나요?
      en: Can the input strings be empty?
    type: good
    why:
      ko: 제약 조건에서 최소 길이가 1이므로 빈 문자열은 없습니다.
      en: Constraints specify minimum length of 1, so empty strings are not possible.
  - q:
      ko: 대문자나 특수문자가 포함될 수 있습니까?
      en: Are uppercase letters or special characters possible?
    type: good
    why:
      ko: 제약 조건에서 소문자 영문자만 명시되어 있습니다.
      en: Constraints explicitly state only lowercase English letters.
  - q:
      ko: 입력 문자열을 수정할 수 있나요?
      en: Can we modify the input strings?
    type: distractor
    why:
      ko: 입력 수정 여부는 정확성에 영향을 주지 않습니다.
      en: Whether we can modify inputs doesn't affect correctness of the algorithm.
  - q:
      ko: 애너그램 쌍을 모두 찾아서 반환해야 하나요?
      en: Should we return all anagram pairs?
    type: distractor
    why:
      ko: 문제는 true/false만 요구합니다. 실제 애너그램 쌍을 찾을 필요는 없습니다.
      en: The problem only asks for true/false boolean, not the actual character mappings.
approach:
  items:
  - name:
      ko: 해시맵으로 문자 빈도수 계산
      en: Hash Map Frequency Counting
    complexity: O(n) time / O(1) space
    type: good
    why:
      ko: 두 문자열을 순회하며 문자별 빈도수를 저장한 후 비교합니다. 소문자만 있으므로 최대 26개 항목만 저장됩니다.
      en: Count characters in both strings and compare dictionaries. Space is O(1) since at most 26 lowercase letters.
  - name:
      ko: 정렬 후 비교
      en: Sort and Compare
    complexity: O(n log n) time / O(n) space
    type: good
    why:
      ko: 두 문자열을 정렬한 후 직접 비교합니다. 구현이 간단하지만 정렬 비용이 더 큽니다.
      en: Sort both strings and compare directly. Simpler code but slower due to sorting overhead.
  - name:
      ko: 중첩 루프로 각 문자 확인
      en: Nested Loop Character Verification
    complexity: O(n²) time / O(1) space
    type: distractor
    why:
      ko: s의 각 문자가 t에 존재하는지 확인하는 방식입니다. 매우 비효율적입니다.
      en: Check each character in s against t individually. Very inefficient with O(n²) time.
  - name:
      ko: 문자 빈도 배열 (고정 크기)
      en: Fixed-size Character Array
    complexity: O(n) time / O(1) space
    type: good
    why:
      ko: 소문자 26개에 대해 크기 26인 배열을 생성하여 빈도수를 저장합니다. 해시맵보다 약간 더 빠릅니다.
      en: Use array of size 26 for lowercase letters instead of hash map. Slightly faster due to fixed array access.
  - name:
      ko: Counter 객체 사용
      en: Built-in Counter (Python)
    complexity: O(n) time / O(1) space
    type: distractor
    why:
      ko: Python의 Counter로 빈도수를 세고 비교합니다. 동작하지만 수동 구현이 아닙니다.
      en: Using built-in tool is valid but doesn't demonstrate algorithm understanding in interviews.
logic:
  format: slot
  slots:
  - label:
      ko: 길이 비교 및 조기 반환
      en: Length Check and Early Exit
    indent: 0
    options:
    - code: 'if len(s) != len(t):'
      type: good
      why:
        ko: 길이가 다르면 절대 애너그램이 될 수 없으므로 즉시 false를 반환합니다.
        en: Different lengths guarantee non-anagram status. Return false immediately to avoid unnecessary processing.
    - code: 'if len(s) < len(t):'
      type: distractor
      why:
        ko: 한쪽 방향만 확인하면 다른 경우를 놓칩니다.
        en: Checking only one direction misses cases where len(s) > len(t).
    - code: 'if s != t:'
      type: distractor
      why:
        ko: 전체 문자열을 비교하면 길이가 같으면서 내용이 다른 경우를 감지할 수 없습니다.
        en: Compares full strings instead of lengths; incorrect for checking anagrams.
    - code: 'if len(s) == len(t): return False'
      type: distractor
      why:
        ko: 조건이 역순입니다. 길이가 같으면 계속 진행해야 합니다.
        en: Inverted logic. Should continue when lengths are equal, not return false.
  - label:
      ko: 빈도수 맵 초기화
      en: Initialize Frequency Maps
    indent: 0
    options:
    - code: countS, countT = {}, {}
      type: good
      why:
        ko: 각 문자열의 문자 빈도수를 독립적으로 저장할 두 개의 딕셔너리를 생성합니다.
        en: Create separate dictionaries for each string to track character frequencies independently.
    - code: count = {}
      type: distractor
      why:
        ko: 하나의 맵만 사용하면 두 문자열의 빈도수를 구분할 수 없습니다.
        en: Single dictionary cannot distinguish between character counts from both strings.
    - code: countS = countT = {}
      type: distractor
      why:
        ko: 같은 객체를 가리키므로 countS를 채운 후 countT 루프에서 덮어씌워집니다.
        en: Both reference same object. Second loop overwrites first string's counts.
    - code: countS, countT = set(), set()
      type: distractor
      why:
        ko: 집합은 빈도수(개수)를 저장할 수 없고 단순히 존재 여부만 저장합니다.
        en: Sets store presence only, not frequency counts. Cannot distinguish 'a' vs 'aa'.
  - label:
      ko: 반복문을 통한 문자 빈도수 계산
      en: Count Characters via Loop
    indent: 1
    options:
    - code: countS[s[i]] = 1 + countS.get(s[i], 0)
      type: good
      why:
        ko: .get() 메서드를 사용하여 키가 없을 때 기본값 0을 반환하고, 각 문자의 빈도수를 안전하게 누적합니다.
        en: Using .get() with default value 0 safely handles missing keys on first occurrence, then increments count.
    - code: countS[s[i]] += 1
      type: distractor
      why:
        ko: 첫 등장할 때 KeyError가 발생합니다. 딕셔너리에 없는 키에 접근할 수 없습니다.
        en: Raises KeyError when key doesn't exist yet. No default value provided.
    - code: countS[s[i]] = countS.get(s[i], 1)
      type: distractor
      why:
        ko: 기본값이 1이면 첫 등장 문자가 2로 계산됩니다. 기본값은 0이어야 합니다.
        en: Default value 1 causes first character to count as 2. Should start from 0.
    - code: 'if s[i] in countS: countS[s[i]] += 1

        else: countS[s[i]] = 1'
      type: distractor
      why:
        ko: 동작하지만 복잡합니다. .get()을 사용한 한 줄이 더 간결하고 Pythonic합니다.
        en: Works correctly but verbose. Using .get() is more concise and idiomatic Python.
  - label:
      ko: 빈도수 맵 비교 및 결과 반환
      en: Compare Frequency Maps and Return
    indent: 0
    options:
    - code: return countS == countT
      type: good
      why:
        ko: 두 딕셔너리의 내용(문자와 빈도수)이 정확히 일치하면 애너그램입니다.
        en: Dictionary equality check verifies both character presence and exact frequency match.
    - code: return set(countS.keys()) == set(countT.keys())
      type: distractor
      why:
        ko: '같은 문자들이 있는지만 확인하고 빈도수 차이를 무시합니다. 예: ''a''와 ''aa''는 같은 문자지만 다른 개수입니다.'
        en: Only checks character presence, ignores frequency. 'a' and 'aa' would be treated as equal.
    - code: return len(countS) == len(countT)
      type: distractor
      why:
        ko: 고유 문자의 개수만 비교합니다. 'ab'와 'cd'는 같은 개수의 고유 문자이지만 애너그램이 아닙니다.
        en: Only compares number of distinct characters, not their identities or counts.
    - code: return sorted(countS.values()) == sorted(countT.values())
      type: distractor
      why:
        ko: '빈도수의 분포만 비교합니다. 예: ''ab''(각 1개)와 ''cd''(각 1개)가 같다고 판단합니다.'
        en: Compares frequency distribution only, ignoring which characters. 'ab' and 'cd' both have [1,1].
trace:
  code:
  - 'class Solution:'
  - '    def isAnagram(self, s: str, t: str) -> bool:'
  - '        if len(s) != len(t):'
  - '            return False'
  - ''
  - '        countS, countT = {}, {}'
  - ''
  - '        for i in range(len(s)):'
  - '            countS[s[i]] = 1 + countS.get(s[i], 0)'
  - '            countT[t[i]] = 1 + countT.get(t[i], 0)'
  - '        return countS == countT'
  - ''
  - '    '
  - '    # easier solution'
  - '    #return True if sorted(s) == sorted(t) else False'
  cases:
  - input: '"anagram"

      "nagaram"'
    expected: 'true'
  - input: '"rat"

      "car"'
    expected: 'false'
  worked_example:
    input: '"anagram"

      "nagaram"'
    steps:
    - ko: '길이 확인: len(''anagram'') = 7, len(''nagaram'') = 7 → 길이가 같으므로 계속 진행'
      en: 'Check lengths: both have 7 characters, proceed to counting'
    - ko: '문자열 s = ''anagram'' 순회하며 빈도수 기록: countS = {a:3, n:1, g:1, r:1, m:1}'
      en: 'Count s: iterate through ''anagram'' → countS = {a:3, n:1, g:1, r:1, m:1}'
    - ko: '문자열 t = ''nagaram'' 순회하며 빈도수 기록: countT = {n:1, a:3, g:1, r:1, m:1}'
      en: 'Count t: iterate through ''nagaram'' → countT = {n:1, a:3, g:1, r:1, m:1}'
    - ko: '딕셔너리 비교: countS == countT → True (모든 문자의 빈도수가 일치)'
      en: 'Compare: countS and countT are identical → return True'
    answer: 'true'
solution:
  code: "class Solution:\n    def isAnagram(self, s: str, t: str) -> bool:\n        if len(s) != len(t):\n            return False\n\n        countS, countT = {}, {}\n\n        for i in range(len(s)):\n            countS[s[i]] = 1 + countS.get(s[i], 0)\n            countT[t[i]] = 1 + countT.get(t[i], 0)\n        return countS == countT\n\n    \n    # easier solution\n    #return True if sorted(s) == sorted(t) else False\n"
  complexity:
    time: O(n)
    space: O(1)
  followup:
  - ko: 유니코드 문자가 포함된다면? 해시맵 방식은 그대로 작동하지만, 고정 배열 방식은 더 큰 범위를 다루기 위해 조정이 필요합니다.
    en: What if inputs contain Unicode characters? Hash map approach still works. Fixed array approach would need larger alphabet range.
  - ko: 매우 큰 문자열(수 GB)에서 메모리가 제한된다면? 문자열을 청크로 나누어 처리하거나 스트림 방식을 고려할 수 있습니다.
    en: If memory is severely limited with huge strings? Consider chunking or streaming approaches to process incrementally.
  - ko: 정렬 방식(O(n log n) 시간, O(n) 공간)과 해시맵 방식(O(n) 시간, O(1) 공간)의 트레이드오프는? 정렬은 더 단순하고 코드가 간단하지만 느립니다. 해시맵은 더 빠르고 공간 효율적입니다.
    en: Trade-offs between sorting O(n log n) vs hash map O(n)? Sorting is simpler but slower. Hash map is faster but requires understanding hash data structures.
```
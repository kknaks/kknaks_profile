---
created: '2026-05-19'
date: '2026-05-19'
day: Day 17
difficulty: medium
id: A-017
source:
  curated_in:
  - neetcode150
  number: 424
  platform: leetcode
  slug: longest-repeating-character-replacement
  url: https://leetcode.com/problems/longest-repeating-character-replacement/
tags:
- hash-table
- string
- sliding-window
title:
  en: Longest Repeating Character Replacement
  ko: 가장 긴 반복 문자 치환
today: false
type: algorithm
updated: '2026-05-19'
visible: true
---

# 가장 긴 반복 문자 치환

## Data

```yaml
problem:
  title:
    ko: 가장 긴 반복 문자 치환
    en: Longest Repeating Character Replacement
  statement:
    ko: '문자열 s와 정수 k가 주어집니다. 문자열의 임의의 문자를 다른 대문자로 변경할 수 있으며, 이 작업을 최대 k번 수행할 수 있습니다.


      주어진 작업을 수행하여 얻을 수 있는 같은 문자로만 이루어진 가장 긴 부분 문자열의 길이를 반환하세요.'
    en: 'You are given a string s and an integer k. You can choose any character of the string and change it to any other uppercase English character. You can perform this operation at most k times.


      Return the length of the longest substring containing the same letter you can get after performing the above operations.'
  constraints:
  - 1 ≤ s.length ≤ 10^5
  - s consists of only uppercase English letters
  - 0 ≤ k ≤ s.length
  io:
  - input: '"ABAB"

      2'
    output: '4'
  - input: '"AABABBA"

      1'
    output: '4'
clarifying:
  items:
  - q:
      ko: k=0일 때 (변경할 수 없음) 결과는 무엇인가요?
      en: What happens when k=0 (no changes allowed)?
    type: good
    why:
      ko: k=0이면 이미 같은 문자로만 이루어진 부분 문자열을 찾아야 하므로, 연속된 같은 문자의 최대 길이를 반환해야 합니다.
      en: With k=0, we can only return the longest sequence of the same character that already exists in the string.
  - q:
      ko: 부분 문자열이 반드시 연속되어야 하나요?
      en: Must the substring be contiguous?
    type: good
    why:
      ko: 네, 부분 문자열은 반드시 연속된 위치에 있어야 합니다. 슬라이딩 윈도우는 이를 보장합니다.
      en: Yes, the substring must be contiguous. The sliding window approach ensures we only work with consecutive characters.
  - q:
      ko: 같은 문자로만 이루어진 부분 문자열을 만들 때, 어느 문자로 변경해야 가장 효율적인가요?
      en: To minimize changes, which character should we change all others to?
    type: good
    why:
      ko: 부분 문자열에서 가장 많은 빈도를 가진 문자로 변경해야 합니다. 그러면 필요한 변경 횟수가 최소화됩니다.
      en: We should change all characters to the most frequent character in the substring to minimize total changes.
  - q:
      ko: 변경 가능한 최대 횟수 k를 정확히 모두 사용해야 하나요?
      en: Must we use exactly k changes?
    type: good
    why:
      ko: 아니요. 최대 k번까지 사용할 수 있다는 뜻이므로, k번보다 적게 사용해도 됩니다.
      en: No. At most k means we can use fewer than k changes if the substring is already mostly one character.
  - q:
      ko: 윈도우 크기가 고정되어 있나요?
      en: Is the window size fixed?
    type: distractor
    why:
      ko: 아니요. 윈도우는 동적으로 조정됩니다. 우측 포인터로 확장하고, 변경 필요 횟수가 k를 초과하면 좌측 포인터로 축소합니다.
      en: No. The window dynamically expands with the right pointer and shrinks with the left pointer when changes exceed k.
  - q:
      ko: 실제로 문자열을 수정해야 하나요?
      en: Do we actually modify the string?
    type: distractor
    why:
      ko: 아니요. 우리는 변경하지 않고도 최대 길이를 계산할 수 있습니다. 길이만 반환하면 됩니다.
      en: No. We calculate the maximum possible length without actually modifying the input string.
approach:
  items:
  - name:
      ko: 슬라이딩 윈도우 + 해시맵
      en: Sliding window with hash map
    complexity: O(n) time / O(1) space
    type: good
    why:
      ko: 두 포인터로 윈도우를 동적으로 조정하고, 해시맵으로 각 문자의 빈도를 추적합니다. 우측 포인터는 한 번, 좌측 포인터도 최대 한 번씩 움직이므로 총 O(n) 시간입니다.
      en: Two pointers maintain a dynamic window while a hash map tracks character frequencies. Each position is visited at most twice, achieving O(n) time.
  - name:
      ko: '브루트 포스: 모든 부분 문자열 확인'
      en: 'Brute force: check all substrings'
    complexity: O(n²) time / O(26) space
    type: distractor
    why:
      ko: 모든 가능한 부분 문자열 쌍(start, end)을 반복하고 각각에 대해 변경 비용을 계산합니다. 너무 느립니다.
      en: Iterate through all O(n²) substring pairs and calculate changes needed for each. Much slower than sliding window.
  - name:
      ko: 문자별 고정 윈도우
      en: Fixed window per character
    complexity: O(26n) time / O(26) space
    type: distractor
    why:
      ko: 26개 각 문자에 대해, 그 문자로 변경했을 때의 최대 길이를 별도로 계산합니다. 슬라이딩 윈도우보다 비효율적입니다.
      en: For each of 26 possible target characters, find the longest substring where we can make it mostly that character. Less efficient than solving once.
  - name:
      ko: '탐욕적 선택: 가장 빈도가 높은 문자 고정'
      en: 'Greedy: always pick most frequent character'
    complexity: O(n log n) time / O(26) space
    type: distractor
    why:
      ko: 각 단계에서 현재 윈도우의 가장 빈번한 문자를 항상 선택합니다. 하지만 이 선택이 최적임을 보장하지 못하며, 매번 최대값을 다시 계산하면 비효율적입니다.
      en: Choosing the most frequent character at each step seems natural but doesn't guarantee optimality and requires recalculating the max.
logic:
  format: slot
  slots:
  - label:
      ko: 문자 빈도 맵 초기화
      en: Initialize character frequency map
    indent: 0
    options:
    - code: count = {}
      type: good
      why:
        ko: 슬라이딩 윈도우 내의 각 문자가 몇 번 나타나는지 추적합니다.
        en: Tracks how many times each character appears in the current window.
    - code: count = []
      type: distractor
      why:
        ko: 리스트는 문자를 인덱스로 사용할 수 없습니다. 딕셔너리가 필요합니다.
        en: A list cannot use characters as keys. Dictionary is needed.
    - code: count = set()
      type: distractor
      why:
        ko: 집합은 빈도 정보를 저장할 수 없습니다.
        en: A set cannot store counts, only presence/absence.
  - label:
      ko: 좌측 포인터 초기화
      en: Initialize left pointer
    indent: 0
    options:
    - code: l = 0
      type: good
      why:
        ko: 슬라이딩 윈도우의 시작(좌측 경계)을 표시합니다.
        en: Marks the left boundary of the sliding window.
    - code: l = -1
      type: distractor
      why:
        ko: 음수 인덱스는 예상치 못한 동작을 초래합니다.
        en: Negative indices in Python slice from the end, causing incorrect behavior.
    - code: l = r
      type: distractor
      why:
        ko: r은 아직 정의되지 않았습니다. 초기값은 고정된 값이어야 합니다.
        en: r is not yet defined; l must be initialized to a fixed value.
  - label:
      ko: 최대 빈도 추적 초기화
      en: Initialize max frequency tracker
    indent: 0
    options:
    - code: maxf = 0
      type: good
      why:
        ko: 현재 윈도우에서 가장 많이 나타나는 문자의 빈도를 기록합니다. 변경이 필요한 문자의 수를 계산하는 핵심 값입니다.
        en: Records the highest frequency of any single character in the window. Essential for calculating how many changes are needed.
    - code: maxf = 1
      type: distractor
      why:
        ko: 초기값 1은 빈 윈도우에서는 잘못된 값입니다.
        en: Starting with 1 is incorrect; the first character will have frequency 1, but maxf should start at 0.
  - label:
      ko: 우측 포인터로 윈도우 확장
      en: Expand window with right pointer
    indent: 1
    options:
    - code: 'for r in range(len(s)):'
      type: good
      why:
        ko: 각 반복마다 우측 포인터 r을 증가시키며 새 문자를 윈도우에 포함합니다.
        en: The right pointer advances one character at a time, expanding the window.
    - code: 'for r in range(1, len(s)):'
      type: distractor
      why:
        ko: 시작 인덱스를 1로 하면 첫 번째 문자를 건너뜁니다.
        en: Starting from 1 skips the first character.
  - label:
      ko: 새 문자의 빈도 증가
      en: Increment character count
    indent: 2
    options:
    - code: count[s[r]] = 1 + count.get(s[r], 0)
      type: good
      why:
        ko: 우측 포인터가 가리키는 새 문자의 빈도를 1 증가시킵니다. 기존 값이 없으면 0에서 시작합니다.
        en: Increments the count for the character at the right pointer. Uses get() to safely handle the first occurrence.
    - code: count[s[r]] += 1
      type: distractor
      why:
        ko: 첫 등장 시 KeyError가 발생합니다.
        en: Raises KeyError on first occurrence of a character.
    - code: count[s[r]] = count[s[r]] + 1
      type: distractor
      why:
        ko: 첫 등장 시 KeyError가 발생합니다. get()으로 안전하게 처리해야 합니다.
        en: Also raises KeyError on first occurrence. Need get() for safety.
  - label:
      ko: 최대 빈도 업데이트
      en: Update maximum frequency
    indent: 2
    options:
    - code: maxf = max(maxf, count[s[r]])
      type: good
      why:
        ko: 새 문자 추가 후, 현재 윈도우에서의 최대 빈도를 갱신합니다. 중요한 최적화는 maxf가 결코 감소하지 않는다는 점입니다.
        en: After adding a character, update the overall max frequency. Crucially, maxf never decreases—this is the algorithm's key optimization.
    - code: maxf = max(maxf, max(count.values()))
      type: distractor
      why:
        ko: 매번 모든 값의 최대값을 다시 계산하면 O(n) 시간이 되어 전체 복잡도가 O(n²)가 됩니다.
        en: Recalculating max over all counts each time defeats the O(n) optimization.
  - label:
      ko: 윈도우 유효성 검증
      en: Check if window is valid
    indent: 2
    options:
    - code: 'if (r - l + 1) - maxf > k:'
      type: good
      why:
        ko: 현재 윈도우 크기에서 최대 빈도를 뺀 값은 변경이 필요한 문자 수입니다. 이 값이 k를 초과하면 윈도우를 축소해야 합니다.
        en: The number of characters to change equals window_size - max_frequency. If this exceeds k, we must shrink.
    - code: 'if (r - l + 1) - maxf >= k:'
      type: distractor
      why:
        ko: '>= 대신 >를 사용해야 합니다. 정확히 k번의 변경은 여전히 유효합니다.'
        en: Using >= is too strict; exactly k changes is valid. Only shrink when changes > k.
    - code: 'if (r - l) - maxf > k:'
      type: distractor
      why:
        ko: 윈도우 크기 공식이 잘못되었습니다. (r - l + 1)이어야 합니다.
        en: Window size is (r - l + 1), not (r - l). Off-by-one error.
  - label:
      ko: 좌측 문자 카운트 감소 및 포인터 이동
      en: Remove left character and move pointer
    indent: 3
    options:
    - code: count[s[l]] -= 1
      type: good
      why:
        ko: 좌측 경계의 문자를 윈도우에서 제거합니다. 빈도를 1 감소시킵니다.
        en: Decrements the count for the character leaving the window at the left boundary.
    - code: del count[s[l]]
      type: distractor
      why:
        ko: 키를 완전히 삭제하면 나중에 같은 문자가 다시 나타날 때 오류가 발생할 수 있습니다.
        en: Deleting the key entirely can cause issues if we encounter that character again later.
    - code: count[s[l]] = 0
      type: distractor
      why:
        ko: 0으로 설정하면 나중에 max(count.values())에서 문제가 될 수 있습니다.
        en: Setting to 0 still pollutes the count dictionary unnecessarily.
trace:
  code:
  - 'class Solution:'
  - '    def characterReplacement(self, s: str, k: int) -> int:'
  - '        count = {}'
  - '        '
  - '        l = 0'
  - '        maxf = 0'
  - '        for r in range(len(s)):'
  - '            count[s[r]] = 1 + count.get(s[r], 0)'
  - '            maxf = max(maxf, count[s[r]])'
  - ''
  - '            if (r - l + 1) - maxf > k:'
  - '                count[s[l]] -= 1'
  - '                l += 1'
  - ''
  - '        return (r - l + 1)'
  cases:
  - input: '"ABAB"

      2'
    expected: '4'
  - input: '"AABABBA"

      1'
    expected: '4'
  worked_example:
    input: '"ABAB"

      2'
    steps:
    - ko: 'r=0: ''A'' 추가, count={''A'':1}, maxf=1, window크기=1, 변경필요=0 ≤ 2 유효'
      en: 'r=0: Add ''A'', count={''A'':1}, maxf=1, window_size=1, changes_needed=0 ≤ 2 ✓'
    - ko: 'r=1: ''B'' 추가, count={''A'':1,''B'':1}, maxf=1, window크기=2, 변경필요=1 ≤ 2 유효'
      en: 'r=1: Add ''B'', count={''A'':1,''B'':1}, maxf=1, window_size=2, changes_needed=1 ≤ 2 ✓'
    - ko: 'r=2: ''A'' 추가, count={''A'':2,''B'':1}, maxf=2, window크기=3, 변경필요=1 ≤ 2 유효'
      en: 'r=2: Add ''A'', count={''A'':2,''B'':1}, maxf=2, window_size=3, changes_needed=1 ≤ 2 ✓'
    - ko: 'r=3: ''B'' 추가, count={''A'':2,''B'':2}, maxf=2, window크기=4, 변경필요=2 ≤ 2 유효, 반복 종료 후 길이 4 반환'
      en: 'r=3: Add ''B'', count={''A'':2,''B'':2}, maxf=2, window_size=4, changes_needed=2 ≤ 2 ✓, loop ends, return 4'
    answer: '4'
solution:
  code: "class Solution:\n    def characterReplacement(self, s: str, k: int) -> int:\n        count = {}\n        \n        l = 0\n        maxf = 0\n        for r in range(len(s)):\n            count[s[r]] = 1 + count.get(s[r], 0)\n            maxf = max(maxf, count[s[r]])\n\n            if (r - l + 1) - maxf > k:\n                count[s[l]] -= 1\n                l += 1\n\n        return (r - l + 1)\n"
  complexity:
    time: O(n)
    space: O(1)
  followup:
  - ko: 문자열에 소문자나 숫자가 포함되면 공간 복잡도는 어떻게 될까요?
    en: What would the space complexity be if the string could contain lowercase letters or digits?
  - ko: k번 이내에서 삽입, 삭제, 치환을 모두 할 수 있다면?
    en: How would the solution change if we could also delete characters within k operations?
  - ko: 문제를 일반화하여 임의의 길이 길이의 반복 패턴을 만들 수 있다면?
    en: What if we needed to find the longest substring with any repeating pattern (not just single character)?
```
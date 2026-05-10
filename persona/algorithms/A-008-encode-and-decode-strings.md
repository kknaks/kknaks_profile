---
created: '2026-05-10'
date: '2026-05-10'
day: Day 08
difficulty: medium
id: A-008
source:
  curated_in:
  - neetcode150
  number: 271
  platform: leetcode
  slug: encode-and-decode-strings
  url: https://leetcode.com/problems/encode-and-decode-strings/
status: draft
tags:
- array
- string
- design
title:
  en: Encode and Decode Strings
  ko: 문자열 인코딩과 디코딩
today: true
type: algorithm
updated: '2026-05-10'
visible: true
---

# 문자열 인코딩과 디코딩

## Data

```yaml
problem:
  title:
    ko: 문자열 인코딩과 디코딩
    en: Encode and Decode Strings
  statement:
    ko: '문자열 목록을 하나의 인코딩된 문자열로 변환하는 encode 함수와, 인코딩된 문자열을 원래의 문자열 목록으로 복원하는 decode 함수를 설계하세요.


      인코딩 포맷은 쉼표나 특수 문자를 포함할 수 있는 임의의 문자열을 정확히 처리할 수 있어야 합니다. 빈 문자열도 포함될 수 있습니다.'
    en: 'Design an encoder and decoder for a list of strings.


      The encode function converts a list of strings into a single encoded string. The decode function takes the encoded string and reconstructs the original list of strings.


      The encoding scheme must reliably handle arbitrary strings, including those containing special characters and empty strings.'
  constraints:
  - 1 ≤ number of strings ≤ 1e2
  - 0 ≤ length of each string ≤ 1e4
  - Strings can contain any ASCII characters
  io:
  - input: '["Hello","World"]'
    output: 5#Hello5#World
  - input: '[""]'
    output: 0#
clarifying:
  items:
  - q:
      ko: 인코딩된 문자열에서 어떻게 각 문자열의 경계를 구분할 것인가?
      en: How do we distinguish where one encoded string ends and another begins?
    type: good
    why:
      ko: 길이 접두사(length prefix)를 사용하면 각 문자열의 정확한 끝 위치를 알 수 있어 모든 문자를 정확히 디코딩할 수 있습니다.
      en: Using a length prefix ensures we know exactly where each string ends, allowing precise decoding regardless of string content.
  - q:
      ko: 빈 문자열(empty string)은 어떻게 처리되는가?
      en: How are empty strings handled in the encoding?
    type: good
    why:
      ko: 길이가 0인 경우 "0#"로 인코딩되어 빈 문자열을 올바르게 표현합니다.
      en: An empty string encodes as "0#", preserving empty strings in the input list.
  - q:
      ko: '"#" 문자가 원본 문자열에 포함되면 어떻게 되는가?'
      en: What if the input strings contain the '#' delimiter character?
    type: good
    why:
      ko: 길이 접두사를 사용하므로 "#" 문자는 구분자가 아닌 데이터의 일부로 취급되어 문제가 없습니다.
      en: The length prefix approach treats '#' as data, not a delimiter, so it poses no issue.
  - q:
      ko: '매우 큰 문자열(예: 1e4 길이)도 효율적으로 처리되는가?'
      en: Does the solution efficiently handle very large strings?
    type: good
    why:
      ko: 전체 문자의 개수에 비례하는 선형 시간으로 처리되므로 효율적입니다.
      en: Linear time complexity proportional to total characters ensures efficiency.
  - q:
      ko: CSV 형식(쉼표로 구분)을 사용하면 더 간단하지 않을까?
      en: Wouldn't using CSV format with commas be simpler?
    type: distractor
    why:
      ko: CSV는 쉼표나 개행 문자를 포함한 문자열을 처리하려면 이스케이핑이 필요하여 더 복잡합니다.
      en: CSV requires escaping for strings containing commas or newlines, adding unnecessary complexity.
  - q:
      ko: '각 문자열을 고정 길이(예: 4바이트) 정수로 인코딩하는 것이 낫지 않을까?'
      en: Wouldn't fixed-width length fields be better than variable-length numbers?
    type: distractor
    why:
      ko: 가변 길이 숫자를 "#"으로 구분하는 방식이 더 간단하고 작은 문자열에서 더 효율적입니다.
      en: Variable-length is simpler to parse and more space-efficient for smaller strings.
  - q:
      ko: 디코더에서 길이를 어떻게 파싱하는가?
      en: How does the decoder identify where the length number ends?
    type: good
    why:
      ko: '"#" 문자를 만날 때까지 숫자를 읽으면, 그 이후부터 정확히 그 길이만큼 문자열을 추출합니다.'
      en: Reading digits until '#' is encountered marks the boundary, then exactly that many characters follow.
approach:
  items:
  - name:
      ko: 길이 접두사 + 구분자 (Length Prefix)
      en: Length Prefix with Delimiter
    complexity: O(n) time / O(n) space
    type: good
    why:
      ko: 각 문자열 앞에 길이를 붙이고 "#"로 구분하면, 디코딩할 때 정확히 몇 개의 문자를 읽을지 알 수 있어 모든 문자를 안전하게 처리할 수 있습니다.
      en: Prepending the length with '#' as a separator allows the decoder to know exactly how many characters to read, reliably handling any string content.
  - name:
      ko: 고정 너비 길이 필드 (Fixed-Width Encoding)
      en: Fixed-Width Length Field
    complexity: O(n) time / O(n + k) space
    type: distractor
    why:
      ko: 예를 들어 항상 4바이트로 길이를 인코딩하면 파싱이 간단해지지만, 빈 공간이 많아져 작은 문자열에서 비효율적입니다.
      en: Using a fixed number of bytes (e.g., 4) for length simplifies parsing but wastes space on short strings.
  - name:
      ko: CSV 형식 + 이스케이핑 (CSV with Escaping)
      en: CSV with Escaping
    complexity: O(n) time / O(n) space
    type: distractor
    why:
      ko: 쉼표를 구분자로 사용하되, 쉼표나 개행이 포함된 문자열은 따옴표로 감싸고 이스케이핑합니다. 더 많은 엣지 케이스를 고려해야 합니다.
      en: Requires escaping commas and quotes within strings, adding parsing complexity with multiple edge cases.
  - name:
      ko: 구분자만 사용 (Delimiter-Only, 위험)
      en: Delimiter-Only (Unsafe)
    complexity: O(n) time / O(n) space
    type: distractor
    why:
      ko: 단순히 "#"으로만 분리하면, "#"을 포함한 문자열을 올바르게 처리할 수 없어서 데이터 손실이 발생할 수 있습니다.
      en: Splitting only on '#' fails if the original strings contain '#', causing data corruption.
logic:
  format: slot
  slots:
  - label:
      ko: 결과 문자열 초기화
      en: Initialize result string
    indent: 0
    options:
    - code: res = ""
      type: good
      why:
        ko: 인코딩된 결과를 누적할 빈 문자열을 준비합니다.
        en: Start with an empty string to accumulate the encoded result.
    - code: res = []
      type: distractor
      why:
        ko: 리스트를 사용하면 문자열 연결이 비효율적입니다.
        en: Using a list requires converting to string at the end, less clean.
    - code: res = ""s
      type: distractor
      why:
        ko: 문법 오류입니다.
        en: Syntax error.
  - label:
      ko: 각 문자열 반복
      en: Iterate through each string
    indent: 0
    options:
    - code: 'for s in strs:'
      type: good
      why:
        ko: 입력 리스트의 각 문자열을 하나씩 처리합니다.
        en: Process each string in the input list one by one.
    - code: 'for i in range(len(strs)):'
      type: distractor
      why:
        ko: 인덱스를 사용하면 불필요하게 복잡해집니다.
        en: Index-based iteration is unnecessarily verbose.
    - code: 'while strs:'
      type: distractor
      why:
        ko: while 루프를 사용하면 strs 리스트가 변경되어 문제가 발생합니다.
        en: Modifying the list during iteration causes issues.
  - label:
      ko: 길이 + 구분자 + 문자열 추가
      en: Append length marker and string
    indent: 1
    options:
    - code: res += str(len(s)) + "#" + s
      type: good
      why:
        ko: '각 문자열의 길이를 "#" 구분자와 함께 붙인 후, 문자열 자체를 추가합니다. 예: "Hello" → "5#Hello"'
        en: Encode as [length]#[string], e.g., "Hello" becomes "5#Hello". The length lets the decoder know exactly how many characters follow.
    - code: res += s + "#" + str(len(s))
      type: distractor
      why:
        ko: 문자열 뒤에 길이를 붙이면 디코딩할 때 길이를 모르고 시작하게 됩니다.
        en: Putting length after the string defeats the purpose—the decoder doesn't know how many chars to read.
    - code: res += "#" + str(len(s)) + s
      type: distractor
      why:
        ko: '"#"이 먼저 오면 디코더가 길이를 파싱하기 어렵습니다.'
        en: Leading '#' makes parsing ambiguous—the decoder wouldn't know if it's part of a previous string.
    - code: res += str(len(s)) + s
      type: distractor
      why:
        ko: 구분자가 없으면 "5Hello3Bye"에서 어디서 끝나는지 알 수 없습니다.
        en: Without a delimiter, "5Hello3Bye" is ambiguous—is it ["5Hello3B", "ye"] or ["5Hello", "3Bye"]?
  - label:
      ko: 인코딩된 결과 반환
      en: Return the encoded string
    indent: 0
    options:
    - code: return res
      type: good
      why:
        ko: 모든 문자열을 처리한 후 완성된 인코딩 문자열을 반환합니다.
        en: Return the fully encoded string after processing all input strings.
    - code: return res[:-1]
      type: distractor
      why:
        ko: 마지막 문자를 제거하는 것은 잘못되었으며, 마지막 문자열의 일부를 손실시킵니다.
        en: Removing the last character corrupts the final string.
    - code: return ""
      type: distractor
      why:
        ko: 빈 문자열을 반환하면 인코딩이 모두 손실됩니다.
        en: Returns empty, losing all encoded data.
trace:
  code:
  - 'class Solution:'
  - '    def encode(self, strs):'
  - '        res = ""'
  - '        for s in strs:'
  - '            res += str(len(s)) + "#" + s'
  - '        return res'
  - ''
  - '    def decode(self, s):'
  - '        res = []'
  - '        i = 0'
  - '        '
  - '        while i < len(s):'
  - '            j = i'
  - '            while s[j] != ''#'':'
  - '                j += 1'
  - '            length = int(s[i:j])'
  - '            i = j + 1'
  - '            j = i + length'
  - '            res.append(s[i:j])'
  - '            i = j'
  - '            '
  - '        return res'
  cases:
  - input: '["Hello","World"]'
    expected: 5#Hello5#World
  - input: '[""]'
    expected: 0#
  worked_example:
    input: '["Hello","World"]'
    steps:
    - ko: '입력: ["Hello", "World"]'
      en: 'Input: ["Hello", "World"]'
    - ko: '첫 번째 문자열 "Hello": 길이=5, "5#" + "Hello" = "5#Hello" 추가'
      en: 'First string "Hello": length=5, append "5#Hello"'
    - ko: '두 번째 문자열 "World": 길이=5, "5#" + "World" = "5#World" 추가'
      en: 'Second string "World": length=5, append "5#World"'
    - ko: '최종 결과: "5#Hello" + "5#World" = "5#Hello5#World"'
      en: 'Final result: "5#Hello5#World"'
    answer: 5#Hello5#World
solution:
  code: "class Solution:\n    def encode(self, strs):\n        res = \"\"\n        for s in strs:\n            res += str(len(s)) + \"#\" + s\n        return res\n\n    def decode(self, s):\n        res = []\n        i = 0\n        \n        while i < len(s):\n            j = i\n            while s[j] != '#':\n                j += 1\n            length = int(s[i:j])\n            i = j + 1\n            j = i + length\n            res.append(s[i:j])\n            i = j\n            \n        return res\n"
  complexity:
    time: O(n)
    space: O(n)
  followup:
  - ko: 만약 문자열이 매우 크거나 리스트가 매우 길다면, 효율성을 더 개선할 수 있을까요?
    en: If strings could be very large or the list very long, could you optimize further (e.g., using a StringBuilder or streaming)?
  - ko: 입력에 null 문자열이 포함될 수 있다면 어떻게 처리해야 할까요?
    en: How would you handle null strings in the input list?
  - ko: 문자열 리스트 대신 중첩된 리스트나 딕셔너리 같은 복잡한 구조를 인코딩할 수 있을까요?
    en: Could this approach extend to encoding nested structures like lists of lists or dictionaries?
```
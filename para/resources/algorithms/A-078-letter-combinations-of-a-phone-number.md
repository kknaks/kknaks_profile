---
created: '2026-08-05'
date: '2026-08-05'
day: Day 78
difficulty: medium
id: A-078
source:
  curated_in:
  - neetcode150
  number: 17
  platform: leetcode
  slug: letter-combinations-of-a-phone-number
  url: https://leetcode.com/problems/letter-combinations-of-a-phone-number/
tags:
- hash-table
- string
- backtracking
title:
  en: Letter Combinations of a Phone Number
  ko: 전화 번호의 글자 조합
today: false
type: algorithm
updated: '2026-08-05'
visible: true
---

# 전화 번호의 글자 조합

## Data

```yaml
problem:
  title:
    ko: 전화 번호의 글자 조합
    en: Letter Combinations of a Phone Number
  statement:
    ko: '2~9 범위의 숫자를 포함하는 문자열이 주어졌을 때, 그 숫자들이 나타낼 수 있는 모든 가능한 글자 조합을 반환하세요. 답은 어떤 순서로든 반환해도 됩니다.


      전화 버튼의 숫자-글자 매핑이 다음과 같이 주어집니다. 1은 어떤 글자에도 매핑되지 않습니다.'
    en: 'Given a string containing digits from 2-9 inclusive, return all possible letter combinations that the number could represent. Return the answer in any order.


      A mapping of digits to letters (just like on the telephone buttons) is given below. Note that 1 does not map to any letters.'
  constraints:
  - 1 ≤ digits.length ≤ 4
  - digits[i] is a digit in the range ['2', '9']
  io:
  - input: '"23"'
    output: '["ad","ae","af","bd","be","bf","cd","ce","cf"]'
  - input: '"2"'
    output: '["a","b","c"]'
clarifying:
  items:
  - q:
      ko: 1은 어떤 글자에도 매핑되지 않나요?
      en: Does 1 not map to any letters?
    type: good
    why:
      ko: 문제 설명에서 1은 매핑되지 않는다고 명시되어 있으며, 제약 조건에서 숫자 범위가 2~9로 제한됩니다.
      en: The problem statement explicitly says 1 does not map to any letters, and constraints specify digits are in range [2, 9].
  - q:
      ko: 결과의 순서가 중요한가요?
      en: Does the order of the result matter?
    type: good
    why:
      ko: 문제에서 "어떤 순서로든 반환해도 됩니다"라고 명시되어 있습니다.
      en: The problem explicitly states 'Return the answer in any order.'
  - q:
      ko: 빈 문자열이 입력되면 어떻게 되나요?
      en: What if the input string is empty?
    type: good
    why:
      ko: 제약 조건에서 최소 길이가 1이므로 빈 입력은 없습니다. 그러나 방어적 코딩을 위해 빈 입력 시 빈 리스트를 반환해야 합니다.
      en: Constraints guarantee minimum length is 1, so empty input shouldn't occur. However, defensive code should handle and return an empty list.
  - q:
      ko: 가능한 조합의 최대 개수는 몇 개인가요?
      en: What is the maximum number of combinations possible?
    type: good
    why:
      ko: 최대 4자리 숫자이고 각 숫자는 최대 4개의 글자로 매핑되므로(7은 'qprs'), 최대 4^4 = 256개의 조합이 가능합니다.
      en: With maximum 4 digits and each digit mapping to at most 4 letters (7 → 'qprs'), maximum is 4^4 = 256 combinations.
  - q:
      ko: 0이나 1이 입력에 포함될 수 있나요?
      en: Can 0 or 1 appear in the input string?
    type: distractor
    why:
      ko: 아니요. 제약 조건에서 명확히 2~9 범위만 가능하다고 명시되어 있습니다.
      en: No. The constraints explicitly specify that digits are only in range [2, 9].
  - q:
      ko: 같은 숫자가 여러 번 나타날 수 있나요?
      en: Can the same digit appear multiple times?
    type: distractor
    why:
      ko: 예, 가능합니다. 예를 들어 '223' 같은 입력이 가능하며, 각 위치의 숫자는 독립적으로 처리됩니다.
      en: Yes. For example, '223' is valid. Each digit position is processed independently regardless of repetition.
  - q:
      ko: 결과를 사전식 정렬(lexicographic order)로 반환해야 하나요?
      en: Should the result be in lexicographic order?
    type: distractor
    why:
      ko: 아니요. 문제에서 "어떤 순서로든 반환해도 됩니다"라고 명시되어 있습니다.
      en: No. The problem states 'return in any order,' so sorting is not required.
approach:
  items:
  - name:
      ko: 백트래킹 (재귀)
      en: Backtracking (Recursive)
    complexity: O(4^n × n) time / O(4^n) space
    type: good
    why:
      ko: 각 숫자마다 최대 4개의 선택지가 있어 4^n개의 조합이 생깁니다. 각 조합 생성에 O(n), 모든 결과 저장에 O(4^n)이 필요합니다.
      en: Each digit has up to 4 choices, generating 4^n combinations. Building each takes O(n), and storing all results requires O(4^n) space.
  - name:
      ko: 반복적 구축 (레벨별 처리)
      en: Iterative Level-by-Level Build
    complexity: O(4^n × n) time / O(4^n) space
    type: good
    why:
      ko: 큐나 리스트를 이용해 한 숫자씩 처리하며, 각 단계에서 이전 결과에 새로운 글자를 추가합니다. 시간/공간 복잡도는 백트래킹과 동일합니다.
      en: Build combinations iteratively by processing one digit at a time and appending its letters to existing combinations. Same complexity as backtracking.
  - name:
      ko: 고정 크기 중첩 반복문
      en: Nested Loops (Fixed-Size)
    complexity: O(4^4) = O(256) time / O(256) space
    type: distractor
    why:
      ko: 입력이 정확히 4자리라고 가정하면 4중 반복문을 사용할 수 있지만, 문제는 가변 길이를 요구하므로 확장성이 없습니다.
      en: Works only if digits length is exactly 4. Problem requires handling variable-length inputs (1-4), so this is not scalable.
  - name:
      ko: 전체 순열 생성
      en: Generate All Permutations
    complexity: O(n!) time / O(n) space
    type: distractor
    why:
      ko: 입력의 모든 순열을 생성하는 것은 이 문제에 필요하지 않으며, 복잡도도 훨씬 높습니다. 우리는 조합만 필요합니다.
      en: Generating permutations of input digits is unnecessary and inefficient. This problem needs combinations, not permutations.
  - name:
      ko: 매핑 테이블만 사용
      en: Mapping Table Lookup Only
    complexity: O(1) time / O(1) space
    type: distractor
    why:
      ko: 매핑 테이블만으로는 실제 조합을 생성할 수 없습니다. 조합을 만들기 위해 백트래킹이나 반복 로직이 필수입니다.
      en: A mapping table only stores digit-to-letters correspondence. It cannot generate combinations without additional algorithmic logic.
logic:
  format: slot
  slots:
  - label:
      ko: 결과 리스트 초기화
      en: Initialize result list
    indent: 0
    options:
    - code: res = []
      type: good
      why:
        ko: 모든 글자 조합을 저장할 빈 리스트를 생성합니다.
        en: Create an empty list to store all generated letter combinations.
    - code: res = {}
      type: distractor
      why:
        ko: 딕셔너리는 순서 있는 결과 리스트로 작동하지 않습니다.
        en: Dictionary doesn't maintain an ordered list of string combinations.
    - code: res = set()
      type: distractor
      why:
        ko: 집합을 사용하면 중복 제거는 불필요하고 순서도 보장되지 않습니다.
        en: Set doesn't preserve order and unnecessary here since there are no duplicates.
  - label:
      ko: 숫자→글자 매핑 생성
      en: Create digit-to-letters mapping
    indent: 0
    options:
    - code: digitToChar = {
      type: good
      why:
        ko: 전화 번호판의 각 숫자(2~9)가 매핑되는 글자들을 정의합니다.
        en: Define a dictionary mapping each digit (2-9) to its corresponding telephone keypad letters.
    - code: digitToChar = [["abc"], ["def"], ["ghi"], ["jkl"], ["mno"], ["qprs"], ["tuv"], ["wxyz"]]
      type: distractor
      why:
        ko: 리스트 기반 매핑은 실제 숫자를 인덱스로 변환해야 하므로 복잡하고 오류가 발생하기 쉽습니다.
        en: List-based mapping requires converting digits to indices, making code error-prone and less readable.
    - code: 'digitToChar = {"a": "2", "b": "2", "c": "2", ...}'
      type: distractor
      why:
        ko: 글자→숫자의 역방향 매핑이므로 문제 해결에 사용할 수 없습니다.
        en: This is reverse mapping (letters to digits), opposite of what we need (digits to letters).
  - label:
      ko: 백트래킹 재귀함수 정의
      en: Define backtracking recursive function
    indent: 0
    options:
    - code: 'def backtrack(i, curStr):'
      type: good
      why:
        ko: 현재 처리할 숫자의 인덱스(i)와 지금까지 만든 조합 문자열(curStr)을 매개변수로 하는 재귀함수를 정의합니다.
        en: Define recursive function with current digit index (i) and current combination string (curStr) as parameters.
    - code: 'def backtrack(curStr):'
      type: distractor
      why:
        ko: 인덱스 없이는 다음에 어떤 숫자를 처리할지 알 수 없습니다.
        en: Without index parameter, we cannot track which digit to process next.
    - code: 'def backtrack(i):'
      type: distractor
      why:
        ko: 현재까지 만든 조합을 추적할 방법이 없어 결과를 구축할 수 없습니다.
        en: Without the combination string, we cannot build the result incrementally.
  - label:
      ko: '기저 사례: 모든 숫자 처리 완료'
      en: 'Base case: all digits processed'
    indent: 1
    options:
    - code: 'if len(curStr) == len(digits):'
      type: good
      why:
        ko: 현재 조합 문자열의 길이가 입력 숫자 개수와 같으면 하나의 완전한 조합이 완성되었습니다.
        en: When current combination length equals input length, one complete combination is formed.
    - code: 'if i == len(digits):'
      type: distractor
      why:
        ko: 이 조건도 작동하지만, curStr 길이 확인이 더 명확합니다.
        en: Also works due to algorithm structure, but checking string length is clearer semantically.
    - code: 'if len(curStr) >= len(digits):'
      type: distractor
      why:
        ko: \">=\" 조건은 불필요합니다. 우리는 정확히 같을 때만 조합이 완성됩니다.
        en: '''>='' is wrong; we only add one letter per call, so equality check is correct.'
  - label:
      ko: 완성된 조합을 결과에 추가
      en: Append completed combination to result
    indent: 2
    options:
    - code: res.append(curStr)
      type: good
      why:
        ko: 기저 사례에 도달한 완성된 조합 문자열을 결과 리스트에 추가합니다.
        en: Add the completed combination string to the result list.
    - code: res.append(list(curStr))
      type: distractor
      why:
        ko: 문제는 문자열 리스트를 요구하지, 리스트의 리스트가 아닙니다.
        en: Problem expects list of strings, not list of character lists.
    - code: res.add(curStr)
      type: distractor
      why:
        ko: res는 리스트이므로 add() 메서드가 없습니다. append()를 사용해야 합니다.
        en: res is a list; use append(), not add() (which is for sets).
  - label:
      ko: 현재 숫자의 글자들을 순회
      en: Iterate through current digit's letters
    indent: 1
    options:
    - code: 'for c in digitToChar[digits[i]]:'
      type: good
      why:
        ko: 현재 처리할 숫자(digits[i])에 매핑된 모든 글자를 하나씩 순회합니다.
        en: Loop through each letter mapped to the current digit (digits[i]).
    - code: 'for c in digitToChar.values():'
      type: distractor
      why:
        ko: 모든 매핑값을 순회하므로 현재 숫자의 글자만 선택하지 못합니다.
        en: Iterates through all mapping values, not just current digit's letters.
    - code: 'for c in digits:'
      type: distractor
      why:
        ko: 숫자 문자를 순회하지, 글자를 순회하지 않습니다.
        en: This iterates over digits themselves, not the letters they map to.
  - label:
      ko: 다음 숫자로 재귀 호출
      en: Recursively process next digit
    indent: 2
    options:
    - code: backtrack(i + 1, curStr + c)
      type: good
      why:
        ko: 현재 글자를 추가한 후 인덱스를 증가시켜 다음 숫자를 재귀적으로 처리합니다.
        en: Call recursively with next index (i+1) and append current letter to combination.
    - code: backtrack(i, curStr + c)
      type: distractor
      why:
        ko: 인덱스를 증가시키지 않으면 같은 숫자에 무한 반복됩니다.
        en: Without incrementing i, would process same digit infinitely.
    - code: backtrack(i + 1, c)
      type: distractor
      why:
        ko: 이전 글자들이 손실됩니다. 지금까지의 조합 전체를 유지해야 합니다.
        en: Passing only current letter loses the previously built combination string.
  - label:
      ko: 빈 입력 처리
      en: Handle empty input
    indent: 0
    options:
    - code: 'if digits:'
      type: good
      why:
        ko: 입력이 비어있으면 백트래킹을 시작하지 않고 빈 리스트를 반환합니다.
        en: If digits is empty, skip backtracking and return empty list.
    - code: 'if len(digits) > 0:'
      type: distractor
      why:
        ko: 논리적으로 동일하지만, 문제의 제약에서 입력은 항상 1 이상이므로 불필요합니다.
        en: Logically equivalent, but constraints guarantee length ≥ 1, so unnecessary.
    - code: 'if digits != "":'
      type: distractor
      why:
        ko: 마찬가지로 불필요합니다.
        en: Also unnecessary given constraints.
trace:
  code:
  - 'class Solution:'
  - '    def letterCombinations(self, digits: str) -> List[str]:'
  - '        res = []'
  - '        digitToChar = {'
  - '            "2": "abc",'
  - '            "3": "def",'
  - '            "4": "ghi",'
  - '            "5": "jkl",'
  - '            "6": "mno",'
  - '            "7": "qprs",'
  - '            "8": "tuv",'
  - '            "9": "wxyz",'
  - '        }'
  - ''
  - '        def backtrack(i, curStr):'
  - '            if len(curStr) == len(digits):'
  - '                res.append(curStr)'
  - '                return'
  - '            for c in digitToChar[digits[i]]:'
  - '                backtrack(i + 1, curStr + c)'
  - ''
  - '        if digits:'
  - '            backtrack(0, "")'
  - ''
  - '        return res'
  cases:
  - input: '"23"'
    expected: '["ad","ae","af","bd","be","bf","cd","ce","cf"]'
  - input: '"2"'
    expected: '["a","b","c"]'
  worked_example:
    input: '"23"'
    steps:
    - ko: digits = "23", backtrack(0, "") 호출
      en: 'Start: digits = "23", call backtrack(0, "")'
    - ko: 'i=0: digits[0]=''2'' → ''abc''. 각 글자마다 backtrack(1, ''a''/''b''/''c'') 호출'
      en: 'i=0: digits[0]=''2'' maps to ''abc''. For each, call backtrack(1, ''a''/''b''/''c'')'
    - ko: 'i=1: digits[1]=''3'' → ''def''. 예: backtrack(1, ''a'')에서 backtrack(2, ''ad''/''ae''/''af'') 호출'
      en: 'i=1: digits[1]=''3'' maps to ''def''. For backtrack(1, ''a''), call backtrack(2, ''ad''/''ae''/''af'')'
    - ko: len(curStr)==len(digits)==2 도달 시 기저 사례. 'ad', 'ae', 'af'... 'cf'까지 9개 추가
      en: 'Base case: len(curStr)==2. Add all 9 combinations: ''ad'', ''ae'', ''af'', ..., ''cf'''
    answer: '["ad","ae","af","bd","be","bf","cd","ce","cf"]'
solution:
  code: "class Solution:\n    def letterCombinations(self, digits: str) -> List[str]:\n        res = []\n        digitToChar = {\n            \"2\": \"abc\",\n            \"3\": \"def\",\n            \"4\": \"ghi\",\n            \"5\": \"jkl\",\n            \"6\": \"mno\",\n            \"7\": \"qprs\",\n            \"8\": \"tuv\",\n            \"9\": \"wxyz\",\n        }\n\n        def backtrack(i, curStr):\n            if len(curStr) == len(digits):\n                res.append(curStr)\n                return\n            for c in digitToChar[digits[i]]:\n                backtrack(i + 1, curStr + c)\n\n        if digits:\n            backtrack(0, \"\")\n\n        return res\n"
  complexity:
    time: O(4^n × n)
    space: O(4^n)
  followup:
  - ko: 입력에 0이 포함될 수 있다면? (0은 보통 공백이나 특수 글자에 매핑)
    en: What if 0 is in the input? (0 typically maps to space or no letters)
  - ko: 재귀 대신 반복(iterative) 방식으로 구현하려면?
    en: How would you implement this iteratively without recursion?
  - ko: '입력이 매우 크다면(예: 100자리) 메모리를 절약하려면?'
    en: How to optimize for very large inputs (e.g., 100+ digits) given exponential result size?
```
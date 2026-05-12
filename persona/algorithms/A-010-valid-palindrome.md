---
created: '2026-05-12'
date: '2026-05-12'
day: Day 10
difficulty: easy
id: A-010
source:
  curated_in:
  - neetcode150
  number: 125
  platform: leetcode
  slug: valid-palindrome
  url: https://leetcode.com/problems/valid-palindrome/
status: draft
tags:
- two-pointers
- string
title:
  en: Valid Palindrome
  ko: 올바른 팰린드롬
today: true
type: algorithm
updated: '2026-05-12'
visible: true
---

# 올바른 팰린드롬

## Data

```yaml
problem:
  title:
    ko: 올바른 팰린드롬
    en: Valid Palindrome
  statement:
    ko: '문구가 팰린드롬인지 판별하는 방법: 모든 대문자를 소문자로 변환하고 모든 영숫자가 아닌 문자를 제거한 후, 앞에서 읽으나 뒤에서 읽으나 같은지 확인합니다. 영숫자 문자는 문자와 숫자를 포함합니다.


      주어진 문자열 s에 대해, 이것이 팰린드롬이면 true를 반환하고, 그렇지 않으면 false를 반환하세요.'
    en: 'A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward. Alphanumeric characters include letters and numbers.


      Given a string s, return true if it is a palindrome, or false otherwise.'
  constraints:
  - 1 ≤ s.length ≤ 2 × 10⁵
  - s consists only of printable ASCII characters
  io:
  - input: '"A man, a plan, a canal: Panama"'
    output: 'true'
  - input: '"race a car"'
    output: 'false'
  - input: '" "'
    output: 'true'
clarifying:
  items:
  - q:
      ko: 대문자는 어떻게 처리해야 하나요?
      en: What should we do with uppercase letters?
    type: good
    why:
      ko: 모든 대문자를 소문자로 변환하여 비교 시 대소문자를 구분하지 않도록 합니다.
      en: Convert all uppercase letters to lowercase so comparison is case-insensitive.
  - q:
      ko: 어떤 문자를 유지해야 하나요?
      en: Which characters should we keep?
    type: good
    why:
      ko: 문자와 숫자만 유지하고 공백, 구두점, 특수문자 등 모든 영숫자가 아닌 문자는 제거합니다.
      en: Keep only alphanumeric characters (letters and numbers); remove spaces, punctuation, and special characters.
  - q:
      ko: 문자열이 팰린드롬인지 어떻게 확인하나요?
      en: How do we check if a string is a palindrome?
    type: good
    why:
      ko: 정제된 문자열을 그 역순과 비교하여 같은지 확인합니다.
      en: Compare the cleaned string with its reverse; if they match, it's a palindrome.
  - q:
      ko: 입력이 빈 문자열이거나 영숫자가 없으면 어떻게 되나요?
      en: What if the input is empty or contains only non-alphanumeric characters?
    type: good
    why:
      ko: 정제 후 빈 문자열이 되며, 빈 문자열은 앞뒤로 읽으나 같으므로 true를 반환합니다.
      en: After cleaning, it becomes an empty string, which reads the same forward and backward, so return true.
  - q:
      ko: 공백은 제거하되 구두점은 유지해야 하나요?
      en: Should we remove spaces but keep punctuation?
    type: distractor
    why:
      ko: 아니오, 공백과 모든 구두점을 포함한 모든 영숫자가 아닌 문자를 제거해야 합니다.
      en: No, we must remove all non-alphanumeric characters, including spaces and punctuation.
  - q:
      ko: 원본 문자열이 그대로 팰린드롬인지 확인하나요?
      en: Do we check if the original string is a palindrome as-is?
    type: distractor
    why:
      ko: 아니오, 먼저 정제하고 정규화한 후의 문자열로 팰린드롬 여부를 판단해야 합니다.
      en: No, we must check the palindrome property after cleaning and normalizing the string.
  - q:
      ko: 정제된 버전을 저장하기 위해 추가 공간을 사용할 수 있나요?
      en: Can we use extra space to store a cleaned version?
    type: good
    why:
      ko: 네, 간단하고 직관적인 구현을 위해 정제된 문자열을 별도로 저장할 수 있습니다.
      en: Yes, storing a cleaned string simplifies implementation, though two-pointer uses O(1) space.
approach:
  items:
  - name:
      ko: 정제 후 역순 비교
      en: Clean then reverse compare
    complexity: O(n) time / O(n) space
    type: good
    why:
      ko: 정제된 문자열을 생성한 후 원본과 역순을 비교하는 직관적이고 구현하기 쉬운 방법입니다.
      en: Build a cleaned string, then compare it with its reverse. Intuitive and simple to implement.
  - name:
      ko: 투 포인터
      en: Two pointers
    complexity: O(n) time / O(1) space
    type: good
    why:
      ko: 양끝에서 시작하는 두 개의 포인터를 사용하여 문자를 비교하면서 진행하여 추가 공간을 사용하지 않습니다.
      en: Use pointers from both ends, comparing characters while skipping non-alphanumeric chars. Achieves O(1) space.
  - name:
      ko: 정규식 기반 필터링
      en: Regex-based filtering
    complexity: O(n) time / O(n) space
    type: distractor
    why:
      ko: 정규식으로 비영숫자 문자를 제거할 수 있지만, 인터뷰에서는 기본 문자열 메서드를 사용하는 것이 더 명확합니다.
      en: While regex can filter non-alphanumeric characters, using basic string methods is clearer for interviews.
  - name:
      ko: 스택 사용
      en: Stack-based approach
    complexity: O(n) time / O(n) space
    type: distractor
    why:
      ko: 스택을 사용하여 문자를 저장했다가 역순으로 비교할 수 있지만, 단순히 슬라이싱을 사용하는 것이 더 효율적입니다.
      en: We could use a stack to reverse and compare, but Python's slicing is simpler and equally efficient.
  - name:
      ko: 모든 부분 문자열 확인 (브루트 포스)
      en: Check all substrings (brute force)
    complexity: O(n²) time / O(n) space
    type: distractor
    why:
      ko: 모든 부분 문자열이 팰린드롬인지 확인하는 방식은 비효율적이고 문제 요구사항과 맞지 않습니다.
      en: Checking if all substrings are palindromes is inefficient and doesn't match the problem requirement.
logic:
  format: slot
  slots:
  - label:
      ko: 정제된 문자열 초기화
      en: Initialize cleaned string
    indent: 0
    options:
    - code: new = ''
      type: good
      why:
        ko: 빈 문자열로 시작하여 정제된 문자를 누적할 변수를 준비합니다.
        en: Start with an empty string to accumulate cleaned characters.
    - code: new = []
      type: distractor
      why:
        ko: 리스트는 작동하지만 후에 문자열 역순 연산자[::-1]을 사용할 수 없습니다.
        en: Lists work for accumulation, but string reversal with [::-1] won't work directly.
    - code: new = None
      type: distractor
      why:
        ko: 초기화되지 않은 상태로 후속 연산에서 오류가 발생합니다.
        en: None is not initialized; later operations will fail.
    - code: cleaned = ''
      type: distractor
      why:
        ko: 변수명이 다르면 후속 코드에서 참조 오류가 발생합니다.
        en: Different variable name causes reference errors in subsequent code.
  - label:
      ko: 입력 문자열 반복
      en: Iterate through input string
    indent: 0
    options:
    - code: 'for a in s:'
      type: good
      why:
        ko: 각 문자를 순차적으로 처리하기 위해 입력 문자열을 반복합니다.
        en: Loop through each character in the input string to process them sequentially.
    - code: 'for i in range(len(s)):'
      type: distractor
      why:
        ko: 인덱스로 반복하는 방식은 작동하지만 더 장황하고 s[i] 접근이 필요합니다.
        en: Index-based loop works but is more verbose and requires s[i] access.
    - code: 'for a in s.lower():'
      type: distractor
      why:
        ko: 미리 소문자로 변환하면 영숫자 필터링과 변환 로직이 섞이는 결과가 됩니다.
        en: Lowercasing early mixes concerns; we should filter first, then lowercase.
  - label:
      ko: 영숫자 문자 필터링
      en: Filter alphanumeric characters
    indent: 1
    options:
    - code: 'if a.isalpha() or a.isdigit():'
      type: good
      why:
        ko: isalpha() 또는 isdigit()을 사용하여 문자와 숫자만 선택하고 다른 문자는 건너뜁니다.
        en: Use isalpha() or isdigit() to keep only letters and numbers, skip everything else.
    - code: 'if not a.isspace():'
      type: distractor
      why:
        ko: 공백만 제외하고 구두점과 특수문자를 포함하게 되어 잘못된 결과를 초래합니다.
        en: Only excludes spaces; keeps punctuation and special characters, leading to wrong answers.
    - code: 'if a.isupper() or a.isdigit():'
      type: distractor
      why:
        ko: 소문자는 필터링되어 정제 후 소문자 문자들이 손실됩니다.
        en: Filters out lowercase letters, losing valid data during cleaning.
    - code: 'if a != '' '' and a != '','':'
      type: distractor
      why:
        ko: 모든 특수문자를 명시적으로 나열할 수 없어 확장성이 떨어집니다.
        en: Can't explicitly list all special characters; not scalable or maintainable.
  - label:
      ko: 소문자 변환 및 누적
      en: Lowercase and accumulate
    indent: 2
    options:
    - code: new += a.lower()
      type: good
      why:
        ko: 선택된 문자를 소문자로 변환하여 정제된 문자열에 추가합니다.
        en: Convert the character to lowercase and append to the cleaned string.
    - code: new += a
      type: distractor
      why:
        ko: 소문자로 변환하지 않으면 대소문자 구분으로 잘못된 비교 결과가 나옵니다.
        en: Without lowercasing, case differences lead to incorrect palindrome checks.
    - code: new.append(a.lower())
      type: distractor
      why:
        ko: 문자열 객체는 append() 메서드를 가지지 않아 AttributeError가 발생합니다.
        en: Strings don't have append(); this causes AttributeError.
    - code: new = new + a.upper()
      type: distractor
      why:
        ko: 대문자로 변환하면 비교 시 일관성이 없어 오류가 발생합니다.
        en: Uppercasing instead of lowercasing causes inconsistency in comparison.
  - label:
      ko: 정제된 문자열과 역순 비교
      en: Compare with reverse
    indent: 0
    options:
    - code: return (new == new[::-1])
      type: good
      why:
        ko: 정제된 문자열이 자신의 역순과 같은지 확인하여 팰린드롬 여부를 판정합니다.
        en: Check if the cleaned string equals its reverse; if yes, it's a palindrome.
    - code: return (new == reversed(new))
      type: distractor
      why:
        ko: reversed()는 반복자 객체를 반환하므로 문자열과 직접 비교할 수 없습니다.
        en: reversed() returns an iterator, not a comparable string object.
    - code: return (s == s[::-1])
      type: distractor
      why:
        ko: 원본 문자열 s를 비교하면 정제 과정을 무시하므로 틀린 결과가 나옵니다.
        en: Comparing original string s ignores cleaning; gives wrong results.
    - code: return len(new) == 0
      type: distractor
      why:
        ko: 문자열 길이가 0인 경우만 true를 반환하므로 팰린드롬 논리와 맞지 않습니다.
        en: Only returns true for empty strings, not checking palindrome property.
trace:
  code:
  - 'class Solution:'
  - '    def isPalindrome(self, s: str) -> bool:'
  - '        new = '''''
  - '        for a in s:'
  - '            if a.isalpha() or a.isdigit():'
  - '                new += a.lower()'
  - '        return (new == new[::-1])'
  cases:
  - input: '"A man, a plan, a canal: Panama"'
    expected: 'true'
  - input: '"race a car"'
    expected: 'false'
  - input: '" "'
    expected: 'true'
  worked_example:
    input: '"A man, a plan, a canal: Panama"'
    steps:
    - ko: '입력: ''A man, a plan, a canal: Panama'''
      en: 'Input: ''A man, a plan, a canal: Panama'''
    - ko: '각 문자를 순회하며 영숫자만 선택하고 소문자로 변환: ''a'', ''m'', ''a'', ''n'', ''a'', ''p'', ''l'', ''a'', ''n'', ''a'', ''c'', ''a'', ''n'', ''a'', ''l'', ''p'', ''a'', ''n'', ''a'', ''m'', ''a'''
      en: 'Iterate through characters, keep only alphanumeric, convert to lowercase: ''a'', ''m'', ''a'', ''n'', ''a'', ''p'', ''l'', ''a'', ''n'', ''a'', ''c'', ''a'', ''n'', ''a'', ''l'', ''p'', ''a'', ''n'', ''a'', ''m'', ''a'''
    - ko: '정제된 문자열: ''amanaplanacanalpanama'''
      en: 'Cleaned string: ''amanaplanacanalpanama'''
    - ko: '역순: ''amanaplanacanalpanama'' (일치) → true 반환'
      en: 'Reverse: ''amanaplanacanalpanama'' (matches) → return true'
    answer: 'true'
solution:
  code: "class Solution:\n    def isPalindrome(self, s: str) -> bool:\n        new = ''\n        for a in s:\n            if a.isalpha() or a.isdigit():\n                new += a.lower()\n        return (new == new[::-1])\n"
  complexity:
    time: O(n)
    space: O(n)
  followup:
  - ko: 투 포인터를 사용하여 O(1) 공간으로 해결할 수 있나요?
    en: Can you solve this with O(1) space using two pointers from both ends?
  - ko: 만약 입력 문자열이 매우 크다면 공간 최적화를 어떻게 할 수 있을까요?
    en: How would you optimize space if the input string is very large?
  - ko: Unicode 문자나 다른 언어의 문자도 처리해야 한다면 어떻게 변경해야 할까요?
    en: How would you modify the solution to handle Unicode or characters from other languages?
```
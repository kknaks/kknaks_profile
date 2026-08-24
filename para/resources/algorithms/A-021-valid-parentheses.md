---
created: '2026-05-23'
date: '2026-05-23'
day: Day 21
difficulty: easy
id: A-021
source:
  curated_in:
  - neetcode150
  number: 20
  platform: leetcode
  slug: valid-parentheses
  url: https://leetcode.com/problems/valid-parentheses/
tags:
- string
- stack
title:
  en: Valid Parentheses
  ko: 유효한 괄호
today: false
type: algorithm
updated: '2026-05-23'
visible: true
---

# 유효한 괄호

## Data

```yaml
problem:
  title:
    ko: 유효한 괄호
    en: Valid Parentheses
  statement:
    en: 'Given a string s containing just the characters ''('', '')'', ''{'', ''}'', ''['' and '']'', determine if the input string is valid.


      An input string is valid if:

      1. Open brackets must be closed by the same type of brackets.

      2. Open brackets must be closed in the correct order.

      3. Every close bracket has a corresponding open bracket of the same type.'
    ko: '괄호 문자 ''('', '')'', ''{'', ''}'', ''['', '']''만 포함하는 문자열 s가 주어질 때, 입력 문자열이 유효한지 판단하세요.


      입력 문자열이 유효하려면:

      1. 열린 괄호는 같은 유형의 괄호로 닫혀야 합니다.

      2. 열린 괄호는 올바른 순서로 닫혀야 합니다.

      3. 모든 닫힌 괄호는 같은 유형의 해당하는 열린 괄호를 가져야 합니다.'
  constraints:
  - 1 ≤ s.length ≤ 10^4
  - s consists of parentheses only '()[]{}'
  io:
  - input: '"()"'
    output: 'true'
  - input: '"()[]{}"'
    output: 'true'
  - input: '"(]"'
    output: 'false'
  - input: '"([])"'
    output: 'true'
  - input: '"([)]"'
    output: 'false'
clarifying:
  items:
  - q:
      ko: 열린 괄호와 닫힌 괄호의 타입이 정확히 일치해야 하나요?
      en: Must opening and closing brackets match in type?
    type: good
    why:
      ko: 네, 조건 1과 3에서 명시합니다. '('는 ')'로만, '['는 ']'로만 닫혀야 합니다.
      en: Yes, conditions 1 and 3 require exact matching. '(' can only close with ')', not with ']' or '}'.
  - q:
      ko: 네스팅된 괄호의 순서가 중요한가요?
      en: Is the order of nested brackets important?
    type: good
    why:
      ko: 네, 조건 2가 '올바른 순서'를 요구합니다. '([)]'는 무효한데, 안쪽 괄호가 먼저 닫혀야 합니다.
      en: Yes, condition 2 requires correct order. '([)]' is invalid because innermost brackets must close before outer ones.
  - q:
      ko: 열린 괄호와 닫힌 괄호의 개수만 세면 충분한가요?
      en: Is counting opening and closing brackets sufficient?
    type: distractor
    why:
      ko: 아니요, 개수 세기만으로는 타입 매칭과 순서를 검증할 수 없습니다.
      en: No, counting ignores type matching and ordering. '([)]' has correct counts but is invalid due to wrong nesting order.
  - q:
      ko: 스택 자료구조가 반드시 필요한가요?
      en: Is a stack data structure essential?
    type: good
    why:
      ko: 네, 스택은 가장 최근의 열린 괄호를 추적하고 LIFO 순서로 매칭을 검증하는 데 이상적입니다.
      en: Yes, a stack naturally enforces LIFO matching and tracks unmatched opening brackets efficiently.
  - q:
      ko: 문자열을 역순으로 처리해야 하나요?
      en: Should the string be processed backwards?
    type: distractor
    why:
      ko: 아니요, 정방향 처리가 필요합니다. 역순은 괄호 매칭 논리를 복잡하게 만듭니다.
      en: No, forward processing is correct. Processing backwards would break the bracket matching logic.
  - q:
      ko: 모든 괄호가 처리된 후 스택이 비어있다는 것은 무엇을 의미하나요?
      en: What does an empty stack at the end signify?
    type: good
    why:
      ko: 모든 열린 괄호가 유효하게 매칭되어 닫혔다는 의미입니다.
      en: It means every opening bracket found a matching closing bracket. Anything remaining in the stack is an unmatched opening bracket.
approach:
  items:
  - name:
      ko: 스택 + 닫힘-열림 매핑
      en: Stack with closing-to-opening map
    complexity: O(n) time / O(1) space
    type: good
    why:
      ko: 닫힌 괄호를 만날 때마다 스택 최상위와 즉시 비교합니다. 맵은 고정 크기(3개)이므로 O(1)입니다.
      en: Each closing bracket is immediately matched against the stack top. Map has fixed size (3 entries), so O(1) auxiliary space besides the stack itself.
  - name:
      ko: 재귀적 괄호 검증
      en: Recursive matching
    complexity: O(n) time / O(n) space
    type: distractor
    why:
      ko: 재귀로 구현 가능하지만 콜 스택으로 O(n) 공간이 필요하고 복잡합니다.
      en: While possible, recursion uses O(n) call stack space and is unnecessarily complex compared to iterative approach.
  - name:
      ko: 카운터 기반 접근
      en: Counter-based approach
    complexity: O(n) time / O(1) space
    type: distractor
    why:
      ko: 각 괄호 타입의 개수만 세면 순서 검증을 놓쳐서 '([)]' 같은 무효한 경우를 통과시킵니다.
      en: Counting alone ignores ordering requirements and would incorrectly validate '([)]' as true.
  - name:
      ko: 정규표현식 반복 제거
      en: Regex-based pair removal
    complexity: O(n²) time / O(n) space
    type: distractor
    why:
      ko: 연속된 매칭 쌍을 반복 제거하지만, 각 반복마다 전체 문자열을 스캔해야 해서 비효율적입니다.
      en: Repeatedly removing matched pairs works but rescans the string each iteration, making it O(n²) and less efficient.
logic:
  format: slot
  slots:
  - label:
      ko: 닫힌 괄호 매핑 초기화
      en: Initialize closing-to-opening map
    indent: 0
    options:
    - code: 'bracketMap = {")": "(", "]": "[", "}": "{"}'
      type: good
      why:
        ko: 닫힌 괄호를 만날 때 해당하는 열린 괄호를 O(1)에 찾기 위해 사전에 정의합니다.
        en: Pre-define a map to quickly look up the expected opening bracket when a closing bracket is encountered.
    - code: 'bracketMap = {"(": ")", "[": "]", "{": "}"}'
      type: distractor
      why:
        ko: 역방향 매핑은 닫힌 괄호 입력에서 열린 괄호를 찾기 어렵습니다.
        en: This maps opening to closing, but we need closing to opening for efficient lookup when processing the string.
    - code: bracketMap = {"()", "[]", "{}"}
      type: distractor
      why:
        ko: 세트로는 키-값 매핑이 불가능합니다.
        en: Sets don't support key-value mapping. A dictionary is required.
  - label:
      ko: 스택 초기화
      en: Initialize empty stack
    indent: 0
    options:
    - code: stack = []
      type: good
      why:
        ko: 열린 괄호를 저장하고 LIFO 순서로 검증하기 위해 비어있는 스택을 준비합니다.
        en: Initialize an empty list to store opening brackets and verify matching in last-in-first-out order.
    - code: stack = {}
      type: distractor
      why:
        ko: 딕셔너리는 LIFO 순서를 보장하지 않습니다.
        en: A dictionary doesn't guarantee LIFO order. A list is needed for proper stack behavior.
    - code: stack = set()
      type: distractor
      why:
        ko: 세트는 순서를 보장하지 않고, 중복된 괄호를 추적할 수 없습니다.
        en: Sets don't maintain order and can't track multiple identical brackets correctly.
  - label:
      ko: 각 문자에 대해 반복
      en: Iterate through each character
    indent: 0
    options:
    - code: 'for c in s:'
      type: good
      why:
        ko: 문자열의 모든 문자를 순차적으로 처리하여 유효성을 검증합니다.
        en: Process each character sequentially to validate bracket pairs one by one.
    - code: 'for c in s.reverse():'
      type: distractor
      why:
        ko: 역순 처리는 괄호 매칭 논리를 깨뜨립니다.
        en: Reverse iteration breaks the bracket matching logic.
    - code: 'for i in range(len(s) - 1):'
      type: distractor
      why:
        ko: 마지막 문자를 놓치게 됩니다.
        en: This skips the last character of the string.
  - label:
      ko: 열린 괄호 처리
      en: Handle opening brackets
    indent: 2
    options:
    - code: stack.append(c)
      type: good
      why:
        ko: 열린 괄호는 매핑에 없으므로 스택에 추가하여 나중에 매칭할 대상으로 저장합니다.
        en: Opening brackets are not in the map keys, so push them to the stack for future matching with closing brackets.
    - code: stack.pop()
      type: distractor
      why:
        ko: 열린 괄호를 만났을 때 pop하면 오류입니다. 먼저 추가해야 합니다.
        en: Never pop on opening brackets. They must be added first to have something to match later.
    - code: return True
      type: distractor
      why:
        ko: 열린 괄호를 만났다고 즉시 참을 반환할 수 없습니다.
        en: Cannot return immediately. The entire string must be processed.
  - label:
      ko: 닫힌 괄호 검증
      en: Validate closing bracket
    indent: 2
    options:
    - code: 'if not stack or stack[-1] != bracketMap[c]:'
      type: good
      why:
        ko: '닫힌 괄호를 만나면: (1) 스택이 비어있지 않은지, (2) 최상위가 매칭되는 열린 괄호인지 모두 확인합니다.'
        en: 'For closing brackets: verify both that the stack is non-empty AND the stack top matches the expected opening bracket.'
    - code: 'if stack or stack[-1] != bracketMap[c]:'
      type: distractor
      why:
        ko: '''or'' 대신 ''and''를 써야 합니다. 두 조건을 모두 만족해야 합니다.'
        en: Should use 'and' not 'or'. Both conditions must be true for the bracket to be valid.
    - code: 'if stack[-1] == bracketMap[c]:'
      type: distractor
      why:
        ko: 스택이 비어있을 때 stack[-1] 접근이 IndexError를 발생시킵니다.
        en: This causes IndexError if the stack is empty. Must check non-empty first.
  - label:
      ko: 매칭된 열린 괄호 제거
      en: Pop matched opening bracket
    indent: 2
    options:
    - code: stack.pop()
      type: good
      why:
        ko: 닫힌 괄호가 유효하게 매칭되었으므로, 스택에서 해당하는 열린 괄호를 제거합니다.
        en: After confirming a match, remove the opening bracket from the stack to continue validating remaining brackets.
    - code: stack.append(c)
      type: distractor
      why:
        ko: 닫힌 괄호를 스택에 추가하는 것은 잘못되었습니다.
        en: Adding the closing bracket to the stack is incorrect. We must remove the matched pair.
    - code: return True
      type: distractor
      why:
        ko: 일부만 확인했으므로 바로 참을 반환할 수 없습니다.
        en: Cannot return true immediately. All characters must be validated.
  - label:
      ko: 최종 유효성 반환
      en: Return validity result
    indent: 0
    options:
    - code: return not stack
      type: good
      why:
        ko: 모든 문자 처리 후, 스택이 비어있으면 모든 괄호가 올바르게 매칭된 것입니다.
        en: After processing all characters, the string is valid only if the stack is empty (all brackets matched).
    - code: return stack
      type: distractor
      why:
        ko: 스택 객체 자체를 반환하면 불린 값이 아닙니다.
        en: Returning the stack object is not a boolean. Must check if it's empty.
    - code: return bool(stack)
      type: distractor
      why:
        ko: 스택이 비어있으면 거짓(유효함)이므로 논리가 역순입니다.
        en: This returns True if stack has elements, but that means invalid. Logic is backward.
trace:
  code:
  - 'class Solution:'
  - '    def isValid(self, s: str) -> bool:'
  - '        bracketMap = {")": "(", "]": "[", "}": "{"}'
  - '        stack = []'
  - ''
  - '        for c in s:'
  - '            if c not in bracketMap:'
  - '                stack.append(c)'
  - '                continue'
  - '            if not stack or stack[-1] != bracketMap[c]:'
  - '                return False'
  - '            stack.pop()'
  - ''
  - '        return not stack'
  cases:
  - input: '"()"'
    expected: 'true'
  - input: '"()[]{}"'
    expected: 'true'
  - input: '"(]"'
    expected: 'false'
  - input: '"([])"'
    expected: 'true'
  - input: '"([)]"'
    expected: 'false'
  worked_example:
    input: '"()"'
    steps:
    - ko: '초기화: stack = [], bracketMap = {'')'': ''('', '']'': ''['', ''}'': ''{''} 준비'
      en: 'Initialize: stack = [], bracketMap ready with 3 closing-to-opening pairs'
    - ko: '처리 ''('': ''('' 는 bracketMap에 없으므로 stack에 추가 → stack = [''('']'
      en: 'Process ''('': not a map key, so push to stack → stack = [''('']'
    - ko: '처리 '')'': bracketMap['')''] = ''('', stack[-1] = ''('' 로 일치 → pop → stack = []'
      en: 'Process '')'': bracketMap['')''] = ''('' matches stack[-1], so pop → stack = []'
    - ko: '모든 문자 처리 완료: stack이 비어있으므로 not stack = True 반환'
      en: 'All characters processed: stack is empty, so return not stack = True'
    answer: 'true'
solution:
  code: "class Solution:\n    def isValid(self, s: str) -> bool:\n        bracketMap = {\")\": \"(\", \"]\": \"[\", \"}\": \"{\"}\n        stack = []\n\n        for c in s:\n            if c not in bracketMap:\n                stack.append(c)\n                continue\n            if not stack or stack[-1] != bracketMap[c]:\n                return False\n            stack.pop()\n\n        return not stack\n"
  complexity:
    time: O(n)
    space: O(n)
  followup:
  - ko: 문자열에 괄호 외의 다른 문자도 포함된다면 어떻게 처리하시겠어요?
    en: What if the string contained letters and digits mixed with brackets? How would you adapt the solution?
  - ko: 괄호 깊이의 최대값을 추적하면서 진행한다면, 이를 어떻게 구현하시겠어요?
    en: How would you modify this to also track and return the maximum nesting depth of brackets?
  - ko: O(1) 공간을 사용하여 이 문제를 풀 수 있을까요? (스택 사용 불가)
    en: Can you solve this with O(1) space without using a separate stack data structure?
```
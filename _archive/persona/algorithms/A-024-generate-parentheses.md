---
created: '2026-05-28'
date: '2026-05-28'
day: Day 24
difficulty: medium
id: A-024
source:
  curated_in:
  - neetcode150
  number: 22
  platform: leetcode
  slug: generate-parentheses
  url: https://leetcode.com/problems/generate-parentheses/
status: draft
tags:
- string
- dynamic-programming
- backtracking
title:
  en: Generate Parentheses
  ko: 괄호 생성하기
today: false
type: algorithm
updated: '2026-05-28'
visible: true
---

# 괄호 생성하기

## Data

```yaml
problem:
  title:
    ko: 괄호 생성하기
    en: Generate Parentheses
  statement:
    ko: n개의 괄호 쌍이 주어졌을 때, 올바르게 형성된 괄호의 모든 조합을 생성하는 함수를 작성하시오.
    en: Given n pairs of parentheses, write a function to generate all combinations of well-formed parentheses.
  constraints:
  - 1 ≤ n ≤ 8
  io:
  - input: '3'
    output: '["((()))","(()())","(())()","()(())","()()()"]'
  - input: '1'
    output: '["()"]'
clarifying:
  items:
  - q:
      ko: 올바르게 형성된 괄호란 정확히 무엇인가?
      en: What exactly does well-formed parentheses mean?
    type: good
    why:
      ko: 모든 열린 괄호는 그 뒤에 대응하는 닫힌 괄호를 가져야 하며, 임의의 접두사에서 열린 괄호의 개수가 닫힌 괄호의 개수보다 크거나 같아야 한다.
      en: Every opening parenthesis must have a matching closing parenthesis after it, and at any prefix, opened ≥ closed.
  - q:
      ko: 출력이 특정 순서로 정렬되어야 하는가?
      en: Must the output be in a specific order or can it be any order?
    type: good
    why:
      ko: 문제는 예시에서 하나의 순서를 보여주지만 명시적으로 정렬을 요구하지 않는다. 어떤 순서든 모든 올바른 조합이 포함되면 된다.
      en: The problem shows one possible order but doesn't explicitly require sorting. Any order is acceptable as long as all valid combinations are included.
  - q:
      ko: n=3일 때 총 몇 개의 괄호 문자가 있는가?
      en: For n=3, how many total parenthesis characters are there?
    type: good
    why:
      ko: n은 괄호 쌍의 개수이므로 총 2n개의 문자(n개의 열린 괄호와 n개의 닫힌 괄호)가 있다.
      en: 'n represents the number of pairs, so there are 2n total characters: n opening and n closing.'
  - q:
      ko: 모든 2^(2n)개의 이진 조합을 생성한 후 필터링하는 것이 좋은 접근법인가?
      en: Is it a good approach to generate all 2^(2n) binary combinations then filter for valid ones?
    type: distractor
    why:
      ko: 기술적으로 작동하지만 비효율적이다. 대부분의 조합이 유효하지 않으므로 많은 시간을 낭비한다.
      en: While it works, it's inefficient—most combinations are invalid, wasting time generating and filtering them.
  - q:
      ko: 임의의 시점에서 열린 괄호와 닫힌 괄호의 개수 사이에는 어떤 관계가 있어야 하는가?
      en: What must be the relationship between open and closed counts at any point?
    type: good
    why:
      ko: 유효한 접두사에서는 항상 openCount ≥ closedCount이어야 한다. 이것이 핵심 제약 조건이며 백트래킹을 가능하게 한다.
      en: 'In any valid prefix: openCount ≥ closedCount. This invariant is key to pruning efficiently.'
  - q:
      ko: 첫 번째에 n개의 열린 괄호를 모두 사용한 후 닫힌 괄호를 추가할 수 있는가?
      en: Can we place all n opening parentheses first, then add closing ones?
    type: distractor
    why:
      ko: 기술적으로 가능한 부분 경로이지만, 모든 올바른 조합을 생성하려면 다양한 분기를 탐색해야 한다.
      en: While a valid partial path, exploring only this branch misses many valid combinations like ()()().
  - q:
      ko: 주어진 n에 대해 정확히 몇 개의 올바른 조합이 존재하는가?
      en: How many valid combinations exist for a given n?
    type: good
    why:
      ko: 정확히 n번째 카탈란 수 C_n개이다. 이는 솔루션의 효율성을 평가하는 데 도움이 된다.
      en: Exactly the nth Catalan number. Understanding this helps evaluate whether an approach is optimal.
approach:
  items:
  - name:
      ko: 카운터를 이용한 백트래킹
      en: Backtracking with open/closed counters
    complexity: O(4^n / √n) time, O(n) space
    type: good
    why:
      ko: 열린 괄호와 닫힌 괄호의 개수를 추적하면서 유효한 조합만 생성한다. 제약 조건을 확인하여 불가능한 분기를 조기에 제거한다.
      en: Tracks open/closed counts to generate only valid combinations. Prunes invalid branches early by checking constraints.
  - name:
      ko: 유효성 조건을 이용한 재귀
      en: Recursion with validity constraints
    complexity: O(4^n / √n) time, O(n) space
    type: good
    why:
      ko: 백트래킹과 동일한 개념으로, 임의의 시점에서 closedN ≤ openN을 확인하여 유효성을 보장한다.
      en: Same as backtracking conceptually—ensures closedN ≤ openN at all times to maintain validity.
  - name:
      ko: 모든 가능성 생성 후 필터링
      en: 'Brute force: generate all 2^(2n) strings and filter'
    complexity: O(4^n × n) time, O(4^n) space
    type: distractor
    why:
      ko: 모든 가능한 0과 1의 조합을 생성한 후 유효한 것만 걸러낸다. 대부분이 유효하지 않아 매우 비효율적이다.
      en: Generates all binary combinations, then filters valid ones. Very inefficient since most won't be valid.
  - name:
      ko: 동적 프로그래밍으로 개수만 계산
      en: Dynamic programming using Catalan recurrence
    complexity: O(n) time, O(n) space
    type: distractor
    why:
      ko: 올바른 조합의 개수는 계산할 수 있지만, 실제 조합을 생성하지는 않는다. 문제는 모든 조합을 나열해야 한다.
      en: Can compute the count but doesn't generate the combinations. The problem requires enumerating all of them.
logic:
  format: slot
  slots:
  - label:
      ko: 스택 초기화
      en: Initialize stack
    indent: 0
    options:
    - code: stack = []
      type: good
      why:
        ko: 스택은 현재 구축 중인 괄호 문자열을 저장한다. 빈 스택에서 시작하여 하나씩 추가 및 제거하며 모든 조합을 탐색한다.
        en: Stack holds the current parenthesis string being built. Start empty and add/remove characters one by one.
    - code: res = []
      type: distractor
      why:
        ko: 이것은 결과를 저장하는 것이고, 현재 조합을 저장하지 않는다.
        en: This stores results, not the current partial combination being built.
    - code: stack = set()
      type: distractor
      why:
        ko: 집합은 순서를 유지하지 않아 괄호 문자열을 만드는 데 부적절하다.
        en: A set doesn't maintain order, essential for building valid parenthesis strings.
    - code: stack = {}
      type: distractor
      why:
        ko: 딕셔너리는 선형 문자열 순서를 관리하기에 적합하지 않다.
        en: A dictionary structure isn't suitable for building a sequential string.
  - label:
      ko: 결과 리스트 초기화
      en: Initialize results list
    indent: 0
    options:
    - code: res = []
      type: good
      why:
        ko: 모든 유효한 조합을 모으는 컨테이너다. 각 완성된 조합이 여기에 추가된다.
        en: Container for collecting all valid combinations. Each completed combination is added here.
    - code: res = set()
      type: distractor
      why:
        ko: 집합을 사용하면 중복 제거는 되지만 출력 순서를 제어할 수 없다.
        en: A set removes duplicates (not needed here) but loses ordering of combinations.
    - code: res = {}
      type: distractor
      why:
        ko: 딕셔너리는 여러 문자열을 순서대로 저장하는 데 부적절하다.
        en: A dictionary isn't the right structure for a list of string combinations.
  - label:
      ko: 기저 사례 확인
      en: Check base case
    indent: 1
    options:
    - code: 'if openN == closedN == n:'
      type: good
      why:
        ko: 열린 괄호와 닫힌 괄호의 개수가 모두 n과 같을 때 종료 조건이다. 이때만 정확히 n개의 유효한 조합이 완성되었다.
        en: When both openN and closedN equal n, we've placed all n pairs correctly. This is when to add to results.
    - code: 'if openN == n:'
      type: distractor
      why:
        ko: 열린 괄호만 확인하는 것은 불충분하다. 닫힌 괄호도 n개여야 한다.
        en: Checking only openN isn't enough—we must also ensure closedN == n for a complete string.
    - code: 'if openN + closedN == 2 * n:'
      type: distractor
      why:
        ko: 합이 2n이어도 각각이 정확히 n이 아닐 수 있다. 각 조건을 명시적으로 확인해야 한다.
        en: Two values can sum to 2n without each being exactly n. Need both conditions explicitly.
    - code: 'if len(stack) == 2 * n:'
      type: distractor
      why:
        ko: 스택의 길이만으로는 올바른 배치를 보장하지 않는다. 각 타입의 개수를 확인해야 한다.
        en: Stack length alone doesn't guarantee correct distribution of open vs closed.
  - label:
      ko: 열린 괄호 추가 조건
      en: 'Constraint: can add opening paren'
    indent: 1
    options:
    - code: 'if openN < n:'
      type: good
      why:
        ko: openN < n일 때만 더 많은 열린 괄호를 추가할 수 있다. n개를 초과하면 정확히 n개의 쌍을 만들 수 없다.
        en: Only add opening parens if openN < n. Otherwise we'd exceed n pairs total.
    - code: 'if openN <= n:'
      type: distractor
      why:
        ko: openN이 이미 n이면 하나 더 추가하면 한계를 넘는다.
        en: If openN == n already, we can't add more without exceeding the limit.
    - code: 'if closedN < openN:'
      type: distractor
      why:
        ko: 이것은 닫힌 괄호를 추가할 수 있는지 확인하는 조건이다.
        en: This checks if we can add closing parens, not opening ones.
    - code: 'if openN < closedN:'
      type: distractor
      why:
        ko: 이 조건은 항상 거짓이므로 열린 괄호를 절대 추가하지 않는다.
        en: This would always be false (openN ≥ closedN by our invariant), so we'd never add opening parens.
  - label:
      ko: 닫힌 괄호 추가 조건
      en: 'Constraint: can add closing paren'
    indent: 1
    options:
    - code: 'if closedN < openN:'
      type: good
      why:
        ko: closedN < openN일 때만 닫힌 괄호를 추가할 수 있다. 닫힌 괄호의 개수는 열린 괄호의 개수를 초과할 수 없다.
        en: Only add closing parens if closedN < openN. Ensures we never close more than we've opened (validity invariant).
    - code: 'if closedN <= openN:'
      type: distractor
      why:
        ko: closedN == openN이면 모든 열린 괄호가 이미 닫혔으므로 더 이상 닫힐 것이 없다.
        en: If closedN == openN, adding more closing parens would close unmatched parens.
    - code: 'if closedN < n:'
      type: distractor
      why:
        ko: 닫힌 괄호의 개수만 확인하면 열린 괄호보다 많이 추가될 수 있다.
        en: Checking only closedN < n doesn't prevent closedN from exceeding openN.
    - code: 'if openN < n:'
      type: distractor
      why:
        ko: 이것은 열린 괄호를 추가할 수 있는지 확인하는 조건이다.
        en: This checks if we can add more opening parens, not closing ones.
  - label:
      ko: 백트래킹 시작
      en: Initiate backtracking
    indent: 0
    options:
    - code: backtrack(0, 0)
      type: good
      why:
        ko: 초기 상태(0개의 열린 괄호, 0개의 닫힌 괄호)에서 재귀 탐색을 시작한다. 빈 스택에서 모든 유효한 조합을 찾는다.
        en: 'Start recursive exploration from the initial state: zero opening parens, zero closing parens, empty stack.'
    - code: backtrack(1, 0)
      type: distractor
      why:
        ko: 이미 하나의 열린 괄호가 있는 상태에서 시작하면 첫 닫힌 괄호 없이 시작하는 조합을 놓친다.
        en: Starting with one paren already placed misses combinations that begin differently.
    - code: backtrack(n, n)
      type: distractor
      why:
        ko: 모든 괄호가 이미 배치된 상태에서 시작하면 탐색할 것이 없다.
        en: Starting with all parens placed means exploration is already complete—nothing to explore.
trace:
  code:
  - 'class Solution:'
  - '    def generateParenthesis(self, n: int) -> List[str]:'
  - '        stack = []'
  - '        res = []'
  - ''
  - '        def backtrack(openN, closedN):'
  - '            if openN == closedN == n:'
  - '                res.append("".join(stack))'
  - '                return'
  - ''
  - '            if openN < n:'
  - '                stack.append("(")'
  - '                backtrack(openN + 1, closedN)'
  - '                stack.pop()'
  - '            if closedN < openN:'
  - '                stack.append(")")'
  - '                backtrack(openN, closedN + 1)'
  - '                stack.pop()'
  - ''
  - '        backtrack(0, 0)'
  - '        return res'
  cases:
  - input: '3'
    expected: '["((()))","(()())","(())()","()(())","()()()"]'
  - input: '1'
    expected: '["()"]'
  worked_example:
    input: '3'
    steps:
    - ko: 'backtrack(0, 0) 호출: stack = [], openN = 0, closedN = 0. 기저 사례 불만족이므로 분기 탐색'
      en: 'Call backtrack(0, 0): stack = [], openN = 0, closedN = 0. Base case not met, explore branches.'
    - ko: 'openN < 3이므로 ''('' 추가: stack = [''(''], backtrack(1, 0) 호출'
      en: 'openN < 3, so add ''('': stack = [''(''], call backtrack(1, 0)'
    - ko: '계속 재귀: ''(('', ''((('' 추가. openN = 3일 때는 열린 괄호를 더 추가할 수 없으므로 closedN < openN 분기로'
      en: 'Continue recursively: add ''(('', then ''(((''. When openN = 3, can only add closing parens.'
    - ko: 'closedN < openN이므로 '')'' 추가: ''((()'' → ''((())'' → ''((()))''. openN == closedN == 3이면 "((()))" 를 결과에 추가'
      en: 'closedN < openN, add '')'': build ''((()'' → ''((())'' → ''(())''. Append "((()))" to results.'
    - ko: '백트래킹하며 다른 분기 탐색: 스택에서 문자 제거, 다른 경로 시도. "(()())" "(())()" "()(())" "()()()" 등 모든 5개 조합 생성'
      en: 'Backtrack and explore alternatives: pop from stack, try different branches. Generate all 5 valid combinations.'
    answer: '["((()))","(()())","(())()","()(())","()()()"]'
solution:
  code: "class Solution:\n    def generateParenthesis(self, n: int) -> List[str]:\n        stack = []\n        res = []\n\n        def backtrack(openN, closedN):\n            if openN == closedN == n:\n                res.append(\"\".join(stack))\n                return\n\n            if openN < n:\n                stack.append(\"(\")\n                backtrack(openN + 1, closedN)\n                stack.pop()\n            if closedN < openN:\n                stack.append(\")\")\n                backtrack(openN, closedN + 1)\n                stack.pop()\n\n        backtrack(0, 0)\n        return res\n"
  complexity:
    time: O(4^n / √n)
    space: O(n)
  followup:
  - ko: 결과를 사전식 순서로 정렬하려면 어떻게 해야 할까?
    en: How would you modify the solution to return results in lexicographically sorted order?
  - ko: 올바른 조합의 개수를 구하려면 어떻게 할까? (실제로 생성하지 않음)
    en: How would you count the number of valid combinations without generating them?
  - ko: 여러 종류의 괄호(소괄호, 중괄호, 대괄호)를 처리하려면 어떻게 할까?
    en: How would you extend the solution to handle multiple bracket types (parentheses, braces, brackets)?
```
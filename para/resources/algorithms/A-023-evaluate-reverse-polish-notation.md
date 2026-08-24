---
created: '2026-05-27'
date: '2026-05-27'
day: Day 23
difficulty: medium
id: A-023
source:
  curated_in:
  - neetcode150
  number: 150
  platform: leetcode
  slug: evaluate-reverse-polish-notation
  url: https://leetcode.com/problems/evaluate-reverse-polish-notation/
tags:
- array
- math
- stack
title:
  en: Evaluate Reverse Polish Notation
  ko: 역폴란드 표기법 계산
today: false
type: algorithm
updated: '2026-05-27'
visible: true
---

# 역폴란드 표기법 계산

## Data

```yaml
problem:
  title:
    ko: 역폴란드 표기법 계산
    en: Evaluate Reverse Polish Notation
  statement:
    ko: '산술 표현식을 역폴란드 표기법(RPN)으로 나타낸 문자열 배열 tokens가 주어집니다.


      표현식을 계산하여 결과를 나타내는 정수를 반환하세요.


      주의:

      - 유효한 연산자는 ''+'', ''-'', ''*'', ''/''입니다.

      - 각 피연산자는 정수입니다.

      - 두 정수의 나눗셈은 항상 0을 향해 절단됩니다.

      - 0으로 나누는 경우는 없습니다.

      - 입력은 유효한 역폴란드 표기법 산술식입니다.

      - 답과 모든 중간 계산 결과는 32비트 정수로 표현 가능합니다.'
    en: 'You are given an array of strings tokens that represents an arithmetic expression in Reverse Polish Notation.


      Evaluate the expression. Return an integer that represents the value of the expression.


      Note that:

      - The valid operators are ''+'', ''-'', ''*'', and ''/''.

      - Each operand may be an integer or another expression.

      - The division between two integers always truncates toward zero.

      - There will not be any division by zero.

      - The input represents a valid arithmetic expression in a reverse polish notation.

      - The answer and all the intermediate calculations can be represented in a 32-bit integer.'
  constraints:
  - 1 ≤ tokens.length ≤ 10⁴
  - tokens[i] is either an operator (+, -, *, /) or an integer in range [-200, 200]
  - Division truncates toward zero
  - No division by zero
  io:
  - input: '["2","1","+","3","*"]'
    output: '9'
  - input: '["4","13","5","/","+"]'
    output: '6'
  - input: '["10","6","9","3","+","-11","*","/","*","17","+","5","+"]'
    output: '22'
clarifying:
  items:
  - q:
      ko: '"0을 향해 절단한다"는 것이 나눗셈에서 무엇을 의미하나요?'
      en: What does 'truncates toward zero' mean for division?
    type: good
    why:
      ko: Python의 정수 나눗셈(//)은 음수에서 바닥값으로 내림하므로, 0을 향한 절단을 위해서는 float 나눗셈 후 int() 변환이 필요합니다.
      en: Python's // operator floors toward negative infinity, not zero. For -13/5, // returns -3 but truncating toward zero should give -2.
  - q:
      ko: 뺄셈과 나눗셈에서 피연산자의 순서가 중요한 이유는 무엇인가요?
      en: Why is operand order critical for subtraction and division?
    type: good
    why:
      ko: 스택에서 첫 번째 pop()은 두 번째 피연산자, 두 번째 pop()은 첫 번째 피연산자입니다. 순서를 뒤바꾸면 결과가 완전히 달라집니다.
      en: First pop() returns the top of stack (second operand), second pop() returns the first operand. Reversing them gives wrong results.
  - q:
      ko: 왜 스택 데이터 구조가 역폴란드 표기법 평가에 적합한가요?
      en: Why is a stack ideal for evaluating Reverse Polish Notation?
    type: good
    why:
      ko: RPN에서 피연산자들은 연산자를 만나기 전에 저장되고, 연산자를 만나면 가장 최근의 두 피연산자를 꺼내야 합니다. 이는 스택의 LIFO 특성과 정확히 일치합니다.
      en: RPN requires storing operands until an operator is encountered, then immediately using the most recent two operands. This LIFO pattern matches stack perfectly.
  - q:
      ko: '"-11"처럼 음수 피연산자를 어떻게 구분하나요?'
      en: How do we distinguish negative operands like '-11' from the minus operator?
    type: good
    why:
      ko: 연산자는 항상 단일 문자 '+', '-', '*', '/'입니다. 다른 문자열은 모두 정수로 파싱합니다. int()는 음수 기호를 올바르게 처리합니다.
      en: 'Operators are always single characters: ''+'', ''-'', ''*'', ''/''. Any other token (including ''-11'') is parsed as integer. int() handles negative signs correctly.'
  - q:
      ko: 덧셈과 곱셈은 교환법칙이 성립하는데 뺄셈과 나눗셈은 아닌 점을 어떻게 처리하나요?
      en: How do we handle that + and * are commutative but - and / are not?
    type: good
    why:
      ko: + 와 *는 순서가 무관하므로 stack.pop() + stack.pop()처럼 바로 사용 가능합니다. 반면 - 와 /는 각 pop 값을 변수에 저장하여 순서를 보존해야 합니다.
      en: 'For +/*, pop order doesn''t matter; pop both and apply directly. For -/÷, save pops in variables to preserve order: a = pop(), b = pop(), then b - a.'
  - q:
      ko: 왜 float(b) / a를 사용한 다음 int()로 변환하나요?
      en: 'Why convert to float division then int() instead of using //?  '
    type: distractor
    why:
      ko: float 나눗셈 후 int()는 0을 향해 절단하지만, // 연산자는 음수에서 바닥값으로 내림합니다.
      en: 'float()/int() truncates toward zero, but // floors toward negative infinity. Example: int(float(-13)/5)=-2 (correct), but -13//5=-3 (wrong).'
  - q:
      ko: 재귀를 사용하여 역폴란드 표기법을 평가할 수 있을까요?
      en: Could we use recursion instead of iteration to evaluate RPN?
    type: distractor
    why:
      ko: 기술적으로는 가능하지만 RPN 평가에 재귀는 불필요합니다. 반복문이 더 효율적이고 간단합니다.
      en: Technically possible, but recursion adds unnecessary complexity. Iterative approach is simpler and standard.
  - q:
      ko: 모든 중간 계산 결과를 모두 저장해야 하나요?
      en: Do we need to store every intermediate calculation result?
    type: distractor
    why:
      ko: 아니요, 스택은 필요한 값들만 자동으로 관리합니다. 마지막에 스택에 남은 값이 최종 결과입니다.
      en: No, stack automatically manages which values to keep. Only the final result remains at the end.
approach:
  items:
  - name:
      ko: 스택 기반 순차 처리
      en: Stack-based sequential processing
    complexity: O(n) time / O(n) space
    type: good
    why:
      ko: 각 토큰을 왼쪽에서 오른쪽으로 순회합니다. 피연산자는 push, 연산자는 top 두 개를 pop하여 계산 후 push합니다.
      en: 'Process each token left-to-right: push operands, pop two operands when encountering an operator, apply the operation, push result. Natural for RPN.'
  - name:
      ko: 재귀 평가
      en: Recursive evaluation
    complexity: O(n) time / O(n) space
    type: distractor
    why:
      ko: 기술적으로 가능하지만 불필요하게 복잡합니다. RPN은 반복문이 자연스럽습니다.
      en: While possible, recursion adds complexity without benefit over iteration.
  - name:
      ko: 중위 표기법으로 변환 후 평가
      en: Convert to infix then evaluate
    complexity: O(n) time / O(n) space
    type: distractor
    why:
      ko: 불필요하게 복잡합니다. RPN은 이미 평가하기 쉬운 형식이므로 변환 단계는 오버헤드입니다.
      en: Unnecessarily complex. RPN is already ideal for direct evaluation; conversion adds overhead.
  - name:
      ko: 큐 기반 처리
      en: Queue-based approach
    complexity: O(n) time / O(n) space
    type: distractor
    why:
      ko: 큐는 FIFO이지만 RPN은 최신 피연산자가 필요하므로 LIFO 스택이 필수입니다.
      en: Queues use FIFO but RPN requires LIFO access to most recent operands. This approach won't work.
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
        ko: LIFO 데이터 구조를 준비합니다. 피연산자와 중간 결과를 저장하는 데 필수적입니다.
        en: Set up the LIFO data structure to store operands and intermediate results.
    - code: queue = []
      type: distractor
      why:
        ko: FIFO이므로 RPN 평가에 적합하지 않습니다.
        en: Queue uses FIFO; RPN requires LIFO for accessing most recent operands.
    - code: nums = {}
      type: distractor
      why:
        ko: 딕셔너리는 순서 기반 접근이 필요한 작업에 부적절합니다.
        en: Dictionary doesn't provide ordered access needed for RPN.
    - code: stack = None
      type: distractor
      why:
        ko: 초기화되지 않아 첫 append 호출에서 오류가 발생합니다.
        en: Uninitialized; will cause AttributeError on first append().
  - label:
      ko: 토큰 순회
      en: Process tokens sequentially
    indent: 0
    options:
    - code: 'for c in tokens:'
      type: good
      why:
        ko: 역폴란드 표기법의 모든 토큰을 왼쪽에서 오른쪽으로 처리합니다.
        en: Iterate through tokens left-to-right, processing operands and operators in order.
    - code: 'for i in range(len(tokens)):'
      type: distractor
      why:
        ko: 작동하지만 불필요하게 장황합니다.
        en: Works but unnecessarily verbose compared to direct iteration.
    - code: 'for c in reversed(tokens):'
      type: distractor
      why:
        ko: 잘못된 순서로 처리하여 잘못된 결과를 낳습니다.
        en: Processing in reverse order will evaluate the expression incorrectly.
  - label:
      ko: 덧셈 연산 (교환법칙 성립)
      en: Addition (commutative operator)
    indent: 2
    options:
    - code: stack.append(stack.pop() + stack.pop())
      type: good
      why:
        ko: 덧셈은 교환법칙이 성립하므로 순서에 관계없이 두 개를 pop하고 더한 후 push합니다.
        en: Addition is commutative, so pop order doesn't matter. Pop, add, and push result.
    - code: a, b = stack.pop(), stack.pop(); stack.append(a + b)
      type: distractor
      why:
        ko: 기술적으로 같은 결과이지만 불필요하게 장황합니다.
        en: Equivalent result but unnecessarily verbose for commutative operation.
    - code: stack.append(stack[0] + stack[1])
      type: distractor
      why:
        ko: 스택의 맨 아래에 접근하여 최신 값을 사용하지 않습니다.
        en: Accesses bottom of stack instead of top; uses wrong operands.
  - label:
      ko: 뺄셈 연산 (순서 보존)
      en: Subtraction (order-dependent)
    indent: 2
    options:
    - code: stack.append(b - a)
      type: good
      why:
        ko: 순서가 중요합니다. 첫 pop은 a(두 번째 피연산자), 두 번째 pop은 b(첫 번째 피연산자)이므로 b - a로 계산합니다.
        en: Order matters. First pop gives a (top/second operand), second pop gives b (first operand). Compute b - a.
    - code: stack.append(a - b)
      type: distractor
      why:
        ko: 뺄셈의 순서가 바뀌어 잘못된 결과입니다.
        en: Reverses operand order; gives wrong result.
    - code: stack.append(stack.pop() - stack.pop())
      type: distractor
      why:
        ko: 순서를 추적하지 않으므로 비교환 연산에서 불명확한 결과를 낳습니다.
        en: Loses operand order tracking; undefined for non-commutative operations.
  - label:
      ko: 나눗셈 (0을 향해 절단)
      en: Division (truncate toward zero)
    indent: 2
    options:
    - code: stack.append(int(float(b) / a))
      type: good
      why:
        ko: float 나눗셈은 정확한 결과를 제공하고, int()로 변환하면 0을 향해 절단됩니다. Python의 // 연산자는 음수에서 바닥값으로 내림하므로 부정확합니다.
        en: float division then int() truncates toward zero. Python's // floors toward negative infinity, failing for negative results.
    - code: stack.append(b // a)
      type: distractor
      why:
        ko: -13 // 5 = -3이지만 올바른 절단은 -2입니다. 음수 결과에서 작동하지 않습니다.
        en: 'Floor division: -13//5=-3 (wrong); truncating toward zero should give -2.'
    - code: stack.append(int(b / a))
      type: distractor
      why:
        ko: 부동 소수점 정밀도 문제가 있을 수 있습니다.
        en: May have floating-point precision issues; explicit float() is safer.
  - label:
      ko: 피연산자 파싱
      en: Push operand values
    indent: 2
    options:
    - code: stack.append(int(c))
      type: good
      why:
        ko: 토큰이 연산자가 아니면 문자열을 정수로 파싱하고 스택에 push합니다. int()는 음수도 올바르게 처리합니다.
        en: Non-operator tokens are parsed from string to integer and pushed. int() correctly handles negative numbers.
    - code: 'if c.isdigit(): stack.append(int(c))'
      type: distractor
      why:
        ko: 음수 피연산자('-11')를 무시합니다.
        en: Rejects negative operands like '-11' since '-' is not a digit.
    - code: stack.append(float(c))
      type: distractor
      why:
        ko: 잘못된 타입입니다. 반환값은 정수여야 합니다.
        en: Wrong type; solution must return integers.
  - label:
      ko: 결과 반환
      en: Return final result
    indent: 0
    options:
    - code: return stack[0]
      type: good
      why:
        ko: 모든 토큰 처리 후 스택에는 최종 결과인 단 하나의 값만 남습니다.
        en: 'After processing all tokens, the stack contains exactly one value: the final result.'
    - code: return sum(stack)
      type: distractor
      why:
        ko: 스택의 모든 값을 합하므로 최종 결과가 아닙니다.
        en: Sums all stack values instead of returning the single result.
    - code: return stack.pop()
      type: distractor
      why:
        ko: 같은 값을 반환하지만 부작용으로 스택을 수정합니다.
        en: Works but modifies the stack (side effect); indexing is cleaner.
trace:
  code:
  - 'class Solution:'
  - '    def evalRPN(self, tokens: List[str]) -> int:'
  - '        stack = []'
  - '        for c in tokens:'
  - '            if c == "+":'
  - '                stack.append(stack.pop() + stack.pop())'
  - '            elif c == "-":'
  - '                a, b = stack.pop(), stack.pop()'
  - '                stack.append(b - a)'
  - '            elif c == "*":'
  - '                stack.append(stack.pop() * stack.pop())'
  - '            elif c == "/":'
  - '                a, b = stack.pop(), stack.pop()'
  - '                stack.append(int(float(b) / a))'
  - '            else:'
  - '                stack.append(int(c))'
  - '        return stack[0]'
  cases:
  - input: '["2","1","+","3","*"]'
    expected: '9'
  - input: '["4","13","5","/","+"]'
    expected: '6'
  - input: '["10","6","9","3","+","-11","*","/","*","17","+","5","+"]'
    expected: '22'
  worked_example:
    input: '["2","1","+","3","*"]'
    steps:
    - ko: '"2" 처리: 정수로 파싱 후 push → stack = [2]'
      en: 'Process ''2'': parse and push → stack = [2]'
    - ko: '"1" 처리: 정수로 파싱 후 push → stack = [2, 1]'
      en: 'Process ''1'': parse and push → stack = [2, 1]'
    - ko: '"+" 처리: pop() 두 번 (1, 2) → 계산 1+2=3 → push → stack = [3]'
      en: 'Process ''+'': pop 1 and 2, add → push 3 → stack = [3]'
    - ko: '"3" 처리: 정수로 파싱 후 push → stack = [3, 3]'
      en: 'Process ''3'': parse and push → stack = [3, 3]'
    - ko: '"*" 처리: pop() 두 번 (3, 3) → 계산 3*3=9 → push → stack = [9] → 반환 9'
      en: 'Process ''*'': pop 3 and 3, multiply → push 9 → stack = [9] → return 9'
    answer: '9'
solution:
  code: "class Solution:\n    def evalRPN(self, tokens: List[str]) -> int:\n        stack = []\n        for c in tokens:\n            if c == \"+\":\n                stack.append(stack.pop() + stack.pop())\n            elif c == \"-\":\n                a, b = stack.pop(), stack.pop()\n                stack.append(b - a)\n            elif c == \"*\":\n                stack.append(stack.pop() * stack.pop())\n            elif c == \"/\":\n                a, b = stack.pop(), stack.pop()\n                stack.append(int(float(b) / a))\n            else:\n                stack.append(int(c))\n        return stack[0]\n"
  complexity:
    time: O(n)
    space: O(n)
  followup:
  - ko: 추가 연산자(^, %, 등)를 지원하려면 어떻게 해야 하나요?
    en: How would you extend this to support additional operators like exponentiation (^) or modulo (%)?
  - ko: 중위 표기법(infix)을 역폴란드 표기법(RPN)으로 변환하려면 어떻게 하나요?
    en: How would you convert an infix expression to RPN (the reverse of this problem)?
  - ko: 부동 소수점 피연산자를 지원하려면 어떻게 수정해야 하나요?
    en: How would you modify this to handle floating-point operands instead of integers?
```
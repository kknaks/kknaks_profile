---
created: '2026-05-27'
date: '2026-05-27'
day: Day 22
difficulty: medium
id: A-022
source:
  curated_in:
  - neetcode150
  number: 155
  platform: leetcode
  slug: min-stack
  url: https://leetcode.com/problems/min-stack/
tags:
- stack
- design
title:
  en: Min Stack
  ko: 최소값 스택
today: false
type: algorithm
updated: '2026-05-27'
visible: true
---

# 최소값 스택

## Data

```yaml
problem:
  title:
    ko: 최소값 스택
    en: Min Stack
  statement:
    ko: '스택이 푸시, 팝, 탑, 그리고 최소 원소를 상수 시간에 검색하는 기능을 지원하도록 설계하세요.


      MinStack 클래스를 구현하세요:

      - MinStack()은 스택 객체를 초기화합니다.

      - void push(int val)은 요소 val을 스택에 추가합니다.

      - void pop()은 스택의 맨 위 요소를 제거합니다.

      - int top()은 스택의 맨 위 요소를 반환합니다.

      - int getMin()은 스택의 최소 원소를 검색합니다.


      모든 함수의 시간 복잡도가 O(1)이어야 합니다.'
    en: 'Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.


      Implement the MinStack class:

      - MinStack() initializes the stack object.

      - void push(int val) pushes the element val onto the stack.

      - void pop() removes the element on the top of the stack.

      - int top() gets the top element of the stack.

      - int getMin() retrieves the minimum element in the stack.


      You must implement a solution with O(1) time complexity for each function.'
  constraints:
  - -2³¹ ≤ val ≤ 2³¹ - 1
  - pop(), top(), and getMin() are always called on non-empty stacks
  - At most 3 × 10⁴ total calls to push, pop, top, and getMin
  io:
  - input: '["MinStack","push","push","push","getMin","pop","top","getMin"]

      [[],[-2],[0],[-3],[],[],[],[]]'
    output: '[null, null, null, null, -3, null, 0, -2]'
clarifying:
  items:
  - q:
      ko: 모든 메서드가 정말 O(1)이어야 하나요?
      en: Do all methods need to be O(1) time?
    type: good
    why:
      ko: 네. 문제에서 명시적으로 모든 함수의 시간 복잡도가 O(1)이어야 한다고 요구합니다.
      en: Yes. The problem explicitly requires O(1) for each function.
  - q:
      ko: 최소값을 구할 때마다 스택 전체를 스캔하면 안 되나요?
      en: Can we scan the entire stack in getMin()?
    type: distractor
    why:
      ko: 아니요. 스캔하면 O(n)이므로 O(1) 요구사항을 위반합니다.
      en: No. Scanning is O(n), violating the O(1) requirement.
  - q:
      ko: 새로운 값이 현재 최소값보다 작으면, 그것이 새로운 최소값이 되나요?
      en: When we push a value smaller than the current minimum, does it become the new minimum?
    type: good
    why:
      ko: 맞습니다. 각 스택 깊이에서 최소값이 변할 수 있으므로 각 레벨의 최소값을 추적해야 합니다.
      en: Yes. The minimum can change at each depth, so we must track it at every level.
  - q:
      ko: 최소값 추적용으로 힙을 사용할 수 있나요?
      en: Can we use a heap to track minimums?
    type: distractor
    why:
      ko: 아니요. 힙은 스택의 LIFO 순서를 유지하지 않으며, pop()에서 임의의 원소를 제거하면 O(n)이 됩니다.
      en: No. Heap doesn't maintain LIFO order; removing arbitrary elements in pop() is O(n).
  - q:
      ko: 최소값 요소를 pop()할 때, 이전 최소값이 자동으로 복구되나요?
      en: When we pop the minimum element, does the previous minimum automatically restore?
    type: good
    why:
      ko: 네. 보조 스택에 각 레벨의 최소값이 저장되어 있으므로, pop할 때 함께 제거되고 이전 최소값이 노출됩니다.
      en: Yes. The auxiliary stack stores the minimum at each level, so the previous minimum is automatically revealed.
  - q:
      ko: getMin()이 스택에서 원소를 제거해야 하나요?
      en: Does getMin() need to remove an element?
    type: distractor
    why:
      ko: 아니요. getMin()은 읽기 전용 연산입니다. pop() 메서드만 제거합니다.
      en: No. getMin() is read-only; only pop() removes elements.
  - q:
      ko: 스택과 최소값을 추적하는 데 하나의 정수 변수만 충분한가요?
      en: Can a single variable track all minimums?
    type: distractor
    why:
      ko: 아니요. pop()할 때 최소값이 변하므로, 각 레벨의 최소값을 모두 저장해야 합니다.
      en: No. The minimum changes when we pop, so we must track it at every level.
approach:
  items:
  - name:
      ko: 보조 스택
      en: Auxiliary Stack
    complexity: O(1) for all operations / O(n) space
    type: good
    why:
      ko: 각 값에 대해 그 시점의 최소값을 별도 스택에 저장하면, 스캔 없이 O(1) getMin()을 구현합니다.
      en: Store the minimum at each level in a separate stack for O(1) getMin() without scanning.
  - name:
      ko: 스택 스캔
      en: Stack Scan
    complexity: O(1) push/pop/top / O(n) getMin
    type: distractor
    why:
      ko: getMin()에서 전체 스택을 검사하면 O(n)이 되어 O(1) 요구사항을 위반합니다.
      en: Scanning the entire stack for getMin() is O(n), violating the O(1) requirement.
  - name:
      ko: 힙 기반 접근
      en: Heap-Based Approach
    complexity: O(log n) push/pop / O(1) getMin
    type: distractor
    why:
      ko: 힙은 스택의 LIFO 순서를 유지하지 못하고, pop()에서 임의의 원소 제거가 O(n)이 필요합니다.
      en: Heap doesn't maintain LIFO order; removing arbitrary elements in pop() is O(n).
  - name:
      ko: 튜플 스택
      en: Tuple Stack
    complexity: O(1) for all operations / O(n) space
    type: good
    why:
      ko: 각 요소를 (value, current_min) 튜플로 저장하면 보조 스택과 동일한 효과를 얻습니다.
      en: Storing (value, current_min) tuples achieves the same as a separate auxiliary stack.
logic:
  format: slot
  slots:
  - label:
      ko: 데이터 구조 초기화
      en: Initialize data structures
    indent: 0
    options:
    - code: self.stack = []
      type: good
      why:
        ko: '이중 스택 구조가 핵심입니다: 하나는 값 저장, 하나는 각 레벨의 최소값 저장.'
        en: 'Dual stacks are essential: one for values, one for minimums at each level.'
    - code: self.stack = {}
      type: distractor
      why:
        ko: 딕셔너리는 LIFO 순서를 보장하지 않습니다.
        en: Dictionary doesn't guarantee LIFO order.
    - code: self.min = float('inf')
      type: distractor
      why:
        ko: 단일 변수로는 pop 후 이전 최소값을 복구할 수 없습니다.
        en: Single variable can't restore previous minimum after pop.
  - label:
      ko: 'Push: 값을 메인 스택에 추가'
      en: 'Push: Add value to main stack'
    indent: 1
    options:
    - code: self.stack.append(val)
      type: good
      why:
        ko: 표준 스택 push 연산으로 새 값을 끝에 추가합니다.
        en: 'Standard stack operation: append the new value to the end.'
    - code: self.stack.insert(0, val)
      type: distractor
      why:
        ko: insert(0, ...)는 O(n)이므로 O(1) 요구사항을 위반합니다.
        en: insert(0, ...) is O(n), violating O(1) requirement.
  - label:
      ko: 'Push: 이 레벨의 최소값 계산'
      en: 'Push: Calculate minimum at this level'
    indent: 1
    options:
    - code: val = min(val, self.minStack[-1] if self.minStack else val)
      type: good
      why:
        ko: '핵심 통찰: 새 값과 이전 최소값 중 더 작은 것이 현재 최소값입니다.'
        en: 'Key insight: the minimum is the smaller of the new value and the previous minimum.'
    - code: val = min(self.stack)
      type: distractor
      why:
        ko: 스택 전체 스캔은 O(n)이므로 O(1) getMin()을 불가능하게 합니다.
        en: Scanning the entire stack is O(n), preventing O(1) getMin().
    - code: val = val
      type: distractor
      why:
        ko: 이전 최소값을 무시하면 새 값이 더 크면 최소값이 잘못됩니다.
        en: Ignoring previous minimum loses it when new value is larger.
  - label:
      ko: 'Push: 최소값을 보조 스택에 저장'
      en: 'Push: Append minimum to auxiliary stack'
    indent: 1
    options:
    - code: self.minStack.append(val)
      type: good
      why:
        ko: 계산된 최소값을 저장하여 메인 스택과의 동기화를 유지합니다.
        en: Store the calculated minimum to keep both stacks synchronized.
    - code: self.minStack.insert(0, val)
      type: distractor
      why:
        ko: insert(0, ...)는 O(n)이므로 O(1) 성능을 깹니다.
        en: insert(0, ...) is O(n), breaking O(1) performance.
  - label:
      ko: 'Pop: 두 스택 모두에서 제거'
      en: 'Pop: Remove from both stacks'
    indent: 1
    options:
    - code: self.stack.pop()
      type: good
      why:
        ko: 메인 스택과 보조 스택의 동기화 불변식을 유지하려면 둘 다 제거해야 합니다.
        en: Must remove from both to maintain synchronization; only removing from one breaks the invariant.
    - code: self.stack.pop()
      type: distractor
      why:
        ko: 메인 스택만 제거하면 보조 스택과 out-of-sync되어 getMin()이 틀립니다.
        en: Removing only from main stack breaks synchronization; getMin() returns wrong value.
  - label:
      ko: 'Top: 맨 위 원소 반환'
      en: 'Top: Return top element'
    indent: 1
    options:
    - code: return self.stack[-1]
      type: good
      why:
        ko: 메인 스택의 맨 위 원소를 반환합니다.
        en: Return the top element from the main stack.
    - code: return self.minStack[-1]
      type: distractor
      why:
        ko: 이것은 최소값이지 탑 원소가 아닙니다.
        en: This returns the minimum, not the top element.
  - label:
      ko: 'GetMin: O(1)에서 최소값 반환'
      en: 'GetMin: Return minimum in O(1)'
    indent: 1
    options:
    - code: return self.minStack[-1]
      type: good
      why:
        ko: 보조 스택의 맨 위가 항상 현재 최소값이므로 O(1) 접근이 가능합니다.
        en: The top of the auxiliary stack is always the current minimum, enabling O(1) access.
    - code: return min(self.stack)
      type: distractor
      why:
        ko: 스택 전체 스캔은 O(n)이므로 O(1) 요구사항을 위반합니다.
        en: Scanning is O(n), violating the O(1) requirement.
trace:
  code:
  - 'class MinStack:'
  - '    def __init__(self):'
  - '        self.stack = []'
  - '        self.minStack = []'
  - ''
  - '    def push(self, val: int) -> None:'
  - '        self.stack.append(val)'
  - '        val = min(val, self.minStack[-1] if self.minStack else val)'
  - '        self.minStack.append(val)'
  - ''
  - '    def pop(self) -> None:'
  - '        self.stack.pop()'
  - '        self.minStack.pop()'
  - ''
  - '    def top(self) -> int:'
  - '        return self.stack[-1]'
  - ''
  - '    def getMin(self) -> int:'
  - '        return self.minStack[-1]'
  cases:
  - input: '["MinStack","push","push","push","getMin","pop","top","getMin"]

      [[],[-2],[0],[-3],[],[],[],[]]'
    expected: '[null, null, null, null, -3, null, 0, -2]'
  worked_example:
    input: '["MinStack","push","push","push","getMin","pop","top","getMin"]

      [[],[-2],[0],[-3],[],[],[],[]]'
    steps:
    - ko: 'MinStack 초기화: stack=[], minStack=[]'
      en: 'Initialize MinStack: stack=[], minStack=[]'
    - ko: 'push(-2), push(0), push(-3) 실행 후: stack=[-2, 0, -3], minStack=[-2, -2, -3] (각 단계의 최소값 추적)'
      en: 'After push(-2), push(0), push(-3): stack=[-2, 0, -3], minStack=[-2, -2, -3] (minimum at each step)'
    - ko: 'getMin() returns -3. pop() 후: stack=[-2, 0], minStack=[-2, -2]. top() returns 0.'
      en: 'getMin() returns -3. After pop(): stack=[-2, 0], minStack=[-2, -2]. top() returns 0.'
    - ko: 최종 getMin() returns -2 (이전 최소값 복구됨)
      en: Final getMin() returns -2 (previous minimum restored)
    answer: '[null, null, null, null, -3, null, 0, -2]'
solution:
  code: "class MinStack:\n    def __init__(self):\n        self.stack = []\n        self.minStack = []\n\n    def push(self, val: int) -> None:\n        self.stack.append(val)\n        val = min(val, self.minStack[-1] if self.minStack else val)\n        self.minStack.append(val)\n\n    def pop(self) -> None:\n        self.stack.pop()\n        self.minStack.pop()\n\n    def top(self) -> int:\n        return self.stack[-1]\n\n    def getMin(self) -> int:\n        return self.minStack[-1]\n"
  complexity:
    time: O(1) for push, pop, top, getMin
    space: O(n) for two stacks of up to n elements each
  followup:
  - ko: getMin()과 getMax()를 모두 O(1)에서 구현하려면?
    en: How would you implement both getMin() and getMax() in O(1)?
  - ko: 스택의 임의의 위치에서 원소를 제거할 수 있어야 한다면, 최소값을 어떻게 추적하시겠어요?
    en: If arbitrary element removal is needed (not just pop), how would you track the minimum?
  - ko: 보조 스택 대신 단일 보조 자료구조로 이 문제를 풀 수 있을까요?
    en: Could you solve this using a single auxiliary structure instead of a full duplicate stack?
```
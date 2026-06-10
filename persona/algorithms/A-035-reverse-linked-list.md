---
created: '2026-06-10'
date: '2026-06-10'
day: Day 35
difficulty: easy
id: A-035
source:
  curated_in:
  - neetcode150
  number: 206
  platform: leetcode
  slug: reverse-linked-list
  url: https://leetcode.com/problems/reverse-linked-list/
status: draft
tags:
- linked-list
- recursion
title:
  en: Reverse Linked List
  ko: 연결 리스트 뒤집기
today: true
type: algorithm
updated: '2026-06-10'
visible: true
---

# 연결 리스트 뒤집기

## Data

```yaml
problem:
  title:
    ko: 연결 리스트 뒤집기
    en: Reverse Linked List
  statement:
    ko: 단일 연결 리스트의 헤드(시작 노드)가 주어질 때, 리스트를 역순으로 뒤집고 역순으로 뒤집어진 리스트를 반환하세요.
    en: Given the head of a singly linked list, reverse the list, and return the reversed list.
  constraints:
  - 0 ≤ number of nodes ≤ 5000
  - -5000 ≤ Node.val ≤ 5000
  io:
  - input: '[1,2,3,4,5]'
    output: '[5,4,3,2,1]'
  - input: '[1,2]'
    output: '[2,1]'
  - input: '[]'
    output: '[]'
clarifying:
  items:
  - q:
      ko: 리스트를 제자리(in-place)에서 뒤집을 수 있나요, 아니면 새 리스트를 만들어도 되나요?
      en: Can we reverse the list in-place, or can we create a new list?
    type: good
    why:
      ko: 공간 복잡도를 최소화할 수 있는지를 묻는 최적화 관련 질문입니다.
      en: This asks about space optimization and whether we can solve it without extra data structures.
  - q:
      ko: 입력이 빈 리스트일 때는 무엇을 반환해야 하나요?
      en: What should we return if the input is an empty list?
    type: good
    why:
      ko: 엣지 케이스 처리를 확인하는 질문으로, 코드가 빈 리스트를 올바르게 처리하는지 검증합니다.
      en: This clarifies edge case behavior and ensures the solution handles empty input correctly.
  - q:
      ko: 입력이 항상 유효한 단일 연결 리스트라고 가정할 수 있나요?
      en: Can we assume the input is always a valid singly linked list?
    type: good
    why:
      ko: 입력 검증이 필요한지를 묻는 질문으로, 문제의 범위를 명확히 합니다.
      en: This clarifies scope and whether input validation is necessary.
  - q:
      ko: 노드의 값을 교환해야 하나요, 아니면 포인터만 변경해야 하나요?
      en: Should we swap node values or just rearrange the pointers?
    type: distractor
    why:
      ko: 노드 값 교환은 비효율적이고 일반적이지 않습니다. 포인터 조작이 표준 방식입니다.
      en: Value swapping is inefficient and unusual; pointer manipulation is the standard approach.
  - q:
      ko: 순환 참조(cycle)가 있는 리스트도 처리해야 하나요?
      en: Do we need to handle lists with cycles?
    type: distractor
    why:
      ko: 문제에서 단일 연결 리스트라고 명시했으므로 순환은 제외됩니다.
      en: The problem specifies a simple singly linked list without cycles.
  - q:
      ko: 양방향 연결 리스트(doubly linked list)도 같은 방법으로 뒤집을 수 있나요?
      en: Can we use the same approach for doubly linked lists?
    type: distractor
    why:
      ko: 양방향 리스트는 추가 이전 포인터 관리가 필요하지만, 이 문제는 단일 연결 리스트만 다룹니다.
      en: Doubly linked lists require handling additional previous pointers, which is out of scope here.
approach:
  items:
  - name:
      ko: 반복적 포인터 역전
      en: Iterative Two-Pointer Reversal
    complexity: O(n) time / O(1) space
    type: good
    why:
      ko: 세 개의 포인터를 사용하여 순회하면서 각 노드의 링크를 역방향으로 변경합니다. 최적의 공간 복잡도를 달성합니다.
      en: Uses three pointers to iterate through the list while reversing each node's link. Achieves optimal space complexity.
  - name:
      ko: 재귀적 역전
      en: Recursive Reversal
    complexity: O(n) time / O(n) space
    type: good
    why:
      ko: 재귀 호출 스택을 이용하여 리스트의 끝에서부터 역으로 링크를 변경합니다. 구현은 우아하지만 스택 공간이 필요합니다.
      en: Uses recursive call stack to reverse links from the end backward. Elegant but requires O(n) stack space.
  - name:
      ko: 스택 사용
      en: Stack-based Approach
    complexity: O(n) time / O(n) space
    type: distractor
    why:
      ko: 모든 노드를 스택에 밀어 넣고 다시 꺼내며 새 리스트를 구성합니다. 작동하지만 추가 공간을 사용하므로 최적이 아닙니다.
      en: Push all nodes to a stack then pop to rebuild the list. Works but uses extra space unnecessarily.
  - name:
      ko: 새 리스트 생성
      en: Create New List
    complexity: O(n) time / O(n) space
    type: distractor
    why:
      ko: 새로운 노드 객체를 생성하여 역순 리스트를 만듭니다. 추가 메모리가 필요하므로 비효율적입니다.
      en: Creates new node objects to build a reversed list. Requires additional memory allocation.
logic:
  format: slot
  slots:
  - label:
      ko: 포인터 초기화
      en: Initialize Pointers
    indent: 0
    options:
    - code: prev, curr = None, head
      type: good
      why:
        ko: prev는 None으로 시작(역방향 체인의 시작), curr은 head로 시작하여 노드를 순회합니다.
        en: prev starts as None (beginning of reversed chain), curr starts at head to traverse nodes.
    - code: prev, curr = head, None
      type: distractor
      why:
        ko: 포인터 할당이 반대이므로 알고리즘이 작동하지 않습니다.
        en: Swapped assignment order breaks the algorithm logic.
    - code: prev = None; curr = head.next
      type: distractor
      why:
        ko: 첫 번째 노드를 건너뛰므로 첫 노드를 잃게 됩니다.
        en: Skips the first node, causing data loss.
  - label:
      ko: 순회 조건
      en: Loop While Nodes Exist
    indent: 0
    options:
    - code: 'while curr:'
      type: good
      why:
        ko: curr이 None이 아닌 동안 계속 순회합니다. None에 도달하면 리스트의 끝에 도달했습니다.
        en: Continue traversing as long as curr is not None. Stops when reaching the end of the list.
    - code: 'while curr.next:'
      type: distractor
      why:
        ko: curr.next가 None일 때 마지막 노드를 처리하지 않습니다.
        en: Skips the last node when curr.next becomes None.
    - code: 'while prev:'
      type: distractor
      why:
        ko: prev는 계속 증가하므로 루프 조건이 의도한 대로 작동하지 않습니다.
        en: prev keeps advancing, causing incorrect loop behavior.
  - label:
      ko: 다음 노드 저장
      en: Save Next Node
    indent: 1
    options:
    - code: temp = curr.next
      type: good
      why:
        ko: 다음 노드의 주소를 임시 변수에 저장합니다. curr.next를 변경하기 전에 반드시 필요합니다.
        en: Saves the address of the next node before modifying curr.next. Essential to avoid losing reference.
    - code: temp = prev
      type: distractor
      why:
        ko: prev를 저장하므로 다음 노드로의 참조를 잃습니다.
        en: Saves prev instead, losing the reference to the next node.
    - code: '# (omitted)'
      type: distractor
      why:
        ko: 이 줄을 생략하면 curr.next 변경 후 다음 노드에 접근할 수 없습니다.
        en: Omitting this causes loss of next node reference after modifying curr.next.
  - label:
      ko: 포인터 역방향
      en: Reverse the Link
    indent: 1
    options:
    - code: curr.next = prev
      type: good
      why:
        ko: 현재 노드의 다음 포인터를 이전 노드로 변경합니다. 링크를 역방향으로 뒤집는 핵심 단계입니다.
        en: Changes current node's next pointer to previous node. This is the key reversal step.
    - code: prev.next = curr
      type: distractor
      why:
        ko: 반대 방향의 할당으로, 순환을 만들 수 있습니다.
        en: Reversed assignment direction, potentially creating cycles.
    - code: curr.prev = prev
      type: distractor
      why:
        ko: prev 속성은 단일 연결 리스트에 없습니다.
        en: Singly linked lists don't have a prev pointer.
  - label:
      ko: prev 이동
      en: Advance prev
    indent: 1
    options:
    - code: prev = curr
      type: good
      why:
        ko: prev를 현재 노드로 이동시킵니다. 역방향 체인을 한 단계 앞으로 진행합니다.
        en: Moves prev to current node. Advances the reversed chain by one step.
    - code: prev = temp
      type: distractor
      why:
        ko: temp는 원래 다음 노드이므로, prev가 역방향 체인에서 뒤로 이동합니다.
        en: temp is the original next node, moving prev backward instead of forward.
    - code: prev = None
      type: distractor
      why:
        ko: prev를 초기화하면 이전 작업이 모두 무효화됩니다.
        en: Resetting prev to None invalidates all previous work.
  - label:
      ko: curr 이동
      en: Advance curr
    indent: 1
    options:
    - code: curr = temp
      type: good
      why:
        ko: curr을 다음 노드로 이동시킵니다. 저장해둔 temp를 사용하여 원래의 다음 노드로 진행합니다.
        en: Moves curr to the next node using the saved temp reference. Continues traversal.
    - code: curr = prev
      type: distractor
      why:
        ko: prev로 이동하면 이미 처리한 노드로 돌아가므로 무한 루프가 됩니다.
        en: Moving to prev creates an infinite loop back to processed nodes.
    - code: curr = curr.next
      type: distractor
      why:
        ko: curr.next는 이미 역방향으로 변경되었으므로 올바른 다음 노드가 아닙니다.
        en: curr.next was already reversed, so this doesn't point to the original next node.
  - label:
      ko: 새 헤드 반환
      en: Return New Head
    indent: 0
    options:
    - code: return prev
      type: good
      why:
        ko: prev는 루프 후 역순 리스트의 새로운 헤드입니다. 원래의 마지막 노드가 첫 번째가 됩니다.
        en: After the loop, prev points to the new head of the reversed list (originally the last node).
    - code: return curr
      type: distractor
      why:
        ko: curr은 루프 후 None이므로 잘못된 반환입니다.
        en: curr is None after the loop, returning incorrect result.
    - code: return head
      type: distractor
      why:
        ko: head는 원래의 첫 노드로, 이제 마지막 노드(None을 가리킴)입니다.
        en: head still points to the original first node, now the last (pointing to None).
trace:
  code:
  - '# Definition for singly-linked list.'
  - '# class ListNode:'
  - '#     def __init__(self, x):'
  - '#         self.val = x'
  - '#         self.next = None'
  - ''
  - ''
  - 'class Solution:'
  - '    def reverseList(self, head: ListNode) -> ListNode:'
  - '        prev, curr = None, head'
  - ''
  - '        while curr:'
  - '            temp = curr.next'
  - '            curr.next = prev'
  - '            prev = curr'
  - '            curr = temp'
  - '        return prev'
  cases:
  - input: '[1,2,3,4,5]'
    expected: '[5,4,3,2,1]'
  - input: '[1,2]'
    expected: '[2,1]'
  - input: '[]'
    expected: '[]'
  worked_example:
    input: '[1,2,3,4,5]'
    steps:
    - ko: '초기: prev=None, curr=노드1. 리스트는 1→2→3→4→5→None'
      en: 'Start: prev=None, curr=Node1. List is 1→2→3→4→5→None'
    - ko: '반복 1: temp=노드2, 노드1→None으로 변경, prev=노드1, curr=노드2'
      en: 'Iter 1: temp=Node2, Node1→None, prev=Node1, curr=Node2'
    - ko: '반복 2: temp=노드3, 노드2→노드1로 변경, prev=노드2, curr=노드3'
      en: 'Iter 2: temp=Node3, Node2→Node1, prev=Node2, curr=Node3'
    - ko: '반복 계속... 마지막 반복: temp=None, 노드5→노드4로 변경, prev=노드5, curr=None'
      en: 'Continue... Final: temp=None, Node5→Node4, prev=Node5, curr=None'
    - ko: '루프 종료: curr=None이므로 반복 멈춤. prev(노드5)를 반환하면 리스트는 5→4→3→2→1→None'
      en: 'Exit: curr=None stops loop. Return prev (Node5). List is now 5→4→3→2→1→None'
    answer: '[5,4,3,2,1]'
solution:
  code: "# Definition for singly-linked list.\n# class ListNode:\n#     def __init__(self, x):\n#         self.val = x\n#         self.next = None\n\n\nclass Solution:\n    def reverseList(self, head: ListNode) -> ListNode:\n        prev, curr = None, head\n\n        while curr:\n            temp = curr.next\n            curr.next = prev\n            prev = curr\n            curr = temp\n        return prev\n"
  complexity:
    time: O(n)
    space: O(1)
  followup:
  - ko: 이 문제를 재귀적으로 구현할 수 있나요? 재귀 방식의 장단점은 무엇인가요?
    en: Can you implement this recursively? What are the pros and cons of the recursive approach?
  - ko: 처음 k개의 노드만 뒤집으려면 어떻게 하나요?
    en: How would you reverse only the first k nodes of the list?
  - ko: 리스트의 노드 쌍(1-2, 3-4, ...)을 교환하는 방식으로 확장할 수 있나요?
    en: Can you extend this to swap pairs of nodes (1-2, 3-4, ...) in the list?
```
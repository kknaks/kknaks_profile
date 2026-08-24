---
created: '2026-06-12'
date: '2026-06-12'
day: Day 37
difficulty: medium
id: A-037
source:
  curated_in:
  - neetcode150
  number: 143
  platform: leetcode
  slug: reorder-list
  url: https://leetcode.com/problems/reorder-list/
tags:
- linked-list
- two-pointers
- stack
- recursion
title:
  en: Reorder List
  ko: 연결 리스트 재배치
today: false
type: algorithm
updated: '2026-06-12'
visible: true
---

# 연결 리스트 재배치

## Data

```yaml
problem:
  title:
    ko: 연결 리스트 재배치
    en: Reorder List
  statement:
    ko: '싱글 연결 리스트의 헤드가 주어집니다. 리스트는 다음과 같이 표현됩니다:


      L₀ → L₁ → … → Lₙ₋₁ → Lₙ


      리스트를 다음 형태로 재배치합니다:


      L₀ → Lₙ → L₁ → Lₙ₋₁ → L₂ → Lₙ₋₂ → …


      리스트의 노드 값은 수정할 수 없습니다. 노드 자체만 변경할 수 있습니다.'
    en: 'You are given the head of a singly linked-list. The list can be represented as:


      L₀ → L₁ → … → Lₙ₋₁ → Lₙ


      Reorder the list to be on the following form:


      L₀ → Lₙ → L₁ → Lₙ₋₁ → L₂ → Lₙ₋₂ → …


      You may not modify the values in the list''s nodes. Only nodes themselves may be changed.'
  constraints:
  - 1 ≤ number of nodes ≤ 5 × 10⁴
  - 1 ≤ Node.val ≤ 1000
  io:
  - input: '[1,2,3,4]'
    output: '[1,4,2,3]'
  - input: '[1,2,3,4,5]'
    output: '[1,5,2,4,3]'
clarifying:
  items:
  - q:
      ko: 노드 포인터를 수정해도 되나요?
      en: Can we modify node pointers?
    type: good
    why:
      ko: 문제의 핵심은 노드 포인터를 재배치하는 것입니다. 값을 바꾸면 안 되지만, 포인터는 자유롭게 변경할 수 있습니다.
      en: The problem specifically allows pointer manipulation—only node values cannot be changed. Understanding this distinction is key to the solution.
  - q:
      ko: 리스트에 노드가 1개일 때는 어떻게 하나요?
      en: What if the list has only one node?
    type: good
    why:
      ko: 단일 노드는 이미 재배치된 상태입니다. 코드에서 경계 케이스로 자동 처리됩니다.
      en: A single node is already in the correct reordered form. The algorithm handles this naturally without special logic.
  - q:
      ko: 리스트가 홀수 길이일 때 중간 노드는 어떻게 되나요?
      en: When the list has odd length, where does the middle node end up?
    type: good
    why:
      ko: 홀수 길이 리스트에서 중간 노드는 그대로 유지됩니다. 예제 2([1,2,3,4,5] → [1,5,2,4,3])에서 3이 중간에 남습니다.
      en: The middle node remains in its position. In example 2, node 3 stays as the final node after reordering.
  - q:
      ko: 추가 자료구조(스택, 큐 등)를 사용해야 하나요?
      en: Do we need to use additional data structures like stacks or queues?
    type: good
    why:
      ko: 필수는 아닙니다. O(1) 공간으로 포인터만 사용하여 해결할 수 있습니다.
      en: Not required. The optimal solution uses only pointers, achieving O(1) space complexity.
  - q:
      ko: 리스트 중간을 어떻게 찾나요?
      en: How can we find the middle of the list?
    type: good
    why:
      ko: Slow와 Fast 포인터를 사용합니다. Fast는 2칸씩, Slow는 1칸씩 이동하여 Fast가 끝에 도달할 때 Slow가 중간을 가리킵니다.
      en: 'Use the two-pointer technique: fast pointer moves 2 steps while slow moves 1 step. When fast reaches the end, slow is at the middle.'
  - q:
      ko: 새로운 연결 리스트 노드를 생성해야 하나요?
      en: Should we create new ListNode objects?
    type: distractor
    why:
      ko: 아니요. 기존 노드들의 포인터만 재배치하면 됩니다. 새 노드 생성은 불필요합니다.
      en: No. We only rearrange pointers of existing nodes. Creating new nodes is unnecessary and wastes space.
  - q:
      ko: 해시맵을 사용하여 노드를 저장하는 것이 효율적인가요?
      en: Is using a hash map to store node values efficient?
    type: distractor
    why:
      ko: 아니요. 해시맵은 O(n) 추가 공간이 필요하고, 포인터 기반 방법이 더 효율적입니다.
      en: No. A hash map wastes O(n) extra space. The pointer-based approach is more efficient.
approach:
  items:
  - name:
      ko: 두 포인터 + 뒤집기 + 병합
      en: Two-pointer + Reverse + Merge
    complexity: O(n) time / O(1) space
    type: good
    why:
      ko: 중간을 찾고(O(n)), 두 번째 절반을 뒤집고(O(n)), 두 리스트를 병합합니다(O(n)). 추가 공간 없이 포인터만 사용합니다.
      en: Find the middle using two pointers (O(n)), reverse the second half (O(n)), then merge both halves (O(n)). Uses only O(1) space with pointer manipulation.
  - name:
      ko: 스택을 이용한 방법
      en: Stack-based approach
    complexity: O(n) time / O(n) space
    type: distractor
    why:
      ko: 모든 노드를 스택에 저장한 후 앞에서부터 pop하며 재배치합니다. 간단하지만 O(n) 공간이 필요합니다.
      en: Store all nodes in a stack, then pop from the back while interleaving. Simple but wastes O(n) space.
  - name:
      ko: 재귀를 이용한 방법
      en: Recursive approach
    complexity: O(n) time / O(n) space
    type: distractor
    why:
      ko: 재귀로 끝에 도달한 후 거슬러 올라오며 재배치합니다. 호출 스택 때문에 O(n) 공간이 필요합니다.
      en: Recursively reach the end, then backtrack and reorder. The call stack uses O(n) space.
  - name:
      ko: 새로운 리스트 생성
      en: Create new list with reordered values
    complexity: O(n) time / O(n) space
    type: distractor
    why:
      ko: 새로운 노드들을 생성하여 재배치합니다. 문제 조건(기존 노드 사용)에 맞지 않고 O(n) 공간이 낭비됩니다.
      en: Create new nodes with reordered values. Violates the constraint of using existing nodes and wastes O(n) space.
logic:
  format: slot
  slots:
  - label:
      ko: 포인터 초기화
      en: Initialize pointers
    indent: 0
    options:
    - code: slow, fast = head, head.next
      type: good
      why:
        ko: Slow는 1칸씩, Fast는 2칸씩 이동하기 위해 초기화합니다. Fast를 head.next에서 시작하면 fast가 None일 때 slow가 정확히 중간을 가리킵니다.
        en: Initialize slow at head and fast at head.next. This ensures that when fast reaches the end, slow points to the middle.
    - code: slow, fast = head, head
      type: distractor
      why:
        ko: Fast를 head에서 시작하면 fast와 slow가 같은 속도로 움직여서 중간을 찾을 수 없습니다.
        en: Starting fast at head means both pointers move at the same pace, so they never reach the middle.
    - code: slow, fast = head.next, head
      type: distractor
      why:
        ko: 포인터의 역할이 바뀌면 리스트의 첫 번째 절반을 잘못 찾게 됩니다.
        en: Reversing the roles of slow and fast breaks the middle-finding logic.
  - label:
      ko: 중간 찾기
      en: Find middle of list
    indent: 1
    options:
    - code: 'while fast and fast.next:'
      type: good
      why:
        ko: fast가 끝에 도달할 때까지 반복합니다. fast와 fast.next가 모두 존재해야 포인터 에러를 피할 수 있습니다.
        en: Continue until fast reaches the end. Check both fast and fast.next to avoid null pointer dereference.
    - code: 'while fast:'
      type: distractor
      why:
        ko: fast.next를 확인하지 않으면 fast.next.next에 접근할 때 에러가 발생합니다.
        en: Without checking fast.next, accessing fast.next.next will cause a null pointer error.
    - code: 'while fast and fast.next and fast.next.next:'
      type: distractor
      why:
        ko: 조건이 너무 많으면 중간을 정확히 찾지 못합니다. 실제로는 fast와 fast.next만 확인하면 충분합니다.
        en: Over-checking the condition prevents reaching the correct middle point.
  - label:
      ko: 리스트 분리
      en: Separate list halves
    indent: 0
    options:
    - code: second = slow.next
      type: good
      why:
        ko: 두 번째 절반의 시작을 저장합니다. slow.next는 두 번째 절반의 헤드입니다.
        en: Capture the head of the second half. slow.next points to the start of the second half.
    - code: second = slow
      type: distractor
      why:
        ko: slow를 두 번째로 사용하면 첫 번째 절반이 손상됩니다.
        en: Using slow as the second half destroys the first half structure.
    - code: second = slow.next.next
      type: distractor
      why:
        ko: 한 노드를 건너뛰므로 뒤집기가 완전하지 않습니다.
        en: Skipping a node prevents complete reversal of the second half.
  - label:
      ko: 중간에서 리스트 끊기
      en: Cut list at middle
    indent: 0
    options:
    - code: prev = slow.next = None
      type: good
      why:
        ko: slow.next를 None으로 설정하여 첫 번째 절반을 종료합니다. 동시에 prev를 초기화하여 뒤집기 준비를 합니다.
        en: Set slow.next = None to terminate the first half. Initialize prev for reversal of the second half.
    - code: prev = None
      type: distractor
      why:
        ko: slow.next = None을 생략하면 첫 번째 절반이 계속 두 번째 절반을 가리킵니다.
        en: Omitting slow.next = None leaves the first half pointing to the second half.
  - label:
      ko: 두 번째 절반 뒤집기
      en: Reverse second half
    indent: 1
    options:
    - code: 'while second:'
      type: good
      why:
        ko: 표준 단일 연결 리스트 뒤집기 알고리즘입니다. second가 None이 될 때까지 각 노드의 next 포인터를 반대로 향하게 합니다.
        en: Standard linked list reversal. Reverse the direction of next pointers for each node until second becomes None.
    - code: 'while second.next:'
      type: distractor
      why:
        ko: 마지막 노드가 뒤집기에서 제외됩니다.
        en: The last node is excluded from reversal.
  - label:
      ko: 두 절반 병합
      en: Merge two halves
    indent: 1
    options:
    - code: 'while second:'
      type: good
      why:
        ko: 첫 번째와 두 번째 절반의 포인터를 교대로 연결합니다. 이를 통해 L₀ → Lₙ → L₁ → Lₙ₋₁ → … 형태를 만듭니다.
        en: Interleave the two halves. Alternate connecting nodes from the first and second halves to create the desired reordered pattern.
    - code: 'while first:'
      type: distractor
      why:
        ko: 두 번째 절반의 끝이 None이 될 때까지 계속 진행해야 하므로 두 번째 절반의 길이를 확인해야 합니다.
        en: The second half is shorter, so checking only first will cause null pointer access.
    - code: first.next = second; first = second
      type: distractor
      why:
        ko: second.next를 업데이트하지 않으면 순서가 잘못됩니다. 두 절반을 교대로 연결해야 합니다.
        en: Not updating second.next breaks the interleaving pattern.
trace:
  code:
  - 'class Solution:'
  - '    def reorderList(self, head: ListNode) -> None:'
  - '        # find middle'
  - '        slow, fast = head, head.next'
  - '        while fast and fast.next:'
  - '            slow = slow.next'
  - '            fast = fast.next.next'
  - ''
  - '        # reverse second half'
  - '        second = slow.next'
  - '        prev = slow.next = None'
  - '        while second:'
  - '            tmp = second.next'
  - '            second.next = prev'
  - '            prev = second'
  - '            second = tmp'
  - ''
  - '        # merge two halfs'
  - '        first, second = head, prev'
  - '        while second:'
  - '            tmp1, tmp2 = first.next, second.next'
  - '            first.next = second'
  - '            second.next = tmp1'
  - '            first, second = tmp1, tmp2'
  cases:
  - input: '[1,2,3,4]'
    expected: '[1,4,2,3]'
  - input: '[1,2,3,4,5]'
    expected: '[1,5,2,4,3]'
  worked_example:
    input: '[1,2,3,4]'
    steps:
    - ko: '초기: slow=1, fast=2. 반복 후: slow=2, fast=4에서 멈춤. 중간은 노드 2.'
      en: 'Start: slow=1, fast=2. After loop: slow=2, fast=4. Middle is node 2.'
    - ko: '두 번째 절반 분리: second=3→4→None, first=1→2→None.'
      en: 'Separate: second half is 3→4→None. First half is 1→2→None.'
    - ko: '두 번째 절반 뒤집기: 4→3→None.'
      en: 'Reverse second half: 4→3→None.'
    - ko: '병합: 1→4→2→3→None. 출력: [1,4,2,3]'
      en: 'Merge: Connect 1→4→2→3→None. Output: [1,4,2,3]'
    answer: '[1,4,2,3]'
solution:
  code: "class Solution:\n    def reorderList(self, head: ListNode) -> None:\n        # find middle\n        slow, fast = head, head.next\n        while fast and fast.next:\n            slow = slow.next\n            fast = fast.next.next\n\n        # reverse second half\n        second = slow.next\n        prev = slow.next = None\n        while second:\n            tmp = second.next\n            second.next = prev\n            prev = second\n            second = tmp\n\n        # merge two halfs\n        first, second = head, prev\n        while second:\n            tmp1, tmp2 = first.next, second.next\n            first.next = second\n            second.next = tmp1\n            first, second = tmp1, tmp2\n"
  complexity:
    time: O(n)
    space: O(1)
  followup:
  - ko: 재귀를 사용하여 같은 문제를 풀 수 있을까요? 공간 복잡도는 얼마일까요?
    en: Can you solve this problem using recursion? What is the space complexity?
  - ko: 원본 리스트 순서를 유지하면서 재배치된 리스트를 별도로 생성해야 한다면?
    en: What if you need to create the reordered list while preserving the original list structure?
  - ko: 이중 연결 리스트(doubly linked list)라면 어떻게 달라질까요?
    en: How would the approach change if the list were doubly linked?
```
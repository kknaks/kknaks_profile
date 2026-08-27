---
created: '2026-06-16'
date: '2026-06-16'
day: Day 41
difficulty: easy
id: A-041
source:
  curated_in:
  - neetcode150
  number: 141
  platform: leetcode
  slug: linked-list-cycle
  url: https://leetcode.com/problems/linked-list-cycle/
tags:
- hash-table
- linked-list
- two-pointers
title:
  en: Linked List Cycle
  ko: 연결 리스트 순환 감지
today: false
type: algorithm
updated: '2026-06-16'
visible: true
---

# 연결 리스트 순환 감지

## Data

```yaml
problem:
  title:
    ko: 연결 리스트 순환 감지
    en: Linked List Cycle
  statement:
    ko: '연결 리스트의 헤드 노드가 주어졌을 때, 연결 리스트에 순환(사이클)이 있는지 판별하시오.


      연결 리스트에서 순환이란 리스트의 어떤 노드에서 시작하여 next 포인터를 따라 계속 이동할 때 다시 도달할 수 있는 노드가 존재하는 경우를 말합니다. 내부적으로 pos는 tail의 next 포인터가 연결된 노드의 인덱스를 나타냅니다. pos는 입력 매개변수로 주어지지 않음을 주의하시오.


      연결 리스트에 순환이 있으면 true를 반환하고, 그렇지 않으면 false를 반환하시오.'
    en: 'Given head, the head of a linked list, determine if the linked list has a cycle in it.


      There is a cycle in a linked list if there is some node in the list that can be reached again by continuously following the next pointer. Internally, pos is used to denote the index of the node that tail''s next pointer is connected to. Note that pos is not passed as a parameter.


      Return true if there is a cycle in the linked list. Otherwise, return false.'
  constraints:
  - 0 ≤ number of nodes ≤ 10^4
  - -10^5 ≤ node.val ≤ 10^5
  - pos is -1 or a valid index in the linked list
  io:
  - input: '[3,2,0,-4]

      1'
    output: 'true'
  - input: '[1,2]

      0'
    output: 'true'
  - input: '[1]

      -1'
    output: 'false'
clarifying:
  items:
  - q:
      ko: pos 매개변수는 함수 입력으로 주어지는가?
      en: Is the position parameter (pos) given as an input to the function?
    type: good
    why:
      ko: 문제에서 명시적으로 'pos는 매개변수로 전달되지 않음'이라고 했으므로, 우리는 노드 포인터 비교만으로 순환을 감지해야 한다.
      en: The problem explicitly states that pos is not passed as a parameter, so we must detect the cycle using only pointer comparisons.
  - q:
      ko: 공간 제약이 없다면 해시 테이블을 사용해도 되는가?
      en: If there is no space constraint, can we use a hash table or set to store visited nodes?
    type: good
    why:
      ko: 해시 테이블은 valid한 접근이지만, 팔로우업 질문에서 O(1) 공간을 사용하는 방법을 묻고 있으므로 two-pointer 접근이 더 우수하다.
      en: A hash table is a valid approach, but the follow-up asks for O(1) space, making two-pointer technique superior.
  - q:
      ko: 연결 리스트가 비어있을 수 있는가?
      en: Can the linked list be empty (head is null)?
    type: good
    why:
      ko: 제약 조건에서 노드 개수가 0 이상이므로, 빈 리스트의 경우를 처리해야 한다.
      en: The constraints state that the number of nodes can be 0, so empty list handling is required.
  - q:
      ko: 순환 고리에 진입하기 전에 여러 노드가 있을 수 있는가?
      en: Can there be multiple nodes before entering the cycle?
    type: good
    why:
      ko: 예제 1에서 처럼 순환은 리스트 중간에서 시작할 수 있으며, 이는 두 포인터 알고리즘의 핵심 테스트 케이스다.
      en: Example 1 shows the cycle can start in the middle of the list, which is a key test case for the two-pointer algorithm.
  - q:
      ko: 노드를 변경하거나 마킹할 수 있는가?
      en: Can we modify node values or mark visited nodes?
    type: distractor
    why:
      ko: 원래 데이터 구조를 수정하지 않는 것이 best practice이며, 이 문제는 원래 구조를 유지한 채 해결할 수 있다.
      en: Modifying the original data structure is not a best practice, and this problem can be solved without any modifications.
  - q:
      ko: 빠른 포인터가 느린 포인터를 따라잡으면 반드시 순환이 있다는 것이 증명되는가?
      en: Is it mathematically guaranteed that if the fast pointer catches the slow pointer, a cycle exists?
    type: good
    why:
      ko: 두 포인터가 만난다는 것은 무한 순환 구조가 존재한다는 것이고, 반대로 fast가 null에 도달하면 순환이 없다.
      en: The fast pointer can only catch the slow pointer if there's a cycle; reaching null guarantees no cycle.
approach:
  items:
  - name:
      ko: 두 포인터 (Floyd의 순환 감지 알고리즘)
      en: Two Pointers (Floyd's Cycle Detection)
    complexity: O(n) time / O(1) space
    type: good
    why:
      ko: 느린 포인터(1칸)와 빠른 포인터(2칸)를 사용하여 순환을 감지한다. O(1) 공간 제약을 만족하는 최적 솔루션이다.
      en: Uses slow pointer (1 step) and fast pointer (2 steps). Optimal solution meeting the O(1) space constraint.
  - name:
      ko: 해시 테이블 / 집합
      en: Hash Table / Set
    complexity: O(n) time / O(n) space
    type: good
    why:
      ko: 방문한 노드를 저장하고 중복 방문을 감지한다. 구현이 간단하지만 추가 메모리를 사용한다.
      en: Store visited nodes and detect revisits. Simple to implement but requires extra memory.
  - name:
      ko: 노드 변경 / 마킹
      en: Node Modification / Marking
    complexity: O(n) time / O(1) space
    type: distractor
    why:
      ko: 노드 값을 변경하거나 마킹하여 방문을 추적할 수 있지만, 원본 데이터 구조를 수정하므로 바람직하지 않다.
      en: Can mark visited nodes by modifying values, but altering the original data structure is not recommended.
  - name:
      ko: 순차 탐색 및 길이 비교
      en: Sequential Traversal with Length Comparison
    complexity: O(n²) time / O(1) space
    type: distractor
    why:
      ko: 두 번 순회하거나 중첩 루프를 사용하면 비효율적이고, 순환의 존재만 확인하면 되므로 불필요하다.
      en: Multiple traversals or nested loops are inefficient when we only need to detect existence of a cycle.
logic:
  format: slot
  slots:
  - label:
      ko: 포인터 초기화
      en: Initialize pointers
    indent: 0
    options:
    - code: slow, fast = head, head
      type: good
      why:
        ko: 두 포인터를 모두 헤드에서 시작하여 같은 위치에서 출발한다.
        en: Both pointers start at the head node, beginning their traversal from the same position.
    - code: slow, fast = head, head.next
      type: distractor
      why:
        ko: fast를 head.next에서 시작하면 짝수 길이 순환을 놓칠 수 있다.
        en: Starting fast at head.next may miss certain cycle patterns.
    - code: slow = head; fast = None
      type: distractor
      why:
        ko: fast를 None으로 초기화하면 루프가 즉시 종료되어 순환을 감지할 수 없다.
        en: Initializing fast as None will immediately terminate the loop.
  - label:
      ko: 반복 조건 검사
      en: Check loop condition
    indent: 0
    options:
    - code: 'while fast and fast.next:'
      type: good
      why:
        ko: fast와 fast.next 모두 존재하는지 확인하여 null 참조를 방지하고 리스트의 끝 도달을 감지한다.
        en: Checking both fast and fast.next prevents null reference errors and detects end of list.
    - code: 'while fast:'
      type: distractor
      why:
        ko: fast.next를 확인하지 않으면 fast.next.next 접근 시 NullPointerException 발생한다.
        en: Without checking fast.next, accessing fast.next.next will cause an error.
    - code: 'while fast and fast.next and slow:'
      type: distractor
      why:
        ko: slow는 항상 null이 아니므로 추가 조건은 불필요하고 코드를 복잡하게 만든다.
        en: slow will never be null in this algorithm, making this condition redundant.
  - label:
      ko: 느린 포인터 이동 (1칸)
      en: Move slow pointer (1 step)
    indent: 1
    options:
    - code: slow = slow.next
      type: good
      why:
        ko: 느린 포인터를 한 칸씩 이동하여 리스트를 천천히 순회한다.
        en: Move slow pointer one node at a time for steady traversal.
    - code: slow = slow.next.next
      type: distractor
      why:
        ko: 느린 포인터도 2칸 이동하면 두 포인터의 속도 차이가 없어져 순환 감지가 실패한다.
        en: Moving slow by 2 steps removes the speed difference needed for cycle detection.
    - code: slow = slow.next if slow else head
      type: distractor
      why:
        ko: 불필요한 조건부 처리로 로직이 복잡해지고, 이미 반복 조건에서 slow 유효성을 보장한다.
        en: Unnecessary conditional complicates logic; validity is already guaranteed by loop condition.
  - label:
      ko: 빠른 포인터 이동 (2칸)
      en: Move fast pointer (2 steps)
    indent: 1
    options:
    - code: fast = fast.next.next
      type: good
      why:
        ko: 빠른 포인터를 두 칸씩 이동하여 느린 포인터보다 빠르게 리스트를 순회한다.
        en: Move fast pointer two nodes at a time to traverse faster than slow pointer.
    - code: fast = fast.next
      type: distractor
      why:
        ko: 빠른 포인터가 1칸만 이동하면 느린 포인터와 같은 속도가 되어 알고리즘이 작동하지 않는다.
        en: Moving fast by 1 step makes it equal speed to slow, breaking the algorithm.
    - code: fast = fast.next.next.next
      type: distractor
      why:
        ko: 3칸 이동은 필요 이상으로 빠르며, 2칸이 최적의 속도 비율(2:1)을 제공한다.
        en: Moving by 3 steps is unnecessarily fast; 2 steps provides optimal 2:1 speed ratio.
  - label:
      ko: 포인터 충돌 확인
      en: Check if pointers meet
    indent: 1
    options:
    - code: 'if slow == fast:'
      type: good
      why:
        ko: 두 포인터가 같은 노드를 가리키면 순환이 존재한다는 의미이므로 true를 반환한다.
        en: If both pointers reference the same node, a cycle exists and we return true.
    - code: 'if slow.val == fast.val:'
      type: distractor
      why:
        ko: 노드 값이 같다고 해서 같은 노드는 아니며, 포인터(주소) 비교가 정확하다.
        en: Node values being equal doesn't mean they're the same node; pointer comparison is required.
    - code: 'if slow == fast and slow != head:'
      type: distractor
      why:
        ko: 순환은 헤드에서 시작할 수 있으므로(예제 2), head 위치에서의 만남도 순환이다.
        en: A cycle can start at the head (see Example 2), so meeting at head is also a cycle.
  - label:
      ko: 최종 결과 반환
      en: Return final result
    indent: 0
    options:
    - code: return False
      type: good
      why:
        ko: 루프가 정상 종료되었다면(fast가 null 도달), 순환이 없으므로 false를 반환한다.
        en: If the loop exits normally (fast reached null), no cycle was found, so return false.
    - code: return True
      type: distractor
      why:
        ko: 루프를 정상 종료한 경우는 순환이 없는 경우이므로 True를 반환하면 잘못된 결과다.
        en: Normal loop exit means no cycle, so returning True would be incorrect.
    - code: return slow == fast
      type: distractor
      why:
        ko: 루프 종료 후 slow == fast는 항상 false이므로 의미가 없다.
        en: After loop exits, slow == fast will always be false, making this redundant.
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
  - '    def hasCycle(self, head: ListNode) -> bool:'
  - '        slow, fast = head, head'
  - ''
  - '        while fast and fast.next:'
  - '            slow = slow.next'
  - '            fast = fast.next.next'
  - '            if slow == fast:'
  - '                return True'
  - '        return False'
  cases:
  - input: '[3,2,0,-4]

      1'
    expected: 'true'
  - input: '[1,2]

      0'
    expected: 'true'
  - input: '[1]

      -1'
    expected: 'false'
  worked_example:
    input: '[3,2,0,-4]

      1'
    steps:
    - ko: '초기 상태: slow와 fast 모두 헤드(값 3)를 가리킴'
      en: 'Initial: both slow and fast point to head (node with value 3)'
    - ko: '반복 1: slow는 노드 2로, fast는 노드 0으로 이동 (fast는 3→2→0)'
      en: 'Iteration 1: slow moves to node 2, fast moves to node 0 (fast: 3→2→0)'
    - ko: '반복 2: slow는 노드 0으로, fast는 노드 2로 이동 (fast는 0→-4→2)'
      en: 'Iteration 2: slow moves to node 0, fast moves to node 2 (fast: 0→-4→2)'
    - ko: '반복 3: slow는 노드 -4로, fast는 노드 0으로 이동 (fast는 2→0→-4→2 순환)'
      en: 'Iteration 3: slow moves to node -4, fast moves to node 0 (entering cycle)'
    - ko: 반복을 계속하면 느린 포인터가 순환을 따라가고 빠른 포인터는 더 빠르게 따라가다가 언젠가 만남 → true 반환
      en: Eventually the fast pointer laps the slow pointer in the cycle and they meet → return true
    answer: 'true'
solution:
  code: "# Definition for singly-linked list.\n# class ListNode:\n#     def __init__(self, x):\n#         self.val = x\n#         self.next = None\n\n\nclass Solution:\n    def hasCycle(self, head: ListNode) -> bool:\n        slow, fast = head, head\n\n        while fast and fast.next:\n            slow = slow.next\n            fast = fast.next.next\n            if slow == fast:\n                return True\n        return False\n"
  complexity:
    time: O(n)
    space: O(1)
  followup:
  - ko: 순환의 시작 노드를 찾으려면 어떻게 해야 하는가? (두 포인터가 만난 후 한 포인터를 헤드로 리셋하고 함께 이동하면 만나는 점이 순환의 시작)
    en: How would you find the node where the cycle begins? (Reset one pointer to head after they meet, move both together until they meet again)
  - ko: 순환의 길이를 구하려면 어떻게 해야 하는가? (두 포인터가 만난 후 한 포인터를 계속 이동시키며 몇 칸 이동했는지 센다)
    en: How would you find the length of the cycle? (After pointers meet, move one pointer and count steps until it returns)
  - ko: 해시 테이블 접근과 비교했을 때 두 포인터의 장단점은 무엇인가? (공간 효율성은 우수하지만, 수학적 증명이 필요하고 구현 시 포인터 이동에 주의해야 한다)
    en: What are the pros and cons of two-pointer vs hash table? (Better space complexity but requires mathematical proof; needs careful pointer movement)
```
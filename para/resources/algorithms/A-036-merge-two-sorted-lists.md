---
created: '2026-06-11'
date: '2026-06-11'
day: Day 36
difficulty: easy
id: A-036
source:
  curated_in:
  - neetcode150
  number: 21
  platform: leetcode
  slug: merge-two-sorted-lists
  url: https://leetcode.com/problems/merge-two-sorted-lists/
tags:
- linked-list
- recursion
title:
  en: Merge Two Sorted Lists
  ko: 정렬된 두 연결 리스트 병합
today: false
type: algorithm
updated: '2026-06-11'
visible: true
---

# 정렬된 두 연결 리스트 병합

## Data

```yaml
problem:
  title:
    ko: 정렬된 두 연결 리스트 병합
    en: Merge Two Sorted Lists
  statement:
    ko: '두 개의 정렬된 연결 리스트 list1과 list2의 헤드가 주어진다.


      두 리스트를 하나의 정렬된 리스트로 병합하라. 리스트는 두 리스트의 노드들을 함께 연결하여 만들어야 한다.


      병합된 연결 리스트의 헤드를 반환하라.'
    en: 'You are given the heads of two sorted linked lists list1 and list2.


      Merge the two lists into one sorted list. The list should be made by splicing together the nodes of the first two lists.


      Return the head of the merged linked list.'
  constraints:
  - 'Number of nodes in both lists: [0, 50]'
  - -100 ≤ Node.val ≤ 100
  - Both lists are sorted in non-decreasing order
  io:
  - input: '[1,2,4]

      [1,3,4]'
    output: '[1,1,2,3,4,4]'
  - input: '[]

      []'
    output: '[]'
  - input: '[]

      [0]'
    output: '[0]'
clarifying:
  items:
  - q:
      ko: 새 노드를 생성해야 하나요, 아니면 기존 노드들을 재배열하나요?
      en: Do we need to create new nodes or rearrange existing ones?
    type: good
    why:
      ko: 입력 노드들을 그대로 사용하고 포인터만 재연결할 수 있으므로 새 노드 생성은 낭비입니다.
      en: We can reuse existing nodes by rearranging pointers, which is more efficient.
  - q:
      ko: 두 리스트가 모두 비어있으면 뭘 반환해야 하나요?
      en: What should we return if both lists are empty?
    type: good
    why:
      ko: 이 경우 None을 반환하는 것이 올바릅니다. 알고리즘이 이를 자동으로 처리합니다.
      en: We return None, which the algorithm handles automatically through the dummy node.
  - q:
      ko: 리스트에 중복된 값이 있을 수 있나요?
      en: Can the lists contain duplicate values?
    type: good
    why:
      ko: 문제에서 "비내림차순"으로 정렬되어 있다고 했으므로 중복은 가능합니다.
      en: Yes, the constraint specifies non-decreasing order, which allows duplicates.
  - q:
      ko: 입력 리스트들이 반드시 정렬되어 있다고 보장할 수 있나요?
      en: Are the input lists guaranteed to be sorted?
    type: good
    why:
      ko: 네, 문제의 제약 조건에서 명시하고 있어 정렬된 리스트를 가정할 수 있습니다.
      en: Yes, this is stated in the constraints, so we can assume sorted input.
  - q:
      ko: 원본 리스트의 구조를 수정해도 괜찮나요?
      en: Can we modify the original lists?
    type: good
    why:
      ko: 네, 이 문제에서는 입력 리스트의 포인터를 변경해도 됩니다.
      en: Yes, we rearrange pointers of the input nodes to form a new linked list.
  - q:
      ko: 병합된 리스트를 한 번 더 정렬해야 하나요?
      en: Do we need to sort the merged list after combining?
    type: distractor
    why:
      ko: 입력 리스트들이 이미 정렬되어 있으므로 올바르게 병합하면 자동으로 정렬됩니다.
      en: No—since both inputs are already sorted, the merge naturally produces a sorted result.
  - q:
      ko: 병합 리스트를 위해 별도로 메모리를 할당해야 하나요?
      en: Should we allocate extra nodes for the merged list?
    type: distractor
    why:
      ko: 기존 노드들을 재사용하는 것이 효율적입니다. 새 노드는 필요하지 않습니다.
      en: No—we can reuse existing nodes to save space and time.
approach:
  items:
  - name:
      ko: 반복문을 이용한 병합 (더미 노드)
      en: Iterative merge with dummy node
    complexity: O(n + m) time / O(1) space
    type: good
    why:
      ko: 각 노드를 정확히 한 번씩 방문합니다. 더미 노드를 사용하여 엣지 케이스를 간단히 처리합니다.
      en: Each node visited exactly once. Dummy node simplifies edge cases without extra space.
  - name:
      ko: 재귀를 이용한 병합
      en: Recursive merge
    complexity: O(n + m) time / O(n + m) space
    type: good
    why:
      ko: 간결하고 직관적입니다. 호출 스택이 O(n+m) 공간을 사용합니다.
      en: Concise and intuitive, but uses O(n+m) space on the call stack.
  - name:
      ko: 배열로 변환 후 정렬
      en: Convert to array, sort, rebuild list
    complexity: O((n+m)log(n+m)) time / O(n+m) space
    type: distractor
    why:
      ko: 이미 정렬된 입력을 다시 정렬하므로 비효율적입니다.
      en: Inefficient because inputs are already sorted; unnecessary O(log) factor.
  - name:
      ko: 힙(우선순위 큐)을 이용한 병합
      en: Merge using a min-heap
    complexity: O((n+m)log(n+m)) time / O(n+m) space
    type: distractor
    why:
      ko: 여러 리스트를 병합할 때는 유용하지만, 두 개의 정렬된 리스트에는 불필요한 오버헤드입니다.
      en: Useful for k > 2 sorted lists, but overkill and slower for just two pre-sorted lists.
logic:
  format: slot
  slots:
  - label:
      ko: 더미 노드 초기화
      en: Initialize dummy node
    indent: 0
    options:
    - code: dummy = node = ListNode()
      type: good
      why:
        ko: 더미 노드는 첫 번째 요소를 특별히 처리할 필요 없이 병합 로직을 단순화합니다.
        en: Dummy node avoids special-casing the first node attachment.
    - code: dummy = ListNode(0)
      type: distractor
      why:
        ko: 더미에 값을 할당하면 안 됩니다. 더미는 단지 자리표일 뿐입니다.
        en: Dummy should have no value; it's just a placeholder.
    - code: node = None
      type: distractor
      why:
        ko: 노드를 None으로 시작하면 첫 번째 요소를 연결할 수 없습니다.
        en: Starting as None prevents attaching the first real node.
  - label:
      ko: 두 리스트 모두에 노드가 있는 동안 반복
      en: Loop while both lists have nodes
    indent: 0
    options:
    - code: 'while list1 and list2:'
      type: good
      why:
        ko: 한 리스트가 비면 루프를 탈출하여 남은 노드들을 처리합니다.
        en: Exit when either list is exhausted; remaining nodes are handled after.
    - code: 'while list1 or list2:'
      type: distractor
      why:
        ko: or 조건은 한쪽 리스트가 끝나도 계속 진행되어 null 오류가 발생합니다.
        en: Using 'or' continues after one list is empty, causing null errors.
    - code: 'while True:'
      type: distractor
      why:
        ko: 무한 루프가 됩니다. 리스트 소진 시 탈출 조건이 필요합니다.
        en: Infinite loop without a termination condition.
  - label:
      ko: 더 작은 값을 비교하고 연결
      en: Compare and attach the smaller value
    indent: 1
    options:
    - code: 'if list1.val < list2.val:'
      type: good
      why:
        ko: 더 작은 값의 노드를 현재 위치에 연결하고, 그 리스트의 포인터를 앞으로 이동합니다.
        en: Attach whichever node has the smaller value, then advance that list's pointer.
    - code: 'if list1.val <= list2.val:'
      type: distractor
      why:
        ko: <= 를 사용하면 값이 같을 때의 순서 선택이 달라질 수 있습니다.
        en: Using <= changes which list gets picked when values are equal.
    - code: 'if list1.val > list2.val:'
      type: distractor
      why:
        ko: 비교가 역순이면 더 큰 값을 선택하여 정렬 순서가 깨집니다.
        en: Reversed comparison selects the larger value, breaking sort order.
  - label:
      ko: 병합된 리스트 포인터 이동
      en: Advance the merged list pointer
    indent: 1
    options:
    - code: node = node.next
      type: good
      why:
        ko: 새로 연결된 노드로 포인터를 이동하여 다음 반복에서 올바른 위치에 연결할 수 있습니다.
        en: Move to the newly attached node so the next node attaches at the correct position.
    - code: dummy = dummy.next
      type: distractor
      why:
        ko: 더미를 이동하면 리스트의 헤드 참조를 잃어버립니다.
        en: Modifying dummy loses our reference to the list head.
    - code: node.next = node.next.next
      type: distractor
      why:
        ko: 노드를 건너뜁니다. 반복마다 정확히 하나의 노드만 연결합니다.
        en: This skips a node; we attach exactly one per iteration.
  - label:
      ko: 남은 노드들 연결
      en: Attach remaining nodes
    indent: 0
    options:
    - code: node.next = list1 or list2
      type: good
      why:
        ko: 한 리스트가 비면 다른 리스트의 남은 노드들을 모두 연결합니다. or 연산자는 null이 아닌 값을 반환합니다.
        en: After one list is exhausted, attach all remaining nodes from the other list.
    - code: return list1 or list2
      type: distractor
      why:
        ko: 반환하면 이미 병합된 노드들을 버립니다. node.next에 할당해야 합니다.
        en: This returns early and discards already-merged nodes.
    - code: node.next = list1 + list2
      type: distractor
      why:
        ko: 링크드 리스트는 + 연산자로 연결할 수 없습니다.
        en: Linked lists cannot be concatenated with +; must assign a node reference.
  - label:
      ko: 병합된 리스트의 헤드 반환
      en: Return the merged list head
    indent: 0
    options:
    - code: return dummy.next
      type: good
      why:
        ko: 더미 노드를 건너뛰고 실제 병합된 리스트의 첫 번째 노드를 반환합니다.
        en: Skip the dummy and return the head of the actual merged list.
    - code: return dummy
      type: distractor
      why:
        ko: 더미 노드를 헤드로 반환하면 결과에 불필요한 노드가 포함됩니다.
        en: Returns the dummy node, which shouldn't be part of the result.
    - code: return node
      type: distractor
      why:
        ko: 루프 후 node는 리스트의 끝을 가리킵니다. 헤드가 아닙니다.
        en: node points to the last node after the loop, not the head.
trace:
  code:
  - '# Definition for singly-linked list.'
  - '# class ListNode:'
  - '#     def __init__(self, val=0, next=None):'
  - '#         self.val = val'
  - '#         self.next = next'
  - ''
  - '# Iterative'
  - 'class Solution:'
  - '    def mergeTwoLists(self, list1: ListNode, list2: ListNode) -> ListNode:'
  - '        dummy = node = ListNode()'
  - ''
  - '        while list1 and list2:'
  - '            if list1.val < list2.val:'
  - '                node.next = list1'
  - '                list1 = list1.next'
  - '            else:'
  - '                node.next = list2'
  - '                list2 = list2.next'
  - '            node = node.next'
  - ''
  - '        node.next = list1 or list2'
  - ''
  - '        return dummy.next'
  - '    '
  - '# Recursive'
  - 'class Solution:'
  - '    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:'
  - '        if not list1:'
  - '            return list2'
  - '        if not list2:'
  - '            return list1'
  - '        lil, big = (list1, list2) if list1.val < list2.val else (list2, list1)'
  - '        lil.next = self.mergeTwoLists(lil.next, big)'
  - '        return lil'
  cases:
  - input: '[1,2,4]

      [1,3,4]'
    expected: '[1,1,2,3,4,4]'
  - input: '[]

      []'
    expected: '[]'
  - input: '[]

      [0]'
    expected: '[0]'
  worked_example:
    input: '[1,2,4]

      [1,3,4]'
    steps:
    - ko: 더미 노드 생성, node = dummy로 시작. list1=[1,2,4], list2=[1,3,4].
      en: 'Create dummy, set node = dummy. Start: list1=[1,2,4], list2=[1,3,4].'
    - ko: '반복: 1≥1(list2 선택), 1<3(list1 선택), 2<3, 4≥3를 차례로 비교하며 [1,1,2,3] 구성.'
      en: 'Iterations: compare 1 vs 1 (pick list2), 1 vs 3 (pick list1), 2 vs 3, 4 vs 3 → [1,1,2,3].'
    - ko: list2 소진. node.next = list1로 남은 [4,4]를 모두 연결.
      en: 'list2 exhausted. Attach remaining list1 [4]. Result: [1,1,2,3,4,4].'
    - ko: dummy.next 반환 → [1,1,2,3,4,4].
      en: Return dummy.next → [1,1,2,3,4,4].
    answer: '[1,1,2,3,4,4]'
solution:
  code: "# Definition for singly-linked list.\n# class ListNode:\n#     def __init__(self, val=0, next=None):\n#         self.val = val\n#         self.next = next\n\n# Iterative\nclass Solution:\n    def mergeTwoLists(self, list1: ListNode, list2: ListNode) -> ListNode:\n        dummy = node = ListNode()\n\n        while list1 and list2:\n            if list1.val < list2.val:\n                node.next = list1\n                list1 = list1.next\n            else:\n                node.next = list2\n                list2 = list2.next\n            node = node.next\n\n        node.next = list1 or list2\n\n        return dummy.next\n    \n# Recursive\nclass Solution:\n    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:\n        if not list1:\n            return list2\n        if not list2:\n            return list1\n        lil, big = (list1, list2) if list1.val < list2.val else (list2, list1)\n        lil.next = self.mergeTwoLists(lil.next,\
    \ big)\n        return lil\n"
  complexity:
    time: O(n + m)
    space: O(1)
  followup:
  - ko: 이 문제를 재귀로 풀 수 있을까요? 시간/공간 복잡도는 어떻게 되나요?
    en: Can you solve this recursively? What's the time/space complexity?
  - ko: k개의 정렬된 리스트를 병합해야 한다면 어떤 방식으로 접근하시겠어요?
    en: How would you approach merging k sorted linked lists?
  - ko: 만약 두 리스트가 정렬되지 않았다면 어떤 전략을 사용하시겠어요?
    en: What if the input lists were not guaranteed to be sorted?
```
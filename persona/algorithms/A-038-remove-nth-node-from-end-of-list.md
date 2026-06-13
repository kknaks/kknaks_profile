---
created: '2026-06-13'
date: '2026-06-13'
day: Day 38
difficulty: medium
id: A-038
source:
  curated_in:
  - neetcode150
  number: 19
  platform: leetcode
  slug: remove-nth-node-from-end-of-list
  url: https://leetcode.com/problems/remove-nth-node-from-end-of-list/
status: draft
tags:
- linked-list
- two-pointers
title:
  en: Remove Nth Node From End of List
  ko: 리스트 끝에서 N번째 노드 제거
today: true
type: algorithm
updated: '2026-06-13'
visible: true
---

# 리스트 끝에서 N번째 노드 제거

## Data

```yaml
problem:
  title:
    ko: 리스트 끝에서 N번째 노드 제거
    en: Remove Nth Node From End of List
  statement:
    ko: 링크드 리스트의 헤드가 주어졌을 때, 끝에서 n번째 노드를 제거하고 헤드를 반환하세요.
    en: Given the head of a linked list, remove the nth node from the end of the list and return its head.
  constraints:
  - 'The number of nodes in the list is sz: 1 ≤ sz ≤ 30'
  - 'Node values: 0 ≤ Node.val ≤ 100'
  - 'n is always valid: 1 ≤ n ≤ sz'
  io:
  - input: '[1,2,3,4,5]

      2'
    output: '[1,2,3,5]'
  - input: '[1]

      1'
    output: '[]'
  - input: '[1,2]

      1'
    output: '[1]'
clarifying:
  items:
  - q:
      ko: 링크드 리스트의 첫 번째 노드를 제거해야 하는 경우 어떻게 처리해야 하나요?
      en: What if we need to remove the first node in the list?
    type: good
    why:
      ko: 이것은 단순해 보이지만 실제로는 어려운 엣지 케이스입니다. 더미 노드를 사용하면 이 경우를 우아하게 처리할 수 있습니다.
      en: This seems simple but is a tricky edge case. Using a dummy node lets us handle it elegantly.
  - q:
      ko: 끝에서 n번째 노드는 1로 시작하나요 아니면 0으로 시작하나요?
      en: Is the nth node from end 1-indexed or 0-indexed?
    type: good
    why:
      ko: 코드에서 'while n > 0'으로 반복하므로 1-인덱싱 시스템을 사용합니다. 이를 이해하는 것이 중요합니다.
      en: The code uses 1-based indexing, as shown by 'while n > 0'. Understanding this is key.
  - q:
      ko: 두 포인터 사이의 거리는 얼마나 되어야 하나요?
      en: What distance should be maintained between the two pointers?
    type: good
    why:
      ko: 오른쪽 포인터를 먼저 n칸 전진시킴으로써 포인터들 사이에 정확히 n칸의 간격을 만듭니다. 이렇게 하면 왼쪽 포인터가 목표 노드 바로 앞에 도달합니다.
      en: By advancing right by n steps first, we create an n-node gap. This positions left just before the target.
  - q:
      ko: 링크된 리스트 구조를 직접 수정할 수 있나요?
      en: Can we directly modify the linked list structure?
    type: good
    why:
      ko: 예, 다음 포인터를 재할당하여 구조를 수정합니다. 이것이 공간 효율적인 이유입니다.
      en: Yes, we modify it by reassigning next pointers. This is why it's space-efficient.
  - q:
      ko: 입력 리스트가 항상 비어있지 않다고 가정할 수 있나요?
      en: Can we assume the input list is never empty?
    type: distractor
    why:
      ko: 제약 조건에서 1 ≤ sz이므로 리스트는 항상 최소 하나의 노드를 포함합니다.
      en: Per constraints 1 ≤ sz, the list always has at least one node.
  - q:
      ko: n이 리스트의 길이보다 클 수 있나요?
      en: Can n be greater than the list length?
    type: distractor
    why:
      ko: 아니요, 제약 조건에서 1 ≤ n ≤ sz입니다. n은 항상 유효합니다.
      en: No, per constraints 1 ≤ n ≤ sz. n is always valid.
  - q:
      ko: 더미 노드가 없으면 문제를 해결할 수 없나요?
      en: Is a dummy node absolutely necessary?
    type: good
    why:
      ko: 꼭 필요한 것은 아니지만, 더미 노드를 사용하면 첫 번째 노드 제거를 포함한 모든 경우를 균일하게 처리할 수 있어 코드가 훨씬 깔끔합니다.
      en: Not strictly necessary, but a dummy node makes handling the first node removal uniform with all other cases, simplifying the code significantly.
approach:
  items:
  - name:
      ko: 투 포인터 방법 (더미 노드 사용)
      en: Two-pointer approach (with dummy node)
    complexity: O(n) time / O(1) space
    type: good
    why:
      ko: 한 번의 패스로 목표 노드를 찾고 제거합니다. 더미 노드를 사용하면 첫 번째 노드 제거를 포함한 모든 엣지 케이스를 우아하게 처리합니다.
      en: Finds and removes the target in one pass. Dummy node elegantly handles all edge cases including first node removal.
  - name:
      ko: 2-패스 방법 (길이 먼저 계산)
      en: Two-pass approach (calculate length first)
    complexity: O(n) time / O(1) space
    type: distractor
    why:
      ko: 작동하지만 리스트를 두 번 순회해야 하고, 문제의 팔로우업에서 한 번의 패스를 요구합니다.
      en: Works but requires two list traversals. The follow-up specifically asks for a single-pass solution.
  - name:
      ko: 배열 저장 방법
      en: Array storage approach
    complexity: O(n) time / O(n) space
    type: distractor
    why:
      ko: 모든 노드를 배열에 저장하므로 불필요한 O(n) 추가 공간을 사용합니다.
      en: Stores all nodes in an array, using unnecessary O(n) extra space.
  - name:
      ko: 재귀 방법
      en: Recursive approach
    complexity: O(n) time / O(n) space
    type: distractor
    why:
      ko: 재귀 호출 스택으로 인해 O(n) 공간이 필요하므로 반복 솔루션보다 효율적이지 않습니다.
      en: Requires O(n) space for the recursion stack, less efficient than the iterative solution.
logic:
  format: slot
  slots:
  - label:
      ko: 더미 노드 생성
      en: Create dummy node
    indent: 0
    options:
    - code: dummy = ListNode(0, head)
      type: good
      why:
        ko: 더미 노드는 첫 번째 노드 제거를 포함한 모든 경우를 균일하게 처리할 수 있게 해줍니다.
        en: Dummy node allows uniform handling of all cases, including removal of the first node.
    - code: dummy = ListNode(0)
      type: distractor
      why:
        ko: 더미가 원본 리스트의 헤드와 연결되지 않아 리스트가 손실됩니다.
        en: Dummy doesn't link to the original list, losing the entire list.
    - code: dummy = head
      type: distractor
      why:
        ko: 새로운 더미 노드를 생성하지 않으므로 첫 번째 노드 제거를 처리할 수 없습니다.
        en: No new dummy node created, can't handle first node removal properly.
  - label:
      ko: 왼쪽 포인터 초기화
      en: Initialize left pointer
    indent: 0
    options:
    - code: left = dummy
      type: good
      why:
        ko: 왼쪽 포인터는 더미에서 시작하여, 두 포인터를 이동한 후 목표 노드 바로 앞에 위치하게 됩니다.
        en: Left starts at dummy so it will end up pointing just before the target node after the traversal.
    - code: left = head
      type: distractor
      why:
        ko: 헤드에서 시작하면 첫 번째 노드를 제거할 수 없습니다.
        en: Starting at head makes it impossible to remove the first node.
    - code: left = None
      type: distractor
      why:
        ko: None에서 포인터를 따라갈 수 없습니다.
        en: Can't traverse from None.
  - label:
      ko: 오른쪽 포인터 초기화
      en: Initialize right pointer
    indent: 0
    options:
    - code: right = head
      type: good
      why:
        ko: 오른쪽 포인터는 헤드에서 시작하여 왼쪽보다 n칸 앞서게 됩니다.
        en: Right starts at head to create an n-node gap ahead of left.
    - code: right = dummy
      type: distractor
      why:
        ko: 더미에서 시작하면 간격이 n+1이 되어 잘못된 노드를 제거합니다.
        en: Starting at dummy creates an n+1 gap, removing the wrong node.
    - code: right = head.next
      type: distractor
      why:
        ko: 한 칸 앞에서 시작하면 간격이 n-1이 되어 잘못된 노드를 제거합니다.
        en: Starting one node ahead creates an n-1 gap, removing the wrong node.
  - label:
      ko: 오른쪽 포인터를 n칸 전진
      en: Advance right pointer by n
    indent: 0
    options:
    - code: right = right.next
      type: good
      why:
        ko: 오른쪽 포인터를 n칸 전진시켜 왼쪽과 오른쪽 사이에 정확히 n칸의 간격을 만듭니다.
        en: Moving right by n steps creates the exact n-node gap between left and right.
    - code: right = right.next.next
      type: distractor
      why:
        ko: 매번 두 칸씩 이동하면 루프 반복 때마다 두 칸씩 움직여 잘못된 위치에 도달합니다.
        en: Moving two steps each iteration advances too far, reaching wrong position.
    - code: left = left.next
      type: distractor
      why:
        ko: 왼쪽을 이동하면 안 되고, 이 단계에서는 오른쪽 포인터만 이동해야 합니다.
        en: Should only move right at this stage, not left.
  - label:
      ko: 양쪽 포인터 함께 이동
      en: Move both pointers together
    indent: 0
    options:
    - code: left = left.next
      type: good
      why:
        ko: 두 포인터를 함께 이동시켜 오른쪽이 끝에 도달할 때 왼쪽이 정확히 목표 노드 앞에 위치하게 합니다.
        en: Moving both together ensures left reaches exactly the node before target when right reaches the end.
    - code: left = left.next.next
      type: distractor
      why:
        ko: 왼쪽을 두 칸씩 이동하면 목표 노드를 건너뜁니다.
        en: Moving left two steps skips the target node.
    - code: right = right.next
      type: distractor
      why:
        ko: 오른쪽만 이동하고 왼쪽을 이동하지 않으면 간격이 유지되지 않습니다.
        en: Moving only right without left breaks the gap maintenance.
  - label:
      ko: 목표 노드 제거
      en: Remove the target node
    indent: 0
    options:
    - code: left.next = left.next.next
      type: good
      why:
        ko: 목표 노드를 건너뛰어 이전 노드를 그 다음 다음 노드에 직접 연결합니다.
        en: Bypass the target node by directly connecting the previous node to the one after target.
    - code: left.next = left.next.next.next
      type: distractor
      why:
        ko: 두 개 노드를 건너뛰므로 의도한 노드 외에 추가 노드도 제거됩니다.
        en: Skips two nodes, removing more than intended.
    - code: left.next.next = None
      type: distractor
      why:
        ko: 리스트의 나머지 부분을 모두 자릅니다.
        en: Truncates the entire rest of the list.
  - label:
      ko: 헤드 반환
      en: Return the new head
    indent: 0
    options:
    - code: return dummy.next
      type: good
      why:
        ko: 더미의 다음 노드가 새로운 리스트의 헤드입니다. 원본 헤드를 반환하면 제거된 첫 번째 노드를 참조할 수 있습니다.
        en: dummy.next is the new head. Returning the original head might reference a removed first node.
    - code: return head
      type: distractor
      why:
        ko: 첫 번째 노드가 제거되었을 수 있으므로 잘못된 헤드를 반환할 수 있습니다.
        en: Head might be the removed node, returning an invalid reference.
    - code: return left
      type: distractor
      why:
        ko: 왼쪽은 목표 노드 앞에 있으므로 실제 리스트의 헤드가 아닙니다.
        en: Left points before the target, not the actual head of the list.
trace:
  code:
  - 'class Solution:'
  - '    def removeNthFromEnd(self, head: ListNode, n: int) -> ListNode:'
  - '        dummy = ListNode(0, head)'
  - '        left = dummy'
  - '        right = head'
  - ''
  - '        while n > 0:'
  - '            right = right.next'
  - '            n -= 1'
  - ''
  - '        while right:'
  - '            left = left.next'
  - '            right = right.next'
  - ''
  - '        # delete'
  - '        left.next = left.next.next'
  - '        return dummy.next'
  cases:
  - input: '[1,2,3,4,5]

      2'
    expected: '[1,2,3,5]'
  - input: '[1]

      1'
    expected: '[]'
  - input: '[1,2]

      1'
    expected: '[1]'
  worked_example:
    input: '[1,2,3,4,5]

      2'
    steps:
    - ko: '더미 노드 생성: dummy -> 1 -> 2 -> 3 -> 4 -> 5'
      en: 'Create dummy node: dummy -> 1 -> 2 -> 3 -> 4 -> 5'
    - ko: '포인터 초기화: left = dummy, right = 1'
      en: 'Initialize pointers: left = dummy, right = 1'
    - ko: '오른쪽을 2칸 전진: right = 3 (간격 = 2)'
      en: 'Advance right by 2: right = 3 (gap = 2)'
    - ko: '양쪽을 함께 이동: left = 3, right = None → 노드 4가 목표 노드'
      en: 'Move both pointers: left = 3, right = None → node 4 is target'
    - ko: '노드 4 제거: left.next = 5 → [1, 2, 3, 5]'
      en: 'Remove node 4: left.next = 5 → [1, 2, 3, 5]'
    answer: '[1,2,3,5]'
solution:
  code: "class Solution:\n    def removeNthFromEnd(self, head: ListNode, n: int) -> ListNode:\n        dummy = ListNode(0, head)\n        left = dummy\n        right = head\n\n        while n > 0:\n            right = right.next\n            n -= 1\n\n        while right:\n            left = left.next\n            right = right.next\n\n        # delete\n        left.next = left.next.next\n        return dummy.next\n"
  complexity:
    time: O(n)
    space: O(1)
  followup:
  - ko: 끝에서 k개의 노드를 한 번에 제거해야 한다면 어떻게 할까요?
    en: What if you need to remove k nodes from the end in a single operation?
  - ko: 더미 노드를 사용하지 않고도 이 문제를 해결할 수 있나요?
    en: Can you solve this without using a dummy node?
  - ko: 이중 연결 리스트(doubly-linked list)라면 어떻게 달라질까요?
    en: How would the solution change if it were a doubly-linked list?
```
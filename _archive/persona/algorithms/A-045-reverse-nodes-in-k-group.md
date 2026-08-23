---
created: '2026-06-20'
date: '2026-06-20'
day: Day 45
difficulty: hard
id: A-045
source:
  curated_in:
  - neetcode150
  number: 25
  platform: leetcode
  slug: reverse-nodes-in-k-group
  url: https://leetcode.com/problems/reverse-nodes-in-k-group/
status: draft
tags:
- linked-list
- recursion
title:
  en: Reverse Nodes in k-Group
  ko: k개 노드씩 연결 리스트 뒤집기
today: false
type: algorithm
updated: '2026-06-20'
visible: true
---

# k개 노드씩 연결 리스트 뒤집기

## Data

```yaml
problem:
  title:
    ko: k개 노드씩 연결 리스트 뒤집기
    en: Reverse Nodes in k-Group
  statement:
    ko: '연결 리스트의 head가 주어질 때, 리스트의 노드를 k개씩 묶어 역순으로 뒤집고 수정된 리스트를 반환하세요.


      k는 양의 정수이며 연결 리스트의 길이 이하입니다. 노드의 개수가 k의 배수가 아니면 끝에 남는 노드들은 그대로 유지해야 합니다.


      리스트의 노드 값은 변경할 수 없으며, 노드들의 연결 관계만 변경할 수 있습니다.'
    en: 'Given the head of a linked list, reverse the nodes of the list k at a time, and return the modified list.


      k is a positive integer and is less than or equal to the length of the linked list. If the number of nodes is not a multiple of k then left-out nodes, in the end, should remain as it is.


      You may not alter the values in the list''s nodes, only nodes themselves may be changed.'
  constraints:
  - The number of nodes in the list is n
  - 1 ≤ k ≤ n ≤ 5000
  - 0 ≤ Node.val ≤ 1000
  io:
  - input: '[1,2,3,4,5]

      2'
    output: '[2,1,4,3,5]'
  - input: '[1,2,3,4,5]

      3'
    output: '[3,2,1,4,5]'
clarifying:
  items:
  - q:
      ko: 끝에 k개 미만의 노드가 남으면 어떻게 하나요?
      en: What happens if fewer than k nodes remain at the end?
    type: good
    why:
      ko: 불완전한 마지막 그룹은 그대로 두어야 하므로, 이 조건이 반복을 언제 멈출지 결정합니다.
      en: Incomplete final groups must remain unchanged; this determines when to exit the reversal loop.
  - q:
      ko: 노드의 값을 수정할 수 있나요?
      en: Can we modify the node values?
    type: good
    why:
      ko: '문제에서 명시적으로 금지: 값 변경 불가, 포인터만 조작 가능합니다.'
      en: The problem explicitly forbids this; only pointer manipulation is allowed.
  - q:
      ko: 왜 더미(dummy) 노드를 사용하나요?
      en: Why do we use a dummy node?
    type: good
    why:
      ko: 더미는 첫 번째 그룹 반전을 다른 그룹과 동일하게 처리하므로, head 변경의 복잡도를 제거합니다.
      en: A dummy node handles the first group's reversal uniformly with other groups, avoiding special cases for head.
  - q:
      ko: 각 반복에서 k번째 노드를 찾는 것이 필수인가요?
      en: Why must we find the k-th node in every iteration?
    type: good
    why:
      ko: k번째 노드를 찾아야만 반전할 범위를 정의할 수 있고, 다음 그룹이 충분한지 확인할 수 있습니다.
      en: Locating the k-th node defines the reversal boundary and checks whether the next group has enough nodes.
  - q:
      ko: 전체 리스트를 먼저 뒤집은 후 조정하면 어떨까요?
      en: Why not reverse the entire list first and then re-arrange?
    type: distractor
    why:
      ko: 훨씬 비효율적이며, k-그룹 단위 조건을 충족시키지 못합니다.
      en: This defeats the purpose of k-group reversal and is far less efficient.
  - q:
      ko: 재귀로 이 문제를 풀 수 있을까요?
      en: Can we solve this recursively?
    type: good
    why:
      ko: '네, 각 k-그룹을 반전시킨 후 나머지를 재귀적으로 처리합니다 (기저: k개 미만의 노드).'
      en: 'Yes, by reversing each k-group and recursing on the remainder (base case: < k nodes).'
  - q:
      ko: 노드 값들을 새로운 노드에 복사하여 새 리스트를 만들어야 하나요?
      en: Should we copy node values into new nodes?
    type: distractor
    why:
      ko: 불필요합니다. 포인터 재배열만으로 충분하며, 이미 제약에서 금지됩니다.
      en: No—pointer rearrangement alone is sufficient and copying violates the constraint.
approach:
  items:
  - name:
      ko: '반복문: 그룹 경계를 추적하며 각 k-그룹 반전'
      en: 'Iterative: Track group boundaries and reverse each k-group in place'
    complexity: O(n) time / O(1) space
    type: good
    why:
      ko: 각 노드를 한 번만 방문하고 포인터만 변경하므로 최적입니다. O(1) 공간으로 follow-up 조건을 만족합니다.
      en: Each node visited once, pointers modified only. O(1) space satisfies the follow-up requirement.
  - name:
      ko: '재귀: k-그룹 반전 후 나머지 재귀 호출'
      en: 'Recursive: Reverse k-group then recurse on remainder'
    complexity: O(n) time / O(n) space (call stack)
    type: good
    why:
      ko: 구조가 명확하고 직관적이지만, 호출 스택이 O(n) 공간을 사용합니다.
      en: Clean structure but uses O(n) call stack space; not ideal for the follow-up.
  - name:
      ko: '스택 사용: 각 그룹을 스택에 저장 후 역순 팝(pop)'
      en: 'Stack-based: Push each group, pop to reverse order'
    complexity: O(n) time / O(k) space
    type: distractor
    why:
      ko: 작동하지만 추가 공간을 낭비하며, 포인터 조작 방식보다 복잡합니다.
      en: Works but wastes extra space and adds unnecessary complexity.
  - name:
      ko: '값 복사: 새 리스트에 복사 후 섹션별 반전'
      en: Copy values into new list then reverse sections
    complexity: O(n) time / O(n) space
    type: distractor
    why:
      ko: 문제의 핵심 제약 '값을 변경할 수 없다'를 위반하고, 불필요한 공간을 사용합니다.
      en: Violates the core constraint (don't alter values) and wastes space.
logic:
  format: slot
  slots:
  - label:
      ko: 더미 노드 생성 및 초기화
      en: Initialize dummy node
    indent: 0
    options:
    - code: dummy = ListNode(0, head)
      type: good
      why:
        ko: 더미 노드는 head를 가리키며, 첫 번째 그룹 반전도 동일한 로직으로 처리 가능하게 합니다.
        en: Dummy points to head and enables uniform handling of the first group reversal.
    - code: dummy = ListNode(head)
      type: distractor
      why:
        ko: 두 번째 인수 누락으로 더미가 head를 가리키지 않으므로 작동하지 않습니다.
        en: Missing the next pointer; dummy won't link to the list.
    - code: dummy = head
      type: distractor
      why:
        ko: 더미 없이는 head 변경 추적이 복잡해지고, 첫 그룹 반전 시 edge case 처리가 필요합니다.
        en: Without a dummy, modifying the head becomes error-prone and requires special handling.
  - label:
      ko: 현재 위치에서 k번째 노드 찾기
      en: Locate the k-th node from current position
    indent: 1
    options:
    - code: kth = self.getKth(groupPrev, k)
      type: good
      why:
        ko: groupPrev에서 k칸 앞으로 이동하여 현재 그룹의 끝을 식별합니다. 반전 범위를 결정합니다.
        en: Move k steps from groupPrev to identify the current group's boundary for reversal.
    - code: kth = self.getKth(groupPrev.next, k)
      type: distractor
      why:
        ko: groupPrev.next부터 세면 (k+1)번째 노드를 반환하므로 off-by-one 오류입니다.
        en: Starts from groupPrev.next; counts off-by-one, returning the (k+1)-th node.
    - code: kth = self.getKth(head, k)
      type: distractor
      why:
        ko: 항상 head부터 세면 현재 그룹의 경계를 못 찾으므로 반전이 무한 루프에 빠집니다.
        en: Always counting from head misses current group boundaries and causes infinite looping.
  - label:
      ko: k개 노드의 가용성 확인
      en: Check if k nodes exist in current group
    indent: 1
    options:
    - code: 'if not kth:'
      type: good
      why:
        ko: kth가 None이면 남은 노드가 k개 미만이므로 반전을 멈춥니다. 문제 요구사항을 만족합니다.
        en: If kth is None, fewer than k nodes remain; stop reversing per problem requirement.
    - code: 'if not kth.next:'
      type: distractor
      why:
        ko: k번째 노드의 다음을 확인하는 것은 off-by-one 오류로, 그룹 경계 판정이 틀립니다.
        en: Checks the node after k-th (off-by-one), misidentifying the group boundary.
    - code: 'if not groupPrev:'
      type: distractor
      why:
        ko: groupPrev는 절대 None이 될 수 없으므로 이 조건은 항상 거짓입니다.
        en: groupPrev never becomes None; this condition always evaluates to false.
  - label:
      ko: k개 노드의 포인터 방향 반전
      en: Reverse pointers within the k-group
    indent: 1
    options:
    - code: prev, curr = kth.next, groupPrev.next
      type: good
      why:
        ko: prev는 다음 그룹 시작으로, curr는 현재 그룹 첫 노드로 초기화한 후, 반복하며 포인터를 역전시킵니다.
        en: Initialize prev to next group's start and curr to current group's first node, then reverse pointers iteratively.
    - code: prev, curr = groupPrev.next, kth.next
      type: distractor
      why:
        ko: 초기화 순서 바꾸면 반전 방향이 역으로 되어 다음 그룹이 현재 그룹으로 링크됩니다.
        en: Swapping initialization reverses the intended direction, breaking group linkage.
    - code: prev, curr = None, groupPrev.next
      type: distractor
      why:
        ko: prev를 None으로 하면 반전 후 그룹의 끝이 다음 그룹과 단절되어 연결이 끊어집니다.
        en: Starting prev as None breaks the link from the reversed group to the next group.
  - label:
      ko: 반전된 그룹을 리스트에 재연결
      en: Reconnect reversed group to the list
    indent: 1
    options:
    - code: tmp = groupPrev.next
      type: good
      why:
        ko: 이전 그룹을 반전된 그룹의 새로운 head(kth)에 연결하고, groupPrev를 다음 반전 준비를 위해 갱신합니다.
        en: Link the previous group to the reversed group's new head, then update groupPrev for the next iteration.
    - code: groupPrev.next = groupNext
      type: distractor
      why:
        ko: groupNext는 다음 그룹의 시작이지, 반전된 그룹의 새로운 head가 아니므로 연결이 틀립니다.
        en: groupNext points to the next group, not the reversed group's new head; connection is wrong.
    - code: groupPrev = kth
      type: distractor
      why:
        ko: groupPrev를 kth로만 업데이트하면 반전 그룹의 첫 노드 참조(tmp)가 손실되어 다음 연결이 불가능합니다.
        en: Updating groupPrev to kth loses the reference to the reversed group's first node, breaking next linkage.
trace:
  code:
  - 'class Solution:'
  - '    def reverseKGroup(self, head: ListNode, k: int) -> ListNode:'
  - '        dummy = ListNode(0, head)'
  - '        groupPrev = dummy'
  - ''
  - '        while True:'
  - '            kth = self.getKth(groupPrev, k)'
  - '            if not kth:'
  - '                break'
  - '            groupNext = kth.next'
  - ''
  - '            # reverse group'
  - '            prev, curr = kth.next, groupPrev.next'
  - '            while curr != groupNext:'
  - '                tmp = curr.next'
  - '                curr.next = prev'
  - '                prev = curr'
  - '                curr = tmp'
  - ''
  - '            tmp = groupPrev.next'
  - '            groupPrev.next = kth'
  - '            groupPrev = tmp'
  - '        return dummy.next'
  - ''
  - '    def getKth(self, curr, k):'
  - '        while curr and k > 0:'
  - '            curr = curr.next'
  - '            k -= 1'
  - '        return curr'
  cases:
  - input: '[1,2,3,4,5]

      2'
    expected: '[2,1,4,3,5]'
  - input: '[1,2,3,4,5]

      3'
    expected: '[3,2,1,4,5]'
  worked_example:
    input: '[1,2,3,4,5]

      2'
    steps:
    - ko: '더미 노드 생성 및 초기화: dummy → 1 → 2 → 3 → 4 → 5 → None'
      en: 'Create dummy pointing to 1; initialize groupPrev = dummy. List: dummy → 1 → 2 → 3 → 4 → 5'
    - ko: '반복 1: getKth(dummy, 2)는 노드 2 반환. [1, 2]를 반전하면 dummy → 2 → 1 → 3 → 4 → 5 → None. groupPrev = 1'
      en: 'Iteration 1: Find node 2; reverse [1,2] → [2,1]. List: dummy → 2 → 1 → 3 → 4 → 5. Update groupPrev = 1'
    - ko: '반복 2: getKth(1, 2)는 노드 4 반환. [3, 4]를 반전하면 dummy → 2 → 1 → 4 → 3 → 5 → None. groupPrev = 3'
      en: 'Iteration 2: Find node 4; reverse [3,4] → [4,3]. List: dummy → 2 → 1 → 4 → 3 → 5. Update groupPrev = 3'
    - ko: '반복 3: getKth(3, 2)는 None 반환 (노드 5만 남음, k=2 미만). 반복 종료. dummy.next 반환'
      en: 'Iteration 3: Only node 5 left (<k=2); getKth returns None. Exit loop. Return dummy.next'
    answer: '[2,1,4,3,5]'
solution:
  code: "class Solution:\n    def reverseKGroup(self, head: ListNode, k: int) -> ListNode:\n        dummy = ListNode(0, head)\n        groupPrev = dummy\n\n        while True:\n            kth = self.getKth(groupPrev, k)\n            if not kth:\n                break\n            groupNext = kth.next\n\n            # reverse group\n            prev, curr = kth.next, groupPrev.next\n            while curr != groupNext:\n                tmp = curr.next\n                curr.next = prev\n                prev = curr\n                curr = tmp\n\n            tmp = groupPrev.next\n            groupPrev.next = kth\n            groupPrev = tmp\n        return dummy.next\n\n    def getKth(self, curr, k):\n        while curr and k > 0:\n            curr = curr.next\n            k -= 1\n        return curr\n"
  complexity:
    time: O(n)
    space: O(1)
  followup:
  - ko: 재귀 방식으로 풀 수 있을까요? 시간과 공간 복잡도는?
    en: How would you solve this recursively? What about time and space complexity?
  - ko: k가 리스트 길이보다 크면 어떻게 되나요?
    en: What if k exceeds the list length?
  - ko: 양방향 연결 리스트(doubly linked list)에도 이 알고리즘을 적용할 수 있나요?
    en: Can this algorithm be adapted for doubly linked lists?
```
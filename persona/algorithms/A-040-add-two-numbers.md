---
created: '2026-06-15'
date: '2026-06-15'
day: Day 40
difficulty: medium
id: A-040
source:
  curated_in:
  - neetcode150
  number: 2
  platform: leetcode
  slug: add-two-numbers
  url: https://leetcode.com/problems/add-two-numbers/
status: draft
tags:
- linked-list
- math
- recursion
title:
  en: Add Two Numbers
  ko: 두 숫자 더하기
today: true
type: algorithm
updated: '2026-06-15'
visible: true
---

# 두 숫자 더하기

## Data

```yaml
problem:
  title:
    ko: 두 숫자 더하기
    en: Add Two Numbers
  statement:
    ko: '두 개의 비어있지 않은 연결 리스트가 주어졌습니다. 각각은 음이 아닌 정수를 나타냅니다. 숫자의 자릿수는 역순으로 저장되며, 각 노드는 한 자리 숫자를 포함합니다. 두 수를 더하고 합을 연결 리스트로 반환하세요.


      두 수는 숫자 0을 제외하고 앞에 0이 없다고 가정할 수 있습니다.'
    en: 'You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.


      You may assume the two numbers do not contain any leading zero, except the number 0 itself.'
  constraints:
  - 1 ≤ number of nodes in each list ≤ 100
  - 0 ≤ Node.val ≤ 9
  - No leading zeros except for the number 0 itself
  io:
  - input: '[2,4,3]

      [5,6,4]'
    output: '[7,0,8]'
  - input: '[0]

      [0]'
    output: '[0]'
  - input: '[9,9,9,9,9,9,9]

      [9,9,9,9]'
    output: '[8,9,9,9,0,0,0,1]'
clarifying:
  items:
  - q:
      ko: 두 리스트의 길이가 다를 수 있나요?
      en: Can the two lists have different lengths?
    type: good
    why:
      ko: 길이가 다른 경우를 처리하는 방식이 해결책의 핵심입니다. 짧은 리스트의 끝에 도달하면 0을 사용해야 합니다.
      en: Handling different lengths is a key part of the solution—when one list is exhausted, treat missing digits as 0.
  - q:
      ko: '마지막 덧셈에서 자리올림이 발생하면 어떻게 하나요? (예: 999 + 1)'
      en: What happens if the final addition produces a carry? (e.g., 999 + 1 = 1000)
    type: good
    why:
      ko: 마지막 자리올림은 새로운 노드를 생성해야 하므로 반복 조건에 carry를 포함시켜야 합니다.
      en: The final carry creates a new digit, so the loop must continue while carry ≠ 0 even if both lists are exhausted.
  - q:
      ko: 입력 리스트를 수정해도 괜찮나요?
      en: Can we modify the input lists?
    type: good
    why:
      ko: 일반적으로 부작용을 피하기 위해 입력을 수정하지 않는 것이 좋습니다. 이 솔루션은 입력을 변경하지 않으므로 더 안전합니다.
      en: Best practice is to avoid modifying inputs to prevent side effects. This solution only advances pointers without altering node values.
  - q:
      ko: 한 노드의 값이 9보다 크면 어떻게 하나요? 예를 들어, 12가 들어올 수 있나요?
      en: Can a node's value exceed 9? Could we have a node with value 12?
    type: good
    why:
      ko: 문제의 제약 조건에서 각 노드의 값은 0 이상 9 이하입니다. 12는 불가능하지만, 두 수를 더한 결과(최대 19)를 다루기 위해 carry를 추출해야 합니다.
      en: The constraints guarantee 0 ≤ Node.val ≤ 9, so input nodes never exceed 9. However, their sum can reach 19 (9+9+1 carry), so we must extract the carry.
  - q:
      ko: 결과에서 더미 노드를 반환하면 안 되나요?
      en: Why do we return dummy.next instead of dummy itself?
    type: good
    why:
      ko: 더미 노드는 값이 없는 헬퍼 노드입니다. 실제 합계의 첫 자리는 dummy.next에 저장됩니다.
      en: The dummy node is a sentinel—it contains no meaningful data. The actual result list starts at dummy.next.
  - q:
      ko: 두 리스트를 먼저 역순으로 뒤집은 다음 더하면 더 효율적일까요?
      en: Would it be more efficient to reverse both lists, add them, then reverse the result?
    type: distractor
    why:
      ko: 불필요한 추가 작업입니다. 리스트가 이미 역순이므로 (LSB 먼저) 그대로 사용하는 것이 더 효율적입니다.
      en: Unnecessary work. The digits are already in reverse order (least significant digit first), so we can add directly without reversing.
  - q:
      ko: 음수도 처리해야 하나요?
      en: Do we need to handle negative numbers?
    type: distractor
    why:
      ko: 문제에서 음이 아닌 정수만 다룬다고 명시되어 있습니다. 음수는 고려할 필요가 없습니다.
      en: The problem explicitly states non-negative integers only, so negative handling is not required.
  - q:
      ko: 결과 리스트의 맨 앞에 더미 노드가 남아있지 않나요?
      en: Doesn't the dummy node stay at the front of the result?
    type: distractor
    why:
      ko: 아니요. dummy.next를 반환하므로 더미 노드는 제외됩니다. 실제 합계의 첫 자리가 반환됩니다.
      en: No, we return dummy.next, which skips the dummy node entirely. The caller gets the actual result starting with the first digit.
approach:
  items:
  - name:
      ko: 반복문 + 더미 노드
      en: Iterative with dummy node
    complexity: O(max(m,n)) time / O(max(m,n)) space
    type: good
    why:
      ko: 두 리스트를 동시에 순회하면서 각 자리를 더하고, 더미 노드는 리스트 생성을 단순화합니다. 공간은 출력 리스트 크기만큼 필요합니다.
      en: Traverse both lists simultaneously, adding digits and tracking carry. The dummy node eliminates special-casing the head. Space is proportional to the output list size.
  - name:
      ko: 재귀
      en: Recursive approach
    complexity: O(max(m,n)) time / O(max(m,n)) space
    type: good
    why:
      ko: 각 노드마다 재귀 호출을 수행하고 반환값으로 carry를 전달합니다. 더 함수형이지만 call stack 메모리를 사용합니다.
      en: Recursively process each node and return the new node with carry bundled in. More functional style but uses call stack space.
  - name:
      ko: 변환 → 더하기 → 역변환
      en: Convert to integers, add, convert back
    complexity: O(max(m,n)) time / O(max(m,n)) space
    type: distractor
    why:
      ko: 리스트를 정수로 변환하고 덧셈 후 다시 리스트로 변환합니다. 매우 긴 숫자의 경우 정수 오버플로우 위험이 있고, 불필요한 변환 과정이 추가됩니다.
      en: Convert lists to integers, add them, convert result back. Risk of integer overflow for very large numbers, and unnecessary conversion overhead.
  - name:
      ko: 뒤집기 → 더하기 → 뒤집기
      en: Reverse, add, reverse result
    complexity: O(max(m,n)) time / O(max(m,n)) space
    type: distractor
    why:
      ko: 먼저 리스트를 뒤집고, 정상 순서로 더하고, 다시 뒤집습니다. 추가 작업으로 인해 비효율적이며, 이미 역순인 입력을 더 활용할 수 있습니다.
      en: Reverse both inputs, add in normal order, reverse result. Extra operations that don't leverage the fact that inputs are already reversed.
  - name:
      ko: 스택 사용
      en: Using a stack
    complexity: O(max(m,n)) time / O(max(m,n)) space
    type: distractor
    why:
      ko: 각 리스트를 스택에 푸시하고 팝하면서 더합니다. 불필요한 복잡성을 추가하며 역순 입력의 이점을 무시합니다.
      en: Push both lists to stacks, then pop and add. Unnecessary complexity that ignores the reversed-order advantage.
logic:
  format: slot
  slots:
  - label:
      ko: 더미 노드 생성
      en: Create dummy node
    indent: 0
    options:
    - code: dummy = ListNode()
      type: good
      why:
        ko: 더미 노드를 사용하면 결과 리스트 구축 시 헤드를 특별히 처리할 필요가 없습니다.
        en: A dummy node eliminates special-casing for the head node when building the result.
    - code: cur = ListNode()
      type: distractor
      why:
        ko: cur은 순회 포인터입니다. dummy는 리스트의 시작점이어야 합니다.
        en: cur is the traversal pointer; we need dummy as a separate head node.
    - code: dummy = l1
      type: distractor
      why:
        ko: 입력 리스트를 다시 사용하면 입력이 변형되고 새 노드를 추가할 수 없습니다.
        en: Reusing l1 mutates the input and prevents proper node appending.
  - label:
      ko: 자리올림 초기화
      en: Initialize carry
    indent: 0
    options:
    - code: carry = 0
      type: good
      why:
        ko: 자리올림은 항상 0에서 시작합니다. 루프의 첫 반복에서 이전 자리올림이 없기 때문입니다.
        en: Carry starts at 0—there's no previous addition before the loop begins.
    - code: carry = 1
      type: distractor
      why:
        ko: 첫 덧셈에 자리올림을 추가하면 결과가 틀립니다.
        en: Starting with carry = 1 makes the first sum incorrect.
    - code: carry = l1.val + l2.val
      type: distractor
      why:
        ko: 자리올림은 단순히 0 또는 1입니다. 전체 합을 저장하면 안 됩니다.
        en: carry holds only 0 or 1, not the full sum.
  - label:
      ko: 반복 조건
      en: Loop while nodes or carry exist
    indent: 0
    options:
    - code: 'while l1 or l2 or carry:'
      type: good
      why:
        ko: 두 리스트의 길이가 다를 수 있으므로, 그리고 마지막 자리올림을 처리하기 위해 세 조건을 모두 확인해야 합니다.
        en: We must continue while either list has nodes (different lengths) or carry remains (e.g., 999 + 1 = 1000).
    - code: 'while l1 or l2:'
      type: distractor
      why:
        ko: 마지막 자리올림을 처리하지 못합니다. 999 + 1 = 1000에서 최종 1이 누락됩니다.
        en: 'Fails to handle final carry. Example: 999 + 1 = 1000 loses the leading 1.'
    - code: 'while l1 and l2:'
      type: distractor
      why:
        ko: 길이가 다른 리스트를 처리하지 못합니다. 한 리스트가 먼저 끝나면 루프가 종료됩니다.
        en: Breaks when lists have different lengths—loop stops as soon as one list is exhausted.
  - label:
      ko: 현재 자릿수 추출
      en: Extract node values
    indent: 1
    options:
    - code: v1 = l1.val if l1 else 0
      type: good
      why:
        ko: 리스트가 끝났으면 0을 사용하여 길이 차이를 처리합니다. 이렇게 하면 한 리스트가 다른 리스트보다 짧은 경우도 안전하게 처리됩니다.
        en: When a list is exhausted, use 0. This cleanly handles different-length lists without special logic.
    - code: v1 = l1.val if l1 else None
      type: distractor
      why:
        ko: None은 정수 덧셈에서 TypeError를 일으킵니다.
        en: None causes a TypeError when added to an integer.
    - code: v1 = l1.next.val if l1 else 0
      type: distractor
      why:
        ko: l1의 현재 값이 아닌 다음 노드의 값을 가져오므로 자리를 건너뜁니다.
        en: Accesses l1.next.val instead of l1.val, skipping the current digit.
  - label:
      ko: 합 계산
      en: Sum current digits and carry
    indent: 1
    options:
    - code: val = v1 + v2 + carry
      type: good
      why:
        ko: 이전 반복에서의 자리올림을 포함하여 현재 자릿수들을 모두 합산합니다. 이 합은 10 이상이 될 수 있습니다.
        en: Add both digits plus any carry from the previous step. The sum can be 0–19.
    - code: val = v1 + v2
      type: distractor
      why:
        ko: 이전 자리올림을 무시하면 결과가 완전히 잘못됩니다.
        en: Omitting carry produces completely incorrect results.
    - code: val = (v1 + v2) * carry
      type: distractor
      why:
        ko: 곱셈은 잘못된 연산입니다. 자리올림은 더해져야 합니다.
        en: Multiplication is wrong; carry must be added.
  - label:
      ko: 자리올림 추출
      en: Extract carry via integer division
    indent: 1
    options:
    - code: carry = val // 10
      type: good
      why:
        ko: '정수 나눗셈으로 십의 자리(자리올림)를 추출합니다. 예: 17 // 10 = 1'
        en: 'Integer division extracts the tens place (carry digit). Example: 17 // 10 = 1.'
    - code: carry = val % 10
      type: distractor
      why:
        ko: 나머지 연산은 일의 자리를 줍니다. 자리올림은 십의 자리입니다.
        en: Modulo gives the ones place; we need the tens place for carry.
    - code: carry = val / 10
      type: distractor
      why:
        ko: 부동소수점 나눗셈은 정수 자리올림을 주지 못합니다. 정수 나눗셈(//)을 사용해야 합니다.
        en: Float division doesn't give an integer carry; use // for integer division.
  - label:
      ko: 새 노드 생성 및 연결
      en: Create and append new node
    indent: 1
    options:
    - code: cur.next = ListNode(val)
      type: good
      why:
        ko: 현재 자리의 값을 가진 새 노드를 결과 리스트에 추가합니다. val은 이미 한 자리 숫자(0-9)입니다.
        en: Append a new node with the current digit (which is val % 10 from the previous line) to the result.
    - code: cur = ListNode(val)
      type: distractor
      why:
        ko: 기존 cur을 대체하면 연결 리스트가 끊어집니다. 대신 cur.next에 추가해야 합니다.
        en: Replacing cur breaks the chain; we need to append to cur.next.
    - code: cur.next = ListNode(val // 10)
      type: distractor
      why:
        ko: val은 이미 한 자리 숫자입니다(val % 10). 다시 나누면 0이 됩니다.
        en: val is already a single digit; dividing again gives 0.
trace:
  code:
  - '# Definition for singly-linked list.'
  - '# class ListNode:'
  - '#     def __init__(self, val=0, next=None):'
  - '#         self.val = val'
  - '#         self.next = next'
  - 'class Solution:'
  - '    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:'
  - '        dummy = ListNode()'
  - '        cur = dummy'
  - ''
  - '        carry = 0'
  - '        while l1 or l2 or carry:'
  - '            v1 = l1.val if l1 else 0'
  - '            v2 = l2.val if l2 else 0'
  - ''
  - '            # new digit'
  - '            val = v1 + v2 + carry'
  - '            carry = val // 10'
  - '            val = val % 10'
  - '            cur.next = ListNode(val)'
  - ''
  - '            # update ptrs'
  - '            cur = cur.next'
  - '            l1 = l1.next if l1 else None'
  - '            l2 = l2.next if l2 else None'
  - ''
  - '        return dummy.next'
  cases:
  - input: '[2,4,3]

      [5,6,4]'
    expected: '[7,0,8]'
  - input: '[0]

      [0]'
    expected: '[0]'
  - input: '[9,9,9,9,9,9,9]

      [9,9,9,9]'
    expected: '[8,9,9,9,0,0,0,1]'
  worked_example:
    input: '[2,4,3]

      [5,6,4]'
    steps:
    - ko: '초기화: dummy=[null], cur=dummy, carry=0'
      en: 'Init: dummy=[null], cur=dummy, carry=0'
    - ko: '반복 1: 2+5+0=7, carry=0, digit=7 → 새 노드(7)'
      en: 'Iter 1: 2+5+0=7, carry=0, digit=7 → append node(7)'
    - ko: '반복 2: 4+6+0=10, carry=1, digit=0 → 새 노드(0)'
      en: 'Iter 2: 4+6+0=10, carry=1, digit=0 → append node(0)'
    - ko: '반복 3: 3+4+1=8, carry=0, digit=8 → 새 노드(8), 루프 종료'
      en: 'Iter 3: 3+4+1=8, carry=0, digit=8 → append node(8), loop ends'
    answer: '[7,0,8]'
solution:
  code: "# Definition for singly-linked list.\n# class ListNode:\n#     def __init__(self, val=0, next=None):\n#         self.val = val\n#         self.next = next\nclass Solution:\n    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:\n        dummy = ListNode()\n        cur = dummy\n\n        carry = 0\n        while l1 or l2 or carry:\n            v1 = l1.val if l1 else 0\n            v2 = l2.val if l2 else 0\n\n            # new digit\n            val = v1 + v2 + carry\n            carry = val // 10\n            val = val % 10\n            cur.next = ListNode(val)\n\n            # update ptrs\n            cur = cur.next\n            l1 = l1.next if l1 else None\n            l2 = l2.next if l2 else None\n\n        return dummy.next\n"
  complexity:
    time: O(max(m, n))
    space: O(max(m, n))
  followup:
  - ko: 만약 숫자의 자릿수가 정상 순서(가장 중요한 자리부터)라면 어떻게 풀겠습니까?
    en: How would you solve this if the digits were in normal order (most significant digit first)?
  - ko: 이 문제를 재귀적으로 해결할 수 있을까요?
    en: Can you solve this problem recursively?
  - ko: 음수를 포함해야 한다면 어떻게 변경해야 할까요?
    en: How would you modify the solution to handle negative numbers?
```
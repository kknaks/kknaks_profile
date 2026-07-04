---
created: '2026-07-03'
date: '2026-07-03'
day: Day 57
difficulty: medium
id: A-057
source:
  curated_in:
  - neetcode150
  number: 230
  platform: leetcode
  slug: kth-smallest-element-in-a-bst
  url: https://leetcode.com/problems/kth-smallest-element-in-a-bst/
status: draft
tags:
- tree
- depth-first-search
- binary-search-tree
- binary-tree
title:
  en: Kth Smallest Element in a BST
  ko: 이진 검색 트리에서 k번째 작은 원소
today: false
type: algorithm
updated: '2026-07-03'
visible: true
---

# 이진 검색 트리에서 k번째 작은 원소

## Data

```yaml
problem:
  title:
    ko: 이진 검색 트리에서 k번째 작은 원소
    en: Kth Smallest Element in a BST
  statement:
    en: Given the root of a binary search tree, and an integer k, return the kth smallest value (1-indexed) of all the values of the nodes in the tree.
    ko: 이진 검색 트리의 루트와 정수 k가 주어질 때, 트리의 모든 노드 값 중에서 k번째로 작은 값(1-indexed)을 반환하세요.
  constraints:
  - 1 ≤ k ≤ n ≤ 10⁴
  - 0 ≤ Node.val ≤ 10⁴
  io:
  - input: '[3,1,4,null,2]

      1'
    output: '1'
  - input: '[5,3,6,2,4,null,null,1]

      3'
    output: '3'
clarifying:
  items:
  - q:
      ko: 이 문제에서 '1-indexed'는 무엇을 의미합니까?
      en: What does '1-indexed' mean in this problem?
    type: good
    why:
      ko: k=1일 때 가장 작은 값을 찾는 것을 의미합니다. 이를 이해해야 카운팅 로직을 올바르게 구현할 수 있습니다.
      en: When k=1, we're looking for the smallest value. Understanding this is crucial for implementing the counting logic correctly.
  - q:
      ko: BST에 중복된 값이 있을 수 있습니까?
      en: Can there be duplicate values in the BST?
    type: good
    why:
      ko: 문제의 제약에 명시적으로 유일성이 언급되지 않았으므로, 중복이 가능하며 각 노드는 별도로 계산됩니다.
      en: The problem constraints don't explicitly state uniqueness, so duplicates are possible and each node counts separately.
  - q:
      ko: 트리는 항상 유효한 BST입니까?
      en: Is the tree always a valid BST?
    type: good
    why:
      ko: 문제에서 암묵적으로 가정합니다. 이를 알면 BST의 성질(중위 순회 = 오름차순)을 활용할 수 있습니다.
      en: The problem assumes this implicitly. Knowing this lets us leverage the in-order traversal = ascending order property.
  - q:
      ko: 솔루션이 트리 구조를 수정해야 합니까?
      en: Does the solution need to modify the tree structure?
    type: good
    why:
      ko: 아니요, 우리는 k번째 값을 찾기만 하면 됩니다. 트리는 수정되지 않습니다.
      en: No, we only need to find the kth value. The tree structure remains unchanged.
  - q:
      ko: 우리는 k번째로 큰 원소를 찾아야 합니까?
      en: Should we find the kth largest element instead?
    type: distractor
    why:
      ko: 아니요, 문제는 명확히 '가장 작은 값'을 요구합니다. k번째 가장 큰 값을 찾으면 틀린 답을 얻습니다.
      en: No, the problem clearly asks for the kth smallest, not largest. Finding largest would give the wrong answer.
  - q:
      ko: 트리는 항상 완벽하게 균형잡혀 있습니까?
      en: Is the tree always perfectly balanced?
    type: distractor
    why:
      ko: 아니요, 트리는 불균형할 수 있습니다. 하지만 이 알고리즘은 여전히 O(h) 공간으로 작동합니다.
      en: No, trees can be unbalanced. But the algorithm still works efficiently with O(h) space complexity.
approach:
  items:
  - name:
      ko: 반복적 중위 순회
      en: Iterative in-order traversal
    complexity: O(k) ~ O(n) time / O(h) space
    type: good
    why:
      ko: 중위 순회는 오름차순으로 값을 방문합니다. 스택을 사용하여 반복적으로 수행하고 k번째 값에 도달할 때까지 탐색합니다.
      en: In-order traversal visits values in ascending order. Use a stack to traverse iteratively until reaching the kth element.
  - name:
      ko: 재귀적 중위 DFS
      en: Recursive in-order DFS
    complexity: O(k) ~ O(n) time / O(h) space
    type: good
    why:
      ko: 재귀 호출을 사용하여 중위 순회를 수행하고, 카운터를 감소시켜 k번째 원소를 찾습니다.
      en: Use recursive calls to perform in-order traversal, decrementing counter until finding the kth element.
  - name:
      ko: 모든 값을 수집하여 정렬
      en: Collect all values and sort
    complexity: O(n log n) time / O(n) space
    type: distractor
    why:
      ko: 모든 노드를 방문하고 전체를 정렬해야 하므로 시간이 더 걸립니다. BST의 성질을 활용하지 않습니다.
      en: Requires visiting all nodes and sorting everything, which is slower and wastes the BST property.
  - name:
      ko: 역순 중위 순회로 k번째 큰 값 찾기
      en: Reverse in-order traversal (find kth largest)
    complexity: O(n - k + 1) time / O(h) space
    type: distractor
    why:
      ko: 역순 순회는 가장 큰 값부터 방문하므로 k번째 가장 큰 값을 찾게 됩니다. 문제의 요구 사항과 다릅니다.
      en: Reverse traversal visits largest first, finding kth largest instead of kth smallest—solves the wrong problem.
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
        ko: 반복적 순회를 위해 노드를 저장할 빈 스택을 생성합니다.
        en: Create an empty stack to store nodes during iterative traversal.
    - code: stack = [root]
      type: distractor
      why:
        ko: 루트를 미리 포함하면 왼쪽 자식들을 탐색하기 전에 처리됩니다.
        en: Pre-including root processes it before exploring left children, breaking in-order sequence.
    - code: stack = {}
      type: distractor
      why:
        ko: 딕셔너리나 집합은 append 메서드가 없습니다.
        en: Dictionaries and sets don't have an append method for this use.
  - label:
      ko: 반복 조건 설정
      en: Main loop condition
    indent: 0
    options:
    - code: 'while stack or curr:'
      type: good
      why:
        ko: 스택에 요소가 있거나 현재 노드가 존재하는 동안 계속 반복합니다.
        en: Continue while stack has elements or current node exists.
    - code: 'while curr:'
      type: distractor
      why:
        ko: 현재 노드가 None이 되면 스택에 남은 노드들을 처리하지 못합니다.
        en: Stops when curr becomes None, missing nodes remaining in the stack.
    - code: 'while stack:'
      type: distractor
      why:
        ko: 스택만 확인하면 현재 노드의 오른쪽 서브트리를 탐색하지 못합니다.
        en: Only checking stack misses traversing the current node's right subtree.
  - label:
      ko: 왼쪽끝까지 탐색
      en: Traverse to leftmost node
    indent: 2
    options:
    - code: curr = curr.left
      type: good
      why:
        ko: 왼쪽 자식이 있을 때까지 계속 왼쪽으로 이동하면서 노드를 스택에 저장합니다. 이는 중위 순회의 첫 번째 부분입니다.
        en: Keep going left while nodes exist, pushing each to stack. This is the first phase of in-order traversal.
    - code: curr = curr.right
      type: distractor
      why:
        ko: 오른쪽으로 가면 중위 순회의 순서를 깨뜨립니다.
        en: Going right breaks the in-order sequence—we haven't processed left children yet.
    - code: 'while curr: k -= 1'
      type: distractor
      why:
        ko: 왼쪽 탐색 중에 카운트하면 올바른 순서로 세지 않게 됩니다.
        en: Counting during left traversal violates in-order sequence—process after popping only.
  - label:
      ko: 스택에서 노드 제거
      en: Pop node from stack
    indent: 1
    options:
    - code: curr = stack.pop()
      type: good
      why:
        ko: 스택의 최상단 노드를 꺼냅니다. 이 노드는 중위 순회에서 처리할 노드입니다.
        en: Pop the top of stack. This is the next node to process in in-order sequence.
    - code: curr = stack[0]
      type: distractor
      why:
        ko: 스택의 처음 요소에 접근하면 LIFO 원칙을 위반합니다.
        en: Accessing first element violates LIFO principle—should pop from the end.
    - code: stack.pop()
      type: distractor
      why:
        ko: 반환값을 할당하지 않으면 현재 노드를 알 수 없습니다.
        en: Not assigning the popped value loses the current node reference.
  - label:
      ko: k번째 원소 확인
      en: Check if kth element found
    indent: 2
    options:
    - code: 'if k == 0:'
      type: good
      why:
        ko: k를 1씩 감소시켜 몇 번 처리했는지 추적하고, k가 0이면 k번째 원소를 찾은 것입니다.
        en: After decrementing k, when it reaches 0 the current node is the kth smallest element.
    - code: 'if k == 1:'
      type: distractor
      why:
        ko: k를 1과 비교하면 (k-1)번째 원소를 반환하게 됩니다.
        en: Comparing with 1 returns the (k-1)th element, off by one.
    - code: 'if k < 0:'
      type: distractor
      why:
        ko: 음수 비교는 k번째 원소를 건너뜁니다.
        en: Negative comparison skips the kth element entirely.
  - label:
      ko: 오른쪽 부분트리 탐색
      en: Move to right subtree
    indent: 1
    options:
    - code: curr = curr.right
      type: good
      why:
        ko: 현재 노드를 처리한 후, 오른쪽 자식으로 이동하여 중위 순회를 계속합니다.
        en: After processing current node, move right to continue the in-order traversal.
    - code: curr = curr.left
      type: distractor
      why:
        ko: 왼쪽으로 가면 이미 처리한 부분을 다시 탐색합니다.
        en: Going left revisits the already-processed left subtree.
    - code: stack.append(curr.right)
      type: distractor
      why:
        ko: 오른쪽 자식은 스택에 넣지 않고 직접 curr에 할당하여 방문합니다.
        en: Right child should be visited directly via curr, not stacked.
trace:
  code:
  - '# Definition for a binary tree node.'
  - '# class TreeNode:'
  - '#     def __init__(self, x):'
  - '#         self.val = x'
  - '#         self.left = None'
  - '#         self.right = None'
  - ''
  - ''
  - 'class Solution:'
  - '    def kthSmallest(self, root: TreeNode, k: int) -> int:'
  - '        stack = []'
  - '        curr = root'
  - ''
  - '        while stack or curr:'
  - '            while curr:'
  - '                stack.append(curr)'
  - '                curr = curr.left'
  - '            curr = stack.pop()'
  - '            k -= 1'
  - '            if k == 0:'
  - '                return curr.val'
  - '            curr = curr.right'
  cases:
  - input: '[3,1,4,null,2]

      1'
    expected: '1'
  - input: '[5,3,6,2,4,null,null,1]

      3'
    expected: '3'
  worked_example:
    input: '[3,1,4,null,2]

      1'
    steps:
    - ko: '루트 3에서 시작하여 왼쪽으로 탐색: 3을 스택에 추가 후 왼쪽 자식 1로 이동'
      en: Start at root 3, push 3 to stack, move to left child 1
    - ko: '1을 스택에 추가: 1의 왼쪽은 없으므로 내부 반복문 탈출. 스택=[3,1]'
      en: Push 1 to stack, 1 has no left child, exit inner loop. Stack=[3,1]
    - ko: '스택에서 1을 꺼내고 k를 1 감소: k=0이므로 1이 1번째로 작은 값'
      en: Pop 1 from stack, decrement k to 0. Since k==0, element 1 is the 1st smallest
    - ko: 1을 반환
      en: Return 1
    answer: '1'
solution:
  code: "# Definition for a binary tree node.\n# class TreeNode:\n#     def __init__(self, x):\n#         self.val = x\n#         self.left = None\n#         self.right = None\n\n\nclass Solution:\n    def kthSmallest(self, root: TreeNode, k: int) -> int:\n        stack = []\n        curr = root\n\n        while stack or curr:\n            while curr:\n                stack.append(curr)\n                curr = curr.left\n            curr = stack.pop()\n            k -= 1\n            if k == 0:\n                return curr.val\n            curr = curr.right\n"
  complexity:
    time: O(k) ~ O(n)
    space: O(h)
  followup:
  - ko: 만약 이진 검색 트리가 자주 삽입/삭제되면서 k번째 가장 작은 원소를 자주 찾아야 한다면, 어떻게 최적화할 수 있을까요?
    en: If the BST is modified frequently with insertions/deletions and you need to find kth smallest often, how would you optimize?
  - ko: 이 문제를 재귀적으로 풀 수 있을까요? 공간 복잡도는 어떻게 될까요?
    en: Can you solve this recursively? What would be the space complexity?
  - ko: '만약 BST가 매우 불균형하다면(예: 연결 리스트처럼) 이 해결책은 여전히 효율적일까요?'
    en: If the BST is very unbalanced (like a linked list), would this solution still be efficient?
```
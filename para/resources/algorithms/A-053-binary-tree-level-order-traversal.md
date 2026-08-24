---
created: '2026-06-29'
date: '2026-06-29'
day: Day 53
difficulty: medium
id: A-053
source:
  curated_in:
  - neetcode150
  number: 102
  platform: leetcode
  slug: binary-tree-level-order-traversal
  url: https://leetcode.com/problems/binary-tree-level-order-traversal/
tags:
- tree
- breadth-first-search
- binary-tree
title:
  en: Binary Tree Level Order Traversal
  ko: 이진 트리 레벨 순서 순회
today: false
type: algorithm
updated: '2026-06-29'
visible: true
---

# 이진 트리 레벨 순서 순회

## Data

```yaml
problem:
  title:
    ko: 이진 트리 레벨 순서 순회
    en: Binary Tree Level Order Traversal
  statement:
    ko: 이진 트리의 루트가 주어질 때, 노드 값들의 레벨 순서 순회를 반환하세요. (즉, 왼쪽에서 오른쪽으로, 레벨별로)
    en: Given the root of a binary tree, return the level order traversal of its nodes' values. (i.e., from left to right, level by level).
  constraints:
  - 0 ≤ number of nodes ≤ 2000
  - -1000 ≤ Node.val ≤ 1000
  io:
  - input: '[3,9,20,null,null,15,7]'
    output: '[[3],[9,20],[15,7]]'
  - input: '[1]'
    output: '[[1]]'
  - input: '[]'
    output: '[]'
clarifying:
  items:
  - q:
      ko: '"레벨 순서 순회"는 정확히 무엇을 의미하나요?'
      en: What does "level order traversal" mean exactly?
    type: good
    why:
      ko: 트리를 위에서 아래로, 같은 레벨 내에서는 왼쪽에서 오른쪽으로 방문하는 너비 우선 탐색입니다.
      en: 'It means visiting nodes breadth-first: top-to-bottom, left-to-right within each level.'
  - q:
      ko: 같은 레벨 내의 노드들이 왼쪽에서 오른쪽 순서대로 정렬되어야 하나요?
      en: Should nodes within each level be ordered left-to-right?
    type: good
    why:
      ko: 예, 문제 설명의 "왼쪽에서 오른쪽으로"가 이를 명시합니다.
      en: Yes, the problem states 'from left to right, level by level.'
  - q:
      ko: 빈 트리의 경우 무엇을 반환해야 하나요?
      en: What should we return for an empty tree?
    type: good
    why:
      ko: '예제 3에서 보듯이 빈 배열을 반환합니다: []'
      en: Return an empty list [], as shown in Example 3.
  - q:
      ko: 노드의 값이 음수일 수 있나요?
      en: Can node values be negative?
    type: good
    why:
      ko: 제약조건에서 -1000 ≤ Node.val ≤ 1000 이므로 음수도 가능합니다.
      en: Yes, constraints allow -1000 ≤ Node.val ≤ 1000, including negative values.
  - q:
      ko: 결과를 단일 평탄화된 리스트로 반환해야 하나요?
      en: Should we return nodes in a single flattened list?
    type: distractor
    why:
      ko: '아니요, 각 레벨이 별도의 리스트로 그룹화되어야 합니다: [[3],[9,20],[15,7]]'
      en: 'No, each level must be grouped in its own list: [[3],[9,20],[15,7]], not a flat list.'
  - q:
      ko: 깊이 우선 탐색(DFS)이 더 나은 접근 방식일까요?
      en: Would depth-first search be a better approach?
    type: distractor
    why:
      ko: DFS는 깊이별 순서를 보장하지 않으므로 "레벨 순서"를 자연스럽게 구현하지 못합니다.
      en: DFS doesn't preserve level order; BFS (breadth-first) is the natural fit for level-order traversal.
approach:
  items:
  - name:
      ko: BFS with Deque
      en: BFS with Deque
    complexity: O(n) time / O(w) space
    type: good
    why:
      ko: 큐를 사용한 너비 우선 탐색이 레벨 순서를 자연스럽게 구현하며, deque의 popleft()는 O(1)입니다.
      en: Queue-based BFS naturally preserves level order; deque.popleft() is O(1) efficient.
  - name:
      ko: Recursive DFS with Level Tracking
      en: Recursive DFS with Level Tracking
    complexity: O(n) time / O(h) space
    type: distractor
    why:
      ko: 작동하지만 깊이별 순서가 되므로 "레벨 순서"를 위해 추가 로직이 필요합니다.
      en: Works but produces depth-order, not level-order; requires extra logic to track levels.
  - name:
      ko: BFS with List pop(0)
      en: BFS with List pop(0)
    complexity: O(n²) time / O(n) space
    type: distractor
    why:
      ko: list.pop(0)은 O(n) 시간이므로 전체 복잡도가 O(n²)가 되어 비효율적입니다.
      en: list.pop(0) is O(n) per call; overall complexity becomes O(n²), inefficient.
  - name:
      ko: Iterative DFS with Stack
      en: Iterative DFS with Stack
    complexity: O(n) time / O(h) space
    type: distractor
    why:
      ko: Stack은 LIFO이므로 레벨 순서를 보장하지 않으며, 결과를 정렬해야 합니다.
      en: Stack-based traversal is LIFO, doesn't preserve level order; would need post-processing.
logic:
  format: slot
  slots:
  - label:
      ko: 결과 리스트 초기화
      en: Initialize result list
    indent: 0
    options:
    - code: res = []
      type: good
      why:
        ko: 레벨별 순회 결과를 저장할 리스트입니다.
        en: List to store the level-order traversal results.
    - code: res = [[]]
      type: distractor
      why:
        ko: 첫 레벨을 이중 리스트로 추가하려 하면 구조 오류가 발생합니다.
        en: Starting with nested empty list causes append structure errors.
    - code: res = None
      type: distractor
      why:
        ko: None은 append 메서드를 가지지 않습니다.
        en: None has no append method.
  - label:
      ko: 큐 자료구조 초기화
      en: Initialize queue
    indent: 0
    options:
    - code: q = collections.deque()
      type: good
      why:
        ko: BFS는 FIFO 큐가 필수이며, deque의 popleft()는 O(1) 성능을 제공합니다.
        en: Queue (FIFO) is essential for BFS; deque.popleft() provides O(1) efficiency.
    - code: q = []
      type: distractor
      why:
        ko: list.pop(0)은 O(n) 시간 복잡도로 전체 성능이 O(n²)가 됩니다.
        en: list.pop(0) is O(n), making overall complexity O(n²).
    - code: q = Stack()
      type: distractor
      why:
        ko: Stack은 LIFO이므로 레벨 순서를 보장할 수 없습니다.
        en: Stack is LIFO, cannot guarantee level order.
  - label:
      ko: 루트 노드로 큐 초기화
      en: Seed queue with root
    indent: 0
    options:
    - code: q.append(root)
      type: good
      why:
        ko: 루트에서 BFS를 시작하며, 이전 조건(line 2)이 빈 트리를 처리합니다.
        en: Start BFS from root; previous if-check handles empty tree.
    - code: q.append(root.val)
      type: distractor
      why:
        ko: 값을 저장하면 나중에 node.left, node.right에 접근할 수 없습니다.
        en: Storing value prevents access to node.left and node.right.
    - code: res.append([root.val])
      type: distractor
      why:
        ko: 결과에 직접 저장하면 레벨별 처리 로직이 불필요해집니다.
        en: Appending to result bypasses level-by-level processing logic.
  - label:
      ko: 큐가 비지 않을 때까지 반복
      en: Process while queue has nodes
    indent: 0
    options:
    - code: 'while q:'
      type: good
      why:
        ko: 모든 노드를 처리할 때까지 반복하며, bool(deque)은 빈 경우 False입니다.
        en: Loop continues while nodes remain; bool(deque) is False when empty.
    - code: 'while q is not None:'
      type: distractor
      why:
        ko: 빈 deque도 None이 아니므로 무한 루프가 발생합니다.
        en: Empty deque is never None; causes infinite loop.
    - code: 'while len(q) > 0:'
      type: distractor
      why:
        ko: 기능상 동등하지만 파이썬 관례상 bool 변환을 권장합니다.
        en: Functionally equivalent but less Pythonic.
  - label:
      ko: 현재 레벨의 노드 개수만큼 반복
      en: Process exactly current level's nodes
    indent: 1
    options:
    - code: 'for i in range(len(q)):'
      type: good
      why:
        ko: len(q)를 고정하여 현재 레벨 노드만 처리하고, 루프 중 추가되는 자식들은 다음 레벨이 됩니다.
        en: Fix len(q) to process only current level; children added in loop become next level.
    - code: 'for node in q:'
      type: distractor
      why:
        ko: 루프 중 q에 추가되는 노드들도 포함되어 레벨이 섞입니다.
        en: Iterating over q directly includes newly-added next-level nodes.
    - code: 'for i in range(len(q) - 1):'
      type: distractor
      why:
        ko: 마지막 노드 하나가 건너뛰어져서 불완전한 레벨이 됩니다.
        en: Skips last node of current level (off-by-one error).
  - label:
      ko: 노드 추출 및 값 수집
      en: Dequeue and record node value
    indent: 2
    options:
    - code: node = q.popleft()
      type: good
      why:
        ko: popleft()로 앞에서 제거(FIFO)하고, 노드 객체로 이후 자식 노드에 접근합니다.
        en: popleft() removes from front (FIFO); returns node object for accessing children.
    - code: node = q.pop()
      type: distractor
      why:
        ko: pop()은 끝에서 제거(LIFO)하여 레벨 순서가 뒤바뀝니다.
        en: pop() removes from end (LIFO) → breaks level order.
    - code: node = q[0]
      type: distractor
      why:
        ko: 참조만 가져올 뿐 제거하지 않아 무한 루프가 발생합니다.
        en: Access without removal causes infinite loop.
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
  - '    def levelOrder(self, root: TreeNode) -> List[List[int]]:'
  - '        res = []'
  - '        q = collections.deque()'
  - '        if root:'
  - '            q.append(root)'
  - ''
  - '        while q:'
  - '            val = []'
  - ''
  - '            for i in range(len(q)):'
  - '                node = q.popleft()'
  - '                val.append(node.val)'
  - '                if node.left:'
  - '                    q.append(node.left)'
  - '                if node.right:'
  - '                    q.append(node.right)'
  - '            res.append(val)'
  - '        return res'
  cases:
  - input: '[3,9,20,null,null,15,7]'
    expected: '[[3],[9,20],[15,7]]'
  - input: '[1]'
    expected: '[[1]]'
  - input: '[]'
    expected: '[]'
  worked_example:
    input: '[3,9,20,null,null,15,7]'
    steps:
    - ko: res=[], q=[]로 시작; 루트 3 존재하므로 q=[3]
      en: Initialize res=[], q=[]; root exists so q=[3]
    - ko: '루프 1: 큐 크기=1, 노드 3 추출, val=[3], 자식 9,20 추가 → q=[9,20], res=[[3]]'
      en: 'Loop 1: dequeue 3, val=[3], enqueue children 9,20 → res=[[3]]'
    - ko: '루프 2: 큐 크기=2, 노드 9,20 추출, val=[9,20], 자식 15,7 추가 → q=[15,7], res=[[3],[9,20]]'
      en: 'Loop 2: dequeue 9,20, val=[9,20], enqueue children 15,7 → res=[[3],[9,20]]'
    - ko: '루프 3: 큐 크기=2, 노드 15,7 추출, val=[15,7], 자식 없음 → q=[], res=[[3],[9,20],[15,7]]'
      en: 'Loop 3: dequeue 15,7, val=[15,7], no children → res=[[3],[9,20],[15,7]]'
    - ko: 큐가 비었으므로 반복 종료, [[3],[9,20],[15,7]] 반환
      en: Queue empty, return [[3],[9,20],[15,7]]
    answer: '[[3],[9,20],[15,7]]'
solution:
  code: "# Definition for a binary tree node.\n# class TreeNode:\n#     def __init__(self, x):\n#         self.val = x\n#         self.left = None\n#         self.right = None\n\n\nclass Solution:\n    def levelOrder(self, root: TreeNode) -> List[List[int]]:\n        res = []\n        q = collections.deque()\n        if root:\n            q.append(root)\n\n        while q:\n            val = []\n\n            for i in range(len(q)):\n                node = q.popleft()\n                val.append(node.val)\n                if node.left:\n                    q.append(node.left)\n                if node.right:\n                    q.append(node.right)\n            res.append(val)\n        return res\n"
  complexity:
    time: O(n)
    space: O(w)
  followup:
  - ko: 트리의 높이가 매우 크지만 너비가 좁다면 어떤 접근을 추천하시겠습니까?
    en: If the tree has large height but small width, what approach would you recommend?
  - ko: 우측에서 좌측 순서로 각 레벨을 순회하려면 어떻게 수정하시겠습니까?
    en: How would you modify the solution to traverse each level right-to-left?
  - ko: 재귀적 DFS로도 레벨 순서 순회를 구현할 수 있을까요? 어떤 추가 정보가 필요한가요?
    en: Can you implement level-order traversal using recursive DFS? What extra information is needed?
```
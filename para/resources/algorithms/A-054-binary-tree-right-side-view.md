---
created: '2026-06-30'
date: '2026-06-30'
day: Day 54
difficulty: medium
id: A-054
source:
  curated_in:
  - neetcode150
  number: 199
  platform: leetcode
  slug: binary-tree-right-side-view
  url: https://leetcode.com/problems/binary-tree-right-side-view/
tags:
- tree
- depth-first-search
- breadth-first-search
- binary-tree
title:
  en: Binary Tree Right Side View
  ko: 이진 트리 우측 뷰
today: false
type: algorithm
updated: '2026-06-30'
visible: true
---

# 이진 트리 우측 뷰

## Data

```yaml
problem:
  title:
    ko: 이진 트리 우측 뷰
    en: Binary Tree Right Side View
  statement:
    ko: 이진 트리의 루트가 주어졌을 때, 트리의 우측에 서 있는 자신을 상상하고, 위에서 아래로 순서대로 볼 수 있는 노드의 값들을 반환하세요.
    en: Given the root of a binary tree, imagine yourself standing on the right side of it, return the values of the nodes you can see ordered from top to bottom.
  constraints:
  - The number of nodes in the tree is in the range [0, 100]
  - -100 ≤ Node.val ≤ 100
  io:
  - input: '[1,2,3,null,5,null,4]'
    output: '[1,3,4]'
  - input: '[1,2,3,4,null,null,null,5]'
    output: '[1,3,4,5]'
  - input: '[1,null,3]'
    output: '[1,3]'
  - input: '[]'
    output: '[]'
clarifying:
  items:
  - q:
      ko: 우측 뷰는 우측 자식이 없는 노드들을 의미하나요?
      en: Does right side view mean nodes without a right child?
    type: distractor
    why:
      ko: 우측 뷰는 각 레벨에서 가장 우측에 보이는 노드를 의미합니다.
      en: Right side view means the rightmost visible node at each level, not nodes lacking right children.
  - q:
      ko: BFS와 DFS 중 어느 것을 사용해야 하나요?
      en: Should we use BFS or DFS for this problem?
    type: good
    why:
      ko: BFS는 자연스럽게 레벨별로 처리하므로 각 레벨의 우측 노드를 찾기 쉽습니다. DFS도 가능하지만 레벨을 명시적으로 추적해야 합니다.
      en: BFS naturally processes level-by-level, making it intuitive to find the rightmost node at each level. DFS works too but requires explicit level tracking.
  - q:
      ko: 빈 트리일 경우 어떻게 처리하나요?
      en: What should we return for an empty tree?
    type: good
    why:
      ko: 빈 트리는 빈 리스트를 반환합니다. 큐가 처음부터 비어있어서 while 루프가 실행되지 않습니다.
      en: An empty tree returns an empty list. The queue starts empty, so the while loop never executes.
  - q:
      ko: 우측 서브트리만 탐색하면 되나요?
      en: Can we only traverse the right subtree of each node?
    type: distractor
    why:
      ko: 아니요, 좌측 서브트리에도 우측 뷰의 일부가 될 수 있는 노드가 있습니다. 모든 노드를 탐색해야 합니다.
      en: No, nodes in the left subtree can also be part of the right view. We must check all nodes.
  - q:
      ko: 현재 레벨의 노드 개수를 알아야 하는 이유는 무엇인가요?
      en: Why do we need to know the current level size?
    type: good
    why:
      ko: 큐에 자식 노드를 추가하기 전에 현재 레벨의 개수를 저장해야 다음 레벨과 분리할 수 있습니다.
      en: We need the size before adding children so we can process exactly the current level, separating it from the next level.
  - q:
      ko: 각 레벨에서 우측 노드를 어떻게 찾나요?
      en: How do we identify the rightmost node at each level?
    type: good
    why:
      ko: 현재 레벨의 모든 노드를 좌에서 우로 처리하면서 rightSide를 계속 업데이트합니다. 마지막 업데이트된 값이 우측 노드입니다.
      en: Process all nodes left-to-right at the current level, continuously updating rightSide. The last updated node is rightmost.
  - q:
      ko: null 노드도 큐에 추가하나요?
      en: Do we add null nodes to the queue?
    type: good
    why:
      ko: 네, null 자식도 추가하지만 if node 체크로 유효한 노드만 처리합니다. 이렇게 하면 구조를 보존합니다.
      en: Yes, we add null children but skip them with the 'if node' check. This preserves level structure naturally.
approach:
  items:
  - name:
      ko: BFS 레벨별 탐색
      en: BFS Level-by-Level Traversal
    complexity: O(n) time / O(w) space, where w is max width
    type: good
    why:
      ko: 각 레벨을 완전히 처리한 후 다음 레벨로 이동하므로, 각 레벨의 우측 노드를 쉽게 식별할 수 있습니다.
      en: Process each level completely before moving to the next, making it straightforward to identify the rightmost node at each level.
  - name:
      ko: DFS 우측 우선 탐색
      en: DFS Right-First Traversal
    complexity: O(n) time / O(h) space, where h is height
    type: good
    why:
      ko: 우측 자식을 먼저 방문하고 깊이를 추적하면, 각 깊이에서 처음 만난 노드가 우측 뷰입니다.
      en: Visit right child first and track depth; the first node encountered at each depth is part of the right view.
  - name:
      ko: 우측 서브트리만 탐색
      en: Right Subtree Only Traversal
    complexity: O(n) time / O(h) space
    type: distractor
    why:
      ko: 좌측 서브트리의 노드도 우측 뷰에 포함될 수 있으므로 이 접근법은 틀립니다.
      en: Left subtree nodes can also be part of the right view, making this approach incorrect.
  - name:
      ko: 해시맵으로 각 레벨의 우측값 저장
      en: HashMap per-Level Rightmost Storage
    complexity: O(n) time / O(h) space
    type: distractor
    why:
      ko: DFS로 모든 노드를 방문하면서 레벨별로 우측 노드를 저장합니다. 작동하지만 불필요하게 복잡합니다.
      en: DFS all nodes and store rightmost at each level in a map. Works but adds unnecessary complexity.
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
        ko: 최종 답을 저장할 리스트를 생성합니다.
        en: Create the list to store the final answer.
    - code: res = None
      type: distractor
      why:
        ko: None은 append 메서드가 없어 나중에 오류가 발생합니다.
        en: None has no append method, causing an error later.
    - code: res = {}
      type: distractor
      why:
        ko: 딕셔너리는 순서를 보장하지 않아 출력 순서가 잘못될 수 있습니다.
        en: Dictionary doesn't guarantee order, making output incorrect.
  - label:
      ko: 루트로 큐 초기화
      en: Initialize queue with root
    indent: 0
    options:
    - code: q = collections.deque([root])
      type: good
      why:
        ko: BFS는 루트에서 시작하며, deque는 양쪽 끝에서 O(1) 연산을 제공합니다.
        en: BFS starts from root, and deque provides O(1) operations on both ends.
    - code: q = [root]
      type: distractor
      why:
        ko: 리스트의 popleft는 O(n)이므로 deque보다 훨씬 느립니다.
        en: List popleft is O(n) whereas deque is O(1), making it much slower.
    - code: q = collections.deque()
      type: distractor
      why:
        ko: 루트를 추가하지 않으면 큐가 비어있어 탐색이 시작되지 않습니다.
        en: Without adding root, the queue is empty and traversal never starts.
  - label:
      ko: 각 레벨을 반복 처리
      en: While loop for each level
    indent: 0
    options:
    - code: 'while q:'
      type: good
      why:
        ko: 큐가 비워질 때까지 각 레벨을 처리하며, 큐의 boolean 상태로 조건을 확인합니다.
        en: Process each level until queue is empty, checking the boolean state of the queue.
    - code: 'if q:'
      type: distractor
      why:
        ko: 한 번만 실행되므로 한 레벨만 처리하고 나머지는 누락됩니다.
        en: Only executes once, processing just one level and missing the rest.
    - code: 'while len(q) > 1:'
      type: distractor
      why:
        ko: 마지막 레벨을 건너뛰므로 우측 뷰의 마지막 노드가 누락됩니다.
        en: Skips the final level, missing the last node in the right view.
  - label:
      ko: 현재 레벨 설정
      en: Setup current level
    indent: 1
    options:
    - code: qLen = len(q)
      type: good
      why:
        ko: 현재 레벨의 정확한 크기를 저장하고 rightSide를 리셋하여 다음 레벨과 분리합니다.
        en: Save the current level size and reset rightSide to separate this level from the next.
    - code: qLen = q.maxlen; rightSide = 0
      type: distractor
      why:
        ko: maxlen은 데큐의 최대 용량이며, 0은 노드가 아니므로 .val 접근에서 오류가 발생합니다.
        en: maxlen is deque capacity (not current length), and 0 is not a node, causing errors later.
    - code: qLen = len(q) - 1
      type: distractor
      why:
        ko: 1을 빼면 마지막 노드를 건너뛰어 우측 뷰가 불완전해집니다.
        en: Subtracting 1 skips the last node, making the right view incomplete.
  - label:
      ko: 현재 레벨의 모든 노드 순회
      en: Iterate through current level
    indent: 1
    options:
    - code: 'for i in range(qLen):'
      type: good
      why:
        ko: 정확히 qLen번 반복하여 현재 레벨만 처리하고, 자식들은 다음 반복에서 다음 레벨이 됩니다.
        en: Loop exactly qLen times to process only this level; children become the next level in the next iteration.
    - code: 'for node in q:'
      type: distractor
      why:
        ko: 루프 중에 큐를 수정하면 반복이 예상대로 작동하지 않습니다.
        en: Modifying the queue while iterating causes unpredictable behavior and incorrect level separation.
    - code: 'for i in range(qLen + 1):'
      type: distractor
      why:
        ko: 범위가 초과하면 존재하지 않는 요소에 접근하려고 하여 IndexError가 발생합니다.
        en: Exceeding the range causes attempts to access non-existent elements, raising an error.
  - label:
      ko: 노드 처리 및 우측 추적
      en: Dequeue and track rightmost
    indent: 2
    options:
    - code: node = q.popleft()
      type: good
      why:
        ko: 노드를 팝하고, 유효하면 우측 노드로 업데이트하고, 양쪽 자식을 큐에 추가합니다.
        en: Dequeue the node, update rightmost if valid, and add both children to queue.
    - code: 'rightSide = node

        q.append(node.left)

        q.append(node.right)'
      type: distractor
      why:
        ko: if 체크 밖에서 업데이트하면 null 노드도 rightSide를 덮어쓰므로 틀린 답이 나옵니다.
        en: Updating outside the if check lets null nodes overwrite rightSide, producing wrong results.
    - code: "if node:\n                    rightSide = node"
      type: distractor
      why:
        ko: 자식을 큐에 추가하지 않으면 트리 탐색이 중단됩니다.
        en: Without enqueueing children, the tree traversal stops prematurely.
  - label:
      ko: 우측 노드값을 결과에 추가
      en: Append rightmost value
    indent: 1
    options:
    - code: 'if rightSide:'
      type: good
      why:
        ko: 레벨에 유효한 노드가 있으면 그 값을 결과 리스트에 추가합니다.
        en: If the level had valid nodes, add the rightmost value to the result list.
    - code: res.append(rightSide)
      type: distractor
      why:
        ko: 노드 객체 자체를 추가하면 값 대신 객체 참조가 저장됩니다.
        en: Appending the node object stores a reference instead of its integer value.
    - code: res.append(rightSide) if rightSide else pass
      type: distractor
      why:
        ko: 이미 if rightSide 블록 내부에 있으므로 추가 체크는 불필요하고 혼란스럽습니다.
        en: Already inside an if rightSide block, so additional checks are redundant and confusing.
trace:
  code:
  - '# Definition for a binary tree node.'
  - '# class TreeNode:'
  - '#     def __init__(self, val=0, left=None, right=None):'
  - '#         self.val = val'
  - '#         self.left = left'
  - '#         self.right = right'
  - 'class Solution:'
  - '    def rightSideView(self, root: TreeNode) -> List[int]:'
  - '        res = []'
  - '        q = collections.deque([root])'
  - ''
  - '        while q:'
  - '            rightSide = None'
  - '            qLen = len(q)'
  - ''
  - '            for i in range(qLen):'
  - '                node = q.popleft()'
  - '                if node:'
  - '                    rightSide = node'
  - '                    q.append(node.left)'
  - '                    q.append(node.right)'
  - '            if rightSide:'
  - '                res.append(rightSide.val)'
  - '        return res'
  cases:
  - input: '[1,2,3,null,5,null,4]'
    expected: '[1,3,4]'
  - input: '[1,2,3,4,null,null,null,5]'
    expected: '[1,3,4,5]'
  - input: '[1,null,3]'
    expected: '[1,3]'
  - input: '[]'
    expected: '[]'
  worked_example:
    input: '[1,2,3,null,5,null,4]'
    steps:
    - ko: '초기: res=[], q=[1]. 레벨 0 처리: 노드 1을 팝하고 우측=1, 자식 2,3 추가. res=[1], q=[2,3]'
      en: 'Initial: res=[], q=[1]. Level 0: Dequeue 1, set rightmost=1, enqueue children. res=[1], q=[2,3]'
    - ko: '레벨 1: 노드 2팝 (우측=2), 노드 3팝 (우측=3으로 업데이트). 자식 5,null,null,4 추가. res=[1,3], q=[5,null,null,4]'
      en: 'Level 1: Dequeue 2 (rightmost=2), then 3 (rightmost→3). Add children. res=[1,3], q=[5,null,null,4]'
    - ko: '레벨 2: 노드 5팝 (우측=5), null 스킵, null 스킵, 노드 4팝 (우측=4로 업데이트). res=[1,3,4], q=[]'
      en: 'Level 2: Dequeue 5 (rightmost=5), skip two nulls, dequeue 4 (rightmost→4). res=[1,3,4], q=[]'
    answer: '[1,3,4]'
solution:
  code: "# Definition for a binary tree node.\n# class TreeNode:\n#     def __init__(self, val=0, left=None, right=None):\n#         self.val = val\n#         self.left = left\n#         self.right = right\nclass Solution:\n    def rightSideView(self, root: TreeNode) -> List[int]:\n        res = []\n        q = collections.deque([root])\n\n        while q:\n            rightSide = None\n            qLen = len(q)\n\n            for i in range(qLen):\n                node = q.popleft()\n                if node:\n                    rightSide = node\n                    q.append(node.left)\n                    q.append(node.right)\n            if rightSide:\n                res.append(rightSide.val)\n        return res\n"
  complexity:
    time: O(n)
    space: O(w), where w is the maximum width of the tree
  followup:
  - ko: DFS로 이 문제를 풀 수 있나요? 시간/공간 복잡도는 어떻게 될까요?
    en: Can you solve this with DFS? What would the time/space complexity be?
  - ko: 좌측 뷰(left side view)를 구하려면 코드를 어떻게 수정해야 하나요?
    en: How would you modify this to get the left side view instead?
  - ko: 공간 복잡도를 O(h)(높이)로 개선할 수 있나요?
    en: Can you optimize the space complexity to O(h) where h is the height?
```
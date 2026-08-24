---
created: '2026-06-22'
date: '2026-06-22'
day: Day 47
difficulty: easy
id: A-047
source:
  curated_in:
  - neetcode150
  number: 104
  platform: leetcode
  slug: maximum-depth-of-binary-tree
  url: https://leetcode.com/problems/maximum-depth-of-binary-tree/
tags:
- tree
- depth-first-search
- breadth-first-search
- binary-tree
title:
  en: Maximum Depth of Binary Tree
  ko: 이진 트리의 최대 깊이
today: false
type: algorithm
updated: '2026-06-22'
visible: true
---

# 이진 트리의 최대 깊이

## Data

```yaml
problem:
  title:
    ko: 이진 트리의 최대 깊이
    en: Maximum Depth of Binary Tree
  statement:
    ko: '이진 트리의 루트가 주어졌을 때, 그것의 최대 깊이를 반환하세요.


      이진 트리의 최대 깊이는 루트 노드에서 가장 먼 리프 노드까지 가는 가장 긴 경로 위의 노드 개수입니다.'
    en: 'Given the root of a binary tree, return its maximum depth.


      A binary tree''s maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.'
  constraints:
  - 0 ≤ number of nodes ≤ 10^4
  - -100 ≤ Node.val ≤ 100
  io:
  - input: '[3,9,20,null,null,15,7]'
    output: '3'
  - input: '[1,null,2]'
    output: '2'
clarifying:
  items:
  - q:
      ko: 빈 트리(root = null)의 최대 깊이는 0입니까?
      en: Does an empty tree (root = null) have maximum depth of 0?
    type: good
    why:
      ko: 문제 제약에서 빈 트리를 허용하므로, null 케이스를 정확히 이해하는 것이 필수적입니다.
      en: The problem constraints allow empty trees [0, 10^4], so understanding the null base case is critical.
  - q:
      ko: 최대 깊이는 가장 긴 경로의 노드 개수입니까 아니면 엣지 개수입니까?
      en: Is maximum depth counted in nodes or edges along the longest path?
    type: good
    why:
      ko: 문제에서 명확히 '가장 긴 경로 위의 노드 개수'라고 정의하고 있으므로 이 구분이 중요합니다.
      en: The problem explicitly states 'number of nodes along the longest path', not edge count.
  - q:
      ko: 루트 노드만 있는 트리의 깊이는 몇입니까?
      en: What is the depth of a tree containing only the root node?
    type: good
    why:
      ko: 기본 케이스를 이해하기 위한 중요한 테스트입니다. 노드가 하나라면 깊이는 1입니다.
      en: Essential test of base case understanding. A single-node tree has depth 1.
  - q:
      ko: null 자식 노드는 깊이 계산에 포함되어야 합니까?
      en: Should null nodes contribute to the depth count?
    type: good
    why:
      ko: null 노드는 세지 않는다는 것을 이해하는 것은 재귀적 구현에서 핵심입니다.
      en: Understanding that null nodes don't count is critical for correct recursive implementation.
  - q:
      ko: 최대 깊이를 찾기 위해 모든 노드를 반드시 방문해야 합니까?
      en: Must we visit every single node to find the maximum depth?
    type: distractor
    why:
      ko: DFS/BFS 탐색은 결과적으로 모든 노드를 방문하지만, 이것이 필수 요구사항은 아닙니다. 혼동할 수 있습니다.
      en: While DFS/BFS visit all nodes, this is not a necessary requirement. Can be confusing.
  - q:
      ko: 스택을 명시적으로 사용하여 재귀 없이 구현할 수 있습니까?
      en: Can we solve this iteratively using an explicit stack?
    type: good
    why:
      ko: DFS 스택과 BFS 큐를 포함한 여러 접근 방식이 가능하며, 이를 알고 있으면 문제 해결 능력을 보여줍니다.
      en: Multiple valid approaches (iterative stack, BFS queue) demonstrate algorithmic flexibility.
approach:
  items:
  - name:
      ko: 재귀적 깊이 우선 탐색
      en: Recursive Depth-First Search
    complexity: O(n) time / O(h) space
    type: good
    why:
      ko: 트리 구조를 자연스럽게 활용하는 우아한 해결책입니다. 각 노드를 O(1)에 처리하고 재귀 스택은 트리 높이만큼만 사용합니다.
      en: Elegant solution leveraging tree structure naturally. Processes each node in O(1); recursion stack uses O(h) space.
  - name:
      ko: 반복적 스택 기반 DFS
      en: Iterative Stack-based DFS
    complexity: O(n) time / O(h) space
    type: good
    why:
      ko: 재귀 스택 제한을 피하고 명시적 스택을 사용합니다. 인터뷰에서 다양한 접근 방식을 알고 있음을 보여줄 수 있습니다.
      en: Avoids recursion depth limits by using explicit stack. Shows awareness of multiple implementation styles.
  - name:
      ko: 너비 우선 탐색 (큐 사용)
      en: Breadth-First Search with Queue
    complexity: O(n) time / O(w) space
    type: good
    why:
      ko: 레벨별 탐색이 깊이를 자연스럽게 세어줍니다. 공간은 트리의 최대 너비 w에 비례하며, 균형 트리에서는 약 O(n/2)입니다.
      en: Level-order traversal naturally counts depth. Space usage is O(w) where w is max level width.
  - name:
      ko: 완전 탐색 - 모든 리프 노드 추적
      en: Brute Force - Enumerate all leaf depths
    complexity: O(n) time / O(h) space
    type: distractor
    why:
      ko: 모든 리프 노드를 명시적으로 찾은 후 최대 깊이를 계산하는 방식은 더 복잡하고 불필요합니다.
      en: Explicitly finding all leaves then computing max depth is more complex than necessary.
  - name:
      ko: 중위 탐색으로 깊이 추적
      en: In-order Traversal with Depth Tracking
    complexity: O(n) time / O(h) space
    type: distractor
    why:
      ko: 특정 탐색 순서(중위, 후위 등)에 제약을 두는 것은 불필요합니다. 모든 탐색 순서가 동일하게 작동합니다.
      en: Restricting to specific traversal order is unnecessary. All traversal orders work equally well.
logic:
  format: slot
  slots:
  - label:
      ko: '기본 케이스: 빈 트리 확인'
      en: 'Base case: Check if tree is empty'
    indent: 0
    options:
    - code: 'if not root:'
      type: good
      why:
        ko: 재귀의 종료 조건입니다. null 또는 빈 서브트리를 먼저 처리해야 합니다.
        en: Termination condition for recursion. Must handle null/empty subtrees as base case.
    - code: 'if root.left is None and root.right is None:'
      type: distractor
      why:
        ko: 이 조건은 리프 노드(자식이 없는 노드)를 확인하는 것이지, 빈 트리를 확인하는 것이 아닙니다.
        en: This checks for leaf nodes (nodes with no children), not empty trees.
    - code: 'if root is not None:'
      type: distractor
      why:
        ko: 조건이 반대로 되어 로직이 잘못됩니다. 기본 케이스를 건너뜁니다.
        en: Condition is inverted; skips base case logic.
  - label:
      ko: '기본 케이스: 반환값'
      en: 'Base case: Return value for empty tree'
    indent: 1
    options:
    - code: return 0
      type: good
      why:
        ko: null 노드는 깊이 계산에 0을 기여합니다. 빈 서브트리의 깊이는 0입니다.
        en: Null nodes contribute 0 to depth calculation. Empty subtree has depth 0.
    - code: return 1
      type: distractor
      why:
        ko: off-by-one 오류입니다. null 노드는 1이 아니라 0을 기여합니다.
        en: Off-by-one error. Null nodes contribute 0, not 1.
    - code: return -1
      type: distractor
      why:
        ko: 음수를 반환하면 max() 계산에서 부정확한 결과를 얻게 됩니다.
        en: Negative value corrupts max() calculation and produces wrong answer.
  - label:
      ko: '재귀: 왼쪽 서브트리 탐색'
      en: 'Recursive call: Explore left subtree'
    indent: 0
    options:
    - code: return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))
      type: good
      why:
        ko: 왼쪽 자식 서브트리의 최대 깊이를 재귀적으로 구합니다.
        en: Recursively compute maximum depth of left subtree.
    - code: self.maxDepth(root.left.left)
      type: distractor
      why:
        ko: 자식이 아니라 손자를 호출하므로, 중간 서브트리를 건너뜁니다.
        en: Calling grandchild instead of child skips intermediate subtree.
    - code: self.maxDepth(root.right)
      type: distractor
      why:
        ko: 이것은 오른쪽 자식입니다. 왼쪽과 오른쪽 모두를 확인해야 합니다.
        en: This is right child. Must check both left and right subtrees.
  - label:
      ko: '결과 결합: 더 깊은 쪽 선택'
      en: 'Combine: Take maximum of both subtrees'
    indent: 0
    options:
    - code: return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))
      type: good
      why:
        ko: 최대 깊이는 왼쪽과 오른쪽 중 더 깊은 쪽입니다. max()를 사용하여 큰 값을 선택합니다.
        en: Maximum depth is the deeper of left and right subtrees. Use max() to select larger value.
    - code: left_depth + right_depth
      type: distractor
      why:
        ko: 두 경로를 더하면 잘못된 계산입니다. 깊이는 최대 경로이지, 합이 아닙니다.
        en: Adding both paths is wrong. Depth is the longest single path, not the sum.
    - code: max(left_depth, right_depth)
      type: distractor
      why:
        ko: 최대값만 취하면 현재 노드를 세지 않습니다. 반드시 +1을 해야 합니다.
        en: Taking max without +1 forgets to count the current node in the depth.
  - label:
      ko: '완전 반환문: 현재 노드 포함'
      en: 'Complete return: Add current node to best subtree'
    indent: 0
    options:
    - code: return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))
      type: good
      why:
        ko: 현재 노드(1)를 더하고, 왼쪽과 오른쪽 깊이의 최대값을 더합니다.
        en: Add current node (1) to the maximum depth of left and right subtrees.
    - code: return 1 + self.maxDepth(root.left) + self.maxDepth(root.right)
      type: distractor
      why:
        ko: 두 자식의 깊이를 더하는 것은 잘못되었습니다. 가장 깊은 경로 하나만 선택해야 합니다.
        en: Adding both child depths is wrong. Only one longest path should be counted.
    - code: return max(self.maxDepth(root.left), self.maxDepth(root.right))
      type: distractor
      why:
        ko: 현재 노드(+1)를 빼먹었습니다. 깊이에는 현재 노드도 포함됩니다.
        en: Forgot to add 1 for current node. Node count must include the current node.
trace:
  code:
  - '# RECURSIVE DFS'
  - 'class Solution:'
  - '    def maxDepth(self, root: TreeNode) -> int:'
  - '        if not root:'
  - '            return 0'
  - ''
  - '        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))'
  - ''
  - ''
  - '# ITERATIVE DFS'
  - 'class Solution:'
  - '    def maxDepth(self, root: TreeNode) -> int:'
  - '        stack = [[root, 1]]'
  - '        res = 0'
  - ''
  - '        while stack:'
  - '            node, depth = stack.pop()'
  - ''
  - '            if node:'
  - '                res = max(res, depth)'
  - '                stack.append([node.left, depth + 1])'
  - '                stack.append([node.right, depth + 1])'
  - '        return res'
  - ''
  - ''
  - '# BFS'
  - 'class Solution:'
  - '    def maxDepth(self, root: TreeNode) -> int:'
  - '        q = deque()'
  - '        if root:'
  - '            q.append(root)'
  - ''
  - '        level = 0'
  - ''
  - '        while q:'
  - ''
  - '            for i in range(len(q)):'
  - '                node = q.popleft()'
  - '                if node.left:'
  - '                    q.append(node.left)'
  - '                if node.right:'
  - '                    q.append(node.right)'
  - '            level += 1'
  - '        return level'
  cases:
  - input: '[3,9,20,null,null,15,7]'
    expected: '3'
  - input: '[1,null,2]'
    expected: '2'
  worked_example:
    input: '[3,9,20,null,null,15,7]'
    steps:
    - ko: 루트 노드 3에서 시작합니다. null이 아니므로 재귀를 계속합니다.
      en: Start at root node 3. Not null, so continue recursion.
    - ko: 'maxDepth(9) 호출: 노드 9는 자식이 없으므로 1 + max(0, 0) = 1을 반환합니다.'
      en: 'Call maxDepth(9): node 9 is a leaf, returns 1 + max(0, 0) = 1.'
    - ko: 'maxDepth(20) 호출: 자식 15와 7이 각각 깊이 1이므로 1 + max(1, 1) = 2를 반환합니다.'
      en: 'Call maxDepth(20): children 15 and 7 each return depth 1, so 1 + max(1, 1) = 2.'
    - ko: maxDepth(3) = 1 + max(1, 2) = 3을 반환합니다.
      en: maxDepth(3) = 1 + max(1, 2) = 3.
    answer: '3'
solution:
  code: "# RECURSIVE DFS\nclass Solution:\n    def maxDepth(self, root: TreeNode) -> int:\n        if not root:\n            return 0\n\n        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))\n\n\n# ITERATIVE DFS\nclass Solution:\n    def maxDepth(self, root: TreeNode) -> int:\n        stack = [[root, 1]]\n        res = 0\n\n        while stack:\n            node, depth = stack.pop()\n\n            if node:\n                res = max(res, depth)\n                stack.append([node.left, depth + 1])\n                stack.append([node.right, depth + 1])\n        return res\n\n\n# BFS\nclass Solution:\n    def maxDepth(self, root: TreeNode) -> int:\n        q = deque()\n        if root:\n            q.append(root)\n\n        level = 0\n\n        while q:\n\n            for i in range(len(q)):\n                node = q.popleft()\n                if node.left:\n                    q.append(node.left)\n                if node.right:\n                    q.append(node.right)\n\
    \            level += 1\n        return level\n"
  complexity:
    time: O(n)
    space: O(h) where h is height
  followup:
  - ko: 스택을 사용하여 반복적인 DFS 버전을 구현할 수 있습니까?
    en: Implement an iterative version using an explicit stack instead of recursion.
  - ko: 최대 깊이뿐만 아니라 최대 깊이까지의 실제 경로도 반환하려면 어떻게 합니까?
    en: How would you modify the solution to also return the actual path to the deepest node?
  - ko: 이 문제에서 BFS와 DFS의 공간 복잡도를 비교하면 어떤 차이가 있습니까?
    en: Compare the space complexity of BFS versus DFS for this specific problem.
```
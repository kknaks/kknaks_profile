---
created: '2026-06-21'
date: '2026-06-21'
day: Day 46
difficulty: easy
id: A-046
source:
  curated_in:
  - neetcode150
  number: 226
  platform: leetcode
  slug: invert-binary-tree
  url: https://leetcode.com/problems/invert-binary-tree/
status: draft
tags:
- tree
- depth-first-search
- breadth-first-search
- binary-tree
title:
  en: Invert Binary Tree
  ko: 이진 트리 뒤집기
today: false
type: algorithm
updated: '2026-06-21'
visible: true
---

# 이진 트리 뒤집기

## Data

```yaml
problem:
  title:
    ko: 이진 트리 뒤집기
    en: Invert Binary Tree
  statement:
    ko: 이진 트리의 루트가 주어졌을 때, 트리를 뒤집고 루트를 반환하세요. 트리를 뒤집는 것은 각 노드에서 왼쪽 자식과 오른쪽 자식을 서로 교환하는 것을 의미합니다.
    en: Given the root of a binary tree, invert the tree, and return its root. Inverting a tree means swapping the left and right children at every node.
  constraints:
  - The number of nodes in the tree is in the range [0, 100]
  - -100 ≤ Node.val ≤ 100
  io:
  - input: '[4,2,7,1,3,6,9]'
    output: '[4,7,2,9,6,3,1]'
  - input: '[2,1,3]'
    output: '[2,3,1]'
  - input: '[]'
    output: '[]'
clarifying:
  items:
  - q:
      ko: 트리를 뒤집는다는 것은 정확히 무엇을 의미하나요?
      en: What exactly does it mean to invert a tree?
    type: good
    why:
      ko: 뒤집기의 정의를 명확히 하면 모든 노드에서 왼쪽과 오른쪽 자식을 교환해야 한다는 것을 이해할 수 있습니다.
      en: Clarifying the definition helps understand that we need to swap left and right children at every node.
  - q:
      ko: 원본 트리를 수정해도 되나요, 아니면 새로운 트리를 만들어야 하나요?
      en: Should we modify the original tree in-place or create a new tree?
    type: good
    why:
      ko: 문제에서 명시적으로 제한하지 않으므로 둘 다 가능하지만, 원본 수정이 공간을 더 절약합니다.
      en: The problem doesn't explicitly restrict this, so both approaches work, but in-place modification saves space.
  - q:
      ko: 재귀 대신 반복문(BFS/큐)을 사용할 수 있나요?
      en: Can we use iteration (BFS/queue) instead of recursion?
    type: good
    why:
      ko: 네, BFS를 사용하면 스택 오버플로우 위험 없이 반복적으로 해결할 수 있습니다.
      en: Yes, BFS allows an iterative solution without recursion stack overflow risk.
  - q:
      ko: 빈 트리는 어떻게 처리해야 하나요?
      en: How should we handle an empty tree?
    type: good
    why:
      ko: 빈 트리(root = None)는 그대로 None을 반환하면 됩니다. 기본 경우로 처리됩니다.
      en: An empty tree (root = None) should return None as-is; it's handled as the base case.
  - q:
      ko: 노드의 값도 역순으로 변경해야 하나요?
      en: Should we also reverse the order of node values?
    type: distractor
    why:
      ko: 아니요, 노드의 값은 변경하지 않습니다. 트리의 구조(왼쪽/오른쪽 자식)만 뒤집습니다.
      en: No, we don't change node values. We only invert the structure (left/right children).
  - q:
      ko: 리프 노드(자식이 없는 노드)만 뒤집으면 되나요?
      en: Do we only need to invert leaf nodes?
    type: distractor
    why:
      ko: 아니요, 모든 노드에서 왼쪽과 오른쪽 자식을 교환해야 합니다.
      en: No, we must swap left and right children at every node, not just leaves.
approach:
  items:
  - name:
      ko: 깊이 우선 탐색 (재귀)
      en: Depth-First Search (Recursion)
    complexity: O(n) time / O(h) space
    type: good
    why:
      ko: 각 노드를 정확히 한 번 방문하고, 재귀 스택은 트리 높이만큼 커집니다. 직관적이고 간단합니다.
      en: Visit each node exactly once; recursion stack depth equals tree height. Intuitive and simple.
  - name:
      ko: 너비 우선 탐색 (큐)
      en: Breadth-First Search (Queue)
    complexity: O(n) time / O(w) space
    type: good
    why:
      ko: 각 노드를 한 번 방문하며, 큐 크기는 트리의 최대 너비에 비례합니다. 반복문 기반이므로 스택 오버플로우를 피할 수 있습니다.
      en: Visit each node once; queue size proportional to tree's max width. Iterative approach avoids recursion stack limits.
  - name:
      ko: 값 역순 처리 (잘못된 접근)
      en: Reversing Node Values (Incorrect)
    complexity: O(n) time / O(h) space
    type: distractor
    why:
      ko: 노드의 값을 역순으로 변경하면 문제를 잘못 이해한 것입니다. 트리는 구조 기반이지 값 기반이 아닙니다.
      en: 'Reversing values misses the problem: we invert structure, not values. The tree structure determines the inversion.'
  - name:
      ko: 리프 노드만 뒤집기 (불완전)
      en: Inverting Only Leaf Nodes (Incomplete)
    complexity: O(n) time / O(h) space
    type: distractor
    why:
      ko: 리프 노드만 처리하면 내부 노드의 구조가 유지되어 완전한 뒤집기가 아닙니다.
      en: Only processing leaves leaves internal nodes unchanged, resulting in an incomplete inversion.
logic:
  format: slot
  slots:
  - label:
      ko: '기본 경우: 공 노드 확인'
      en: 'Base Case: Check for null node'
    indent: 0
    options:
    - code: 'if not root:'
      type: good
      why:
        ko: 트리가 비어있거나 노드가 None이면 재귀를 중단합니다. 이는 모든 재귀의 종료 조건입니다.
        en: If the tree is empty (root is None), stop recursion. This is the termination condition for all recursive calls.
    - code: 'if root is None:'
      type: distractor
      why:
        ko: '`is None` 대신 `not root`를 사용하는 것이 더 Pythonic하고 일반적입니다.'
        en: Using `is None` works but `not root` is more Pythonic; both are functionally equivalent.
    - code: 'if not root.left and not root.right:'
      type: distractor
      why:
        ko: 리프 노드만 확인하면 안 됩니다. 모든 null 노드를 기본 경우로 처리해야 합니다.
        en: This only checks leaf nodes; we need to handle all None nodes as base cases.
  - label:
      ko: '자식 교환: 왼쪽과 오른쪽 교체'
      en: 'Swap Children: Exchange left and right'
    indent: 1
    options:
    - code: root.left, root.right = root.right, root.left
      type: good
      why:
        ko: 현재 노드의 왼쪽과 오른쪽 자식을 동시에 교환합니다. Python의 튜플 할당으로 임시 변수 없이 우아하게 처리됩니다.
        en: Simultaneously swap the current node's left and right children. Python's tuple assignment avoids temporary variables.
    - code: 'temp = root.left

        root.left = root.right

        root.right = temp'
      type: distractor
      why:
        ko: 작동하지만 불필요한 임시 변수를 사용합니다. Python에서는 튜플 할당이 더 간단합니다.
        en: Works but uses unnecessary temp variable; Python tuple assignment is cleaner.
    - code: root.left, root.right = root.left, root.right
      type: distractor
      why:
        ko: 왼쪽과 오른쪽을 바꾸지 않고 그대로 유지합니다. 교환이 없으므로 아무것도 뒤집어지지 않습니다.
        en: Assigns left to left, right to right—no swap occurs, so nothing is inverted.
  - label:
      ko: '재귀: 왼쪽 부분트리 처리'
      en: 'Recursion: Process left subtree'
    indent: 1
    options:
    - code: self.invertTree(root.left)
      type: good
      why:
        ko: 왼쪽 자식에 대해 동일한 뒤집기 연산을 재귀적으로 수행합니다.
        en: Recursively apply the same inversion operation to the left child.
    - code: self.invertTree(root.right)
      type: distractor
      why:
        ko: 오른쪽을 먼저 처리하면 논리적 순서가 바뀝니다. 두 호출을 모두 해야 합니다.
        en: Processing right first changes order; both calls are needed.
    - code: self.invertTree(root.left.left)
      type: distractor
      why:
        ko: 왼쪽의 왼쪽만 처리하면 일부 노드를 건너뜁니다. 왼쪽 자식 전체를 처리해야 합니다.
        en: Processing only left.left skips nodes; we must process the entire left child.
  - label:
      ko: '재귀: 오른쪽 부분트리 처리'
      en: 'Recursion: Process right subtree'
    indent: 1
    options:
    - code: self.invertTree(root.right)
      type: good
      why:
        ko: 오른쪽 자식에 대해 동일한 뒤집기 연산을 재귀적으로 수행합니다.
        en: Recursively apply the same inversion operation to the right child.
    - code: self.invertTree(root.left)
      type: distractor
      why:
        ko: 왼쪽을 두 번 처리하면 오른쪽이 누락됩니다. 왼쪽과 오른쪽 모두 처리해야 합니다.
        en: Processing left twice misses the right subtree; both must be processed.
    - code: pass
      type: distractor
      why:
        ko: 오른쪽 부분트리를 건너뛰면 완전한 뒤집기가 불가능합니다.
        en: Skipping the right subtree results in incomplete inversion.
  - label:
      ko: '반환: 뒤집힌 노드 반환'
      en: 'Return: Return the inverted node'
    indent: 1
    options:
    - code: return root
      type: good
      why:
        ko: 뒤집힌 현재 노드를 반환합니다. 모든 재귀 호출이 완료된 후 수정된 트리를 반환합니다.
        en: Return the current inverted node after all recursive calls complete, propagating the modified tree back up.
    - code: return None
      type: distractor
      why:
        ko: None을 반환하면 뒤집힌 트리를 잃어버립니다. 현재 노드를 반환해야 합니다.
        en: Returning None loses the inverted tree; we must return the current node.
    - code: return root.left
      type: distractor
      why:
        ko: 왼쪽 자식만 반환하면 오른쪽 부분이 누락됩니다. 루트를 반환해야 합니다.
        en: Returning only left child loses the right subtree; return root to preserve both.
trace:
  code:
  - '# Definition for a binary tree node.'
  - '# class TreeNode:'
  - '#     def __init__(self, val=0, left=None, right=None):'
  - '#         self.val = val'
  - '#         self.left = left'
  - '#         self.right = right'
  - 'class Solution:'
  - '    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:'
  - '        if not root:'
  - '            return None'
  - '        '
  - '        # swap the children'
  - '        root.left, root.right = root.right, root.left'
  - '        '
  - '        # make 2 recursive calls'
  - '        self.invertTree(root.left)'
  - '        self.invertTree(root.right)'
  - '        return root'
  cases:
  - input: '[4,2,7,1,3,6,9]'
    expected: '[4,7,2,9,6,3,1]'
  - input: '[2,1,3]'
    expected: '[2,3,1]'
  - input: '[]'
    expected: '[]'
  worked_example:
    input: '[4,2,7,1,3,6,9]'
    steps:
    - ko: 'root=4에서 시작: 왼쪽(2)과 오른쪽(7)을 교환 → 4의 왼쪽=7, 오른쪽=2'
      en: 'Start at root 4: swap left (2) and right (7) → 4''s left becomes 7, right becomes 2'
    - ko: '왼쪽 부분트리(7)에서: 왼쪽(6)과 오른쪽(9)을 교환 → 7의 왼쪽=9, 오른쪽=6'
      en: 'Left subtree (7): swap left (6) and right (9) → 7''s left becomes 9, right becomes 6'
    - ko: '오른쪽 부분트리(2)에서: 왼쪽(1)과 오른쪽(3)을 교환 → 2의 왼쪽=3, 오른쪽=1'
      en: 'Right subtree (2): swap left (1) and right (3) → 2''s left becomes 3, right becomes 1'
    - ko: 모든 노드의 교환이 완료되었고, 뒤집힌 트리가 반환됨
      en: All nodes processed, inverted tree returned with level-order [4,7,2,9,6,3,1]
    answer: '[4,7,2,9,6,3,1]'
solution:
  code: "# Definition for a binary tree node.\n# class TreeNode:\n#     def __init__(self, val=0, left=None, right=None):\n#         self.val = val\n#         self.left = left\n#         self.right = right\nclass Solution:\n    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:\n        if not root:\n            return None\n        \n        # swap the children\n        root.left, root.right = root.right, root.left\n        \n        # make 2 recursive calls\n        self.invertTree(root.left)\n        self.invertTree(root.right)\n        return root\n"
  complexity:
    time: O(n)
    space: O(h)
  followup:
  - ko: BFS(너비 우선 탐색)를 사용하여 반복적으로 해결할 수 있나요?
    en: Can you solve this iteratively using BFS with a queue?
  - ko: 원본 트리를 수정하지 않고 새로운 뒤집힌 트리를 만들 수 있나요?
    en: How would you create a new inverted tree without modifying the original?
  - ko: 매우 깊은 트리(깊이 10,000+)에서 재귀 깊이 제한을 피하려면 어떻게 해야 할까요?
    en: How would you avoid recursion depth limits for very deep trees (depth 10,000+)?
```
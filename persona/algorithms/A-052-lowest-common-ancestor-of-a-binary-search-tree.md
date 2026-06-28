---
created: '2026-06-28'
date: '2026-06-28'
day: Day 52
difficulty: medium
id: A-052
source:
  curated_in:
  - neetcode150
  number: 235
  platform: leetcode
  slug: lowest-common-ancestor-of-a-binary-search-tree
  url: https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/
status: draft
tags:
- tree
- depth-first-search
- binary-search-tree
- binary-tree
title:
  en: Lowest Common Ancestor of a Binary Search Tree
  ko: 이진 탐색 트리의 최저 공통 조상
today: true
type: algorithm
updated: '2026-06-28'
visible: true
---

# 이진 탐색 트리의 최저 공통 조상

## Data

```yaml
problem:
  title:
    ko: 이진 탐색 트리의 최저 공통 조상
    en: Lowest Common Ancestor of a Binary Search Tree
  statement:
    en: 'Given a binary search tree (BST), find the lowest common ancestor (LCA) node of two given nodes in the BST.


      According to the definition of LCA on Wikipedia: "The lowest common ancestor is defined between two nodes p and q as the lowest node in T that has both p and q as descendants (where we allow a node to be a descendant of itself)."'
    ko: '이진 탐색 트리(BST)가 주어지면, 두 개의 주어진 노드 p와 q의 최저 공통 조상(LCA) 노드를 찾으세요.


      위키피디아의 LCA 정의에 따르면: "최저 공통 조상은 두 노드 p와 q 사이에서 p와 q를 모두 후손으로 가지는 T의 가장 낮은 노드로 정의됩니다(노드가 자기 자신의 후손이 될 수 있습니다)."'
  constraints:
  - 2 ≤ number of nodes ≤ 10^5
  - -10^9 ≤ Node.val ≤ 10^9
  - All Node.val are unique
  - p ≠ q and both exist in BST
  io:
  - input: '[6,2,8,0,4,7,9,null,null,3,5]

      2

      8'
    output: '6'
  - input: '[6,2,8,0,4,7,9,null,null,3,5]

      2

      4'
    output: '2'
  - input: '[2,1]

      2

      1'
    output: '2'
clarifying:
  items:
  - q:
      ko: 노드가 자기 자신의 후손이 될 수 있다는 것이 무엇을 의미하나요?
      en: What does it mean that a node can be a descendant of itself?
    type: good
    why:
      ko: LCA 정의의 핵심입니다. p가 q의 조상이면 p 자신이 LCA가 될 수 있다는 뜻입니다.
      en: This is crucial to the LCA definition—if p is an ancestor of q, then p itself can be the LCA.
  - q:
      ko: p와 q를 찾기 위해 먼저 트리를 탐색해야 하나요?
      en: Do we need to search for p and q in the tree first?
    type: good
    why:
      ko: 문제에서 p와 q가 존재한다고 보장하므로, 노드의 값만 비교하여 네비게이션할 수 있습니다.
      en: The problem guarantees both exist, so we can navigate using only their values without searching.
  - q:
      ko: BST 성질이 LCA 찾기에 어떻게 도움이 되나요?
      en: How does the BST property help us find the LCA efficiently?
    type: good
    why:
      ko: BST의 순서 성질(좌 < 루트 < 우)로 인해 매 단계마다 절반의 트리를 제거할 수 있습니다.
      en: BST ordering lets us eliminate half the tree at each step without examining every node.
  - q:
      ko: p와 q가 다른 부분트리에 있으면 어떻게 되나요?
      en: What if p and q are in different subtrees of the current node?
    type: good
    why:
      ko: 그 경우 현재 노드가 분기점이며, 이것이 LCA입니다. else 절에서 처리됩니다.
      en: Then the current node is the split point and is the LCA—handled by the else clause.
  - q:
      ko: 시간 복잡도가 항상 O(log n)인가요?
      en: Is the time complexity always O(log n)?
    type: distractor
    why:
      ko: 아니요. 한쪽으로 치우친 트리에서는 최악의 경우 O(n)이 될 수 있습니다.
      en: No—worst case with a skewed (unbalanced) tree can be O(n).
  - q:
      ko: LCA는 항상 p 또는 q 중 하나인가요?
      en: Is the LCA always either p or q?
    type: distractor
    why:
      ko: 아니요. LCA는 p와 q 사이의 분기점이 될 수 있으며, 둘 다는 아닐 수 있습니다.
      en: No—the LCA can be a node strictly between p and q, or equal to neither.
  - q:
      ko: 반환된 노드가 정말 p와 q의 조상인지 검증해야 하나요?
      en: Should we verify the returned node is actually an ancestor of both p and q?
    type: good
    why:
      ko: 아니요. BST 성질과 입력 보장(p, q 존재)이 알고리즘의 정확성을 보장합니다.
      en: No—the BST property and input guarantees ensure the algorithm is correct by construction.
approach:
  items:
  - name:
      ko: BST 성질을 이용한 순회 (반복식)
      en: BST property traversal (iterative)
    complexity: O(log n) avg / O(n) worst; O(1) space
    type: good
    why:
      ko: BST의 순서 성질을 직접 활용하여 필요한 방향만 진행합니다. 반복 기반이므로 스택 오버헤드가 없습니다.
      en: Leverages BST ordering to eliminate half the tree each step. Iterative means no stack overhead.
  - name:
      ko: 경로 추적 후 비교
      en: Path tracking and comparison
    complexity: O(n) time / O(h) space
    type: good
    why:
      ko: 루트에서 각 노드까지의 경로를 찾고 첫 분기점을 식별합니다. 더 직관적이지만 덜 효율적입니다.
      en: Find root-to-node paths, then locate first divergence. More intuitive but slower.
  - name:
      ko: 전체 트리 재귀 탐색
      en: Recursive DFS of entire tree
    complexity: O(n) time / O(h) space
    type: distractor
    why:
      ko: 동작하지만 BST 성질을 무시하여 모든 노드를 확인합니다.
      en: Works but ignores BST property, needlessly visiting all nodes.
  - name:
      ko: 모든 노드를 집합에 저장
      en: Hash set of all nodes
    complexity: O(n) time / O(n) space
    type: distractor
    why:
      ko: 경로를 찾을 수 있지만 BST 이점을 버리고 불필요한 메모리를 사용합니다.
      en: Could work but wastes memory and doesn't exploit BST ordering.
  - name:
      ko: 선형 스캔으로 p, q 찾기
      en: Linear search for p and q
    complexity: O(n) time / O(1) space
    type: distractor
    why:
      ko: 트리 구조를 완전히 무시하고 배열처럼 처리합니다.
      en: Completely ignores tree structure and treats it as an array.
logic:
  format: slot
  slots:
  - label:
      ko: 무한 반복 루프 시작
      en: Begin infinite loop for traversal
    indent: 0
    options:
    - code: 'while True:'
      type: good
      why:
        ko: LCA를 찾을 때까지 계속 진행합니다. 각 반복에서 root를 업데이트하거나 반환합니다.
        en: Continue until LCA is found. Each iteration updates root or returns the answer.
    - code: 'for i in range(n):'
      type: distractor
      why:
        ko: 반복 횟수를 미리 알 수 없으므로 잘못된 루프 종류입니다.
        en: Wrong loop type; we don't know the iteration count in advance.
    - code: 'while root is not None:'
      type: distractor
      why:
        ko: valid input이 주어지면 root는 None이 되지 않으므로 조기 종료할 수 있습니다.
        en: Could terminate prematurely; root should never become None with valid input.
  - label:
      ko: 양쪽 노드가 우측 부분트리에 있는지 확인
      en: Check if both nodes are in right subtree
    indent: 1
    options:
    - code: 'if root.val < p.val and root.val < q.val:'
      type: good
      why:
        ko: p와 q의 값이 모두 root보다 크면, 둘 다 오른쪽 부분트리에 있습니다.
        en: If both p.val and q.val exceed root.val, both lie in the right subtree.
    - code: 'if root.val <= p.val and root.val <= q.val:'
      type: distractor
      why:
        ko: 등호를 포함하면 root가 p 또는 q와 같을 때 잘못된 분기가 됩니다.
        en: Including ≤ causes wrong branch when root equals p or q.
    - code: 'if root.val < p.val or root.val < q.val:'
      type: distractor
      why:
        ko: AND 대신 OR을 사용하면 한 노드만 오른쪽에 있어도 진행합니다.
        en: Using OR instead of AND incorrectly proceeds when only one node is right.
    - code: 'if p.val > root.val and q.val > root.val:'
      type: distractor
      why:
        ko: 비교 순서는 같지만 이것은 관례에 어긋나고 비교 방향이 명확하지 않습니다.
        en: Reversed comparison order; less clear and unconventional.
  - label:
      ko: 우측 부분트리로 이동
      en: Move to right subtree
    indent: 2
    options:
    - code: root = root.right
      type: good
      why:
        ko: 양쪽 노드가 오른쪽에 있으므로 root를 우측 자식으로 업데이트합니다.
        en: Update root to right child to continue the search in that direction.
    - code: root = root.left
      type: distractor
      why:
        ko: 방향이 정반대입니다. 오른쪽으로 가야 합니다.
        en: Wrong direction—should go right, not left.
    - code: return root.right
      type: distractor
      why:
        ko: 아직 반환해야 할 시점이 아닙니다. root를 업데이트하고 계속 탐색합니다.
        en: Should not return yet—update root and continue searching.
    - code: root = root.right.right
      type: distractor
      why:
        ko: 한 단계씩 이동해야 하는데 두 단계를 건너뜁니다.
        en: Should move one level at a time, not skip levels.
  - label:
      ko: 양쪽 노드가 좌측 부분트리에 있는지 확인
      en: Check if both nodes are in left subtree
    indent: 1
    options:
    - code: 'elif root.val > p.val and root.val > q.val:'
      type: good
      why:
        ko: p와 q의 값이 모두 root보다 작으면, 둘 다 왼쪽 부분트리에 있습니다.
        en: If both p.val and q.val are less than root.val, both lie in the left subtree.
    - code: 'elif root.val >= p.val and root.val >= q.val:'
      type: distractor
      why:
        ko: 등호를 포함하면 root가 p 또는 q와 같을 때 잘못된 분기가 됩니다.
        en: Including ≥ causes wrong branch when root equals p or q.
    - code: 'elif root.val > p.val or root.val > q.val:'
      type: distractor
      why:
        ko: AND 대신 OR을 사용하면 한 노드만 왼쪽에 있어도 진행합니다.
        en: Using OR instead of AND incorrectly proceeds when only one node is left.
    - code: 'elif p.val < root.val and q.val < root.val:'
      type: distractor
      why:
        ko: 비교 순서는 같지만 이것은 관례에 어긋나고 비교 방향이 명확하지 않습니다.
        en: Reversed comparison order; less clear and unconventional.
  - label:
      ko: 좌측 부분트리로 이동
      en: Move to left subtree
    indent: 2
    options:
    - code: root = root.left
      type: good
      why:
        ko: 양쪽 노드가 왼쪽에 있으므로 root를 좌측 자식으로 업데이트합니다.
        en: Update root to left child to continue the search in that direction.
    - code: root = root.right
      type: distractor
      why:
        ko: 방향이 정반대입니다. 왼쪽으로 가야 합니다.
        en: Wrong direction—should go left, not right.
    - code: return root.left
      type: distractor
      why:
        ko: 아직 반환해야 할 시점이 아닙니다. root를 업데이트하고 계속 탐색합니다.
        en: Should not return yet—update root and continue searching.
    - code: root = root
      type: distractor
      why:
        ko: 루트를 변경하지 않으면 무한 루프가 됩니다.
        en: No update creates an infinite loop.
  - label:
      ko: 분기점이거나 조상 노드 반환
      en: Return split point or ancestor node
    indent: 1
    options:
    - code: 'else:'
      type: good
      why:
        ko: 위 두 조건이 모두 거짓이면 현재 root가 LCA입니다(root == p 또는 q이거나, 둘이 다른 부분에 위치).
        en: When neither left nor right condition holds, root is the LCA—it's either p/q or their split point.
    - code: 'else: return None'
      type: distractor
      why:
        ko: LCA를 찾았는데 None을 반환하면 안 됩니다.
        en: Wrong—we found the LCA, should not return None.
    - code: 'else: continue'
      type: distractor
      why:
        ko: 루프를 계속하면 무한 루프가 됩니다. 조건을 만족하는 경로가 없기 때문입니다.
        en: Continuing creates an infinite loop—we've reached the LCA.
    - code: 'else: return root.left if root.left else root.right'
      type: distractor
      why:
        ko: 현재 노드을 반환해야 하는데 자식 노드를 반환합니다.
        en: Should return root itself, not one of its children.
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
  - '    def lowestCommonAncestor('
  - '        self, root: "TreeNode", p: "TreeNode", q: "TreeNode"'
  - '    ) -> "TreeNode":'
  - '        while True:'
  - '            if root.val < p.val and root.val < q.val:'
  - '                root = root.right'
  - '            elif root.val > p.val and root.val > q.val:'
  - '                root = root.left'
  - '            else:'
  - '                return root'
  cases:
  - input: '[6,2,8,0,4,7,9,null,null,3,5]

      2

      8'
    expected: '6'
  - input: '[6,2,8,0,4,7,9,null,null,3,5]

      2

      4'
    expected: '2'
  - input: '[2,1]

      2

      1'
    expected: '2'
  worked_example:
    input: '[6,2,8,0,4,7,9,null,null,3,5]

      2

      8'
    steps:
    - ko: 루트 = 6, p = 2, q = 8에서 시작합니다.
      en: 'Start: root = 6, p = 2, q = 8'
    - ko: 6 < 2이고 6 < 8? 아니요 (6은 2보다 큼). 6 > 2이고 6 > 8? 아니요 (6은 8보다 작음).
      en: Is 6 < 2 and 6 < 8? No. Is 6 > 2 and 6 > 8? No.
    - ko: 한 노드(2)는 왼쪽, 다른 노드(8)는 오른쪽에 있으므로 현재 노드 6이 분기점입니다.
      en: One node (2) is in left subtree, other (8) in right—6 is the split point.
    - ko: LCA = 6을 반환합니다.
      en: Return 6 as the LCA
    answer: '6'
solution:
  code: "# Definition for a binary tree node.\n# class TreeNode:\n#     def __init__(self, x):\n#         self.val = x\n#         self.left = None\n#         self.right = None\n\n\nclass Solution:\n    def lowestCommonAncestor(\n        self, root: \"TreeNode\", p: \"TreeNode\", q: \"TreeNode\"\n    ) -> \"TreeNode\":\n        while True:\n            if root.val < p.val and root.val < q.val:\n                root = root.right\n            elif root.val > p.val and root.val > q.val:\n                root = root.left\n            else:\n                return root\n"
  complexity:
    time: O(log n) average / O(n) worst case
    space: O(1)
  followup:
  - ko: 이것이 BST가 아닌 일반 이진 트리라면 어떻게 풀어야 할까요?
    en: How would you solve this if it were a general binary tree, not a BST?
  - ko: 재귀적 접근법으로 풀 수 있을까요? 반복식과 비교하면 어떤 장단점이 있을까요?
    en: Can you solve this recursively? What are the trade-offs versus iteration?
  - ko: 두 개가 아닌 k개의 노드의 LCA를 찾으려면 이 알고리즘을 어떻게 일반화할 수 있을까요?
    en: How would you generalize this to find the LCA of k nodes instead of just two?
```